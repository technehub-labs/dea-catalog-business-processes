"""CR-BP-222 one-shot: sweep legacy dea:* id tokens out of narrative fields
in canonical entity YAML files (mv1 completion, prose layer).

This script mutates only current-state narrative string values:
definitions, descriptions, triggers, outcomes, scope text, input/output
descriptions, cell-charter text, composes rationales, and evidence
reference strings. `metadata.change_history` prose is deliberately
PRESERVED (historical attestation; landed history is immutable), as are
the two values registered in reconciliation/migration-id-map.yaml
known_residuals (their dispositions live in their own repair CRs).

Rewrites are token-for-token substitutions driven by the id_map — the
script never invents a mapping. An unmapped, unexcepted token outside
change_history is reported and left in place; the script exits 2 in
that case so the omission cannot pass silently.

Formatting is preserved exactly: edits are applied to the raw text
line-by-line (same discipline as repair_mv1_hrefs.py), so the diff is
token substitution only.

Idempotent: on an already-swept tree the report shows 0 rewrites and
nothing is written.

Run with --dry-run to print the report without writing. The CI gate
`scripts/check_id_system.py` rule IDM-009 is the long-running
verification surface; this script is the one-shot remediation that the
gate's first clean run proves correct.

Authoritative reference: CR-BP-222 (2026-11-02, eaojnr).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

LEGACY_TOKEN_RE = re.compile(r"\bdea:(?:pc|group|process|activity|task|scope)-[a-z0-9-]+")

# Per-case exceptions (CR-BP-222 §3). Exact raw-text replacements for
# tokens the general regex cannot map (source-string truncations).
# Each tuple: (file name suffix, exact old substring, new substring).
EXCEPTIONS: list[tuple[str, str, str]] = [
    (
        "processes-process-fa-retire-wkbrsa.yaml",
        "within the dea:pc-fa-re'",
        "within the processes:pc-fa-retire-64q5p9'",
    ),
]


def _load_id_map() -> dict[str, str]:
    map_path = ROOT / "reconciliation" / "migration-id-map.yaml"
    data = yaml.safe_load(map_path.read_text()) or {}
    return data.get("id_map", {}) or {}


def _residual_tokens() -> set[str]:
    """Legacy tokens registered in known_residuals (preserved by policy)."""
    map_path = ROOT / "reconciliation" / "migration-id-map.yaml"
    data = yaml.safe_load(map_path.read_text()) or {}
    tokens: set[str] = set()
    for r in data.get("known_residuals", []) or []:
        legacy = r.get("legacy_value")
        if isinstance(legacy, str):
            tokens.update(LEGACY_TOKEN_RE.findall(legacy))
    return tokens


def _iter_submittable_lines(text: str):
    """Yield (index, line) for lines eligible for substitution.

    Skips metadata.change_history subtrees: from a `change_history:`
    key line until the next non-blank, non-sequence-item line at
    indent <= the key's indent. Block-sequence entries under the key
    (`- cr: ...`) sit at the SAME indent as the key, so a same-indent
    `- ` line is still inside the subtree.
    """
    skipping_until_indent: int | None = None
    for i, line in enumerate(text.splitlines(keepends=True)):
        stripped = line.strip()
        indent = len(line) - len(line.lstrip(" "))
        if skipping_until_indent is not None:
            if stripped == "":
                continue
            if indent > skipping_until_indent:
                continue
            if indent == skipping_until_indent and stripped.startswith("- "):
                continue  # sequence entry under the skipped key
            skipping_until_indent = None  # sibling key: subtree ended
        m = re.match(r"^(\s*)change_history:", line)
        if m:
            skipping_until_indent = len(m.group(1))
            continue
        yield i, line


def repair_file(path: Path, id_map: dict[str, str], residuals: set[str],
                dry_run: bool) -> tuple[int, int, int, Counter]:
    """Return (rewrites, preserved, left_unmapped, per-token counter).

    `preserved` counts tokens intentionally kept (registered residuals);
    `left_unmapped` counts tokens with no disposition — these fail the run.
    """
    text = path.read_text()
    rewrites = 0
    preserved = 0
    left: Counter = Counter()

    # 1. Per-case exceptions (exact raw-text replacements, applied first).
    for suffix, old, new in EXCEPTIONS:
        if path.name.endswith(suffix) and old in text:
            text = text.replace(old, new)
            rewrites += 1

    # 2. General token substitution on eligible lines.
    lines = text.splitlines(keepends=True)
    eligible = {i for i, _ in _iter_submittable_lines(text)}
    for i, line in enumerate(lines):
        if i not in eligible:
            continue
        if not LEGACY_TOKEN_RE.search(line):
            continue

        def _sub(m: re.Match) -> str:
            nonlocal rewrites, preserved
            token = m.group(0)
            new = id_map.get(token)
            if token in residuals:
                preserved += 1
                return token
            if new is None:
                left[token] += 1
                return token
            rewrites += 1
            return new

        new_line = LEGACY_TOKEN_RE.sub(_sub, line)
        if new_line != line:
            lines[i] = new_line

    new_text = "".join(lines)
    if rewrites and not dry_run and new_text != path.read_text():
        path.write_text(new_text)
    return rewrites, preserved, sum(left.values()), left


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("--dry-run", action="store_true",
                        help="Report without writing files.")
    args = parser.parse_args(argv)

    id_map = _load_id_map()
    residuals = _residual_tokens()

    files = sorted(
        p for p in (ROOT / "entities" / "v1-alpha").rglob("*.yaml")
        if not any(s in p.parts for s in ("research", "candidates", "retired"))
    )

    total_rewrites = 0
    total_left = 0
    total_preserved = 0
    files_touched = 0
    left_overall: Counter = Counter()
    for p in files:
        rewrites, preserved, n_left, left = repair_file(
            p, id_map, residuals, args.dry_run)
        if rewrites:
            files_touched += 1
            total_rewrites += rewrites
        total_preserved += preserved
        if n_left:
            total_left += n_left
            left_overall.update(left)

    mode = "DRY-RUN " if args.dry_run else ""
    print(f"{mode}repair_narrative_ids: files_touched={files_touched} "
          f"rewrites={total_rewrites} preserved_residuals={total_preserved} "
          f"left_unmapped={total_left}")
    for token, n in left_overall.most_common(20):
        print(f"  LEFT {n:4d}  {token}")
    if total_left:
        print("ERROR: unmapped legacy tokens remain outside change_history / "
              "known_residuals; add an explicit CR exception or id_map entry "
              "before landing.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
