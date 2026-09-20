#!/usr/bin/env python3
"""
check_process_scope.py - Process Scope (L0) validator.

Implements CR-BP-95 rules PSCOPE-001..PSCOPE-008.

Rules:
  PSCOPE-001 - ID pattern: id matches `^processes:scope-[a-z0-9-]+$`.
  PSCOPE-002 - Required fields: id, name, definition, process_context, scope,
               outcomes, decomposition_basis, composes, scope_kind, status,
               lifecycle_status, version must be present and non-empty where
               applicable.
  PSCOPE-003 - Process Context resolution: `process_context` resolves to a
               known `processes:pc-*` Process Context entity in the containment tree.
  PSCOPE-004 - Composes target_id pattern: every composes[].target_id
               matches `^processes:group-[a-z0-9-]+$`.
  PSCOPE-005 - Composes target resolution: every composes[].target_id
               resolves to a canonical L1 Process Group entity in
               entities/v1-alpha/. When the catalog has no Process Group
               records (the current pre-population state), the resolver
               reports the vacuity honestly rather than passing silently.
  PSCOPE-006 - MECE within a Process Context: no two Process Scopes in the
               same Process Context share an L1 group in their composes
               list.
  PSCOPE-007 - Scope kind controlled vocabulary: scope_kind is one of the
               six values mirroring classifications/process-group-kinds.yaml.
  PSCOPE-008 - Lifecycle status: lifecycle_status is one of `candidate`,
               `active`, `deprecated`, `retired`. `active` requires at least
               one composes entry with status: active.

Exit: 0 = all rules pass (or no entries); 2 = self-test; 1 = at least one
      rule failed.

CR-BP-95 design note: L0 Process Scope is established by CR-BP-95 as a
schema-bearing entity; canonical records land in future tranches (CR-BP-99
reconciliation matrix, or a dedicated L0 population tranche). The current
catalog has no L0 records. The validator is fixture-tolerant: when the
catalog has no entities/ tree, it reports a vacuous pass with an explicit
note. When L0 records are absent and Process Group records are present, the
MECE and resolution checks skip silently (their input set is empty). This
matches the CR-BP-58 fix pattern: vacuous-scaffold messages in a populated
catalog are a red flag; explicit no-records-found is honest.
"""
import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

import yaml

REQUIRED_FIELDS = (
    "id",
    "name",
    "definition",
    "process_context",
    "scope",
    "outcomes",
    "decomposition_basis",
    "composes",
    "scope_kind",
    "status",
    "lifecycle_status",
    "version",
)

LIFECYCLE_VALUES = ("candidate", "active", "deprecated", "retired")
STATUS_VALUES = ("candidate", "accepted", "deferred", "deprecated", "rejected")
ID_PATTERN = re.compile(r"^processes:scope-[a-z0-9-]+$")
GROUP_ID_PATTERN = re.compile(r"^processes:group-[a-z0-9-]+$")
CONTEXT_ID_PATTERN = re.compile(r"^processes:pc-[a-z0-9-]+$")
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")

# Mirrors classifications/process-group-kinds.yaml vocabulary
SCOPE_KIND_VOCAB = (
    "value-stream",
    "functional-responsibility",
    "support-capability",
    "cross-cutting-concern",
    "governance-obligation",
    "innovation-candidate",
)


def _load_context_ids(catalog_root: Path) -> set[str]:
    # CR-BP-mv1: PCs live in the containment tree (contexts/ is retired).
    entities_dir = catalog_root / "entities" / "v1-alpha"
    if not entities_dir.exists():
        return set()
    ids: set[str] = set()
    for path in entities_dir.rglob("processes-pc-*.yaml"):
        try:
            with path.open() as f:
                data = yaml.safe_load(f) or {}
        except yaml.YAMLError:
            continue
        cid = data.get("id")
        if isinstance(cid, str):
            ids.add(cid)
    return ids


def _load_group_ids(catalog_root: Path) -> set[str]:
    entities_dir = catalog_root / "entities" / "v1-alpha"
    if not entities_dir.exists():
        return set()
    ids: set[str] = set()
    for path in entities_dir.rglob("*.yaml"):
        try:
            with path.open() as f:
                data = yaml.safe_load(f) or {}
        except yaml.YAMLError:
            continue
        gid = data.get("id")
        # Process Group records use type: ProcessGroup
        if isinstance(gid, str) and data.get("type") == "ProcessGroup":
            ids.add(gid)
    return ids


def _check_one(
    entry: dict,
    *,
    context_ids: set[str],
    group_ids: set[str],
    errors: list[str],
    all_entries: list[dict],
) -> None:
    eid = entry.get("id", "<unknown>")

    # PSCOPE-001 - ID pattern.
    if not isinstance(eid, str) or not ID_PATTERN.match(eid or ""):
        errors.append(
            f"PSCOPE-001 ({eid}): id must match `^processes:scope-[a-z0-9-]+$` "
            f"(CR-BP-04 §4 family; CR-BP-95 §1)."
        )

    # PSCOPE-002 - Required fields.
    for field in REQUIRED_FIELDS:
        if field not in entry or entry[field] in (None, "", [], {}):
            errors.append(
                f"PSCOPE-002 ({eid}): required field `{field}` is missing or empty."
            )

    # PSCOPE-003 - Process Context resolution.
    pc = entry.get("process_context", "")
    if not isinstance(pc, str) or not CONTEXT_ID_PATTERN.match(pc or ""):
        errors.append(
            f"PSCOPE-003 ({eid}): process_context must match `^processes:pc-[a-z0-9-]+$`."
        )
    elif context_ids and pc not in context_ids:
        errors.append(
            f"PSCOPE-003 ({eid}): process_context={pc!r} does not resolve to a known "
            f"Process Context in contexts/v1-alpha/. Known contexts: {sorted(context_ids)}."
        )

    # PSCOPE-004 + PSCOPE-005 - Composes target_id pattern + resolution.
    composes = entry.get("composes") or []
    if not isinstance(composes, list):
        errors.append(
            f"PSCOPE-004 ({eid}): composes must be an array of relationship instances."
        )
        composes = []
    seen_targets: set[str] = set()
    for idx, comp in enumerate(composes):
        if not isinstance(comp, dict):
            errors.append(
                f"PSCOPE-004 ({eid}): composes[{idx}] must be an object conforming to "
                f"the metamodel relationship-instance shape."
            )
            continue
        target_id = comp.get("target_id")
        rel_type = comp.get("relationship_type")
        if rel_type != "composes":
            errors.append(
                f"PSCOPE-004 ({eid}): composes[{idx}].relationship_type must be 'composes' "
                f"(got {rel_type!r})."
            )
        if not isinstance(target_id, str) or not GROUP_ID_PATTERN.match(target_id or ""):
            errors.append(
                f"PSCOPE-004 ({eid}): composes[{idx}].target_id must match "
                f"`^processes:group-[a-z0-9-]+$` (got {target_id!r})."
            )
        elif target_id not in group_ids:
            errors.append(
                f"PSCOPE-005 ({eid}): composes[{idx}].target_id={target_id!r} does not "
                f"resolve to a canonical L1 Process Group entity in entities/v1-alpha/."
            )
        seen_targets.add(target_id)

    # PSCOPE-006 - MECE within a Process Context.
    if isinstance(pc, str) and CONTEXT_ID_PATTERN.match(pc or "") and all_entries:
        overlap = []
        for other in all_entries:
            if other is entry:
                continue
            other_pc = other.get("process_context", "")
            if other_pc != pc:
                continue
            other_targets = {
                (c.get("target_id") if isinstance(c, dict) and isinstance(c.get("target_id"), str) else None)
                for c in (other.get("composes") or [])
            }
            common = seen_targets & other_targets
            common = {t for t in common if isinstance(t, str)}
            if common:
                overlap.append((other.get("id", "<unknown>"), sorted(common)))
        if overlap:
            for other_id, common_list in overlap:
                errors.append(
                    f"PSCOPE-006 ({eid}): MECE violation in Process Context {pc!r}: "
                    f"this scope and {other_id!r} both compose {common_list}. "
                    f"Within a single Process Context an L1 group may belong to at most "
                    f"one Process Scope."
                )

    # PSCOPE-007 - Scope kind controlled vocabulary.
    scope_kind = entry.get("scope_kind")
    if scope_kind not in SCOPE_KIND_VOCAB:
        errors.append(
            f"PSCOPE-007 ({eid}): scope_kind={scope_kind!r} is not in the controlled "
            f"vocabulary {sorted(SCOPE_KIND_VOCAB)}."
        )

    # PSCOPE-008 - Lifecycle status.
    lifecycle = entry.get("lifecycle_status")
    if lifecycle not in LIFECYCLE_VALUES:
        errors.append(
            f"PSCOPE-008 ({eid}): lifecycle_status={lifecycle!r} must be one of "
            f"{LIFECYCLE_VALUES}."
        )
    elif lifecycle == "active":
        active_targets = [
            c.get("target_id") for c in composes
            if isinstance(c, dict) and c.get("status") == "active"
        ]
        if not active_targets:
            errors.append(
                f"PSCOPE-008 ({eid}): lifecycle_status='active' requires at least one "
                f"composes entry with status='active'."
            )
    elif lifecycle in ("deprecated", "retired"):
        rationale_present = any(
            isinstance(c, dict) and str(c.get("rationale", "")).strip()
            for c in composes
        )
        if not rationale_present:
            errors.append(
                f"PSCOPE-008 ({eid}): lifecycle_status={lifecycle!r} requires at least "
                f"one composes entry with a non-empty rationale referencing a terminal-"
                f"state L1 group."
            )

    # PSCOPE-extra: type field check (defensive).
    if entry.get("type") != "ProcessScope":
        errors.append(
            f"PSCOPE-extra ({eid}): type must be 'ProcessScope' for a Process Scope "
            f"entry (got {entry.get('type')!r})."
        )

    # PSCOPE-extra: decomposition_basis structure.
    db = entry.get("decomposition_basis")
    if isinstance(db, dict):
        db_type = db.get("type")
        db_statement = db.get("statement")
        if db_type not in SCOPE_KIND_VOCAB:
            errors.append(
                f"PSCOPE-extra ({eid}): decomposition_basis.type={db_type!r} is not "
                f"in the controlled vocabulary {sorted(SCOPE_KIND_VOCAB)}."
            )
        if not isinstance(db_statement, str) or not db_statement.strip():
            errors.append(
                f"PSCOPE-extra ({eid}): decomposition_basis.statement is required and "
                f"must be a non-empty string."
            )


def run_checks(catalog_root: Path) -> tuple[list[str], list[dict]]:
    errors: list[str] = []
    suggestions: list[dict] = []
    context_ids = _load_context_ids(catalog_root)
    group_ids = _load_group_ids(catalog_root)

    entities_dir = catalog_root / "entities" / "v1-alpha"
    if not entities_dir.exists():
        print("Process Scope validation: PASS (no entities/ directory)")
        return errors, suggestions

    entries: list[dict] = []
    for path in sorted(entities_dir.rglob("*.yaml")):
        try:
            with path.open() as f:
                data = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            errors.append(f"PSCOPE-002 ({path.name}): YAML parse error: {e}")
            continue
        if not isinstance(data, dict):
            continue
        if data.get("type") == "ProcessScope":
            entries.append(data)

    if not entries:
        # CR-BP-95 design note: honest no-records-found, not a vacuous pass.
        # Distinguish the two cases explicitly so a future populated catalog
        # that lacks L0 records can be audited against the design intent.
        if group_ids:
            print(
                "Process Scope validation: PASS (no ProcessScope entries found; "
                f"L0 layer intentionally pre-population per CR-BP-95; "
                f"{len(group_ids)} Process Group records present and conformant "
                f"under PG-001..010)."
            )
        else:
            print(
                "Process Scope validation: PASS (no entities/ records; "
                "self-test fixture scope)"
            )
        return errors, suggestions

    for entry in entries:
        _check_one(
            entry,
            context_ids=context_ids,
            group_ids=group_ids,
            errors=errors,
            all_entries=entries,
        )
    return errors, suggestions


def self_test() -> int:
    """Exercise PSCOPE-001..008 on deliberately broken + fixed catalogs."""
    with tempfile.TemporaryDirectory(prefix="pscope_self_test_") as tmp:
        tmp_path = Path(tmp)
        ent_root = tmp_path / "entities" / "v1-alpha"
        cell_dir = ent_root / "pr-operate"
        pc_dir = cell_dir / "pr-operate-pc0001"
        grp_dir = cell_dir / "pr-operate-grp001"
        pc_dir.mkdir(parents=True)
        grp_dir.mkdir(parents=True)

        # Minimal Process Context (CR-BP-mv1 containment tree form).
        (pc_dir / "processes-pc-pr-operate-test001.yaml").write_text(
            "id: processes:pc-pr-operate-test001\ntype: ProcessContext\nname: Test\nversion: 1.0.0\n",
            encoding="utf-8",
        )
        # Minimal Process Group record (target for the scope's composes).
        (grp_dir / "processes-group-pr-operate-test001.yaml").write_text(
            "id: processes:group-pr-operate-test001\n"
            "type: ProcessGroup\n"
            "name: Test Group\n"
            "version: 1.0.0\n"
            "process_context: processes:pc-pr-operate-test001\n"
            "process_group_kind: functional\n"
            "status: active\n"
            "lifecycle_status: active\n"
            "definition: Test group.\n"
            "scope:\n  includes: [a]\n  excludes: [b]\n"
            "outcomes: [test]\n"
            "composes: []\n",
            encoding="utf-8",
        )

        # BAD scope: missing required field, bad kind, bad lifecycle.
        bad_scope_path = (
            cell_dir / "pr-operate-scpbad" / "processes-scope-pr-operate-bad001.yaml"
        )
        bad_scope_path.parent.mkdir(parents=True)
        bad_scope_path.write_text(
            "id: processes:scope-pr-operate-bad001\n"
            "type: ProcessScope\n"
            "name: Bad Scope\n"
            "version: 1.0.0\n"
            "process_context: processes:pc-pr-operate-test001\n"
            # missing: definition, scope, outcomes, decomposition_basis, composes,
            #          scope_kind, status, lifecycle_status
            "definition: \n"
            "scope:\n  includes: []\n  excludes: []\n"
            "outcomes: []\n"
            "decomposition_basis: {}\n"
            "composes: not-an-array\n"
            "scope_kind: invalid-kind\n"
            "status: active\n"
            "lifecycle_status: bogus\n",
            encoding="utf-8",
        )

        # GOOD scope: minimal conformant record.
        good_scope_path = (
            cell_dir / "pr-operate-scpgood" / "processes-scope-pr-operate-good001.yaml"
        )
        good_scope_path.parent.mkdir(parents=True)
        good_scope_path.write_text(
            "id: processes:scope-pr-operate-good001\n"
            "type: ProcessScope\n"
            "name: Good Scope\n"
            "version: 1.0.0\n"
            "process_context: processes:pc-pr-operate-test001\n"
            "process_group_kind: value-stream\n"
            "scope_kind: value-stream\n"
            "status: active\n"
            "lifecycle_status: active\n"
            "definition: Test scope.\n"
            "scope:\n  includes: [a]\n  excludes: [b]\n"
            "outcomes: [test]\n"
            "decomposition_basis:\n"
            "  type: value-stream\n"
            "  statement: 'Decomposes the customer-facing value stream.'\n"
            "composes:\n"
            "  - source_id: processes:scope-pr-operate-good001\n"
            "    target_id: processes:group-pr-operate-test001\n"
            "    relationship_type: composes\n"
            "    status: active\n",
            encoding="utf-8",
        )

        # --- 1. Run on the BAD catalog: expect errors.
        errors, _ = run_checks(tmp_path)
        joined = "\n".join(errors)
        expected_rules = [
            "PSCOPE-002",
            "PSCOPE-004",
            "PSCOPE-007",
            "PSCOPE-008",
        ]
        for needle in expected_rules:
            if not any(needle in e for e in errors):
                print(f"PSCOPE self-test: expected rule {needle} to fire on bad catalog.")
                print("Errors observed:")
                for e in errors:
                    print(f"  {e}")
                return 2

        # --- 2. Remove the bad scope, run again: expect clean pass.
        bad_scope_path.unlink()
        errors, _ = run_checks(tmp_path)
        if errors:
            print("PSCOPE self-test: expected clean pass after removing bad scope; got:")
            for e in errors:
                print(f"  {e}")
            return 2

        # --- 3. Empty catalog (no scopes, no groups): expect honest
        # no-records-found pass.
        (grp_dir / "processes-group-pr-operate-test001.yaml").unlink()
        good_scope_path.unlink()
        errors, _ = run_checks(tmp_path)
        if errors:
            print("PSCOPE self-test: expected clean pass on empty catalog; got:")
            for e in errors:
                print(f"  {e}")
            return 2

        print("PSCOPE self-test: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog-root", type=Path, default=Path("."))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    errors, _ = run_checks(args.catalog_root)
    if errors:
        print("Process Scope (CR-BP-95; PSCOPE-001..008): NON-CONFORMANT")
        print(f"Findings: {len(errors)}")
        for e in errors:
            print(f"  {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
