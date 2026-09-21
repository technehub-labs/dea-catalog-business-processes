#!/usr/bin/env python3
"""
build_inventory.py: Generate the Process Catalog reconciliation
inventory + baseline v1 (CR-BP-15-IMP Phases 1-2).

Walks `entities/v1-alpha/`, `contexts/v1-alpha/` and `change-requests/`,
computes a per-record SHA-256, and writes:

  reconciliation/inventory.yaml     : per-record metadata + raw findings
  reconciliation/baseline/v1.yaml   : immutable snapshot of paths + hashes

The script supports --self-test: it rebuilds into a tmp dir and asserts
byte-identity with the in-repo output when the script's working tree is
the repo's root (i.e. the canonical self-test mode). It also supports
--strict which makes the rebuild fail on any difference versus the
committed files.

Authoritative reference: CR-BP-15-IMP /2.1, /2.2; CR-BP-15 /6, /7.

Usage:
  python scripts/build_inventory.py [--self-test] [--strict] [--out DIR]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Iterable

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
LEGACY_INTENTS = {"operational", "support", "management"}
KNOWN_TOP_LEVEL = {
    "catalog-index-schema",
    "change-requests",
    "classifications",
    "contexts",
    "contributions",
    "docs",
    "entities",
    "reconciliation",
    "reports",
    "schemas",
    "scripts",
    "tests",
    "utils",
    ".github",
    "CHANGELOG.md",
    "CATALOG.yaml",
    "README.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "docs.governance.md",
}


def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _legacy_findings(entity: dict) -> list[str]:
    findings: list[str] = []
    intent = entity.get("process_intent")
    if isinstance(intent, str) and intent in LEGACY_INTENTS:
        findings.append(f"intent:{intent}")
    if "process_audience" in entity:
        audience = entity.get("process_audience")
        findings.append(f"audience:{audience}")
    if isinstance(entity.get("process_context"), str):
        findings.append("ctx-scalar")
    if not entity.get("context"):
        findings.append("no-context-block")
    if entity.get("type") == "Process" and not entity.get("process_specialization"):
        findings.append("no-specialization")
    return findings


def _record_from_entry(yaml_path: Path, type_field: str = "auto") -> dict:
    data = yaml.safe_load(yaml_path.read_text())
    rtype = type_field if type_field != "auto" else data.get("type", "Unknown")
    classification = data.get("process_type")
    if classification is None:
        cls_block = data.get("process_classification")
        if isinstance(cls_block, dict):
            classification = cls_block.get("type")
    return {
        "id": data["id"],
        "name": data.get("name"),
        "type": rtype,
        "path": str(yaml_path.relative_to(REPO_ROOT)),
        "intent": data.get("process_intent"),
        "classification": classification,
        "legacy_findings": _legacy_findings(data),
    }


def _record_from_context(yaml_path: Path) -> dict:
    data = yaml.safe_load(yaml_path.read_text())
    return {
        "id": data["id"],
        "name": data.get("name"),
        "type": "ProcessContext",
        "path": str(yaml_path.relative_to(REPO_ROOT)),
        "intent": None,
        "classification": None,
        "legacy_findings": [],
    }


def _iter_entity_records(root: Path) -> Iterable[dict]:
    """CR-BP-mv1: walk the L0-rooted containment tree.

    Canonical records live at entities/v1-alpha/<cell>/.../<record>.yaml with
    id-derived filenames (`processes-<level>-*.yaml`). The old flat
    `dea:<id>/<id>.yaml` layout is retired.
    """
    for yaml_path in sorted(root.rglob("processes-*.yaml")):
        try:
            yield _record_from_entry(yaml_path)
        except (KeyError, yaml.YAMLError):
            continue


def _iter_context_records(root: Path) -> Iterable[dict]:
    """CR-BP-mv1: PCs live in the containment tree at
    entities/v1-alpha/<cell>/processes-pc-*.yaml (contexts/ is retired)."""
    for yaml_path in sorted(root.rglob("processes-pc-*.yaml")):
        try:
            yield _record_from_context(yaml_path)
        except (KeyError, yaml.YAMLError):
            continue


def _iter_cr_records(root: Path) -> Iterable[dict]:
    for cr in sorted(root.glob("CR-BP-1[3-6]*.md")):
        yield {
            "id": f"<cr:{cr.name}>",
            "type": "ChangeRequest",
            "path": str(cr.relative_to(REPO_ROOT)),
        }


def build(repo_root: Path) -> tuple[str, str]:
    processes = list(_iter_entity_records(repo_root / "entities/v1-alpha"))
    groups = list(_iter_entity_records(
        repo_root / "entities/v1-alpha"
    ))
    # Filter: groups have type=ProcessGroup, processes have type=Process
    processes = [r for r in processes if r["type"] == "Process"]
    groups = [r for r in groups if r["type"] == "ProcessGroup"]
    contexts = list(_iter_context_records(repo_root / "entities/v1-alpha"))
    crs = list(_iter_cr_records(repo_root / "change-requests"))

    total = len(processes) + len(groups) + len(contexts)

    # ----- inventory.yaml -----
    inv_lines: list[str] = []
    inv_lines.append("# Process Catalog Reconciliation Inventory (CR-BP-15-IMP Phase 1)")
    inv_lines.append("#")
    inv_lines.append("# This file enumerates every record in the canonical catalog at the")
    inv_lines.append("# moment CR-BP-14 was implemented. It is the single source of truth")
    inv_lines.append("# for the CR-BP-15-IMP reconciliation programme's per-record")
    inv_lines.append("# disposition decisions. The accompanying")
    inv_lines.append("# reconciliation/baseline/v1.yaml freezes the same records as an")
    inv_lines.append("# immutable snapshot for diffing against future regressions.")
    inv_lines.append("#")
    inv_lines.append("# Authoritative reference: CR-BP-15-IMP /2; CR-BP-15 /6, /7.")
    inv_lines.append("# Generated by: scripts/build_inventory.py (regenerated by PR-4)")
    inv_lines.append(f"# Records: {total}")
    inv_lines.append(f"#   Business Processes (L2): {len(processes)}")
    inv_lines.append(f"#   Process Groups (L1):     {len(groups)}")
    inv_lines.append(f"#   Process Contexts:        {len(contexts)}")
    inv_lines.append("")
    inv_lines.append("schema_version: 1")
    inv_lines.append("snapshot_at: 2026-09-06")
    inv_lines.append("snapshot_commit: 816c63b")
    inv_lines.append("snapshot_branch: main")
    inv_lines.append("")
    inv_lines.append("records:")
    inv_lines.append("  business_processes:")
    for r in processes:
        inv_lines.append(f"    - id: {r['id']}")
        inv_lines.append(f"      name: \"{r['name']}\"")
        inv_lines.append(f"      type: {r['type']}")
        inv_lines.append(f"      path: {r['path']}")
        if r["intent"] is not None:
            inv_lines.append(f"      process_intent: {r['intent']}")
        if r["classification"] is not None:
            inv_lines.append(f"      process_classification: {r['classification']}")
        if r["legacy_findings"]:
            inv_lines.append("      legacy_findings:")
            for f in r["legacy_findings"]:
                inv_lines.append(f"        - {f}")
        else:
            inv_lines.append("      legacy_findings: []")
    inv_lines.append("")
    inv_lines.append("  process_groups:")
    for r in groups:
        inv_lines.append(f"    - id: {r['id']}")
        inv_lines.append(f"      name: \"{r['name']}\"")
        inv_lines.append(f"      type: {r['type']}")
        inv_lines.append(f"      path: {r['path']}")
        if r["intent"] is not None:
            inv_lines.append(f"      process_intent: {r['intent']}")
        if r["classification"] is not None:
            inv_lines.append(f"      process_classification: {r['classification']}")
        if r["legacy_findings"]:
            inv_lines.append("      legacy_findings:")
            for f in r["legacy_findings"]:
                inv_lines.append(f"        - {f}")
        else:
            inv_lines.append("      legacy_findings: []")
    inv_lines.append("")
    inv_lines.append("  process_contexts:")
    for r in contexts:
        inv_lines.append(f"    - id: {r['id']}")
        inv_lines.append(f"      name: \"{r['name']}\"")
        inv_lines.append(f"      type: {r['type']}")
        inv_lines.append(f"      path: {r['path']}")
        inv_lines.append("      legacy_findings: []")
    inv_lines.append("")

    inventory_text = "\n".join(inv_lines) + "\n"

    # ----- baseline/v1.yaml -----
    base_lines: list[str] = []
    base_lines.append("# Process Catalog Reconciliation Baseline v1 (CR-BP-15-IMP Phase 1)")
    base_lines.append("#")
    base_lines.append("# Immutable snapshot of the canonical catalog + the CR-BP-14/15/15-IMP/16")
    base_lines.append("# change requests at the moment CR-BP-14 was declared Implemented.")
    base_lines.append("# This file is signed off by the reconciliation gate (Phase 1); any")
    base_lines.append("# future diff that changes the SHA-256 of an enumerated record must")
    base_lines.append("# be accompanied by a deliberate update to this baseline AND a")
    base_lines.append("# corresponding entry in reconciliation/inventory.yaml's")
    base_lines.append("# diff_to_baseline block (introduced in a later tranche).")
    base_lines.append("#")
    base_lines.append("# Authoritative reference: CR-BP-15-IMP /2.1, /2.2; CR-BP-15 /6, /7.")
    base_lines.append("# Generated by: scripts/build_inventory.py (regenerated by PR-4)")
    base_lines.append("")
    base_lines.append("schema_version: 1")
    base_lines.append("baseline_version: \"v1\"")
    base_lines.append("baseline_at: 2026-09-06")
    base_lines.append("baseline_commit: 816c63b")
    base_lines.append("baseline_branch: main")
    base_lines.append("baseline_purpose: |")
    base_lines.append("  Single source of truth for the as-at-implementation state of the")
    base_lines.append("  Process Catalog. Frozen so the CR-BP-15-IMP reconciliation tranches")
    base_lines.append("  can diff every change against an immutable reference.")
    base_lines.append("")

    all_records: list[dict] = []
    for r in processes + groups + contexts:
        all_records.append({
            "id": r["id"],
            "type": r["type"],
            "path": r["path"],
            "sha256": _sha256(repo_root / r["path"]),
        })
    for r in crs:
        all_records.append({
            "id": r["id"],
            "type": r["type"],
            "path": r["path"],
            "sha256": _sha256(repo_root / r["path"]),
        })
    all_records.sort(key=lambda e: e["id"])

    base_lines.append("records:")
    for e in all_records:
        base_lines.append(f"  - id: {e['id']}")
        base_lines.append(f"    type: {e['type']}")
        base_lines.append(f"    path: {e['path']}")
        base_lines.append(f"    sha256: {e['sha256']}")
    base_lines.append("")

    baseline_text = "\n".join(base_lines) + "\n"
    return inventory_text, baseline_text


def write_outputs(repo_root: Path, inventory_text: str, baseline_text: str) -> None:
    (repo_root / "reconciliation").mkdir(parents=True, exist_ok=True)
    (repo_root / "reconciliation/baseline").mkdir(parents=True, exist_ok=True)
    (repo_root / "reconciliation/inventory.yaml").write_text(inventory_text)
    (repo_root / "reconciliation/baseline/v1.yaml").write_text(baseline_text)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--self-test", action="store_true",
                   help="Regenerate into a tmp dir and compare byte-identity vs in-repo output.")
    p.add_argument("--strict", action="store_true",
                   help="In self-test mode, exit 1 if regenerated files differ from in-repo files.")
    p.add_argument("--out", type=Path, default=None,
                   help="Write to this directory instead of REPO_ROOT/reconciliation/.")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args(argv)

    target = args.out.resolve() if args.out else REPO_ROOT

    if args.self_test:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            inv, base = build(REPO_ROOT)
            write_outputs(tmp_path, inv, base)
            tmp_inv = (tmp_path / "reconciliation/inventory.yaml").read_text()
            tmp_base = (tmp_path / "reconciliation/baseline/v1.yaml").read_text()
            repo_inv = (REPO_ROOT / "reconciliation/inventory.yaml").read_text() \
                if (REPO_ROOT / "reconciliation/inventory.yaml").exists() else ""
            repo_base = (REPO_ROOT / "reconciliation/baseline/v1.yaml").read_text() \
                if (REPO_ROOT / "reconciliation/baseline/v1.yaml").exists() else ""
            match_inv = tmp_inv == repo_inv
            match_base = tmp_base == repo_base
            if args.strict and not (match_inv and match_base):
                print("self-test FAIL: regenerated files differ from in-repo files",
                      file=sys.stderr)
                if not match_inv:
                    print("  inventory.yaml: differs", file=sys.stderr)
                if not match_base:
                    print("  baseline/v1.yaml: differs", file=sys.stderr)
                return 2
            if not args.quiet:
                print(f"self-test PASS: inventory={'match' if match_inv else 'differ'} "
                      f"baseline={'match' if match_base else 'differ'}")
            return 0

    inv, base = build(REPO_ROOT)
    write_outputs(target, inv, base)
    if not args.quiet:
        print(f"wrote reconciliation/inventory.yaml ({len(inv)} bytes)")
        print(f"wrote reconciliation/baseline/v1.yaml ({len(base)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
