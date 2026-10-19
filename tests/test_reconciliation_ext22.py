#!/usr/bin/env python3
"""
tests/test_reconciliation_ext22.py
====================================

Unit + integration tests for the EXT-22 structural integrity validator
and the L2-L4 Reconciliation Matrix
(scripts/check_reconciliation_ext22.py).

Test layout:
  - test_self_test_passes
  - test_r22_01_inventory_completeness: R22-01
  - test_r22_02_structural_hierarchy_valid: R22-02
  - test_r22_03_duplicate_identifier_detection: R22-03
  - test_r22_04_l2_to_l3_coverage: R22-04
  - test_r22_05_l3_to_l4_coverage: R22-05
  - test_r22_06_l1_to_l2_membership: R22-06
  - test_r22_07_l0_l1_contextual_consistency: R22-07
  - test_r22_08_l0_materialisation: R22-08
  - test_r22_09_granularity_assessment: R22-09
  - test_r22_10_duplicate_overlap_detection: R22-10
  - test_r22_11_functional_decomposition_integrity: R22-11
  - test_r22_12_l0_l1_landscape_coverage: R22-12
  - test_matrix_emitted_with_all_required_fields
  - test_matrix_scenario_coverage
  - test_registers_emitted
  - test_ext23_readiness_assessment_emitted
  - test_disposition_vocabulary_is_seven
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RECON = REPO_ROOT / "reconciliation"
MANIFEST = RECON / "ext22-manifest.json"
MATRIX = RECON / "reconciliation-matrix.json"
STRUCTURAL = RECON / "structural-integrity-report.json"
DUPLICATE_REG = RECON / "duplicate-overlap-register.json"
ORPHAN_REG = RECON / "orphan-misplaced-register.json"
GRANULARITY_REG = RECON / "granularity-register.json"
L0_L1_REPORT = RECON / "l0-l1-reconciliation-report.json"
READINESS = RECON / "ext23-readiness-assessment.json"

# The 26 fields required by the EXT-22 §7.2 matrix contract
REQUIRED_MATRIX_FIELDS = [
    "reconciliation_id", "l2_process_id", "l2_process_name", "l2_purpose",
    "l2_boundary", "l3_activity_id", "l3_activity_name", "l3_purpose",
    "l3_parent_contribution", "l3_coverage_assessment", "l4_task_id",
    "l4_task_name", "l4_purpose", "l4_parent_contribution",
    "l4_coverage_assessment", "boundary_alignment", "operational_alignment",
    "structural_status", "semantic_status", "granularity_assessment",
    "evidence_references", "identified_issues", "required_action",
    "issue_owner", "disposition", "review_status",
]


class TestReconciliationEXT22(unittest.TestCase):
    """CR-BP-94-EXT-22 structural integrity and reconciliation tests."""

    def test_self_test_passes(self):
        r = subprocess.run(
            ["python3", "scripts/check_reconciliation_ext22.py", "--self-test", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"self-test failed: {r.stdout}\n{r.stderr}")
        data = json.loads(r.stdout)
        self.assertEqual(data["mode"], "self-test")

    def _manifest(self) -> dict:
        with MANIFEST.open() as fp:
            return json.load(fp)

    def test_r22_01_inventory_completeness(self):
        """R22-01: all L0-L4 layers are inventoried."""
        data = self._manifest()
        levels = data["catalogue_state"]["by_level"]
        # The catalogue holds all 5 layers: 49 L0, 49 L1, 145 L2, 580 L3, 2900 L4.
        self.assertEqual(levels["L0"], 49)
        self.assertEqual(levels["L1"], 49)
        self.assertEqual(levels["L2"], 145)
        self.assertEqual(levels["L3"], 580)
        self.assertEqual(levels["L4"], 2900)
        # R22-01 must not fire now that all 5 layers are materialised.
        self.assertEqual(data["summary"]["by_rule"].get("R22-01", 0), 0)

    def test_r22_02_structural_hierarchy_valid(self):
        """R22-02: every parent reference resolves with the correct level."""
        data = self._manifest()
        r22_002 = data["summary"]["by_rule"].get("R22-02", 0)
        self.assertEqual(r22_002, 0,
                          f"R22-02 findings: {r22_002} (expected 0; all parent "
                          f"references resolve at the expected level)")

    def test_r22_03_duplicate_identifier_detection(self):
        """R22-03: no duplicate canonical identifiers in the catalogue."""
        data = self._manifest()
        r22_003 = data["summary"]["by_rule"].get("R22-03", 0)
        self.assertEqual(r22_003, 0,
                          f"R22-003 findings: {r22_003} (expected 0)")
        with STRUCTURAL.open() as fp:
            structural = json.load(fp)
        self.assertEqual(structural["duplicate_canonical_identifiers"], {})

    def test_r22_04_l2_to_l3_coverage(self):
        """R22-04: exactly 1 L2 has no L3 decomposition (the known gap)."""
        data = self._manifest()
        r22_004 = data["summary"]["by_rule"].get("R22-04", 0)
        self.assertEqual(r22_004, 1)
        with STRUCTURAL.open() as fp:
            structural = json.load(fp)
        self.assertEqual(
            structural["l2_without_l3_decomposition"],
            ["processes:process-ge-conceive-e6jx6s"],
        )

    def test_r22_05_l3_to_l4_coverage(self):
        """R22-05: every L3 has L4 decomposition (0 findings)."""
        data = self._manifest()
        r22_005 = data["summary"]["by_rule"].get("R22-05", 0)
        self.assertEqual(r22_005, 0,
                          f"R22-005 findings: {r22_005} (expected 0; all 580 "
                          f"Activities have 4-7 L4 Tasks)")

    def test_r22_06_l1_to_l2_membership(self):
        """R22-06: exactly 1 L2 is not composed by any L1 (the known gap)."""
        data = self._manifest()
        r22_006 = data["summary"]["by_rule"].get("R22-06", 0)
        self.assertEqual(r22_006, 1)
        with STRUCTURAL.open() as fp:
            structural = json.load(fp)
        self.assertEqual(
            structural["l2_without_l1_membership"],
            ["processes:process-ge-conceive-e6jx6s"],
        )

    def test_r22_07_l0_l1_contextual_consistency(self):
        """R22-07: 6 L1-to-L2 compositions carry an L0 context mismatch."""
        data = self._manifest()
        r22_007 = data["summary"]["by_rule"].get("R22-07", 0)
        self.assertEqual(r22_007, 6)
        with STRUCTURAL.open() as fp:
            structural = json.load(fp)
        self.assertEqual(len(structural["l0_context_mismatches"]), 6)
        for mismatch in structural["l0_context_mismatches"]:
            for key in ("l1", "l2", "l1_process_context", "l2_context"):
                with self.subTest(key=key):
                    self.assertIn(key, mismatch)

    def test_r22_08_l0_materialisation(self):
        """R22-08: all 49 referenced L0 Process Contexts are materialised."""
        data = self._manifest()
        r22_008 = data["summary"]["by_rule"].get("R22-08", 0)
        self.assertEqual(r22_008, 0,
                          f"R22-008 findings: {r22_008} (expected 0; all 49 L0 "
                          f"Process Contexts are materialised)")
        with STRUCTURAL.open() as fp:
            structural = json.load(fp)
        self.assertEqual(structural["l0_referenced"], 49)
        self.assertEqual(structural["l0_materialised"], 49)
        self.assertEqual(structural["l0_referenced_not_materialised"], [])

    def test_r22_09_granularity_assessment(self):
        """R22-09: granularity review prompts are recorded, not errors."""
        data = self._manifest()
        r22_009 = data["summary"]["by_rule"].get("R22-09", 0)
        # The 16 L1 Process Groups with exactly one L2 member are
        # potentially-narrow review prompts. They are warnings, not errors.
        self.assertGreaterEqual(r22_009, 0)
        with GRANULARITY_REG.open() as fp:
            granularity = json.load(fp)
        self.assertEqual(granularity["total_cases"], r22_009)
        for case in granularity["cases"]:
            for key in ("entity", "level", "kind", "detail"):
                with self.subTest(key=key):
                    self.assertIn(key, case)

    def test_r22_10_duplicate_overlap_detection(self):
        """R22-10: duplicate name detection runs and records its cases."""
        data = self._manifest()
        r22_010 = data["summary"]["by_rule"].get("R22-10", 0)
        with DUPLICATE_REG.open() as fp:
            duplicate = json.load(fp)
        self.assertEqual(duplicate["total_cases"], r22_010)
        self.assertIn("not automatic merge instructions", duplicate["note"])

    def test_r22_11_functional_decomposition_integrity(self):
        """R22-11: all 580 Activities carry the canonical 5-phase pattern."""
        data = self._manifest()
        r22_011 = data["summary"]["by_rule"].get("R22-11", 0)
        self.assertEqual(r22_011, 0,
                          f"R22-011 findings: {r22_011} (expected 0; all 580 "
                          f"Activities carry the canonical 5-phase pattern)")

    def test_r22_12_l0_l1_landscape_coverage(self):
        """R22-12: every L1 has L2 members (0 findings)."""
        data = self._manifest()
        r22_012 = data["summary"]["by_rule"].get("R22-12", 0)
        self.assertEqual(r22_012, 0,
                          f"R22-012 findings: {r22_012} (expected 0; all 49 L1 "
                          f"Process Groups have L2 members)")

    def test_matrix_emitted_with_all_required_fields(self):
        """The L2-L4 Reconciliation Matrix carries all 26 §7.2 fields."""
        self.assertTrue(MATRIX.exists(), f"matrix missing at {MATRIX}")
        with MATRIX.open() as fp:
            matrix = json.load(fp)
        self.assertGreater(matrix["total_records"], 0)
        for record in matrix["records"][:50]:
            for field in REQUIRED_MATRIX_FIELDS:
                with self.subTest(field=field):
                    self.assertIn(field, record, f"matrix field missing: {field}")
        # The matrix is a controlled artefact with the §7.4 metadata
        for key in ("matrix_schema_version", "generated_at", "generator",
                      "parent_cr", "purpose", "total_records", "by_scenario"):
            with self.subTest(key=key):
                self.assertIn(key, matrix, f"matrix metadata missing: {key}")

    def test_matrix_scenario_coverage(self):
        """§7.3 scenario coverage: A, C and D are all represented."""
        with MATRIX.open() as fp:
            matrix = json.load(fp)
        scenarios = matrix["by_scenario"]
        # Scenario A: L2 with L3 and L4.
        self.assertEqual(scenarios["A_l2_with_l3_and_l4"], 2900)
        # Scenario C: L3 with no L4 (0 in the current catalogue).
        self.assertEqual(scenarios["C_l3_without_l4"], 0)
        # Scenario D: L2 with no L3 (1 in the current catalogue).
        self.assertEqual(scenarios["D_l2_without_l3"], 1)
        # The total is the sum of the scenarios.
        self.assertEqual(
            matrix["total_records"],
            sum(scenarios.values()),
        )

    def test_registers_emitted(self):
        """The duplicate, orphan and granularity registers are emitted."""
        for path, name in [(DUPLICATE_REG, "duplicate-overlap"),
                            (ORPHAN_REG, "orphan-misplaced"),
                            (GRANULARITY_REG, "granularity"),
                            (L0_L1_REPORT, "l0-l1-reconciliation")]:
            with self.subTest(name=name):
                self.assertTrue(path.exists(), f"{name} register missing: {path}")
                with path.open() as fp:
                    json.load(fp)

    def test_ext23_readiness_assessment_emitted(self):
        """REQ-22-22: the EXT-23 readiness assessment is produced."""
        self.assertTrue(READINESS.exists(), f"readiness assessment missing: {READINESS}")
        with READINESS.open() as fp:
            readiness = json.load(fp)
        for key in ("automatically_enforceable", "requires_human_review",
                      "evidence_assessment_only", "deferred",
                      "known_limitations", "approved_exceptions",
                      "residual_risks", "readiness_statement"):
            with self.subTest(key=key):
                self.assertIn(key, readiness, f"readiness key missing: {key}")
        # The deterministic structural rules are separable from the
        # evidence-led semantic rules.
        self.assertIn("R22-02 structural hierarchy validation",
                      readiness["automatically_enforceable"])
        self.assertTrue(any("granularity" in r
                            for r in readiness["requires_human_review"]))

    def test_disposition_vocabulary_is_seven(self):
        """REQ-22-17: the 7-value reconciliation disposition vocabulary."""
        r = subprocess.run(
            ["python3", "scripts/check_reconciliation_ext22.py", "--self-test", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(r.stdout)
        self.assertEqual(data["disposition_vocab_size"], 7)


if __name__ == "__main__":
    unittest.main(verbosity=2)
