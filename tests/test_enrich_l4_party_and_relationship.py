"""
Tests for the PartyAndRelationship L4 Task content enrichment generator
(CR-BP-L4-02).

Covers:
  - Bounded-work table covers all 7 (stage, phase) pairs in scope.
  - BP-AR-004 capability-process avoidance (defensive: not triggered in P&R
    but the assertion must hold for any generated record).
  - Per-stage evidence grounding: every Task has 3 evidence entries drawn
    from the stage's governing-sector library.
  - Definition / trigger / outcome / responsibility / boundary.{inclusions,
    exclusions} fields are all populated and non-trivial on every Task.
  - Live-run validator conformance (check_task_model.py stays CONFORMANT,
    0 findings, 2800 records).
  - Idempotence: running the generator twice on the same checkout produces
    byte-identical output.
  - Scope filter: --scope SUFFIX restricts generation to a subset.
"""
from __future__ import annotations

import glob
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import enrich_l4_party_and_relationship as enrich  # noqa: E402

ENTITIES = ROOT / "entities" / "v1-alpha"
DOMAIN = "PartyAndRelationship"


def _pr_task_paths() -> list[Path]:
    """All PartyAndRelationship L4 Task yaml paths (CR-BP-mv1 tree)."""
    out = []
    for p in sorted(ENTITIES.rglob("processes-task-*.yaml")):
        if not p.is_file():
            continue
        with p.open() as f:
            d = yaml.safe_load(f)
        coord = d.get("ecfConformance", {}).get("canonicalReferences", [{}])[0]
        if coord.get("domain") == DOMAIN:
            out.append(p)
    return out


@pytest.fixture(scope="module", autouse=True)
def _ensure_live_enrichment_run():
    """Run the enrichment generator against the live tree once per test module.

    The post-run state is what the assertions validate. Idempotence is
    separately asserted in test_idempotence_running_twice_produces_identical_files.
    """
    result = subprocess.run(
        [sys.executable, "scripts/enrich_l4_party_and_relationship.py"],
        cwd=ROOT, capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, f"Live enrichment failed: {result.stderr}"
    yield


def _load_tasks(domain: str = DOMAIN) -> list[tuple[Path, dict]]:
    out = []
    for path in _pr_task_paths():
        with path.open() as f:
            out.append((path, yaml.safe_load(f)))
    return out


def _stage_phase(task: dict) -> tuple[str, str]:
    coord = task.get("ecfConformance", {}).get("canonicalReferences", [{}])[0]
    return coord.get("stage"), enrich._phase_from_task_id(task["id"])


# ---- bounded-work table coverage -----------------------------------------

def test_bounded_work_covers_all_pr_cells_and_phases():
    """Every (stage, phase) pair present in P&R Tasks must be in BOUNDED_WORK."""
    tasks = _load_tasks()
    pairs = {_stage_phase(t) for _, t in tasks}
    assert len(pairs) >= 7 * 5, f"Expected >=35 (stage, phase) pairs, got {len(pairs)}"
    for st, ph in pairs:
        assert (st, ph) in enrich.BOUNDED_WORK, \
            f"Missing bounded-work entry for ({st}, {ph})"


# ---- BP-AR-004 capability-process avoidance (defensive) -------------------

def test_no_task_definition_contains_capability_process():
    """No enriched Task definition may contain the forbidden 'capability process' substring.

    BP-AR-004 forbids the conflation; the P&R enrichment prose must not
    introduce it inadvertently (no P&R Activity ends in 'Capability' so
    the risk is low, but the assertion is defense-in-depth).
    """
    tasks = _load_tasks()
    offenders = []
    for path, t in tasks:
        defn = t.get("definition", "")
        if "capability process" in defn.lower():
            offenders.append((path.name, defn))
    assert offenders == [], f"BP-AR-004 violations: {offenders}"


# ---- evidence grounding ----------------------------------------------------

def test_every_task_has_three_evidence_entries():
    """Every enriched Task carries exactly 3 evidence[] entries (TASK-005 evidence[2+])."""
    tasks = _load_tasks()
    bad = []
    for path, t in tasks:
        ev = t.get("evidence", [])
        if len(ev) != 3:
            bad.append((path.name, len(ev)))
    assert bad == [], f"Tasks with != 3 evidence entries: {bad}"


def test_evidence_strength_values_are_e1_e2_or_e3():
    tasks = _load_tasks()
    allowed = {"E1", "E2", "E3"}
    bad = []
    for path, t in tasks:
        for ev in t.get("evidence", []):
            if ev.get("strength") not in allowed:
                bad.append((path.name, ev))
    assert bad == [], f"Bad evidence strength: {bad}"


def test_evidence_cites_governing_sector_source_per_stage():
    """Each Task's evidence[] must cite at least one source drawn from the
    stage's governing-sector library in STAGE_EVIDENCE."""
    tasks = _load_tasks()
    bad = []
    for path, t in tasks:
        st, _ = _stage_phase(t)
        allowed_sources = {s["source"] for s in enrich.STAGE_EVIDENCE[st]}
        cited = {ev.get("source") for ev in t.get("evidence", [])}
        if not (cited & allowed_sources):
            bad.append((path.name, st, sorted(cited)))
    assert bad == [], f"Tasks missing governing-sector evidence: {bad}"


# ---- field population ------------------------------------------------------

def test_all_required_prose_fields_populated():
    """definition, trigger, outcome, responsibility, boundary.inclusions[2+],
    boundary.exclusions[2+] all populated on every Task."""
    tasks = _load_tasks()
    bad = []
    for path, t in tasks:
        if len(t.get("definition", "")) < 80:
            bad.append((path.name, "definition too short"))
        if len(t.get("trigger", "")) < 40:
            bad.append((path.name, "trigger too short"))
        if len(t.get("outcome", "")) < 40:
            bad.append((path.name, "outcome too short"))
        if not t.get("responsibility"):
            bad.append((path.name, "responsibility empty"))
        b = t.get("boundary", {})
        if len(b.get("inclusions", [])) < 2:
            bad.append((path.name, "boundary.inclusions < 2"))
        if len(b.get("exclusions", [])) < 2:
            bad.append((path.name, "boundary.exclusions < 2"))
    assert bad == [], f"Bad prose fields: {bad}"


# ---- count assertions ------------------------------------------------------

def test_live_catalog_count_is_220_pr_tasks():
    """220 PartyAndRelationship L4 Tasks across 7 cells (44 Activities x 5 phases)."""
    tasks = _load_tasks()
    assert len(tasks) == 220, f"Expected 220 P&R Tasks, got {len(tasks)}"


def test_live_catalog_count_per_stage():
    """Per-stage counts match the expected decomposition (Activate/Improve/
    Operate/Retire = 20; Build/Conceive = 40; Design = 60)."""
    tasks = _load_tasks()
    by_stage = {}
    for _, t in tasks:
        st, _ = _stage_phase(t)
        by_stage[st] = by_stage.get(st, 0) + 1
    assert by_stage == {
        "Activate": 20,
        "Build": 40,
        "Conceive": 40,
        "Design": 60,
        "Improve": 20,
        "Operate": 20,
        "Retire": 20,
    }, f"Per-stage counts drifted: {by_stage}"


# ---- validator conformance (live-run) --------------------------------------

def test_live_run_check_task_model_conformant():
    """The L4 Task validator must report CONFORMANT, 0 findings, 2800 records
    after the enrichment lands (regression: check the generator didn't break
    the existing 2800-record surface)."""
    result = subprocess.run(
        [sys.executable, "scripts/check_task_model.py"],
        cwd=ROOT, capture_output=True, text=True, timeout=180,
    )
    out = (result.stdout or "") + (result.stderr or "")
    assert "Records checked:  2800" in out, f"Count drift: {out}"
    assert "Findings:         0" in out, f"Findings not 0: {out}"
    assert "CONFORMANT" in out, f"Not conformant: {out}"


# ---- idempotence -----------------------------------------------------------

def test_idempotence_running_twice_produces_identical_files(tmp_path):
    """Running the generator against the live tree and then again must leave
    every P&R Task yaml byte-identical to the post-first-run state.

    We snapshot the first run's output to tmp_path, run again, and diff.
    """
    targets = _pr_task_paths()
    # Snapshot
    snapshot = {p: p.read_bytes() for p in targets}

    # Run the generator (live mode)
    result = subprocess.run(
        [sys.executable, "scripts/enrich_l4_party_and_relationship.py"],
        cwd=ROOT, capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, f"Generator failed: {result.stderr}"

    # Second run must produce the same bytes
    result2 = subprocess.run(
        [sys.executable, "scripts/enrich_l4_party_and_relationship.py"],
        cwd=ROOT, capture_output=True, text=True, timeout=120,
    )
    assert result2.returncode == 0, f"Second run failed: {result2.stderr}"

    for p in targets:
        after = p.read_bytes()
        assert after == snapshot[p], f"Drift after second run: {p.name}"


# ---- scope filter ----------------------------------------------------------

def test_scope_filter_restricts_writes(tmp_path):
    """--scope SUFFIX must restrict the generator to paths containing the
    substring (dry-run only: no on-disk mutation).

    CR-BP-mv1: task paths no longer carry human-readable activity slugs;
    the activity directory name (`<cell>-<hash>`) is the unique scope token
    for one Activity's 5 Tasks.
    """
    result = subprocess.run(
        [sys.executable, "scripts/enrich_l4_party_and_relationship.py",
         "--dry-run", "--scope", "pr-activate-y46zs2"],
        cwd=ROOT, capture_output=True, text=True, timeout=60,
    )
    out = result.stdout
    # Only 5 Tasks should match the scope (1 Activity x 5 phases)
    assert "tasks_written: 5" in out, f"Scope filter wrong: {out}"