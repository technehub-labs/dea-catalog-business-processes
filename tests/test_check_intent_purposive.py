"""Tests for the CR-BP-34b Intent Purposive validator.

Locks behaviour for PSP-001..003 by exercising both the in-process
`evaluate()` function and the CLI self-test entry point, plus a
live-catalog assertion that all 126 canonical Business Process
records pass all three rules.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_intent_purposive.py"

# Import the validator in-process so we can hit the evaluate() function
# directly without spinning up subprocesses for every rule.
sys.path.insert(0, str(ROOT / "scripts"))
from check_intent_purposive import (  # noqa: E402
    APPROVED_INTENTS,
    ORG_COMPONENT_DENYLIST,
    _RULES,
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


def _record(intent=None):
    """Build a record with the given process_intent (or None)."""
    return {
        "id": "dea:process-self-test",
        "name": "Self Test",
        "type": "Process",
        "version": "1.0.0",
        "process_intent": intent,
    }


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
    assert "Records checked:  136" in result.stdout
    assert "Findings:         0" in result.stdout


def test_cli_json_emits_well_formed_payload():
    result = _run(["--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["verdict"] == "CONFORMANT"
    assert payload["candidate_count"] == 136
    assert payload["finding_count"] == 0
    rule_ids = {r["id"] for r in payload["rules"]}
    assert rule_ids == {"PSP-001", "PSP-002", "PSP-003"}
    assert set(payload["approved_intents"]) == {
        "govern", "manage", "operate", "deliver",
        "support", "develop", "transform",
    }
    assert payload["org_component_denylist_size"] == len(ORG_COMPONENT_DENYLIST)


# -----------------------------------------------------------------------------
# evaluate() — per-rule
# -----------------------------------------------------------------------------


def test_evaluate_baseline_approved_intent_returns_no_findings():
    assert evaluate([_record("operate")]) == []


def test_evaluate_all_seven_approved_values_pass():
    for intent in sorted(APPROVED_INTENTS):
        assert evaluate([_record(intent)]) == [], (
            f"approved value {intent!r} should pass all three rules"
        )


def test_evaluate_psp_001_present_but_empty():
    f = evaluate([_record("")])
    assert len(f) == 1 and f[0]["rule"] == "PSP-001"
    assert "empty" in f[0]["diagnostic"]


def test_evaluate_psp_001_absent_is_silent():
    """Absent process_intent is allowed; PSP-001 only fires when present-but-empty."""
    assert evaluate([_record(None)]) == []


def test_evaluate_psp_001_non_string_fires():
    f = evaluate([_record(123)])
    assert len(f) == 1 and f[0]["rule"] == "PSP-001"
    assert "must be a string" in f[0]["diagnostic"]


def test_evaluate_psp_002_unapproved_value_fires():
    f = evaluate([_record("not-a-purpose")])
    assert len(f) == 1 and f[0]["rule"] == "PSP-002"
    assert "not in approved vocabulary" in f[0]["diagnostic"]
    assert "operate" in f[0]["diagnostic"]  # shows the vocabulary


def test_evaluate_psp_002_does_not_double_fire_on_empty():
    """Empty intent fires only PSP-001, not PSP-002 (single rule per gap)."""
    f = evaluate([_record("")])
    rule_set = {x["rule"] for x in f}
    assert rule_set == {"PSP-001"}


def test_evaluate_psp_003_org_component_word_fires():
    f = evaluate([_record("operations")])
    rule_set = {x["rule"] for x in f}
    # "operations" is not in APPROVED_INTENTS AND is in the denylist,
    # so both PSP-002 and PSP-003 fire.
    assert "PSP-003" in rule_set
    psp_003 = next(x for x in f if x["rule"] == "PSP-003")
    assert "organizational component" in psp_003["diagnostic"]


def test_evaluate_psp_003_case_insensitive():
    f = evaluate([_record("HR")])
    assert any(x["rule"] == "PSP-003" for x in f)


def test_evaluate_psp_003_whitespace_stripped():
    f = evaluate([_record("  finance  ")])
    assert any(x["rule"] == "PSP-003" for x in f)


def test_evaluate_psp_003_ecf_domain_name_in_intent_fires():
    """ECF domain names belong in process_context, not intent."""
    for ecf_name in (
        "strategyAndDirection",
        "agencyAndOrganization",
        "partyAndRelationship",
        "productAndValue",
        "enablementAndOperations",
        "financeAndAccounting",
        "governanceAndExistence",
    ):
        f = evaluate([_record(ecf_name)])
        assert any(x["rule"] == "PSP-003" for x in f), ecf_name


def test_evaluate_psp_003_lifecycle_stage_in_intent_fires():
    """Lifecycle stage names belong in process_context, not intent."""
    for stage in ("conceive", "design", "build", "activate", "improve", "retire"):
        f = evaluate([_record(stage)])
        assert any(x["rule"] == "PSP-003" for x in f), stage


def test_evaluate_aggregates_across_records():
    findings = evaluate([
        _record("operate"),  # pass
        _record(""),         # PSP-001
        _record("operations"),  # PSP-002 + PSP-003
    ])
    # All three findings, same record_id, mixed rules.
    assert len(findings) == 3
    rule_set = {f["rule"] for f in findings}
    assert rule_set == {"PSP-001", "PSP-002", "PSP-003"}


# -----------------------------------------------------------------------------
# Coverage metadata
# -----------------------------------------------------------------------------


def test_rules_metadata_has_three_entries():
    rule_ids = [rid for rid, _fn, _label in _RULES]
    assert rule_ids == ["PSP-001", "PSP-002", "PSP-003"]


def test_approved_vocabulary_is_seven_values():
    assert len(APPROVED_INTENTS) == 7


def test_org_component_denylist_is_curated():
    """The denylist should be intentional, not a regex of all org words.

    Sanity check: at least 20 entries, no overlap with approved
    intent vocabulary (the two sets are disjoint by construction).
    """
    assert len(ORG_COMPONENT_DENYLIST) >= 20
    assert APPROVED_INTENTS.isdisjoint(ORG_COMPONENT_DENYLIST)
