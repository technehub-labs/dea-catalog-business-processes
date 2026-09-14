"""Tests for the CR-BP-34c Lifecycle State-Machine validator.

Locks behaviour for LCM-001..005 by exercising both the in-process
`evaluate()` function and the CLI self-test entry point, plus a
live-catalog assertion that all 126 canonical Business Process
records satisfy all five rules.

LCM-003 / LCM-004 use case-sensitive marker matching: the
transition-event convention is "DEPRECATED" (uppercase), while
narrative mentions use "lifecycle_status=deprecated" (camelCase).
The case-sensitive match cleanly separates the two.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_lifecycle_state.py"

sys.path.insert(0, str(ROOT / "scripts"))
from check_lifecycle_state import (  # noqa: E402
    APPROVED_LIFECYCLE_STATES,
    LEGACY_COMPATIBILITY_SET,
    _RULES_PATH,
    _RULES_RECORD,
    _has_deprecation_marker,
    _self_test,
    evaluate,
)


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def _path(state: str = "candidate") -> Path:
    """Path helper: retired records go in _retired/; others in v1-alpha/."""
    if state == "retired":
        return Path("/x/_retired/dea:process-self-test/dea:process-self-test.yaml")
    return Path("/x/v1-alpha/dea:process-self-test/dea:process-self-test.yaml")


def _record(status_value="candidate", ls_value="candidate", ch=None):
    """Build a record. Provides a DEPRECATED marker when ls='deprecated'."""
    d = {
        "id": "dea:process-self-test",
        "name": "Self Test",
        "type": "Process",
        "version": "1.0.0",
        "lifecycle_status": ls_value,
        "status": status_value,
    }
    if ch is not None:
        d["metadata"] = {"change_history": ch}
    elif ls_value == "deprecated":
        d["metadata"] = {"change_history": [
            {"cr": "CR-BP-21a", "change": "This entry is now DEPRECATED."}
        ]}
    return d


# -----------------------------------------------------------------------------
# CLI-level tests
# -----------------------------------------------------------------------------


def test_cli_self_test_passes():
    result = _run(["--self-test"])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "self-test PASS" in result.stdout


def test_cli_in_process_self_test():
    rc = _self_test()
    assert rc == 0


def test_cli_live_catalog_conformant():
    result = _run(["--strict"])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CONFORMANT" in result.stdout
    assert "Records checked:  130" in result.stdout
    assert "Findings:         0" in result.stdout


def test_cli_json_emits_well_formed_payload():
    result = _run(["--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["verdict"] == "CONFORMANT"
    assert payload["candidate_count"] == 130
    assert payload["finding_count"] == 0
    rule_ids = {r["id"] for r in payload["rules"]}
    assert rule_ids == {"LCM-001", "LCM-002", "LCM-003", "LCM-004", "LCM-005"}
    assert "candidate" in payload["approved_lifecycle_states"]
    assert "deprecated" in payload["approved_lifecycle_states"]
    assert "retired" in payload["approved_lifecycle_states"]
    assert payload["legacy_compatibility_set"] == ["candidate"]


# -----------------------------------------------------------------------------
# LCM-001 (vocabulary)
# -----------------------------------------------------------------------------


def test_lcm_001_all_approved_values_pass():
    """Every approved state, with a sensible path, must pass."""
    for state in sorted(APPROVED_LIFECYCLE_STATES):
        ch = ([{"change": "This entry is now DEPRECATED."}]
              if state == "deprecated" else None)
        findings = evaluate([(_path(state), _record(
            status_value=state, ls_value=state, ch=ch
        ))])
        assert findings == [], (state, findings)


def test_lcm_001_unknown_value_fires():
    f = evaluate([(_path(), _record(ls_value="Draft-Proposed",
                                     status_value="Draft-Proposed"))])
    assert len(f) == 1 and f[0]["rule"] == "LCM-001"


def test_lcm_001_missing_lifecycle_status_fires():
    r = _record()
    r.pop("lifecycle_status")
    f = evaluate([(_path(), r)])
    assert any(x["rule"] == "LCM-001" for x in f)


def test_lcm_001_non_string_value_fires():
    r = _record()
    r["lifecycle_status"] = 42
    f = evaluate([(_path(), r)])
    assert any(x["rule"] == "LCM-001" for x in f)


# -----------------------------------------------------------------------------
# LCM-002 (status ↔ lifecycle_status)
# -----------------------------------------------------------------------------


def test_lcm_002_identical_values_pass():
    assert evaluate([(_path(), _record())]) == []


def test_lcm_002_drift_fires():
    f = evaluate([(_path(), _record(status_value="candidate", ls_value="draft"))])
    assert any(x["rule"] == "LCM-002" for x in f)


def test_lcm_002_absent_status_is_allowed():
    r = _record()
    r.pop("status")
    assert evaluate([(_path(), r)]) == []


def test_lcm_002_both_in_legacy_set_passes():
    """candidate + candidate is the legacy compatibility case."""
    assert evaluate([(_path(), _record(
        status_value="candidate", ls_value="candidate"))]) == []


# -----------------------------------------------------------------------------
# LCM-003 (deprecation audit trail)
# -----------------------------------------------------------------------------


def test_lcm_003_deprecated_with_marker_passes():
    f = evaluate([(_path(), _record(
        status_value="deprecated", ls_value="deprecated",
        ch=[{"change": "This entry is now DEPRECATED."}]
    ))])
    assert f == []


def test_lcm_003_deprecated_without_marker_fires():
    f = evaluate([(_path(), _record(
        status_value="deprecated", ls_value="deprecated",
        ch=[{"change": "Migrated away."}]
    ))])
    assert any(x["rule"] == "LCM-003" for x in f)


def test_lcm_003_case_sensitive_uppercase_only():
    """Lowercase 'deprecated' is narrative; only UPPERCASE 'DEPRECATED' is a marker."""
    f = evaluate([(_path(), _record(
        status_value="deprecated", ls_value="deprecated",
        ch=[{"change": "this entry is now deprecated."}]
    ))])
    assert any(x["rule"] == "LCM-003" for x in f)


def test_lcm_003_only_applies_to_deprecated_records():
    """LCM-003 must not fire on candidate records (even with marker)."""
    f = evaluate([(_path(), _record(
        status_value="candidate", ls_value="candidate",
        ch=[{"change": "DEPRECATED marker in narrative."}]
    ))])
    # That would be LCM-004 (zombie marker), not LCM-003.
    rule_set = {x["rule"] for x in f}
    assert "LCM-003" not in rule_set


# -----------------------------------------------------------------------------
# LCM-004 (no zombie deprecation markers)
# -----------------------------------------------------------------------------


def test_lcm_004_candidate_with_marker_fires():
    f = evaluate([(_path(), _record(
        status_value="candidate", ls_value="candidate",
        ch=[{"change": "Marked DEPRECATED but rolled back."}]
    ))])
    assert any(x["rule"] == "LCM-004" for x in f)


def test_lcm_004_narrative_lowercase_does_not_fire():
    """A non-deprecated record mentioning 'deprecated' (lowercase) is allowed."""
    f = evaluate([(_path(), _record(
        status_value="candidate", ls_value="candidate",
        ch=[{"change": "lifecycle_status=deprecated in narrative"}]
    ))])
    assert f == []


def test_lcm_004_deprecated_is_exempt():
    """LCM-004 does not fire on deprecated records (LCM-003 covers them)."""
    f = evaluate([(_path(), _record(
        status_value="deprecated", ls_value="deprecated",
        ch=[{"change": "Now DEPRECATED."}]
    ))])
    rule_set = {x["rule"] for x in f}
    assert "LCM-004" not in rule_set


# -----------------------------------------------------------------------------
# LCM-005 (retired records in archive)
# -----------------------------------------------------------------------------


def test_lcm_005_retired_in_v1_alpha_fires():
    f = evaluate([(_path("retired_with_wrong_path"), _record(
        status_value="retired", ls_value="retired"
    ))])
    # Override path to wrong location
    wrong_path = Path("/x/v1-alpha/dea:process-self-test/dea:process-self-test.yaml")
    f = evaluate([(wrong_path, _record(
        status_value="retired", ls_value="retired"
    ))])
    assert any(x["rule"] == "LCM-005" for x in f)


def test_lcm_005_retired_in_archive_passes():
    archive_path = Path("/x/_retired/dea:process-self-test/dea:process-self-test.yaml")
    f = evaluate([(archive_path, _record(
        status_value="retired", ls_value="retired"
    ))])
    assert f == []


def test_lcm_005_only_applies_to_retired_records():
    """Non-retired records are exempt from LCM-005."""
    f = evaluate([(_path(), _record())])
    rule_set = {x["rule"] for x in f}
    assert "LCM-005" not in rule_set


# -----------------------------------------------------------------------------
# Helpers + coverage metadata
# -----------------------------------------------------------------------------


def test_has_deprecation_marker_case_sensitive():
    """_has_deprecation_marker must be case-sensitive."""
    upper = [{"change": "This entry is now DEPRECATED."}]
    lower = [{"change": "this entry is now deprecated."}]
    camel = [{"change": "lifecycle_status=deprecated and a redirect."}]
    assert _has_deprecation_marker(upper) is True
    assert _has_deprecation_marker(lower) is False
    assert _has_deprecation_marker(camel) is False


def test_approved_vocabulary_is_correct():
    assert APPROVED_LIFECYCLE_STATES == {
        "draft", "proposed", "validated", "published",
        "deprecated", "retired", "candidate",
    }


def test_legacy_set_is_candidate_only():
    assert LEGACY_COMPATIBILITY_SET == {"candidate"}


def test_rules_metadata_has_five_entries():
    record_rule_ids = [rid for rid, _fn, _label in _RULES_RECORD]
    path_rule_ids = [rid for rid, _fn, _label in _RULES_PATH]
    assert record_rule_ids == ["LCM-001", "LCM-002", "LCM-003", "LCM-004"]
    assert path_rule_ids == ["LCM-005"]


def test_evaluate_aggregates_across_records():
    """Multi-record evaluation sums findings from all records."""
    p = _path()
    findings = evaluate([
        (p, _record()),  # passes all
        (p, _record(ls_value="BAD", status_value="BAD")),  # LCM-001
        (p, _record(status_value="candidate", ls_value="draft")),  # LCM-002
    ])
    rule_set = {f["rule"] for f in findings}
    assert "LCM-001" in rule_set
    assert "LCM-002" in rule_set
