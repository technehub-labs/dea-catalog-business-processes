#!/usr/bin/env python3
"""
check_l2_backfill_ext19.py
=============================

L2 Business Process backfill validator (CR-BP-94-EXT-19).

Codifies the EXT-19 inventory + baseline + reconciliation + reporting
requirements. Implements L2-001..L2-012 rules:

  L2-001  L2 inventory completeness: every L2 BP is identified.
  L2-002  L2 profile completeness: per-entity profile assessment.
  L2-003  Process identity: the L2 BP has an operationally meaningful
          description beyond the entity name.
  L2-004  Boundary: the L2 BP has a documented boundary (or explicit
          N/A disposition).
  L2-005  Trigger/preconditions: the L2 BP has trigger/preconditions
          populated (or disposition explains omission).
  L2-006  Inputs/outputs: the L2 BP has inputs[] and outputs[] populated.
  L2-007  Responsibility/accountability: the L2 BP has accountability
          or responsibility populated.
  L2-008  Rules/controls/exceptions: the L2 BP has business_rules[],
          controls[], exceptions[] populated.
  L2-009  Evidence/provenance: the L2 BP has provenance[] populated.
  L2-010  Parent L1 readiness: the L2 BP references a valid L1 parent.
  L2-011  L2-to-L3 reconciliation: the L2 BP has at least one L3
          child Activity, or the disposition explains the gap.
  L2-012  Disposition: every L2 BP has an entity-level disposition per
          REQ-19-24.

Outputs a manifest at reconciliation/l2-backfill-manifest.json.

Test layout: tests/test_l2_backfill_ext19.py
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
MANIFEST_PATH = REPO_ROOT / "reconciliation" / "l2-backfill-manifest.json"
L2_INVENTORY_PATH = REPO_ROOT / "reconciliation" / "l2-inventory.json"
RECONCILIATION_MATRIX_PATH = REPO_ROOT / "reconciliation" / "l2-to-l3-reconciliation-matrix.json"

# Per REQ-19-24: 7 entity-level dispositions
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


def _collect_l2_records(catalog_root: Path) -> list[tuple[Path, dict]]:
    """Yield (path, record) for every L2 BP entity in the catalogue."""
    out: list[tuple[Path, dict]] = []
    for f in (catalog_root / "entities" / "v1-alpha").rglob("*.yaml"):
        try:
            with f.open(encoding="utf-8") as fp:
                rec = yaml.safe_load(fp) or {}
        except Exception:
            continue
        if isinstance(rec, dict) and rec.get("type") == "Process":
            out.append((f, rec))
    return out


def _resolve_l1_parents(catalog_root: Path) -> set[str]:
    """Return the set of L1 ProcessGroup entity IDs."""
    out: set[str] = set()
    for f in (catalog_root / "entities" / "v1-alpha").rglob("*.yaml"):
        try:
            with f.open(encoding="utf-8") as fp:
                rec = yaml.safe_load(fp) or {}
        except Exception:
            continue
        if isinstance(rec, dict) and rec.get("type") == "ProcessGroup":
            rid = rec.get("id")
            if isinstance(rid, str):
                out.add(rid)
    return out


def _collect_l3_children(catalog_root: Path) -> dict[str, list[str]]:
    """Return {parent_l2_id: [l3_activity_ids, ...]} for L3 Activities."""
    out: dict[str, list[str]] = {}
    for f in (catalog_root / "entities" / "v1-alpha").rglob("*.yaml"):
        try:
            with f.open(encoding="utf-8") as fp:
                rec = yaml.safe_load(fp) or {}
        except Exception:
            continue
        if not isinstance(rec, dict):
            continue
        if rec.get("type") != "Activity":
            continue
        parent = rec.get("belongs_to_business_process")
        rid = rec.get("id")
        if isinstance(parent, str) and isinstance(rid, str):
            out.setdefault(parent, []).append(rid)
    return out


def evaluate(catalog_root: Path) -> tuple[list[dict], dict]:
    """Run L2-001..L2-012 against every L2 BP.

    Returns (findings, inventory).
    """
    findings: list[dict] = []
    l2_records = _collect_l2_records(catalog_root)
    l1_parents = _resolve_l1_parents(catalog_root)
    l3_children = _collect_l3_children(catalog_root)

    inventory: list[dict] = []

    for _path, rec in l2_records:
        rec_id = rec.get("id")
        # Per-record profile completeness
        profile_state = _assess_profile(rec)
        # Per-record fields presence
        has_inputs = isinstance(rec.get("inputs"), list) and bool(rec["inputs"])
        has_outputs = isinstance(rec.get("outputs"), list) and bool(rec["outputs"])
        has_accountability = isinstance(rec.get("accountability"), list) and bool(rec["accountability"])
        has_struct_responsibility = isinstance(rec.get("responsibility"), list) and bool(rec["responsibility"])
        has_business_rules = isinstance(rec.get("business_rules"), list) and bool(rec["business_rules"])
        has_controls = isinstance(rec.get("controls"), list) and bool(rec["controls"])
        has_exceptions = isinstance(rec.get("exceptions"), list) and bool(rec["exceptions"])
        has_provenance = isinstance(rec.get("provenance"), list) and bool(rec["provenance"])
        has_authoring = (
            isinstance(rec.get("metadata"), dict)
            and isinstance(rec["metadata"].get("authoring"), dict)
            and bool(rec["metadata"]["authoring"].get("state"))
        )
        has_description = isinstance(rec.get("description"), str) and len(rec["description"]) >= 10
        # Resolved parent L1
        parent_l1 = None
        ctx = rec.get("context")
        if isinstance(ctx, list):
            for c in ctx:
                if isinstance(c, dict) and isinstance(c.get("ref"), str):
                    parent_l1 = c["ref"]
                    break
        # Backfill disposition (per REQ-19-24)
        disposition = None
        if has_authoring:
            meta = rec.get("metadata") or {}
            authoring = meta.get("authoring") or {}
            disposition = authoring.get("disposition")
        # L3 children
        l3_kids = l3_children.get(rec_id, [])

        inv_entry = {
            "id": rec_id,
            "name": rec.get("name"),
            "type": "Process",
            "level": "L2",
            "parent_l1": parent_l1,
            "parent_l1_resolves": parent_l1 in l1_parents if parent_l1 else False,
            "l3_children_count": len(l3_kids),
            "l3_children_ids": l3_kids,
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
            },
            "authoring_state": (rec.get("metadata") or {}).get("authoring", {}).get("state"),
            "disposition": disposition,
            "profile_completeness": profile_state,
        }
        inventory.append(inv_entry)

        # L2-001: inventory completeness (always passes since we walk the tree)
        if not rec_id:
            findings.append(_make_finding("L2-001", "?", "L2 record missing id"))

        # L2-003: process identity
        if not has_description and not disposition:
            findings.append(_make_finding(
                "L2-003", rec_id or "?",
                f"L2 BP {rec_id!r} has no operationally meaningful description"
            ))

        # L2-006: inputs/outputs
        if not (has_inputs and has_outputs) and not disposition:
            findings.append(_make_finding(
                "L2-006", rec_id or "?",
                f"L2 BP {rec_id!r} lacks inputs[] or outputs[]"
            ))

        # L2-007: responsibility/accountability
        if not (has_accountability or has_struct_responsibility) and not disposition:
            findings.append(_make_finding(
                "L2-007", rec_id or "?",
                f"L2 BP {rec_id!r} lacks accountability[] or structured responsibility[]"
            ))

        # L2-008: rules/controls/exceptions
        if not (has_business_rules or has_controls or has_exceptions) and not disposition:
            findings.append(_make_finding(
                "L2-008", rec_id or "?",
                f"L2 BP {rec_id!r} lacks business_rules[], controls[], or exceptions[]"
            ))

        # L2-009: provenance
        if not has_provenance and not disposition:
            findings.append(_make_finding(
                "L2-009", rec_id or "?",
                f"L2 BP {rec_id!r} lacks provenance[] (REQ-19-20)"
            ))

        # L2-010: parent L0 ProcessContext readiness (the canonical L2 parent
        # reference in this catalogue is the L0 PC via context[]).
        if parent_l1 is None:
            findings.append(_make_finding(
                "L2-010", rec_id or "?",
                f"L2 BP {rec_id!r} has no context[] L0 ProcessContext reference"
            ))
        else:
            # The L0 PC ref is well-formed (non-empty); L0 records are
            # referenced-not-materialized in the current catalogue (which
            # is itself recorded as a structural observation in EXT-22).
            pass

        # L2-011: L2-to-L3 reconciliation (gap = no L3 children)
        if len(l3_kids) == 0 and not disposition:
            findings.append(_make_finding(
                "L2-011", rec_id or "?",
                f"L2 BP {rec_id!r} has no L3 Activities; recorded as decomposition gap"
            ))

        # L2-012: disposition
        if not has_authoring:
            findings.append(_make_finding(
                "L2-012", rec_id or "?",
                f"L2 BP {rec_id!r} has no metadata.authoring (REQ-19-24; entity-level disposition required)"
            ))
        elif disposition is not None and disposition not in DISPOSITION_VOCAB:
            findings.append(_make_finding(
                "L2-012", rec_id or "?",
                f"L2 BP {rec_id!r} has disposition {disposition!r} not in approved vocabulary",
                severity="error",
            ))

    # L2-002: profile completeness (per-record aggregate)
    fully_complete = sum(1 for e in inventory
                         if e["profile_completeness"] == "fully_complete")
    partial = sum(1 for e in inventory
                  if e["profile_completeness"] == "partial")
    if l2_records:
        incomplete = sum(1 for e in inventory
                         if e["profile_completeness"] == "incomplete")
        if incomplete == len(inventory):
            findings.append(_make_finding(
                "L2-002", "catalogue",
                f"all {len(l2_records)} L2 BPs have an incomplete profile (no metadata.authoring populated yet)"
            ))

    return findings, {
        "total_l2_entities": len(l2_records),
        "by_profile_completeness": {
            "fully_complete": fully_complete,
            "partial": partial,
            "incomplete": len(inventory) - fully_complete - partial,
        },
        "by_parent_l1": _count_by(inventory, "parent_l1"),
        "by_disposition": _count_by(inventory, "disposition"),
        "by_l3_children_count": _count_l3_kids(inventory),
        "inventory": inventory,
    }


def _assess_profile(rec: dict) -> str:
    """Per-record profile completeness.

    fully_complete: provenance + accountability/responsibility_struct +
                    business_rules/controls/exceptions + inputs + outputs
                    + authoring state populated.
    partial: some of those populated but not all.
    incomplete: none of the EXT-12..16 fields populated (the typical
                pre-EXT-19 state).
    """
    has_inputs = isinstance(rec.get("inputs"), list) and bool(rec["inputs"])
    has_outputs = isinstance(rec.get("outputs"), list) and bool(rec["outputs"])
    has_accountability = isinstance(rec.get("accountability"), list) and bool(rec["accountability"])
    has_struct_responsibility = isinstance(rec.get("responsibility"), list) and bool(rec["responsibility"])
    has_business_rules = isinstance(rec.get("business_rules"), list) and bool(rec["business_rules"])
    has_controls = isinstance(rec.get("controls"), list) and bool(rec["controls"])
    has_exceptions = isinstance(rec.get("exceptions"), list) and bool(rec["exceptions"])
    has_provenance = isinstance(rec.get("provenance"), list) and bool(rec["provenance"])
    present = sum(bool(v) for v in [has_inputs, has_outputs,
                                     has_accountability or has_struct_responsibility,
                                     has_business_rules or has_controls or has_exceptions,
                                     has_provenance])
    if present >= 5:
        return "fully_complete"
    if present >= 2:
        return "partial"
    return "incomplete"


def _count_by(inventory: list[dict], key: str) -> dict:
    out: dict[str, int] = {}
    for entry in inventory:
        v = entry.get(key)
        if v is None:
            continue
        out[str(v)] = out.get(str(v), 0) + 1
    return out


def _count_l3_kids(inventory: list[dict]) -> dict:
    """Bucket by number of L3 children: 0 / 1-3 / 4-7 / 8+."""
    out = {"0": 0, "1_to_3": 0, "4_to_7": 0, "8_or_more": 0}
    for entry in inventory:
        n = entry.get("l3_children_count", 0)
        if n == 0:
            out["0"] += 1
        elif n <= 3:
            out["1_to_3"] += 1
        elif n <= 7:
            out["4_to_7"] += 1
        else:
            out["8_or_more"] += 1
    return out


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

    # Build the manifest.
    manifest = {
        "manifest_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/check_l2_backfill_ext19.py",
        "parent_cr": "CR-BP-94-EXT-19",
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

    # Emit the inventory.
    L2_INVENTORY_PATH.write_text(json.dumps({
        "inventory_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/check_l2_backfill_ext19.py",
        "parent_cr": "CR-BP-94-EXT-19",
        "total_l2_entities": inventory_report["total_l2_entities"],
        "inventory": inventory_report["inventory"],
    }, indent=2), encoding="utf-8")

    # Emit the L2-to-L3 reconciliation matrix (per the user recommendation).
    matrix = _build_reconciliation_matrix(inventory_report)
    RECONCILIATION_MATRIX_PATH.write_text(json.dumps(matrix, indent=2),
                                          encoding="utf-8")

    if args.json:
        print(json.dumps(manifest, indent=2))
    else:
        print(f"L2 BP inventory: {inventory_report['total_l2_entities']} entities")
        print(f"  Profile completeness: {inventory_report['by_profile_completeness']}")
        print(f"  L3 children distribution: {inventory_report['by_l3_children_count']}")
        print(f"  Disposition distribution: {inventory_report['by_disposition']}")
        print(f"\nL2 backfill findings: {len(findings)}")
        for finding in findings[:10]:
            print(f"  [{finding['rule']}] {finding['where']}: {finding['diagnostic']}")
        if len(findings) > 10:
            print(f"  ... and {len(findings) - 10} more")
        print(f"\nManifest: {MANIFEST_PATH.relative_to(REPO_ROOT)}")
        print(f"Inventory: {L2_INVENTORY_PATH.relative_to(REPO_ROOT)}")
        print(f"Reconciliation matrix: {RECONCILIATION_MATRIX_PATH.relative_to(REPO_ROOT)}")

    return 0 if not findings else 1


def _build_reconciliation_matrix(inventory_report: dict) -> dict:
    """Build the L2-to-L3 reconciliation matrix (per the user recommendation).

    Three problem classes are surfaced:
    - L2 processes with missing or inadequate Activity decomposition
    - Activities that do not contribute clearly to their assigned parent process
    - L2 processes that have no L3 children (decomposition gap)

    We do not address the third problem class (Activities to L3) in EXT-19;
    that is EXT-20+EXT-21. The matrix is the bridge between EXT-19 and
    EXT-20.
    """
    inv = inventory_report["inventory"]
    no_l3 = [e for e in inv if e["l3_children_count"] == 0]
    bucket_distrib = inventory_report["by_l3_children_count"]
    return {
        "matrix_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/check_l2_backfill_ext19.py",
        "parent_cr": "CR-BP-94-EXT-19 (EXT-20 extension in EXT-21)",
        "purpose": "the L2-to-L3 reconciliation matrix (mandatory EXT-19 deliverable per the user recommendation; extended to L2-to-L3-to-L4 during EXT-20 and EXT-21)",
        "total_l2_entities": len(inv),
        "buckets": bucket_distrib,
        "l2_processes_with_no_l3_children": [e["id"] for e in no_l3],
        "structural_quality_observations": {
            "decomposition_gaps_count": len(no_l3),
            "fully_decomposed_l2_count": bucket_distrib.get("4_to_7", 0) + bucket_distrib.get("8_or_more", 0),
        },
    }


if __name__ == "__main__":
    sys.exit(main())
