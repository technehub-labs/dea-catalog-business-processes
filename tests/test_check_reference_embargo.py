"""Tests for the CR-BP-112 Reference Embargo validator.

Locks behaviour for EMB-001..004 by exercising both the in-process
`evaluate()` function and the CLI self-test entry point, plus
per-rule pass/fail fixtures that hit live repository state.

The tests cover:

* EMB-001  substantive embargoed-term occurrence outside the
           sealed-file allowlist (blocking).
* EMB-002  allowlist data file missing or malformed (blocking).
* EMB-003  sealed-file integrity drift (SHA-256 mismatch;
           blocking).
* EMB-004  false-positive registry hit that matches no recorded
           entry pattern (advisory).
* Token-class 2 mask: the `CR-BP-TMF-EMBARGO` and `TMF-EMBARGO`
  id tokens must be permitted wherever they appear as part of a
  CR id token.
* Sealed-path mask: the path of every entry in the allowlist
  `sealed_files` block must be permitted wherever it appears
  (so documentation links to the carrier do not trip EMB-001).
* False-positive registry: a `sid` pattern on a registered file
  must suppress EMB-001 hits.

Authoritative reference: CR-BP-112 (2026-10-12).
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_reference_embargo.py"

sys.path.insert(0, str(ROOT / "scripts"))
from check_reference_embargo import (  # noqa: E402
    EMBARGOED_TERMS,
    MASKED_TOKEN_PATTERN,
    TERM_PATTERNS,
    _iter_files,
    _load_allowlist,
    _mask_token,
    _sha256,
    _term_hit,
    evaluate,
)


# ---------------------------------------------------------------------------
# In-process fixtures: token-class 2 mask + sealed-path mask
# ---------------------------------------------------------------------------


def test_token_class_2_mask_full_id() -> None:
    """`CR-BP-TMF-EMBARGO` is permitted (id token, class 2)."""
    line = "Depends on CR-BP-TMF-EMBARGO strip (2026-09-22)."
    assert _term_hit(line) is None, (
        f"id token should not trip the gate, but got: {_term_hit(line)}"
    )


def test_token_class_2_mask_bare_component() -> None:
    """`TMF-EMBARGO` (the bare component) is permitted (class 2)."""
    line = "The CR_NUMBER_PATTERN lists TMF-EMBARGO as a path component."
    assert _term_hit(line) is None, (
        f"TMF-EMBARGO bare component should not trip the gate, "
        f"but got: {_term_hit(line)}"
    )


def test_sealed_path_mask_full_path() -> None:
    """Documentation links to the sealed carrier are permitted."""
    sealed = ("change-requests/CR-BP-TMF-EMBARGO-tmforum-reference-strip.md",)
    line = "Carrier: `change-requests/CR-BP-TMF-EMBARGO-tmforum-reference-strip.md`."
    assert _term_hit(line, sealed) is None, (
        f"sealed-path mention should not trip the gate, "
        f"but got: {_term_hit(line, sealed)}"
    )


def test_sealed_path_mask_bare_filename() -> None:
    """The bare filename (no directory prefix) is also permitted."""
    sealed = ("change-requests/CR-BP-TMF-EMBARGO-tmforum-reference-strip.md",)
    line = "See CR-BP-TMF-EMBARGO-tmforum-reference-strip.md section 3."
    assert _term_hit(line, sealed) is None, (
        f"sealed-path bare filename should not trip the gate, "
        f"but got: {_term_hit(line, sealed)}"
    )


def test_substantive_hit_not_masked() -> None:
    """A real substantive hit on a term is not masked."""
    line = "The directory cited tmforum as a source of BPSS process definitions."
    hit = _term_hit(line)
    assert hit == "tmforum", f"expected 'tmforum' hit, got {hit!r}"


# ---------------------------------------------------------------------------
# EMB-001: substantive embargoed-term occurrence
# ---------------------------------------------------------------------------


def _write_allowlist(tmp: Path, allowlist: dict) -> Path:
    """Write an allowlist data file under `tmp/reconciliation/`
    and return the path. Helper for the per-rule fixture tests."""
    (tmp / "reconciliation").mkdir(parents=True, exist_ok=True)
    p = tmp / "reconciliation" / "reference-embargo-allowlist.yaml"
    p.write_text(yaml.safe_dump(allowlist, sort_keys=False))
    return p


def test_emb001_substantive_hit_blocks(tmp_path: Path) -> None:
    """A non-sealed file with a substantive hit produces EMB-001."""
    (tmp_path / "x.md").write_text("The tmforum reference was used as source.\n")
    ap = _write_allowlist(tmp_path, {"version": 1, "sealed_files": [], "false_positives": []})
    blocking, _ = evaluate(tmp_path, allowlist_path=ap)
    assert any(
        r == "EMB-001" and "tmforum" in m for r, m in blocking
    ), f"expected EMB-001 'tmforum' hit, got: {blocking}"


# ---------------------------------------------------------------------------
# EMB-002: allowlist data file
# ---------------------------------------------------------------------------


def test_emb002_missing_allowlist_blocks(tmp_path: Path) -> None:
    """A repo without the allowlist data file produces EMB-002."""
    blocking, _ = evaluate(tmp_path, allowlist_path=tmp_path / "reconciliation" / "reference-embargo-allowlist.yaml")
    assert any(
        r == "EMB-002" and "missing" in m for r, m in blocking
    ), f"expected EMB-002 missing-allowlist, got: {blocking}"


def test_emb002_malformed_allowlist_blocks(tmp_path: Path) -> None:
    """An allowlist missing required keys produces EMB-002."""
    (tmp_path / "reconciliation").mkdir(parents=True)
    ap = tmp_path / "reconciliation" / "reference-embargo-allowlist.yaml"
    ap.write_text("version: 1\n")
    blocking, _ = evaluate(tmp_path, allowlist_path=ap)
    assert any(
        r == "EMB-002" and "malformed" in m for r, m in blocking
    ), f"expected EMB-002 malformed, got: {blocking}"


# ---------------------------------------------------------------------------
# EMB-003: sealed-file integrity drift
# ---------------------------------------------------------------------------


def test_emb003_sealed_file_drift_blocks(tmp_path: Path) -> None:
    """Tampering a sealed file produces EMB-003."""
    (tmp_path / "reconciliation").mkdir(parents=True)
    sealed = tmp_path / "sealed.md"
    sealed.write_text("Original content.\n")
    allowlist = {
        "version": 1,
        "sealed_files": [
            {
                "path": "sealed.md",
                "sha256": _sha256(sealed),
                "rationale": "Sealed test file.",
            },
        ],
        "false_positives": [],
    }
    ap = _write_allowlist(tmp_path, allowlist)
    # No drift: no finding
    b1, _ = evaluate(tmp_path, allowlist_path=ap)
    assert not any(r == "EMB-003" for r, _ in b1)
    # Tamper
    sealed.write_text("Original content.\nAdded sentence.\n")
    b2, _ = evaluate(tmp_path, allowlist_path=ap)
    assert any(
        r == "EMB-003" and "drift" in m for r, m in b2
    ), f"expected EMB-003 drift, got: {b2}"


def test_emb003_self_reference_exempt(tmp_path: Path) -> None:
    """The allowlist's self-reference is exempt at the gate level."""
    (tmp_path / "reconciliation").mkdir(parents=True)
    allowlist = {
        "version": 1,
        "sealed_files": [
            {
                "path": "reconciliation/reference-embargo-allowlist.yaml",
                "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
                "rationale": "Self-reference (exempt).",
            },
        ],
        "false_positives": [],
    }
    ap = _write_allowlist(tmp_path, allowlist)
    blocking, _ = evaluate(tmp_path, allowlist_path=ap)
    assert not any(r == "EMB-003" for r, _ in blocking), (
        f"self-reference should be exempt from EMB-003, got: {blocking}"
    )


# ---------------------------------------------------------------------------
# EMB-004: false-positive registry hygiene (advisory)
# ---------------------------------------------------------------------------


def test_emb004_unmatched_pattern_advisory(tmp_path: Path) -> None:
    """A registered false-positive pattern that matches nothing is EMB-004."""
    (tmp_path / "reconciliation").mkdir(parents=True)
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "noop.py").write_text("pass\n")
    allowlist = {
        "version": 1,
        "sealed_files": [],
        "false_positives": [
            {
                "path": "scripts/noop.py",
                "pattern": r"\bnever_matches_this_pattern_xyzzy\b",
                "rationale": "Dead pattern test fixture.",
            },
        ],
    }
    ap = _write_allowlist(tmp_path, allowlist)
    blocking, advisory = evaluate(tmp_path, allowlist_path=ap)
    assert any(
        r == "EMB-004" and "no current content" in m for r, m in advisory
    ), f"expected EMB-004 dead pattern, got: advisory={advisory}"


def test_false_positive_pattern_suppresses_hit(tmp_path: Path) -> None:
    """A registered `sid` pattern suppresses EMB-001 hits in code."""
    (tmp_path / "reconciliation").mkdir(parents=True)
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "iter.py").write_text(
        "for sid in sections:\n    print(sid)\n"
    )
    allowlist = {
        "version": 1,
        "sealed_files": [],
        "false_positives": [
            {
                "path": "scripts/iter.py",
                "pattern": r"\bsid\b",
                "rationale": "Python variable name (CR-BP-TMF-EMBARGO section 3).",
            },
        ],
    }
    ap = _write_allowlist(tmp_path, allowlist)
    blocking, _ = evaluate(tmp_path, allowlist_path=ap)
    assert not any(
        r == "EMB-001" for r, _ in blocking
    ), f"false-positive pattern should suppress EMB-001, got: {blocking}"


# ---------------------------------------------------------------------------
# Live-repo posture: the live catalog must currently emit zero findings
# ---------------------------------------------------------------------------


def test_live_repo_emb001_clean() -> None:
    """The live repository currently emits zero EMB-001 blocking hits."""
    blocking, _ = evaluate(ROOT)
    emb001 = [(r, m) for r, m in blocking if r == "EMB-001"]
    assert not emb001, f"live repo has EMB-001 hits: {emb001}"


def test_live_repo_emb003_clean() -> None:
    """The live repository currently emits zero EMB-003 blocking hits."""
    blocking, _ = evaluate(ROOT)
    emb003 = [(r, m) for r, m in blocking if r == "EMB-003"]
    assert not emb003, f"live repo has EMB-003 hits: {emb003}"


# ---------------------------------------------------------------------------
# CLI: --self-test
# ---------------------------------------------------------------------------


def test_cli_self_test_passes() -> None:
    """`check_reference_embargo.py --self-test` exits 0."""
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--self-test"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert r.returncode == 0, (
        f"--self-test failed: stdout={r.stdout!r} stderr={r.stderr!r}"
    )


def test_cli_strict_clean_live() -> None:
    """`check_reference_embargo.py --strict` is clean on the live repo."""
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--strict"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert r.returncode == 0, (
        f"--strict failed: stdout={r.stdout!r} stderr={r.stderr!r}"
    )
