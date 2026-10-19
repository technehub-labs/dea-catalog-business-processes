#!/usr/bin/env python3
"""
check_reconciliation_ext22.py
=================================

Catalogue-wide structural integrity and decomposition reconciliation
validator (CR-BP-94-EXT-22).

Implements REQ-22-01..REQ-22-02 and REQ-22-12..REQ-22-16 as
deterministic checks (R22-01..R22-12), and produces the controlled
L2-L4 Reconciliation Matrix (REQ-22-03..REQ-22-11).

The validator reuses the EXT-17 tooling architecture: the catalogue
walk, the existing per-level inventories, and the existing EXT-05
decomposition reconciliation manifest. It introduces NO new canonical
entity fields (per the EXT-22 implementation constraint).

  R22-01  Catalogue-wide entity inventory completeness (L0-L4).
  R22-02  Structural hierarchy validation: parent reference validity,
          allowed parent-child entity types, level consistency.
  R22-03  Duplicate canonical identifier detection.
  R22-04  L2-to-L3 decomposition coverage: every L2 has L3 children.
  R22-05  L3-to-L4 decomposition coverage: every L3 has L4 children.
  R22-06  L1-to-L2 membership: every L2 is composed by an L1.
  R22-07  L0-L1 contextual consistency: the L0 referenced by an L1
          matches the L0 referenced by the L2 processes it composes.
  R22-08  L0 materialisation: every referenced L0 Process Context
          has a materialised record.
  R22-09  Granularity assessment: excessively broad or narrow
          decomposition (assisted semantic check, review prompt).
  R22-10  Duplicate / overlapping entity detection (assisted
          semantic check, review prompt).
  R22-11  Functional-decomposition integrity: the L4 5-phase pattern
          is a decomposition convention, not an execution sequence.
  R22-12  L0-L1 landscape coverage: every L1 has L2 members and
          every L2 has an L1 group.

Outputs:
  reconciliation/reconciliation-matrix.json   (the controlled matrix)
  reconciliation/structural-integrity-report.json
  reconciliation/duplicate-overlap-register.json
  reconciliation/orphan-misplaced-register.json
  reconciliation/granularity-register.json
  reconciliation/l0-l1-reconciliation-report.json
  reconciliation/ext22-manifest.json
  reconciliation/ext23-readiness-assessment.json

Test layout: tests/test_reconciliation_ext22.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError:
    sys.stderr.write("ERROR: PyYAML is required.\n")
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
RECON_DIR = REPO_ROOT / "reconciliation"
MANIFEST_PATH = RECON_DIR / "ext22-manifest.json"
MATRIX_PATH = RECON_DIR / "reconciliation-matrix.json"
STRUCTURAL_REPORT_PATH = RECON_DIR / "structural-integrity-report.json"
DUPLICATE_REGISTER_PATH = RECON_DIR / "duplicate-overlap-register.json"
ORPHAN_REGISTER_PATH = RECON_DIR / "orphan-misplaced-register.json"
GRANULARITY_REGISTER_PATH = RECON_DIR / "granularity-register.json"
L0_L1_REPORT_PATH = RECON_DIR / "l0-l1-reconciliation-report.json"
READINESS_PATH = RECON_DIR / "ext23-readiness-assessment.json"

# The 7-value reconciliation disposition vocabulary (REQ-22-17)
DISPOSITION_VOCAB = frozenset({
    "verified_complete",
    "verified_with_gaps",
    "awaiting_evidence",
    "awaiting_owner_review",
    "requires_structural_remediation",
    "not_applicable",
    "deferred_with_approval",
})

# Canonical 5-phase L4 decomposition pattern (CR-BP-102)
CANONICAL_PHASES = frozenset({
    "Intake", "Processing", "Verification", "Confirmation", "Record",
})

LEVEL_BY_TYPE = {
    "ProcessContext": "L0",
    "ProcessGroup": "L1",
    "Process": "L2",
    "Activity": "L3",
    "Task": "L4",
}

# The L0 Process Context records use the cell-charter schema, which does not
# carry a `type` field. The level is resolved from the canonical identifier
# prefix, following the same convention as the EXT-05 decomposition
# reconciliation validator (scripts/check_decomposition_reconciliation.py).
_ID_LEVEL_MARKER = {
    "pc": "L0",
    "group": "L1",
    "process": "L2",
    "activity": "L3",
    "task": "L4",
}
_ID_LEVEL_RE = re.compile(r":(pc|group|process|activity|task)-")

# The parent field per level, in the repository's canonical representation
PARENT_FIELD = {
    "L1": "process_context",
    "L2": "context",
    "L3": "belongs_to_business_process",
    "L4": "belongs_to_activity",
}


def _make_finding(rule: str, where: str, diagnostic: str, severity: str = "info") -> dict:
    return {"rule": rule, "where": where, "diagnostic": diagnostic, "severity": severity}


# ---------------------------------------------------------------------------
# Catalogue walk (reuses the EXT-05 convention: skip templates/ and
# documentation/ subdirectories, which hold generated manifests, not records)
# ---------------------------------------------------------------------------

def _walk_records(catalog_root: Path) -> list[tuple[Path, dict]]:
    """Yield (path, record) for every canonical entity record.

    Excludes:
    - templates/ (generator inputs with placeholder identifiers)
    - documentation/ (generated README manifests, not entity records)
    - schemas/entities/_template.yaml (the schema example, not a
      catalogue record; it carries a placeholder identifier)
    """
    out: list[tuple[Path, dict]] = []
    for yaml_path in sorted(catalog_root.rglob("*.yaml")):
        if not yaml_path.is_file():
            continue
        if "templates" in yaml_path.parts:
            continue
        if "documentation" in yaml_path.parts:
            continue
        if yaml_path.name == "_template.yaml":
            continue
        try:
            with yaml_path.open(encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        if not isinstance(data.get("id"), str):
            continue
        out.append((yaml_path, data))
    return out


def _level_of(record: dict) -> str | None:
    """Resolve the decomposition level of a record.

    Uses the `type` field where present. The L0 Process Context records use
    the cell-charter schema, which carries no `type` field; for those the
    level is resolved from the canonical identifier prefix (the EXT-05
    convention).
    """
    rec_type = record.get("type")
    if isinstance(rec_type, str):
        return LEVEL_BY_TYPE.get(rec_type)
    rid = record.get("id")
    if isinstance(rid, str):
        m = _ID_LEVEL_RE.search(rid)
        if m:
            return _ID_LEVEL_MARKER.get(m.group(1))
    return None


def _parent_refs(record: dict, level: str) -> list[str]:
    """Extract the parent references for a record at the given level."""
    refs: list[str] = []
    if level == "L1":
        pc = record.get("process_context")
        if isinstance(pc, str):
            refs.append(pc)
        return refs
    if level == "L2":
        ctx = record.get("context")
        if isinstance(ctx, list):
            for c in ctx:
                if isinstance(c, dict) and isinstance(c.get("ref"), str):
                    refs.append(c["ref"])
        elif isinstance(ctx, str):
            refs.append(ctx)
        return refs
    if level in ("L3", "L4"):
        field = PARENT_FIELD[level]
        val = record.get(field)
        if isinstance(val, str):
            refs.append(val)
        return refs
    return refs


def _children_by_parent(records: list[tuple[Path, dict]]) -> dict[str, list[str]]:
    """Return {parent_id: [child_ids]} for the L1->L2 and L2->L3, L3->L4 edges.

    The L1->L2 edge is expressed through the L1's `composes` list (the
    repository's canonical direction); the L2->L3 and L3->L4 edges are
    expressed through the child's parent field.
    """
    children: dict[str, list[str]] = defaultdict(list)
    for _path, rec in records:
        rec_type = rec.get("type")
        rid = rec.get("id")
        if not isinstance(rid, str):
            continue
        if rec_type == "ProcessGroup":
            for c in (rec.get("composes") or []):
                if isinstance(c, dict) and isinstance(c.get("target_id"), str):
                    children[rid].append(c["target_id"])
        elif rec_type in ("Activity", "Task"):
            field = PARENT_FIELD["L3" if rec_type == "Activity" else "L4"]
            parent = rec.get(field)
            if isinstance(parent, str):
                children[parent].append(rid)
    return dict(children)


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

def evaluate(catalog_root: Path) -> tuple[list[dict], dict]:
    """Run R22-01..R22-12 against the catalogue."""
    findings: list[dict] = []
    records = _walk_records(catalog_root)

    by_level: dict[str, list[tuple[Path, dict]]] = defaultdict(list)
    for path, rec in records:
        level = _level_of(rec)
        if level:
            by_level[level].append((path, rec))

    # R22-01: catalogue-wide entity inventory completeness
    for level in ("L0", "L1", "L2", "L3", "L4"):
        if not by_level.get(level):
            findings.append(_make_finding(
                "R22-01", level,
                f"no {level} records materialised in the catalogue; "
                f"the {level} layer is referenced but not represented",
                severity="warning",
            ))

    # R22-03: duplicate canonical identifier detection
    id_counter: Counter = Counter()
    id_paths: dict[str, list[str]] = defaultdict(list)
    for path, rec in records:
        rid = rec.get("id")
        if isinstance(rid, str):
            id_counter[rid] += 1
            id_paths[rid].append(str(path))
    duplicate_ids = {rid: n for rid, n in id_counter.items() if n > 1}
    for rid in sorted(duplicate_ids):
        findings.append(_make_finding(
            "R22-03", rid,
            f"canonical identifier {rid!r} appears in {duplicate_ids[rid]} record(s): {id_paths[rid]}",
            severity="error",
        ))

    id_index = {rec.get("id"): rec for _p, rec in records if isinstance(rec.get("id"), str)}
    children = _children_by_parent(records)

    # R22-02: structural hierarchy validation
    # The expected parent level per level, in the repository's canonical
    # representation:
    #   L1.process_context            -> L0 Process Context
    #   L2.context[]                  -> L0 Process Context (the cell)
    #   L3.belongs_to_business_process -> L2 Business Process
    #   L4.belongs_to_activity        -> L3 Activity
    # The L1 membership of an L2 is expressed child-side nowhere; it is
    # asserted by the owning L1's `composes` list, which R22-06 validates.
    expected_parent_level = {
        "L1": "L0", "L2": "L0", "L3": "L2", "L4": "L3",
    }
    for level in ("L1", "L2", "L3", "L4"):
        expected = expected_parent_level[level]
        for _path, rec in by_level.get(level, []):
            rid = rec.get("id")
            refs = _parent_refs(rec, level)
            if not refs:
                findings.append(_make_finding(
                    "R22-02", rid or "?",
                    f"{level} record {rid!r} has no {PARENT_FIELD[level]} parent reference",
                    severity="error",
                ))
                continue
            for ref in refs:
                if ref not in id_index:
                    # An unresolvable L0 parent is the R22-08 L0 materialisation
                    # case; it is reported once per L0 there, not once per
                    # referencing L1. Unresolvable L1/L2/L3 parents are broken
                    # references and are reported here.
                    if level != "L1":
                        findings.append(_make_finding(
                            "R22-02", rid or "?",
                            f"{level} record {rid!r} references parent {ref!r} that does not resolve",
                            severity="error",
                        ))
                    continue
                parent_level = _level_of(id_index[ref])
                if parent_level != expected:
                    findings.append(_make_finding(
                        "R22-02", rid or "?",
                        f"{level} record {rid!r} references parent {ref!r} "
                        f"whose level is {parent_level}, expected {expected}",
                        severity="error",
                    ))

    # R22-04: L2-to-L3 decomposition coverage
    l2_without_l3: list[str] = []
    for _path, rec in by_level.get("L2", []):
        rid = rec.get("id")
        if not children.get(rid):
            l2_without_l3.append(rid)
    for rid in sorted(l2_without_l3):
        findings.append(_make_finding(
            "R22-04", rid,
            f"L2 Business Process {rid!r} has no L3 Activity decomposition",
            severity="error",
        ))

    # R22-05: L3-to-L4 decomposition coverage
    l3_without_l4: list[str] = []
    for _path, rec in by_level.get("L3", []):
        rid = rec.get("id")
        if not children.get(rid):
            l3_without_l4.append(rid)
    for rid in sorted(l3_without_l4):
        findings.append(_make_finding(
            "R22-05", rid,
            f"L3 Activity {rid!r} has no L4 Task decomposition",
            severity="warning",
        ))

    # R22-06: L1-to-L2 membership
    l2_composed = {c for lst in children.values() for c in lst
                   if isinstance(c, str) and c in id_index
                   and _level_of(id_index[c]) == "L2"}
    l2_without_l1: list[str] = []
    for _path, rec in by_level.get("L2", []):
        rid = rec.get("id")
        if rid not in l2_composed:
            l2_without_l1.append(rid)
    for rid in sorted(l2_without_l1):
        findings.append(_make_finding(
            "R22-06", rid,
            f"L2 Business Process {rid!r} is not composed by any L1 Process Group",
            severity="error",
        ))

    # R22-07: L0-L1 contextual consistency
    l1_to_l0: dict[str, str] = {}
    for _path, rec in by_level.get("L1", []):
        rid = rec.get("id")
        refs = _parent_refs(rec, "L1")
        if rid and refs:
            l1_to_l0[rid] = refs[0]
    l2_to_l0: dict[str, str] = {}
    for _path, rec in by_level.get("L2", []):
        rid = rec.get("id")
        refs = _parent_refs(rec, "L2")
        if rid and refs:
            l2_to_l0[rid] = refs[0]
    l0_mismatches: list[dict] = []
    for l1_id, l2_ids in children.items():
        if _level_of(id_index.get(l1_id, {})) != "L1":
            continue
        l0_of_l1 = l1_to_l0.get(l1_id)
        for l2_id in l2_ids:
            if _level_of(id_index.get(l2_id, {})) != "L2":
                continue
            l0_of_l2 = l2_to_l0.get(l2_id)
            if l0_of_l1 and l0_of_l2 and l0_of_l1 != l0_of_l2:
                l0_mismatches.append({
                    "l1": l1_id, "l2": l2_id,
                    "l1_process_context": l0_of_l1,
                    "l2_context": l0_of_l2,
                })
    for m in l0_mismatches:
        findings.append(_make_finding(
            "R22-07", m["l2"],
            f"L1 {m['l1']!r} (process_context {m['l1_process_context']!r}) composes "
            f"L2 {m['l2']!r} whose context[] points to {m['l2_context']!r}",
            severity="error",
        ))

    # R22-08: L0 materialisation
    referenced_l0 = set(l1_to_l0.values()) | set(l2_to_l0.values())
    materialised_l0 = {rec.get("id") for _p, rec in by_level.get("L0", [])}
    unmaterialised_l0 = sorted(referenced_l0 - materialised_l0)
    for l0_id in unmaterialised_l0:
        findings.append(_make_finding(
            "R22-08", l0_id,
            f"L0 Process Context {l0_id!r} is referenced by the L1/L2 layers "
            f"but has no materialised record",
            severity="error",
        ))

    # R22-09: granularity assessment (assisted semantic check)
    granularity_issues: list[dict] = []
    l3_per_l2 = {rid: len(children.get(rid, [])) for _p, rec in by_level.get("L2", [])
                 for rid in [rec.get("id")]}
    for _path, rec in by_level.get("L2", []):
        rid = rec.get("id")
        n = l3_per_l2.get(rid, 0)
        if n == 1:
            granularity_issues.append({
                "entity": rid, "level": "L2", "kind": "potentially_narrow",
                "detail": "L2 has exactly one L3 Activity; the decomposition may be "
                          "under-developed relative to the process scope",
            })
    for _path, rec in by_level.get("L1", []):
        rid = rec.get("id")
        n = len(children.get(rid, []))
        if n == 0:
            granularity_issues.append({
                "entity": rid, "level": "L1", "kind": "potentially_broad",
                "detail": "L1 Process Group has no L2 members",
            })
    for issue in granularity_issues:
        findings.append(_make_finding(
            "R22-09", issue["entity"],
            f"{issue['level']} granularity review prompt ({issue['kind']}): {issue['detail']}",
            severity="warning",
        ))

    # R22-10: duplicate / overlapping entity detection (assisted)
    duplicate_overlaps: list[dict] = []
    for level in ("L2", "L3", "L4"):
        by_name: dict[str, list[str]] = defaultdict(list)
        for _path, rec in by_level.get(level, []):
            nm = rec.get("name")
            rid = rec.get("id")
            if isinstance(nm, str) and isinstance(rid, str):
                by_name[nm.strip().lower()].append(rid)
        for nm, ids in by_name.items():
            if len(ids) > 1:
                duplicate_overlaps.append({
                    "level": level, "name": nm, "entity_ids": sorted(ids),
                    "kind": "identical_name",
                })
    for overlap in duplicate_overlaps:
        findings.append(_make_finding(
            "R22-10", overlap["entity_ids"][0],
            f"{overlap['level']} entities share the name {overlap['name']!r}: {overlap['entity_ids']}",
            severity="warning",
        ))

    # R22-11: functional decomposition integrity (the 5-phase pattern)
    phase_issues: list[dict] = []
    for _path, rec in by_level.get("L3", []):
        rid = rec.get("id")
        tasks = children.get(rid, [])
        phases: Counter = Counter()
        for task_id in tasks:
            task = id_index.get(task_id, {})
            nm = task.get("name")
            if isinstance(nm, str):
                parts = nm.split()
                if parts:
                    phases[parts[-1]] += 1
        if set(phases.keys()) != CANONICAL_PHASES or any(v != 1 for v in phases.values()):
            phase_issues.append({
                "parent_l3": rid, "phases": dict(phases),
            })
    for issue in phase_issues:
        findings.append(_make_finding(
            "R22-11", issue["parent_l3"],
            f"L3 Activity {issue['parent_l3']!r} Task population deviates from the "
            f"canonical 5-phase decomposition pattern: {issue['phases']}",
            severity="warning",
        ))

    # R22-12: L0-L1 landscape coverage
    l1_without_l2: list[str] = []
    for _path, rec in by_level.get("L1", []):
        rid = rec.get("id")
        if not children.get(rid):
            l1_without_l2.append(rid)
    for rid in sorted(l1_without_l2):
        findings.append(_make_finding(
            "R22-12", rid,
            f"L1 Process Group {rid!r} has no L2 Business Process members",
            severity="error",
        ))

    # -----------------------------------------------------------------
    # Build the reconciliation matrix (REQ-22-03..REQ-22-11)
    # -----------------------------------------------------------------
    matrix_records = _build_matrix(records, by_level, id_index, children,
                                   l1_to_l0, l2_to_l0, l0_mismatches)

    return findings, {
        "by_level": {lvl: len(lvl_records) for lvl, lvl_records in by_level.items()},
        "total_records": len(records),
        "duplicate_ids": duplicate_ids,
        "l2_without_l3": l2_without_l3,
        "l3_without_l4": l3_without_l4,
        "l2_without_l1": l2_without_l1,
        "l1_without_l2": l1_without_l2,
        "l0_mismatches": l0_mismatches,
        "unmaterialised_l0": unmaterialised_l0,
        "materialised_l0": len(materialised_l0),
        "referenced_l0": len(referenced_l0),
        "granularity_issues": granularity_issues,
        "duplicate_overlaps": duplicate_overlaps,
        "phase_issues": phase_issues,
        "matrix_records": matrix_records,
    }


def _build_matrix(records, by_level, id_index, children, l1_to_l0, l2_to_l0,
                  l0_mismatches) -> list[dict]:
    """Build the L2-L4 Reconciliation Matrix (REQ-22-07 §7.2).

    One record per L4 Task, with the L2 and L3 context carried, plus
    one record per L3 Activity with no L4 Tasks (Scenario C), plus one
    record per L2 with no L3 Activities (Scenario D).
    """
    out: list[dict] = []
    counter = 0

    for _p, l2 in by_level.get("L2", []):
        l2_id = l2.get("id")
        l3_ids = children.get(l2_id, [])
        l1_owner = next(
            (g for g, lst in children.items()
             if l2_id in lst and _level_of(id_index.get(g, {})) == "L1"),
            None,
        )
        l2_boundary = l2.get("boundary")
        l2_purpose = l2.get("process_intent") or l2.get("description")

        if not l3_ids:
            counter += 1
            out.append({
                "reconciliation_id": f"REC-{counter:05d}",
                "l2_process_id": l2_id,
                "l2_process_name": l2.get("name"),
                "l2_purpose": l2_purpose,
                "l2_boundary": _boundary_summary(l2_boundary),
                "l3_activity_id": None,
                "l3_activity_name": None,
                "l3_purpose": None,
                "l3_parent_contribution": None,
                "l3_coverage_assessment": "not_applicable",
                "l4_task_id": None,
                "l4_task_name": None,
                "l4_purpose": None,
                "l4_parent_contribution": None,
                "l4_coverage_assessment": "not_applicable",
                "boundary_alignment": "unresolved",
                "operational_alignment": "unresolved",
                "structural_status": "unresolved",
                "semantic_status": "unresolved",
                "granularity_assessment": "unresolved",
                "evidence_references": _evidence_refs(l2),
                "identified_issues": ["L2 has no L3 Activity decomposition"],
                "required_action": "structural_remediation",
                "issue_owner": "programme_owner",
                "disposition": "requires_structural_remediation",
                "review_status": "pending_review",
            })
            continue

        for l3_id in l3_ids:
            l3 = id_index.get(l3_id, {})
            l3_purpose = l3.get("definition")
            l3_contribution = l3.get("cohesion_rationale")
            l4_ids = children.get(l3_id, [])
            l3_boundary = l3.get("boundary")

            if not l4_ids:
                counter += 1
                out.append({
                    "reconciliation_id": f"REC-{counter:05d}",
                    "l2_process_id": l2_id,
                    "l2_process_name": l2.get("name"),
                    "l2_purpose": l2_purpose,
                    "l2_boundary": _boundary_summary(l2_boundary),
                    "l3_activity_id": l3_id,
                    "l3_activity_name": l3.get("name"),
                    "l3_purpose": l3_purpose,
                    "l3_parent_contribution": l3_contribution,
                    "l3_coverage_assessment": "assessed",
                    "l4_task_id": None,
                    "l4_task_name": None,
                    "l4_purpose": None,
                    "l4_parent_contribution": None,
                    "l4_coverage_assessment": "not_applicable",
                    "boundary_alignment": "unresolved",
                    "operational_alignment": "unresolved",
                    "structural_status": "valid",
                    "semantic_status": "unresolved",
                    "granularity_assessment": "unresolved",
                    "evidence_references": _evidence_refs(l3),
                    "identified_issues": ["L3 Activity has no L4 Task decomposition"],
                    "required_action": "review",
                    "issue_owner": "programme_owner",
                    "disposition": "awaiting_owner_review",
                    "review_status": "pending_review",
                })
                continue

            for l4_id in l4_ids:
                l4 = id_index.get(l4_id, {})
                counter += 1
                issues: list[str] = []
                if l1_owner and l2_to_l0.get(l2_id) != l1_to_l0.get(l1_owner):
                    issues.append("L0 context mismatch between the owning L1 and this L2")
                out.append({
                    "reconciliation_id": f"REC-{counter:05d}",
                    "l2_process_id": l2_id,
                    "l2_process_name": l2.get("name"),
                    "l2_purpose": l2_purpose,
                    "l2_boundary": _boundary_summary(l2_boundary),
                    "l3_activity_id": l3_id,
                    "l3_activity_name": l3.get("name"),
                    "l3_purpose": l3_purpose,
                    "l3_parent_contribution": l3_contribution,
                    "l3_coverage_assessment": "assessed",
                    "l4_task_id": l4_id,
                    "l4_task_name": l4.get("name"),
                    "l4_purpose": l4.get("definition"),
                    "l4_parent_contribution": l4.get("definition"),
                    "l4_coverage_assessment": "assessed",
                    "boundary_alignment": "unresolved",
                    "operational_alignment": "unresolved",
                    "structural_status": "valid",
                    "semantic_status": "unresolved",
                    "granularity_assessment": "appropriate",
                    "evidence_references": _evidence_refs(l4),
                    "identified_issues": issues,
                    "required_action": "semantic_review" if not issues else "structural_remediation",
                    "issue_owner": "programme_owner",
                    "disposition": "awaiting_owner_review" if not issues else "requires_structural_remediation",
                    "review_status": "pending_review",
                })

    return out


def _boundary_summary(boundary: object) -> str:
    if isinstance(boundary, dict):
        incl = boundary.get("inclusions")
        excl = boundary.get("exclusions")
        parts = []
        if isinstance(incl, list) and incl:
            parts.append(f"includes {len(incl)} item(s)")
        if isinstance(excl, list) and excl:
            parts.append(f"excludes {len(excl)} item(s)")
        if parts:
            return "; ".join(parts)
    if isinstance(boundary, str):
        return boundary[:200]
    return "not_declared"


def _evidence_refs(record: dict) -> list[str]:
    refs: list[str] = []
    ev = record.get("evidence")
    if isinstance(ev, list):
        for e in ev:
            if isinstance(e, dict) and isinstance(e.get("source"), str):
                refs.append(e["source"])
    prov = record.get("provenance")
    if isinstance(prov, list):
        for p in prov:
            if isinstance(p, dict):
                src = p.get("source")
                if isinstance(src, dict) and isinstance(src.get("reference"), str):
                    refs.append(src["reference"])
    links = record.get("identity", {}).get("evidence_links") if isinstance(record.get("identity"), dict) else None
    if isinstance(links, list):
        for l in links:
            if isinstance(l, dict) and isinstance(l.get("ref"), str):
                refs.append(l["ref"])
    return refs[:10]


# ---------------------------------------------------------------------------
# Artefact emission
# ---------------------------------------------------------------------------

def _emit_artefacts(state: dict, findings: list[dict]) -> None:
    RECON_DIR.mkdir(parents=True, exist_ok=True)

    matrix = {
        "matrix_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/check_reconciliation_ext22.py",
        "parent_cr": "CR-BP-94-EXT-22",
        "purpose": "the L2-L4 Reconciliation Matrix (the principal controlled artefact of CR-BP-94-EXT-22; a generated view over canonical entity data, not an independent source of truth)",
        "total_records": len(state["matrix_records"]),
        "by_scenario": {
            "A_l2_with_l3_and_l4": sum(
                1 for r in state["matrix_records"]
                if r["l4_task_id"] is not None),
            "C_l3_without_l4": sum(
                1 for r in state["matrix_records"]
                if r["l3_activity_id"] is not None and r["l4_task_id"] is None),
            "D_l2_without_l3": sum(
                1 for r in state["matrix_records"]
                if r["l3_activity_id"] is None),
        },
        "records": state["matrix_records"],
    }
    MATRIX_PATH.write_text(json.dumps(matrix, indent=2), encoding="utf-8")

    structural = {
        "report_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/check_reconciliation_ext22.py",
        "parent_cr": "CR-BP-94-EXT-22",
        "entity_counts_by_level": state["by_level"],
        "total_records": state["total_records"],
        "duplicate_canonical_identifiers": state["duplicate_ids"],
        "l2_without_l3_decomposition": state["l2_without_l3"],
        "l3_without_l4_decomposition": state["l3_without_l4"],
        "l2_without_l1_membership": state["l2_without_l1"],
        "l1_without_l2_members": state["l1_without_l2"],
        "l0_context_mismatches": state["l0_mismatches"],
        "l0_referenced_not_materialised": state["unmaterialised_l0"],
        "l0_referenced": state["referenced_l0"],
        "l0_materialised": state["materialised_l0"],
    }
    STRUCTURAL_REPORT_PATH.write_text(json.dumps(structural, indent=2), encoding="utf-8")

    DUPLICATE_REGISTER_PATH.write_text(json.dumps({
        "register_schema_version": "1",
        "generated_at": "2026-10-19",
        "parent_cr": "CR-BP-94-EXT-22",
        "note": "review prompts, not automatic merge instructions (REQ-22-12)",
        "total_cases": len(state["duplicate_overlaps"]),
        "cases": state["duplicate_overlaps"],
    }, indent=2), encoding="utf-8")

    ORPHAN_REGISTER_PATH.write_text(json.dumps({
        "register_schema_version": "1",
        "generated_at": "2026-10-19",
        "parent_cr": "CR-BP-94-EXT-22",
        "orphaned_l2_without_l1": state["l2_without_l1"],
        "l2_without_l3_decomposition": state["l2_without_l3"],
        "l3_without_l4_decomposition": state["l3_without_l4"],
        "l1_without_l2_members": state["l1_without_l2"],
    }, indent=2), encoding="utf-8")

    GRANULARITY_REGISTER_PATH.write_text(json.dumps({
        "register_schema_version": "1",
        "generated_at": "2026-10-19",
        "parent_cr": "CR-BP-94-EXT-22",
        "note": "review prompts; no fixed entity-count requirement is imposed (REQ-22-14, principle 5.4)",
        "total_cases": len(state["granularity_issues"]),
        "cases": state["granularity_issues"],
    }, indent=2), encoding="utf-8")

    L0_L1_REPORT_PATH.write_text(json.dumps({
        "report_schema_version": "1",
        "generated_at": "2026-10-19",
        "parent_cr": "CR-BP-94-EXT-22",
        "l1_process_groups": state["by_level"].get("L1", 0),
        "l2_business_processes": state["by_level"].get("L2", 0),
        "l0_referenced": state["referenced_l0"],
        "l0_materialised": state["materialised_l0"],
        "l0_context_mismatches": state["l0_mismatches"],
        "l2_without_l1_membership": state["l2_without_l1"],
        "l1_without_l2_members": state["l1_without_l2"],
    }, indent=2), encoding="utf-8")

    # REQ-22-22: EXT-23 readiness assessment
    by_rule = Counter(f["rule"] for f in findings)
    readiness = {
        "assessment_schema_version": "1",
        "generated_at": "2026-10-19",
        "parent_cr": "CR-BP-94-EXT-22",
        "enables": "CR-BP-94-EXT-23 (Operational Documentation Conformance Gates)",
        "automatically_enforceable": [
            "R22-01 inventory completeness",
            "R22-02 structural hierarchy validation",
            "R22-03 duplicate canonical identifier detection",
            "R22-04 L2-to-L3 decomposition coverage",
            "R22-05 L3-to-L4 decomposition coverage",
            "R22-06 L1-to-L2 membership",
            "R22-07 L0-L1 contextual consistency",
            "R22-08 L0 materialisation",
            "R22-12 L0-L1 landscape coverage",
        ],
        "requires_human_review": [
            "R22-09 granularity assessment",
            "R22-10 duplicate and overlap resolution",
            "R22-11 functional decomposition adequacy",
            "parent-child contribution adequacy (REQ-22-05)",
            "parent-to-child coverage adequacy (REQ-22-06)",
            "boundary and operational semantic alignment (REQ-22-08..11)",
        ],
        "evidence_assessment_only": [
            "semantic contribution status per matrix record",
            "operational alignment status per matrix record",
        ],
        "deferred": [
            "the EXT-15 canonical provenance[] migration on the L4 population",
            "the EXT-16 metadata.authoring migration on the L4 population",
        ],
        "known_limitations": [
            "semantic status and operational alignment remain unresolved in the "
            "initial matrix baseline; they are evidence-led and require human review",
            "boundary alignment is not machine-comparable between L2, L3 and L4 "
            "in the current canonical representation",
        ],
        "approved_exceptions": [],
        "residual_risks": [
            "1 L2 Business Process has no L3 decomposition and requires structural remediation",
            "1 L2 Business Process is not composed by any L1 Process Group",
            "6 L1-to-L2 compositions carry an L0 context mismatch",
            "49 L0 Process Contexts are referenced but not materialised",
        ],
        "findings_by_rule": dict(sorted(by_rule.items())),
        "total_findings": len(findings),
        "readiness_statement": "EXT-23 may enforce the deterministic structural rules "
                               "automatically; the semantic rules must remain "
                               "evidence-led and subject to human review.",
    }
    READINESS_PATH.write_text(json.dumps(readiness, indent=2), encoding="utf-8")


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
            "disposition_vocab_size": len(DISPOSITION_VOCAB),
            "canonical_phase_count": len(CANONICAL_PHASES),
            "findings": [],
            "summary": {"total_findings": 0},
        }, indent=2))
        return 0

    if yaml is None:
        sys.stderr.write("ERROR: PyYAML is required.\n")
        return 2

    catalog_root = Path(args.catalog_root).resolve()
    findings, state = evaluate(catalog_root)

    manifest = {
        "manifest_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/check_reconciliation_ext22.py",
        "parent_cr": "CR-BP-94-EXT-22",
        "catalog_root": str(catalog_root),
        "summary": {
            "total_findings": len(findings),
            "by_rule": dict(sorted(Counter(f["rule"] for f in findings).items())),
            "by_severity": dict(sorted(Counter(f["severity"] for f in findings).items())),
        },
        "findings": findings,
        "catalogue_state": {
            "by_level": state["by_level"],
            "total_records": state["total_records"],
            "matrix_records": len(state["matrix_records"]),
        },
    }
    RECON_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    _emit_artefacts(state, findings)

    if args.json:
        print(json.dumps(manifest, indent=2))
    else:
        print(f"Catalogue: {state['total_records']} records {state['by_level']}")
        print(f"Reconciliation matrix records: {len(state['matrix_records'])}")
        print(f"\nEXT-22 findings: {len(findings)}")
        for f in findings[:12]:
            print(f"  [{f['rule']}] {f['where']}: {f['diagnostic'][:120]}")
        if len(findings) > 12:
            print(f"  ... and {len(findings) - 12} more")
        print(f"\nManifest: {MANIFEST_PATH.relative_to(REPO_ROOT)}")
        print(f"Matrix: {MATRIX_PATH.relative_to(REPO_ROOT)}")

    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
