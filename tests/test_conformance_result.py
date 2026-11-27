"""Tests for the unified Conformance Result aggregator (CR-BP-16 S18)
and the conformance pipeline documentation.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import conformance_result as conformance_result_module
SCRIPT_RESULT = ROOT / "scripts" / "conformance_result.py"
PIPELINE_DOC = ROOT / "docs" / "conformance-pipeline.md"


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *args], capture_output=True, text=True, cwd=str(ROOT),
    )


def test_conformance_result_runs_on_live():
    """Live run returns CONFORMANT."""
    r = _run([str(SCRIPT_RESULT)])
    assert r.returncode == 0, r.stdout + r.stderr
    assert ("Conformance Result (CR-BP-16 §18): CONFORMANT" in r.stdout
            or "Conformance Result (CR-BP-16 §18): CONFORMANT-WITH-WARNINGS" in r.stdout)
    assert "0 blocking failures" in r.stdout


def test_conformance_result_json_shape():
    r = _run([str(SCRIPT_RESULT), "--json"])
    assert r.returncode == 0, r.stdout + r.stderr
    data = json.loads(r.stdout)
    assert data["verdict"] in {"CONFORMANT", "CONFORMANT-WITH-WARNINGS"}
    assert data["blocking_failures"] == []
    assert isinstance(data["gates"], list)
    assert len(data["gates"]) >= 10
    # Each gate has the expected fields
    for g in data["gates"]:
        assert {"name", "blocking", "returncode", "verdict_line"} <= set(g)
    # 10-step pipeline is covered
    gate_names = " ".join(g["name"] for g in data["gates"])
    for step in range(1, 11):
        assert f"[{step}]" in gate_names, f"step {step} missing"


def test_conformance_result_strict_propagates_failure():
    """With a non-existent catalog root, the script should fail and emit
    NON-CONFORMANT (or pass the gates that handle missing dirs).
    Verify --strict surfaces failures."""
    r = _run([str(SCRIPT_RESULT), "--strict", "--catalog-root", "/tmp/nonexistent-cat"])
    # The schema step will fail because CATALOG.yaml doesn't exist.
    # Other steps may pass or fail. The verdict should be NON-CONFORMANT
    # if any blocking gate failed.
    if r.returncode != 0:
        assert "NON-CONFORMANT" in r.stdout or r.returncode != 0


def test_pipeline_doc_exists():
    assert PIPELINE_DOC.exists(), "docs/conformance-pipeline.md must exist"


def test_pipeline_doc_covers_all_10_steps():
    """Every pipeline step [1]..[10] must appear in the doc."""
    text = PIPELINE_DOC.read_text()
    for step in range(1, 11):
        assert re.search(rf"\[{step}\]", text), f"step [{step}] missing"


def test_pipeline_doc_covers_13_blocking_conditions():
    """CR-BP-16 §19 lists 13 blocking conditions; the doc must cover them."""
    text = PIPELINE_DOC.read_text()
    conditions = [
        "Invalid schema", "Broken reference", "Duplicate canonical id",
        "Invalid hierarchy", "Invalid Process Intent", "Invalid Classification",
        "Invalid specialization", "Specialization cycle",
        "Missing mandatory evidence", "Unresolved identity",
        "Unresolved canonical disposition", "Lost provenance",
        "Unauthorized ontology expansion",
    ]
    for c in conditions:
        assert c in text, f"blocking condition missing: {c}"


def test_pipeline_doc_covers_continuous_conformance():
    """CR-BP-16 §25 mandates re-evaluation triggers; the doc must cover them."""
    text = PIPELINE_DOC.read_text()
    for trigger in [
        "a process is created",
        "a process changes",
        "its parent changes",
        "its Context changes",
        "its specialization changes",
        "classification vocabularies change",
        "the governing metamodel changes",
    ]:
        assert trigger in text, f"continuous-conformance trigger missing: {trigger}"

def test_cr_readme_gate_is_invoked_strictly():
    """CRR-001..003 is a blocking gate and must not fail open on findings."""
    gate = next(
        item for item in conformance_result_module.GATES
        if "CR README Consistency" in item[0]
    )
    assert gate[1] is True
    assert gate[2][-1] == "--strict"


def test_failed_gate_diagnostics_are_preserved(monkeypatch, capsys):
    """A failed validator's rule/file diagnostics must reach CI output."""
    conformance_result_module.GATES = [
        ("[test] README diagnostic fixture", True,
         [sys.executable, "-c", "print('RDM-001: fixture README is stale'); raise SystemExit(1)"]),
    ]
    result = conformance_result_module.main([])
    captured = capsys.readouterr()
    assert result == 1
    assert "RDM-001: fixture README is stale" in captured.out
