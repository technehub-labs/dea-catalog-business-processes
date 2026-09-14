#!/usr/bin/env python3
"""Lifecycle Discovery Validator (CR-BP-62; DISC-001..008).

Structural validation of lifecycle process-discovery records at
``discovery/v1-alpha/*.yaml`` against
``schemas/discovery/lifecycle-discovery.schema.json`` and the
CR-BP-62 section-16 disposition model. DISC-001..008 are the
machine-checkable face of BP-LIFE-001..015: CI validates structural
completeness; it never admits or rejects canonicality (CR-BP-62 §20).
Canonical admission remains governed by catalog maintainers.

Live-catalog posture at landing: zero discovery records (regression
guard). The gate becomes exercised by CR-BP-63 (Activate/Retire
discovery exercise, 14 records).

CLI:
    python3 scripts/check_lifecycle_discovery.py              human summary
    python3 scripts/check_lifecycle_discovery.py --strict     exit 1 on findings
    python3 scripts/check_lifecycle_discovery.py --json       machine-readable
    python3 scripts/check_lifecycle_discovery.py --self-test  in-process battery

Exit codes: 0 pass; 1 findings under --strict; 2 self-test / I/O error.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema
import yaml

SCHEMA_PATH = "schemas/discovery/lifecycle-discovery.schema.json"
DISCOVERY_GLOB = "discovery/v1-alpha/*.yaml"

DOMAINS = {
    "GovernanceAndExistence",
    "PartyAndRelationship",
    "ProductAndValue",
    "FinanceAndAccounting",
    "AgencyAndOrganization",
    "EnablementAndOperations",
    "StrategyAndDirection",
}

STAGES = {
    "Conceive",
    "Design",
    "Build",
    "Activate",
    "Operate",
    "Improve",
    "Retire",
}

DISPOSITIONS = {
    "ADMIT-CANONICAL",
    "ADMIT-SPECIALIZATION",
    "ADMIT-CROSS-STAGE",
    "RECORD-PATTERN",
    "DEFER",
    "MERGE",
    "RECLASSIFY",
    "REJECT",
}

SCORING_DIMENSIONS = (
    "process_reality",
    "semantic_stability",
    "cross_domain_applicability",
    "boundary_clarity",
    "evidence_strength",
)

# Section-15 process-absence checklist keys.
CONTEXT_CHECKLIST = (
    "concerns_identified",
    "candidates_considered",
    "adjacent_contexts_reviewed",
    "existing_processes_searched",
    "lifecycle_spanning_considered",
    "capability_distinctions_tested",
    "pattern_candidates_considered",
    "evidence_assessed",
)


def _load_schema(catalog_root: Path) -> dict:
    return json.loads((catalog_root / SCHEMA_PATH).read_text())


def _load_records(catalog_root: Path) -> list[tuple[Path, dict]]:
    pairs: list[tuple[Path, dict]] = []
    for path in sorted(catalog_root.glob(DISCOVERY_GLOB)):
        try:
            data = yaml.safe_load(path.read_text())
        except (OSError, yaml.YAMLError):
            data = None
        if isinstance(data, dict):
            pairs.append((path, data))
    return pairs


def _load_bp_names(catalog_root: Path) -> set[str]:
    """Canonical BP record names (DISC-007 duplicate check)."""
    names: set[str] = set()
    for path in sorted(catalog_root.glob("entities/v1-alpha/*/dea:process-*.yaml")):
        try:
            data = yaml.safe_load(path.read_text())
        except (OSError, yaml.YAMLError):
            continue
        if isinstance(data, dict) and data.get("type") == "Process":
            name = data.get("name")
            if isinstance(name, str):
                names.add(name.strip().lower())
    return names


def _check_disc_001(schema: dict):
    def fn(record: dict) -> str | None:
        try:
            jsonschema.validate(record, schema)
        except jsonschema.ValidationError as exc:
            return f"record fails lifecycle-discovery schema: {exc.message}"
        return None
    return fn


def _check_disc_002(record: dict) -> str | None:
    ctx = (record.get("discovery") or {}).get("ecf_context") or {}
    dom, stage = ctx.get("domain"), ctx.get("lifecycle_stage")
    if dom not in DOMAINS:
        return f"ecf_context.domain {dom!r} is not a canonical ECF domain"
    if stage not in STAGES:
        return f"ecf_context.lifecycle_stage {stage!r} is not a canonical ECF stage"
    return None


def _candidates(record: dict) -> list[dict]:
    return (record.get("discovery") or {}).get("candidates") or []


def _check_disc_003(record: dict) -> str | None:
    for cand in _candidates(record):
        ident = cand.get("proposed_identity") or {}
        if not ident.get("verb") or not ident.get("object"):
            return (
                f"candidate {cand.get('name')!r}: proposed_identity must carry "
                f"a non-empty verb and object (identity contract)"
            )
    return None


def _check_disc_004(record: dict) -> str | None:
    for cand in _candidates(record):
        disp = (cand.get("disposition") or {}).get("type")
        if disp not in DISPOSITIONS:
            return (
                f"candidate {cand.get('name')!r}: disposition.type {disp!r} "
                f"is not one of the eight section-16 dispositions"
            )
    return None


def _check_disc_005(record: dict) -> str | None:
    rat = (record.get("discovery") or {}).get("rationale") or {}
    for cand in _candidates(record):
        disp = cand.get("disposition") or {}
        dtype = disp.get("type")
        name = cand.get("name")
        if dtype in {"REJECT", "DEFER", "RECLASSIFY"}:
            if not rat.get("excluded") and not rat.get("unresolved"):
                return (
                    f"candidate {name!r}: {dtype} requires rationale.excluded "
                    f"or rationale.unresolved on the record"
                )
        if dtype == "ADMIT-CANONICAL" and not disp.get("canonical_process_ref"):
            return f"candidate {name!r}: ADMIT-CANONICAL requires disposition.canonical_process_ref"
        if dtype == "ADMIT-SPECIALIZATION" and not disp.get("specialization_of"):
            return f"candidate {name!r}: ADMIT-SPECIALIZATION requires disposition.specialization_of"
    return None


def _check_disc_006(record: dict) -> str | None:
    for cand in _candidates(record):
        disp = (cand.get("disposition") or {}).get("type")
        if disp == "ADMIT-CANONICAL":
            sources = (cand.get("evidence") or {}).get("sources") or []
            if not sources:
                return (
                    f"candidate {cand.get('name')!r}: ADMIT-CANONICAL requires "
                    f"non-empty evidence.sources (BP-LIFE-015 structural face)"
                )
    return None


def _check_disc_007(bp_names: set[str]):
    def fn(record: dict) -> str | None:
        for cand in _candidates(record):
            disp = (cand.get("disposition") or {}).get("type")
            if disp == "ADMIT-CANONICAL":
                name = (cand.get("name") or "").strip().lower()
                if name in bp_names:
                    return (
                        f"candidate {cand.get('name')!r}: name duplicates an "
                        f"existing canonical BP record (BP-LIFE-008/010 structural face)"
                    )
        return None
    return fn


def _check_disc_008(record: dict) -> str | None:
    for cand in _candidates(record):
        scoring = cand.get("scoring") or {}
        total = scoring.get("total")
        if not isinstance(total, int) or isinstance(total, bool) or not 0 <= total <= 10:
            return (
                f"candidate {cand.get('name')!r}: scoring.total must be an "
                f"integer 0-10"
            )
        missing = [d for d in SCORING_DIMENSIONS if d not in scoring]
        if missing:
            return (
                f"candidate {cand.get('name')!r}: scoring missing dimensions "
                f"{missing}"
            )
    return None


def _rule_list(schema: dict, bp_names: set[str]):
    return (
        ("DISC-001", _check_disc_001(schema), "discovery record schema validity"),
        ("DISC-002", _check_disc_002, "canonical ECF coordinate vocabulary"),
        ("DISC-003", _check_disc_003, "candidate identity verb + object"),
        ("DISC-004", _check_disc_004, "disposition vocabulary"),
        ("DISC-005", _check_disc_005, "disposition-conditional rationale"),
        ("DISC-006", _check_disc_006, "ADMIT-CANONICAL requires evidence sources"),
        ("DISC-007", _check_disc_007(bp_names), "ADMIT-CANONICAL duplicate name check"),
        ("DISC-008", _check_disc_008, "canonicality scoring shape"),
    )


def evaluate(pairs, schema: dict, bp_names: set[str]) -> list[dict]:
    findings: list[dict] = []
    for path, record in pairs:
        rec_id = (record.get("discovery") or {}).get("id") or path.name
        for rule_id, fn, _label in _rule_list(schema, bp_names):
            diagnostic = fn(record)
            if diagnostic is not None:
                findings.append({
                    "rule": rule_id,
                    "record_id": rec_id,
                    "diagnostic": diagnostic,
                })
    return findings


def _verdict(findings: list[dict]) -> str:
    return "NON-CONFORMANT" if findings else "CONFORMANT"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--catalog-root", default=".")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    catalog_root = Path(args.catalog_root).resolve()
    try:
        schema = _load_schema(catalog_root)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot load {SCHEMA_PATH}: {exc}", file=sys.stderr)
        return 2
    pairs = _load_records(catalog_root)
    bp_names = _load_bp_names(catalog_root)
    rules = _rule_list(schema, bp_names)
    findings = evaluate(pairs, schema, bp_names)
    verdict = _verdict(findings)

    if args.json:
        print(json.dumps({
            "verdict": verdict,
            "record_count": len(pairs),
            "finding_count": len(findings),
            "findings": findings,
            "rules": [{"id": rid, "name": lbl} for rid, _, lbl in rules],
        }, indent=2, sort_keys=True))
    else:
        print(f"Lifecycle Discovery (CR-BP-62; DISC-001..008): {verdict}")
        print(f"  Discovery records checked: {len(pairs)}")
        print(f"  Findings:                  {len(findings)}")
        for rid, _, lbl in rules:
            n = sum(1 for f in findings if f["rule"] == rid)
            print(f"    {rid} ({lbl}): {n}")
        if findings:
            print("\nFindings:")
            for f in findings:
                print(f"  [{f['rule']}] {f['record_id']}: {f['diagnostic']}")

    if findings and args.strict:
        return 1
    return 0


def _fixture(disposition: str = "RECORD-PATTERN", **overrides) -> dict:
    cand = {
        "name": "Transition to Service",
        "proposed_identity": {"verb": "Transition", "object": "Service", "scope": "enterprise"},
        "trigger": "Approved object is ready for operational transition.",
        "inputs": "Validated product/service/capability.",
        "transformation": "Move the object from prepared state into operational service.",
        "outcome": "Object is accepted into operational service.",
        "boundary": "Begins at readiness approval; ends at operational acceptance.",
        "actors": "Service owner; operations.",
        "controls": "Launch approval policy.",
        "evidence": {"sources": ["ITIL service transition"], "evidence_strength": "moderate"},
        "evaluation": {k: "assessed" for k in (
            "process_reality", "transformation", "trigger", "outcome", "boundary",
            "semantic_identity", "cross_context_stability", "cross_domain_applicability",
            "ecf_independence", "duplication", "composition", "capability_distinction",
            "governance_distinction", "lifecycle_span",
        )},
        "scoring": {
            "process_reality": 2, "semantic_stability": 2, "cross_domain_applicability": 2,
            "boundary_clarity": 1, "evidence_strength": 1, "total": 8,
            "rationale": "Established transformation with workable boundary.",
        },
        "disposition": {"type": disposition, "related_contexts": []},
    }
    for key, value in overrides.items():
        cand[key] = value
    return {
        "discovery": {
            "id": "dea:discovery-enablement-and-operations-activate",
            "ecf_context": {"domain": "EnablementAndOperations", "lifecycle_stage": "Activate"},
            "candidates": [cand],
            "context_evaluation": {k: True for k in CONTEXT_CHECKLIST} | {"process_empty": False},
            "rationale": {
                "included": "Transition-to-service candidates evaluated.",
                "excluded": "Capability-only candidates reclassified.",
                "unresolved": "Cross-stage span of Deploy/Cut Over unresolved.",
            },
        }
    }


def _self_test() -> int:
    schema = {
        "type": "object",
        "required": ["discovery"],
        "properties": {"discovery": {"type": "object", "required": ["id"]}},
    }
    bp_names = {"operate quality control"}
    rules = dict((rid, fn) for rid, fn, _ in _rule_list(schema, bp_names))

    cases: list[tuple[str, str, bool]] = []  # (rule, case-label, expect_finding)

    good = _fixture()
    bad_schema = {"not_discovery": True}
    bad_domain = _fixture()
    bad_domain["discovery"]["ecf_context"]["domain"] = "Sales"
    bad_stage = _fixture()
    bad_stage["discovery"]["ecf_context"]["stage"] = "Activate"
    bad_identity = _fixture(proposed_identity={"verb": "", "object": "Service"})
    bad_disp = _fixture(disposition="MAYBE")
    reject_no_rationale = _fixture(disposition="REJECT")
    reject_no_rationale["discovery"]["rationale"]["excluded"] = ""
    reject_no_rationale["discovery"]["rationale"]["unresolved"] = ""
    admit_no_ref = _fixture(disposition="ADMIT-CANONICAL")
    spec_no_ref = _fixture(disposition="ADMIT-SPECIALIZATION")
    admit_no_evidence = _fixture(disposition="ADMIT-CANONICAL")
    admit_no_evidence["discovery"]["candidates"][0]["disposition"]["canonical_process_ref"] = "dea:process-x"
    admit_no_evidence["discovery"]["candidates"][0]["evidence"]["sources"] = []
    admit_dup = _fixture(name="Operate Quality Control", disposition="ADMIT-CANONICAL")
    admit_dup["discovery"]["candidates"][0]["disposition"]["canonical_process_ref"] = "dea:process-x"
    bad_total = _fixture()
    bad_total["discovery"]["candidates"][0]["scoring"]["total"] = 11
    missing_dim = _fixture()
    del missing_dim["discovery"]["candidates"][0]["scoring"]["boundary_clarity"]

    checks = [
        ("DISC-001", good, False), ("DISC-001", bad_schema, True),
        ("DISC-002", good, False), ("DISC-002", bad_domain, True),
        ("DISC-003", good, False), ("DISC-003", bad_identity, True),
        ("DISC-004", good, False), ("DISC-004", bad_disp, True),
        ("DISC-005", good, False), ("DISC-005", reject_no_rationale, True),
        ("DISC-005", admit_no_ref, True), ("DISC-005", spec_no_ref, True),
        ("DISC-006", admit_no_evidence, True), ("DISC-006", admit_dup, False),
        ("DISC-007", admit_dup, True), ("DISC-007", good, False),
        ("DISC-008", bad_total, True), ("DISC-008", missing_dim, True),
        ("DISC-008", good, False),
    ]
    failures = 0
    for rid, record, expect in checks:
        diagnostic = rules[rid](record)
        got = diagnostic is not None
        if got != expect:
            print(f"self-test FAIL: {rid} expected finding={expect}, got={got} ({diagnostic})")
            failures += 1
    if failures:
        print(f"self-test FAIL ({failures} cases)")
        return 2
    print(f"self-test PASS ({len(checks)} cases)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
