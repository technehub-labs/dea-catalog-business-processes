#!/usr/bin/env python3
"""
check_business_rules_controls_exceptions_ext14.py
==================================================

L2/L3/L4 business rules, controls, exceptions, deviations validator
(CR-BP-94-EXT-14).

Codifies the EXT-14 requirements:

  GO-001  business_rules (when present) has the EXT-14 attributes
          (id, name, description, source, source_ref, maturity,
          rationale, owner).
  GO-002  business_rules[].source is in the rule-source vocabulary
          (regulatory | contractual | governance | operational | sector).
  GO-003  business_rules[].maturity is in the rule-maturity vocabulary
          (proposed | documented | approved | in_force | monitored | retired).
  GO-004  controls (when present) has the EXT-14 attributes
          (id, name, description, type, enforces, automation, frequency,
          evidence, owner).
  GO-005  controls[].type is in the control-type vocabulary
          (preventive | detective | corrective | directive).
  GO-006  controls[].automation is in the automation vocabulary
          (manual | semi_automated | automated).
  GO-007  controls[].frequency is in the frequency vocabulary
          (continuous | daily | weekly | monthly | quarterly | annual
          | on_event | on_request).
  GO-008  exceptions (when present) has the EXT-14 attributes
          (id, name, description, classification, detection, response,
          escalation, resolution, owner).
  GO-009  exceptions[].classification is in the classification vocabulary
          (recoverable | non_recoverable | business | technical).
  GO-010  L0/L1 do NOT carry business_rules/controls/exceptions/
          deviations (non-executable per EXT-11 + EXT-14 §8).

The validator writes a manifest at reconciliation/governance-manifest.json
and runs as gate [39] in scripts/conformance_result.py (ADVISORY;
flipped to blocking under CR-BP-94-EXT-23).

Test layout: tests/test_business_rules_controls_exceptions_ext14.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError:
    sys.stderr.write("ERROR: PyYAML is required.\n")
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "reconciliation" / "governance-manifest.json"

# Controlled vocabularies (per EXT-14)
RULE_SOURCES = frozenset({"regulatory", "contractual", "governance", "operational", "sector"})
RULE_MATURITIES = frozenset({
    "proposed", "documented", "approved", "in_force", "monitored", "retired",
})
CONTROL_TYPES = frozenset({"preventive", "detective", "corrective", "directive"})
CONTROL_AUTOMATION = frozenset({"manual", "semi_automated", "automated"})
CONTROL_FREQUENCY = frozenset({
    "continuous", "daily", "weekly", "monthly", "quarterly", "annual",
    "on_event", "on_request",
})
EXCEPTION_CLASSIFICATIONS = frozenset({
    "recoverable", "non_recoverable", "business", "technical",
})
DEVIATION_STATUSES = frozenset({
    "detected", "authorised", "unauthorised", "remediated", "escalated", "closed",
})
DEVIATION_SEVERITIES = frozenset({"high", "medium", "low"})

# Non-executable levels (per EXT-11)
NON_EXECUTABLE_LEVELS = frozenset({"L0", "L1"})

# Type -> level mapping
LEVEL_BY_TYPE = {
    "ProcessContext": "L0",
    "ProcessGroup": "L1",
    "Process": "L2",
    "Activity": "L3",
    "Task": "L4",
}


def _make_finding(rule: str, where: str, diagnostic: str) -> dict:
    return {"rule": rule, "where": where, "diagnostic": diagnostic, "advisory": True}


def evaluate(records: Iterable[tuple[Path, dict]]) -> list[dict]:
    """Run GO-001..GO-010 against every (path, record) pair. Returns findings."""
    findings: list[dict] = []

    for path, record in records:
        rec_id = record.get("id") or path.parent.name
        entity_type = record.get("type")
        level = LEVEL_BY_TYPE.get(entity_type) if isinstance(entity_type, str) else None
        where = f"{rec_id} ({entity_type} {level})"

        # GO-010: non-executable levels MUST NOT declare EXT-14 fields.
        if level in NON_EXECUTABLE_LEVELS:
            for field in ("business_rules", "controls", "exceptions", "deviations"):
                if field in record:
                    findings.append(_make_finding(
                        "GO-010", where,
                        f"non-executable {level} record declares {field!r}; "
                        f"per EXT-11 PR-006, L0/L1 are non-executable",
                    ))

        # GO-001 + GO-002 + GO-003: business_rules[].
        business_rules = record.get("business_rules")
        if isinstance(business_rules, list):
            seen_rule_ids: set[str] = set()
            for i, entry in enumerate(business_rules):
                entry_where = f"{where} business_rules[{i}]"
                if not isinstance(entry, dict):
                    findings.append(_make_finding(
                        "GO-001", entry_where,
                        "business_rules entry is not a dict",
                    ))
                    continue
                for required_key in ("id", "name", "description", "source",
                                      "source_ref", "maturity", "rationale", "owner"):
                    if required_key not in entry:
                        findings.append(_make_finding(
                            "GO-001", entry_where,
                            f"business_rules entry missing EXT-14 field {required_key!r}",
                        ))
                rid = entry.get("id")
                if isinstance(rid, str):
                    if rid in seen_rule_ids:
                        findings.append(_make_finding(
                            "GO-001", entry_where,
                            f"duplicate business_rule id {rid!r} within record",
                        ))
                    seen_rule_ids.add(rid)
                src = entry.get("source")
                if src is not None and src not in RULE_SOURCES:
                    findings.append(_make_finding(
                        "GO-002", entry_where,
                        f"business_rules[].source {src!r} is not in the EXT-14 rule-source vocabulary",
                    ))
                mat = entry.get("maturity")
                if mat is not None and mat not in RULE_MATURITIES:
                    findings.append(_make_finding(
                        "GO-003", entry_where,
                        f"business_rules[].maturity {mat!r} is not in the EXT-14 rule-maturity vocabulary",
                    ))

        # GO-004 + GO-005 + GO-006 + GO-007: controls[].
        controls = record.get("controls")
        if isinstance(controls, list):
            seen_ctrl_ids: set[str] = set()
            for i, entry in enumerate(controls):
                entry_where = f"{where} controls[{i}]"
                if not isinstance(entry, dict):
                    findings.append(_make_finding(
                        "GO-004", entry_where,
                        "controls entry is not a dict",
                    ))
                    continue
                for required_key in ("id", "name", "description", "type",
                                      "enforces", "automation", "frequency",
                                      "evidence", "owner"):
                    if required_key not in entry:
                        findings.append(_make_finding(
                            "GO-004", entry_where,
                            f"controls entry missing EXT-14 field {required_key!r}",
                        ))
                cid = entry.get("id")
                if isinstance(cid, str):
                    if cid in seen_ctrl_ids:
                        findings.append(_make_finding(
                            "GO-004", entry_where,
                            f"duplicate control id {cid!r} within record",
                        ))
                    seen_ctrl_ids.add(cid)
                t = entry.get("type")
                if t is not None and t not in CONTROL_TYPES:
                    findings.append(_make_finding(
                        "GO-005", entry_where,
                        f"controls[].type {t!r} is not in the EXT-14 control-type vocabulary",
                    ))
                auto = entry.get("automation")
                if auto is not None and auto not in CONTROL_AUTOMATION:
                    findings.append(_make_finding(
                        "GO-006", entry_where,
                        f"controls[].automation {auto!r} is not in the EXT-14 automation vocabulary",
                    ))
                freq = entry.get("frequency")
                if freq is not None and freq not in CONTROL_FREQUENCY:
                    findings.append(_make_finding(
                        "GO-007", entry_where,
                        f"controls[].frequency {freq!r} is not in the EXT-14 frequency vocabulary",
                    ))

        # GO-008 + GO-009: exceptions[].
        exceptions = record.get("exceptions")
        if isinstance(exceptions, list):
            seen_exc_ids: set[str] = set()
            for i, entry in enumerate(exceptions):
                entry_where = f"{where} exceptions[{i}]"
                if not isinstance(entry, dict):
                    findings.append(_make_finding(
                        "GO-008", entry_where,
                        "exceptions entry is not a dict",
                    ))
                    continue
                for required_key in ("id", "name", "description", "classification",
                                      "detection", "response", "escalation",
                                      "resolution", "owner"):
                    if required_key not in entry:
                        findings.append(_make_finding(
                            "GO-008", entry_where,
                            f"exceptions entry missing EXT-14 field {required_key!r}",
                        ))
                eid = entry.get("id")
                if isinstance(eid, str):
                    if eid in seen_exc_ids:
                        findings.append(_make_finding(
                            "GO-008", entry_where,
                            f"duplicate exception id {eid!r} within record",
                        ))
                    seen_exc_ids.add(eid)
                cls = entry.get("classification")
                if cls is not None and cls not in EXCEPTION_CLASSIFICATIONS:
                    findings.append(_make_finding(
                        "GO-009", entry_where,
                        f"exceptions[].classification {cls!r} is not in the EXT-14 classification vocabulary",
                    ))

        # Deviations[] (validated structurally; no GO rule in EXT-14, but check
        # the controlled vocabularies if deviations are present).
        deviations = record.get("deviations")
        if isinstance(deviations, list):
            for i, entry in enumerate(deviations):
                entry_where = f"{where} deviations[{i}]"
                if not isinstance(entry, dict):
                    continue
                st = entry.get("status")
                if st is not None and st not in DEVIATION_STATUSES:
                    findings.append(_make_finding(
                        "GO-008", entry_where,
                        f"deviations[].status {st!r} is not in the EXT-14 status vocabulary",
                    ))
                sev = entry.get("severity")
                if sev is not None and sev not in DEVIATION_SEVERITIES:
                    findings.append(_make_finding(
                        "GO-008", entry_where,
                        f"deviations[].severity {sev!r} is not in the EXT-14 severity vocabulary",
                    ))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true",
                        help="run a synthetic self-test (no live tree scan)")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--catalog-root", default=".", help="catalog root")
    args = parser.parse_args()

    catalog_root = Path(args.catalog_root).resolve()

    if args.self_test:
        synthetic = [
            (Path("test.yaml"), {
                "id": "test:bp-1",
                "type": "Process",
                "business_rules": [
                    {"id": "r1", "name": "KYC must verify identity",
                     "description": "Every customer must be KYC-verified",
                     "source": "regulatory", "source_ref": "https://...",
                     "maturity": "in_force",
                     "rationale": "Per SMCR.",
                     "owner": "compliance_officer"},
                ],
                "controls": [
                    {"id": "c1", "name": "ID verification",
                     "description": "Automated ID check",
                     "type": "preventive", "enforces": "r1",
                     "automation": "automated", "frequency": "continuous",
                     "evidence": ["audit log"],
                     "owner": "compliance_officer"},
                ],
                "exceptions": [
                    {"id": "e1", "name": "Missing ID",
                     "description": "Customer submits without ID",
                     "classification": "recoverable",
                     "detection": "continuous",
                     "response": "Request ID from customer",
                     "escalation": "Compliance team",
                     "resolution": "Re-attempt with ID",
                     "owner": "compliance_officer"},
                ],
                "deviations": [
                    {"id": "d1", "rule_ref": "r1",
                     "description": "Customer onboarded without ID",
                     "status": "remediated", "severity": "high",
                     "detected_at": "2026-10-01",
                     "remediated_at": "2026-10-02",
                     "remediation": "ID obtained; onboarding re-verified"},
                ],
            }),
        ]
        findings = evaluate(synthetic)
        result = {"mode": "self-test", "findings": findings,
                  "summary": {"total_findings": len(findings)}}
        print(json.dumps(result, indent=2))
        return 0 if not findings else 1

    if yaml is None:
        sys.stderr.write("ERROR: PyYAML is required.\n")
        return 2

    records: list[tuple[Path, dict]] = []
    for f in (catalog_root / "entities" / "v1-alpha").rglob("*.yaml"):
        try:
            with f.open(encoding="utf-8") as fp:
                rec = yaml.safe_load(fp)
        except Exception:
            continue
        if isinstance(rec, dict):
            records.append((f, rec))

    findings = evaluate(records)

    manifest = {
        "manifest_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/check_business_rules_controls_exceptions_ext14.py",
        "parent_cr": "CR-BP-94-EXT-14",
        "catalog_root": str(catalog_root),
        "summary": {
            "total_records": len(records),
            "total_findings": len(findings),
            "by_rule": {},
        },
        "findings": findings,
        "controlled_vocabularies": {
            "rule_sources": sorted(RULE_SOURCES),
            "rule_maturities": sorted(RULE_MATURITIES),
            "control_types": sorted(CONTROL_TYPES),
            "control_automation": sorted(CONTROL_AUTOMATION),
            "control_frequency": sorted(CONTROL_FREQUENCY),
            "exception_classifications": sorted(EXCEPTION_CLASSIFICATIONS),
            "deviation_statuses": sorted(DEVIATION_STATUSES),
            "deviation_severities": sorted(DEVIATION_SEVERITIES),
        },
    }
    for finding in findings:
        manifest["summary"]["by_rule"].setdefault(finding["rule"], 0)
        manifest["summary"]["by_rule"][finding["rule"]] += 1

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", encoding="utf-8") as fp:
        json.dump(manifest, fp, indent=2)

    if args.json:
        print(json.dumps(manifest, indent=2))
    else:
        if not findings:
            print(f"OK: business_rules/controls/exceptions conform (0 findings). "
                  f"Manifest at {MANIFEST_PATH.relative_to(REPO_ROOT)}")
        else:
            print(f"FAIL: {len(findings)} findings across {len(records)} records.")
            for finding in findings:
                print(f"  [{finding['rule']}] {finding['where']}: {finding['diagnostic']}")

    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
