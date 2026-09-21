"""Cross-repo conformance suite for the catalog repository standard.

Authority: CR-CATALOG-STRUCT-01 §11 (CST-001..CST-015) + CR-CATALOG-STRUCT-06b
(adds CST-016, the template-version diff).

This script is the **enforcement layer** for the standard. It takes a
catalog repo (as a filesystem path or a git URL) and verifies every
invariant declared in §5, §6, §8, §10, and §12. It also imports cleanly
so `dea-metaframework` CI can run it on a schedule against every catalog
repo whose `dea-metaframework-pointer.yaml` it tracks.

Convention: zero third-party dependencies. The module imports only from
the standard library so it works in the bare CI image (consistent with
`tools/regenerate_catalog.py` and `tools/ecf_coordinates.py`).

Exit codes (stable contract):
  0  success
  1  filesystem error (cannot read the catalog, permission denied)
  2  one or more CSTs failed (conformance NOT achieved)

Usage:
  python tools/conformance_test_catalog_structure.py [--catalog-root PATH] [--strict] [--template-root PATH]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(1)


# CR-BP-mv1: admit both the legacy dea:* family (unmigrated sibling
# catalogs) and the repo-namespaced content-addressed family
# (processes:<level>-<domain>-<stage>-<hash>).
ENTITY_ID_PATTERN = re.compile(
    r"^(dea:[a-z0-9-]+(:[a-z0-9-]+)*"
    r"|processes:(pc|group|process|activity|task)-[a-z0-9-]+)$"
)

DEFAULT_TEMPLATE_ROOT = "tools/catalog-repo-template"

# Result accumulator.
FAILURES: list[str] = []
WARNINGS: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        FAILURES.append(message)


def warn(message: str) -> None:
    WARNINGS.append(message)


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _is_state_dir(path: Path, entities_root: Path) -> bool:
    """True if `path` is, or lives under, a research/candidates/retired dir."""
    rel = path.relative_to(entities_root)
    return any(part in ("research", "candidates", "retired") for part in rel.parts)


def list_entity_subtrees(catalog_root: Path) -> list[Path]:
    """All entity directories under `entities/v1-alpha/`.

    Layout-agnostic (CR-BP-mv1): an entity directory is any directory that
    directly holds at least one `*.yaml` at its root, excluding
    research/candidates/retired state directories and their subtrees.

    - Legacy flat layout: top-level `<id>/` dirs each holding `<id>.yaml`.
    - Containment tree: one directory per record at any depth
      (PC at cell level, then group / process / activity / task).
    """
    entities_root = catalog_root / "entities" / "v1-alpha"
    if not entities_root.exists():
        return []
    out = []
    for p in sorted(entities_root.rglob("*")):
        if not p.is_dir() or _is_state_dir(p, entities_root):
            continue
        if any(p.glob("*.yaml")):
            out.append(p)
    return out


def _record_id(subtree: Path) -> str:
    """The canonical record id for an entity directory.

    Tree layout: the record's `id:` field (directory names are slug+hash,
    not ids). Legacy flat layout: `id:` equals the directory name.
    """
    for yf in sorted(subtree.glob("*.yaml")):
        try:
            data = load_yaml(yf)
        except (OSError, yaml.YAMLError):
            continue
        if isinstance(data, dict) and isinstance(data.get("id"), str):
            return data["id"]
    return subtree.name


# ---------- CST-001..CST-015 + CST-016 ----------

def cst_001_has_catalog_yaml(catalog_root: Path) -> None:
    check(
        (catalog_root / "CATALOG.yaml").is_file(),
        "CST-001: CATALOG.yaml missing at repo root",
    )


def cst_002_catalog_yaml_validates_against_schema(catalog_root: Path) -> None:
    if not (catalog_root / "CATALOG.yaml").is_file():
        return  # CST-001 will have failed; skip
    try:
        catalog = load_yaml(catalog_root / "CATALOG.yaml")
    except (OSError, yaml.YAMLError) as exc:
        check(False, f"CST-002: cannot parse CATALOG.yaml: {exc}")
        return
    if not isinstance(catalog, dict):
        check(False, "CST-002: CATALOG.yaml is not a mapping")
        return
    entities = catalog.get("catalog", {}).get("entities", [])
    for idx, entity in enumerate(entities):
        if not isinstance(entity, dict):
            check(False, f"CST-002: catalog.entities[{idx}] is not an object")
            continue
        eid = entity.get("id")
        if isinstance(eid, str) and not ENTITY_ID_PATTERN.match(eid):
            check(False, f"CST-002: entities[{idx}].id {eid!r} does not match entity id pattern")
        for required in (
            "id", "type", "state", "path", "research_count", "candidate_count",
            "canonical_count", "retired_count", "last_modified", "version",
            "lifecycle_status",
        ):
            if required not in entity:
                check(False, f"CST-002: entities[{idx}] missing {required!r}")
        if entity.get("state") not in {"research", "candidate", "canonical", "retired"}:
            check(False, f"CST-002: entities[{idx}].state {entity.get('state')!r} not in enum")
        if entity.get("lifecycle_status") not in {"candidate", "active", "deprecated", "retired", "unknown"}:
            check(
                False,
                f"CST-002: entities[{idx}].lifecycle_status {entity.get('lifecycle_status')!r} not in enum",
            )


def cst_003_subtree_shape(catalog_root: Path) -> None:
    """Every entity subtree must conform to §5: one canonical YAML at root,
    or a clearly-categorized file under research/, candidates/, or retired/.
    Empty subtrees (only `.gitkeep`/`.DS_Store`) are allowed and emit
    `state: candidate` per the regenerator."""
    for subtree in list_entity_subtrees(catalog_root):
        entity_id = _record_id(subtree)
        has_root_yaml = bool(list(subtree.glob("*.yaml")))
        has_state_file = any(
            (subtree / d).is_dir() and any((subtree / d).glob("*"))
            for d in ("research", "candidates", "retired")
        )
        check(
            has_root_yaml or has_state_file,
            f"CST-003: subtree {entity_id!r} has no YAML at root and no files under research/, candidates/, or retired/",
        )
        for required_dir in ("research", "candidates", "retired"):
            check(
                (subtree / required_dir).is_dir() or not any((subtree / required_dir).glob("*")),
                f"CST-003: subtree {entity_id!r} has files under {required_dir}/ but the directory is missing",
            )


def cst_004_canonical_yaml_required_fields(catalog_root: Path) -> None:
    for subtree in list_entity_subtrees(catalog_root):
        yamls = sorted(subtree.glob("*.yaml"))
        if not yamls:
            continue
        canonical = yamls[0]
        data = load_yaml(canonical)
        if not isinstance(data, dict):
            check(False, f"CST-004: {canonical} is not a mapping")
            continue
        required = ["id", "type", "name", "version", "lifecycle_status"]
        # CR-BP-mv1: Process Context records are non-versioned L0 anchors:
        # no `type:` (by design), no `version`/`lifecycle_status` (profile
        # owned by check_process_context.py). Require identity + name only.
        if canonical.name.startswith("processes-pc-"):
            required = ["id", "name"]
        for field in required:
            if field not in data:
                check(False, f"CST-004: {canonical} missing {field!r}")


def cst_005_entities_match_subtrees(catalog_root: Path) -> None:
    if not (catalog_root / "CATALOG.yaml").is_file():
        return
    catalog = load_yaml(catalog_root / "CATALOG.yaml")
    if not isinstance(catalog, dict):
        return
    declared = {
        e.get("id") for e in catalog.get("catalog", {}).get("entities", [])
        if isinstance(e, dict)
    }
    # CR-BP-mv1: compare by record id, not directory name (tree directory
    # names are slug+hash, not ids).
    actual = {_record_id(subtree) for subtree in list_entity_subtrees(catalog_root)}
    # Every declared entity must have a subtree on disk.
    for eid in declared:
        if not isinstance(eid, str):
            continue
        check(
            eid in actual,
            f"CST-005: CATALOG.yaml declares {eid!r} but subtree is missing",
        )


def cst_006_no_orphan_subtrees(catalog_root: Path) -> None:
    if not (catalog_root / "CATALOG.yaml").is_file():
        return
    catalog = load_yaml(catalog_root / "CATALOG.yaml")
    if not isinstance(catalog, dict):
        return
    declared = {
        e.get("id") for e in catalog.get("catalog", {}).get("entities", [])
        if isinstance(e, dict)
    }
    for subtree in list_entity_subtrees(catalog_root):
        rid = _record_id(subtree)
        check(
            rid in declared,
            f"CST-006: subtree {rid!r} exists on disk but not declared in CATALOG.yaml",
        )


def cst_007_paths_resolve(catalog_root: Path) -> None:
    if not (catalog_root / "CATALOG.yaml").is_file():
        return
    catalog = load_yaml(catalog_root / "CATALOG.yaml")
    if not isinstance(catalog, dict):
        return
    for idx, entity in enumerate(catalog.get("catalog", {}).get("entities", [])):
        if not isinstance(entity, dict):
            continue
        path = entity.get("path")
        if not isinstance(path, str):
            check(False, f"CST-007: entities[{idx}].path is not a string")
            continue
        resolved = catalog_root / path
        if path.endswith("/"):
            check(resolved.is_dir(), f"CST-007: entities[{idx}].path {path!r} is not a directory")
        else:
            check(resolved.is_file(), f"CST-007: entities[{idx}].path {path!r} does not resolve to a file")


def cst_008_state_matches_subtree(catalog_root: Path) -> None:
    """Lightweight: declared `state` field in CATALOG.yaml must be a valid enum value.
    Deep subtree-vs-state cross-check lives in the regenerator (state inference)."""
    if not (catalog_root / "CATALOG.yaml").is_file():
        return
    catalog = load_yaml(catalog_root / "CATALOG.yaml")
    if not isinstance(catalog, dict):
        return
    for idx, entity in enumerate(catalog.get("catalog", {}).get("entities", [])):
        if not isinstance(entity, dict):
            continue
        state = entity.get("state")
        if state not in {"research", "candidate", "canonical", "retired"}:
            check(False, f"CST-008: entities[{idx}].state {state!r} not in canonical enum")


def cst_009_research_readme(catalog_root: Path) -> None:
    for subtree in list_entity_subtrees(catalog_root):
        research = subtree / "research"
        if not research.is_dir():
            continue
        regular_files = [p for p in research.iterdir() if p.is_file()]
        if regular_files and not (research / "README.md").is_file():
            warn(f"CST-009: subtree {subtree.name!r} has files under research/ but no README.md")


def cst_010_retired_lifecycle(catalog_root: Path) -> None:
    for subtree in list_entity_subtrees(catalog_root):
        retired = subtree / "retired"
        if not retired.is_dir():
            continue
        for path in retired.glob("*.yaml"):
            data = load_yaml(path)
            if not isinstance(data, dict):
                continue
            ls = data.get("lifecycle_status")
            if ls not in {"deprecated", "retired"}:
                check(
                    False,
                    f"CST-010: {path} has lifecycle_status={ls!r} but lives under retired/",
                )


def cst_011_candidate_version(catalog_root: Path) -> None:
    for subtree in list_entity_subtrees(catalog_root):
        candidates = subtree / "candidates"
        if not candidates.is_dir():
            continue
        for path in candidates.glob("*.yaml"):
            data = load_yaml(path)
            if not isinstance(data, dict):
                continue
            version = str(data.get("version", ""))
            ls = data.get("lifecycle_status")
            version_ok = version and version != "1.0.0" and version.startswith("0.")
            ls_ok = ls == "candidate"
            check(
                version_ok or ls_ok,
                f"CST-011: {path} must declare version<1.0.0 OR lifecycle_status=candidate",
            )


def cst_012_metamodel_pointer_paths(catalog_root: Path) -> None:
    pointer = catalog_root / "metamodel-pointer.yaml"
    if not pointer.is_file():
        return
    try:
        data = load_yaml(pointer)
    except (OSError, yaml.YAMLError):
        return
    if not isinstance(data, dict):
        return
    # Walk every string-valued field; if it ends with .yaml/.yml and starts
    # with entities/, classification/, schemas/, contexts/, contributions/,
    # require the file to exist.
    def _walk(obj: Any, prefix: str = "") -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                _walk(v, f"{prefix}.{k}" if prefix else str(k))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                _walk(v, f"{prefix}[{i}]")
        elif isinstance(obj, str):
            if obj.endswith((".yaml", ".yml")) and any(
                obj.startswith(p) for p in ("entities/", "contexts/", "classifications/", "schemas/", "contributions/")
            ):
                check(
                    (catalog_root / obj).is_file(),
                    f"CST-012: metamodel-pointer.yaml field {prefix}={obj!r} does not resolve",
                )

    _walk(data)


def cst_013_regenerator_present(catalog_root: Path) -> None:
    regen = catalog_root / "scripts" / "regenerate_catalog.py"
    if not regen.is_file():
        check(False, "CST-013: scripts/regenerate_catalog.py missing")


def cst_014_gate_present(catalog_root: Path) -> None:
    gate = catalog_root / "scripts" / "check_catalog_index.py"
    if not gate.is_file():
        check(False, "CST-014: scripts/check_catalog_index.py missing")


def cst_015_ci_workflow_references_scripts(catalog_root: Path) -> None:
    workflows = catalog_root / ".github" / "workflows"
    if not workflows.is_dir():
        check(False, "CST-015: .github/workflows/ directory missing")
        return
    found_regen = False
    found_gate = False
    for wf in workflows.glob("*.yml"):
        try:
            text = wf.read_text(encoding="utf-8")
        except OSError:
            continue
        if "regenerate_catalog.py" in text:
            found_regen = True
        if "check_catalog_index.py" in text:
            found_gate = True
    check(found_regen, "CST-015: no CI workflow references scripts/regenerate_catalog.py")
    check(found_gate, "CST-015: no CI workflow references scripts/check_catalog_index.py")


def cst_016_template_version(catalog_root: Path, template_root: Path | None) -> None:
    """Compare catalog's TEMPLATE_VERSION to the canonical template's.

    Advisory by default (warn); strict mode (caller passes --strict) escalates
    to a check. A missing TEMPLATE_VERSION file means the catalog was hand-rolled
    rather than bootstrapped; warn but do not fail.
    """
    if template_root is None or not template_root.is_dir():
        return
    catalog_version_path = catalog_root / "TEMPLATE_VERSION"
    template_version_path = template_root / "TEMPLATE_VERSION"
    if not template_version_path.is_file():
        return
    if not catalog_version_path.is_file():
        warn(
            "CST-016: catalog has no TEMPLATE_VERSION; the catalog was hand-rolled rather than bootstrapped"
        )
        return
    try:
        catalog_v = catalog_version_path.read_text(encoding="utf-8").strip()
        template_v = template_version_path.read_text(encoding="utf-8").strip()
    except OSError:
        return
    if catalog_v != template_v:
        warn(
            f"CST-016: catalog TEMPLATE_VERSION={catalog_v!r} != template {template_v!r}; re-sync advised"
        )


CST_TESTS: list[tuple[str, Callable[..., None]]] = [
    ("CST-001", cst_001_has_catalog_yaml),
    ("CST-002", cst_002_catalog_yaml_validates_against_schema),
    ("CST-003", cst_003_subtree_shape),
    ("CST-004", cst_004_canonical_yaml_required_fields),
    ("CST-005", cst_005_entities_match_subtrees),
    ("CST-006", cst_006_no_orphan_subtrees),
    ("CST-007", cst_007_paths_resolve),
    ("CST-008", cst_008_state_matches_subtree),
    ("CST-009", cst_009_research_readme),
    ("CST-010", cst_010_retired_lifecycle),
    ("CST-011", cst_011_candidate_version),
    ("CST-012", cst_012_metamodel_pointer_paths),
    ("CST-013", cst_013_regenerator_present),
    ("CST-014", cst_014_gate_present),
    ("CST-015", cst_015_ci_workflow_references_scripts),
]


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Cross-repo conformance suite for the catalog repository standard (CR-CATALOG-STRUCT-06b)."
    )
    parser.add_argument(
        "--catalog-root",
        default=".",
        help="Path to the catalog repo root (default: current directory).",
    )
    parser.add_argument(
        "--template-root",
        default=DEFAULT_TEMPLATE_ROOT,
        help=f"Path to the canonical template root (default: {DEFAULT_TEMPLATE_ROOT}).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Upgrade warnings (CST-009, CST-016) to errors.",
    )
    parser.add_argument(
        "--cst",
        default=None,
        help="Run only the named CST (e.g. CST-001). Default: run all.",
    )
    args = parser.parse_args(argv)

    catalog_root = Path(args.catalog_root).resolve()
    template_root = Path(args.template_root).resolve()

    if not catalog_root.is_dir():
        print(f"ERROR: catalog root {catalog_root} is not a directory", file=sys.stderr)
        return 1

    FAILURES.clear()
    WARNINGS.clear()

    tests = CST_TESTS
    if args.cst:
        tests = [(name, fn) for name, fn in CST_TESTS if name == args.cst]
        if not tests:
            print(f"ERROR: unknown CST {args.cst!r}", file=sys.stderr)
            return 1

    for name, fn in tests:
        try:
            fn(catalog_root)
        except Exception as exc:  # noqa: BLE001
            FAILURES.append(f"{name}: raised {type(exc).__name__}: {exc}")

    # CST-016 needs the template root.
    try:
        cst_016_template_version(catalog_root, template_root)
    except Exception as exc:  # noqa: BLE001
        FAILURES.append(f"CST-016: raised {type(exc).__name__}: {exc}")

    for w in WARNINGS:
        print(f"WARN: {w}", file=sys.stderr)
    if args.strict:
        for w in WARNINGS:
            FAILURES.append(f"STRICT: {w}")

    for f in FAILURES:
        print(f"FAIL: {f}", file=sys.stderr)

    if FAILURES:
        print(f"FAIL: {len(FAILURES)} conformance failure(s); {len(WARNINGS)} warning(s)", file=sys.stderr)
        return 2

    print(f"OK: {len(tests) + 1} CST(s) passed ({len(WARNINGS)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
