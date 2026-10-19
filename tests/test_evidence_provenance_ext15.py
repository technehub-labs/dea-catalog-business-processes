#!/usr/bin/env python3
"""
tests/test_evidence_provenance_ext15.py
=======================================

Unit + integration tests for the EXT-15 evidence/provenance/confidence
validator (scripts/check_evidence_provenance_ext15.py).

Test layout:
  - test_self_test_passes
  - test_l2_record_with_full_ext15_structure_passes
  - test_l0_l1_cannot_carry_top_level_provenance: EV-010
  - test_provenance_source_class_vocabulary: EV-002
  - test_provenance_confidentiality_vocabulary: EV-003
  - test_provenance_review_status_vocabulary: EV-004
  - test_ai_assisted_source_requires_evidence_limitations: EV-005
  - test_per_assertion_confidence_vocabulary: EV-006
  - test_per_assertion_verification_status_vocabulary: EV-007
  - test_per_assertion_uncertainty_state_vocabulary: EV-008
  - test_duplicate_provenance_id_is_a_finding
  - test_live_catalogue_validator_returns_zero_findings: live integration
  - test_manifest_emitted: gate wiring
  - test_l2_template_documents_ext15_extensions: template integrity
  - test_multiple_provenance_records_for_same_assertion: EV-009 (allowed)
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "reconciliation" / "evidence-manifest.json"
L2_TEMPLATE = REPO_ROOT / "templates" / "business-process.yaml"


class TestEvidenceProvenanceEXT15(unittest.TestCase):
    """CR-BP-94-EXT-15 evidence/provenance/confidence tests."""

    # Self-test
    def test_self_test_passes(self):
        r = subprocess.run(
            ["python3", "scripts/check_evidence_provenance_ext15.py", "--self-test", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"self-test failed: {r.stdout}")
        data = json.loads(r.stdout)
        self.assertEqual(data["summary"]["total_findings"], 0)

    # Full L2 record with all EXT-15 fields passes.
    def test_l2_record_with_full_ext15_structure_passes(self):
        record = {
            "id": "test:bp-1",
            "type": "Process",
            "provenance": [
                {"id": "prov-1",
                 "source": {"title": "KYC Policy v3.2",
                            "source_class": "authoritative_document",
                            "owner": "Compliance",
                            "location": "https://...",
                            "publication_date": "2026-01-15",
                            "accessed_date": "2026-10-19",
                            "confidentiality": "internal"},
                 "assertions_supported": ["KYC required for all customers"],
                 "evidence_limitations": "Covers UK only",
                 "reviewer": "Compliance Officer",
                 "review_status": "verified",
                 "review_date": "2026-10-19"},
            ],
            "inputs": [
                {"id": "i1", "name": "Customer ID",
                 "description": "Government-issued ID",
                 "source": "customer",
                 "provenance": {"source": "prov-1",
                                "confidence": "high",
                                "verification_status": "verified",
                                "verification_date": "2026-10-19",
                                "verification_reviewer": "Compliance Officer",
                                "uncertainty_state": "not_applicable"}},
            ],
        }
        from scripts.check_evidence_provenance_ext15 import evaluate
        findings = evaluate([(Path("test.yaml"), record)])
        self.assertEqual(findings, [], f"unexpected findings: {findings}")

    # EV-010: L0/L1 cannot carry top-level provenance.
    def test_l0_l1_cannot_carry_top_level_provenance(self):
        from scripts.check_evidence_provenance_ext15 import evaluate
        for level_type, level in [("ProcessContext", "L0"), ("ProcessGroup", "L1")]:
            record = {
                "id": f"test:{level}",
                "type": level_type,
                "provenance": [
                    {"id": "prov-1",
                     "source": {"title": "x", "source_class": "authoritative_document"},
                     "assertions_supported": ["x"],
                     "review_status": "verified"},
                ],
            }
            with self.subTest(level=level):
                findings = evaluate([(Path(f"test_{level}.yaml"), record)])
                rules = {f["rule"] for f in findings}
                self.assertIn("EV-010", rules,
                              f"L0/L1 should trigger EV-010; got {findings}")

    # EV-002: source.source_class vocabulary
    def test_provenance_source_class_vocabulary(self):
        from scripts.check_evidence_provenance_ext15 import evaluate
        record = {
            "id": "test:bp-bad-source",
            "type": "Process",
            "provenance": [
                {"id": "prov-1",
                 "source": {"title": "x", "source_class": "fake_source"},
                 "assertions_supported": ["x"],
                 "review_status": "verified"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("EV-002", rules, f"expected EV-002; got {findings}")

    # EV-003: confidentiality vocabulary
    def test_provenance_confidentiality_vocabulary(self):
        from scripts.check_evidence_provenance_ext15 import evaluate
        record = {
            "id": "test:bp-bad-conf",
            "type": "Process",
            "provenance": [
                {"id": "prov-1",
                 "source": {"title": "x", "source_class": "authoritative_document",
                            "confidentiality": "top_secret"},
                 "assertions_supported": ["x"],
                 "review_status": "verified"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("EV-003", rules, f"expected EV-003; got {findings}")

    # EV-004: review_status vocabulary
    def test_provenance_review_status_vocabulary(self):
        from scripts.check_evidence_provenance_ext15 import evaluate
        record = {
            "id": "test:bp-bad-rs",
            "type": "Process",
            "provenance": [
                {"id": "prov-1",
                 "source": {"title": "x", "source_class": "authoritative_document"},
                 "assertions_supported": ["x"],
                 "review_status": "kind_of_verified"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("EV-004", rules, f"expected EV-004; got {findings}")

    # EV-005: AI-assisted source requires non-empty evidence_limitations
    def test_ai_assisted_source_requires_evidence_limitations(self):
        from scripts.check_evidence_provenance_ext15 import evaluate
        record = {
            "id": "test:bp-ai-no-limits",
            "type": "Process",
            "provenance": [
                {"id": "prov-1",
                 "source": {"title": "AI summary", "source_class": "ai_assisted_research"},
                 "assertions_supported": ["x"],
                 "review_status": "verified",
                 "evidence_limitations": ""},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("EV-005", rules, f"expected EV-005; got {findings}")

    # AI-assisted source WITH limitations passes
    def test_ai_assisted_source_with_limitations_passes(self):
        from scripts.check_evidence_provenance_ext15 import evaluate
        record = {
            "id": "test:bp-ai-with-limits",
            "type": "Process",
            "provenance": [
                {"id": "prov-1",
                 "source": {"title": "AI summary", "source_class": "ai_assisted_research"},
                 "assertions_supported": ["x"],
                 "review_status": "verified",
                 "evidence_limitations": "AI summary requires independent validation"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertNotIn("EV-005", rules, f"unexpected EV-005: {findings}")

    # EV-006: confidence vocabulary
    def test_per_assertion_confidence_vocabulary(self):
        from scripts.check_evidence_provenance_ext15 import evaluate
        record = {
            "id": "test:bp-bad-conf",
            "type": "Process",
            "inputs": [
                {"id": "i1", "name": "x", "description": "x",
                 "provenance": {"confidence": "definitely"}},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("EV-006", rules, f"expected EV-006; got {findings}")

    # EV-007: verification_status vocabulary
    def test_per_assertion_verification_status_vocabulary(self):
        from scripts.check_evidence_provenance_ext15 import evaluate
        record = {
            "id": "test:bp-bad-vs",
            "type": "Process",
            "inputs": [
                {"id": "i1", "name": "x", "description": "x",
                 "provenance": {"verification_status": "kind_of"}},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("EV-007", rules, f"expected EV-007; got {findings}")

    # EV-008: uncertainty_state vocabulary
    def test_per_assertion_uncertainty_state_vocabulary(self):
        from scripts.check_evidence_provenance_ext15 import evaluate
        record = {
            "id": "test:bp-bad-us",
            "type": "Process",
            "inputs": [
                {"id": "i1", "name": "x", "description": "x",
                 "provenance": {"uncertainty_state": "maybe"}},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("EV-008", rules, f"expected EV-008; got {findings}")

    # Duplicate provenance id
    def test_duplicate_provenance_id_is_a_finding(self):
        from scripts.check_evidence_provenance_ext15 import evaluate
        record = {
            "id": "test:bp-dup-prov",
            "type": "Process",
            "provenance": [
                {"id": "prov-1",
                 "source": {"title": "x", "source_class": "authoritative_document"},
                 "assertions_supported": ["x"],
                 "review_status": "verified"},
                {"id": "prov-1",
                 "source": {"title": "y", "source_class": "authoritative_document"},
                 "assertions_supported": ["y"],
                 "review_status": "verified"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("EV-001", rules, f"expected EV-001; got {findings}")

    # EV-009: multiple provenance records for the same assertion are allowed
    def test_multiple_provenance_records_for_same_assertion(self):
        from scripts.check_evidence_provenance_ext15 import evaluate
        record = {
            "id": "test:bp-multi-prov",
            "type": "Process",
            "provenance": [
                {"id": "prov-1",
                 "source": {"title": "x", "source_class": "authoritative_document"},
                 "assertions_supported": ["KYC required"],
                 "review_status": "verified"},
                {"id": "prov-2",
                 "source": {"title": "y", "source_class": "owner_confirmation"},
                 "assertions_supported": ["KYC required"],
                 "review_status": "verified"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        # EV-009 is the "this is allowed" rule; no finding should be raised.
        self.assertEqual(findings, [], f"EV-009 should not produce findings: {findings}")

    # Live integration
    def test_live_catalogue_validator_returns_zero_findings(self):
        r = subprocess.run(
            ["python3", "scripts/check_evidence_provenance_ext15.py", "--json"],
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
        for vocab in ("source_classes", "confidentiality_classes",
                      "confidence_levels", "verification_statuses",
                      "uncertainty_states"):
            with self.subTest(vocab=vocab):
                self.assertIn(vocab, manifest["controlled_vocabularies"])
                self.assertGreater(len(manifest["controlled_vocabularies"][vocab]), 0)

    # Template integrity
    def test_l2_template_documents_ext15_extensions(self):
        text = L2_TEMPLATE.read_text(encoding="utf-8")
        for marker in (
            "provenance:",
            "EXT-15",
            "ai_assisted_research",
            "uncertainty_state",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text,
                              f"L2 template should document {marker!r}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
