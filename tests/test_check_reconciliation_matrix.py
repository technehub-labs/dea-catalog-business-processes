"""Tests for the CR-BP-99 reconciliation matrix validator (RCM-001..010)."""

import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_reconciliation_matrix.py"
MATRIX_PATH = ROOT / "reconciliation" / "cr-bp-99-matrix.yaml"

sys.path.insert(0, str(ROOT / "scripts"))
from check_reconciliation_matrix import (  # noqa: E402
    ALLOWED_CATEGORIES,
    ALLOWED_DISPOSITIONS,
    ALLOWED_STATUSES,
    REQUIRED_FINDING_FIELDS,
    REQUIRED_ROW_FIELDS,
    ROW_ID_PATTERN,
    RULE_IDS,
    _check_categories,
    _check_disposition,
    _check_row_fields,
    _check_row_id_format,
    _check_schema,
    _check_status,
    _check_summary_counts,
    _check_unique_ids,
    evaluate,
    verdict,
)


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------


def test_row_id_pattern_matches_matrix_NNN():
    assert ROW_ID_PATTERN.match("matrix-001")
    assert ROW_ID_PATTERN.match("matrix-099")
    assert ROW_ID_PATTERN.match("matrix-999")
    assert not ROW_ID_PATTERN.match("matrix-1")
    assert not ROW_ID_PATTERN.match("matrix-0001")
    assert not ROW_ID_PATTERN.match("M-001")


def test_allowed_dispositions_enum():
    assert ALLOWED_DISPOSITIONS == frozenset({"backfill", "defer", "accept_as_is", "relax_rule"})


def test_allowed_statuses_enum():
    assert ALLOWED_STATUSES == frozenset({"open", "closed"})


def test_allowed_categories_includes_required():
    assert "act_backfill" in ALLOWED_CATEGORIES
    assert "doc_deferred" in ALLOWED_CATEGORIES
    assert "pre_existing" in ALLOWED_CATEGORIES
    assert "pg_conformant" in ALLOWED_CATEGORIES


def test_required_row_fields_complete():
    assert REQUIRED_ROW_FIELDS == frozenset({
        "id", "finding", "category", "disposition", "owner",
        "remediation", "status",
    })


def test_required_finding_fields_complete():
    assert REQUIRED_FINDING_FIELDS == frozenset({"rule", "record_id", "summary"})


def test_rule_ids_match_ten_checks():
    assert len(RULE_IDS) == 10
    assert "RCM-001" in RULE_IDS
    assert "RCM-010" in RULE_IDS


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def _minimal_matrix(rows=None):
    return {
        "matrix_version": 1,
        "generated_at": "2026-09-18",
        "rows": rows or [
            {
                "id": "matrix-001",
                "finding": {"rule": "TST", "record_id": "x", "summary": "test"},
                "category": "pre_existing",
                "disposition": "backfill",
                "owner": "CR-BP-99",
                "remediation": "test",
                "status": "closed",
                "closed_in": "PR-999",
            }
        ],
        "summary": {
            "total_rows": len(rows) if rows else 1,
            "by_disposition": {"backfill": len(rows) if rows else 1},
            "by_status": {"closed": len(rows) if rows else 1},
        },
        "invariants": [{"id": "test invariant"}],
    }


# -----------------------------------------------------------------------------
# RCM-001
# -----------------------------------------------------------------------------


def test_rcm_001_pass():
    matrix = _minimal_matrix()
    findings = _check_schema(matrix)
    assert findings == []


def test_rcm_001_fail_not_dict():
    findings = _check_schema(["not", "a", "dict"])
    assert any(f.rule == "RCM-001" for f in findings)


def test_rcm_001_fail_missing_top_level():
    findings = _check_schema({"matrix_version": 1})
    assert any(f.rule == "RCM-001" for f in findings)


def test_rcm_001_fail_rows_not_list():
    matrix = _minimal_matrix()
    matrix["rows"] = "not-a-list"
    findings = _check_schema(matrix)
    assert any(f.rule == "RCM-001" for f in findings)


# -----------------------------------------------------------------------------
# RCM-002 row fields
# -----------------------------------------------------------------------------


def test_rcm_002_pass():
    matrix = _minimal_matrix()
    findings = _check_row_fields(matrix["rows"])
    assert findings == []


def test_rcm_002_fail_missing_id():
    matrix = _minimal_matrix()
    matrix["rows"][0].pop("id")
    findings = _check_row_fields(matrix["rows"])
    assert any(f.rule == "RCM-002" for f in findings)


def test_rcm_002_fail_finding_missing_fields():
    matrix = _minimal_matrix()
    matrix["rows"][0]["finding"] = {"rule": "TST"}
    findings = _check_row_fields(matrix["rows"])
    assert any(f.rule == "RCM-002" for f in findings)


# -----------------------------------------------------------------------------
# RCM-003 row id format
# -----------------------------------------------------------------------------


def test_rcm_003_pass():
    matrix = _minimal_matrix()
    findings = _check_row_id_format(matrix["rows"])
    assert findings == []


def test_rcm_003_fail_short_id():
    matrix = _minimal_matrix()
    matrix["rows"][0]["id"] = "matrix-1"
    findings = _check_row_id_format(matrix["rows"])
    assert any(f.rule == "RCM-003" for f in findings)


# -----------------------------------------------------------------------------
# RCM-004 disposition
# -----------------------------------------------------------------------------


def test_rcm_004_pass():
    matrix = _minimal_matrix()
    findings = _check_disposition(matrix["rows"])
    assert findings == []


def test_rcm_004_fail_unknown_disposition():
    matrix = _minimal_matrix()
    matrix["rows"][0]["disposition"] = "rename"
    findings = _check_disposition(matrix["rows"])
    assert any(f.rule == "RCM-004" for f in findings)


# -----------------------------------------------------------------------------
# RCM-005 / RCM-006 status + closed_in
# -----------------------------------------------------------------------------


def test_rcm_005_pass():
    matrix = _minimal_matrix()
    findings = _check_status(matrix["rows"])
    assert findings == []


def test_rcm_005_fail_unknown_status():
    matrix = _minimal_matrix()
    matrix["rows"][0]["status"] = "pending"
    findings = _check_status(matrix["rows"])
    assert any(f.rule == "RCM-005" for f in findings)


def test_rcm_006_fail_closed_without_closed_in():
    matrix = _minimal_matrix()
    matrix["rows"][0].pop("closed_in")
    findings = _check_status(matrix["rows"])
    assert any(f.rule == "RCM-006" for f in findings)


def test_rcm_006_pass_open_row_no_closed_in():
    matrix = _minimal_matrix([
        {
            "id": "matrix-001",
            "finding": {"rule": "TST", "record_id": "x", "summary": "test"},
            "category": "pre_existing",
            "disposition": "defer",
            "owner": "EXT-06",
            "remediation": "test",
            "status": "open",
        }
    ])
    findings = _check_status(matrix["rows"])
    assert findings == []


# -----------------------------------------------------------------------------
# RCM-007 categories
# -----------------------------------------------------------------------------


def test_rcm_007_pass():
    matrix = _minimal_matrix()
    findings = _check_categories(matrix["rows"])
    assert findings == []


def test_rcm_007_fail_unknown_category():
    matrix = _minimal_matrix()
    matrix["rows"][0]["category"] = "unknown_category"
    findings = _check_categories(matrix["rows"])
    assert any(f.rule == "RCM-007" for f in findings)


# -----------------------------------------------------------------------------
# RCM-008 unique ids
# -----------------------------------------------------------------------------


def test_rcm_008_pass():
    matrix = _minimal_matrix()
    findings = _check_unique_ids(matrix["rows"])
    assert findings == []


def test_rcm_008_fail_duplicate():
    matrix = _minimal_matrix([
        {
            "id": "matrix-001",
            "finding": {"rule": "TST", "record_id": "x", "summary": "test"},
            "category": "pre_existing",
            "disposition": "backfill",
            "owner": "CR-BP-99",
            "remediation": "test",
            "status": "closed",
            "closed_in": "PR-999",
        },
        {
            "id": "matrix-001",
            "finding": {"rule": "TST", "record_id": "y", "summary": "test"},
            "category": "pre_existing",
            "disposition": "backfill",
            "owner": "CR-BP-99",
            "remediation": "test",
            "status": "closed",
            "closed_in": "PR-999",
        },
    ])
    findings = _check_unique_ids(matrix["rows"])
    assert any(f.rule == "RCM-008" for f in findings)


# -----------------------------------------------------------------------------
# RCM-009 summary counts
# -----------------------------------------------------------------------------


def test_rcm_009_pass():
    matrix = _minimal_matrix()
    findings = _check_summary_counts(matrix)
    assert findings == []


def test_rcm_009_fail_disposition_mismatch():
    matrix = _minimal_matrix()
    matrix["summary"]["by_disposition"] = {"defer": 1}
    findings = _check_summary_counts(matrix)
    assert any(f.rule == "RCM-009" and "disposition" in f.message for f in findings)


def test_rcm_009_fail_total_rows_mismatch():
    matrix = _minimal_matrix()
    matrix["summary"]["total_rows"] = 99
    findings = _check_summary_counts(matrix)
    assert any(f.rule == "RCM-009" and "total_rows" in f.message for f in findings)


# -----------------------------------------------------------------------------
# Aggregate evaluate() + verdict()
# -----------------------------------------------------------------------------


def test_evaluate_minimal_matrix_conformant():
    findings = evaluate(_minimal_matrix())
    assert verdict(findings) == "CONFORMANT"


def test_evaluate_propagates_errors():
    matrix = _minimal_matrix()
    matrix["rows"][0]["disposition"] = "rename"
    findings = evaluate(matrix)
    assert verdict(findings) == "NON-CONFORMANT"
    assert any(f.rule == "RCM-004" for f in findings)


# -----------------------------------------------------------------------------
# CLI
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
    """Live matrix: 21 rows / 0 findings / CONFORMANT."""
    result = _run([])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CONFORMANT" in result.stdout
    assert "Rows checked:  21" in result.stdout


def test_cli_json_emits_well_formed_payload():
    result = _run(["--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["verdict"] == "CONFORMANT"
    assert payload["rows_checked"] == 21
    rule_ids = {r["id"] for r in payload["rules"]}
    assert rule_ids == {"RCM-001", "RCM-002", "RCM-003", "RCM-004", "RCM-005",
                        "RCM-006", "RCM-007", "RCM-008", "RCM-009", "RCM-010"}


def test_live_matrix_has_21_rows():
    """Cross-check: live matrix actually has 21 rows (CR-BP-100 matrix-021)."""
    with open(MATRIX_PATH) as f:
        matrix = yaml.safe_load(f)
    assert len(matrix["rows"]) == 21
    # All 9 ACT-011 backfills are closed.
    backfills = [r for r in matrix["rows"] if r["disposition"] == "backfill"]
    assert len(backfills) == 9
    assert all(r["status"] == "closed" for r in backfills)


def test_live_matrix_act011_backfills_target_correct_records():
    """The 9 backfill rows target the exact records identified by ACT-011."""
    expected = {
        "dea:activity-calculate-compensation",
        "dea:activity-commit-agent-topology",
        "dea:activity-commit-role-catalogue",
        "dea:activity-disburse-payroll",
        "dea:activity-execute-payments-to-plan",
        "dea:activity-fit-out-facilities",
        "dea:activity-manage-collections",
        "dea:activity-resolve-attendance-exceptions",
        "dea:activity-score-finding-severity",
    }
    with open(MATRIX_PATH) as f:
        matrix = yaml.safe_load(f)
    actual = {r["finding"]["record_id"] for r in matrix["rows"]
              if r["disposition"] == "backfill"}
    assert actual == expected


def test_live_matrix_summary_counts_consistent():
    with open(MATRIX_PATH) as f:
        matrix = yaml.safe_load(f)
    summary = matrix["summary"]
    assert summary["total_rows"] == len(matrix["rows"])
    assert summary["by_disposition"] == {"backfill": 9, "defer": 4, "accept_as_is": 8}
    assert summary["by_status"] == {"closed": 15, "open": 6}