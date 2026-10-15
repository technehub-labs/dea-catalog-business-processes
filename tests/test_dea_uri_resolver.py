"""Test suite for dea_uri_resolver.py (CR-BP-128).

The resolver implements the U-01 Cross-Catalog URI Standard
(CR-BP-126) and the dea:// URI Scheme Specification (CR-BP-127).
20 tests cover URI parsing, scope resolution, legacy id resolution,
file path computation, and the CLI.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "dea_uri_resolver.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("dea_uri_resolver", SCRIPT)
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, cwd=str(ROOT),
    )


# --------------------------------------------------------------------------- #
# URI parsing (5 tests)
# --------------------------------------------------------------------------- #

def test_parse_canonical_uri():
    mod = _load_module()
    parsed = mod.parse_uri("dea://dea-catalog-business-processes/processes:process-foo-bar-f3n8wb")
    assert parsed is not None
    assert parsed["scope"] == "dea-catalog-business-processes"
    assert parsed["entity_id"] == "processes:process-foo-bar-f3n8wb"
    assert parsed["is_legacy"] is False


def test_parse_legacy_uri():
    mod = _load_module()
    parsed = mod.parse_uri("dea://dea-catalog-business-processes/dea:process-foo-bar")
    assert parsed is not None
    assert parsed["scope"] == "dea-catalog-business-processes"
    assert parsed["entity_id"] == "dea:process-foo-bar"
    assert parsed["is_legacy"] is True


def test_parse_malformed_uri_no_scheme():
    mod = _load_module()
    assert mod.parse_uri("https://example.com/foo") is None


def test_parse_malformed_uri_no_scope():
    mod = _load_module()
    assert mod.parse_uri("dea:///processes:process-foo-bar-f3n8wb") is None


def test_parse_long_descriptor_uri():
    mod = _load_module()
    parsed = mod.parse_uri(
        "dea://dea-catalog-business-processes/processes:process-manage-customer-relationship-f3n8wb"
    )
    assert parsed is not None
    assert parsed["entity_id"] == "processes:process-manage-customer-relationship-f3n8wb"


# --------------------------------------------------------------------------- #
# id rest splitting (4 tests)
# --------------------------------------------------------------------------- #

def test_split_rest_pc():
    mod = _load_module()
    parts = mod._split_rest("pc-fa-retire-64q5p9")
    assert parts is not None
    assert parts["token"] == "pc"
    assert parts["descriptor"] == "fa-retire"
    assert parts["hash"] == "64q5p9"
    assert parts["slug"] == "fa-retire"  # slug is descriptor only (matches live tree dirs)


def test_split_rest_short_bp():
    mod = _load_module()
    parts = mod._split_rest("process-foo-bar-f3n8wb")
    assert parts is not None
    assert parts["token"] == "process"
    assert parts["descriptor"] == "foo-bar"
    assert parts["slug"] == "foo-bar"


def test_split_rest_long_bp():
    mod = _load_module()
    parts = mod._split_rest("process-manage-customer-relationship-f3n8wb")
    assert parts is not None
    assert parts["token"] == "process"
    assert parts["descriptor"] == "manage-customer-relationship"
    assert parts["slug"] == "manage-customer-relationship"


def test_split_rejects_uppercase_hash():
    """Hash must be base32 lowercase."""
    mod = _load_module()
    parts = mod._split_rest("pc-fa-retire-ABC123")
    assert parts is None  # hash contains uppercase


# --------------------------------------------------------------------------- #
# Registry + migration map (3 tests)
# --------------------------------------------------------------------------- #

def test_load_registry_returns_dict():
    mod = _load_module()
    reg = mod._load_registry()
    assert isinstance(reg, dict)
    # The live tree has at least the 7 catalog scopes from CR-BP-124
    expected_scopes = [
        "dea-catalog-business-capabilities",
        "dea-catalog-business-objects",
        "dea-catalog-organizational-units",
        "dea-catalog-actors",
        "dea-catalog-stakeholders",
        "dea-metamodel",
        "dea-architecture-framework",
    ]
    for scope in expected_scopes:
        assert scope in reg, f"missing scope: {scope}"


def test_load_migration_map_returns_dict():
    mod = _load_module()
    m = mod._load_migration_map()
    assert isinstance(m, dict)
    assert len(m) > 100  # 3640 lines; expect hundreds of legacy ids


def test_migration_map_resolves_known_legacy_id():
    """The 35 dea: legacy tails in entities/v1-alpha/ are in the map."""
    mod = _load_module()
    m = mod._load_migration_map()
    # Pick a known legacy id from the live tree
    legacy_id = "dea:activity-acquire-regulator-acknowledged-accounting-or-rate-framework"
    assert legacy_id in m
    assert m[legacy_id].startswith("processes:activity-")


# --------------------------------------------------------------------------- #
# Resolution (5 tests)
# --------------------------------------------------------------------------- #

def test_resolve_canonical_uri_existing_file():
    """A known canonical id resolves to an existing file path."""
    mod = _load_module()
    # Find an actual entity id from the live tree
    entities = list((ROOT / "entities" / "v1-alpha").rglob("*.yaml"))
    assert entities, "no entities in live tree"
    # Take the first one
    path = entities[0]
    # Extract the id from the file
    text = path.read_text()
    rid = None
    for line in text.splitlines():
        if line.strip().startswith("id:"):
            rid = line.split(":", 1)[1].strip()
            break
    assert rid, f"no id in {path}"
    # Construct the URI
    uri = f"dea://dea-catalog-business-processes/{rid}"
    result = mod.resolve(uri)
    assert result["resolved"] is True
    assert result["path"] == path
    assert result["entity_id"] == rid
    assert result["exists"] is True


def test_resolve_canonical_uri_nonexistent_file():
    """A valid id with no corresponding file returns resolved=True with exists=False."""
    mod = _load_module()
    uri = "dea://dea-catalog-business-processes/processes:process-this-does-not-exist-f3n8wb"
    result = mod.resolve(uri)
    assert result["resolved"] is True
    assert result["exists"] is False


def test_resolve_legacy_uri_resolves_via_migration_map():
    mod = _load_module()
    # A known legacy id from the live tree
    legacy_id = "dea:activity-acquire-regulator-acknowledged-accounting-or-rate-framework"
    uri = f"dea://dea-catalog-business-processes/{legacy_id}"
    result = mod.resolve(uri)
    assert result["resolved"] is True
    assert result["is_legacy"] is True
    assert result["entity_id"].startswith("processes:activity-")


def test_resolve_unknown_scope_returns_error():
    mod = _load_module()
    uri = "dea://unknown-scope/processes:process-foo-bar-f3n8wb"
    result = mod.resolve(uri)
    assert result["resolved"] is False
    assert "unknown scope" in result["error"]


def test_resolve_malformed_uri_returns_error():
    mod = _load_module()
    result = mod.resolve("not-a-uri")
    assert result["resolved"] is False
    assert "malformed" in result["error"]


# --------------------------------------------------------------------------- #
# CLI tests (3 tests)
# --------------------------------------------------------------------------- #

def test_cli_list_exits_zero():
    r = _run("--list")
    assert r.returncode == 0
    assert "dea-catalog-business-processes" in r.stdout
    assert "dea-catalog-business-capabilities" in r.stdout


def test_cli_resolve_prints_path():
    """A known canonical id resolves to a file path via the CLI."""
    r = _run("dea://dea-catalog-business-processes/processes:process-foo-bar-f3n8wb")
    assert r.returncode in (0, 2)  # 0 if file exists, 2 if not
    assert "entities" in r.stdout
    assert "v1-alpha" in r.stdout


def test_cli_unknown_scope_exits_one():
    r = _run("dea://unknown-scope/processes:process-foo-bar-f3n8wb")
    assert r.returncode == 1
    assert "unknown scope" in r.stderr


# --------------------------------------------------------------------------- #
# Local tree (1 integration test)
# --------------------------------------------------------------------------- #

def test_resolve_pc_record_in_live_tree():
    """A real PC record resolves to its file path."""
    mod = _load_module()
    # Take a known PC record from the live tree
    pc_files = list((ROOT / "entities" / "v1-alpha").rglob("pc-*"))
    if not pc_files:
        pytest.skip("no PC records in live tree")
    # Use the first PC file to construct a URI
    pc_file = pc_files[0]
    text = pc_file.read_text()
    rid = None
    for line in text.splitlines():
        if line.strip().startswith("id:"):
            rid = line.split(":", 1)[1].strip()
            break
    if not rid:
        pytest.skip("no id in PC file")
    uri = f"dea://dea-catalog-business-processes/{rid}"
    result = mod.resolve(uri)
    assert result["resolved"] is True
    assert result["path"] == pc_file
    assert result["exists"] is True
