#!/usr/bin/env python3
"""
tests/test_l2_backfill_ext19.py
==================================

Unit + integration tests for the EXT-19 L2 backfill validator
(scripts/check_l2_backfill_ext19.py).

Test layout:
  - test_self_test_passes
  - test_l2_inventory_completeness: L2-001
  - test_l2_profile_complete_count: L2-002
  - test_l2_process_identity_findings: L2-003
  - test_l2_inputs_outputs_findings: L2-006
  - test_l2_responsibility_accountability_findings: L2-007
  - test_l2_rules_controls_exceptions_findings: L2-008
  - test_l2_provenance_findings: L2-009
  - test_l2_parent_l0_pc_findings: L2-010
  - test_l2_to_l3_reconciliation_matrix: L2-011 (the user-recommended matrix)
  - test_l2_disposition_findings: L2-012
  - test_l2_inventory_manifest_emitted
  - test_l2_to_l3_matrix_manifest_emitted
  - test_l2_backfill_manifest_emitted
  - test_disposition_vocabulary_is_seven
  - test_l2_template_unchanged_by_ext19
  - test_l2_to_l3_matrix_identifies_decomposition_gaps
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
L2_INVENTORY = REPO_ROOT / "reconciliation" / "l2-inventory.json"
L2_BACKFILL_MANIFEST = REPO_ROOT / "reconciliation" / "l2-backfill-manifest.json"
L2_TO_L3_MATRIX = REPO_ROOT / "reconciliation" / "l2-to-l3-reconciliation-matrix.json"


class TestL2BackfillEXT19(unittest.TestCase):
    """CR-BP-94-EXT-19 L2 backfill tests."""

    def test_self_test_passes(self):
        r = subprocess.run(
            ["python3", "scripts/check_l2_backfill_ext19.py", "--self-test", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"self-test failed: {r.stdout}\n{r.stderr}")
        data = json.loads(r.stdout)
        self.assertEqual(data["mode"], "self-test")

    def test_l2_inventory_completeness(self):
        """L2-001: 146 L2 BPs identified from the actual catalogue."""
        with L2_INVENTORY.open() as fp:
            data = json.load(fp)
        self.assertEqual(data["total_l2_entities"], 146)

    def test_l2_profile_complete_count(self):
        """L2-002: per-record profile completeness."""
        with L2_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        profile = data["inventory_summary"]["by_profile_completeness"]
        # Pre-EXT-19 state: 0 fully_complete, 0 partial, 146 incomplete
        self.assertEqual(profile["fully_complete"], 0)
        self.assertEqual(profile["partial"], 0)
        self.assertEqual(profile["incomplete"], 146)

    def test_l2_process_identity_findings(self):
        """L2-003: the L2 BPs lack operationally meaningful descriptions."""
        with L2_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        # The L2 BPs DO have a description (12 fields), but the L2-003
        # checks for >=10 chars. Check that findings are present for
        # records without descriptions.
        l2_003 = data["summary"]["by_rule"].get("L2-003", 0)
        # The 146 L2 BPs all have a description >= 10 chars, so L2-003
        # should be 0.
        self.assertEqual(l2_003, 0, f"L2-003 findings: {l2_003} (expected 0)")

    def test_l2_inputs_outputs_findings(self):
        """L2-006: 146 L2 BPs lack inputs[]/outputs[]."""
        with L2_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l2_006 = data["summary"]["by_rule"].get("L2-006", 0)
        self.assertEqual(l2_006, 146)

    def test_l2_responsibility_accountability_findings(self):
        """L2-007: 146 L2 BPs lack accountability/responsibility."""
        with L2_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l2_007 = data["summary"]["by_rule"].get("L2-007", 0)
        self.assertEqual(l2_007, 146)

    def test_l2_rules_controls_exceptions_findings(self):
        """L2-008: 146 L2 BPs lack business_rules/controls/exceptions."""
        with L2_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l2_008 = data["summary"]["by_rule"].get("L2-008", 0)
        self.assertEqual(l2_008, 146)

    def test_l2_provenance_findings(self):
        """L2-009: 146 L2 BPs lack provenance[]."""
        with L2_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l2_009 = data["summary"]["by_rule"].get("L2-009", 0)
        self.assertEqual(l2_009, 146)

    def test_l2_parent_l0_pc_findings(self):
        """L2-010: 1 L2 BP lacks context[] L0 PC ref (the gap)."""
        with L2_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        # 145 of 146 have context[]; 1 is missing (processes:process-pr-improve-t6uvan)
        l2_010 = data["summary"]["by_rule"].get("L2-010", 0)
        self.assertEqual(l2_010, 1)

    def test_l2_to_l3_reconciliation_matrix(self):
        """L2-011: the L2-to-L3 reconciliation matrix surfaced (the
        user-recommended mandatory EXT-19 deliverable)."""
        with L2_TO_L3_MATRIX.open() as fp:
            data = json.load(fp)
        self.assertEqual(data["total_l2_entities"], 146)
        # 145 L2 BPs have 4-7 L3 children; 1 L2 BP has 0 L3 children (gap)
        buckets = data["buckets"]
        self.assertEqual(buckets["0"], 1)
        self.assertEqual(buckets["4_to_7"], 145)
        # The structural_quality_observations record the gap count
        self.assertEqual(data["structural_quality_observations"]["decomposition_gaps_count"], 1)

    def test_l2_disposition_findings(self):
        """L2-012: 146 L2 BPs lack metadata.authoring (REQ-19-24)."""
        with L2_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l2_012 = data["summary"]["by_rule"].get("L2-012", 0)
        self.assertEqual(l2_012, 146)

    def test_l2_inventory_manifest_emitted(self):
        self.assertTrue(L2_INVENTORY.exists(),
                        f"inventory manifest missing at {L2_INVENTORY}")
        with L2_INVENTORY.open() as fp:
            data = json.load(fp)
        # Each inventory entry has the L2-001 fields
        for entry in data["inventory"]:
            for key in ("id", "name", "type", "level", "parent_l1",
                          "l3_children_count", "fields_present",
                          "authoring_state", "disposition",
                          "profile_completeness"):
                with self.subTest(key=key):
                    self.assertIn(key, entry, f"missing key: {key}")

    def test_l2_to_l3_matrix_manifest_emitted(self):
        self.assertTrue(L2_TO_L3_MATRIX.exists(),
                        f"reconciliation matrix missing at {L2_TO_L3_MATRIX}")
        with L2_TO_L3_MATRIX.open() as fp:
            data = json.load(fp)
        for key in ("matrix_schema_version", "purpose",
                      "total_l2_entities", "buckets",
                      "l2_processes_with_no_l3_children",
                      "structural_quality_observations"):
            with self.subTest(key=key):
                self.assertIn(key, data, f"missing key: {key}")

    def test_l2_backfill_manifest_emitted(self):
        self.assertTrue(L2_BACKFILL_MANIFEST.exists(),
                        f"backfill manifest missing at {L2_BACKFILL_MANIFEST}")
        with L2_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        for key in ("manifest_schema_version", "summary", "findings",
                      "inventory_summary"):
            with self.subTest(key=key):
                self.assertIn(key, data, f"missing key: {key}")

    def test_disposition_vocabulary_is_seven(self):
        """REQ-19-24: 7 entity-level dispositions."""
        r = subprocess.run(
            ["python3", "scripts/check_l2_backfill_ext19.py", "--self-test", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(r.stdout)
        self.assertEqual(data["disposition_vocab_size"], 7,
                          f"expected 7 dispositions, got {data['disposition_vocab_size']}")

    def test_l2_template_unchanged_by_ext19(self):
        """EXT-19 does not modify the L2 template; it consumes the EXT-12..16
        fields. This is the catalyst CR for the actual content backfill.

        The L2 template should still document the EXT-12..16 fields."""
        template_path = REPO_ROOT / "templates" / "business-process.yaml"
        with template_path.open() as fp:
            text = fp.read()
        for marker in ("provenance:", "metadata.authoring:", "EXT-15", "EXT-16"):
            with self.subTest(marker=marker):
                self.assertIn(marker, text, f"L2 template should still document {marker!r}")

    def test_l2_to_l3_matrix_identifies_decomposition_gaps(self):
        """The matrix MUST identify any L2 BP that has no L3 children as a
        decomposition gap (REQ-19-19)."""
        with L2_TO_L3_MATRIX.open() as fp:
            data = json.load(fp)
        gaps = data["l2_processes_with_no_l3_children"]
        # 1 L2 BP has 0 L3 children; the matrix records it as a gap.
        self.assertEqual(len(gaps), 1)
        # The decomposition_gaps_count matches.
        self.assertEqual(data["structural_quality_observations"]["decomposition_gaps_count"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
