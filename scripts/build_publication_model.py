#!/usr/bin/env python3
"""Build the deterministic CR-BP-239 canonical publication model.

Canonical entity YAML remains authoritative. This builder preserves source
records and adds resolved relationship, ECF placement and governance views.
It never infers relationships from directory names or record names.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parent.parent
MODEL_SCHEMA_VERSION = "1.0.0"
ECF_TAG = "v2.7.0"
ECF_COMMIT = "8858839111f1458e597c46741f27dbd71ec19518"
ECF_DEPENDENCY = "dea:ecf@2.7.0"
FILE_RE = re.compile(r"^processes-(pc|group|process|activity|task)-[a-z0-9-]+\.yaml$")
LEVELS = {
    "pc": ("L0", "ProcessContext"),
    "group": ("L1", "ProcessGroup"),
    "process": ("L2", "BusinessProcess"),
    "activity": ("L3", "Activity"),
    "task": ("L4", "Task"),
}


def _json_value(value: Any) -> Any:
    """Convert YAML-native date/time values to stable JSON-compatible values."""
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(k): _json_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(v) for v in value]
    return value


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _git_commit(path: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=path, check=True,
            capture_output=True, text=True,
        )
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def _load_ecf(ecf_root: Path, verify_commit: bool = True):
    module_path = ecf_root / "tools" / "ecf_coordinates.py"
    if not module_path.is_file():
        raise FileNotFoundError(f"pinned ECF coordinate module not found: {module_path}")
    if verify_commit:
        actual = _git_commit(ecf_root)
        if actual and actual != ECF_COMMIT:
            raise ValueError(
                f"ECF checkout is {actual}, expected {ECF_COMMIT} ({ECF_TAG})"
            )
    spec = importlib.util.spec_from_file_location("opendea_ecf_coordinates", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load ECF coordinate module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not callable(getattr(module, "enumerate_coordinates", None)):
        raise ValueError("ECF coordinate module does not expose enumerate_coordinates()")
    return module


def _discover_records(root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    entity_root = root / "entities" / "v1-alpha"
    if not entity_root.is_dir():
        raise FileNotFoundError(f"canonical entity root not found: {entity_root}")
    excluded = {"research", "candidates", "retired", "documentation", "discovery",
                "reports", "templates"}
    for path in sorted(entity_root.rglob("processes-*.yaml")):
        if any(part in excluded for part in path.relative_to(entity_root).parts[:-1]):
            continue
        match = FILE_RE.fullmatch(path.name)
        if not match:
            findings.append({
                "code": "INV-UNCLASSIFIED-FILE", "severity": "error",
                "message": "Canonical-looking process file does not match the identity filename contract.",
                "source_path": path.relative_to(root).as_posix(),
            })
            continue
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            findings.append({
                "code": "INV-UNREADABLE-ENTITY", "severity": "error",
                "message": f"Entity YAML cannot be read: {exc}",
                "source_path": path.relative_to(root).as_posix(),
            })
            continue
        if not isinstance(raw, dict):
            findings.append({
                "code": "INV-NONMAPPING-ENTITY", "severity": "error",
                "message": "Canonical entity YAML must be a mapping.",
                "source_path": path.relative_to(root).as_posix(),
            })
            continue
        token = match.group(1)
        level, entity_type = LEVELS[token]
        expected_id = "processes:" + path.stem[len("processes-"):]
        record_id = raw.get("id")
        if record_id != expected_id:
            findings.append({
                "code": "INV-IDENTITY-PATH-MISMATCH", "severity": "error",
                "message": "Record id does not match its canonical filename identity.",
                "source_id": record_id if isinstance(record_id, str) else None,
                "source_path": path.relative_to(root).as_posix(),
                "expected_id": expected_id,
            })
        records.append({
            "id": record_id, "name": raw.get("name"), "type": entity_type,
            "level": level, "source_path": path.relative_to(root).as_posix(),
            "record": _json_value(raw),
        })
    return records, findings


def _context_ref(record: dict[str, Any]) -> str | None:
    context = record.get("context")
    if isinstance(context, list):
        refs = [item.get("ref") for item in context
                if isinstance(item, dict) and isinstance(item.get("ref"), str)]
        return refs[0] if len(refs) == 1 else None
    if isinstance(context, dict) and isinstance(context.get("ref"), str):
        return context["ref"]
    return None


def _relationship(source: str, target: Any, kind: str, assertion: str,
                  path: str, resolved: bool, **extra: Any) -> dict[str, Any]:
    return {
        "source_id": source, "target_id": target, "relationship_type": kind,
        "assertion_source": assertion, "source_path": path,
        "resolution": "resolved" if resolved else "unresolved",
        **extra,
    }


def build_model(root: Path = ROOT, ecf_root: Path | None = None,
                source_commit: str | None = None, build_commit: str | None = None,
                verify_ecf_commit: bool = True) -> dict[str, Any]:
    root = root.resolve()
    ecf_root = (ecf_root or (root / ".metaframework")).resolve()
    dependencies = yaml.safe_load((root / "dependencies.yaml").read_text(encoding="utf-8")) or {}
    if dependencies.get("ecf_contract") != ECF_DEPENDENCY:
        raise ValueError(
            f"dependencies.yaml ecf_contract must be {ECF_DEPENDENCY}; "
            f"found {dependencies.get('ecf_contract')!r}"
        )
    ecf = _load_ecf(ecf_root, verify_ecf_commit)
    coordinates = ecf.enumerate_coordinates()
    coordinate_by_key = {(c["domain"], c["stage"]): c for c in coordinates}
    if len(coordinates) != 49 or len(coordinate_by_key) != 49:
        raise ValueError("pinned ECF contract must enumerate exactly 49 unique coordinates")

    baseline_path = root / "reconciliation/closure/current-inventory-baseline.json"
    lifecycle_path = root / "reconciliation/closure/lifecycle-register.json"
    ownership_path = root / "reconciliation/closure/ownership-register.json"
    baseline = _read_json(baseline_path)
    lifecycle = _read_json(lifecycle_path)
    ownership = _read_json(ownership_path)
    snapshot_commit = source_commit or baseline.get("source_commit")
    if not isinstance(snapshot_commit, str) or not snapshot_commit:
        raise ValueError("inventory baseline must identify the canonical entity snapshot commit")
    build_commit = build_commit or _git_commit(root)

    lifecycle_rows = lifecycle.get("records", [])
    lifecycle_by_id: dict[str, dict[str, Any]] = {}
    for row in lifecycle_rows:
        if isinstance(row, dict) and isinstance(row.get("record_id"), str):
            if row["record_id"] in lifecycle_by_id:
                raise ValueError(f"duplicate lifecycle register identity: {row['record_id']}")
            lifecycle_by_id[row["record_id"]] = row
    ownership_by_id: dict[str, dict[str, Any]] = {}
    for row in ownership.get("dispositions", []):
        if isinstance(row, dict) and isinstance(row.get("bp_id"), str):
            if row["bp_id"] in ownership_by_id:
                raise ValueError(f"duplicate ownership disposition: {row['bp_id']}")
            ownership_by_id[row["bp_id"]] = row

    entities, findings = _discover_records(root)
    by_id: dict[str, dict[str, Any]] = {}
    duplicates: set[str] = set()
    for entity in entities:
        rid = entity.get("id")
        if not isinstance(rid, str) or not rid:
            findings.append({
                "code": "INV-MISSING-ID", "severity": "error",
                "message": "Canonical entity has no non-empty string id.",
                "source_path": entity["source_path"],
            })
            continue
        if rid in by_id:
            duplicates.add(rid)
            findings.append({
                "code": "INV-DUPLICATE-ID", "severity": "error",
                "message": "Canonical identity occurs in more than one entity file.",
                "source_id": rid, "source_path": entity["source_path"],
                "other_source_path": by_id[rid]["source_path"],
            })
        else:
            by_id[rid] = entity

    for entity in entities:
        rid = entity.get("id")
        lifecycle_row = lifecycle_by_id.get(rid)
        if lifecycle_row is None:
            findings.append({
                "code": "GOV-LIFECYCLE-MISSING", "severity": "error",
                "message": "Canonical entity has no lifecycle-register row.",
                "source_id": rid, "source_path": entity["source_path"],
            })
        entity["lifecycle_state"] = lifecycle_row.get("lifecycle_state") if lifecycle_row else None
        entity["governance"] = {
            "lifecycle": _json_value(lifecycle_row) if lifecycle_row else None,
            "ownership": _json_value(ownership_by_id.get(rid)) if entity["level"] == "L2" else None,
        }
        entity["field_provenance"] = {
            key: {"source_path": entity["source_path"], "source_key": key}
            for key in entity["record"]
        }
        entity["ecf_coordinate"] = None

    # Resolve L0 cells directly from their canonical domain/stage declarations.
    l0_by_id: dict[str, dict[str, Any]] = {}
    cell_contexts: dict[tuple[str, str], list[str]] = defaultdict(list)
    for entity in entities:
        if entity["level"] != "L0":
            continue
        record = entity["record"]
        key = (record.get("domain"), record.get("lifecycle_stage"))
        if key not in coordinate_by_key:
            findings.append({
                "code": "ECF-INVALID-L0-COORDINATE", "severity": "error",
                "message": "L0 Process Context does not resolve to a canonical ECF coordinate.",
                "source_id": entity["id"], "source_path": entity["source_path"],
                "domain": key[0], "stage": key[1],
            })
            continue
        if key in cell_contexts and cell_contexts[key]:
            findings.append({
                "code": "ECF-DUPLICATE-CELL-PLACEMENT", "severity": "error",
                "message": "More than one L0 Process Context asserts the same ECF coordinate.",
                "source_id": entity["id"], "source_path": entity["source_path"],
                "other_context_ids": sorted(cell_contexts[key]),
            })
        cell_contexts[key].append(entity["id"])
        l0_by_id[entity["id"]] = entity
        entity["ecf_coordinate"] = coordinate_by_key[key]

    relationships: list[dict[str, Any]] = []
    l1_context: dict[str, str] = {}
    l2_context: dict[str, str] = {}
    l2_groups: dict[str, list[str]] = defaultdict(list)
    l3_parent: dict[str, str] = {}
    l4_parent: dict[str, str] = {}

    # L1 -> L0 context; L1 -> L2 containment is asserted only by L1 composes[].
    for entity in entities:
        if entity["level"] != "L1":
            continue
        rid, record = entity["id"], entity["record"]
        context_id = record.get("process_context")
        ok = isinstance(context_id, str) and context_id in l0_by_id
        relationships.append(_relationship(rid, context_id, "in_process_context",
                                            "process_context", entity["source_path"], ok))
        if ok:
            l1_context[rid] = context_id
        else:
            findings.append({
                "code": "HIERARCHY-L1-CONTEXT-UNRESOLVED", "severity": "error",
                "message": "L1 Process Group process_context does not resolve to an L0 Process Context.",
                "source_id": rid, "target_id": context_id,
                "source_path": entity["source_path"],
            })
        for edge in record.get("composes", []) or []:
            if not isinstance(edge, dict) or edge.get("relationship_type", "composes") != "composes":
                continue
            source, target = edge.get("source_id"), edge.get("target_id")
            target_entity = by_id.get(target) if isinstance(target, str) else None
            valid = source == rid and target_entity is not None and target_entity["level"] == "L2"
            relationships.append(_relationship(
                rid, target, "composes", "ProcessGroup.composes[]",
                entity["source_path"], valid, asserted_edge=_json_value(edge),
            ))
            if valid:
                l2_groups[target].append(rid)
            else:
                findings.append({
                    "code": "HIERARCHY-L1-L2-COMPOSITION-INVALID", "severity": "error",
                    "message": "L1 composes assertion must originate at this group and target a canonical L2 Business Process.",
                    "source_id": rid, "target_id": target,
                    "source_path": entity["source_path"],
                })

    # L2 -> L0 context is an independent assertion, not a substitute for L1 composition.
    for entity in entities:
        if entity["level"] != "L2":
            continue
        rid, record = entity["id"], entity["record"]
        context_id = _context_ref(record)
        ok = isinstance(context_id, str) and context_id in l0_by_id
        relationships.append(_relationship(rid, context_id, "in_process_context",
                                            "context[].ref", entity["source_path"], ok))
        if ok:
            l2_context[rid] = context_id
        else:
            findings.append({
                "code": "HIERARCHY-L2-CONTEXT-UNRESOLVED", "severity": "error",
                "message": "L2 context[].ref must resolve independently to an L0 Process Context.",
                "source_id": rid, "target_id": context_id,
                "source_path": entity["source_path"],
            })
        parents = sorted(set(l2_groups.get(rid, [])))
        if len(parents) == 0 and entity.get("lifecycle_status") not in {"deprecated", "retired"}:
            findings.append({
                "code": "HIERARCHY-L2-GROUP-MISSING", "severity": "error",
                "message": "L2 Business Process has no incoming L1 ProcessGroup.composes assertion.",
                "source_id": rid, "target_id": context_id,
                "source_path": entity["source_path"],
            })
        elif len(parents) > 1:
            findings.append({
                "code": "HIERARCHY-L2-MULTIPLE-GROUPS", "severity": "error",
                "message": "L2 Business Process has multiple incoming L1 composition assertions.",
                "source_id": rid, "source_path": entity["source_path"],
                "parent_group_ids": parents,
            })
        for parent_id in parents:
            parent_context = l1_context.get(parent_id)
            if context_id and parent_context and context_id != parent_context:
                findings.append({
                    "code": "HIERARCHY-L2-CONTEXT-CONFLICT", "severity": "error",
                    "message": "L2 context assertion conflicts with its L1 group's Process Context.",
                    "source_id": rid, "target_id": parent_id,
                    "source_path": entity["source_path"],
                    "l2_context_id": context_id, "l1_context_id": parent_context,
                })

    # L3/L4 hierarchy is taken from their explicit parent-reference fields.
    for entity in entities:
        if entity["level"] == "L3":
            rid, parent = entity["id"], entity["record"].get("belongs_to_business_process")
            parent_entity = by_id.get(parent) if isinstance(parent, str) else None
            ok = parent_entity is not None and parent_entity["level"] == "L2"
            relationships.append(_relationship(rid, parent, "belongs_to_business_process",
                                                "belongs_to_business_process",
                                                entity["source_path"], ok))
            if ok:
                l3_parent[rid] = parent
            else:
                findings.append({
                    "code": "HIERARCHY-L3-PARENT-UNRESOLVED", "severity": "error",
                    "message": "L3 Activity parent must resolve to a canonical L2 Business Process.",
                    "source_id": rid, "target_id": parent, "source_path": entity["source_path"],
                })
        elif entity["level"] == "L4":
            rid, parent = entity["id"], entity["record"].get("belongs_to_activity")
            parent_entity = by_id.get(parent) if isinstance(parent, str) else None
            ok = parent_entity is not None and parent_entity["level"] == "L3"
            relationships.append(_relationship(rid, parent, "belongs_to_activity",
                                                "belongs_to_activity",
                                                entity["source_path"], ok))
            if ok:
                l4_parent[rid] = parent
            else:
                findings.append({
                    "code": "HIERARCHY-L4-PARENT-UNRESOLVED", "severity": "error",
                    "message": "L4 Task parent must resolve to a canonical L3 Activity.",
                    "source_id": rid, "target_id": parent, "source_path": entity["source_path"],
                })

    # Preserve other explicitly declared relationship assertions without reinterpretation.
    for entity in entities:
        for edge in entity["record"].get("relationships", []) or []:
            if isinstance(edge, dict):
                target = edge.get("target_id")
                relationships.append(_relationship(
                    entity["id"], target, str(edge.get("relationship_type", "unspecified")),
                    "relationships[]", entity["source_path"],
                    isinstance(target, str) and target in by_id,
                    asserted_edge=edge,
                ))

    # Inherit a display coordinate only through the validated hierarchy.
    for entity in entities:
        rid = entity["id"]
        if entity["level"] == "L1":
            context_id = l1_context.get(rid)
        elif entity["level"] == "L2":
            context_id = l2_context.get(rid)
        elif entity["level"] == "L3":
            context_id = l2_context.get(l3_parent.get(rid, ""))
        elif entity["level"] == "L4":
            context_id = l2_context.get(l3_parent.get(l4_parent.get(rid, ""), ""))
        else:
            context_id = None
        if context_id in l0_by_id:
            entity["ecf_coordinate"] = l0_by_id[context_id]["ecf_coordinate"]

    by_level = Counter(e["level"] for e in entities)
    by_lifecycle = Counter(e["lifecycle_state"] or "unregistered" for e in entities)
    by_domain = Counter()
    by_stage = Counter()
    for entity in entities:
        coord = entity.get("ecf_coordinate")
        if coord:
            by_domain[coord["domain"]] += 1
            by_stage[coord["stage"]] += 1

    cells = []
    for coordinate in coordinates:
        key = (coordinate["domain"], coordinate["stage"])
        context_ids = sorted(cell_contexts.get(key, []))
        groups = sorted(
            (e["id"] for e in entities if e["level"] == "L1"
             and l1_context.get(e["id"]) in context_ids)
        )
        process_ids = sorted(
            (e["id"] for e in entities if e["level"] == "L2"
             and l2_context.get(e["id"]) in context_ids)
        )
        cells.append({
            **coordinate,
            "process_context_ids": context_ids,
            "process_group_ids": groups,
            "business_process_ids": process_ids,
            "counts": {
                "L0": len(context_ids), "L1": len(groups), "L2": len(process_ids),
                "L3": sum(1 for p in l3_parent.values() if p in process_ids),
                "L4": sum(1 for p in l4_parent.values()
                          if p in {a for a, bp in l3_parent.items() if bp in process_ids}),
            },
        })

    expected = baseline.get("canonical_entity_population", {})
    observed = {"L0": by_level["L0"], "L1": by_level["L1"], "L2": by_level["L2"],
                "L3": by_level["L3"], "L4": by_level["L4"], "total": len(entities)}
    baseline_keys = {"L0": "L0_ProcessContext", "L1": "L1_ProcessGroup",
                     "L2": "L2_BusinessProcess", "L3": "L3_Activity", "L4": "L4_Task"}
    for level, key in baseline_keys.items():
        if expected.get(key) != observed[level]:
            findings.append({
                "code": "INV-BASELINE-COUNT-MISMATCH", "severity": "error",
                "message": "Observed canonical population differs from the reconciled inventory baseline.",
                "level": level, "expected": expected.get(key), "observed": observed[level],
            })
    if expected.get("total") != observed["total"]:
        findings.append({
            "code": "INV-BASELINE-TOTAL-MISMATCH", "severity": "error",
            "message": "Observed canonical population total differs from the reconciled inventory baseline.",
            "expected": expected.get("total"), "observed": observed["total"],
        })

    model = {
        "model_schema_version": MODEL_SCHEMA_VERSION,
        "catalogue": {
            "id": "dea:catalog/business-processes",
            "version": (dependencies.get("catalogs") or [{}])[0].get("version"),
        },
        "provenance": {
            "canonical_entity_snapshot_commit": snapshot_commit,
            "build_commit": build_commit,
            "inventory_baseline_path": "reconciliation/closure/current-inventory-baseline.json",
            "inventory_baseline_schema_version": baseline.get("baseline_schema_version"),
            "ecf_contract": {
                "identifier": "dea:ecf", "version": ECF_TAG.lstrip("v"),
                "tag": ECF_TAG, "commit": ECF_COMMIT,
                "coordinate_module": "tools/ecf_coordinates.py",
            },
            "metamodel_pin": dependencies.get("metamodel_pin"),
            "dependency_manifest": "dependencies.yaml",
        },
        "inventory": {
            "total": observed["total"], "by_level": dict(sorted(by_level.items())),
            "by_lifecycle_state": dict(sorted(by_lifecycle.items())),
            "by_ecf_domain": dict(sorted(by_domain.items())),
            "by_lifecycle_stage": dict(sorted(by_stage.items())),
            "baseline": _json_value(expected),
        },
        "coordinates": cells,
        "entities": sorted(entities, key=lambda e: (e["level"], str(e.get("id")))),
        "relationships": sorted(
            relationships,
            key=lambda r: (str(r.get("source_id")), str(r.get("relationship_type")),
                           str(r.get("target_id")), r.get("source_path", "")),
        ),
        "findings": sorted(findings, key=lambda f: (
            f.get("severity", ""), f.get("code", ""), str(f.get("source_id", "")),
            f.get("source_path", ""),
        )),
    }
    canonical = json.dumps(model, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=False).encode("utf-8")
    model["model_digest"] = "sha256:" + hashlib.sha256(canonical).hexdigest()
    return model


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--ecf-root", type=Path, default=None)
    parser.add_argument("--schema", type=Path, default=ROOT / "schemas/publication-model.schema.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-findings", action="store_true",
                        help="write the model even when error findings exist")
    args = parser.parse_args(argv)
    model = build_model(args.root, args.ecf_root)
    schema = _read_json(args.schema)
    errors = sorted(Draft7Validator(schema).iter_errors(model), key=lambda e: list(e.path))
    if errors:
        for error in errors:
            print(f"SCHEMA: {'/'.join(map(str, error.path))}: {error.message}", file=sys.stderr)
        return 2
    error_findings = [f for f in model["findings"] if f.get("severity") == "error"]
    if error_findings and not args.allow_findings:
        print(json.dumps(error_findings, indent=2, ensure_ascii=False), file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(model, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(f"publication-model: {args.output} entities={model['inventory']['total']} "
          f"coordinates={len(model['coordinates'])} findings={len(model['findings'])} "
          f"digest={model['model_digest']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
