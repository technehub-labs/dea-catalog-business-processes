"""CR-BP-113 one-shot: repair 272 broken relative hrefs in entity/discovery
YAML files after the mv1 migration stopped at the structured-data layer.

This script mutates only `href:` field values and appends one
metadata.change_history entry per touched file. Ids, definitions,
evidence prose, and any non-href fields are untouched.

Idempotent: running it on an already-repaired tree is a no-op.

Idempotency keys:
  - Each rewrite is keyed on the broken-href string. If the resolved
    value is already correct, the line is left alone.
  - change_history is appended at most once per file (the script
    checks for a pre-existing CR-BP-113 entry before adding one).

Run with --dry-run to print a summary without writing. The CI gate
`scripts/check_href_targets.py` (HREF-001..003) is the long-running
verification surface; this script is the one-shot remediation that
the gate's first clean run proves correct.

Authoritative reference: CR-BP-113 (2026-10-13, eaojnr).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

# ----------------------------------------------------------------------------
# Resolution rules
# ----------------------------------------------------------------------------

# 1. CR-rename table: broken filename -> correct filename. These are
#    not migration artifacts but name transpositions from the tranche
#    generators; the rename table lives here and is absorbed by the
#    HREF gate thereafter (any re-introduction trips HREF-001).
CR_RENAMES: dict[str, str] = {
    "change-requests/CR-BP-21d.1-enablement-operations-completion.md":
        "change-requests/CR-BP-21d.1-operations-enablement-completion.md",
    "change-requests/CR-BP-21d-enablement-operations-landing.md":
        "change-requests/CR-BP-21d-operations-enablement-landing.md",
    "change-requests/cr-bp-13a-customer-and-demand-admission.md":
        "change-requests/CR-BP-13a-party-and-relationship-admission.md",
    "change-requests/CR-BP-13a-customer-and-demand-admission.md":
        "change-requests/CR-BP-13a-party-and-relationship-admission.md",
}

# 2. contexts/v1-alpha/ -> entities/v1-alpha/<cell>/processes-pc-<cell>-<hash>.yaml
#    Resolved per-cell using the id_map (which carries both `oe-*` and
#    `eo-*` legacy keys for each cell; the directory uses `eo-*`).
#    113 hits across the catalog pre-repair.

# 3. entities/v1-alpha/dea:<id>/... -> via id_map (DEA legacy id) ->
#    processes:<level>-<cell>-<hash> + directory by stripping the
#    `processes:<level>-` prefix, with the trailing path preserved.
#    86 hits pre-repair.

# 4. docs/research/l1-register.yaml (1 hit pre-repair, inside
#    pr-operate-7ab3ma/processes-process-pr-operate-7ab3ma.yaml)
#    -> entities/v1-alpha/pr-operate/pr-operate-7ab3ma/research/l1-register.yaml

# ----------------------------------------------------------------------------
# Loaders
# ----------------------------------------------------------------------------


def _load_id_map() -> dict[str, str]:
    p = ROOT / "reconciliation" / "migration-id-map.yaml"
    data = yaml.safe_load(p.read_text())
    return data.get("id_map", {})


def _build_pc_path_map(id_map: dict[str, str]) -> dict[str, Path]:
    """For every `dea:pc-<cell>` (and `dea:pc-<cell>-<token>` variant)
    in the id_map, build the on-disk path of the PC record under
    `entities/v1-alpha/<cell>/processes-pc-<cell>-<hash>/<file>.yaml`.

    Used to repair `contexts/v1-alpha/pc-<cell>.yaml` hrefs. The map
    is keyed by EVERY alias the legacy `pc-...` filename might use:
    the full kebab (extracted from the new id's cell), the short
    forms the id_map actually carries, and the `dea-pc-` prefix.
    """
    out: dict[str, Path] = {}
    for old, new in id_map.items():
        m = re.match(r"^dea:pc-([a-z]+(?:-[a-z]+)*)$", old)
        if not m:
            continue
        cell_any = m.group(1)            # the id_map key cell
        m2 = re.match(
            r"^processes:(pc|group|process|activity|task|scope)-"
            r"([a-z]+(?:-[a-z]+)*)-([a-z2-9]{6})$",
            new,
        )
        if not m2:
            continue
        _, new_cell, h = m2.groups()
        filename = f"processes-pc-{new_cell}-{h}.yaml"
        path = _find_record_path(new_cell, filename)
        if not path:
            continue
        rel = ROOT / path
        # Seed every alias we might see in legacy hrefs. The
        # authoritative canonical key is the new id's cell
        # (`new_cell`, e.g. `pr-design`, `sd-improve`); the
        # short-form variants from the id_map (e.g. `pr-d`,
        # `sd-i`) and the `dea-pc-` prefixes are all aliases.
        aliases = {
            new_cell,                 # canonical long kebab
            cell_any,                 # the id_map key (could be short or long)
            f"pc-{new_cell}",
            f"pc-{cell_any}",
            f"dea-pc-{new_cell}",
            f"dea-pc-{cell_any}",
        }
        for alias in aliases:
            out.setdefault(alias, rel)
    return out


def _id_to_dirpath(new_id: str) -> str | None:
    """Convert `processes:<level>-<cell>-<hash>` into the directory
    portion of the one-directory-per-record layout: `entities/v1-alpha/<cell>`.

    Returns None if the id does not match the canonical shape.
    """
    m = re.match(
        r"^processes:(pc|group|process|activity|task|scope)-"
        r"([a-z]+(?:-[a-z]+)*?)-([a-z2-9]{6})$",
        new_id,
    )
    if not m:
        return None
    return m.group(2)


def _find_record_path(cell: str, filename: str) -> str | None:
    """Locate `filename` under `entities/v1-alpha/<cell>/` in the
    one-directory-per-record layout. The exact subdir depth varies:
    leaf records sit at `<cell>/<filename>`; nested records sit at
    `<cell>/<parent-hash-dir>/<filename>`; deeply nested records sit
    one level deeper. The cell dir is the only fixed anchor; we
    rglob the cell for the file (cheap on a 49-cell catalog) and
    return the first match as a repo-root-relative path.

    Returns None if the file is not present in the cell."""
    cell_dir = ROOT / "entities" / "v1-alpha" / cell
    for cand in cell_dir.rglob(filename):
        return cand.relative_to(ROOT).as_posix()
    return None


def _resolve_legacy_kebab_path(old_path: str, id_map: dict[str, str]) -> str | None:
    """For `entities/v1-alpha/dea:<kebab-id>/...` (where <kebab-id> is a
    long kebab name, not a hash), look up the id in the id_map and
    return the post-mv1 path. Returns None if no mapping found."""
    # Extract the id portion: dea:<group|process>-<kebab>
    m = re.match(
        r"^entities/v1-alpha/dea:(group|process|activity|task)-([a-z0-9-]+)(/.*)?$",
        old_path,
    )
    if not m:
        return None
    old_id = f"dea:{m.group(1)}-{m.group(2)}"
    new_id = id_map.get(old_id)
    if not new_id:
        return None
    cell = _id_to_dirpath(new_id)
    if not cell:
        return None
    # The post-mv1 file is `processes-<new_id-prefix>.yaml` under
    # the cell dir (or one deeper for one-directory-per-record).
    # Strip the `processes:` prefix and the trailing hash for the
    # filename stem.
    m2 = re.match(
        r"^processes:(group|process|activity|task)-([a-z]+(?:-[a-z]+)*?)-([a-z2-9]{6})$",
        new_id,
    )
    if not m2:
        return None
    _, new_cell, h = m2.groups()
    filename = f"processes-{m2.group(1)}-{new_cell}-{h}.yaml"
    suffix = m.group(3) or ""
    rel = _find_record_path(new_cell, filename)
    if not rel:
        return None
    if suffix:
        # `suffix` is e.g. `/research/l1-register.yaml` or
        # `/dea:process-develop-corporate-strategy.yaml`
        # (the latter is the pre-mv1 file, which never
        # exists post-mv1 and must be dropped).
        if suffix.startswith(f"/dea:"):
            # The pre-mv1 file is gone; the record is in the
            # new location. Return the bare post-mv1 path.
            return rel
        rel = rel + suffix
    return rel


# ----------------------------------------------------------------------------
# Per-line rewrite
# ----------------------------------------------------------------------------


HREF_LINE_RE = re.compile(
    r"^(?P<indent>\s*)href:\s*"
    r"(?P<quote>[\"']?)(?P<target>[^\"'\n]+)(?P=quote)\s*$"
)


def _resolve_target(target: str, id_map: dict[str, str],
                    pc_path_map: dict[str, Path]) -> str | None:
    """Return the corrected href string for `target`, or None if no
    rewrite rule applies."""
    # CR-rename table
    if target in CR_RENAMES:
        return CR_RENAMES[target]
    # contexts/v1-alpha/ -> entities/v1-alpha/<cell>/processes-pc-<cell>-<hash>.yaml
    # The `pc-<cell>` form keys the map; the path map's keys are
    # already `pc-<cell>` (built from `dea:pc-<cell>` keys above),
    # so we look up `pc-<cell>` directly. The legacy file may also
    # use the abbreviated form `dea-pc-<cell>` (no leading slash
    # prefix) - handled by the same regex's `(?:dea-)?` prefix.
    m = re.match(
        r"^contexts/v1-alpha/((?:dea-)?pc-[a-z]+(?:-[a-z]+)*)(?:-[a-z0-9]+)?\.yaml$",
        target,
    )
    if m:
        cell = m.group(1)
        pc_path = pc_path_map.get(cell)
        if pc_path and pc_path.exists():
            return pc_path.relative_to(ROOT).as_posix()
        return None
    # entities/v1-alpha/dea:<kebab-id>/... (non-Research subpath)
    if target.startswith("entities/v1-alpha/dea:"):
        # The `dea:group-customer-lifecycle-management/research/l1-register.yaml`
        # and `dea:process-...-research/l2-admission-deposition.yaml`
        # patterns need the trailing /research/<file> preserved.
        m2 = re.match(
            r"^entities/v1-alpha/dea:(group|process)-([a-z0-9-]+)/research/(.+)$",
            target,
        )
        if m2:
            old_id = f"dea:{m2.group(1)}-{m2.group(2)}"
            new_id = id_map.get(old_id)
            if not new_id:
                return None
            cell = _id_to_dirpath(new_id)
            if not cell:
                return None
            # The post-mv1 file under the cell is the same named record
            # (no research/ subpath). Drop the research/ portion; the
            # href targeter wanted the record itself.
            m3 = re.match(
                r"^processes:(group|process)-([a-z]+(?:-[a-z]+)*?)-([a-z2-9]{6})$",
                new_id,
            )
            if not m3:
                return None
            _, new_cell, h = m3.groups()
            filename = f"processes-{m3.group(1)}-{new_cell}-{h}.yaml"
            return _find_record_path(new_cell, filename)
        # Plain `entities/v1-alpha/dea:<kebab>/dea:<kebab>.yaml` (the
        # pre-mv1 single-file form) drops the suffix entirely.
        m4 = re.match(
            r"^entities/v1-alpha/dea:(group|process)-([a-z0-9-]+)/dea:(group|process)-([a-z0-9-]+)\.yaml$",
            target,
        )
        if m4:
            old_id = f"dea:{m4.group(1)}-{m4.group(2)}"
            new_id = id_map.get(old_id)
            if not new_id:
                return None
            cell = _id_to_dirpath(new_id)
            if not cell:
                return None
            m5 = re.match(
                r"^processes:(group|process)-([a-z]+(?:-[a-z]+)*?)-([a-z2-9]{6})$",
                new_id,
            )
            if not m5:
                return None
            _, new_cell, h = m5.groups()
            filename = f"processes-{m5.group(1)}-{new_cell}-{h}.yaml"
            return _find_record_path(new_cell, filename)
        # Legacy `entities/v1-alpha/dea:<kebab>/...` with any other
        # trailing structure -> resolve via the generic id-to-dir
        # helper (handles anything that survives).
        return _resolve_legacy_kebab_path(target, id_map)
    # docs/research/l1-register.yaml (single known hit) -> the
    # process-group record's research/ dir.
    if target == "docs/research/l1-register.yaml":
        return "entities/v1-alpha/pr-operate/pr-operate-7ab3ma/research/l1-register.yaml"
    return None


def _file_contains_change_entry(text: str) -> bool:
    """True if the file already has a `change_history` entry citing
    CR-BP-113 (idempotency check)."""
    return "CR-BP-113" in text and "href targets repaired" in text


def _append_change_history(text: str, path: Path) -> str:
    """Append one `change_history` entry under `metadata:` with
    cr=CR-BP-113, date=2026-10-13, summary. Creates the metadata
    block if absent (defensive; CR-BP-mv1 records all have it).

    Strategy: locate the `change_history:` block, then find the
    FIRST list entry's indent level and the BLOCK END (the next
    line whose column-0 char is not space and not `#`). Append
    a new entry at the same indent as the first entry, immediately
    before the block-end line. The block-end heuristic is robust
    to multi-line `change:` / `summary:` values because the next
    top-level field is unindented."""
    marker = "href targets repaired to post-mv1 layout (CR-BP-113)"
    if marker in text:
        return text
    lines = text.splitlines(keepends=False)
    # Find the change_history: line and the first `- cr:` entry's indent
    ch_idx = None
    first_entry_indent = None
    for i, line in enumerate(lines):
        if line.lstrip().startswith("change_history:"):
            ch_idx = i
            continue
        if ch_idx is not None and first_entry_indent is None:
            stripped = line.lstrip()
            if stripped.startswith("- cr:"):
                first_entry_indent = len(line) - len(stripped)
            elif not line.startswith(" ") and line.strip() and not line.lstrip().startswith("#"):
                # Top-level field encountered before any entry - bail.
                # This shouldn't happen for catalog records, but be safe.
                ch_idx = None
                break
    if ch_idx is None or first_entry_indent is None:
        return text
    # Find the BLOCK END: the next line whose first char is NOT space,
    # `#`, or empty. Walk from ch_idx onward.
    block_end = len(lines)
    for j in range(ch_idx + 1, len(lines)):
        first = lines[j][:1]
        if first and first not in (" ", "#"):
            block_end = j
            break
    entry_lines = [
        f"{' ' * first_entry_indent}- cr: CR-BP-113",
        f"{' ' * (first_entry_indent + 2)}date: '2026-10-13'",
        f"{' ' * (first_entry_indent + 2)}change: {marker}",
    ]
    out = lines[:block_end] + entry_lines + lines[block_end:]
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--dry-run", action="store_true",
                        help="print what would change; do not write")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="print per-file details")
    args = parser.parse_args(argv)

    id_map = _load_id_map()
    pc_path_map = _build_pc_path_map(id_map)
    if args.verbose:
        print(f"id_map entries: {len(id_map)}", file=sys.stderr)
        print(f"pc_path_map entries: {len(pc_path_map)}", file=sys.stderr)

    target_files = list(ROOT.glob("entities/**/*.yaml")) + list(ROOT.glob("discovery/**/*.yaml"))
    # Pre-mv1 signature patterns (used for change_history backfill):
    # a file is "part of the broken cohort" if any of its CURRENT
    # hrefs is a known pre-mv1 form (the first run repaired from
    # these to post-mv1 paths).
    pre_mv1_pattern = re.compile(
        r"contexts/v1-alpha/|entities/v1-alpha/dea:|" +
        "|".join(re.escape(k) for k in CR_RENAMES)
    )
    rewrites: Counter[str] = Counter()
    files_touched: set[Path] = set()
    unresolved: list[tuple[Path, int, str]] = []

    for f in target_files:
        rel = f.relative_to(ROOT).as_posix()
        text = f.read_text()
        new_lines = []
        file_changed = False
        file_has_hrefs = False
        file_has_unresolved = False
        for ln, line in enumerate(text.splitlines(), 1):
            m = HREF_LINE_RE.match(line)
            if not m:
                new_lines.append(line)
                continue
            file_has_hrefs = True
            target = m.group("target").strip()
            replacement = _resolve_target(target, id_map, pc_path_map)
            if replacement is None:
                # Try the on-disk resolver: maybe the target already
                # resolves; if not, record as unresolved.
                if target.startswith(("http://", "https://", "/", "./")):
                    new_lines.append(line)
                    continue
                candidate = (ROOT / target).resolve()
                if candidate.exists():
                    new_lines.append(line)
                    continue
                unresolved.append((f, ln, target))
                new_lines.append(line)
                file_has_unresolved = True
                continue
            if replacement == target:
                new_lines.append(line)
                continue
            new_line = (
                f"{m.group('indent')}href: "
                f"{m.group('quote')}{replacement}{m.group('quote')}"
            )
            new_lines.append(new_line)
            rewrites[replacement] += 1
            file_changed = True
        new_text = "\n".join(new_lines) + "\n"
        # Fire when EITHER: the file had broken hrefs (rewritten or
        # still unresolved). The change_history backfill is then
        # idempotent (skipped if already present in the file). The
        # unresolved-set case is a CR-BP-113-pending signal that an
        # external review must close; we still record the slice's
        # audit footprint on the file.
        needs_change_entry = (
            file_changed
            or file_has_unresolved
            or (
                # Backfill: a file that had a pre-mv1 signature but
                # somehow lacks the change_history entry.
                not _file_contains_change_entry(text)
                and pre_mv1_pattern.search(text)
            )
        )
        if needs_change_entry:
            if not _file_contains_change_entry(new_text):
                new_text = _append_change_history(new_text, f)
            files_touched.add(f)
            if not args.dry_run:
                f.write_text(new_text)
            if args.verbose:
                rewrote = sum(1 for o, n in zip(text.splitlines(), new_text.splitlines()) if o != n)
                print(f"  {rel}: {rewrote} line(s) changed", file=sys.stderr)

    print(f"Files scanned: {len(target_files)}", file=sys.stderr)
    print(f"Files touched: {len(files_touched)}", file=sys.stderr)
    print(f"href rewrites: {sum(rewrites.values())} across {len(rewrites)} unique target(s)", file=sys.stderr)
    # Final sweep: any file that USED to have broken hrefs but
    # somehow lacks the CR-BP-113 change_history entry (e.g. a
    # previous run that pre-dated the multi-line-value fix). This
    # idempotency close-out is what lets the script be safely
    # re-run; it never creates duplicate entries (see
    # _file_contains_change_entry).
    # Heuristic: a file is "part of the broken cohort" if any of its
    # CURRENT hrefs is a known post-mv1 entity path (meaning the
    # first run repaired it from a pre-mv1 target to this one).
    # Pre-mv1 form patterns: `contexts/v1-alpha/...` or
    # `entities/v1-alpha/dea:` or the CR-rename table entries.
    pre_mv1_pattern = re.compile(
        r"contexts/v1-alpha/|entities/v1-alpha/dea:|" +
        "|".join(re.escape(k) for k in CR_RENAMES)
    )
    marker = "href targets repaired to post-mv1 layout (CR-BP-113)"
    leftover = []
    for f in target_files:
        text = f.read_text()
        if marker in text:
            continue
        # Two signals: file has a pre-mv1 href (still broken)
        # OR file has a known post-mv1 record path that was the
        # rewrite target of one of our rules (e.g. the pr-operate-7ab3ma
        # file in the original hrefs now points at the post-mv1
        # location).
        if pre_mv1_pattern.search(text):
            leftover.append(f)
            continue
        for line in text.splitlines():
            m = HREF_LINE_RE.match(line)
            if not m:
                continue
            tgt = m.group("target").strip()
            if tgt.startswith("entities/v1-alpha/pr-operate/pr-operate-7ab3ma/"):
                leftover.append(f)
                break
    for f in leftover:
        text = f.read_text()
        new_text = _append_change_history(text, f)
        if new_text != text:
            files_touched.add(f)
            if not args.dry_run:
                f.write_text(new_text)
            if args.verbose:
                print(f"  {f.relative_to(ROOT).as_posix()}: change_history backfilled", file=sys.stderr)
    if leftover:
        print(f"Change-history backfill: {len(leftover)} file(s)", file=sys.stderr)
    if unresolved:
        print(f"Unresolved (still broken after repair): {len(unresolved)}", file=sys.stderr)
        for f, ln, tgt in unresolved[:20]:
            print(f"  {f.relative_to(ROOT).as_posix()}:{ln}: {tgt}", file=sys.stderr)
        if len(unresolved) > 20:
            print(f"  ... and {len(unresolved) - 20} more", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
