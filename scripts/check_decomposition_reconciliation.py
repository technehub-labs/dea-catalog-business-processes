#!/usr/bin/env python3
"""
check_decomposition_reconciliation.py
=====================================

Decomposition reconciliation validator (CR-BP-94-EXT-05).

Codifies DOC-021..025, the parent-child decomposition traceability
rules that complement DOC-001..020 (CR-BP-94-EXT-01 / EXT-02 / EXT-04).
The decomposition chain is:

  L0 (ProcessContext) -- top-level cell
    |
    v  process_groups: list[str]
  L1 (ProcessGroup) -- bounded grouping
    |  process_context: str  (L0 id)
    v  composes: list[str]
  L2 (Process) -- business process
    |  part_of: list[str]  (L1 ids)
    v  composes: list[str]
  L3 (Activity) -- bounded unit
    |  belongs_to_business_process: str  (L2 id)
    v  composes: list[str]
  L4 (Task) -- leaf
       belongs_to_activity: str  (L3 id)

The five rules:

  DOC-021  L1.process_context references a valid L0 parent.
  DOC-022  L2.part_of references valid L1 parents.
  DOC-023  L3.belongs_to_business_process references a valid L2 parent.
  DOC-024  L4.belongs_to_activity references a valid L3 parent.
  DOC-025  Reverse direction. Every child referenced in a parent's
           process_groups / composes list actually exists in the
           catalog (no orphans, no dangling refs).

The validator reads the EXT-04 validation manifest at
reconciliation/validation-manifest.json to gate on records whose
README is well-formed. Records with unresolved DOC-016/017/018
findings are skipped (the decomposition chain for those records
is not in a known state).

The validator is wired as gate [35] Decomposition Reconciliation
(advisory) in scripts/conformance_result.py. EXT-06 flips the
gate to blocking.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError:
    sys.stderr.write("ERROR: PyYAML is required.\n")
    sys.exit(2)


# -----------------------------------------------------------------------------
# Manifest schema version (bump on structural change to the manifest format).
# -----------------------------------------------------------------------------

MANIFEST_SCHEMA_VERSION = 1
MANIFEST_GENERATOR = "scripts/check_decomposition_reconciliation.py"
MANIFEST_PARENT_CR = "CR-BP-94-EXT-05"

# Id-marker to level mapping (shared with EXT-04).
_ID_LEVEL_MARKER: dict[str, str] = {
    "pc": "L0", "group": "L1", "process": "L2",
    "activity": "L3", "task": "L4",
}
_ID_LEVEL_RE = re.compile(r":(pc|group|process|activity|task)-")


def _resolve_level(record: dict) -> str | None:
    entity_type = record.get("type")
    if isinstance(entity_type, str):
        # Map ProcessContext -> L0 explicitly.
        return {
            "ProcessContext": "L0",
            "ProcessGroup": "L1",
            "Process": "L2",
            "Activity": "L3",
            "Task": "L4",
        }.get(entity_type)
    rid = record.get("id")
    if isinstance(rid, str):
        m = _ID_LEVEL_RE.search(rid)
        if m:
            return _ID_LEVEL_MARKER.get(m.group(1))
    return None


def _load_validation_manifest(catalog_root: Path) -> dict:
    """Load the EXT-04 validation manifest if present; else empty dict."""
    path = catalog_root / "reconciliation" / "validation-manifest.json"
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _record_passes_validation_gate(
    record_id: str, validation_manifest: dict,
) -> bool:
    """Return True iff the record has no unresolved DOC-016/017/018 findings.

    Records with unresolved DOC-019/020 (L0 metrics / cell_charter)
    are NOT skipped; the decomposition chain does not depend on
    the metrics or cell_charter fields.
    """
    if not validation_manifest:
        return True
    blocking_rules = ("DOC-016", "DOC-017", "DOC-018")
    for finding in validation_manifest.get("findings", []):
        if (finding.get("record_id") == record_id
                and finding.get("rule") in blocking_rules):
            return False
    return True


# -----------------------------------------------------------------------------
# Findings
# -----------------------------------------------------------------------------


def evaluate(
    records: Iterable[tuple[Path, dict]],
    id_index: dict[str, dict],
    validation_manifest: dict,
) -> list[dict]:
    """Run DOC-021..025 against every (path, record) pair.

    Args:
        records: iterable of (yaml_path, record_dict).
        id_index: mapping from canonical id to record_dict. Built by
            `_build_id_index` from the same record set.
        validation_manifest: the EXT-04 validation manifest (used to
            gate DOC-021..025 on records whose README is well-formed).

    Returns:
        List of findings, one per (record, rule) pair that fails.
    """
    findings: list[dict] = []

    for path, record in records:
        rec_id = record.get("id")
        if not isinstance(rec_id, str):
            continue
        level = _resolve_level(record)
        if level is None:
            continue

        # Gate on EXT-04 validation: skip records with unresolved
        # DOC-016/017/018 findings.
        if not _record_passes_validation_gate(rec_id, validation_manifest):
            continue

        # DOC-021: L1.process_context references a valid L0.
        if level == "L1":
            pc_ref = record.get("process_context")
            if isinstance(pc_ref, str) and pc_ref not in id_index:
                findings.append({
                    "rule": "DOC-021",
                    "record_id": rec_id,
                    "level": level,
                    "diagnostic": f"L1.process_context={pc_ref!r} does not "
                                   f"reference a known L0 id",
                    "parent_ref": pc_ref,
                    "advisory": True,
                })

        # DOC-022: L2.part_of references valid L1 parents.
        if level == "L2":
            part_of = record.get("part_of")
            if isinstance(part_of, list):
                for ref in part_of:
                    if isinstance(ref, str) and ref not in id_index:
                        findings.append({
                            "rule": "DOC-022",
                            "record_id": rec_id,
                            "level": level,
                            "diagnostic": f"L2.part_of contains {ref!r} "
                                           f"which is not a known L1 id",
                            "parent_ref": ref,
                            "advisory": True,
                        })

        # DOC-023: L3.belongs_to_business_process references a valid L2.
        if level == "L3":
            bp_ref = record.get("belongs_to_business_process")
            if isinstance(bp_ref, str) and bp_ref not in id_index:
                findings.append({
                    "rule": "DOC-023",
                    "record_id": rec_id,
                    "level": level,
                    "diagnostic": f"L3.belongs_to_business_process={bp_ref!r} "
                                   f"does not reference a known L2 id",
                    "parent_ref": bp_ref,
                    "advisory": True,
                })

        # DOC-024: L4.belongs_to_activity references a valid L3.
        if level == "L4":
            act_ref = record.get("belongs_to_activity")
            if isinstance(act_ref, str) and act_ref not in id_index:
                findings.append({
                    "rule": "DOC-024",
                    "record_id": rec_id,
                    "level": level,
                    "diagnostic": f"L4.belongs_to_activity={act_ref!r} "
                                   f"does not reference a known L3 id",
                    "parent_ref": act_ref,
                    "advisory": True,
                })

    # DOC-025: Reverse direction. Build child -> parents index and
    # check that every child referenced in a parent's child list
    # actually exists in the catalog.
    seen_pairs: set[tuple[str, str, str]] = set()  # (parent_id, child_id, kind)
    for path, record in records:
        rec_id = record.get("id")
        if not isinstance(rec_id, str):
            continue
        level = _resolve_level(record)
        if level is None:
            continue
        if not _record_passes_validation_gate(rec_id, validation_manifest):
            continue

        if level == "L0":
            # L0.process_groups is a list of L1 child ids.
            pgs = record.get("process_groups")
            if isinstance(pgs, list):
                for child in pgs:
                    if isinstance(child, str) and child not in id_index:
                        findings.append({
                            "rule": "DOC-025",
                            "record_id": rec_id,
                            "level": level,
                            "diagnostic": f"L0.process_groups contains {child!r} "
                                           f"which is not a known record id",
                            "child_ref": child,
                            "advisory": True,
                        })

        if level == "L1":
            # L1.composes is a list of L2 child ids.
            composes = record.get("composes")
            if isinstance(composes, list):
                for child in composes:
                    if isinstance(child, str) and child not in id_index:
                        findings.append({
                            "rule": "DOC-025",
                            "record_id": rec_id,
                            "level": level,
                            "diagnostic": f"L1.composes contains {child!r} "
                                           f"which is not a known record id",
                            "child_ref": child,
                            "advisory": True,
                        })

        if level == "L2":
            # L2.composes is a list of L3 child ids.
            composes = record.get("composes")
            if isinstance(composes, list):
                for child in composes:
                    if isinstance(child, str) and child not in id_index:
                        findings.append({
                            "rule": "DOC-025",
                            "record_id": rec_id,
                            "level": level,
                            "diagnostic": f"L2.composes contains {child!r} "
                                           f"which is not a known record id",
                            "child_ref": child,
                            "advisory": True,
                        })

        if level == "L3":
            # L3.composes is a list of L4 child ids.
            composes = record.get("composes")
            if isinstance(composes, list):
                for child in composes:
                    if isinstance(child, str) and child not in id_index:
                        findings.append({
                            "rule": "DOC-025",
                            "record_id": rec_id,
                            "level": level,
                            "diagnostic": f"L3.composes contains {child!r} "
                                           f"which is not a known record id",
                            "child_ref": child,
                            "advisory": True,
                        })

    return findings


# -----------------------------------------------------------------------------
# Catalog walk + id index + manifest emission
# -----------------------------------------------------------------------------


def _walk_records(catalog_root: Path):
    """Yield (yaml_path, record_dict) for every record under the catalog root.

    Excludes the templates/ directory; the template YAMLs use
    placeholder strings (e.g. ``processes:group-<cell>``) that the
    generator expands when creating a real record. Walking the
    templates would produce false-positive DOC-021..024 findings.
    """
    for yaml_path in sorted(catalog_root.rglob("*.yaml")):
        if not yaml_path.is_file():
            continue
        # Skip the template directory; templates are inputs to the
        # generator, not real records.
        if "templates" in yaml_path.parts:
            continue
        try:
            with yaml_path.open(encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        if not isinstance(data.get("id"), str):
            continue
        yield yaml_path, data


def _build_id_index(records: Iterable[tuple[Path, dict]]) -> dict[str, dict]:
    """Build a mapping from canonical id to record_dict."""
    index: dict[str, dict] = {}
    for _, record in records:
        rid = record.get("id")
        if isinstance(rid, str):
            index[rid] = record
    return index


def _build_manifest(catalog_root: Path) -> dict:
    """Build the decomposition reconciliation manifest for the catalog."""
    records = list(_walk_records(catalog_root))
    id_index = _build_id_index(records)
    validation_manifest = _load_validation_manifest(catalog_root)
    findings = evaluate(records, id_index, validation_manifest)

    rule_tally: dict[str, int] = {
        "DOC-021": 0, "DOC-022": 0, "DOC-023": 0, "DOC-024": 0, "DOC-025": 0,
    }
    for f in findings:
        rule_tally[f["rule"]] = rule_tally.get(f["rule"], 0) + 1

    return {
        "manifest_schema_version": MANIFEST_SCHEMA_VERSION,
        "generated_at": _dt.date.today().isoformat(),
        "generator": MANIFEST_GENERATOR,
        "parent_cr": MANIFEST_PARENT_CR,
        "catalog_root": str(catalog_root),
        "summary": {
            "total_records": len(records),
            "by_rule": rule_tally,
            "total_findings": len(findings),
            "advisory_findings": len(findings),  # all findings are advisory
        },
        "findings": findings,
    }


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--catalog-root", default=".",
        help="Path to the catalog root (default: current directory).",
    )
    parser.add_argument(
        "--manifest-dir", default=None,
        help="Directory to write the manifest artefacts. "
             "Default: <catalog-root>/reconciliation/.",
    )
    parser.add_argument(
        "--self-test", action="store_true",
        help="Run self-test with synthetic fixtures and exit.",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        from tests.test_check_decomposition_reconciliation import run_self_test
        return run_self_test()

    catalog_root = Path(args.catalog_root).resolve()
    if not catalog_root.is_dir():
        sys.stderr.write(f"ERROR: catalog root {catalog_root} is not a directory.\n")
        return 2

    manifest = _build_manifest(catalog_root)

    manifest_dir = Path(args.manifest_dir).resolve() if args.manifest_dir \
        else catalog_root / "reconciliation"
    manifest_dir.mkdir(parents=True, exist_ok=True)

    json_path = manifest_dir / "decomposition-reconciliation-manifest.json"
    yaml_path = manifest_dir / "decomposition-reconciliation-manifest.yaml"

    json_path.write_text(json.dumps(manifest, indent=2, sort_keys=False), encoding="utf-8")
    yaml_path.write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    s = manifest["summary"]
    print(f"Decomposition Reconciliation (CR-BP-94-EXT-05): {s['total_records']} records, "
          f"{s['total_findings']} advisory findings")
    print(f"  By rule: {s['by_rule']}")
    print(f"  Manifest: {json_path}")
    print(f"  YAML:     {yaml_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
