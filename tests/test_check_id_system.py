"""Test suite for check_id_system.py (CR-BP-mv1; CR-BP-126 IDM-001 fix).

The IDM-001 pattern was corrected in CR-BP-126: the original
`[a-z]{2,3}` requirement for the domain code was too strict and
excluded BP records with long descriptors. The corrected form
`(-[a-z]+){1,4}` matches all 5 type families.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_id_system.py"

# Extract the ID_PATTERN regex from the script
import importlib.util

spec = importlib.util.spec_from_file_location("check_id_system", SCRIPT)
assert spec is not None
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)
ID_PATTERN = mod.ID_PATTERN


# All 5 type families
def test_idm001_pc_record():
    assert ID_PATTERN.match("processes:pc-fa-retire-64q5p9")


def test_idm001_activity_record():
    assert ID_PATTERN.match("processes:activity-sd-improve-mu6upn")


def test_idm001_task_record():
    assert ID_PATTERN.match("processes:task-sd-improve-3pccaq")


def test_idm001_process_group():
    assert ID_PATTERN.match("processes:group-sd-improve-vdz4xp")


def test_idm001_bp_short_descriptor():
    assert ID_PATTERN.match("processes:process-foo-bar-f3n8wb")


def test_idm001_bp_long_descriptor():
    """The corrected pattern matches BP records with long descriptors
    like `process-manage-customer-relationship` (6 chars)."""
    assert ID_PATTERN.match("processes:process-manage-customer-relationship-f3n8wb")


def test_idm001_three_segment_descriptor():
    """3 segments between type and hash."""
    assert ID_PATTERN.match("processes:process-foo-bar-baz-f3n8wb")


def test_idm001_four_segment_descriptor():
    """4 segments (max) between type and hash."""
    assert ID_PATTERN.match("processes:process-foo-bar-baz-qux-f3n8wb")


def test_idm001_rejects_uppercase():
    """No uppercase allowed."""
    assert not ID_PATTERN.match("Processes:process-foo-bar-f3n8wb")
    assert not ID_PATTERN.match("processes:Process-foo-bar-f3n8wb")


def test_idm001_rejects_missing_hash():
    """Hash is required (6 chars from base32)."""
    assert not ID_PATTERN.match("processes:process-foo-bar")


def test_idm001_rejects_short_hash():
    """Hash must be exactly 6 chars."""
    assert not ID_PATTERN.match("processes:process-foo-bar-f3n8w")
    assert not ID_PATTERN.match("processes:process-foo-bar-f3n8wbc")


def test_idm001_rejects_five_segment_descriptor():
    """5 segments is too many (max 4)."""
    assert not ID_PATTERN.match("processes:process-foo-bar-baz-qux-quux-f3n8wb")


def test_idm001_rejects_no_namespace():
    """Namespace is required (e.g. processes:)."""
    assert not ID_PATTERN.match("process-foo-bar-baz-f3n8wb")


def test_idm001_rejects_legacy_dea_namespace():
    """Legacy `dea:` ids are NOT matched by the canonical pattern
    (they are grandfathered per EGV-012 + the IS-004 disposition)."""
    assert not ID_PATTERN.match("dea:process-foo-bar-baz")


def test_idm001_live_tree_all_records_match():
    """Every id in the live tree's entities/v1-alpha/ matches the
    corrected pattern. This is the regression test that prevented
    the IDM-001 fix from breaking the live tree."""
    entities_dir = ROOT / "entities" / "v1-alpha"
    if not entities_dir.exists():
        return  # no entities dir; skip
    bad = []
    total = 0
    for path in entities_dir.rglob("*.yaml"):
        # Skip non-records (config, registry, etc.)
        if path.name in {"entity-system-registry.yaml", "conformance_report.yaml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        # Find `id:` at start of line
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("id:"):
                rid = line.split(":", 1)[1].strip()
                if not rid:
                    continue
                total += 1
                # Legacy `dea:` ids are grandfathered
                if rid.startswith("dea:"):
                    continue
                if not ID_PATTERN.match(rid):
                    bad.append((str(path), rid))
    assert bad == [], f"non-canonical ids found: {bad[:10]} (of {total} records)"
