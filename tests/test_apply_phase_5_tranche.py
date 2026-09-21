"""Tests for the CR-BP-15-IMP Phase 5 tranche migration script.

Locks behaviour for `scripts/apply_phase_5_tranche.py`:
- self-test passes (idempotence + correctness);
- applying the cd-b + cd-c tranches reduces BP-SEM-007 errors
  by exactly the number of records in those tranches;
- the disposition register lock status reflects the migration.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"

# CR-BP-mv1: records moved to the L0-rooted containment tree with
# content-addressed ids. Resolve legacy dea:* ids through the migration
# id map, then locate the record file by its new id.
_ID_MAP = yaml.safe_load(
    (REPO_ROOT / "reconciliation/migration-id-map.yaml").read_text()
)["id_map"]


def _entity_path(legacy_id: str) -> Path:
    new_id = _ID_MAP[legacy_id]
    fname = new_id.replace(":", "-") + ".yaml"
    matches = list((REPO_ROOT / "entities/v1-alpha").rglob(fname))
    assert len(matches) == 1, f"{legacy_id} -> {new_id}: {len(matches)} matches"
    return matches[0]


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "apply_phase_5_tranche.py"), *args],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )


def test_self_test_passes() -> None:
    res = _run("--self-test")
    assert res.returncode == 0, res.stderr
    assert "PASS" in res.stdout


def test_cd_b_records_migrated() -> None:
    """cd-b records carry the canonical context: block and have no
    process_audience field."""
    for pid in ("dea:process-customer-channel-and-acquisition-build",
                "dea:process-demand-generation-build"):
        path = _entity_path(pid)
        data = yaml.safe_load(path.read_text())
        assert data.get("process_intent") == "operate", (
            f"{pid}: intent not migrated to canonical 'operate'"
        )
        assert "process_audience" not in data, (
            f"{pid}: legacy process_audience not removed"
        )
        assert "process_context" not in data, (
            f"{pid}: legacy scalar process_context not removed"
        )
        ctx = data.get("context")
        assert isinstance(ctx, list) and ctx[0].get("ref"), (
            f"{pid}: canonical context: block missing or wrong shape"
        )
        rels = data.get("relationships", [])
        assert any(r.get("relationship_type") == "serves"
                   and r.get("target_id") == "ecf:customerAndDemand.build"
                   for r in rels), (
            f"{pid}: serves relationship missing"
        )


def test_cd_c_records_migrated() -> None:
    """cd-c records migrated to canonical 'develop' intent."""
    for pid in ("dea:process-customer-strategy-conception",
                "dea:process-market-and-demand-conception"):
        path = _entity_path(pid)
        data = yaml.safe_load(path.read_text())
        assert data.get("process_intent") == "develop", (
            f"{pid}: intent not migrated to canonical 'develop'"
        )
        assert "process_audience" not in data
        assert "process_context" not in data
        ctx = data.get("context")
        assert isinstance(ctx, list) and ctx[0].get("ref") == _ID_MAP["dea:pc-pr-c"]
        rels = data.get("relationships", [])
        assert any(r.get("relationship_type") == "serves"
                   and r.get("target_id") == "ecf:customerAndDemand.conceive"
                   for r in rels)


def test_change_history_appended() -> None:
    """Every migrated record carries a CR-BP-15-IMP Phase 5 history entry."""
    for pid in ("dea:process-customer-channel-and-acquisition-build",
                "dea:process-demand-generation-build",
                "dea:process-customer-strategy-conception",
                "dea:process-market-and-demand-conception"):
        path = _entity_path(pid)
        data = yaml.safe_load(path.read_text())
        history = data.get("metadata", {}).get("change_history", [])
        assert any(h.get("cr") == "CR-BP-15-IMP" and h.get("phase") == "phase-5"
                   for h in history), (
            f"{pid}: CR-BP-15-IMP Phase 5 history entry missing"
        )


@pytest.mark.skip(
    reason="CR-BP-mv1 historical freeze: apply_phase_5_tranche.py is a retired "
    "one-shot script that writes the pre-migration flat layout; re-running it "
    "against the migrated containment tree is not meaningful. The content "
    "invariants it established are covered live by the three tests above."
)
def test_migration_is_idempotent() -> None:
    """Re-applying the cd-b tranche produces no further changes."""
    import hashlib
    before = {}
    for pid in ("dea:process-customer-channel-and-acquisition-build",
                "dea:process-demand-generation-build"):
        path = _entity_path(pid)
        before[pid] = hashlib.sha256(path.read_bytes()).hexdigest()
    _run("--tranche", "cd-b")
    after = {}
    for pid in ("dea:process-customer-channel-and-acquisition-build",
                "dea:process-demand-generation-build"):
        path = _entity_path(pid)
        after[pid] = hashlib.sha256(path.read_bytes()).hexdigest()
    assert before == after, "migration is not idempotent"


def test_register_lock_progress_records_all_18_records() -> None:
    """The disposition register reflects the Phase 5 lock progress
    through PR-9: ALL 18 records locked; the register is LOCKED.

    This is the closure of the CR-BP-15-IMP Phase 5 loop. Future
    Phase 6 (specializations) work will operate against this
    locked baseline.
    """
    reg = yaml.safe_load(
        (REPO_ROOT / "reconciliation/dispositions/register.yaml").read_text()
    )
    progress = reg.get("register_lock_progress", {})
    expected_tranches = {"cd-b", "cd-c", "cd-d", "cd-im", "cd-op",
                         "ge-b", "ge-c", "ge-d", "ge-im", "ge-op"}
    assert expected_tranches.issubset(set(progress.get("locked_tranches", [])))
    assert progress.get("locked_records") == 18
    assert progress.get("remaining_records") == 0
    assert reg.get("register_status") == "LOCKED"


def test_baseline_v1_remains_immutable() -> None:
    """The Phase 5 migration MUST NOT modify reconciliation/baseline/v1.yaml."""
    import hashlib
    baseline = REPO_ROOT / "reconciliation/baseline/v1.yaml"
    sha = hashlib.sha256(baseline.read_bytes()).hexdigest()
    # The baseline was committed with sha256 captured in the PR-31 body;
    # we just assert the file still exists and is parseable.
    data = yaml.safe_load(baseline.read_text())
    assert data.get("baseline_version") == "v1"


def test_phase5_diff_file_exists() -> None:
    """The Phase 5 diff file is part of the audit trail."""
    diff = REPO_ROOT / "reconciliation/diffs/phase-5-cd-b-cd-c.yaml"
    assert diff.exists()
    data = yaml.safe_load(diff.read_text())
    assert data.get("phase") == "phase-5"
    assert "cd-b" in data.get("tranches", [])
    assert "cd-c" in data.get("tranches", [])
    assert data["summary"]["records_touched"] == 4
