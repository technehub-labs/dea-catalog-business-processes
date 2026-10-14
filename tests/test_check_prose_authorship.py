"""Test suite for check_prose_authorship.py (CR-BP-118c).

The 118a/118b authorship gate (test_check_authorship.py) covers
metadata fields; this suite covers the parallel content-field gate.
Same shape: 21 tests covering CLI, the two rules, the registry,
and the live catalog.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_prose_authorship.py"
REGISTRY = ROOT / "reconciliation" / "prose-fields.yaml"


def _load_module():
    spec = importlib.util.spec_from_file_location("check_prose_authorship_test", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, cwd=str(ROOT),
    )


# --------------------------------------------------------------------------- #
# CLI tests
# --------------------------------------------------------------------------- #

def test_cli_self_test_passes():
    r = _run("--self-test")
    assert r.returncode == 0, r.stderr
    assert "self-test PASS" in r.stdout


def test_cli_live_catalog_conformant():
    r = _run()
    assert r.returncode == 0
    assert "CONFORMANT" in r.stdout


def test_cli_live_catalog_strict_passes():
    r = _run("--strict")
    assert r.returncode == 0
    assert "CONFORMANT" in r.stdout


def test_cli_json_shape():
    r = _run("--json")
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert "verdict" in data
    assert "findings" in data
    assert data["verdict"] in ("CONFORMANT", "CONFORMANT-WITH-WARNINGS", "NON-CONFORMANT")


# --------------------------------------------------------------------------- #
# Registry tests
# --------------------------------------------------------------------------- #

def test_registry_loads_expected_fields():
    """The registry must declare the four content fields (name, definition,
    description, summary) on the entities/v1-alpha/**/*.yaml glob."""
    mod = _load_module()
    reg = mod._load_registry(REGISTRY)
    paths = {f["path"] for f in reg["fields"]}
    assert "name" in paths
    assert "definition" in paths
    assert "description" in paths
    assert "summary" in paths


def test_registry_allowlist_includes_agent():
    """The cornerstone of CR-BP-118c: 'Agent' is in the allowlist because
    the dea-catalog-processes domain vocabulary uses it as a workforce noun
    in 299+ content fields."""
    mod = _load_module()
    reg = mod._load_registry(REGISTRY)
    assert "Agent" in reg["allowlist"]


def test_registry_denylist_excludes_agent():
    """The denylist must not include 'Agent' (it is allowlisted instead)."""
    mod = _load_module()
    reg = mod._load_registry(REGISTRY)
    assert "Agent" not in reg["denylist"]


def test_registry_denylist_includes_canonical_tokens():
    mod = _load_module()
    reg = mod._load_registry(REGISTRY)
    for token in ("Coder", "Hermes", "Claude", "GPT", "Cline", "OpenAI", "MiniMax", "MiniMax-M3"):
        assert token in reg["denylist"], f"missing {token}"


# --------------------------------------------------------------------------- #
# Field-extractor tests
# --------------------------------------------------------------------------- #

def test_extract_inline_single_line(tmp_path):
    mod = _load_module()
    f = tmp_path / "f.yaml"
    f.write_text("name: A simple value\n")
    out = mod._extract_field_values(f, "name")
    assert out == [(1, "A simple value")]


def test_extract_quoted_single_line(tmp_path):
    mod = _load_module()
    f = tmp_path / "f.yaml"
    f.write_text('name: "A quoted value"\n')
    out = mod._extract_field_values(f, "name")
    assert out == [(1, "A quoted value")]


def test_extract_block_scalar(tmp_path):
    mod = _load_module()
    f = tmp_path / "f.yaml"
    f.write_text("definition: |\n  Line one.\n  Line two.\n  Line three.\n")
    out = mod._extract_field_values(f, "definition")
    assert len(out) == 1
    line_no, value = out[0]
    assert line_no == 1
    assert "Line one." in value
    assert "Line two." in value
    assert "Line three." in value


def test_extract_folded_scalar(tmp_path):
    mod = _load_module()
    f = tmp_path / "f.yaml"
    f.write_text("definition: >\n  Folded line one\n  folded line two.\n")
    out = mod._extract_field_values(f, "definition")
    assert len(out) == 1
    line_no, value = out[0]
    assert line_no == 1
    assert "Folded" in value and "folded" in value


def test_extract_field_absent(tmp_path):
    mod = _load_module()
    f = tmp_path / "f.yaml"
    f.write_text("name: A record\ndescription: A description.\n")
    out = mod._extract_field_values(f, "definition")
    assert out == []


# --------------------------------------------------------------------------- #
# Allowlist / denylist tests
# --------------------------------------------------------------------------- #

def test_word_boundary_allows_agent():
    """Word-boundary matching: 'MultiAgent' must not match 'Agent' as a
    whole word. The 'Agent' allowlist entry protects the dea-catalog-
    processes domain vocabulary (workforce/role noun)."""
    mod = _load_module()
    # Agent (allowlist) word-boundary match
    assert mod._matches_allowlist("Agent", "Agent Operations")
    # 'MultiAgent' embeds Agent without word boundary: must NOT match
    assert not mod._matches_allowlist("Agent", "MultiAgent Platform")


# --------------------------------------------------------------------------- #
# End-to-end evaluator tests
# --------------------------------------------------------------------------- #

def test_evaluator_clean_passes(tmp_path):
    """A fixture with all-allowlist (Agent) content must yield 0 findings."""
    mod = _load_module()
    reg = tmp_path / "prose-fields.yaml"
    reg.write_text(
        "fields:\n  - path: name\n    file_glob: '*.yaml'\n"
        "allowlist:\n  - Agent\n"
        "denylist:\n  - Coder\n  - MiniMax\n",
        encoding="utf-8",
    )
    f = tmp_path / "f.yaml"
    f.write_text("name: Agent Operations\n")
    findings = mod.evaluate(tmp_path, reg)
    assert findings == []


def test_evaluator_flags_coder_in_name(tmp_path):
    mod = _load_module()
    reg = tmp_path / "prose-fields.yaml"
    reg.write_text(
        "fields:\n  - path: name\n    file_glob: '*.yaml'\n"
        "allowlist:\n  - Agent\n"
        "denylist:\n  - Coder\n",
        encoding="utf-8",
    )
    f = tmp_path / "f.yaml"
    f.write_text("name: Built by Coder (eaojnr)\n")
    findings = mod.evaluate(tmp_path, reg)
    prose_001 = [x for x in findings if x["rule"] == "PROSE-001"]
    assert len(prose_001) == 1
    assert prose_001[0]["matched"] == "Coder"
    assert prose_001[0]["file"].endswith("f.yaml")
    assert prose_001[0]["line"] == 1


def test_evaluator_flags_minimax_in_block(tmp_path):
    mod = _load_module()
    reg = tmp_path / "prose-fields.yaml"
    reg.write_text(
        "fields:\n  - path: definition\n    file_glob: '*.yaml'\n"
        "allowlist:\n  - Agent\n"
        "denylist:\n  - MiniMax\n",
        encoding="utf-8",
    )
    f = tmp_path / "f.yaml"
    f.write_text("definition: |\n  Generated by MiniMax-M3 on 2026-10-13.\n")
    findings = mod.evaluate(tmp_path, reg)
    prose_001 = [x for x in findings if x["rule"] == "PROSE-001"]
    assert len(prose_001) == 1
    assert prose_001[0]["matched"] == "MiniMax"


def test_evaluator_flags_empty_value(tmp_path):
    mod = _load_module()
    reg = tmp_path / "prose-fields.yaml"
    reg.write_text(
        "fields:\n  - path: name\n    file_glob: '*.yaml'\n"
        "allowlist:\n  - Agent\n"
        "denylist:\n  - Coder\n",
        encoding="utf-8",
    )
    f = tmp_path / "f.yaml"
    f.write_text("name: ''\n")
    findings = mod.evaluate(tmp_path, reg)
    prose_002 = [x for x in findings if x["rule"] == "PROSE-002"]
    assert len(prose_002) == 1


def test_evaluator_agent_does_not_trigger(tmp_path):
    """'Agent' is allowlisted; an 'Agent' word in content must not raise
    PROSE-001 even though 'Agent' is in the denylist semantics."""
    mod = _load_module()
    reg = tmp_path / "prose-fields.yaml"
    reg.write_text(
        "fields:\n  - path: name\n    file_glob: '*.yaml'\n"
        "allowlist:\n  - Agent\n"
        "denylist:\n  - Agent\n",  # both lists include Agent; allowlist wins
        encoding="utf-8",
    )
    f = tmp_path / "f.yaml"
    f.write_text("name: Agent Operations\n")
    findings = mod.evaluate(tmp_path, reg)
    assert findings == []


# --------------------------------------------------------------------------- #
# Live catalog: 0 findings on the current dea-catalog-processes main
# --------------------------------------------------------------------------- #

def test_live_catalog_has_zero_prose_001_findings():
    """The 118c gate's contract: 0 PROSE-001 findings on the live tree.

    The dea-catalog-processes catalog has 299+ 'Agent' content hits, all
    of which are allowlisted domain vocabulary. The gate stays CONFORMANT.
    """
    mod = _load_module()
    findings = mod.evaluate()
    prose_001 = [f for f in findings if f["rule"] == "PROSE-001"]
    assert prose_001 == [], (
        f"expected 0 PROSE-001 findings on the live tree, got {len(prose_001)}: "
        f"{prose_001[:5]}"
    )
