"""Tests for CR-BP-15-IMP Phase 3-4 disposition register + tranche plan.

Locks behaviour for `scripts/check_dispositions.py`:
- every inventory Business Process has exactly one disposition entry;
- every disposition id is in the canonical 9;
- RECLASSIFY changes conform to the CR-BP-14 axes and canonical
  vocabularies;
- tranche plan entries reference disposition entries.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "check_dispositions.py"), *args],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )


def test_self_test_passes() -> None:
    res = _run("--self-test")
    assert res.returncode == 0, res.stderr
    assert "PASS" in res.stdout


def test_disposition_register_is_locked() -> None:
    """Every Business Process in inventory has exactly one disposition."""
    inv = yaml.safe_load(
        (REPO_ROOT / "reconciliation/inventory.yaml").read_text()
    )
    reg = yaml.safe_load(
        (REPO_ROOT / "reconciliation/dispositions/register.yaml").read_text()
    )
    bp_ids = {r["id"] for r in inv["records"]["business_processes"]}
    reg_ids = {d["record_id"] for d in reg["dispositions"]}
    assert bp_ids == reg_ids, (
        f"missing={bp_ids - reg_ids}; extra={reg_ids - bp_ids}"
    )


def test_all_disposition_ids_canonical() -> None:
    """Every disposition is one of the 9 canonical ids."""
    valid = {"RETAIN", "RECLASSIFY", "RENAME", "SPECIALIZE",
             "MERGE", "SPLIT", "MOVE", "DEFER", "RETIRE"}
    reg = yaml.safe_load(
        (REPO_ROOT / "reconciliation/dispositions/register.yaml").read_text()
    )
    bad = [d for d in reg["dispositions"]
           if d.get("disposition") not in valid]
    assert not bad, f"non-canonical disposition ids: {bad}"


def test_all_reclassify_changes_use_canonical_axes() -> None:
    """Every RECLASSIFY change references a CR-BP-14 semantic axis."""
    valid_axes = {"process_intent", "process_type", "process_context",
                  "process_specialization", "process_audience"}
    reg = yaml.safe_load(
        (REPO_ROOT / "reconciliation/dispositions/register.yaml").read_text()
    )
    for d in reg["dispositions"]:
        if d.get("disposition") != "RECLASSIFY":
            continue
        for change in d.get("changes", []):
            assert change.get("axis") in valid_axes, (
                f"{d['record_id']}: axis {change.get('axis')!r} invalid"
            )


def test_all_reclassify_intent_targets_canonical() -> None:
    """Every RECLASSIFY intent target is a canonical Process Intent."""
    canonical = {"govern", "manage", "operate", "deliver",
                 "support", "develop", "transform"}
    reg = yaml.safe_load(
        (REPO_ROOT / "reconciliation/dispositions/register.yaml").read_text()
    )
    for d in reg["dispositions"]:
        if d.get("disposition") != "RECLASSIFY":
            continue
        for change in d.get("changes", []):
            if change.get("axis") == "process_intent":
                target = change.get("to")
                assert target in canonical, (
                    f"{d['record_id']}: intent -> {target!r} not canonical"
                )


def test_all_reclassify_context_targets_resolve() -> None:
    """Every RECLASSIFY context target is a valid Process Context id."""
    reg = yaml.safe_load(
        (REPO_ROOT / "reconciliation/dispositions/register.yaml").read_text()
    )
    ctx_files = list((REPO_ROOT / "contexts/v1-alpha").glob("dea-*.yaml")) + \
        list((REPO_ROOT / "contexts/v1-alpha").glob("dea_*.yaml"))
    valid_ctx_ids: set[str] = set()
    for f in ctx_files:
        data = yaml.safe_load(f.read_text())
        if data.get("id"):
            valid_ctx_ids.add(data["id"])
    for d in reg["dispositions"]:
        if d.get("disposition") != "RECLASSIFY":
            continue
        for change in d.get("changes", []):
            if change.get("axis") != "process_context":
                continue
            target = change.get("to")
            if target.startswith("dea:pc-"):
                assert target in valid_ctx_ids, (
                    f"{d['record_id']}: context {target!r} not in registry"
                )


def test_tranche_plan_covers_all_records() -> None:
    """Every record in the tranche plan also appears in the register."""
    plan = yaml.safe_load(
        (REPO_ROOT / "reconciliation/tranches/plan.yaml").read_text()
    )
    reg = yaml.safe_load(
        (REPO_ROOT / "reconciliation/dispositions/register.yaml").read_text()
    )
    plan_records: set[str] = set()
    for t in plan["tranches"]:
        plan_records.update(t.get("records", []))
    reg_records = {d["record_id"] for d in reg["dispositions"]}
    assert plan_records == reg_records, (
        f"plan_records - reg_records = {plan_records - reg_records}; "
        f"reg_records - plan_records = {reg_records - plan_records}"
    )


def test_tranche_count_is_ten() -> None:
    """Plan contains the canonical tranches.

    67 = 60 pre-existing (10 + 5 CR-BP-21a..e + 20 CR-BP-21{a,b,c,d}.1)
    + 5 CR-BP-21e.1 (fa-c.1/d.1/b.1/op.1/im.1)
    + 2 CR-BP-64 discovery-driven admissions (pv-act.64, pv-ret.64).
    """
    plan = yaml.safe_load(
        (REPO_ROOT / "reconciliation/tranches/plan.yaml").read_text()
    )
    assert len(plan["tranches"]) == 67


def test_live_check_dispositions_passes() -> None:
    """Running the validator on the live register + plan must exit 0."""
    res = _run()
    assert res.returncode == 0, res.stderr or res.stdout
    combined = (res.stdout or "") + (res.stderr or "")
    assert "DISP-OK" in combined
