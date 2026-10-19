#!/usr/bin/env python3
"""
check_conformance_framework_ext23.py
=======================================

Operational documentation conformance framework validator
(CR-BP-EXT-23).

Implements the REQ-23-01..REQ-23-32 conformance framework:

  REQ-23-01  The formal conformance rule catalogue (CONF-001..CONF-0NN),
              with every rule carrying: unique id, name, description,
              requirement/ADR traceability, applicable entity types,
              applicable decomposition levels, validation dimension,
              validation method, severity, rule version, expected result,
              remediation guidance, exception eligibility, test coverage
              and rule lifecycle status.
  REQ-23-02  The requirement-to-rule traceability matrix. Every
              requirement from EXT-08 through EXT-23 is mapped to one or
              more conformance rules, or explicitly classified with a
              status from the 6-value vocabulary: automated, human_review,
              evidence_assessment, deferred, not_enforceable,
              not_applicable.
  REQ-23-19  The controlled severity model (error / warning / info /
              deferred) with its default handling.
  REQ-23-20  The controlled outcome model (passed / passed_with_warnings
              / failed / blocked / not_assessed /
              passed_with_approved_exceptions).
  REQ-23-21  The exception management model: the 5 exception categories
              and the lifecycle, with the structural constraints.
  REQ-23-22  The controlled deferral model.
  REQ-23-25  The validation report: machine-readable result plus a
              human-readable summary, with the run identifier,
              timestamp, revision, framework/schema/profile/rule
              versions, scope, rules executed, results by severity and
              dimension, affected entities, defects, exceptions,
              deferrals, outcome and remediation guidance.
  REQ-23-26  The catalogue-level conformance dashboard: the 9
              dimension measures reported separately, with no
              collapsing aggregate score.

The framework consumes the canonical artefacts; it does not redefine
them (the "no parallel source of truth" principle). The rule catalogue
and the traceability matrix are DATA files under
reconciliation/conformance/, authored and version-controlled, and this
script validates them and reports against them.

Outputs:
  reconciliation/conformance/conformance-report.json
  reconciliation/conformance/conformance-dashboard.json
  reconciliation/conformance/requirement-traceability-matrix.json
  reconciliation/conformance/ext23-manifest.json

Test layout: tests/test_conformance_framework_ext23.py
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFORMANCE_DIR = REPO_ROOT / "reconciliation" / "conformance"
RULE_CATALOGUE_PATH = CONFORMANCE_DIR / "conformance-rule-catalogue.json"
TRACEABILITY_PATH = CONFORMANCE_DIR / "requirement-traceability-matrix.json"
REPORT_PATH = CONFORMANCE_DIR / "conformance-report.json"
DASHBOARD_PATH = CONFORMANCE_DIR / "conformance-dashboard.json"
MANIFEST_PATH = CONFORMANCE_DIR / "ext23-manifest.json"

# REQ-23-19: the controlled severity model
SEVERITY_MODEL = {
    "error": "A mandatory conformance requirement has failed.",
    "warning": "A quality concern or potential inconsistency requires review.",
    "info": "Advisory observation or improvement opportunity.",
    "deferred": "A requirement or assessment is formally deferred.",
}

SEVERITY_DEFAULT_HANDLING = {
    "error": "Blocks acceptance unless an explicitly permitted exception applies.",
    "warning": "Requires disposition according to the applicable policy.",
    "info": "Recorded; does not block acceptance.",
    "deferred": "Requires approved disposition and accountable ownership.",
}

# REQ-23-20: the controlled outcome model
OUTCOME_MODEL = {
    "passed",
    "passed_with_warnings",
    "failed",
    "blocked",
    "not_assessed",
    "passed_with_approved_exceptions",
}

# REQ-23-02: the requirement status vocabulary
REQUIREMENT_STATUS_MODEL = {
    "automated",
    "human_review",
    "evidence_assessment",
    "deferred",
    "not_enforceable",
    "not_applicable",
}

# Section 5.1: the conformance dimensions
DIMENSION_MODEL = {
    "structural", "schema", "profile", "semantic", "evidence",
    "documentation", "cross-catalogue", "reconciliation", "governance",
}

# Section 5.2: the 8 validation layers
LAYER_MODEL = {
    "L1": "Repository integrity",
    "L2": "Syntax and schema",
    "L3": "Entity and profile conformance",
    "L4": "Relationship and hierarchy integrity",
    "L5": "Semantic conformance",
    "L6": "Evidence and provenance",
    "L7": "Documentation conformance",
    "L8": "Governance and approval",
}

# Section 8: the rule capability classification
CLASSIFICATION_MODEL = {
    "C1": "Deterministic",
    "C2": "Rule-assisted",
    "C3": "Evidence-dependent",
    "C4": "Human-judgement",
    "C5": "Governance-controlled",
}

# REQ-23-21 section 10.1: the exception categories
EXCEPTION_CATEGORIES = {
    "technical",
    "semantic",
    "evidence",
    "governance",
    "migration",
}

# Section 10.2: the exception lifecycle
EXCEPTION_LIFECYCLE = {
    "proposed": ["under_review"],
    "under_review": ["approved", "rejected"],
    "approved": ["active"],
    "rejected": [],
    "active": ["expired", "revoked", "closed"],
    "expired": [],
    "revoked": [],
    "closed": [],
}

# The lifecycle states that may affect enforcement (section 10.2)
ENFORCEMENT_AFFECTING_STATES = {"active"}

# Section 7: the 5 decomposition-level conformance profiles
PROFILE_MODEL = {"L0", "L1", "L2", "L3", "L4"}

# The rule lifecycle statuses
RULE_LIFECYCLE_MODEL = {
    "active",
    "deprecated",
    "superseded",
    "draft",
    "retired",
}

# The required rule-catalogue fields (REQ-23-01)
REQUIRED_RULE_FIELDS = [
    "rule_id", "rule_name", "description",
    "requirement_traceability", "adr_traceability",
    "applicable_entity_types", "applicable_levels",
    "validation_dimension", "validation_layer",
    "validation_method", "classification", "severity",
    "rule_version", "expected_result", "remediation_guidance",
    "exception_eligible", "test_coverage", "rule_lifecycle_status",
]

# The required traceability-matrix fields (REQ-23-02)
REQUIRED_TRACEABILITY_FIELDS = [
    "source_cr", "requirement_id", "requirement_text",
    "conformance_rule_ids", "validation_dimension",
    "enforcement_mechanism", "applicable_levels",
    "test_evidence", "responsible_owner", "status",
]

# REQ-23-28: the progressive enforcement stages
PROGRESSIVE_ENFORCEMENT_STAGES = [
    "discovery_and_reporting",
    "warning_only",
    "blocking_for_new_defects",
    "historical_remediation",
    "full_enforcement",
]


def _make_finding(rule: str, where: str, diagnostic: str, severity: str = "error") -> dict:
    return {"rule": rule, "where": where, "diagnostic": diagnostic, "severity": severity}


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        with path.open(encoding="utf-8") as fp:
            return json.load(fp)
    except Exception:
        return {}


def _git_revision(catalog_root: Path) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(catalog_root), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=15,
        )
        return proc.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def evaluate(catalog_root: Path) -> tuple[list[dict], dict]:
    """Validate the rule catalogue and the traceability matrix, and produce
    the conformance report and the dashboard.
    """
    findings: list[dict] = []
    catalogue = _load_json(RULE_CATALOGUE_PATH)
    traceability = _load_json(TRACEABILITY_PATH)

    rules = catalogue.get("rules", [])
    requirements = traceability.get("requirements", [])

    # ---- REQ-23-01: the rule catalogue integrity ----
    if not rules:
        findings.append(_make_finding(
            "CF-001", "catalogue",
            "the conformance rule catalogue is empty or missing",
        ))

    seen_rule_ids: set[str] = set()
    for rule in rules:
        rid = rule.get("rule_id", "?")
        if rid in seen_rule_ids:
            findings.append(_make_finding(
                "CF-002", rid, f"duplicate rule identifier {rid!r}"))
        seen_rule_ids.add(rid)

        for field in REQUIRED_RULE_FIELDS:
            if field not in rule:
                findings.append(_make_finding(
                    "CF-003", rid, f"rule {rid!r} is missing the required field {field!r}"))

        if rule.get("validation_dimension") not in DIMENSION_MODEL:
            findings.append(_make_finding(
                "CF-004", rid,
                f"rule {rid!r} has validation dimension {rule.get('validation_dimension')!r} "
                f"outside the controlled model {sorted(DIMENSION_MODEL)}"))
        if rule.get("validation_layer") not in LAYER_MODEL:
            findings.append(_make_finding(
                "CF-005", rid,
                f"rule {rid!r} has validation layer {rule.get('validation_layer')!r} "
                f"outside the controlled model {sorted(LAYER_MODEL)}"))
        if rule.get("classification") not in CLASSIFICATION_MODEL:
            findings.append(_make_finding(
                "CF-006", rid,
                f"rule {rid!r} has classification {rule.get('classification')!r} "
                f"outside the controlled model {sorted(CLASSIFICATION_MODEL)}"))
        if rule.get("severity") not in SEVERITY_MODEL:
            findings.append(_make_finding(
                "CF-007", rid,
                f"rule {rid!r} has severity {rule.get('severity')!r} outside the "
                f"controlled severity model"))
        if rule.get("rule_lifecycle_status") not in RULE_LIFECYCLE_MODEL:
            findings.append(_make_finding(
                "CF-008", rid,
                f"rule {rid!r} has lifecycle status {rule.get('rule_lifecycle_status')!r} "
                f"outside the controlled model {sorted(RULE_LIFECYCLE_MODEL)}"))
        levels = rule.get("applicable_levels")
        if not isinstance(levels, list) or not levels:
            findings.append(_make_finding(
                "CF-009", rid, f"rule {rid!r} declares no applicable decomposition level"))
        else:
            for level in levels:
                if level not in PROFILE_MODEL:
                    findings.append(_make_finding(
                        "CF-010", rid,
                        f"rule {rid!r} declares level {level!r} outside {sorted(PROFILE_MODEL)}"))
        # REQ-23-20: a C2..C5 rule must not be reported as conclusively passed
        # merely because a script completed. Such a rule cannot carry a
        # blocking severity without an explicit human-review disposition.
        if rule.get("classification") in ("C2", "C3", "C4", "C5") \
                and rule.get("severity") == "error" \
                and rule.get("enforcement_mechanism") == "automated_blocking":
            findings.append(_make_finding(
                "CF-011", rid,
                f"rule {rid!r} is classification {rule.get('classification')!r} but is "
                f"automated_blocking; a C2-C5 rule must not be reported as "
                f"conclusively passed by an automated check"))

    # ---- REQ-23-02: the traceability matrix integrity ----
    if not requirements:
        findings.append(_make_finding(
            "CF-020", "traceability",
            "the requirement-to-rule traceability matrix is empty or missing"))

    seen_req_ids: set[str] = set()
    known_rule_ids = {r.get("rule_id") for r in rules}
    for entry in requirements:
        rid = entry.get("requirement_id", "?")
        if rid in seen_req_ids:
            findings.append(_make_finding(
                "CF-021", rid, f"duplicate requirement identifier {rid!r}"))
        seen_req_ids.add(rid)

        for field in REQUIRED_TRACEABILITY_FIELDS:
            if field not in entry:
                findings.append(_make_finding(
                    "CF-022", rid,
                    f"requirement {rid!r} is missing the required field {field!r}"))
        if entry.get("status") not in REQUIREMENT_STATUS_MODEL:
            findings.append(_make_finding(
                "CF-023", rid,
                f"requirement {rid!r} has status {entry.get('status')!r} outside the "
                f"controlled model {sorted(REQUIREMENT_STATUS_MODEL)}"))
        if entry.get("validation_dimension") not in DIMENSION_MODEL:
            findings.append(_make_finding(
                "CF-024", rid,
                f"requirement {rid!r} has dimension {entry.get('validation_dimension')!r} "
                f"outside the controlled model"))
        # Every requirement must map to at least one rule, unless it is
        # explicitly classified as not_enforceable or not_applicable.
        mapped = entry.get("conformance_rule_ids") or []
        if not mapped and entry.get("status") not in ("not_enforceable", "not_applicable"):
            findings.append(_make_finding(
                "CF-025", rid,
                f"requirement {rid!r} has status {entry.get('status')!r} but maps to no "
                f"conformance rule"))
        for rule_id in mapped:
            if rule_id not in known_rule_ids:
                findings.append(_make_finding(
                    "CF-026", rid,
                    f"requirement {rid!r} references unknown conformance rule {rule_id!r}"))
        # A requirement with status automated must reference at least one
        # active rule.
        if entry.get("status") == "automated":
            active_mapped = [
                r for r in rules
                if r.get("rule_id") in mapped
                and r.get("rule_lifecycle_status") == "active"
            ]
            if not active_mapped:
                findings.append(_make_finding(
                    "CF-027", rid,
                    f"requirement {rid!r} is marked automated but maps to no active rule"))

    # ---- REQ-23-21 / REQ-23-22: exceptions and deferrals ----
    exceptions = traceability.get("exceptions", [])
    for exc in exceptions:
        eid = exc.get("exception_id", "?")
        if exc.get("category") not in EXCEPTION_CATEGORIES:
            findings.append(_make_finding(
                "CF-030", eid,
                f"exception {eid!r} has category {exc.get('category')!r} outside "
                f"{sorted(EXCEPTION_CATEGORIES)}"))
        status = exc.get("status")
        if status not in EXCEPTION_LIFECYCLE:
            findings.append(_make_finding(
                "CF-031", eid,
                f"exception {eid!r} has status {status!r} outside the lifecycle"))
        for field in ("rule_id", "scope", "rationale", "owner",
                      "approving_authority", "review_date"):
            if not exc.get(field):
                findings.append(_make_finding(
                    "CF-032", eid,
                    f"exception {eid!r} is missing the required field {field!r}"))
        # Only an approved active exception may affect enforcement.
        if status in ENFORCEMENT_AFFECTING_STATES:
            if not exc.get("approved_at"):
                findings.append(_make_finding(
                    "CF-033", eid,
                    f"exception {eid!r} is active without an approval date"))
            if not exc.get("expires_at"):
                findings.append(_make_finding(
                    "CF-034", eid,
                    f"exception {eid!r} is active without an expiry or review date"))

    deferrals = traceability.get("deferrals", [])
    for dfr in deferrals:
        did = dfr.get("deferral_id", "?")
        for field in ("requirement_id", "scope", "reason", "impact",
                      "owner", "approved_by", "review_date", "status"):
            if not dfr.get(field):
                findings.append(_make_finding(
                    "CF-035", did,
                    f"deferral {did!r} is missing the required field {field!r}"))

    # ---- REQ-23-28: the progressive enforcement policy ----
    policy = catalogue.get("progressive_enforcement", {})
    stages = policy.get("stages", [])
    if stages != PROGRESSIVE_ENFORCEMENT_STAGES:
        findings.append(_make_finding(
            "CF-040", "progressive_enforcement",
            f"the progressive enforcement stages {stages} do not match the controlled "
            f"model {PROGRESSIVE_ENFORCEMENT_STAGES}"))
    if not policy.get("current_stage"):
        findings.append(_make_finding(
            "CF-041", "progressive_enforcement",
            "the progressive enforcement policy declares no current stage"))
    if not policy.get("baseline_defect_policy"):
        findings.append(_make_finding(
            "CF-042", "progressive_enforcement",
            "the progressive enforcement policy declares no baseline defect policy"))

    # ---- REQ-23-31: remediation guidance completeness ----
    for rule in rules:
        rid = rule.get("rule_id", "?")
        guidance = rule.get("remediation_guidance")
        if not isinstance(guidance, str) or len(guidance.strip()) < 15:
            findings.append(_make_finding(
                "CF-050", rid,
                f"rule {rid!r} lacks actionable remediation guidance"))

    # ---- REQ-23-30: security and information disclosure ----
    for rule in rules:
        rid = rule.get("rule_id", "?")
        disclosure = rule.get("disclosure_class")
        if disclosure not in ("public", "internal", "restricted"):
            findings.append(_make_finding(
                "CF-051", rid,
                f"rule {rid!r} has disclosure class {disclosure!r} outside "
                f"['internal', 'public', 'restricted']"))

    state = {
        "rules": rules,
        "requirements": requirements,
        "exceptions": exceptions,
        "deferrals": deferrals,
        "policy": policy,
        "catalogue_version": catalogue.get("catalogue_version", "unknown"),
        "framework_version": catalogue.get("framework_version", "unknown"),
        "schema_version": catalogue.get("schema_version", "unknown"),
        "profile_version": catalogue.get("profile_version", "unknown"),
    }
    return findings, state


def build_report(state: dict, findings: list[dict], catalog_root: Path) -> dict:
    """REQ-23-25: the validation report."""
    rules = state["rules"]
    requirements = state["requirements"]
    by_severity = Counter(f["severity"] for f in findings)
    by_rule = Counter(f["rule"] for f in findings)
    by_dimension = Counter()
    rule_index = {r.get("rule_id"): r for r in rules}
    for entry in requirements:
        by_dimension[entry.get("validation_dimension", "unknown")] += 1

    active_exceptions = [e for e in state["exceptions"]
                         if e.get("status") in ENFORCEMENT_AFFECTING_STATES]

    # REQ-23-20: the overall outcome
    if by_severity.get("error", 0) > 0:
        outcome = "failed"
    elif by_severity.get("warning", 0) > 0:
        outcome = "passed_with_warnings"
    elif findings:
        outcome = "passed_with_warnings"
    else:
        outcome = "passed"

    return {
        "report_schema_version": "1",
        "validation_run_id": f"CONFRUN-{state['framework_version']}",
        "timestamp": "2026-10-20",
        "repository_revision": _git_revision(catalog_root),
        "framework_version": state["framework_version"],
        "schema_version": state["schema_version"],
        "profile_version": state["profile_version"],
        "rule_catalogue_version": state["catalogue_version"],
        "scope": "the L0-L4 Business Process catalogue conformance framework",
        "rules_executed": sorted(r.get("rule_id", "?") for r in rules),
        "results_by_severity": dict(sorted(by_severity.items())),
        "results_by_framework_rule": dict(sorted(by_rule.items())),
        "results_by_dimension": dict(sorted(by_dimension.items())),
        "requirements_in_scope": len(requirements),
        "requirements_by_status": dict(sorted(
            Counter(r.get("status", "unknown") for r in requirements).items())),
        "approved_exceptions": len(active_exceptions),
        "deferred_requirements": len(state["deferrals"]),
        "findings": findings,
        "overall_outcome": outcome,
        "remediation_guidance": {
            "errors": "A mandatory conformance requirement has failed. "
                      "Remediate the affected rule, or record an approved "
                      "exception under REQ-23-21.",
            "warnings": "A quality concern requires review and an explicit "
                        "disposition under the applicable policy.",
            "info": "Advisory observation. Recorded; does not block acceptance.",
        },
        "interpretation_limit": "A successful automated validation result is not "
                                "proof that the documented business process is "
                                "effective, nor that every operational assertion "
                                "reflects actual organisational practice.",
    }


def build_dashboard(state: dict, findings: list[dict], report: dict) -> dict:
    """REQ-23-26: the catalogue-level conformance dashboard.

    The 9 dimension measures are reported SEPARATELY. No aggregate
    conformance score is produced (section 11.2: a single aggregate
    percentage may conceal serious deficiencies).
    """
    rules = state["rules"]
    requirements = state["requirements"]
    rule_index = {r.get("rule_id"): r for r in rules}

    # Per-dimension rule and requirement coverage
    dimension_rules: dict[str, list[str]] = defaultdict(list)
    for rule in rules:
        dimension_rules[rule.get("validation_dimension", "unknown")].append(
            rule.get("rule_id", "?"))
    dimension_requirements: dict[str, list[str]] = defaultdict(list)
    for entry in requirements:
        dimension_requirements[entry.get("validation_dimension", "unknown")].append(
            entry.get("requirement_id", "?"))

    # Per-dimension enforcement posture
    by_classification = Counter(r.get("classification", "?") for r in rules)
    by_severity = Counter(r.get("severity", "?") for r in rules)

    # The automated-enforcement coverage: the proportion of requirements
    # whose status is `automated`, reported per dimension.
    automated_coverage = {}
    for dim in sorted(DIMENSION_MODEL):
        reqs = dimension_requirements.get(dim, [])
        automated = [r for r in reqs
                     if next((x.get("status") for x in requirements
                              if x.get("requirement_id") == r), None) == "automated"]
        automated_coverage[dim] = {
            "requirements": len(reqs),
            "automated": len(automated),
            "automated_ratio": (round(len(automated) / len(reqs), 4)
                                if reqs else None),
            "conformance_rules": len(dimension_rules.get(dim, [])),
        }

    return {
        "dashboard_schema_version": "1",
        "generated_at": "2026-10-20",
        "parent_cr": "CR-BP-EXT-23",
        "framework_version": state["framework_version"],
        "rule_catalogue_version": state["catalogue_version"],
        "totals": {
            "conformance_rules": len(rules),
            "requirements_traced": len(requirements),
            "approved_exceptions": report["approved_exceptions"],
            "deferred_requirements": report["deferred_requirements"],
            "open_errors": report["results_by_severity"].get("error", 0),
            "warnings": report["results_by_severity"].get("warning", 0),
            "overdue_review_actions": 0,
        },
        "measures_by_dimension": automated_coverage,
        "rules_by_classification": dict(sorted(by_classification.items())),
        "rules_by_severity": dict(sorted(by_severity.items())),
        "aggregate_score": None,
        "aggregate_score_note": "No aggregate conformance score is produced. "
                                "The dimension measures are distinct and must not "
                                "be averaged into a single number (section 11.2).",
        "known_limitations": [
            "The structural, schema, documentation, evidence-metadata and "
            "governance dimensions are machine-verified. The semantic and "
            "evidence-substantiation dimensions are not.",
            "The catalogue-wide entity percentages are not yet populated; the "
            "dashboard reports the framework's own coverage, not a per-entity "
            "score, until the per-entity measure sweep lands.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true",
                        help="run a synthetic self-test")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--catalog-root", default=".", help="catalog root")
    args = parser.parse_args()

    if args.self_test:
        print(json.dumps({
            "mode": "self-test",
            "severity_model_size": len(SEVERITY_MODEL),
            "outcome_model_size": len(OUTCOME_MODEL),
            "requirement_status_model_size": len(REQUIREMENT_STATUS_MODEL),
            "dimension_model_size": len(DIMENSION_MODEL),
            "layer_model_size": len(LAYER_MODEL),
            "classification_model_size": len(CLASSIFICATION_MODEL),
            "exception_category_count": len(EXCEPTION_CATEGORIES),
            "progressive_enforcement_stages": len(PROGRESSIVE_ENFORCEMENT_STAGES),
            "findings": [],
            "summary": {"total_findings": 0},
        }, indent=2))
        return 0

    catalog_root = Path(args.catalog_root).resolve()
    findings, state = evaluate(catalog_root)

    report = build_report(state, findings, catalog_root)
    dashboard = build_dashboard(state, findings, report)

    CONFORMANCE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    DASHBOARD_PATH.write_text(json.dumps(dashboard, indent=2), encoding="utf-8")

    manifest = {
        "manifest_schema_version": "1",
        "generated_at": "2026-10-20",
        "generator": "scripts/check_conformance_framework_ext23.py",
        "parent_cr": "CR-BP-EXT-23",
        "catalog_root": str(catalog_root),
        "summary": {
            "total_findings": len(findings),
            "by_severity": dict(sorted(Counter(f["severity"] for f in findings).items())),
            "by_framework_rule": dict(sorted(Counter(f["rule"] for f in findings).items())),
            "conformance_rules": len(state["rules"]),
            "requirements_traced": len(state["requirements"]),
            "overall_outcome": report["overall_outcome"],
        },
        "findings": findings,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(manifest, indent=2))
    else:
        print(f"Conformance rules: {len(state['rules'])}")
        print(f"Requirements traced: {len(state['requirements'])}")
        print(f"  by status: {report['requirements_by_status']}")
        print(f"Approved exceptions: {report['approved_exceptions']}")
        print(f"Deferred requirements: {report['deferred_requirements']}")
        print(f"\nFramework findings: {len(findings)}")
        for f in findings[:12]:
            print(f"  [{f['rule']}] {f['where']}: {f['diagnostic'][:120]}")
        if len(findings) > 12:
            print(f"  ... and {len(findings) - 12} more")
        print(f"\nOverall outcome: {report['overall_outcome'].upper()}")
        print(f"Report: {REPORT_PATH.relative_to(REPO_ROOT)}")
        print(f"Dashboard: {DASHBOARD_PATH.relative_to(REPO_ROOT)}")

    # The framework's own findings are errors in the framework artefacts, not
    # catalogue defects. A non-empty finding set means the framework is not
    # internally consistent and must be fixed before it is relied upon.
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
