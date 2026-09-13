"""Tests for the architectural-regression detector
(CR-BP-16 S21; BP-AR-001..007) and the conformance report
generator (CR-BP-16 S23).
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRIPT_BPAR = ROOT / "scripts" / "check_architectural_regression.py"
SCRIPT_REPORT = ROOT / "scripts" / "build_conformance_report.py"


def _run(args: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *args], capture_output=True, text=True, cwd=str(cwd),
    )


def test_bpar_self_test_passes():
    r = _run([str(SCRIPT_BPAR), "--self-test"])
    assert r.returncode == 0, r.stdout + r.stderr
    assert "self-test PASS" in r.stdout


def test_bpar_live_run_is_conformant():
    r = _run([str(SCRIPT_BPAR)])
    assert r.returncode == 0, r.stdout + r.stderr
    assert "CONFORMANT" in r.stdout
    assert "no architectural regressions detected" in r.stdout


def test_bpar_rejects_canonical_bad(tmp_path):
    """A fixture that triggers BP-AR-001, 002, 005, 006, 007
    must produce non-zero exit under --strict."""
    sandbox = tmp_path / "sandbox"
    shutil.copytree(ROOT / "entities", sandbox / "entities")
    bad_file = sandbox / "entities" / "v1-alpha" / "dea:process-customer-channel-and-acquisition-build" / "dea:process-customer-channel-and-acquisition-build.yaml"
    data = yaml.safe_load(bad_file.read_text())
    # Introduce forbidden tokens in name + description.
    data["name"] = "Process Kernel Design"
    data["description"] = (data.get("description") or "") + " Decomposed specialization example."
    data["process_audience"] = "party-relationship"  # BP-AR-005
    bad_file.write_text(yaml.safe_dump(data, sort_keys=False))
    r = _run([str(SCRIPT_BPAR), "--strict", "--catalog-root", str(sandbox)])
    assert r.returncode != 0, (
        "strict mode should fail on an architectural regression fixture: "
        + r.stdout + r.stderr
    )
    assert "BP-AR-001" in r.stdout or "BP-AR-007" in r.stdout


def test_bpar_json_output_is_well_formed():
    r = _run([str(SCRIPT_BPAR), "--json"])
    assert r.returncode == 0, r.stdout + r.stderr
    data = json.loads(r.stdout)
    assert "verdict" in data
    assert "findings" in data
    assert data["verdict"] in {"CONFORMANT", "CONFORMANT-WITH-WARNINGS", "NON-CONFORMANT"}


def test_conformance_report_live_is_level_4():
    """All 38 canonical records should reach Level 4 (Canonically
    Conformant) on the locked population."""
    r = _run([str(SCRIPT_REPORT)])
    assert r.returncode == 0, r.stdout + r.stderr
    report = yaml.safe_load(
        (ROOT / "reconciliation" / "conformance_report.yaml").read_text()
    )
    assert report["total_records"] == 597
    assert report["conformance_levels"] == {0: 0, 1: 0, 2: 0, 3: 0, 4: 597}


def test_conformance_report_check_passes():
    """The check mode must agree with the live report."""
    r = _run([str(SCRIPT_REPORT), "--check"])
    assert r.returncode == 0, r.stdout + r.stderr
    assert "is current" in r.stdout


def test_conformance_report_excludes_research_files():
    """Research/ subdirectories inside Process Groups must NOT
    be treated as canonical records."""
    report = yaml.safe_load(
        (ROOT / "reconciliation" / "conformance_report.yaml").read_text()
    )
    for r in report["records"]:
        assert "/research/" not in r["path"], (
            f"research file leaked into canonical report: {r['path']}"
        )