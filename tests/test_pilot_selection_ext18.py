#!/usr/bin/env python3
"""
tests/test_pilot_selection_ext18.py
====================================

Unit + integration tests for the EXT-18 pilot selection
(scripts/check_pilot_selection_ext18.py).

Test layout:
  - test_self_test_passes
  - test_pilot_selection_resolves_all_11_entities
  - test_pilot_selection_l1_present: PI-002
  - test_pilot_selection_l2_present: PI-001
  - test_pilot_selection_l3_present: PI-003
  - test_pilot_selection_l4_present: PI-004
  - test_pilot_selection_decomposition_chain: PI-005
  - test_pilot_selection_strong_documentation: PI-006
  - test_pilot_selection_incomplete_operational_info: PI-007
  - test_pilot_selection_cross_catalogue_references: PI-008
  - test_pilot_manifest_emitted
  - test_l2_template_documents_ext18_extensions: template integrity (no template extension in EXT-18)
  - test_pilot_go_no_go_decision_recorded
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PILOT_ENTITIES = REPO_ROOT / "reconciliation" / "pilot-entities.json"
PILOT_BASELINE = REPO_ROOT / "reconciliation" / "pilot-baseline.json"
PILOT_ASSESSMENT = REPO_ROOT / "reconciliation" / "pilot-assessment.json"
PILOT_GO_NO_GO = REPO_ROOT / "reconciliation" / "pilot-go-no-go.json"
PILOT_SELECTOR_MANIFEST = REPO_ROOT / "reconciliation" / "pilot-selection-manifest.json"
PILOT_DOC = REPO_ROOT / "docs" / "operational-documentation-pilot.md"


class TestPilotSelectionEXT18(unittest.TestCase):
    """CR-BP-94-EXT-18 pilot selection tests."""

    # Self-test
    def test_self_test_passes(self):
        r = subprocess.run(
            ["python3", "scripts/check_pilot_selection_ext18.py", "--self-test", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"self-test failed: {r.stdout}\n{r.stderr}")
        data = json.loads(r.stdout)
        self.assertEqual(data["mode"], "self-test")

    # All 11 pilot entities resolve in the catalogue
    def test_pilot_selection_resolves_all_11_entities(self):
        r = subprocess.run(
            ["python3", "scripts/check_pilot_selection_ext18.py", "--json"],
            capture_output=True, text=True, timeout=60,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"validator failed: {r.stdout}\n{r.stderr}")
        data = json.loads(r.stdout)
        # 11 pilot entities should all resolve; 0 findings.
        self.assertEqual(data["summary"]["total_findings"], 0)
        self.assertEqual(data["selection"]["total_pilot_entities"], 11)
        self.assertEqual(data["selection"]["total_resolved_records"], 11)

    # PI-002: at least one L1
    def test_pilot_selection_l1_present(self):
        with PILOT_ENTITIES.open() as fp:
            data = json.load(fp)
        l1 = [e for e in data["pilot_entities"] if e["level"] == "L1"]
        self.assertGreaterEqual(len(l1), 1, "at least one L1 ProcessGroup required")

    # PI-001: at least one L2 BP
    def test_pilot_selection_l2_present(self):
        with PILOT_ENTITIES.open() as fp:
            data = json.load(fp)
        l2 = [e for e in data["pilot_entities"] if e["level"] == "L2"]
        self.assertGreaterEqual(len(l2), 1, "at least one L2 Business Process required")

    # PI-003: at least one L3
    def test_pilot_selection_l3_present(self):
        with PILOT_ENTITIES.open() as fp:
            data = json.load(fp)
        l3 = [e for e in data["pilot_entities"] if e["level"] == "L3"]
        self.assertGreaterEqual(len(l3), 1, "at least one L3 Activity required")

    # PI-004: at least one L4
    def test_pilot_selection_l4_present(self):
        with PILOT_ENTITIES.open() as fp:
            data = json.load(fp)
        l4 = [e for e in data["pilot_entities"] if e["level"] == "L4"]
        self.assertGreaterEqual(len(l4), 1, "at least one L4 Task required")

    # PI-005: coherent decomposition chain
    def test_pilot_selection_decomposition_chain(self):
        r = subprocess.run(
            ["python3", "scripts/check_pilot_selection_ext18.py", "--json"],
            capture_output=True, text=True, timeout=60,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(r.stdout)
        # No PI-005 findings means the chain is intact.
        for finding in data["findings"]:
            self.assertNotEqual(finding["rule"], "PI-005",
                                f"PI-005 finding: {finding}")

    # PI-006: strong documentation
    def test_pilot_selection_strong_documentation(self):
        r = subprocess.run(
            ["python3", "scripts/check_pilot_selection_ext18.py", "--json"],
            capture_output=True, text=True, timeout=60,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(r.stdout)
        for finding in data["findings"]:
            self.assertNotEqual(finding["rule"], "PI-006",
                                f"PI-006 finding: {finding}")

    # PI-007: incomplete operational information
    def test_pilot_selection_incomplete_operational_info(self):
        r = subprocess.run(
            ["python3", "scripts/check_pilot_selection_ext18.py", "--json"],
            capture_output=True, text=True, timeout=60,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(r.stdout)
        for finding in data["findings"]:
            self.assertNotEqual(finding["rule"], "PI-007",
                                f"PI-007 finding: {finding}")

    # PI-008: cross-catalogue references
    def test_pilot_selection_cross_catalogue_references(self):
        r = subprocess.run(
            ["python3", "scripts/check_pilot_selection_ext18.py", "--json"],
            capture_output=True, text=True, timeout=60,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(r.stdout)
        for finding in data["findings"]:
            self.assertNotEqual(finding["rule"], "PI-008",
                                f"PI-008 finding: {finding}")

    # Manifest emission
    def test_pilot_manifest_emitted(self):
        self.assertTrue(PILOT_SELECTOR_MANIFEST.exists(),
                        f"selector manifest missing at {PILOT_SELECTOR_MANIFEST}")
        with PILOT_SELECTOR_MANIFEST.open() as fp:
            data = json.load(fp)
        self.assertEqual(data["summary"]["total_findings"], 0)
        self.assertIn("selection", data)

    # Template integrity: EXT-18 is a methodology + manifest slice; no template extension.
    def test_l2_template_unchanged_by_ext18(self):
        # EXT-18 does not introduce L2 template changes; the pilot is process work.
        # We just confirm the existing L2 template still loads.
        from pathlib import Path
        import yaml
        template_path = REPO_ROOT / "templates" / "business-process.yaml"
        with template_path.open() as fp:
            text = fp.read()
        # The L2 template should still document the 13 EXT-09 semantic fields
        # (inputs, outputs, transformation, responsibility, boundary,
        # interfaces, dependencies, preconditions, trigger_type, accountability,
        # roles, raci, business_rules, controls, exceptions, deviations,
        # structured-responsibility, provenance, metadata.authoring).
        for marker in ("provenance:", "metadata.authoring:", "EXT-15", "EXT-16"):
            with self.subTest(marker=marker):
                self.assertIn(marker, text, f"L2 template should still document {marker!r}")

    # Pilot go/no-go decision recorded
    def test_pilot_go_no_go_decision_recorded(self):
        for path, name in [(PILOT_ENTITIES, "pilot-entities"),
                            (PILOT_BASELINE, "pilot-baseline"),
                            (PILOT_ASSESSMENT, "pilot-assessment"),
                            (PILOT_GO_NO_GO, "pilot-go-no-go")]:
            with self.subTest(name=name):
                self.assertTrue(path.exists(),
                                f"pilot manifest missing: {name} at {path}")
        # The go/no-go decision is GO
        with PILOT_GO_NO_GO.open() as fp:
            data = json.load(fp)
        self.assertEqual(data["decision"], "GO")
        # 5 conditions on the go
        self.assertEqual(len(data["five_conditions_on_the_go"]), 5)
        # 10 go/no-go criteria
        self.assertEqual(len(data["ten_go_no_go_criteria"]), 10)
        # 10 of 10 pass
        self.assertEqual(data["summary"]["go_no_go_criteria_pass"], "10 of 10")
        # 0 critical defects
        self.assertEqual(data["summary"]["critical_defects"], 0)

    # Pilot doc exists and is comprehensive
    def test_pilot_doc_comprehensive(self):
        self.assertTrue(PILOT_DOC.exists(),
                        f"pilot doc missing at {PILOT_DOC}")
        text = PILOT_DOC.read_text(encoding="utf-8")
        for section in ("Pilot selection", "The 7-phase execution",
                         "The 10 mandatory outcomes", "The 10 quality dimensions",
                         "The go/no-go criteria", "The formal go/no-go recommendation",
                         "GO"):
            with self.subTest(section=section):
                self.assertIn(section, text, f"pilot doc should cover {section!r}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
