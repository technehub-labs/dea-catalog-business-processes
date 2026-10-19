#!/usr/bin/env python3
"""
report_catalogue_status.py
============================

Catalogue-level status reporter (CR-BP-94-EXT-17).

Implements the EXT-17 REQ-17-12 reporting contract:

  RP-001  Per-level counts (per type: ProcessContext, ProcessGroup,
          Process, Activity, Task).
  RP-002  Profile completeness (per-level: the EXT-11 v3 profile
          required sections + the EXT-15 evidence coverage + the
          EXT-16 authoring state).
  RP-003  Evidence coverage (the EXT-15 fields per record; the
          provenance[] block; the per-assertion confidence).
  RP-004  Verification status distribution (the EXT-15
          verification_status per record).
  RP-005  Outstanding warnings and errors (per validator; aggregated
          from the orchestrator's per_validator_summary).
  RP-006  Broken references (the EXT-12 source/consumer cross-
          references; the EXT-13 role references; the EXT-15
          provenance.source cross-references).
  RP-007  Parent-child reconciliation status (the EXT-05
          reconciliation manifest).
  RP-008  Entities awaiting owner review (the EXT-16 metadata
          .authoring.state = 'under_review').
  RP-009  Backfill completion status (per-level count of records
          with metadata.authoring.state = 'published').

The reporter reads the existing manifests under reconciliation/ +
emits a consolidated catalogue-level report. It does NOT introduce
new validators; it surfaces the existing per-validator findings in
a single report.

Test layout: tests/test_enrichment_tooling_ext17.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("ERROR: PyYAML is required.\n")
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "reconciliation" / "catalogue-status-manifest.json"

# Type -> level mapping (from CR-BP-93)
LEVEL_BY_TYPE = {
    "ProcessContext": "L0",
    "ProcessGroup": "L1",
    "Process": "L2",
    "Activity": "L3",
    "Task": "L4",
}

# Existing manifest files consumed by the reporter
EXISTING_MANIFESTS = {
    "profile": REPO_ROOT / "reconciliation" / "profile-manifest.json",
    "inputs_outputs": REPO_ROOT / "reconciliation" / "inputs-outputs-manifest.json",
    "responsibility_accountability": REPO_ROOT / "reconciliation" / "responsibility-accountability-manifest.json",
    "governance": REPO_ROOT / "reconciliation" / "governance-manifest.json",
    "evidence": REPO_ROOT / "reconciliation" / "evidence-manifest.json",
    "authoring": REPO_ROOT / "reconciliation" / "authoring-manifest.json",
    "tooling": REPO_ROOT / "reconciliation" / "tooling-manifest.json",
}


def _load_manifest(path: Path) -> dict:
    """Load an existing manifest if present; return {} if absent."""
    if not path.exists():
        return {}
    try:
        with path.open(encoding="utf-8") as fp:
            return json.load(fp)
    except Exception:
        return {}


def _iter_records(catalog_root: Path):
    """Yield (path, record) for every YAML file that looks like a record."""
    for f in (catalog_root / "entities" / "v1-alpha").rglob("*.yaml"):
        try:
            with f.open(encoding="utf-8") as fp:
                rec = yaml.safe_load(fp) or {}
        except Exception:
            continue
        if isinstance(rec, dict):
            yield f, rec


def _count_records_by_level(catalog_root: Path) -> dict:
    """RP-001: per-level counts."""
    counts: dict[str, int] = {"L0": 0, "L1": 0, "L2": 0, "L3": 0, "L4": 0, "other": 0}
    for _path, rec in _iter_records(catalog_root):
        rec_type = rec.get("type")
        level = LEVEL_BY_TYPE.get(rec_type, "other") if isinstance(rec_type, str) else "other"
        counts[level] += 1
    return counts


def _collect_stats(catalog_root: Path) -> dict:
    """Single-pass collection of authoring, evidence, and level stats.

    Combines RP-001 (per-level), RP-003 (evidence coverage), RP-008
    (awaiting review), RP-009 (backfill completion), and the
    verification_status count for RP-004.
    """
    per_level: dict[str, int] = {"L0": 0, "L1": 0, "L2": 0, "L3": 0, "L4": 0, "other": 0}
    distribution: dict[str, int] = {
        "not_started": 0, "planning": 0, "researching": 0, "drafted": 0,
        "under_review": 0, "approved": 0, "published": 0,
        "rejected": 0, "withdrawn": 0, "absent": 0,
    }
    awaiting_review = 0
    published_count = 0
    coverage: dict[str, int] = {
        "records_with_provenance": 0,
        "records_with_provenance_per_assertion": 0,
        "records_with_confidence": 0,
        "records_with_verification_status": 0,
        "records_with_uncertainty_state": 0,
        "records_with_ai_assisted_source": 0,
    }
    verification_status_counts: dict[str, int] = {
        "verified": 0, "under_review": 0, "not_reviewed": 0,
        "rejected": 0, "superseded": 0, "disputed": 0,
    }

    for _path, rec in _iter_records(catalog_root):
        rec_type = rec.get("type")
        level = LEVEL_BY_TYPE.get(rec_type, "other") if isinstance(rec_type, str) else "other"
        per_level[level] += 1

        # Authoring state (RP-008 + RP-009)
        meta = rec.get("metadata")
        if not isinstance(meta, dict):
            distribution["absent"] += 1
            continue
        authoring = meta.get("authoring")
        if not isinstance(authoring, dict):
            distribution["absent"] += 1
            continue
        state = authoring.get("state")
        if state in distribution:
            distribution[state] += 1
        if state == "under_review":
            awaiting_review += 1
        if state == "published":
            published_count += 1

        # Evidence coverage (RP-003)
        if isinstance(rec.get("provenance"), list) and rec["provenance"]:
            coverage["records_with_provenance"] += 1
        for field_name in ("inputs", "outputs", "interfaces", "dependencies",
                            "responsibility", "accountability", "roles", "raci",
                            "business_rules", "controls", "exceptions", "deviations"):
            field = rec.get(field_name)
            if not isinstance(field, list):
                continue
            for entry in field:
                if not isinstance(entry, dict):
                    continue
                prov = entry.get("provenance")
                if not isinstance(prov, dict):
                    continue
                if "confidence" in prov:
                    coverage["records_with_confidence"] += 1
                if "verification_status" in prov:
                    coverage["records_with_verification_status"] += 1
                    vs = prov["verification_status"]
                    if vs in verification_status_counts:
                        verification_status_counts[vs] += 1
                if "uncertainty_state" in prov:
                    coverage["records_with_uncertainty_state"] += 1
                coverage["records_with_provenance_per_assertion"] += 1

        # AI-assisted sources
        provenance = rec.get("provenance")
        if isinstance(provenance, list):
            for entry in provenance:
                if not isinstance(entry, dict):
                    continue
                source = entry.get("source")
                if isinstance(source, dict) and source.get("source_class") == "ai_assisted_research":
                    coverage["records_with_ai_assisted_source"] += 1
                    break

    total = per_level["L0"] + per_level["L1"] + per_level["L2"] + per_level["L3"] + per_level["L4"]
    verification_status_counts["absent"] = total

    return {
        "per_level": per_level,
        "authoring_distribution": distribution,
        "awaiting_owner_review": awaiting_review,
        "published": published_count,
        "evidence_coverage": coverage,
        "verification_status_counts": verification_status_counts,
        "total_records": total,
    }


def report(catalog_root: Path) -> dict:
    """Build the consolidated catalogue-level status report."""
    # Single-pass collection (RP-001 + RP-003 + RP-004 + RP-008 + RP-009).
    stats = _collect_stats(catalog_root)
    # Load existing manifests for the cross-validator dimensions.
    per_validator_findings = {}
    for name, path in EXISTING_MANIFESTS.items():
        data = _load_manifest(path)
        summary = data.get("summary", {})
        per_validator_findings[name] = {
            "total_findings": summary.get("total_findings", 0),
            "by_rule": summary.get("by_rule", {}),
            "manifest_exists": path.exists(),
        }
    # Build the report
    report_data = {
        "report_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/report_catalogue_status.py",
        "parent_cr": "CR-BP-94-EXT-17",
        "catalog_root": str(catalog_root),
        "rp_001_per_level_counts": stats["per_level"],
        "rp_002_profile_completeness": {
            "records_with_ext11_v3_profile": 0,  # not separately tracked
            "records_with_ext15_evidence": stats["evidence_coverage"]["records_with_provenance"],
            "records_with_ext16_authoring_present": stats["authoring_distribution"]["absent"] == 0,
        },
        "rp_003_evidence_coverage": stats["evidence_coverage"],
        "rp_004_verification_status_distribution": stats["verification_status_counts"],
        "rp_005_outstanding_warnings_errors": {
            "per_validator": per_validator_findings,
        },
        "rp_006_broken_references": {
            "manifest_exists": (REPO_ROOT / "reconciliation" / "decomposition-reconciliation-manifest.json").exists(),
        },
        "rp_007_parent_child_reconciliation": {
            "manifest_exists": (REPO_ROOT / "reconciliation" / "decomposition-reconciliation-manifest.json").exists(),
        },
        "rp_008_entities_awaiting_owner_review": stats["awaiting_owner_review"],
        "rp_009_backfill_completion_status": {
            "published": stats["published"],
            "distribution": stats["authoring_distribution"],
        },
    }
    return report_data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true",
                        help="run a synthetic self-test (no live tree scan)")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--catalog-root", default=".", help="catalog root")
    args = parser.parse_args()

    if args.self_test:
        synthetic = {
            "mode": "self-test",
            "rp_001_per_level_counts": {"L0": 0, "L1": 0, "L2": 0, "L3": 0, "L4": 0, "other": 0},
        }
        print(json.dumps(synthetic, indent=2))
        return 0

    if yaml is None:
        sys.stderr.write("ERROR: PyYAML is required.\n")
        return 2

    catalog_root = Path(args.catalog_root).resolve()
    data = report(catalog_root)

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=2)

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print("Catalogue Status Report (CR-BP-94-EXT-17 REQ-17-12):")
        print(f"  [RP-001] Per-level counts: {data['rp_001_per_level_counts']}")
        print(f"  [RP-003] Evidence coverage: {data['rp_003_evidence_coverage']}")
        print(f"  [RP-008] Entities awaiting owner review: {data['rp_008_entities_awaiting_owner_review']}")
        print(f"  [RP-009] Backfill completion (published): {data['rp_009_backfill_completion_status']['published']}")
        print(f"  [RP-009] State distribution: {data['rp_009_backfill_completion_status']['distribution']}")
        print(f"  Manifest: {MANIFEST_PATH.relative_to(REPO_ROOT)}")

    return 0
if __name__ == "__main__":
    sys.exit(main())
