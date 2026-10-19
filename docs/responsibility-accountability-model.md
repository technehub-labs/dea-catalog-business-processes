# Process Responsibility and Accountability Model (CR-BP-94-EXT-13)

**Status**: Normative (proposed for adoption under CR-BP-94-EXT-13)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-19
**Source CR**: CR-BP-94-EXT-13 (Process Responsibility and Accountability Model)
**Parent programme**: DEA-PROCESS-ENRICH-000 (charter at `docs/operational-documentation-programme/DEA-PROCESS-ENRICH-000-programme-charter.md`)
**Predecessors**: CR-BP-94-EXT-10 (PR #179, merged), CR-BP-94-EXT-11 (PR #180, merged), CR-BP-94-EXT-12 (PR #181, merged)
**Tranche gate**: G4_accountability (closes by this slice)
**Repository**: technehub-labs/dea-catalog-business-processes
**Path**: `change-requests/CR-BP-94-EXT-13-process-responsibility-and-accountability-model.md`

---

## 1. Purpose

This document is the **EXT-13 schema extension and semantic contract** for responsibility, accountability, performer, role, and the role-catalog model at L2/L3/L4. It implements the EXT-10 inventory's routed-gap table (EXT-13 owns: accountability, performer) and the EXT-13 CR's design.

It extends the existing CR-BP-96 `responsibility` structure (performer / type / scope / accountabilities sub-fields), adds the new optional L2 top-level fields `accountability:` and `roles:`, and adds the optional `raci:` block for RACI-style role-to-activity assignment per the controlled vocabulary.

The CR-BP-94 trigger, outcome, identity, inputs, transformation, outputs, and boundary fields are **preserved**; the EXT-13 work is additive.

---

## 2. Conceptual model

EXT-13 distinguishes five concepts that are routinely conflated:

| Concept | Definition | Cardinality |
|---|---|---|
| **Role** | An abstract capability that an individual, system, or organisational unit may hold. The role is defined independently of any specific assignment. | n/a (catalog) |
| **Role assignment** | The relationship binding a role to a process/activity/task. | 1..n per role |
| **Performer** | The actual actor (individual, system, team, organisation, external party) that executes the work. | 1..n per role assignment |
| **Responsibility** | The obligation to perform the work. May be shared across multiple performers. | 1..n per activity/task |
| **Accountability** | The answerability for the outcome. There MUST be at most one accountable role per outcome; accountability cannot be delegated. | 0..1 per outcome (often 1) |

A **role** is a description of a capability. A **performer** is a person or system that fills the role. **Responsibility** attaches to a role; the role is then performed by one or more performers. **Accountability** attaches to a role for an outcome; the role may be performed by one or more individuals, but only one role may be the accountable role for a given outcome.

---

## 3. The responsibility model

The existing `responsibility:` field (CR-BP-96 BP-QUAL-008) is preserved. EXT-13 introduces a structured form:

```yaml
responsibility:
  - role: <organisational role name>
    performer: <who/what actually does the work>
    type: human | system | team | organization | external_party
    scope: process | activity | task | sub-process
    accountabilities:
      - <accountability-1>
      - <accountability-2>
  - role: <role-2>
    ...
```

The plain-string form (e.g. `responsibility: | <prose>`) is preserved for backward compatibility. Records that use only the plain-string form continue to validate.

### 3.1 Responsibility vs accountability

A person or system may be **responsible for** executing the work (e.g. preparing a regulatory filing) without being **accountable for** the outcome (e.g. a compliance officer who signs the attestation). The catalog MUST NOT conflate these. Per EXT-13 §4, accountability is the answerability for the outcome; responsibility is the obligation to perform the work.

### 3.2 Performer model

The `performer` sub-field carries the actual actor. Controlled vocabulary:

| Value | Description |
|---|---|
| `human` | An individual (employee, contractor, agent) |
| `system` | An information system or automated service |
| `team` | A team of humans (and possibly systems) |
| `organization` | An organisational unit (department, division, subsidiary) |
| `external_party` | An external party (vendor, counterparty, regulator, customer, supplier) |

A performer MAY change over time without changing the role; the role definition is the stable reference, the performer assignment is a transient detail.

### 3.3 Performer vs role

A **performer** is the actual actor; a **role** is the abstract capability. A role may be performed by many performers at different times; a performer may hold many roles simultaneously. The catalog MUST allow a role to be defined independently of any specific performer.

---

## 4. The accountability model

EXT-13 introduces the new optional L2 top-level field `accountability:` (array of structured entries). Per EXT-13 §4:

```yaml
accountability:
  - role: <accountable role name>
    type: human | committee | board | individual
    scope: process | activity | task | sub-process
    outcomes:
      - <outcome-1>
      - <outcome-2>
    rationale: |
      <Why this role holds accountability (regulatory, contractual, governance).>
```

### 4.1 The non-delegation rule

Accountability cannot be delegated. A role that is accountable for an outcome may designate performers to execute the work, but the accountability for the outcome remains with the role. The catalog MUST NOT record an outcome with zero accountability; it MAY record a single accountable role or a small bounded set (typically one).

### 4.2 Sources of accountability

A role may hold accountability derived from:

- **Regulatory**: a regulator has assigned the accountability (e.g. SMCR in the UK, attestation rules under SOX)
- **Contractual**: a counterparty agreement has assigned the accountability (e.g. a service-level agreement, a client contract)
- **Governance**: the enterprise has assigned the accountability (e.g. a board mandate, a delegation of authority)
- **Operational**: the operating model has assigned the accountability (e.g. a process owner)

The `rationale` field captures the source; the validator (RA-008) confirms a non-empty rationale is provided.

### 4.3 Accountability vs role

Accountability is associated with a **role**, not an individual. The role is the durable reference; the individual occupying the role is a transient detail. When the individual changes, the accountability for the role is unchanged.

---

## 5. Role catalog (new L2 top-level field)

EXT-13 introduces the new optional L2 top-level field `roles:` (array of structured entries). Per EXT-13 §6:

```yaml
roles:
  - id: <role-id>
    name: <role name>
    type: organisational | cross_cutting | external | system
    description: |
      <What this role represents.>
    reporting_line: <where the role reports>
    capability_owner: <who owns the capability definition>
```

A role in the catalog is referenced by `responsibility[].role`, `accountability[].role`, and `raci[].assignments[].role`. Roles in the responsibility/accountability lists that are not present in the catalog are flagged by the validator (RA-009).

### 5.1 Role classification

| Value | Description |
|---|---|
| `organisational` | A role defined by the enterprise (e.g. Compliance Officer, KYC Analyst) |
| `cross_cutting` | A role that spans organisational boundaries (e.g. Process Owner, Risk Manager) |
| `external` | A role fulfilled by an external party (e.g. Regulator, External Auditor) |
| `system` | A role fulfilled by an information system or automated service |

---

## 6. RACI-style assignment (optional)

EXT-13 introduces the new optional L2 top-level field `raci:` (array of structured entries). Per EXT-13 §7:

```yaml
raci:
  - id: <raci-id>
    scheme: raci | rasci | rapid | daciar | paci
    assignments:
      - role: <role-id>
        activity: <activity or sub-process id>
        assignment: <controlled-vocabulary value>
```

The `scheme` field is the controlled vocabulary for the role-assignment framework; the `assignments[]` list binds roles to activities per the scheme. The validator (RA-010) confirms a single accountable assignment per outcome when the raci block is used.

### 6.1 Scheme vocabulary

| Value | Description |
|---|---|
| `raci` | Responsible, Accountable, Consulted, Informed |
| `rasci` | Responsible, Accountable, Supports, Consulted, Informed |
| `rapid` | Recommend, Agree, Perform, Input, Decide |
| `daciar` | Drive, Approve, Contribute, Inform, Accept, Reject |
| `paci` | Perform, Accountable, Consulted, Informed |

### 6.2 Assignment vocabulary

| Value | Description |
|---|---|
| `responsible` | Performs the work (RACI / RASCI) |
| `accountable` | Answerable for the outcome (RACI / RASCI) |
| `consulted` | Provides input before or during the work (RACI / RASCI) |
| `informed` | Kept informed of progress or completion (RACI / RASCI) |
| `supports` | Helps complete the work (RASCI) |
| `recommend` | Recommends the decision (RAPID) |
| `agree` | Must agree before the decision is made (RAPID) |
| `perform` | Performs the action (RAPID) |
| `input` | Provides input to the decision (RAPID) |
| `decide` | Makes the final decision (RAPID) |
| `drive` | Drives the process forward (DACIAR) |
| `approve` | Approves the deliverable (DACIAR) |
| `contribute` | Contributes to the deliverable (DACIAR) |
| `accept` | Accepts the deliverable (DACIAR) |
| `reject` | May reject the deliverable (DACIAR) |
| `inform` | Kept informed of progress or completion (DACIAR) |
| `perform` | Performs the action (PACI) |

---

## 7. The 8 governance relationships

EXT-13 §5 describes the eight governance relationships that arise between accountable roles, responsible roles, and the rest of the catalog:

1. **Accountable for outcome**: the role answerable for a specific outcome.
2. **Responsible for execution**: the role performing the work.
3. **Consulted for input**: the role providing expertise before or during execution.
4. **Informed of progress**: the role kept up-to-date.
5. **Approves deliverable**: the role authorising the deliverable.
6. **Reviews and accepts**: the role accepting the deliverable as final.
7. **Escalates to**: the role receiving escalations when blocked.
8. **Owns the capability**: the role owning the capability definition (the catalog's role catalog owner).

The 8 relationships map to the assignment vocabulary in §6.2. The catalog may express these as natural-language statements or as structured `raci:` blocks.

---

## 8. L2-L4 applicability

| Concern | L2 BusinessProcess | L3 Activity | L4 Task |
|---|---|---|---|
| Accountability | Process-level outcome | Activity contribution | Task contribution |
| Responsibility | Process-level execution | Activity execution | Task execution |
| Performer | Process-level performer | Activity performer | Task performer |
| Role catalog | Roles referenced by the BP | (may inherit from BP) | (may inherit from Activity) |
| RACI | Process-level assignment | Activity-level assignment | Task-level assignment |

L0 and L1 are non-executable (per EXT-11); these concepts are not applicable at L0/L1.

A child's role assignments MUST NOT be auto-copied from the parent. The child MAY inherit the role catalog (the parent's `roles[]` entries) and MAY declare new performers / sub-roles.

---

## 9. Compatibility and migration

EXT-13 is **additive**:

- Existing records that use only the CR-BP-96 plain-string `responsibility:` form continue to validate.
- The new `accountability:` field is optional. Records without it remain conformant.
- The new `roles:` field is optional. Records without it remain conformant.
- The new `raci:` field is optional. Records without it remain conformant.
- The structured `responsibility[]` form is optional; the plain-string form is preserved.

The EXT-10 regression test (`tests/test_schema_inventory_ext10.py`) is updated to acknowledge the closure of the `accountability` and `performer` gaps (these are now legitimately in the L2 template; they were the EXT-13 routed gaps).

The 145 existing L2 records have **0** of the new fields populated (per the EXT-10 inventory; the CR-BP-96 advisory policy passes vacuously). The EXT-19 L2 backfill tranche is the work that populates them.

---

## 10. Validator and manifest

EXT-13 lands:

- `scripts/check_responsibility_accountability_ext13.py` (the validator; RA-001..RA-010 rules)
- `reconciliation/responsibility-accountability-manifest.json` (per-record manifest)
- `gate [38] Responsibility/Accountability` wired ADVISORY in `scripts/conformance_result.py`
- `tests/test_responsibility_accountability_ext13.py` (unit + integration)

The validator enforces:

- **RA-001**: `responsibility` (when structured) has the EXT-13 attributes (role, performer, type, scope, accountabilities)
- **RA-002**: `responsibility[].type` is in the performer vocabulary
- **RA-003**: `accountability` (when present) has the EXT-13 attributes (role, type, scope, outcomes, rationale)
- **RA-004**: `accountability[].type` is in the accountable vocabulary
- **RA-005**: `roles[]` (when present) has the EXT-13 attributes (id, name, type, description, reporting_line, capability_owner)
- **RA-006**: `roles[].type` is in the role vocabulary
- **RA-007**: `raci[].scheme` is in the scheme vocabulary
- **RA-008**: `raci[].assignments[].assignment` is in the assignment vocabulary
- **RA-009**: roles referenced by `responsibility[]` and `accountability[]` resolve to entries in `roles[]` (when the catalog is present)
- **RA-010**: L0/L1 do NOT carry responsibility/accountability/roles/raci (non-executable per EXT-11)

---

## 11. References

- `templates/business-process.yaml` (the L2 template; EXT-13 extensions documented inline)
- `change-requests/CR-BP-94-EXT-13-process-responsibility-and-accountability-model.md` (the EXT-13 CR)
- `docs/operational-documentation-semantic-contract.md` (EXT-09; the upstream semantic contract)
- `docs/operational-schema-inventory.md` (EXT-10; the schema inventory + routed-gap table)
- `docs/inputs-outputs-interface-semantics.md` (EXT-12; the upstream semantic doc)
- `templates/documentation-profile-ext11-v3.yaml` (EXT-11; the v3 profile that consumes the EXT-13 fields)
- `reconciliation/programme-register.json` (the 17-CR register)
- `reconciliation/profile-manifest.json` (EXT-11 manifest)
- `reconciliation/inputs-outputs-manifest.json` (EXT-12 manifest)
