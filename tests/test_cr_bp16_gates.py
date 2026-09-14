"""Tests for the CR metadata validator (CR-BP-16 S16; CR-META-001..006),
documentation conformance checker (CR-BP-16 S22; DOC-001..003),
and admission gate (CR-BP-16 S15; ADM-001..008).
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT_CR_META = ROOT / "scripts" / "check_cr_metadata.py"
SCRIPT_DOC = ROOT / "scripts" / "check_documentation_conformance.py"
SCRIPT_ADM = ROOT / "scripts" / "check_admission_gate.py"


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *args], capture_output=True, text=True, cwd=str(ROOT),
    )


# CR metadata


def test_cr_meta_self_test_passes():
    r = _run([str(SCRIPT_CR_META), "--self-test"])
    assert r.returncode == 0, r.stdout + r.stderr
    assert "self-test PASS" in r.stdout


def test_cr_meta_runs_advisory_on_live():
    """Live run is advisory (returns 0) and surfaces findings for
    legacy CRs without S21 metadata."""
    r = _run([str(SCRIPT_CR_META)])
    assert r.returncode == 0, r.stdout + r.stderr
    # CR-BP-13A is the §21 reference and should not appear in findings.
    assert "CR-BP-13a" not in r.stdout or "0 findings" in r.stdout


def test_cr_meta_strict_passes_when_no_new_failures():
    """--strict returns 0 when no NEW CR (mtime >= cutoff) fails."""
    r = _run([str(SCRIPT_CR_META), "--strict"])
    # After PR-13, all touched-in-this-session CRs have S21 metadata
    # and pass. Legacy CRs are advisory. So returncode MUST be 0.
    assert r.returncode == 0, r.stdout + r.stderr
    # The verdict should be ADVISORY-LEGACY or CONFORMANT
    assert any(s in r.stdout for s in ("ADVISORY-LEGACY", "CONFORMANT"))


def test_cr_meta_strict_fails_on_new_bad_fixture(tmp_path):
    """A new CR file (touch -d "now") without S21 metadata must
    fail --strict."""
    import os
    from datetime import datetime, timezone
    sandbox = tmp_path / "sandbox"
    cr_dir = sandbox / "change-requests"
    cr_dir.mkdir(parents=True)
    bad = (
        "# CR-BP-XX-bad\n\n"
        "Some prose, no metadata.\n"
    )
    p = cr_dir / "CR-XX-bad.md"
    p.write_text(bad)
    # Set mtime to 2099-01-01 to ensure the file is "new" by the cutoff
    future = datetime(2099, 1, 1, tzinfo=timezone.utc).timestamp()
    os.utime(p, (future, future))
    r = _run([str(SCRIPT_CR_META), "--strict", "--catalog-root", str(sandbox)])
    assert r.returncode != 0, r.stdout + r.stderr
    assert "NON-CONFORMANT" in r.stdout


def test_cr_meta_strict_passes_on_legacy_bad_fixture(tmp_path):
    """A legacy CR file (mtime < cutoff) without S21 metadata must
    pass --strict (advisory only)."""
    import os
    from datetime import datetime, timezone
    sandbox = tmp_path / "sandbox"
    cr_dir = sandbox / "change-requests"
    cr_dir.mkdir(parents=True)
    bad = (
        "# CR-BP-YY-bad\n\n"
        "Some prose, no metadata.\n"
    )
    p = cr_dir / "CR-YY-bad.md"
    p.write_text(bad)
    # Set mtime to 2000-01-01 (way before any cutoff)
    past = datetime(2000, 1, 1, tzinfo=timezone.utc).timestamp()
    os.utime(p, (past, past))
    r = _run([str(SCRIPT_CR_META), "--strict", "--catalog-root", str(sandbox)])
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ADVISORY-LEGACY" in r.stdout


def test_cr_meta_accepts_layer_with_parenthetical_qualifier():
    """`L1 (Process Catalog)` MUST be accepted as a valid Layer."""
    r = _run([str(SCRIPT_CR_META), "--json"])
    import json
    data = json.loads(r.stdout)
    # CR-BP-13A uses L1 (Process Catalog). Should NOT have CR-META-002.
    rule_002_new = [f for f in data["new_findings"]
                    if f["rule"] == "CR-META-002" and "13a" in f["path"]]
    assert not rule_002_new, (
        "Layer 'L1 (Process Catalog)' should be accepted (normalized to L1)"
    )


def test_cr_meta_accepts_status_with_date_qualifier():
    """`Proposed (2026-09-03)` MUST be accepted as a valid Status."""
    r = _run([str(SCRIPT_CR_META), "--json"])
    import json
    data = json.loads(r.stdout)
    # CR-BP-03C uses Proposed (2026-09-03). Should NOT have CR-META-001
    # due to status (only due to legacy or some other rule).
    rule_001_new = [f for f in data["new_findings"]
                    if f["rule"] == "CR-META-001" and "03C" in f["path"]]
    assert not rule_001_new, (
        "Status 'Proposed (2026-09-03)' should be accepted "
        "(normalized to Proposed)"
    )


def test_cr_meta_json_shape():
    r = _run([str(SCRIPT_CR_META), "--json"])
    assert r.returncode == 0, r.stdout + r.stderr
    import json
    data = json.loads(r.stdout)
    assert "verdict" in data
    assert "findings" in data


def test_cr_meta_detects_missing_metadata(tmp_path):
    """A bad CR fixture triggers CR-META-001..004 + 006."""
    sandbox = tmp_path / "sandbox"
    sandbox.mkdir()
    cr_dir = sandbox / "change-requests"
    cr_dir.mkdir()
    bad = (
        "# CR-BP-XX-bad\n\n"
        "**Layer**: L99\n"
        "**Owner**: \n"
        "**Depends on**: nothing here\n"
    )
    (cr_dir / "CR-XX-bad.md").write_text(bad)
    r = _run([str(SCRIPT_CR_META), "--catalog-root", str(sandbox), "--json"])
    import json
    data = json.loads(r.stdout)
    rules = {f["rule"] for f in data["findings"]}
    for code in ("CR-META-001", "CR-META-002", "CR-META-003", "CR-META-004", "CR-META-006"):
        assert code in rules, f"expected {code} to fire"


# Documentation conformance


def test_doc_self_test_passes():
    r = _run([str(SCRIPT_DOC), "--self-test"])
    assert r.returncode == 0, r.stdout + r.stderr
    assert "self-test PASS" in r.stdout


def test_doc_runs_on_live():
    r = _run([str(SCRIPT_DOC)])
    assert r.returncode == 0, r.stdout + r.stderr


def test_doc_json_shape():
    r = _run([str(SCRIPT_DOC), "--json"])
    import json
    data = json.loads(r.stdout)
    assert "verdict" in data
    assert "findings" in data


# Admission gate


def test_adm_self_test_passes():
    r = _run([str(SCRIPT_ADM), "--self-test"])
    assert r.returncode == 0, r.stdout + r.stderr
    assert "self-test PASS" in r.stdout


def test_adm_live_runs_against_locked_records():
    """On the locked population, all 18 canonical BPs are checked.
    Some legacy fields (triggers, outcomes) MAY produce findings;
    that's expected (advisory mode)."""
    r = _run([str(SCRIPT_ADM)])
    assert r.returncode == 0, r.stdout + r.stderr


def test_adm_strict_fails_on_bad_fixture(tmp_path):
    """A candidate with missing required fields MUST fail --strict."""
    sandbox = tmp_path / "sandbox"
    shutil.copytree(ROOT / "entities", sandbox / "entities")
    shutil.copytree(ROOT / "contexts", sandbox / "contexts")
    bad_dir = sandbox / "entities" / "v1-alpha" / "dea:process-bad-candidate"
    bad_dir.mkdir()
    (bad_dir / "dea:process-bad-candidate.yaml").write_text(
        "id: dea:process-bad-candidate\n"
        "name: Bad\n"
        "type: Process\n"
        "version: '1.0.0'\n"
        "process_intent: harmonise\n"  # bad intent
        "process_type: core\n"
        "context: [{ref: dea:pc-unknown}]\n"  # unresolved
        "change_history: []\n"  # empty
    )
    r = _run([str(SCRIPT_ADM), "--strict", "--catalog-root", str(sandbox)])
    assert r.returncode != 0, r.stdout + r.stderr
    assert "ADM-003" in r.stdout or "ADM-006" in r.stdout or "ADM-008" in r.stdout


def test_adm_json_shape():
    r = _run([str(SCRIPT_ADM), "--json"])
    import json
    data = json.loads(r.stdout)
    assert "verdict" in data
    assert "findings" in data
    assert "candidate_count" in data
    assert data["candidate_count"] == 129  # 129 canonical BPs (119 + 7 CR-BP-21f.1 + 2 CR-BP-64 + 1 CR-BP-65 admissions)


# CR-BP-16 §17 Step 8: provenance blocking policy
# (--strict-provenance flag and metadata.change_history path).


def test_adm_strict_provenance_passes_on_locked_population():
    """The 18 LOCKED records all carry proper metadata.change_history
    with a CR-BP-13* or CR-BP-03C admission reference. --strict-provenance
    MUST therefore return CONFORMANT-WITH-WARNINGS (zero blocking
    findings). Exit code 0."""
    r = _run([str(SCRIPT_ADM), "--strict-provenance"])
    assert r.returncode == 0, r.stdout + r.stderr
    assert "NON-CONFORMANT" not in r.stdout
    # No provenance-specific FINDINGS should appear. The header
    # always contains 'ADM-001..008', so we match the per-finding
    # '[ADM-NNN]' marker:
    assert "[ADM-008]" not in r.stdout
    assert "[ADM-001]" not in r.stdout
    # Boundary (ADM-005) findings are advisory and expected to remain:
    assert "CONFORMANT-WITH-WARNINGS" in r.stdout


def test_adm_strict_provenance_blocks_missing_provenance(tmp_path):
    """A record whose metadata.change_history is missing MUST fail
    --strict-provenance on ADM-008. ADM-001 only fires when
    change_history is present but lacks an admission CR (covered
    by the no-admission-cr test below)."""
    import json
    sandbox = tmp_path / "sandbox"
    shutil.copytree(ROOT / "entities", sandbox / "entities")
    shutil.copytree(ROOT / "contexts", sandbox / "contexts")
    bad_dir = sandbox / "entities" / "v1-alpha" / "dea:process-no-provenance"
    bad_dir.mkdir()
    (bad_dir / "dea:process-no-provenance.yaml").write_text(
        "id: dea:process-no-provenance\n"
        "name: No Provenance\n"
        "type: Process\n"
        "version: '1.0.0'\n"
        "process_intent: manage\n"
        "process_type: core\n"
        "context: [{ref: dea:pc-pr-op}]\n"
        # NOTE: no change_history; no metadata.change_history.
        # This MUST trigger ADM-008 (provenance missing).
    )
    r = _run([str(SCRIPT_ADM), "--strict-provenance", "--json",
              "--catalog-root", str(sandbox)])
    assert r.returncode != 0, r.stdout + r.stderr
    data = json.loads(r.stdout)
    rules = [f["rule"] for f in data["findings"]
             if "dea:process-no-provenance" in f["path"]]
    assert "ADM-008" in rules
    # Provenance rules are the BLOCKING ones; boundary findings remain advisory.
    blocking_rules = {f["rule"] for f in data["blocking_findings"]}
    assert "ADM-008" in blocking_rules


def test_adm_strict_provenance_blocks_no_admission_cr(tmp_path):
    """A record whose change_history has only non-admission CRs
    (e.g. CR-BP-15-IMP migration entries but no CR-BP-13* /
    CR-BP-03C reference) MUST fail --strict-provenance on ADM-001
    only (the entry is structurally fine for ADM-008)."""
    import json
    sandbox = tmp_path / "sandbox"
    shutil.copytree(ROOT / "entities", sandbox / "entities")
    shutil.copytree(ROOT / "contexts", sandbox / "contexts")
    bad_dir = sandbox / "entities" / "v1-alpha" / "dea:process-no-admission-cr"
    bad_dir.mkdir()
    (bad_dir / "dea:process-no-admission-cr.yaml").write_text(
        "id: dea:process-no-admission-cr\n"
        "name: No Admission CR\n"
        "type: Process\n"
        "version: '1.0.0'\n"
        "process_intent: manage\n"
        "process_type: core\n"
        "context: [{ref: dea:pc-pr-op}]\n"
        "metadata:\n"
        "  change_history:\n"
        "    - cr: CR-BP-15-IMP\n"
        "      date: '2026-09-06'\n"
        "      change: Phase 5 migration only; never admitted.\n"
    )
    r = _run([str(SCRIPT_ADM), "--strict-provenance", "--json",
              "--catalog-root", str(sandbox)])
    assert r.returncode != 0, r.stdout + r.stderr
    data = json.loads(r.stdout)
    target_rules = [f["rule"] for f in data["findings"]
                    if "dea:process-no-admission-cr" in f["path"]]
    blocking_target_rules = [f["rule"] for f in data["blocking_findings"]
                             if "dea:process-no-admission-cr" in f["path"]]
    # ADM-001 fires (no admission CR); ADM-008 does NOT fire
    # (the entry is structurally valid).
    assert "ADM-001" in target_rules
    assert "ADM-001" in blocking_target_rules
    assert "ADM-008" not in target_rules
    assert "ADM-008" not in blocking_target_rules


def test_adm_strict_provenance_accepts_cr_bp_03c_as_admission(tmp_path):
    """CR-BP-03C is the canonical sample-process-contribution CR.
    It predates the formal CR-BP-13 admission programme but is
    functionally equivalent for ADM-001 (it admitted the first
    canonical sample process). A record whose change_history
    references ONLY CR-BP-03C MUST pass --strict-provenance."""
    import json
    sandbox = tmp_path / "sandbox"
    shutil.copytree(ROOT / "entities", sandbox / "entities")
    shutil.copytree(ROOT / "contexts", sandbox / "contexts")
    ok_dir = sandbox / "entities" / "v1-alpha" / "dea:process-via-03c"
    ok_dir.mkdir()
    (ok_dir / "dea:process-via-03c.yaml").write_text(
        "id: dea:process-via-03c\n"
        "name: Via 03C\n"
        "type: Process\n"
        "version: '1.0.0'\n"
        "process_intent: manage\n"
        "process_type: core\n"
        "context: [{ref: dea:pc-pr-op}]\n"
        "metadata:\n"
        "  change_history:\n"
        "    - cr: CR-BP-03C\n"
        "      date: '2026-09-03'\n"
        "      change: Sample-process-contribution admission.\n"
    )
    r = _run([str(SCRIPT_ADM), "--strict-provenance", "--json",
              "--catalog-root", str(sandbox)])
    data = json.loads(r.stdout)
    target_rules = [f["rule"] for f in data["findings"]
                    if "dea:process-via-03c" in f["path"]]
    # CR-BP-03C is accepted: no ADM-001 finding; no ADM-008 finding.
    assert "ADM-001" not in target_rules, r.stdout
    assert "ADM-008" not in target_rules, r.stdout


def test_adm_reads_change_history_from_metadata_block(tmp_path):
    """Regression test: the validator previously queried
    top-level `change_history`, missing records that stored
    their provenance under `metadata.change_history`. All 18
    LOCKED records use the canonical metadata path; the
    validator MUST read it."""
    sandbox = tmp_path / "sandbox"
    shutil.copytree(ROOT / "entities", sandbox / "entities")
    shutil.copytree(ROOT / "contexts", sandbox / "contexts")
    r = _run([str(SCRIPT_ADM), "--strict-provenance",
              "--catalog-root", str(sandbox)])
    # No ADM-008 firing on any of the 18 LOCKED records:
    assert "[ADM-008]" not in r.stdout, r.stdout
    # And no ADM-001 firing either (every record has CR-BP-13a/b
    # or CR-BP-03C in change_history):
    assert "[ADM-001]" not in r.stdout, r.stdout