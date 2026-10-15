#!/usr/bin/env python3
"""dea_uri_sync.py

CLI tool that syncs catalog repositories (scopes) with the
remote. Clones a scope's repo if absent, or fetches + pulls
if present. Useful for keeping local clones in sync with the
remote.

Usage:
  python3 scripts/dea_uri_sync.py <scope>
      Sync a specific scope.
  python3 scripts/dea_uri_sync.py --all
      Sync all known scopes.
  python3 scripts/dea_uri_sync.py --ref <ref>
      Checkout a specific ref (branch, tag, SHA) after sync.
  python3 scripts/dea_uri_sync.py --depth <n>
      Clone depth for new clones (default 1 = shallow).
  python3 scripts/dea_uri_sync.py --list
      List all known scopes.

Exit codes:
  0  All requested scopes synced successfully.
  1  One or more scopes failed to sync.
  2  No scopes provided and --all not set.

This is T9.7 (sync tool). The tool is data-driven from
reconciliation/cross-catalog-resolution.yaml. It pairs with
the remote-fetcher in scripts/dea_uri_resolver.py (--remote
flag) but is dedicated to multi-scope sync workflows.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Optional

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "reconciliation" / "cross-catalog-resolution.yaml"
SIBLING_ROOT = Path("/home/hermes/Projects/dea-sibling-check")
LOCAL_ROOT = ROOT  # the in-thread repo

DEFAULT_SCOPE_PATHS = {
    "dea-catalog-business-processes": LOCAL_ROOT,
}


# ---------------------------------------------------------------------------- #
# Registry
# ---------------------------------------------------------------------------- #

def _load_registry(path: Path = REGISTRY_PATH) -> dict:
    """Load the cross-catalog resolution registry. Returns {scope: entry}."""
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="ignore")
    data = yaml.safe_load(text) or {}
    catalogs = data.get("catalogs", [])
    return {entry["scope"]: entry for entry in catalogs if "scope" in entry}


def _local_repo_path(scope: str, registries: dict) -> Optional[Path]:
    """Get the local path to the catalog repository for a scope."""
    if scope in DEFAULT_SCOPE_PATHS:
        return DEFAULT_SCOPE_PATHS[scope]
    entry = registries.get(scope, {})
    repo = entry.get("repository", "")
    if not repo:
        return None
    sibling = SIBLING_ROOT / repo
    if sibling.exists():
        return sibling
    return None


# ---------------------------------------------------------------------------- #
# Git operations
# ---------------------------------------------------------------------------- #

def _run_git(args: list, cwd: Path, timeout: int = 60) -> tuple[int, str, str]:
    """Run a git command; return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except FileNotFoundError:
        return 127, "", "git not found"


def clone_scope(scope: str, registries: dict, depth: int = 1) -> dict:
    """Clone a scope's repo from GitHub.

    Returns {scope, status, path, message}.
    status is one of: 'cloned', 'already-exists', 'unknown', 'failed'.
    """
    if scope in DEFAULT_SCOPE_PATHS:
        return {"scope": scope, "status": "skipped", "path": str(DEFAULT_SCOPE_PATHS[scope]),
                "message": "in-thread scope; not synced"}
    entry = registries.get(scope)
    if not entry:
        return {"scope": scope, "status": "unknown", "path": None,
                "message": "scope not in registry"}
    repo = entry.get("repository", "")
    if not repo:
        return {"scope": scope, "status": "unknown", "path": None,
                "message": "no repository in registry"}
    target = SIBLING_ROOT / repo
    if target.exists():
        return {"scope": scope, "status": "already-exists", "path": str(target),
                "message": "local clone present (use pull_scope to update)"}
    SIBLING_ROOT.mkdir(parents=True, exist_ok=True)
    url = f"https://github.com/{repo}.git"
    rc, out, err = _run_git(["clone", "--depth", str(depth), url, str(target)], cwd=Path("."), timeout=120)
    if rc == 0:
        return {"scope": scope, "status": "cloned", "path": str(target), "message": "ok"}
    return {"scope": scope, "status": "failed", "path": str(target),
            "message": f"clone failed: {err.strip()[:200]}"}


def pull_scope(scope: str, registries: dict, ref: Optional[str] = None) -> dict:
    """Pull the latest changes for a scope's local clone.

    Returns {scope, status, path, message, ref}.
    status is one of: 'updated', 'up-to-date', 'checkout-failed', 'no-local', 'unknown'.
    """
    if scope in DEFAULT_SCOPE_PATHS:
        return {"scope": scope, "status": "skipped", "path": str(DEFAULT_SCOPE_PATHS[scope]),
                "message": "in-thread scope; not synced", "ref": None}
    repo_path = _local_repo_path(scope, registries)
    if repo_path is None:
        return {"scope": scope, "status": "no-local", "path": None,
                "message": "no local clone; use clone_scope first", "ref": None}
    # Fetch
    rc, out, err = _run_git(["fetch", "--all", "--prune"], cwd=repo_path, timeout=120)
    if rc != 0:
        return {"scope": scope, "status": "failed", "path": str(repo_path),
                "message": f"fetch failed: {err.strip()[:200]}", "ref": None}
    # Optionally checkout a ref
    if ref:
        rc, out, err = _run_git(["checkout", ref], cwd=repo_path, timeout=30)
        if rc != 0:
            return {"scope": scope, "status": "checkout-failed", "path": str(repo_path),
                    "message": f"checkout {ref!r} failed: {err.strip()[:200]}", "ref": ref}
    # Pull (fast-forward only)
    rc, out, err = _run_git(["pull", "--ff-only"], cwd=repo_path, timeout=60)
    if rc == 0:
        return {"scope": scope, "status": "updated", "path": str(repo_path),
                "message": out.strip()[:200] or "ok", "ref": ref}
    if "Already up to date" in out or "Already up-to-date" in out:
        return {"scope": scope, "status": "up-to-date", "path": str(repo_path),
                "message": "already up to date", "ref": ref}
    return {"scope": scope, "status": "failed", "path": str(repo_path),
            "message": f"pull failed: {err.strip()[:200]}", "ref": ref}


def sync_scope(scope: str, registries: dict, depth: int = 1, ref: Optional[str] = None) -> dict:
    """Sync a scope: clone if absent, else pull (and optionally checkout)."""
    local = _local_repo_path(scope, registries)
    if local is None:
        return clone_scope(scope, registries, depth=depth)
    return pull_scope(scope, registries, ref=ref)


# ---------------------------------------------------------------------------- #
# CLI
# ---------------------------------------------------------------------------- #

def main(argv: list) -> int:
    parser = argparse.ArgumentParser(
        description="Sync catalog repositories (scopes) with the remote.",
    )
    parser.add_argument("scope", nargs="?", help="The scope to sync")
    parser.add_argument("--all", action="store_true",
                        help="Sync all known scopes")
    parser.add_argument("--ref", help="Checkout a specific ref after sync")
    parser.add_argument("--depth", type=int, default=1,
                        help="Clone depth for new clones (default 1 = shallow)")
    parser.add_argument("--list", action="store_true",
                        help="List all known scopes and exit")
    args = parser.parse_args(argv)

    registries = _load_registry()

    if args.list:
        scopes = sorted(set(list(registries.keys()) + list(DEFAULT_SCOPE_PATHS.keys())))
        for scope in scopes:
            local = _local_repo_path(scope, registries)
            entry = registries.get(scope, {})
            repo = entry.get("repository", "<in-thread>")
            status = "local" if local else "remote-only"
            print(f"  {scope}: {repo} [{status}]")
        return 0

    if args.all:
        scopes = sorted(set(list(registries.keys()) + list(DEFAULT_SCOPE_PATHS.keys())))
    elif args.scope:
        scopes = [args.scope]
    else:
        parser.error("scope is required (or use --all / --list)")

    results = []
    for scope in scopes:
        result = sync_scope(scope, registries, depth=args.depth, ref=args.ref)
        results.append(result)
        status = result["status"]
        msg = result.get("message", "")
        print(f"  {scope}: {status} - {msg}")

    failed = [r for r in results if r["status"] in ("failed", "unknown", "no-local", "checkout-failed")]
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
