"""Tests for the CR-BP-32 Activity Model validator.

Locks behaviour for ACT-001..010 by exercising both the in-process
`evaluate()` function and the CLI self-test entry point, plus a
live-catalog assertion that the catalog currently emits zero
findings (no Activity records exist yet; 126 BP records are
intentionally never inspected per CR-BP-32 §17).

The tests cover:

* ACT-001  parent-BP reference present + matches `dea:process-*`
* ACT-002  Activity is not promoted to BusinessProcess via auxiliary
           fields (`kind`, `process_kind`, `promoted_to`)
* ACT-003  cohesion rationale present + ≥ 20 chars
* ACT-004  Activity has `composes[]` with a `dea:task-*` target OR
           `decomposition_boundary: l4-reached`
* ACT-005  composition entries use `dea:composes` (forbidden
           alternatives: `parent_activity`, `child_activities`,
           `decomposes`, `contains_activity`)
* ACT-006  no execution-ordering fields on the record or in metadata
* ACT-007  Activity id ≠ `dea:function-*`
* ACT-008  no implementation-detail marker fields
* ACT-009  no execution-model fields (CR-BP-33 owns execution)
* ACT-010  bidirectional traceability (parent BP declares the
           Activity in `metadata.activity_references[]` or
           `composes[]`)

The BP records in the live catalog are NEVER inspected; the
validator filters on `type: Activity` and skips everything else.
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
SCRIPT = ROOT / "scripts" / "check_activity_model.py"

sys.path.insert(0, str(ROOT / "scripts"))
from check_activity_model import (  # noqa: E402
    ACTIVITY_TYPE,
    CANONICAL_COMPOSITION_TYPE,
    FORBIDDEN_COMPOSITION_TYPES,
    FORBIDDEN_EXECUTION_FIELDS,
    FORBIDDEN_EXECUTION_MODEL_FIELDS,
    FORBIDDEN_IMPLEMENTATION_FIELDS,
    _check_act_001,
    _check_act_002,
    _check_act_003,
    _check_act_004,
    _check_act_005,
    _check_act_006,
    _check_act_007,
    _check_act_008,
    _check_act_009,
    _build_parent_index,
    _is_activity,
    _load_records,
    evaluate,
)


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def _record(id_="dea:activity-self-test",
            name="Self Test Activity",
            belongs_to="dea:process-manage-customer-relationship",
            cohesion=("This activity groups the cohesive logical work of "
                      "validating customer eligibility prior to fulfilment. "
                      "The grouping is justified by the single outcome: a "
                      "decision to proceed or hold."),
            composes: list | None = None,
            boundary=None,
            extra=None):
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
    """Live run: 537 Activity records (5 CR-BP-42 + 32 CR-BP-43 + 8 CR-BP-44 + 28 CR-BP-45 + 36 CR-BP-46 + 40 CR-BP-47 + 32 CR-BP-48 + 28 CR-BP-49 + 40 CR-BP-50 + 24 CR-BP-51 + 36 CR-BP-52 + 44 CR-BP-53 + 48 CR-BP-54 + 28 CR-BP-55 + 36 CR-BP-56 + 36 CR-BP-57 + 20 CR-BP-69 + 12 CR-BP-77 + 4 CR-BP-79), 138 BP records (126 + 2 CR-BP-64 + 1 CR-BP-65 + 1 CR-BP-66 + 1 CR-BP-67 + 1 CR-BP-71 + 1 CR-BP-73 + 1 CR-BP-75 + 1 CR-BP-78 + 1 CR-BP-81 + 1 CR-BP-82 + 1 CR-BP-83 + 1 CR-BP-86 admissions), 0 findings."""
    result = _run([])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Activity Model (CR-BP-32; ACT-001..010): CONFORMANT" in result.stdout
    assert "Activity records: 537" in result.stdout
    assert "BP records:       139" in result.stdout
    assert "Findings:         0" in result.stdout


def test_cli_strict_mode_treats_findings_as_failure(tmp_path, monkeypatch):
    """--strict exits 1 only when findings exist."""
    # Construct an Activity fixture that violates ACT-003.
    activity_dir = tmp_path / "dea:activity-bad"
    activity_dir.mkdir()
    activity_yaml = activity_dir / "dea:activity-bad.yaml"
    activity_yaml.write_text(yaml.safe_dump(_record(
        id_="dea:activity-bad",
        cohesion="",  # ACT-003 violation
        boundary=None,
    )))
    # Mirror the v1-alpha/ structure expected by _load_records
    v1 = tmp_path / "entities" / "v1-alpha"
    v1.mkdir(parents=True)
    target = v1 / "dea:activity-bad"
    target.mkdir()
    (target / "dea:activity-bad.yaml").write_text(
        activity_yaml.read_text()
    )
    # Run with --strict against the temp catalog; expect non-zero exit
    result = subprocess.run(
        [sys.executable, str(SCRIPT),
         "--catalog-root", str(tmp_path), "--strict"],
        check=False, capture_output=True, text=True,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert "NON-CONFORMANT" in result.stdout
    assert "ACT-003" in result.stdout


def test_cli_json_shape():
    result = _run(["--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert data["verdict"] == "CONFORMANT"
    assert data["activity_record_count"] == 537
    assert data["bp_record_count"] == 139
    assert data["finding_count"] == 0
    assert data["canonical_composition_type"] == CANONICAL_COMPOSITION_TYPE
    assert sorted(data["forbidden_composition_types"]) == sorted(FORBIDDEN_COMPOSITION_TYPES)
    rule_ids = {r["id"] for r in data["rules"]}
    assert "ACT-001" in rule_ids
    assert "ACT-009" in rule_ids
    assert "ACT-010" in {r["id"] for r in data["rules"]}


# -----------------------------------------------------------------------------
# Rule-level tests
# -----------------------------------------------------------------------------


def test_act_001_missing_belongs_to():
    r = _record(belongs_to="")
    diag = _check_act_001(r)
    assert diag is not None and "belongs_to_business_process" in diag


def test_act_001_bad_pattern():
    r = _record(belongs_to="dea:function-foo")
    diag = _check_act_001(r)
    assert diag is not None and "dea:process-*" in diag


def test_act_001_pass():
    assert _check_act_001(_record()) is None


def test_act_002_promotion_attempt():
    for aux in ("kind", "process_kind", "promoted_to"):
        r = _record(extra={aux: "BusinessProcess"})
        assert _check_act_002(r) is not None, aux


def test_act_002_pass():
    assert _check_act_002(_record()) is None


def test_act_003_missing():
    r = _record(cohesion="")
    assert _check_act_003(r) is not None


def test_act_003_too_short():
    r = _record(cohesion="short")
    assert _check_act_003(r) is not None


def test_act_003_pass():
    assert _check_act_003(_record()) is None


def test_act_004_no_composes_no_boundary():
    r = _record(composes=[], boundary=None)
    assert _check_act_004(r) is not None


def test_act_004_composes_without_task_target():
    r = _record(composes=[{
        "target_id": "dea:group-foo",
        "relationship_type": CANONICAL_COMPOSITION_TYPE,
    }])
    assert _check_act_004(r) is not None


def test_act_004_composes_with_task_target():
    r = _record(composes=[{
        "target_id": "dea:task-validate-eligibility",
        "relationship_type": CANONICAL_COMPOSITION_TYPE,
    }])
    assert _check_act_004(r) is None


def test_act_004_boundary_marker_passes():
    for marker in ("l4-reached", "L4", "atomic", "no-further-decomposition"):
        r = _record(composes=[], boundary=marker)
        assert _check_act_004(r) is None, marker


def test_act_005_forbidden_relationship_type():
    for bad in FORBIDDEN_COMPOSITION_TYPES:
        r = _record(composes=[{
            "target_id": "dea:task-x",
            "relationship_type": bad,
        }])
        assert _check_act_005(r) is not None, bad


def test_act_005_non_canonical_relationship_type():
    r = _record(composes=[{
        "target_id": "dea:task-x",
        "relationship_type": "contains",
    }])
    assert _check_act_005(r) is not None


def test_act_005_canonical_passes():
    r = _record(composes=[{
        "target_id": "dea:task-x",
        "relationship_type": CANONICAL_COMPOSITION_TYPE,
    }])
    assert _check_act_005(r) is None


def test_act_006_top_level_execution_fields():
    for fld in FORBIDDEN_EXECUTION_FIELDS:
        r = _record(extra={fld: 1})
        assert _check_act_006(r) is not None, fld


def test_act_006_metadata_execution_fields():
    r = _record(extra={"metadata": {"execution_order": 1}})
    assert _check_act_006(r) is not None


def test_act_006_clean():
    assert _check_act_006(_record()) is None


def test_act_007_function_id():
    r = _record(id_="dea:function-something")
    assert _check_act_007(r) is not None


def test_act_007_clean():
    assert _check_act_007(_record()) is None


def test_act_008_implementation_detail_fields():
    for fld in FORBIDDEN_IMPLEMENTATION_FIELDS:
        r = _record(extra={fld: "x"})
        assert _check_act_008(r) is not None, fld


def test_act_008_clean():
    assert _check_act_008(_record()) is None


def test_act_009_execution_model_fields():
    for fld in FORBIDDEN_EXECUTION_MODEL_FIELDS:
        r = _record(extra={fld: "x"})
        assert _check_act_009(r) is not None, fld


def test_act_009_clean():
    assert _check_act_009(_record()) is None


def test_act_010_reverse_traceability_missing():
    """Parent BP on disk but does not reference the Activity."""
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        bp_id = "dea:process-test-bp"
        bp_yaml = td_path / "bp.yaml"
        bp_yaml.write_text(yaml.safe_dump({
            "id": bp_id,
            "name": "Test BP",
            "type": "Process",
            "version": "1.0.0",
        }))
        idx = _build_parent_index_for(td_path)
        # idx may or may not find the BP depending on layout;
        # the test below uses direct injection via evaluate().
        r = _record(belongs_to=bp_id, id_="dea:activity-orphan")
        f = evaluate([(td_path / "dea:activity-orphan.yaml", r)],
                     parent_index={bp_id: bp_yaml})
        assert any(x["rule"] == "ACT-010" for x in f)


def test_act_010_reverse_traceability_present():
    """Parent BP declares the Activity in metadata.activity_references[]."""
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        bp_id = "dea:process-test-bp"
        bp_yaml = td_path / "bp.yaml"
        bp_yaml.write_text(yaml.safe_dump({
            "id": bp_id,
            "name": "Test BP",
            "type": "Process",
            "version": "1.0.0",
            "metadata": {"activity_references": ["dea:activity-tracked"]},
        }))
        r = _record(belongs_to=bp_id, id_="dea:activity-tracked")
        f = evaluate([(td_path / "dea:activity-tracked.yaml", r)],
                     parent_index={bp_id: bp_yaml})
        assert not any(x["rule"] == "ACT-010" for x in f)


def test_act_010_parent_bp_absent_degrades_to_forward():
    """Parent BP not on disk → ACT-010 forward-only check."""
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        r = _record(belongs_to="dea:process-nonexistent",
                    id_="dea:activity-solo")
        f = evaluate([(td_path / "dea:activity-solo.yaml", r)],
                     parent_index={})
        assert not any(x["rule"] == "ACT-010" for x in f)


# -----------------------------------------------------------------------------
# Type filter — BP records are NEVER inspected
# -----------------------------------------------------------------------------


def test_bp_records_are_never_inspected():
    """A Process record with deliberately-bad Activity fields stays clean."""
    bp = {
        "id": "dea:process-foo",
        "name": "Foo",
        "type": "Process",
        "version": "1.0.0",
        # Even deliberately-bad Activity-style fields are ignored.
        "execution_order": 1,
        "workflow": "bpmn:process_foo",
        "script_ref": "x.py",
    }
    assert evaluate([(Path("/x"), bp)]) == []


def test_is_activity_discriminator():
    assert _is_activity({"type": ACTIVITY_TYPE}) is True
    assert _is_activity({"type": "Process"}) is False
    assert _is_activity({}) is False


def test_load_records_empty_when_no_activity_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "entities" / "v1-alpha").mkdir(parents=True)
    assert _load_records(tmp_path) == []


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def _build_parent_index_for(catalog_root: Path) -> dict[str, Path]:
    return _build_parent_index(catalog_root)
