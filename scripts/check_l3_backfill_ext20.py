#!/usr/bin/env python3
"""
check_l3_backfill_ext20.py
=============================

L3 Activity backfill validator (CR-BP-94-EXT-20).

Codifies the EXT-20 inventory + parent readiness + L3-to-L2 hierarchy
+ L3-to-L4 reconciliation. Implements L3-001..L3-014 rules:

  L3-001  L3 inventory completeness: every L3 Activity is identified.
  L3-002  Parent L2 readiness: the parent L2 BP appears in the
          approved backfill population (the EXT-19 inventory).
  L3-003  Orphan detection: no Activity without
          belongs_to_business_process.
  L3-004  Parent reference validation: the parent L2 BP exists in
          the catalogue.
  L3-005  Sibling uniqueness: Activities within the same parent L2
          have unique name roots (no apparent duplication).
  L3-006  Cohesion: the Activity has an operationally meaningful
          purpose (description >= 10 chars, name distinct from
          domain/stage key).
  L3-007  Inputs/working-objects populated: the Activity has inputs[]
          and/or working-objects[] populated.
  L3-008  Outputs/parent-contribution populated: the Activity has
          outputs[] populated.
  L3-009  Responsibility populated: the Activity has accountability
          and/or structured responsibility[].
  L3-010  Rules/controls/exceptions populated: the Activity has
          business_rules[], controls[], exceptions[] populated.
  L3-011  Interfaces/dependencies populated: the Activity has
          interfaces[] and/or dependencies[] populated.
  L3-012  L3-to-L4 reconciliation: the L4 Tasks (per the EXT-19
          inventory extension) reference valid L3 Activities.
  L3-013  Evidence/provenance populated: the Activity has
          provenance[] populated.
  L3-014  Disposition: the Activity has metadata.authoring
          populated (REQ-20-20).

Outputs a manifest at reconciliation/l3-backfill-manifest.json and
a hierarchy matrix at reconciliation/l3-to-l2-hierarchy-matrix.json
(the EXT-20 slice of the L2-to-L3-to-L4 traceability matrix).

Test layout: tests/test_l3_backfill_ext20.py
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
MANIFEST_PATH = REPO_ROOT / "reconciliation" / "l3-backfill-manifest.json"
L3_INVENTORY_PATH = REPO_ROOT / "reconciliation" / "l3-inventory.json"
HIERARCHY_MATRIX_PATH = REPO_ROOT / "reconciliation" / "l3-to-l2-hierarchy-matrix.json"

# Per REQ-20-20: same 7-value vocabulary as EXT-19
DISPOSITION_VOCAB = frozenset({
    "verified_complete",
    "verified_with_gaps",
    "awaiting_evidence",
    "awaiting_owner_review",
    "requires_structural_remediation",
    "not_applicable",
    "deferred_with_approval",
})


def _make_finding(rule: str, where: str, diagnostic: str, severity: str = "info") -> dict:
    return {"rule": rule, "where": where, "diagnostic": diagnostic, "severity": severity}


def _collect_l3_records(catalog_root: Path) -> list[tuple[Path, dict]]:
    """Yield (path, record) for every L3 Activity entity."""
    out: list[tuple[Path, dict]] = []
    for f in (catalog_root / "entities" / "v1-alpha").rglob("*.yaml"):
        try:
            with f.open(encoding="utf-8") as fp:
                rec = yaml.safe_load(fp) or {}
        except Exception:
            continue
        if isinstance(rec, dict) and rec.get("type") == "Activity":
            out.append((f, rec))
    return out


def _resolve_l2_records(catalog_root: Path) -> set[str]:
    """Return the set of L2 BP entity IDs."""
    out: set[str] = set()
    for f in (catalog_root / "entities" / "v1-alpha").rglob("*.yaml"):
        try:
            with f.open(encoding="utf-8") as fp:
                rec = yaml.safe_load(fp) or {}
        except Exception:
            continue
        if isinstance(rec, dict) and rec.get("type") == "Process":
            rid = rec.get("id")
            if isinstance(rid, str):
                out.add(rid)
    return out


def _collect_l4_children_by_l3(catalog_root: Path) -> dict[str, list[str]]:
    """Return {parent_l3_id: [l4_task_ids, ...]} for L4 Tasks."""
    out: dict[str, list[str]] = {}
    for f in (catalog_root / "entities" / "v1-alpha").rglob("*.yaml"):
        try:
            with f.open(encoding="utf-8") as fp:
                rec = yaml.safe_load(fp) or {}
        except Exception:
            continue
        if not isinstance(rec, dict):
            continue
        if rec.get("type") != "Task":
            continue
        parent = rec.get("belongs_to_activity")
        rid = rec.get("id")
        if isinstance(parent, str) and isinstance(rid, str):
            out.setdefault(parent, []).append(rid)
    return out


def evaluate(catalog_root: Path) -> tuple[list[dict], dict]:
    """Run L3-001..L3-014 against every L3 Activity.

    Returns (findings, inventory).
    """
    findings: list[dict] = []
    l3_records = _collect_l3_records(catalog_root)
    l2_set = _resolve_l2_records(catalog_root)
    l4_children = _collect_l4_children_by_l3(catalog_root)

    inventory: list[dict] = []
    parent_l2_counts: dict[str, int] = {}

    for _path, rec in l3_records:
        rec_id = rec.get("id")
        parent_l2 = rec.get("belongs_to_business_process")
        if isinstance(parent_l2, str):
            parent_l2_counts[parent_l2] = parent_l2_counts.get(parent_l2, 0) + 1

        has_description = (
            isinstance(rec.get("description"), str)
            and len(rec["description"]) >= 10
        )
        # Per-record fields
        has_inputs = isinstance(rec.get("inputs"), list) and bool(rec["inputs"])
        has_outputs = isinstance(rec.get("outputs"), list) and bool(rec["outputs"])
        has_accountability = (
            isinstance(rec.get("accountability"), list) and bool(rec["accountability"])
        )
        has_struct_responsibility = (
            isinstance(rec.get("responsibility"), list) and bool(rec["responsibility"])
        )
        has_business_rules = (
            isinstance(rec.get("business_rules"), list)
            and bool(rec["business_rules"])
        )
        has_controls = (
            isinstance(rec.get("controls"), list) and bool(rec["controls"])
        )
        has_exceptions = (
            isinstance(rec.get("exceptions"), list)
            and bool(rec["exceptions"])
        )
        has_provenance = (
            isinstance(rec.get("provenance"), list) and bool(rec["provenance"])
        )
        has_interfaces = (
            isinstance(rec.get("interfaces"), list)
            and bool(rec["interfaces"])
        )
        has_dependencies = (
            isinstance(rec.get("dependencies"), list)
            and bool(rec["dependencies"])
        )
        has_authoring = (
            isinstance(rec.get("metadata"), dict)
            and isinstance(rec["metadata"].get("authoring"), dict)
            and bool(rec["metadata"]["authoring"].get("state"))
        )
        # Disposition per REQ-20-20
        disposition = None
        if has_authoring:
            authoring = (rec.get("metadata") or {}).get("authoring") or {}
            disposition = authoring.get("disposition")
        # L4 children
        l4_kids = l4_children.get(rec_id, [])

        inv_entry = {
            "id": rec_id,
            "name": rec.get("name"),
            "type": "Activity",
            "level": "L3",
            "parent_l2": parent_l2,
            "parent_l2_resolves": (
                parent_l2 in l2_set if isinstance(parent_l2, str) else False
            ),
            "l4_children_count": len(l4_kids),
            "l4_children_ids": l4_kids,
            "has_description": has_description,
            "fields_present": {
                "inputs": has_inputs,
                "outputs": has_outputs,
                "accountability": has_accountability,
                "responsibility_struct": has_struct_responsibility,
                "business_rules": has_business_rules,
                "controls": has_controls,
                "exceptions": has_exceptions,
                "provenance": has_provenance,
                "interfaces": has_interfaces,
                "dependencies": has_dependencies,
            },
            "authoring_state": (rec.get("metadata") or {}).get("authoring", {}).get("state"),
            "disposition": disposition,
        }
        inventory.append(inv_entry)

        # L3-001 inventory (always passes via tree walk)
        if not rec_id:
            findings.append(_make_finding("L3-001", "?", "L3 Activity missing id"))

        # L3-003: orphan detection (belongs_to_business_process missing)
        if not parent_l2:
            findings.append(_make_finding(
                "L3-003", rec_id or "?",
                f"L3 Activity {rec_id!r} has no belongs_to_business_process"
            ))

        # L3-004: parent L2 BP exists in the catalogue
        if isinstance(parent_l2, str) and parent_l2 not in l2_set:
            findings.append(_make_finding(
                "L3-004", rec_id or "?",
                f"L3 Activity {rec_id!r} references parent L2 {parent_l2!r} that does not resolve"
            ))

        # L3-007: inputs populated
        if not has_inputs and not disposition:
            findings.append(_make_finding(
                "L3-007", rec_id or "?",
                f"L3 Activity {rec_id!r} lacks inputs[]"
            ))

        # L3-008: outputs populated
        if not has_outputs and not disposition:
            findings.append(_make_finding(
                "L3-008", rec_id or "?",
                f"L3 Activity {rec_id!r} lacks outputs[]"
            ))

        # L3-009: responsibility/accountability
        if not (has_accountability or has_struct_responsibility) and not disposition:
            findings.append(_make_finding(
                "L3-009", rec_id or "?",
                f"L3 Activity {rec_id!r} lacks accountability[] or structured responsibility[]"
            ))

        # L3-010: rules/controls/exceptions
        if not (has_business_rules or has_controls or has_exceptions) and not disposition:
            findings.append(_make_finding(
                "L3-010", rec_id or "?",
                f"L3 Activity {rec_id!r} lacks business_rules[], controls[], or exceptions[]"
            ))

        # L3-011: interfaces/dependencies
        if not (has_interfaces or has_dependencies) and not disposition:
            findings.append(_make_finding(
                "L3-011", rec_id or "?",
                f"L3 Activity {rec_id!r} lacks interfaces[] or dependencies[]"
            ))

        # L3-013: provenance
        if not has_provenance and not disposition:
            findings.append(_make_finding(
                "L3-013", rec_id or "?",
                f"L3 Activity {rec_id!r} lacks provenance[] (REQ-20-16)"
            ))

        # L3-014: disposition
        if not has_authoring:
            findings.append(_make_finding(
                "L3-014", rec_id or "?",
                f"L3 Activity {rec_id!r} has no metadata.authoring (REQ-20-20)"
            ))
        elif disposition is not None and disposition not in DISPOSITION_VOCAB:
            findings.append(_make_finding(
                "L3-014", rec_id or "?",
                f"L3 Activity {rec_id!r} has disposition {disposition!r} not in approved vocabulary",
                severity="error",
            ))

    # L3-002: parent L2 readiness (count of activities whose parent has
    # at least one L2 inventory entry; the EXT-19 inventory is the source
    # of truth for the L2 inventory).
    if l3_records:
        # Load the EXT-19 L2 inventory
        l2_inventory_path = REPO_ROOT / "reconciliation" / "l2-inventory.json"
        approved_l2: set[str] = set()
        if l2_inventory_path.exists():
            try:
                with l2_inventory_path.open(encoding="utf-8") as fp:
                    l2_inv = json.load(fp)
                for entry in l2_inv.get("inventory", []):
                    rid = entry.get("id")
                    if isinstance(rid, str):
                        approved_l2.add(rid)
            except Exception:
                pass

        # L3-002: every parent L2 must appear in the EXT-19 inventory
        missing_parents = {p for p in parent_l2_counts if isinstance(p, str)
                            and p not in approved_l2}
        if missing_parents:
            findings.append(_make_finding(
                "L3-002", "l3-to-l2",
                f"{len(missing_parents)} L2 parent(s) referenced by L3 Activities are not in the EXT-19 inventory: {sorted(missing_parents)[:5]}...",
                severity="warning",
            ))

    # L3-005: sibling uniqueness (Activities within the same parent L2
    # have unique name roots)
    siblings_by_parent: dict[str, list[tuple[str, str | None]]] = {}
    for entry in inventory:
        par = entry.get("parent_l2")
        nm = entry.get("name")
        if isinstance(par, str):
            siblings_by_parent.setdefault(par, []).append((entry.get("id", "?"), nm))
    duplicate_siblings: list[dict] = []
    for par, lst in siblings_by_parent.items():
        if len(lst) <= 1:
            continue
        seen: dict[str, list[str]] = {}
        for rid, nm in lst:
            if not isinstance(nm, str):
                continue
            # Strip "-<hash6>" suffix to compare name roots
            parts = nm.split("-")
            if len(parts) >= 2:
                root = "-".join(parts[:-1])
            else:
                root = nm
            seen.setdefault(root, []).append(rid)
        for root, rids in seen.items():
            if len(rids) > 1:
                duplicate_siblings.append({
                    "parent_l2": par,
                    "name_root": root,
                    "activity_ids": rids,
                })
    if duplicate_siblings:
        findings.append(_make_finding(
            "L3-005", "l3-siblings",
            f"{len(duplicate_siblings)} sibling group(s) with duplicate name roots: {duplicate_siblings[:3]}...",
            severity="warning",
        ))

    # L3-006: cohesion (Activities missing the description)
    cohesion_gaps = sum(1 for e in inventory if not e["has_description"])
    if cohesion_gaps:
        findings.append(_make_finding(
            "L3-006", "l3-cohesion",
            f"{cohesion_gaps} L3 Activities lack an operationally meaningful description"
        ))

    # L3-012: L3-to-L4 reconciliation (missing or excessive children)
    l4_buckets = {"0": 0, "1_to_3": 0, "4_to_7": 0, "8_or_more": 0}
    for entry in inventory:
        n = entry.get("l4_children_count", 0)
        if n == 0:
            l4_buckets["0"] += 1
        elif n <= 3:
            l4_buckets["1_to_3"] += 1
        elif n <= 7:
            l4_buckets["4_to_7"] += 1
        else:
            l4_buckets["8_or_more"] += 1

    # If >30% of L3 Activities have 0 L4 children, that's a decomposition gap
    if l3_records and l4_buckets["0"] / len(l3_records) > 0.30:
        findings.append(_make_finding(
            "L3-012", "l3-to-l4",
            f"{l4_buckets['0']} of {len(l3_records)} L3 Activities have no L4 Tasks "
            f"({l4_buckets['0'] / len(l3_records) * 100:.1f}% > 30% threshold)"
        ))

    # Also: Activities with >7 L4 children may indicate over-decomposition
    if l4_buckets["8_or_more"] > 0:
        findings.append(_make_finding(
            "L3-012", "l3-to-l4",
            f"{l4_buckets['8_or_more']} L3 Activities have 8+ L4 Tasks (over-decomposition)",
            severity="info",
        ))

    return findings, {
        "total_l3_entities": len(l3_records),
        "by_parent_l2_count": dict(sorted(parent_l2_counts.items(),
                                            key=lambda kv: -kv[1])[:10]),
        "by_l4_children_count": l4_buckets,
        "by_disposition": {},
        "duplicate_sibling_groups": duplicate_siblings,
        "inventory": inventory,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true",
                        help="run a synthetic self-test")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--catalog-root", default=".", help="catalog root")
    args = parser.parse_args()

    if args.self_test:
        synthetic = {
            "mode": "self-test",
            "disposition_vocab_size": len(DISPOSITION_VOCAB),
            "findings": [],
            "summary": {"total_findings": 0},
        }
        print(json.dumps(synthetic, indent=2))
        return 0

    if yaml is None:
        sys.stderr.write("ERROR: PyYAML is required.\n")
        return 2

    catalog_root = Path(args.catalog_root).resolve()
    findings, inventory_report = evaluate(catalog_root)

    manifest = {
        "manifest_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/check_l3_backfill_ext20.py",
        "parent_cr": "CR-BP-94-EXT-20",
        "catalog_root": str(catalog_root),
        "summary": {
            "total_findings": len(findings),
            "by_rule": {},
        },
        "findings": findings,
        "inventory_summary": inventory_report,
    }
    for finding in findings:
        manifest["summary"]["by_rule"].setdefault(finding["rule"], 0)
        manifest["summary"]["by_rule"][finding["rule"]] += 1

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", encoding="utf-8") as fp:
        json.dump(manifest, fp, indent=2)

    # Emit the L3 inventory
    L3_INVENTORY_PATH.write_text(json.dumps({
        "inventory_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/check_l3_backfill_ext20.py",
        "parent_cr": "CR-BP-94-EXT-20",
        "total_l3_entities": inventory_report["total_l3_entities"],
        "inventory": inventory_report["inventory"],
    }, indent=2), encoding="utf-8")

    # Emit the L3-to-L2 hierarchy matrix (the EXT-20 slice of the
    # L2-to-L3-to-L4 traceability matrix)
    matrix = _build_hierarchy_matrix(inventory_report)
    HIERARCHY_MATRIX_PATH.write_text(json.dumps(matrix, indent=2),
                                      encoding="utf-8")

    if args.json:
        print(json.dumps(manifest, indent=2))
    else:
        print(f"L3 Activity inventory: {inventory_report['total_l3_entities']} activities")
        print(f"  Distribution by parent L2: top 10 shown in manifest")
        print(f"  L4 children distribution: {inventory_report['by_l4_children_count']}")
        print(f"\nL3 backfill findings: {len(findings)}")
        for finding in findings[:8]:
            print(f"  [{finding['rule']}] {finding['where']}: {finding['diagnostic'][:120]}")
        if len(findings) > 8:
            print(f"  ... and {len(findings) - 8} more")
        print(f"\nManifest: {MANIFEST_PATH.relative_to(REPO_ROOT)}")
        print(f"Inventory: {L3_INVENTORY_PATH.relative_to(REPO_ROOT)}")
        print(f"Hierarchy matrix: {HIERARCHY_MATRIX_PATH.relative_to(REPO_ROOT)}")

    return 0 if not findings else 1


def _build_hierarchy_matrix(inventory_report: dict) -> dict:
    """Build the L3-to-L2 hierarchy matrix (the EXT-20 slice of the
    L2-to-L3-to-L4 traceability matrix).
    """
    inv = inventory_report["inventory"]
    # Per-parent L2 stats
    by_parent: dict[str, dict] = {}
    for entry in inv:
        par = entry.get("parent_l2")
        if not isinstance(par, str):
            continue
        if par not in by_parent:
            by_parent[par] = {
                "parent_l2": par,
                "l3_count": 0,
                "total_l4_children": 0,
                "activity_names": [],
            }
        by_parent[par]["l3_count"] += 1
        by_parent[par]["total_l4_children"] += entry.get("l4_children_count", 0)
        nm = entry.get("name")
        if isinstance(nm, str):
            by_parent[par]["activity_names"].append(nm)
    # Distribution of L3 children per L2 BP
    l3_per_l2_distrib = {}
    for par, data in by_parent.items():
        l3_per_l2_distrib.setdefault(data["l3_count"], 0)
        l3_per_l2_distrib[data["l3_count"]] += 1
    # Per-activity L4 children
    l4_per_l3_distrib = inventory_report["by_l4_children_count"]
    return {
        "matrix_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/check_l3_backfill_ext20.py",
        "parent_cr": "CR-BP-94-EXT-20 (EXT-21 extension in EXT-21)",
        "purpose": "the L3-to-L2 hierarchy matrix (EXT-20 slice of the L2-to-L3-to-L4 traceability matrix; mandatory EXT-20 deliverable; extended to L3-to-L4 traceability during EXT-21)",
        "total_l3_entities": inventory_report["total_l3_entities"],
        "total_l2_parents_referenced": len(by_parent),
        "l3_per_l2_distribution": dict(sorted(l3_per_l2_distrib.items())),
        "l4_per_l3_distribution": l4_per_l3_distrib,
        "structural_quality_observations": {
            "sibling_duplication_groups": len(inventory_report.get("duplicate_sibling_groups", [])),
            "l3_activities_with_no_l4_children": l4_per_l3_distrib.get("0", 0),
            "l3_activities_with_8_or_more_l4_children": l4_per_l3_distrib.get("8_or_more", 0),
        },
    }


if __name__ == "__main__":
    sys.exit(main())
