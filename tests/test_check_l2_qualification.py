"""Tests for the CR-BP-34a L2 Qualification validator.

Locks behaviour for BP-C1..C4 by exercising both the in-process
`evaluate()` function and the CLI self-test entry point, plus a
live-catalog assertion that all 126 canonical Business Process
records pass all four rules.
"""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_l2_qualification.py"

# Import the validator in-process so we can hit the evaluate() function
# directly without spinning up subprocesses for every rule.
sys.path.insert(0, str(ROOT / "scripts"))
from check_l2_qualification import (  # noqa: E402
    _RULES,
    evaluate,
    _self_test,
)


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def _baseline_record(**overrides):
    """Return a record that satisfies all four L2 qualification criteria."""
    base = {
        "id": "dea:process-self-test",
        "name": "Self Test",
        "type": "Process",
        "version": "1.0.0",
        "lifecycle_status": "candidate",
        "status": "candidate",
        "process_intent": "operate",
        "process_type": "core",
        "description": "Self-test record.",
        "trigger": "An input arrives.",
        "outcome": "An output is produced.",
        "identity": {
            "verb": "Test",
            "object": "Self",
            "outcome_statement": "Self-test outcome.",
            "evidence_links": [{"type": "standard", "ref": "https://example.com"}],
        },
        "metadata": {
            "change_history": [
                {"cr": "CR-BP-34a", "date": "2026-09-10", "change": "self-test"}
            ],
        },
    }
    base.update(overrides)
    return base


# -----------------------------------------------------------------------------
# CLI-level tests
# -----------------------------------------------------------------------------


def test_cli_self_test_passes():
    result = _run(["--self-test"])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "self-test PASS" in result.stdout


def test_cli_in_process_self_test():
    """Hit the --self-test entry point directly (no subprocess)."""
    rc = _self_test()
    assert rc == 0


def test_cli_live_catalog_conformant():
    """The 126 canonical BP records must pass all four rules."""
    result = _run(["--strict"])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CONFORMANT" in result.stdout
    assert "Records checked:  128" in result.stdout
    assert "Findings:         0" in result.stdout


def test_cli_json_emits_well_formed_payload():
    result = _run(["--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    import json
    payload = json.loads(result.stdout)
    assert payload["verdict"] == "CONFORMANT"
    assert payload["candidate_count"] == 128
    assert payload["finding_count"] == 0
    rule_ids = {r["id"] for r in payload["rules"]}
    assert rule_ids == {"BP-C1", "BP-C2", "BP-C3", "BP-C4"}


# -----------------------------------------------------------------------------
# evaluate() — per-rule
# -----------------------------------------------------------------------------


def test_evaluate_baseline_returns_no_findings():
    assert evaluate([_baseline_record()]) == []


def test_evaluate_bp_c1_trigger_missing():
    f = evaluate([_baseline_record(trigger="")])
    assert len(f) == 1 and f[0]["rule"] == "BP-C1"
    assert "trigger" in f[0]["diagnostic"]


def test_evaluate_bp_c1_outcome_missing():
    f = evaluate([_baseline_record(outcome="")])
    assert len(f) == 1 and f[0]["rule"] == "BP-C1"
    assert "outcome" in f[0]["diagnostic"]


def test_evaluate_bp_c2_identity_block_missing():
    """When the identity block is entirely absent, BP-C2 fails.

    Note: BP-C4 also fires in this case because it depends on
    identity.evidence_links. The test asserts the BP-C2 finding is
    present and the record_id matches; it does not assert no other
    rules fire.
    """
    f = evaluate([_baseline_record(identity=None)])
    bp_c2 = [x for x in f if x["rule"] == "BP-C2"]
    assert len(bp_c2) == 1
    assert "outcome_statement" in bp_c2[0]["diagnostic"]


def test_evaluate_bp_c2_outcome_statement_empty():
    f = evaluate([_baseline_record(identity={
        "verb": "x", "object": "y", "outcome_statement": "",
        "evidence_links": [{"ref": "x"}],
    })])
    assert len(f) == 1 and f[0]["rule"] == "BP-C2"


def test_evaluate_bp_c3_lifecycle_status_missing():
    f = evaluate([_baseline_record(lifecycle_status="")])
    assert len(f) == 1 and f[0]["rule"] == "BP-C3"


def test_evaluate_bp_c3_id_pattern_violation():
    f = evaluate([_baseline_record(id="dea:wrong-prefix")])
    assert len(f) == 1 and f[0]["rule"] == "BP-C3"
    assert "does not match" in f[0]["diagnostic"]


def test_evaluate_bp_c4_evidence_links_missing():
    f = evaluate([_baseline_record(identity={
        "verb": "x", "object": "y", "outcome_statement": "z",
        "evidence_links": [],
    })])
    assert len(f) == 1 and f[0]["rule"] == "BP-C4"


def test_evaluate_bp_c4_change_history_missing():
    f = evaluate([_baseline_record(metadata={"change_history": []})])
    assert len(f) == 1 and f[0]["rule"] == "BP-C4"


def test_evaluate_accepts_top_level_change_history():
    """Legacy top-level `change_history` shape must satisfy BP-C4."""
    rec = _baseline_record()
    rec.pop("metadata", None)
    rec["change_history"] = [{"cr": "CR-BP-34a"}]
    assert evaluate([rec]) == []


def test_evaluate_multi_rule_failure_yields_one_finding_per_rule():
    rec = _baseline_record(
        trigger="",
        identity={
            "verb": "x", "object": "y", "outcome_statement": "",
            "evidence_links": [{"ref": "x"}],
        },
    )
    findings = evaluate([rec])
    rule_set = {f["rule"] for f in findings}
    assert rule_set == {"BP-C1", "BP-C2"}
    assert len(findings) == 2


def test_evaluate_aggregates_across_records():
    rec_a = _baseline_record()  # passes all four
    rec_b = _baseline_record(id="dea:process-self-test-b", trigger="")
    findings = evaluate([rec_a, rec_b])
    assert len(findings) == 1
    assert findings[0]["record_id"] == "dea:process-self-test-b"
    assert findings[0]["rule"] == "BP-C1"


# -----------------------------------------------------------------------------
# Coverage metadata
# -----------------------------------------------------------------------------


def test_rules_metadata_has_four_entries():
    """Sanity: BP-C1..C4 is the complete rule set; no extras, no gaps."""
    rule_ids = [rid for rid, _fn, _label in _RULES]
    assert rule_ids == ["BP-C1", "BP-C2", "BP-C3", "BP-C4"]
