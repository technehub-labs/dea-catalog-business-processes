"""CR-BP-113: change-requests/README.md Consistency Gate (CRR-001..003)

The hand-maintained CR index table in change-requests/README.md is
the canonical discoverability surface for the catalog's governance
chain. Three rules keep it clean:

  CRR-001  (blocking).  Every CR link in every markdown table row in
                          change-requests/README.md resolves on disk.
  CRR-002  (blocking).  No duplicate CR link appears in the same
                          table (a paste corruption that historically
                          accumulated 148 copies of CR-BP-90 in one
                          paste session).
  CRR-003  (blocking).  Every CR file under change-requests/ has
                          exactly one row in the in-repo table
                          (the Cross-repo context section is exempt:
                          those are sibling-repo CRs that may or may
                          not have a row).

The table stays hand-maintained (no generator) because the per-row
summaries are editorial. The gate turns paste corruption into a CI
failure so the next migration / paste session cannot re-introduce
the same drift.

Authoritative reference: CR-BP-113 (2026-10-13, eaojnr).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "change-requests" / "README.md"
CR_DIR = ROOT / "change-requests"

# Markdown link to a CR file: [CR-BP-...](CR-BP-...md) - capture both.
CR_LINK_RE = re.compile(
    r"\[(?P<label>CR-[A-Z]+-[A-Za-z0-9._-]+)\]"
    r"\((?P<target>CR-[A-Za-z0-9._-]+\.md)\)"
)
TABLE_ROW_RE = re.compile(r"^\|\s*\[CR-[A-Z]+-[A-Za-z0-9._-]+\]")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _iter_table_rows(text: str, in_cross_repo: bool) -> list[tuple[int, str]]:
    """Yield (line_number, line) for each markdown table row, but
    skip rows in the `## Cross-repo context` section (those are
    sibling-repo CRs and are NOT subject to the in-repo uniqueness
    rule CRR-003, only to CRR-001/002 link resolution)."""
    rows = []
    for ln, line in enumerate(text.splitlines(), 1):
        if TABLE_ROW_RE.match(line):
            rows.append((ln, line))
    return rows


def _section_for_line(text: str, line_number: int) -> str:
    """Return the H2 section the given line lives under."""
    current = ""
    for ln, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            current = line[3:].strip()
        if ln == line_number:
            return current
    return current


# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------


def evaluate(allowlist_sealed: tuple[str, ...] = ()) -> tuple[
    list[tuple[str, str]], list[tuple[str, str]]
]:
    blocking: list[tuple[str, str]] = []
    advisory: list[tuple[str, str]] = []

    if not README.exists():
        blocking.append(("CRR-001", f"README does not exist: {README}"))
        return blocking, advisory

    text = README.read_text()
    rows = _iter_table_rows(text, in_cross_repo=False)

    # CRR-001: every CR link in every row resolves on disk.
    for ln, line in rows:
        for m in CR_LINK_RE.finditer(line):
            target = m.group("target")
            if not (CR_DIR / target).exists():
                blocking.append((
                    "CRR-001",
                    f"README.md:{ln}: CR link target missing on disk: {target}",
                ))

    # CRR-002: no duplicate CR link in the SAME table. The CR's
    # intent is in-repo uniqueness (the in-repo table indexes
    # canonical CR files; a row repeated in the same table is a
    # paste corruption). The cross-repo table legitimately repeats
    # sibling-repo CRs once per narrative anchor (e.g. CG-001 lands
    # in `dea-metaframework`; CR-BP-90 row follows), so cross-repo
    # duplicates are exempt.
    tables: list[tuple[int, list[tuple[int, str]], bool]] = []
    cur_start = None
    cur_rows: list[tuple[int, str]] = []
    in_table = False
    in_cross_repo_table = False
    for ln, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            in_cross_repo_table = "Cross-repo" in line
            in_table = False
            continue
        if TABLE_ROW_RE.match(line):
            if not in_table:
                cur_start = ln
                cur_rows = []
                in_table = True
            cur_rows.append((ln, line))
        else:
            if in_table:
                # End of table: blank line, H2, or narrative line
                if not line.strip() or line.startswith("## "):
                    tables.append((cur_start, cur_rows, in_cross_repo_table))
                    in_table = False
    if in_table:
        tables.append((cur_start, cur_rows, in_cross_repo_table))

    for start, table_rows, in_cross_repo in tables:
        if in_cross_repo:
            # Cross-repo table allows duplicates (one per narrative anchor).
            continue
        labels = []
        for ln, line in table_rows:
            for m in CR_LINK_RE.finditer(line):
                labels.append((ln, m.group("label")))
        c = Counter(lbl for _, lbl in labels)
        for lbl, n in c.items():
            if n > 1:
                offending = [ln for ln, lb in labels if lb == lbl]
                blocking.append((
                    "CRR-002",
                    f"README.md: duplicate CR link '{lbl}' "
                    f"({n} times in in-repo table starting at line {start}): "
                    f"lines {offending}",
                ))

    # CRR-003: every CR file under change-requests/ has exactly one
    # row in the in-repo table (the first table, before the
    # `## Cross-repo context` section).
    in_repo_table: list[tuple[int, str]] = []
    in_cross_repo = False
    for ln, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            in_cross_repo = "Cross-repo" in line
            continue
        if TABLE_ROW_RE.match(line) and not in_cross_repo:
            in_repo_table.append((ln, line))
    in_repo_files = set()
    for ln, line in in_repo_table:
        for m in CR_LINK_RE.finditer(line):
            in_repo_files.add(m.group("target"))
    on_disk = {p.name for p in CR_DIR.glob("CR-*.md")}
    missing = on_disk - in_repo_files
    if missing:
        for m in sorted(missing):
            blocking.append((
                "CRR-003",
                f"README.md: CR file present on disk but missing from "
                f"in-repo table: {m}",
            ))

    return blocking, advisory


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _verdict(blocking: list, advisory: list) -> str:
    if blocking:
        return "NON-CONFORMANT"
    if advisory:
        return "CONFORMANT-WITH-WARNINGS"
    return "CONFORMANT"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    blocking, advisory = evaluate()
    verdict = _verdict(blocking, advisory)

    if args.json:
        import json
        print(json.dumps({
            "verdict": verdict,
            "blocking": [{"rule": r, "message": m} for r, m in blocking],
            "advisory": [{"rule": r, "message": m} for r, m in advisory],
        }, indent=2))
    else:
        print(f"CR README Consistency (CR-BP-113; CRR-001..003): {verdict}")
        print(f"  {len(blocking)} blocking finding(s); {len(advisory)} advisory.")
        for rule, msg in blocking[:20]:
            print(f"    [{rule}] {msg}")
        if len(blocking) > 20:
            print(f"    ... and {len(blocking) - 20} more")
    if args.strict and blocking:
        return 1
    return 0


def _self_test() -> int:
    """Exercise CRR-001..003 on hand-rolled fixtures. Returns 0 on
    PASS, non-zero on FAIL."""
    import tempfile
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        cr_dir = tmp_root / "change-requests"
        cr_dir.mkdir(parents=True)
        # Create one CR file that exists
        (cr_dir / "CR-BP-1-ok.md").write_text("# CR-BP-1\n")
        # Build a README with: valid row, duplicate row, missing link
        readme = cr_dir / "README.md"
        readme.write_text(
            "## In this repo\n"
            "| [CR-BP-1](CR-BP-1-ok.md) | Title | Status | Notes |\n"
            "| [CR-BP-1](CR-BP-1-ok.md) | Title | Status | Notes |\n"
            "| [CR-BP-2](CR-BP-2-missing.md) | Title | Status | Notes |\n"
        )
        # Monkey-patch the module-level constants
        global README, CR_DIR
        original_readme, original_cr_dir = README, CR_DIR
        README, CR_DIR = readme, cr_dir
        try:
            blocking, _ = evaluate()
        finally:
            README, CR_DIR = original_readme, original_cr_dir
        if not any(r == "CRR-001" and "CR-BP-2-missing.md" in m for r, m in blocking):
            failures.append("CRR-001: did not flag missing CR target")
        if not any(r == "CRR-002" and "CR-BP-1" in m for r, m in blocking):
            failures.append("CRR-002: did not flag duplicate CR link")
        if any(r == "CRR-003" and "missing" in m for r, m in blocking):
            failures.append("CRR-003: false positive (no orphan CR on disk)")
        # Add a fixture where a CR file is on disk but absent from
        # the table, to assert CRR-003 fires.
        (cr_dir / "CR-BP-99-orphan.md").write_text("# CR-BP-99 orphan\n")
        # Re-run with the orphan
        README, CR_DIR = readme, cr_dir
        try:
            blocking2, _ = evaluate()
        finally:
            README, CR_DIR = original_readme, original_cr_dir
        if not any(r == "CRR-003" and "CR-BP-99-orphan.md" in m
                   for r, m in blocking2):
            failures.append("CRR-003: did not flag orphan CR file")
    if failures:
        print("self-test FAIL:")
        for f in failures:
            print(f"  {f}")
        return 2
    print("self-test PASS: 3 cases (CRR-001/002/003)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
