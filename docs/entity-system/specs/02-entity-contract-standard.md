# Entity Contract Standard

> **CR-BP-122 Stage 2 output 2.** Normative spec for the General Entity System's entity contract discipline in `dea-catalog-business-processes`. Foundation: [00-charter.md](../00-charter.md), [02-normative-design-proposal.md §2](../02-normative-design-proposal.md). Companion: [CR-012 EGV-005](../../../../dea-governance/change-requests/CR-012-org-wide-entity-governance.md).

## 1. Scope

This spec codifies the **entity contract discipline** for every governed entity in `dea-catalog-business-processes`. The discipline is built on CR-012 normative requirement **EGV-005 (Canonical Entity Contract)**.

The discipline covers:
- The common entity envelope (the universal fields every entity has).
- The type-specific profiles (the per-entity-type fields that extend the envelope).
- The extension rules (how new entity types are added without weakening the common invariants).
- The reconciliation with the metamodel's entity-type definitions.

## 2. Normative rules

### EC-001 (common envelope) - blocking

> Every governed entity in `dea-catalog-processes` SHALL conform to a common entity envelope. The envelope specifies the universal fields:
>
> ```yaml
> id: <persistent-entity-identifier>     # required, universal
> type: <canonical-entity-type>           # required, universal
> name: <preferred-human-readable-name>   # required, universal
> definition: <normative-meaning>         # required, universal
> description: <optional-explanatory>     # optional, universal
>
> relationships: []                       # optional, universal; typed references
> classifications: []                     # optional, universal; ECF + process axes
> provenance: {}                          # required, universal; CR linkage + change history
>
> lifecycle:                              # required, universal
>   status: <governed-lifecycle-state>
>   admitted_at: <iso-8601>
>   admitted_by: <cr-id>
> ```
>
> The envelope is the **conformance check target**: the entity-system umbrella gate walks the envelope fields and asserts presence + format for every record. The envelope is NOT a schema; the existing per-type schemas (PG, BP, Activity, Task, ProcessContext, ProcessScope) are the type-specific profiles that extend the envelope.

**Source rules**: EGV-005 (canonical entity contract), CR-BP-03 (4-axis classification), CR-BP-12 (Process Group profile), CR-BP-31 (ECF conformance block). **Verification**: the entity-system umbrella gate (Stage 3-4, CR-BP-123) walks the envelope fields; per-type schemas are validated by their existing per-type gates (PG-001..PG-008, BP-SEM-001..014, etc.).

### EC-002 (type-specific profiles) - blocking

> The 5 entity types in `dea-catalog-processes` extend the common envelope with type-specific required and optional fields. The profiles are documented in `schemas/entities/<type>.schema.json` and are the existing per-type schemas:
>
> | Type | Profile | Required fields beyond the envelope |
> |---|---|---|
> | `Process` (L2) | `schemas/entities/process.schema.json` | `process_intent`, `process_type`, `process_specialization`, `process_audience` (legacy alias), `ecf_conformance` block (CR-BP-31) |
> | `ProcessContext` (L0) | `schemas/entities/process-context.schema.json` | `domain`, `lifecycle_stage`, `cell_charter` |
> | `ProcessGroup` (L1) | `schemas/entities/process-group.schema.json` | `group_kind` (6-value controlled vocabulary), `composes[]` (relationship_type: composes; cardinality >= 1) |
> | `Activity` (L3) | `schemas/entities/activity.schema.json` | `activity_kind`, `execution_model` |
> | `Task` (L4) | `schemas/entities/task.schema.json` | `task_kind`, `inputs[]`, `outputs[]` |
>
> The 6th type `ProcessScope` (L0 alternative) is dormant-by-design per CR-BP-100; the schema + template + validator + doc profile remain as forward-compatibility surface only. Admission requires an explicit CR.

**Source rules**: EGV-005 (canonical entity contract), CR-BP-12 (L1 Process Group profile), CR-BP-31 (ECF conformance block), CR-BP-100 (ProcessScope dormant-by-design). **Verification**: per-type gates (PG-001..PG-008, BP-SEM-001..014, etc.) assert the type-specific required fields are present.

### EC-003 (extension rules) - blocking

> A new entity type is added to the catalog by:
>
> 1. Authoring a per-type schema at `schemas/entities/<new-type>.schema.json`.
> 2. Defining the type in `metamodel-pointer.yaml` (or the metamodel's entity-type registry).
> 3. Adding the type to the `LEVEL_BY_TYPE` map (the catalog's level-by-type dispatch).
> 4. Adding per-type gate(s) to `scripts/conformance_result.py`.
> 5. Filing a CR that documents the new type, its schema, its gate, and its conformance profile.
>
> The new type's profile MUST extend the common envelope (EC-001); it MUST NOT redefine the universal fields; it MUST NOT weaken any common invariant. The extension is additive only.

**Source rules**: EGV-005 (canonical entity contract), the metamodel-pointer.yaml discipline. **Verification**: the CR's gate stage is the natural review point for the new type's conformance profile; the entity-system umbrella gate asserts the extension is additive.

### EC-004 (metamodel reconciliation) - blocking

> The catalog instantiates the metamodel's entity-type definitions through profiles. The metamodel's `dea:entity-business-process` (the first Core specialisation on the `dea:entity-process` kernel, per CR-MM-PROC-01 + ADR-0006) is the type definition that the catalog's `Process` profile extends.
>
> The catalog's profiles SHALL NOT redefine the canonical entity types. The catalog MAY add catalog-specific required and optional fields (e.g. `process_intent`, `process_type`) that the metamodel does not define; the metamodel-pointer.yaml is the cross-reference declaration.

**Source rules**: EGV-001 (canonical governance authority), EGV-005 (canonical entity contract), CR-MM-PROC-01 (process kernel + specialisation), ADR-0006 (OpenDEAM v0.6.0 process-kernel specialisation). **Verification**: the entity-system umbrella gate asserts the catalog's profiles are consistent with the metamodel-pointer.yaml declarations; the conformance rollup's per-type gates assert the catalog-specific fields are valid.

## 3. The common envelope schema

The envelope is documented as a JSON Schema at `schemas/entities/_envelope.schema.json` (forward-looking; the existing per-type schemas are the implementation). The schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dea.technehub-labs.org/schemas/entities/_envelope.schema.json",
  "title": "DEA Catalog Entity Envelope",
  "description": "The common envelope every entity in the DEA catalog must conform to (per EGV-005).",
  "type": "object",
  "required": ["id", "type", "name", "definition", "lifecycle", "provenance"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^[a-z][a-z0-9-]*:[a-z0-9-]+-[a-z2-9]{6}$",
      "description": "Persistent entity identifier (per IS-001)."
    },
    "type": {
      "type": "string",
      "enum": ["Process", "ProcessContext", "ProcessGroup", "Activity", "Task", "ProcessScope"],
      "description": "Canonical entity type (per EGV-005)."
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "description": "Preferred human-readable name."
    },
    "definition": {
      "type": "string",
      "minLength": 1,
      "description": "Normative meaning (per EGV-005)."
    },
    "description": {
      "type": "string",
      "description": "Optional explanatory text."
    },
    "relationships": {
      "type": "array",
      "items": {"$ref": "https://dea.technehub-labs.org/schemas/entities/_relationship.schema.json"},
      "description": "Typed references to other entities (per EGV-006)."
    },
    "classifications": {
      "type": "array",
      "description": "Classification axes (ECF coordinate, process_type, process_intent)."
    },
    "provenance": {
      "type": "object",
      "required": ["change_history"],
      "properties": {
        "change_history": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["cr", "date", "change"],
            "properties": {
              "cr": {"type": "string"},
              "date": {"type": "string", "format": "date"},
              "change": {"type": "string"}
            }
          }
        }
      },
      "description": "Per-record change history (per EGV-008)."
    },
    "lifecycle": {
      "type": "object",
      "required": ["status", "admitted_at", "admitted_by"],
      "properties": {
        "status": {
          "type": "string",
          "enum": ["proposed", "admitted", "deprecated", "retired", "superseded"],
          "description": "Governed lifecycle state (per the Lifecycle Standard)."
        },
        "admitted_at": {"type": "string", "format": "date"},
        "admitted_by": {"type": "string"},
        "deprecated_at": {"type": "string", "format": "date"},
        "retired_at": {"type": "string", "format": "date"}
      },
      "description": "Lifecycle block (per the Lifecycle Standard)."
    }
  },
  "additionalProperties": true
}
```

The envelope is **advisory** at the JSON Schema level (per `additionalProperties: true`); the per-type schemas are the implementation. The envelope's normative rules (EC-001..EC-004) are the conformance check target.

## 4. Worked example (cross-reference)

See the [Identity Standard §3](01-identity-standard.md) for a worked example demonstrating EC-001 (envelope compliance: id, type, name, definition, description, relationships, classifications, provenance, lifecycle all present and conformant) and EC-002 (the Process profile's required fields beyond the envelope: process_intent, process_type, process_specialization, ecf_conformance block).

## 5. Acceptance criteria

- AC-EC-01 Every record in `entities/v1-alpha/` and `contexts/v1-alpha/` carries the 5 required envelope fields (id, type, name, definition, lifecycle, provenance).
- AC-EC-02 The 5 entity types (Process, ProcessContext, ProcessGroup, Activity, Task) have per-type schemas; the 6th type (ProcessScope) is dormant-by-design.
- AC-EC-03 Every record's `lifecycle.status` is one of the 5 governed states (per the Lifecycle Standard).
- AC-EC-04 Every record's `provenance.change_history[]` entries carry `cr`, `date`, `change` keys (per CR-BP-113 provenance).
- AC-EC-05 The catalog's profiles are consistent with the metamodel-pointer.yaml declarations (per EC-004).

## 6. Cross-references

- CR-012 EGV-005 (the org-wide normative requirement)
- CR-BP-03 (4-axis classification; the catalog's classification axes)
- CR-BP-12 (L1 Process Group profile; the type-specific profile example)
- CR-BP-31 (ECF conformance block; the BP and PG conformance block shape)
- CR-BP-100 (ProcessScope dormant-by-design; the L0 alternative that is empty)
- CR-MM-PROC-01 + ADR-0006 (the process kernel + specialisation discipline)
- The Identity Standard (§1) for the `id` field
- The Lifecycle Standard (§4) for the `lifecycle` block
- The Relationship Standard (§3) for the `relationships[]` entries
