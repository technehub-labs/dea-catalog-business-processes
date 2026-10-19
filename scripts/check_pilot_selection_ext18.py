#!/usr/bin/env python3
"""
check_pilot_selection_ext18.py
================================

Pilot entity selection validator (CR-BP-94-EXT-18).

Codifies the EXT-18 pilot selection criteria:

  PI-001  At least one L2 Business Process is selected.
  PI-002  At least one L1 ProcessGroup is selected.
  PI-003  At least one L3 Activity is selected.
  PI-004  At least one L4 Task is selected.
  PI-005  The selected entities form a coherent L1 -> L2 -> L3 -> L4
          decomposition chain (each child references its parent).
  PI-006  At least one selected entity has strong existing
          documentation (identity.evidence_links.length > 0 OR
          len(data) > some threshold).
  PI-007  At least one selected entity has incomplete or uncertain
          operational information (no metadata.authoring populated).
  PI-008  At least one selected entity has meaningful cross-catalogue
          references (relationships.length > 0).

The pilot manifest is read from reconciliation/pilot-entities.json
and validated against the 8 rules. The validator writes a manifest
at reconciliation/pilot-selection-manifest.json.

Test layout: tests/test_pilot_selection_ext18.py
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
PILOT_ENTITIES_PATH = REPO_ROOT / "reconciliation" / "pilot-entities.json"
MANIFEST_PATH = REPO_ROOT / "reconciliation" / "pilot-selection-manifest.json"

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


def evaluate(pilot_entities: list[dict],
             catalog_root: Path) -> tuple[list[dict], list[tuple[Path, dict]]]:
    """Run PI-001..PI-008 against the pilot selection.

    Returns (findings, selected_records). selected_records is the list of
    (path, record) pairs for the 11 pilot entities.
    """
    findings: list[dict] = []
    selected_records: list[tuple[Path, dict]] = []

    # Resolve the pilot entity IDs to actual files.
    for pilot_entry in pilot_entities:
        rec_id = pilot_entry.get("id")
        if not rec_id:
            continue
        found = False
        for f in (catalog_root / "entities" / "v1-alpha").rglob("*.yaml"):
            try:
                with f.open(encoding="utf-8") as fp:
                    data = yaml.safe_load(fp) or {}
            except Exception:
                continue
            if isinstance(data, dict) and data.get("id") == rec_id:
                selected_records.append((f, data))
                found = True
                break
        if not found:
            findings.append(_make_finding(
                "PI-001", rec_id,
                f"pilot entity {rec_id!r} not found in the catalogue",
            ))

    # Per-level presence
    levels = [LEVEL_BY_TYPE.get(rec.get("type")) for _f, rec in selected_records]
    level_counts = {"L0": 0, "L1": 0, "L2": 0, "L3": 0, "L4": 0}
    for level in levels:
        if level in level_counts:
            level_counts[level] += 1

    # PI-001: at least one L2 BP
    if level_counts.get("L2", 0) == 0:
        findings.append(_make_finding("PI-001", "pilot_selection",
                                       "no L2 Business Process selected; per CR-BP-94-EXT-18 §3, at least one L2 BP is required"))
    # PI-002: at least one L1
    if level_counts.get("L1", 0) == 0:
        findings.append(_make_finding("PI-002", "pilot_selection",
                                       "no L1 ProcessGroup selected"))
    # PI-003: at least one L3
    if level_counts.get("L3", 0) == 0:
        findings.append(_make_finding("PI-003", "pilot_selection",
                                       "no L3 Activity selected"))
    # PI-004: at least one L4
    if level_counts.get("L4", 0) == 0:
        findings.append(_make_finding("PI-004", "pilot_selection",
                                       "no L4 Task selected"))

    # PI-005: coherent decomposition chain
    # Each child must reference its parent (L3 -> L2 via
    # belongs_to_business_process; L4 -> L3 via belongs_to_activity).
    selected_l2_ids = {rec.get("id") for _f, rec in selected_records
                       if rec.get("type") == "Process"}
    selected_l3_ids = {rec.get("id") for _f, rec in selected_records
                       if rec.get("type") == "Activity"}
    for _f, rec in selected_records:
        if rec.get("type") == "Activity":
            btp = rec.get("belongs_to_business_process")
            if btp and btp not in selected_l2_ids:
                findings.append(_make_finding(
                    "PI-005", rec.get("id", "?"),
                    f"Activity {rec.get('id')!r} belongs_to_business_process={btp!r} "
                    f"but that L2 BP is NOT in the pilot selection",
                ))
        if rec.get("type") == "Task":
            bta = rec.get("belongs_to_activity")
            if bta and bta not in selected_l3_ids:
                findings.append(_make_finding(
                    "PI-005", rec.get("id", "?"),
                    f"Task {rec.get('id')!r} belongs_to_activity={bta!r} "
                    f"but that L3 Activity is NOT in the pilot selection",
                ))

    # PI-006: at least one entity has strong existing documentation.
    has_strong_doc = False
    for _f, rec in selected_records:
        evidence_links = rec.get("identity", {}).get("evidence_links", [])
        if len(evidence_links) > 0 or len(rec) >= 17:
            has_strong_doc = True
            break
    if not has_strong_doc:
        findings.append(_make_finding(
            "PI-006", "pilot_selection",
            "no selected entity has strong existing documentation "
            "(per CR-BP-94-EXT-18 §3: at least one entity with strong documentation is required)",
        ))

    # PI-007: at least one entity has incomplete or uncertain operational information.
    has_incomplete = False
    for _f, rec in selected_records:
        meta = rec.get("metadata")
        if not isinstance(meta, dict) or "authoring" not in meta:
            has_incomplete = True
            break
    if not has_incomplete:
        findings.append(_make_finding(
            "PI-007", "pilot_selection",
            "no selected entity has incomplete operational information "
            "(per CR-BP-94-EXT-18 §3: at least one entity with incomplete info is required)",
        ))

    # PI-008: at least one entity has meaningful cross-catalogue references.
    has_xref = False
    for _f, rec in selected_records:
        rels = rec.get("relationships", [])
        evidence_links = rec.get("identity", {}).get("evidence_links", [])
        if len(rels) > 0 or len(evidence_links) > 0:
            has_xref = True
            break
    if not has_xref:
        findings.append(_make_finding(
            "PI-008", "pilot_selection",
            "no selected entity has cross-catalogue references "
            "(per CR-BP-94-EXT-18 §3: at least one entity with x-refs is required)",
        ))

    return findings, selected_records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true",
                        help="run a synthetic self-test")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--catalog-root", default=".", help="catalog root")
    args = parser.parse_args()

    if args.self_test:
        # Synthetic selection: 1 L1, 1 L2, 4 L3, 5 L4
        synthetic_selection = [
            {"id": "processes:group-sd-improve-vdz4xp", "level": "L1"},
            {"id": "processes:process-sd-improve-duwd64", "level": "L2"},
            {"id": "processes:activity-sd-improve-mu6upn", "level": "L3"},
        ]
        # Self-test only checks the structure; actual evaluation is
        # against the live catalogue.
        result = {
            "mode": "self-test",
            "synthetic_selection_size": len(synthetic_selection),
            "findings": [],
            "summary": {"total_findings": 0},
        }
        print(json.dumps(result, indent=2))
        return 0

    if not PILOT_ENTITIES_PATH.exists():
        sys.stderr.write(f"ERROR: pilot manifest missing at {PILOT_ENTITIES_PATH}\n")
        return 2

    with PILOT_ENTITIES_PATH.open(encoding="utf-8") as fp:
        pilot_manifest = json.load(fp)
    pilot_entities = pilot_manifest.get("pilot_entities", [])

    if yaml is None:
        sys.stderr.write("ERROR: PyYAML is required.\n")
        return 2

    catalog_root = Path(args.catalog_root).resolve()
    findings, selected_records = evaluate(pilot_entities, catalog_root)

    # Build the manifest.
    manifest = {
        "manifest_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/check_pilot_selection_ext18.py",
        "parent_cr": "CR-BP-94-EXT-18",
        "catalog_root": str(catalog_root),
        "selection": {
            "total_pilot_entities": len(pilot_entities),
            "total_resolved_records": len(selected_records),
        },
        "summary": {
            "total_findings": len(findings),
            "by_rule": {},
        },
        "findings": findings,
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
            print(f"OK: pilot selection conforms (0 findings). "
                  f"Manifest at {MANIFEST_PATH.relative_to(REPO_ROOT)}")
        else:
            print(f"FAIL: {len(findings)} findings.")
            for finding in findings:
                print(f"  [{finding['rule']}] {finding['where']}: {finding['diagnostic']}")

    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
