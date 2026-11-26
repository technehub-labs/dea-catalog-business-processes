"""Tests for the CR-BP-238 canonical inventory audit."""

import importlib.util
import json
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_canonical_inventory.py"
SPEC = importlib.util.spec_from_file_location("check_canonical_inventory", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def _write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _fixture(root: Path) -> tuple[list[dict], dict]:
    definitions = [
        ("pc", "pc-one", "ProcessContext", None, "L0_ProcessContext"),
        ("group", "group-one", "ProcessGroup", "ProcessGroup", "L1_ProcessGroup"),
        ("process", "process-one", "Process", "Process", "L2_BusinessProcess"),
        ("activity", "activity-one", "Activity", "Activity", "L3_Activity"),
        ("task", "task-one", "Task", "Task", "L4_Task"),
    ]
    rows = []
    ids = []
    for token, suffix, kind, declared_type, _ in definitions:
        record_id = f"processes:{token}-{suffix}"
        record = {"id": record_id, "name": suffix.replace("-", " ").title()}
        if declared_type:
            record["type"] = declared_type
        path = root / "entities" / "v1-alpha" / "test-cell" / f"processes-{token}-{suffix}.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        rows.append({
            "record_id": record_id,
            "record_name": record["name"],
            "entity_kind": kind,
            "lifecycle_state": "active",
        })
        ids.append(record_id)

    population = {
        "L0_ProcessContext": 1,
        "L1_ProcessGroup": 1,
        "L2_BusinessProcess": 1,
        "L3_Activity": 1,
        "L4_Task": 1,
        "total": 5,
    }
    _write_json(
        root / "reconciliation" / "closure" / "catalogue-baseline.json",
        {"baseline_date": "2026-10-20", "entity_population": population},
    )
    _write_json(
        root / "reconciliation" / "closure" / "lifecycle-register.json",
        {"total_records": 5, "records": rows},
    )
    _write_json(
        root / "CATALOG.yaml",
        {
            "catalog": {
                "counts": {
                    "entities": 5, "canonical": 5, "retired": 0, "candidates": 0,
                },
                "entities": [
                    {"id": record_id, "state": "canonical"} for record_id in ids
                ],
            }
        },
    )
    _write_json(
        root / "reconciliation" / "closure" / "ownership-register.json",
        {"dispositions": [{
            "bp_id": "processes:process-process-one",
            "bp_name": "Process One",
        }]},
    )
    _write_json(
        root / "reconciliation" / "l2-inventory.json",
        {"total_l2_entities": 1, "inventory": [{
            "id": "processes:process-process-one",
            "fields_present": {"inputs": True, "outputs": True},
        }]},
    )
    _write_json(
        root / "reconciliation" / "closure" / "current-inventory-baseline.json",
        {
            "source_commit": "0123456789abcdef",
            "canonical_entity_population": {
                "L0_ProcessContext": 1, "L1_ProcessGroup": 1,
                "L2_BusinessProcess": 1, "L3_Activity": 1,
                "L4_Task": 1, "total": 5,
            },
            "governance_registers": {
                "lifecycle": {"rows": 5, "states": {"active": 5}},
                "ownership": {"rows": 1},
                "l2_inventory": {"rows": 1, "inputs_declared": 1, "outputs_declared": 1},
            },
            "catalogue_index_state_counts": {
                "entities": 5, "canonical": 5, "retired": 0, "candidates": 0,
            },
        },
    )
    return rows, population


def test_clean_inventory_reconciles_all_representations(tmp_path: Path) -> None:
    _fixture(tmp_path)
    report = MODULE.audit(tmp_path)

    assert report["inventory"]["counts_by_level"] == {
        "L0": 1, "L1": 1, "L2": 1, "L3": 1, "L4": 1,
    }
    assert report["inventory"]["total_entity_files"] == 5
    assert report["catalog_index"]["entity_count"] == 5
    assert report["lifecycle_register"]["actual_rows"] == 5
    assert report["ownership_register"]["actual_rows"] == 1
    assert report["l2_inventory"]["inputs_outputs_complete"] == 1
    assert report["finding_count"] == 0


def test_duplicate_orphan_and_historical_baseline_drift_are_reported(
    tmp_path: Path,
) -> None:
    rows, population = _fixture(tmp_path)
    rows.append(dict(rows[2]))
    rows.append({
        "record_id": "dea:legacy-research-record",
        "record_name": "",
        "entity_kind": "unknown",
        "lifecycle_state": "active",
    })
    _write_json(
        tmp_path / "reconciliation" / "closure" / "lifecycle-register.json",
        {"total_records": len(rows), "records": rows},
    )
    population["L2_BusinessProcess"] = 2
    population["total"] = 6
    _write_json(
        tmp_path / "reconciliation" / "closure" / "catalogue-baseline.json",
        {"baseline_date": "2026-10-20", "entity_population": population},
    )

    report = MODULE.audit(tmp_path)
    codes = {finding["code"] for finding in report["findings"]}

    assert "INV-018" in codes  # lifecycle row outside the canonical entity set
    assert "INV-020" in codes  # duplicate lifecycle identity
    assert "INV-024" not in codes  # historical baseline is not a current-state gate
    assert "INV-025" in codes  # unknown lifecycle entity kind
    assert "INV-026" in codes  # legacy/non-canonical lifecycle identifier
    assert "INV-036" in codes  # current baseline lifecycle row count drift
    assert report["lifecycle_register"]["actual_rows"] == 7
    assert report["observations"][0]["code"] == "HIST-001"



def test_ownership_and_l2_inventory_duplicates_are_blocking(tmp_path: Path) -> None:
    _fixture(tmp_path)
    ownership_path = tmp_path / "reconciliation" / "closure" / "ownership-register.json"
    ownership = json.loads(ownership_path.read_text(encoding="utf-8"))
    extra_owner = dict(ownership["dispositions"][0])
    extra_owner["bp_id"] = "processes:process-unregistered"
    ownership["dispositions"].append(extra_owner)
    _write_json(ownership_path, ownership)

    l2_path = tmp_path / "reconciliation" / "l2-inventory.json"
    l2_inventory = json.loads(l2_path.read_text(encoding="utf-8"))
    l2_inventory["inventory"][0]["fields_present"]["outputs"] = False
    l2_inventory["inventory"].append(dict(l2_inventory["inventory"][0]))
    l2_inventory["total_l2_entities"] = 2
    _write_json(l2_path, l2_inventory)

    report = MODULE.audit(tmp_path)
    codes = {finding["code"] for finding in report["findings"]}

    assert "INV-028" in codes  # duplicate ownership identity
    assert "INV-029" in codes  # ownership identity set differs from canonical L2
    assert "INV-031" in codes  # duplicate L2 inventory identity
    assert "INV-033" in codes  # missing output declaration
    assert "INV-040" not in codes  # declared row count matches physical rows
