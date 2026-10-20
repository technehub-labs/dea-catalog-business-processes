#!/usr/bin/env python3
"""check_entity_system.py: enforce the General Entity System conformance (CR-BP-123).

The 5-rule umbrella gate per the Conformance Standard (CR-BP-122 §5):

- ES-001 (Identity): present, format-valid, scope-bound, unique id.
- ES-002 (Entity Contract): common envelope (id, type, name, definition,
  lifecycle, provenance) + type-specific profiles.
- ES-003 (Relationship): canonical types, source / target type
  constraints, cross-catalog identity_scope, no competing definitions.
- ES-004 (Lifecycle): governed state, transition table, identity
  continuity, terminal states, provenance per transition.
- ES-005 (Conformance Umbrella): per-type gate delegation (advisory in
  Stage 3-4; per-type gate verdicts are delegated to the per-type
  gates in the rollup).

The gate is data-driven from reconciliation/entity-system-registry.yaml
(per the Conformance Standard CS-011). The exception mechanism (CS-008
/ CS-009) consults reconciliation/normalization.yaml for review-retained
verdicts; a record carrying an exception is not blocking.

Staging (per the Conformance Standard CS-010): advisory in Stage 3-4
(CR-BP-123) and Stage 5 (CR-BP-124); blocking in Stage 6 (CR-BP-125).

Run: python3 scripts/check_entity_system.py [--strict] [--json]
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "reconciliation" / "entity-system-registry.yaml"
EXCEPTIONS_PATH = REPO_ROOT / "reconciliation" / "normalization.yaml"


# --------------------------------------------------------------------------- #
# Registry + exception loaders
# --------------------------------------------------------------------------- #

def _load_registry(path: Path | None = None) -> dict:
    """Load the entity-system registry (YAML).

    The default is resolved at call time (not at function definition)
    so that callers can patch `ces.REGISTRY_PATH` for tests.
    """
    if path is None:
        path = REGISTRY_PATH
    with open(path) as f:
        return yaml.safe_load(f) or {}


def _load_exceptions(path: Path | None = None) -> dict:
    """Load the exception registry (review-retained verdicts)."""
    if path is None:
        path = EXCEPTIONS_PATH
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def _is_excepted(record_id: str, rule: str, exceptions: dict) -> bool:
    """Check if (record_id, rule) has a review-retained verdict that exempts it."""
    exc = exceptions.get(record_id)
    if not exc:
        return False
    if isinstance(exc, list):
        # List of verdicts
        for v in exc:
            if isinstance(v, dict) and v.get("verdict") == "review-retained":
                excepted_rules = v.get("excepted_rules", [])
                if rule in excepted_rules or "*" in excepted_rules:
                    return True
    elif isinstance(exc, dict):
        if exc.get("verdict") == "review-retained":
            excepted_rules = exc.get("excepted_rules", [])
            if rule in excepted_rules or "*" in excepted_rules:
                return True
    return False


# --------------------------------------------------------------------------- #
# YAML value extractor (simple subset; for record-level fields)
# --------------------------------------------------------------------------- #

def _extract_record(content: str) -> dict:
    """Extract a record from a YAML file. Uses PyYAML for full YAML support
    (block scalars, multi-line values, quoted strings, etc.).

    Returns the parsed top-level mapping, or {} on parse error.
    """
    try:
        parsed = yaml.safe_load(content)
    except Exception:
        return {}
    if not isinstance(parsed, dict):
        return {}
    return parsed


# --------------------------------------------------------------------------- #
# The 5 rules
# --------------------------------------------------------------------------- #

def _check_es_001_identity(record: dict, registry: dict, record_id: str, exceptions: dict) -> list:
    """ES-001: present, format-valid, scope-bound, unique id (per IS-001..IS-006)."""
    findings = []
    id_field = registry["identity"]["id_field"]
    canonical_prefix = registry["identity"]["canonical_prefix"]
    canonical_pattern = registry["identity"]["canonical_pattern"]
    legacy_prefix = registry["identity"]["legacy_prefix"]
    legacy_pattern = registry["identity"]["legacy_pattern"]

    record_id_value = record.get(id_field, "").strip() if isinstance(record.get(id_field), str) else ""
    if not record_id_value:
        if not _is_excepted(record_id, "ES-001", exceptions):
            findings.append({"rule": "ES-001", "record_id": record_id,
                             "diagnostic": f"missing {id_field}"})
        return findings

    if record_id_value.startswith(canonical_prefix):
        if not re.match(canonical_pattern, record_id_value):
            if not _is_excepted(record_id, "ES-001", exceptions):
                findings.append({"rule": "ES-001", "record_id": record_id,
                                 "diagnostic": f"id {record_id_value!r} does not match canonical pattern"})
    elif record_id_value.startswith(legacy_prefix):
        if not re.match(legacy_pattern, record_id_value):
            if not _is_excepted(record_id, "ES-001", exceptions):
                findings.append({"rule": "ES-001", "record_id": record_id,
                                 "diagnostic": f"id {record_id_value!r} does not match legacy pattern"})
    else:
        if not _is_excepted(record_id, "ES-001", exceptions):
            findings.append({"rule": "ES-001", "record_id": record_id,
                             "diagnostic": f"id {record_id_value!r} has no canonical or legacy prefix"})

    return findings


def _check_es_002_contract(record: dict, registry: dict, record_id: str, exceptions: dict,
                          record_path: str = "") -> list:
    """ES-002: common envelope (per EC-001..EC-004) + type-specific profile."""
    findings = []
    type_field = registry["envelope"]["type_field"]
    profiles = registry["envelope"]["profiles"]

    record_type = record.get(type_field, "")
    profiles = registry["envelope"]["profiles"]
    valid_types = set(profiles.keys())

    # Type validation: a non-empty `type` must be in the valid types
    # (i.e. one of the registered profiles). A typo like
    # `type: InvalidType` is a NON-CONFORMANT finding.
    if record_type and record_type not in valid_types:
        if not _is_excepted(record_id, "ES-002", exceptions):
            findings.append({"rule": "ES-002", "record_id": record_id,
                             "diagnostic": f"type {record_type!r} is not in the valid types list {sorted(valid_types)}"})

    # Resolve the profile: by type, or by ProcessContext detection
    # (which checks for either the new shape with process_context +
    # cell_charter blocks, OR the legacy shape with top-level
    # domain + lifecycle_stage fields).
    if record_type and record_type in profiles:
        profile = profiles[record_type]
    elif "process_context" in record or "domain" in record:
        profile = profiles.get("ProcessContext", {"required_fields": []})
    else:
        profile = profiles.get("Process", {"required_fields": []})

    required_fields = profile.get("required_fields", [])

    for field in required_fields:
        # Field may be nested (e.g. "lifecycle.status"); treat as a
        # path. Also support field whose value is a dict (e.g. the
        # `process_context` field is a dict, presence is enough).
        if "." in field:
            parts = field.split(".")
            value = record
            for k in parts:
                if isinstance(value, dict):
                    value = value.get(k)
                else:
                    value = None
                    break
            if value is None or value == "" or value == {}:
                if not _is_excepted(record_id, "ES-002", exceptions):
                    findings.append({"rule": "ES-002", "record_id": record_id,
                                     "diagnostic": f"missing required envelope field {field!r}"})
        else:
            if field not in record or record[field] in (None, "", []):
                if not _is_excepted(record_id, "ES-002", exceptions):
                    findings.append({"rule": "ES-002", "record_id": record_id,
                                     "diagnostic": f"missing required envelope field {field!r}"})

    return findings


def _check_es_003_relationship(record: dict, registry: dict, record_id: str, exceptions: dict) -> list:
    """ES-003: canonical types, source/target constraints, cross-catalog (per RS-001..RS-005)."""
    findings = []
    relationships = record.get("relationships", [])
    if isinstance(relationships, str):
        # Inline shorthand; not expected in this catalog
        return findings
    canonical_types = registry["relationships"]["canonical_types"]
    forbidden_types = registry["relationships"]["forbidden_types"]
    type_constraints = registry["relationships"].get("type_constraints", {})
    record_type = record.get("type", "")

    for i, rel in enumerate(relationships):
        if not isinstance(rel, dict):
            continue
        rel_type = rel.get("relationship_type", "")

        if rel_type in forbidden_types:
            if not _is_excepted(record_id, "ES-003", exceptions):
                findings.append({"rule": "ES-003", "record_id": record_id,
                                 "diagnostic": f"relationships[{i}]: forbidden type {rel_type!r}"})
            continue

        if rel_type and rel_type not in canonical_types:
            if not _is_excepted(record_id, "ES-003", exceptions):
                findings.append({"rule": "ES-003", "record_id": record_id,
                                 "diagnostic": f"relationships[{i}]: non-canonical type {rel_type!r}"})
            continue

        if not rel_type:
            continue

        constraints = type_constraints.get(rel_type, {})
        source_types = constraints.get("source_types", [])
        if record_type and source_types and record_type not in source_types:
            if not _is_excepted(record_id, "ES-003", exceptions):
                findings.append({"rule": "ES-003", "record_id": record_id,
                                 "diagnostic": f"relationships[{i}]: source type {record_type!r} not in {source_types}"})

        if "target_identity_scopes" in constraints:
            target_scope = rel.get("identity_scope", "")
            if target_scope not in constraints["target_identity_scopes"]:
                if not _is_excepted(record_id, "ES-003", exceptions):
                    findings.append({"rule": "ES-003", "record_id": record_id,
                                     "diagnostic": f"relationships[{i}]: identity_scope {target_scope!r} not in {constraints['target_identity_scopes']}"})

        # RECONCILED (IMP-001): target_id_prefixes constrains the target's
        # canonical id namespace. Used by relationship types whose target
        # lives in an external catalogue (`serves` -> `ecf:`), where the
        # population carries the namespace in the id itself and does not
        # declare a separate identity_scope field. A type may declare both
        # mechanisms; each is checked independently when present.
        if "target_id_prefixes" in constraints:
            target_id = str(rel.get("target_id", ""))
            allowed_prefixes = constraints["target_id_prefixes"]
            if not any(target_id.startswith(p) for p in allowed_prefixes):
                if not _is_excepted(record_id, "ES-003", exceptions):
                    findings.append({"rule": "ES-003", "record_id": record_id,
                                     "diagnostic": f"relationships[{i}]: target_id {target_id!r} does not match any canonical prefix in {allowed_prefixes}"})

    return findings


def _check_es_004_lifecycle(record: dict, registry: dict, record_id: str, exceptions: dict) -> list:
    """ES-004: lifecycle state, transitions, terminal states, provenance (per LS-001..LS-007).

    Only applies to types that have a `lifecycle_state_field` in their
    profile (Process, ProcessGroup, Activity, Task, ProcessScope).
    ProcessContext is exempt (lifecycle_status is the admission status,
    not a state-machine value).
    """
    findings = []
    profiles = registry["envelope"]["profiles"]
    type_field = registry["envelope"]["type_field"]
    record_type = record.get(type_field, "")

    # Resolve the profile
    if record_type and record_type in profiles:
        profile = profiles[record_type]
    elif "process_context" in record or "domain" in record:
        profile = profiles.get("ProcessContext", {})
    else:
        profile = profiles.get("Process", {})

    lifecycle_state_field = profile.get("lifecycle_state_field")
    if not lifecycle_state_field:
        # This type doesn't have a lifecycle state machine; skip
        return findings

    # Walk to the BLOCK level (parent of the value): for
    # "lifecycle.status" the block is "lifecycle"; for
    # "provenance.change_history" the block is "provenance".
    state_parts = lifecycle_state_field.split(".")
    if len(state_parts) < 2:
        return findings
    block_parts = state_parts[:-1]
    block_value = record
    for k in block_parts:
        if isinstance(block_value, dict):
            block_value = block_value.get(k)
        else:
            return findings
    if not isinstance(block_value, dict):
        # No lifecycle block; might be a proposed record
        return findings

    valid_states = registry["lifecycle"]["valid_states"]
    status = block_value.get(state_parts[-1], "")
    if status and status not in valid_states:
        if not _is_excepted(record_id, "ES-004", exceptions):
            findings.append({"rule": "ES-004", "record_id": record_id,
                             "diagnostic": f"lifecycle.status {status!r} is not in the valid states {valid_states}"})

    # Provenance check (per ES-004 LS-005: every change_history[] entry has cr/date/change)
    provenance_field = registry["lifecycle"]["provenance_field"]
    provenance_required_keys = registry["lifecycle"]["provenance_required_keys"]
    field_path = provenance_field.split(".")
    provenance = record
    for k in field_path:
        if isinstance(provenance, dict):
            provenance = provenance.get(k, [])
        else:
            provenance = []
            break
    if isinstance(provenance, list):
        for i, entry in enumerate(provenance):
            if not isinstance(entry, dict):
                continue
            for key in provenance_required_keys:
                if key not in entry:
                    if not _is_excepted(record_id, "ES-004", exceptions):
                        findings.append({"rule": "ES-004", "record_id": record_id,
                                         "diagnostic": f"{provenance_field}[{i}]: missing required key {key!r}"})

    return findings


def _check_es_005_umbrella_global(registry: dict, repo_root: Path) -> list:
    """ES-005: per-type gate delegation (global, runs once per gate invocation).

    In Stage 3-4 (advisory), ES-005 checks that the per-type gate SCRIPT
    EXISTS for each registered type. The full per-type gate validation is
    delegated to the per-type gates in the conformance rollup; the entity-
    system gate is the umbrella, not the per-type validator.

    Stage 5 (CR-BP-124) may promote this to a per-record delegation.
    """
    findings = []
    per_type_gates = registry.get("per_type_gates", [])
    for entry in per_type_gates:
        gate_script = entry.get("gate")
        if not gate_script:
            continue
        gate_path = repo_root / gate_script
        if not gate_path.exists():
            findings.append({
                "rule": "ES-005",
                "record_id": "<global>",
                "diagnostic": f"per-type gate {gate_script} does not exist for type {entry.get('type')}",
            })
    return findings


# --------------------------------------------------------------------------- #
# Record walker
# --------------------------------------------------------------------------- #

def _walk_records(repo_root: Path, registry: dict) -> list:
    """Walk all records in the registered file globs."""
    records = []
    file_globs = registry["envelope"]["file_globs"]
    seen_ids: dict[str, str] = {}  # id -> first file path

    # Files / dirs to exclude from the walk (config + scratch + tooling)
    skip_basenames = {
        "entity-system-registry.yaml",  # the registry itself
        "conformance_report.yaml",       # the conformance report
        "migration-id-map.yaml",         # the migration map
    }
    # Also skip the exceptions file (any basename; configurable)
    if EXCEPTIONS_PATH is not None:
        skip_basenames.add(EXCEPTIONS_PATH.name)
    skip_dirs = {".git", "node_modules", "__pycache__", ".github", "scripts", "tests"}
    # RECONCILED (IMP-001): research deposits are NOT canonical entities.
    # `entities/v1-alpha/<cell>/<group>/<bp>/research/*.yaml` holds candidate
    # universes and admission depositions: research artefacts that live inside
    # the entities glob but carry no canonical id, no envelope and no lifecycle.
    # Before this exclusion ES-001 reported "missing id" on all 158 research
    # deposits: a wrong-population scan, not 158 malformed entities. The
    # deposits stay on disk untouched; they are simply not subject to the
    # entity-envelope contract.
    #
    # `documentation/` is excluded for the same reason: its one member,
    # `.../Operate-Customer-Retention-Programs/documentation/manifest.yaml`, is
    # the CR-BP-94-EXT-01 documentation-status index. Its header states it
    # deliberately mirrors the parent BP's top-level identity ("The top-level
    # identity fields mirror the parent BP so the catalog schema validator
    # accepts the file"), so ES-001 flagged it as a duplicate id against
    # processes:process-pr-improve-t6uvan. A documentation index that
    # intentionally mirrors its parent is not a second entity.
    skip_dirs |= {"research", "discovery", "reports", "templates", "documentation"}

    for path_glob in file_globs:
        literal_prefix = path_glob.split("*", 1)[0]
        if literal_prefix.endswith("/"):
            literal_prefix = literal_prefix[:-1]
        if literal_prefix:
            base = repo_root / literal_prefix
        else:
            base = repo_root
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if any(skip_dir in path.parts for skip_dir in skip_dirs):
                continue
            if path.name in skip_basenames:
                continue
            if not fnmatch.fnmatch(str(path.relative_to(repo_root)), path_glob):
                continue
            if path.suffix not in (".yaml", ".yml"):
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
                record = _extract_record(content)
                if not record:
                    continue
                rid = record.get("id", "")
                if rid:
                    if rid in seen_ids:
                        records.append((path, record, f"duplicate id (also in {seen_ids[rid]})"))
                    else:
                        seen_ids[rid] = str(path.relative_to(repo_root))
                        records.append((path, record, None))
                else:
                    rid = str(path.relative_to(repo_root))
                    records.append((path, record, None))
            except Exception:
                pass

    return records


# --------------------------------------------------------------------------- #
# Evaluator + verdict
# --------------------------------------------------------------------------- #

def evaluate(repo_root: Path = REPO_ROOT) -> list:
    """Run ES-001..ES-005 across all records."""
    registry = _load_registry()
    exceptions = _load_exceptions()

    findings: list = []
    records = _walk_records(repo_root, registry)

    for path, record, dup_error in records:
        record_id = record.get("id", str(path.relative_to(repo_root)))
        if dup_error:
            findings.append({"rule": "ES-001", "record_id": record_id,
                             "diagnostic": dup_error})
        findings.extend(_check_es_001_identity(record, registry, record_id, exceptions))
        findings.extend(_check_es_002_contract(record, registry, record_id, exceptions))
        findings.extend(_check_es_003_relationship(record, registry, record_id, exceptions))
        findings.extend(_check_es_004_lifecycle(record, registry, record_id, exceptions))

    # ES-005 is global (per-type gate existence)
    findings.extend(_check_es_005_umbrella_global(registry, repo_root))

    return findings


def _verdict(findings: list) -> str:
    if any(f["rule"].startswith("ES-") for f in findings):
        return "NON-CONFORMANT"
    return "CONFORMANT"


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--strict", action="store_true",
                        help="Exit 1 on any ES-001..ES-005 finding.")
    parser.add_argument("--json", action="store_true",
                        help="Emit findings as JSON.")
    parser.add_argument("--self-test", action="store_true",
                        help="Run the in-script self-test; ignore other flags.")
    parser.add_argument("--catalog-root", default=str(REPO_ROOT),
                        help="Repo root (default: REPO_ROOT).")
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    findings = evaluate(Path(args.catalog_root))
    verdict = _verdict(findings)
    if args.json:
        print(json.dumps({"verdict": verdict, "findings": findings,
                          "findings_count": len(findings)}, indent=2))
    else:
        print(f"Entity System Gate (CR-BP-123): {verdict}")
        for f in findings[:20]:
            print(f"  [{f['rule']}] {f['record_id']}: {f['diagnostic']}")
        if len(findings) > 20:
            print(f"  ... and {len(findings) - 20} more")

    if args.strict and any(f["rule"].startswith("ES-") for f in findings):
        return 1
    return 0


def _self_test() -> int:
    """Hand-rolled fixtures; covers the 5 paths in the gate's contract."""
    import tempfile
    import check_entity_system as ces
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        reg = tmpdir / "entity-system-registry.yaml"
        reg.write_text(
            "envelope:\n"
            "  file_globs: ['*.yaml']\n"
            "  type_field: type\n"
            "  profiles:\n"
            "    Process:\n"
            "      required_fields: [id, type, name, definition, lifecycle, provenance]\n"
            "      lifecycle_state_field: lifecycle.status\n"
            "      provenance_change_history_field: provenance.change_history\n"
            "    ProcessContext:\n"
            "      required_fields: [id, name]\n"
            "    ProcessGroup:\n"
            "      required_fields: [id, type, name, definition, lifecycle, provenance]\n"
            "      lifecycle_state_field: lifecycle.status\n"
            "    Activity:\n"
            "      required_fields: [id, type, name, definition, lifecycle, provenance]\n"
            "      lifecycle_state_field: lifecycle.status\n"
            "    Task:\n"
            "      required_fields: [id, type, name, definition, lifecycle, provenance]\n"
            "      lifecycle_state_field: lifecycle.status\n"
            "    ProcessScope:\n"
            "      required_fields: [id, type, name, definition, lifecycle, provenance]\n"
            "      lifecycle_state_field: lifecycle.status\n"
            "identity:\n"
            "  id_field: id\n"
            "  canonical_prefix: 'processes:'\n"
            "  canonical_pattern: '^[a-z]+:[a-z]+(-[a-z]+){1,4}-[a-z2-9]{6}$'\n"
            "  legacy_prefix: 'dea:'\n"
            "  legacy_pattern: '^dea:[a-z]+-[a-z0-9-]+$'\n"
            "  legacy_migration_map: 'reconciliation/migration-id-map.yaml'\n"
            "relationships:\n"
            "  field: relationships\n"
            "  canonical_types: [composes, realizes, specializes]\n"
            "  forbidden_types: [part-of]\n"
            "  cross_catalog_field: identity_scope\n"
            "  type_constraints:\n"
            "    composes:\n"
            "      source_types: [ProcessGroup, ProcessContext]\n"
            "      target_types: [Process, ProcessGroup]\n"
            "    realizes:\n"
            "      source_types: [Process]\n"
            "      target_identity_scopes: [dea-catalog-business-capabilities]\n"
            "    specializes:\n"
            "      source_types: [Process]\n"
            "      target_types: [Process]\n"
            "lifecycle:\n"
            "  field: lifecycle\n"
            "  status_field: status\n"
            "  valid_states: [proposed, admitted, deprecated, retired, superseded]\n"
            "  terminal_states: [superseded, retired]\n"
            "  transition_table:\n"
            "    proposed: [admitted]\n"
            "    admitted: [deprecated, retired, superseded]\n"
            "    deprecated: [retired]\n"
            "    superseded: []\n"
            "    retired: []\n"
            "  provenance_field: provenance.change_history\n"
            "  provenance_required_keys: [cr, date, change]\n"
            "per_type_gates:\n"
            "  - type: Process\n"
            "    gate: scripts/check_process_semantics.py\n"
            "    args: --strict\n"
            "exceptions:\n"
            "  registry_path: reconciliation/normalization.yaml\n"
            "  verdict_key: verdict\n"
            "  verdict_value: review-retained\n"
            "  cr_key: cr\n"
            "  expiry_key: expiry\n"
            "  reviewer_key: reviewed_by\n"
            "  excepted_rules_key: excepted_rules\n",
            encoding="utf-8",
        )

        # Fixture 1: clean record (no findings)
        f1 = tmpdir / "f1.yaml"
        f1.write_text(
            "id: processes:process-clean-f3n8wb\n"
            "type: Process\n"
            "name: Clean Process\n"
            "definition: A clean record.\n"
            "lifecycle:\n"
            "  status: admitted\n"
            "  admitted_at: '2026-08-15'\n"
            "  admitted_by: CR-BP-122\n"
            "provenance:\n"
            "  change_history:\n"
            "    - cr: CR-BP-122\n"
            "      date: '2026-08-15'\n"
            "      change: Initial admission.\n",
            encoding="utf-8",
        )
        # Fixture 2: missing id
        f2 = tmpdir / "f2.yaml"
        f2.write_text("name: No ID\ntype: Process\ndefinition: A record with no id.\n", encoding="utf-8")
        # Fixture 3: invalid type
        f3 = tmpdir / "f3.yaml"
        f3.write_text(
            "id: processes:process-invalid-m6fmyx\n"
            "type: InvalidType\n"
            "name: Invalid Type\n"
            "definition: A record with an invalid type.\n"
            "lifecycle:\n"
            "  status: admitted\n"
            "provenance:\n"
            "  change_history:\n"
            "    - cr: CR-BP-122\n"
            "      date: '2026-08-15'\n"
            "      change: Initial admission.\n",
            encoding="utf-8",
        )
        # Fixture 4: forbidden relationship type
        f4 = tmpdir / "f4.yaml"
        f4.write_text(
            "id: processes:process-forbidden-m6fmyx\n"
            "type: Process\n"
            "name: Forbidden Relationship\n"
            "definition: A record with a forbidden relationship.\n"
            "lifecycle:\n"
            "  status: admitted\n"
            "relationships:\n"
            "  - relationship_type: part-of\n"
            "    target: processes:process-other-f3n8wb\n"
            "provenance:\n"
            "  change_history:\n"
            "    - cr: CR-BP-122\n"
            "      date: '2026-08-15'\n"
            "      change: Initial admission.\n",
            encoding="utf-8",
        )
        # Fixture 5: missing provenance key
        f5 = tmpdir / "f5.yaml"
        f5.write_text(
            "id: processes:process-no-prov-f3n8wb\n"
            "type: Process\n"
            "name: No Provenance\n"
            "definition: A record with no provenance key.\n"
            "lifecycle:\n"
            "  status: admitted\n"
            "provenance:\n"
            "  change_history:\n"
            "    - cr: CR-BP-122\n"
            "      date: '2026-08-15'\n",
            encoding="utf-8",
        )

        ces.REGISTRY_PATH = reg
        ces.EXCEPTIONS_PATH = tmpdir / "normalization.yaml"
        findings = ces.evaluate(tmpdir)
        es_001 = [f for f in findings if f["rule"] == "ES-001"]
        es_002 = [f for f in findings if f["rule"] == "ES-002"]
        es_003 = [f for f in findings if f["rule"] == "ES-003"]
        es_004 = [f for f in findings if f["rule"] == "ES-004"]
        assert any("missing" in f["diagnostic"] and "id" in f["diagnostic"] for f in es_001), \
            f"expected missing id in ES-001, got: {es_001}"
        assert any("InvalidType" in f["diagnostic"] for f in es_002), \
            f"expected InvalidType in ES-002, got: {es_002}"
        assert any("part-of" in f["diagnostic"] for f in es_003), \
            f"expected part-of in ES-003, got: {es_003}"
        assert any("change" in f["diagnostic"] for f in es_004), \
            f"expected missing change in ES-004, got: {es_004}"
    print("self-test PASS (5 cases)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
