"""Tests for CR-BP-117c C-1/C-3 tooling.

- scripts/rename_dirs_human_names.py: kebab transform, plan shape,
  collision fallback.
- generate_readmes.py path-scheme section: deterministic tree render
  for L0 PC READMEs.

Authoritative reference: CR-BP-117 §4 (2026-10-13, eaojnr).
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from rename_dirs_human_names import build_plan, kebab  # noqa: E402
import generate_readmes as gr  # noqa: E402


# ---------------------------------------------------------------------------
# kebab transform
# ---------------------------------------------------------------------------


class TestKebab:
    @pytest.mark.parametrize("name,expected", [
        ("Conclude Regulated Run-Off", "Conclude-Regulated-Run-Off"),
        ("Wind Down Liabilities", "Wind-Down-Liabilities"),
        ("Confirm Finality", "Confirm-Finality"),
        # comma collapse
        ("Accounting, Reporting, and Treasury Operation",
         "Accounting-Reporting-and-Treasury-Operation"),
        # parens collapse
        ("Activate Continuing-Supervisor Notification (Billing)",
         "Activate-Continuing-Supervisor-Notification-Billing"),
        # slash runs collapse to single hyphens
        ("Screen Candidates Against Sanctions / AML / FCRA / ADA",
         "Screen-Candidates-Against-Sanctions-AML-FCRA-ADA"),
    ])
    def test_transform(self, name, expected):
        assert kebab(name) == expected

    def test_never_empty_for_real_names(self):
        assert kebab("A") == "A"


# ---------------------------------------------------------------------------
# plan shape (fixture tree)
# ---------------------------------------------------------------------------


def _mk_cell(root: Path) -> Path:
    cell = root / "entities" / "v1-alpha" / "zz-test"
    cell.mkdir(parents=True)
    (cell / "processes-pc-zz-test-aaaaaa.yaml").write_text(
        "id: processes:pc-zz-test-aaaaaa\nname: Test Cell\n"
    )
    grp = cell / "zz-test-bbbbbb"
    grp.mkdir()
    (grp / "processes-group-zz-test-bbbbbb.yaml").write_text(
        "id: processes:group-zz-test-bbbbbb\nname: Test Group\n"
    )
    proc = grp / "zz-test-cccccc"
    proc.mkdir()
    (proc / "processes-process-zz-test-cccccc.yaml").write_text(
        "id: processes:process-zz-test-cccccc\nname: Test Process\n"
    )
    return cell


def test_plan_renames_group_and_process_dirs():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        cell = _mk_cell(root)
        import rename_dirs_human_names as rn
        old_root, old_ent = rn.REPO_ROOT, rn.ENTITIES
        rn.REPO_ROOT, rn.ENTITIES = root, root / "entities" / "v1-alpha"
        try:
            renames, problems = build_plan()
        finally:
            rn.REPO_ROOT, rn.ENTITIES = old_root, old_ent
        assert not problems
        targets = {old.name: new.name for old, new in renames}
        assert targets == {
            "zz-test-bbbbbb": "Test-Group",
            "zz-test-cccccc": "Test-Process",
        }
        # deepest-first ordering: process dir (deeper) before group dir
        names = [old.name for old, _ in renames]
        assert names.index("zz-test-cccccc") < names.index("zz-test-bbbbbb")


def test_plan_skips_cell_root_pc():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        cell = _mk_cell(root)
        import rename_dirs_human_names as rn
        old_root, old_ent = rn.REPO_ROOT, rn.ENTITIES
        rn.REPO_ROOT, rn.ENTITIES = root, root / "entities" / "v1-alpha"
        try:
            renames, _ = build_plan()
        finally:
            rn.REPO_ROOT, rn.ENTITIES = old_root, old_ent
        # the cell dir itself is never a rename target
        assert all(cell not in (old, new) for old, new in renames)


# ---------------------------------------------------------------------------
# path-scheme render (fixture tree via monkeypatched ENTITIES_ROOT)
# ---------------------------------------------------------------------------


def test_path_scheme_renders_tree():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        cell = _mk_cell(root)
        old_ent = gr.ENTITIES_ROOT
        gr.ENTITIES_ROOT = root / "entities" / "v1-alpha"
        try:
            record = yaml.safe_load(
                (cell / "processes-pc-zz-test-aaaaaa.yaml").read_text()
            )
            out = gr.render_section("path-scheme", record, "L0")
        finally:
            gr.ENTITIES_ROOT = old_ent
        assert "```" in out
        assert "zz-test/" in out
        assert "zz-test-bbbbbb/  (L1 ProcessGroup)" in out
        assert "zz-test-cccccc/  (L2 Process)" in out
        # process dir is nested under the group dir (depth indent)
        lines = out.splitlines()
        g = next(i for i, l in enumerate(lines) if "Test Group" in l or "zz-test-bbbbbb" in l)
        p = next(i for i, l in enumerate(lines) if "zz-test-cccccc" in l)
        assert lines[p].startswith("    ")  # deeper indent than group
        assert lines[g].startswith("  ")


def test_path_scheme_malformed_id():
    out = gr.render_section("path-scheme", {"id": "garbage"}, "L0")
    assert "unavailable" in out


# ---------------------------------------------------------------------------
# live tree invariants (post-rename)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not (ROOT / "entities" / "v1-alpha" / "fa-retire" / "Regulated-Run-Off").exists(),
    reason="live rename not yet applied",
)
def test_live_no_hash_dirs_remain():
    """After C-1, no directory *below the cell root* is named with a
    bare BASE32 hash suffix (`<slug>-<hash6>`). Cell dirs themselves
    keep their `<domain>-<stage>` slugs by design (C-1 scope)."""
    import re
    # IDM-004 strict alphabet (no i/l/o/u); cell dirs like fa-retire
    # contain i and are excluded by depth scoping anyway.
    hash_dir = re.compile(r"-[abcdefghjkmnpqrstuvwxyz23456789]{6}$")
    offenders = []
    for cell in (ROOT / "entities" / "v1-alpha").iterdir():
        if not cell.is_dir():
            continue
        for p in cell.rglob("*"):
            if p.is_dir() and p != cell and hash_dir.search(p.name):
                offenders.append(p)
    assert not offenders, f"{len(offenders)} hash dirs remain: {offenders[:3]}"
