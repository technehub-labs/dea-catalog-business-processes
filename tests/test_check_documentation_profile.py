"""Tests for the CR-BP-94-EXT-01 Documentation Profile validator.

Locks behaviour for DOC-001..005 by exercising both the in-process
`evaluate()` function and the CLI self-test entry point, plus the live
catalog assertion that DOC-001..005 emit advisory findings (the
existing 294 README assets are introductory; expanded README assets
land in EXT-02 / EXT-06).
"""

import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_documentation_profile.py"

sys.path.insert(0, str(ROOT / "scripts"))
from check_documentation_profile import (  # noqa: E402
    EXPECTED_HEADINGS,
    LEVEL_BY_TYPE,
    PROFILE_REGISTRY,
    _governing_cr,
    _readme_references_cr,
    _readme_references_id,
    _resolve_level,
    _resolve_profile,
    evaluate,
)


# -----------------------------------------------------------------------------
# Profile registry sanity
# -----------------------------------------------------------------------------


def test_profile_registry_has_five_entries() -> None:
    """CR-BP-94-EXT-01a: registry now covers L0/L1/L2/L3/L4 (was L2/L3/L4 in EXT-01)."""
    assert set(PROFILE_REGISTRY.keys()) == {
        ("ProcessContext", "L0"),
        ("ProcessGroup", "L1"),
        ("Process", "L2"),
        ("Activity", "L3"),
        ("Task", "L4"),
    }


def test_l0_profile_resolves_for_processcontext_record() -> None:
    record = {"type": "ProcessContext"}
    profile = _resolve_profile(record)
    assert profile is not None
    assert profile["profile_id"] == "dea:profile-readme-l0-process-context-v1"


def test_l1_profile_resolves_for_processgroup_record() -> None:
    record = {"type": "ProcessGroup"}
    profile = _resolve_profile(record)
    assert profile is not None
    assert profile["profile_id"] == "dea:profile-readme-l1-process-group-v1"


def test_l0_profile_required_sections() -> None:
    """L0 ProcessContext profile: 11 required sections; outcomes is conditional."""
    profile = PROFILE_REGISTRY[("ProcessContext", "L0")]
    required = profile["required_section_ids"]
    assert len(required) == 11
    assert "outcomes" not in required
    for sec in ("entity-identity", "formal-definition", "semantic-dimensions",
                "decomposition", "behavior", "interfaces", "roles",
                "rules-controls", "evidence", "completeness", "revision-history"):
        assert sec in required, sec


def test_l1_profile_required_sections() -> None:
    """L1 ProcessGroup profile: 11 required sections; outcomes is conditional."""
    profile = PROFILE_REGISTRY[("ProcessGroup", "L1")]
    required = profile["required_section_ids"]
    assert len(required) == 11
    assert "outcomes" not in required
    for sec in ("entity-identity", "formal-definition", "semantic-dimensions",
                "decomposition", "behavior", "interfaces", "roles",
                "rules-controls", "evidence", "completeness", "revision-history"):
        assert sec in required, sec


def test_profile_resolves_for_process_record() -> None:
    record = {"type": "Process"}
    profile = _resolve_profile(record)
    assert profile is not None
    assert profile["profile_id"] == "dea:profile-readme-l2-process-v1"


def test_profile_resolves_for_activity_record() -> None:
    record = {"type": "Activity"}
    profile = _resolve_profile(record)
    assert profile is not None
    assert profile["profile_id"] == "dea:profile-readme-l3-activity-v1"


def test_profile_unresolved_for_unknown_type() -> None:
    """A type not in the registry returns None (DOC-002 will fire)."""
    assert _resolve_profile({"type": "Unknown"}) is None


def test_resolve_level_by_type() -> None:
    # CR-BP-94-EXT-01a: cardinal entities L0/L1 added to LEVEL_BY_TYPE.
    assert _resolve_level({"type": "ProcessContext"}) == "L0"
    assert _resolve_level({"type": "ProcessGroup"}) == "L1"
    assert _resolve_level({"type": "Process"}) == "L2"
    assert _resolve_level({"type": "Activity"}) == "L3"
    assert _resolve_level({"type": "Task"}) == "L4"
    assert _resolve_level({"type": "Unknown"}) is None
    assert _resolve_level({}) is None


def test_l2_profile_required_sections_complete() -> None:
    """L2 profile lists all 12 standard sections per the architecture doc."""
    profile = PROFILE_REGISTRY[("Process", "L2")]
    required = profile["required_section_ids"]
    assert len(required) == 12
    assert "entity-identity" in required
    assert "formal-definition" in required
    assert "semantic-dimensions" in required
    assert "decomposition" in required
    assert "behavior" in required
    assert "interfaces" in required
    assert "roles" in required
    assert "rules-controls" in required
    assert "outcomes" in required
    assert "evidence" in required
    assert "completeness" in required
    assert "revision-history" in required


def test_l3_profile_treats_outcomes_as_conditional() -> None:
    """L3 profile: outcomes is conditional (Activity doesn't own metrics).

    The profile registry (PROFILE_REGISTRY) lists `outcomes` in
    required_section_ids for L2 because the L2 BP profile has it
    mandatory. The L3 profile lists outcomes NOT in the required
    sections (the validator's DOC-002 check skips it), but the
    `outcomes` section is still authored as a conditional /
    not_applicable section per the L3 profile template.
    """
    profile = PROFILE_REGISTRY[("Activity", "L3")]
    required = profile["required_section_ids"]
    # L3 profile does NOT require outcomes (it's conditional at L3).
    assert "outcomes" not in required
    # L3 still requires all 11 other sections.
    assert len(required) == 11
    for sec in ("entity-identity", "formal-definition", "semantic-dimensions",
                "decomposition", "behavior", "interfaces", "roles",
                "rules-controls", "evidence", "completeness", "revision-history"):
        assert sec in required, sec


def test_l4_profile_treats_outcomes_as_not_applicable() -> None:
    """L4 profile: outcomes is not_applicable (Tasks don't own metrics)."""
    profile = PROFILE_REGISTRY[("Task", "L4")]
    required = profile["required_section_ids"]
    assert "outcomes" not in required
    assert len(required) == 11


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def _record(id_="processes:process-self-test", name="Self Test",
            type_="Process", governing_cr="CR-BP-13a",
            lifecycle_status="candidate"):
    return {
        "id": id_,
        "name": name,
        "type": type_,
        "version": "1.0.0",
        "lifecycle_status": lifecycle_status,
        "metadata": {"established_by": governing_cr},
    }


def _readme(entity_id="processes:process-self-test", cr="CR-BP-13a",
            include_all_sections=True):
    body = [f"# Canonical Business Process: `{entity_id}`", ""]
    body.append(f"Governed by {cr}.")
    body.append("")
    if include_all_sections:
        for i, sid in enumerate([
            "Entity Identity and Classification",
            "Formal Definition and Scope",
            "Canonical Semantic Dimensions",
            "Decomposition and Composition",
            "Behavior and Workflow",
            "Inputs, Outputs, and Interfaces",
            "Roles, Responsibilities, and Accountability",
            "Business Rules and Controls",
            "Outcomes and Performance",
            "Evidence and Traceability",
            "Documentation Completeness",
            "Revision History",
        ], start=1):
            body.append(f"## {i}. {sid}")
            body.append("")
    return "\n".join(body)


def _run(args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, check=False,
    )


# -----------------------------------------------------------------------------
# DOC-001: README exists
# -----------------------------------------------------------------------------


def test_doc_001_readme_missing(tmp_path):
    """A record with no README.md emits DOC-001."""
    d = tmp_path / "processes:process-x"
    d.mkdir()
    (d / "processes:process-x.yaml").write_text(yaml.safe_dump(_record(id_="processes:process-x")))
    f = evaluate([(d / "processes:process-x.yaml", _record(id_="processes:process-x"))])
    assert any(fnd["rule"] == "DOC-001" and fnd["advisory"] for fnd in f), f


def test_doc_001_readme_present_no_finding(tmp_path):
    """A record with a well-formed README emits no DOC-001 finding."""
    d = tmp_path / "processes:process-x"
    d.mkdir()
    (d / "processes:process-x.yaml").write_text(yaml.safe_dump(_record(id_="processes:process-x")))
    (d / "README.md").write_text(_readme("processes:process-x"))
    f = evaluate([(d / "processes:process-x.yaml", _record(id_="processes:process-x"))])
    assert not any(fnd["rule"] == "DOC-001" for fnd in f), f


# -----------------------------------------------------------------------------
# DOC-002: Required section identifiers present
# -----------------------------------------------------------------------------


def test_doc_002_missing_section(tmp_path):
    """A record with a README missing required sections emits DOC-002."""
    d = tmp_path / "processes:process-y"
    d.mkdir()
    (d / "processes:process-y.yaml").write_text(yaml.safe_dump(_record(id_="processes:process-y")))
    (d / "README.md").write_text("# Canonical Business Process: `dea:process-y`\n\n## 1. Entity Identity and Classification\n")
    f = evaluate([(d / "processes:process-y.yaml", _record(id_="processes:process-y"))])
    missing = [fnd for fnd in f if fnd["rule"] == "DOC-002" and fnd["record_id"] == "processes:process-y"]
    assert missing, f
    # Should be missing at least 11 of the 12 required sections.
    assert len(missing) >= 11, f"expected many DOC-002 findings, got {len(missing)}"


def test_doc_002_full_readme_passes(tmp_path):
    """A record with a fully-populated README emits no DOC-002 finding."""
    d = tmp_path / "processes:process-z"
    d.mkdir()
    (d / "processes:process-z.yaml").write_text(yaml.safe_dump(_record(id_="processes:process-z")))
    (d / "README.md").write_text(_readme("processes:process-z"))
    f = evaluate([(d / "processes:process-z.yaml", _record(id_="processes:process-z"))])
    assert not any(fnd["rule"] == "DOC-002" for fnd in f), f


# -----------------------------------------------------------------------------
# DOC-003: README entity id matches YAML
# -----------------------------------------------------------------------------


def test_doc_003_id_mismatch(tmp_path):
    """README's H1 doesn't reference the YAML id -> DOC-003 fires."""
    d = tmp_path / "processes:process-q"
    d.mkdir()
    (d / "processes:process-q.yaml").write_text(yaml.safe_dump(_record(id_="processes:process-q")))
    (d / "README.md").write_text("# Canonical Business Process: `dea:process-other`\n\n" + _readme("processes:process-other")[200:])
    f = evaluate([(d / "processes:process-q.yaml", _record(id_="processes:process-q"))])
    assert any(fnd["rule"] == "DOC-003" for fnd in f), f


def test_doc_003_id_match(tmp_path):
    """README's H1 references the YAML id -> no DOC-003 finding."""
    d = tmp_path / "processes:process-r"
    d.mkdir()
    (d / "processes:process-r.yaml").write_text(yaml.safe_dump(_record(id_="processes:process-r")))
    (d / "README.md").write_text(_readme("processes:process-r"))
    f = evaluate([(d / "processes:process-r.yaml", _record(id_="processes:process-r"))])
    assert not any(fnd["rule"] == "DOC-003" for fnd in f), f


# -----------------------------------------------------------------------------
# DOC-004: No unresolved placeholders at validated lifecycle
# -----------------------------------------------------------------------------


def test_doc_004_placeholder_at_validated_lifecycle(tmp_path):
    """Placeholder at validated lifecycle -> DOC-004 fires."""
    d = tmp_path / "processes:process-s"
    d.mkdir()
    (d / "processes:process-s.yaml").write_text(yaml.safe_dump(_record(id_="processes:process-s", lifecycle_status="active")))
    (d / "README.md").write_text(_readme("processes:process-s").replace("## 1.", "## 1. {{section_name}}\n\n## 1.", 1))
    f = evaluate([(d / "processes:process-s.yaml", _record(id_="processes:process-s", lifecycle_status="active"))])
    assert any(fnd["rule"] == "DOC-004" for fnd in f), f


def test_doc_004_placeholder_at_candidate_allowed(tmp_path):
    """Placeholder at candidate lifecycle does NOT fire DOC-004 (EXT-04 promotes)."""
    d = tmp_path / "processes:process-t"
    d.mkdir()
    (d / "processes:process-t.yaml").write_text(yaml.safe_dump(_record(id_="processes:process-t", lifecycle_status="candidate")))
    (d / "README.md").write_text(_readme("processes:process-t").replace("## 1.", "## 1. {{section_name}}\n\n## 1.", 1))
    f = evaluate([(d / "processes:process-t.yaml", _record(id_="processes:process-t", lifecycle_status="candidate"))])
    assert not any(fnd["rule"] == "DOC-004" for fnd in f), f


# -----------------------------------------------------------------------------
# DOC-005: Governing CR referenced
# -----------------------------------------------------------------------------


def test_doc_005_cr_referenced(tmp_path):
    """README references the governing CR -> no DOC-005 finding."""
    d = tmp_path / "processes:process-u"
    d.mkdir()
    (d / "processes:process-u.yaml").write_text(yaml.safe_dump(_record(id_="processes:process-u")))
    (d / "README.md").write_text(_readme("processes:process-u", cr="CR-BP-13a"))
    f = evaluate([(d / "processes:process-u.yaml", _record(id_="processes:process-u"))])
    assert not any(fnd["rule"] == "DOC-005" for fnd in f), f


def test_doc_005_cr_not_referenced(tmp_path):
    """README does NOT reference the governing CR -> DOC-005 fires."""
    d = tmp_path / "processes:process-v"
    d.mkdir()
    (d / "processes:process-v.yaml").write_text(yaml.safe_dump(_record(id_="processes:process-v")))
    readme_text = _readme("processes:process-v", cr="CR-BP-13a").replace("Governed by CR-BP-13a.", "")
    (d / "README.md").write_text(readme_text)
    f = evaluate([(d / "processes:process-v.yaml", _record(id_="processes:process-v"))])
    assert any(fnd["rule"] == "DOC-005" for fnd in f), f


# -----------------------------------------------------------------------------
# Helper unit tests
# -----------------------------------------------------------------------------


def test_governing_cr_extracts_from_metadata():
    r = _record(governing_cr="CR-BP-42")
    assert _governing_cr(r) == "CR-BP-42"


def test_governing_cr_returns_none_when_absent():
    assert _governing_cr({}) is None


def test_readme_references_id_in_h1():
    assert _readme_references_id("# Canonical: `dea:x`", "dea:x") is True


def test_readme_does_not_reference_id_when_h1_missing():
    assert _readme_references_id("Some content", "dea:x") is False


def test_readme_references_cr_present():
    assert _readme_references_cr("Governed by CR-BP-13a.", "CR-BP-13a") is True


def test_readme_does_not_reference_cr_when_absent():
    assert _readme_references_cr("Just text", "CR-BP-13a") is False


# -----------------------------------------------------------------------------
# CLI-level tests
# -----------------------------------------------------------------------------


def test_cli_self_test_passes():
    result = _run(["--self-test"])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "self-test PASS" in result.stdout


def test_cli_live_run_returns_verdict():
    """Live catalog: many advisory findings (introductory READMEs)."""
    result = _run([])
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Documentation Profile (CR-BP-94-EXT-01 DOC-001..005)" in result.stdout


def test_cli_strict_mode_acceptable_for_advisory_findings():
    """--strict exits 0 because all DOC-001..005 findings are advisory."""
    result = _run(["--strict"])
    assert result.returncode == 0, result.stdout + result.stderr


def test_cli_json_emits_well_formed_payload():
    result = _run(["--json"])
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert "verdict" in payload
    assert "rules" in payload
    rule_ids = {r["id"] for r in payload["rules"]}
    assert rule_ids == {"DOC-001", "DOC-002", "DOC-003", "DOC-004", "DOC-005"}
    # Profile registry is exposed.
    assert "profile_registry" in payload
    profile_keys = {tuple(p["key"]) for p in payload["profile_registry"]}
    assert profile_keys == {
        ("ProcessContext", "L0"),
        ("ProcessGroup", "L1"),
        ("Process", "L2"),
        ("Activity", "L3"),
        ("Task", "L4"),
    }


def test_findings_are_tagged_advisory():
    """All DOC-001..005 findings must carry advisory=True (REQ: gate is advisory)."""
    result = _run(["--json"])
    payload = json.loads(result.stdout)
    for fnd in payload["findings"]:
        assert fnd.get("advisory") is True, fnd
