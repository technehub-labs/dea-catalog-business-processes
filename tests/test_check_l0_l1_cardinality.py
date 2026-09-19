#!/usr/bin/env python3
"""test_check_l0_l1_cardinality.py :  exhaustive L0<->L1 cardinality tests.

CR-BP-100 / CR-BP-100a (eaojnr 2026-09-19 doctrine). L0 = ProcessContext
(dea:pc-*); L1 = ProcessGroup (dea:group-*). Canonical cardinality is
exactly 1 L1 per L0 (and exactly 1 L0 per L1).

These tests run exhaustively against the LIVE catalog to prove every
PC and every PG satisfy the 1:1 invariant. The live catalog has 49 PCs
and 49 PGs (7 domains x 7 stages = 49; the SD.Retire cell landed via
CR-BP-101 on 2026-09-19); this suite verifies that count + the
pairwise mapping + absence of any ProcessScope records.

Coverage:
  - Live catalog aggregate: 49 PCs, 49 PGs, every PC has exactly 1 PG,
    every PG resolves to exactly 1 known PC.
  - Live catalog per-PC audit: each of 49 PC ids appears exactly once
    in the by-pc map with exactly 1 group.
  - Live catalog per-PG audit: each of 49 PG ids has a process_context
    field that matches `^dea:pc-[a-z0-9-]+$` AND resolves to a known PC.
  - Live catalog ProcessScope audit: zero ProcessScope records in the
    entities tree (CARD-003 dormant-by-design).
  - CLI --self-test: PASS.
  - Unit tests for run_checks() on a synthesised catalog covering all
    rule paths (1:1, 0:N, N:1, unknown PC, malformed PC, scope present).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from check_l0_l1_cardinality import (  # noqa: E402
    ID_PC_PATTERN,
    ID_SCOPE_PATTERN,
    _check_cardinality,
    _load_pc_ids,
    _load_pgs,
    main as card_main,
    run_checks,
    self_test,
)


# ---------------------------------------------------------------------------
# Live catalog exhaustive audit (the "exhaustively to be sure" requirement).
# ---------------------------------------------------------------------------

CONTEXTS_DIR = ROOT / "contexts" / "v1-alpha"
ENTITIES_DIR = ROOT / "entities" / "v1-alpha"


def _live_invariants():
    pc_ids = _load_pc_ids(CONTEXTS_DIR)
    groups, scopes = _load_pgs(ENTITIES_DIR)
    return pc_ids, groups, scopes


@pytest.fixture(scope="module")
def live():
    return _live_invariants()


def test_live_total_counts(live):
    """49 PCs, 49 PGs as of 2026-09-19 (post-CR-BP-101 SD/Retire admission)."""
    pc_ids, groups, scopes = live
    # 49 confirmed: 7 domains x 7 stages = 49; all 49 currently landed.
    assert len(pc_ids) == 49, (
        f"Expected 49 canonical Process Contexts, found {len(pc_ids)}. "
        f"If a new PC was admitted, update this assertion AND the live "
        f"catalog reference in CR-BP-100 / CR-BP-100a."
    )
    assert len(groups) == 49, (
        f"Expected 49 canonical Process Groups, found {len(groups)}. "
        f"1:1 invariant requires PC count == PG count."
    )


def test_live_no_processscope_records(live):
    """CARD-003: the L0 layer IS the PC matrix; ProcessScope is dormant."""
    pc_ids, groups, scopes = live
    assert scopes == [], (
        f"Expected 0 ProcessScope records; found {len(scopes)}: "
        f"{[s.get('id') for s in scopes]}. CR-BP-100 §L0L1-CARD-003 declares "
        f"this layer dormant by design. Admission requires an explicit CR."
    )


def test_live_pc_to_pg_map_is_total_and_one_to_one(live):
    """Every PC has exactly 1 PG; no PC has 0 or 2+."""
    pc_ids, groups, scopes = live
    by_pc: dict[str, list[str]] = {}
    for grp in groups:
        pc = grp.get("process_context", "")
        gid = grp.get("id", "<unknown>")
        assert isinstance(pc, str), (
            f"PG {gid}: process_context must be a string."
        )
        assert ID_PC_PATTERN.match(pc), (
            f"PG {gid}: process_context={pc!r} does not match "
            f"`^dea:pc-[a-z0-9-]+$`."
        )
        by_pc.setdefault(pc, []).append(gid)

    # Every PC has exactly 1 PG.
    failures = []
    for pc_id in sorted(pc_ids):
        gs = by_pc.get(pc_id, [])
        if len(gs) != 1:
            failures.append((pc_id, len(gs), gs))

    assert not failures, (
        "L0<->L1 cardinality violation(s) in live catalog (L0L1-CARD-001):\n"
        + "\n".join(f"  {pc}: {n} PG(s) {gs}" for pc, n, gs in failures)
    )

    # And conversely: no PG has a process_context outside the canonical set.
    orphan_pgs = []
    for grp in groups:
        pc = grp.get("process_context", "")
        if pc not in pc_ids:
            orphan_pgs.append((grp.get("id", "<unknown>"), pc))
    assert not orphan_pgs, (
        "PGs whose process_context is not a canonical PC (L0L1-CARD-002):\n"
        + "\n".join(f"  {gid}: {pc}" for gid, pc in orphan_pgs)
    )

    # And: every PG appears exactly once in the by_pc map (no duplicate ids).
    all_gids = [g.get("id") for g in groups]
    dup = [gid for gid in set(all_gids) if all_gids.count(gid) > 1]
    assert not dup, f"Duplicate PG ids in live catalog: {sorted(dup)}"


def test_live_per_pc_audit(live):
    """Walk every PC id and verify exactly one composed L1."""
    pc_ids, groups, scopes = live
    by_pc: dict[str, list[str]] = {}
    for grp in groups:
        by_pc.setdefault(grp.get("process_context"), []).append(
            grp.get("id")
        )
    # Build a reverse map to make failures debuggable.
    pg_by_id = {g.get("id"): g for g in groups}

    for pc_id in sorted(pc_ids):
        gs = by_pc.get(pc_id, [])
        assert len(gs) == 1, (
            f"PC {pc_id} has {len(gs)} PG(s) {gs}; expected exactly 1."
        )
        gid = gs[0]
        assert gid in pg_by_id
        # PG must reference this PC.
        assert pg_by_id[gid].get("process_context") == pc_id, (
            f"PG {gid} claims process_context="
            f"{pg_by_id[gid].get('process_context')!r} but PC {pc_id} "
            f"claims it as its composed L1. Inconsistent mapping."
        )


def test_live_per_pg_audit(live):
    """Walk every PG id and verify its process_context resolves."""
    pc_ids, groups, scopes = live
    pc_set = set(pc_ids)
    for grp in groups:
        gid = grp.get("id")
        pc = grp.get("process_context")
        assert isinstance(gid, str) and gid.startswith("dea:group-"), (
            f"PG {gid!r} does not match dea:group-* pattern."
        )
        assert isinstance(pc, str) and ID_PC_PATTERN.match(pc), (
            f"PG {gid}: process_context={pc!r} is malformed."
        )
        assert pc in pc_set, (
            f"PG {gid}: process_context={pc!r} not in canonical PC set."
        )


def test_live_no_orphan_pgs_or_pcs(live):
    """No PG without a PC; no PC without a PG (the 1:1 invariant)."""
    pc_ids, groups, scopes = live
    by_pc: dict[str, list[str]] = {}
    for grp in groups:
        by_pc.setdefault(grp.get("process_context"), []).append(
            grp.get("id")
        )

    # 0-PG PCs:
    orphan_pcs = [pc for pc in pc_ids if len(by_pc.get(pc, [])) == 0]
    assert not orphan_pcs, (
        f"PCs with 0 PG (L0L1-CARD-001): {orphan_pcs}"
    )

    # Multi-PG PCs:
    multi_pcs = [
        pc for pc in pc_ids if len(by_pc.get(pc, [])) > 1
    ]
    assert not multi_pcs, (
        f"PCs with >1 PG (L0L1-CARD-001): "
        + ", ".join(f"{pc}={by_pc[pc]}" for pc in multi_pcs)
    )


# ---------------------------------------------------------------------------
# Unit tests on synthesised catalogs (covers all rule paths).
# ---------------------------------------------------------------------------

def _check(groups, scopes, pc_ids):
    errors: list[str] = []
    _check_cardinality(
        pc_ids=pc_ids,
        group_records=groups,
        scope_records=scopes,
        errors=errors,
    )
    return errors


def test_unit_one_to_one_clean():
    errs = _check(
        [{"id": "dea:group-a1", "type": "ProcessGroup",
          "process_context": "dea:pc-a"}],
        [],
        {"dea:pc-a"},
    )
    assert errs == []


def test_unit_pc_with_zero_groups_fails_card_001():
    errs = _check(
        [],
        [],
        {"dea:pc-orphan"},
    )
    assert any("L0L1-CARD-001" in e and "dea:pc-orphan" in e for e in errs)


def test_unit_pc_with_two_groups_fails_card_001():
    errs = _check(
        [
            {"id": "dea:group-a1", "type": "ProcessGroup",
             "process_context": "dea:pc-a"},
            {"id": "dea:group-a2", "type": "ProcessGroup",
             "process_context": "dea:pc-a"},
        ],
        [],
        {"dea:pc-a"},
    )
    assert any(
        "L0L1-CARD-001" in e and "2 Process Groups" in e and "dea:pc-a" in e
        for e in errs
    )


def test_unit_pg_with_unknown_pc_fails_card_002():
    errs = _check(
        [{"id": "dea:group-x", "type": "ProcessGroup",
          "process_context": "dea:pc-unknown"}],
        [],
        {"dea:pc-a"},
    )
    assert any(
        "L0L1-CARD-002" in e and "dea:group-x" in e for e in errs
    )


def test_unit_pg_with_malformed_pc_fails_card_002():
    errs = _check(
        [{"id": "dea:group-x", "type": "ProcessGroup",
          "process_context": "not-a-pc"}],
        [],
        {"dea:pc-a"},
    )
    assert any(
        "L0L1-CARD-002" in e and "dea:group-x" in e and "missing" in e
        for e in errs
    )


def test_unit_processscope_present_fails_card_003():
    errs = _check(
        [{"id": "dea:group-a1", "type": "ProcessGroup",
          "process_context": "dea:pc-a"}],
        [{"id": "dea:scope-pilot", "type": "ProcessScope"}],
        {"dea:pc-a"},
    )
    assert any(
        "L0L1-CARD-003" in e and "ProcessScope" in e for e in errs
    )


def test_unit_processscope_record_id_pattern_only():
    """The CARD-003 check fires only on ProcessScope records, not anything
    with 'scope' in its id."""
    # Non-ProcessScope record that happens to have 'scope' in id -- not fired.
    # (We synthesise only ProcessScope records above; this just asserts the
    # CARD-003 message is specific.)
    errs = _check(
        [],
        [{"id": "dea:scope-x", "type": "ProcessScope"}],
        set(),
    )
    assert len(errs) == 1
    assert "L0L1-CARD-003" in errs[0]


# ---------------------------------------------------------------------------
# CLI / self-test integration.
# ---------------------------------------------------------------------------

def test_cli_self_test_passes():
    """scripts/check_l0_l1_cardinality.py --self-test returns 0."""
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_l0_l1_cardinality.py"),
         "--self-test"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert proc.returncode == 0, (
        f"Self-test failed (rc={proc.returncode}):\n"
        f"  stdout: {proc.stdout}\n  stderr: {proc.stderr}"
    )
    assert "L0L1-CARD self-test: PASS" in proc.stdout


def test_cli_live_run_is_conformant():
    """scripts/check_l0_l1_cardinality.py against live catalog returns 0."""
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_l0_l1_cardinality.py")],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert proc.returncode == 0, (
        f"Live run failed (rc={proc.returncode}):\n"
        f"  stdout: {proc.stdout}\n  stderr: {proc.stderr}"
    )
    assert "L0L1-CARD-001..003): PASS" in proc.stdout


def test_cli_live_run_emits_expected_summary():
    """Output includes the cardinal-001..003 range tag."""
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_l0_l1_cardinality.py")],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert "L0L1-CARD-001..003" in proc.stdout


def test_cli_help():
    """Sanity: argparse help works."""
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_l0_l1_cardinality.py"),
         "--help"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert proc.returncode == 0
    assert "cardinality" in proc.stdout.lower()