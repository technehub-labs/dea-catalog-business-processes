"""Tests for scripts/check_readme_consistency.py (RDM-001..002).

Locks behaviour for the README drift gate. Record READMEs are a
generated artifact post-CR-BP-114: the entity record is the source
of truth, scripts/generate_readmes.py renders, this gate verifies.

Authoritative reference: CR-BP-114 (2026-10-13, eaojnr).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_readme_consistency.py"
GENERATOR = ROOT / "scripts" / "generate_readmes.py"

sys.path.insert(0, str(ROOT / "scripts"))
from check_readme_consistency import evaluate  # noqa: E402


# ---------------------------------------------------------------------------
# RDM-001 (blocking): record README missing or stale
# ---------------------------------------------------------------------------


def test_rdm001_live_repo_clean() -> None:
    """Live repo: every record README matches generator output."""
    blocking, _ = evaluate()
    rdm001 = [m for r, m in blocking if r == "RDM-001"]
    assert not rdm001, f"live repo has RDM-001 hits: {rdm001[:5]}"


def test_rdm002_live_repo_clean() -> None:
    """Live repo: no orphan READMEs under entities/."""
    _, advisory = evaluate()
    rdm002 = [m for r, m in advisory if r == "RDM-002"]
    assert not rdm002, f"live repo has RDM-002 hits: {rdm002[:5]}"


# ---------------------------------------------------------------------------
# Generator contract
# ---------------------------------------------------------------------------


def test_generator_check_mode_exit_zero_on_current_tree() -> None:
    """generate_readmes.py --check exits 0 when the tree is current."""
    r = subprocess.run(
        [sys.executable, str(GENERATOR), "--check"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert r.returncode == 0, f"--check failed: {r.stdout[-500:]}"


def test_generator_force_then_check_roundtrip() -> None:
    """--force rewrites are idempotent: a second --check stays clean."""
    # The tree was regenerated in CR-BP-114; verify idempotency by
    # checking a single scope twice.
    scope = "entities/v1-alpha/ao-build/ao-build-m6fmyx"
    r1 = subprocess.run(
        [sys.executable, str(GENERATOR), "--force", "--scope", scope],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert r1.returncode == 0
    r2 = subprocess.run(
        [sys.executable, str(GENERATOR), "--check", "--scope", scope],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert r2.returncode == 0, f"scope check failed: {r2.stdout[-500:]}"


def test_generated_readme_uses_post_mv1_ids() -> None:
    """Generated READMEs carry the record's processes:* id, not dea:*."""
    blocking, _ = evaluate()
    assert not blocking
    # Spot-check one known record README.
    p = ROOT / "entities/v1-alpha/ao-build/ao-build-m6fmyx/README.md"
    text = p.read_text()
    assert "processes:group-ao-build-m6fmyx" in text
    assert "dea:group-" not in text.split("## 10.")[0]  # pre-evidence sections


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
        f"--strict failed: stdout={r.stdout[-500:]!r} stderr={r.stderr!r}"
    )


def test_cli_json_output_is_stable() -> None:
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--json"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert r.returncode == 0
    import json
    payload = json.loads(r.stdout)
    for key in ("verdict", "blocking", "advisory"):
        assert key in payload, f"missing key in JSON: {key}"
    assert payload["verdict"] == "CONFORMANT", payload["verdict"]
