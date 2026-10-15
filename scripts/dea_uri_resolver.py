#!/usr/bin/env python3
"""dea_uri_resolver.py

CLI tool that resolves a dea:// URI to a file path on disk,
per the U-01 Cross-Catalog URI Standard (CR-BP-126) and the
dea:// URI Scheme Specification (CR-BP-127).

Usage:
  python3 scripts/dea_uri_resolver.py <dea-uri>
      Print the local file path (or "unresolvable" + exit 1).
  python3 scripts/dea_uri_resolver.py --exists <dea-uri>
      Exit 0 if the file exists locally, 1 otherwise.
  python3 scripts/dea_uri_resolver.py --fetch <dea-uri>
      Print the file contents (or "unresolvable" + exit 1).
  python3 scripts/dea_uri_resolver.py --list
      List all known scopes.
  python3 scripts/dea_uri_resolver.py --resolve <dea-uri>
      Print the resolved path AND the canonical URI form.

The resolver is data-driven from the cross-catalog resolution
registry at reconciliation/cross-catalog-resolution.yaml. The
legacy dea: ids are resolved via the migration id map at
reconciliation/migration-id-map.yaml (CR-BP-mv1; 3640 lines).

Exit codes:
  0  Resolved (or scope listed, for --list)
  1  Unresolvable (URI malformed, scope unknown, legacy id unknown)
  2  File does not exist locally (for --exists / --fetch)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "reconciliation" / "cross-catalog-resolution.yaml"
MIGRATION_MAP_PATH = ROOT / "reconciliation" / "migration-id-map.yaml"
SIBLING_ROOT = Path("/home/hermes/Projects/dea-sibling-check")
LOCAL_ROOT = ROOT  # the current repo is the in-thread scope

# ---------------------------------------------------------------------------- #
# URI parsing
# ---------------------------------------------------------------------------- #

# dea://{scope}/{entity-id}
# entity-id is canonical (namespace:token-descriptor-hash) or legacy (dea:...)
DEA_URI_PATTERN = re.compile(
    r"^dea://(?P<scope>[a-z][a-z0-9-]+)/(?P<entity_id>.+)$"
)

# canonical id: {namespace}:{token}-{descriptor}-{hash}
# hash is 6 chars from base32 (no 0/o/1/l)
CANONICAL_ID_PATTERN = re.compile(
    r"^(?P<namespace>[a-z]+):(?P<rest>[a-z]+(-[a-z]+){1,4}-[a-z2-9]{6})$"
)
LEGACY_ID_PATTERN = re.compile(
    r"^dea:(?P<rest>[a-z0-9-]+)$"
)

# Scope -> local repo path. The current repo is the in-thread scope.
DEFAULT_SCOPE_PATHS = {
    "dea-catalog-business-processes": LOCAL_ROOT,
}


def parse_uri(uri: str) -> Optional[dict]:
    """Parse a dea:// URI. Returns dict with scope, entity_id, is_legacy, or None."""
    m = DEA_URI_PATTERN.match(uri)
    if not m:
        return None
    scope = m.group("scope")
    entity_id = m.group("entity_id")

    if entity_id.startswith("dea:"):
        return {"scope": scope, "entity_id": entity_id, "is_legacy": True}
    return {"scope": scope, "entity_id": entity_id, "is_legacy": False}


def _split_rest(rest: str) -> Optional[dict]:
    """Split an id's rest part into token, descriptor, hash.
    rest format: {token}-{descriptor-segments...}-{hash}
    where hash is 6 chars from base32 (no 0/o/1/l).
    The slug is the descriptor (without the hash) -- the live tree's
    directory naming convention uses the descriptor only, not the
    descriptor+hash.
    """
    # Find the last 6-char segment that looks like a base32 hash
    parts = rest.split("-")
    if len(parts) < 3:
        return None
    hash_segment = parts[-1]
    if not re.match(r"^[a-z2-9]{6}$", hash_segment):
        return None
    token = parts[0]
    descriptor = "-".join(parts[1:-1])
    if not descriptor:
        return None
    return {"token": token, "descriptor": descriptor, "hash": hash_segment, "slug": descriptor}


# ---------------------------------------------------------------------------- #
# Registry + migration map loaders
# ---------------------------------------------------------------------------- #

def _load_registry(path: Path = REGISTRY_PATH) -> dict:
    """Load the cross-catalog resolution registry. Returns {scope: entry}."""
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="ignore")
    data = yaml.safe_load(text) or {}
    catalogs = data.get("catalogs", [])
    return {entry["scope"]: entry for entry in catalogs if "scope" in entry}


def _load_migration_map(path: Path = MIGRATION_MAP_PATH) -> dict:
    """Load the legacy id -> canonical id migration map. Returns {legacy_id: canonical_id}."""
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8", errors="ignore")
    data = yaml.safe_load(text) or {}
    id_map = data.get("id_map", {})
    # The id_map is a flat dict: {legacy_id: canonical_id}
    return id_map


# ---------------------------------------------------------------------------- #
# Resolution
# ---------------------------------------------------------------------------- #

def _local_repo_path(scope: str, registries: dict) -> Optional[Path]:
    """Get the local path to the catalog repository for a scope."""
    if scope in DEFAULT_SCOPE_PATHS:
        return DEFAULT_SCOPE_PATHS[scope]
    entry = registries.get(scope, {})
    repo = entry.get("repository", "")
    if not repo:
        return None
    # Try the sibling check directory first
    sibling = SIBLING_ROOT / repo
    if sibling.exists():
        return sibling
    return None


def _resolve_path(entity_id: str, repo_path: Path) -> Optional[Path]:
    """Compute the file path for a canonical entity id."""
    m = CANONICAL_ID_PATTERN.match(entity_id)
    if not m:
        return None
    rest = m.group("rest")
    parts = _split_rest(rest)
    if not parts:
        return None
    slug = parts["slug"]
    # The filename: {namespace}-{rest} with : replaced by -
    filename = entity_id.replace(":", "-")
    # The file is at entities/v1-alpha/{slug}/{filename}.yaml
    path = repo_path / "entities" / "v1-alpha" / slug / f"{filename}.yaml"
    if path.exists():
        return path
    # Try alternative: file at the slug directory root (some catalogs)
    alt = repo_path / "entities" / "v1-alpha" / slug / filename
    if alt.exists():
        return alt
    return path  # return the expected path even if it doesn't exist (caller decides)


def _resolve_legacy_path(legacy_id: str, repo_path: Path, migration_map: dict) -> Optional[Path]:
    """Resolve a legacy dea: id via the migration map, then to a file path."""
    canonical_id = migration_map.get(legacy_id)
    if not canonical_id:
        return None
    return _resolve_path(canonical_id, repo_path)


def resolve(uri: str) -> dict:
    """Resolve a dea:// URI to a file path. Returns a result dict."""
    parsed = parse_uri(uri)
    if not parsed:
        return {"resolved": False, "error": f"malformed URI: {uri}"}

    scope = parsed["scope"]
    entity_id = parsed["entity_id"]
    registries = _load_registry()
    repo_path = _local_repo_path(scope, registries)

    if repo_path is None:
        return {"resolved": False, "error": f"unknown scope: {scope}",
                "known_scopes": sorted(list(registries.keys()) + list(DEFAULT_SCOPE_PATHS.keys()))}

    if parsed["is_legacy"]:
        migration_map = _load_migration_map()
        path = _resolve_legacy_path(entity_id, repo_path, migration_map)
        if not path:
            return {"resolved": False, "error": f"unknown legacy id: {entity_id}",
                    "scope": scope, "repo": str(repo_path)}
        canonical_id = migration_map.get(entity_id)
        return {"resolved": True, "path": path, "scope": scope, "repo": str(repo_path),
                "entity_id": canonical_id, "legacy_id": entity_id, "is_legacy": True}
    else:
        path = _resolve_path(entity_id, repo_path)
        if not path:
            return {"resolved": False, "error": f"invalid entity id format: {entity_id}",
                    "scope": scope, "repo": str(repo_path)}
        # Check if it exists
        exists = path.exists()
        return {"resolved": True, "path": path, "scope": scope, "repo": str(repo_path),
                "entity_id": entity_id, "exists": exists, "is_legacy": False}


# ---------------------------------------------------------------------------- #
# CLI
# ---------------------------------------------------------------------------- #

def main(argv: list) -> int:
    parser = argparse.ArgumentParser(
        description="Resolve a dea:// URI to a file path on disk.",
    )
    parser.add_argument("uri", nargs="?", help="The dea:// URI to resolve")
    parser.add_argument("--exists", action="store_true",
                        help="Exit 0 if file exists locally, 1 otherwise")
    parser.add_argument("--fetch", action="store_true",
                        help="Print the file contents instead of the path")
    parser.add_argument("--list", action="store_true",
                        help="List all known scopes and exit")
    parser.add_argument("--resolve", action="store_true",
                        help="Print the resolved path AND the canonical URI form")
    args = parser.parse_args(argv)

    if args.list:
        registries = _load_registry()
        scopes = sorted(set(list(registries.keys()) + list(DEFAULT_SCOPE_PATHS.keys())))
        print("Known scopes:")
        for scope in scopes:
            entry = registries.get(scope, {})
            repo = entry.get("repository", "<in-thread>")
            print(f"  {scope}: {repo}")
        return 0

    if not args.uri:
        parser.error("uri is required (or use --list)")

    result = resolve(args.uri)
    if not result["resolved"]:
        print(f"unresolvable: {result['error']}", file=sys.stderr)
        if "known_scopes" in result:
            print(f"  known scopes: {result['known_scopes']}", file=sys.stderr)
        return 1

    path = result["path"]

    if args.exists:
        if path.exists():
            return 0
        return 2

    if args.fetch:
        if not path.exists():
            print(f"file does not exist: {path}", file=sys.stderr)
            return 2
        print(path.read_text(encoding="utf-8", errors="ignore"))
        return 0

    if args.resolve:
        entity_id = result["entity_id"]
        canonical_uri = f"dea://{result['scope']}/{entity_id}"
        print(f"path: {path}")
        print(f"uri:  {canonical_uri}")
        return 0 if path.exists() else 2

    # Default: print the path
    print(path)
    return 0 if path.exists() else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
