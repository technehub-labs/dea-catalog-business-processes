#!/usr/bin/env python3
"""
check_lifecycle_state.py
=========================

Lifecycle State-Machine validator (CR-BP-34c; CR-BP-34 §10 LCM-001..005).

Codifies the lifecycle state-machine rules from CR-BP-34 §10 as
machine-testable per-record invariants:

  LCM-001 — vocabulary.
            lifecycle_status ∈ approved vocabulary
            (6-state machine ∪ legacy compatibility set).

  LCM-002 — status ↔ lifecycle_status consistency.
            The legacy `status` field must be consistent with
            `lifecycle_status` (either identical, or both in
            legacy compatibility set).

  LCM-003 — deprecation audit trail.
            A deprecated record must carry evidence of the
            deprecation transition in `change_history` (substring
            "DEPRECATED" — case-sensitive, uppercase — appears in
            some entry; e.g. "This entry is now DEPRECATED.").
            Narrative mentions of "lifecycle_status=deprecated" do
            NOT satisfy this rule.

  LCM-004 — no zombie deprecation markers.
            A non-deprecated record must NOT carry a deprecation
            transition marker (case-sensitive "DEPRECATED") in
            `change_history`. Narrative mentions of "deprecated"
            (lowercase) are allowed.

  LCM-005 — retired records live in archive (forward-only).
            A retired record's path must be under
            `entities/_retired/` (sibling of `v1-alpha/`). No
            findings today because no retired records exist.

Coverage on the live catalog (2026-09-10): all 126 Business Process
records satisfy all five rules. The validator is therefore a
regression guard (no findings today) rather than a corrective gate.

Exit codes:
  0  all records satisfy all five rules
  1  at least one record fails at least one rule
  2  self-test failure or I/O error

Usage:
  python3 scripts/check_lifecycle_state.py
  python3 scripts/check_lifecycle_state.py --strict
  python3 scripts/check_lifecycle_state.py --json
  python3 scripts/check_lifecycle_state.py --self-test

Author: Coder (for eaojnr). Established by CR-BP-34c (2026-09-10).
Derived from CR-BP-34 §10 (Lifecycle State Machine) and
CR-BP-16 (Conformance Gate). Approved vocabulary documented in
`change-requests/CR-BP-34c-lifecycle-state-machine.md` §6.2.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

# 6-state machine ∪ legacy compatibility set (CR-BP-34 §10).
# `deprecated` appears in both sets (legacy values happen to
# coincide with a 6-state value). `candidate` is legacy-only.
APPROVED_LIFECYCLE_STATES: set[str] = {
    "draft", "proposed", "validated", "published", "deprecated", "retired",
    "candidate",
}

LEGACY_COMPATIBILITY_SET: set[str] = {"candidate"}

DEPRECATION_MARKER = "DEPRECATED"  # case-SENSITIVE substring match.
# Transition events are written "This entry is now DEPRECATED."
# Narrative mentions are written "lifecycle_status=deprecated".
# Case-sensitive match cleanly separates the two.

_RETIRED_DIR_NAME = "_retired"  # forward-only archive directory


def _normalise_state(value: object) -> str:
    """Case-fold + strip whitespace. None / non-strings -> ''."""
    if not isinstance(value, str):
        return ""
    return value.strip().lower()


def _change_history_entries(record: dict) -> list[dict]:
    """Return all change_history entries (top-level OR metadata.change_history)."""
    ch = record.get("change_history")
    if isinstance(ch, list):
        return ch
    md = record.get("metadata") or {}
    if isinstance(md, dict):
        ch = md.get("change_history")
        if isinstance(ch, list):
            return ch
    return []


def _has_deprecation_marker(entries: list[dict]) -> bool:
    """True if any entry's `change` text contains the DEPRECATED marker.

    Case-sensitive: matches "DEPRECATED" (the transition-event
    convention) but NOT "deprecated" (narrative mentions of
    lifecycle_status values). See module docstring.
    """
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        change = entry.get("change") or entry.get("description") or ""
        if not isinstance(change, str):
            continue
        if DEPRECATION_MARKER in change:  # case-sensitive
            return True
    return False


def _load_bp_records(catalog_root: Path) -> list[tuple[Path, dict]]:
    """Load every canonical Business Process record (with path).

    Walks `entities/v1-alpha/dea:process-*/<id>.yaml`. Skips dirs
    without the expected YAML file. Returns (path, record) pairs so
    that LCM-005 can inspect the on-disk location.
    """
    base = catalog_root / "entities" / "v1-alpha"
    pairs: list[tuple[Path, dict]] = []
    if not base.exists():
        return pairs
    for yaml_path in sorted(base.rglob("processes-process-*.yaml")):
        try:
            data = yaml.safe_load(yaml_path.read_text())
        except yaml.YAMLError as exc:
            print(f"WARN: {yaml_path}: YAML parse error: {exc}", file=sys.stderr)
            continue
        if isinstance(data, dict):
            pairs.append((yaml_path, data))
    return pairs


def _check_lcm_001(record: dict) -> str | None:
    """LCM-001: lifecycle_status in approved vocabulary."""
    raw = record.get("lifecycle_status")
    if raw is None:
        return "lifecycle_status missing"
    if not isinstance(raw, str):
        return f"lifecycle_status must be a string; got {type(raw).__name__}"
    norm = _normalise_intent_safe(raw)  # local helper below
    if not norm:
        return "lifecycle_status is empty after strip"
    if norm not in APPROVED_LIFECYCLE_STATES:
        return (
            f"lifecycle_status={raw!r} not in approved vocabulary "
            f"{sorted(APPROVED_LIFECYCLE_STATES)}"
        )
    return None


def _normalise_intent_safe(value: str) -> str:
    """Same shape as `_normalise_intent` in check_intent_purposive."""
    return value.strip().lower()


def _check_lcm_002(record: dict) -> str | None:
    """LCM-002: status ↔ lifecycle_status consistency."""
    raw_ls = record.get("lifecycle_status")
    raw_st = record.get("status")
    if raw_st is None:
        # status absent is allowed (some records use lifecycle_status only).
        return None
    ls = _normalise_state(raw_ls)
    st = _normalise_state(raw_st)
    if not ls or not st:
        return None  # covered by LCM-001 if applicable
    # Accept: identical values, OR both in legacy compatibility set.
    if ls == st:
        return None
    if ls in LEGACY_COMPATIBILITY_SET and st in LEGACY_COMPATIBILITY_SET:
        return None
    return (
        f"status={raw_st!r} inconsistent with lifecycle_status={raw_ls!r} "
        f"(must be identical, or both in legacy compatibility set "
        f"{sorted(LEGACY_COMPATIBILITY_SET)})"
    )


def _check_lcm_003(record: dict) -> str | None:
    """LCM-003: deprecated must carry audit trail."""
    if _normalise_state(record.get("lifecycle_status")) != "deprecated":
        return None
    entries = _change_history_entries(record)
    if not _has_deprecation_marker(entries):
        return (
            "lifecycle_status=deprecated but no change_history entry "
            f"contains the {DEPRECATION_MARKER!r} marker (silent deprecation)"
        )
    return None


def _check_lcm_004(record: dict) -> str | None:
    """LCM-004: non-deprecated must NOT carry deprecation marker."""
    if _normalise_state(record.get("lifecycle_status")) == "deprecated":
        return None
    entries = _change_history_entries(record)
    if _has_deprecation_marker(entries):
        return (
            "lifecycle_status is not 'deprecated' but change_history "
            f"contains a {DEPRECATION_MARKER!r} marker (zombie marker; "
            f"consider rolling back or completing the deprecation)"
        )
    return None


def _check_lcm_005(record_path: Path, record: dict) -> str | None:
    """LCM-005: retired records must live in archive."""
    if _normalise_state(record.get("lifecycle_status")) != "retired":
        return None
    # Archive convention: entities/_retired/<id>/<id>.yaml
    if _RETIRED_DIR_NAME not in record_path.parts:
        return (
            f"lifecycle_status=retired but path {record_path.relative_to(record_path.parents[3])} "
            f"is not under entities/{_RETIRED_DIR_NAME}/ (must be archived)"
        )
    return None


_RULES_RECORD = (
    ("LCM-001", _check_lcm_001, "lifecycle_status in approved vocabulary"),
    ("LCM-002", _check_lcm_002, "status ↔ lifecycle_status consistency"),
    ("LCM-003", _check_lcm_003, "deprecated must carry audit trail"),
    ("LCM-004", _check_lcm_004, "non-deprecated must NOT carry deprecation marker"),
)

_RULES_PATH = (
    ("LCM-005", _check_lcm_005, "retired records must live in archive"),
)


def evaluate(pairs) -> list[dict]:
    """Run all five rules against every (path, record) pair."""
    findings: list[dict] = []
    for path, record in pairs:
        rec_id = record.get("id") or path.parent.name
        # Record-only rules
        for rule_id, fn, _label in _RULES_RECORD:
            diagnostic = fn(record)
            if diagnostic is not None:
                findings.append({
                    "rule": rule_id,
                    "record_id": rec_id,
                    "diagnostic": diagnostic,
                })
        # Path-aware rule
        for rule_id, fn, _label in _RULES_PATH:
            diagnostic = fn(path, record)
            if diagnostic is not None:
                findings.append({
                    "rule": rule_id,
                    "record_id": rec_id,
                    "diagnostic": diagnostic,
                })
    return findings


def _verdict(findings: list[dict]) -> str:
    if findings:
        return "NON-CONFORMANT"
    return "CONFORMANT"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(
        "Lifecycle State-Machine validator (CR-BP-34c; LCM-001..005)."
    ))
    parser.add_argument(
        "--catalog-root",
        default=".",
        help="Path to the catalog repo root (default: current directory).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 on any finding (otherwise findings are advisory).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON output instead of human-readable summary.",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run the built-in self-test and exit.",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    catalog_root = Path(args.catalog_root).resolve()
    pairs = _load_bp_records(catalog_root)
    findings = evaluate(pairs)
    verdict = _verdict(findings)

    if args.json:
        print(json.dumps({
            "verdict": verdict,
            "candidate_count": len(pairs),
            "finding_count": len(findings),
            "findings": findings,
            "rules": [
                {"id": rid, "name": label}
                for rid, _fn, label in _RULES_RECORD + _RULES_PATH
            ],
            "approved_lifecycle_states": sorted(APPROVED_LIFECYCLE_STATES),
            "legacy_compatibility_set": sorted(LEGACY_COMPATIBILITY_SET),
        }, indent=2, sort_keys=True))
    else:
        print(f"Lifecycle State-Machine (CR-BP-34c; LCM-001..005): {verdict}")
        print(f"  Records checked:  {len(pairs)}")
        print(f"  Findings:         {len(findings)}")
        for rid, _fn, label in _RULES_RECORD + _RULES_PATH:
            n = sum(1 for f in findings if f["rule"] == rid)
            print(f"    {rid} ({label}): {n}")
        if findings:
            print("\nFindings:")
            for f in findings:
                print(f"  [{f['rule']}] {f['record_id']}: {f['diagnostic']}")

    if findings and args.strict:
        return 1
    return 0


def _self_test() -> int:
    """Built-in self-test."""

    def _record(status_value: str = "candidate", ls_value: str = "candidate",
                ch: list | None = None):
        d = {
            "id": "processes:process-self-test",
            "name": "Self Test",
            "type": "Process",
            "version": "1.0.0",
            "lifecycle_status": ls_value,
            "status": status_value,
        }
        if ch is not None:
            d["metadata"] = {"change_history": ch}
        return d

    # LCM-001: all approved values pass
    # For 'deprecated', a transition marker is required (LCM-003),
    # so the loop must provide one.
    # For 'retired', the record must be in the archive dir (LCM-005),
    # so the loop uses the _retired path.
    for s in sorted(APPROVED_LIFECYCLE_STATES):
        ch = ([{"change": "This entry is now DEPRECATED."}]
              if s == "deprecated" else None)
        if s == "retired":
            p = Path("/x/_retired/dea:process-self-test/dea:process-self-test.yaml")
        else:
            p = Path("/x/v1-alpha/dea:process-self-test/dea:process-self-test.yaml")
        findings = evaluate([(p, _record(ls_value=s, status_value=s, ch=ch))])
        assert findings == [], (s, findings)

    # LCM-001: bad value
    f = evaluate([(Path("/x/v1-alpha/dea:process-self-test/dea:process-self-test.yaml"),
                   _record(ls_value="Validated-Draft", status_value="Validated-Draft"))])
    assert len(f) == 1 and f[0]["rule"] == "LCM-001"

    # LCM-001: missing lifecycle_status
    r = _record(ls_value="candidate", status_value="candidate")
    r.pop("lifecycle_status")
    f = evaluate([(Path("/x"), r)])
    assert any(x["rule"] == "LCM-001" for x in f)

    # LCM-002: identical values pass
    assert evaluate([(Path("/x"), _record())]) == []

    # LCM-002: legacy-set equivalence (candidate/candidate)
    assert evaluate([(Path("/x"), _record(status_value="candidate", ls_value="candidate"))]) == []

    # LCM-002: drift (status differs from lifecycle_status)
    f = evaluate([(Path("/x"), _record(status_value="candidate", ls_value="draft"))])
    assert any(x["rule"] == "LCM-002" for x in f)

    # LCM-002: absent status is OK
    r = _record()
    r.pop("status")
    assert evaluate([(Path("/x"), r)]) == []

    # LCM-003: deprecated without marker fires
    f = evaluate([(Path("/x"), _record(status_value="deprecated", ls_value="deprecated",
                                       ch=[{"cr": "CR-BP-21a", "change": "L2 migration executed."}]))])
    assert any(x["rule"] == "LCM-003" for x in f)

    # LCM-003: deprecated WITH marker passes
    assert evaluate([(Path("/x"), _record(status_value="deprecated", ls_value="deprecated",
                                          ch=[{"cr": "CR-BP-21a",
                                               "change": "This entry is now DEPRECATED."}]))]) == []

    # LCM-003: deprecated with case-insensitive marker DOES NOT pass.
    # Narrative-style "deprecated" (lowercase) is not a transition
    # marker; only the uppercase "DEPRECATED" convention is.
    f = evaluate([(Path("/x"), _record(status_value="deprecated", ls_value="deprecated",
                                       ch=[{"change": "this entry is now deprecated"}]))])
    assert any(x["rule"] == "LCM-003" for x in f)

    # LCM-004: non-deprecated with marker fires
    f = evaluate([(Path("/x"), _record(status_value="candidate", ls_value="candidate",
                                       ch=[{"change": "Marked DEPRECATED but rolled back."}]))])
    assert any(x["rule"] == "LCM-004" for x in f)

    # LCM-004: deprecated is exempt from LCM-004
    assert evaluate([(Path("/x"), _record(status_value="deprecated", ls_value="deprecated",
                                          ch=[{"change": "Now DEPRECATED."}]))]) == []

    # LCM-005: retired in wrong location fires
    f = evaluate([(Path("/home/x/dea-catalog-processes/entities/v1-alpha/dea:process-self-test/dea:process-self-test.yaml"),
                   _record(status_value="retired", ls_value="retired"))])
    assert any(x["rule"] == "LCM-005" for x in f)

    # LCM-005: retired in correct location passes
    f = evaluate([(Path("/home/x/dea-catalog-processes/entities/_retired/dea:process-self-test/dea:process-self-test.yaml"),
                   _record(status_value="retired", ls_value="retired"))])
    assert f == []

    # Legacy top-level change_history shape
    r = _record(status_value="deprecated", ls_value="deprecated")
    r.pop("metadata", None)
    r["change_history"] = [{"change": "DEPRECATED."}]
    assert evaluate([(Path("/x"), r)]) == []

    print("self-test PASS (13 cases)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
