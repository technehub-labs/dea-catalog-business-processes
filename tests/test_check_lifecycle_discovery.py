"""Tests for the CR-BP-62 Lifecycle Discovery validator (DISC-001..008).

Note: `from check_lifecycle_discovery import ...` resolves at runtime via
the sys.path.insert below (scripts/ is not a configured package; pyright
cannot resolve the import -- this is expected and matches the pattern
used by the other validator test modules).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_lifecycle_discovery.py"
sys.path.insert(0, str(ROOT / "scripts"))
from check_lifecycle_discovery import (  # noqa: E402
    _check_disc_002,
    _check_disc_003,
    _check_disc_004,
    _check_disc_005,
    _check_disc_006,
    _check_disc_008,
    _fixture,
    _load_records,
    evaluate,
)


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, cwd=str(ROOT),
    )


def test_cli_self_test_passes():
    r = _run(["--self-test"])
    assert r.returncode == 0, r.stdout + r.stderr
    assert "self-test PASS" in r.stdout


def test_cli_live_run_conformant_on_discovery_records():
    r = _run([])
    assert r.returncode == 0, r.stdout + r.stderr
    assert "CONFORMANT" in r.stdout
    # CR-BP-63 landed the 14 Activate/Retire discovery records; CR-BP-70
    # added one P&R x Activate escape-clause record;
    # CR-BP-72 added one A&O x Retire escape-clause record.
    assert "Discovery records checked: 17" in r.stdout
    assert "Findings:                  0" in r.stdout


def test_cli_json_shape():
    r = _run(["--json"])
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data["verdict"] == "CONFORMANT"
    assert data["record_count"] == 17
    assert data["finding_count"] == 0
    assert isinstance(data["findings"], list)
    assert len(data["rules"]) == 8
    assert {rule["id"] for rule in data["rules"]} == {
        f"DISC-00{i}" for i in range(1, 9)
    }


def test_cli_strict_exit_zero_on_empty_catalog():
    r = _run(["--strict"])
    assert r.returncode == 0, r.stdout + r.stderr


def test_disc_002_rejects_noncanonical_domain():
    rec = _fixture()
    rec["discovery"]["ecf_context"]["domain"] = "Sales"
    assert _check_disc_002(rec) is not None


def test_disc_002_accepts_canonical_coordinate():
    assert _check_disc_002(_fixture()) is None


def test_disc_003_requires_verb_and_object():
    rec = _fixture(proposed_identity={"verb": "Transition", "object": ""})
    assert _check_disc_003(rec) is not None
    assert _check_disc_003(_fixture()) is None


def test_disc_004_disposition_vocabulary():
    assert _check_disc_004(_fixture(disposition="MAYBE")) is not None
    assert _check_disc_004(_fixture(disposition="DEFER")) is None


def test_disc_005_reject_requires_rationale():
    rec = _fixture(disposition="REJECT")
    rec["discovery"]["rationale"]["excluded"] = ""
    rec["discovery"]["rationale"]["unresolved"] = ""
    assert _check_disc_005(rec) is not None


def test_disc_005_admit_canonical_requires_ref():
    assert _check_disc_005(_fixture(disposition="ADMIT-CANONICAL")) is not None


def test_disc_005_admit_specialization_requires_parent():
    assert _check_disc_005(_fixture(disposition="ADMIT-SPECIALIZATION")) is not None


def test_disc_006_admit_canonical_requires_evidence_sources():
    rec = _fixture(disposition="ADMIT-CANONICAL")
    rec["discovery"]["candidates"][0]["disposition"]["canonical_process_ref"] = "dea:process-x"
    rec["discovery"]["candidates"][0]["evidence"]["sources"] = []
    assert _check_disc_006(rec) is not None
    rec["discovery"]["candidates"][0]["evidence"]["sources"] = ["ITIL service transition"]
    assert _check_disc_006(rec) is None


def test_disc_008_total_bounds_and_dimensions():
    rec = _fixture()
    rec["discovery"]["candidates"][0]["scoring"]["total"] = 11
    assert _check_disc_008(rec) is not None
    rec2 = _fixture()
    del rec2["discovery"]["candidates"][0]["scoring"]["semantic_stability"]
    assert _check_disc_008(rec2) is not None
    assert _check_disc_008(_fixture()) is None


def test_evaluate_runs_all_rules_on_fixture(tmp_path):
    schema = json.loads(
        (ROOT / "schemas" / "discovery" / "lifecycle-discovery.schema.json").read_text()
    )
    findings = evaluate([(tmp_path / "x.yaml", _fixture())], schema, (set(), set()))
    # The bare fixture fails DISC-001 against the real schema only if the
    # fixture drifts from the schema; it should pass all eight rules.
    assert findings == [], findings


def test_load_records_covers_discovery_dir():
    pairs = _load_records(ROOT)
    assert len(pairs) == 17
    # Stages are read from each record's ecf_context.lifecycle_stage field;
    # filename-suffix parsing was incorrect for escape records whose slug ends
    # in '-escape.yaml' (CR-BP-70). The file's outer dict wraps the discovery
    # body under the `discovery:` key.
    def _stage(rec):
        body = rec.get("discovery") if isinstance(rec, dict) else None
        if not isinstance(body, dict):
            return None
        return body.get("ecf_context", {}).get("lifecycle_stage")
    stages = {_stage(rec) for _, rec in pairs}
    assert stages == {"Activate", "Retire"}
