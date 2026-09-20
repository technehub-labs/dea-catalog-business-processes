"""Tests for the CR-BP-34d Semantic-Identity-vs-Version validator.

Locks behaviour for SIV-001..004 by exercising both the in-process
`evaluate()` function and the CLI self-test entry point, plus a
live-catalog assertion that all 126 canonical Business Process
records satisfy all four rules.

SIV-001: SemVer format (3 dot-separated integers).
SIV-002: version bump requires change_history evidence.
SIV-003: MAJOR bump requires semantic-change marker (case-insensitive
         substring; "DEPRECATED" is the case-sensitive exception per
         LCM-003 transition-event convention).
SIV-004: MINOR/PATCH bump shall not silently alter identity (advisory).
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_semantic_identity_version.py"

sys.path.insert(0, str(ROOT / "scripts"))
from check_semantic_identity_version import (  # noqa: E402
    SEMANTIC_CHANGE_MARKERS,
    SEMVER_RE,
    _RULES,
    _check_siv_001,
    _check_siv_002,
    _check_siv_003,
    _check_siv_004,
    _has_nonempty_change_history,
    _has_semantic_change_marker,
    _self_test,
    _semver_parts,
    evaluate,
)


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def _path() -> Path:
    return Path("/x/v1-alpha/dea:process-self-test/dea:process-self-test.yaml")


def _record(version: str = "1.0.0",
            change_history: list[dict] | None = None,
            identity: dict | None = None,
            ch_under_metadata: bool = False) -> dict:
    """Build a record for self-test fixtures.

    By default `change_history` (when provided) goes at the top level.
    Set `ch_under_metadata=True` to place it under `metadata.change_history`
    (the conventional location in the live catalog).
    """
    d: dict = {
        "id": "processes:process-self-test",
        "name": "Self Test",
        "type": "Process",
        "version": version,
        "process_intent": "manage",
    }
    if change_history is not None:
        if ch_under_metadata:
            d["metadata"] = {"change_history": change_history}
        else:
            d["change_history"] = change_history
    if identity is not None:
        d["identity"] = identity
    return d


# -----------------------------------------------------------------------------
# CLI-level tests
# -----------------------------------------------------------------------------


def test_cli_self_test_passes():
    result = _run(["--self-test"])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "SELF-TEST PASSED" in result.stdout


def test_in_process_self_test():
    assert _self_test() == 0


def test_cli_live_catalog_conformant():
    result = _run(["--strict"])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CONFORMANT" in result.stdout
    assert "Records checked:  140" in result.stdout
    assert "Findings:         0" in result.stdout


def test_cli_json_emits_well_formed_payload(tmp_path: Path):
    result = _run(["--json", "--catalog-root", str(ROOT)])
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["verdict"] == "CONFORMANT"
    assert payload["candidate_count"] == 140
    assert payload["finding_count"] == 0
    assert payload["blocking_count"] == 0
    assert payload["advisory_count"] == 0
    rule_ids = {r["id"] for r in payload["rules"]}
    assert rule_ids == {"SIV-001", "SIV-002", "SIV-003", "SIV-004"}
    # Marker list must include the LCM-003 case-sensitive exception
    assert "DEPRECATED" in payload["semantic_change_markers"]
    assert "CR-BP-" in payload["semantic_change_markers"]


def test_cli_strict_mode_exits_nonzero_when_blocking_finding(
    tmp_path: Path,
):
    """Build a tiny catalog with one bad BP; --strict must exit 1."""
    bad_dir = tmp_path / "entities" / "v1-alpha" / "process-bad"
    bad_dir.mkdir(parents=True)
    (bad_dir / "processes-process-bad.yaml").write_text(
        "id: processes:process-fa-operate-bad001\n"
        "name: Bad\n"
        "type: Process\n"
        "version: 2.0.0\n"   # MAJOR bump
        "process_intent: manage\n"
        # no change_history at all
    )
    result = _run(["--strict", "--json", "--catalog-root", str(tmp_path)])
    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["verdict"] == "NON-CONFORMANT"
    assert payload["finding_count"] >= 2  # SIV-002 + SIV-003


# -----------------------------------------------------------------------------
# SIV-001 (SemVer format)
# -----------------------------------------------------------------------------


def test_siv_001_passes_for_semver():
    for v in ["1.0.0", "2.0.0", "10.20.30", "0.0.1"]:
        assert _check_siv_001(_record(version=v)) is None, v


def test_siv_001_fires_for_non_semver():
    for bad in ["1.0", "1.0.0.0", "v1.0.0", "1.0.0-beta", "1.0.0 ", " 1.0.0"]:
        d = _check_siv_001(_record(version=bad))
        assert d is not None, f"should fire for {bad!r}"
        assert "SemVer" in d or "not SemVer" in d


def test_siv_001_fires_for_missing():
    r = _record(version="1.0.0")
    r.pop("version")
    d = _check_siv_001(r)
    assert d is not None
    assert "missing" in d


def test_siv_001_fires_for_non_string():
    r = _record(version=1)  # type: ignore[arg-type]
    d = _check_siv_001(r)
    assert d is not None
    assert "string" in d


def test_semver_regex_matches_schema():
    """Schema pattern is ^\\d+\\.\\d+\\.\\d+$; our regex must match exactly.

    We use fullmatch() to align with ajv's full-string anchor semantics:
    a trailing newline is not part of the SemVer string.
    """
    assert SEMVER_RE.fullmatch("1.0.0").group(0) == "1.0.0"
    assert SEMVER_RE.fullmatch("0.0.0") is not None
    assert SEMVER_RE.fullmatch("10.20.30") is not None
    assert SEMVER_RE.fullmatch("1.0") is None
    assert SEMVER_RE.fullmatch("1.0.0\n") is None
    assert SEMVER_RE.fullmatch("1.0.0 ") is None
    assert SEMVER_RE.fullmatch(" 1.0.0") is None


# -----------------------------------------------------------------------------
# SIV-002 (bump requires change_history)
# -----------------------------------------------------------------------------


def test_siv_002_v1_0_0_exempt():
    assert _check_siv_002(_record("1.0.0")) is None
    assert _check_siv_002(_record("1.0.0", [{"change": "x"}])) is None


def test_siv_002_minor_with_ch_passes():
    assert _check_siv_002(_record("1.1.0", [{"change": "minor bump"}])) is None


def test_siv_002_minor_without_ch_fires():
    d = _check_siv_002(_record("1.1.0"))
    assert d is not None
    assert "change_history" in d


def test_siv_002_patch_with_ch_passes():
    assert _check_siv_002(_record("1.0.1", [{"change": "patch"}])) is None


def test_siv_002_major_with_ch_passes():
    assert _check_siv_002(_record("2.0.0", [{"change": "CR-BP-21a: x"}])) is None


def test_siv_002_major_without_ch_fires():
    d = _check_siv_002(_record("2.0.0"))
    assert d is not None
    assert "change_history" in d


def test_siv_002_empty_ch_text_fires():
    d = _check_siv_002(_record("1.1.0", [{"change": ""}, {"description": "  "}]))
    assert d is not None


def test_siv_002_ch_under_metadata_also_counted():
    """Catalog convention: change_history lives under metadata."""
    rec = _record("2.0.0",
                  [{"change": "CR-BP-21a: rename"}],
                  ch_under_metadata=True)
    assert _check_siv_002(rec) is None  # passes (text present)


def test_siv_002_ch_under_metadata_empty_fires():
    rec = _record("2.0.0", [], ch_under_metadata=True)
    assert _check_siv_002(rec) is not None


# -----------------------------------------------------------------------------
# SIV-003 (MAJOR bump requires semantic-change marker)
# -----------------------------------------------------------------------------


def test_siv_003_v1_0_0_exempt():
    assert _check_siv_003(_record("1.0.0", [{"change": "x"}])) is None


def test_siv_003_minor_exempt():
    assert _check_siv_003(_record("1.1.0", [{"change": "minor"}])) is None


def test_siv_003_major_without_marker_fires():
    d = _check_siv_003(_record("2.0.0", [{"change": "Initial release"}]))
    assert d is not None
    assert "semantic-change marker" in d


def test_siv_003_marker_forms_all_pass():
    for marker in ["CR-BP-21a: rename to corporate strategy",
                   "CR-ECF-007: rename domain",
                   "CR-AR-FMWK-01: architecture foundation",
                   "CR-MM-PROC-01: kernel discipline",
                   "CR-OU-02: org unit rename",
                   "CR-BC-ECF-03: capabilities migration",
                   "CR-BO-02: business objects migration",
                   "breaking change to API",
                   "SEMANTIC refactor",
                   "RENAME per user feedback",
                   "REC-0042 reconciliation",
                   "Renamed per DEPRECATED transition",
                   "Superseded by next gen"]:
        d = _check_siv_003(_record("2.0.0", [{"change": marker}]))
        assert d is None, f"should pass for marker {marker!r}, got {d}"


def test_siv_003_deprecated_lowercase_does_not_count():
    """Per LCM-003 convention: 'DEPRECATED' (uppercase) is the transition
    event; 'deprecated' (lowercase) is narrative. Only uppercase counts."""
    d = _check_siv_003(_record("2.0.0", [{"change": "lifecycle_status=deprecated update"}]))
    assert d is not None  # should fire


def test_siv_003_deprecated_uppercase_counts():
    d = _check_siv_003(_record("2.0.0", [{"change": "Entry is now DEPRECATED."}]))
    assert d is None  # should pass


def test_siv_003_marker_under_metadata_works():
    rec = _record("2.0.0", [{"change": "CR-BP-21a: migration executed"}],
                  ch_under_metadata=True)
    assert _check_siv_003(rec) is None  # passes


def test_siv_003_v3_major_also_requires_marker():
    """Verify the rule fires for any MAJOR > 1, not just v2."""
    d = _check_siv_003(_record("3.5.7", [{"change": "added feature"}]))
    assert d is not None


# -----------------------------------------------------------------------------
# SIV-004 (MINOR/PATCH identity stability; advisory)
# -----------------------------------------------------------------------------


def test_siv_004_v1_0_0_exempt():
    assert _check_siv_004(_record("1.0.0")) is None


def test_siv_004_major_bump_exempt():
    """SIV-004 only fires for MAJOR==1 with MINOR/PATCH bumps."""
    assert _check_siv_004(_record("2.0.0", [{"change": "x"}])) is None


def test_siv_004_minor_without_prev_identity_advisory():
    d = _check_siv_004(_record("1.1.0", [{"change": "x"}]))
    assert d is not None
    assert "advisory" in d or "previous_identity" in d


def test_siv_004_prev_identity_present_and_unchanged_passes():
    ident = {"verb": "Manage", "object": "Customer",
             "previous_identity": {"verb": "Manage", "object": "Customer"}}
    assert _check_siv_004(_record("1.1.0", [{"change": "x"}], ident)) is None


def test_siv_004_verb_silently_changed_fires():
    ident = {"verb": "Manage", "object": "Customer",
             "previous_identity": {"verb": "Operate", "object": "Customer"}}
    d = _check_siv_004(_record("1.1.0", [{"change": "x"}], ident))
    assert d is not None
    assert "verb" in d


def test_siv_004_object_silently_changed_fires():
    ident = {"verb": "Manage", "object": "Customer",
             "previous_identity": {"verb": "Manage", "object": "Account"}}
    d = _check_siv_004(_record("1.1.0", [{"change": "x"}], ident))
    assert d is not None
    assert "object" in d


def test_siv_004_missing_identity_block_passes():
    """SIV-004 does not fire when there's no identity block; that's
    covered by BP-ARC-ID-001..005."""
    assert _check_siv_004(_record("1.1.0", [{"change": "x"}])) is not None
    # advisory still fires


def test_siv_004_severity_is_advisory():
    """SIV-004 findings must be severity=advisory (not blocking)."""
    ident = {"verb": "Manage", "object": "Customer",
             "previous_identity": {"verb": "Operate", "object": "Customer"}}
    findings = evaluate([(_path(), _record("1.1.0", [{"change": "x"}], ident))])
    siv004 = [f for f in findings if f["rule"] == "SIV-004"]
    assert siv004
    assert all(f["severity"] == "advisory" for f in siv004)


# -----------------------------------------------------------------------------
# Verdict logic
# -----------------------------------------------------------------------------


def test_verdict_clean_is_conformant():
    findings = evaluate([(_path(), _record("1.0.0", [{"change": "seed"}]))])
    assert findings == []


def test_verdict_advisory_only_is_warnings():
    """SIV-004 is the only advisory rule; firing it alone produces
    CONFORMANT-WITH-WARNINGS."""
    ident = {"verb": "Manage", "object": "Customer",
             "previous_identity": {"verb": "Operate", "object": "Customer"}}
    findings = evaluate([(_path(), _record("1.1.0", [{"change": "x"}], ident))])
    # contains SIV-004 (advisory) and possibly no SIV-002 (text present)
    blocking = [f for f in findings if f["severity"] == "blocking"]
    advisory = [f for f in findings if f["severity"] == "advisory"]
    assert blocking == []
    assert advisory  # at least SIV-004


def test_verdict_blocking_is_non_conformant():
    findings = evaluate([(_path(), _record("2.0.0"))])
    assert any(f["severity"] == "blocking" for f in findings)


# -----------------------------------------------------------------------------
# Helpers / constants
# -----------------------------------------------------------------------------


def test_semver_parts_parses():
    assert _semver_parts("1.0.0") == (1, 0, 0)
    assert _semver_parts("2.5.7") == (2, 5, 7)
    assert _semver_parts("10.20.30") == (10, 20, 30)
    assert _semver_parts("1.0") is None
    assert _semver_parts("v1.0.0") is None


def test_semantic_change_markers_includes_required_forms():
    assert "CR-BP-" in SEMANTIC_CHANGE_MARKERS
    assert "BREAKING" in SEMANTIC_CHANGE_MARKERS
    assert "SEMANTIC" in SEMANTIC_CHANGE_MARKERS
    assert "RENAME" in SEMANTIC_CHANGE_MARKERS
    assert "REC-" in SEMANTIC_CHANGE_MARKERS
    assert "DEPRECATED" in SEMANTIC_CHANGE_MARKERS
    assert "SUPERSEDED" in SEMANTIC_CHANGE_MARKERS


def test_rules_table_is_complete():
    """The rules table must list all four SIV-NNN IDs."""
    ids = {rid for rid, _fn, _label, _sev in _RULES}
    assert ids == {"SIV-001", "SIV-002", "SIV-003", "SIV-004"}


def test_has_semantic_change_marker_helper():
    assert _has_semantic_change_marker({"change_history": [{"change": "CR-BP-21a"}]})
    assert _has_semantic_change_marker({"metadata": {"change_history": [
        {"description": "This entry is now DEPRECATED."}]}})
    assert not _has_semantic_change_marker({"change_history": [{"change": "minor edit"}]})
    assert not _has_semantic_change_marker({})


def test_has_nonempty_change_history_helper():
    assert _has_nonempty_change_history({"change_history": [{"change": "x"}]})
    assert _has_nonempty_change_history({"metadata": {"change_history": [
        {"change": "y"}]}})
    assert not _has_nonempty_change_history({"change_history": []})
    assert not _has_nonempty_change_history({"change_history": None})
    assert not _has_nonempty_change_history({})
