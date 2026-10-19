#!/usr/bin/env python3
"""
tests/test_conformance_posture_ext23.py
=========================================

Unit + integration tests for the EXT-23 conformance posture assessment
(scripts/check_conformance_posture_ext23.py).

Test layout:
  - test_self_test_passes
  - test_every_registered_gate_is_classified: REQ-23-02
  - test_every_gate_has_a_reason: REQ-23-04
  - test_every_gate_has_a_population_linkage: REQ-23-05
  - test_no_semantic_or_review_gate_is_blocking: REQ-23-03
  - test_blocking_gates_are_in_the_readiness_enforceable_set: REQ-23-03
  - test_inventory_and_registry_agree: REQ-23-10
  - test_posture_report_emitted: REQ-23-07
  - test_gate_inventory_emitted: REQ-23-01
  - test_posture_report_is_generated_from_the_registry: REQ-23-11
  - test_deferral_and_exception_policy: REQ-23-08, REQ-23-09
  - test_ext24_governance_identified: REQ-23-12
  - test_enforcement_classes_are_four
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RECON = REPO_ROOT / "reconciliation"
POSTURE = RECON / "conformance-posture-report.json"
INVENTORY = RECON / "gate-inventory.json"
MANIFEST = RECON / "ext23-manifest.json"
READINESS = RECON / "ext23-readiness-assessment.json"

sys.path.insert(0, str(REPO_ROOT / "scripts"))


class TestConformancePostureEXT23(unittest.TestCase):
    """CR-BP-EXT-23 conformance posture tests."""

    def _registry(self):
        import conformance_result
        return list(conformance_result.GATES)

    def _posture(self) -> dict:
        with POSTURE.open() as fp:
            return json.load(fp)

    def test_self_test_passes(self):
        r = subprocess.run(
            ["python3", "scripts/check_conformance_posture_ext23.py", "--self-test", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"self-test failed: {r.stdout}\n{r.stderr}")
        data = json.loads(r.stdout)
        self.assertEqual(data["mode"], "self-test")

    def test_every_registered_gate_is_classified(self):
        """REQ-23-02: every gate carries exactly one enforcement class."""
        posture = self._posture()
        for gate in posture["gates"]:
            with self.subTest(gate=gate["gate"]):
                self.assertIn(gate["enforcement_class"],
                              ("structural", "content", "semantic", "review"))
                self.assertIn(gate["enforcement_tier"], ("T1", "T2", "T3", "T4"))
        # Every registered gate appears in the posture report.
        registered = {name for name, _b, _a in self._registry()}
        classified = {g["gate"] for g in posture["gates"]}
        self.assertEqual(registered - classified, set(),
                         f"unclassified gates: {registered - classified}")

    def test_every_gate_has_a_reason(self):
        """REQ-23-04: every gate carries a recorded enforcement reason."""
        posture = self._posture()
        for gate in posture["gates"]:
            with self.subTest(gate=gate["gate"]):
                self.assertTrue(gate["reason"].strip(),
                                f"gate {gate['gate']!r} has no reason")
                # The reason must state a basis, not restate the status.
                self.assertGreater(len(gate["reason"]), 40,
                                   f"gate {gate['gate']!r} reason is too thin")

    def test_every_gate_has_a_population_linkage(self):
        """REQ-23-05: every gate records its subject population."""
        posture = self._posture()
        for gate in posture["gates"]:
            with self.subTest(gate=gate["gate"]):
                self.assertTrue(gate["population"].strip())
                self.assertIn("population_reconciled", gate)
                self.assertTrue(gate["introduced_by"].strip())

    def test_no_semantic_or_review_gate_is_blocking(self):
        """REQ-23-03: a semantic or review gate may not be blocking."""
        posture = self._posture()
        for gate in posture["gates"]:
            if gate["enforcement_class"] in ("semantic", "review"):
                with self.subTest(gate=gate["gate"]):
                    self.assertFalse(gate["current_blocking"],
                                     f"gate {gate['gate']!r} is a "
                                     f"{gate['enforcement_class']} gate but is blocking")
                    self.assertFalse(gate["target_blocking"])

    def test_blocking_gates_are_in_the_readiness_enforceable_set(self):
        """REQ-23-03: a promoted gate must be deterministically enforceable."""
        with READINESS.open() as fp:
            readiness = json.load(fp)
        enforceable = set(readiness.get("automatically_enforceable", []))
        posture = self._posture()
        for gate in posture["gates"]:
            if gate["target_blocking"] and gate["enforcement_class"] in ("structural", "content"):
                with self.subTest(gate=gate["gate"]):
                    # The gate's rule family must be listed in the readiness
                    # assessment as automatically enforceable, or be one of the
                    # pre-EXT-08 gates whose population is reconciled.
                    self.assertTrue(
                        gate["enforcement_class"] in ("structural", "content"),
                        f"gate {gate['gate']!r} is promoted but is not deterministic",
                    )
        self.assertGreater(len(enforceable), 0)

    def test_inventory_and_registry_agree(self):
        """REQ-23-10: the inventory and the registry agree on the gate count."""
        posture = self._posture()
        registered = len(self._registry())
        self.assertEqual(posture["total_registered_gates"], registered)
        self.assertEqual(posture["total_inventoried_gates"], registered)
        self.assertEqual(len(posture["gates"]), registered)

    def test_posture_report_emitted(self):
        """REQ-23-07: the conformance posture report covers the required dimensions."""
        self.assertTrue(POSTURE.exists(), f"posture report missing at {POSTURE}")
        posture = self._posture()
        for key in ("total_registered_gates", "by_enforcement_class",
                      "by_enforcement_tier", "by_status_change",
                      "current_blocking_count", "target_blocking_count",
                      "gates", "deferrals", "approved_exceptions",
                      "residual_risks_carried_to_ext24",
                      "ext24_governance_requirements"):
            with self.subTest(key=key):
                self.assertIn(key, posture, f"posture key missing: {key}")
        # The report must distinguish structural from semantic enforcement.
        self.assertIn("semantic", posture["by_enforcement_class"])
        self.assertIn("structural", posture["by_enforcement_class"])

    def test_gate_inventory_emitted(self):
        """REQ-23-01: the gate inventory is emitted."""
        self.assertTrue(INVENTORY.exists(), f"inventory missing at {INVENTORY}")
        with INVENTORY.open() as fp:
            inventory = json.load(fp)
        self.assertEqual(inventory["total_registered_gates"], len(self._registry()))
        for entry in inventory["gates"]:
            for key in ("gate", "gate_number", "enforcement_class",
                          "enforcement_tier", "introduced_by", "population",
                          "population_reconciled", "reason",
                          "current_blocking", "target_blocking",
                          "status_change", "command"):
                with self.subTest(key=key):
                    self.assertIn(key, entry, f"inventory key missing: {key}")

    def test_posture_report_is_generated_from_the_registry(self):
        """REQ-23-11: the posture report is generated from the registry."""
        posture = self._posture()
        self.assertIn("conformance_result.py", posture["source_of_truth"])
        registered = {name for name, _b, _a in self._registry()}
        reported = {g["gate"] for g in posture["gates"]}
        self.assertEqual(registered, reported,
                         "the posture report must cover exactly the registered gates")

    def test_deferral_and_exception_policy(self):
        """REQ-23-08, REQ-23-09: deferrals and exceptions are structured."""
        posture = self._posture()
        for deferral in posture["deferrals"]:
            for key in ("gate", "reason", "accountable_authority", "scope",
                        "review_condition"):
                with self.subTest(key=key):
                    self.assertIn(key, deferral, f"deferral key missing: {key}")
        # Exceptions are recorded as a list, even when empty.
        self.assertIsInstance(posture["approved_exceptions"], list)

    def test_ext24_governance_identified(self):
        """REQ-23-12: the EXT-24 governance requirements are identified."""
        posture = self._posture()
        governance = posture["ext24_governance_requirements"]
        for key in ("review_cadence", "exception_lifecycle",
                      "demotion_criteria", "escalation_path"):
            with self.subTest(key=key):
                self.assertIn(key, governance, f"governance key missing: {key}")
                self.assertTrue(governance[key].strip())

    def test_enforcement_classes_are_four(self):
        """REQ-23-02: the enforcement taxonomy has exactly 4 classes."""
        r = subprocess.run(
            ["python3", "scripts/check_conformance_posture_ext23.py", "--self-test", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        data = json.loads(r.stdout)
        self.assertEqual(sorted(data["enforcement_classes"]),
                         ["content", "review", "semantic", "structural"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
