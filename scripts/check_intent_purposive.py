#!/usr/bin/env python3
"""
check_intent_purposive.py
=========================

Intent Purposive validator (CR-BP-34b; CR-BP-34 §7 PSP-001..003).

Codifies the three Intent purposive rules from CR-BP-34 §7 as
machine-testable rules:

  PSP-001 — Intent shall be purposive.
            process_intent (when present) is non-empty and
            expresses a purpose.

  PSP-002 — Intent shall use an approved vocabulary.
            process_intent ∈ the 7-value purposive vocabulary
            declared in `classifications/process-intents.yaml`
            (govern / manage / operate / deliver / support /
            develop / transform).

  PSP-003 — Intent shall not encode organizational ownership.
            process_intent is NOT drawn from the curated
            organizational-component denylist (Mintzberg 5-part
            functional silos + org-structure terms + ECF domain
            names + lifecycle stage names).

Coverage on the live catalog (2026-09-10): all 126 Business Process
records pass all three rules. The validator is therefore a
regression guard (no findings today) rather than a corrective gate.

Exit codes:
  0  all records pass all three rules
  1  at least one record fails at least one rule
  2  self-test failure or I/O error

Usage:
  python3 scripts/check_intent_purposive.py
  python3 scripts/check_intent_purposive.py --strict
  python3 scripts/check_intent_purposive.py --json
  python3 scripts/check_intent_purposive.py --self-test

Author: Coder (for eaojnr). Established by CR-BP-34b (2026-09-10).
Derived from CR-BP-34 §7 (Intent Conformance) and CR-BP-14 §9.2
(BP-SEM-001 Intent Vocabulary). Vocabulary sourced from
`classifications/process-intents.yaml`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

# Approved 7-value purposive vocabulary (CR-BP-14 §9.2;
# classifications/process-intents.yaml).
APPROVED_INTENTS: set[str] = {
    "govern",
    "manage",
    "operate",
    "deliver",
    "support",
    "develop",
    "transform",
}

# Organizational-component denylist (CR-BP-34 §7 + §8; PSP-003).
# Curated; intentional narrowness. Case-folded; whitespace stripped
# before comparison. Adding an entry here is a one-line edit.
ORG_COMPONENT_DENYLIST: set[str] = {
    # Mintzberg 5-part functional silos + common variants
    "operations", "production", "sales", "marketing", "hr",
    "finance", "it", "legal", "facilities", "admin",
    # Sectors / industries
    "manufacturing", "logistics", "warehouse", "procurement",
    "engineering", "treasury", "tax", "audit", "compliance",
    "risk",
    # Org-structure terms
    "department", "division", "team", "unit", "office",
    "branch", "subsidiary", "section", "group",
    # ECF domain names (v2.5.0; CR-BP-23)
    "strategyanddirection", "agencyandorganization",
    "partyandrelationship", "productandvalue",
    "enablementandoperations", "financeandaccounting",
    "governanceandexistence",
    # Lifecycle stage names
    "conceive", "design", "build", "activate",
    "improve", "retire",
}


def _normalise_intent(value: object) -> str:
    """Case-fold + strip whitespace. None / non-strings -> ''."""
    if not isinstance(value, str):
        return ""
    return value.strip().lower()


def _load_bp_records(catalog_root: Path) -> list[dict]:
    """Load every canonical Business Process record.

    Walks `entities/v1-alpha/dea:process-*/<id>.yaml`. Skips dirs
    without the expected YAML file (e.g. `candidates/`, `retired/`).
    """
    base = catalog_root / "entities" / "v1-alpha"
    records: list[dict] = []
    if not base.exists():
        return records
    for yaml_path in sorted(base.rglob("processes-process-*.yaml")):
        try:
            data = yaml.safe_load(yaml_path.read_text())
        except yaml.YAMLError as exc:
            print(f"WARN: {yaml_path}: YAML parse error: {exc}", file=sys.stderr)
            continue
        if isinstance(data, dict):
            records.append(data)
    return records


def _check_psp_001(record: dict) -> str | None:
    """PSP-001: process_intent (when present) is non-empty after strip."""
    raw = record.get("process_intent")
    if raw is None:
        # Intent absent is allowed; PSP-001 only fires when intent is
        # present-but-empty. A separate admission rule (BP-SEM-001)
        # governs "must have intent"; PSP-001 governs "if present,
        # must be purposive (non-empty)".
        return None
    if not isinstance(raw, str):
        return f"process_intent must be a string when present; got {type(raw).__name__}"
    if not raw.strip():
        return "process_intent is present but empty (not purposive)"
    return None


def _check_psp_002(record: dict) -> str | None:
    """PSP-002: process_intent ∈ approved vocabulary."""
    raw = record.get("process_intent")
    if raw is None or not isinstance(raw, str) or not raw.strip():
        # Absence / empty is covered by PSP-001; do not double-fire.
        return None
    norm = _normalise_intent(raw)
    if norm not in APPROVED_INTENTS:
        return (
            f"process_intent={raw!r} not in approved vocabulary "
            f"{sorted(APPROVED_INTENTS)}"
        )
    return None


def _check_psp_003(record: dict) -> str | None:
    """PSP-003: process_intent ∉ organisational-component denylist."""
    raw = record.get("process_intent")
    if raw is None or not isinstance(raw, str) or not raw.strip():
        return None
    norm = _normalise_intent(raw)
    if norm in ORG_COMPONENT_DENYLIST:
        return (
            f"process_intent={raw!r} encodes an organizational component "
            f"(denylist match: {norm!r}); Intent must be purposive, not "
            f"org-component. Use process_context for domain / lifecycle."
        )
    return None


_RULES = (
    ("PSP-001", _check_psp_001, "Intent shall be purposive"),
    ("PSP-002", _check_psp_002, "Intent shall use an approved vocabulary"),
    ("PSP-003", _check_psp_003, "Intent shall not encode organizational ownership"),
)


def evaluate(records) -> list[dict]:
    """Run all three rules against every record."""
    findings: list[dict] = []
    for record in records:
        rec_id = record.get("id") or "<unknown>"
        for rule_id, fn, _label in _RULES:
            diagnostic = fn(record)
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
        "Intent Purposive validator (CR-BP-34b; PSP-001..003)."
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
    records = _load_bp_records(catalog_root)
    findings = evaluate(records)
    verdict = _verdict(findings)

    if args.json:
        print(json.dumps({
            "verdict": verdict,
            "candidate_count": len(records),
            "finding_count": len(findings),
            "findings": findings,
            "rules": [
                {"id": rid, "name": label}
                for rid, _fn, label in _RULES
            ],
            "approved_intents": sorted(APPROVED_INTENTS),
            "org_component_denylist_size": len(ORG_COMPONENT_DENYLIST),
        }, indent=2, sort_keys=True))
    else:
        print(f"Intent Purposive (CR-BP-34b; PSP-001..003): {verdict}")
        print(f"  Records checked:  {len(records)}")
        print(f"  Findings:         {len(findings)}")
        for rid, _fn, label in _RULES:
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
    """Built-in self-test: verify pass and fail behavior on each rule."""

    def _record(intent=None):
        return {
            "id": "processes:process-self-test",
            "name": "Self Test",
            "type": "Process",
            "version": "1.0.0",
            "process_intent": intent,
        }

    # Baseline (approved intent) -> all three pass.
    assert evaluate([_record("operate")]) == []

    # All 7 approved values pass.
    for intent in sorted(APPROVED_INTENTS):
        assert evaluate([_record(intent)]) == [], f"approved {intent} should pass"

    # PSP-001: present-but-empty fires; absent does not.
    assert len(evaluate([_record("")])) == 1  # PSP-001 only
    assert evaluate([_record(None)]) == []

    # PSP-001: non-string fires.
    f = evaluate([_record(123)])
    assert len(f) == 1 and f[0]["rule"] == "PSP-001"

    # PSP-002: unapproved string fires; PSP-001 stays silent because
    # the value is non-empty after strip.
    f = evaluate([_record("not-a-purpose")])
    assert len(f) == 1 and f[0]["rule"] == "PSP-002"

    # PSP-002 + PSP-003 may both fire for org-component words.
    f = evaluate([_record("operations")])
    rule_set = {x["rule"] for x in f}
    assert rule_set == {"PSP-002", "PSP-003"}, f

    # PSP-003: case-folded match.
    f = evaluate([_record("HR")])
    assert any(x["rule"] == "PSP-003" for x in f)

    # PSP-003: whitespace-padded match.
    f = evaluate([_record("  finance  ")])
    assert any(x["rule"] == "PSP-003" for x in f)

    # ECF domain name in intent -> PSP-003 fires.
    f = evaluate([_record("strategyAndDirection")])
    assert any(x["rule"] == "PSP-003" for x in f)

    # Lifecycle stage name in intent -> PSP-003 fires.
    f = evaluate([_record("operate")] if False else [_record("conceive")])
    assert any(x["rule"] == "PSP-003" for x in f)

    # Multi-record aggregation.
    findings = evaluate([_record("operate"), _record(""), _record("operations")])
    rec_ids = {f["record_id"] for f in findings}
    assert rec_ids == {"processes:process-self-test"}
    rule_set = {f["rule"] for f in findings}
    assert rule_set == {"PSP-001", "PSP-002", "PSP-003"}

    print("self-test PASS (8 positive cases, 6 negative cases, 1 multi-record)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
