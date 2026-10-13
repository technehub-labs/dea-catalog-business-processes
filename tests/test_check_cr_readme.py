"""Tests for scripts/check_cr_readme.py (CRR-001..003).

Authoritative reference: CR-BP-113 (2026-10-13, eaojnr).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_cr_readme.py"

sys.path.insert(0, str(ROOT / "scripts"))
from check_cr_readme import (  # noqa: E402
    CR_LINK_RE,
    evaluate,
)


# ---------------------------------------------------------------------------
# CRR-001 (blocking): every CR link resolves on disk
# ---------------------------------------------------------------------------


def test_crr001_live_clean() -> None:
    """Live repo: every CR link in every markdown table row resolves."""
    blocking, _ = evaluate()
    crr001 = [m for r, m in blocking if r == "CRR-001"]
    assert not crr001, f"live README has CRR-001 hits: {crr001[:5]}"


# ---------------------------------------------------------------------------
# CRR-002 (blocking): no duplicate CR link in the in-repo table
# ---------------------------------------------------------------------------


def test_crr002_live_clean() -> None:
    """Live repo: no in-repo table has the same CR link twice."""
    blocking, _ = evaluate()
    crr002 = [m for r, m in blocking if r == "CRR-002"]
    assert not crr002, f"live README has CRR-002 hits: {crr002[:5]}"


# ---------------------------------------------------------------------------
# CRR-003 (blocking): every CR file has exactly one in-repo row
# ---------------------------------------------------------------------------


def test_crr003_live_clean() -> None:
    """Live repo: every CR file on disk has a row in the in-repo table."""
    blocking, _ = evaluate()
    crr003 = [m for r, m in blocking if r == "CRR-003"]
    assert not crr003, f"live README has CRR-003 hits: {crr003[:5]}"


# ---------------------------------------------------------------------------
# Live catalog posture
# ---------------------------------------------------------------------------


def test_live_repo_verdict_is_conformant() -> None:
    """Live repo: the gate's verdict is CONFORMANT."""
    blocking, _ = evaluate()
    assert not blocking, f"unexpected blocking: {blocking[:5]}"


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


def test_cr_link_regex_matches_expected_forms() -> None:
    """The CR link regex matches the canonical markdown link shape."""
    s = "| [CR-BP-113](CR-BP-113-mv1-migration-completion.md) | x |"
    m = CR_LINK_RE.search(s)
    assert m is not None
    assert m.group("label") == "CR-BP-113"
    assert m.group("target") == "CR-BP-113-mv1-migration-completion.md"
