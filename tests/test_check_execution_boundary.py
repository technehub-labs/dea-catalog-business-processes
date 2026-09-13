"""Tests for the CR-BP-33 Execution Boundary validator.

Locks behaviour for EXE-001..010 by exercising both the in-process
`evaluate()` function and the CLI self-test entry point, plus a
live-catalog assertion that all 161 records currently emit zero
findings (no records carry Workflow references or execution-bearing
fields; the validator is a forward-looking regression guard).

The tests cover:

* EXE-001  composes[] entries carry no execution-ordering annotations
* EXE-002  dea:composes entries carry no execution-ordering annotations
* EXE-003  Workflow records carry no BP classification fields
* EXE-004  singleton workflow fields are rejected (list required)
* EXE-005  multiple workflow refs do not split the BP (singular
           process_intent / process_type axes)
* EXE-006  execution actors are canonical `dea:actor-*` references
* EXE-007  execution systems are canonical `dea:system-*` references
* EXE-008  Workflow records carry no identity.verb / identity.object
* EXE-009  no implementation-detail fields on any record
* EXE-010  workflow_references[] entries declare relationship_kind
           from the controlled vocabulary (reference / operational /
           scenario / implementation)
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_execution_boundary.py"

sys.path.insert(0, str(ROOT / "scripts"))
from check_execution_boundary import (  # noqa: E402
    BP_CLASSIFICATION_FIELDS,
    FORBIDDEN_COMPOSITION_ORDERING_FIELDS,
    FORBIDDEN_IMPLEMENTATION_FIELDS,
    FORBIDDEN_SINGLETON_WORKFLOW_FIELDS,
    WORKFLOW_REL_KIND_VOCABULARY,
    WORKFLOW_TYPE,
    _check_exe_001,
    _check_exe_002,
    _check_exe_003,
    _check_exe_004,
    _check_exe_005,
    _check_exe_006,
    _check_exe_007,
    _check_exe_008,
    _check_exe_009,
    _check_exe_010,
    evaluate,
)


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def _record(id_="dea:process-self-test",
            name="Self Test",
            type_="Process",
            extra=None):
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


def _workflow_record(id_="dea:workflow-self-test",
                     name="Self Test Workflow",
                     extra=None):
    d = {
        "id": id_,
        "name": name,
        "type": WORKFLOW_TYPE,
        "version": "1.0.0",
    }
    if extra:
        d.update(extra)
    return d


# -----------------------------------------------------------------------------
# CLI-level tests
# -----------------------------------------------------------------------------


def test_cli_self_test_passes():
    result = _run(["--self-test"])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "self-test PASS" in result.stdout


def test_cli_live_run_returns_conformant():
    """Live run: 470 records (161 pre-CR-BP-42 + 309 Activity records from CR-BP-42..52), 0 opted-in, 0 findings."""
    result = _run([])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Execution Boundary (CR-BP-33; EXE-001..010): CONFORMANT" in result.stdout
    assert "Records checked:   470" in result.stdout
    assert "Opted-in (with Workflow refs): 0" in result.stdout
    assert "Findings:          0" in result.stdout


def test_cli_json_shape():
    result = _run(["--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert data["verdict"] == "CONFORMANT"
    assert data["record_count"] == 470
    assert data["opted_in_record_count"] == 0
    assert data["finding_count"] == 0
    rule_ids = {r["id"] for r in data["rules"]}
    assert "EXE-001" in rule_ids
    assert "EXE-010" in rule_ids
    assert set(data["workflow_relationship_kinds"]) == WORKFLOW_REL_KIND_VOCABULARY


def test_cli_strict_mode_fails_on_findings(tmp_path):
    """--strict exits 1 when a record carries an execution leak."""
    v1 = tmp_path / "entities" / "v1-alpha"
    v1.mkdir(parents=True)
    bad_dir = v1 / "dea:process-bad"
    bad_dir.mkdir()
    bad_yaml = bad_dir / "dea:process-bad.yaml"
    bad_yaml.write_text(yaml.safe_dump(_record(
        id_="dea:process-bad",
        extra={"executed_by": "the Sales team"},  # EXE-006 violation
    )))
    result = subprocess.run(
        [sys.executable, str(SCRIPT),
         "--catalog-root", str(tmp_path), "--strict"],
        check=False, capture_output=True, text=True,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert "NON-CONFORMANT" in result.stdout
    assert "EXE-006" in result.stdout


# -----------------------------------------------------------------------------
# Rule-level tests
# -----------------------------------------------------------------------------


def test_exe_001_forbids_ordering_annotations():
    for fld in FORBIDDEN_COMPOSITION_ORDERING_FIELDS:
        r = _record(extra={"composes": [
            {"target_id": "dea:activity-x",
             "relationship_type": "dea:composes",
             fld: 1}]})
        assert _check_exe_001(r) is not None, fld


def test_exe_001_clean_composes():
    r = _record(extra={"composes": [
        {"target_id": "dea:activity-x",
         "relationship_type": "dea:composes"}]})
    assert _check_exe_001(r) is None


def test_exe_002_forbids_ordering_on_composes_relationship():
    r = _record(extra={"composes": [
        {"target_id": "dea:activity-x",
         "relationship_type": "dea:composes",
         "precedes": "dea:activity-y"}]})
    assert _check_exe_002(r) is not None


def test_exe_002_non_composes_relationship_is_exempt():
    r = _record(extra={"composes": [
        {"target_id": "dea:activity-x",
         "relationship_type": "references",
         "precedes": "dea:activity-y"}]})
    assert _check_exe_002(r) is None


def test_exe_003_forbids_bp_classification_on_workflow():
    for fld in BP_CLASSIFICATION_FIELDS:
        r = _workflow_record(extra={fld: "manage"})
        assert _check_exe_003(r) is not None, fld


def test_exe_003_bp_record_is_exempt():
    r = _record(extra={"process_intent": "manage"})
    assert _check_exe_003(r) is None


def test_exe_004_forbids_singleton_workflow_field():
    for fld in FORBIDDEN_SINGLETON_WORKFLOW_FIELDS:
        r = _record(extra={fld: "dea:workflow-x"})
        assert _check_exe_004(r) is not None, fld


def test_exe_004_workflow_references_list_is_accepted():
    r = _record(extra={"workflow_references": [
        {"workflow_id": "dea:workflow-x",
         "relationship_kind": "operational"}]})
    assert _check_exe_004(r) is None


def test_exe_005_multiple_workflows_with_duplicate_intent_list_fails():
    r = _record(extra={
        "workflow_references": [
            {"workflow_id": "dea:workflow-x", "relationship_kind": "operational"},
            {"workflow_id": "dea:workflow-y", "relationship_kind": "scenario"},
        ],
        "process_intent": ["manage", "operate"],
    })
    assert _check_exe_005(r) is not None


def test_exe_005_multiple_workflows_with_singular_intent_passes():
    r = _record(extra={
        "workflow_references": [
            {"workflow_id": "dea:workflow-x", "relationship_kind": "operational"},
            {"workflow_id": "dea:workflow-y", "relationship_kind": "scenario"},
        ],
        "process_intent": "manage",
    })
    assert _check_exe_005(r) is None


def test_exe_005_single_workflow_is_exempt():
    r = _record(extra={
        "workflow_references": [
            {"workflow_id": "dea:workflow-x", "relationship_kind": "operational"},
        ],
        "process_intent": ["manage", "operate"],
    })
    assert _check_exe_005(r) is None


def test_exe_006_inline_actor_string_fails():
    for bad in ("the Sales team", "a manager", "Finance", "operations dept"):
        r = _record(extra={"executed_by": bad})
        assert _check_exe_006(r) is not None, bad


def test_exe_006_canonical_actor_id_passes():
    r = _record(extra={"executed_by": "dea:actor-sales-manager"})
    assert _check_exe_006(r) is None


def test_exe_006_reference_style_actor_passes():
    r = _record(extra={"executed_by": {"actor_reference": "dea:actor-sales-manager"}})
    assert _check_exe_006(r) is None


def test_exe_007_inline_system_string_fails():
    r = _record(extra={"execution_system": "SAP"})
    assert _check_exe_007(r) is not None


def test_exe_007_canonical_system_id_passes():
    r = _record(extra={"execution_system": "dea:system-sap-erp"})
    assert _check_exe_007(r) is None


def test_exe_008_workflow_with_identity_fails():
    r = _workflow_record(extra={"identity": {"verb": "Manage", "object": "X"}})
    assert _check_exe_008(r) is not None


def test_exe_008_workflow_without_identity_passes():
    r = _workflow_record()
    assert _check_exe_008(r) is None


def test_exe_008_bp_record_with_identity_is_exempt():
    r = _record()
    assert _check_exe_008(r) is None


def test_exe_009_forbids_implementation_detail_fields():
    for fld in FORBIDDEN_IMPLEMENTATION_FIELDS:
        r = _record(extra={fld: "x"})
        assert _check_exe_009(r) is not None, fld


def test_exe_009_metadata_implementation_detail_fails():
    r = _record(extra={"metadata": {"api_sequence": ["GET /x", "POST /y"]}})
    assert _check_exe_009(r) is not None


def test_exe_010_missing_relationship_kind_fails():
    r = _record(extra={"workflow_references": [
        {"workflow_id": "dea:workflow-x"}]})
    assert _check_exe_010(r) is not None


def test_exe_010_invalid_relationship_kind_fails():
    r = _record(extra={"workflow_references": [
        {"workflow_id": "dea:workflow-x",
         "relationship_kind": "unknown"}]})
    assert _check_exe_010(r) is not None


def test_exe_010_valid_relationship_kinds_pass():
    for kind in WORKFLOW_REL_KIND_VOCABULARY:
        r = _record(extra={"workflow_references": [
            {"workflow_id": "dea:workflow-x",
             "relationship_kind": kind}]})
        assert _check_exe_010(r) is None, kind


# -----------------------------------------------------------------------------
# Universal / type-agnostic tests
# -----------------------------------------------------------------------------


def test_bp_record_with_no_workflow_references_is_clean():
    r = _record()
    assert evaluate([(Path("/x"), r)]) == []


def test_activity_record_with_no_workflow_references_is_clean():
    r = _record(type_="Activity", id_="dea:activity-self-test")
    assert evaluate([(Path("/x"), r)]) == []


def test_process_group_record_with_no_workflow_references_is_clean():
    r = _record(type_="ProcessGroup", id_="dea:group-self-test")
    assert evaluate([(Path("/x"), r)]) == []


def test_process_context_record_with_no_workflow_references_is_clean():
    r = _record(type_="ProcessContext", id_="dea:pc-self-test")
    assert evaluate([(Path("/x"), r)]) == []
