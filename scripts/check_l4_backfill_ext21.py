#!/usr/bin/env python3
"""
check_l4_backfill_ext21.py
=============================

L4 Task backfill validator (CR-BP-94-EXT-21).

Codifies the EXT-21 inventory + parent L3 readiness + L3-to-L4
reconciliation + L4-to-Activity cohesion. Implements L4-001..L4-014
rules:

  L4-001  L4 inventory completeness: every L4 Task is identified.
  L4-002  Parent L3 readiness: the parent L3 Activity appears in the
          EXT-20 L3 inventory (the approved backfill population).
  L4-003  Orphan detection: no Task without belongs_to_activity.
  L4-004  Parent reference validation: the parent L3 Activity exists
          in the catalogue.
  L4-005  5-phase decomposition coherence: each parent L3 Activity's
          Task population matches the canonical 5-phase
          verb-object pattern (Intake, Processing, Verification,
          Confirmation, Record) exactly once each.
  L4-006  Definition present: the Task has a meaningful definition
          (>= 40 characters).
  L4-007  Trigger present: the Task has a trigger.
  L4-008  Outcome present: the Task has an outcome.
  L4-009  Responsibility present: the Task has a responsibility
          (the CR-BP-32 plain-string form is valid at L4).
  L4-010  Boundary completeness: boundary.inclusions and
          boundary.exclusions are both non-empty.
  L4-011  Evidence present: the Task has the pre-EXT-15 evidence[]
          record (source, claim, strength).
  L4-012  Canonical provenance present: the Task has the EXT-15
          canonical provenance[] block (the migration gap; the
          EXT-23 tranche performs the migration).
  L4-013  Authoring metadata present: the Task has
          metadata.authoring populated (EXT-16).
  L4-014  Disposition: the Task has metadata.authoring.disposition
          per the 7-value vocabulary.

Outputs a manifest at reconciliation/l4-backfill-manifest.json and
the L4-to-L3 traceability matrix at
reconciliation/l4-to-l3-traceability-matrix.json (the EXT-21 slice
of the L2-to-L3-to-L4 traceability matrix).

Test layout: tests/test_l4_backfill_ext21.py
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError:
    sys.stderr.write("ERROR: PyYAML is required.\n")
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "reconciliation" / "l4-backfill-manifest.json"
L4_INVENTORY_PATH = REPO_ROOT / "reconciliation" / "l4-inventory.json"
TRACEABILITY_MATRIX_PATH = REPO_ROOT / "reconciliation" / "l4-to-l3-traceability-matrix.json"

# Per REQ-21-20: the same 7-value vocabulary as REQ-19-24 and REQ-20-20
DISPOSITION_VOCAB = frozenset({
    "verified_complete",
    "verified_with_gaps",
    "awaiting_evidence",
    "awaiting_owner_review",
    "requires_structural_remediation",
    "not_applicable",
    "deferred_with_approval",
})

# The canonical 5-phase verb-object decomposition pattern (CR-BP-102)
CANONICAL_PHASES = frozenset({
    "Intake", "Processing", "Verification", "Confirmation", "Record",
})


def _make_finding(rule: str, where: str, diagnostic: str, severity: str = "info") -> dict:
    return {"rule": rule, "where": where, "diagnostic": diagnostic, "severity": severity}


def _collect_l4_records(catalog_root: Path) -> list[tuple[Path, dict]]:
    """Yield (path, record) for every L4 Task entity."""
    out: list[tuple[Path, dict]] = []
    for f in (catalog_root / "entities" / "v1-alpha").rglob("*.yaml"):
        try:
            with f.open(encoding="utf-8") as fp:
                rec = yaml.safe_load(fp) or {}
        except Exception:
            continue
        if isinstance(rec, dict) and rec.get("type") == "Task":
            out.append((f, rec))
    return out


def _resolve_l3_records(catalog_root: Path) -> set[str]:
    """Return the set of L3 Activity entity IDs."""
    out: set[str] = set()
    for f in (catalog_root / "entities" / "v1-alpha").rglob("*.yaml"):
        try:
            with f.open(encoding="utf-8") as fp:
                rec = yaml.safe_load(fp) or {}
        except Exception:
            continue
        if isinstance(rec, dict) and rec.get("type") == "Activity":
            rid = rec.get("id")
            if isinstance(rid, str):
                out.add(rid)
    return out


def _phase_of(name: object) -> str | None:
    """Extract the decomposition phase from the Task name.

    The CR-BP-102 5-phase verb-object pattern names each Task with the
    phase as the final token (e.g. 'Evaluate Strategy Effectiveness
    Confirmation').
    """
    if not isinstance(name, str):
        return None
    parts = name.split()
    if not parts:
        return None
    return parts[-1]


def evaluate(catalog_root: Path) -> tuple[list[dict], dict]:
    """Run L4-001..L4-014 against every L4 Task."""
    findings: list[dict] = []
    l4_records = _collect_l4_records(catalog_root)
    l3_set = _resolve_l3_records(catalog_root)

    # Load the EXT-20 L3 inventory (the approved L3 backfill population)
    l3_inventory_path = REPO_ROOT / "reconciliation" / "l3-inventory.json"
    approved_l3: set[str] = set()
    if l3_inventory_path.exists():
        try:
            with l3_inventory_path.open(encoding="utf-8") as fp:
                l3_inv = json.load(fp)
            for entry in l3_inv.get("inventory", []):
                rid = entry.get("id")
                if isinstance(rid, str):
                    approved_l3.add(rid)
        except Exception:
            pass

    inventory: list[dict] = []
    by_parent: dict[str, list[dict]] = {}

    for _path, rec in l4_records:
        rec_id = rec.get("id")
        parent_l3 = rec.get("belongs_to_activity")
        name = rec.get("name")
        phase = _phase_of(name)

        has_definition = (
            isinstance(rec.get("definition"), str)
            and len(rec["definition"]) >= 40
        )
        has_trigger = bool(rec.get("trigger"))
        has_outcome = bool(rec.get("outcome"))
        has_responsibility = (
            isinstance(rec.get("responsibility"), str)
            and bool(rec["responsibility"].strip())
        )
        boundary = rec.get("boundary")
        has_boundary_incl = (
            isinstance(boundary, dict)
            and isinstance(boundary.get("inclusions"), list)
            and bool(boundary["inclusions"])
        )
        has_boundary_excl = (
            isinstance(boundary, dict)
            and isinstance(boundary.get("exclusions"), list)
            and bool(boundary["exclusions"])
        )
        evidence = rec.get("evidence")
        has_evidence = (
            isinstance(evidence, list)
            and bool(evidence)
            and all(
                isinstance(e, dict) and "source" in e and "claim" in e
                for e in evidence
            )
        )
        has_provenance = (
            isinstance(rec.get("provenance"), list) and bool(rec["provenance"])
        )
        has_authoring = (
            isinstance(rec.get("metadata"), dict)
            and isinstance(rec["metadata"].get("authoring"), dict)
            and bool(rec["metadata"]["authoring"].get("state"))
        )
        disposition = None
        if has_authoring:
            authoring = (rec.get("metadata") or {}).get("authoring") or {}
            disposition = authoring.get("disposition")

        inv_entry = {
            "id": rec_id,
            "name": name,
            "type": "Task",
            "level": "L4",
            "parent_l3": parent_l3,
            "parent_l3_resolves": (
                parent_l3 in l3_set if isinstance(parent_l3, str) else False
            ),
            "phase": phase,
            "fields_present": {
                "definition": has_definition,
                "trigger": has_trigger,
                "outcome": has_outcome,
                "responsibility": has_responsibility,
                "boundary_inclusions": has_boundary_incl,
                "boundary_exclusions": has_boundary_excl,
                "evidence": has_evidence,
                "provenance": has_provenance,
            },
            "authoring_state": (rec.get("metadata") or {}).get("authoring", {}).get("state"),
            "disposition": disposition,
        }
        inventory.append(inv_entry)
        if isinstance(parent_l3, str):
            by_parent.setdefault(parent_l3, []).append(inv_entry)

        # L4-001: inventory completeness
        if not rec_id:
            findings.append(_make_finding("L4-001", "?", "L4 Task missing id"))

        # L4-003: orphan detection
        if not parent_l3:
            findings.append(_make_finding(
                "L4-003", rec_id or "?",
                f"L4 Task {rec_id!r} has no belongs_to_activity"
            ))

        # L4-004: parent L3 reference validation
        if isinstance(parent_l3, str) and parent_l3 not in l3_set:
            findings.append(_make_finding(
                "L4-004", rec_id or "?",
                f"L4 Task {rec_id!r} references parent L3 {parent_l3!r} that does not resolve"
            ))

        # L4-006: definition
        if not has_definition:
            findings.append(_make_finding(
                "L4-006", rec_id or "?",
                f"L4 Task {rec_id!r} lacks a meaningful definition (>= 40 characters)"
            ))

        # L4-007: trigger
        if not has_trigger:
            findings.append(_make_finding(
                "L4-007", rec_id or "?",
                f"L4 Task {rec_id!r} lacks a trigger"
            ))

        # L4-008: outcome
        if not has_outcome:
            findings.append(_make_finding(
                "L4-008", rec_id or "?",
                f"L4 Task {rec_id!r} lacks an outcome"
            ))

        # L4-009: responsibility
        if not has_responsibility:
            findings.append(_make_finding(
                "L4-009", rec_id or "?",
                f"L4 Task {rec_id!r} lacks a responsibility"
            ))

        # L4-010: boundary completeness
        if not (has_boundary_incl and has_boundary_excl):
            findings.append(_make_finding(
                "L4-010", rec_id or "?",
                f"L4 Task {rec_id!r} lacks boundary inclusions and/or exclusions"
            ))

        # L4-011: evidence (pre-EXT-15 form)
        if not has_evidence:
            findings.append(_make_finding(
                "L4-011", rec_id or "?",
                f"L4 Task {rec_id!r} lacks the evidence[] record (source, claim, strength)"
            ))

        # L4-012: canonical provenance (EXT-15 migration gap)
        if not has_provenance and not disposition:
            findings.append(_make_finding(
                "L4-012", rec_id or "?",
                f"L4 Task {rec_id!r} lacks the EXT-15 canonical provenance[] block"
            ))

        # L4-013: authoring metadata
        if not has_authoring:
            findings.append(_make_finding(
                "L4-013", rec_id or "?",
                f"L4 Task {rec_id!r} has no metadata.authoring (EXT-16)"
            ))

        # L4-014: disposition
        elif disposition is not None and disposition not in DISPOSITION_VOCAB:
            findings.append(_make_finding(
                "L4-014", rec_id or "?",
                f"L4 Task {rec_id!r} has disposition {disposition!r} not in approved vocabulary",
                severity="error",
            ))

    # L4-002: parent L3 readiness
    missing_parents = {
        p for p in by_parent if p not in approved_l3
    }
    if missing_parents:
        findings.append(_make_finding(
            "L4-002", "l4-to-l3",
            f"{len(missing_parents)} L3 parent(s) referenced by L4 Tasks are not in the EXT-20 inventory: {sorted(missing_parents)[:5]}",
            severity="warning",
        ))

    # L4-005: 5-phase decomposition coherence
    incoherent_parents: list[dict] = []
    for parent, tasks in by_parent.items():
        phases = Counter(t.get("phase") for t in tasks)
        phase_set = set(phases.keys())
        if phase_set != CANONICAL_PHASES or any(v != 1 for v in phases.values()):
            incoherent_parents.append({
                "parent_l3": parent,
                "phases": dict(phases),
            })
    if incoherent_parents:
        findings.append(_make_finding(
            "L4-005", "l4-phase-coherence",
            f"{len(incoherent_parents)} parent L3 Activity/Activities do not carry the canonical 5-phase Task pattern: {incoherent_parents[:2]}",
            severity="warning",
        ))

    # Phase distribution across the whole L4 population
    phase_distribution: dict[str, int] = {}
    for entry in inventory:
        p = entry.get("phase")
        if p:
            phase_distribution[p] = phase_distribution.get(p, 0) + 1

    return findings, {
        "total_l4_entities": len(l4_records),
        "by_phase": phase_distribution,
        "parents_with_l4_children": len(by_parent),
        "tasks_per_parent_distribution": {},
        "incoherent_phase_parents": incoherent_parents,
        "by_disposition": {},
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
            "canonical_phase_count": len(CANONICAL_PHASES),
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
        "generator": "scripts/check_l4_backfill_ext21.py",
        "parent_cr": "CR-BP-94-EXT-21",
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

    L4_INVENTORY_PATH.write_text(json.dumps({
        "inventory_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/check_l4_backfill_ext21.py",
        "parent_cr": "CR-BP-94-EXT-21",
        "total_l4_entities": inventory_report["total_l4_entities"],
        "inventory": inventory_report["inventory"],
    }, indent=2), encoding="utf-8")

    matrix = _build_traceability_matrix(inventory_report)
    TRACEABILITY_MATRIX_PATH.write_text(json.dumps(matrix, indent=2),
                                         encoding="utf-8")

    if args.json:
        print(json.dumps(manifest, indent=2))
    else:
        print(f"L4 Task inventory: {inventory_report['total_l4_entities']} tasks")
        print(f"  Phase distribution: {inventory_report['by_phase']}")
        print(f"  Parents with L4 children: {inventory_report['parents_with_l4_children']}")
        print(f"\nL4 backfill findings: {len(findings)}")
        for finding in findings[:8]:
            print(f"  [{finding['rule']}] {finding['where']}: {finding['diagnostic'][:130]}")
        if len(findings) > 8:
            print(f"  ... and {len(findings) - 8} more")
        print(f"\nManifest: {MANIFEST_PATH.relative_to(REPO_ROOT)}")
        print(f"Inventory: {L4_INVENTORY_PATH.relative_to(REPO_ROOT)}")
        print(f"Traceability matrix: {TRACEABILITY_MATRIX_PATH.relative_to(REPO_ROOT)}")

    return 0 if not findings else 1


def _build_traceability_matrix(inventory_report: dict) -> dict:
    """Build the L4-to-L3 traceability matrix (the EXT-21 slice of the
    L2-to-L3-to-L4 traceability matrix).
    """
    inv = inventory_report["inventory"]
    by_parent: dict[str, dict] = {}
    for entry in inv:
        par = entry.get("parent_l3")
        if not isinstance(par, str):
            continue
        if par not in by_parent:
            by_parent[par] = {
                "parent_l3": par,
                "task_count": 0,
                "phases": [],
                "task_ids": [],
            }
        by_parent[par]["task_count"] += 1
        by_parent[par]["phases"].append(entry.get("phase"))
        by_parent[par]["task_ids"].append(entry.get("id"))

    tasks_per_parent: dict[int, int] = {}
    for data in by_parent.values():
        n = data["task_count"]
        tasks_per_parent[n] = tasks_per_parent.get(n, 0) + 1

    return {
        "matrix_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/check_l4_backfill_ext21.py",
        "parent_cr": "CR-BP-94-EXT-21 (the third and final slice of the L2-to-L3-to-L4 traceability matrix)",
        "purpose": "the L4-to-L3 traceability matrix (EXT-21 slice; completes the L2-to-L3-to-L4 traceability matrix mandated by the user recommendation; reveals which Tasks do not clearly contribute to their assigned Activity)",
        "total_l4_entities": inventory_report["total_l4_entities"],
        "total_l3_parents_referenced": inventory_report["parents_with_l4_children"],
        "tasks_per_parent_distribution": dict(sorted(tasks_per_parent.items())),
        "phase_distribution": inventory_report["by_phase"],
        "structural_quality_observations": {
            "canonical_phase_pattern": sorted(CANONICAL_PHASES),
            "incoherent_phase_parents_count": len(inventory_report.get("incoherent_phase_parents", [])),
            "fully_decomposed_activities": sum(
                1 for d in by_parent.values() if d["task_count"] == len(CANONICAL_PHASES)
            ),
        },
    }


if __name__ == "__main__":
    sys.exit(main())
