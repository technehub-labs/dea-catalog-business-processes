#!/usr/bin/env python3
"""
tests/test_authoring_methodology_ext16.py
=========================================

Unit + integration tests for the EXT-16 authoring methodology
validator (scripts/check_authoring_methodology_ext16.py).

Test layout:
  - test_self_test_passes
  - test_l2_record_with_full_ext16_structure_passes
  - test_l0_l1_cannot_carry_metadata_authoring: AM-010
  - test_state_vocabulary: AM-003
  - test_methodology_version_required: AM-001 + AM-002
  - test_author_required_when_state_is_drafted_or_later: AM-004
  - test_reviewer_required_when_state_is_under_review_or_later: AM-005
  - test_ai_assistance_used_must_be_boolean: AM-006
  - test_ai_assistance_validation_vocabulary: AM-007
  - test_quality_dimensions_must_cover_8_dimensions: AM-008
  - test_quality_dimension_value_vocabulary: AM-008
  - test_source_priority_used_vocabulary: AM-009
  - test_live_catalogue_validator_returns_zero_findings: live integration
  - test_manifest_emitted: gate wiring
  - test_l2_template_documents_ext16_extensions: template integrity
  - test_ai_assistance_used_false_does_not_require_validation: AM-007
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "reconciliation" / "authoring-manifest.json"
L2_TEMPLATE = REPO_ROOT / "templates" / "business-process.yaml"


def _make_full_authoring():
    """Return a complete metadata.authoring block that passes all rules."""
    return {
        "methodology_version": "1.0.0",
        "state": "published",
        "research_plan": {
            "scope": "KYC process enrichment",
            "sources_consulted": ["KYC Policy v3.2"],
            "gaps_identified": ["Refresh frequency"],
            "blockers": [],
        },
        "author": "KYC Analyst",
        "author_date": "2026-10-15",
        "reviewer": "Compliance Officer",
        "review_date": "2026-10-17",
        "review_outcome": "approved",
        "ai_assistance": {
            "used": True,
            "tool": "extraction",
            "role": "gap_analysis",
            "validation": "independently_validated",
        },
        "evidence_inheritance": {
            "from_parent": None,
            "inherited_fields": [],
        },
        "source_priority_used": "owner_confirmation",
        "quality_dimensions": {
            "semantic_correctness": "pass",
            "decomposition_appropriateness": "pass",
            "evidence_quality": "pass",
            "parent_child_consistency": "n_a",
            "cross_catalogue_validity": "pass",
            "profile_completeness": "pass",
            "publication_safety": "pass",
            "readme_consistency": "pass",
        },
    }


class TestAuthoringMethodologyEXT16(unittest.TestCase):
    """CR-BP-94-EXT-16 authoring methodology tests."""

    # Self-test
    def test_self_test_passes(self):
        r = subprocess.run(
            ["python3", "scripts/check_authoring_methodology_ext16.py", "--self-test", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"self-test failed: {r.stdout}")
        data = json.loads(r.stdout)
        self.assertEqual(data["summary"]["total_findings"], 0)

    # Full L2 record with all EXT-16 fields passes.
    def test_l2_record_with_full_ext16_structure_passes(self):
        record = {
            "id": "test:bp-1",
            "type": "Process",
            "metadata": {
                "established_by": "CR-BP-94-EXT-19",
                "established_at": "2026-10-19",
                "change_history": [
                    {"cr": "CR-BP-94-EXT-19", "date": "2026-10-19",
                     "change": "Initial enrichment"},
                ],
                "authoring": _make_full_authoring(),
            },
        }
        from scripts.check_authoring_methodology_ext16 import evaluate
        findings = evaluate([(Path("test.yaml"), record)])
        self.assertEqual(findings, [], f"unexpected findings: {findings}")

    # AM-010: L0/L1 cannot carry metadata.authoring.
    def test_l0_l1_cannot_carry_metadata_authoring(self):
        from scripts.check_authoring_methodology_ext16 import evaluate
        for level_type, level in [("ProcessContext", "L0"), ("ProcessGroup", "L1")]:
            record = {
                "id": f"test:{level}",
                "type": level_type,
                "metadata": {
                    "authoring": _make_full_authoring(),
                },
            }
            with self.subTest(level=level):
                findings = evaluate([(Path(f"test_{level}.yaml"), record)])
                rules = {f["rule"] for f in findings}
                self.assertIn("AM-010", rules,
                              f"L0/L1 should trigger AM-010; got {findings}")

    # AM-003: state vocabulary
    def test_state_vocabulary(self):
        from scripts.check_authoring_methodology_ext16 import evaluate
        record = {
            "id": "test:bp-bad-state",
            "type": "Process",
            "metadata": {"authoring": {**_make_full_authoring(),
                                        "state": "in_progress"}},
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("AM-003", rules, f"expected AM-003; got {findings}")

    # AM-001 + AM-002: methodology_version required
    def test_methodology_version_required(self):
        from scripts.check_authoring_methodology_ext16 import evaluate
        a = _make_full_authoring()
        del a["methodology_version"]
        record = {
            "id": "test:bp-no-mv",
            "type": "Process",
            "metadata": {"authoring": a},
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("AM-001", rules, f"expected AM-001; got {findings}")

    # AM-004: author required when state is drafted
    def test_author_required_when_state_is_drafted_or_later(self):
        from scripts.check_authoring_methodology_ext16 import evaluate
        a = _make_full_authoring()
        a["state"] = "drafted"
        del a["author"]
        record = {
            "id": "test:bp-no-author",
            "type": "Process",
            "metadata": {"authoring": a},
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("AM-004", rules, f"expected AM-004; got {findings}")

    # AM-005: reviewer required when state is under_review
    def test_reviewer_required_when_state_is_under_review_or_later(self):
        from scripts.check_authoring_methodology_ext16 import evaluate
        a = _make_full_authoring()
        a["state"] = "under_review"
        del a["reviewer"]
        record = {
            "id": "test:bp-no-reviewer",
            "type": "Process",
            "metadata": {"authoring": a},
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("AM-005", rules, f"expected AM-005; got {findings}")

    # AM-006: ai_assistance.used must be a boolean
    def test_ai_assistance_used_must_be_boolean(self):
        from scripts.check_authoring_methodology_ext16 import evaluate
        a = _make_full_authoring()
        a["ai_assistance"] = {"used": "yes", "validation": "independently_validated"}
        record = {
            "id": "test:bp-ai-not-bool",
            "type": "Process",
            "metadata": {"authoring": a},
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("AM-006", rules, f"expected AM-006; got {findings}")

    # AM-007: AI validation vocabulary
    def test_ai_assistance_validation_vocabulary(self):
        from scripts.check_authoring_methodology_ext16 import evaluate
        a = _make_full_authoring()
        a["ai_assistance"]["validation"] = "maybe"
        record = {
            "id": "test:bp-ai-bad-val",
            "type": "Process",
            "metadata": {"authoring": a},
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("AM-007", rules, f"expected AM-007; got {findings}")

    # AM-007: AI used=false does not require validation
    def test_ai_assistance_used_false_does_not_require_validation(self):
        from scripts.check_authoring_methodology_ext16 import evaluate
        a = _make_full_authoring()
        a["ai_assistance"] = {"used": False}
        record = {
            "id": "test:bp-ai-no",
            "type": "Process",
            "metadata": {"authoring": a},
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertNotIn("AM-007", rules, f"unexpected AM-007: {findings}")

    # AM-008: quality_dimensions must cover 8 dimensions
    def test_quality_dimensions_must_cover_8_dimensions(self):
        from scripts.check_authoring_methodology_ext16 import evaluate
        a = _make_full_authoring()
        del a["quality_dimensions"]["evidence_quality"]
        record = {
            "id": "test:bp-no-qd",
            "type": "Process",
            "metadata": {"authoring": a},
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("AM-008", rules, f"expected AM-008; got {findings}")

    # AM-008: quality dimension value vocabulary
    def test_quality_dimension_value_vocabulary(self):
        from scripts.check_authoring_methodology_ext16 import evaluate
        a = _make_full_authoring()
        a["quality_dimensions"]["semantic_correctness"] = "kinda"
        record = {
            "id": "test:bp-bad-qd",
            "type": "Process",
            "metadata": {"authoring": a},
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("AM-008", rules, f"expected AM-008; got {findings}")

    # AM-009: source_priority_used vocabulary
    def test_source_priority_used_vocabulary(self):
        from scripts.check_authoring_methodology_ext16 import evaluate
        a = _make_full_authoring()
        a["source_priority_used"] = "best_guess"
        record = {
            "id": "test:bp-bad-spu",
            "type": "Process",
            "metadata": {"authoring": a},
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("AM-009", rules, f"expected AM-009; got {findings}")

    # Live integration
    def test_live_catalogue_validator_returns_zero_findings(self):
        r = subprocess.run(
            ["python3", "scripts/check_authoring_methodology_ext16.py", "--json"],
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
        for vocab in ("authoring_states", "ai_validation_states",
                      "source_priority_values", "quality_dimensions",
                      "quality_values", "review_outcomes"):
            with self.subTest(vocab=vocab):
                self.assertIn(vocab, manifest["controlled_vocabularies"])
                self.assertGreater(len(manifest["controlled_vocabularies"][vocab]), 0)

    # Template integrity
    def test_l2_template_documents_ext16_extensions(self):
        text = L2_TEMPLATE.read_text(encoding="utf-8")
        for marker in (
            "metadata.authoring:",
            "EXT-16",
            "methodology_version",
            "ai_assistance",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text,
                              f"L2 template should document {marker!r}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
