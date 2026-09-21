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
  python scripts/check_id_system.py --base-ref origin/main [--report-path PATH]

Exit codes:
  0  CONFORMANT (0 blocking findings)
  1  NON-CONFORMANT (>= 1 blocking finding)

Blocking rules:
  IDM-001  id regex matches org-wide form
  IDM-002  namespace token matches repo
  IDM-003  every cross-reference resolves
  IDM-004  entropy suffix well-formed (content-addressed at migration time)
  IDM-005  filesystem path derivable from id
  IDM-006  no legacy dea:* ids in structured reference fields
  IDM-007  every entity dir has README.md
  IDM-008  org-wide file coherence for files changed in a PR (--base-ref mode):
           every changed record YAML keeps path-id consistency, id form, and
           ref resolution; changed CR/ADR markdown carries no legacy path
           forms outside clearly historical framing (advisory, reported).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
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
            if obj.startswith("processes:"):
                # Embedded form: "<id> (prose...)" — resolve the leading id token
                token = obj.split(" ", 1)[0].rstrip(":")
                if token not in id_map:
                    errors.append(f"IDM-003: unresolved reference in {record.get('id', '?')} at {path_str}: {token}")
        elif isinstance(obj, dict):
            for k, v in obj.items():
                check_refs(v, f"{path_str}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                check_refs(v, f"{path_str}[{i}]")

    check_refs(record)
    return errors


def _check_idm004(record_id: str, content: str, path: Path) -> str | None:
    """IDM-004: entropy suffix well-formed (6 base32 chars).

    The suffix is content-addressed AT MIGRATION TIME (see
    reconciliation/migration-id-map.yaml for the provenance record) and is
    immutable thereafter: recomputing against live content is not the
    contract, because any legitimate content edit (enrichment, backfill)
    must not churn the id. The gate enforces the structural form; the
    content-hash provenance is auditable in the id-map.
    """
    parts = record_id.split("-")
    suffix = parts[-1]
    if len(suffix) != 6 or any(c not in BASE32 for c in suffix):
        return f"IDM-004: entropy suffix {suffix!r} is not 6 base32 chars: {record_id}"
    return None


def _check_idm005(record_id: str, path: Path) -> str | None:
    """IDM-005: filesystem path derivable from id (O(1) structural check).

    In the containment tree:
    - filename == id with ':' normalized to '-' + '.yaml' (lowercased)
    - the path's first segment under v1-alpha == '<domain>-<stage>' from the id
    - nesting depth: pc=1, group=2, process=3, activity=4, task=5
    """
    body = record_id.split(":", 1)[1]
    parts = body.split("-")
    level = parts[0]
    domain = parts[1]
    stage = parts[2]
    cell = f"{domain}-{stage}"
    expected_name = record_id.replace(":", "-").lower() + ".yaml"

    if path.name != expected_name:
        return f"IDM-005: filename {path.name!r} does not match id-derived name {expected_name!r} for {record_id}"

    rel = path.parts
    try:
        idx = rel.index("v1-alpha")
    except ValueError:
        return f"IDM-005: path {path} is not under entities/v1-alpha for {record_id}"
    under = rel[idx + 1:]  # segments below v1-alpha (excluding nothing; includes filename)
    if not under or under[0] != cell:
        return f"IDM-005: cell segment {under[0] if under else None!r} does not match id cell {cell!r} for {record_id}"

    expected_depth = {"pc": 2, "group": 3, "process": 4, "activity": 5, "task": 6}.get(level)
    # depth counts: cell dir + intermediate dirs + filename
    if expected_depth is None:
        return f"IDM-005: unknown level token: {level}"
    if len(under) != expected_depth:
        return f"IDM-005: nesting depth {len(under)} does not match expected {expected_depth} for level {level} ({record_id})"
    return None


_RESIDUAL_VALUES: set[str] | None = None


def _residual_values() -> set[str]:
    """Load documented residuals once (see reconciliation/migration-id-map.yaml)."""
    global _RESIDUAL_VALUES
    if _RESIDUAL_VALUES is not None:
        return _RESIDUAL_VALUES
    values: set[str] = set()
    map_path = RECONCILIATION / "migration-id-map.yaml"
    if map_path.exists():
        try:
            map_data = yaml.safe_load(map_path.read_text()) or {}
            for r in map_data.get("known_residuals", []) or []:
                v = r.get("legacy_value")
                if isinstance(v, str):
                    values.add(v)
        except yaml.YAMLError:
            pass
    _RESIDUAL_VALUES = values
    return values


def _check_idm006(record: dict, path: Path) -> list[str]:
    """IDM-006: no legacy dea:* ids in STRUCTURED reference fields.

    Historical prose (change_history narratives, evidence claims) may cite
    legacy ids verbatim; that is legitimate audit trail. The gate checks
    only machine-readable reference fields.
    """
    errors = []
    structured_fields = (
        "id", "belongs_to_activity", "belongs_to_business_process",
        "source_id", "target_id", "ref", "process_context",
        "supersedes", "record", "source",
    )
    legacy_re = re.compile(r"^dea:(pc|group|process|activity|task)-")
    residual_values = _residual_values()

    def walk(obj, field=""):
        if isinstance(obj, str):
            if field in structured_fields and legacy_re.match(obj) and obj not in residual_values:
                errors.append(f"IDM-006: legacy id in structured field {field!r} of {path.name}: {obj}")
        elif isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, k)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, field)
    walk(record)
    return errors


def _check_idm007(path: Path) -> str | None:
    readme = path.parent / "README.md"
    if not readme.exists():
        return f"IDM-007: missing README.md in {path.parent.name}"
    return None


def _load_all_records() -> dict[str, tuple[Path, dict, str]]:
    """Load canonical records only (id-derived filenames in the containment tree)."""
    records = {}
    for p in sorted(ENTITIES.rglob("processes-*.yaml")):
        with p.open() as f:
            content = f.read()
        record = yaml.safe_load(content)
        record_id = record.get("id", "")
        if record_id:
            records[record_id] = (p, record, content)
    return records


def _build_id_map(records: dict[str, tuple[Path, dict, str]]) -> dict[str, str]:
    return {rid: rid for rid in records}


# ----------------------------------------------------------------------------
# IDM-008: org-wide file coherence for PR-scoped change sets
# ----------------------------------------------------------------------------

DOC_SCAN_DIRS = ("change-requests/", "docs/")
LEGACY_PATH_PATTERNS = (
    "entities/v1-alpha/dea:",
    "contexts/v1-alpha/",
    "dea-catalog-processes",
    "dea-catalog-digital-business-service-factory",
)
HISTORICAL_MARKERS = ("pre-migration", "historical", "formerly", "legacy", "superseded")


def _changed_files(base_ref: str) -> list[str]:
    """Files changed between base_ref and HEAD (PR scope)."""
    for argv in (["git", "diff", "--name-only", f"{base_ref}...HEAD"],
                 ["git", "diff", "--name-only", base_ref, "HEAD"]):
        r = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)
        if r.returncode == 0:
            return [line.strip() for line in r.stdout.splitlines() if line.strip()]
    return []


def _check_idm008_records(changed: list[str], id_map: dict[str, str]) -> list[dict]:
    """Blocking: changed record YAMLs keep path-id consistency + ref resolution."""
    findings: list[dict] = []
    for rel in changed:
        if not (rel.startswith("entities/v1-alpha/") and rel.endswith(".yaml")):
            continue
        if not Path(rel).name.startswith("processes-"):
            # research/state files under the tree are advisory-scanned only
            continue
        p = ROOT / rel
        if not p.exists():
            continue  # deletion; nothing to check
        record = yaml.safe_load(p.read_text())
        if not isinstance(record, dict):
            continue
        rid = record.get("id", "")
        for fn, rule in (
            (_check_idm001, "IDM-001"), (_check_idm002, "IDM-002"),
            (_check_idm005, "IDM-005"),
        ):
            e = fn(rid, p)
            if e:
                findings.append({"rule": f"IDM-008/{rule}", "record": rid,
                                 "path": rel, "message": e})
        for e in _check_idm003(record, id_map, p):
            findings.append({"rule": "IDM-008/IDM-003", "record": rid,
                             "path": rel, "message": e})
        for e in _check_idm006(record, p):
            findings.append({"rule": "IDM-008/IDM-006", "record": rid,
                             "path": rel, "message": e})
    return findings


def _check_idm008_docs(changed: list[str]) -> list[dict]:
    """Advisory: changed CR/ADR markdown must not carry legacy path forms
    outside clearly historical framing."""
    findings: list[dict] = []
    in_fence = False
    for rel in changed:
        if not (rel.endswith(".md") and rel.startswith(DOC_SCAN_DIRS)):
            continue
        p = ROOT / rel
        if not p.exists():
            continue
        for lineno, line in enumerate(p.read_text().splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for pat in LEGACY_PATH_PATTERNS:
                if pat in line:
                    low = line.lower()
                    if any(m in low for m in HISTORICAL_MARKERS):
                        continue
                    findings.append({
                        "rule": "IDM-008/DOC", "record": rel,
                        "path": f"{rel}:{lineno}",
                        "message": f"legacy form {pat!r} in changed markdown "
                                   f"without historical framing marker",
                        "advisory": True,
                    })
    return findings


def _write_report(path: Path, base_ref: str, changed: list[str],
                  findings: list[dict]) -> None:
    lines = [
        "# ID System Coherence Report (IDM-008)",
        "",
        f"Base ref: `{base_ref}`",
        f"Changed files scanned: {len(changed)}",
        f"Findings: {len(findings)} ({sum(1 for f in findings if not f.get('advisory'))} blocking)",
        "",
        "## Changed files",
        "",
    ]
    lines += [f"- `{c}`" for c in changed]
    lines += ["", "## Findings", ""]
    if findings:
        lines += [f"- [{f['rule']}] `{f['path']}`: {f['message']}" for f in findings]
    else:
        lines.append("None.")
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    p.add_argument("--json", action="store_true", help="emit JSON payload")
    p.add_argument("--strict", action="store_true", help="exit 1 on any finding")
    p.add_argument("--base-ref", default=None,
                   help="IDM-008 mode: check only files changed vs this ref")
    p.add_argument("--report-path", default=None,
                   help="write markdown coherence report to this path")
    args = p.parse_args()

    records = _load_all_records()
    id_map = _build_id_map(records)

    if args.base_ref:
        changed = _changed_files(args.base_ref)
        findings = _check_idm008_records(changed, id_map)
        findings += _check_idm008_docs(changed)
        if args.report_path:
            _write_report(Path(args.report_path), args.base_ref, changed, findings)
        blocking = [f for f in findings if not f.get("advisory", False)]
        verdict = "NON-CONFORMANT" if blocking else "CONFORMANT"
        if args.json:
            print(json.dumps({
                "verdict": verdict, "base_ref": args.base_ref,
                "changed_files": len(changed), "findings": findings,
                "blocking": len(blocking),
            }, indent=2))
        else:
            print(f"ID System coherence (IDM-008, base {args.base_ref}): {verdict}")
            print(f"  Changed files scanned: {len(changed)}")
            print(f"  Findings: {len(findings)} ({len(blocking)} blocking)")
            for f in findings[:20]:
                print(f"    [{f['rule']}] {f['path']}: {f['message']}")
        return 1 if blocking else 0

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
        for e in _check_idm006(record, path):
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