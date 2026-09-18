"""Tests for the CR-BP-34a L2 Qualification validator.

Locks behaviour for BP-C1..C4 by exercising both the in-process
`evaluate()` function and the CLI self-test entry point, plus a
live-catalog assertion that all 139 canonical Business Process
records pass all four rules.

CR-BP-96 extends the validator with BP-QUAL-001..012. The
001/002/006/007/010/012 rules are aliases of the BP-C family; the
003/004/005/008/009 rules are advisory structure checks for OPTIONAL
fields (CR-BP-96 design intent). BP-QUAL-011 (Specialization
Integrity) is deferred under CR-BP-92 §21.
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
    _BP_QUAL_ALIASES,
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
    """The 131 canonical BP records must pass all four rules."""
    result = _run(["--strict"])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CONFORMANT" in result.stdout
    assert "Records checked:  139" in result.stdout
    assert "Findings:         0" in result.stdout


def test_cli_json_emits_well_formed_payload():
    result = _run(["--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    import json
    payload = json.loads(result.stdout)
    assert payload["verdict"] == "CONFORMANT"
    assert payload["candidate_count"] == 139
    assert payload["finding_count"] == 0
    rule_ids = {r["id"] for r in payload["rules"]}
    assert rule_ids == {"BP-C1", "BP-C2", "BP-C3", "BP-C4",
                        "BP-QUAL-003", "BP-QUAL-004", "BP-QUAL-005",
                        "BP-QUAL-008", "BP-QUAL-009"}


# -----------------------------------------------------------------------------
# evaluate(): per-rule
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
    assert rule_ids == ["BP-C1", "BP-C2", "BP-C3", "BP-C4",
                        "BP-QUAL-003", "BP-QUAL-004", "BP-QUAL-005",
                        "BP-QUAL-008", "BP-QUAL-009"]


# -----------------------------------------------------------------------------
# CR-BP-96 BP-QUAL extensions (advisory; OPTIONAL fields).
# -----------------------------------------------------------------------------


def test_evaluate_bp_qual_003_passes_vacuously_when_field_absent() -> None:
    """BP-QUAL-003: input field absent -> advisory passes vacuously."""
    f = evaluate([_baseline_record()])
    assert not any(fnd["rule"] == "BP-QUAL-003" for fnd in f)


def test_evaluate_bp_qual_003_fires_when_inputs_empty_list() -> None:
    """BP-QUAL-003: inputs present but empty -> advisory finding."""
    f = evaluate([_baseline_record(inputs=[])])
    assert any(fnd["rule"] == "BP-QUAL-003" and fnd["advisory"] for fnd in f), f


def test_evaluate_bp_qual_003_fires_when_input_entry_missing_required() -> None:
    """BP-QUAL-003: input entry missing required field -> advisory finding."""
    f = evaluate([_baseline_record(inputs=[{"id": "in-1", "name": "Input 1"}])])
    assert any(fnd["rule"] == "BP-QUAL-003" for fnd in f), f


def test_evaluate_bp_qual_003_passes_on_valid_input_entry() -> None:
    """BP-QUAL-003: input entry with full shape -> no finding."""
    f = evaluate([_baseline_record(inputs=[
        {"id": "in-1", "name": "Input 1", "description": "A description.",
         "source": "dea:source-x"},
    ])])
    assert not any(fnd["rule"] == "BP-QUAL-003" for fnd in f)


def test_evaluate_bp_qual_004_passes_on_valid_transformation_string() -> None:
    """BP-QUAL-004: transformation as non-empty string -> no finding."""
    f = evaluate([_baseline_record(transformation="Input X is converted to output Y.")])
    assert not any(fnd["rule"] == "BP-QUAL-004" for fnd in f)


def test_evaluate_bp_qual_004_passes_on_valid_transformation_list() -> None:
    """BP-QUAL-004: transformation as list of step objects -> no finding."""
    f = evaluate([_baseline_record(transformation=[
        {"name": "Step 1", "description": "First step."},
        {"name": "Step 2", "description": "Second step."},
    ])])
    assert not any(fnd["rule"] == "BP-QUAL-004" for fnd in f)


def test_evaluate_bp_qual_004_fires_on_empty_string() -> None:
    """BP-QUAL-004: transformation present but empty string -> advisory."""
    f = evaluate([_baseline_record(transformation="")])
    assert any(fnd["rule"] == "BP-QUAL-004" and fnd["advisory"] for fnd in f), f


def test_evaluate_bp_qual_005_passes_on_valid_output_entry() -> None:
    """BP-QUAL-005: output entry with full shape -> no finding."""
    f = evaluate([_baseline_record(outputs=[
        {"id": "out-1", "name": "Output 1", "description": "A description.",
         "consumer": "dea:consumer-x"},
    ])])
    assert not any(fnd["rule"] == "BP-QUAL-005" for fnd in f)


def test_evaluate_bp_qual_005_fires_when_output_entry_missing_required() -> None:
    """BP-QUAL-005: output entry missing required field -> advisory."""
    f = evaluate([_baseline_record(outputs=[{"id": "out-1"}])])
    assert any(fnd["rule"] == "BP-QUAL-005" for fnd in f), f


def test_evaluate_bp_qual_008_passes_on_valid_responsibility_string() -> None:
    """BP-QUAL-008: responsibility as non-empty string -> no finding."""
    f = evaluate([_baseline_record(responsibility="Operations team")])
    assert not any(fnd["rule"] == "BP-QUAL-008" for fnd in f)


def test_evaluate_bp_qual_008_fires_on_empty_string() -> None:
    """BP-QUAL-008: responsibility present but empty string -> advisory."""
    f = evaluate([_baseline_record(responsibility="")])
    assert any(fnd["rule"] == "BP-QUAL-008" and fnd["advisory"] for fnd in f), f


def test_evaluate_bp_qual_009_passes_on_valid_boundary_object() -> None:
    """BP-QUAL-009: boundary as non-empty object -> no finding."""
    f = evaluate([_baseline_record(boundary={"scope": "all customer segments"})])
    assert not any(fnd["rule"] == "BP-QUAL-009" for fnd in f)


def test_evaluate_bp_qual_009_fires_on_empty_object() -> None:
    """BP-QUAL-009: boundary present but empty object -> advisory."""
    f = evaluate([_baseline_record(boundary={})])
    assert any(fnd["rule"] == "BP-QUAL-009" and fnd["advisory"] for fnd in f), f


def test_bp_qual_aliases_match_existing_bp_c_family() -> None:
    """The BP-QUAL-001/002/006/007/010/012 aliases inherit BP-C verdicts."""
    assert _BP_QUAL_ALIASES["BP-QUAL-001"] == "BP-C3"
    assert _BP_QUAL_ALIASES["BP-QUAL-002"] == "BP-C1"
    assert _BP_QUAL_ALIASES["BP-QUAL-006"] == "BP-C1+BP-C2"
    assert _BP_QUAL_ALIASES["BP-QUAL-007"] == "BP-C2"
    assert _BP_QUAL_ALIASES["BP-QUAL-010"] == "BP-C3"
    assert _BP_QUAL_ALIASES["BP-QUAL-012"] == "BP-C4"


def test_bp_qual_findings_are_tagged_advisory() -> None:
    """BP-QUAL findings must carry advisory=True so --strict does not fail."""
    f = evaluate([_baseline_record(inputs=[])])
    bp_qual_findings = [fnd for fnd in f if fnd["rule"].startswith("BP-QUAL")]
    assert bp_qual_findings, "expected at least one BP-QUAL finding"
    for fnd in bp_qual_findings:
        assert fnd["advisory"] is True, fnd
