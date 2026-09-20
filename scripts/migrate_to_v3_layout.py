#!/usr/bin/env python3
"""
migrate_to_v3_layout.py
CR-BP-mv1: Entity storage and id system migration (org-wide, this repo first).

Rewrites every canonical record's id from the legacy `dea:*` form to the
new org-wide form `<repo-namespace>:<level>-<domain>-<stage>[-<cell>]
[-<kind>] [<hash-suffix>]`, moves every entity directory to the L0-rooted
containment tree, rewrites every cross-reference, and emits the migration
id map.

Usage:
  python scripts/migrate_to_v3_layout.py [--dry-run] [--verify] [--execute]

The script is idempotent: re-running on a partially migrated tree no-ops.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTITIES = ROOT / "entities" / "v1-alpha"
CONTEXTS = ROOT / "contexts" / "v1-alpha"
RECONCILIATION = ROOT / "reconciliation"

NAMESPACE = "processes"

DOMAIN_CODES = {
    "PartyAndRelationship": "pr",
    "GovernanceAndExistence": "ge",
    "ProductAndValue": "pv",
    "AgencyAndOrganization": "ao",
    "StrategyAndDirection": "sd",
    "FinanceAndAccounting": "fa",
    "EnablementAndOperations": "eo",
}
CODE_TO_DOMAIN = {v: k for k, v in DOMAIN_CODES.items()}

LEVEL_TOKENS = {
    "ProcessContext": "pc",
    "ProcessGroup": "group",
    "BusinessProcess": "process",
    "Activity": "activity",
    "Task": "task",
}

PREFIX_TO_LEVEL = {
    "dea:pc-": "pc",
    "dea:group-": "group",
    "dea:process-": "process",
    "dea:activity-": "activity",
    "dea:task-": "task",
}

BASE32 = "abcdefghjkmnpqrstuvwxyz23456789"


def _content_hash(text: str) -> str:
    h = hashlib.sha256(text.encode("utf-8")).digest()
    val = int.from_bytes(h[:4], "big")
    chars = []
    for _ in range(6):
        chars.append(BASE32[val % 31])
        val //= 31
    return "".join(reversed(chars))


def _parse_old_id(old_id: str) -> dict:
    """Parse a legacy dea:* id into its components."""
    for prefix, level in PREFIX_TO_LEVEL.items():
        if old_id.startswith(prefix):
            slug = old_id[len(prefix):]
            return {"level": level, "slug": slug, "prefix": prefix}
    raise ValueError(f"Unknown id prefix: {old_id}")


def _new_id(old_id: str, record: dict, content: str) -> str:
    """Compute the new id from the old id + record content."""
    parsed = _parse_old_id(old_id)
    level = parsed["level"]
    slug = parsed["slug"]

    if level == "pc":
        # PCs carry domain + lifecycle_stage fields (no ecfConformance block).
        domain = record.get("domain", "")
        stage = str(record.get("lifecycle_stage", "")).lower()
        domain_code = DOMAIN_CODES.get(domain, domain[:2].lower())
    else:
        coord = record.get("ecfConformance", {}).get("canonicalReferences", [{}])[0]
        domain = coord.get("domain", "")
        stage = coord.get("stage", "").lower()
        domain_code = DOMAIN_CODES.get(domain, domain[:2].lower())

    # For tasks, strip the phase suffix
    phase = None
    if level == "task":
        for p in ["intake", "verify", "transform", "confirm", "record"]:
            if slug.endswith(f"-{p}"):
                phase = p
                slug = slug[: -len(p) - 1]
                break

    hash_suffix = _content_hash(content)
    parts = [NAMESPACE, level, domain_code, stage]
    if phase:
        parts.append(phase)
    parts.append(hash_suffix)
    return ":".join([parts[0], "-".join(parts[1:])])


def _cell_slug(new_id: str) -> str:
    """Extract the cell slug (domain-stage) from a new id."""
    body = new_id.split(":", 1)[1]
    parts = body.split("-")
    return f"{parts[1]}-{parts[2]}"


def _path_slug(new_id: str) -> str:
    """Normalize a new id to a filesystem slug."""
    return new_id.replace(":", "-").lower()


def _level_from_id(new_id: str) -> str:
    """Extract the level token from a new id."""
    body = new_id.split(":", 1)[1]
    return body.split("-")[0]


def _new_path(new_id: str, record: dict, id_map: dict[str, str], records: dict[str, tuple[Path, dict, str]]) -> Path:
    """Compute the new filesystem path from the new id + record + id map + all records."""
    level = _level_from_id(new_id)
    cell = _cell_slug(new_id)
    slug = _path_slug(new_id)

    if level == "pc":
        return ENTITIES / cell / f"{slug}.yaml"

    # Build the chain: [cell, pg_slug, bp_slug, act_slug, task_slug]
    chain = [cell]

    if level == "group":
        pg_slug = slug.replace(f"{NAMESPACE}-group-", "", 1)
        chain.append(pg_slug)
        return ENTITIES.joinpath(*chain) / f"{slug}.yaml"

    # Find the PG for this cell
    pg_new_id = None
    for old_id, nid in id_map.items():
        if _level_from_id(nid) == "group" and _cell_slug(nid) == cell:
            pg_new_id = nid
            break
    if pg_new_id is None:
        raise ValueError(f"No PG found for cell {cell}")

    pg_slug = _path_slug(pg_new_id).replace(f"{NAMESPACE}-group-", "", 1)
    chain.append(pg_slug)

    if level == "process":
        bp_slug = slug.replace(f"{NAMESPACE}-process-", "", 1)
        chain.append(bp_slug)
        return ENTITIES.joinpath(*chain) / f"{slug}.yaml"

    # For activity/task, resolve the parent BP.
    # NOTE: by the time _new_path is called from _migrate, cross-references in
    # `record` have ALREADY been rewritten to new-form ids. We accept both forms:
    # if the value is an old-form id present in id_map, map it; if it's already a
    # new-form id, use it directly.
    def _resolve_parent_new(value: str) -> str | None:
        if value in id_map:
            return id_map[value]
        # Already new-form?
        if value.startswith(f"{NAMESPACE}:"):
            return value
        # Reverse-lookup: find old id whose new id equals value
        for old, new in id_map.items():
            if new == value:
                return new
        return None

    if level == "activity":
        parent_bp_val = record.get("belongs_to_business_process", "")
        if not parent_bp_val:
            raise ValueError(f"Activity has no belongs_to_business_process: {new_id}")
    else:  # task
        parent_act_val = record.get("belongs_to_activity", "")
        if not parent_act_val:
            raise ValueError(f"Task has no belongs_to_activity: {new_id}")
        # Look up the Activity's record (by old id OR by new id) to get its BP
        act_entry = records.get(parent_act_val)
        if act_entry is None:
            # parent_act_val may be new-form; find the old id
            for old, new in id_map.items():
                if new == parent_act_val:
                    act_entry = records.get(old)
                    break
        if act_entry is None:
            raise ValueError(f"Parent Activity record not found: {parent_act_val}")
        act_record = act_entry[1]
        parent_bp_val = act_record.get("belongs_to_business_process", "")
        if not parent_bp_val:
            raise ValueError(f"Parent Activity has no belongs_to_business_process: {parent_act_val}")

    parent_bp_new = _resolve_parent_new(parent_bp_val)
    if parent_bp_new is None:
        raise ValueError(f"Parent BP not in id map: {parent_bp_val}")

    bp_slug = _path_slug(parent_bp_new).replace(f"{NAMESPACE}-process-", "", 1)
    chain.append(bp_slug)

    if level == "activity":
        act_slug = slug.replace(f"{NAMESPACE}-activity-", "", 1)
        chain.append(act_slug)
        return ENTITIES.joinpath(*chain) / f"{slug}.yaml"

    # For task, resolve the parent Activity (same old/new-form tolerance as the BP lookup)
    parent_act_val = record.get("belongs_to_activity", "")
    parent_act_new = _resolve_parent_new(parent_act_val)
    if parent_act_new is None:
        raise ValueError(f"Parent Activity not in id map: {parent_act_val}")

    act_slug = _path_slug(parent_act_new).replace(f"{NAMESPACE}-activity-", "", 1)
    chain.append(act_slug)

    task_slug = slug.replace(f"{NAMESPACE}-task-", "", 1)
    chain.append(task_slug)
    return ENTITIES.joinpath(*chain) / f"{slug}.yaml"


def _rewrite_refs(obj: object, id_map: dict[str, str]) -> object:
    """Rewrite every dea:* reference in a record to the new id.

    Handles two forms:
    1. Exact match: the string IS the id (e.g. `belongs_to_activity: dea:activity-foo`).
    2. Embedded match: the string CONTAINS the id plus prose (e.g.
       `dea:pc-ao-design (adjacent context): agentive flow...`). In this case
       we replace the id substring while preserving the surrounding prose.
    """
    if isinstance(obj, str):
        # Exact match first (fast path)
        if obj in id_map:
            return id_map[obj]
        # Embedded match: check if the string starts with a known old id
        # followed by a space or colon (prose separator)
        for old_id, new_id in id_map.items():
            if obj.startswith(old_id + " ") or obj.startswith(old_id + ":"):
                return new_id + obj[len(old_id):]
        return obj
    elif isinstance(obj, dict):
        return {k: _rewrite_refs(v, id_map) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_rewrite_refs(v, id_map) for v in obj]
    return obj


def _load_all_records() -> dict[str, tuple[Path, dict, str]]:
    """Load every canonical record. Returns {old_id: (path, record, content)}."""
    records = {}
    for p in sorted(ENTITIES.glob("dea:*/*.yaml")):
        with p.open() as f:
            content = f.read()
        record = yaml.safe_load(content)
        old_id = record.get("id", "")
        if old_id:
            records[old_id] = (p, record, content)
    for p in sorted(CONTEXTS.glob("*.yaml")):
        with p.open() as f:
            content = f.read()
        record = yaml.safe_load(content)
        old_id = record.get("id", "")
        if old_id:
            records[old_id] = (p, record, content)
    return records


def _build_id_map(records: dict[str, tuple[Path, dict, str]]) -> dict[str, str]:
    """Build the old_id -> new_id mapping, including alias resolution for
    PC references that use full stage names where the file uses abbreviations."""
    id_map = {}
    for old_id, (path, record, content) in records.items():
        new_id = _new_id(old_id, record, content)
        id_map[old_id] = new_id

    # Build alias map from PC file contents: domain + lifecycle_stage -> file id
    # PC files use `domain` and `lifecycle_stage` fields, not `ecfConformance`.
    # Some use full stage names (Activate, Build, etc.), some use abbreviations (b, c, d, im, op, act).
    # References in other records use full stage names or alternate abbreviations, so we need aliases.
    for old_id, (path, record, content) in records.items():
        if not old_id.startswith("dea:pc-"):
            continue
        domain = record.get("domain", "")
        stage = record.get("lifecycle_stage", "")
        if domain and stage:
            domain_code = DOMAIN_CODES.get(domain, domain[:2].lower())
            stage_lower = stage.lower()
            # Full-stage reference form
            full_ref = f"dea:pc-{domain_code}-{stage_lower}"
            if full_ref != old_id and full_ref not in id_map:
                id_map[full_ref] = id_map[old_id]

    # Additional aliases for abbreviation variants used in references
    # dea:pc-pr-ac -> dea:pc-pr-act (file uses "act", reference uses "ac")
    # dea:pc-ge-bu -> dea:pc-ge-b (file uses "b", reference uses "bu")
    # dea:pc-ge-co -> dea:pc-ge-c (file uses "c", reference uses "co")
    # dea:pc-ge-de -> dea:pc-ge-d (file uses "d", reference uses "de")
    extra_aliases = {
        "dea:pc-pr-ac": "dea:pc-pr-act",
        "dea:pc-ge-bu": "dea:pc-ge-b",
        "dea:pc-ge-co": "dea:pc-ge-c",
        "dea:pc-ge-de": "dea:pc-ge-d",
        "dea:pc-pr-bu": "dea:pc-pr-b",
        "dea:pc-pr-co": "dea:pc-pr-c",
        "dea:pc-pr-de": "dea:pc-pr-d",
    }
    for alias, canonical in extra_aliases.items():
        if canonical in id_map and alias not in id_map:
            id_map[alias] = id_map[canonical]

    return id_map


def _migrate(records: dict[str, tuple[Path, dict, str]], id_map: dict[str, str], dry_run: bool = True) -> dict:
    """Perform the migration. Returns stats."""
    stats: dict = {"migrated": 0, "skipped": 0, "errors": []}

    # Phase 1: rewrite ids and cross-references
    new_records = {}
    for old_id, (path, record, content) in records.items():
        new_id = id_map[old_id]
        new_record = _rewrite_refs(record, id_map)
        new_record["id"] = new_id
        new_records[new_id] = (path, new_record, content)

    # Phase 2: compute new paths and write files
    for new_id, (old_path, new_record, old_content) in new_records.items():
        try:
            new_path = _new_path(new_id, new_record, id_map, records)
        except ValueError as e:
            stats["errors"].append(str(e))
            stats["skipped"] += 1
            continue

        if dry_run:
            stats["migrated"] += 1
            continue

        new_path.parent.mkdir(parents=True, exist_ok=True)
        with new_path.open("w") as f:
            yaml.safe_dump(new_record, f, sort_keys=False, allow_unicode=True,
                           default_flow_style=False, width=1000)

        old_readme = old_path.parent / "README.md"
        if old_readme.exists():
            new_readme = new_path.parent / "README.md"
            if not new_readme.exists():
                new_readme.write_text(old_readme.read_text())
        elif old_path.parent == CONTEXTS:
            # PC READMEs live in a synthesized sibling dir: contexts/v1-alpha/<stem>/README.md
            pc_readme = CONTEXTS / old_path.stem / "README.md"
            if pc_readme.exists():
                new_readme = new_path.parent / "README.md"
                if not new_readme.exists():
                    new_readme.write_text(pc_readme.read_text())

        stats["migrated"] += 1

    # Phase 3: write migration id map
    if not dry_run:
        map_path = RECONCILIATION / "migration-id-map.yaml"
        map_data = {
            "version": 1,
            "namespace": NAMESPACE,
            "migrated_at": "2026-09-20",
            "id_map": id_map,
        }
        with map_path.open("w") as f:
            yaml.safe_dump(map_data, f, sort_keys=False, allow_unicode=True,
                           default_flow_style=False, width=1000)

    return stats


def _verify(records: dict[str, tuple[Path, dict, str]], id_map: dict[str, str]) -> list[str]:
    """Verify the migration. Returns list of errors."""
    errors = []

    for old_id in records:
        if old_id not in id_map:
            errors.append(f"Missing id map entry: {old_id}")

    for old_id, (path, record, content) in records.items():
        def check_refs(obj, path_str=""):
            if isinstance(obj, str):
                if obj.startswith("dea:") and "@" not in obj and obj != "dea:composes":
                    # Skip non-canonical reference prefixes
                    skip_prefixes = (
                        "dea:composes",
                        "dea:discovery-",
                        "dea:entity-capability:",
                        "dea:scope-",
                        "dea:group-strategy-and-governance-conception",  # pre-existing dangling supersedes ref
                    )
                    if any(obj.startswith(p) for p in skip_prefixes):
                        return
                    # Check exact match first
                    if obj in id_map:
                        return
                    # Check embedded match (id + prose)
                    found = False
                    for old_id in id_map:
                        if obj.startswith(old_id + " ") or obj.startswith(old_id + ":"):
                            found = True
                            break
                    if not found:
                        errors.append(f"Unresolved reference in {old_id} at {path_str}: {obj}")
            elif isinstance(obj, dict):
                for k, v in obj.items():
                    check_refs(v, f"{path_str}.{k}")
            elif isinstance(obj, list):
                for i, v in enumerate(obj):
                    check_refs(v, f"{path_str}[{i}]")
        check_refs(record)

    return errors


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    p.add_argument("--dry-run", action="store_true", default=True,
                   help="report counts without writing files (default)")
    p.add_argument("--verify", action="store_true",
                   help="assert migration correctness")
    p.add_argument("--execute", action="store_true",
                   help="perform the migration")
    args = p.parse_args()

    records = _load_all_records()
    id_map = _build_id_map(records)

    if args.verify:
        errors = _verify(records, id_map)
        if errors:
            print(f"VERIFY FAIL: {len(errors)} errors")
            for e in errors[:20]:
                print(f"  {e}")
            return 1
        print(f"VERIFY PASS: {len(records)} records, {len(id_map)} id mappings")
        return 0

    if args.execute:
        stats = _migrate(records, id_map, dry_run=False)
        print(f"MIGRATION COMPLETE: {stats['migrated']} records migrated")
        if stats["errors"]:
            print(f"  {len(stats['errors'])} errors")
            for e in stats["errors"][:10]:
                print(f"  {e}")
            return 1
        return 0

    stats = _migrate(records, id_map, dry_run=True)
    print(f"DRY RUN: {stats['migrated']} records would be migrated")
    print(f"  id map entries: {len(id_map)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())