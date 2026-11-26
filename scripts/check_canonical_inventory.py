#!/usr/bin/env python3
"""Read-only canonical entity inventory and lifecycle reconciliation.

CR-BP-238 Slice A. Enumerates canonical entity record files under
entities/v1-alpha and compares their identities with CATALOG.yaml,
the EXT-24 lifecycle register, and the dated closure baseline.

The default mode reports findings without modifying repository data.
Use --strict to return a non-zero exit status when findings exist.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
ENTITY_ROOT = Path("entities/v1-alpha")
LEVELS = {
    "pc": ("L0", "ProcessContext", "L0_ProcessContext"),
    "group": ("L1", "ProcessGroup", "L1_ProcessGroup"),
    "process": ("L2", "Process", "L2_BusinessProcess"),
    "activity": ("L3", "Activity", "L3_Activity"),
    "task": ("L4", "Task", "L4_Task"),
}
FILE_RE = re.compile(
    r"^processes-(pc|group|process|activity|task)-[a-z0-9-]+\.yaml$"
)
ID_RE = re.compile(r"^processes:(pc|group|process|activity|task)-[a-z0-9-]+$")


def _finding(code: str, message: str, **details: Any) -> dict[str, Any]:
    result: dict[str, Any] = {"code": code, "message": message}
    if details:
        result["details"] = details
    return result


def _read_json(path: Path, findings: list[dict[str, Any]], code: str) -> dict[str, Any]:
    if not path.is_file():
        findings.append(_finding(code, f"Required file is missing: {path.as_posix()}"))
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        findings.append(_finding(code, f"Cannot read {path.as_posix()}: {exc}"))
        return {}
    if not isinstance(value, dict):
        findings.append(_finding(code, f"{path.as_posix()} must contain a JSON object"))
        return {}
    return value


def _read_yaml(path: Path, findings: list[dict[str, Any]], code: str) -> dict[str, Any]:
    if not path.is_file():
        findings.append(_finding(code, f"Required file is missing: {path.as_posix()}"))
        return {}
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        findings.append(_finding(code, f"Cannot read {path.as_posix()}: {exc}"))
        return {}
    if not isinstance(value, dict):
        findings.append(_finding(code, f"{path.as_posix()} must contain a YAML mapping"))
        return {}
    return value


def _source_commit(root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def audit(catalog_root: Path = ROOT) -> dict[str, Any]:
    """Return a deterministic inventory report; never writes to the repository."""
    root = catalog_root.resolve()
    findings: list[dict[str, Any]] = []
    observations: list[dict[str, Any]] = []
    entity_root = root / ENTITY_ROOT

    if not entity_root.is_dir():
        findings.append(_finding("INV-001", "Canonical entity root is missing"))
        return {
            "report_schema_version": "1",
            "source_commit": _source_commit(root),
            "inventory": {},
            "catalog_index": {},
            "lifecycle_register": {},
            "historical_baseline": {},
            "findings": findings,
            "observations": observations,
        }

    counts: Counter[str] = Counter()
    expected_by_id: dict[str, dict[str, str]] = {}
    file_records: list[dict[str, str]] = []

    # Canonical records use the processes-<kind>-<id>.yaml naming contract.
    # Research files and documentation/support files are deliberately excluded.
    for path in sorted(entity_root.rglob("processes-*.yaml")):
        match = FILE_RE.fullmatch(path.name)
        if not match:
            findings.append(_finding(
                "INV-002",
                "Unclassified canonical-looking entity filename",
                path=path.relative_to(root).as_posix(),
            ))
            continue

        token = match.group(1)
        level, entity_kind, _baseline_key = LEVELS[token]
        try:
            record = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            findings.append(_finding(
                "INV-003", "Entity YAML cannot be read",
                path=path.relative_to(root).as_posix(), error=str(exc),
            ))
            continue
        if not isinstance(record, dict):
            findings.append(_finding(
                "INV-003", "Entity YAML must contain a mapping",
                path=path.relative_to(root).as_posix(),
            ))
            continue

        record_id = record.get("id")
        expected_id = "processes:" + path.stem[len("processes-"):]
        relative_path = path.relative_to(root).as_posix()
        if not isinstance(record_id, str) or not record_id:
            findings.append(_finding(
                "INV-004", "Canonical entity record has no string id",
                path=relative_path,
            ))
            continue
        if record_id != expected_id:
            findings.append(_finding(
                "INV-005", "Entity identifier does not match its canonical filename",
                path=relative_path, record_id=record_id, expected_id=expected_id,
            ))

        id_match = ID_RE.fullmatch(record_id)
        if not id_match or id_match.group(1) != token:
            findings.append(_finding(
                "INV-006", "Entity identifier does not conform to its filename entity kind",
                path=relative_path, record_id=record_id, filename_kind=token,
            ))

        declared_type = record.get("type")
        # L0 ProcessContext cell-charter records historically omit the type field.
        if declared_type is not None and declared_type != entity_kind:
            findings.append(_finding(
                "INV-007", "Declared entity type disagrees with its L0-L4 identity",
                path=relative_path, record_id=record_id,
                declared_type=declared_type, expected_type=entity_kind,
            ))

        counts[level] += 1
        if record_id in expected_by_id:
            findings.append(_finding(
                "INV-008", "Canonical entity identifier occurs in more than one file",
                record_id=record_id,
                paths=[expected_by_id[record_id]["path"], relative_path],
            ))
        else:
            expected_by_id[record_id] = {
                "level": level,
                "entity_kind": entity_kind,
                "path": relative_path,
            }
        file_records.append({
            "id": record_id,
            "level": level,
            "entity_kind": entity_kind,
            "path": relative_path,
        })

    expected_counts = {level: counts.get(level, 0) for level in ("L0", "L1", "L2", "L3", "L4")}
    total = sum(expected_counts.values())

    # Compare the generated catalogue index with the canonical filesystem set.
    index = _read_yaml(root / "CATALOG.yaml", findings, "INV-009")
    catalog = index.get("catalog", {}) if isinstance(index.get("catalog"), dict) else {}
    index_counts = catalog.get("counts", {}) if isinstance(catalog.get("counts"), dict) else {}
    index_entities = catalog.get("entities", [])
    if isinstance(index_entities, list):
        index_ids = [
            item.get("id") for item in index_entities
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        ]
        if len(index_ids) != len(index_entities):
            findings.append(_finding(
                "INV-010", "Catalogue index contains entries without a string id"
            ))
        if len(index_ids) != len(set(index_ids)):
            findings.append(_finding(
                "INV-011", "Catalogue index contains duplicate entity identifiers"
            ))
        filesystem_ids = set(expected_by_id)
        index_id_set = set(index_ids)
        if filesystem_ids != index_id_set:
            findings.append(_finding(
                "INV-012", "Catalogue index identity set differs from canonical filesystem inventory",
                missing_from_index=sorted(filesystem_ids - index_id_set),
                missing_from_filesystem=sorted(index_id_set - filesystem_ids),
            ))
    else:
        findings.append(_finding("INV-010", "catalog.entities must be a list"))

    if index_counts.get("entities") != total:
        findings.append(_finding(
            "INV-013", "Catalogue index entity count differs from filesystem inventory",
            index_count=index_counts.get("entities"), filesystem_count=total,
        ))
    state_total = sum(
        index_counts.get(key, 0)
        for key in ("canonical", "retired", "candidates")
        if isinstance(index_counts.get(key, 0), int)
    )
    if state_total != index_counts.get("entities"):
        findings.append(_finding(
            "INV-014", "Catalogue index state counts do not sum to its entity count",
            state_total=state_total, entity_count=index_counts.get("entities"),
        ))

    # Compare the lifecycle register: exactly one row per canonical identity.
    lifecycle = _read_json(
        root / "reconciliation/closure/lifecycle-register.json", findings, "INV-015"
    )
    lifecycle_records = lifecycle.get("records", [])
    lifecycle_ids: list[str] = []
    lifecycle_kind_counts: Counter[str] = Counter()
    if not isinstance(lifecycle_records, list):
        findings.append(_finding("INV-016", "Lifecycle register records must be a list"))
        lifecycle_records = []

    for row in lifecycle_records:
        if not isinstance(row, dict):
            findings.append(_finding("INV-016", "Lifecycle register contains a non-object row"))
            continue
        record_id = row.get("record_id")
        entity_kind = row.get("entity_kind")
        if not isinstance(record_id, str) or not record_id:
            findings.append(_finding("INV-017", "Lifecycle row has no string record_id"))
            continue
        lifecycle_ids.append(record_id)
        lifecycle_kind_counts[str(entity_kind)] += 1
        known_kinds = {value[1] for value in LEVELS.values()}
        if entity_kind not in known_kinds:
            findings.append(_finding(
                "INV-025", "Lifecycle row has an unknown entity_kind",
                record_id=record_id, entity_kind=entity_kind,
            ))
        if not ID_RE.fullmatch(record_id):
            findings.append(_finding(
                "INV-026", "Lifecycle row uses a non-canonical entity identifier",
                record_id=record_id, entity_kind=entity_kind,
            ))
        expected = expected_by_id.get(record_id)
        if expected is None:
            findings.append(_finding(
                "INV-018", "Lifecycle row does not resolve to a canonical entity file",
                record_id=record_id, entity_kind=entity_kind,
                record_name=row.get("record_name"),
            ))
        elif entity_kind != expected["entity_kind"]:
            findings.append(_finding(
                "INV-019", "Lifecycle entity_kind disagrees with canonical entity kind",
                record_id=record_id, lifecycle_kind=entity_kind,
                expected_kind=expected["entity_kind"],
            ))

    duplicate_lifecycle_ids = sorted(
        record_id for record_id, n in Counter(lifecycle_ids).items() if n > 1
    )
    for record_id in duplicate_lifecycle_ids:
        findings.append(_finding(
            "INV-020", "Lifecycle register contains a duplicate canonical identity",
            record_id=record_id,
            row_count=Counter(lifecycle_ids)[record_id],
        ))

    lifecycle_id_set = set(lifecycle_ids)
    for record_id in sorted(set(expected_by_id) - lifecycle_id_set):
        findings.append(_finding(
            "INV-021", "Canonical entity has no lifecycle-register row",
            record_id=record_id, path=expected_by_id[record_id]["path"],
        ))

    declared_lifecycle_total = lifecycle.get("total_records")
    if declared_lifecycle_total != len(lifecycle_records):
        findings.append(_finding(
            "INV-022", "Lifecycle register total_records does not equal its row count",
            declared_total=declared_lifecycle_total, actual_rows=len(lifecycle_records),
        ))

    # Reconcile the L2 ownership register and EXT-19 L2 inventory to the
    # canonical L2 filesystem identity set. Supporting registers are not
    # allowed to manufacture additional Process identities.
    canonical_l2_ids = {
        record_id for record_id, record in expected_by_id.items()
        if record["level"] == "L2"
    }

    ownership = _read_json(
        root / "reconciliation/closure/ownership-register.json", findings, "INV-027"
    )
    ownership_rows = ownership.get("dispositions", [])
    if not isinstance(ownership_rows, list):
        findings.append(_finding("INV-027", "Ownership register dispositions must be a list"))
        ownership_rows = []
    ownership_ids = [
        row.get("bp_id") for row in ownership_rows
        if isinstance(row, dict) and isinstance(row.get("bp_id"), str)
    ]
    ownership_duplicates = sorted(
        rid for rid, n in Counter(ownership_ids).items() if n > 1
    )
    for rid in ownership_duplicates:
        findings.append(_finding(
            "INV-028", "Ownership register contains a duplicate L2 identity",
            record_id=rid, row_count=Counter(ownership_ids)[rid],
        ))
    if set(ownership_ids) != canonical_l2_ids:
        findings.append(_finding(
            "INV-029", "Ownership register identity set differs from canonical L2 population",
            missing=sorted(canonical_l2_ids - set(ownership_ids)),
            additional=sorted(set(ownership_ids) - canonical_l2_ids),
        ))

    l2_inventory = _read_json(
        root / "reconciliation/l2-inventory.json", findings, "INV-030"
    )
    l2_rows = l2_inventory.get("inventory", [])
    if not isinstance(l2_rows, list):
        findings.append(_finding("INV-030", "L2 inventory must contain an inventory list"))
        l2_rows = []
    l2_ids = [
        row.get("id") for row in l2_rows
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    ]
    if l2_inventory.get("total_l2_entities") != len(l2_rows):
        findings.append(_finding(
            "INV-040", "L2 inventory total_l2_entities does not equal its row count",
            declared_total=l2_inventory.get("total_l2_entities"),
            actual_rows=len(l2_rows),
        ))
    l2_duplicates = sorted(rid for rid, n in Counter(l2_ids).items() if n > 1)
    for rid in l2_duplicates:
        findings.append(_finding(
            "INV-031", "L2 inventory contains a duplicate Process identity",
            record_id=rid, row_count=Counter(l2_ids)[rid],
        ))
    if set(l2_ids) != canonical_l2_ids:
        findings.append(_finding(
            "INV-032", "L2 inventory identity set differs from canonical L2 population",
            missing=sorted(canonical_l2_ids - set(l2_ids)),
            additional=sorted(set(l2_ids) - canonical_l2_ids),
        ))
    missing_io = sorted(
        row.get("id") for row in l2_rows
        if isinstance(row, dict)
        and isinstance(row.get("id"), str)
        and not (
            (row.get("fields_present") or {}).get("inputs") is True
            and (row.get("fields_present") or {}).get("outputs") is True
        )
    )
    if missing_io:
        findings.append(_finding(
            "INV-033", "Canonical L2 inventory contains processes without both inputs and outputs",
            missing_record_ids=missing_io,
        ))

    current_baseline = _read_json(
        root / "reconciliation/closure/current-inventory-baseline.json",
        findings, "INV-034",
    )
    current_population = current_baseline.get("canonical_entity_population", {})
    expected_baseline_counts = {
        "L0": current_population.get("L0_ProcessContext"),
        "L1": current_population.get("L1_ProcessGroup"),
        "L2": current_population.get("L2_BusinessProcess"),
        "L3": current_population.get("L3_Activity"),
        "L4": current_population.get("L4_Task"),
    } if isinstance(current_population, dict) else {}
    if expected_baseline_counts != expected_counts or current_population.get("total") != total:
        findings.append(_finding(
            "INV-035", "Current inventory baseline population differs from canonical filesystem inventory",
            baseline=expected_baseline_counts, current=expected_counts,
            baseline_total=current_population.get("total"), current_total=total,
        ))
    baseline_registers = current_baseline.get("governance_registers", {})
    baseline_lifecycle = baseline_registers.get("lifecycle", {})
    baseline_ownership = baseline_registers.get("ownership", {})
    baseline_l2 = baseline_registers.get("l2_inventory", {})
    actual_register_counts = {
        "lifecycle": len(lifecycle_records),
        "ownership": len(ownership_rows),
        "l2_inventory": len(l2_rows),
    }
    declared_register_counts = {
        "lifecycle": baseline_lifecycle.get("rows"),
        "ownership": baseline_ownership.get("rows"),
        "l2_inventory": baseline_l2.get("rows"),
    }
    if declared_register_counts != actual_register_counts:
        findings.append(_finding(
            "INV-036", "Current inventory baseline register counts differ from actual registers",
            baseline=declared_register_counts, current=actual_register_counts,
        ))
    baseline_io = {
        "inputs_declared": baseline_l2.get("inputs_declared"),
        "outputs_declared": baseline_l2.get("outputs_declared"),
    }
    actual_io = {
        "inputs_declared": sum(
            1 for row in l2_rows if isinstance(row, dict)
            and (row.get("fields_present") or {}).get("inputs") is True
        ),
        "outputs_declared": sum(
            1 for row in l2_rows if isinstance(row, dict)
            and (row.get("fields_present") or {}).get("outputs") is True
        ),
    }
    if baseline_io != actual_io:
        findings.append(_finding(
            "INV-037", "Current inventory baseline L2 I/O coverage differs from L2 inventory",
            baseline=baseline_io, current=actual_io,
        ))
    baseline_state_counts = current_baseline.get("catalogue_index_state_counts", {})
    actual_state_counts = {
        "entities": index_counts.get("entities"),
        "canonical": index_counts.get("canonical"),
        "retired": index_counts.get("retired"),
        "candidates": index_counts.get("candidates"),
    }
    if baseline_state_counts != actual_state_counts:
        findings.append(_finding(
            "INV-038", "Current inventory baseline catalogue state counts differ from CATALOG.yaml",
            baseline=baseline_state_counts, current=actual_state_counts,
        ))
    baseline_lifecycle_states = baseline_lifecycle.get("states", {})
    actual_lifecycle_states = dict(sorted(Counter(
        row.get("lifecycle_state") for row in lifecycle_records
        if isinstance(row, dict) and isinstance(row.get("lifecycle_state"), str)
    ).items()))
    if baseline_lifecycle_states != actual_lifecycle_states:
        findings.append(_finding(
            "INV-039", "Current inventory baseline lifecycle-state counts differ from lifecycle register",
            baseline=baseline_lifecycle_states, current=actual_lifecycle_states,
        ))

    # The EXT-24 baseline is intentionally historical; compare it, but never rewrite it.
    baseline = _read_json(
        root / "reconciliation/closure/catalogue-baseline.json", findings, "INV-023"
    )
    population = baseline.get("entity_population", {})
    baseline_map = {
        "L0": "L0_ProcessContext",
        "L1": "L1_ProcessGroup",
        "L2": "L2_BusinessProcess",
        "L3": "L3_Activity",
        "L4": "L4_Task",
    }
    baseline_counts = {
        level: population.get(key) for level, key in baseline_map.items()
    } if isinstance(population, dict) else {}
    baseline_mismatches = {
        level: {"historical": baseline_counts.get(level), "current": expected_counts[level]}
        for level in baseline_map
        if baseline_counts.get(level) != expected_counts[level]
    }
    if baseline_mismatches:
        observations.append(_finding(
            "HIST-001",
            "Dated EXT-24 programme-closure baseline differs from the current inventory; retain it as historical evidence",
            mismatches=baseline_mismatches,
            baseline_date=baseline.get("baseline_date"),
        ))

    findings.sort(key=lambda item: (
        item.get("code", ""),
        str(item.get("details", {}).get("record_id", "")),
        str(item.get("details", {}).get("path", "")),
    ))
    return {
        "report_schema_version": "1",
        "source_commit": _source_commit(root),
        "inventory": {
            "root": ENTITY_ROOT.as_posix(),
            "counts_by_level": expected_counts,
            "total_entity_files": total,
            "unique_entity_ids": len(expected_by_id),
            "records": sorted(file_records, key=lambda item: item["id"]),
        },
        "catalog_index": {
            "entity_count": index_counts.get("entities"),
            "canonical_count": index_counts.get("canonical"),
            "retired_count": index_counts.get("retired"),
            "candidate_count": index_counts.get("candidates"),
            "identity_count": len(index_entities) if isinstance(index_entities, list) else None,
        },
        "lifecycle_register": {
            "declared_total": declared_lifecycle_total,
            "actual_rows": len(lifecycle_records),
            "unique_ids": len(set(lifecycle_ids)),
            "entity_kind_counts": dict(sorted(lifecycle_kind_counts.items())),
            "duplicate_ids": duplicate_lifecycle_ids,
        },
        "ownership_register": {
            "actual_rows": len(ownership_rows),
            "unique_ids": len(set(ownership_ids)),
            "duplicate_ids": ownership_duplicates,
        },
        "l2_inventory": {
            "declared_total": l2_inventory.get("total_l2_entities"),
            "actual_rows": len(l2_rows),
            "unique_ids": len(set(l2_ids)),
            "duplicate_ids": l2_duplicates,
            "inputs_outputs_complete": len(l2_rows) - len(missing_io),
        },
        "current_baseline": {
            "source_commit": current_baseline.get("source_commit"),
            "reconciled_at": current_baseline.get("reconciled_at"),
            "counts_by_level": expected_baseline_counts,
        },
        "historical_baseline": {
            "date": baseline.get("baseline_date"),
            "counts_by_level": baseline_counts,
            "total": population.get("total") if isinstance(population, dict) else None,
            "is_historical": True,
        },
        "findings": findings,
        "finding_count": len(findings),
        "observations": observations,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog-root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, help="Write the JSON report to this path")
    parser.add_argument(
        "--strict", action="store_true",
        help="Return exit code 1 when any inventory reconciliation finding exists",
    )
    args = parser.parse_args()

    report = audit(args.catalog_root)
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else args.catalog_root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)

    print(
        f"Canonical inventory: {report['inventory'].get('total_entity_files', 0)} files; "
        f"{report['finding_count']} reconciliation findings.",
        file=sys.stderr,
    )
    return 1 if args.strict and report["finding_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
