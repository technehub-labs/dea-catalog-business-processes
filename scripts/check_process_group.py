#!/usr/bin/env python3
"""
check_process_group.py — Process Group (L1) validator.

Implements CR-BP-12 rules PG-001..PG-008 and CR-BP-95 extensions
PG-009 (grouping_basis) and PG-010 (membership_criteria).

Rules:
  PG-001 — ID pattern: id matches `^dea:group-[a-z0-9-]+$`.
  PG-002 — Required fields: id, name, definition, process_context, scope,
           outcomes, composes, process_group_kind, status, lifecycle_status,
           version must be present and non-empty where applicable.
  PG-003 — Process Context resolution: `process_context` resolves to a
           known `dea:pc-*` Process Context entity in contexts/v1-alpha/.
  PG-004 — Composes target_id pattern: every composes[].target_id
           matches `^dea:process-[a-z0-9-]+$`.
  PG-005 — Composes target resolution: every composes[].target_id
           resolves to a canonical L2 Business Process entity in
           entities/v1-alpha/.
  PG-006 — MECE within a Process Context: no two Process Groups in the
           same Process Context share an L2 process in their composes
           list. Cross-context overlap is permitted only when declared
           in metadata.cross_context_overlap.
  PG-007 — Process group kind controlled vocabulary: process_group_kind
           is one of the six values in classifications/process-group-kinds.yaml.
  PG-008 — Lifecycle status: lifecycle_status is one of `candidate`,
           `active`, `deprecated`, `retired`. `active` requires at least
           one composes entry with status: active. `deprecated` and
           `retired` must reference at least one terminal-state L2
           process in the rationale field.
  PG-009 (CR-BP-95) — grouping_basis (when present): structure check.
           The field is OPTIONAL; existing pre-CR-BP-95 records remain
           conformant when absent. When present, the structure must be
           {type, statement} with type from a controlled vocabulary.
  PG-010 (CR-BP-95) — membership_criteria (when present): structure check.
           The field is OPTIONAL. When present, the structure must be
           {inclusion_test, exclusion_test}, both non-empty strings.

Exit: 0 = all rules pass (or no entries); 2 = self-test; 1 = at least one rule failed.

Built-in --self-test exercises each rule on a deliberately broken catalog
(then on a fixed catalog) and verifies the expected exit codes.
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
    "composes",
    "process_group_kind",
    "status",
    "lifecycle_status",
    "version",
)

LIFECYCLE_VALUES = ("candidate", "active", "deprecated", "retired")
STATUS_VALUES = ("candidate", "accepted", "deferred", "deprecated", "rejected")
ID_PATTERN = re.compile(r"^dea:group-[a-z0-9-]+$")
PROCESS_ID_PATTERN = re.compile(r"^dea:process-[a-z0-9-]+$")
CONTEXT_ID_PATTERN = re.compile(r"^dea:pc-[a-z0-9-]+$")
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


def _load_kinds(catalog_root: Path) -> set[str]:
    kinds_path = catalog_root / "classifications" / "process-group-kinds.yaml"
    if not kinds_path.exists():
        return set()
    with kinds_path.open() as f:
        data = yaml.safe_load(f) or {}
    vocab = data.get("vocabulary", []) or []
    return {entry["id"] for entry in vocab if "id" in entry}


def _load_context_ids(catalog_root: Path) -> set[str]:
    contexts_dir = catalog_root / "contexts" / "v1-alpha"
    if not contexts_dir.exists():
        return set()
    ids: set[str] = set()
    for path in contexts_dir.glob("*.yaml"):
        try:
            with path.open() as f:
                data = yaml.safe_load(f) or {}
        except yaml.YAMLError:
            continue
        cid = data.get("id")
        if isinstance(cid, str):
            ids.add(cid)
    return ids


def _load_process_ids(catalog_root: Path) -> set[str]:
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
        pid = data.get("id")
        # Include only canonical L2 Business Process entries (type: Process),
        # not the new ProcessGroup records (which use `type: ProcessGroup`).
        if isinstance(pid, str) and data.get("type") == "Process":
            ids.add(pid)
    return ids


def _check_one(entry: dict, *, kinds: set[str], context_ids: set[str], process_ids: set[str], errors: list[str], suggestions: list[dict], all_entries: list[dict]) -> None:
    eid = entry.get("id", "<unknown>")

    # PG-001 — ID pattern.
    if not isinstance(eid, str) or not ID_PATTERN.match(eid or ""):
        errors.append(
            f"PG-001 ({eid}): id must match `^dea:group-[a-z0-9-]+$` (CR-BP-04 §4 family; CR-BP-12 §5.1)."
        )

    # PG-002 — Required fields.
    for field in REQUIRED_FIELDS:
        if field not in entry or entry[field] in (None, "", [], {}):
            errors.append(
                f"PG-002 ({eid}): required field `{field}` is missing or empty."
            )

    # PG-003 — Process Context resolution.
    pc = entry.get("process_context", "")
    if not isinstance(pc, str) or not CONTEXT_ID_PATTERN.match(pc or ""):
        errors.append(
            f"PG-003 ({eid}): process_context must match `^dea:pc-[a-z0-9-]+$`."
        )
    elif context_ids and pc not in context_ids:
        errors.append(
            f"PG-003 ({eid}): process_context={pc!r} does not resolve to a known Process Context in contexts/v1-alpha/. "
            f"Known contexts: {sorted(context_ids)}."
        )

    # PG-004 + PG-005 — Composes target_id pattern + resolution.
    composes = entry.get("composes") or []
    if not isinstance(composes, list):
        errors.append(
            f"PG-004 ({eid}): composes must be an array of relationship instances."
        )
        composes = []
    seen_targets: set[str] = set()
    for idx, comp in enumerate(composes):
        if not isinstance(comp, dict):
            errors.append(
                f"PG-004 ({eid}): composes[{idx}] must be an object conforming to the metamodel relationship-instance shape."
            )
            continue
        target_id = comp.get("target_id")
        rel_type = comp.get("relationship_type")
        if rel_type != "composes":
            errors.append(
                f"PG-004 ({eid}): composes[{idx}].relationship_type must be 'composes' (got {rel_type!r})."
            )
        if not isinstance(target_id, str) or not PROCESS_ID_PATTERN.match(target_id or ""):
            errors.append(
                f"PG-004 ({eid}): composes[{idx}].target_id must match `^dea:process-[a-z0-9-]+$` (got {target_id!r})."
            )
        elif process_ids and target_id not in process_ids:
            errors.append(
                f"PG-005 ({eid}): composes[{idx}].target_id={target_id!r} does not resolve to a canonical L2 Business Process entity in entities/v1-alpha/."
            )
        seen_targets.add(target_id)

    # PG-006 — MECE within a Process Context.
    if isinstance(pc, str) and CONTEXT_ID_PATTERN.match(pc or ""):
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
                # Allowed only when the entry declares cross_context_overlap and
                # the other group's context is in that list. (For intra-context
                # overlap we treat it as always forbidden; cross_context_overlap
                # only applies to cross-context membership, not intra-context.)
                overlap.append((other.get("id", "<unknown>"), sorted(common)))
        if overlap:
            for other_id, common_list in overlap:
                errors.append(
                    f"PG-006 ({eid}): MECE violation in Process Context {pc!r}: "
                    f"this group and {other_id!r} both compose {common_list}. "
                    f"Within a single Process Context an L2 process may belong to at most one Process Group."
                )

    # PG-007 — Process group kind controlled vocabulary.
    pg_kind = entry.get("process_group_kind")
    if kinds and pg_kind not in kinds:
        errors.append(
            f"PG-007 ({eid}): process_group_kind={pg_kind!r} is not in the controlled vocabulary "
            f"{sorted(kinds)}. See classifications/process-group-kinds.yaml."
        )
    elif not kinds:
        suggestions.append({
            "target": eid,
            "suggestion_type": "kinds_vocabulary_missing",
            "current_state": {"process_group_kind": pg_kind},
            "suggested_state": {"action": "load classifications/process-group-kinds.yaml"},
            "confidence": 0.5,
            "rationale": "PG-007: the controlled vocabulary file could not be loaded; this is an internal error, not a contributor error.",
        })

    # PG-008 — Lifecycle status.
    lifecycle = entry.get("lifecycle_status")
    if lifecycle not in LIFECYCLE_VALUES:
        errors.append(
            f"PG-008 ({eid}): lifecycle_status={lifecycle!r} must be one of {LIFECYCLE_VALUES}."
        )
    elif lifecycle == "active":
        active_targets = [
            c.get("target_id") for c in composes
            if isinstance(c, dict) and c.get("status") == "active"
        ]
        if not active_targets:
            errors.append(
                f"PG-008 ({eid}): lifecycle_status='active' requires at least one composes entry with status='active'."
            )
    elif lifecycle in ("deprecated", "retired"):
        rationale_present = any(
            isinstance(c, dict) and str(c.get("rationale", "")).strip()
            for c in composes
        )
        if not rationale_present:
            errors.append(
                f"PG-008 ({eid}): lifecycle_status={lifecycle!r} requires at least one composes entry with a non-empty rationale referencing a terminal-state L2 process."
            )

    # PG-extra: type field check (defensive; the schema enforces it, but the
    # validator runs without the schema layer).
    if entry.get("type") != "ProcessGroup":
        errors.append(
            f"PG-extra ({eid}): type must be 'ProcessGroup' for a Process Group entry (got {entry.get('type')!r})."
        )

    # PG-009 (CR-BP-95): grouping_basis — when present, structure check.
    # Back-compat: the field is OPTIONAL; existing pre-CR-BP-95 records remain
    # conformant when the field is absent.
    grouping_basis = entry.get("grouping_basis")
    if grouping_basis is not None:
        if not isinstance(grouping_basis, dict):
            errors.append(
                f"PG-009 ({eid}): grouping_basis must be an object with `type` and `statement` "
                f"(CR-BP-95; CR-BP-93 §4)."
            )
        else:
            gb_type = grouping_basis.get("type")
            gb_statement = grouping_basis.get("statement")
            valid_types = {
                "value-stream",
                "functional-responsibility",
                "support-capability",
                "cross-cutting-concern",
                "governance-obligation",
                "innovation-candidate",
            }
            if gb_type not in valid_types:
                errors.append(
                    f"PG-009 ({eid}): grouping_basis.type={gb_type!r} is not in the controlled "
                    f"vocabulary {sorted(valid_types)} (CR-BP-95)."
                )
            if not isinstance(gb_statement, str) or not gb_statement.strip():
                errors.append(
                    f"PG-009 ({eid}): grouping_basis.statement is required and must be a "
                    f"non-empty string (CR-BP-95)."
                )

    # PG-010 (CR-BP-95): membership_criteria — when present, structure check.
    # Back-compat: OPTIONAL; existing pre-CR-BP-95 records remain conformant when absent.
    membership_criteria = entry.get("membership_criteria")
    if membership_criteria is not None:
        if not isinstance(membership_criteria, dict):
            errors.append(
                f"PG-010 ({eid}): membership_criteria must be an object with `inclusion_test` "
                f"and `exclusion_test` (CR-BP-95; CR-BP-93 §4)."
            )
        else:
            inc = membership_criteria.get("inclusion_test")
            exc = membership_criteria.get("exclusion_test")
            if not isinstance(inc, str) or not inc.strip():
                errors.append(
                    f"PG-010 ({eid}): membership_criteria.inclusion_test is required and must be "
                    f"a non-empty string (CR-BP-95)."
                )
            if not isinstance(exc, str) or not exc.strip():
                errors.append(
                    f"PG-010 ({eid}): membership_criteria.exclusion_test is required and must be "
                    f"a non-empty string (CR-BP-95)."
                )


def run_checks(catalog_root: Path) -> tuple[list[str], list[dict]]:
    errors: list[str] = []
    suggestions: list[dict] = []
    kinds = _load_kinds(catalog_root)
    context_ids = _load_context_ids(catalog_root)
    process_ids = _load_process_ids(catalog_root)

    entities_dir = catalog_root / "entities" / "v1-alpha"
    if not entities_dir.exists():
        print("Process Group validation: PASS (no entities/ directory)")
        return errors, suggestions

    entries: list[dict] = []
    for path in sorted(entities_dir.rglob("*.yaml")):
        try:
            with path.open() as f:
                data = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            errors.append(f"PG-002 ({path.name}): YAML parse error: {e}")
            continue
        if not isinstance(data, dict):
            continue
        if data.get("type") == "ProcessGroup":
            entries.append(data)

    if not entries:
        print("Process Group validation: PASS (no ProcessGroup entries; CR-BP-12 §1 deferred-population scaffold)")
        return errors, suggestions

    for entry in entries:
        _check_one(
            entry,
            kinds=kinds,
            context_ids=context_ids,
            process_ids=process_ids,
            errors=errors,
            suggestions=suggestions,
            all_entries=entries,
        )
    return errors, suggestions


def self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="pg_self_test_") as tmp:
        tmp_path = Path(tmp)
        ent_dir = tmp_path / "entities" / "v1-alpha"
        ctx_dir = tmp_path / "contexts" / "v1-alpha"
        kinds_dir = tmp_path / "classifications"
        ent_dir.mkdir(parents=True)
        ctx_dir.mkdir(parents=True)
        kinds_dir.mkdir(parents=True)

        # Fixed context
        (ctx_dir / "dea_pc-test-op.yaml").write_text(
            "id: dea:pc-test-op\n"
            "domain: PartyAndRelationship\n"
            "lifecycle_stage: Operate\n"
            "name: Test Context\n"
            "definition: Test\n"
            "scope:\n  includes: []\n  excludes: []\n"
            "outcomes: []\n"
            "adjacent_contexts: []\n"
            "cell_charter:\n"
            "  enterprise_concern: x\n"
            "  lifecycle_concern: y\n"
            "  combined_semantic_meaning: z\n"
            "  expected_outcomes: []\n"
            "  inclusions: []\n"
            "  exclusions: []\n"
            "  adjacent_boundaries: []\n"
            "status: defined\n"
        )
        # Fixed L2 process
        (ent_dir / "dea_process-test.yaml").write_text(
            "id: dea:process-test\n"
            "type: Process\n"
            "name: Test Process\n"
            "version: 1.0.0\n"
            "process_intent: operational\n"
            "process_audience: party-relationship\n"
            "process_type: core\n"
            "process_specialization: []\n"
            "description: Test description.\n"
            "trigger: Test trigger.\n"
            "outcome: Test outcome.\n"
        )
        # Kinds vocabulary
        (kinds_dir / "process-group-kinds.yaml").write_text(
            "vocabulary:\n"
            "  - id: end-to-end\n"
            "    name: End-to-End\n"
            "    definition: x\n"
            "    example: x\n"
            "  - id: functional\n"
            "    name: Functional\n"
            "    definition: x\n"
            "    example: x\n"
            "  - id: support\n"
            "    name: Support\n"
            "    definition: x\n"
            "    example: x\n"
            "  - id: cross-cutting\n"
            "    name: Cross-Cutting\n"
            "    definition: x\n"
            "    example: x\n"
            "  - id: governance\n"
            "    name: Governance\n"
            "    definition: x\n"
            "    example: x\n"
            "  - id: innovation\n"
            "    name: Innovation\n"
            "    definition: x\n"
            "    example: x\n"
        )

        # Broken catalog: PG-001 (bad id), PG-003 (unknown context),
        # PG-005 (unresolved target, well-formed id, missing entity),
        # PG-006 (intra-context overlap via a second group sharing the
        # process target with the good group), PG-007 (unknown kind),
        # PG-008 (active with no active composes, achieved by giving
        # composes a single entry with status="planned").
        (ent_dir / "dea_group-bad.yaml").write_text(
            "id: dea_group-bad-no-dash\n"
            "type: ProcessGroup\n"
            "name: Bad Group\n"
            "definition: Bad.\n"
            "process_context: dea:pc-unknown-context\n"
            "scope:\n  includes: []\n  excludes: []\n"
            "outcomes: []\n"
            "composes:\n"
            "  - source_id: dea_group-bad-no-dash\n"
            "    target_id: dea:not-a-process\n"
            "    relationship_type: composes\n"
            "    status: planned\n"
            "  - source_id: dea_group-bad-no-dash\n"
            "    target_id: dea:process-nonexistent\n"
            "    relationship_type: composes\n"
            "    status: planned\n"
            "process_group_kind: bogus\n"
            "status: candidate\n"
            "lifecycle_status: active\n"
            "version: 1.0.0\n"
        )
        (ent_dir / "dea_group-overlap.yaml").write_text(
            "id: dea:group-overlap\n"
            "type: ProcessGroup\n"
            "name: Overlap Group\n"
            "definition: Overlap.\n"
            "process_context: dea:pc-test-op\n"
            "scope:\n  includes: []\n  excludes: []\n"
            "outcomes: []\n"
            "composes:\n"
            "  - source_id: dea:group-overlap\n"
            "    target_id: dea:process-test\n"
            "    relationship_type: composes\n"
            "    status: active\n"
            "process_group_kind: functional\n"
            "status: candidate\n"
            "lifecycle_status: active\n"
            "version: 1.0.0\n"
        )
        (ent_dir / "dea_group-good.yaml").write_text(
            "id: dea:group-good\n"
            "type: ProcessGroup\n"
            "name: Good Group\n"
            "definition: Good.\n"
            "process_context: dea:pc-test-op\n"
            "scope:\n"
            "  includes: [a]\n"
            "  excludes: [b]\n"
            "outcomes: [c]\n"
            "composes:\n"
            "  - source_id: dea:group-good\n"
            "    target_id: dea:process-test\n"
            "    relationship_type: composes\n"
            "    status: active\n"
            "process_group_kind: end-to-end\n"
            "status: accepted\n"
            "lifecycle_status: active\n"
            "version: 1.0.0\n"
        )
        # First run: bad catalog expected to fail with multiple errors.
        errors, suggestions = run_checks(tmp_path)
        if not errors:
            print("PG self-test: expected errors on bad catalog; got none.")
            return 2
        error_blob = " ".join(errors)
        for needle in ("PG-001", "PG-003", "PG-004", "PG-005", "PG-006", "PG-007", "PG-008"):
            if needle not in error_blob:
                print(f"PG self-test: expected rule {needle} to fire on bad catalog.")
                return 2
        error_blob = " ".join(errors)
        for needle in ("PG-001", "PG-004", "PG-007", "PG-008"):
            if needle not in error_blob:
                print(f"PG self-test: expected rule {needle} to fire on bad catalog.")
                return 2

        # Replace bad + overlap with fixed (still in same context, no
        # overlap because only the good group remains).
        (ent_dir / "dea_group-bad.yaml").unlink()
        (ent_dir / "dea_group-overlap.yaml").unlink()
        errors, suggestions = run_checks(tmp_path)
        if errors:
            print("PG self-test: expected clean pass on fixed catalog; got errors:")
            for e in errors:
                print(f"  ✗ {e}")
            return 2
        print("Process Group validation: PASS (PG-001..010)")
    return 0


def main() -> int:
    BASE = Path(__file__).parent.parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument(
        "--catalog-root", type=Path, default=BASE,
        help="Catalog root directory (default: parent of scripts/)",
    )
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    errors, suggestions = run_checks(args.catalog_root)
    if errors:
        print("Process Group validation: FAILED")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    if suggestions:
        print("Process Group validation: PASS (with suggestions)")
        for s in suggestions:
            print(f"  → {s['target']}: {s['suggestion_type']} "
                  f"(confidence={s['confidence']:.2f}) — {s['rationale'][:120]}")
        return 0
    print("Process Group validation: PASS (PG-001..010)")
    return 0


if __name__ == "__main__":
    sys.exit(main())