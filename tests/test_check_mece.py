"""Tests for the CR-BP-36 MECE Validation validator.

Locks behaviour for MECE-001..008 by exercising both the in-process
`evaluate()` function and the CLI self-test entry point, plus a
live-catalog assertion that all 161 records currently emit zero
findings (the catalog is fully aligned after the MECE-008
remediation in this slice).

The tests cover:

* MECE-001  every register-landed coordinate has a PC record
* MECE-002  every PC has at least one PG referencing it
* MECE-003  every PG composes at least one BP
* MECE-004  no two BPs share the same (identity.verb, identity.object)
* MECE-005  no two PGs share the same (process_context, name)
* MECE-006  every register-landed coordinate has at least one PG
* MECE-007  every PG references an existing PC (no orphans)
* MECE-008  every non-deprecated BP is composed by at least one PG
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
SCRIPT = ROOT / "scripts" / "check_mece.py"

sys.path.insert(0, str(ROOT / "scripts"))
from check_mece import (  # noqa: E402
    _check_mece_001,
    _check_mece_002,
    _check_mece_003,
    _check_mece_004,
    _check_mece_005,
    _check_mece_006,
    _check_mece_007,
    _check_mece_008,
    evaluate,
)


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=False,
        capture_output=True,
        text=True,
    )


# -----------------------------------------------------------------------------
# CLI-level tests
# -----------------------------------------------------------------------------


def test_cli_self_test_passes():
    result = _run(["--self-test"])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "self-test PASS" in result.stdout


def test_cli_live_run_returns_conformant():
    """Live run: 161 records, 0 findings (after MECE-008 remediation)."""
    result = _run([])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "MECE Validation (CR-BP-36; MECE-001..008): CONFORMANT" in result.stdout
    assert "Findings: 0" in result.stdout


def test_cli_json_shape():
    result = _run(["--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert data["verdict"] == "CONFORMANT"
    assert data["finding_count"] == 0
    rule_ids = {r["id"] for r in data["rules"]}
    assert "MECE-001" in rule_ids
    assert "MECE-008" in rule_ids


def test_cli_strict_mode_fails_on_findings(tmp_path):
    """--strict exits 1 when a genuine MECE violation exists."""
    # Build a minimal catalog with an orphan BP
    v1 = tmp_path / "entities" / "v1-alpha" / "pr-operate"
    v1.mkdir(parents=True)
    bp_dir = v1 / "pr-operate-orphan1"
    bp_dir.mkdir()
    (bp_dir / "processes-process-pr-operate-orphan1.yaml").write_text(yaml.safe_dump({
        "id": "processes:process-pr-operate-orphan1",
        "name": "Orphan Process",
        "type": "Process",
        "version": "1.0.0",
        "identity": {"verb": "Orphan", "object": "Process"},
        "lifecycle_status": "candidate",
    }))
    result = subprocess.run(
        [sys.executable, str(SCRIPT),
         "--catalog-root", str(tmp_path), "--strict"],
        check=False, capture_output=True, text=True,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    assert "NON-CONFORMANT" in result.stdout
    assert "MECE-008" in result.stdout


# -----------------------------------------------------------------------------
# Rule-level tests (unit)
# -----------------------------------------------------------------------------


def _make_pc(id_, domain, stage):
    return {"id": id_, "domain": domain, "lifecycle_stage": stage,
            "name": f"{domain} x {stage}"}


def _make_pg(id_, pc_ref, name, composes_targets=None):
    composes = []
    if composes_targets:
        for t in composes_targets:
            composes.append({
                "source_id": id_,
                "target_id": t,
                "relationship_type": "dea:composes",
            })
    return {"id": id_, "name": name, "type": "ProcessGroup",
            "version": "1.0.0", "process_context": pc_ref,
            "composes": composes}


def _make_bp(id_, verb, obj, lifecycle_status="candidate"):
    return {"id": id_, "name": f"{verb} {obj}", "type": "Process",
            "version": "1.0.0",
            "identity": {"verb": verb, "object": obj},
            "lifecycle_status": lifecycle_status}


def test_mece_001_missing_pc():
    register_coords = {("D1", "S1"): "processes:pc-d1-s1"}
    pc_index = {}
    findings = _check_mece_001(register_coords, pc_index)
    assert len(findings) == 1
    assert "D1" in findings[0] and "S1" in findings[0]


def test_mece_001_pc_exists():
    register_coords = {("D1", "S1"): "processes:pc-d1-s1"}
    pc_index = {("D1", "S1"): "processes:pc-d1-s1"}
    assert _check_mece_001(register_coords, pc_index) == []


def test_mece_002_pc_without_pg():
    pc_pairs = [(Path("/x"), _make_pc("processes:pc-d1-s1", "D1", "S1"))]
    pg_pc_index = {}
    findings = _check_mece_002(pc_pairs, pg_pc_index)
    assert len(findings) == 1


def test_mece_002_pc_with_pg():
    pc_pairs = [(Path("/x"), _make_pc("processes:pc-d1-s1", "D1", "S1"))]
    pg_pc_index = {"processes:pc-d1-s1": ["processes:group-g1"]}
    assert _check_mece_002(pc_pairs, pg_pc_index) == []


def test_mece_003_pg_without_bp():
    pg_pairs = [(Path("/x"), _make_pg("processes:group-g1", "processes:pc-d1-s1", "G1"))]
    bp_ids = set()
    findings = _check_mece_003(pg_pairs, bp_ids)
    assert len(findings) == 1


def test_mece_003_pg_with_bp():
    pg_pairs = [(Path("/x"), _make_pg("processes:group-g1", "processes:pc-d1-s1", "G1",
                                     composes_targets=["processes:process-b1"]))]
    bp_ids = {"processes:process-b1"}
    assert _check_mece_003(pg_pairs, bp_ids) == []


def test_mece_004_duplicate_identity():
    bp_pairs = [
        (Path("/x"), _make_bp("processes:process-b1", "Manage", "Thing")),
        (Path("/y"), _make_bp("processes:process-b2", "manage", "thing")),
    ]
    findings = _check_mece_004(bp_pairs)
    assert len(findings) == 1
    assert "b2" in findings[0]


def test_mece_004_unique_identity():
    bp_pairs = [
        (Path("/x"), _make_bp("processes:process-b1", "Manage", "Thing")),
        (Path("/y"), _make_bp("processes:process-b2", "Manage", "Other")),
    ]
    assert _check_mece_004(bp_pairs) == []


def test_mece_005_duplicate_pc_name():
    pg_pairs = [
        (Path("/x"), _make_pg("processes:group-g1", "processes:pc-d1-s1", "Group One")),
        (Path("/y"), _make_pg("processes:group-g2", "processes:pc-d1-s1", "group one")),
    ]
    findings = _check_mece_005(pg_pairs)
    assert len(findings) == 1


def test_mece_005_different_name_passes():
    pg_pairs = [
        (Path("/x"), _make_pg("processes:group-g1", "processes:pc-d1-s1", "Group One")),
        (Path("/y"), _make_pg("processes:group-g2", "processes:pc-d1-s1", "Group Two")),
    ]
    assert _check_mece_005(pg_pairs) == []


def test_mece_005_different_pc_passes():
    pg_pairs = [
        (Path("/x"), _make_pg("processes:group-g1", "processes:pc-d1-s1", "Group One")),
        (Path("/y"), _make_pg("processes:group-g2", "processes:pc-d2-s2", "Group One")),
    ]
    assert _check_mece_005(pg_pairs) == []


def test_mece_006_register_coordinate_without_pg():
    register_coords = {("D1", "S1"): "processes:pc-d1-s1"}
    pc_index = {("D1", "S1"): "processes:pc-d1-s1"}
    pg_pc_index = {}
    findings = _check_mece_006(register_coords, pc_index, pg_pc_index)
    assert len(findings) == 1


def test_mece_006_register_coordinate_with_pg():
    register_coords = {("D1", "S1"): "processes:pc-d1-s1"}
    pc_index = {("D1", "S1"): "processes:pc-d1-s1"}
    pg_pc_index = {"processes:pc-d1-s1": ["processes:group-g1"]}
    assert _check_mece_006(register_coords, pc_index, pg_pc_index) == []


def test_mece_007_orphan_pg():
    pg_pairs = [(Path("/x"), _make_pg("processes:group-g1", "processes:pc-nonexistent", "G1"))]
    pc_ids = {"processes:pc-d1-s1"}
    findings = _check_mece_007(pg_pairs, pc_ids)
    assert len(findings) == 1
    assert "nonexistent" in findings[0]


def test_mece_007_valid_pg():
    pg_pairs = [(Path("/x"), _make_pg("processes:group-g1", "processes:pc-d1-s1", "G1"))]
    pc_ids = {"processes:pc-d1-s1"}
    assert _check_mece_007(pg_pairs, pc_ids) == []


def test_mece_008_orphan_bp():
    bp_pairs = [(Path("/x"), _make_bp("processes:process-b1", "Manage", "Thing"))]
    bp_composed_by = {}
    findings = _check_mece_008(bp_pairs, bp_composed_by)
    assert len(findings) == 1


def test_mece_008_composed_bp():
    bp_pairs = [(Path("/x"), _make_bp("processes:process-b1", "Manage", "Thing"))]
    bp_composed_by = {"processes:process-b1": ["processes:group-g1"]}
    assert _check_mece_008(bp_pairs, bp_composed_by) == []


def test_mece_008_deprecated_bp_exempt():
    bp_pairs = [(Path("/x"), _make_bp("processes:process-b1", "Old", "Thing",
                                      lifecycle_status="deprecated"))]
    bp_composed_by = {}
    assert _check_mece_008(bp_pairs, bp_composed_by) == []


def test_mece_008_candidate_bp_not_exempt():
    bp_pairs = [(Path("/x"), _make_bp("processes:process-b1", "New", "Thing",
                                      lifecycle_status="candidate"))]
    bp_composed_by = {}
    findings = _check_mece_008(bp_pairs, bp_composed_by)
    assert len(findings) == 1
