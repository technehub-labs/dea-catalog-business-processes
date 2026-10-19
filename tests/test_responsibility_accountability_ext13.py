#!/usr/bin/env python3
"""
tests/test_responsibility_accountability_ext13.py
==================================================

Unit + integration tests for the EXT-13 responsibility/accountability
validator (scripts/check_responsibility_accountability_ext13.py).

Test layout:
  - test_self_test_passes: validator's self-test returns 0 findings
  - test_l2_record_with_full_ext13_structure_passes
  - test_l0_l1_cannot_carry_accountability_roles_raci: RA-010
  - test_responsibility_type_vocabulary: RA-002
  - test_accountability_type_vocabulary: RA-004
  - test_role_type_vocabulary: RA-006
  - test_raci_scheme_vocabulary: RA-007
  - test_raci_assignment_vocabulary: RA-008
  - test_role_references_resolve_to_catalog: RA-009
  - test_role_reference_does_not_resolve_is_a_finding
  - test_accountability_rationale_required_and_nonempty: RA-003
  - test_live_catalogue_validator_returns_zero_findings: live integration
  - test_manifest_emitted: gate wiring
  - test_l2_template_documents_ext13_extensions: template integrity
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "reconciliation" / "responsibility-accountability-manifest.json"
L2_TEMPLATE = REPO_ROOT / "templates" / "business-process.yaml"


class TestResponsibilityAccountabilityEXT13(unittest.TestCase):
    """CR-BP-94-EXT-13 responsibility/accountability tests."""

    # Self-test
    def test_self_test_passes(self):
        r = subprocess.run(
            ["python3", "scripts/check_responsibility_accountability_ext13.py", "--self-test", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"self-test failed: {r.stdout}")
        data = json.loads(r.stdout)
        self.assertEqual(data["summary"]["total_findings"], 0)

    # Full L2 record with all EXT-13 structured fields passes.
    def test_l2_record_with_full_ext13_structure_passes(self):
        record = {
            "id": "test:bp-1",
            "type": "Process",
            "responsibility": [
                {"role": "kyc_analyst", "performer": "KYC Analyst",
                 "type": "human", "scope": "process",
                 "accountabilities": ["Verify identity"]},
            ],
            "accountability": [
                {"role": "compliance_officer", "type": "human",
                 "scope": "process",
                 "outcomes": ["Customer is KYC-cleared"],
                 "rationale": "Per SMCR, the compliance officer is accountable for KYC outcomes"},
            ],
            "roles": [
                {"id": "kyc_analyst", "name": "KYC Analyst",
                 "type": "organisational", "description": "...",
                 "reporting_line": "Compliance", "capability_owner": "Compliance"},
                {"id": "compliance_officer", "name": "Compliance Officer",
                 "type": "organisational", "description": "...",
                 "reporting_line": "Compliance", "capability_owner": "Compliance"},
            ],
            "raci": [
                {"id": "raci-1", "scheme": "raci",
                 "assignments": [
                     {"role": "kyc_analyst", "activity": "act-1",
                      "assignment": "responsible"},
                     {"role": "compliance_officer", "activity": "act-1",
                      "assignment": "accountable"},
                 ]},
            ],
        }
        from scripts.check_responsibility_accountability_ext13 import evaluate
        findings = evaluate([(Path("test.yaml"), record)])
        self.assertEqual(findings, [], f"unexpected findings: {findings}")

    # RA-010: L0/L1 records cannot carry accountability/roles/raci.
    def test_l0_l1_cannot_carry_accountability_roles_raci(self):
        from scripts.check_responsibility_accountability_ext13 import evaluate
        for level_type, level in [("ProcessContext", "L0"), ("ProcessGroup", "L1")]:
            record = {
                "id": f"test:{level}",
                "type": level_type,
                "accountability": [
                    {"role": "x", "type": "human", "scope": "process",
                     "outcomes": ["x"], "rationale": "x"},
                ],
                "roles": [
                    {"id": "x", "name": "x", "type": "organisational",
                     "description": "x", "reporting_line": "x",
                     "capability_owner": "x"},
                ],
                "raci": [
                    {"id": "r1", "scheme": "raci",
                     "assignments": [{"role": "x", "activity": "x",
                                       "assignment": "responsible"}]},
                ],
            }
            with self.subTest(level=level):
                findings = evaluate([(Path(f"test_{level}.yaml"), record)])
                rules = {f["rule"] for f in findings}
                self.assertIn("RA-010", rules, f"L0/L1 should trigger RA-010; got {findings}")

    # RA-002: responsibility[].type vocabulary
    def test_responsibility_type_vocabulary(self):
        from scripts.check_responsibility_accountability_ext13 import evaluate
        record = {
            "id": "test:bp-bad-resp",
            "type": "Process",
            "responsibility": [
                {"role": "r1", "performer": "p1", "type": "robot",
                 "scope": "process", "accountabilities": ["x"]},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("RA-002", rules, f"expected RA-002; got {findings}")

    # RA-004: accountability[].type vocabulary
    def test_accountability_type_vocabulary(self):
        from scripts.check_responsibility_accountability_ext13 import evaluate
        record = {
            "id": "test:bp-bad-acc",
            "type": "Process",
            "accountability": [
                {"role": "r1", "type": "ai",
                 "scope": "process", "outcomes": ["x"], "rationale": "x"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("RA-004", rules, f"expected RA-004; got {findings}")

    # RA-006: roles[].type vocabulary
    def test_role_type_vocabulary(self):
        from scripts.check_responsibility_accountability_ext13 import evaluate
        record = {
            "id": "test:bp-bad-role",
            "type": "Process",
            "roles": [
                {"id": "r1", "name": "x", "type": "internal",
                 "description": "x", "reporting_line": "x", "capability_owner": "x"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("RA-006", rules, f"expected RA-006; got {findings}")

    # RA-007: raci[].scheme vocabulary
    def test_raci_scheme_vocabulary(self):
        from scripts.check_responsibility_accountability_ext13 import evaluate
        record = {
            "id": "test:bp-bad-scheme",
            "type": "Process",
            "raci": [
                {"id": "r1", "scheme": "made_up_scheme",
                 "assignments": []},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("RA-007", rules, f"expected RA-007; got {findings}")

    # RA-008: raci[].assignments[].assignment vocabulary
    def test_raci_assignment_vocabulary(self):
        from scripts.check_responsibility_accountability_ext13 import evaluate
        record = {
            "id": "test:bp-bad-assign",
            "type": "Process",
            "raci": [
                {"id": "r1", "scheme": "raci",
                 "assignments": [{"role": "r", "activity": "a",
                                   "assignment": "imaginary"}]},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("RA-008", rules, f"expected RA-008; got {findings}")

    # RA-009: role references resolve
    def test_role_references_resolve_to_catalog(self):
        from scripts.check_responsibility_accountability_ext13 import evaluate
        record = {
            "id": "test:bp-resolved",
            "type": "Process",
            "responsibility": [
                {"role": "kyc_analyst", "performer": "KYC Analyst",
                 "type": "human", "scope": "process",
                 "accountabilities": ["x"]},
            ],
            "accountability": [
                {"role": "compliance_officer", "type": "human",
                 "scope": "process", "outcomes": ["x"],
                 "rationale": "Per SMCR..."},
            ],
            "roles": [
                {"id": "kyc_analyst", "name": "KYC Analyst",
                 "type": "organisational", "description": "...",
                 "reporting_line": "Compliance", "capability_owner": "Compliance"},
                {"id": "compliance_officer", "name": "Compliance Officer",
                 "type": "organisational", "description": "...",
                 "reporting_line": "Compliance", "capability_owner": "Compliance"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertNotIn("RA-009", rules, f"unexpected RA-009: {findings}")

    # RA-009: role reference does not resolve
    def test_role_reference_does_not_resolve_is_a_finding(self):
        from scripts.check_responsibility_accountability_ext13 import evaluate
        record = {
            "id": "test:bp-unresolved",
            "type": "Process",
            "responsibility": [
                {"role": "phantom_role", "performer": "...",
                 "type": "human", "scope": "process",
                 "accountabilities": ["x"]},
            ],
            "roles": [
                {"id": "kyc_analyst", "name": "KYC Analyst",
                 "type": "organisational", "description": "...",
                 "reporting_line": "Compliance", "capability_owner": "Compliance"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("RA-009", rules, f"expected RA-009; got {findings}")

    # RA-003: accountability.rationale must be non-empty
    def test_accountability_rationale_required_and_nonempty(self):
        from scripts.check_responsibility_accountability_ext13 import evaluate
        record = {
            "id": "test:bp-empty-rationale",
            "type": "Process",
            "accountability": [
                {"role": "r1", "type": "human", "scope": "process",
                 "outcomes": ["x"], "rationale": ""},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("RA-003", rules, f"expected RA-003; got {findings}")

    # Live integration
    def test_live_catalogue_validator_returns_zero_findings(self):
        r = subprocess.run(
            ["python3", "scripts/check_responsibility_accountability_ext13.py", "--json"],
            capture_output=True, text=True, timeout=60,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"live validator failed: {r.stdout}\n{r.stderr}")
        data = json.loads(r.stdout)
        self.assertEqual(data["summary"]["total_findings"], 0,
                         f"live findings: {data['findings']}")

    # Manifest emission
    def test_manifest_emitted(self):
        self.assertTrue(MANIFEST_PATH.exists(),
                        f"manifest missing at {MANIFEST_PATH}")
        with MANIFEST_PATH.open(encoding="utf-8") as fp:
            manifest = json.load(fp)
        self.assertIn("controlled_vocabularies", manifest)
        for vocab in ("performer_types", "accountable_types", "role_types",
                      "raci_schemes", "raci_assignments"):
            with self.subTest(vocab=vocab):
                self.assertIn(vocab, manifest["controlled_vocabularies"])
                self.assertGreater(len(manifest["controlled_vocabularies"][vocab]), 0)

    # Template integrity
    def test_l2_template_documents_ext13_extensions(self):
        text = L2_TEMPLATE.read_text(encoding="utf-8")
        for marker in (
            "accountability:",
            "roles:",
            "raci:",
            "EXT-13",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text,
                              f"L2 template should document {marker!r}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
