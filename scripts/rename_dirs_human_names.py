"""rename_dirs_human_names.py  -  CR-BP-117c C-1: level-named intermediate dirs.

Renames every record directory below the cell root from the opaque
`<cell>-<hash>` form to the record's kebab-cased display name:

    fa-retire/fa-retire-2ptdnw/fa-retire-wkbrsa/...
    ->
    fa-retire/Conclude-Regulated-Run-Off/Wind-Down-Liabilities/...

Rules
-----
- Only directories that directly contain a `processes-*.yaml` record are
  renamed; the cell directory (`fa-retire/`) is untouched, and the PC
  record lives at the cell root so it has no intermediate dir.
- Transform: `re.sub(r'[^A-Za-z0-9]+', '-', name).strip('-')`  -  keeps
  capitalization, collapses runs of unsafe characters (spaces, commas,
  slashes, parens) into single hyphens.
- Collision fallback: if two sibling dirs would map to the same name
  (impossible today per EID-001 live = 0, but defensive), the loser gets
  a `-<hash>` suffix from its id.
- Order: deepest dirs first (bottom-up) so a parent rename never
  invalidates a child path already processed.
- Uses `git mv` so history is preserved.

Gate safety (verified 2026-10-13):
- IDM-005 checks filename + cell segment + depth only  -  intermediate dir
  names are unconstrained.
- READMEs embed no dir paths (verified by grep over the live tree).
- CATALOG.yaml holds paths and is regenerated after the rename.

CLI: --dry-run (default; prints mapping + collisions), --apply (git mv).
Exit 0 success / 1 collision-without-fallback or git error / 2 usage.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
ENTITIES = REPO_ROOT / "entities" / "v1-alpha"

# Matches the IDM-001 canonical form: level-domain-stage-(slug)*-hash.
# Tasks and activities carry an extra slug segment (e.g.
# processes:task-fa-retire-intake-g9cskr); groups/processes do not.
_ID_RE = re.compile(
    r"^processes:(pc|group|process|activity|task|scope)-[a-z0-9-]+-([a-z2-9]{6})$"
)


def kebab(name: str) -> str:
    """Record display name -> dir name. Keeps capitalization."""
    return re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-")


def iter_record_dirs() -> list[tuple[Path, str, str, int]]:
    """Yield (dir, record_id, kebab_name, depth_below_cell) for dirs
    holding a record yaml, excluding cell-root PC records (depth 0)."""
    out = []
    for yml in sorted(ENTITIES.rglob("processes-*.yaml")):
        try:
            d = yaml.safe_load(yml.read_text())
        except (OSError, yaml.YAMLError):
            continue
        if not isinstance(d, dict):
            continue
        rid = d.get("id")
        name = d.get("name")
        if not isinstance(rid, str) or not isinstance(name, str):
            continue
        m = _ID_RE.match(rid)
        if not m or m.group(1) in ("pc", "scope"):
            continue  # PC/scope records live at the cell root; no dir rename
        rel = yml.parent.relative_to(ENTITIES)
        depth_below_cell = len(rel.parts) - 1  # 1 = group dir, 4 = task dir
        if depth_below_cell < 1:
            continue
        out.append((yml.parent, rid, kebab(name), depth_below_cell))
    return out


def build_plan() -> tuple[list[tuple[Path, Path]], list[str]]:
    """Return (renames, problems). renames are (old_dir, new_dir) pairs
    ordered deepest-first."""
    entries = iter_record_dirs()
    # collision detection within each parent dir
    by_parent: dict[Path, list[tuple[Path, str, str, int]]] = defaultdict(list)
    for e in entries:
        by_parent[e[0].parent].append(e)

    renames: list[tuple[Path, Path]] = []
    problems: list[str] = []
    for parent, kids in by_parent.items():
        seen: dict[str, list[tuple[Path, str]]] = defaultdict(list)
        for d, rid, kname, _ in kids:
            seen[kname].append((d, rid))
        for kname, holders in seen.items():
            if len(holders) == 1:
                d, rid = holders[0]
                if d.name != kname:
                    renames.append((d, d.parent / kname))
            else:
                # hash-suffix fallback (defensive; EID-001 says unreachable)
                for d, rid in holders:
                    suffix = rid.rsplit("-", 1)[-1]
                    new = d.parent / f"{kname}-{suffix}"
                    renames.append((d, new))
                    problems.append(
                        f"collision fallback: {kname} x {len(holders)} in {parent}"
                    )
    # deepest first
    renames.sort(key=lambda t: len(t[0].parts), reverse=True)
    return renames, problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--apply", action="store_true",
                    help="Perform the renames via git mv (default is dry-run).")
    args = ap.parse_args(argv)

    renames, problems = build_plan()
    already_named = sum(1 for d, _, k, _ in iter_record_dirs() if d.name == k)
    print(f"records with renamable dirs: {len(renames) + already_named}")
    print(f"already human-named: {already_named}")
    print(f"to rename: {len(renames)}")
    if problems:
        print(f"collision fallbacks applied: {len(problems)}")
        for p in problems[:10]:
            print(f"  {p}")

    if not args.apply:
        print("\ndry-run; first 15 renames:")
        for old, new in renames[:15]:
            print(f"  {old.relative_to(REPO_ROOT)} -> {new.name}")
        if len(renames) > 15:
            print(f"  ... and {len(renames) - 15} more")
        return 0

    failures = 0
    for old, new in renames:
        if new.exists():
            print(f"SKIP (target exists): {new.relative_to(REPO_ROOT)}")
            failures += 1
            continue
        r = subprocess.run(
            ["git", "mv", str(old.relative_to(REPO_ROOT)),
             str(new.relative_to(REPO_ROOT))],
            cwd=str(REPO_ROOT), capture_output=True, text=True,
        )
        if r.returncode != 0:
            print(f"FAIL git mv {old} -> {new}: {r.stderr.strip()}")
            failures += 1
    print(f"\napplied: {len(renames) - failures} / {len(renames)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
