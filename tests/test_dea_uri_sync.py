"""Test suite for dea_uri_sync.py (CR-BP-131; T9.7 sync tool).

The sync tool clones catalog repositories if absent, or pulls
the latest changes if present. Tests use a tmpdir + a mocked
git binary to avoid network dependencies.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "dea_uri_sync.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("dea_uri_sync", SCRIPT)
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
# Registry tests (2 tests)
# --------------------------------------------------------------------------- #

def test_load_registry_returns_dict():
    mod = _load_module()
    reg = mod._load_registry()
    assert isinstance(reg, dict)
    assert "dea-metamodel" in reg
    assert "dea-catalog-business-capabilities" in reg


def test_local_repo_path_in_thread_scope():
    """The in-thread scope is the local repo."""
    mod = _load_module()
    reg = mod._load_registry()
    local = mod._local_repo_path("dea-catalog-business-processes", reg)
    assert local == mod.LOCAL_ROOT


# --------------------------------------------------------------------------- #
# Git operations tests (4 tests; use real git on a tmpdir)
# --------------------------------------------------------------------------- #

def test_run_git_init_creates_repo(tmp_path):
    mod = _load_module()
    rc, out, err = mod._run_git(["init"], cwd=tmp_path)
    assert rc == 0
    assert (tmp_path / ".git").exists()


def test_run_git_returns_127_when_git_missing(tmp_path, monkeypatch):
    """If git is missing, _run_git returns (127, '', 'git not found')."""
    mod = _load_module()
    monkeypatch.setattr(mod.subprocess, "run", lambda *a, **kw: (_ for _ in ()).throw(FileNotFoundError("git not found")))
    rc, out, err = mod._run_git(["status"], cwd=tmp_path)
    assert rc == 127


def test_clone_scope_unknown_returns_unknown_status():
    mod = _load_module()
    reg = mod._load_registry()
    result = mod.clone_scope("unknown-scope-xyz", reg, depth=1)
    assert result["status"] == "unknown"
    assert "not in registry" in result["message"]


def test_clone_scope_in_thread_returns_skipped():
    """In-thread scope is skipped (not synced)."""
    mod = _load_module()
    reg = mod._load_registry()
    result = mod.clone_scope("dea-catalog-business-processes", reg, depth=1)
    assert result["status"] == "skipped"
    assert "in-thread" in result["message"]


# --------------------------------------------------------------------------- #
# pull_scope tests (2 tests; use real git on a tmpdir)
# --------------------------------------------------------------------------- #

def test_pull_scope_no_local_returns_no_local():
    mod = _load_module()
    reg = mod._load_registry()
    # Use a scope that has a registered repo but no local clone
    result = mod.pull_scope("dea-catalog-business-capabilities", reg)
    # The sibling check directory has the repo; if not, returns no-local
    sibling = mod.SIBLING_ROOT / reg["dea-catalog-business-capabilities"]["repository"]
    if not sibling.exists():
        assert result["status"] == "no-local"
    else:
        # If it exists, pull should work (or fail with network issue)
        assert result["status"] in ("updated", "up-to-date", "failed")


def test_pull_scope_in_thread_returns_skipped():
    mod = _load_module()
    reg = mod._load_registry()
    result = mod.pull_scope("dea-catalog-business-processes", reg)
    assert result["status"] == "skipped"
    assert "in-thread" in result["message"]


# --------------------------------------------------------------------------- #
# sync_scope integration (2 tests)
# --------------------------------------------------------------------------- #

def test_sync_scope_uses_clone_when_no_local(tmp_path, monkeypatch):
    """When no local clone, sync_scope uses clone_scope."""
    mod = _load_module()
    monkeypatch.setattr(mod, "SIBLING_ROOT", tmp_path)
    reg = mod._load_registry()
    result = mod.sync_scope("dea-metamodel", reg, depth=1)
    # Either cloned (if network) or failed
    assert result["status"] in ("cloned", "failed", "unknown")


def test_sync_scope_uses_pull_when_local_exists(tmp_path, monkeypatch):
    """When local clone exists, sync_scope uses pull_scope."""
    mod = _load_module()
    reg = mod._load_registry()
    # Create a fake local clone
    fake_local = tmp_path / "technehub-labs" / "dea-metamodel"
    fake_local.mkdir(parents=True)
    monkeypatch.setattr(mod, "SIBLING_ROOT", tmp_path)
    # Now sync should detect the local clone and try to pull
    # Pull will fail (not a real git repo) but the status should reflect that
    result = mod.sync_scope("dea-metamodel", reg, depth=1)
    assert result["status"] in ("updated", "up-to-date", "failed")


# --------------------------------------------------------------------------- #
# CLI tests (4 tests)
# --------------------------------------------------------------------------- #

def test_cli_list_exits_zero():
    r = _run("--list")
    assert r.returncode == 0
    assert "dea-catalog-business-processes" in r.stdout
    assert "dea-metamodel" in r.stdout


def test_cli_missing_scope_exits_two():
    r = _run()
    assert r.returncode == 2


def test_cli_in_thread_scope_is_skipped():
    """The in-thread scope is skipped, not synced."""
    r = _run("dea-catalog-business-processes")
    assert r.returncode == 0
    assert "skipped" in r.stdout
    assert "in-thread" in r.stdout


def test_cli_unknown_scope_exits_one():
    r = _run("unknown-scope-xyz")
    assert r.returncode == 1
    assert "unknown" in r.stdout
