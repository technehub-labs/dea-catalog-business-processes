#!/usr/bin/env python3
"""
tests/test_business_rules_controls_exceptions_ext14.py
=======================================================

Unit + integration tests for the EXT-14 business rules / controls /
exceptions validator (scripts/check_business_rules_controls_exceptions_ext14.py).

Test layout:
  - test_self_test_passes
  - test_l2_record_with_full_ext14_structure_passes
  - test_l0_l1_cannot_carry_ext14_fields: GO-010
  - test_business_rules_source_vocabulary: GO-002
  - test_business_rules_maturity_vocabulary: GO-003
  - test_controls_type_vocabulary: GO-005
  - test_controls_automation_vocabulary: GO-006
  - test_controls_frequency_vocabulary: GO-007
  - test_exceptions_classification_vocabulary: GO-009
  - test_duplicate_rule_id_is_a_finding
  - test_duplicate_control_id_is_a_finding
  - test_duplicate_exception_id_is_a_finding
  - test_live_catalogue_validator_returns_zero_findings: live integration
  - test_manifest_emitted: gate wiring
  - test_l2_template_documents_ext14_extensions: template integrity
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "reconciliation" / "governance-manifest.json"
L2_TEMPLATE = REPO_ROOT / "templates" / "business-process.yaml"


class TestBusinessRulesControlsExceptionsEXT14(unittest.TestCase):
    """CR-BP-94-EXT-14 business rules/controls/exceptions tests."""

    # Self-test
    def test_self_test_passes(self):
        r = subprocess.run(
            ["python3", "scripts/check_business_rules_controls_exceptions_ext14.py", "--self-test", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"self-test failed: {r.stdout}")
        data = json.loads(r.stdout)
        self.assertEqual(data["summary"]["total_findings"], 0)

    # Full L2 record with all EXT-14 fields passes.
    def test_l2_record_with_full_ext14_structure_passes(self):
        record = {
            "id": "test:bp-1",
            "type": "Process",
            "business_rules": [
                {"id": "r1", "name": "KYC must verify identity",
                 "description": "Every customer must be KYC-verified",
                 "source": "regulatory", "source_ref": "https://...",
                 "maturity": "in_force", "rationale": "Per SMCR.",
                 "owner": "compliance_officer"},
            ],
            "controls": [
                {"id": "c1", "name": "ID verification",
                 "description": "Automated ID check",
                 "type": "preventive", "enforces": "r1",
                 "automation": "automated", "frequency": "continuous",
                 "evidence": ["audit log"],
                 "owner": "compliance_officer"},
            ],
            "exceptions": [
                {"id": "e1", "name": "Missing ID",
                 "description": "Customer submits without ID",
                 "classification": "recoverable",
                 "detection": "continuous",
                 "response": "Request ID from customer",
                 "escalation": "Compliance team",
                 "resolution": "Re-attempt with ID",
                 "owner": "compliance_officer"},
            ],
            "deviations": [
                {"id": "d1", "rule_ref": "r1",
                 "description": "Customer onboarded without ID",
                 "status": "remediated", "severity": "high",
                 "detected_at": "2026-10-01",
                 "remediated_at": "2026-10-02",
                 "remediation": "ID obtained"},
            ],
        }
        from scripts.check_business_rules_controls_exceptions_ext14 import evaluate
        findings = evaluate([(Path("test.yaml"), record)])
        self.assertEqual(findings, [], f"unexpected findings: {findings}")

    # GO-010: L0/L1 cannot carry EXT-14 fields.
    def test_l0_l1_cannot_carry_ext14_fields(self):
        from scripts.check_business_rules_controls_exceptions_ext14 import evaluate
        for level_type, level in [("ProcessContext", "L0"), ("ProcessGroup", "L1")]:
            record = {
                "id": f"test:{level}",
                "type": level_type,
                "business_rules": [
                    {"id": "r1", "name": "x", "description": "x",
                     "source": "regulatory", "source_ref": "x",
                     "maturity": "in_force", "rationale": "x", "owner": "x"},
                ],
                "controls": [
                    {"id": "c1", "name": "x", "description": "x",
                     "type": "preventive", "enforces": "x",
                     "automation": "manual", "frequency": "daily",
                     "evidence": ["x"], "owner": "x"},
                ],
                "exceptions": [
                    {"id": "e1", "name": "x", "description": "x",
                     "classification": "recoverable", "detection": "daily",
                     "response": "x", "escalation": "x", "resolution": "x",
                     "owner": "x"},
                ],
                "deviations": [
                    {"id": "d1", "rule_ref": "x", "description": "x",
                     "status": "detected", "severity": "high",
                     "detected_at": "2026-10-01"},
                ],
            }
            with self.subTest(level=level):
                findings = evaluate([(Path(f"test_{level}.yaml"), record)])
                rules = {f["rule"] for f in findings}
                self.assertIn("GO-010", rules,
                              f"L0/L1 should trigger GO-010; got {findings}")

    # GO-002: business_rules[].source vocabulary
    def test_business_rules_source_vocabulary(self):
        from scripts.check_business_rules_controls_exceptions_ext14 import evaluate
        record = {
            "id": "test:bp-bad-source",
            "type": "Process",
            "business_rules": [
                {"id": "r1", "name": "x", "description": "x",
                 "source": "imaginary", "source_ref": "x",
                 "maturity": "in_force", "rationale": "x", "owner": "x"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("GO-002", rules, f"expected GO-002; got {findings}")

    # GO-003: business_rules[].maturity vocabulary
    def test_business_rules_maturity_vocabulary(self):
        from scripts.check_business_rules_controls_exceptions_ext14 import evaluate
        record = {
            "id": "test:bp-bad-maturity",
            "type": "Process",
            "business_rules": [
                {"id": "r1", "name": "x", "description": "x",
                 "source": "regulatory", "source_ref": "x",
                 "maturity": "drafting", "rationale": "x", "owner": "x"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("GO-003", rules, f"expected GO-003; got {findings}")

    # GO-005: controls[].type vocabulary
    def test_controls_type_vocabulary(self):
        from scripts.check_business_rules_controls_exceptions_ext14 import evaluate
        record = {
            "id": "test:bp-bad-ctrl-type",
            "type": "Process",
            "controls": [
                {"id": "c1", "name": "x", "description": "x",
                 "type": "advisory", "enforces": "x",
                 "automation": "manual", "frequency": "daily",
                 "evidence": ["x"], "owner": "x"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("GO-005", rules, f"expected GO-005; got {findings}")

    # GO-006: controls[].automation vocabulary
    def test_controls_automation_vocabulary(self):
        from scripts.check_business_rules_controls_exceptions_ext14 import evaluate
        record = {
            "id": "test:bp-bad-automation",
            "type": "Process",
            "controls": [
                {"id": "c1", "name": "x", "description": "x",
                 "type": "preventive", "enforces": "x",
                 "automation": "ai_magic", "frequency": "daily",
                 "evidence": ["x"], "owner": "x"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("GO-006", rules, f"expected GO-006; got {findings}")

    # GO-007: controls[].frequency vocabulary
    def test_controls_frequency_vocabulary(self):
        from scripts.check_business_rules_controls_exceptions_ext14 import evaluate
        record = {
            "id": "test:bp-bad-freq",
            "type": "Process",
            "controls": [
                {"id": "c1", "name": "x", "description": "x",
                 "type": "preventive", "enforces": "x",
                 "automation": "manual", "frequency": "whenever",
                 "evidence": ["x"], "owner": "x"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("GO-007", rules, f"expected GO-007; got {findings}")

    # GO-009: exceptions[].classification vocabulary
    def test_exceptions_classification_vocabulary(self):
        from scripts.check_business_rules_controls_exceptions_ext14 import evaluate
        record = {
            "id": "test:bp-bad-cls",
            "type": "Process",
            "exceptions": [
                {"id": "e1", "name": "x", "description": "x",
                 "classification": "kinda_works", "detection": "daily",
                 "response": "x", "escalation": "x", "resolution": "x",
                 "owner": "x"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("GO-009", rules, f"expected GO-009; got {findings}")

    # Duplicate rule id
    def test_duplicate_rule_id_is_a_finding(self):
        from scripts.check_business_rules_controls_exceptions_ext14 import evaluate
        record = {
            "id": "test:bp-dup-r",
            "type": "Process",
            "business_rules": [
                {"id": "r1", "name": "x", "description": "x",
                 "source": "regulatory", "source_ref": "x",
                 "maturity": "in_force", "rationale": "x", "owner": "x"},
                {"id": "r1", "name": "y", "description": "y",
                 "source": "regulatory", "source_ref": "x",
                 "maturity": "in_force", "rationale": "x", "owner": "x"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("GO-001", rules, f"expected GO-001; got {findings}")

    # Duplicate control id
    def test_duplicate_control_id_is_a_finding(self):
        from scripts.check_business_rules_controls_exceptions_ext14 import evaluate
        record = {
            "id": "test:bp-dup-c",
            "type": "Process",
            "controls": [
                {"id": "c1", "name": "x", "description": "x",
                 "type": "preventive", "enforces": "x",
                 "automation": "manual", "frequency": "daily",
                 "evidence": ["x"], "owner": "x"},
                {"id": "c1", "name": "y", "description": "y",
                 "type": "preventive", "enforces": "x",
                 "automation": "manual", "frequency": "daily",
                 "evidence": ["x"], "owner": "x"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("GO-004", rules, f"expected GO-004; got {findings}")

    # Duplicate exception id
    def test_duplicate_exception_id_is_a_finding(self):
        from scripts.check_business_rules_controls_exceptions_ext14 import evaluate
        record = {
            "id": "test:bp-dup-e",
            "type": "Process",
            "exceptions": [
                {"id": "e1", "name": "x", "description": "x",
                 "classification": "recoverable", "detection": "daily",
                 "response": "x", "escalation": "x", "resolution": "x",
                 "owner": "x"},
                {"id": "e1", "name": "y", "description": "y",
                 "classification": "recoverable", "detection": "daily",
                 "response": "x", "escalation": "x", "resolution": "x",
                 "owner": "x"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("GO-008", rules, f"expected GO-008; got {findings}")

    # Live integration
    def test_live_catalogue_validator_returns_zero_findings(self):
        r = subprocess.run(
            ["python3", "scripts/check_business_rules_controls_exceptions_ext14.py", "--json"],
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
        for vocab in ("rule_sources", "rule_maturities", "control_types",
                      "control_automation", "control_frequency",
                      "exception_classifications", "deviation_statuses",
                      "deviation_severities"):
            with self.subTest(vocab=vocab):
                self.assertIn(vocab, manifest["controlled_vocabularies"])
                self.assertGreater(len(manifest["controlled_vocabularies"][vocab]), 0)

    # Template integrity
    def test_l2_template_documents_ext14_extensions(self):
        text = L2_TEMPLATE.read_text(encoding="utf-8")
        for marker in (
            "business_rules:",
            "controls:",
            "exceptions:",
            "deviations:",
            "EXT-14",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text,
                              f"L2 template should document {marker!r}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
