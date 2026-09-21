"""CATALOG.yaml gate (CR-CATALOG-STRUCT-06a).

Validates the committed `CATALOG.yaml` against the JSON Schema and runs
structural sanity checks. The gate is read-only; it does NOT regenerate
the file. If `CATALOG.yaml` is stale, the gate tells the caller to run
the regenerator.

Convention: zero third-party dependencies at minimum. The module tries
to import `jsonschema` (commonly available in catalog repo CI images);
if absent, it falls back to a manual structural check that mirrors the
schema's required/optional contract.

Exit codes (stable contract):
  0  success
  1  schema validation failed
  2  structural sanity failure (path missing, id mismatch, orphan, etc.)
  3  unused (regenerator owns this code)

Usage:
  python tools/check_catalog_index.py [--catalog-root PATH] [--strict] [--schema PATH]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(1)

try:
    from jsonschema import Draft7Validator as _Draft7Validator  # type: ignore
    HAVE_JSONSCHEMA = True
except ImportError:
    _Draft7Validator = None  # type: ignore
    HAVE_JSONSCHEMA = False


# Re-export at module scope for type checkers.
Draft7Validator = _Draft7Validator

DEFAULT_SCHEMA_PATH = "catalog-index-schema/catalog-index-schema.json"

ENTITY_ID_PATTERN = re.compile(r"^processes:[a-z0-9-]+$")


def load_schema(schema_path: Path) -> dict[str, Any]:
    with schema_path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def list_subtrees(catalog_root: Path) -> list[Path]:
    """List every directory under `entities/v1-alpha/`; sorted lexicographically."""
    entities_root = catalog_root / "entities" / "v1-alpha"
    if not entities_root.exists():
        return []
    return sorted([p for p in entities_root.iterdir() if p.is_dir()])


def schema_validate(payload: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    """Validate `payload` against `schema`; return list of error messages."""
    if HAVE_JSONSCHEMA and Draft7Validator is not None:
        validator = Draft7Validator(schema)
        return [f"{'/'.join(str(p) for p in err.absolute_path) or '<root>'}: {err.message}" for err in validator.iter_errors(payload)]
    # Manual fallback: enforce required keys and enum values; sufficient for
    # the gate's contract (the regenerator's `validate_payload` is the
    # source of truth on this same shape).
    errors: list[str] = []
    catalog = payload.get("catalog")
    if not isinstance(catalog, dict):
        return ["<root>.catalog: must be an object"]
    for key in [
        "id", "name", "abbreviation", "version", "status", "metamodel_version",
        "description", "repository", "owner", "entities", "cross_cutting",
        "counts", "research_registers",
    ]:
        if key not in catalog:
            errors.append(f"catalog.{key}: required")
    entities = catalog.get("entities")
    if isinstance(entities, list):
        for idx, entity in enumerate(entities):
            if not isinstance(entity, dict):
                errors.append(f"catalog.entities[{idx}]: must be an object")
                continue
            for key in [
                "id", "type", "state", "path", "research_count", "candidate_count",
                "canonical_count", "retired_count", "last_modified", "version",
                "lifecycle_status",
            ]:
                if key not in entity:
                    errors.append(f"catalog.entities[{idx}].{key}: required")
            if entity.get("state") not in {"research", "candidate", "canonical", "retired"}:
                errors.append(f"catalog.entities[{idx}].state: {entity.get('state')!r} not in enum")
            if entity.get("lifecycle_status") not in {"candidate", "active", "deprecated", "retired", "unknown"}:
                errors.append(
                    f"catalog.entities[{idx}].lifecycle_status: {entity.get('lifecycle_status')!r} not in enum"
                )
    return errors


def structural_sanity(
    payload: dict[str, Any], catalog_root: Path
) -> tuple[list[str], list[str]]:
    """Run structural sanity checks beyond schema validation.

    Returns (errors, warnings). Errors block exit 0; warnings only block
    in `--strict` mode.
    """
    errors: list[str] = []
    warnings: list[str] = []
    catalog = payload.get("catalog")
    if not isinstance(catalog, dict):
        return ["payload missing catalog object"], []

    entities = catalog.get("entities", [])
    declared_ids: set[str] = set()

    for idx, entity in enumerate(entities):
        if not isinstance(entity, dict):
            continue
        eid = entity.get("id")
        path = entity.get("path")
        if isinstance(eid, str):
            declared_ids.add(eid)
            if not ENTITY_ID_PATTERN.match(eid):
                errors.append(f"entities[{idx}].id {eid!r}: does not match entity id pattern")
        if isinstance(path, str):
            resolved = catalog_root / path
            # Allow trailing-slash subtree roots (no file resolution).
            if path.endswith("/"):
                if not resolved.is_dir():
                    errors.append(f"entities[{idx}].path {path!r}: directory missing at {resolved}")
            else:
                if not resolved.is_file():
                    errors.append(f"entities[{idx}].path {path!r}: file missing at {resolved}")

    # CST-006 (forwarded to STRUCT-06b): every record file on disk is enumerated.
    entities_root = catalog_root / "entities" / "v1-alpha"
    if entities_root.exists():
        for record_file in sorted(entities_root.rglob("processes-*.yaml")):
            data = load_yaml(record_file) or {}
            rid = data.get("id")
            if isinstance(rid, str) and rid not in declared_ids:
                errors.append(f"record {rid!r}: exists on disk at {record_file} but not declared in CATALOG.yaml (orphan)")

    # research/ subdirectories SHOULD have README.md if non-empty (CST-009).
    if entities_root.exists():
        for research in sorted(entities_root.rglob("research")):
            if not research.is_dir():
                continue
            regular_files = [p for p in research.iterdir() if p.is_file()]
            if regular_files and not (research / "README.md").exists():
                warnings.append(
                    f"research dir {research}: non-empty but missing README.md"
                )

    # cross_cutting paths should exist (or be deliberately absent during scaffolding).
    cross_cutting = catalog.get("cross_cutting", {})
    if isinstance(cross_cutting, dict):
        for label, rel in cross_cutting.items():
            if not isinstance(rel, str):
                continue
            target = catalog_root / rel
            if not target.exists():
                warnings.append(f"cross_cutting.{label}: path {rel!r} not found at {target}")

    # counts must match entity array (cheap aggregate check).
    counts = catalog.get("counts", {})
    if isinstance(counts, dict):
        declared_total = len(entities)
        if counts.get("entities") != declared_total:
            errors.append(
                f"counts.entities {counts.get('entities')} != len(entities) {declared_total}"
            )
        if isinstance(counts.get("canonical"), int):
            actual_canonical = sum(1 for e in entities if isinstance(e, dict) and e.get("state") == "canonical")
            if counts["canonical"] != actual_canonical:
                errors.append(
                    f"counts.canonical {counts['canonical']} != actual {actual_canonical}"
                )

    return errors, warnings


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate CATALOG.yaml for a catalog repo (CR-CATALOG-STRUCT-06a)."
    )
    parser.add_argument(
        "--catalog-root",
        default=".",
        help="Path to the catalog repo root (default: current directory).",
    )
    parser.add_argument(
        "--schema",
        default=DEFAULT_SCHEMA_PATH,
        help=f"Schema path relative to catalog-root (default: {DEFAULT_SCHEMA_PATH}).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Upgrade warnings to errors.",
    )
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    catalog_root = Path(args.catalog_root).resolve()
    schema_path = (catalog_root / args.schema).resolve()
    catalog_path = catalog_root / "CATALOG.yaml"

    if not catalog_root.is_dir():
        print(f"ERROR: catalog root {catalog_root} is not a directory", file=sys.stderr)
        return 1
    if not schema_path.exists():
        print(f"ERROR: schema not found at {schema_path}", file=sys.stderr)
        return 1
    if not catalog_path.exists():
        print(f"ERROR: CATALOG.yaml not found at {catalog_path}", file=sys.stderr)
        return 1

    try:
        schema = load_schema(schema_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read schema {schema_path}: {exc}", file=sys.stderr)
        return 1
    try:
        payload = load_yaml(catalog_path)
    except (OSError, yaml.YAMLError) as exc:
        print(f"ERROR: cannot read {catalog_path}: {exc}", file=sys.stderr)
        return 1

    if not isinstance(payload, dict):
        print(f"ERROR: {catalog_path} did not parse to a YAML mapping", file=sys.stderr)
        return 1

    # Phase 1: schema validation.
    schema_errors = schema_validate(payload, schema)
    if schema_errors:
        for err in schema_errors:
            print(f"SCHEMA: {err}", file=sys.stderr)
        return 1

    # Phase 2: structural sanity.
    sanity_errors, warnings = structural_sanity(payload, catalog_root)
    for warning in warnings:
        print(f"WARN: {warning}", file=sys.stderr)
    if sanity_errors:
        for err in sanity_errors:
            print(f"SANITY: {err}", file=sys.stderr)
        return 2

    if args.strict and warnings:
        print(f"ERROR: --strict mode and {len(warnings)} warning(s) present", file=sys.stderr)
        return 2

    if not HAVE_JSONSCHEMA:
        print(
            "NOTE: jsonschema package not installed; ran manual fallback validation. "
            "Install jsonschema for full draft-07 coverage.",
            file=sys.stderr,
        )

    entities_count = len(payload.get("catalog", {}).get("entities", []))
    print(f"OK: CATALOG.yaml validates ({entities_count} entities)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
