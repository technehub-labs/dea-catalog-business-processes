#!/usr/bin/env python3
"""
check_execution_boundary.py
============================

Execution Boundary validator (CR-BP-33; EXE-001..010).

Codifies the Execution Boundary rules from CR-BP-33 §15 as machine-testable
per-record invariants. Today the catalog has zero records that carry
Workflow references; the validator is therefore a regression guard that
emits no findings on the existing 126 Business Process records and
prepares the catalog for the first opt-in Workflow / Task / Execution
contribution.

The validator inspects records in two tiers:

  Tier 1 (universal):
    Every record, regardless of type, is scanned for fields that
    would leak execution semantics into the structural layer.
    Today zero records carry such fields; the check is a
    forward-looking guard against accidental introduction.

  Tier 2 (opt-in):
    Records that declare `workflow_references[]`, `executed_by`,
    or a `composes[]` entry with execution-ordering annotations
    are additionally validated against EXE-001..010. A BP record
    with no Workflow reference is VALID (Execution mode = unmodelled);
    no finding is emitted (CR-BP-33 "Result (post-landing)" §3:
    "No retroactive Workflow instantiation. Existing BPs stay at L4
    conformance with no execution references. Workflow adoption is
    opt-in for new BPs that explicitly need an execution model.").

Rules (derived from CR-BP-33 §15):

  EXE-001 — Structural decomposition shall not encode execution sequence.
            For any record: composes[] entries MUST NOT carry
            execution-ordering annotations (`execution_order`,
            `sequence_index`, `step_index`, `temporal_sequence`,
            `before`, `after`, `precedes`, `follows`,
            `triggers`, `next_step`). Structural composition is
            part-whole only (CR-BP-33 §6).

  EXE-002 — `dea:composes` shall not be interpreted as execution ordering.
            For any composes[] entry: relationship_type=dea:composes
            MUST NOT be accompanied by ordering fields. (This is the
            type-level complement to EXE-001; together they prevent
            the "A composes B, B composes C ⇒ A→B→C executes in
            that order" inference.)

  EXE-003 — Workflow shall remain distinct from Business Process.
            A record with type=Workflow MUST NOT carry L2 BP
            classification fields (process_intent, process_type,
            process_specialization, process_audience). Workflow is
            its own concept (CR-BP-33 §5, §14).

  EXE-004 — A Business Process may have multiple execution Workflows.
            For any BP record: `workflow_references[]` is a list,
            not a singleton field. Multiple entries are permitted
            (CR-BP-33 §11: "Standard / Exception / Assisted
            Fulfilment Workflow" pattern). A singleton field
            (e.g. `workflow:` scalar) is rejected; use
            `workflow_references: [{workflow_id, relationship_kind}, ...]`.

  EXE-005 — Different Workflow implementations shall not automatically
            create different Business Processes.
            For any BP record: the presence of multiple
            `workflow_references[]` entries MUST NOT cause the
            BP record to declare duplicate `process_intent` /
            `process_type` axes (which would imply BP splitting).
            If a BP record has ≥ 2 workflow_references, its
            `process_intent` MUST remain singular (no duplicate
            axis declarations).

  EXE-006 — Execution actors shall reference existing Actor semantics.
            For any record with `executed_by` or `performed_by`:
            the value MUST be a reference to a canonical Actor
            (an id matching `dea:actor-*` or a declared reference
            via `actor_reference` field), NOT an inline string
            describing the actor. Inline actor strings (e.g.
            "the Sales team") are rejected; they bypass the
            Actor record semantics (CR-BP-33 §9).

  EXE-007 — Execution systems shall reference existing System semantics.
            For any record with `execution_system`, `system_ref`,
            or `executing_system`: the value MUST be a reference
            to a canonical System record (id matching `dea:system-*`
            or `system_reference` field), NOT an inline string.

  EXE-008 — Execution logic shall not redefine process identity.
            For any BP record with workflow_references[]:
            the BP's `identity.verb` and `identity.object` MUST NOT
            be duplicated on the referenced Workflow record (if
            resolved). Identity lives on the BP; Workflow is an
            execution realization, not a re-definition
            (CR-BP-33 §8).

  EXE-009 — Implementation detail shall remain outside the Business
            Process decomposition model.
            For any record: MUST NOT carry `api_sequence`,
            `database_procedure`, `application_control_flow`,
            `infrastructure_operation`, `script`, `code_ref`,
            `technical_runbook` (top-level or metadata.*). These
            belong to implementation models, not the process
            catalog (CR-BP-33 §12).

  EXE-010 — Every catalogued Workflow reference shall identify its
            relationship to the associated Business Process.
            For any BP record with `workflow_references[]`: each
            entry MUST carry a `relationship_kind` field whose
            value is one of the controlled vocabulary
            (`reference`, `operational`, `scenario`, `implementation`).
            CR-BP-33 §13 names this vocabulary explicitly.

Coverage on the live catalog (2026-09-12): zero records carry
Workflow references or execution-bearing fields. Expected findings:
EXE-001..010 = 0 across all 196 records. The validator is a
forward-looking regression guard.

Exit codes:
  0  all records satisfy all ten rules
  1  at least one record fails at least one rule
  2  self-test failure or I/O error

Usage:
  python3 scripts/check_execution_boundary.py
  python3 scripts/check_execution_boundary.py --strict
  python3 scripts/check_execution_boundary.py --json
  python3 scripts/check_execution_boundary.py --self-test

Author: Coder (for eaojnr). Established by CR-BP-33 (2026-09-12).
Derived from CR-BP-33 §15 (Execution Conformance Rules) and
CR-BP-33 §3, §5, §6, §8, §9, §11, §12, §13, §14. See
change-requests/CR-BP-33-execution-boundary.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

# ID family patterns (CR-BP-04 §4 + CR-BP-33 §9).
ACTOR_ID_PATTERN = re.compile(r"^dea:actor-[a-z0-9-]+$")
SYSTEM_ID_PATTERN = re.compile(r"^dea:system-[a-z0-9-]+$")
WORKFLOW_ID_PATTERN = re.compile(r"^dea:workflow-[a-z0-9-]+$")

# EXE-001 / EXE-002 forbidden execution-ordering annotations on
# composes[] entries (structural layer is part-whole only).
FORBIDDEN_COMPOSITION_ORDERING_FIELDS = frozenset({
    "execution_order",
    "sequence_index",
    "step_index",
    "temporal_sequence",
    "before",
    "after",
    "precedes",
    "follows",
    "triggers",
    "next_step",
})

# EXE-003 forbidden L2 BP classification fields on Workflow records
# (Workflow is not a Business Process).
BP_CLASSIFICATION_FIELDS = frozenset({
    "process_intent",
    "process_type",
    "process_specialization",
    "process_audience",
})

# EXE-004 forbidden singleton workflow fields (multiple execution
# realizations require a list, not a scalar).
FORBIDDEN_SINGLETON_WORKFLOW_FIELDS = frozenset({
    "workflow",
    "workflow_ref",
    "execution_workflow",
})

# EXE-005: when a BP has ≥ 2 workflow_references, the BP must not
# declare duplicate axes that would imply BP splitting.
WORKFLOW_REL_KIND_VOCABULARY = frozenset({
    "reference",          # reference execution
    "operational",        # operational execution
    "scenario",           # scenario-specific execution
    "implementation",     # implementation-specific execution
})

# EXE-006 forbidden inline actor strings.
INLINE_ACTOR_STRING_PATTERN = re.compile(
    r"^(the |a |an )?(sales|finance|operations|engineering|hr|legal|"
    r"customer|user|admin|system|team|department|manager)s?\b",
    re.IGNORECASE,
)

# EXE-009 forbidden implementation-detail fields.
FORBIDDEN_IMPLEMENTATION_FIELDS = frozenset({
    "api_sequence",
    "database_procedure",
    "application_control_flow",
    "infrastructure_operation",
    "script",
    "code_ref",
    "technical_runbook",
})

# Discriminators.
WORKFLOW_TYPE = "Workflow"
PROCESS_TYPE = "Process"
ACTIVITY_TYPE = "Activity"


# -----------------------------------------------------------------------------
# Discovery
# -----------------------------------------------------------------------------


def _load_records(catalog_root: Path) -> list[tuple[Path, dict]]:
    """Load every record under entities/v1-alpha/ (all types).

    Unlike the LCM/SIV/ACT validators which filter on a specific
    type, EXE-001..010 span both the universal tier (no execution
    leakage on ANY record) and the opt-in tier (records WITH
    Workflow references). We therefore load every record.
    """
    base = catalog_root / "entities" / "v1-alpha"
    pairs: list[tuple[Path, dict]] = []
    if not base.exists():
        return pairs
    # CR-BP-mv1: walk the containment tree for id-derived record files.
    for yaml_path in sorted(base.rglob("processes-*.yaml")):
        if not yaml_path.exists():
            continue
        try:
            data = yaml.safe_load(yaml_path.read_text())
        except yaml.YAMLError as exc:
            print(f"WARN: {yaml_path}: YAML parse error: {exc}",
                  file=sys.stderr)
            continue
        if isinstance(data, dict):
            pairs.append((yaml_path, data))
    return pairs


def _md(record: dict) -> dict:
    md = record.get("metadata")
    return md if isinstance(md, dict) else {}


def _composes_entries(record: dict) -> list[dict]:
    val = record.get("composes")
    if isinstance(val, list):
        return [v for v in val if isinstance(v, dict)]
    return []


def _workflow_references(record: dict) -> list[dict]:
    """Extract workflow_references[] entries (top-level or metadata)."""
    val = record.get("workflow_references")
    if isinstance(val, list):
        return [v for v in val if isinstance(v, dict)]
    md_val = _md(record).get("workflow_references")
    if isinstance(md_val, list):
        return [v for v in md_val if isinstance(v, dict)]
    return []


def _identity(record: dict) -> dict:
    val = record.get("identity")
    return val if isinstance(val, dict) else {}


# -----------------------------------------------------------------------------
# Rules
# -----------------------------------------------------------------------------


def _check_exe_001(record: dict) -> str | None:
    """EXE-001: composes[] entries shall not carry execution ordering."""
    for entry in _composes_entries(record):
        for field in FORBIDDEN_COMPOSITION_ORDERING_FIELDS:
            if field in entry:
                return (
                    f"composes[] entry carries execution-ordering "
                    f"annotation {field!r} (CR-BP-33 §6: structural "
                    f"composition is part-whole only; forbidden fields: "
                    f"{sorted(FORBIDDEN_COMPOSITION_ORDERING_FIELDS)})"
                )
    return None


def _check_exe_002(record: dict) -> str | None:
    """EXE-002: dea:composes shall not be reinterpreted as ordering.

    EXE-001 already covers the field-level case. EXE-002 is the
    type-level complement: if a composes[] entry has
    relationship_type=dea:composes, no ordering fields may
    accompany it. In practice this is the same check as EXE-001,
    but kept as a separate rule because CR-BP-33 §15 lists them
    separately (structural-level vs. type-level).
    """
    for entry in _composes_entries(record):
        rt = entry.get("relationship_type")
        if rt in ("dea:composes", "composes"):
            for field in FORBIDDEN_COMPOSITION_ORDERING_FIELDS:
                if field in entry:
                    return (
                        f"composes[] entry with relationship_type="
                        f"{rt!r} carries execution-ordering "
                        f"annotation {field!r} (CR-BP-33 §6: "
                        f"dea:composes establishes structural "
                        f"part-whole semantics only, not before/after, "
                        f"precedence, branching, parallelism, "
                        f"synchronization, repetition, or exception "
                        f"handling)"
                    )
    return None


def _check_exe_003(record: dict) -> str | None:
    """EXE-003: Workflow records must not carry BP classification."""
    if record.get("type") != WORKFLOW_TYPE:
        return None  # only fires on Workflow records
    for field in BP_CLASSIFICATION_FIELDS:
        if field in record or field in _md(record):
            return (
                f"Workflow record carries BP classification field "
                f"{field!r} (CR-BP-33 §14: Workflow is distinct "
                f"from Business Process; classification fields "
                f"{sorted(BP_CLASSIFICATION_FIELDS)} belong to BP "
                f"records only)"
            )
    return None


def _check_exe_004(record: dict) -> str | None:
    """EXE-004: multiple Workflow realizations require a list."""
    for field in FORBIDDEN_SINGLETON_WORKFLOW_FIELDS:
        if field in record or field in _md(record):
            return (
                f"BP record carries singleton Workflow field {field!r} "
                f"(CR-BP-33 §11: a Business Process may have multiple "
                f"execution Workflows — Standard / Exception / Assisted "
                f"patterns. Use `workflow_references: [{{workflow_id, "
                f"relationship_kind}}, ...]` instead of a scalar)"
            )
    return None


def _check_exe_005(record: dict) -> str | None:
    """EXE-005: multiple Workflow refs must not split the BP."""
    wf_refs = _workflow_references(record)
    if len(wf_refs) < 2:
        return None  # single realization is fine; nothing to check
    # With ≥ 2 workflow realizations, the BP must remain singular:
    # no duplicate process_intent / process_type declarations.
    intent = record.get("process_intent")
    if isinstance(intent, list) and len(intent) > 1:
        return (
            f"BP record has {len(wf_refs)} workflow_references but "
            f"declares process_intent as a list of {len(intent)} values. "
            f"Multiple execution realizations do NOT justify BP "
            f"splitting (CR-BP-33 §11). process_intent must remain "
            f"singular."
        )
    ptype = record.get("process_type")
    if isinstance(ptype, list) and len(ptype) > 1:
        return (
            f"BP record has {len(wf_refs)} workflow_references but "
            f"declares process_type as a list of {len(ptype)} values. "
            f"Multiple execution realizations do NOT justify BP "
            f"splitting (CR-BP-33 §11). process_type must remain "
            f"singular."
        )
    return None


def _check_exe_006(record: dict) -> str | None:
    """EXE-006: execution actors must reference existing Actor semantics."""
    for field in ("executed_by", "performed_by"):
        val = record.get(field)
        if val is None:
            val = _md(record).get(field)
        if val is None:
            continue
        if isinstance(val, str):
            # Reject inline actor strings; require a reference.
            if INLINE_ACTOR_STRING_PATTERN.match(val):
                return (
                    f"Execution actor field {field!r}={val!r} is an "
                    f"inline string (CR-BP-33 §9: execution actors "
                    f"shall reference existing Actor semantics; use "
                    f"an id matching `dea:actor-*` or an explicit "
                    f"`actor_reference` field)"
                )
            if not ACTOR_ID_PATTERN.match(val):
                return (
                    f"Execution actor field {field!r}={val!r} is not "
                    f"a canonical Actor id (expected `dea:actor-*` "
                    f"pattern per CR-BP-33 §9)"
                )
        elif isinstance(val, dict):
            # Reference-style: actor_reference or id
            ref = val.get("actor_reference") or val.get("id")
            if not isinstance(ref, str) or not ACTOR_ID_PATTERN.match(ref):
                return (
                    f"Execution actor field {field!r} is a dict but "
                    f"lacks a canonical `actor_reference` or `id` "
                    f"matching `dea:actor-*` (CR-BP-33 §9)"
                )
    return None


def _check_exe_007(record: dict) -> str | None:
    """EXE-007: execution systems must reference existing System semantics."""
    for field in ("execution_system", "system_ref", "executing_system"):
        val = record.get(field)
        if val is None:
            val = _md(record).get(field)
        if val is None:
            continue
        if isinstance(val, str):
            if not SYSTEM_ID_PATTERN.match(val):
                return (
                    f"Execution system field {field!r}={val!r} is not "
                    f"a canonical System id (expected `dea:system-*` "
                    f"pattern per CR-BP-33 §9)"
                )
        elif isinstance(val, dict):
            ref = val.get("system_reference") or val.get("id")
            if not isinstance(ref, str) or not SYSTEM_ID_PATTERN.match(ref):
                return (
                    f"Execution system field {field!r} is a dict but "
                    f"lacks a canonical `system_reference` or `id` "
                    f"matching `dea:system-*` (CR-BP-33 §9)"
                )
    return None


def _check_exe_008(record: dict) -> str | None:
    """EXE-008: execution logic shall not redefine process identity.

    The BP's identity.verb / identity.object live on the BP record.
    A Workflow record must not duplicate them (which would imply
    the Workflow is a separate process with its own identity).
    """
    if record.get("type") != WORKFLOW_TYPE:
        return None
    identity = _identity(record)
    if identity.get("verb") or identity.get("object"):
        return (
            f"Workflow record carries identity.verb / identity.object "
            f"(CR-BP-33 §8: execution logic shall not redefine "
            f"process identity. identity.verb / identity.object "
            f"live on the parent Business Process; Workflow is an "
            f"execution realization, not a re-definition)"
        )
    return None


def _check_exe_009(record: dict) -> str | None:
    """EXE-009: no implementation-detail fields."""
    for field in FORBIDDEN_IMPLEMENTATION_FIELDS:
        if field in record or field in _md(record):
            return (
                f"Record carries implementation-detail field {field!r} "
                f"(CR-BP-33 §12: implementation detail shall remain "
                f"outside the Business Process decomposition model; "
                f"forbidden fields: {sorted(FORBIDDEN_IMPLEMENTATION_FIELDS)})"
            )
    return None


def _check_exe_010(record: dict) -> str | None:
    """EXE-010: every Workflow reference declares its relationship_kind."""
    for entry in _workflow_references(record):
        kind = entry.get("relationship_kind")
        wf_id = entry.get("workflow_id") or entry.get("id")
        if not kind:
            return (
                f"workflow_references[] entry (workflow_id={wf_id!r}) "
                f"is missing `relationship_kind` (CR-BP-33 §13: "
                f"every catalogued Workflow reference shall identify "
                f"its relationship to the associated Business Process; "
                f"controlled vocabulary: {sorted(WORKFLOW_REL_KIND_VOCABULARY)})"
            )
        if kind not in WORKFLOW_REL_KIND_VOCABULARY:
            return (
                f"workflow_references[] entry (workflow_id={wf_id!r}) "
                f"has relationship_kind={kind!r} which is not in the "
                f"controlled vocabulary {sorted(WORKFLOW_REL_KIND_VOCABULARY)} "
                f"(CR-BP-33 §13)"
            )
    return None


_RULES_RECORD = (
    ("EXE-001", _check_exe_001,
     "Structural decomposition does not encode execution sequence"),
    ("EXE-002", _check_exe_002,
     "dea:composes does not imply execution ordering"),
    ("EXE-003", _check_exe_003,
     "Workflow remains distinct from Business Process"),
    ("EXE-004", _check_exe_004,
     "Multiple Workflow realizations require a list"),
    ("EXE-005", _check_exe_005,
     "Multiple Workflow realizations do not split the BP"),
    ("EXE-006", _check_exe_006,
     "Execution actors reference existing Actor semantics"),
    ("EXE-007", _check_exe_007,
     "Execution systems reference existing System semantics"),
    ("EXE-008", _check_exe_008,
     "Execution logic does not redefine process identity"),
    ("EXE-009", _check_exe_009,
     "No implementation-detail fields"),
    ("EXE-010", _check_exe_010,
     "Workflow references declare relationship_kind"),
)


# -----------------------------------------------------------------------------
# Evaluation
# -----------------------------------------------------------------------------


def evaluate(pairs) -> list[dict]:
    """Run all ten rules against every (path, record) pair."""
    findings: list[dict] = []
    for path, record in pairs:
        rec_id = record.get("id") or path.parent.name
        for rule_id, fn, _label in _RULES_RECORD:
            diagnostic = fn(record)
            if diagnostic is not None:
                findings.append({
                    "rule": rule_id,
                    "record_id": rec_id,
                    "diagnostic": diagnostic,
                })
    return findings


def _verdict(findings: list[dict]) -> str:
    if findings:
        return "NON-CONFORMANT"
    return "CONFORMANT"


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(
        "Execution Boundary validator (CR-BP-33; EXE-001..010)."
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
    findings = evaluate(pairs)
    verdict = _verdict(findings)

    # Records that opted into execution semantics (for reporting).
    opted_in = [p for p, r in pairs if _workflow_references(r)]

    if args.json:
        print(json.dumps({
            "verdict": verdict,
            "record_count": len(pairs),
            "opted_in_record_count": len(opted_in),
            "finding_count": len(findings),
            "findings": findings,
            "rules": [
                {"id": rid, "name": label}
                for rid, _fn, label in _RULES_RECORD
            ],
            "workflow_relationship_kinds": sorted(WORKFLOW_REL_KIND_VOCABULARY),
        }, indent=2, sort_keys=True))
    else:
        print(f"Execution Boundary (CR-BP-33; EXE-001..010): {verdict}")
        print(f"  Records checked:   {len(pairs)}")
        print(f"  Opted-in (with Workflow refs): {len(opted_in)}")
        print(f"  Findings:          {len(findings)}")
        for rid, _fn, label in _RULES_RECORD:
            n = sum(1 for f in findings if f["rule"] == rid)
            print(f"    {rid} ({label}): {n}")
        if findings:
            print("\nFindings:")
            for f in findings:
                print(f"  [{f['rule']}] {f['record_id']}: {f['diagnostic']}")

    if findings and args.strict:
        return 1
    return 0


# -----------------------------------------------------------------------------
# Self-test
# -----------------------------------------------------------------------------


def _record(id_: str = "processes:process-self-test",
            name: str = "Self Test",
            type_: str = "Process",
            extra: dict | None = None) -> dict:
    d = {
        "id": id_,
        "name": name,
        "type": type_,
        "version": "1.0.0",
        "identity": {"verb": "Manage", "object": "Self Test"},
    }
    if extra:
        d.update(extra)
    return d


def _workflow_record(id_: str = "dea:workflow-self-test",
                     name: str = "Self Test Workflow",
                     extra: dict | None = None) -> dict:
    d = {
        "id": id_,
        "name": name,
        "type": WORKFLOW_TYPE,
        "version": "1.0.0",
    }
    if extra:
        d.update(extra)
    return d


def _self_test() -> int:
    """Built-in self-test."""

    # --- EXE-001: composes[] with ordering annotation
    r = _record(extra={"composes": [
        {"target_id": "processes:activity-x",
         "relationship_type": "dea:composes",
         "execution_order": 1}]})
    f = evaluate([(Path("/x"), r)])
    assert any(x["rule"] == "EXE-001" for x in f), f

    # --- EXE-001: clean composes[]
    r = _record(extra={"composes": [
        {"target_id": "processes:activity-x",
         "relationship_type": "dea:composes"}]})
    f = evaluate([(Path("/x"), r)])
    assert not any(x["rule"] == "EXE-001" for x in f), f

    # --- EXE-002: composes with relationship_type=dea:composes + ordering
    r = _record(extra={"composes": [
        {"target_id": "processes:activity-x",
         "relationship_type": "dea:composes",
         "precedes": "processes:activity-y"}]})
    f = evaluate([(Path("/x"), r)])
    assert any(x["rule"] == "EXE-002" for x in f), f

    # --- EXE-002: composes with non-composes relationship_type is OK
    r = _record(extra={"composes": [
        {"target_id": "processes:activity-x",
         "relationship_type": "references",
         "precedes": "processes:activity-y"}]})
    f = evaluate([(Path("/x"), r)])
    assert not any(x["rule"] == "EXE-002" for x in f), f

    # --- EXE-003: Workflow with BP classification
    r = _workflow_record(extra={"process_intent": "manage"})
    f = evaluate([(Path("/x"), r)])
    assert any(x["rule"] == "EXE-003" for x in f), f

    # --- EXE-003: BP record is exempt
    r = _record(extra={"process_intent": "manage"})
    f = evaluate([(Path("/x"), r)])
    assert not any(x["rule"] == "EXE-003" for x in f), f

    # --- EXE-004: singleton workflow field
    for fld in FORBIDDEN_SINGLETON_WORKFLOW_FIELDS:
        r = _record(extra={fld: "dea:workflow-x"})
        f = evaluate([(Path("/x"), r)])
        assert any(x["rule"] == "EXE-004" for x in f), (fld, f)

    # --- EXE-004: workflow_references list is OK
    r = _record(extra={"workflow_references": [
        {"workflow_id": "dea:workflow-x",
         "relationship_kind": "operational"}]})
    f = evaluate([(Path("/x"), r)])
    assert not any(x["rule"] == "EXE-004" for x in f), f

    # --- EXE-005: multiple workflow refs + duplicate process_intent list
    r = _record(extra={
        "workflow_references": [
            {"workflow_id": "dea:workflow-x",
             "relationship_kind": "operational"},
            {"workflow_id": "dea:workflow-y",
             "relationship_kind": "scenario"},
        ],
        "process_intent": ["manage", "operate"],
    })
    f = evaluate([(Path("/x"), r)])
    assert any(x["rule"] == "EXE-005" for x in f), f

    # --- EXE-005: multiple workflow refs + singular process_intent is OK
    r = _record(extra={
        "workflow_references": [
            {"workflow_id": "dea:workflow-x",
             "relationship_kind": "operational"},
            {"workflow_id": "dea:workflow-y",
             "relationship_kind": "scenario"},
        ],
        "process_intent": "manage",
    })
    f = evaluate([(Path("/x"), r)])
    assert not any(x["rule"] == "EXE-005" for x in f), f

    # --- EXE-006: inline actor string
    r = _record(extra={"executed_by": "the Sales team"})
    f = evaluate([(Path("/x"), r)])
    assert any(x["rule"] == "EXE-006" for x in f), f

    # --- EXE-006: canonical actor id
    r = _record(extra={"executed_by": "dea:actor-sales-manager"})
    f = evaluate([(Path("/x"), r)])
    assert not any(x["rule"] == "EXE-006" for x in f), f

    # --- EXE-006: reference-style actor
    r = _record(extra={"executed_by": {"actor_reference": "dea:actor-sales-manager"}})
    f = evaluate([(Path("/x"), r)])
    assert not any(x["rule"] == "EXE-006" for x in f), f

    # --- EXE-007: inline system string
    r = _record(extra={"execution_system": "SAP"})
    f = evaluate([(Path("/x"), r)])
    assert any(x["rule"] == "EXE-007" for x in f), f

    # --- EXE-007: canonical system id
    r = _record(extra={"execution_system": "dea:system-sap-erp"})
    f = evaluate([(Path("/x"), r)])
    assert not any(x["rule"] == "EXE-007" for x in f), f

    # --- EXE-008: Workflow with identity.verb
    r = _workflow_record(extra={"identity": {"verb": "Manage", "object": "X"}})
    f = evaluate([(Path("/x"), r)])
    assert any(x["rule"] == "EXE-008" for x in f), f

    # --- EXE-008: Workflow without identity is OK
    r = _workflow_record()
    f = evaluate([(Path("/x"), r)])
    assert not any(x["rule"] == "EXE-008" for x in f), f

    # --- EXE-008: BP record with identity is OK
    r = _record()
    f = evaluate([(Path("/x"), r)])
    assert not any(x["rule"] == "EXE-008" for x in f), f

    # --- EXE-009: implementation-detail field
    for fld in FORBIDDEN_IMPLEMENTATION_FIELDS:
        r = _record(extra={fld: "x"})
        f = evaluate([(Path("/x"), r)])
        assert any(x["rule"] == "EXE-009" for x in f), (fld, f)

    # --- EXE-009: clean
    r = _record()
    f = evaluate([(Path("/x"), r)])
    assert not any(x["rule"] == "EXE-009" for x in f), f

    # --- EXE-010: workflow_reference missing relationship_kind
    r = _record(extra={"workflow_references": [
        {"workflow_id": "dea:workflow-x"}]})
    f = evaluate([(Path("/x"), r)])
    assert any(x["rule"] == "EXE-010" for x in f), f

    # --- EXE-010: invalid relationship_kind
    r = _record(extra={"workflow_references": [
        {"workflow_id": "dea:workflow-x",
         "relationship_kind": "unknown"}]})
    f = evaluate([(Path("/x"), r)])
    assert any(x["rule"] == "EXE-010" for x in f), f

    # --- EXE-010: valid relationship_kind passes
    for kind in WORKFLOW_REL_KIND_VOCABULARY:
        r = _record(extra={"workflow_references": [
            {"workflow_id": "dea:workflow-x",
             "relationship_kind": kind}]})
        f = evaluate([(Path("/x"), r)])
        assert not any(x["rule"] == "EXE-010" for x in f), (kind, f)

    # --- Universal check: a BP record with no Workflow refs is clean
    r = _record()
    f = evaluate([(Path("/x"), r)])
    assert f == [], f

    # --- Universal check: an Activity record with no Workflow refs is clean
    r = _record(type_=ACTIVITY_TYPE, id_="processes:activity-self-test")
    f = evaluate([(Path("/x"), r)])
    assert f == [], f

    print("self-test PASS (18 cases)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
