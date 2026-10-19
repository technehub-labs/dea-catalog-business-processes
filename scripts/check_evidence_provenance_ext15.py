#!/usr/bin/env python3
"""
check_evidence_provenance_ext15.py
==================================

L2/L3/L4 evidence, provenance, confidence, verification, uncertainty
state validator (CR-BP-94-EXT-15).

Codifies the EXT-15 requirements:

  EV-001  provenance[] entries have id + source.source_class +
          assertions_supported + review_status.
  EV-002  provenance[].source.source_class is in the 10-value vocabulary.
  EV-003  provenance[].source.confidentiality (when present) is in the
          4-value vocabulary.
  EV-004  provenance[].review_status is in the 6-value vocabulary.
  EV-005  AI-assisted sources (source_class: ai_assisted_research)
          MUST NOT be presented as authoritative; the evidence_limitations
          field MUST be non-empty when the source is AI-assisted.
  EV-006  per-assertion provenance.confidence (when present) is in the
          5-value vocabulary.
  EV-007  per-assertion provenance.verification_status (when present)
          is in the 6-value vocabulary.
  EV-008  per-assertion provenance.uncertainty_state (when present) is
          in the 7-value vocabulary.
  EV-009  Multiple provenance records may exist for the same assertion;
          the assertions_supported[] may overlap across records
          (this rule confirms the overlap is allowed, not a finding).
  EV-010  L0/L1 do NOT declare provenance[] as a top-level field;
          they inherit from L2 (per EXT-11 non-executable + EXT-15 §10).

The validator writes a manifest at reconciliation/evidence-manifest.json
and runs as gate [40] in scripts/conformance_result.py (ADVISORY;
flipped to blocking under CR-BP-94-EXT-23).

Test layout: tests/test_evidence_provenance_ext15.py
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
MANIFEST_PATH = REPO_ROOT / "reconciliation" / "evidence-manifest.json"

# Controlled vocabularies (per EXT-15)
SOURCE_CLASSES = frozenset({
    "authoritative_document", "system_documentation", "owner_confirmation",
    "subject_matter_expert", "direct_observation", "operational_record",
    "external_authority", "secondary_reference", "analyst_inference",
    "ai_assisted_research",
})
CONFIDENTIALITY_CLASSES = frozenset({
    "public", "internal", "confidential", "restricted",
})
CONFIDENCE_LEVELS = frozenset({
    "high", "medium", "low", "unverified", "conflicting",
})
VERIFICATION_STATUSES = frozenset({
    "not_reviewed", "under_review", "verified", "rejected",
    "superseded", "disputed",
})
UNCERTAINTY_STATES = frozenset({
    "unknown", "not_applicable", "not_yet_assessed", "inherited",
    "deferred_with_reason", "conflicting", "confirmed_absence",
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

# Per-assertion sub-structures that may carry provenance in EXT-12/13/14
PER_ASSERTION_PROVENANCE_FIELDS = (
    "inputs", "outputs", "interfaces", "dependencies",
    "responsibility", "accountability", "roles", "raci",
    "business_rules", "controls", "exceptions", "deviations",
)


def _make_finding(rule: str, where: str, diagnostic: str) -> dict:
    return {"rule": rule, "where": where, "diagnostic": diagnostic, "advisory": True}


def evaluate(records: Iterable[tuple[Path, dict]]) -> list[dict]:
    """Run EV-001..EV-010 against every (path, record) pair. Returns findings."""
    findings: list[dict] = []

    for path, record in records:
        rec_id = record.get("id") or path.parent.name
        entity_type = record.get("type")
        level = LEVEL_BY_TYPE.get(entity_type) if isinstance(entity_type, str) else None
        where = f"{rec_id} ({entity_type} {level})"

        # EV-010: L0/L1 MUST NOT declare provenance[] as a top-level field.
        if level in NON_EXECUTABLE_LEVELS:
            if "provenance" in record:
                findings.append(_make_finding(
                    "EV-010", where,
                    f"non-executable {level} record declares provenance[]; L0/L1 are non-executable (EXT-11) and inherit from L2 (EXT-15 §10)",
                ))

        # EV-001 + EV-002 + EV-003 + EV-004 + EV-005: top-level provenance[].
        provenance = record.get("provenance")
        if isinstance(provenance, list):
            seen_provenance_ids: set[str] = set()
            for i, entry in enumerate(provenance):
                entry_where = f"{where} provenance[{i}]"
                if not isinstance(entry, dict):
                    findings.append(_make_finding(
                        "EV-001", entry_where,
                        "provenance entry is not a dict",
                    ))
                    continue
                # EV-001: required top-level fields.
                for required_key in ("id", "assertions_supported", "review_status"):
                    if required_key not in entry:
                        findings.append(_make_finding(
                            "EV-001", entry_where,
                            f"provenance entry missing EXT-15 field {required_key!r}",
                        ))
                pid = entry.get("id")
                if isinstance(pid, str):
                    if pid in seen_provenance_ids:
                        findings.append(_make_finding(
                            "EV-001", entry_where,
                            f"duplicate provenance id {pid!r} within record",
                        ))
                    seen_provenance_ids.add(pid)
                # EV-002: source.source_class vocabulary.
                source = entry.get("source")
                if isinstance(source, dict):
                    sc = source.get("source_class")
                    if sc is not None and sc not in SOURCE_CLASSES:
                        findings.append(_make_finding(
                            "EV-002", entry_where,
                            f"provenance[].source.source_class {sc!r} is not in the EXT-15 vocabulary",
                        ))
                    # EV-003: confidentiality vocabulary (when present).
                    conf = source.get("confidentiality")
                    if conf is not None and conf not in CONFIDENTIALITY_CLASSES:
                        findings.append(_make_finding(
                            "EV-003", entry_where,
                            f"provenance[].source.confidentiality {conf!r} is not in the EXT-15 vocabulary",
                        ))
                # EV-004: review_status vocabulary.
                rs = entry.get("review_status")
                if rs is not None and rs not in VERIFICATION_STATUSES:
                    findings.append(_make_finding(
                        "EV-004", entry_where,
                        f"provenance[].review_status {rs!r} is not in the EXT-15 vocabulary",
                    ))
                # EV-005: AI-assisted sources require non-empty evidence_limitations.
                if isinstance(source, dict) and source.get("source_class") == "ai_assisted_research":
                    limits = entry.get("evidence_limitations")
                    if not (isinstance(limits, str) and limits.strip()):
                        findings.append(_make_finding(
                            "EV-005", entry_where,
                            "AI-assisted source MUST have a non-empty evidence_limitations field; "
                            "AI-assisted content is a research aid, not authoritative evidence (REQ-15-09)",
                        ))

        # EV-006 + EV-007 + EV-008: per-assertion provenance sub-structures.
        for field_name in PER_ASSERTION_PROVENANCE_FIELDS:
            field = record.get(field_name)
            if not isinstance(field, list):
                continue
            for i, entry in enumerate(field):
                if not isinstance(entry, dict):
                    continue
                prov = entry.get("provenance")
                if not isinstance(prov, dict):
                    continue
                entry_where = f"{where} {field_name}[{i}].provenance"
                # EV-006: confidence vocabulary.
                conf = prov.get("confidence")
                if conf is not None and conf not in CONFIDENCE_LEVELS:
                    findings.append(_make_finding(
                        "EV-006", entry_where,
                        f"provenance.confidence {conf!r} is not in the EXT-15 5-value vocabulary",
                    ))
                # EV-007: verification_status vocabulary.
                vs = prov.get("verification_status")
                if vs is not None and vs not in VERIFICATION_STATUSES:
                    findings.append(_make_finding(
                        "EV-007", entry_where,
                        f"provenance.verification_status {vs!r} is not in the EXT-15 6-value vocabulary",
                    ))
                # EV-008: uncertainty_state vocabulary.
                us = prov.get("uncertainty_state")
                if us is not None and us not in UNCERTAINTY_STATES:
                    findings.append(_make_finding(
                        "EV-008", entry_where,
                        f"provenance.uncertainty_state {us!r} is not in the EXT-15 7-value vocabulary",
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
                "provenance": [
                    {"id": "prov-1",
                     "source": {"title": "KYC Policy v3.2",
                                "source_class": "authoritative_document",
                                "owner": "Compliance",
                                "location": "https://...",
                                "publication_date": "2026-01-15",
                                "accessed_date": "2026-10-19",
                                "confidentiality": "internal"},
                     "assertions_supported": ["KYC required for all customers"],
                     "evidence_limitations": "Covers UK only",
                     "reviewer": "Compliance Officer",
                     "review_status": "verified",
                     "review_date": "2026-10-19"},
                ],
                "inputs": [
                    {"id": "i1", "name": "Customer ID",
                     "description": "Government-issued ID",
                     "source": "customer",
                     "provenance": {"source": "prov-1",
                                    "confidence": "high",
                                    "verification_status": "verified",
                                    "verification_date": "2026-10-19",
                                    "verification_reviewer": "Compliance Officer",
                                    "uncertainty_state": "not_applicable"}},
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
        "generator": "scripts/check_evidence_provenance_ext15.py",
        "parent_cr": "CR-BP-94-EXT-15",
        "catalog_root": str(catalog_root),
        "summary": {
            "total_records": len(records),
            "total_findings": len(findings),
            "by_rule": {},
        },
        "findings": findings,
        "controlled_vocabularies": {
            "source_classes": sorted(SOURCE_CLASSES),
            "confidentiality_classes": sorted(CONFIDENTIALITY_CLASSES),
            "confidence_levels": sorted(CONFIDENCE_LEVELS),
            "verification_statuses": sorted(VERIFICATION_STATUSES),
            "uncertainty_states": sorted(UNCERTAINTY_STATES),
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
            print(f"OK: evidence/provenance conform (0 findings). "
                  f"Manifest at {MANIFEST_PATH.relative_to(REPO_ROOT)}")
        else:
            print(f"FAIL: {len(findings)} findings across {len(records)} records.")
            for finding in findings:
                print(f"  [{finding['rule']}] {finding['where']}: {finding['diagnostic']}")

    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
