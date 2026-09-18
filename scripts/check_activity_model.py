#!/usr/bin/env python3
"""
check_activity_model.py
========================

Activity Model validator (CR-BP-32 ACT-001..010 + CR-BP-97 ACT-011..015).

Codifies the Activity Model rules from CR-BP-32 §15 as machine-testable
per-record invariants. The CR-BP-97 extensions (ACT-011..015) are five
structure checks for OPTIONAL fields on the Activity record (per CR-BP-92 §12):

  ACT-011  Cohesive work statement adequacy (extends ACT-003).
           When the Activity is non-deprecated, the `definition` field
           must be a substantive prose statement (>= 120 chars). Back-compat:
           ACT-003 already requires `cohesion_rationale`; ACT-011 strengthens
           the `definition` minimum.

  ACT-012  Inputs/Outputs integrity (advisory; OPTIONAL field).
           When `inputs[]` or `outputs[]` is present, structure is enforced
           (id/name/description/source per CR-BP-92 §4 universal contract).

  ACT-013  Outcome contribution (advisory; OPTIONAL field).
           When `outcome_contribution:` is present, must be a non-empty string.

  ACT-014  Boundary and exclusions (advisory; OPTIONAL field).
           When `boundary:` is present, must be a non-empty string or
           non-empty object with inclusions/exclusions.

  ACT-015  Sibling distinction (advisory; cross-record check).
           When two Activities share the same parent Business Process and
           the same `name`, emit a finding. The check is scoped to records
           whose names are non-empty and matching exactly.

Back-compat rule (per CR-BP-95): the underlying OPTIONAL fields are absent
on all existing Activity records; advisory checks pass vacuously when the
field is absent. Backfill across the existing record population is the
work of a separate reconciliation slice (CR-BP-99 or a dedicated L3
enrichment tranche), not CR-BP-97.

ACT-016..020 from the recon programme are covered by the existing
ACT-004 (Task decomposition integrity) and ACT-010 (Activity traceability)
checks; CR-BP-97 reconciles the prose rather than introducing net-new
rules for these.

Today the catalog has zero Activity records; the validator is therefore
a regression guard that emits no findings on the existing canonical
Business Process records (none of which are Activity-typed) and prepares
the catalog for the first Activity contributions.

The validator only inspects records whose `type` discriminator is
`Activity` (or records that opt into Activity decomposition by declaring
the `composes` shape defined in §14). The canonical Business Process
records (`type: Process`) are NEVER inspected and produce zero findings
by construction (CR-BP-32 §17 "Result (post-landing)": existing BPs
without Activity decomposition are valid and remain at L4 conformance).

Rules (derived from CR-BP-32 §15 + CR-BP-97 §12):

  ACT-001 — Every Activity belongs to a Business Process.
            type=Activity ⇒ belongs_to_business_process (top-level or
            metadata.belongs_to_business_process) is set AND resolves to
            a known `dea:process-*` id (best-effort: presence + pattern;
            full resolution to a BP record is enforced when at least
            one Activity exists in the catalog).

  ACT-002 — An Activity shall not be represented as a Business Process.
            type=Activity ⇒ type != "Process" (i.e., single-typed).

  ACT-003 — Every Activity declares a cohesion rationale.
            type=Activity ⇒ cohesion_rationale (top-level or
            metadata.cohesion_rationale) is a non-empty string ≥ 20
            characters (long enough to be a rationale, not a label).

  ACT-004 — An Activity declares at least one composed Task
            (decomposition reaches L4) OR explicitly marks the
            boundary rationale.
            type=Activity ⇒ either composes[] has ≥1 entry pointing
            at a `dea:task-*` id, OR `decomposition_boundary: l4-reached`
            is asserted (acknowledges the case where decomposition
            ends at the Activity itself per CR-BP-32 §12).

  ACT-005 — Activity composition uses dea:composes.
            For every composes[] entry, relationship_type must be
            `dea:composes`. Forbidden alternatives are recorded in
            CR-BP-32 §7: parent_activity, child_activities, decomposes,
            contains_activity. The validator rejects those.

  ACT-006 — Activity decomposition does not imply execution sequence.
            type=Activity ⇒ MUST NOT carry execution-ordering fields
            (execution_order, temporal_sequence, start_time, end_time,
            duration, sequence_index, step_index). Composition is
            structural only (CR-BP-32 §7).

  ACT-007 — Activity is not a synonym for Business Function.
            type=Activity ⇒ id MUST NOT match `dea:function-*` (the
            Business Function ID family; CR-BP-04 §4 reserves that
            family for Business Functions, not Activities).

  ACT-008 — Activity does not represent implementation detail.
            type=Activity ⇒ MUST NOT carry implementation-detail
            marker fields (script_ref, api_call_ref, system_operation,
            procedure_ref, work_instruction_ref, technical_step_ref).
            CR-BP-32 §12 establishes L4 as the catalog decomposition
            boundary; anything below L4 is implementation detail
            outside the catalog.

  ACT-009 — Activity does not introduce an independent execution model.
            type=Activity ⇒ MUST NOT carry workflow-modeling fields
            (workflow, bpmn, execution_model, workflow_definition,
            bpmn_process). CR-BP-32 §11 reserves execution semantics
            for CR-BP-33.

  ACT-010 — Activity traceability to parent Business Process.
            type=Activity ⇒ `belongs_to_business_process` is recorded
            in the parent BP's `metadata.activity_references` list (or
            the BP record declares `composes[]` entries whose
            target_id matches the Activity id). Bidirectional
            traceability is enforced whenever BOTH records exist
            in the catalog; for a solo Activity (parent BP absent
            or the catalog has no BPs at all) the rule degrades to
            "forward reference present".

Coverage on the live catalog (2026-09-12): zero Activity records.
Expected findings: ACT-001..010 = 0 across all 131 BP records (the
validator never touches BP records). The validator is therefore a
forward-looking regression guard, not a corrective gate.

Exit codes:
  0  all Activity records (if any) satisfy all ten rules
  1  at least one Activity record fails at least one rule
  2  self-test failure or I/O error

Usage:
  python3 scripts/check_activity_model.py
  python3 scripts/check_activity_model.py --strict
  python3 scripts/check_activity_model.py --json
  python3 scripts/check_activity_model.py --self-test

Author: Coder (for eaojnr). Established by CR-BP-32 (2026-09-12).
Derived from CR-BP-32 §15 (Activity Conformance Rules) and
CR-BP-32 §7, §11, §12, §14 (composition / execution / boundary /
repository changes). See change-requests/CR-BP-32-activity-model.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Callable

import yaml

# ID families (CR-BP-04 §4 + CR-BP-32 §14).
# Activity ids use the `dea:activity-*` family (mirrors the
# `dea:process-*` / `dea:group-*` / `dea:pc-*` / `dea:scope-*` families).
BP_ID_PATTERN = re.compile(r"^dea:process-[a-z0-9-]+$")
ACTIVITY_ID_PATTERN = re.compile(r"^dea:activity-[a-z0-9-]+$")
FUNCTION_ID_PATTERN = re.compile(r"^dea:function-[a-z0-9-]+$")
TASK_ID_PATTERN = re.compile(r"^dea:task-[a-z0-9-]+$")

# CR-BP-32 §7 forbids these relationship_type values for composition.
# The canonical name is `dea:composes` (same as PG-005 / BP-ARC conventions).
FORBIDDEN_COMPOSITION_TYPES = frozenset({
    "parent_activity",
    "child_activities",
    "decomposes",
    "contains_activity",
})
CANONICAL_COMPOSITION_TYPE = "dea:composes"

# CR-BP-32 §6 / §15 field naming for cohesion rationale.
MIN_COHESION_RATIONALE_LEN = 20  # chars; rejects labels, accepts rationales

# CR-BP-32 §6 forbidden field names for execution ordering on Activity
# (composition is structural only).
FORBIDDEN_EXECUTION_FIELDS = frozenset({
    "execution_order",
    "temporal_sequence",
    "start_time",
    "end_time",
    "duration",
    "sequence_index",
    "step_index",
})

# CR-BP-32 §12 forbids these field names because they imply
# implementation detail below L4.
FORBIDDEN_IMPLEMENTATION_FIELDS = frozenset({
    "script_ref",
    "api_call_ref",
    "system_operation",
    "procedure_ref",
    "work_instruction_ref",
    "technical_step_ref",
})

# CR-BP-32 §11 forbids these field names because Activity does NOT
# introduce execution semantics (CR-BP-33 owns those).
FORBIDDEN_EXECUTION_MODEL_FIELDS = frozenset({
    "workflow",
    "bpmn",
    "execution_model",
    "workflow_definition",
    "bpmn_process",
})

# Discriminator value (mirrors `type: ProcessGroup`, `type: Process`,
# `type: ProcessContext` on the existing record types).
ACTIVITY_TYPE = "Activity"


# -----------------------------------------------------------------------------
# Discovery
# -----------------------------------------------------------------------------


def _load_records(catalog_root: Path) -> list[tuple[Path, dict]]:
    """Load every Activity record (with path).

    Walks `entities/v1-alpha/dea:activity-*/<id>.yaml`. Skips dirs
    without the expected YAML file. Also picks up any record whose
    `type: Activity` discriminator is set even if its id does not
    match the family (defensive — the regenerator may admit Activity
    records before the id family is enforced).

    Returns (path, record) pairs.
    """
    base = catalog_root / "entities" / "v1-alpha"
    pairs: list[tuple[Path, dict]] = []
    if not base.exists():
        return pairs
    for entry in sorted(base.iterdir()):
        if not entry.is_dir():
            continue
        # Conventional Activity dir (id family)
        yaml_path = entry / f"{entry.name}.yaml"
        if yaml_path.exists():
            try:
                data = yaml.safe_load(yaml_path.read_text())
            except yaml.YAMLError as exc:
                print(f"WARN: {yaml_path}: YAML parse error: {exc}",
                      file=sys.stderr)
                continue
            if isinstance(data, dict):
                pairs.append((yaml_path, data))
                continue
        # Defensive: any record file under v1-alpha that declares
        # type: Activity. Useful for contributors testing the
        # schema before the id-family is enforced.
        for yf in sorted(entry.glob("*.yaml")):
            try:
                data = yaml.safe_load(yf.read_text())
            except yaml.YAMLError as exc:
                print(f"WARN: {yf}: YAML parse error: {exc}",
                      file=sys.stderr)
                continue
            if isinstance(data, dict) and data.get("type") == ACTIVITY_TYPE:
                pairs.append((yf, data))
    return pairs


def _is_activity(record: dict) -> bool:
    """True iff the record is an Activity (discriminator check)."""
    return record.get("type") == ACTIVITY_TYPE


# -----------------------------------------------------------------------------
# Field accessors (top-level + metadata fallback)
# -----------------------------------------------------------------------------


def _md(record: dict) -> dict:
    md = record.get("metadata")
    return md if isinstance(md, dict) else {}


def _cohesion_rationale(record: dict) -> str | None:
    val = record.get("cohesion_rationale")
    if isinstance(val, str) and val.strip():
        return val.strip()
    md_val = _md(record).get("cohesion_rationale")
    if isinstance(md_val, str) and md_val.strip():
        return md_val.strip()
    return None


def _belongs_to_bp(record: dict) -> str | None:
    val = record.get("belongs_to_business_process")
    if isinstance(val, str) and val.strip():
        return val.strip()
    md_val = _md(record).get("belongs_to_business_process")
    if isinstance(md_val, str) and md_val.strip():
        return md_val.strip()
    return None


def _composes_entries(record: dict) -> list[dict]:
    val = record.get("composes")
    if isinstance(val, list):
        return [v for v in val if isinstance(v, dict)]
    return []


def _decomposition_boundary(record: dict) -> str | None:
    val = record.get("decomposition_boundary")
    if isinstance(val, str) and val.strip():
        return val.strip()
    md_val = _md(record).get("decomposition_boundary")
    if isinstance(md_val, str) and md_val.strip():
        return md_val.strip()
    return None


# -----------------------------------------------------------------------------
# Rules
# -----------------------------------------------------------------------------


def _check_act_001(record: dict) -> str | None:
    """ACT-001: Every Activity belongs to a Business Process."""
    bp = _belongs_to_bp(record)
    if not bp:
        return (
            "type=Activity but belongs_to_business_process is missing "
            "(top-level or metadata.belongs_to_business_process)"
        )
    if not BP_ID_PATTERN.match(bp):
        return (
            f"belongs_to_business_process={bp!r} does not match the "
            f"`dea:process-*` id family (CR-BP-04 §4 BP id pattern)"
        )
    return None


def _check_act_002(record: dict) -> str | None:
    """ACT-002: Activity is NOT a Business Process."""
    # A record cannot be both Process (L2) and Activity (L3). The
    # type field is a single discriminator; double-typed records
    # are not permitted by the entity schema. The check catches
    # the orthogonal case where a `kind` or auxiliary field tries
    # to promote an Activity to BP.
    for aux in ("kind", "process_kind", "promoted_to"):
        val = record.get(aux)
        if val in ("BusinessProcess", "Process", "L2Process"):
            return (
                f"Activity declares {aux}={val!r} which promotes it to a "
                f"Business Process (Activity ≠ Business Process per CR-BP-32 §5)"
            )
    return None


def _check_act_003(record: dict) -> str | None:
    """ACT-003: Every Activity has a cohesion rationale."""
    rationale = _cohesion_rationale(record)
    if not rationale:
        return (
            "Activity must declare a non-empty `cohesion_rationale` "
            "(CR-BP-32 §6; top-level or metadata.cohesion_rationale)"
        )
    if len(rationale) < MIN_COHESION_RATIONALE_LEN:
        return (
            f"cohesion_rationale is too short ({len(rationale)} chars; "
            f"need ≥ {MIN_COHESION_RATIONALE_LEN}). A rationale is "
            f"required, not a label."
        )
    return None


def _check_act_004(record: dict) -> str | None:
    """ACT-004: Activity has ≥1 composed Task OR boundary marker."""
    composes = _composes_entries(record)
    if composes:
        # At least one entry must point at a Task id (or be a Task
        # reference when the catalog's Task schema is registered).
        # Until `dea:Task` lands (CR-BP-33), accept any `dea:task-*`
        # id OR an explicit task_kind field.
        for entry in composes:
            target = entry.get("target_id")
            if isinstance(target, str) and TASK_ID_PATTERN.match(target):
                return None
            kind = entry.get("target_kind") or entry.get("task_kind")
            if kind in ("Task", "dea:Task"):
                return None
        # composes[] present but no Task target → still flag (the
        # Activity declares decomposition but does not terminate
        # at the L4 boundary)
        return (
            "Activity declares composes[] but no entry targets a "
            "`dea:task-*` id (CR-BP-32 §12: L4 is the decomposition "
            "boundary). Set `decomposition_boundary: l4-reached` if "
            "decomposition ends at the Activity itself."
        )
    # No composes[]. The Activity must declare the boundary marker.
    boundary = _decomposition_boundary(record)
    if boundary and boundary.strip().lower() in ("l4-reached",
                                                "l4",
                                                "atomic",
                                                "no-further-decomposition"):
        return None
    return (
        "Activity has no composes[] entries and no "
        "`decomposition_boundary` marker. Either add ≥1 Task "
        "reference to composes[], or assert "
        "`decomposition_boundary: l4-reached`."
    )


def _check_act_005(record: dict) -> str | None:
    """ACT-005: Composition uses dea:composes (not custom rels)."""
    for entry in _composes_entries(record):
        rt = entry.get("relationship_type")
        if rt in FORBIDDEN_COMPOSITION_TYPES:
            return (
                f"composes[] entry uses forbidden relationship_type={rt!r} "
                f"(CR-BP-32 §7 forbids {sorted(FORBIDDEN_COMPOSITION_TYPES)}; "
                f"use {CANONICAL_COMPOSITION_TYPE!r})"
            )
        if rt is not None and rt != CANONICAL_COMPOSITION_TYPE:
            return (
                f"composes[] entry uses relationship_type={rt!r}; "
                f"CR-BP-32 §7 mandates {CANONICAL_COMPOSITION_TYPE!r}"
            )
    return None


def _check_act_006(record: dict) -> str | None:
    """ACT-006: No execution-ordering fields (composition is structural)."""
    for field in FORBIDDEN_EXECUTION_FIELDS:
        if field in record:
            return (
                f"Activity carries execution-ordering field {field!r} "
                f"(CR-BP-32 §7: composition is structural only; "
                f"forbidden fields: {sorted(FORBIDDEN_EXECUTION_FIELDS)})"
            )
        if field in _md(record):
            return (
                f"Activity carries execution-ordering field "
                f"metadata.{field!r} (CR-BP-32 §7: composition is "
                f"structural only)"
            )
    return None


def _check_act_007(record: dict) -> str | None:
    """ACT-007: Activity id ≠ Business Function id."""
    rec_id = record.get("id")
    if isinstance(rec_id, str) and FUNCTION_ID_PATTERN.match(rec_id):
        return (
            f"id={rec_id!r} belongs to the Business Function id family "
            f"(dea:function-*). Activity is NOT a synonym for Business "
            f"Function (CR-BP-32 §3.1). Use the dea:activity-* family."
        )
    return None


def _check_act_008(record: dict) -> str | None:
    """ACT-008: No implementation-detail marker fields."""
    for field in FORBIDDEN_IMPLEMENTATION_FIELDS:
        if field in record or field in _md(record):
            return (
                f"Activity carries implementation-detail field "
                f"{field!r} (CR-BP-32 §12: L4 is the catalog "
                f"decomposition boundary; anything below belongs to "
                f"implementation detail)"
            )
    return None


def _check_act_009(record: dict) -> str | None:
    """ACT-009: No execution-model fields (CR-BP-33 owns execution)."""
    for field in FORBIDDEN_EXECUTION_MODEL_FIELDS:
        if field in record or field in _md(record):
            return (
                f"Activity carries execution-model field {field!r} "
                f"(CR-BP-32 §11: Activity does not introduce execution "
                f"semantics; those belong to CR-BP-33)"
            )
    return None


# A reverse-check dispatcher keyed on the parent BP id; populated by
# the caller (see evaluate() below). Each entry is the parent BP
# path. The forward check (ACT-001) handles the no-parent-BP case.
_PARENT_INDEX: dict[str, Path] = {}


# Re-declare ACT-010 with reverse-check support. We keep the
# standalone _check_act_010 above as a forward-only fallback for
# tests that construct records in isolation.
def _check_act_010_reverse(record: dict) -> str | None:
    rec_id = record.get("id")
    bp_ref = _belongs_to_bp(record)
    if not isinstance(rec_id, str) or not bp_ref:
        return None
    if bp_ref not in _PARENT_INDEX:
        return None  # parent BP absent; forward reference suffices
    parent_path = _PARENT_INDEX[bp_ref]
    try:
        parent = yaml.safe_load(parent_path.read_text())
    except (yaml.YAMLError, OSError):
        return None
    if not isinstance(parent, dict):
        return None
    # Reverse reference must appear in metadata.activity_references[]
    # OR in composes[] entries.
    md = parent.get("metadata") or {}
    activity_refs = md.get("activity_references") if isinstance(md, dict) else None
    if isinstance(activity_refs, list) and rec_id in activity_refs:
        return None
    for entry in parent.get("composes") or []:
        if isinstance(entry, dict) and entry.get("target_id") == rec_id:
            return None
    return (
        f"Activity {rec_id!r} declares belongs_to_business_process="
        f"{bp_ref!r}, but the parent BP does not list {rec_id!r} in "
        f"`metadata.activity_references` or in a composes[] entry "
        f"(ACT-010 bidirectional traceability)"
    )


# _RULES table — note ACT-010 is path-aware via the caller-set
# _PARENT_INDEX; the wrapper below delegates to it.
def _check_act_010_wrapper(record: dict, _path: Path) -> str | None:
    return _check_act_010_reverse(record)


# CR-BP-97 ACT-011..015 extensions (advisory; OPTIONAL fields).
# These checks pass vacuously when the field is absent (back-compat rule
# per CR-BP-95). When the field IS present, structure is enforced.
# ACT-016..020 are covered by existing ACT-004 / ACT-010; CR-BP-97
# reconciles the prose rather than introducing net-new rules.

MIN_DEFINITION_LEN_ACT_011 = 120  # Substantive prose minimum for the cohesive work statement.


def _definition(record: dict) -> str:
    """Return the Activity's `definition:` string, top-level or metadata."""
    val = record.get("definition")
    if isinstance(val, str):
        return val.strip()
    md = record.get("metadata") or {}
    if isinstance(md, dict):
        val = md.get("definition")
        if isinstance(val, str):
            return val.strip()
    return ""


def _check_act_011(record: dict) -> str | None:
    """ACT-011 (CR-BP-97): Cohesive work statement adequacy.

    The Activity's `definition:` field must be substantive prose (>= 120 chars).
    Back-compat: ACT-003 already requires `cohesion_rationale`; ACT-011
    strengthens the `definition` minimum. The check skips `deprecated`
    lifecycle records (deprecation may carry a minimal definition).
    """
    lifecycle = (record.get("lifecycle_status") or "").strip().lower()
    if lifecycle in ("deprecated", "retired"):
        return None
    definition = _definition(record)
    if len(definition) < MIN_DEFINITION_LEN_ACT_011:
        return (
            f"Activity `definition` is too short "
            f"({len(definition)} chars; need >= {MIN_DEFINITION_LEN_ACT_011}). "
            f"A cohesive work statement is required, not a label."
        )
    return None


def _check_act_012(record: dict) -> str | None:
    """ACT-012 (CR-BP-97): Inputs/Outputs integrity (advisory; OPTIONAL).

    When `inputs[]` or `outputs[]` is present, every entry must conform to
    the universal-contract shape (CR-BP-92 §4).
    """
    inputs = record.get("inputs")
    if inputs is not None:
        if not isinstance(inputs, list) or not inputs:
            return "inputs present but empty"
        for idx, item in enumerate(inputs):
            if not isinstance(item, dict):
                return f"inputs[{idx}] must be an object with id/name/description/source"
            for required in ("id", "name", "description", "source"):
                if not str(item.get(required, "")).strip():
                    return f"inputs[{idx}].{required} missing or empty"
    outputs = record.get("outputs")
    if outputs is not None:
        if not isinstance(outputs, list) or not outputs:
            return "outputs present but empty"
        for idx, item in enumerate(outputs):
            if not isinstance(item, dict):
                return f"outputs[{idx}] must be an object with id/name/description/consumer"
            for required in ("id", "name", "description", "consumer"):
                if not str(item.get(required, "")).strip():
                    return f"outputs[{idx}].{required} missing or empty"
    return None


def _check_act_013(record: dict) -> str | None:
    """ACT-013 (CR-BP-97): Outcome contribution (advisory; OPTIONAL).

    When `outcome_contribution:` is present, must be a non-empty string.
    """
    contribution = record.get("outcome_contribution")
    if contribution is None:
        return None
    if not isinstance(contribution, str) or not contribution.strip():
        return "outcome_contribution present but empty string"
    return None


def _check_act_014(record: dict) -> str | None:
    """ACT-014 (CR-BP-97): Boundary and exclusions (advisory; OPTIONAL).

    When `boundary:` is present, must be a non-empty string or a non-empty
    object with inclusions/exclusions.
    """
    boundary = record.get("boundary")
    if boundary is None:
        return None
    if isinstance(boundary, str):
        if not boundary.strip():
            return "boundary present but empty string"
        return None
    if isinstance(boundary, dict):
        if not boundary:
            return "boundary present but empty object"
        return None
    return "boundary must be a string or a non-empty object"


# Cross-record check; populated by evaluate() via _SIBLING_INDEX.
# _SIBLING_INDEX maps (parent_bp_id, activity_name) -> list of activity ids.
_SIBLING_INDEX: dict[tuple[str, str], list[str]] = {}


def _check_act_015(record: dict) -> str | None:
    """ACT-015 (CR-BP-97): Sibling distinction (advisory; cross-record).

    When two or more Activities share the same parent Business Process and
    the same `name`, emit a finding. The check uses the in-memory sibling
    index populated by evaluate().
    """
    rec_id = record.get("id")
    name = (record.get("name") or "").strip()
    bp_ref = _belongs_to_bp(record)
    if not isinstance(rec_id, str) or not name or not bp_ref:
        return None
    siblings = _SIBLING_INDEX.get((bp_ref, name), [])
    if len(siblings) > 1 and rec_id in siblings:
        return (
            f"Activity name={name!r} appears on multiple sibling Activities "
            f"in the same parent BP ({bp_ref!r}): {siblings}. "
            f"Each sibling should have a distinct name."
        )
    return None


_RULES_RECORD = (
    ("ACT-001", _check_act_001,
     "Every Activity belongs to a Business Process"),
    ("ACT-002", _check_act_002,
     "Activity is not a Business Process"),
    ("ACT-003", _check_act_003,
     "Every Activity has a cohesion rationale"),
    ("ACT-004", _check_act_004,
     "Activity has composed Task OR boundary marker"),
    ("ACT-005", _check_act_005,
     "Composition uses dea:composes"),
    ("ACT-006", _check_act_006,
     "No execution-ordering fields"),
    ("ACT-007", _check_act_007,
     "Activity id is not Business Function id"),
    ("ACT-008", _check_act_008,
     "No implementation-detail marker fields"),
    ("ACT-009", _check_act_009,
     "No execution-model fields (CR-BP-33 owns execution)"),
    # CR-BP-97 extensions (advisory; OPTIONAL fields).
    ("ACT-011", _check_act_011,
     "Cohesive work statement adequacy"),
    ("ACT-012", _check_act_012,
     "Inputs/Outputs integrity (advisory; OPTIONAL)"),
    ("ACT-013", _check_act_013,
     "Outcome contribution (advisory; OPTIONAL)"),
    ("ACT-014", _check_act_014,
     "Boundary and exclusions (advisory; OPTIONAL)"),
    ("ACT-015", _check_act_015,
     "Sibling distinction (advisory; cross-record)"),
)


# -----------------------------------------------------------------------------
# Evaluation
# -----------------------------------------------------------------------------


def _build_parent_index(catalog_root: Path) -> dict[str, Path]:
    """Build {bp_id -> bp_yaml_path} for every BP record on disk.

    Used by ACT-010 to enforce bidirectional traceability: when an
    Activity names a parent BP that exists in the catalog, the parent
    BP must declare the Activity in metadata.activity_references or
    composes[].
    """
    base = catalog_root / "entities" / "v1-alpha"
    index: dict[str, Path] = {}
    if not base.exists():
        return index
    for entry in sorted(base.iterdir()):
        if not entry.is_dir() or not entry.name.startswith("dea:process-"):
            continue
        yaml_path = entry / f"{entry.name}.yaml"
        if not yaml_path.exists():
            continue
        try:
            data = yaml.safe_load(yaml_path.read_text())
        except yaml.YAMLError:
            continue
        if isinstance(data, dict):
            rec_id = data.get("id")
            if isinstance(rec_id, str):
                index[rec_id] = yaml_path
    return index


def evaluate(pairs, parent_index: dict[str, Path] | None = None) -> list[dict]:
    """Run all rules (ACT-001..009 + ACT-011..015) against every (path, record) pair.

    Only records with type=Activity are inspected (per CR-BP-32 §17).
    Business Process records (type=Process) are NEVER inspected.

    CR-BP-97: this function also populates the in-memory _SIBLING_INDEX
    (used by ACT-015 cross-record check) before running the rule set.
    Findings from ACT-011..015 are tagged `advisory: True` so the
    --strict mode does not fail on them.
    """
    global _PARENT_INDEX, _SIBLING_INDEX
    if parent_index is None:
        parent_index = {}
    _PARENT_INDEX = parent_index
    # Populate the sibling index from the activity records themselves.
    _SIBLING_INDEX = {}
    for _path, record in pairs:
        if not _is_activity(record):
            continue
        rec_id = record.get("id")
        name = (record.get("name") or "").strip()
        bp_ref = _belongs_to_bp(record)
        if not isinstance(rec_id, str) or not name or not bp_ref:
            continue
        _SIBLING_INDEX.setdefault((bp_ref, name), []).append(rec_id)

    findings: list[dict] = []
    for path, record in pairs:
        if not _is_activity(record):
            continue  # BP records are out of scope (CR-BP-32 §17)
        rec_id = record.get("id") or path.parent.name
        # Record-only rules
        for rule_id, fn, _label in _RULES_RECORD:
            diagnostic = fn(record)
            if diagnostic is not None:
                findings.append({
                    "rule": rule_id,
                    "record_id": rec_id,
                    "diagnostic": diagnostic,
                    "advisory": rule_id.startswith("ACT-01") and rule_id not in (
                        "ACT-001", "ACT-002", "ACT-003", "ACT-004",
                        "ACT-005", "ACT-006", "ACT-007", "ACT-008", "ACT-009",
                    ),
                })
        # ACT-010 (reverse-traceability)
        diagnostic = _check_act_010_wrapper(record, path)
        if diagnostic is not None:
            findings.append({
                "rule": "ACT-010",
                "record_id": rec_id,
                "diagnostic": diagnostic,
                "advisory": False,
            })
    return findings


def _verdict(findings: list[dict]) -> str:
    """Compute verdict from findings.

    CR-BP-97 design intent: only mandatory (non-advisory) findings count
    toward NON-CONFORMANT. Advisory findings are surfaced for transparency
    but do not change the verdict.
    """
    mandatory = [f for f in findings if not f.get("advisory", False)]
    if mandatory:
        return "NON-CONFORMANT"
    return "CONFORMANT"


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(
        "Activity Model validator (CR-BP-32; ACT-001..010)."
    ))
    parser.add_argument(
        "--catalog-root",
        default=".",
        help="Path to the catalog repo root (default: current directory).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 on any finding (otherwise findings are advisory).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON output instead of human-readable summary.",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run the built-in self-test and exit.",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    catalog_root = Path(args.catalog_root).resolve()
    pairs = _load_records(catalog_root)
    activity_pairs = [(p, r) for p, r in pairs if _is_activity(r)]
    parent_index = _build_parent_index(catalog_root)
    findings = evaluate(activity_pairs, parent_index=parent_index)
    verdict = _verdict(findings)

    if args.json:
        print(json.dumps({
            "verdict": verdict,
            "activity_record_count": len(activity_pairs),
            "bp_record_count": len(parent_index),
            "finding_count": len(findings),
            "findings": findings,
            "rules": [
                {"id": rid, "name": label}
                for rid, _fn, label in _RULES_RECORD
            ] + [{"id": "ACT-010",
                  "name": "Activity traceability to parent BP"}],
            "forbidden_composition_types": sorted(FORBIDDEN_COMPOSITION_TYPES),
            "canonical_composition_type": CANONICAL_COMPOSITION_TYPE,
        }, indent=2, sort_keys=True))
    else:
        print(f"Activity Model (CR-BP-32 ACT-001..010 + CR-BP-97 ACT-011..015): {verdict}")
        print(f"  Activity records: {len(activity_pairs)}")
        print(f"  BP records:       {len(parent_index)}")
        print(f"  Findings:         {len(findings)}")
        for rid, _fn, label in _RULES_RECORD:
            n = sum(1 for f in findings if f["rule"] == rid)
            advisory_marker = " [advisory]" if rid.startswith("ACT-011") or rid.startswith("ACT-012") or rid.startswith("ACT-013") or rid.startswith("ACT-014") or rid.startswith("ACT-015") else ""
            print(f"    {rid} ({label}): {n}{advisory_marker}")
        n = sum(1 for f in findings if f["rule"] == "ACT-010")
        print(f"    ACT-010 (Activity traceability to parent BP): {n}")
        if findings:
            print("\nFindings:")
            for f in findings:
                adv = " [advisory]" if f.get("advisory") else ""
                print(f"  [{f['rule']}{adv}] {f['record_id']}: {f['diagnostic']}")

    if findings and args.strict:
        # CR-BP-97: --strict only fails on mandatory findings, not advisory.
        mandatory_findings = [f for f in findings if not f.get("advisory", False)]
        if mandatory_findings:
            return 1
    return 0


# -----------------------------------------------------------------------------
# Self-test
# -----------------------------------------------------------------------------


def _record(id_: str = "dea:activity-self-test",
            name: str = "Self Test Activity",
            belongs_to: str = "dea:process-manage-customer-relationship",
            cohesion: str = (
                "This activity groups the cohesive logical work of "
                "validating customer eligibility prior to fulfilment. "
                "The grouping is justified by the single outcome: a "
                "decision to proceed or hold."),
            composes: list | None = None,
            boundary: str | None = "l4-reached",
            definition: str | None = (
                "The cohesive grouping of work within the parent Business "
                "Process that validates customer eligibility prior to "
                "fulfilment, contributing materially to the parent process "
                "outcome without independently satisfying the qualification "
                "criteria of a Business Process. The grouping is justified "
                "by the single outcome: a decision to proceed or hold."),
            extra: dict | None = None) -> dict:
    d = {
        "id": id_,
        "name": name,
        "type": ACTIVITY_TYPE,
        "version": "1.0.0",
        "belongs_to_business_process": belongs_to,
        "cohesion_rationale": cohesion,
    }
    if composes is not None:
        d["composes"] = composes
    if boundary is not None:
        d["decomposition_boundary"] = boundary
    if definition is not None:
        d["definition"] = definition
    if extra:
        d.update(extra)
    return d


def _self_test() -> int:
    """Built-in self-test."""
    import tempfile

    def _path(tmpdir: Path, id_: str) -> Path:
        return tmpdir / id_ / f"{id_}.yaml"

    # The self-test exercises rule logic via evaluate() directly so
    # the rules can be tested in isolation from the file system.
    # The on-disk ACT-010 reverse check requires a real parent BP,
    # so we set _PARENT_INDEX manually for that case.

    # --- ACT-001: missing belongs_to_business_process
    r = _record(belongs_to="")
    f = evaluate([(Path("/x"), r)])
    assert any(x["rule"] == "ACT-001" for x in f), f

    # --- ACT-001: bad pattern
    r = _record(belongs_to="dea:function-foo")
    f = evaluate([(Path("/x"), r)])
    assert any(x["rule"] == "ACT-001" for x in f), f

    # --- ACT-001: passes
    assert evaluate([(Path("/x"), _record())]) == []

    # --- ACT-002: promotion attempt via `kind`
    r = _record(extra={"kind": "BusinessProcess"})
    f = evaluate([(Path("/x"), r)])
    assert any(x["rule"] == "ACT-002" for x in f), f

    # --- ACT-002: passes
    assert evaluate([(Path("/x"), _record())]) == []

    # --- ACT-003: missing rationale
    r = _record(cohesion="")
    f = evaluate([(Path("/x"), r)])
    assert any(x["rule"] == "ACT-003" for x in f), f

    # --- ACT-003: too short
    r = _record(cohesion="short")
    f = evaluate([(Path("/x"), r)])
    assert any(x["rule"] == "ACT-003" for x in f), f

    # --- ACT-003: passes
    assert evaluate([(Path("/x"), _record())]) == []

    # --- ACT-004: no composes, no boundary marker
    f = evaluate([(Path("/x"), _record(composes=[], boundary=None))])
    assert any(x["rule"] == "ACT-004" for x in f), f

    # --- ACT-004: composes present but no Task target
    f = evaluate([(Path("/x"), _record(composes=[
        {"target_id": "dea:group-foo",
         "relationship_type": CANONICAL_COMPOSITION_TYPE}]))])
    assert any(x["rule"] == "ACT-004" for x in f), f

    # --- ACT-004: composes with Task target passes
    assert evaluate([(Path("/x"), _record(composes=[
        {"target_id": "dea:task-validate-eligibility",
         "relationship_type": CANONICAL_COMPOSITION_TYPE}]))]) == []

    # --- ACT-004: boundary marker passes
    assert evaluate([(Path("/x"), _record(
        composes=[],
        boundary="l4-reached"))]) == []

    # --- ACT-005: forbidden relationship_type
    f = evaluate([(Path("/x"), _record(composes=[
        {"target_id": "dea:task-x",
         "relationship_type": "decomposes"}]))])
    assert any(x["rule"] == "ACT-005" for x in f), f

    # --- ACT-005: non-canonical relationship_type
    f = evaluate([(Path("/x"), _record(composes=[
        {"target_id": "dea:task-x",
         "relationship_type": "contains"}]))])
    assert any(x["rule"] == "ACT-005" for x in f), f

    # --- ACT-005: canonical passes
    assert evaluate([(Path("/x"), _record(composes=[
        {"target_id": "dea:task-x",
         "relationship_type": CANONICAL_COMPOSITION_TYPE}]))]) == []

    # --- ACT-006: execution-ordering field
    for fld in FORBIDDEN_EXECUTION_FIELDS:
        r = _record(extra={fld: 1})
        f = evaluate([(Path("/x"), r)])
        assert any(x["rule"] == "ACT-006" for x in f), (fld, f)
    # Metadata-scoped
    r = _record(extra={"metadata": {"execution_order": 1}})
    f = evaluate([(Path("/x"), r)])
    assert any(x["rule"] == "ACT-006" for x in f), f

    # --- ACT-006: clean
    assert evaluate([(Path("/x"), _record())]) == []

    # --- ACT-007: Business Function id
    r = _record(id_="dea:function-something")
    f = evaluate([(Path("/x"), r)])
    assert any(x["rule"] == "ACT-007" for x in f), f

    # --- ACT-007: clean
    assert evaluate([(Path("/x"), _record())]) == []

    # --- ACT-008: implementation-detail field
    for fld in FORBIDDEN_IMPLEMENTATION_FIELDS:
        r = _record(extra={fld: "x"})
        f = evaluate([(Path("/x"), r)])
        assert any(x["rule"] == "ACT-008" for x in f), (fld, f)
    assert evaluate([(Path("/x"), _record())]) == []

    # --- ACT-009: execution-model field
    for fld in FORBIDDEN_EXECUTION_MODEL_FIELDS:
        r = _record(extra={fld: "x"})
        f = evaluate([(Path("/x"), r)])
        assert any(x["rule"] == "ACT-009" for x in f), (fld, f)
    assert evaluate([(Path("/x"), _record())]) == []

    # --- ACT-010: reverse-traceability requires parent BP on disk.
    # Build a temp parent BP that does NOT reference this Activity.
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        bp_id: str = "dea:process-test-bp"
        bp_yaml = td_path / "bp.yaml"
        bp_yaml.write_text(yaml.safe_dump({
            "id": bp_id,
            "name": "Test BP",
            "type": "Process",
            "version": "1.0.0",
        }))
        # Parent index present but no reverse reference → ACT-010 fires
        idx = {bp_id: bp_yaml}
        r = _record(belongs_to=bp_id,
                    id_="dea:activity-orphan")
        f = evaluate([(td_path / "dea:activity-orphan.yaml", r)],
                     parent_index=idx)
        assert any(x["rule"] == "ACT-010" for x in f), f

        # Parent declares reverse reference → passes
        bp_yaml.write_text(yaml.safe_dump({
            "id": bp_id,
            "name": "Test BP",
            "type": "Process",
            "version": "1.0.0",
            "metadata": {"activity_references": ["dea:activity-tracked"]},
        }))
        r = _record(belongs_to=bp_id,
                    id_="dea:activity-tracked")
        f = evaluate([(td_path / "dea:activity-tracked.yaml", r)],
                     parent_index=idx)
        assert not any(x["rule"] == "ACT-010" for x in f), f

        # Parent BP absent → ACT-010 degrades to forward check only
        r = _record(belongs_to="dea:process-nonexistent",
                    id_="dea:activity-solo")
        f = evaluate([(td_path / "dea:activity-solo.yaml", r)],
                     parent_index={})
        assert not any(x["rule"] == "ACT-010" for x in f), f

    # --- Type filter: BP records are never inspected
    bp_record = {
        "id": "dea:process-foo",
        "name": "Foo",
        "type": "Process",
        "version": "1.0.0",
        # even deliberately-bad fields are ignored on a Process
        "execution_order": 1,
        "workflow": "bpmn:process_foo",
    }
    assert evaluate([(Path("/x"), bp_record)]) == []

    print("self-test PASS (20 cases)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
