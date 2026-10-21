#!/usr/bin/env python3
"""Tests for the entity map generator (L0 x L1 overview + per-cell drill-down).

Run:  cd tests && python3 -m unittest test_generate_entity_map
      (tests/ has no __init__.py, so the module must be run from inside tests/)

These tests assert the map's PROPERTIES, not its pixels: that every canonical
record is placed exactly once, that the level counts reconcile with the
catalogue, and that cell position is derived from the parent link rather than
assumed from the path. A map that silently drops a cell is worse than no map.
"""
import importlib.util
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _load():
    spec = importlib.util.spec_from_file_location(
        "generate_entity_map", REPO / "scripts" / "generate_entity_map.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mod = _load()


class TestLevelResolution(unittest.TestCase):
    """A record's level comes from its type, or from its id prefix for L0."""

    def test_l0_has_no_type_field_and_resolves_by_id_prefix(self):
        doc = {"id": "processes:pc-sd-improve-ft9k5f", "name": "Cell",
               "domain": "StrategyAndDirection", "lifecycle_stage": "Improve"}
        self.assertEqual(mod.level_of(doc), "L0")

    def test_declared_types_resolve(self):
        cases = {"ProcessGroup": "L1", "ProcessScope": "L1",
                 "Process": "L2", "Activity": "L3", "Task": "L4"}
        for typ, want in cases.items():
            with self.subTest(type=typ):
                self.assertEqual(mod.level_of({"id": "x", "type": typ}), want)

    def test_unknown_type_is_not_silently_mapped(self):
        self.assertEqual(mod.level_of({"id": "x", "type": "Widget"}), "?")


class TestParentContext(unittest.TestCase):
    """Cell position derives from the parent link each record carries."""

    def test_l1_scalar_process_context(self):
        doc = {"id": "processes:group-x", "type": "ProcessGroup",
               "process_context": "processes:pc-fa-retire-64q5p9"}
        self.assertEqual(mod.parent_context_id(doc), "processes:pc-fa-retire-64q5p9")

    def test_l2_context_list_with_ref(self):
        doc = {"id": "processes:process-x", "type": "Process",
               "context": [{"ref": "processes:pc-sd-improve-ft9k5f"}]}
        self.assertEqual(mod.parent_context_id(doc), "processes:pc-sd-improve-ft9k5f")

    def test_l2_context_list_ignores_non_cell_refs(self):
        doc = {"id": "processes:process-x", "type": "Process",
               "context": [{"ref": "dea:catalog-thing"}, {"ref": "processes:pc-y"}]}
        self.assertEqual(mod.parent_context_id(doc), "processes:pc-y")

    def test_missing_parent_returns_none_rather_than_guessing(self):
        self.assertIsNone(mod.parent_context_id({"id": "processes:task-x", "type": "Task"}))


class TestWalkExcludesNonCanonical(unittest.TestCase):
    """Research and documentation artefacts are not canonical records."""

    def test_record_count_matches_catalogue(self):
        records = mod.iter_records(REPO / "entities" / "v1-alpha")
        self.assertEqual(len(records), 3723,
                         "canonical record count changed; the map's totals must be re-verified")

    def test_no_research_or_documentation_records(self):
        records = mod.iter_records(REPO / "entities" / "v1-alpha")
        offenders = [str(p) for p, _d in records
                     if "research" in p.parts or "documentation" in p.parts]
        self.assertEqual(offenders, [], "non-canonical artefacts leaked into the walk")


class TestCellAssembly(unittest.TestCase):
    """Every record is placed exactly once, into a real cell."""

    @classmethod
    def setUpClass(cls):
        cls.records = mod.iter_records(REPO / "entities" / "v1-alpha")
        cls.cells, cls.audit = mod.build_cells(cls.records)

    def test_grid_is_7x7_and_fully_occupied(self):
        domains, stages = mod.axis_order(self.cells)
        self.assertEqual(len(domains), 7)
        self.assertEqual(len(stages), 7)
        self.assertEqual(len(self.cells), 49, "every ECF cell must be occupied")

    def test_stage_order_follows_the_lifecycle(self):
        _domains, stages = mod.axis_order(self.cells)
        self.assertEqual(stages, ["Conceive", "Design", "Build", "Activate",
                                  "Operate", "Improve", "Retire"])

    def test_every_record_placed_exactly_once(self):
        placed = sum(c["counts"]["L2"] + c["counts"]["L3"] + c["counts"]["L4"]
                     for c in self.cells.values())
        unplaced = sum(len(v) for v in self.audit.values())
        self.assertEqual(placed, 145 + 580 + 2900)
        self.assertEqual(unplaced, 0, f"unplaced records: {self.audit}")

    def test_level_counts_match_the_catalogue(self):
        tally = {lv: 0 for lv in ("L0", "L1", "L2", "L3", "L4")}
        for _p, d in self.records:
            lv = mod.level_of(d)
            if lv in tally:
                tally[lv] += 1
        self.assertEqual(tally, {"L0": 49, "L1": 49, "L2": 145,
                                "L3": 580, "L4": 2900})

    def test_one_group_per_cell(self):
        counts = [len(c["groups"]) for c in self.cells.values()]
        self.assertEqual(set(counts), {1},
                         "each cell carries exactly one L1 Process Group")


class TestDrilldownTree(unittest.TestCase):
    """The drill-down chain L2 -> L3 -> L4 must reconcile with the overview."""

    @classmethod
    def setUpClass(cls):
        records = mod.iter_records(REPO / "entities" / "v1-alpha")
        cls.tree = mod.build_tree(records)

    def test_l2_reconciles(self):
        n = sum(len(v) for v in self.tree["l2_by_cell"].values())
        self.assertEqual(n, 145)

    def test_l3_reconciles(self):
        n = sum(len(v) for v in self.tree["l3_by_l2"].values())
        self.assertEqual(n, 580)

    def test_l4_reconciles(self):
        n = sum(len(v) for v in self.tree["l4_by_l3"].values())
        self.assertEqual(n, 2900)

    def test_every_l3_parent_resolves_to_an_l2(self):
        for l2_id, acts in self.tree["l3_by_l2"].items():
            self.assertIn(l2_id, self.tree["records"],
                          f"L3 parent {l2_id} is not a canonical record")


class TestRendering(unittest.TestCase):
    """Rendered output must escape once and must not emit D-004 violations."""

    @classmethod
    def setUpClass(cls):
        records = mod.iter_records(REPO / "entities" / "v1-alpha")
        cells, audit = mod.build_cells(records)
        domains, stages = mod.axis_order(cells)
        cls.html = mod.render(cells, domains, stages, {
            "repo": "test", "revision": "test", "generated_at": "test",
            "totals": {"L0": 49, "L1": 49, "L2": 145, "L3": 580, "L4": 2900},
            "audit": audit})

    def test_row_labels_are_escaped_exactly_once(self):
        # A double-escaped ampersand is the regression this test guards:
        # esc() applied to an already-escaped string renders as "&AMP;".
        self.assertNotIn("&AMP;", self.html)
        self.assertIn("Agency &amp; Organization", self.html)

    def test_no_d004_violations(self):
        for name, ch in (("em dash", "\u2014"), ("en dash", "\u2013"),
                         ("two-em dash", "\u2E3B")):
            with self.subTest(char=name):
                self.assertEqual(self.html.count(ch), 0)
        self.assertEqual(self.html.count(";;;"), 0)

    def test_renders_every_cell(self):
        self.assertEqual(self.html.count('class="colhead"'), 7)
        self.assertEqual(self.html.count('class="rowhead"'), 7)
        self.assertEqual(self.html.count('class="cell-head"'), 49)


if __name__ == "__main__":
    unittest.main()