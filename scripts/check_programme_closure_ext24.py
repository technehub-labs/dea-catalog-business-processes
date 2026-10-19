#!/usr/bin/env python3
"""
check_programme_closure_ext24.py
================================

Programme closure + operational governance validator (CR-BP-94-EXT-24).

Implements the closure-matters regime across REQ-24-01..REQ-24-46, scoped
to the foundation slice:

  REQ-24-01..05  Programme closure assessment (closure matrix)
  REQ-24-06..08  Authoritative catalogue baseline
  REQ-24-09      Governance roles register
  REQ-24-10      Ownership register (L2 Business Process dispositions)
  REQ-24-13      Entity lifecycle register
  REQ-24-21      Exception register
  REQ-24-22      Deferred-work register
  REQ-24-39..40  Improvement backlog + classification

Outputs:
  reconciliation/closure/ext24-manifest.json

Test layout: tests/test_programme_closure_ext24.py
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
CLOSURE_DIR = REPO_ROOT / "reconciliation" / "closure"
CLOSURE_MATRIX = CLOSURE_DIR / "programme-closure-matrix.json"
BASELINE = CLOSURE_DIR / "catalogue-baseline.json"
RESIDUAL_GAPS = CLOSURE_DIR / "residual-gap-register.json"
GOVERNANCE_ROLES = CLOSURE_DIR / "governance-roles.json"
OWNERSHIP_REGISTER = CLOSURE_DIR / "ownership-register.json"
LIFECYCLE_REGISTER = CLOSURE_DIR / "lifecycle-register.json"
EXCEPTION_REGISTER = CLOSURE_DIR / "exception-register.json"
DEFERRED_REGISTER = CLOSURE_DIR / "deferred-work-register.json"
IMPROVEMENT_BACKLOG = CLOSURE_DIR / "improvement-backlog.json"
MANIFEST = CLOSURE_DIR / "ext24-manifest.json"

# REQ-24-13 entity lifecycle vocabulary
LIFECYCLE_STATES = {
    "proposed", "under_review", "approved", "active",
    "superseded", "deprecated", "retired",
}

# REQ-24-21 exception categories (reused from EXT-23)
EXCEPTION_CATEGORIES = {"technical", "semantic", "evidence", "governance", "migration"}

# REQ-24-39/40 improvement categories
IMPROVEMENT_CATEGORIES = {
    "defect_correction", "completeness_improvement", "semantic_improvement",
    "structural_improvement", "metamodel_alignment", "automation_improvement",
    "governance_improvement", "integration_improvement", "innovation",
}


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as fp:
        return json.load(fp)


def _git_revision() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"],
                              capture_output=True, text=True, timeout=15,
                              cwd=str(REPO_ROOT)).stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def _make_finding(rule: str, where: str, diagnostic: str, severity: str = "error") -> dict:
    return {"rule": rule, "where": where, "diagnostic": diagnostic, "severity": severity}


def evaluate() -> tuple[list[dict], dict]:
    """Validate every closure artefact and produce the manifest payload."""
    findings: list[dict] = []

    # ---- REQ-24-01..05: the closure matrix ----
    cm = _load_json(CLOSURE_MATRIX)
    crs = cm.get("crs", [])
    if not crs:
        findings.append(_make_finding(
            "CG-001", "closure-matrix",
            "the programme closure matrix is empty or missing"))
    valid_statuses = {"completed", "completed_with_approved_exceptions",
                      "partially_completed", "deferred", "blocked",
                      "not_started", "not_applicable"}
    for entry in crs:
        cid = entry.get("cr_id", "?")
        for field in ("cr_id", "title", "approved_scope",
                      "implementation_status", "closure_status",
                      "acceptance_criteria_status", "validation_evidence",
                      "outstanding_issues", "approved_deviations",
                      "deferred_requirements", "closure_recommendation"):
            value = entry.get(field)
            if value is None:
                findings.append(_make_finding(
                    "CG-002", cid, f"closure entry {cid!r} missing field {field!r}"))
            elif isinstance(value, str) and not value.strip():
                findings.append(_make_finding(
                    "CG-002", cid, f"closure entry {cid!r} has empty field {field!r}"))
        if entry.get("closure_status") not in valid_statuses:
            findings.append(_make_finding(
                "CG-003", cid,
                f"closure entry {cid!r} has status "
                f"{entry.get('closure_status')!r} outside {sorted(valid_statuses)}"))

    # ---- REQ-24-06..08: the catalogue baseline ----
    base = _load_json(BASELINE)
    for key in ("baseline_revision", "baseline_date", "entity_population",
                "schema_versions", "profile_versions", "vocabulary_versions",
                "validation_rule_versions", "reconciliation_status",
                "evidence_status", "exception_status", "deferred_work",
                "known_limitations"):
        if key not in base:
            findings.append(_make_finding(
                "CG-010", "baseline",
                f"catalogue baseline is missing the required field {key!r}"))

    # ---- REQ-24-09: governance roles ----
    roles = _load_json(GOVERNANCE_ROLES).get("roles", [])
    required_role_fields = ["role_id", "role_name", "primary_responsibility",
                             "mapped_to", "scope"]
    for role in roles:
        rid = role.get("role_id", "?")
        for field in required_role_fields:
            if not role.get(field):
                findings.append(_make_finding(
                    "CG-020", rid, f"role {rid!r} is missing field {field!r}"))

    # ---- REQ-24-10: ownership register ----
    own = _load_json(OWNERSHIP_REGISTER)
    dispositions = own.get("dispositions", [])
    if not dispositions:
        findings.append(_make_finding(
            "CG-030", "ownership",
            "the ownership register carries no L2 Business Process dispositions"))
    for d in dispositions:
        bp_id = d.get("bp_id", "?")
        for field in ("bp_id", "bp_name", "owner", "owner_status", "review_due"):
            if not d.get(field):
                findings.append(_make_finding(
                    "CG-031", bp_id,
                    f"ownership disposition {bp_id!r} is missing field {field!r}"))

    # ---- REQ-24-13: lifecycle register ----
    lc = _load_json(LIFECYCLE_REGISTER).get("records", [])
    for rec in lc:
        rid = rec.get("record_id", "?")
        if rec.get("lifecycle_state") not in LIFECYCLE_STATES:
            findings.append(_make_finding(
                "CG-040", rid,
                f"lifecycle record {rid!r} has state "
                f"{rec.get('lifecycle_state')!r} outside {sorted(LIFECYCLE_STATES)}"))

    # ---- REQ-24-21: exception register ----
    excs = _load_json(EXCEPTION_REGISTER).get("exceptions", [])
    for exc in excs:
        eid = exc.get("exception_id", "?")
        if exc.get("category") not in EXCEPTION_CATEGORIES:
            findings.append(_make_finding(
                "CG-050", eid,
                f"exception {eid!r} has category {exc.get('category')!r} outside "
                f"{sorted(EXCEPTION_CATEGORIES)}"))
        for field in ("rule_id", "scope", "rationale", "owner",
                      "approving_authority", "review_date"):
            if not exc.get(field):
                findings.append(_make_finding(
                    "CG-051", eid,
                    f"exception {eid!r} is missing field {field!r}"))

    # ---- REQ-24-22: deferred-work register ----
    df = _load_json(DEFERRED_REGISTER).get("deferrals", [])
    for dfr in df:
        did = dfr.get("deferral_id", "?")
        for field in ("requirement_id", "scope", "reason", "impact",
                      "owner", "approved_by", "review_date", "status"):
            if not dfr.get(field):
                findings.append(_make_finding(
                    "CG-060", did,
                    f"deferral {did!r} is missing field {field!r}"))

    # ---- REQ-24-39/40: improvement backlog ----
    ib = _load_json(IMPROVEMENT_BACKLOG).get("items", [])
    for item in ib:
        iid = item.get("item_id", "?")
        if item.get("category") not in IMPROVEMENT_CATEGORIES:
            findings.append(_make_finding(
                "CG-070", iid,
                f"improvement item {iid!r} has category "
                f"{item.get('category')!r} outside {sorted(IMPROVEMENT_CATEGORIES)}"))
        for field in ("item_id", "description", "origin", "impact",
                      "priority", "dependencies", "owner", "proposed_action",
                      "status", "target_review_date"):
            if not item.get(field):
                findings.append(_make_finding(
                    "CG-071", iid,
                    f"improvement item {iid!r} is missing field {field!r}"))

    # ---- REQ-24-04: residual gap register ----
    rg = _load_json(RESIDUAL_GAPS).get("gaps", [])
    for g in rg:
        gid = g.get("gap_id", "?")
        for field in ("gap_id", "description", "affected_requirement",
                        "affected_entity", "impact", "severity",
                        "owner", "proposed_action", "target_date", "disposition"):
            if not g.get(field):
                findings.append(_make_finding(
                    "CG-080", gid,
                    f"residual gap {gid!r} is missing field {field!r}"))

    state = {
        "crs": crs,
        "baseline": base,
        "residual_gaps": rg,
        "roles": roles,
        "ownership_dispositions": dispositions,
        "lifecycle_records": lc,
        "exceptions": excs,
        "deferrals": df,
        "improvement_items": ib,
    }
    return findings, state


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="synthetic self-test")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()

    if args.self_test:
        print(json.dumps({
            "mode": "self-test",
            "lifecycle_states": len(LIFECYCLE_STATES),
            "exception_categories": len(EXCEPTION_CATEGORIES),
            "improvement_categories": len(IMPROVEMENT_CATEGORIES),
            "findings": [],
        }, indent=2))
        return 0

    findings, state = evaluate()
    by_severity = Counter(f["severity"] for f in findings)
    by_rule = Counter(f["rule"] for f in findings)
    if by_severity.get("error", 0) > 0:
        outcome = "failed"
    elif findings:
        outcome = "passed_with_warnings"
    else:
        outcome = "passed"

    manifest = {
        "manifest_schema_version": "1",
        "generated_at": "2026-10-20",
        "generator": "scripts/check_programme_closure_ext24.py",
        "parent_cr": "CR-BP-94-EXT-24",
        "repository_revision": _git_revision(),
        "summary": {
            "total_findings": len(findings),
            "by_severity": dict(sorted(by_severity.items())),
            "by_framework_rule": dict(sorted(by_rule.items())),
            "closure_cr_count": len(state["crs"]),
            "baseline_present": bool(state["baseline"]),
            "residual_gap_count": len(state["residual_gaps"]),
            "governance_role_count": len(state["roles"]),
            "ownership_disposition_count": len(state["ownership_dispositions"]),
            "lifecycle_record_count": len(state["lifecycle_records"]),
            "exception_count": len(state["exceptions"]),
            "deferral_count": len(state["deferrals"]),
            "improvement_item_count": len(state["improvement_items"]),
            "overall_outcome": outcome,
        },
        "findings": findings,
    }

    CLOSURE_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(manifest, indent=2))
    else:
        print(f"Closure CRs assessed: {len(state['crs'])}")
        print(f"Residual gaps: {len(state['residual_gaps'])}")
        print(f"Governance roles: {len(state['roles'])}")
        print(f"Ownership dispositions (L2): {len(state['ownership_dispositions'])}")
        print(f"Lifecycle records: {len(state['lifecycle_records'])}")
        print(f"Approved exceptions: {len(state['exceptions'])}")
        print(f"Deferred-work items: {len(state['deferrals'])}")
        print(f"Improvement backlog items: {len(state['improvement_items'])}")
        print(f"\nFramework findings: {len(findings)}")
        for f in findings[:12]:
            print(f"  [{f['rule']}] {f['where']}: {f['diagnostic'][:120]}")
        if len(findings) > 12:
            print(f"  ... and {len(findings) - 12} more")
        print(f"\nOverall outcome: {outcome.upper()}")

    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())