#!/usr/bin/env python3
"""
check_responsibility_accountability_ext13.py
=============================================

L2/L3/L4 responsibility, accountability, performer, role, RACI-style
validator (CR-BP-94-EXT-13).

Codifies the EXT-13 requirements:

  RA-001  responsibility (when structured) has the EXT-13 attributes
          (role, performer, type, scope, accountabilities).
  RA-002  responsibility[].type is in the performer vocabulary
          (human | system | team | organization | external_party).
  RA-003  accountability (when present) has the EXT-13 attributes
          (role, type, scope, outcomes, rationale).
  RA-004  accountability[].type is in the accountable vocabulary
          (human | committee | board | individual).
  RA-005  roles[] (when present) has the EXT-13 attributes
          (id, name, type, description, reporting_line, capability_owner).
  RA-006  roles[].type is in the role vocabulary
          (organisational | cross_cutting | external | system).
  RA-007  raci[].scheme is in the scheme vocabulary
          (raci | rasci | rapid | daciar | paci).
  RA-008  raci[].assignments[].assignment is in the assignment vocabulary
          (16 values per the EXT-13 §6.2 controlled vocabulary).
  RA-009  roles referenced by responsibility[] / accountability[] resolve
          to entries in roles[] (when the catalog is present).
  RA-010  L0/L1 do NOT carry responsibility (structured form) /
          accountability / roles / raci (non-executable per EXT-11).

The validator writes a manifest at
reconciliation/responsibility-accountability-manifest.json and runs as
gate [38] in scripts/conformance_result.py (ADVISORY; flipped to
blocking under CR-BP-94-EXT-23).

Test layout: tests/test_responsibility_accountability_ext13.py
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
MANIFEST_PATH = REPO_ROOT / "reconciliation" / "responsibility-accountability-manifest.json"

# Controlled vocabularies (per EXT-13)
PERFORMER_TYPES = frozenset({"human", "system", "team", "organization", "external_party"})
ACCOUNTABLE_TYPES = frozenset({"human", "committee", "board", "individual"})
ROLE_TYPES = frozenset({"organisational", "cross_cutting", "external", "system"})
RACI_SCHEMES = frozenset({"raci", "rasci", "rapid", "daciar", "paci"})
RACI_ASSIGNMENTS = frozenset({
    "responsible", "accountable", "consulted", "informed",
    "supports", "recommend", "agree", "perform", "input",
    "decide", "drive", "approve", "contribute", "accept",
    "reject", "inform",
})

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
    """Run RA-001..RA-010 against every (path, record) pair. Returns findings."""
    findings: list[dict] = []

    for path, record in records:
        rec_id = record.get("id") or path.parent.name
        entity_type = record.get("type")
        level = LEVEL_BY_TYPE.get(entity_type) if isinstance(entity_type, str) else None
        where = f"{rec_id} ({entity_type} {level})"

        # RA-010: non-executable levels MUST NOT declare the EXT-13 structured fields.
        if level in NON_EXECUTABLE_LEVELS:
            for field in ("accountability", "roles", "raci"):
                if field in record:
                    findings.append(_make_finding(
                        "RA-010", where,
                        f"non-executable {level} record declares {field!r}; "
                        f"per EXT-11 PR-006, L0/L1 are non-executable",
                    ))
            # If responsibility is structured (list of dicts) at L0/L1, also flag.
            resp = record.get("responsibility")
            if isinstance(resp, list):
                findings.append(_make_finding(
                    "RA-010", where,
                    f"non-executable {level} record declares structured responsibility[]; L0/L1 are non-executable",
                ))

        # RA-001 + RA-002: responsibility structured form.
        responsibility = record.get("responsibility")
        if isinstance(responsibility, list):
            for i, entry in enumerate(responsibility):
                entry_where = f"{where} responsibility[{i}]"
                if not isinstance(entry, dict):
                    findings.append(_make_finding(
                        "RA-001", entry_where,
                        "responsibility entry is not a dict",
                    ))
                    continue
                for required_key in ("role", "performer", "type", "scope", "accountabilities"):
                    if required_key not in entry:
                        findings.append(_make_finding(
                            "RA-001", entry_where,
                            f"responsibility entry missing EXT-13 field {required_key!r}",
                        ))
                t = entry.get("type")
                if t is not None and t not in PERFORMER_TYPES:
                    findings.append(_make_finding(
                        "RA-002", entry_where,
                        f"responsibility[].type {t!r} is not in the EXT-13 performer vocabulary",
                    ))

        # RA-003 + RA-004: accountability.
        accountability = record.get("accountability")
        if isinstance(accountability, list):
            for i, entry in enumerate(accountability):
                entry_where = f"{where} accountability[{i}]"
                if not isinstance(entry, dict):
                    findings.append(_make_finding(
                        "RA-003", entry_where,
                        "accountability entry is not a dict",
                    ))
                    continue
                for required_key in ("role", "type", "scope", "outcomes", "rationale"):
                    if required_key not in entry:
                        findings.append(_make_finding(
                            "RA-003", entry_where,
                            f"accountability entry missing EXT-13 field {required_key!r}",
                        ))
                # RA-004: type vocabulary.
                t = entry.get("type")
                if t is not None and t not in ACCOUNTABLE_TYPES:
                    findings.append(_make_finding(
                        "RA-004", entry_where,
                        f"accountability[].type {t!r} is not in the EXT-13 accountable vocabulary",
                    ))
                # RA-003: rationale must be non-empty.
                rat = entry.get("rationale")
                if isinstance(rat, str) and not rat.strip():
                    findings.append(_make_finding(
                        "RA-003", entry_where,
                        "accountability[].rationale is empty; the rationale is mandatory (per EXT-13 §4.2)",
                    ))

        # RA-005 + RA-006: roles catalog.
        roles = record.get("roles")
        if isinstance(roles, list):
            seen_role_ids: set[str] = set()
            for i, entry in enumerate(roles):
                entry_where = f"{where} roles[{i}]"
                if not isinstance(entry, dict):
                    findings.append(_make_finding(
                        "RA-005", entry_where,
                        "roles entry is not a dict",
                    ))
                    continue
                for required_key in ("id", "name", "type", "description",
                                      "reporting_line", "capability_owner"):
                    if required_key not in entry:
                        findings.append(_make_finding(
                            "RA-005", entry_where,
                            f"roles entry missing EXT-13 field {required_key!r}",
                        ))
                rid = entry.get("id")
                if isinstance(rid, str):
                    if rid in seen_role_ids:
                        findings.append(_make_finding(
                            "RA-005", entry_where,
                            f"duplicate role id {rid!r} within record",
                        ))
                    seen_role_ids.add(rid)
                t = entry.get("type")
                if t is not None and t not in ROLE_TYPES:
                    findings.append(_make_finding(
                        "RA-006", entry_where,
                        f"roles[].type {t!r} is not in the EXT-13 role vocabulary",
                    ))

            # RA-009: roles referenced by responsibility[] / accountability[] resolve.
            if isinstance(responsibility, list) or isinstance(accountability, list):
                catalog = seen_role_ids
                # Also support role-by-name references (when id is absent on the role,
                # the role may be referenced by name). We accept any role id OR name.
                name_set: set[str] = set()
                for r in roles:
                    if isinstance(r, dict) and isinstance(r.get("name"), str):
                        name_set.add(r["name"])
                if isinstance(responsibility, list):
                    for i, entry in enumerate(responsibility):
                        if not isinstance(entry, dict):
                            continue
                        ref = entry.get("role")
                        if isinstance(ref, str) and ref not in catalog and ref not in name_set:
                            findings.append(_make_finding(
                                "RA-009", f"{where} responsibility[{i}]",
                                f"responsibility[].role {ref!r} does not resolve to a role in the catalog",
                            ))
                if isinstance(accountability, list):
                    for i, entry in enumerate(accountability):
                        if not isinstance(entry, dict):
                            continue
                        ref = entry.get("role")
                        if isinstance(ref, str) and ref not in catalog and ref not in name_set:
                            findings.append(_make_finding(
                                "RA-009", f"{where} accountability[{i}]",
                                f"accountability[].role {ref!r} does not resolve to a role in the catalog",
                            ))

        # RA-007 + RA-008: raci block.
        raci = record.get("raci")
        if isinstance(raci, list):
            for i, entry in enumerate(raci):
                entry_where = f"{where} raci[{i}]"
                if not isinstance(entry, dict):
                    findings.append(_make_finding(
                        "RA-007", entry_where,
                        "raci entry is not a dict",
                    ))
                    continue
                scheme = entry.get("scheme")
                if scheme is not None and scheme not in RACI_SCHEMES:
                    findings.append(_make_finding(
                        "RA-007", entry_where,
                        f"raci[].scheme {scheme!r} is not in the EXT-13 scheme vocabulary",
                    ))
                assignments = entry.get("assignments")
                if isinstance(assignments, list):
                    for j, a in enumerate(assignments):
                        a_where = f"{entry_where} assignments[{j}]"
                        if not isinstance(a, dict):
                            continue
                        assignment = a.get("assignment")
                        if assignment is not None and assignment not in RACI_ASSIGNMENTS:
                            findings.append(_make_finding(
                                "RA-008", a_where,
                                f"raci[].assignments[].assignment {assignment!r} is not in the EXT-13 assignment vocabulary",
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
        # Synthetic: a record that satisfies all rules.
        synthetic = [
            (Path("test.yaml"), {
                "id": "test:bp-1",
                "type": "Process",
                "responsibility": [
                    {"role": "kyc_analyst", "performer": "KYC Analyst",
                     "type": "human", "scope": "process",
                     "accountabilities": ["Verify identity"]},
                ],
                "accountability": [
                    {"role": "compliance_officer", "type": "human",
                     "scope": "process", "outcomes": ["Customer is KYC-cleared"],
                     "rationale": "Per SMCR, the compliance officer is accountable for KYC outcomes"},
                ],
                "roles": [
                    {"id": "kyc_analyst", "name": "KYC Analyst",
                     "type": "organisational", "description": "...",
                     "reporting_line": "Compliance", "capability_owner": "Compliance"},
                    {"id": "compliance_officer", "name": "Compliance Officer",
                     "type": "organisational", "description": "...",
                     "reporting_line": "Compliance", "capability_owner": "Compliance"},
                ],
                "raci": [
                    {"id": "raci-1", "scheme": "raci",
                     "assignments": [
                         {"role": "kyc_analyst", "activity": "act-1",
                          "assignment": "responsible"},
                         {"role": "compliance_officer", "activity": "act-1",
                          "assignment": "accountable"},
                     ]},
                ],
            }),
        ]
        findings = evaluate(synthetic)
        result = {"mode": "self-test", "findings": findings,
                  "summary": {"total_findings": len(findings)}}
        print(json.dumps(result, indent=2))
        return 0 if not findings else 1

    # Live mode: scan entities/v1-alpha/.
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
        "generator": "scripts/check_responsibility_accountability_ext13.py",
        "parent_cr": "CR-BP-94-EXT-13",
        "catalog_root": str(catalog_root),
        "summary": {
            "total_records": len(records),
            "total_findings": len(findings),
            "by_rule": {},
        },
        "findings": findings,
        "controlled_vocabularies": {
            "performer_types": sorted(PERFORMER_TYPES),
            "accountable_types": sorted(ACCOUNTABLE_TYPES),
            "role_types": sorted(ROLE_TYPES),
            "raci_schemes": sorted(RACI_SCHEMES),
            "raci_assignments": sorted(RACI_ASSIGNMENTS),
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
            print(f"OK: responsibility/accountability conform (0 findings). "
                  f"Manifest at {MANIFEST_PATH.relative_to(REPO_ROOT)}")
        else:
            print(f"FAIL: {len(findings)} findings across {len(records)} records.")
            for finding in findings:
                print(f"  [{finding['rule']}] {finding['where']}: {finding['diagnostic']}")

    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
