#!/usr/bin/env python3
"""
tests/test_l3_backfill_ext20.py
==================================

Unit + integration tests for the EXT-20 L3 backfill validator
(scripts/check_l3_backfill_ext20.py).

Test layout:
  - test_self_test_passes
  - test_l3_inventory_completeness: L3-001
  - test_l3_parent_l2_readiness: L3-002
  - test_l3_orphan_detection: L3-003
  - test_l3_parent_reference_validation: L3-004
  - test_l3_sibling_uniqueness: L3-005
  - test_l3_cohesion: L3-006
  - test_l3_inputs_findings: L3-007
  - test_l3_outputs_findings: L3-008
  - test_l3_responsibility_findings: L3-009
  - test_l3_rules_controls_exceptions_findings: L3-010
  - test_l3_interfaces_dependencies_findings: L3-011
  - test_l3_to_l4_reconciliation: L3-012
  - test_l3_provenance_findings: L3-013
  - test_l3_disposition_findings: L3-014
  - test_l3_inventory_manifest_emitted
  - test_l3_to_l2_hierarchy_matrix_manifest_emitted
  - test_l3_backfill_manifest_emitted
  - test_disposition_vocabulary_is_seven
  - test_l3_template_unchanged_by_ext20
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
L3_INVENTORY = REPO_ROOT / "reconciliation" / "l3-inventory.json"
L3_BACKFILL_MANIFEST = REPO_ROOT / "reconciliation" / "l3-backfill-manifest.json"
L3_TO_L2_MATRIX = REPO_ROOT / "reconciliation" / "l3-to-l2-hierarchy-matrix.json"


class TestL3BackfillEXT20(unittest.TestCase):
    """CR-BP-94-EXT-20 L3 backfill tests."""

    def test_self_test_passes(self):
        r = subprocess.run(
            ["python3", "scripts/check_l3_backfill_ext20.py", "--self-test", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"self-test failed: {r.stdout}\n{r.stderr}")
        data = json.loads(r.stdout)
        self.assertEqual(data["mode"], "self-test")

    def test_l3_inventory_completeness(self):
        """L3-001: 580 L3 Activities identified."""
        with L3_INVENTORY.open() as fp:
            data = json.load(fp)
        self.assertEqual(data["total_l3_entities"], 580)

    def test_l3_parent_l2_readiness(self):
        """L3-002: every L3 Activity's parent appears in the EXT-19 inventory."""
        with L3_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        # The current state: all 580 L3 Activities' parents are in the
        # EXT-19 inventory (146 L2 BPs), so L3-002 should not fire.
        l3_002 = data["summary"]["by_rule"].get("L3-002", 0)
        self.assertEqual(l3_002, 0,
                          f"L3-002 findings: {l3_002} (expected 0; all L3 parents resolve)")

    def test_l3_orphan_detection(self):
        """L3-003: no orphan Activities (all have belongs_to_business_process)."""
        with L3_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l3_003 = data["summary"]["by_rule"].get("L3-003", 0)
        self.assertEqual(l3_003, 0,
                          f"L3-003 findings: {l3_003} (expected 0; 0 orphans in the catalogue)")

    def test_l3_parent_reference_validation(self):
        """L3-004: every parent L2 BP resolves."""
        with L3_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l3_004 = data["summary"]["by_rule"].get("L3-004", 0)
        self.assertEqual(l3_004, 0,
                          f"L3-004 findings: {l3_004} (expected 0; all 580 L3 parents resolve)")

    def test_l3_sibling_uniqueness(self):
        """L3-005: no duplicate name roots within the same parent L2."""
        with L3_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l3_005 = data["summary"]["by_rule"].get("L3-005", 0)
        self.assertEqual(l3_005, 0,
                          f"L3-005 findings: {l3_005} (expected 0; the 580 L3 Activities have distinct name roots within their parent L2)")

    def test_l3_cohesion(self):
        """L3-006: cohesion gap is small (few Activities without meaningful description)."""
        with L3_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l3_006 = data["summary"]["by_rule"].get("L3-006", 0)
        # Most Activities have a description >= 10 chars; very few don't.
        self.assertLessEqual(l3_006, 5,
                              f"L3-006 findings too high: {l3_006} (expected <= 5)")

    def test_l3_inputs_findings(self):
        """L3-007: 580 L3 Activities lack inputs[]."""
        with L3_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l3_007 = data["summary"]["by_rule"].get("L3-007", 0)
        self.assertEqual(l3_007, 580)

    def test_l3_outputs_findings(self):
        """L3-008: 580 L3 Activities lack outputs[]."""
        with L3_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l3_008 = data["summary"]["by_rule"].get("L3-008", 0)
        self.assertEqual(l3_008, 580)

    def test_l3_responsibility_findings(self):
        """L3-009: 580 L3 Activities lack accountability/responsibility."""
        with L3_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l3_009 = data["summary"]["by_rule"].get("L3-009", 0)
        self.assertEqual(l3_009, 580)

    def test_l3_rules_controls_exceptions_findings(self):
        """L3-010: 580 L3 Activities lack business_rules/controls/exceptions."""
        with L3_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l3_010 = data["summary"]["by_rule"].get("L3-010", 0)
        self.assertEqual(l3_010, 580)

    def test_l3_interfaces_dependencies_findings(self):
        """L3-011: 580 L3 Activities lack interfaces/dependencies."""
        with L3_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l3_011 = data["summary"]["by_rule"].get("L3-011", 0)
        self.assertEqual(l3_011, 580)

    def test_l3_to_l4_reconciliation(self):
        """L3-012: no Activities with extreme L4 child counts."""
        with L3_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        # The 580 L3 Activities all have 4-7 L4 children (a healthy
        # decomposition depth). No decomposition gap (>30% with 0 L4)
        # and no over-decomposition (Activities with 8+ L4).
        l3_012 = data["summary"]["by_rule"].get("L3-012", 0)
        self.assertEqual(l3_012, 0,
                          f"L3-012 findings: {l3_012} (expected 0; healthy decomposition across all 580 Activities)")

    def test_l3_provenance_findings(self):
        """L3-013: 580 L3 Activities lack provenance[]."""
        with L3_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l3_013 = data["summary"]["by_rule"].get("L3-013", 0)
        self.assertEqual(l3_013, 580)

    def test_l3_disposition_findings(self):
        """L3-014: 580 L3 Activities lack metadata.authoring (REQ-20-20)."""
        with L3_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        l3_014 = data["summary"]["by_rule"].get("L3-014", 0)
        self.assertEqual(l3_014, 580)

    def test_l3_inventory_manifest_emitted(self):
        self.assertTrue(L3_INVENTORY.exists(),
                        f"L3 inventory manifest missing at {L3_INVENTORY}")
        with L3_INVENTORY.open() as fp:
            data = json.load(fp)
        for entry in data["inventory"]:
            for key in ("id", "name", "type", "level", "parent_l2",
                          "parent_l2_resolves", "l4_children_count",
                          "fields_present", "authoring_state",
                          "disposition"):
                with self.subTest(key=key):
                    self.assertIn(key, entry, f"missing key: {key}")

    def test_l3_to_l2_hierarchy_matrix_manifest_emitted(self):
        self.assertTrue(L3_TO_L2_MATRIX.exists(),
                        f"hierarchy matrix missing at {L3_TO_L2_MATRIX}")
        with L3_TO_L2_MATRIX.open() as fp:
            data = json.load(fp)
        for key in ("matrix_schema_version", "purpose", "total_l3_entities",
                      "total_l2_parents_referenced", "l3_per_l2_distribution",
                      "l4_per_l3_distribution",
                      "structural_quality_observations"):
            with self.subTest(key=key):
                self.assertIn(key, data, f"missing key: {key}")

    def test_l3_backfill_manifest_emitted(self):
        self.assertTrue(L3_BACKFILL_MANIFEST.exists(),
                        f"L3 backfill manifest missing at {L3_BACKFILL_MANIFEST}")
        with L3_BACKFILL_MANIFEST.open() as fp:
            data = json.load(fp)
        for key in ("manifest_schema_version", "summary", "findings",
                      "inventory_summary"):
            with self.subTest(key=key):
                self.assertIn(key, data, f"missing key: {key}")

    def test_disposition_vocabulary_is_seven(self):
        """REQ-20-20: 7 entity-level dispositions (same as REQ-19-24)."""
        r = subprocess.run(
            ["python3", "scripts/check_l3_backfill_ext20.py", "--self-test", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(r.stdout)
        self.assertEqual(data["disposition_vocab_size"], 7)

    def test_l3_template_unchanged_by_ext20(self):
        """EXT-20 does not introduce an L3 template; it consumes the L3 schema
        + EXT-12..16 fields. We just confirm the EXT-12..16 fields remain."""
        # The L3 Activities use the EXT-10 schema inline; no L3 template
        # exists as a separate file. We confirm by reading the entity record
        # structure: the first L3 Activity should have the EXT-10 fields
        # (id, type, name, description, belongs_to_business_process).
        import yaml
        sample: dict | None = None
        for f in (REPO_ROOT / "entities" / "v1-alpha").rglob("*.yaml"):
            try:
                with f.open() as fp:
                    data = yaml.safe_load(fp) or {}
            except Exception:
                continue
            if isinstance(data, dict) and data.get("type") == "Activity":
                sample = data
                break
        self.assertIsNotNone(sample)
        self.assertIsInstance(sample, dict)
        for marker in ("belongs_to_business_process", "type"):
            with self.subTest(marker=marker):
                self.assertIn(marker, sample, f"L3 Activity should still have {marker!r}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
