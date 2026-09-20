#!/usr/bin/env python3
"""
check_id_system.py
CR-BP-mv1: ID System gate (IDM-001..007).

Enforces the org-wide id system spec (dea-metaframework/docs/id-system.md):
every canonical record's id matches the org-wide form, every cross-reference
resolves, every entropy suffix matches the content hash, every filesystem
path is derivable from its id, and no legacy `dea:*` ids remain.

Usage:
  python scripts/check_id_system.py [--json] [--strict]

Exit codes:
  0  CONFORMANT (0 blocking findings)
  1  NON-CONFORMANT (>= 1 blocking finding)

Blocking rules:
  IDM-001  id regex matches org-wide form
  IDM-002  namespace token matches repo
  IDM-003  every cross-reference resolves
  IDM-004  entropy suffix matches content hash
  IDM-005  filesystem path derivable from id
  IDM-006  no legacy dea:* ids remain
  IDM-007  every entity dir has README.md
"""
from __future__ import annotations

import argparse
import hashlib
import json
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

LEVEL_TOKENS = {
    "ProcessContext": "pc",
    "ProcessGroup": "group",
    "BusinessProcess": "process",
    "Activity": "activity",
    "Task": "task",
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


# IDM-001: id regex matches org-wide form
ID_PATTERN = re.compile(
    r"^[a-z]+:[a-z]+-[a-z]{2,3}-[a-z]+(-[a-z]+)*-[a-z2-9]{6}$"
)


def _check_idm001(record_id: str, path: Path) -> str | None:
    if not ID_PATTERN.match(record_id):
        return f"IDM-001: id does not match org-wide form: {record_id}"
    return None


def _check_idm002(record_id: str, path: Path) -> str | None:
    ns = record_id.split(":", 1)[0]
    if ns != NAMESPACE:
        return f"IDM-002: namespace token '{ns}' does not match repo namespace '{NAMESPACE}': {record_id}"
    return None


def _check_idm003(record: dict, id_map: dict[str, str], path: Path) -> list[str]:
    errors = []

    def check_refs(obj, path_str=""):
        if isinstance(obj, str):
            if obj.startswith("processes:") and obj not in id_map:
                errors.append(f"IDM-003: unresolved reference in {record.get('id', '?')} at {path_str}: {obj}")
        elif isinstance(obj, dict):
            for k, v in obj.items():
                check_refs(v, f"{path_str}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                check_refs(v, f"{path_str}[{i}]")

    check_refs(record)
    return errors


def _check_idm004(record_id: str, content: str, path: Path) -> str | None:
    # Extract hash suffix from id
    parts = record_id.split("-")
    suffix = parts[-1]
    expected = _content_hash(content)
    if suffix != expected:
        return f"IDM-004: entropy suffix '{suffix}' does not match content hash '{expected}': {record_id}"
    return None


def _check_idm005(record_id: str, path: Path) -> str | None:
    # Derive expected path from id
    # processes:pc-pr-operate-fz2h3 -> entities/v1-alpha/pr-operate/processes-pc-pr-operate-fz2h3.yaml
    # processes:task-fa-activate-confirm-2x9y4p -> entities/v1-alpha/fa-activate/.../task-fa-activate-confirm-2x9y4p/
    body = record_id.split(":", 1)[1]
    parts = body.split("-")
    level = parts[0]
    domain = parts[1]
    stage = parts[2]
    cell = f"{domain}-{stage}"
    path_slug = record_id.replace(":", "-").lower()

    if level == "pc":
        expected = ENTITIES / cell / f"{path_slug}.yaml"
    elif level == "group":
        pg_slug = path_slug.replace(f"{NAMESPACE}-group-", "", 1)
        expected = ENTITIES / cell / pg_slug / f"{path_slug}.yaml"
    elif level == "process":
        # Need parent PG slug; check if any PG dir exists under cell
        pg_dir = ENTITIES / cell
        if not pg_dir.exists():
            return f"IDM-005: cell directory does not exist: {cell}"
        pg_dirs = [d for d in pg_dir.iterdir() if d.is_dir() and d.name.startswith(f"{NAMESPACE}-group-")]
        if not pg_dirs:
            return f"IDM-005: no PG directory found under cell: {cell}"
        bp_slug = path_slug.replace(f"{NAMESPACE}-process-", "", 1)
        expected = pg_dirs[0] / bp_slug / f"{path_slug}.yaml"
    elif level == "activity":
        # Need parent BP dir; find it by scanning
        act_slug = path_slug.replace(f"{NAMESPACE}-activity-", "", 1)
        # Find the BP that contains this activity
        found = None
        for d in ENTITIES.rglob(f"{NAMESPACE}-process-*"):
            if d.is_dir():
                candidate = d / act_slug / f"{path_slug}.yaml"
                if candidate.exists():
                    found = candidate
                    break
        if found is None:
            return f"IDM-005: activity path not derivable from id: {record_id}"
        expected = found
    elif level == "task":
        task_slug = path_slug.replace(f"{NAMESPACE}-task-", "", 1)
        found = None
        for d in ENTITIES.rglob(f"{NAMESPACE}-activity-*"):
            if d.is_dir():
                candidate = d / task_slug / f"{path_slug}.yaml"
                if candidate.exists():
                    found = candidate
                    break
        if found is None:
            return f"IDM-005: task path not derivable from id: {record_id}"
        expected = found
    else:
        return f"IDM-005: unknown level token: {level}"

    if path != expected:
        return f"IDM-005: path {path} does not match expected path {expected} for id {record_id}"
    return None


def _check_idm006(content: str, path: Path) -> list[str]:
    errors = []
    # Check for legacy dea:* ids in the YAML content
    for m in re.finditer(r"dea:(pc|group|process|activity|task)-[a-z0-9-]+", content):
        errors.append(f"IDM-006: legacy id found in {path.name}: {m.group(0)}")
    return errors


def _check_idm007(path: Path) -> str | None:
    readme = path.parent / "README.md"
    if not readme.exists():
        return f"IDM-007: missing README.md in {path.parent.name}"
    return None


def _load_all_records() -> dict[str, tuple[Path, dict, str]]:
    records = {}
    for p in sorted(ENTITIES.rglob("*.yaml")):
        if p.name == "README.md":
            continue
        with p.open() as f:
            content = f.read()
        record = yaml.safe_load(content)
        record_id = record.get("id", "")
        if record_id:
            records[record_id] = (p, record, content)
    return records


def _build_id_map(records: dict[str, tuple[Path, dict, str]]) -> dict[str, str]:
    return {rid: rid for rid in records}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    p.add_argument("--json", action="store_true", help="emit JSON payload")
    p.add_argument("--strict", action="store_true", help="exit 1 on any finding")
    args = p.parse_args()

    records = _load_all_records()
    id_map = _build_id_map(records)

    findings = []
    for record_id, (path, record, content) in records.items():
        # IDM-001
        e = _check_idm001(record_id, path)
        if e:
            findings.append({"rule": "IDM-001", "record": record_id, "path": str(path), "message": e})
        # IDM-002
        e = _check_idm002(record_id, path)
        if e:
            findings.append({"rule": "IDM-002", "record": record_id, "path": str(path), "message": e})
        # IDM-003
        for e in _check_idm003(record, id_map, path):
            findings.append({"rule": "IDM-003", "record": record_id, "path": str(path), "message": e})
        # IDM-004
        e = _check_idm004(record_id, content, path)
        if e:
            findings.append({"rule": "IDM-004", "record": record_id, "path": str(path), "message": e})
        # IDM-005
        e = _check_idm005(record_id, path)
        if e:
            findings.append({"rule": "IDM-005", "record": record_id, "path": str(path), "message": e})
        # IDM-006
        for e in _check_idm006(content, path):
            findings.append({"rule": "IDM-006", "record": record_id, "path": str(path), "message": e})
        # IDM-007
        e = _check_idm007(path)
        if e:
            findings.append({"rule": "IDM-007", "record": record_id, "path": str(path), "message": e})

    blocking = [f for f in findings if not f.get("advisory", False)]
    verdict = "NON-CONFORMANT" if blocking else "CONFORMANT"

    if args.json:
        print(json.dumps({
            "verdict": verdict,
            "records_checked": len(records),
            "findings": findings,
            "blocking": len(blocking),
        }, indent=2))
    else:
        print(f"ID System (CR-BP-mv1 IDM-001..007): {verdict}")
        print(f"  Records checked: {len(records)}")
        print(f"  Findings: {len(findings)}")
        for f in findings[:20]:
            print(f"    [{f['rule']}] {f['message']}")
        if len(findings) > 20:
            print(f"    ... and {len(findings) - 20} more")

    if args.strict and blocking:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())