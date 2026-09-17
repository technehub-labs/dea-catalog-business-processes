"""Tests for the CR-BP-95 Process Group extensions (PG-009, PG-010).

Locks behaviour for the optional `grouping_basis` and `membership_criteria`
fields introduced by CR-BP-95. Back-compat: the fields are OPTIONAL on the
existing 48 PG records; absence must not flag an error.

The tests cover:

* PG-009: grouping_basis structure (when present)
* PG-010: membership_criteria structure (when present)
* Back-compat: pre-CR-BP-95 PG records remain conformant without the new fields
* CLI self-test still passes after the extension
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_process_group.py"

sys.path.insert(0, str(ROOT / "scripts"))
from check_process_group import run_checks  # noqa: E402


def _write_minimal_pg(tmp_path: Path, *, grouping_basis=None, membership_criteria=None) -> Path:
    """Write a minimal conformant PG record; optionally with grouping_basis / membership_criteria."""
    entities = tmp_path / "entities" / "v1-alpha" / "dea:group-x"
    entities.mkdir(parents=True)
    # Provide a target BP record so the composes resolves; otherwise PG-005 fires.
    bp_dir = tmp_path / "entities" / "v1-alpha" / "dea:process-x"
    bp_dir.mkdir(parents=True)
    (bp_dir / "dea:process-x.yaml").write_text(
        "id: dea:process-x\n"
        "type: Process\n"
        "name: X\n"
        "version: 1.0.0\n"
        "lifecycle_status: active\n"
        "process_intent: manage\n"
        "process_type: core\n"
        "trigger: trigger\n"
        "outcome: outcome\n"
        "identity:\n"
        "  verb: Do\n"
        "  object: X\n"
        "  outcome_statement: outcome.\n"
        "  evidence_links: [{type: documentation, ref: docs/x.md}]\n"
        "relationships:\n"
        "  - source_id: dea:process-x\n"
        "    relationship_type: serves\n"
        "    target_id: ecf:governanceAndExistence.conceive\n"
        "ecfConformance:\n"
        "  framework: EnterpriseConceptFramework\n"
        "  contractVersion: 1.0.0\n"
        "  profile: dea:ecf@1.0.0\n"
        "  status: conformant\n"
        "  affiliation: inherits-catalog\n"
        "  canonicalReferences:\n"
        "    - kind: coordinate\n"
        "      domain: GovernanceAndExistence\n"
        "      stage: Conceive\n"
        "      identifier: ecf:governanceExistence.conceive\n"
        "metadata:\n"
        "  established_by: test\n"
        "  established_at: '2026-09-18'\n"
        "  change_history:\n"
        "    - cr: test\n"
        "      date: '2026-09-18'\n"
        "      change: test\n"
        "context:\n"
        "  - ref: dea:pc-test\n",
        encoding="utf-8",
    )
    body = (
        "id: dea:group-x\n"
        "type: ProcessGroup\n"
        "name: X\n"
        "version: 1.0.0\n"
        "process_context: dea:pc-test\n"
        "process_group_kind: functional\n"
        "scope:\n  includes: [a]\n  excludes: [b]\n"
        "outcomes: [x]\n"
        "composes:\n"
        "  - source_id: dea:group-x\n"
        "    target_id: dea:process-x\n"
        "    relationship_type: composes\n"
        "    status: active\n"
        "status: active\n"
        "lifecycle_status: active\n"
        "definition: x\n"
    )
    if grouping_basis is not None:
        import yaml
        gb_dump = yaml.safe_dump(grouping_basis, default_flow_style=False, sort_keys=False)
        # Indent each line by 2 spaces so the result nests correctly under `grouping_basis:`.
        gb_indented = "\n".join("  " + ln if ln.strip() else ln for ln in gb_dump.splitlines())
        body += "\ngrouping_basis:\n" + gb_indented
    if membership_criteria is not None:
        import yaml
        mc_dump = yaml.safe_dump(membership_criteria, default_flow_style=False, sort_keys=False)
        mc_indented = "\n".join("  " + ln if ln.strip() else ln for ln in mc_dump.splitlines())
        body += "\nmembership_criteria:\n" + mc_indented
    path = entities / "dea:group-x.yaml"
    path.write_text(body, encoding="utf-8")
    return path


def test_pg_without_new_fields_passes(tmp_path: Path) -> None:
    """Back-compat: pre-CR-BP-95 PG record without grouping_basis or membership_criteria."""
    _write_minimal_pg(tmp_path)
    errors, _ = run_checks(tmp_path)
    assert errors == [], errors


def test_pg009_valid_grouping_basis_passes(tmp_path: Path) -> None:
    """PG-009 happy path."""
    _write_minimal_pg(
        tmp_path,
        grouping_basis={
            "type": "functional-responsibility",
            "statement": "Groups processes by organizational function.",
        },
    )
    errors, _ = run_checks(tmp_path)
    assert errors == [], errors


def test_pg009_invalid_grouping_basis_type_fails(tmp_path: Path) -> None:
    """PG-009: invalid type in controlled vocabulary."""
    _write_minimal_pg(
        tmp_path,
        grouping_basis={
            "type": "not-a-controlled-type",
            "statement": "x",
        },
    )
    errors, _ = run_checks(tmp_path)
    assert any("PG-009" in e for e in errors), errors


def test_pg009_missing_statement_fails(tmp_path: Path) -> None:
    """PG-009: statement missing or empty."""
    _write_minimal_pg(
        tmp_path,
        grouping_basis={"type": "value-stream", "statement": ""},
    )
    errors, _ = run_checks(tmp_path)
    assert any("PG-009" in e for e in errors), errors


def test_pg010_valid_membership_criteria_passes(tmp_path: Path) -> None:
    """PG-010 happy path."""
    _write_minimal_pg(
        tmp_path,
        membership_criteria={
            "inclusion_test": "BP belongs if trigger is customer-initiated.",
            "exclusion_test": "BP is excluded if trigger is regulator-initiated.",
        },
    )
    errors, _ = run_checks(tmp_path)
    assert errors == [], errors


def test_pg010_missing_inclusion_test_fails(tmp_path: Path) -> None:
    """PG-010: inclusion_test missing."""
    _write_minimal_pg(
        tmp_path,
        membership_criteria={
            "inclusion_test": "",
            "exclusion_test": "x",
        },
    )
    errors, _ = run_checks(tmp_path)
    assert any("PG-010" in e for e in errors), errors


# --- Live catalog assertion --------------------------------------------------


def test_live_catalog_passes_pg_001_through_010() -> None:
    """The live catalog has 48 PG records, none yet carrying grouping_basis
    or membership_criteria. They MUST remain conformant (back-compat).
    """
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS (PG-001..010)" in result.stdout


# --- CLI self-test -----------------------------------------------------------


def test_cli_self_test_still_passes() -> None:
    """PG self-test must continue to pass after PG-009/010 extension.

    The self_test() function exercises the rule set on a deliberately broken
    catalog then a fixed one; on success it returns 0 with no special marker.
    """
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--self-test"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS (PG-001..010)" in result.stdout
