"""Tests for scripts/check_entity_identity.py (EID-001..004).

Locks behaviour for the CR-BP-117a entity-identity clarity gate.

Authoritative reference: CR-BP-117 (2026-10-13, eaojnr).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_entity_identity.py"

sys.path.insert(0, str(ROOT / "scripts"))
from check_entity_identity import (  # noqa: E402
    evaluate,
    _ID_RE,
    _level_of,
    _level_name,
)


# ---------------------------------------------------------------------------
# Id-level inference
# ---------------------------------------------------------------------------


class TestLevelInference:
    @pytest.mark.parametrize("rid,expected", [
        ("processes:pc-pr-operate-aaaaaa", 0),
        ("processes:group-pr-operate-aaaaaa", 1),
        ("processes:process-pr-operate-aaaaaa", 2),
        ("processes:activity-pr-operate-aaaaaa", 3),
        ("processes:task-pr-operate-aaaaaa", 4),
        ("processes:scope-pr-operate-aaaaaa", 0),
    ])
    def test_known_tokens(self, rid, expected):
        assert _level_of(rid) == expected

    @pytest.mark.parametrize("rid", [
        "processes:unknown-pr-operate-aaaaaa",
        "dea:process-bad-id",
        "garbage",
        "",
    ])
    def test_unknown_returns_none(self, rid):
        assert _level_of(rid) is None


class TestLevelName:
    def test_l0_pc(self):
        assert _level_name("processes:pc-pr-operate-aaaaaa") == "L0 ProcessContext"

    def test_l1_group(self):
        assert _level_name("processes:group-pr-operate-aaaaaa") == "L1 ProcessGroup"

    def test_l2_process(self):
        assert _level_name("processes:process-pr-operate-aaaaaa") == "L2 Process"

    def test_l3_activity(self):
        assert _level_name("processes:activity-pr-operate-aaaaaa") == "L3 Activity"

    def test_l4_task(self):
        assert _level_name("processes:task-pr-operate-aaaaaa") == "L4 Task"


# ---------------------------------------------------------------------------
# EID-001 (same-level collisions)
# ---------------------------------------------------------------------------


def test_eid001_same_level_collision():
    """Two L2 processes with the same name -> EID-001 blocking."""
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        cell = root / "entities" / "v1-alpha" / "pr-operate"
        cell.mkdir(parents=True)
        (cell / "processes-process-pr-operate-aaaaaa.yaml").parent.mkdir(
            parents=True, exist_ok=True,
        )
        (cell / "processes-process-pr-operate-aaaaaa.yaml").write_text(
            "id: processes:process-pr-operate-aaaaaa\n"
            "name: Demand Operate\n"
            "type: Process\n"
            "version: 1.0.0\n"
        )
        (cell / "processes-process-pr-operate-bbbbbb.yaml").write_text(
            "id: processes:process-pr-operate-bbbbbb\n"
            "name: Demand Operate\n"
            "type: Process\n"
            "version: 1.0.0\n"
        )
        blocking, _ = evaluate(root)
        assert any(r == "EID-001" and "Demand Operate" in m for r, m in blocking)


def test_eid001_cross_level_allowed():
    """Same name at L0 and L1 -> NOT EID-001 (containment tree)."""
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        cell = root / "entities" / "v1-alpha" / "pr-operate"
        cell.mkdir(parents=True)
        (cell / "processes-pc-pr-operate-aaaaaa.yaml").write_text(
            "id: processes:pc-pr-operate-aaaaaa\n"
            "name: Demand Operate\n"
            "type: ProcessContext\n"
        )
        (cell / "processes-group-pr-operate-aaaaaa.yaml").write_text(
            "id: processes:group-pr-operate-aaaaaa\n"
            "name: Demand Operate\n"
            "type: ProcessGroup\n"
        )
        blocking, _ = evaluate(root)
        # EID-001 should NOT fire; EID-004 will fire (advisory).
        assert not any(r == "EID-001" for r, _ in blocking)


def test_eid004_reports_cross_level():
    """Cross-level name reuse -> EID-004 advisory."""
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        cell = root / "entities" / "v1-alpha" / "pr-operate"
        cell.mkdir(parents=True)
        (cell / "processes-pc-pr-operate-aaaaaa.yaml").write_text(
            "id: processes:pc-pr-operate-aaaaaa\n"
            "name: Demand Operate\n"
            "type: ProcessContext\n"
        )
        (cell / "processes-group-pr-operate-aaaaaa.yaml").write_text(
            "id: processes:group-pr-operate-aaaaaa\n"
            "name: Demand Operate\n"
            "type: ProcessGroup\n"
        )
        _, advisory = evaluate(root)
        assert any(r == "EID-004" and "Demand Operate" in m for r, m in advisory)


# ---------------------------------------------------------------------------
# Live repo
# ---------------------------------------------------------------------------


def test_live_no_same_level_collisions():
    """Live repo: 0 EID-001 same-level collisions (IDM-001 catches at write)."""
    blocking, _ = evaluate(ROOT)
    eid001 = [m for r, m in blocking if r == "EID-001"]
    assert not eid001, f"live repo has EID-001 hits: {eid001[:3]}"


def test_live_22_cross_level_inventory():
    """Live repo: 22 cross-level name collisions (per CR-BP-117 §1)."""
    _, advisory = evaluate(ROOT)
    eid004 = [m for r, m in advisory if r == "EID-004"]
    # The exact count can drift as records are added; assert range.
    assert 20 <= len(eid004) <= 30, (
        f"expected ~22 cross-level collisions; got {len(eid004)}"
    )


def test_live_eid002_id_in_first_line():
    """Live repo: every record README references the canonical id in line 1."""
    _, advisory = evaluate(ROOT)
    eid002 = [m for r, m in advisory if r == "EID-002"]
    assert not eid002, f"live repo has EID-002 hits: {eid002[:3]}"


def test_live_eid003_level_token_in_body():
    """Live repo: every record README surfaces the level token in body."""
    _, advisory = evaluate(ROOT)
    eid003 = [m for r, m in advisory if r == "EID-003"]
    assert not eid003, f"live repo has EID-003 hits: {eid003[:3]}"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_self_test_passes():
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--self-test"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert r.returncode == 0, (
        f"--self-test failed: stdout={r.stdout!r} stderr={r.stderr!r}"
    )


def test_cli_strict_clean_on_live():
    """Live repo under --strict must pass (advisory EID-004 is non-blocking)."""
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--strict"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert r.returncode == 0, (
        f"--strict failed: stdout={r.stdout[-500:]!r}"
    )


def test_cli_json_output_is_stable():
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--json"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert r.returncode == 0
    import json
    payload = json.loads(r.stdout)
    for key in ("gate", "verdict", "blocking", "advisory"):
        assert key in payload
    assert payload["gate"] == "EID-001..004"
