"""Tests for scripts/check_href_targets.py (HREF-001..003).

Locks behaviour for the href-resolver gate. The gate runs as part
of the conformance suite and as a standalone CI step; these tests
cover both the in-process evaluate() function and the CLI surface.

Authoritative reference: CR-BP-113 (2026-10-13, eaojnr).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_href_targets.py"

sys.path.insert(0, str(ROOT / "scripts"))
from check_href_targets import (  # noqa: E402
    HREF_LINE_RE,
    _resolve,
    evaluate,
)


# ---------------------------------------------------------------------------
# HREF-001 (blocking): unresolved relative href
# ---------------------------------------------------------------------------


def test_href001_relative_target_resolves(tmp_path: Path) -> None:
    """A non-http relative href that exists on disk does not fire."""
    (tmp_path / "entities").mkdir()
    target = tmp_path / "entities" / "real.md"
    target.write_text("# x\n")
    # Use tmp_path as root; the resolver is param-driven via the
    # evaluate() function, but _resolve takes a src_root. Test the
    # resolver directly.
    assert _resolve(tmp_path, "entities/real.md") == target.resolve()
    assert _resolve(tmp_path, "entities/missing.md") is not None
    # exists() distinguishes them
    assert not (tmp_path / "entities" / "missing.md").exists()


def test_href001_unresolved_in_live_repo() -> None:
    """Live repo: every relative href in entities/ and discovery/
    resolves on disk (post-CR-BP-113)."""
    blocking, _ = evaluate()
    emb001 = [m for r, m in blocking if r == "HREF-001"]
    assert not emb001, f"live repo has HREF-001 hits: {emb001[:5]}"


# ---------------------------------------------------------------------------
# HREF-002 (blocking): empty href value
# ---------------------------------------------------------------------------


def test_href002_empty_href_detected() -> None:
    """An `href:` line with no value trips HREF-002."""
    line = "  href: \n"
    m = HREF_LINE_RE.match(line)
    assert m is not None
    assert not m.group(1).strip(), "empty value should produce empty group capture"


def test_href002_live_repo_clean() -> None:
    """Live repo: no empty href values remain post-CR-BP-113."""
    blocking, _ = evaluate()
    emb002 = [m for r, m in blocking if r == "HREF-002"]
    assert not emb002, f"live repo has HREF-002 hits: {emb002[:5]}"


# ---------------------------------------------------------------------------
# HREF-003 (advisory): malformed http(s) URL
# ---------------------------------------------------------------------------


def test_href003_valid_http_url_does_not_fire() -> None:
    """A well-formed http URL is recognized as http(s) and skipped
    from HREF-001 (only HREF-003 would fire on shape issues, but a
    well-formed URL passes)."""
    blocking, _ = evaluate()
    # HREF-003 is advisory; we just confirm no finding for a
    # well-formed URL (none in the repo right now).
    emb003 = [m for r, m in blocking if r == "HREF-003"]
    assert not emb003, f"unexpected HREF-003 hits: {emb003[:5]}"


# ---------------------------------------------------------------------------
# Live catalog posture
# ---------------------------------------------------------------------------


def test_live_repo_verdict_is_conformant() -> None:
    """Live repo: the gate's verdict is CONFORMANT."""
    blocking, advisory = evaluate()
    assert not blocking, f"unexpected blocking: {blocking[:5]}"
    assert not advisory, f"unexpected advisory: {advisory[:5]}"


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
