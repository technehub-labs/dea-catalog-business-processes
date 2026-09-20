"""
Tests for the GovernanceAndExistence L4 Task content enrichment generator
(CR-BP-L4-03).

Covers:
  - Bounded-work table covers all (stage, phase) pairs in scope.
  - BP-AR-004 capability-process avoidance (defensive).
  - Per-stage evidence grounding: every Task has 3 evidence entries drawn
    from the stage's governing-sector library.
  - Definition / trigger / outcome / responsibility / boundary.{inclusions,
    exclusions} fields populated on every Task.
  - Live-run validator conformance (check_task_model.py stays CONFORMANT,
    0 findings, 2800 records).
  - Idempotence: running the generator twice produces byte-identical output.
  - Scope filter: --scope SUFFIX restricts generation to a subset.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import enrich_l4_governance_and_existence as enrich  # noqa: E402

ENTITIES = ROOT / "entities" / "v1-alpha"
DOMAIN = "GovernanceAndExistence"


def _ge_task_paths() -> list[Path]:
    out = []
    for p in sorted(ENTITIES.glob("dea:task-*")):
        with (p / f"{p.name}.yaml").open() as f:
            d = yaml.safe_load(f)
        coord = d.get("ecfConformance", {}).get("canonicalReferences", [{}])[0]
        if coord.get("domain") == DOMAIN:
            out.append(p / f"{p.name}.yaml")
    return out


@pytest.fixture(scope="module", autouse=True)
def _ensure_live_enrichment_run():
    result = subprocess.run(
        [sys.executable, "scripts/enrich_l4_governance_and_existence.py"],
        cwd=ROOT, capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, f"Live enrichment failed: {result.stderr}"
    yield


def _load_tasks(domain: str = DOMAIN) -> list[tuple[Path, dict]]:
    out = []
    for path in _ge_task_paths():
        with path.open() as f:
            out.append((path, yaml.safe_load(f)))
    return out


def _stage_phase(task: dict) -> tuple[str, str]:
    coord = task.get("ecfConformance", {}).get("canonicalReferences", [{}])[0]
    return coord.get("stage"), enrich._phase_from_task_id(task["id"])


def test_bounded_work_covers_all_ge_cells_and_phases():
    tasks = _load_tasks()
    pairs = {_stage_phase(t) for _, t in tasks}
    assert len(pairs) >= 7 * 5, f"Expected >=35 (stage, phase) pairs, got {len(pairs)}"
    for st, ph in pairs:
        assert (st, ph) in enrich.BOUNDED_WORK, \
            f"Missing bounded-work entry for ({st}, {ph})"


def test_no_task_definition_contains_capability_process():
    tasks = _load_tasks()
    offenders = []
    for path, t in tasks:
        defn = t.get("definition", "")
        if "capability process" in defn.lower():
            offenders.append((path.name, defn))
    assert offenders == [], f"BP-AR-004 violations: {offenders}"


def test_every_task_has_three_evidence_entries():
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
    tasks = _load_tasks()
    bad = []
    for path, t in tasks:
        st, _ = _stage_phase(t)
        allowed_sources = {s["source"] for s in enrich.STAGE_EVIDENCE[st]}
        cited = {ev.get("source") for ev in t.get("evidence", [])}
        if not (cited & allowed_sources):
            bad.append((path.name, st, sorted(cited)))
    assert bad == [], f"Tasks missing governing-sector evidence: {bad}"


def test_all_required_prose_fields_populated():
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


def test_live_catalog_count_is_340_ge_tasks():
    """340 GovernanceAndExistence L4 Tasks across 7 cells (68 Activities x 5 phases)."""
    tasks = _load_tasks()
    assert len(tasks) == 340, f"Expected 340 G&E Tasks, got {len(tasks)}"


def test_live_catalog_count_per_stage():
    """Per-stage counts match the expected decomposition (Activate/Retire = 20;
    Conceive = 40; Build/Design/Improve = 60; Operate = 80)."""
    tasks = _load_tasks()
    by_stage = {}
    for _, t in tasks:
        st, _ = _stage_phase(t)
        by_stage[st] = by_stage.get(st, 0) + 1
    assert by_stage == {
        "Activate": 20,
        "Build": 60,
        "Conceive": 40,
        "Design": 60,
        "Improve": 60,
        "Operate": 80,
        "Retire": 20,
    }, f"Per-stage counts drifted: {by_stage}"


def test_live_run_check_task_model_conformant():
    """The L4 Task validator must report CONFORMANT, 0 findings, 2800 records
    after the enrichment lands."""
    result = subprocess.run(
        [sys.executable, "scripts/check_task_model.py"],
        cwd=ROOT, capture_output=True, text=True, timeout=180,
    )
    out = (result.stdout or "") + (result.stderr or "")
    assert "Records checked:  2800" in out, f"Count drift: {out}"
    assert "Findings:         0" in out, f"Findings not 0: {out}"
    assert "CONFORMANT" in out, f"Not conformant: {out}"


def test_idempotence_running_twice_produces_identical_files():
    targets = _ge_task_paths()
    snapshot = {p: p.read_bytes() for p in targets}

    result = subprocess.run(
        [sys.executable, "scripts/enrich_l4_governance_and_existence.py"],
        cwd=ROOT, capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, f"Generator failed: {result.stderr}"

    result2 = subprocess.run(
        [sys.executable, "scripts/enrich_l4_governance_and_existence.py"],
        cwd=ROOT, capture_output=True, text=True, timeout=120,
    )
    assert result2.returncode == 0, f"Second run failed: {result2.stderr}"

    for p in targets:
        after = p.read_bytes()
        assert after == snapshot[p], f"Drift after second run: {p.name}"


def test_scope_filter_restricts_writes():
    """--scope SUFFIX must restrict the generator to paths containing the
    substring (dry-run only: no on-disk mutation)."""
    result = subprocess.run(
        [sys.executable, "scripts/enrich_l4_governance_and_existence.py",
         "--dry-run", "--scope", "run-board-and-committee-cycles"],
        cwd=ROOT, capture_output=True, text=True, timeout=60,
    )
    out = result.stdout
    assert "tasks_written: 5" in out, f"Scope filter wrong: {out}"