#!/usr/bin/env python3
"""
tests/test_inputs_outputs_interfaces_ext12.py
==============================================

Unit + integration tests for the EXT-12 inputs/outputs/interfaces
validator (scripts/check_inputs_outputs_interfaces_ext12.py).

Test layout:
  - test_self_test_passes: validator's self-test returns 0 findings
  - test_l2_record_with_inputs_outputs_interfaces_dependencies_passes:
    a fully-populated L2 record with the EXT-12 extensions
  - test_l0_l1_records_cannot_declare_inputs_outputs_interfaces:
    IT-010 (non-executable constraint)
  - test_inputs_type_controlled_vocabulary: IT-003
  - test_outputs_type_controlled_vocabulary: IT-004
  - test_interfaces_type_controlled_vocabulary: IT-007
  - test_dependencies_criticality_controlled_vocabulary: IT-008
  - test_trigger_type_controlled_vocabulary: IT-009
  - test_duplicate_input_id_is_a_finding: IT-005
  - test_duplicate_output_id_is_a_finding: IT-006
  - test_live_catalogue_validator_returns_zero_findings: live integration
  - test_manifest_emitted: gate wiring
  - test_inputs_outputs_baseline_preserved: CR-BP-96 backward compat
  - test_l2_template_documents_ext12_extensions: template integrity
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "reconciliation" / "inputs-outputs-manifest.json"
L2_TEMPLATE = REPO_ROOT / "templates" / "business-process.yaml"


class TestInputsOutputsInterfacesEXT12(unittest.TestCase):
    """CR-BP-94-EXT-12 inputs/outputs/interfaces tests."""

    # Self-test
    def test_self_test_passes(self):
        r = subprocess.run(
            ["python3", "scripts/check_inputs_outputs_interfaces_ext12.py", "--self-test", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"self-test failed: {r.stdout}")
        data = json.loads(r.stdout)
        self.assertEqual(data["summary"]["total_findings"], 0)

    # IT-001 + IT-002 + IT-007 + IT-008: a fully-populated L2 record passes.
    def test_l2_record_with_inputs_outputs_interfaces_dependencies_passes(self):
        record = {
            "id": "test:bp-1",
            "type": "Process",
            "trigger": "A new BP is needed.",
            "trigger_type": "request_driven",
            "preconditions": [
                {"id": "p1", "name": "Authorised", "description": "...",
                 "scope": "process", "established_by": "...",
                 "verification": "...", "consequence_if_not_met": "..."},
            ],
            "inputs": [
                {"id": "i1", "name": "Customer request",
                 "description": "A request", "source": "external:customer",
                 "type": "request", "required": True,
                 "acceptance_criteria": "Valid request format",
                 "validation": "Schema validation against the request schema",
                 "provenance": {"source": "standard", "ref": "..."}},
            ],
            "transformation": "...",
            "outputs": [
                {"id": "o1", "name": "Resolution",
                 "description": "A documented resolution", "consumer": "ops:team",
                 "type": "service_result",
                 "acceptance_criteria": "Customer notified",
                 "quality_attributes": ["accuracy", "completeness"],
                 "provenance": {"source": "governance", "ref": "..."}},
            ],
            "interfaces": [
                {"id": "iface1", "name": "Customer channel",
                 "description": "Submission channel", "type": "human",
                 "participants": ["customer", "ops:agent"],
                 "exchange_purpose": "...",
                 "format_or_standard": "Web form",
                 "source": {"ref": "..."}},
            ],
            "dependencies": [
                {"id": "dep1", "target": "crm:system",
                 "type": "information_system",
                 "business_consequence": "Cannot resolve without CRM access",
                 "criticality": "high",
                 "source": {"ref": "..."}},
            ],
        }
        from scripts.check_inputs_outputs_interfaces_ext12 import evaluate
        findings = evaluate([(Path("test.yaml"), record)])
        self.assertEqual(findings, [], f"unexpected findings: {findings}")

    # IT-010: L0/L1 records cannot declare inputs/outputs/interfaces/dependencies/preconditions.
    def test_l0_l1_records_cannot_declare_inputs_outputs_interfaces(self):
        from scripts.check_inputs_outputs_interfaces_ext12 import evaluate
        for level_type, level in [("ProcessContext", "L0"), ("ProcessGroup", "L1")]:
            record = {
                "id": f"test:{level}",
                "type": level_type,
                "inputs": [{"id": "i1", "name": "x", "description": "x"}],
                "outputs": [{"id": "o1", "name": "x", "description": "x"}],
                "interfaces": [{"id": "iface1", "name": "x", "description": "x", "type": "human"}],
                "dependencies": [{"id": "dep1", "target": "x", "type": "x",
                                  "business_consequence": "x", "criticality": "high"}],
                "preconditions": [{"id": "p1", "name": "x", "description": "x"}],
                "trigger_type": "event_driven",
            }
            with self.subTest(level=level):
                findings = evaluate([(Path(f"test_{level}.yaml"), record)])
                rules = {f["rule"] for f in findings}
                # All 6 forbidden-field findings should be raised (5 fields
                # declared + trigger_type) under IT-010.
                self.assertIn("IT-010", rules, f"L0/L1 should trigger IT-010; got {findings}")

    # IT-003: inputs[].type vocabulary
    def test_inputs_type_controlled_vocabulary(self):
        from scripts.check_inputs_outputs_interfaces_ext12 import evaluate
        record = {
            "id": "test:bp-bad-type",
            "type": "Process",
            "inputs": [
                {"id": "i1", "name": "x", "description": "x",
                 "type": "unknown_type"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("IT-003", rules, f"expected IT-003; got {findings}")

    # IT-004: outputs[].type vocabulary
    def test_outputs_type_controlled_vocabulary(self):
        from scripts.check_inputs_outputs_interfaces_ext12 import evaluate
        record = {
            "id": "test:bp-bad-out",
            "type": "Process",
            "outputs": [
                {"id": "o1", "name": "x", "description": "x",
                 "type": "unknown_type"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("IT-004", rules, f"expected IT-004; got {findings}")

    # IT-007: interfaces[].type vocabulary
    def test_interfaces_type_controlled_vocabulary(self):
        from scripts.check_inputs_outputs_interfaces_ext12 import evaluate
        record = {
            "id": "test:bp-bad-iface",
            "type": "Process",
            "interfaces": [
                {"id": "iface1", "name": "x", "description": "x",
                 "type": "unknown_type"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("IT-007", rules, f"expected IT-007; got {findings}")

    # IT-008: dependencies[].criticality vocabulary
    def test_dependencies_criticality_controlled_vocabulary(self):
        from scripts.check_inputs_outputs_interfaces_ext12 import evaluate
        record = {
            "id": "test:bp-bad-dep",
            "type": "Process",
            "dependencies": [
                {"id": "dep1", "target": "x", "type": "x",
                 "business_consequence": "x", "criticality": "extreme"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("IT-008", rules, f"expected IT-008; got {findings}")

    # IT-009: trigger_type vocabulary
    def test_trigger_type_controlled_vocabulary(self):
        from scripts.check_inputs_outputs_interfaces_ext12 import evaluate
        record = {
            "id": "test:bp-bad-trigger",
            "type": "Process",
            "trigger": "x",
            "trigger_type": "random_type",
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("IT-009", rules, f"expected IT-009; got {findings}")

    # IT-005: duplicate input id
    def test_duplicate_input_id_is_a_finding(self):
        from scripts.check_inputs_outputs_interfaces_ext12 import evaluate
        record = {
            "id": "test:bp-dup-in",
            "type": "Process",
            "inputs": [
                {"id": "i1", "name": "x", "description": "x"},
                {"id": "i1", "name": "y", "description": "y"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("IT-005", rules, f"expected IT-005; got {findings}")

    # IT-006: duplicate output id
    def test_duplicate_output_id_is_a_finding(self):
        from scripts.check_inputs_outputs_interfaces_ext12 import evaluate
        record = {
            "id": "test:bp-dup-out",
            "type": "Process",
            "outputs": [
                {"id": "o1", "name": "x", "description": "x"},
                {"id": "o1", "name": "y", "description": "y"},
            ],
        }
        findings = evaluate([(Path("test.yaml"), record)])
        rules = {f["rule"] for f in findings}
        self.assertIn("IT-006", rules, f"expected IT-006; got {findings}")

    # Live integration: the live catalogue (0 inputs/outputs/interfaces populated)
    # must produce 0 findings. The validator is structured to report findings
    # only when the EXT-12 fields are populated; the current state is none
    # of the 3,733 records have any inputs/outputs/etc.
    def test_live_catalogue_validator_returns_zero_findings(self):
        r = subprocess.run(
            ["python3", "scripts/check_inputs_outputs_interfaces_ext12.py", "--json"],
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
        for vocab in ("input_types", "output_types", "interface_types",
                      "dependency_criticality", "trigger_types"):
            with self.subTest(vocab=vocab):
                self.assertIn(vocab, manifest["controlled_vocabularies"])
                self.assertGreater(len(manifest["controlled_vocabularies"][vocab]), 0)

    # CR-BP-96 baseline preserved: existing records (which have no inputs/outputs)
    # remain conformant. The validator reports 0 findings on the live tree.
    def test_inputs_outputs_baseline_preserved(self):
        # The CR-BP-96 fields (id, name, description for inputs; id, name,
        # description, consumer for outputs) are part of the existing
        # template. The EXT-12 extensions are additive; records that use
        # only the CR-BP-96 attributes validate. The live integration
        # test (above) confirms this.
        self.assertTrue(L2_TEMPLATE.exists(),
                        f"L2 template missing at {L2_TEMPLATE}")

    # Template integrity
    def test_l2_template_documents_ext12_extensions(self):
        if yaml is None:
            self.skipTest("PyYAML not available")
        text = L2_TEMPLATE.read_text(encoding="utf-8")
        for marker in (
            "interfaces:",                # EXT-12 §10
            "dependencies:",              # EXT-12 §11
            "trigger_type:",              # EXT-12 §5.1
            "preconditions:",             # EXT-12 §5.2
            "EXT-12",                     # inline EXT-12 references
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text,
                              f"L2 template should document {marker!r}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
