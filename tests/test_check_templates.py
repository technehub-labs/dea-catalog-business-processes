"""Tests for scripts/check_templates.py (TPL-001..005).

Authoritative reference: CR-BP-113 (2026-10-13, eaojnr).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_templates.py"

sys.path.insert(0, str(ROOT / "scripts"))
from check_templates import (  # noqa: E402
    LEGACY_ID_RE,
    POST_MV1_ID_RE,
    TEMPLATE_SCHEMA_MAP,
    _iter_templates,
    evaluate,
)


# ---------------------------------------------------------------------------
# TPL-001 (blocking): legacy dea:* in id fields
# ---------------------------------------------------------------------------


def test_tpl001_no_legacy_ids_in_live_templates() -> None:
    """Live templates: every `id:` field uses the post-mv1 family."""
    blocking, _ = evaluate()
    tpl001 = [m for r, m in blocking if r == "TPL-001"]
    assert not tpl001, f"live templates have legacy ids: {tpl001[:5]}"


def test_legacy_id_regex_matches_known_forms() -> None:
    """The legacy regex catches every dea:<level>- form."""
    for s in ("dea:process-foo", "dea:activity-bar", "dea:task-baz",
              "dea:group-qux", "dea:pc-fred", "dea:scope-bleh"):
        assert LEGACY_ID_RE.match(s), f"should match: {s}"
    # Post-mv1 forms are NOT caught
    for s in ("processes:process-foo", "processes:activity-bar",
              "processes:pc-pr-op"):
        assert not LEGACY_ID_RE.match(s), f"false positive on: {s}"


def test_post_mv1_id_regex_matches_canonical_forms() -> None:
    """The post-mv1 regex catches the canonical family."""
    for s in ("processes:process-ao-activate-bsjbfc",
              "processes:activity-fa-activate-yrhcfm",
              "processes:pc-pr-operate-pwue5a"):
        assert POST_MV1_ID_RE.match(s), f"should match: {s}"


# ---------------------------------------------------------------------------
# TPL-002 (blocking): legacy dea:* in structured reference fields
# ---------------------------------------------------------------------------


def test_tpl002_live_clean() -> None:
    """Live templates: every structured reference field uses post-mv1."""
    blocking, _ = evaluate()
    tpl002 = [m for r, m in blocking if r == "TPL-002"]
    assert not tpl002, f"live templates have legacy refs: {tpl002[:5]}"


# ---------------------------------------------------------------------------
# TPL-003 (advisory): template schema-load
# ---------------------------------------------------------------------------


def test_tpl003_schemas_loadable() -> None:
    """All schemas referenced by the 5 entity templates load as JSON."""
    import json
    schemas_dir = ROOT / "schemas" / "entities"
    for tpl_name, schema_name in TEMPLATE_SCHEMA_MAP.items():
        if schema_name is None:
            continue
        schema_path = schemas_dir / schema_name
        assert schema_path.exists(), f"schema missing: {schema_path}"
        json.loads(schema_path.read_text())


# ---------------------------------------------------------------------------
# TPL-004 (blocking): evidence-link type enum
# ---------------------------------------------------------------------------


def test_tpl004_no_stale_evidence_enum_in_live_templates() -> None:
    """Live templates: no stale `evidence | reference` enum comment."""
    blocking, _ = evaluate()
    tpl004 = [m for r, m in blocking if r == "TPL-004"]
    assert not tpl004, f"live templates have stale enum: {tpl004[:5]}"


# ---------------------------------------------------------------------------
# TPL-005 (advisory): copy-to path comments
# ---------------------------------------------------------------------------


def test_tpl005_no_pre_mv1_copy_to_paths_in_live_templates() -> None:
    """Live templates: no `entities/v1-alpha/dea:` copy-to paths."""
    blocking, _ = evaluate()
    tpl005 = [m for r, m in blocking if r == "TPL-005"]
    assert not tpl005, f"live templates have pre-mv1 paths: {tpl005[:5]}"


# ---------------------------------------------------------------------------
# Live catalog posture
# ---------------------------------------------------------------------------


def test_live_repo_verdict_is_conformant() -> None:
    """Live repo: the gate's verdict is CONFORMANT."""
    blocking, _ = evaluate()
    assert not blocking, f"unexpected blocking: {blocking[:5]}"


def test_iter_templates_skips_doc_profile() -> None:
    """Doc-profile templates are out of CR-BP-113 §4 scope."""
    paths = _iter_templates()
    for p in paths:
        assert not p.name.startswith("documentation-profile-"), p.name


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_self_test_passes() -> None:
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--self-test"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert r.returncode == 0, (
        f"--self-test failed: stdout={r.stdout!r} stderr={r.stderr!r}"
    )


def test_cli_strict_clean_on_live() -> None:
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--strict"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert r.returncode == 0, (
        f"--strict failed: stdout={r.stdout!r} stderr={r.stderr!r}"
    )
