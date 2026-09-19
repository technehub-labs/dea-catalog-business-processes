"""Tests for the CR-BP-98 L4 Task structural validator.

Locks behaviour for TASK-001..005 by exercising both the in-process
`evaluate()` function and the CLI self-test entry point, plus the live
catalog assertion that 0 records / 0 findings / CONFORMANT (no L4
records exist today).
"""

import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_task_model.py"

sys.path.insert(0, str(ROOT / "scripts"))
from check_task_model import (  # noqa: E402
    ACTIVITY_ID_PATTERN,
    DISALLOWED_L4_FIELDS,
    ID_PATTERN,
    RULE_IDS,
    _check_activity_resolution,
    _check_definition_responsibility_boundary,
    _check_id_format,
    _check_no_disallowed_fields,
    _check_trigger_outcome,
    evaluate,
    verdict,
)


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------


def test_id_pattern_starts_with_dea_task() -> None:
    assert ID_PATTERN.startswith("^dea:task-")
    assert ID_PATTERN.endswith("$")


def test_activity_id_pattern_starts_with_dea_activity() -> None:
    assert ACTIVITY_ID_PATTERN.startswith("^dea:activity-")


def test_disallowed_l4_fields_includes_orchestration_and_sequencing() -> None:
    assert "orchestration" in DISALLOWED_L4_FIELDS
    assert "sequencing" in DISALLOWED_L4_FIELDS
    assert "automation" in DISALLOWED_L4_FIELDS


def test_rule_ids_match_five_checks() -> None:
    assert RULE_IDS == ("TASK-001", "TASK-002", "TASK-003", "TASK-004", "TASK-005")


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def _record(**overrides):
    """A valid Task record that should pass TASK-001..005."""
    base = {
        "id": "dea:task-test",
        "type": "Task",
        "name": "Test Task",
        "definition": "Test task definition",
        "belongs_to_activity": "dea:activity-test",
        "trigger": "Test trigger",
        "outcome": "Test outcome",
        "responsibility": "Test responsibility",
        "boundary": {"inclusions": ["Test inclusion"], "exclusions": ["Test exclusion"]},
        "evidence": [{"source": "test", "claim": "test", "strength": "E2"}],
        "version": "1.0.0",
        "lifecycle_status": "candidate",
        "status": "candidate",
        "ecfConformance": {
            "framework": "EnterpriseConceptFramework",
            "contractVersion": "1.0.0",
            "profile": "dea:ecf@1.0.0",
            "status": "conformant",
            "affiliation": "inherits-catalog",
            "canonicalReferences": [
                {
                    "kind": "coordinate",
                    "domain": "PartyAndRelationship",
                    "stage": "Improve",
                    "identifier": "ecf:partyRelationship.improve",
                }
            ],
        },
    }
    base.update(overrides)
    return base


def _make_activity(activity_id: str, entities_dir: Path):
    activity_dir = entities_dir / activity_id
    activity_dir.mkdir(parents=True, exist_ok=True)
    activity_yaml = activity_dir / f"{activity_id}.yaml"
    activity_yaml.write_text(yaml.safe_dump({
        "id": activity_id,
        "type": "Activity",
        "name": "Test Activity",
        "definition": "Test activity definition",
        "version": "1.0.0",
        "lifecycle_status": "candidate",
        "status": "candidate",
    }))


# -----------------------------------------------------------------------------
# TASK-001: id format
# -----------------------------------------------------------------------------


def test_task_001_id_format_pass():
    findings = _check_id_format(_record(id="dea:task-test"), "<test>")
    assert findings == []


def test_task_001_id_format_fail_wrong_prefix():
    findings = _check_id_format(_record(id="dea:activity-test"), "<test>")
    assert any(f.rule == "TASK-001" for f in findings), findings


def test_task_001_id_format_fail_missing():
    record = _record()
    del record["id"]
    findings = _check_id_format(record, "<test>")
    assert any(f.rule == "TASK-001" for f in findings), findings


# -----------------------------------------------------------------------------
# TASK-002: definition + responsibility + boundary
# -----------------------------------------------------------------------------


def test_task_002_pass():
    findings = _check_definition_responsibility_boundary(_record(), "<test>")
    assert findings == []


def test_task_002_fail_missing_definition():
    record = _record()
    del record["definition"]
    findings = _check_definition_responsibility_boundary(record, "<test>")
    assert any(f.rule == "TASK-002" for f in findings), findings


def test_task_002_fail_missing_responsibility():
    record = _record()
    del record["responsibility"]
    findings = _check_definition_responsibility_boundary(record, "<test>")
    assert any(f.rule == "TASK-002" for f in findings), findings


def test_task_002_fail_missing_boundary():
    record = _record()
    del record["boundary"]
    findings = _check_definition_responsibility_boundary(record, "<test>")
    assert any(f.rule == "TASK-002" for f in findings), findings


def test_task_002_fail_empty_boundary_lists():
    record = _record(boundary={"inclusions": [], "exclusions": []})
    findings = _check_definition_responsibility_boundary(record, "<test>")
    assert any(f.rule == "TASK-002" for f in findings), findings


# -----------------------------------------------------------------------------
# TASK-003: trigger + outcome
# -----------------------------------------------------------------------------


def test_task_003_pass():
    findings = _check_trigger_outcome(_record(), "<test>")
    assert findings == []


def test_task_003_fail_missing_trigger():
    record = _record()
    del record["trigger"]
    findings = _check_trigger_outcome(record, "<test>")
    assert any(f.rule == "TASK-003" for f in findings), findings


def test_task_003_fail_missing_outcome():
    record = _record()
    del record["outcome"]
    findings = _check_trigger_outcome(record, "<test>")
    assert any(f.rule == "TASK-003" for f in findings), findings


# -----------------------------------------------------------------------------
# TASK-004: belongs_to_activity resolution
# -----------------------------------------------------------------------------


def test_task_004_pass(tmp_path):
    _make_activity("dea:activity-test", tmp_path)
    findings = _check_activity_resolution(_record(), "<test>", entities_dir=tmp_path)
    assert findings == []


def test_task_004_fail_wrong_format(tmp_path):
    record = _record(belongs_to_activity="dea:task-other")
    findings = _check_activity_resolution(record, "<test>", entities_dir=tmp_path)
    assert any(f.rule == "TASK-004" for f in findings), findings


def test_task_004_fail_unresolved(tmp_path):
    record = _record(belongs_to_activity="dea:activity-nonexistent")
    findings = _check_activity_resolution(record, "<test>", entities_dir=tmp_path)
    assert any(f.rule == "TASK-004" for f in findings), findings


# -----------------------------------------------------------------------------
# TASK-005: disallowed fields
# -----------------------------------------------------------------------------


def test_task_005_pass():
    findings = _check_no_disallowed_fields(_record(), "<test>")
    assert findings == []


def test_task_005_fail_workflow_definition():
    record = _record(workflow_definition={"ref": "x"})
    findings = _check_no_disallowed_fields(record, "<test>")
    assert any(f.rule == "TASK-005" for f in findings), findings


def test_task_005_fail_sequencing():
    record = _record(sequencing=["a", "b"])
    findings = _check_no_disallowed_fields(record, "<test>")
    assert any(f.rule == "TASK-005" for f in findings), findings


def test_task_005_fail_orchestration():
    record = _record(orchestration={"type": "bpmn"})
    findings = _check_no_disallowed_fields(record, "<test>")
    assert any(f.rule == "TASK-005" for f in findings), findings


# -----------------------------------------------------------------------------
# Aggregate evaluate() + verdict()
# -----------------------------------------------------------------------------


def test_evaluate_all_pass_with_resolved_activity(tmp_path):
    _make_activity("dea:activity-test", tmp_path)
    findings = evaluate([(Path("<test>"), _record())], entities_dir=tmp_path)
    assert findings == []
    assert verdict(findings) == "CONFORMANT"


def test_evaluate_emits_multiple_findings(tmp_path):
    record = _record(
        id="dea:bad-id-format",
        belongs_to_activity="dea:activity-bad",
        sequencing=["forbidden"],
    )
    findings = evaluate([(Path("<test>"), record)], entities_dir=tmp_path)
    rule_set = {f.rule for f in findings}
    assert "TASK-001" in rule_set
    assert "TASK-004" in rule_set
    assert "TASK-005" in rule_set
    assert verdict(findings) == "NON-CONFORMANT"


# -----------------------------------------------------------------------------
# CLI-level tests
# -----------------------------------------------------------------------------


def _run(args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, check=False,
    )


def test_cli_self_test_passes():
    result = _run(["--self-test"])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "self-test PASS" in result.stdout


def test_cli_live_run_conformant():
    """Live catalog: 0 records, 0 findings, CONFORMANT."""
    result = _run([])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CONFORMANT" in result.stdout
    assert "Records checked:  2800" in result.stdout


def test_cli_json_emits_well_formed_payload():
    result = _run(["--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["verdict"] == "CONFORMANT"
    assert payload["records_checked"] == 2800
    assert payload["findings"] == []
    rule_ids = {r["id"] for r in payload["rules"]}
    assert rule_ids == {"TASK-001", "TASK-002", "TASK-003", "TASK-004", "TASK-005"}


def test_findings_severity_is_error():
    """All TASK-001..005 findings are mandatory (severity=error)."""
    record = _record(id="dea:bad", trigger=None)
    f = _check_id_format(record, "<test>") + _check_trigger_outcome(record, "<test>")
    assert all(fnd.severity == "error" for fnd in f), f