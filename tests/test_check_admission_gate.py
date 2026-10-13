"""Tests for scripts/check_admission_gate.py (ADM-001 marker mechanism).

Locks behaviour for the CR-BP-115 admission-authority marker:
the _ADMISSION_CR_RE regex allowlist is replaced by a data-driven
marker carried in the CR files themselves.

Authoritative reference: CR-BP-115 (2026-10-13, eaojnr).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_admission_gate.py"

sys.path.insert(0, str(ROOT / "scripts"))
from check_admission_gate import (  # noqa: E402
    _BARE_CR_ID,
    _load_admission_authorities,
    _MARKER_RE,
)

MANIFEST = sorted([
    "CR-BP-03C", "CR-BP-101", "CR-BP-101a", "CR-BP-106", "CR-BP-111",
    "CR-BP-13", "CR-BP-13a", "CR-BP-13b", "CR-BP-19", "CR-BP-20",
    "CR-BP-21a", "CR-BP-21a.1", "CR-BP-21b", "CR-BP-21b.1",
    "CR-BP-21c", "CR-BP-21c.1", "CR-BP-21d", "CR-BP-21d.1",
    "CR-BP-21e", "CR-BP-21e.1", "CR-BP-21f.1", "CR-BP-64", "CR-BP-65",
    "CR-BP-66", "CR-BP-67", "CR-BP-71", "CR-BP-73", "CR-BP-75",
    "CR-BP-78", "CR-BP-81", "CR-BP-82", "CR-BP-83", "CR-BP-86",
])


# ---------------------------------------------------------------------------
# Marker regex
# ---------------------------------------------------------------------------


class TestMarkerRegex:
    def test_matches_yes(self):
        m = _MARKER_RE.match("**Admission authority**: yes")
        assert m is not None
        assert m.group(1).split("(")[0].strip().lower() == "yes"

    def test_matches_yes_with_qualifier(self):
        m = _MARKER_RE.match(
            "**Admission authority**: yes (L2 admission tranche)"
        )
        assert m is not None
        assert m.group(1).split("(")[0].strip().lower() == "yes"

    def test_ignores_yes_ish(self):
        m = _MARKER_RE.match("**Admission authority**: yes-ish")
        assert m is not None
        assert m.group(1).split("(")[0].strip().lower() != "yes"

    def test_ignores_no(self):
        m = _MARKER_RE.match("**Admission authority**: no")
        assert m is not None
        assert m.group(1).split("(")[0].strip().lower() != "yes"

    def test_ignores_indented(self):
        assert _MARKER_RE.match("    **Admission authority**: yes") is None

    def test_ignores_body_text(self):
        assert _MARKER_RE.match(
            "some text **Admission authority**: yes more text"
        ) is None


# ---------------------------------------------------------------------------
# Bare CR id derivation
# ---------------------------------------------------------------------------


class TestBareCrId:
    @pytest.mark.parametrize("stem,expected", [
        ("CR-BP-115-admission-authority-marker", "CR-BP-115"),
        ("CR-BP-13a-party-and-relationship-admission", "CR-BP-13a"),
        ("CR-BP-21a.1-strategy-direction-completion", "CR-BP-21a.1"),
        ("CR-BP-03C-sample-process-contribution", "CR-BP-03C"),
        ("CR-BP-101a-sd-retire-activity-decomposition", "CR-BP-101a"),
        ("CR-BP-L4-02-pr-domain-content-enrichment", "CR-BP-L4-02"),
        ("CR-BP-mv1-entity-storage-and-id-system-migration", "CR-BP-mv1"),
        ("CR-CATALOG-STRUCT-02", "CR-CATALOG-STRUCT-02"),
        ("CR-ECF-CG-004", "CR-ECF-CG-004"),
        ("CR-BP-02", "CR-BP-02"),
        ("CR-BP-13-research-ratification", "CR-BP-13"),
    ])
    def test_derivation(self, stem, expected):
        m = _BARE_CR_ID.match(stem)
        assert m is not None, f"no match for {stem}"
        assert m.group(1) == expected


# ---------------------------------------------------------------------------
# Authority loading (fixture tree)
# ---------------------------------------------------------------------------


class TestLoadAdmissionAuthorities:
    def test_marked_cr_admits(self, tmp_path):
        cr_dir = tmp_path / "change-requests"
        cr_dir.mkdir()
        (cr_dir / "CR-BP-99-test-admission.md").write_text(
            "**Status**: Accepted\n**Admission authority**: yes\n"
        )
        auths = _load_admission_authorities(tmp_path)
        assert "CR-BP-99" in auths

    def test_unmarked_cr_rejected(self, tmp_path):
        cr_dir = tmp_path / "change-requests"
        cr_dir.mkdir()
        (cr_dir / "CR-BP-99-test-no-marker.md").write_text(
            "**Status**: Accepted\n"
        )
        auths = _load_admission_authorities(tmp_path)
        assert "CR-BP-99" not in auths

    def test_malformed_marker_ignored(self, tmp_path):
        cr_dir = tmp_path / "change-requests"
        cr_dir.mkdir()
        (cr_dir / "CR-BP-99-test-malformed.md").write_text(
            "**Status**: Accepted\n**Admission authority**: yes-ish\n"
        )
        auths = _load_admission_authorities(tmp_path)
        assert "CR-BP-99" not in auths

    def test_missing_dir_returns_empty(self, tmp_path):
        auths = _load_admission_authorities(tmp_path)
        assert auths == frozenset()


# ---------------------------------------------------------------------------
# Live repo: backfill manifest equality
# ---------------------------------------------------------------------------


def test_live_authorities_match_manifest():
    """The live change-requests/ tree yields exactly the 33 manifest ids."""
    auths = _load_admission_authorities(ROOT)
    assert sorted(auths) == MANIFEST, (
        f"live authorities {sorted(auths)} != manifest {MANIFEST}"
    )


def test_live_no_cr_bp_115_in_authorities():
    """CR-BP-115 defines the marker but does not declare it."""
    auths = _load_admission_authorities(ROOT)
    assert "CR-BP-115" not in auths


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_self_test_passes():
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--self-test"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert r.returncode == 0, (
        f"--self-test failed: stdout={r.stdout!r} stderr={r.stderr!r}"
    )


def test_cli_strict_provenance_conformant():
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--strict-provenance"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert r.returncode == 0, (
        f"--strict-provenance failed: {r.stdout[-300:]!r}"
    )


def test_cli_json_has_admission_authorities():
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "--json"],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    assert r.returncode == 0
    import json
    payload = json.loads(r.stdout)
    assert "admission_authorities" in payload
    assert len(payload["admission_authorities"]) == 33
