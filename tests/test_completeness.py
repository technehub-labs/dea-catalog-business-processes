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
        # the seven operational fields are populated in 0 records (the programme's core thesis)
        for k, v in d["adoption"]["operational_fields"].items():
            self.assertEqual(v["populated"], 0, k)

    def test_strict_passes_post_ce_l0(self):
        r = self._run("--strict")
        self.assertEqual(r.returncode, 0, "strict must pass once the CE-L0 tranche has remediated the 8 escape-clause PCs")
        self.assertIn("0 blocking", r.stdout)


if __name__ == "__main__":
    unittest.main()
