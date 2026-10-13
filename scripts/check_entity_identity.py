"""check_entity_identity.py - Entity-Identity Clarity Gate (CR-BP-117a; EID-001..004).

Rules
-----
EID-001 (advisory). A record's `name` does not appear under any other
    id at the *same* level (L0/L1/L2/L3/L4). A name that appears at
    multiple *different* levels is allowed (it is the containment tree
    speaking: the cell *and* the group inside the cell can share a
    parallel name; the relationship is "this group operates this
    cell"). Same-level identity collisions are real defects: two
    records at the same level claiming the same name confuse the
    user about which one they're reading.

EID-002 (advisory). Every record's README references the canonical
    id token in its first line. Removes the cross-record id collision
    risk at the user-facing surface (the readme's title and the
    record's `name` are not the same field; both should be present).

EID-003 (advisory). The README body surfaces the level token
    explicitly (e.g. "required at the L2 level"). Removes the
    level-collision ambiguity at a glance. CR-BP-117c will add an
    explicit Path section; EID-003 in this slice is the lower-bar
    body check.

EID-004 (advisory, informational). Cross-level name reuse is the
    containment tree speaking. Reported as an inventory entry so
    users see the level-collision surface at a glance. Not a defect;
    CR-BP-117c will add the level token to the README header for
    at-a-glance disambiguation.

CLI: --strict (advisory findings fail), --json, --self-test.
Exit 0 conformant / 1 non-conformant / 2 usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]

# Level token -> (level number, expected entity type)
LEVEL_TOKENS: dict[str, tuple[int, str]] = {
    "pc": (0, "ProcessContext"),
    "group": (1, "ProcessGroup"),
    "process": (2, "Process"),
    "activity": (3, "Activity"),
    "task": (4, "Task"),
    "scope": (0, "ProcessScope"),
}

_ID_RE = re.compile(
    r"^processes:(pc|group|process|activity|task|scope)-([a-z0-9]+)-([a-z0-9]+)-([a-z0-9]+)$"
)


def _id_level(token: str) -> int:
    return LEVEL_TOKENS[token][0]


def _entity_path(root: Path) -> Path:
    return root / "entities" / "v1-alpha"


def _iter_records(root: Path) -> Iterable[tuple[str, dict, Path]]:
    """Yield (id, dict, path) for every canonical record under entities/."""
    for p in sorted(_entity_path(root).rglob("*.yaml")):
        try:
            d = yaml.safe_load(p.read_text())
        except (OSError, yaml.YAMLError):
            continue
        if not isinstance(d, dict):
            continue
        rid = d.get("id")
        if not isinstance(rid, str):
            continue
        yield rid, d, p


def _level_of(rid: str) -> int | None:
    m = _ID_RE.match(rid)
    if not m:
        return None
    return _id_level(m.group(1))


def _level_name(rid: str) -> str:
    """User-friendly level name (e.g. 'L0 ProcessContext', 'L2 Process')."""
    m = _ID_RE.match(rid)
    if not m:
        return "L?"
    tok = m.group(1)
    num, name = LEVEL_TOKENS.get(tok, (0, "Record"))
    return f"L{num} {name}"


def _is_orphan_readme(p: Path) -> bool:
    """A README that is not the cell-root template and not in research/."""
    if p.name != "README.md":
        return False
    if "/research/" in p.as_posix():
        return False
    return True


def evaluate(root: Path | None = None) -> tuple[list, list]:
    """Return (blocking, advisory) findings as (rule, message) pairs."""
    if root is None:
        root = REPO_ROOT
    blocking: list[tuple[str, str]] = []
    advisory: list[tuple[str, str]] = []

    # Inventory: id -> {level, name, type, path}
    inventory: dict[str, dict] = {}
    for rid, d, p in _iter_records(root):
        lvl = _level_of(rid)
        if lvl is None:
            continue
        inventory[rid] = {
            "level": lvl,
            "name": d.get("name"),
            "type": d.get("type"),
            "path": p,
        }

    # EID-001: same-level identity collisions.
    by_name_level: dict[tuple[str, int], list[str]] = defaultdict(list)
    for rid, info in inventory.items():
        if info["name"]:
            by_name_level[(info["name"], info["level"])].append(rid)
    for (name, level), rids in by_name_level.items():
        if len(rids) > 1:
            blocking.append((
                "EID-001",
                f"same-level identity collision: name={name!r} level=L{level} "
                f"appears under {len(rids)} ids: {', '.join(sorted(rids)[:5])}"
                + (f" (+{len(rids) - 5} more)" if len(rids) > 5 else ""),
            ))

    # EID-002: README surfaces the level token in the displayed name.
    # The generator's existing format includes "# L0 ProcessContext -- <id>"
    # already; this finding checks the README's first line is the modern
    # header, not a stale pre-mv1 one.
    for rid, info in inventory.items():
        rel = info["path"].relative_to(root)
        readme = info["path"].parent / "README.md"
        if not readme.exists():
            continue
        try:
            text = readme.read_text()
        except OSError:
            continue
        first = text.splitlines()[0] if text else ""
        # Modern generator output: "# Canonical <Type>: `<id>`"
        # The level token is in the body ("required at the L<n> level").
        expected_id_token = f"`{rid}`"
        if expected_id_token not in first:
            advisory.append((
                "EID-002",
                f"{readme.relative_to(root)}: first line does not reference "
                f"the canonical id {expected_id_token!r}; got {first!r}",
            ))

    # EID-003: README body surfaces the level token explicitly. The
    # generator output for L1/L2/L3/L4 records includes "required at the
    # L<n> level" in the first body paragraph; L0 cells reference the
    # L0 cell name. This rule is the "is the user told what level
    # they're reading" check. CR-BP-117c will add an explicit Path
    # section; EID-003 in this slice is the lower-bar body check.
    for rid, info in inventory.items():
        readme = info["path"].parent / "README.md"
        if not readme.exists():
            continue
        try:
            text = readme.read_text()
        except OSError:
            continue
        lvl = info["level"]
        level_phrase_options = [
            f"L{lvl} ", f" L{lvl} ", f"L{lvl}\n", f" L{lvl}\n",
        ]
        if not any(opt in text for opt in level_phrase_options):
            advisory.append((
                "EID-003",
                f"{readme.relative_to(root)}: README body does not surface "
                f"the level token 'L{lvl}'; navigation context is implicit",
            ))

    # EID-004 (advisory, informational). Cross-level name reuse is the
    # containment tree speaking: a name at L0 and a different name at
    # L1 within the same cell is the *expected* relationship
    # (group operates cell). This is not a defect; it is reported as
    # an inventory entry for users who want to disambiguate by level
    # at a glance. CR-BP-117c will add the level token to the README
    # header for at-a-glance disambiguation.
    cross_level: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for rid, info in inventory.items():
        if info["name"]:
            cross_level[info["name"]].append((info["level"], rid))
    for name, occurrences in cross_level.items():
        levels = sorted({lvl for lvl, _ in occurrences})
        if len(levels) > 1:
            preview = ", ".join(f"L{lvl}({rid})" for lvl, rid in occurrences[:3])
            advisory.append((
                "EID-004",
                f"cross-level name {name!r} appears at L{levels[0]}..L{levels[-1]}: "
                f"{preview}" + (
                    f" (+{len(occurrences) - 3} more)" if len(occurrences) > 3 else ""
                ),
            ))

    return blocking, advisory


def _verdict(blocking: list, advisory: list) -> str:
    if blocking:
        return "NON-CONFORMANT"
    # EID-004 is informational, not a defect; --strict still passes.
    if advisory:
        return "CONFORMANT-WITH-WARNINGS"
    return "CONFORMANT"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--strict", action="store_true",
                        help="Advisory findings also fail the gate.")
    parser.add_argument("--json", action="store_true", help="JSON output.")
    parser.add_argument("--self-test", action="store_true",
                        help="Run fixture-based self-test and exit.")
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    blocking, advisory = evaluate()
    verdict = _verdict(blocking, advisory)

    if args.json:
        print(json.dumps({
            "gate": "EID-001..004",
            "verdict": verdict,
            "blocking": [{"rule": r, "message": m} for r, m in blocking],
            "advisory": [{"rule": r, "message": m} for r, m in advisory],
        }, indent=2))
    else:
        print(f"Entity Identity Clarity (CR-BP-117a; EID-001..004): {verdict}")
        print(f"  {len(blocking)} blocking finding(s); {len(advisory)} advisory.")
        for r, m in blocking[:25]:
            print(f"    [BLOCKING] [{r}] {m}")
        for r, m in advisory[:10]:
            print(f"    [{r}] {m}")
        if len(blocking) > 25:
            print(f"    ... and {len(blocking) - 25} more blocking")
        if len(advisory) > 10:
            print(f"    ... and {len(advisory) - 10} more advisory")

    if blocking:
        return 1
    if advisory and args.strict and _has_defect_advisory(blocking, advisory):
        return 1
    return 0


def _has_defect_advisory(blocking: list, advisory: list) -> bool:
    """EID-004 is informational; treat it as non-defect under --strict."""
    for r, _ in advisory:
        if r != "EID-004":
            return True
    return False


def _self_test() -> int:
    """Fixture-based self-test."""
    import tempfile
    failures: list[str] = []

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        cell = root / "entities" / "v1-alpha" / "pr-operate"
        cell.mkdir(parents=True)

        # Case 1: two records at the same level with the same name -> EID-001 blocking.
        rec_a = cell / "rec-a"
        rec_a.mkdir()
        (rec_a / "processes-process-pr-operate-recaaaaa.yaml").write_text(
            "id: processes:process-pr-operate-recaaaaa\n"
            "name: Demand Operate\n"
            "type: Process\n"
            "version: 1.0.0\n"
        )
        rec_b = cell / "rec-b"
        rec_b.mkdir()
        (rec_b / "processes-process-pr-operate-recbbbbb.yaml").write_text(
            "id: processes:process-pr-operate-recbbbbb\n"
            "name: Demand Operate\n"
            "type: Process\n"
            "version: 1.0.0\n"
        )

        blocking, _ = evaluate(root)
        if not any(r == "EID-001" and "Demand Operate" in m for r, m in blocking):
            failures.append("case1: same-level name collision did not fire EID-001")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        cell = root / "entities" / "v1-alpha" / "pr-operate"
        cell.mkdir(parents=True)

        # Case 2: same name at different levels -> allowed (not EID-001).
        pc = cell / "pr-operate-aaaaaa"
        pc.mkdir()
        (pc / "processes-pc-pr-operate-aaaaaa.yaml").write_text(
            "id: processes:pc-pr-operate-aaaaaa\n"
            "name: Demand Operate\n"
            "type: ProcessContext\n"
        )
        grp = cell / "pr-operate-bbbbbb"
        grp.mkdir()
        (grp / "processes-group-pr-operate-bbbbbb.yaml").write_text(
            "id: processes:group-pr-operate-bbbbbb\n"
            "name: Demand Operate\n"
            "type: ProcessGroup\n"
        )
        blocking, _ = evaluate(root)
        if any(r == "EID-001" for r, _ in blocking):
            failures.append("case2: cross-level same-name fired EID-001 (should not)")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        cell = root / "entities" / "v1-alpha" / "pr-operate"
        cell.mkdir(parents=True)
        rec = cell / "pr-operate-aaaaaa"
        rec.mkdir()
        (rec / "processes-process-pr-operate-aaaaaaa.yaml").write_text(
            "id: processes:process-pr-operate-aaaaaa\n"
            "name: Demand Operate\n"
            "type: Process\n"
            "version: 1.0.0\n"
        )
        # Stale README with no level token in the header.
        (rec / "README.md").write_text("# Demand Operate\n")
        _, advisory = evaluate(root)
        if not any(r == "EID-002" for r, _ in advisory):
            failures.append("case3: stale README did not fire EID-002")

    if failures:
        print("self-test FAIL:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("self-test PASS: 3 cases (EID-001 same-level, cross-level allow, EID-002 stale)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
