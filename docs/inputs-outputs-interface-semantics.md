# Inputs, Outputs and Interface Semantics (CR-BP-94-EXT-12)

**Status**: Normative (proposed for adoption under CR-BP-94-EXT-12)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-19
**Source CR**: CR-BP-94-EXT-12 (Process Inputs, Outputs and Interface Semantics)
**Parent programme**: DEA-PROCESS-ENRICH-000 (charter at `docs/operational-documentation-programme/DEA-PROCESS-ENRICH-000-programme-charter.md`)
**Predecessors**: CR-BP-94-EXT-10 (PR #179, merged; schema inventory), CR-BP-94-EXT-11 (PR #180, merged; L0-L4 profiles)
**Tranche gate**: G3_interfaces (closes by this slice)
**Repository**: technehub-labs/dea-catalog-business-processes
**Path**: `change-requests/CR-BP-94-EXT-12-process-inputs-outputs-and-interface-semantics.md`

---

## 1. Purpose

This document is the **EXT-12 schema extension and semantic contract** for inputs, outputs, transformation, interfaces, and dependencies at L2/L3/L4. It implements the EXT-10 inventory's routed-gap table (EXT-12 owns: precondition, interface, dependency) and the EXT-12 CR's design.

It extends the existing CR-BP-96 inputs/transformation/outputs structures with the additional EXT-12 attributes (type, required, acceptance_criteria, validation, provenance, quality_attributes), adds the new optional top-level fields `interfaces:` and `dependencies:` (which are EXPLICITLY authorised by the EXT-10 Routed-gap table), and adds the `trigger_type:` sub-field for trigger classification.

The CR-BP-94 trigger, outcome, identity, and other RETAIN fields are **preserved**; the EXT-12 work is additive.

---

## 2. Conceptual operational contract

The documented process transformation MUST be understandable through the following conceptual relationship:

```
Trigger / Invocation Condition
             |
             v
       Preconditions
             |
             v
      Input Acquisition
             |
             v
       Transformation
             |
             v
       Output Production
             |
             v
       Output Consumption
             |
             v
       Intended Outcome
```

This is a **semantic model**, not a required execution sequence. Actual processes may involve iterative, concurrent, or conditional work. EXT-12 does NOT define workflow orchestration (per CR-BP-98).

---

## 3. Trigger and preconditions

### 3.1 Trigger

The existing `trigger:` field (BP-C1) is preserved (non-empty string). EXT-12 adds the optional `trigger_type:` sub-field with the controlled vocabulary:

| Value | Description |
|---|---|
| `event_driven` | Process invoked by an event (e.g. customer submission received) |
| `time_driven` | Process invoked at a scheduled time (e.g. monthly close) |
| `request_driven` | Process invoked by a request (e.g. user ticket) |
| `condition_driven` | Process invoked when a condition holds (e.g. threshold exceeded) |
| `decision_driven` | Process invoked by a decision (e.g. approval granted) |
| `external_obligation_driven` | Process invoked by an external obligation (e.g. regulatory filing deadline) |

A trigger MUST identify the circumstance that invokes the process, not simply describe what the process achieves.

### 3.2 Preconditions

EXT-10 routed "precondition" to EXT-12. The implementation here is the L2 optional field `preconditions:` (array of structured entries):

```yaml
preconditions:
  - id: <precondition-id>
    name: <precondition name>
    description: |
      <The condition that must hold.>
    scope: <process | activity | task | external>
    established_by: <entity or source>
    verification: <how the precondition is verified>
    consequence_if_not_met: |
      <What happens if the condition is not satisfied.>
```

Preconditions MUST NOT be conflated with input validation rules.

---

## 4. Input model (extended CR-BP-96)

The existing `inputs:` array (CR-BP-96) carries entries with `id`, `name`, `description`, `source`. EXT-12 EXTENDS each entry with the **optional** attributes:

| Attribute | Type | Purpose |
|---|---|---|
| `type` | enum | classification (see below) |
| `required` | bool | whether the input is mandatory |
| `acceptance_criteria` | string | conditions for acceptable use |
| `validation` | string | applicable validation requirements |
| `provenance` | object | source/author of the assertion |

### 4.1 Input classification (controlled vocabulary)

Per EXT-12 §6.3:

| Value | Description |
|---|---|
| `information` | An information object |
| `business_object` | A business object |
| `request` | A request from a participant |
| `decision` | A decision (e.g. approval) |
| `transaction` | A transaction (e.g. payment instruction) |
| `material` | A physical or material input |
| `document` | A document or record |
| `external_data` | External data (e.g. market price) |
| `prior_process_output` | An output from a prior process |

### 4.2 Input vs resource

The same real-world object may play different roles in different process contexts. A system, employee, facility, or budget is ordinarily a **resource** or **dependency**, NOT an input. The classification follows its function in the documented transformation.

---

## 5. Output model (extended CR-BP-96)

The existing `outputs:` array (CR-BP-96) carries entries with `id`, `name`, `description`, `consumer`. EXT-12 EXTENDS each entry with the **optional** attributes:

| Attribute | Type | Purpose |
|---|---|---|
| `type` | enum | classification (see below) |
| `acceptance_criteria` | string | conditions defining acceptable output |
| `quality_attributes` | array | relevant quality expectations |
| `provenance` | object | source/author of the assertion |

### 5.1 Output classification (controlled vocabulary)

| Value | Description |
|---|---|
| `information` | An information object |
| `business_object` | A business object |
| `decision` | A decision |
| `service_result` | The result of a service delivery |
| `changed_object` | A business object that has been changed |
| `document` | A document or record |
| `report` | A report |

### 5.2 Output vs outcome

Every output is described as a produced result. An **outcome** describes the effect achieved through use of the output. The catalogue MUST NOT claim that an outcome has been achieved merely because an output exists.

### 5.3 Output consumer

A consumer MAY be: another Business Process, an Activity or Task, a Business Function, an organizational role, an Information System, an external party, a customer or supplier. A consumer reference MUST use the canonical entity identifier when the referenced entity exists in the governed model.

---

## 6. Interface model (NEW top-level L2 field)

EXT-12 introduces the new optional L2 top-level field `interfaces:` (array of structured entries). Per EXT-12 §10:

```yaml
interfaces:
  - id: <interface-id>
    name: <interface name>
    description: |
      <What this interface represents.>
    type: <controlled vocabulary value>
    participants:
      - <participant-1>
      - <participant-2>
    exchange_purpose: |
      <What is exchanged and why.>
    format_or_standard: <where established>
    source:
      ref: <uri>
```

### 6.1 Interface classification (controlled vocabulary)

Per EXT-12 §10.4:

| Value | Description |
|---|---|
| `human` | Human-to-human interaction |
| `organizational` | Organizational-to-organizational interaction |
| `information` | Information exchange (records, documents) |
| `system` | System-mediated (Information System / API) |
| `physical` | Physical (goods, materials) |
| `contractual` | Contractual interaction |
| `regulatory` | Regulatory submission or notification |

### 6.2 Business interface vs system interface

A **business interface** is a defined point of interaction between business entities. A **system interface** is a specialisation: it is mediated by an Information System or technical service. The system interface MUST NOT be represented as a Business Process input or output merely because an application transmits the data.

---

## 7. Dependencies (NEW top-level L2 field)

EXT-12 introduces the new optional L2 top-level field `dependencies:` (array of structured entries). Per EXT-12 §11:

```yaml
dependencies:
  - id: <dependency-id>
    target: <dependent entity, resource, service, or condition>
    type: <dependency type from the controlled vocabulary>
    business_consequence: |
      <What happens if the dependency is unavailable.>
    criticality: high | medium | low
    source:
      ref: <uri>
```

Dependencies are **distinct from decomposition relationships**. A dependency is a material reliance; a `composes:` relationship is structural part-of.

---

## 8. Transformation model

The existing `transformation:` field (CR-BP-96) is preserved. EXT-12 §7 establishes the principles:

1. Express the business change, assessment, decision, or service activity.
2. Explain how relevant inputs are used.
3. Explain the business logic or governing principles at an appropriate level.
4. Describe the nature of the resulting outputs.
5. Avoid duplicating a detailed task sequence.
6. Avoid merely restating the process title.
7. Avoid embedding system implementation details unless essential to the business semantics.

A transformation MAY be expressed as structured narrative or a more formal representation. EXT-12 does NOT require every process to have a mathematically formal transformation function.

---

## 9. L2-L4 applicability

| Concern | L2 BusinessProcess | L3 Activity | L4 Task |
|---|---|---|---|
| Trigger | Process invocation | Activity activation, where meaningful | Task initiation condition, where meaningful |
| Preconditions | Process conditions | Activity conditions | Task conditions |
| Inputs | Process-level business inputs | Activity working inputs | Task working objects |
| Transformation | Full process transformation | Cohesive activity work | Bounded action |
| Outputs | Process outputs | Activity results | Task result |
| Outcomes | Process-level intended outcomes | Contribution to parent outcome | Contribution to Activity result |
| Interfaces | Principal business interfaces | Relevant hand-offs | Specific interaction where relevant |
| Dependencies | Material process dependencies | Activity dependencies | Task dependencies |

L0 and L1 are non-executable (per EXT-11); these concepts are not applicable at L0/L1.

A child input or output MUST NOT automatically be copied from the parent. Where a child uses a parent-level input, the relationship must be explicit and the child's actual use described.

---

## 10. Compatibility and migration

EXT-12 is **additive**:

- Existing L2 records that use only the CR-BP-96 attributes (`id`, `name`, `description`, `source` for inputs; `id`, `name`, `description`, `consumer` for outputs) continue to validate.
- The new `interfaces:` and `dependencies:` fields are optional. Records without them remain conformant.
- The `trigger_type:` sub-field is optional. Records without it remain conformant.
- The `preconditions:` field is optional. Records without it remain conformant.

The EXT-10 regression test (`tests/test_schema_inventory_ext10.py`) is updated to acknowledge the closure of the `interface` and `dependency` gaps (these concepts are now legitimately in the schema; they were the EXT-10 routed gaps).

The 145 existing L2 records have **0** inputs/outputs/transformation populated (per the EXT-10 inventory). The EXT-19 L2 backfill tranche is the work that populates them.

---

## 11. Validator and manifest

EXT-12 lands:

- `scripts/check_inputs_outputs_interfaces_ext12.py` (the validator; IT-001..IT-010 rules)
- `reconciliation/inputs-outputs-manifest.json` (per-record manifest)
- `gate [37] Inputs/Outputs/Interfaces` wired ADVISORY in `scripts/conformance_result.py`
- `tests/test_inputs_outputs_interfaces_ext12.py` (unit + integration)

---

## 12. References

- `templates/business-process.yaml` (the L2 template; EXT-12 extensions documented inline)
- `change-requests/CR-BP-94-EXT-12-process-inputs-outputs-and-interface-semantics.md` (the EXT-12 CR)
- `docs/operational-documentation-semantic-contract.md` (EXT-09; the upstream semantic contract)
- `docs/operational-schema-inventory.md` (EXT-10; the schema inventory + routed-gap table)
- `templates/documentation-profile-ext11-v3.yaml` (EXT-11; the v3 profile that consumes the EXT-12 fields)
- `reconciliation/programme-register.json` (the 17-CR register)
- `reconciliation/profile-manifest.json` (EXT-11 manifest)
