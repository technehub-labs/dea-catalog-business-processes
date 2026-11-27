from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_publication_model import build_model  # noqa: E402


DOMAINS = [
    "GovernanceAndExistence", "StrategyAndDirection", "AgencyAndOrganization",
    "PartyAndRelationship", "ProductAndValue", "EnablementAndOperations",
    "FinanceAndAccounting",
]
STAGES = ["Conceive", "Design", "Build", "Activate", "Operate", "Improve", "Retire"]


def _write_yaml(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def _fixture(tmp_path: Path) -> tuple[Path, Path]:
    root = tmp_path
    ecf = root / ".metaframework"
    (ecf / "tools").mkdir(parents=True)
    (ecf / "tools/ecf_coordinates.py").write_text(
        "DOMAINS = " + repr(DOMAINS) + "\n"
        "STAGES = " + repr(STAGES) + "\n"
        "def enumerate_coordinates():\n"
        "    return [{'domain': d, 'stage': s, 'identifier': f'ecf:{d}.{s.lower()}', "
        "'label': f'{d} x {s}'} for d in DOMAINS for s in STAGES]\n",
        encoding="utf-8",
    )
    (root / "dependencies.yaml").write_text(
        "ecf_contract: dea:ecf@2.7.0\nmetamodel_pin: '1.0.0'\n"
        "catalogs:\n  - id: dea:catalog/business-processes\n    version: v0.5.0\n",
        encoding="utf-8",
    )
    (root / "reconciliation/closure").mkdir(parents=True)
    baseline = {
        "baseline_schema_version": "1",
        "source_commit": "123456789abcdef",
        "canonical_entity_population": {
            "L0_ProcessContext": 1, "L1_ProcessGroup": 1,
            "L2_BusinessProcess": 1, "L3_Activity": 1,
            "L4_Task": 1, "total": 5,
        },
    }
    (root / "reconciliation/closure/current-inventory-baseline.json").write_text(
        json.dumps(baseline), encoding="utf-8"
    )
    ids = [
        "processes:pc-governance-conceive-abc",
        "processes:group-governance-conceive-def",
        "processes:process-governance-conceive-ghi",
        "processes:activity-governance-conceive-jkl",
        "processes:task-governance-conceive-mno",
    ]
    (root / "reconciliation/closure/lifecycle-register.json").write_text(
        json.dumps({"records": [
            {"record_id": rid, "lifecycle_state": "active"} for rid in ids
        ]}), encoding="utf-8"
    )
    (root / "reconciliation/closure/ownership-register.json").write_text(
        json.dumps({"dispositions": [
            {"bp_id": ids[2], "owner": "Process Owner", "owner_status": "confirmed"}
        ]}), encoding="utf-8"
    )
    base = root / "entities/v1-alpha/go-conceive"
    _write_yaml(base / "processes-pc-governance-conceive-abc.yaml", {
        "id": ids[0], "name": "Governance Context",
        "domain": DOMAINS[0], "lifecycle_stage": STAGES[0],
    })
    _write_yaml(base / "Group/processes-group-governance-conceive-def.yaml", {
        "id": ids[1], "type": "ProcessGroup", "name": "Governance Group",
        "process_context": ids[0],
        "composes": [{
            "source_id": ids[1], "target_id": ids[2],
            "relationship_type": "composes", "status": "active",
        }],
    })
    _write_yaml(base / "Group/Process/processes-process-governance-conceive-ghi.yaml", {
        "id": ids[2], "type": "Process", "name": "Governance Process",
        "context": [{"ref": ids[0]}],
        "definition": "Formal process definition for the fixture.",
        "plain_language_description": "A concise fixture description.",
        "worked_example": "An example grounded in the fixture source.",
        "process_intent": "manage",
        "process_classification": {"type": "management"},
        "process_specialization": ["governance"],
        "inputs": [{"name": "Request", "description": "An input request."}],
        "outputs": [{"name": "Decision", "description": "A recorded decision."}],
    })
    _write_yaml(base / "Group/Process/Activity/processes-activity-governance-conceive-jkl.yaml", {
        "id": ids[3], "type": "Activity", "name": "Governance Activity",
        "belongs_to_business_process": ids[2],
    })
    _write_yaml(base / "Group/Process/Activity/Task/processes-task-governance-conceive-mno.yaml", {
        "id": ids[4], "type": "Task", "name": "Governance Task",
        "belongs_to_activity": ids[3],
    })
    return root, ecf


def test_model_preserves_distinct_hierarchy_assertions_and_is_deterministic(tmp_path):
    root, ecf = _fixture(tmp_path)
    first = build_model(root, ecf, build_commit="abcdef123456", verify_ecf_commit=False)
    second = build_model(root, ecf, build_commit="abcdef123456", verify_ecf_commit=False)

    assert first["model_digest"] == second["model_digest"]
    assert first["provenance"]["canonical_entity_snapshot_commit"] == "123456789abcdef"
    assert len(first["coordinates"]) == 49
    assert first["inventory"]["total"] == 5
    assert not [f for f in first["findings"] if f["severity"] == "error"]

    edges = first["relationships"]
    assert any(e["relationship_type"] == "composes"
               and e["assertion_source"] == "ProcessGroup.composes[]"
               for e in edges)
    assert any(e["relationship_type"] == "in_process_context"
               and e["assertion_source"] == "context[].ref"
               for e in edges)
    entities = {e["id"]: e for e in first["entities"]}
    assert entities["processes:task-governance-conceive-mno"]["ecf_coordinate"]["stage"] == "Conceive"
    assert entities["processes:process-governance-conceive-ghi"]["governance"]["ownership"]["owner"] == "Process Owner"


def test_model_conforms_to_published_schema(tmp_path):
    root, ecf = _fixture(tmp_path)
    model = build_model(root, ecf, build_commit="abcdef123456", verify_ecf_commit=False)
    schema = json.loads((ROOT / "schemas/publication-model.schema.json").read_text(encoding="utf-8"))
    errors = list(Draft7Validator(schema).iter_errors(model))
    assert errors == []


def test_deprecated_l2_without_composition_is_not_reported_as_missing_group(tmp_path):
    root, ecf = _fixture(tmp_path)
    base = root / "entities/v1-alpha/go-conceive/Group/Process"
    process_path = base / "processes-process-governance-conceive-ghi.yaml"
    group_path = root / "entities/v1-alpha/go-conceive/Group/processes-group-governance-conceive-def.yaml"
    process = yaml.safe_load(process_path.read_text(encoding="utf-8"))
    process["lifecycle_status"] = "deprecated"
    process["status"] = "deprecated"
    _write_yaml(process_path, process)
    group = yaml.safe_load(group_path.read_text(encoding="utf-8"))
    group["composes"] = []
    _write_yaml(group_path, group)
    lifecycle_path = root / "reconciliation/closure/lifecycle-register.json"
    lifecycle = json.loads(lifecycle_path.read_text(encoding="utf-8"))
    for record in lifecycle["records"]:
        if record["record_id"] == process["id"]:
            record["lifecycle_state"] = "deprecated"
    lifecycle_path.write_text(json.dumps(lifecycle), encoding="utf-8")
    model = build_model(root, ecf, build_commit="abcdef123456", verify_ecf_commit=False)
    missing = [f for f in model["findings"] if f["code"] == "HIERARCHY-L2-GROUP-MISSING"]
    assert missing == []
