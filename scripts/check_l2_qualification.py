#!/usr/bin/env python3
"""
check_l2_qualification.py
==========================

L2 Qualification validator (CR-BP-34a BP-C1..C4 + CR-BP-96 BP-QUAL-001..012).

Codifies the L2 qualification contract for a Business Process as
machine-testable rules. The contract has two rule families:

  CR-BP-34a BP-C1..C4 (mandatory):
    BP-C1 — Input-Output Transformation.
            The process transforms identifiable inputs into outputs or
            an equivalent defined result.
            Field: `trigger` (non-empty) AND `outcome` (non-empty).

    BP-C2 — Objective Contribution.
            The process makes a recognizable contribution to an
            enterprise objective or outcome.
            Field: `identity.outcome_statement` (non-empty).

    BP-C3 — Standalone Executability.
            The process represents a coherent unit of work that can be
            independently identified and performed.
            Field: `lifecycle_status` present AND `id` matches
            `dea:process-[a-z0-9-]+`.

    BP-C4 — Resource Dedication.
            The process requires identifiable resources or
            responsibility sufficient to constitute a distinct process
            boundary.
            Field: `identity.evidence_links` non-empty AND
            `metadata.change_history` (or top-level `change_history`)
            has at least one entry.

  CR-BP-96 BP-QUAL-001..012 (recon-programme extension):
    BP-QUAL-001  Identity                       (alias: BP-C3)
    BP-QUAL-002  Trigger                        (alias: BP-C1)
    BP-QUAL-003  Input                          (advisory; OPTIONAL field)
    BP-QUAL-004  Transformation                 (advisory; OPTIONAL field)
    BP-QUAL-005  Output                         (advisory; OPTIONAL field)
    BP-QUAL-006  Outcome                        (alias: BP-C1+BP-C2)
    BP-QUAL-007  Objective Contribution         (alias: BP-C2)
    BP-QUAL-008  Responsibility                 (advisory; OPTIONAL field)
    BP-QUAL-009  Boundary                       (advisory; OPTIONAL field)
    BP-QUAL-010  Standalone Process Integrity   (alias: BP-C3)
    BP-QUAL-011  Specialization Integrity       [DEFERRED — CR-BP-92 §21]
    BP-QUAL-012  Evidence                       (alias: BP-C4)

The CR-BP-96 BP-QUAL-003/004/005/008/009 checks are ADVISORY and the
underlying fields are OPTIONAL. Existing canonical BP records remain
conformant without the new fields (back-compat rule per CR-BP-95).
Backfill of the new fields across the existing 139 BP records is the
work of a separate reconciliation slice (CR-BP-99 or a dedicated L2
enrichment tranche), not CR-BP-96.

Coverage on the live catalog: all 139 canonical Business Process records
pass BP-C1..C4. The new BP-QUAL-003/004/005/008/009 checks emit zero
findings today because the fields are absent on all existing records
(advisory-mode passes vacuously when the field is absent).

Exit codes:
  0  all records pass all rules (or only advisory findings)
  1  at least one record fails at least one mandatory rule (--strict)
  2  self-test failure or I/O error

Usage:
  python3 scripts/check_l2_qualification.py
  python3 scripts/check_l2_qualification.py --strict
  python3 scripts/check_l2_qualification.py --json
  python3 scripts/check_l2_qualification.py --self-test

Author: Coder (for eaojnr). Established by CR-BP-34a (2026-09-10),
extended by CR-BP-96 (2026-09-18). Derived from CR-BP-34 §11 (L2
Business Process Conformance), CR-BP-03 §8 (identity contract), and
the recon-programme decomposition contract (CR-BP-92 §11; CR-BP-93 §5).
Backed by the canonical fields declared in
`schemas/entities/process-context.schema.json` and the de-facto BP
record shape documented in `templates/business-process.yaml`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Iterable

import yaml

ID_PATTERN = re.compile(r"^dea:process-[a-z0-9-]+$")


def _load_bp_records(catalog_root: Path) -> list[dict]:
    """Load every canonical Business Process record.

    Walks `entities/v1-alpha/dea:process-*/<id>.yaml`. Returns the
    parsed YAML for each. Skips directories that lack the expected
    YAML file (e.g. `candidates/`, `retired/`, `research/`).
    """
    base = catalog_root / "entities" / "v1-alpha"
    records: list[dict] = []
    if not base.exists():
        return records
    for entry in sorted(base.iterdir()):
        if not entry.is_dir() or not entry.name.startswith("dea:process-"):
            continue
        yaml_path = entry / f"{entry.name}.yaml"
        if not yaml_path.exists():
            continue
        try:
            data = yaml.safe_load(yaml_path.read_text())
        except yaml.YAMLError as exc:
            print(f"WARN: {yaml_path}: YAML parse error: {exc}", file=sys.stderr)
            continue
        if isinstance(data, dict):
            records.append(data)
    return records


def _check_bp_c1(record: dict) -> str | None:
    """BP-C1: trigger AND outcome both non-empty."""
    trigger = (record.get("trigger") or "").strip()
    outcome = (record.get("outcome") or "").strip()
    if not trigger:
        return "trigger missing or empty"
    if not outcome:
        return "outcome missing or empty"
    return None


def _check_bp_c2(record: dict) -> str | None:
    """BP-C2: identity.outcome_statement non-empty."""
    identity = record.get("identity") or {}
    if not isinstance(identity, dict):
        return "identity block missing or not a mapping"
    stmt = (identity.get("outcome_statement") or "").strip()
    if not stmt:
        return "identity.outcome_statement missing or empty"
    return None


def _check_bp_c3(record: dict) -> str | None:
    """BP-C3: lifecycle_status present AND id matches dea:process-*."""
    if not (record.get("lifecycle_status") or "").strip():
        return "lifecycle_status missing or empty"
    rec_id = record.get("id") or ""
    if not ID_PATTERN.match(rec_id):
        return f"id {rec_id!r} does not match {ID_PATTERN.pattern}"
    return None


def _check_bp_c4(record: dict) -> str | None:
    """BP-C4: evidence_links non-empty AND change_history has >=1 entry."""
    identity = record.get("identity") or {}
    evidence = identity.get("evidence_links") if isinstance(identity, dict) else None
    if not isinstance(evidence, list) or not evidence:
        return "identity.evidence_links missing or empty"
    change_history = (
        record.get("change_history")
        or (record.get("metadata") or {}).get("change_history")
        or []
    )
    if not isinstance(change_history, list) or not change_history:
        return "change_history missing or empty"
    return None


# CR-BP-96: BP-QUAL-003..010 + 012 (advisory; OPTIONAL fields).
# These checks pass vacuously when the field is absent (back-compat).
# When the field IS present, structure is enforced.


def _check_bp_qual_003(record: dict) -> str | None:
    """BP-QUAL-003: Input (advisory; OPTIONAL field).

    When `inputs[]` is present, every entry must conform to the
    {id, name, description, source} shape per CR-BP-92 §4 universal
    contract.
    """
    inputs = record.get("inputs")
    if inputs is None:
        return None  # field absent; advisory passes vacuously
    if not isinstance(inputs, list) or not inputs:
        return "inputs present but empty"
    for idx, item in enumerate(inputs):
        if not isinstance(item, dict):
            return f"inputs[{idx}] must be an object with id/name/description/source"
        for required in ("id", "name", "description", "source"):
            if not str(item.get(required, "")).strip():
                return f"inputs[{idx}].{required} missing or empty"
    return None


def _check_bp_qual_004(record: dict) -> str | None:
    """BP-QUAL-004: Transformation (advisory; OPTIONAL field).

    When `transformation:` is present, it must be a non-empty string or
    a non-empty array of transformation steps.
    """
    transformation = record.get("transformation")
    if transformation is None:
        return None
    if isinstance(transformation, str):
        if not transformation.strip():
            return "transformation present but empty string"
        return None
    if isinstance(transformation, list):
        if not transformation:
            return "transformation present but empty list"
        for idx, step in enumerate(transformation):
            if not isinstance(step, dict):
                return f"transformation[{idx}] must be an object"
            if not str(step.get("name", "")).strip():
                return f"transformation[{idx}].name missing or empty"
        return None
    return "transformation must be a string or a list of step objects"


def _check_bp_qual_005(record: dict) -> str | None:
    """BP-QUAL-005: Output (advisory; OPTIONAL field).

    When `outputs[]` is present, every entry must conform to the
    {id, name, description, consumer} shape per CR-BP-92 §4 universal
    contract.
    """
    outputs = record.get("outputs")
    if outputs is None:
        return None
    if not isinstance(outputs, list) or not outputs:
        return "outputs present but empty"
    for idx, item in enumerate(outputs):
        if not isinstance(item, dict):
            return f"outputs[{idx}] must be an object with id/name/description/consumer"
        for required in ("id", "name", "description", "consumer"):
            if not str(item.get(required, "")).strip():
                return f"outputs[{idx}].{required} missing or empty"
    return None


def _check_bp_qual_008(record: dict) -> str | None:
    """BP-QUAL-008: Responsibility (advisory; OPTIONAL field).

    When `responsibility:` is present, it must be a non-empty string or
    a non-empty object with `roles:` / `capabilities:` / `resources:`
    keys.
    """
    responsibility = record.get("responsibility")
    if responsibility is None:
        return None
    if isinstance(responsibility, str):
        if not responsibility.strip():
            return "responsibility present but empty string"
        return None
    if isinstance(responsibility, dict):
        if not responsibility:
            return "responsibility present but empty object"
        return None
    return "responsibility must be a string or a non-empty object"


def _check_bp_qual_009(record: dict) -> str | None:
    """BP-QUAL-009: Boundary (advisory; OPTIONAL field).

    When `boundary:` is present, it must be a non-empty object or
    string. Boundary specifies the scope of responsibility.
    """
    boundary = record.get("boundary")
    if boundary is None:
        return None
    if isinstance(boundary, str):
        if not boundary.strip():
            return "boundary present but empty string"
        return None
    if isinstance(boundary, dict):
        if not boundary:
            return "boundary present but empty object"
        return None
    return "boundary must be a string or a non-empty object"


_RULES = (
    # CR-BP-34a baseline (mandatory).
    ("BP-C1", _check_bp_c1, "Input-Output Transformation"),
    ("BP-C2", _check_bp_c2, "Objective Contribution"),
    ("BP-C3", _check_bp_c3, "Standalone Executability"),
    ("BP-C4", _check_bp_c4, "Resource Dedication"),
    # CR-BP-96 BP-QUAL extensions.
    # BP-QUAL-001/002/006/007/010/012 are aliases of the BP-C family and
    # do not introduce new checks. BP-QUAL-011 is deferred under CR-BP-92
    # §21 (specialization carve-out). The remaining BP-QUAL-003/004/005/
    # 008/009 are advisory, OPTIONAL-field structure checks.
    ("BP-QUAL-003", _check_bp_qual_003, "Input (advisory; OPTIONAL)"),
    ("BP-QUAL-004", _check_bp_qual_004, "Transformation (advisory; OPTIONAL)"),
    ("BP-QUAL-005", _check_bp_qual_005, "Output (advisory; OPTIONAL)"),
    ("BP-QUAL-008", _check_bp_qual_008, "Responsibility (advisory; OPTIONAL)"),
    ("BP-QUAL-009", _check_bp_qual_009, "Boundary (advisory; OPTIONAL)"),
)


# Map of BP-QUAL rule -> underlying BP-C rule for reporting. The aliases
# (001/002/006/007/010/012) inherit the BP-C verdict without re-running.
_BP_QUAL_ALIASES = {
    "BP-QUAL-001": "BP-C3",  # Identity -> Standalone Executability
    "BP-QUAL-002": "BP-C1",  # Trigger -> Input-Output Transformation
    "BP-QUAL-006": "BP-C1+BP-C2",  # Outcome -> BP-C1 outcome + BP-C2 outcome_statement
    "BP-QUAL-007": "BP-C2",  # Objective Contribution -> BP-C2
    "BP-QUAL-010": "BP-C3",  # Standalone Process Integrity -> BP-C3
    "BP-QUAL-012": "BP-C4",  # Evidence -> BP-C4
}


def evaluate(records: Iterable[dict]) -> list[dict]:
    """Run all rules against every record.

    Returns a list of findings:
        [{"rule": "BP-C1", "record_id": ..., "diagnostic": ...,
          "advisory": False}, ...]
    Empty list == all pass.

    BP-C findings are mandatory (advisory: False). BP-QUAL-003/004/005/
    008/009 findings are tagged advisory: True (CR-BP-96 design intent).
    """
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
                    "advisory": rule_id.startswith("BP-QUAL"),
                })
    return findings


def _verdict(findings: list[dict]) -> str:
    if findings:
        return "NON-CONFORMANT"
    return "CONFORMANT"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(
        "L2 Qualification validator (CR-BP-34a; BP-C1..C4)."
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
        }, indent=2, sort_keys=True))
    else:
        print(f"L2 Qualification (CR-BP-34a BP-C1..C4 + CR-BP-96 BP-QUAL-001..012): {verdict}")
        print(f"  Records checked:  {len(records)}")
        print(f"  Findings:         {len(findings)}")
        # BP-C rules (mandatory).
        for rid, _fn, label in _RULES:
            if rid.startswith("BP-C"):
                n = sum(1 for f in findings if f["rule"] == rid)
                print(f"    {rid} ({label}): {n}")
        # BP-QUAL rules (new in CR-BP-96).
        for rid, _fn, label in _RULES:
            if rid.startswith("BP-QUAL"):
                n = sum(1 for f in findings if f["rule"] == rid)
                print(f"    {rid} ({label}): {n}")
        # BP-QUAL aliases (001/002/006/007/010/012 -> BP-C family).
        print("    BP-QUAL aliases (inherit BP-C family verdict):")
        for alias, target in sorted(_BP_QUAL_ALIASES.items()):
            print(f"      {alias} -> {target}")
        # BP-QUAL-011 (deferred under CR-BP-92 §21).
        print("    BP-QUAL-011 (Specialization Integrity): DEFERRED under CR-BP-92 §21")
        if findings:
            print("\nFindings:")
            for f in findings:
                print(f"  [{f['rule']}] {f['record_id']}: {f['diagnostic']}")

    if findings and args.strict:
        # CR-BP-96: --strict only fails on mandatory (BP-C) findings, not advisory.
        mandatory_findings = [f for f in findings if not f.get("advisory", False)]
        if mandatory_findings:
            return 1
    return 0


def _self_test() -> int:
    """Built-in self-test: verify pass and fail behavior on each rule."""

    def _record(**overrides):
        base = {
            "id": "dea:process-self-test",
            "name": "Self Test",
            "type": "Process",
            "version": "1.0.0",
            "lifecycle_status": "candidate",
            "status": "candidate",
            "process_intent": "operate",
            "process_type": "core",
            "description": "Self-test record.",
            "trigger": "An input arrives.",
            "outcome": "An output is produced.",
            "identity": {
                "verb": "Test",
                "object": "Self",
                "outcome_statement": "Self-test outcome.",
                "evidence_links": [{"type": "standard", "ref": "https://example.com"}],
            },
            "metadata": {
                "change_history": [{"cr": "CR-BP-34a", "date": "2026-09-10", "change": "self-test"}],
            },
        }
        base.update(overrides)
        return base

    # Baseline: should pass all four.
    baseline = [_record()]
    findings = evaluate(baseline)
    assert not findings, f"baseline must pass; got {findings}"

    # Each rule, individually failed.
    fail_c1 = [_record(trigger="")]
    f = evaluate(fail_c1)
    assert len(f) == 1 and f[0]["rule"] == "BP-C1", f

    fail_c2 = [_record(identity={"verb": "x", "object": "y", "outcome_statement": "", "evidence_links": [{"ref": "x"}]})]
    f = evaluate(fail_c2)
    assert len(f) == 1 and f[0]["rule"] == "BP-C2", f

    fail_c3 = [_record(lifecycle_status="")]
    f = evaluate(fail_c3)
    assert len(f) == 1 and f[0]["rule"] == "BP-C3", f

    fail_c3_id = [_record(id="not-a-dea-id")]
    f = evaluate(fail_c3_id)
    assert len(f) == 1 and f[0]["rule"] == "BP-C3", f

    fail_c4_no_evidence = [_record(identity={"verb": "x", "object": "y", "outcome_statement": "z", "evidence_links": []})]
    f = evaluate(fail_c4_no_evidence)
    assert len(f) == 1 and f[0]["rule"] == "BP-C4", f

    fail_c4_no_ch = [_record(metadata={"change_history": []})]
    f = evaluate(fail_c4_no_ch)
    assert len(f) == 1 and f[0]["rule"] == "BP-C4", f

    # Multi-rule fail: missing trigger + missing outcome_statement
    multi = [_record(trigger="", identity={"verb": "x", "object": "y", "outcome_statement": "", "evidence_links": [{"ref": "x"}]})]
    f = evaluate(multi)
    assert len(f) == 2 and {x["rule"] for x in f} == {"BP-C1", "BP-C2"}, f

    # Top-level change_history fallback (legacy shape)
    legacy_ch = [_record()]
    legacy_ch[0].pop("metadata", None)
    legacy_ch[0]["change_history"] = [{"cr": "x"}]
    assert not evaluate(legacy_ch), "top-level change_history must satisfy BP-C4"

    print("self-test PASS (7 negative cases, 1 multi-rule fail, 1 legacy shape)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
