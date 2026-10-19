#!/usr/bin/env python3
"""
check_authoring_methodology_ext16.py
=====================================

L2/L3/L4 authoring methodology validator (CR-BP-94-EXT-16).

Codifies the EXT-16 requirements:

  AM-001  metadata.authoring (when present) is a dict with the EXT-16
          attributes (methodology_version, state, author, etc.).
  AM-002  metadata.authoring.methodology_version is non-empty.
  AM-003  metadata.authoring.state is in the 9-value vocabulary
          (not_started | planning | researching | drafted |
          under_review | approved | published | rejected | withdrawn).
  AM-004  metadata.authoring.author is non-empty when state is
          'drafted' or later (drafted, under_review, approved,
          published, rejected).
  AM-005  metadata.authoring.reviewer is non-empty when state is
          'under_review' or later (under_review, approved, published).
  AM-006  metadata.authoring.ai_assistance.used is a boolean.
  AM-007  When ai_assistance.used is true, ai_assistance.validation
          is in the 2-value vocabulary
          (independently_validated | pending_validation).
  AM-008  metadata.authoring.quality_dimensions covers the 8 EXT-16
          review dimensions (semantic_correctness, decomposition_appropriateness,
          evidence_quality, parent_child_consistency, cross_catalogue_validity,
          profile_completeness, publication_safety, readme_consistency).
  AM-009  metadata.authoring.source_priority_used is in the 9-value
          vocabulary (organisational_policy | owner_confirmation |
          operational_documentation | system_architecture | direct_observation |
          sme_confirmation | external_authority | secondary_research |
          analyst_inference).
  AM-010  L0/L1 do NOT carry metadata.authoring (they inherit from L2
          per EXT-11 non-executable + EXT-16 §15).

The validator writes a manifest at reconciliation/authoring-manifest.json
and runs as gate [41] in scripts/conformance_result.py (ADVISORY;
flipped to blocking under CR-BP-94-EXT-23).

Test layout: tests/test_authoring_methodology_ext16.py
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
MANIFEST_PATH = REPO_ROOT / "reconciliation" / "authoring-manifest.json"

# Controlled vocabularies (per EXT-16)
AUTHORING_STATES = frozenset({
    "not_started", "planning", "researching", "drafted",
    "under_review", "approved", "published", "rejected", "withdrawn",
})
AUTHORING_STATES_REQUIRING_AUTHOR = frozenset({
    "drafted", "under_review", "approved", "published", "rejected",
})
AUTHORING_STATES_REQUIRING_REVIEWER = frozenset({
    "under_review", "approved", "published",
})
AI_VALIDATION_STATES = frozenset({
    "independently_validated", "pending_validation",
})
SOURCE_PRIORITY_VALUES = frozenset({
    "organisational_policy", "owner_confirmation",
    "operational_documentation", "system_architecture",
    "direct_observation", "sme_confirmation",
    "external_authority", "secondary_research",
    "analyst_inference",
})
QUALITY_DIMENSIONS = frozenset({
    "semantic_correctness", "decomposition_appropriateness",
    "evidence_quality", "parent_child_consistency",
    "cross_catalogue_validity", "profile_completeness",
    "publication_safety", "readme_consistency",
})
QUALITY_VALUES = frozenset({"pass", "fail", "n_a"})
REVIEW_OUTCOMES = frozenset({"approved", "rejected", "revisions_required"})

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
    """Run AM-001..AM-010 against every (path, record) pair. Returns findings."""
    findings: list[dict] = []

    for path, record in records:
        rec_id = record.get("id") or path.parent.name
        entity_type = record.get("type")
        level = LEVEL_BY_TYPE.get(entity_type) if isinstance(entity_type, str) else None
        where = f"{rec_id} ({entity_type} {level})"

        # AM-010: L0/L1 MUST NOT carry metadata.authoring.
        if level in NON_EXECUTABLE_LEVELS:
            metadata = record.get("metadata")
            if isinstance(metadata, dict) and "authoring" in metadata:
                findings.append(_make_finding(
                    "AM-010", where,
                    f"non-executable {level} record declares metadata.authoring; "
                    f"L0/L1 are non-executable (EXT-11) and inherit from L2 (EXT-16 §15)",
                ))

        # Get the authoring block (may be absent).
        metadata = record.get("metadata")
        if not isinstance(metadata, dict):
            continue
        authoring = metadata.get("authoring")
        if authoring is None:
            # AM-001..AM-009: authoring block absent is fine (optional).
            continue
        if not isinstance(authoring, dict):
            findings.append(_make_finding(
                "AM-001", where,
                "metadata.authoring is not a dict",
            ))
            continue

        # AM-001: required top-level fields.
        for required_key in ("methodology_version", "state", "author", "author_date"):
            if required_key not in authoring:
                findings.append(_make_finding(
                    "AM-001", where,
                    f"metadata.authoring missing EXT-16 field {required_key!r}",
                ))

        # AM-002: methodology_version non-empty.
        mv = authoring.get("methodology_version")
        if isinstance(mv, str) and not mv.strip():
            findings.append(_make_finding(
                "AM-002", where,
                "metadata.authoring.methodology_version is empty",
            ))

        # AM-003: state vocabulary.
        state = authoring.get("state")
        if state is not None and state not in AUTHORING_STATES:
            findings.append(_make_finding(
                "AM-003", where,
                f"metadata.authoring.state {state!r} is not in the EXT-16 9-value vocabulary",
            ))

        # AM-004: author non-empty when state is 'drafted' or later.
        if state in AUTHORING_STATES_REQUIRING_AUTHOR:
            author = authoring.get("author")
            if not (isinstance(author, str) and author.strip()):
                findings.append(_make_finding(
                    "AM-004", where,
                    f"metadata.authoring.author is required when state is {state!r}",
                ))

        # AM-005: reviewer non-empty when state is 'under_review' or later.
        if state in AUTHORING_STATES_REQUIRING_REVIEWER:
            reviewer = authoring.get("reviewer")
            if not (isinstance(reviewer, str) and reviewer.strip()):
                findings.append(_make_finding(
                    "AM-005", where,
                    f"metadata.authoring.reviewer is required when state is {state!r}",
                ))

        # AM-006: ai_assistance.used is a boolean.
        ai = authoring.get("ai_assistance")
        if isinstance(ai, dict):
            used = ai.get("used")
            if not isinstance(used, bool):
                findings.append(_make_finding(
                    "AM-006", where,
                    f"metadata.authoring.ai_assistance.used is {used!r}; must be a boolean",
                ))
            # AM-007: when used is true, validation is in the 2-value vocabulary.
            if used is True:
                val = ai.get("validation")
                if val is not None and val not in AI_VALIDATION_STATES:
                    findings.append(_make_finding(
                        "AM-007", where,
                        f"metadata.authoring.ai_assistance.validation {val!r} is not in the EXT-16 2-value vocabulary",
                    ))

        # AM-008: quality_dimensions covers the 8 dimensions.
        qd = authoring.get("quality_dimensions")
        if isinstance(qd, dict):
            for dim in QUALITY_DIMENSIONS:
                if dim not in qd:
                    findings.append(_make_finding(
                        "AM-008", where,
                        f"metadata.authoring.quality_dimensions missing required EXT-16 dimension {dim!r}",
                    ))
                else:
                    v = qd[dim]
                    if v not in QUALITY_VALUES:
                        findings.append(_make_finding(
                            "AM-008", where,
                            f"metadata.authoring.quality_dimensions.{dim} {v!r} is not in the EXT-16 pass/fail/n_a vocabulary",
                        ))

        # AM-009: source_priority_used vocabulary.
        spu = authoring.get("source_priority_used")
        if spu is not None and spu not in SOURCE_PRIORITY_VALUES:
            findings.append(_make_finding(
                "AM-009", where,
                f"metadata.authoring.source_priority_used {spu!r} is not in the EXT-16 9-value vocabulary",
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
                "metadata": {
                    "established_by": "CR-BP-94-EXT-19",
                    "established_at": "2026-10-19",
                    "change_history": [
                        {"cr": "CR-BP-94-EXT-19", "date": "2026-10-19",
                         "change": "Initial enrichment"},
                    ],
                    "authoring": {
                        "methodology_version": "1.0.0",
                        "state": "published",
                        "research_plan": {
                            "scope": "KYC process enrichment",
                            "sources_consulted": ["KYC Policy v3.2"],
                            "gaps_identified": ["Refresh frequency"],
                            "blockers": [],
                        },
                        "author": "KYC Analyst",
                        "author_date": "2026-10-15",
                        "reviewer": "Compliance Officer",
                        "review_date": "2026-10-17",
                        "review_outcome": "approved",
                        "ai_assistance": {
                            "used": True,
                            "tool": "extraction",
                            "role": "gap_analysis",
                            "validation": "independently_validated",
                        },
                        "evidence_inheritance": {
                            "from_parent": None,
                            "inherited_fields": [],
                        },
                        "source_priority_used": "owner_confirmation",
                        "quality_dimensions": {
                            "semantic_correctness": "pass",
                            "decomposition_appropriateness": "pass",
                            "evidence_quality": "pass",
                            "parent_child_consistency": "n_a",
                            "cross_catalogue_validity": "pass",
                            "profile_completeness": "pass",
                            "publication_safety": "pass",
                            "readme_consistency": "pass",
                        },
                    },
                },
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
        "generator": "scripts/check_authoring_methodology_ext16.py",
        "parent_cr": "CR-BP-94-EXT-16",
        "catalog_root": str(catalog_root),
        "summary": {
            "total_records": len(records),
            "total_findings": len(findings),
            "by_rule": {},
        },
        "findings": findings,
        "controlled_vocabularies": {
            "authoring_states": sorted(AUTHORING_STATES),
            "ai_validation_states": sorted(AI_VALIDATION_STATES),
            "source_priority_values": sorted(SOURCE_PRIORITY_VALUES),
            "quality_dimensions": sorted(QUALITY_DIMENSIONS),
            "quality_values": sorted(QUALITY_VALUES),
            "review_outcomes": sorted(REVIEW_OUTCOMES),
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
            print(f"OK: authoring methodology conform (0 findings). "
                  f"Manifest at {MANIFEST_PATH.relative_to(REPO_ROOT)}")
        else:
            print(f"FAIL: {len(findings)} findings across {len(records)} records.")
            for finding in findings:
                print(f"  [{finding['rule']}] {finding['where']}: {finding['diagnostic']}")

    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
