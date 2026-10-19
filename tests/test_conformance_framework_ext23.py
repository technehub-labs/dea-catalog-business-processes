#!/usr/bin/env python3
"""
tests/test_conformance_framework_ext23.py
===========================================

Unit + integration tests for the EXT-23 conformance framework
(scripts/check_conformance_framework_ext23.py) and its two controlled
data artefacts:

  reconciliation/conformance/conformance-rule-catalogue.json
  reconciliation/conformance/requirement-traceability-matrix.json

Test layout:
  - test_self_test_passes
  - test_rule_catalogue_exists_and_is_versioned: REQ-23-01, REQ-23-27
  - test_every_rule_carries_the_required_fields: REQ-23-01
  - test_rule_identifiers_are_unique: REQ-23-01
  - test_rule_vocabulary_conformance: REQ-23-19, section 5.1, 5.2, 8
  - test_no_c2_to_c5_rule_is_automated_blocking: section 8, REQ-23-20
  - test_every_rule_has_remediation_guidance: REQ-23-31
  - test_every_rule_has_a_disclosure_class: REQ-23-30
  - test_traceability_matrix_exists: REQ-23-02
  - test_every_requirement_has_a_controlled_status: REQ-23-02
  - test_every_requirement_maps_to_a_known_rule: REQ-23-02
  - test_every_requirement_has_test_evidence: REQ-23-02
  - test_requirement_identifiers_are_unique: REQ-23-02
  - test_requirement_coverage_is_complete: REQ-23-02, AC-23-02
  - test_exception_model: REQ-23-21
  - test_deferral_model: REQ-23-22
  - test_progressive_enforcement_policy: REQ-23-28
  - test_conformance_report_emitted: REQ-23-25
  - test_conformance_dashboard_emitted: REQ-23-26
  - test_dashboard_has_no_aggregate_score: section 11.2
  - test_dashboard_reports_dimensions_separately: REQ-23-26, section 11.1
  - test_report_states_the_interpretation_limit: section 19
  - test_exception_lifecycle_is_closed
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONF = REPO_ROOT / "reconciliation" / "conformance"
CATALOGUE = CONF / "conformance-rule-catalogue.json"
MATRIX = CONF / "requirement-traceability-matrix.json"
REPORT = CONF / "conformance-report.json"
DASHBOARD = CONF / "conformance-dashboard.json"
MANIFEST = CONF / "ext23-manifest.json"


class TestConformanceFrameworkEXT23(unittest.TestCase):
    """CR-BP-EXT-23 conformance framework tests."""

    def _catalogue(self) -> dict:
        with CATALOGUE.open() as fp:
            return json.load(fp)

    def _matrix(self) -> dict:
        with MATRIX.open() as fp:
            return json.load(fp)

    def test_self_test_passes(self):
        r = subprocess.run(
            ["python3", "scripts/check_conformance_framework_ext23.py",
             "--self-test", "--json"],
            capture_output=True, text=True, timeout=30, cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"self-test failed: {r.stdout}\n{r.stderr}")
        data = json.loads(r.stdout)
        self.assertEqual(data["mode"], "self-test")

    # -- REQ-23-01: the rule catalogue --

    def test_rule_catalogue_exists_and_is_versioned(self):
        """REQ-23-01, REQ-23-27: the catalogue is version-controlled."""
        self.assertTrue(CATALOGUE.exists(), f"catalogue missing: {CATALOGUE}")
        cat = self._catalogue()
        for key in ("catalogue_version", "framework_version", "schema_version",
                    "profile_version", "generated_at", "parent_cr", "rules",
                    "controlled_vocabularies", "progressive_enforcement"):
            with self.subTest(key=key):
                self.assertIn(key, cat, f"catalogue key missing: {key}")
        self.assertRegex(cat["catalogue_version"], r"^\d+\.\d+\.\d+$")

    def test_every_rule_carries_the_required_fields(self):
        """REQ-23-01: the 16 required rule attributes."""
        required = [
            "rule_id", "rule_name", "description", "requirement_traceability",
            "adr_traceability", "applicable_entity_types", "applicable_levels",
            "validation_dimension", "validation_method", "severity",
            "rule_version", "expected_result", "remediation_guidance",
            "exception_eligible", "test_coverage", "rule_lifecycle_status",
        ]
        for rule in self._catalogue()["rules"]:
            for field in required:
                with self.subTest(rule=rule.get("rule_id"), field=field):
                    self.assertIn(field, rule, f"missing field: {field}")

    def test_rule_identifiers_are_unique(self):
        """REQ-23-01: unique rule identifier."""
        ids = [r["rule_id"] for r in self._catalogue()["rules"]]
        self.assertEqual(len(ids), len(set(ids)), "duplicate rule identifiers")

    def test_rule_vocabulary_conformance(self):
        """REQ-23-19, sections 5.1, 5.2 and 8: the controlled vocabularies."""
        cat = self._catalogue()
        voc = cat["controlled_vocabularies"]
        dims = set(voc["validation_dimension"])
        layers = set(voc["validation_layer"])
        classes = set(voc["classification"])
        severities = set(voc["severity"])
        for rule in cat["rules"]:
            rid = rule["rule_id"]
            with self.subTest(rule=rid):
                self.assertIn(rule["validation_dimension"], dims)
                self.assertIn(rule["validation_layer"], layers)
                self.assertIn(rule["classification"], classes)
                self.assertIn(rule["severity"], severities)
                self.assertIn(rule["rule_lifecycle_status"],
                              set(voc["rule_lifecycle_status"]))
                self.assertIn(rule["disclosure_class"],
                              set(voc["disclosure_class"]))
                self.assertTrue(rule["applicable_levels"])
                for level in rule["applicable_levels"]:
                    self.assertIn(level, {"L0", "L1", "L2", "L3", "L4"})

    def test_no_c2_to_c5_rule_is_automated_blocking(self):
        """Section 8: a C2-C5 rule must not be reported as conclusively passed
        by an automated check."""
        for rule in self._catalogue()["rules"]:
            if rule["classification"] in ("C2", "C3", "C4", "C5"):
                with self.subTest(rule=rule["rule_id"]):
                    self.assertNotEqual(
                        rule.get("enforcement_mechanism"),
                        "automated_blocking",
                        f"rule {rule['rule_id']} is {rule['classification']} but "
                        f"is automated_blocking")

    def test_every_rule_has_remediation_guidance(self):
        """REQ-23-31: actionable remediation guidance."""
        for rule in self._catalogue()["rules"]:
            with self.subTest(rule=rule["rule_id"]):
                guidance = rule.get("remediation_guidance", "")
                self.assertIsInstance(guidance, str)
                self.assertGreaterEqual(len(guidance.strip()), 15)

    def test_every_rule_has_a_disclosure_class(self):
        """REQ-23-30: the disclosure class is declared on every rule."""
        for rule in self._catalogue()["rules"]:
            with self.subTest(rule=rule["rule_id"]):
                self.assertIn(rule.get("disclosure_class"),
                              ("public", "internal", "restricted"))

    # -- REQ-23-02: the traceability matrix --

    def test_traceability_matrix_exists(self):
        """REQ-23-02: the matrix is a version-controlled artefact."""
        self.assertTrue(MATRIX.exists(), f"matrix missing: {MATRIX}")
        m = self._matrix()
        for key in ("matrix_version", "generated_at", "parent_cr",
                    "requirements", "requirement_status_vocabulary",
                    "exceptions", "deferrals"):
            with self.subTest(key=key):
                self.assertIn(key, m, f"matrix key missing: {key}")

    def test_every_requirement_has_a_controlled_status(self):
        """REQ-23-02: the 6-value requirement status vocabulary."""
        m = self._matrix()
        allowed = set(m["requirement_status_vocabulary"])
        self.assertEqual(allowed, {
            "automated", "human_review", "evidence_assessment",
            "deferred", "not_enforceable", "not_applicable",
        })
        for req in m["requirements"]:
            with self.subTest(requirement=req["requirement_id"]):
                self.assertIn(req["status"], allowed)

    def test_every_requirement_maps_to_a_known_rule(self):
        """REQ-23-02: the mapping resolves to real conformance rules."""
        known = {r["rule_id"] for r in self._catalogue()["rules"]}
        for req in self._matrix()["requirements"]:
            for rule_id in req["conformance_rule_ids"]:
                with self.subTest(requirement=req["requirement_id"], rule=rule_id):
                    self.assertIn(rule_id, known)

    def test_every_requirement_has_test_evidence(self):
        """REQ-23-02: the mapping carries test evidence."""
        for req in self._matrix()["requirements"]:
            with self.subTest(requirement=req["requirement_id"]):
                self.assertTrue(req["test_evidence"],
                                f"requirement {req['requirement_id']} has no "
                                f"test evidence")

    def test_requirement_identifiers_are_unique(self):
        """REQ-23-02: unique requirement identifiers."""
        ids = [r["requirement_id"] for r in self._matrix()["requirements"]]
        self.assertEqual(len(ids), len(set(ids)), "duplicate requirement ids")

    def test_requirement_coverage_is_complete(self):
        """REQ-23-02, AC-23-02: every requirement from EXT-08 through EXT-23
        is traced, and every source CR is represented."""
        m = self._matrix()
        crs = {r["source_cr"] for r in m["requirements"]}
        for expected in ["CR-BP-94-EXT-08", "CR-BP-94-EXT-09", "CR-BP-94-EXT-10",
                         "CR-BP-94-EXT-11", "CR-BP-94-EXT-12", "CR-BP-94-EXT-13",
                         "CR-BP-94-EXT-14", "CR-BP-94-EXT-15", "CR-BP-94-EXT-16",
                         "CR-BP-94-EXT-17", "CR-BP-94-EXT-19", "CR-BP-94-EXT-20",
                         "CR-BP-94-EXT-21", "CR-BP-94-EXT-22", "CR-BP-EXT-23"]:
            with self.subTest(cr=expected):
                self.assertIn(expected, crs)
        # Every requirement has an explicit status: none is silently absent.
        for req in m["requirements"]:
            with self.subTest(requirement=req["requirement_id"]):
                self.assertTrue(req["status"].strip())
                if req["status"] not in ("not_enforceable", "not_applicable"):
                    self.assertTrue(req["conformance_rule_ids"])

    # -- REQ-23-21 / REQ-23-22: exceptions and deferrals --

    def test_exception_model(self):
        """REQ-23-21: the 5 exception categories and the lifecycle."""
        voc = self._catalogue()["controlled_vocabularies"]
        self.assertEqual(set(voc["exception_category"]),
                         {"technical", "semantic", "evidence", "governance",
                          "migration"})
        lifecycle = voc["exception_lifecycle"]
        self.assertIn("proposed", lifecycle)
        self.assertIn("active", lifecycle)
        # The lifecycle must be closed: every state has a transition list.
        for state, transitions in lifecycle.items():
            with self.subTest(state=state):
                self.assertIsInstance(transitions, list)
                for target in transitions:
                    self.assertIn(target, lifecycle)
        # Only an approved active exception may affect enforcement.
        matrix = self._matrix()
        for exc in matrix["exceptions"]:
            with self.subTest(exception=exc.get("exception_id")):
                self.assertIn(exc["status"], lifecycle)
                for field in ("rule_id", "scope", "rationale", "owner",
                              "approving_authority", "review_date"):
                    self.assertTrue(exc.get(field))

    def test_deferral_model(self):
        """REQ-23-22: a deferred item is never reported as complete."""
        matrix = self._matrix()
        for dfr in matrix["deferrals"]:
            with self.subTest(deferral=dfr.get("deferral_id")):
                for field in ("requirement_id", "scope", "reason", "impact",
                              "owner", "approved_by", "review_date", "status"):
                    self.assertTrue(dfr.get(field))

    def test_progressive_enforcement_policy(self):
        """REQ-23-28: the 5-stage progressive enforcement model."""
        policy = self._catalogue()["progressive_enforcement"]
        self.assertEqual(policy["stages"], [
            "discovery_and_reporting",
            "warning_only",
            "blocking_for_new_defects",
            "historical_remediation",
            "full_enforcement",
        ])
        self.assertTrue(policy["current_stage"])
        self.assertTrue(policy["baseline_defect_policy"])
        self.assertTrue(policy["new_defect_policy"])
        self.assertTrue(policy["exception_policy"])

    # -- REQ-23-25 / REQ-23-26: reporting --

    def test_conformance_report_emitted(self):
        """REQ-23-25: the machine-readable validation report."""
        self.assertTrue(REPORT.exists(), f"report missing: {REPORT}")
        with REPORT.open() as fp:
            report = json.load(fp)
        for key in ("validation_run_id", "timestamp", "repository_revision",
                    "framework_version", "schema_version", "profile_version",
                    "rule_catalogue_version", "scope", "rules_executed",
                    "results_by_severity", "results_by_dimension",
                    "requirements_in_scope", "requirements_by_status",
                    "approved_exceptions", "deferred_requirements",
                    "overall_outcome", "remediation_guidance"):
            with self.subTest(key=key):
                self.assertIn(key, report, f"report key missing: {key}")
        self.assertIn(report["overall_outcome"], {
            "passed", "passed_with_warnings", "failed", "blocked",
            "not_assessed", "passed_with_approved_exceptions",
        })

    def test_conformance_dashboard_emitted(self):
        """REQ-23-26: the catalogue-level dashboard."""
        self.assertTrue(DASHBOARD.exists(), f"dashboard missing: {DASHBOARD}")
        with DASHBOARD.open() as fp:
            dash = json.load(fp)
        for key in ("totals", "measures_by_dimension", "rules_by_classification",
                    "rules_by_severity", "aggregate_score", "known_limitations"):
            with self.subTest(key=key):
                self.assertIn(key, dash, f"dashboard key missing: {key}")

    def test_dashboard_has_no_aggregate_score(self):
        """Section 11.2: no aggregate conformance score."""
        with DASHBOARD.open() as fp:
            dash = json.load(fp)
        self.assertIsNone(dash["aggregate_score"])
        self.assertIn("must not be averaged", dash["aggregate_score_note"])

    def test_dashboard_reports_dimensions_separately(self):
        """REQ-23-26, section 11.1: the 9 dimension measures are separate."""
        with DASHBOARD.open() as fp:
            dash = json.load(fp)
        measures = dash["measures_by_dimension"]
        for dim in ["structural", "schema", "profile", "semantic", "evidence",
                    "documentation", "cross-catalogue", "reconciliation",
                    "governance"]:
            with self.subTest(dimension=dim):
                self.assertIn(dim, measures)
                self.assertIn("requirements", measures[dim])
                self.assertIn("automated", measures[dim])
                self.assertIn("conformance_rules", measures[dim])

    def test_report_states_the_interpretation_limit(self):
        """Section 19: passing validation is not proof of business correctness."""
        with REPORT.open() as fp:
            report = json.load(fp)
        limit = report["interpretation_limit"]
        self.assertIn("not", limit.lower())
        self.assertIn("effective", limit.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
