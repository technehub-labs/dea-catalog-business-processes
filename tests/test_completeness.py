"""Tests for scripts/check_completeness.py (CR-BP-CE-0 gate [50]).

Run from inside tests/:  python3 -m unittest test_completeness
(tests/ has no __init__.py; see the repo test-running convention.)
"""
import subprocess, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import check_completeness as cc  # noqa: E402

PC_FULL = {"id": "processes:pc-x-y-aaaaaa", "domain": "D", "lifecycle_stage": "S",
           "name": "N", "definition": "d",
           "scope": {"includes": ["a", "b", "c"], "excludes": ["a", "b", "c"]},
           "outcomes": ["x", "y", "z"], "adjacent_contexts": ["p"], "processes": ["q"],
           "cell_charter": {k: "v" for k in
                            ["enterprise_concern", "lifecycle_concern", "combined_semantic_meaning",
                             "expected_outcomes", "inclusions", "exclusions", "adjacent_boundaries"]},
           "status": "active"}
P = lambda s: ROOT / "entities" / "v1-alpha" / s  # a path under ROOT so relative_to works


class TestLevelInference(unittest.TestCase):
    def test_type_field_wins(self):
        self.assertEqual(cc.level_of({"id": "x", "type": "Task"}), "Task")

    def test_pc_prefix(self):
        self.assertEqual(cc.level_of({"id": "processes:pc-a-b-c"}), "ProcessContext")

    def test_uninferable(self):
        self.assertIsNone(cc.level_of({"id": "processes:weird"}))


class TestDomainResolution(unittest.TestCase):
    """R7: the finding counter and the denominator must resolve the domain the
    same way, or the per-domain completeness figures count one population and
    divide by another."""

    def test_top_level_domain_wins(self):
        r = {"domain": "FinanceAndAccounting",
             "ecfConformance": {"canonicalReferences": [{"domain": "Other"}]}}
        self.assertEqual(cc.domain_of(r), "FinanceAndAccounting")

    def test_ecf_conformance_fallback(self):
        # Only ProcessContext carries a top-level `domain`; every other level
        # resolves through ecfConformance.canonicalReferences[0].domain.
        r = {"id": "processes:task-x", "type": "Task",
             "ecfConformance": {"canonicalReferences": [{"domain": "ProductAndValue"}]}}
        self.assertEqual(cc.domain_of(r), "ProductAndValue")

    def test_first_matching_reference_wins(self):
        r = {"ecfConformance": {"canonicalReferences": [
            {"domain": "First"}, {"domain": "Second"}]}}
        self.assertEqual(cc.domain_of(r), "First")

    def test_unresolvable_is_question_mark(self):
        self.assertEqual(cc.domain_of({"id": "x"}), "?")
        self.assertEqual(cc.domain_of({"ecfConformance": {}}), "?")
        self.assertEqual(cc.domain_of({"ecfConformance": {"canonicalReferences": []}}), "?")

    def test_non_dict_references_are_safe(self):
        r = {"ecfConformance": {"canonicalReferences": ["not-a-dict", {"domain": "Ok"}]}}
        self.assertEqual(cc.domain_of(r), "Ok")


class TestRuleLevelMapping(unittest.TestCase):
    """The rule code carries the level (CR-BP-CE-0 R1 mapping). Attributing the
    level from the rule code is what makes by_level.findings real; keying the
    counter on the level NAME while findings are keyed on the rule code yields
    a structurally-zero column."""

    def test_each_level_segment_maps_to_its_canonical_level(self):
        self.assertEqual(cc.level_of_rule("CE-L0-003"), "ProcessContext")
        self.assertEqual(cc.level_of_rule("CE-L1-005"), "ProcessGroup")
        self.assertEqual(cc.level_of_rule("CE-L2-006"), "Process")
        self.assertEqual(cc.level_of_rule("CE-L3-001"), "Activity")
        self.assertEqual(cc.level_of_rule("CE-L4-002"), "Task")

    def test_cross_level_rule_has_no_level(self):
        self.assertIsNone(cc.level_of_rule("CE-000"))

    def test_unknown_segment_has_no_level(self):
        self.assertIsNone(cc.level_of_rule("CE-L9-001"))


class TestReportAttribution(unittest.TestCase):
    """The CE-900 artifact must carry the per-domain completeness that the CR
    specifies, with one consistent domain resolution."""

    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable, str(ROOT / "scripts" / "check_completeness.py"),
                        "--advisory"], capture_output=True, text=True, cwd=str(ROOT))
        import yaml as _y
        cls.rep = _y.safe_load(
            (ROOT / "reconciliation" / "completeness-report.yaml").read_text(encoding="utf-8"))

    def test_by_domain_is_emitted_with_totals_and_pct(self):
        self.assertIn("by_domain", self.rep)
        self.assertTrue(self.rep["by_domain"])
        for dom, d in self.rep["by_domain"].items():
            self.assertIn("records", d, dom)
            self.assertIn("findings", d, dom)
            self.assertIn("completeness_pct", d, dom)
            self.assertGreater(d["records"], 0, dom)
            self.assertTrue(0.0 <= d["completeness_pct"] <= 100.0, dom)

    def test_no_unresolved_pseudo_domain(self):
        # The pseudo-domain '?' meant the per-domain signal was unusable.
        self.assertNotIn("?", self.rep["by_domain"])
        self.assertNotIn("?", self.rep["by_domain_findings"])

    def test_domain_totals_cover_every_record(self):
        self.assertEqual(sum(d["records"] for d in self.rep["by_domain"].values()),
                         self.rep["record_count"])

    def test_by_level_findings_sum_to_total_findings(self):
        # Guards the structurally-zero column: the per-level finding counts
        # must add up to the findings actually raised.
        self.assertEqual(sum(d["findings"] for d in self.rep["by_level"].values()),
                         self.rep["summary"]["total_findings"])

    def test_by_domain_findings_sum_to_total_findings(self):
        self.assertEqual(sum(self.rep["by_domain_findings"].values()),
                         self.rep["summary"]["total_findings"])

    def test_by_level_findings_are_not_structurally_zero(self):
        # At least one level must carry findings; a zero column everywhere
        # is the signature of the rule-code/level-name key mismatch.
        self.assertTrue(any(d["findings"] > 0 for d in self.rep["by_level"].values()),
                        self.rep["by_level"])

    def test_records_with_findings_never_exceeds_records(self):
        for section in ("by_level", "by_domain"):
            for k, d in self.rep[section].items():
                self.assertLessEqual(d["records_with_findings"], d["records"], f"{section}.{k}")

    def test_by_rule_is_emitted(self):
        self.assertIn("by_rule", self.rep)
        self.assertEqual(sum(self.rep["by_rule"].values()), self.rep["summary"]["total_findings"])


class TestProfiles(unittest.TestCase):
    def test_complete_pc_no_blocking(self):
        f = cc.check_record(P("p.yaml"), PC_FULL, {})
        self.assertFalse([x for x in f if x["severity"] == "blocking"], f)

    def test_empty_pc_flagged(self):
        f = cc.check_record(P("p.yaml"), {"id": "processes:pc-x-y-bbbbbb"}, {})
        self.assertTrue(any(x["rule"] == "CE-L0-001" for x in f))

    def test_pc_prohibited_type(self):
        bad = dict(PC_FULL); bad["type"] = "ProcessContext"
        f = cc.check_record(P("p.yaml"), bad, {})
        self.assertTrue(any(x["rule"] == "CE-L0-006" for x in f))

    def test_pc_short_scope_advisory(self):
        bad = dict(PC_FULL); bad["scope"] = {"includes": ["a"], "excludes": ["a", "b", "c"]}
        f = cc.check_record(P("p.yaml"), bad, {})
        self.assertTrue(any(x["rule"] == "CE-L0-002" and x["severity"] == "advisory" for x in f))

    def test_process_classification_advisory(self):
        p = {"id": "processes:process-x", "type": "Process", "name": "N",
             "version": "1.0.0", "process_intent": "manage"}
        f = cc.check_record(P("p.yaml"), p, {})
        self.assertTrue(any(x["rule"] == "CE-L2-002" for x in f))

    def test_process_capabilities_prohibited(self):
        p = {"id": "processes:process-x", "type": "Process", "name": "N", "version": "1.0.0",
             "process_intent": "manage", "capabilities_delivered": ["x"]}
        f = cc.check_record(P("p.yaml"), p, {})
        self.assertTrue(any(x["rule"] == "CE-L2-010" and x["severity"] == "blocking" for x in f))

    def test_task_bad_responsibility(self):
        t = {"id": "processes:task-x", "type": "Task", "name": "N", "definition": "d",
             "belongs_to_activity": "a", "trigger": "t", "outcome": "o", "version": "1",
             "lifecycle_status": "c", "status": "c", "ecfConformance": {},
             "responsibility": "bogus custodian"}
        f = cc.check_record(P("p.yaml"), t, {})
        self.assertTrue(any(x["rule"] == "CE-L4-002" for x in f))

    def test_task_good_responsibility(self):
        t = {"id": "processes:task-x", "type": "Task", "name": "N", "definition": "d",
             "belongs_to_activity": "a", "trigger": "t", "outcome": "o", "version": "1",
             "lifecycle_status": "c", "status": "c", "ecfConformance": {},
             "responsibility": "records custodian"}
        f = cc.check_record(P("p.yaml"), t, {})
        self.assertFalse(any(x["rule"] == "CE-L4-002" for x in f))

    def test_activity_has_no_trigger_requirement(self):
        # R4 reconciliation: Activity's canonical schema does NOT declare trigger/outcome.
        a = {"id": "processes:activity-x", "type": "Activity", "name": "N", "version": "1",
             "belongs_to_business_process": "b", "cohesion_rationale": "c"}
        f = cc.check_record(P("p.yaml"), a, {})
        self.assertFalse([x for x in f if x["severity"] == "blocking"], f)


class TestCli(unittest.TestCase):
    def _run(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "scripts" / "check_completeness.py"), *args],
                              capture_output=True, text=True, cwd=str(ROOT))

    def test_self_test(self):
        r = self._run("--self-test")
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_advisory_returns_zero(self):
        r = self._run("--advisory")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("3723 records", r.stdout)

    def test_report_written(self):
        self._run("--advisory")
        rep = ROOT / "reconciliation" / "completeness-report.yaml"
        self.assertTrue(rep.exists())
        import yaml as _y
        d = _y.safe_load(rep.read_text())
        self.assertEqual(d["record_count"], 3723)
        self.assertIn("by_level", d)
        # The seven operational fields were populated in 0 records at the CE-0
        # baseline (the programme's core thesis). The tranches populate them
        # progressively with provenance-marked values: CE-L1 lands the L1
        # `owner` candidates (49 PGs); CE-L2 lands the L2 `owner` candidates
        # (145 BPs) and the derived `process_classification` blocks (145).
        # `owner` is therefore 49 + 145 = 194 with both tranches merged (145
        # from CE-L2 alone while CE-L1 is pending), and the rest remain 0
        # pending their tranches or the human governance sweep.
        import glob as _glob
        import yaml as _yaml
        l1_owner = sum(
            1 for p in _glob.glob(str(ROOT / "entities" / "**" / "processes-group-*.yaml"), recursive=True)
            if _yaml.safe_load(open(p, encoding="utf-8")).get("owner")
        )
        l2_owner = sum(
            1 for p in _glob.glob(str(ROOT / "entities" / "**" / "processes-process-*.yaml"), recursive=True)
            if _yaml.safe_load(open(p, encoding="utf-8")).get("owner")
        )
        for k, v in d["adoption"]["operational_fields"].items():
            expected = (l1_owner + l2_owner) if k == "owner" else 0
            self.assertEqual(v["populated"], expected, k)
        pc_pop = d["adoption"]["process_classification"]["populated"]
        self.assertEqual(
            pc_pop,
            sum(1 for p in _glob.glob(str(ROOT / "entities" / "**" / "processes-process-*.yaml"), recursive=True)
                if _yaml.safe_load(open(p, encoding="utf-8")).get("process_classification")),
            "process_classification counter must match the L2 records carrying the block",
        )

    def test_strict_passes_post_ce_l0(self):
        r = self._run("--strict")
        self.assertEqual(r.returncode, 0, "strict must pass once the CE-L0 tranche has remediated the 8 escape-clause PCs")
        self.assertIn("0 blocking", r.stdout)


if __name__ == "__main__":
    unittest.main()
