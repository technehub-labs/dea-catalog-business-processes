#!/usr/bin/env python3
"""
tests/test_programme_closure_ext24.py
======================================

Unit + integration tests for the EXT-24 programme closure validator
(scripts/check_programme_closure_ext24.py) and the 8 controlled closure
artefacts under reconciliation/closure/.

Test layout:
  - test_self_test_passes
  - test_closure_matrix_exists_and_complete: REQ-24-01..05
  - test_every_cr_has_closure_status: REQ-24-01
  - test_catalogue_baseline_exists_and_complete: REQ-24-06..08
  - test_baseline_entity_population_matches_repo: REQ-24-06
  - test_baseline_records_known_limitations: REQ-24-07
  - test_residual_gap_register_exists_and_complete: REQ-24-04
  - test_governance_roles_register_exists: REQ-24-09
  - test_every_role_has_required_fields: REQ-24-09
  - test_ownership_register_covers_l2_business_processes: REQ-24-10
  - test_every_l2_disposition_has_required_fields: REQ-24-10
  - test_lifecycle_register_exists: REQ-24-13
  - test_every_lifecycle_record_has_controlled_state: REQ-24-13
  - test_exception_register_exists: REQ-24-21
  - test_every_exception_has_required_fields: REQ-24-21
  - test_deferral_register_exists: REQ-24-22
  - test_every_deferral_has_required_fields: REQ-24-22
  - test_improvement_backlog_exists: REQ-24-39..40
  - test_every_improvement_has_controlled_category: REQ-24-40
  - test_every_improvement_has_required_fields: REQ-24-39
  - test_validator_runs_clean
  - test_baseline_distinguishes_verified_from_gaps: REQ-24-07
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLOSURE = REPO_ROOT / "reconciliation" / "closure"
MATRIX = CLOSURE / "programme-closure-matrix.json"
BASELINE = CLOSURE / "catalogue-baseline.json"
RESIDUAL_GAPS = CLOSURE / "residual-gap-register.json"
ROLES = CLOSURE / "governance-roles.json"
OWNERSHIP = CLOSURE / "ownership-register.json"
LIFECYCLE = CLOSURE / "lifecycle-register.json"
EXCEPTIONS = CLOSURE / "exception-register.json"
DEFERRALS = CLOSURE / "deferred-work-register.json"
IMPROVEMENTS = CLOSURE / "improvement-backlog.json"
MANIFEST = CLOSURE / "ext24-manifest.json"


class TestProgrammeClosureEXT24(unittest.TestCase):
    """CR-BP-94-EXT-24 programme closure tests."""

    def _load(self, path: Path) -> dict:
        with path.open() as fp:
            return json.load(fp)

    def test_self_test_passes(self):
        r = subprocess.run(
            ["python3", "scripts/check_programme_closure_ext24.py",
             "--self-test", "--json"],
            capture_output=True, text=True, timeout=30, cwd=str(REPO_ROOT),
        )
        self.assertEqual(r.returncode, 0, f"self-test failed: {r.stderr}")
        data = json.loads(r.stdout)
        self.assertEqual(data["mode"], "self-test")

    # ---- REQ-24-01..05: the closure matrix ----

    def test_closure_matrix_exists_and_complete(self):
        self.assertTrue(MATRIX.exists(), f"matrix missing: {MATRIX}")
        m = self._load(MATRIX)
        for key in ("matrix_schema_version", "parent_cr", "scope", "crs"):
            with self.subTest(key=key):
                self.assertIn(key, m, f"matrix key missing: {key}")
        # The full 17-CR programme is represented
        cr_ids = {c["cr_id"] for c in m["crs"]}
        for cid in ("CR-BP-94-EXT-08", "CR-BP-94-EXT-19", "CR-BP-94-EXT-22",
                    "CR-BP-EXT-23", "CR-BP-94-EXT-24"):
            with self.subTest(cr=cid):
                self.assertIn(cid, cr_ids)

    def test_every_cr_has_closure_status(self):
        valid = {"completed", "completed_with_approved_exceptions",
                 "partially_completed", "deferred", "blocked",
                 "not_started", "not_applicable"}
        m = self._load(MATRIX)
        for cr in m["crs"]:
            with self.subTest(cr=cr["cr_id"]):
                self.assertIn(cr["closure_status"], valid)
                self.assertTrue(cr["closure_recommendation"].strip())

    # ---- REQ-24-06..08: the catalogue baseline ----

    def test_catalogue_baseline_exists_and_complete(self):
        self.assertTrue(BASELINE.exists(), f"baseline missing: {BASELINE}")
        b = self._load(BASELINE)
        for key in ("baseline_revision", "baseline_date",
                    "entity_population", "schema_versions",
                    "profile_versions", "vocabulary_versions",
                    "validation_rule_versions", "reconciliation_status",
                    "evidence_status", "exception_status",
                    "deferred_work", "known_limitations"):
            with self.subTest(key=key):
                self.assertIn(key, b, f"baseline key missing: {key}")

    def test_baseline_entity_population_matches_repo(self):
        """The baseline numbers must agree with the live catalogue."""
        import glob, re, collections
        files = glob.glob(str(REPO_ROOT / "entities/v1-alpha/**/*.yaml"),
                          recursive=True)
        types = collections.Counter()
        l0 = 0
        for fp in files:
            if "/discovery/" in fp or "/templates/" in fp:
                continue
            if fp.endswith(("_template.yaml", "README.yaml", "README.md")):
                continue
            with open(fp, encoding="utf-8") as f:
                text = f.read()
            m = re.search(r"^type:\s*([^\n]+)", text, re.M)
            if m:
                types[m.group(1).strip()] += 1
            else:
                id_m = re.search(r"^id:\s*([^\n]+)", text, re.M)
                if id_m and "pc-" in id_m.group(1)[:20]:
                    l0 += 1

        b = self._load(BASELINE)
        self.assertEqual(b["entity_population"]["L0_ProcessContext"], l0)
        self.assertEqual(b["entity_population"]["L1_ProcessGroup"],
                         types.get("ProcessGroup", 0))
        self.assertEqual(b["entity_population"]["L2_BusinessProcess"],
                         types.get("Process", 0))
        self.assertEqual(b["entity_population"]["L3_Activity"],
                         types.get("Activity", 0))
        self.assertEqual(b["entity_population"]["L4_Task"],
                         types.get("Task", 0))

    def test_baseline_records_known_limitations(self):
        b = self._load(BASELINE)
        self.assertGreater(len(b["known_limitations"]), 0,
                           "baseline must record known limitations")
        # The baseline must NOT pretend that documented practice equals
        # actual organisational practice (section 19 of the CR).
        self.assertTrue(any("semantic" in k.lower() or "evidence" in k.lower()
                            for k in b["known_limitations"]))

    def test_baseline_distinguishes_verified_from_gaps(self):
        """REQ-24-07: the baseline distinguishes verified / accepted / deferred."""
        b = self._load(BASELINE)
        self.assertIn("integrity_notes", b)
        self.assertIn("NOT considered fully verified", b["integrity_notes"])

    # ---- REQ-24-04: residual gap register ----

    def test_residual_gap_register_exists_and_complete(self):
        self.assertTrue(RESIDUAL_GAPS.exists(), f"residual gaps missing")
        rg = self._load(RESIDUAL_GAPS)
        self.assertGreater(len(rg["gaps"]), 0, "no residual gaps recorded")
        for gap in rg["gaps"]:
            with self.subTest(gap=gap.get("gap_id")):
                for field in ("gap_id", "description", "affected_requirement",
                                "affected_entity", "impact", "severity",
                                "owner", "proposed_action", "target_date",
                                "disposition"):
                    self.assertTrue(gap.get(field),
                                    f"gap {gap.get('gap_id')!r} missing field {field!r}")

    # ---- REQ-24-09: governance roles ----

    def test_governance_roles_register_exists(self):
        self.assertTrue(ROLES.exists(), f"roles missing")
        r = self._load(ROLES)
        self.assertGreaterEqual(len(r["roles"]), 9,
                                "the 9 proposed governance roles must be present")

    def test_every_role_has_required_fields(self):
        r = self._load(ROLES)
        for role in r["roles"]:
            with self.subTest(role=role.get("role_id")):
                for field in ("role_id", "role_name", "primary_responsibility",
                                "mapped_to", "scope"):
                    self.assertTrue(role.get(field),
                                    f"role {role.get('role_id')!r} missing {field!r}")

    # ---- REQ-24-10: ownership register ----

    def test_ownership_register_covers_l2_business_processes(self):
        self.assertTrue(OWNERSHIP.exists())
        o = self._load(OWNERSHIP)
        self.assertGreater(len(o["dispositions"]), 0)
        # Every L2 BP in the live catalogue has an explicit disposition.
        import glob, re
        live_l2 = 0
        for fp in glob.glob(str(REPO_ROOT / "entities/v1-alpha/**/*.yaml"),
                             recursive=True):
            if "/discovery/" in fp or "/templates/" in fp:
                continue
            if fp.endswith(("_template.yaml", "README.yaml", "README.md")):
                continue
            with open(fp, encoding="utf-8") as f:
                text = f.read()
            if re.search(r"^type:\s*Process\b", text, re.M):
                live_l2 += 1
        self.assertEqual(len(o["dispositions"]), live_l2,
                         f"ownership dispositions {len(o['dispositions'])} must match "
                         f"live L2 BP count {live_l2}")

    def test_every_l2_disposition_has_required_fields(self):
        o = self._load(OWNERSHIP)
        for d in o["dispositions"]:
            with self.subTest(bp=d.get("bp_id")):
                for field in ("bp_id", "bp_name", "owner", "owner_status",
                                "review_due"):
                    self.assertTrue(d.get(field),
                                    f"L2 disposition {d.get('bp_id')!r} missing {field!r}")

    # ---- REQ-24-13: lifecycle register ----

    def test_lifecycle_register_exists(self):
        self.assertTrue(LIFECYCLE.exists())
        l = self._load(LIFECYCLE)
        self.assertGreater(len(l["records"]), 0)

    def test_every_lifecycle_record_has_controlled_state(self):
        valid = {"proposed", "under_review", "approved", "active",
                 "superseded", "deprecated", "retired"}
        l = self._load(LIFECYCLE)
        for rec in l["records"]:
            with self.subTest(record=rec.get("record_id")):
                self.assertIn(rec["lifecycle_state"], valid)

    # ---- REQ-24-21: exception register ----

    def test_exception_register_exists(self):
        self.assertTrue(EXCEPTIONS.exists())
        e = self._load(EXCEPTIONS)
        self.assertEqual(e["exceptions"], [],
                         "no approved exceptions exist at programme closure; "
                         "the EXT-23 deferred gates are ADVISORY, not approved exceptions")

    def test_every_exception_has_required_fields(self):
        valid = {"technical", "semantic", "evidence", "governance", "migration"}
        e = self._load(EXCEPTIONS)
        for exc in e["exceptions"]:
            with self.subTest(exception=exc.get("exception_id")):
                self.assertIn(exc["category"], valid)
                for field in ("rule_id", "scope", "rationale", "owner",
                                "approving_authority", "review_date"):
                    self.assertTrue(exc.get(field))

    # ---- REQ-24-22: deferred-work register ----

    def test_deferral_register_exists(self):
        self.assertTrue(DEFERRALS.exists())
        d = self._load(DEFERRALS)
        self.assertGreater(len(d["deferrals"]), 0)

    def test_every_deferral_has_required_fields(self):
        d = self._load(DEFERRALS)
        for dfr in d["deferrals"]:
            with self.subTest(deferral=dfr.get("deferral_id")):
                for field in ("requirement_id", "scope", "reason", "impact",
                                "owner", "approved_by", "review_date", "status"):
                    self.assertTrue(dfr.get(field),
                                    f"deferral {dfr.get('deferral_id')!r} missing {field!r}")

    # ---- REQ-24-39/40: improvement backlog ----

    def test_improvement_backlog_exists(self):
        self.assertTrue(IMPROVEMENTS.exists())
        i = self._load(IMPROVEMENTS)
        self.assertGreater(len(i["items"]), 0)

    def test_every_improvement_has_controlled_category(self):
        valid = {"defect_correction", "completeness_improvement",
                 "semantic_improvement", "structural_improvement",
                 "metamodel_alignment", "automation_improvement",
                 "governance_improvement", "integration_improvement", "innovation"}
        i = self._load(IMPROVEMENTS)
        for item in i["items"]:
            with self.subTest(item=item.get("item_id")):
                self.assertIn(item["category"], valid)

    def test_every_improvement_has_required_fields(self):
        i = self._load(IMPROVEMENTS)
        for item in i["items"]:
            with self.subTest(item=item.get("item_id")):
                for field in ("item_id", "description", "origin", "impact",
                                "priority", "dependencies", "owner",
                                "proposed_action", "status", "target_review_date"):
                    self.assertTrue(item.get(field),
                                    f"item {item.get('item_id')!r} missing {field!r}")

    # ---- Integration ----

    def test_validator_runs_clean(self):
        r = subprocess.run(
            ["python3", "scripts/check_programme_closure_ext24.py"],
            capture_output=True, text=True, timeout=60, cwd=str(REPO_ROOT),
        )
        # The framework's own findings must be zero at programme closure.
        self.assertIn("PASSED", r.stdout,
                      f"validator did not PASS: {r.stdout}\n{r.stderr}")


if __name__ == "__main__":
    unittest.main(verbosity=2)