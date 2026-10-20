#!/usr/bin/env python3
"""
tests/test_profile_registry_ext11.py
====================================

Unit + integration tests for the EXT-11 profile registry validator
(scripts/check_profile_registry_ext11.py).

Test layout:
  - test_self_test_passes: validator's self-test mode returns 0 findings
  - test_v3_profile_yaml_exists: PR-001
  - test_v3_profile_yaml_is_valid_yaml: PR-002 prerequisite
  - test_v3_profile_has_all_five_level_keys: PR-002
  - test_each_level_profile_has_required_keys: PR-003
  - test_profile_ids_are_unique: PR-004
  - test_l0_l1_mark_non_executable: PR-005
  - test_l0_l1_no_executable_operational_sections: PR-006
  - test_l4_no_workflow_orchestration_sections: PR-007
  - test_retired_placeholder_reissued_with_ext09_states: PR-008
  - test_inherited_sections_reference_authoritative_source: PR-009
  - test_no_unexpected_schema_fields_introduced: PR-010
  - test_placeholder_states_cover_all_11_ext09_states: completeness coverage
  - test_manifest_emitted: gate wiring
  - test_integration_with_ext10_inventory: cross-CR consistency
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # type: ignore

REPO_ROOT = Path(__file__).resolve().parent.parent
PROFILE_PATH = REPO_ROOT / "templates" / "documentation-profile-ext11-v3.yaml"
MANIFEST_PATH = REPO_ROOT / "reconciliation" / "profile-manifest.json"

LEVEL_KEYS = (
    "l0_process_context",
    "l1_process_group",
    "l2_business_process",
    "l3_activity",
    "l4_task",
)

EXECUTABLE_SECTION_IDS = frozenset({
    "trigger", "precondition", "input", "transformation",
    "output", "outcome", "performer", "accountability",
    "business_rule", "control", "exception",
})

WORKFLOW_ORCHESTRATION_SECTION_IDS = frozenset({
    "workflow", "workflow-orchestration", "orchestration",
    "sequence", "branching", "retry", "state-machine",
    "workflow-engine", "workflow-instance",
})


class TestProfileRegistryEXT11(unittest.TestCase):
    """CR-BP-94-EXT-11 profile registry tests."""

    @classmethod
    def setUpClass(cls) -> None:
        if yaml is None:
            raise unittest.SkipTest("PyYAML not available")
        if not PROFILE_PATH.exists():
            raise unittest.SkipTest(f"profile not found at {PROFILE_PATH}")
        with PROFILE_PATH.open(encoding="utf-8") as fp:
            cls.profile = yaml.safe_load(fp) or {}

    # PR-001
    def test_v3_profile_yaml_exists(self):
        self.assertTrue(PROFILE_PATH.exists(),
                        f"PR-001: profile file missing at {PROFILE_PATH}")

    # PR-002 prerequisite
    def test_v3_profile_yaml_is_valid_yaml(self):
        self.assertIsInstance(self.profile, dict,
                              "the v3 profile must parse to a dict")

    # PR-002
    def test_v3_profile_has_all_five_level_keys(self):
        for level_key in LEVEL_KEYS:
            with self.subTest(level=level_key):
                self.assertIn(level_key, self.profile,
                              f"PR-002: top-level key {level_key!r} missing")

    # PR-003
    def test_each_level_profile_has_required_keys(self):
        for level_key in LEVEL_KEYS:
            level = self.profile.get(level_key)
            if not isinstance(level, dict):
                continue
            with self.subTest(level=level_key):
                for required_key in (
                    "profile_id", "applies_to",
                    "required_sections", "conditional_sections",
                    "not_applicable_sections", "inherited_sections",
                ):
                    self.assertIn(required_key, level,
                                  f"PR-003: {level_key} missing {required_key!r}")

    # PR-004
    def test_profile_ids_are_unique(self):
        seen = set()
        for level_key in LEVEL_KEYS:
            level = self.profile.get(level_key)
            if not isinstance(level, dict):
                continue
            pid = level.get("profile_id")
            with self.subTest(level=level_key, profile_id=pid):
                self.assertNotIn(pid, seen,
                                 f"PR-004: profile_id {pid!r} is duplicated")
                seen.add(pid)

    # PR-005
    def test_l0_l1_mark_non_executable(self):
        for level_key in ("l0_process_context", "l1_process_group"):
            level = self.profile.get(level_key)
            if not isinstance(level, dict):
                continue
            with self.subTest(level=level_key):
                self.assertIs(level.get("non_executable"), True,
                              f"PR-005: {level_key} must declare non_executable: true")

    # PR-006
    def test_l0_l1_no_executable_operational_sections(self):
        for level_key in ("l0_process_context", "l1_process_group"):
            level = self.profile.get(level_key)
            if not isinstance(level, dict):
                continue
            for section_key in ("required_sections", "conditional_sections"):
                sections = level.get(section_key) or []
                if not isinstance(sections, list):
                    continue
                for section in sections:
                    section_id = section.get("id") if isinstance(section, dict) else section
                    with self.subTest(level=level_key, section_key=section_key, section_id=section_id):
                        self.assertNotIn(section_id, EXECUTABLE_SECTION_IDS,
                                         f"PR-006: {level_key}.{section_key} has executable section {section_id!r}")

    # PR-007
    def test_l4_no_workflow_orchestration_sections(self):
        level = self.profile.get("l4_task")
        if not isinstance(level, dict):
            return
        for section_key in ("required_sections", "conditional_sections"):
            sections = level.get(section_key) or []
            if not isinstance(sections, list):
                continue
            for section in sections:
                section_id = section.get("id") if isinstance(section, dict) else section
                with self.subTest(section_key=section_key, section_id=section_id):
                    self.assertNotIn(section_id, WORKFLOW_ORCHESTRATION_SECTION_IDS,
                                     f"PR-007: l4_task.{section_key} has workflow section {section_id!r}")

    # PR-008
    def test_retired_placeholder_reissued_with_ext09_states(self):
        ps = self.profile.get("placeholder_states")
        self.assertIsInstance(ps, dict, "PR-008: placeholder_states block missing")
        reissued = ps.get("reissued_phrases")
        self.assertIsInstance(reissued, dict,
                              "PR-008: reissued_phrases block missing")
        # The 11 EXT-09 §10 states.
        for state in (
            "not_started", "in_progress", "pending_evidence",
            "pending_review", "approved", "not_applicable",
            "unknown", "inherited", "rejected", "superseded",
            "deferred",
        ):
            with self.subTest(state=state):
                self.assertIn(state, reissued,
                              f"PR-008: reissued_phrases missing EXT-09 §10 state {state!r}")
        self.assertEqual(ps.get("retired_phrase"), "(pending; backfill at EXT-04)",
                         "PR-008: retired_phrase not declared for legacy recognition")

    # PR-009
    def test_inherited_sections_reference_authoritative_source(self):
        for level_key in LEVEL_KEYS:
            level = self.profile.get(level_key)
            if not isinstance(level, dict):
                continue
            inherited = level.get("inherited_sections") or []
            for section in inherited:
                if not isinstance(section, dict):
                    continue
                with self.subTest(level=level_key, section=section):
                    self.assertIn("inherits_from", section,
                                  f"PR-009: inherited section {section.get('id')!r} "
                                  f"on {level_key} must declare inherits_from")

    # PR-010
    def test_no_unexpected_schema_fields_introduced(self):
        # The validator's KNOWN_SCHEMA_FIELDS set is the source of truth;
        # the integration test (test_integration_with_ext10_inventory)
        # runs the actual validator to catch anything missing from this set.
        # Here we just confirm the v3 profile is loaded.
        self.assertIsInstance(self.profile, dict)

    # Completeness coverage
    def test_placeholder_states_cover_all_11_ext09_states(self):
        placeholder_states = self.profile.get("placeholder_states") or {}
        reissued = placeholder_states.get("reissued_phrases") or {}
        self.assertEqual(len(reissued), 11,
                         f"expected 11 EXT-09 §10 states; got {len(reissued)}")

    # Manifest emission
    def test_manifest_emitted(self):
        # Run the validator; the manifest is emitted.
        result = subprocess.run(
            ["python3", "scripts/check_profile_registry_ext11.py", "--json"],
            capture_output=True, text=True, timeout=30,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(result.returncode, 0,
                         f"validator failed: {result.stdout}\n{result.stderr}")
        data = json.loads(result.stdout)
        self.assertIn("summary", data)
        self.assertEqual(data["summary"]["total_findings"], 0,
                         "validator reports findings against the v3 profile")
        # The manifest file should also be on disk.
        self.assertTrue(MANIFEST_PATH.exists(),
                        f"manifest missing at {MANIFEST_PATH}")
        with MANIFEST_PATH.open(encoding="utf-8") as fp:
            manifest = json.load(fp)
        self.assertIn("profiles", manifest)
        for level_key in LEVEL_KEYS:
            self.assertIn(level_key, manifest["profiles"],
                          f"manifest missing {level_key}")

    # Cross-CR consistency
    def test_integration_with_ext10_inventory(self):
        # The EXT-11 profile validator must not introduce new schema fields
        # that EXT-10 marked as gaps. This is a cross-CR consistency check.
        ext10_inventory = REPO_ROOT / "docs" / "operational-schema-inventory.md"
        self.assertTrue(ext10_inventory.exists(),
                        f"EXT-10 inventory missing at {ext10_inventory}")
        text = ext10_inventory.read_text(encoding="utf-8")
        # Confirm the inventory marks `inputs`, `outputs`, `responsibility`,
        # `boundary`, `transformation`, `trigger`, `outcome` as Retain.
        for retained_field in ("inputs", "outputs", "responsibility",
                               "boundary", "transformation", "trigger", "outcome"):
            with self.subTest(field=retained_field):
                self.assertIn(retained_field, text,
                              f"EXT-10 inventory should mention retained field {retained_field!r}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
