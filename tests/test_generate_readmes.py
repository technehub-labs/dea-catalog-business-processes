#!/usr/bin/env python3
"""test_generate_readmes.py — EXT-02 README generator tests.

CR-BP-94-EXT-02. Verifies:
  - generate_readmes discovers all canonical records across both
    storage shapes (directory-per-record + flat-file).
  - resolve_level() correctly identifies L0/L1/L2/L3/L4 by type or id pattern.
  - resolve_readme_path() honours both storage shapes.
  - generate_readme() produces all required section headings per profile.
  - End-to-end run closes DOC-001 to 0 against the live catalog.
  - --dry-run does not touch the filesystem.
  - --scope filters by record id.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_resolve_level_by_type():
    from scripts.generate_readmes import resolve_level
    assert resolve_level({"type": "ProcessContext", "id": "processes:pc-x-y"}) == "L0"
    assert resolve_level({"type": "ProcessGroup", "id": "processes:group-x"}) == "L1"
    assert resolve_level({"type": "Process", "id": "processes:process-x"}) == "L2"
    assert resolve_level({"type": "Activity", "id": "processes:activity-x"}) == "L3"
    assert resolve_level({"type": "Task", "id": "processes:task-x"}) == "L4"
    # PC fallback: id pattern when type is absent.
    assert resolve_level({"id": "processes:pc-x-y"}) == "L0"
    # Unknown.
    assert resolve_level({"type": "Unknown", "id": "x"}) is None
    assert resolve_level({}) is None


def test_resolve_record_paths_counts():
    from scripts.generate_readmes import resolve_record_paths
    paths = resolve_record_paths()
    # CR-BP-mv1: all 3,598 records (PCs included) live in the containment
    # tree under entities/v1-alpha/; the contexts/ root is retired.
    assert len(paths) >= 3598, f"Expected >= 3598 paths, got {len(paths)}"
    entities_count = sum(1 for p in paths if "/entities/" in str(p))
    pc_count = sum(1 for p in paths if p.name.startswith("processes-pc-"))
    assert entities_count >= 3598, f"Expected >= 3598 entity paths, got {entities_count}"
    assert pc_count >= 49, f"Expected >= 49 PC paths, got {pc_count}"


def test_resolve_readme_path_directory_shape():
    from scripts.generate_readmes import resolve_readme_path
    # Directory-per-record shape (L1/L2/L3/L4).
    p = Path("/fake/entities/v1-alpha/dea:group-x/dea:group-x.yaml")
    assert resolve_readme_path(p, "processes:group-x") == Path(
        "/fake/entities/v1-alpha/dea:group-x/README.md"
    )


def test_resolve_readme_path_flat_shape():
    from scripts.generate_readmes import resolve_readme_path
    # Flat-file shape (L0 ProcessContext).
    p = Path("/fake/contexts/v1-alpha/dea-pc-x-y.yaml")
    assert resolve_readme_path(p, "processes:pc-x-y") == Path(
        "/fake/contexts/v1-alpha/dea-pc-x-y/README.md"
    )


def test_generate_readme_required_sections_l0():
    from scripts.generate_readmes import generate_readme, SECTION_HEADINGS
    record = {
        "id": "processes:pc-test",
        "domain": "StrategyAndDirection",
        "lifecycle_stage": "Retire",
        "name": "Test PC",
        "definition": "Test definition.",
    }
    out = generate_readme(record, "L0")
    # L0 requires 11 sections (no outcomes).
    for sid in [
        "entity-identity", "formal-definition", "semantic-dimensions",
        "decomposition", "behavior", "interfaces", "roles",
        "rules-controls", "evidence", "completeness", "revision-history",
    ]:
        assert SECTION_HEADINGS[sid] in out, f"L0 README missing section {sid}"


def test_generate_readme_required_sections_l2():
    from scripts.generate_readmes import generate_readme, SECTION_HEADINGS
    record = {
        "id": "processes:process-test",
        "type": "Process",
        "name": "Test BP",
        "version": "1.0.0",
        "lifecycle_status": "candidate",
        "definition": "Test definition.",
        "trigger": "Test trigger.",
        "outcome": "Test outcome.",
        "identity": {"verb": "Test", "object": "Process", "scope": "test"},
        "part_of": ["processes:group-x"],
        "process_scope": {"includes": ["x"], "excludes": ["y"]},
        "ecfConformance": {
            "canonicalReferences": [
                {"domain": "StrategyAndDirection", "stage": "Retire"}
            ]
        },
    }
    out = generate_readme(record, "L2")
    # L2 requires 12 sections (includes outcomes).
    for sid in [
        "entity-identity", "formal-definition", "semantic-dimensions",
        "decomposition", "behavior", "interfaces", "roles",
        "rules-controls", "outcomes", "evidence", "completeness",
        "revision-history",
    ]:
        assert SECTION_HEADINGS[sid] in out, f"L2 README missing section {sid}"


def test_cli_dry_run_does_not_write():
    """--dry-run reports without touching the filesystem."""
    result = subprocess.run(
        [sys.executable, "scripts/generate_readmes.py", "--dry-run"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, result.stderr
    # The dry-run summary line is always present.
    assert "generate_readmes: written=" in result.stdout
    # --dry-run writes nothing: re-running should still show the same counts.
    result2 = subprocess.run(
        [sys.executable, "scripts/generate_readmes.py", "--dry-run"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    line1 = [l for l in result.stdout.splitlines() if "generate_readmes:" in l][0]
    line2 = [l for l in result2.stdout.splitlines() if "generate_readmes:" in l][0]
    assert line1 == line2, f"dry-run not idempotent:\n  {line1}\n  {line2}"


def test_cli_scope_filters_by_record_id(tmp_path):
    """--scope restricts generation to a single record id."""
    # Pick a real record id (the SD/Retire BP) that has a README so the
    # dry-run line is non-empty and we can verify the scope actually
    # narrows the scan to a single record.
    real_scope = "processes:process-sd-retire-umxf3c"  # CR-BP-mv1 id form
    result = subprocess.run(
        [
            sys.executable, "scripts/generate_readmes.py",
            "--scope", real_scope,
            "--dry-run",
        ],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, result.stderr
    summary = [l for l in result.stdout.splitlines() if "generate_readmes:" in l][0]
    assert "total_scanned=1" in summary, f"scope did not filter: {summary}"

    # And a non-existent scope should yield zero scanned records.
    fake_scope = "processes:process-does-not-exist-record-xyz"
    result2 = subprocess.run(
        [
            sys.executable, "scripts/generate_readmes.py",
            "--scope", fake_scope,
            "--dry-run",
        ],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert result2.returncode == 0, result2.stderr
    summary2 = [l for l in result2.stdout.splitlines() if "generate_readmes:" in l][0]
    assert "total_scanned=0" in summary2, f"non-existent scope should yield 0: {summary2}"


def test_live_run_closes_doc_001():
    """End-to-end: the generator closes DOC-001 to 0 on the live catalog.

    DOC-001 = README exists at entities/v1-alpha/<id>/README.md (and the
    L0 equivalent at contexts/v1-alpha/<id>/README.md). The generator
    writes all canonical records, so after a single run DOC-001 == 0.
    """
    # Pre-flight: count existing READMEs that satisfy DOC-001.
    pre = subprocess.run(
        [
            sys.executable, "scripts/check_documentation_profile.py",
            "--json",
        ],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    pre_data = json.loads(pre.stdout)
    pre_doc001 = sum(1 for f in pre_data.get("findings", []) if f["rule"] == "DOC-001")
    # Run generator.
    gen = subprocess.run(
        [sys.executable, "scripts/generate_readmes.py"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert gen.returncode == 0, gen.stderr
    # Post-flight.
    post = subprocess.run(
        [
            sys.executable, "scripts/check_documentation_profile.py",
            "--json",
        ],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    post_data = json.loads(post.stdout)
    post_doc001 = sum(1 for f in post_data.get("findings", []) if f["rule"] == "DOC-001")
    assert post_doc001 == 0, f"Expected DOC-001 == 0 after run, got {post_doc001}"
    # Generator wrote >= 1 (assuming at least one record was missing).
    summary = [l for l in gen.stdout.splitlines() if "generate_readmes:" in l][0]
    assert "written=" in summary
