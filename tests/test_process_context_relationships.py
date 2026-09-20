"""CR-BP-14 Phase 2: Process Context block and contextual relationships.

Locks the canonical representation established by CR-BP-14 §13 and §20:

- The `context:` block exists on both schemas and references Process
  Context canonical ids (`dea:pc-*`).
- The relationship_type enum admits `serves` and `contributes-to`
  (metamodel registry ids; catalog-governed extension).
- `target_id` admits canonical ECF identifiers
  (`ecf:<lowerCamelDomain>[.<lowerCamelStage>]`) alongside entity ids.
- A synthetic entry using the canonical representation validates; one
  with a malformed context reference fails.
"""

import json
from pathlib import Path

import pytest
import yaml
from jsonschema import validate
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parent.parent

CONTEXTUAL_TYPES = {"serves", "contributes-to"}


def load_entity_schema():
    return json.loads((ROOT / "schemas" / "entity.schema.json").read_text())


def load_contribution_schema():
    return json.loads(
        (ROOT / "schemas" / "contribution.schema.json").read_text()
    )


def base_entry() -> dict:
    return {
        "id": "processes:process-example-process",
        "name": "Manage Example Process",
        "type": "Process",
        "version": "1.0.0",
        "process_intent": "manage",
        "process_audience": "party-relationship",
    }


def relationship(target_id, rel_type="serves"):
    return {
        "source_id": "processes:process-example-process",
        "target_id": target_id,
        "relationship_type": rel_type,
    }


@pytest.mark.parametrize("loader", [load_entity_schema, load_contribution_schema])
def test_context_block_shape(loader):
    schema = loader()
    props = schema["properties"]
    if "proposed_entry" in props:
        props = props["proposed_entry"]["properties"]
    block = props["context"]
    assert block["type"] == "array"
    item = block["items"]
    assert item["required"] == ["ref"]
    assert item["additionalProperties"] is False
    assert item["properties"]["ref"]["pattern"] == r"^processes:pc-[a-z0-9-]+$"


@pytest.mark.parametrize("loader", [load_entity_schema, load_contribution_schema])
def test_contextual_relationship_types_admitted(loader):
    schema = loader()
    props = schema["properties"]
    if "proposed_entry" in props:
        props = props["proposed_entry"]["properties"]
    enum = set(
        props["relationships"]["items"]["properties"]["relationship_type"]["enum"]
    )
    assert CONTEXTUAL_TYPES <= enum
    # operates-within is deliberately absent: its semantics are carried
    # by the context block (programme decision D2).
    assert "operates-within" not in enum


def test_ecf_target_identifiers_validate():
    schema = load_entity_schema()
    entry = base_entry()
    entry["relationships"] = [
        relationship("ecf:customerAndDemand.operate", "serves"),
        relationship("ecf:governanceAndExistence", "contributes-to"),
        relationship("processes:pc-pr-op", "serves"),
    ]
    validate(entry, schema)  # must not raise


def test_context_block_with_multiple_refs_validates():
    schema = load_entity_schema()
    entry = base_entry()
    entry["context"] = [{"ref": "processes:pc-pr-op"}, {"ref": "processes:pc-pr-im"}]
    validate(entry, schema)  # must not raise


@pytest.mark.parametrize(
    "bad_ref",
    ["dea_pc-pr-op", "dea:pc_cd_op", "party-relationship", "processes:group-x", ""],
)
def test_malformed_context_ref_rejected(bad_ref):
    schema = load_entity_schema()
    entry = base_entry()
    entry["context"] = [{"ref": bad_ref}]
    with pytest.raises(ValidationError):
        validate(entry, schema)


@pytest.mark.parametrize(
    "bad_target",
    ["ecf:party-relationship", "ecf:PartyAndRelationship.operate", "ecf:", "ECF:customerAndDemand.operate"],
)
def test_malformed_ecf_target_rejected(bad_target):
    schema = load_entity_schema()
    entry = base_entry()
    entry["relationships"] = [relationship(bad_target, "serves")]
    with pytest.raises(ValidationError):
        validate(entry, schema)


def test_existing_canonical_entries_still_validate():
    """The 13a/13b entries carry a legacy scalar `process_context`
    field that predates the canonical context block. The schema must
    remain permissive toward it until the CR-BP-15-IMP Phase 10
    migration; this test locks that no entry broke."""
    schema = load_entity_schema()
    entries = sorted(
        (ROOT / "entities" / "v1-alpha").rglob("processes-process-*.yaml")
    )
    assert entries, "expected canonical process entries"
    for path in entries:
        data = yaml.safe_load(path.read_text())
        if data.get("type") != "Process":
            continue
        validate(data, schema)
