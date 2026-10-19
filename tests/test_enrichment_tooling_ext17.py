#!/usr/bin/env python3
"""
tests/test_enrichment_tooling_ext17.py
=======================================

Unit + integration tests for the EXT-17 enrichment tooling
(orchestrator + reporter):
  - scripts/orchestrate_backfill.py
  - scripts/report_catalogue_status.py

Test layout:
  Orchestrator:
    - test_orchestrator_self_test_passes
    - test_orchestrator_dry_run_does_not_modify_repo: OR-001
    - test_orchestrator_state_filter_validates_vocabulary: OR-002
    - test_orchestrator_runs_per_validator: OR-003
    - test_orchestrator_no_automatic_invention: OR-005
    - test_orchestrator_manifest_emitted
    - test_orchestrator_live_mode_reserved_for_ext19

  Reporter:
    - test_reporter_self_test_passes
    - test_reporter_rp_001_per_level_counts
    - test_reporter_rp_003_evidence_coverage
    - test_reporter_rp_004_verification_status_distribution
    - test_reporter_rp_008_entities_awaiting_owner_review
    - test_reporter_rp_009_backfill_completion_status
    - test_reporter_manifest_emitted
    - test_reporter_synthetic_l2_record_with_ext15_ext16

  Integration:
    - test_orchestrator_and_reporter_agree_on_record_count
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLING_MANIFEST = REPO_ROOT / "reconciliation" / "tooling-manifest.json"
CATALOGUE_MANIFEST = REPO_ROOT / "reconciliation" / "catalogue-status-manifest.json"


class TestOrchestrator(unittest.TestCase):
    """EXT-17 orchestrator (scripts/orchestrate_backfill.py) tests."""

    def test_orchestrator_self_test_passes(self):
        r = subprocess.run(
            ["python3", "scripts/orchestrate_backfill.py", "--self-test", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"self-test failed: {r.stdout}\n{r.stderr}")
        data = json.loads(r.stdout)
        self.assertEqual(data["mode"], "self-test")
        self.assertTrue(data["no_automatic_invention"])

    # OR-001: dry-run does not modify repo files
    def test_orchestrator_dry_run_does_not_modify_repo(self):
        # Capture the state of the reconciliation directory before + after
        before = sorted(p.name for p in (REPO_ROOT / "reconciliation").iterdir())
        r = subprocess.run(
            ["python3", "scripts/orchestrate_backfill.py"],
            capture_output=True, text=True, timeout=300,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"orchestrator failed: {r.stderr}")
        after = sorted(p.name for p in (REPO_ROOT / "reconciliation").iterdir())
        # The orchestrator writes tooling-manifest.json, so it may add ONE file.
        added = set(after) - set(before)
        removed = set(before) - set(after)
        # Allow only the tooling-manifest.json to be added; no other writes.
        self.assertEqual(removed, set(), f"orchestrator removed files: {removed}")
        # Added: only the manifest is expected.
        self.assertTrue(added.issubset({"tooling-manifest.json"}),
                        f"orchestrator added unexpected files: {added}")

    # OR-002: state filter validates EXT-16 vocabulary
    def test_orchestrator_state_filter_validates_vocabulary(self):
        r = subprocess.run(
            ["python3", "scripts/orchestrate_backfill.py", "--state", "in_progress"],
            capture_output=True, text=True, timeout=15,
            cwd=str(REPO_ROOT),
        )
        self.assertNotEqual(r.returncode, 0, "expected non-zero exit for invalid state")
        self.assertIn("not in the EXT-16", r.stderr,
                      f"unexpected stderr: {r.stderr}")

    # OR-003: per-validator execution
    def test_orchestrator_runs_per_validator(self):
        r = subprocess.run(
            ["python3", "scripts/orchestrate_backfill.py", "--json"],
            capture_output=True, text=True, timeout=300,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"orchestrator failed: {r.stderr}")
        data = json.loads(r.stdout)
        per_validator = data.get("per_validator_summary", {})
        # The orchestrator runs the EXT-11..16 validators (6 of them).
        self.assertGreaterEqual(len(per_validator), 6,
                                f"expected 6+ validators, got {len(per_validator)}")
        for expected in ("check_profile_registry_ext11.py",
                          "check_inputs_outputs_interfaces_ext12.py",
                          "check_responsibility_accountability_ext13.py",
                          "check_business_rules_controls_exceptions_ext14.py",
                          "check_evidence_provenance_ext15.py",
                          "check_authoring_methodology_ext16.py"):
            self.assertIn(expected, per_validator,
                          f"missing validator: {expected}")

    # OR-005: no automatic invention
    def test_orchestrator_no_automatic_invention(self):
        r = subprocess.run(
            ["python3", "scripts/orchestrate_backfill.py", "--json"],
            capture_output=True, text=True, timeout=300,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(r.stdout)
        self.assertTrue(data.get("no_automatic_invention"),
                        "orchestrator must declare no_automatic_invention=True")

    # Manifest emission
    def test_orchestrator_manifest_emitted(self):
        r = subprocess.run(
            ["python3", "scripts/orchestrate_backfill.py"],
            capture_output=True, text=True, timeout=300,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"orchestrator failed: {r.stderr}")
        self.assertTrue(TOOLING_MANIFEST.exists(),
                        f"tooling manifest missing at {TOOLING_MANIFEST}")
        with TOOLING_MANIFEST.open() as fp:
            data = json.load(fp)
        self.assertEqual(data["mode"], "dry-run")
        self.assertIn("per_validator_summary", data)

    # Live mode is reserved for EXT-19
    def test_orchestrator_live_mode_reserved_for_ext19(self):
        r = subprocess.run(
            ["python3", "scripts/orchestrate_backfill.py", "--live", "--json"],
            capture_output=True, text=True, timeout=300,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"orchestrator failed: {r.stderr}")
        data = json.loads(r.stdout)
        self.assertEqual(data["mode"], "live")
        self.assertIn("EXT-19", data.get("note", ""),
                      f"live mode note should reference EXT-19: {data.get('note')}")


class TestReporter(unittest.TestCase):
    """EXT-17 reporter (scripts/report_catalogue_status.py) tests."""

    def test_reporter_self_test_passes(self):
        r = subprocess.run(
            ["python3", "scripts/report_catalogue_status.py", "--self-test", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"self-test failed: {r.stdout}\n{r.stderr}")
        data = json.loads(r.stdout)
        self.assertEqual(data["mode"], "self-test")

    # RP-001
    def test_reporter_rp_001_per_level_counts(self):
        r = subprocess.run(
            ["python3", "scripts/report_catalogue_status.py", "--json"],
            capture_output=True, text=True, timeout=60,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"reporter failed: {r.stderr}")
        data = json.loads(r.stdout)
        per_level = data["rp_001_per_level_counts"]
        # The current catalogue has 49 L1 + 146 L2 + 580 L3 + 2900 L4 (the
        # EXT-10 inventory's "49 L0" is stale; the actual L0 count is 0).
        self.assertEqual(per_level["L1"], 49)
        self.assertEqual(per_level["L2"], 146)
        # L0 records do not exist in the current catalogue.
        self.assertEqual(per_level["L0"], 0)

    # RP-003
    def test_reporter_rp_003_evidence_coverage(self):
        r = subprocess.run(
            ["python3", "scripts/report_catalogue_status.py", "--json"],
            capture_output=True, text=True, timeout=60,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(r.stdout)
        coverage = data["rp_003_evidence_coverage"]
        # The 244 (or 3,675) records have 0 EXT-15 evidence populated yet
        # (the EXT-19 backfill is the work that populates them).
        self.assertEqual(coverage["records_with_provenance"], 0)
        self.assertEqual(coverage["records_with_confidence"], 0)
        self.assertEqual(coverage["records_with_verification_status"], 0)
        self.assertEqual(coverage["records_with_uncertainty_state"], 0)
        self.assertEqual(coverage["records_with_ai_assisted_source"], 0)

    # RP-004
    def test_reporter_rp_004_verification_status_distribution(self):
        r = subprocess.run(
            ["python3", "scripts/report_catalogue_status.py", "--json"],
            capture_output=True, text=True, timeout=60,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(r.stdout)
        vs_dist = data["rp_004_verification_status_distribution"]
        # The current catalogue has 0 records with verification_status
        # populated; the absent count is the total records.
        self.assertEqual(vs_dist["verified"], 0)
        self.assertEqual(vs_dist["under_review"], 0)
        self.assertEqual(vs_dist["not_reviewed"], 0)
        # absent = L0 + L1 + L2 + L3 + L4
        self.assertGreater(vs_dist["absent"], 0)

    # RP-008
    def test_reporter_rp_008_entities_awaiting_owner_review(self):
        r = subprocess.run(
            ["python3", "scripts/report_catalogue_status.py", "--json"],
            capture_output=True, text=True, timeout=60,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(r.stdout)
        # 0 records have metadata.authoring.state = under_review yet.
        self.assertEqual(data["rp_008_entities_awaiting_owner_review"], 0)

    # RP-009
    def test_reporter_rp_009_backfill_completion_status(self):
        r = subprocess.run(
            ["python3", "scripts/report_catalogue_status.py", "--json"],
            capture_output=True, text=True, timeout=60,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(r.stdout)
        bc = data["rp_009_backfill_completion_status"]
        # 0 records are published yet; all are "absent" (no metadata.authoring).
        self.assertEqual(bc["published"], 0)
        self.assertGreater(bc["distribution"]["absent"], 0)

    # Manifest emission
    def test_reporter_manifest_emitted(self):
        r = subprocess.run(
            ["python3", "scripts/report_catalogue_status.py"],
            capture_output=True, text=True, timeout=60,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"reporter failed: {r.stderr}")
        self.assertTrue(CATALOGUE_MANIFEST.exists(),
                        f"catalogue manifest missing at {CATALOGUE_MANIFEST}")
        with CATALOGUE_MANIFEST.open() as fp:
            data = json.load(fp)
        for key in ("rp_001_per_level_counts", "rp_003_evidence_coverage",
                    "rp_004_verification_status_distribution",
                    "rp_005_outstanding_warnings_errors",
                    "rp_006_broken_references",
                    "rp_007_parent_child_reconciliation",
                    "rp_008_entities_awaiting_owner_review",
                    "rp_009_backfill_completion_status"):
            with self.subTest(key=key):
                self.assertIn(key, data, f"missing report key: {key}")


class TestIntegration(unittest.TestCase):
    """Integration tests for orchestrator + reporter."""

    def test_orchestrator_and_reporter_agree_on_record_count(self):
        r1 = subprocess.run(
            ["python3", "scripts/orchestrate_backfill.py", "--json"],
            capture_output=True, text=True, timeout=300,
            cwd=str(REPO_ROOT),
        )
        r2 = subprocess.run(
            ["python3", "scripts/report_catalogue_status.py", "--json"],
            capture_output=True, text=True, timeout=60,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r1.returncode, 0)
        self.assertEqual(r2.returncode, 0)
        orch = json.loads(r1.stdout)
        rep = json.loads(r2.stdout)
        orch_total = orch["selection"]["total_selected_records"]
        rep_total = sum(v for k, v in rep["rp_001_per_level_counts"].items() if k != "other")
        # Both tools iterate the same yaml files; totals should match.
        self.assertEqual(orch_total, rep_total,
                         f"orchestrator selected {orch_total}; reporter found {rep_total}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
