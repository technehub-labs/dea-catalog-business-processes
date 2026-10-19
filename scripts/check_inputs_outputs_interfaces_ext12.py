#!/usr/bin/env python3
"""
check_inputs_outputs_interfaces_ext12.py
=========================================

L2/L3/L4 inputs, outputs, transformation, interfaces, dependencies
validator (CR-BP-94-EXT-12).

Codifies the EXT-12 requirements:

  IT-001  Each L2 record may declare inputs[] (array of objects).
          Each entry has at minimum id + name + description (CR-BP-96
          baseline); EXT-12 adds the OPTIONAL attributes type,
          required, acceptance_criteria, validation, provenance.
  IT-002  Each L2 record may declare outputs[] (array of objects).
          Each entry has at minimum id + name + description (CR-BP-96
          baseline); EXT-12 adds the OPTIONAL attributes type,
          acceptance_criteria, quality_attributes, provenance.
  IT-003  When inputs[].type is declared, it is in the controlled
          vocabulary (information | business_object | request |
          decision | transaction | material | document |
          external_data | prior_process_output).
  IT-004  When outputs[].type is declared, it is in the controlled
          vocabulary (information | business_object | decision |
          service_result | changed_object | document | report).
  IT-005  inputs[].id is locally unique within the record.
  IT-006  outputs[].id is locally unique within the record.
  IT-007  interfaces[] entries have id, name, description, type, and
          the type is in the controlled vocabulary (human |
          organizational | information | system | physical |
          contractual | regulatory).
  IT-008  dependencies[] entries have id, target, type,
          business_consequence, and criticality (high | medium | low).
  IT-009  trigger_type (when declared) is in the controlled vocabulary
          (event_driven | time_driven | request_driven |
          condition_driven | decision_driven | external_obligation_driven).
  IT-010  L0/L1 records MUST NOT declare inputs[]/outputs[]/
          interfaces[]/dependencies[]/preconditions[] (they are
          non-executable per EXT-09 §11.1/§11.2 + EXT-11 PR-006).

The validator writes a manifest at reconciliation/inputs-outputs-manifest.json
and runs as gate [37] in scripts/conformance_result.py (ADVISORY; flipped
to blocking under CR-BP-94-EXT-23).

Test layout: tests/test_inputs_outputs_interfaces_ext12.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError:
    sys.stderr.write("ERROR: PyYAML is required.\n")
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "reconciliation" / "inputs-outputs-manifest.json"

# Controlled vocabularies (per EXT-12)
INPUT_TYPES = frozenset({
    "information", "business_object", "request", "decision", "transaction",
    "material", "document", "external_data", "prior_process_output",
})
OUTPUT_TYPES = frozenset({
    "information", "business_object", "decision", "service_result",
    "changed_object", "document", "report",
})
INTERFACE_TYPES = frozenset({
    "human", "organizational", "information", "system", "physical",
    "contractual", "regulatory",
})
DEPENDENCY_CRITICALITY = frozenset({"high", "medium", "low"})
TRIGGER_TYPES = frozenset({
    "event_driven", "time_driven", "request_driven", "condition_driven",
    "decision_driven", "external_obligation_driven",
})

# Non-executable levels (per EXT-11)
NON_EXECUTABLE_LEVELS = frozenset({"L0", "L1"})

# Type -> level mapping (per CR-BP-93 §3)
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
    """Run IT-001..IT-010 against every (path, record) pair. Returns findings."""
    findings: list[dict] = []

    for path, record in records:
        rec_id = record.get("id") or path.parent.name
        entity_type = record.get("type")
        level = LEVEL_BY_TYPE.get(entity_type) if isinstance(entity_type, str) else None
        where = f"{rec_id} ({entity_type} {level})"

        # IT-010: non-executable levels MUST NOT declare inputs/outputs/interfaces/dependencies/preconditions.
        if level in NON_EXECUTABLE_LEVELS:
            for field in ("inputs", "outputs", "interfaces", "dependencies", "preconditions"):
                if field in record:
                    findings.append(_make_finding(
                        "IT-010", where,
                        f"non-executable {level} record declares {field!r}; "
                        f"per EXT-11 PR-006, L0/L1 are non-executable",
                    ))
            # Also no trigger_type at L0/L1
            if "trigger_type" in record:
                findings.append(_make_finding(
                    "IT-010", where,
                    f"non-executable {level} record declares trigger_type; L0/L1 are non-executable",
                ))

        # IT-001 + IT-002 + IT-003 + IT-004 + IT-005 + IT-006: inputs[] and outputs[].
        inputs = record.get("inputs")
        if inputs is not None and isinstance(inputs, list):
            seen_input_ids: set[str] = set()
            for i, entry in enumerate(inputs):
                entry_where = f"{where} inputs[{i}]"
                if not isinstance(entry, dict):
                    findings.append(_make_finding(
                        "IT-001", entry_where,
                        "inputs entry is not a dict",
                    ))
                    continue
                # CR-BP-96 baseline: id, name, description.
                for required_key in ("id", "name", "description"):
                    if required_key not in entry:
                        findings.append(_make_finding(
                            "IT-001", entry_where,
                            f"inputs entry missing required CR-BP-96 field {required_key!r}",
                        ))
                # IT-005: local id uniqueness.
                eid = entry.get("id")
                if isinstance(eid, str):
                    if eid in seen_input_ids:
                        findings.append(_make_finding(
                            "IT-005", entry_where,
                            f"duplicate input id {eid!r} within record",
                        ))
                    seen_input_ids.add(eid)
                # IT-003: optional type in controlled vocabulary.
                t = entry.get("type")
                if t is not None and t not in INPUT_TYPES:
                    findings.append(_make_finding(
                        "IT-003", entry_where,
                        f"inputs[].type {t!r} is not in the EXT-12 controlled vocabulary",
                    ))

        outputs = record.get("outputs")
        if outputs is not None and isinstance(outputs, list):
            seen_output_ids: set[str] = set()
            for i, entry in enumerate(outputs):
                entry_where = f"{where} outputs[{i}]"
                if not isinstance(entry, dict):
                    findings.append(_make_finding(
                        "IT-002", entry_where,
                        "outputs entry is not a dict",
                    ))
                    continue
                for required_key in ("id", "name", "description"):
                    if required_key not in entry:
                        findings.append(_make_finding(
                            "IT-002", entry_where,
                            f"outputs entry missing required CR-BP-96 field {required_key!r}",
                        ))
                eid = entry.get("id")
                if isinstance(eid, str):
                    if eid in seen_output_ids:
                        findings.append(_make_finding(
                            "IT-006", entry_where,
                            f"duplicate output id {eid!r} within record",
                        ))
                    seen_output_ids.add(eid)
                t = entry.get("type")
                if t is not None and t not in OUTPUT_TYPES:
                    findings.append(_make_finding(
                        "IT-004", entry_where,
                        f"outputs[].type {t!r} is not in the EXT-12 controlled vocabulary",
                    ))

        # IT-007: interfaces[] structure + type vocabulary.
        interfaces = record.get("interfaces")
        if interfaces is not None and isinstance(interfaces, list):
            seen_interface_ids: set[str] = set()
            for i, entry in enumerate(interfaces):
                entry_where = f"{where} interfaces[{i}]"
                if not isinstance(entry, dict):
                    findings.append(_make_finding(
                        "IT-007", entry_where,
                        "interfaces entry is not a dict",
                    ))
                    continue
                for required_key in ("id", "name", "description", "type"):
                    if required_key not in entry:
                        findings.append(_make_finding(
                            "IT-007", entry_where,
                            f"interfaces entry missing required EXT-12 field {required_key!r}",
                        ))
                eid = entry.get("id")
                if isinstance(eid, str):
                    if eid in seen_interface_ids:
                        findings.append(_make_finding(
                            "IT-007", entry_where,
                            f"duplicate interface id {eid!r} within record",
                        ))
                    seen_interface_ids.add(eid)
                t = entry.get("type")
                if t is not None and t not in INTERFACE_TYPES:
                    findings.append(_make_finding(
                        "IT-007", entry_where,
                        f"interfaces[].type {t!r} is not in the EXT-12 controlled vocabulary",
                    ))

        # IT-008: dependencies[] structure + criticality vocabulary.
        dependencies = record.get("dependencies")
        if dependencies is not None and isinstance(dependencies, list):
            seen_dep_ids: set[str] = set()
            for i, entry in enumerate(dependencies):
                entry_where = f"{where} dependencies[{i}]"
                if not isinstance(entry, dict):
                    findings.append(_make_finding(
                        "IT-008", entry_where,
                        "dependencies entry is not a dict",
                    ))
                    continue
                for required_key in ("id", "target", "type", "business_consequence", "criticality"):
                    if required_key not in entry:
                        findings.append(_make_finding(
                            "IT-008", entry_where,
                            f"dependencies entry missing required EXT-12 field {required_key!r}",
                        ))
                eid = entry.get("id")
                if isinstance(eid, str):
                    if eid in seen_dep_ids:
                        findings.append(_make_finding(
                            "IT-008", entry_where,
                            f"duplicate dependency id {eid!r} within record",
                        ))
                    seen_dep_ids.add(eid)
                crit = entry.get("criticality")
                if crit is not None and crit not in DEPENDENCY_CRITICALITY:
                    findings.append(_make_finding(
                        "IT-008", entry_where,
                        f"dependencies[].criticality {crit!r} is not in the EXT-12 controlled vocabulary",
                    ))

        # IT-009: trigger_type vocabulary.
        trigger_type = record.get("trigger_type")
        if trigger_type is not None and trigger_type not in TRIGGER_TYPES:
            findings.append(_make_finding(
                "IT-009", where,
                f"trigger_type {trigger_type!r} is not in the EXT-12 controlled vocabulary",
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
                "inputs": [
                    {"id": "i1", "name": "Customer request",
                     "description": "A request", "source": "external",
                     "type": "request", "required": True},
                ],
                "outputs": [
                    {"id": "o1", "name": "Resolution",
                     "description": "A documented resolution", "consumer": "ops",
                     "type": "service_result", "quality_attributes": ["accuracy"]},
                ],
                "interfaces": [
                    {"id": "iface1", "name": "Customer channel",
                     "description": "Submission channel", "type": "human",
                     "participants": ["customer", "ops"]},
                ],
                "dependencies": [
                    {"id": "dep1", "target": "CRM", "type": "system",
                     "business_consequence": "Cannot resolve without CRM",
                     "criticality": "high"},
                ],
                "trigger_type": "request_driven",
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

    # Build the manifest.
    manifest = {
        "manifest_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/check_inputs_outputs_interfaces_ext12.py",
        "parent_cr": "CR-BP-94-EXT-12",
        "catalog_root": str(catalog_root),
        "summary": {
            "total_records": len(records),
            "total_findings": len(findings),
            "by_rule": {},
        },
        "findings": findings,
        "controlled_vocabularies": {
            "input_types": sorted(INPUT_TYPES),
            "output_types": sorted(OUTPUT_TYPES),
            "interface_types": sorted(INTERFACE_TYPES),
            "dependency_criticality": sorted(DEPENDENCY_CRITICALITY),
            "trigger_types": sorted(TRIGGER_TYPES),
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
            print(f"OK: inputs/outputs/interfaces conform (0 findings). "
                  f"Manifest at {MANIFEST_PATH.relative_to(REPO_ROOT)}")
        else:
            print(f"FAIL: {len(findings)} findings across {len(records)} records.")
            for finding in findings:
                print(f"  [{finding['rule']}] {finding['where']}: {finding['diagnostic']}")

    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
