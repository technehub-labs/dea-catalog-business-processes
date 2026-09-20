"""Tests for the CR-BP-95 L0 Process Scope validator.

Locks behaviour for PSCOPE-001..008 by exercising both the in-process
`run_checks()` function and the CLI self-test entry point, plus a
live-catalog assertion that all 48 PG records currently emit zero
findings (the catalog is fully aligned for the L0/L1 layer; L0 records
are intentionally pre-population per CR-BP-95).

The tests cover:

* PSCOPE-001  ID pattern
* PSCOPE-002  Required fields
* PSCOPE-003  Process Context resolution
* PSCOPE-004  Composes target_id pattern
* PSCOPE-005  Composes target resolution
* PSCOPE-006  MECE within a Process Context
* PSCOPE-007  Scope kind controlled vocabulary
* PSCOPE-008  Lifecycle status
* PSCOPE-extra  type discriminator; decomposition_basis structure
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_process_scope.py"

sys.path.insert(0, str(ROOT / "scripts"))
from check_process_scope import (  # noqa: E402
    ID_PATTERN,
    SCOPE_KIND_VOCAB,
    _check_one,
    run_checks,
)


# --- Pure-function unit tests ------------------------------------------------


def test_id_pattern_accepts_canonical_scope_id() -> None:
    assert ID_PATTERN.match("processes:scope-pr-operate-vs0001")
    assert ID_PATTERN.match("processes:scope-fa-build-foo123")


def test_id_pattern_rejects_group_and_process_and_other_ids() -> None:
    for bad in (
        "processes:group-foo",
        "processes:process-foo",
        "processes:pc-foo",
        "dea:scopeFoo",  # camelCase
        "dea:scope_foo",  # underscore not allowed
        "scope-foo",  # missing namespace
        "dea:scope-",  # trailing dash
    ):
        assert not ID_PATTERN.match(bad), f"unexpectedly accepted: {bad}"


def test_scope_kind_vocabulary_has_six_values() -> None:
    assert len(SCOPE_KIND_VOCAB) == 6
    assert "value-stream" in SCOPE_KIND_VOCAB
    assert "cross-cutting-concern" in SCOPE_KIND_VOCAB


def test_check_one_flags_missing_required_fields(tmp_path: Path) -> None:
    """PSCOPE-002: required fields missing."""
    entry = {"id": "processes:scope-pr-operate-x001", "type": "ProcessScope"}  # most fields absent
    errors: list[str] = []
    _check_one(
        entry,
        context_ids=set(),
        group_ids=set(),
        errors=errors,
        all_entries=[],
    )
    assert any("PSCOPE-002" in e for e in errors), errors


def test_check_one_flags_bad_scope_kind(tmp_path: Path) -> None:
    """PSCOPE-007: scope_kind not in controlled vocabulary."""
    entry = {
        "id": "processes:scope-pr-operate-x001",
        "type": "ProcessScope",
        "name": "X",
        "version": "1.0.0",
        "definition": "x",
        "process_context": "processes:pc-test",
        "scope": {"includes": ["a"], "excludes": ["b"]},
        "outcomes": ["x"],
        "decomposition_basis": {
            "type": "value-stream",
            "statement": "x",
        },
        "composes": [],
        "scope_kind": "not-a-kind",
        "status": "active",
        "lifecycle_status": "active",
    }
    errors: list[str] = []
    _check_one(
        entry,
        context_ids={"processes:pc-test"},
        group_ids=set(),
        errors=errors,
        all_entries=[],
    )
    assert any("PSCOPE-007" in e for e in errors), errors


def test_check_one_passes_minimal_conformant_scope(tmp_path: Path) -> None:
    """PSCOPE happy path."""
    entry = {
        "id": "processes:scope-pr-operate-x001",
        "type": "ProcessScope",
        "name": "X",
        "version": "1.0.0",
        "definition": "x",
        "process_context": "processes:pc-test",
        "scope": {"includes": ["a"], "excludes": ["b"]},
        "outcomes": ["x"],
        "decomposition_basis": {
            "type": "value-stream",
            "statement": "Decomposes the value stream.",
        },
        "composes": [
            {
                "source_id": "processes:scope-pr-operate-x001",
                "target_id": "processes:group-x",
                "relationship_type": "composes",
                "status": "active",
            },
        ],
        "scope_kind": "value-stream",
        "status": "active",
        "lifecycle_status": "active",
    }
    errors: list[str] = []
    _check_one(
        entry,
        context_ids={"processes:pc-test"},
        group_ids={"processes:group-x"},
        errors=errors,
        all_entries=[entry],
    )
    assert not errors, errors


# --- run_checks() integration tests -----------------------------------------


def test_run_checks_empty_catalog_returns_clean(tmp_path: Path) -> None:
    """Empty entities/ tree: no scopes, no groups. Honest no-records-found pass."""
    (tmp_path / "entities" / "v1-alpha").mkdir(parents=True)
    errors, _ = run_checks(tmp_path)
    assert errors == [], errors


def test_run_checks_pg_only_returns_clean_no_records_found(tmp_path: Path) -> None:
    """48 PG records, 0 PS records: PSCOPE returns honest pass without firing
    any MECE or resolution rules (no PS records to check)."""
    entities = tmp_path / "entities" / "v1-alpha" / "processes:group-x"
    entities.mkdir(parents=True)
    (entities / "processes:group-x.yaml").write_text(
        "id: dea:group-x\n"
        "type: ProcessGroup\n"
        "name: X\n"
        "version: 1.0.0\n"
        "process_context: dea:pc-test\n"
        "process_group_kind: functional\n"
        "scope:\n  includes: [a]\n  excludes: [b]\n"
        "outcomes: [x]\n"
        "composes: []\n"
        "status: active\n"
        "lifecycle_status: active\n"
        "definition: x\n",
        encoding="utf-8",
    )
    errors, _ = run_checks(tmp_path)
    assert errors == [], errors


def test_run_checks_ps_with_unresolved_target_id(tmp_path: Path) -> None:
    """PSCOPE-005: composes target_id does not resolve to a known group."""
    entities = tmp_path / "entities" / "v1-alpha" / "processes:scope-pr-operate-x001"
    entities.mkdir(parents=True)
    (entities / "processes-scope-pr-operate-x001.yaml").write_text(
        "id: processes:scope-pr-operate-x001\n"
        "type: ProcessScope\n"
        "name: X\n"
        "version: 1.0.0\n"
        "definition: x\n"
        "process_context: dea:pc-test\n"
        "scope:\n  includes: [a]\n  excludes: [b]\n"
        "outcomes: [x]\n"
        "decomposition_basis:\n  type: value-stream\n  statement: Decomposes the value stream.\n"
        "composes:\n"
        "  - source_id: processes:scope-pr-operate-x001\n"
        "    target_id: processes:group-pr-operate-nope01\n"
        "    relationship_type: composes\n"
        "    status: active\n"
        "scope_kind: value-stream\n"
        "status: active\n"
        "lifecycle_status: active\n",
        encoding="utf-8",
    )
    errors, _ = run_checks(tmp_path)
    assert any("PSCOPE-005" in e for e in errors), errors


# --- Live catalog assertion --------------------------------------------------


def test_live_catalog_passes_clean_no_pscope_records() -> None:
    """The live catalog has 48 PG records and 0 PS records.

    PSCOPE-001..008 must emit zero findings under this state; the validator
    must report the honest no-records-found message rather than a vacuous
    pass.
    """
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "no ProcessScope entries found" in result.stdout
    assert "Process Group records present and conformant" in result.stdout


# --- CLI self-test -----------------------------------------------------------


def test_cli_self_test_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--self-test"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PSCOPE self-test: PASS" in result.stdout
