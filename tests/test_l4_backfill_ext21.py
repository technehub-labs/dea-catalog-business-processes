#!/usr/bin/env python3
"""
tests/test_l4_backfill_ext21.py
==================================

Unit + integration tests for the EXT-21 L4 backfill validator
(scripts/check_l4_backfill_ext21.py).

Test layout:
  - test_self_test_passes
  - test_l4_inventory_completeness: L4-001
  - test_l4_parent_l3_readiness: L4-002
  - test_l4_orphan_detection: L4-003
  - test_l4_parent_reference_validation: L4-004
  - test_l4_phase_coherence: L4-005
  - test_l4_definition_findings: L4-006
  - test_l4_trigger_findings: L4-007
  - test_l4_outcome_findings: L4-008
  - test_l4_responsibility_findings: L4-009
  - test_l4_boundary_findings: L4-010
  - test_l4_evidence_findings: L4-011
  - test_l4_provenance_findings: L4-012
  - test_l4_authoring_findings: L4-013
  - test_l4_disposition_vocabulary: L4-014
  - test_l4_inventory_manifest_emitted
  - test_l4_to_l3_traceability_matrix_manifest_emitted
  - test_l4_backfill_manifest_emitted
  - test_traceability_matrix_completes_l2_to_l4
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
L4_INVENTORY = REPO_ROOT / "reconciliation" / "l4-inventory.json"
L4_BACKFILL_MANIFEST = REPO_ROOT / "reconciliation" / "l4-backfill-manifest.json"
L4_TO_L3_MATRIX = REPO_ROOT / "reconciliation" / "l4-to-l3-traceability-matrix.json"
L3_TO_L2_MATRIX = REPO_ROOT / "reconciliation" / "l3-to-l2-hierarchy-matrix.json"
L2_TO_L3_MATRIX = REPO_ROOT / "reconciliation" / "l2-to-l3-reconciliation-matrix.json"


class TestL4BackfillEXT21(unittest.TestCase):
    """CR-BP-94-EXT-21 L4 backfill tests."""

    def test_self_test_passes(self):
        r = subprocess.run(
            ["python3", "scripts/check_l4_backfill_ext21.py", "--self-test", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"self-test failed: {r.stdout}\n{r.stderr}")
        data = json.loads(r.stdout)
        self.assertEqual(data["mode"], "self-test")
        self.assertEqual(data["canonical_phase_count"], 5)

    def test_l4_inventory_completeness(self):
        """L4-001: 2900 L4 Tasks identified."""
        with L4_INVENTORY.open() as fp:
            data = json.load(fp)
        self.assertEqual(data["total_l4_entities"], 2900)

    def test_l4_parent_l3_readiness(self):
        """L4-002: every parent L3 appears in the EXT-20 inventory."""
        with L4_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l4_002 = data["summary"]["by_rule"].get("L4-002", 0)
        self.assertEqual(l4_002, 0,
                          f"L4-002 findings: {l4_002} (expected 0; all L3 parents resolve)")

    def test_l4_orphan_detection(self):
        """L4-003: no orphan Tasks."""
        with L4_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l4_003 = data["summary"]["by_rule"].get("L4-003", 0)
        self.assertEqual(l4_003, 0,
                          f"L4-003 findings: {l4_003} (expected 0; 0 orphans)")

    def test_l4_parent_reference_validation(self):
        """L4-004: every parent L3 Activity resolves."""
        with L4_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l4_004 = data["summary"]["by_rule"].get("L4-004", 0)
        self.assertEqual(l4_004, 0,
                          f"L4-004 findings: {l4_004} (expected 0)")

    def test_l4_phase_coherence(self):
        """L4-005: every parent L3 carries the canonical 5-phase pattern."""
        with L4_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l4_005 = data["summary"]["by_rule"].get("L4-005", 0)
        self.assertEqual(l4_005, 0,
                          f"L4-005 findings: {l4_005} (expected 0; all 580 parents are phase-coherent)")

    def test_l4_definition_findings(self):
        """L4-006: 0 findings; all 2900 Tasks have a meaningful definition."""
        with L4_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l4_006 = data["summary"]["by_rule"].get("L4-006", 0)
        self.assertEqual(l4_006, 0,
                          f"L4-006 findings: {l4_006} (expected 0; all definitions >= 40 chars)")

    def test_l4_trigger_findings(self):
        """L4-007: 0 findings; all 2900 Tasks have a trigger."""
        with L4_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        self.assertEqual(data["summary"]["by_rule"].get("L4-007", 0), 0)

    def test_l4_outcome_findings(self):
        """L4-008: 0 findings; all 2900 Tasks have an outcome."""
        with L4_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        self.assertEqual(data["summary"]["by_rule"].get("L4-008", 0), 0)

    def test_l4_responsibility_findings(self):
        """L4-009: 0 findings; all 2900 Tasks have a responsibility."""
        with L4_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        self.assertEqual(data["summary"]["by_rule"].get("L4-009", 0), 0)

    def test_l4_boundary_findings(self):
        """L4-010: 0 findings; all 2900 Tasks have inclusions and exclusions."""
        with L4_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        self.assertEqual(data["summary"]["by_rule"].get("L4-010", 0), 0)

    def test_l4_evidence_findings(self):
        """L4-011: 0 findings; all 2900 Tasks have the pre-EXT-15 evidence[] record."""
        with L4_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        self.assertEqual(data["summary"]["by_rule"].get("L4-011", 0), 0)

    def test_l4_provenance_findings(self):
        """L4-012: 2900 findings; the EXT-15 canonical provenance[] is the
        migration gap that the EXT-23 tranche resolves."""
        with L4_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l4_012 = data["summary"]["by_rule"].get("L4-012", 0)
        self.assertEqual(l4_012, 2900)

    def test_l4_authoring_findings(self):
        """L4-013: 2900 findings; the EXT-16 authoring metadata is the
        migration gap that the EXT-23 tranche resolves."""
        with L4_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l4_013 = data["summary"]["by_rule"].get("L4-013", 0)
        self.assertEqual(l4_013, 2900)

    def test_l4_disposition_vocabulary(self):
        """L4-014: the 7-value programme disposition vocabulary."""
        r = subprocess.run(
            ["python3", "scripts/check_l4_backfill_ext21.py", "--self-test", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(r.stdout)
        self.assertEqual(data["disposition_vocab_size"], 7)

    def test_l4_inventory_manifest_emitted(self):
        self.assertTrue(L4_INVENTORY.exists(),
                        f"L4 inventory manifest missing at {L4_INVENTORY}")
        with L4_INVENTORY.open() as fp:
            data = json.load(fp)
        for entry in data["inventory"]:
            for key in ("id", "name", "type", "level", "parent_l3",
                          "parent_l3_resolves", "phase", "fields_present",
                          "authoring_state", "disposition"):
                with self.subTest(key=key):
                    self.assertIn(key, entry, f"missing key: {key}")

    def test_l4_to_l3_traceability_matrix_manifest_emitted(self):
        self.assertTrue(L4_TO_L3_MATRIX.exists(),
                        f"traceability matrix missing at {L4_TO_L3_MATRIX}")
        with L4_TO_L3_MATRIX.open() as fp:
            data = json.load(fp)
        for key in ("matrix_schema_version", "purpose", "total_l4_entities",
                      "total_l3_parents_referenced",
                      "tasks_per_parent_distribution", "phase_distribution",
                      "structural_quality_observations"):
            with self.subTest(key=key):
                self.assertIn(key, data, f"missing key: {key}")

    def test_l4_backfill_manifest_emitted(self):
        self.assertTrue(L4_BACKFILL_MANIFEST.exists(),
                        f"L4 backfill manifest missing at {L4_BACKFILL_MANIFEST}")
        with L4_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        for key in ("manifest_schema_version", "summary", "findings",
                      "inventory_summary"):
            with self.subTest(key=key):
                self.assertIn(key, data, f"missing key: {key}")

    def test_traceability_matrix_completes_l2_to_l4(self):
        """The EXT-21 matrix completes the L2-to-L3-to-L4 traceability matrix
        mandated by the user recommendation. All 3 slices must be present."""
        self.assertTrue(L2_TO_L3_MATRIX.exists(), "EXT-19 matrix slice missing")
        self.assertTrue(L3_TO_L2_MATRIX.exists(), "EXT-20 matrix slice missing")
        self.assertTrue(L4_TO_L3_MATRIX.exists(), "EXT-21 matrix slice missing")
        # EXT-19 slice: 146 L2 entities
        with L2_TO_L3_MATRIX.open() as fp:
            l2_slice = json.load(fp)
        self.assertEqual(l2_slice["total_l2_entities"], 146)
        # EXT-20 slice: 580 L3 entities
        with L3_TO_L2_MATRIX.open() as fp:
            l3_slice = json.load(fp)
        self.assertEqual(l3_slice["total_l3_entities"], 580)
        # EXT-21 slice: 2900 L4 entities across 580 L3 parents
        with L4_TO_L3_MATRIX.open() as fp:
            l4_slice = json.load(fp)
        self.assertEqual(l4_slice["total_l4_entities"], 2900)
        self.assertEqual(l4_slice["total_l3_parents_referenced"], 580)
        # Every L3 parent carries exactly 5 Tasks
        self.assertEqual(l4_slice["tasks_per_parent_distribution"], {"5": 580})
        # The 5 phases are equally distributed
        self.assertEqual(
            l4_slice["phase_distribution"],
            {"Confirmation": 580, "Intake": 580, "Processing": 580,
             "Record": 580, "Verification": 580},
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
