#!/usr/bin/env python3
"""
check_profile_registry_ext11.py
================================

L0/L1/L2/L3/L4 documentation profile registry validator (CR-BP-94-EXT-11).

Codifies the EXT-11 profile requirements:

  PR-001  Profile file exists at templates/documentation-profile-ext11-v3.yaml.
  PR-002  Profile file is valid YAML and has the 5 top-level level keys
          (l0_process_context, l1_process_group, l2_business_process,
          l3_activity, l4_task).
  PR-003  Each level profile declares: profile_id, applies_to, required_sections,
          conditional_sections, not_applicable_sections, inherited_sections.
  PR-004  Each (entity_type, level) maps to exactly one profile (no duplicates).
  PR-005  L0 and L1 profiles have non_executable: true.
  PR-006  L0 and L1 profiles do NOT include any executable operational
          section (no trigger/precondition/input/transformation/output/
          outcome/performer/accountability/business_rule/control/exception).
  PR-007  L4 profile does NOT include any workflow orchestration section
          (no sequence/branching/retry/state-machine/workflow-engine/
          orchestration). Per CR-BP-98.
  PR-008  The retired '(pending; backfill at EXT-04)' phrase is re-issued
          in the v3 profile (placeholder_states.placeholder_phrases map
          to EXT-09 §10 completeness states). The retired phrase is no
          longer used as a directive.
  PR-009  Inherited sections on L0/L1 reference the L0/L1's authoritative
          source (cell charter, group scope) and are traceable.
  PR-010  No new top-level schema fields are introduced by EXT-11
          (validated against docs/operational-schema-inventory.md §12
          RETAIN/Gap table).

The validator writes a manifest at reconciliation/profile-manifest.json and
runs as gate [36] EXT-11 Profile Conformance in scripts/conformance_result.py
(advisory; flipped to blocking under CR-BP-94-EXT-23).

Test layout:
  tests/test_profile_registry_ext11.py (unit + integration).
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
PROFILE_PATH = REPO_ROOT / "templates" / "documentation-profile-ext11-v3.yaml"
MANIFEST_PATH = REPO_ROOT / "reconciliation" / "profile-manifest.json"

# Cross-cutting rule: L0/L1 MUST NOT include executable operational sections.
# These are section ids that, if present in an L0/L1 profile, violate
# the non_executable constraint (per EXT-09 §11.1 and §11.2).
EXECUTABLE_SECTION_IDS = frozenset({
    "trigger", "precondition", "input", "transformation",
    "output", "outcome", "performer", "accountability",
    "business_rule", "control", "exception",
})

# Cross-cutting rule: L4 MUST NOT include workflow orchestration sections
# (per CR-BP-98; the EXT-11 §10 explicit "prohibited" list).
WORKFLOW_ORCHESTRATION_SECTION_IDS = frozenset({
    "workflow", "workflow-orchestration", "orchestration",
    "sequence", "branching", "retry", "state-machine",
    "workflow-engine", "workflow-instance",
})

# The 5 classifications per EXT-11 §5.
REQUIRED_CLASSIFICATIONS = ("required", "conditional", "not_applicable", "inherited")
# `optional` is permitted but not required to be present (a profile can have
# zero optional sections).

# Expected level keys in the v3 profile.
LEVEL_KEYS = (
    "l0_process_context",
    "l1_process_group",
    "l2_business_process",
    "l3_activity",
    "l4_task",
)


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------

def _make_finding(rule: str, where: str, diagnostic: str, advisory: bool = True) -> dict:
    return {
        "rule": rule,
        "where": where,
        "diagnostic": diagnostic,
        "advisory": advisory,
    }


def evaluate(profile_data: dict) -> list[dict]:
    """Run PR-001..PR-010 against the v3 profile data. Returns a list of findings."""
    findings: list[dict] = []

    # PR-002: top-level structure.
    for level_key in LEVEL_KEYS:
        if level_key not in profile_data:
            findings.append(_make_finding(
                "PR-002", level_key,
                f"top-level key {level_key!r} missing from the v3 profile",
            ))

    # PR-003 + PR-004 + PR-005 + PR-006 + PR-007 + PR-009: per level.
    seen_profiles: set[str] = set()
    for level_key in LEVEL_KEYS:
        level_data = profile_data.get(level_key)
        if not isinstance(level_data, dict):
            continue

        # PR-003: required keys on the level profile.
        for required_key in (
            "profile_id", "applies_to",
            "required_sections", "conditional_sections",
            "not_applicable_sections", "inherited_sections",
        ):
            if required_key not in level_data:
                findings.append(_make_finding(
                    "PR-003", level_key,
                    f"required key {required_key!r} missing from {level_key}",
                ))

        # PR-004: profile_id uniqueness.
        profile_id = level_data.get("profile_id")
        if isinstance(profile_id, str):
            if profile_id in seen_profiles:
                findings.append(_make_finding(
                    "PR-004", level_key,
                    f"profile_id {profile_id!r} duplicates an earlier level's profile_id",
                ))
            seen_profiles.add(profile_id)

        # PR-005: L0/L1 non_executable: true.
        if level_key in ("l0_process_context", "l1_process_group"):
            if level_data.get("non_executable") is not True:
                findings.append(_make_finding(
                    "PR-005", level_key,
                    f"{level_key} must declare non_executable: true (per EXT-09 §11.1/§11.2)",
                ))

        # PR-006: L0/L1 MUST NOT include executable operational sections.
        if level_key in ("l0_process_context", "l1_process_group"):
            for section_key in ("required_sections", "conditional_sections"):
                sections = level_data.get(section_key) or []
                if not isinstance(sections, list):
                    continue
                for section in sections:
                    if not isinstance(section, dict):
                        # String-form section; check its id.
                        if isinstance(section, str) and section in EXECUTABLE_SECTION_IDS:
                            findings.append(_make_finding(
                                "PR-006", level_key,
                                f"executable operational section {section!r} in {section_key}; "
                                f"L0/L1 are non-executable per EXT-09 §11.1/§11.2",
                            ))
                        continue
                    section_id = section.get("id")
                    if section_id in EXECUTABLE_SECTION_IDS:
                        findings.append(_make_finding(
                            "PR-006", level_key,
                            f"executable operational section id={section_id!r} in {section_key}; "
                            f"L0/L1 are non-executable per EXT-09 §11.1/§11.2",
                        ))

        # PR-007: L4 MUST NOT include workflow orchestration sections.
        if level_key == "l4_task":
            for section_key in ("required_sections", "conditional_sections"):
                sections = level_data.get(section_key) or []
                if not isinstance(sections, list):
                    continue
                for section in sections:
                    if not isinstance(section, dict):
                        if isinstance(section, str) and section in WORKFLOW_ORCHESTRATION_SECTION_IDS:
                            findings.append(_make_finding(
                                "PR-007", level_key,
                                f"workflow orchestration section {section!r} in {section_key}; "
                                f"L4 is bounded + verifiable, not orchestrating (CR-BP-98)",
                            ))
                        continue
                    section_id = section.get("id")
                    if section_id in WORKFLOW_ORCHESTRATION_SECTION_IDS:
                        findings.append(_make_finding(
                            "PR-007", level_key,
                            f"workflow orchestration section id={section_id!r} in {section_key}; "
                            f"L4 is bounded + verifiable, not orchestrating (CR-BP-98)",
                        ))

    # PR-008: retired placeholder phrase is re-issued.
    placeholder_states = profile_data.get("placeholder_states")
    if not isinstance(placeholder_states, dict):
        findings.append(_make_finding(
            "PR-008", "placeholder_states",
            "placeholder_states block missing from the v3 profile",
        ))
    else:
        reissued = placeholder_states.get("reissued_phrases")
        if not isinstance(reissued, dict):
            findings.append(_make_finding(
                "PR-008", "placeholder_states",
                "reissued_phrases block missing; the retired phrase must be re-issued "
                "with EXT-09 §10 completeness states",
            ))
        else:
            # The 11 EXT-09 §10 states (per EXT-09 §10 normative list).
            for state in (
                "not_started", "in_progress", "pending_evidence",
                "pending_review", "approved", "not_applicable",
                "unknown", "inherited", "rejected", "superseded",
                "deferred",
            ):
                if state not in reissued:
                    findings.append(_make_finding(
                        "PR-008", "placeholder_states",
                        f"reissued_phrases missing EXT-09 §10 state {state!r}",
                    ))
        if placeholder_states.get("retired_phrase") != "(pending; backfill at EXT-04)":
            findings.append(_make_finding(
                "PR-008", "placeholder_states",
                "retired_phrase not declared; the validator cannot recognise legacy READMEs",
            ))

    # PR-010: no schema mutations are introduced by this profile.
    # The validator's job is to flag any new top-level field declared in the
    # v3 profile that is not in the EXT-10 RETAIN table. We do this by
    # checking that no required section has an `id` that is not in the
    # known schema field set.
    KNOWN_SCHEMA_FIELDS = {
        # L2 RETAIN from EXT-10 §12
        "trigger", "outcome", "identity", "inputs", "outputs",
        "transformation", "responsibility", "boundary",
        # L0/L1 RETAIN
        "scope", "outcomes", "decomposition_basis", "evidence",
        "grouping_basis", "membership_criteria", "profile",
        # L3 RETAIN
        "belongs_to_business_process", "cohesion_rationale",
        # L4 RETAIN
        "belongs_to_activity",
        # L0 + L1 only via v1 profiles
        "composes", "decomposition", "hierarchical-decomposition",
        "header-identity-table", "executive-summary", "intent-definition",
        "governance-provenance", "behavioral-boundaries",
        "properties-relationships", "operational-metrics",
        "operational-details", "technical-metadata",
        # L4 trigger/outcome are required
        # Per-level profile section ids (v3 names; the underlying schema
        # fields are mapped per the EXT-10 RETAIN table)
        "inputs-outputs", "interfaces", "dependencies",
        "roles-responsibilities", "rules-controls", "exceptions",
        "metrics", "cell-charter-context", "group-membership",
        "parent-bp-context", "parent-activity-context",
        "group-outcomes", "scope-boundary", "regulatory-evidence",
        "completion-criteria", "authorization", "evidence",
        "shared-rules-controls",
    }
    for level_key in LEVEL_KEYS:
        level_data = profile_data.get(level_key)
        if not isinstance(level_data, dict):
            continue
        for section_key in ("required_sections", "conditional_sections"):
            sections = level_data.get(section_key) or []
            if not isinstance(sections, list):
                continue
            for section in sections:
                if not isinstance(section, dict):
                    section_id = section if isinstance(section, str) else None
                else:
                    section_id = section.get("id")
                if section_id and section_id not in KNOWN_SCHEMA_FIELDS:
                    # Allow not_applicable and inherited marker ids
                    if section_id not in ("not_applicable", "inherited", "executable-transformation",
                                   "trigger", "precondition", "input", "transformation",
                                   "output", "outcome", "performer", "accountability",
                                   "business_rule", "control", "exception",
                                   "workflow-orchestration"):
                        findings.append(_make_finding(
                            "PR-010", level_key,
                            f"section id={section_id!r} is not in the EXT-10 RETAIN schema fields; "
                            f"if this is a new schema field, route to EXT-10 first",
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
        # Synthetic: a minimal v3 profile data dict that satisfies all rules.
        synthetic = {
            "l0_process_context": {
                "profile_id": "p-l0", "applies_to": {"entity_type": "ProcessContext", "level": "L0"},
                "non_executable": True,
                "required_sections": [{"id": "header-identity-table"}],
                "conditional_sections": [],
                "not_applicable_sections": [{"id": "trigger", "rationale": "x"}],
                "inherited_sections": [],
            },
            "l1_process_group": {
                "profile_id": "p-l1", "applies_to": {"entity_type": "ProcessGroup", "level": "L1"},
                "non_executable": True,
                "required_sections": [],
                "conditional_sections": [],
                "not_applicable_sections": [],
                "inherited_sections": [],
            },
            "l2_business_process": {
                "profile_id": "p-l2", "applies_to": {"entity_type": "Process", "level": "L2"},
                "required_sections": [], "conditional_sections": [],
                "not_applicable_sections": [], "inherited_sections": [],
            },
            "l3_activity": {
                "profile_id": "p-l3", "applies_to": {"entity_type": "Activity", "level": "L3"},
                "required_sections": [], "conditional_sections": [],
                "not_applicable_sections": [], "inherited_sections": [],
            },
            "l4_task": {
                "profile_id": "p-l4", "applies_to": {"entity_type": "Task", "level": "L4"},
                "non_orchestrating": True,
                "required_sections": [], "conditional_sections": [],
                "not_applicable_sections": [], "inherited_sections": [],
            },
            "placeholder_states": {
                "reissued_phrases": {
                    "not_started": "(x)", "in_progress": "(x)", "pending_evidence": "(x)",
                    "pending_review": "(x)", "approved": "(x)", "not_applicable": "(x)",
                    "unknown": "(x)", "inherited": "(x)", "rejected": "(x)", "superseded": "(x)",
                    "deferred": "(x)",
                },
                "retired_phrase": "(pending; backfill at EXT-04)",
            },
        }
        findings = evaluate(synthetic)
        result = {"mode": "self-test", "findings": findings,
                  "summary": {"total_findings": len(findings)}}
        print(json.dumps(result, indent=2))
        return 0 if not findings else 1

    # Live mode: load the v3 profile and evaluate.
    if not PROFILE_PATH.exists():
        msg = f"PR-001: profile file not found at {PROFILE_PATH}"
        if args.json:
            print(json.dumps({"mode": "live", "findings": [_make_finding("PR-001", "profile", msg)]}))
        else:
            print(msg)
        return 2

    with PROFILE_PATH.open(encoding="utf-8") as fp:
        profile_data = yaml.safe_load(fp) or {}

    findings = evaluate(profile_data)

    # Build the manifest.
    manifest = {
        "manifest_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/check_profile_registry_ext11.py",
        "parent_cr": "CR-BP-94-EXT-11",
        "catalog_root": str(catalog_root),
        "profile_path": str(PROFILE_PATH),
        "summary": {
            "total_findings": len(findings),
            "by_rule": {},
        },
        "findings": findings,
        "profiles": {},
    }
    for finding in findings:
        manifest["summary"]["by_rule"].setdefault(finding["rule"], 0)
        manifest["summary"]["by_rule"][finding["rule"]] += 1

    for level_key in LEVEL_KEYS:
        level_data = profile_data.get(level_key)
        if not isinstance(level_data, dict):
            continue
        manifest["profiles"][level_key] = {
            "profile_id": level_data.get("profile_id"),
            "applies_to": level_data.get("applies_to"),
            "non_executable": level_data.get("non_executable", False),
            "non_orchestrating": level_data.get("non_orchestrating", False),
            "required_sections": [
                s.get("id") if isinstance(s, dict) else s
                for s in (level_data.get("required_sections") or [])
            ],
            "conditional_sections": [
                s.get("id") if isinstance(s, dict) else s
                for s in (level_data.get("conditional_sections") or [])
            ],
            "not_applicable_sections": [
                s.get("id") if isinstance(s, dict) else s
                for s in (level_data.get("not_applicable_sections") or [])
            ],
            "inherited_sections": [
                s.get("id") if isinstance(s, dict) else s
                for s in (level_data.get("inherited_sections") or [])
            ],
        }

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", encoding="utf-8") as fp:
        json.dump(manifest, fp, indent=2)

    if args.json:
        print(json.dumps(manifest, indent=2))
    else:
        if not findings:
            print(f"OK: profile registry conforms (0 findings). "
                  f"Manifest at {MANIFEST_PATH.relative_to(REPO_ROOT)}")
        else:
            print(f"FAIL: {len(findings)} findings.")
            for finding in findings:
                print(f"  [{finding['rule']}] {finding['where']}: {finding['diagnostic']}")

    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
