"""CATALOG.yaml regenerator (CR-CATALOG-STRUCT-06a).

Walks a catalog repo's filesystem and emits the canonical `CATALOG.yaml`
index. The file is machine-generated only; hand-edits are forbidden by
CR-CATALOG-STRUCT-01 §6.3.

Convention: zero third-party dependencies. The module imports only from
the standard library so it works in the bare CI image (consistent with
`tools/ecf_coordinates.py`).

Exit codes (stable contract):
  0  success
  1  filesystem error (cannot read subtree, permission denied)
  2  schema validation failed (regenerated payload fails schema)
  3  --check mode: committed CATALOG.yaml is stale

Usage:
  python tools/regenerate_catalog.py [--catalog-root PATH] [--output PATH] \\
      [--check] [--dry-run] [--verbose] [--schema PATH]
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - PyYAML is required at runtime
    print("ERROR: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(1)

# State precedence per CR-CATALOG-STRUCT-06a §4.1.
# Lower number = lower precedence (subordinate to higher precedence).
STATE_PRECEDENCE: dict[str, int] = {
    "research": 1,
    "candidate": 2,
    "retired": 3,
    "canonical": 4,
    "placeholder": 5,
}

# Lifecycle values that imply a retired state for an otherwise-canonical subtree.
RETIRED_LIFECYCLE_STATUSES: frozenset[str] = frozenset({"deprecated", "retired"})

# Schema path default; relative to the catalog root.
DEFAULT_SCHEMA_PATH = "catalog-index-schema/catalog-index-schema.json"

# metamodel-pointer.yaml keys we consume (case-sensitive; mirrors what other
# catalog repos already use).
POINTER_KEYS: dict[str, str] = {
    "id": "catalog.id",
    "name": "catalog.name",
    "abbreviation": "catalog.abbreviation",
    "version": "catalog.version",
    "status": "catalog.status",
    "metamodel_version": "catalog.metamodel_version",
    "description": "catalog.description",
    "owner": "catalog.owner",
}

# Default owner if metamodel-pointer.yaml is absent.
DEFAULT_OWNER = "TechNeHub Labs"

# Cross-cutting paths (relative to catalog root).
CROSS_CUTTING_PATHS: dict[str, str] = {
    "classifications": "classifications/",
    "schemas": "schemas/",
    "validators": "scripts/",
    "contributions_queue": "contributions/",
    "change_requests": "change-requests/",
}

# Entity id pattern: CR-BP-mv1 org-wide form
# (e.g. processes:task-fa-activate-confirm-kuz7yt). Matches the
# schema's entity_entry.id pattern.
import re
ENTITY_ID_PATTERN = re.compile(r"^processes:[a-z0-9-]+$")


def load_schema(schema_path: Path) -> dict[str, Any]:
    with schema_path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_yaml(path: Path) -> dict[str, Any] | None:
    """Load a YAML file; return None on empty or non-mapping content."""
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except (OSError, yaml.YAMLError):
        return None
    if not isinstance(data, dict):
        return None
    return data


def read_pointer(catalog_root: Path) -> dict[str, Any]:
    """Read metamodel-pointer.yaml at the catalog root; return empty dict on absence."""
    pointer_path = catalog_root / "metamodel-pointer.yaml"
    if not pointer_path.exists():
        return {}
    data = load_yaml(pointer_path) or {}
    return data


def detect_repository_url(catalog_root: Path) -> str:
    """Read git origin URL; sanitize embedded credentials; return empty string on failure.

    git's remote URL may include embedded credentials when the user has
    authenticated via `git config credential.helper` or similar (e.g.
    `https://x-access-token:<TOKEN>@github.com/...`). Strip any
    userinfo before returning; the credential portion must never appear
    in CATALOG.yaml.
    """
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=str(catalog_root),
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired, FileNotFoundError):
        return ""
    if result.returncode != 0:
        return ""
    return _strip_url_credentials(result.stdout.strip())


def _strip_url_credentials(url: str) -> str:
    """Remove userinfo (user:pass@ or PAT-as-username@) from a URL.

    GitHub's authenticated clone URL embeds the PAT as the username:
        https://<TOKEN>@github.com/owner/repo.git
    The credential portion must not appear in catalog output (CR-BP-12
    §8 + STRUCT-06a security review).
    """
    if "@" not in url:
        return url
    scheme_end = url.find("://")
    if scheme_end < 0:
        return url
    after_scheme = scheme_end + 3
    at_index = url.find("@", after_scheme)
    if at_index < 0:
        return url
    return url[:after_scheme] + url[at_index + 1:]


def catalog_name_from_dir(catalog_root: Path) -> str:
    """Derive a catalog id from the repo directory name when the pointer is absent."""
    return catalog_root.resolve().name


def build_catalog_metadata(
    catalog_root: Path, pointer: dict[str, Any], verbose: bool
) -> tuple[dict[str, Any], list[str]]:
    """Build the `catalog:` block from metamodel-pointer.yaml + defaults."""
    warnings: list[str] = []
    catalog_id = pointer.get("id")
    if not isinstance(catalog_id, str) or not catalog_id:
        derived = catalog_name_from_dir(catalog_root)
        catalog_id = f"dea:catalog-{derived}" if not derived.startswith("dea:") else derived
        warnings.append(f"metamodel-pointer.yaml missing 'id'; defaulted to {catalog_id!r}")

    metadata: dict[str, Any] = {
        "id": catalog_id,
        "name": pointer.get("name", catalog_root.resolve().name),
        "abbreviation": pointer.get("abbreviation", catalog_root.resolve().name[:4].upper()),
        "version": str(pointer.get("version", "0.0.0")),
        "status": pointer.get("status", "active"),
        "metamodel_version": str(pointer.get("metamodel_version", "unknown")),
        "description": str(pointer.get("description", "")),
        "repository": detect_repository_url(catalog_root),
        "owner": pointer.get("owner", DEFAULT_OWNER),
    }
    return metadata, warnings


def list_subtrees(catalog_root: Path) -> list[Path]:
    """CR-BP-mv1: list canonical record files in the containment tree.

    The iteration unit is the record file (`processes-*.yaml`), not the
    old per-entity flat directory. Every record file is one entity.
    """
    entities_root = catalog_root / "entities" / "v1-alpha"
    if not entities_root.exists():
        return []
    return sorted(entities_root.rglob("processes-*.yaml"))


def entity_id_from_subtree(subtree: Path) -> str:
    """CR-BP-mv1: derive the entity id from the record file's `id:` field.

    `subtree` here is the record file path (the iteration unit changed in
    CR-BP-mv1); the id lives inside the record, not in the directory name.
    """
    data = load_yaml(subtree) or {}
    return str(data.get("id", subtree.stem))


def read_canonical_yaml(subtree: Path, entity_id: str) -> dict[str, Any] | None:
    """CR-BP-mv1: load the canonical record file directly.

    `subtree` is the record file path in the containment tree; the record
    IS the canonical file, so this is a direct load.
    """
    return load_yaml(subtree)


def state_research_present(subtree: Path) -> bool:
    return (subtree / "research").is_dir() and any(
        p.is_file() for p in (subtree / "research").iterdir()
    )


def state_candidates_present(subtree: Path) -> bool:
    return (subtree / "candidates").is_dir() and any(
        p.is_file() for p in (subtree / "candidates").iterdir()
    )


def state_retired_present(subtree: Path) -> bool:
    return (subtree / "retired").is_dir() and any(
        p.is_file() for p in (subtree / "retired").iterdir()
    )


def infer_state(subtree: Path, canonical: dict[str, Any] | None) -> tuple[str, str | None]:
    """CR-BP-mv1: infer the entity's state from the record file.

    `subtree` is the record file path. Every record in the containment tree
    is canonical unless its lifecycle_status is retired. The record's own
    directory may carry research/ subdirectories (BP-era deposition state).
    """
    record_dir = subtree.parent
    canonical_path = None
    if subtree.exists():
        # Path relative to the catalog root (entities/v1-alpha/... form).
        parts = subtree.parts
        try:
            idx = parts.index("v1-alpha")
            canonical_path = str(Path("entities") / "v1-alpha" / Path(*parts[idx + 1:]))
        except ValueError:
            canonical_path = str(subtree)

    has_research = state_research_present(record_dir)
    has_candidates = state_candidates_present(record_dir)
    has_retired = state_retired_present(record_dir)

    if canonical is not None:
        lifecycle = canonical.get("lifecycle_status")
        if lifecycle in RETIRED_LIFECYCLE_STATUSES:
            return "retired", canonical_path
        return "canonical", canonical_path

    if has_candidates:
        return "candidate", canonical_path
    if has_research:
        return "research", canonical_path
    if has_retired:
        return "retired", canonical_path
    return "candidate", canonical_path


def count_regular_files(directory: Path) -> int:
    """Count regular files under a directory (recursive=False)."""
    if not directory.is_dir():
        return 0
    return sum(1 for p in directory.iterdir() if p.is_file())


def list_research_files(subtree: Path) -> list[str]:
    """Lexicographically sorted regular file names under research/."""
    research = subtree / "research"
    if not research.is_dir():
        return []
    return sorted(p.name for p in research.iterdir() if p.is_file())


def max_mtime_date(subtree: Path) -> str:
    """Max mtime across the subtree's regular files, formatted YYYY-MM-DD (UTC).

    Filesystem mtime is reset to checkout time on every `git checkout`,
    so on fresh-clone runs the returned date is the clone date, not the
    real last-edit date. Prefer :func:`git_last_commit_date` whenever
    the subtree is inside a git working tree.
    """
    from datetime import datetime, timezone

    latest = 0.0
    for path in subtree.rglob("*"):
        if path.is_file():
            try:
                latest = max(latest, path.stat().st_mtime)
            except OSError:
                continue
    if latest == 0.0:
        return "1970-01-01"
    return datetime.fromtimestamp(latest, tz=timezone.utc).strftime("%Y-%m-%d")


def git_last_commit_date(subtree: Path, repo_root: Path) -> str:
    """Last git commit date affecting any file under the subtree.

    Returns YYYY-MM-DD (UTC). Falls back to filesystem mtime when git
    is unavailable or the subtree is not under version control. Falls
    back to 1970-01-01 when neither path yields a value (defensive
    default for empty subtrees).

    This is the canonical source of truth for `last_modified`; it is
    stable across fresh clones (where filesystem mtime is reset to
    checkout time) and across long-running local checkouts (where
    filesystem mtime accumulates spurious updates). The same approach
    is used by `scripts/check_cr_metadata.py` for the §21 metadata
    cutoff probe (see PR-13 and docs/conformance-pipeline.md §9).
    """
    from datetime import datetime, timezone
    import subprocess

    if not (repo_root / ".git").exists():
        return max_mtime_date(subtree)

    try:
        out = subprocess.check_output(
            [
                "git", "-C", str(repo_root),
                "log", "-1", "--format=%ct",
                "--", str(subtree.relative_to(repo_root)),
            ],
            stderr=subprocess.DEVNULL,
            timeout=5,
        ).decode("utf-8", errors="replace").strip()
    except (subprocess.SubprocessError, OSError):
        return max_mtime_date(subtree)

    if not out.isdigit():
        return max_mtime_date(subtree)
    return datetime.fromtimestamp(int(out), tz=timezone.utc).strftime("%Y-%m-%d")


def entity_path_for(subtree: Path, state: str) -> str | None:
    """CR-BP-mv1: build the repo-relative path field for the entity entry.

    `subtree` is the record file path; the path field is the record file's
    repo-relative path (entities/v1-alpha/<cell>/.../processes-*.yaml).
    """
    parts = subtree.parts
    try:
        idx = parts.index("v1-alpha")
        return str(Path("entities") / "v1-alpha" / Path(*parts[idx + 1:]))
    except ValueError:
        return str(subtree)


def build_entity_entry(
    subtree: Path, catalog_root: Path, verbose: bool
) -> tuple[dict[str, Any], list[str]]:
    """Build one entities[] entry. Returns (entry, warnings).

    `last_modified` is read from the git last-commit date for the
    subtree (stable across fresh clones); falls back to filesystem
    mtime if git is unavailable. See `git_last_commit_date`.
    """
    warnings: list[str] = []
    entity_id = entity_id_from_subtree(subtree)
    canonical = read_canonical_yaml(subtree, entity_id)
    state, _canonical_path_from_infer = infer_state(subtree, canonical)
    path = entity_path_for(subtree, state)
    record_dir = subtree.parent

    if path is None:
        warnings.append(f"entity {entity_id!r} has no resolvable path; emitting raw path")

    if canonical is None:
        version = "0.0.0"
        lifecycle_status = "candidate"
        entity_type = "unknown"
    else:
        version = str(canonical.get("version", "0.0.0"))
        lifecycle_status = str(canonical.get("lifecycle_status", "unknown"))
        entity_type = str(canonical.get("type", "unknown"))

    entry: dict[str, Any] = {
        "id": entity_id,
        "type": entity_type,
        "state": state,
        "path": path,
        "research_count": count_regular_files(record_dir / "research"),
        "candidate_count": count_regular_files(record_dir / "candidates"),
        "canonical_count": 1 if subtree.exists() else 0,
        "retired_count": count_regular_files(record_dir / "retired"),
        "last_modified": git_last_commit_date(record_dir, catalog_root),
        "version": version,
        "lifecycle_status": lifecycle_status,
    }

    if verbose:
        print(
            f"  entity {entity_id}: state={state} type={entity_type} version={version} "
            f"research={entry['research_count']} candidates={entry['candidate_count']} "
            f"retired={entry['retired_count']}",
            file=sys.stderr,
        )

    return entry, warnings


def build_research_registers(entities: list[dict[str, Any]], catalog_root: Path) -> list[dict[str, Any]]:
    """Build research_registers[] from the entity entries.

    CR-BP-mv1: research/ dirs live under the owning record's directory in the
    containment tree (e.g. under a BP dir), not under flat per-entity dirs.
    """
    registers: list[dict[str, Any]] = []
    entities_root = catalog_root / "entities" / "v1-alpha"
    if not entities_root.exists():
        return registers
    by_dir = {}
    for entity in entities:
        p = entity.get("path")
        if isinstance(p, str) and not p.endswith("/"):
            by_dir[str(Path(p).parent)] = entity["id"]
    for research_dir in sorted(entities_root.rglob("research")):
        if not research_dir.is_dir():
            continue
        parent_rel = str(research_dir.parent.relative_to(entities_root))
        owner_key = str(Path("entities/v1-alpha") / parent_rel)
        owner_id = by_dir.get(owner_key)
        research_files = list_research_files(research_dir)
        registers.append(
            {
                "entity_id": owner_id or parent_rel,
                "path": f"{owner_key}/research/",
                "files": research_files,
            }
        )
    return registers


def count_open_change_requests(catalog_root: Path) -> int:
    """Count CR-*.md files in change-requests/ whose status is not 'Merged'.

    Heuristic: look for the word 'Merged' on the line immediately following
    the '# CR-...' heading. Files without a status line are conservatively
    counted as open.
    """
    cr_dir = catalog_root / "change-requests"
    if not cr_dir.is_dir():
        return 0
    open_count = 0
    for path in sorted(cr_dir.glob("CR-*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            open_count += 1
            continue
        # Take the first 30 lines; look for a status line.
        head = "\n".join(text.splitlines()[:30])
        if "Status**: Merged" in head or "Status**: Merged" in head:
            continue
        if "Status**: Proposed" in head or "Status**: Draft" in head:
            open_count += 1
            continue
        if "Status**:" in head:
            # Some other status (Accepted, Superseded, etc.): conservative: open.
            open_count += 1
            continue
        # No status line found: conservative open.
        open_count += 1
    return open_count


def build_payload(
    catalog_root: Path, schema: dict[str, Any], verbose: bool
) -> tuple[dict[str, Any], list[str]]:
    """Build the full CATALOG.yaml payload."""
    all_warnings: list[str] = []

    pointer = read_pointer(catalog_root)
    catalog_meta, meta_warnings = build_catalog_metadata(catalog_root, pointer, verbose)
    all_warnings.extend(meta_warnings)

    subtrees = list_subtrees(catalog_root)
    entities: list[dict[str, Any]] = []
    for subtree in subtrees:
        entity_id = entity_id_from_subtree(subtree)
        if not ENTITY_ID_PATTERN.match(entity_id):
            all_warnings.append(
                f"subtree name {entity_id!r} does not match the canonical entity id pattern; skipping"
            )
            continue
        entry, entry_warnings = build_entity_entry(
            subtree, catalog_root, verbose
        )
        entities.append(entry)
        all_warnings.extend(entry_warnings)

    entities.sort(key=lambda e: e["id"])
    research_registers = build_research_registers(entities, catalog_root)

    # Counts (recomputed deterministically).
    counts = {
        "entities": len(entities),
        "research_files": sum(e["research_count"] for e in entities),
        "candidates": sum(1 for e in entities if e["state"] == "candidate"),
        "canonical": sum(1 for e in entities if e["state"] == "canonical"),
        "retired": sum(1 for e in entities if e["state"] == "retired"),
        "open_change_requests": count_open_change_requests(catalog_root),
    }

    payload = {
        "catalog": {
            **catalog_meta,
            "entities": entities,
            "cross_cutting": dict(CROSS_CUTTING_PATHS),
            "counts": counts,
            "research_registers": research_registers,
        }
    }
    return payload, all_warnings


def validate_payload(payload: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    """Lightweight structural validation against the schema.

    The schema is JSON Schema draft-07. We do a minimal manual check
    (sufficient for the regenerator's contract); the gate
    (`tools/check_catalog_index.py`) is the authoritative validator and
    may pull in `jsonschema` if available, falling back to a manual check
    otherwise. Here we mirror that fallback so --check can exit 2 cleanly
    when the payload drifts.
    """
    errors: list[str] = []
    catalog = payload.get("catalog")
    if not isinstance(catalog, dict):
        return ["payload missing top-level 'catalog' object"]

    required = [
        "id", "name", "abbreviation", "version", "status", "metamodel_version",
        "description", "repository", "owner", "entities", "cross_cutting",
        "counts", "research_registers",
    ]
    for key in required:
        if key not in catalog:
            errors.append(f"catalog.{key} is required")

    entities = catalog.get("entities")
    if not isinstance(entities, list):
        errors.append("catalog.entities must be a list")
        return errors

    for idx, entity in enumerate(entities):
        if not isinstance(entity, dict):
            errors.append(f"catalog.entities[{idx}] is not an object")
            continue
        for key in [
            "id", "type", "state", "path", "research_count", "candidate_count",
            "canonical_count", "retired_count", "last_modified", "version",
            "lifecycle_status",
        ]:
            if key not in entity:
                errors.append(f"catalog.entities[{idx}].{key} is required")
        if entity.get("state") not in {"research", "candidate", "canonical", "retired"}:
            errors.append(f"catalog.entities[{idx}].state {entity.get('state')!r} not in enum")
        if entity.get("lifecycle_status") not in {"candidate", "active", "deprecated", "retired", "unknown"}:
            errors.append(
                f"catalog.entities[{idx}].lifecycle_status {entity.get('lifecycle_status')!r} not in enum"
            )
        if not isinstance(entity.get("last_modified", ""), str) or len(entity.get("last_modified", "")) != 10:
            errors.append(f"catalog.entities[{idx}].last_modified must be YYYY-MM-DD")

    counts = catalog.get("counts")
    if not isinstance(counts, dict):
        errors.append("catalog.counts must be an object")
    else:
        for key in ["entities", "research_files", "candidates", "canonical", "retired", "open_change_requests"]:
            if key not in counts:
                errors.append(f"catalog.counts.{key} is required")

    return errors


def render_yaml(payload: dict[str, Any]) -> str:
    """Render the payload as YAML, deterministically (sorted keys, block style)."""
    return yaml.safe_dump(
        payload,
        sort_keys=True,
        default_flow_style=False,
        allow_unicode=True,
        width=10000,  # disable line wrapping to keep entity entries on single lines
    )


def atomic_write(output_path: Path, content: str) -> None:
    """Write content to output_path atomically via tmp + os.replace."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = output_path.with_suffix(output_path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, output_path)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Regenerate CATALOG.yaml for a catalog repo (CR-CATALOG-STRUCT-06a)."
    )
    parser.add_argument(
        "--catalog-root",
        default=".",
        help="Path to the catalog repo root (default: current directory).",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output path (default: <catalog-root>/CATALOG.yaml).",
    )
    parser.add_argument(
        "--schema",
        default=DEFAULT_SCHEMA_PATH,
        help=f"Schema path relative to catalog-root (default: {DEFAULT_SCHEMA_PATH}).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 0 if committed CATALOG.yaml matches regenerator output; do not write.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the regenerated YAML to stdout; do not write.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print per-entity detection diagnostics to stderr.",
    )
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    catalog_root = Path(args.catalog_root).resolve()
    output_path = Path(args.output).resolve() if args.output else (catalog_root / "CATALOG.yaml")
    schema_path = (catalog_root / args.schema).resolve()

    if not catalog_root.is_dir():
        print(f"ERROR: catalog root {catalog_root} is not a directory", file=sys.stderr)
        return 1

    if not schema_path.exists():
        print(f"ERROR: schema not found at {schema_path}", file=sys.stderr)
        return 1

    try:
        schema = load_schema(schema_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read schema {schema_path}: {exc}", file=sys.stderr)
        return 1

    try:
        payload, warnings = build_payload(catalog_root, schema, args.verbose)
    except OSError as exc:
        print(f"ERROR: filesystem error while walking {catalog_root}: {exc}", file=sys.stderr)
        return 1

    errors = validate_payload(payload, schema)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 2

    rendered = render_yaml(payload)

    for warning in warnings:
        print(f"WARN: {warning}", file=sys.stderr)

    if args.dry_run:
        sys.stdout.write(rendered)
        return 0

    if args.check:
        if not output_path.exists():
            print(
                f"ERROR: {output_path} does not exist; run without --check to generate it",
                file=sys.stderr,
            )
            return 3
        committed = output_path.read_text(encoding="utf-8")
        if committed == rendered:
            print(f"OK: {output_path} is current")
            return 0
        print(
            f"ERROR: {output_path} is stale; run `python tools/regenerate_catalog.py` to refresh",
            file=sys.stderr,
        )
        return 3

    try:
        atomic_write(output_path, rendered)
    except OSError as exc:
        print(f"ERROR: cannot write {output_path}: {exc}", file=sys.stderr)
        return 1

    if args.verbose:
        print(f"OK: wrote {output_path} ({len(rendered)} bytes; {len(payload['catalog']['entities'])} entities)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
