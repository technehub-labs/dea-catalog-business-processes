# Decomposition Semantic Contract

**Source of truth:** CR-BP-93 (Decomposition Semantic Contract).
**Recon programme:** CR-BP-92 (Decomposition and Execution Boundary Hardening) §8.
**Establishes:** normative definitions, allowed/disallowed interpretations, decomposition relationships, and level-specific qualification criteria for **Process Context**, **L0 Process Scope**, **L1 Process Group**, **L2 Business Process**, **L3 Activity**, and **L4 Task**.
**Where this fits:** this document is the **decomposition** half of the catalog's normative contract. The **characterization** half (Process Intent, Process Classification, Process Specialization, Process Audience, Process Relationships) lives in [`docs/semantic-contract.md`](semantic-contract.md), [`docs/classification.md`](classification.md), [`docs/identity.md`](identity.md), and [`docs/architecture.md`](architecture.md). The two halves together constitute the catalog's reader-facing semantic contract.

This document supersedes the decomposition-relevant prose previously scattered across `docs/architecture.md`, `docs/semantic-contract.md`, `docs/identity.md`, and the schema descriptions in `schemas/entities/*.schema.json`. Where this document and a Change Request disagree, the Change Request governs.

---

## 1. The decomposition chain

The Process Catalog organizes process architecture across six normative layers, separated by what each layer answers about the work:

```text
Process Context       where responsibility is examined              (catalog topology)
        |
        v
L0  Process Scope     what responsibility is organized              (architectural boundary)
        |
        v
L1  Process Group     how related responsibilities are grouped      (catalog entity)
        |
        v
L2  Business Process  what work is performed                        (catalog entity)
        |
        v
L3  Activity          what cohesive work contributes                (catalog entity)
        |
        v
L4  Task              what bounded unit of work is performed        (decomposition boundary)
```

Decomposition (L0-L4) and characterization (Intent / Classification / Specialization / Context / Relationships) are **separate concerns**. No one of these concepts substitutes for another.

---

## 2. Process Context

**Question answered:** *Where is process architecture being examined?*

### Definition

> A **Process Context** is a non-executable catalog-topology construct that establishes the locus at which process architecture is examined. It is a single cell of the ECF Domain x Lifecycle Stage matrix.

### Allowed

* A Process Context exists at a single `Domain x Lifecycle Stage` cell.
* A Process Context names the bounded area of process responsibility it covers (`context_name`, `process_area`, etc.).
* A Process Context may serve as a parent of one or more L0 Process Scopes (where L0 lands as a schema-bearing entity) or, in the current prose-only L0 model, as the implicit parent of one or more L1 Process Groups.
* A Process Context has an ECF coordinate reference (`ecf:domain.stage`) that is the authoritative identifier for the cell.

### Disallowed

* A Process Context **does not perform work**; it is not a Process, Business Process, Process Group, Business Function, Capability, or Organization Unit.
* A Process Context **does not have inputs, outputs, transformation, or outcome**. It does not satisfy the L2 qualification criteria.
* A Process Context **does not automatically constitute a Process Scope**. The two concepts are separated by §3.

### Where the contract lives today

* Canonical records: `contexts/v1-alpha/dea:pc-*.yaml` (35 records at the time of writing).
* Schema: `schemas/entities/process-context.schema.json`.
* Gate: `scripts/check_process_context.py` (PC-001..PC-008).
* Reader-facing: `docs/context.md`.

---

## 3. L0 Process Scope

**Question answered:** *What coherent process responsibility is being covered?*

### Definition

> **L0 Process Scope** is a non-executable architectural boundary that defines a coherent and bounded area of process responsibility within a Process Context.

### Allowed

* L0 establishes the population of process concerns to be decomposed; it does not itself perform work.
* L0 has a **scope statement**, a **scope boundary**, **inclusions**, **exclusions**, and a **decomposition basis**.
* L0 is the parent of one or more L1 Process Groups.
* L0 may carry a `metadata.scope` label (per `docs/identity.md` §1 canonical id families: `dea:scope-*`).

### Disallowed

* L0 is **not** a Process, Business Process, Process Group, Business Function, Capability, or Organization Unit.
* L0 is **not executable**. It has no inputs, outputs, transformation, outcome, or trigger.
* An **ECF coordinate does not automatically constitute an L0 Process Scope**. The two concepts are intentionally separated: a coordinate identifies *where* architecture is examined; an L0 scope identifies *what coherent responsibility is being covered*.

### Where the contract lives today

* Canonical records: **none**. L0 is currently a prose-only construct documented here + in `docs/architecture.md` §"Decomposition".
* Schema: **none**. The decision whether L0 lands as a schema + gate (CR-BP-95) or remains prose-only with non-schema enforcement is deferred to CR-BP-95 (L0/L1 Conformance Gate).
* Gate: **none**. The L0 validation rule set proposed in CR-BP-92 §10 is the input to CR-BP-95.

---

## 4. L1 Process Group

**Question answered:** *How are related responsibilities grouped?*

### Definition

> **L1 Process Group** is the canonical entity that organizes related Business Processes within an L0 Process Scope according to an explicit process-centric grouping principle.

### Allowed

* L1 has a `grouping_basis` that is explicit, testable, and selected from a controlled vocabulary (the controlled vocabulary is established by CR-BP-95; until then the existing `kind:` field is the closest analogue).
* L1 has a `grouping_statement`, `membership_criteria`, `inclusions`, `exclusions`, `adjacent_groups`, `parent_process_scope`, and `child_business_processes`.
* L1 is composed by exactly one parent L0 Process Scope (or, in the current prose-only L0 model, by exactly one parent Process Context).
* L1 composes one or more L2 Business Processes.

### Disallowed

* L1 is **not** a Business Function, organizational unit, capability, or arbitrary naming convenience.
* L1 does **not perform work**. It is an organizational construct.
* A Business Function shall not be reified as a Process Group. (The Process Group vs Business Function distinction is the same distinction the existing MECE-007 / MECE-008 / PG-005..008 gates enforce; this section restates it under the decomposition-half of the contract.)

### Where the contract lives today

* Canonical records: `entities/v1-alpha/dea:group-*/dea:group-*.yaml` (48 directories at the time of writing).
* Schema: `schemas/entities/process-group.schema.json`.
* Gates: `scripts/check_process_group.py` (PG-001..008) and `scripts/check_mece.py` (MECE-001..008).
* Reader-facing: `docs/architecture.md` §"Decomposition".

### The `grouping_basis` field

The current `kind:` field on PG records (e.g. `kind: cross-cutting`) is the closest existing analogue to the proposed `grouping_basis.type`. The controlled vocabulary for `grouping_basis.type` is established by CR-BP-95 and may be backfilled across existing PG records in a separate record-reconciliation slice (deferred to CR-BP-99 §14).

---

## 5. L2 Business Process

**Question answered:** *What meaningful enterprise transformation is performed?*

### Definition

> A **Business Process** is an independently meaningful, bounded enterprise transformation that converts inputs into outputs and contributes to a defined outcome/objective under identifiable responsibility.

### Allowed

* L2 has a **trigger**, **input**, **transformation**, **output**, **outcome**, **objective contribution**, **responsibility**, **boundary**, and **evidence**.
* L2 stands as a coherent unit of work (Standalone Executability; BP-C3).
* L2 has identifiable resource responsibility (Resource Dedication; BP-C4).
* L2 has a process-intent (canonical: one of `govern / manage / operate / deliver / support / develop / transform`; see `docs/classification.md`).
* L2 has a process-classification (canonical block form `process_classification.type` per CR-BP-14 §20; one of the five-value vocabulary in `docs/classification.md`).
* L2 has at most one parent L1 Process Group (composes relationship).
* L2 composes one or more L3 Activities.
* L2 carries `ecfConformance` metadata anchoring it to its ECF coordinate.

### Disallowed

* L2 is **not** an Activity, Task, workflow step, work instruction, software operation, organizational role, capability, or implementation artifact.
* L2 does **not** imply sequence. Composition is structural only; it does not imply execution order, temporal sequence, organizational ownership, automation, or system implementation.
* L2's `process_specialization` field may carry an explicit declared ancestry to the OpenDEA Process kernel (`dea:Process`); any tightening of specialization validation is **deferred** under the program governance doctrine (CR-BP-92 §21).

### Where the contract lives today

* Canonical records: `entities/v1-alpha/dea:process-*/dea:process-*.yaml` (139 records at the time of writing; 138 active + 1 deprecated under CR-BP-21a split decision).
* Schema: implicit (no `business-process.schema.json` file; the BP shape is the union of `process-context.schema.json`, the ACT/EXE gates, and the BP-C1..C4 / BP-SEM-001..014 / BP-AR-001..007 / LCM-001..005 / SIV-001..004 / PSP-001..003 gate families).
* Gates: `scripts/check_l2_qualification.py` (BP-C1..C4), `scripts/check_process_semantics.py` (BP-SEM-001..014), `scripts/check_architectural_regression.py` (BP-AR-001..007), `scripts/check_lifecycle_state.py` (LCM-001..005), `scripts/check_semantic_identity_version.py` (SIV-001..004), `scripts/check_intent_purposive.py` (PSP-001..003).
* Reader-facing: `docs/semantic-contract.md` §"The dimensions of a Business Process", `docs/identity.md`, `docs/classification.md`, `docs/architecture.md`.

---

## 6. L3 Activity

**Question answered:** *What cohesive body of work contributes to the parent Business Process?*

### Definition

> An **Activity** is a cohesive body of work within a Business Process that contributes materially to the parent process outcome while not independently satisfying the qualification criteria of a Business Process.

### Allowed

* L3 has a **parent Business Process** (ACT-001, ACT-010).
* L3 has a **cohesive work statement** (ACT-003), **inputs**, **outputs**, **outcome contribution**, **responsibility**, **boundary**, **exclusions**, **sibling distinction**, and **Task decomposition basis** (universal-contract coverage; ACT-011..015 under CR-BP-97).
* L3 fails the L2 qualification criteria (Standalone Executability; Resource Dedication). It is therefore not a Business Process (ACT-002).
* L3 has at most one parent L2 Business Process (composes relationship).
* L3 composes one or more L4 Tasks **OR** carries the explicit `decomposition_boundary: l4-reached` marker (ACT-004; CR-BP-32 §12).

### Disallowed

* L3 is **not** a system function, organizational role, capability, workflow, or implementation step.
* L3 is **not** an independently-qualified Business Process (ACT-002). It does not pass BP-C1..C4.
* L3 carries **no execution-ordering fields** (ACT-006; EXE-002). Sequencing belongs to Workflow/Execution realization.
* L3 carries **no execution-model fields** (ACT-009). Workflow Definition, Workflow Instance, and Execution live downstream of L4.

### Where the contract lives today

* Canonical records: `entities/v1-alpha/dea:activity-*/dea:activity-*.yaml` (553 records at the time of writing).
* Schema: `schemas/entities/activity.schema.json`.
* Gates: `scripts/check_activity_model.py` (ACT-001..010), `scripts/check_execution_boundary.py` (EXE-001..010).
* Reader-facing: `docs/architecture.md` §"Decomposition".

---

## 7. L4 Task

**Question answered:** *What bounded unit of work is performed?*

### Definition

> **L4 Task** is the lowest semantic level of process decomposition. A Task is bounded, actionable, single-responsibility, and independently verifiable for completion.

### Allowed

* L4 is the **decomposition boundary** (CR-BP-32 §12). Anything below L4 belongs to implementation detail outside the catalog.
* L4 is composed by exactly one parent L3 Activity (or, where the parent Activity carries `decomposition_boundary: l4-reached`, L4 is not present and the Activity is itself the boundary).
* L4 is bounded, actionable, single-responsibility, and independently verifiable for completion.

### Disallowed

* L4 is **not** a workflow step, software operation, work instruction, implementation detail, workflow instance, or execution event. The L4 vs Workflow Definition vs Workflow Instance vs Execution boundary is established by CR-BP-98.
* L4 has **no automation, sequencing, branching, conditions, dependencies, participants, events, orchestration, or state transition semantics** (CR-BP-92 §10). Those semantics are realized downstream by Workflow.

### Where the contract lives today

* Canonical records: **none**. L4 is referenced in `activity.schema.json` (`composes[]` entries may target `dea:task-*`) and in `scripts/check_execution_boundary.py` (EXE-001..010), but no Task records exist today. The decision whether L4 lands as a schema + gate is deferred to CR-BP-98 (Task Boundary and Workflow Realization).

---

## 8. The decomposition-vs-execution separation

```text
PROCESS ARCHITECTURE          EXECUTION REALIZATION
L0 -> L1 -> L2 -> L3 -> L4    L4 -> Workflow -> Workflow Instance -> Execution
```

Workflow is **not** an additional process-decomposition level. Workflow realizes and coordinates work; it does not constitute another process-decomposition level.

### The compositional non-implication principle

```text
BusinessProcess
    composes
Activity
    composes
Task
```

does **not** imply:

```text
Task A -> Task B -> Task C
```

Sequence belongs to Workflow/Execution realization (RF-09; ACT-005; ACT-006; EXE-002).

---

## 9. Level-specific information requirements

The following matrix restates CR-BP-92 §5 as the authoritative decomposition-half of the contract. Mandatory attributes are level-specific.

| Attribute      |              L0 |                   L1 |           L2 |         L3 |               L4 |
| -------------- | --------------: | -------------------: | -----------: | ---------: | ---------------: |
| Definition     |        Required |             Required |     Required |   Required |         Required |
| Purpose        |        Required |             Required |     Required |   Required |         Required |
| Boundary       |        Required |             Required |     Required |   Required |         Required |
| Objectives     |        Required |             Required |     Required |   Required |       Contextual |
| Inputs         |      Contextual |           Contextual |     Required |   Required |         Required |
| Transformation |  Not applicable |       Not applicable |     Required |   Required |           Action |
| Outputs        |      Contextual |            Aggregate |     Required |   Required |         Required |
| Outcomes       |        Required |             Required |     Required |   Required | Completion state |
| Trigger        |  Not applicable |       Not applicable |     Required | Contextual |         Required |
| Responsibility | Scope ownership | Group responsibility |     Required |   Required |         Required |
| Children       |              L1 |                   L2 |           L3 |         L4 |      Realization |
| Evidence       |        Required |             Required |     Required |   Required |         Required |
| Workflow       |  Not applicable |       Not applicable |    Reference |  Reference |      Realization |
| Execution      |  Not applicable |       Not applicable |     Boundary |   Boundary | Execution-facing |

The matrix is the **decomposition-half input to CR-BP-99 (Reconciliation Matrix)**. The characterization-half matrix (Intent / Classification / Specialization / Context / Relationships) lives in `docs/semantic-contract.md` §"The dimensions of a Business Process".

---

## 10. Universal decomposition-element contract

The following conceptual contract is **common across all six decomposition layers**. Mandatory attributes are level-specific (per §9). The fields are not required to be present on every record; they are required to be **expressible** at the level where they are applicable.

```yaml
id:
name:
level:
type:

definition:
purpose:

context:
  process_context:
  process_scope:

boundary:
  scope:
  inclusions:
  exclusions:
  adjacent_elements:

objectives:
  - id:
    statement:

inputs:
  - id:
    name:
    description:
    source:

outputs:
  - id:
    name:
    description:
    consumer:

outcomes:
  - id:
    statement:

responsibilities:
  roles:
  capabilities:
  resources:

relationships:
  parent:
  children:
  contributes_to:
  realizes:

evidence:
  - type:
    ref:

governance:
  status:
  owner:
  version:
  effective_from:
```

This is a **common conceptual contract**, not a requirement that every field be mandatory at every level. The level-specific matrix (§9) governs what is mandatory at each level.

---

## 11. Glossary reconciliation

This section reconciles the decomposition-half vocabulary used across the catalog. The terms below are the authoritative decomposition-half definitions; the same terms may have narrower senses in specific gate prose, in which case the gate prose governs.

| Term                       | Layer | Authoritative definition                                                                                          |
| -------------------------- | ----- | ----------------------------------------------------------------------------------------------------------------- |
| **Process Context**        | (n/a) | Non-executable catalog-topology construct at a Domain x Lifecycle Stage cell.                                     |
| **Process Scope**          | L0    | Non-executable architectural boundary defining a coherent area of process responsibility within a Process Context.|
| **Process Group**          | L1    | Canonical entity that organizes related Business Processes within an L0 Process Scope.                            |
| **Business Process**       | L2    | Independently meaningful, bounded enterprise transformation (Trigger -> Input -> Transformation -> Output -> Outcome -> Objective).|
| **Activity**               | L3    | Cohesive body of work within a Business Process that does not independently satisfy L2 qualification.            |
| **Task**                   | L4    | Lowest semantic decomposition level; bounded, actionable, single-responsibility, independently verifiable.        |
| **Workflow Definition**    | (n/a) | Coordinates work; introduces sequencing, branching, conditions, dependencies, participants, events, orchestration, state transitions, automation. |
| **Workflow Instance**      | (n/a) | A specific invocation of a Workflow Definition against a specific input set.                                      |
| **Execution**              | (n/a) | What actually happens when a Workflow Instance runs.                                                              |
| **Outcome**                | (n/a) | What is observed after Execution.                                                                                 |

---

## 12. Allowed/disallowed semantic interpretations

A decomposition element is allowed to satisfy the corresponding row above and **only** the corresponding row. The disallowed interpretations are codified:

| If the element is a...        | Then it is **not** ...                                                                          |
| ----------------------------- | ----------------------------------------------------------------------------------------------- |
| Process Context               | Process, Business Process, Process Group, Business Function, Capability, Organization Unit.     |
| L0 Process Scope              | Same as above; not executable; not the same as its parent Process Context.                      |
| L1 Process Group              | Business Function, organizational unit, capability, arbitrary naming convenience.               |
| L2 Business Process           | Activity, Task, workflow step, work instruction, software operation, organizational role, capability, implementation artifact. |
| L3 Activity                   | System function, organizational role, capability, workflow, implementation step.                |
| L4 Task                       | Workflow step, software operation, work instruction, implementation detail, workflow instance, execution event. |
| Workflow Definition           | A process-decomposition level (not L0..L4). It realizes, not decomposes.                        |

---

## 13. Where this contract intersects the recon programme

The recon programme (CR-BP-92 §16) requires explicit reconciliation between normative prose, schemas, validators, tests, and canonical records. This document is the **normative prose** layer for the decomposition half. The remaining four layers are addressed by the downstream slices:

* **Schema layer** (process-context / process-group / activity + the implicit BP / proposed L0 + L4 schemas): CR-BP-94 (templates) + CR-BP-95 (L0/L1 gate) + CR-BP-96 (L2 gate) + CR-BP-97 (L3 gate) + CR-BP-98 (L4/WF boundary).
* **Validator layer** (the per-gate scripts): same slices.
* **Test layer**: same slices.
* **Canonical-record layer**: CR-BP-99 (Reconciliation Matrix) for any record-level changes.

This document establishes the basis against which CR-BP-99 reconciles.

---

## 14. Non-goals

This document does **not**:

* introduce new entities (no new L0, no new L4, no new Workflow Definition as a decomposition level);
* redefine existing gates (the existing BP-C1..C4 / BP-SEM-001..014 / BP-AR-001..007 / LCM-001..005 / SIV-001..004 / PSP-001..003 / ACT-001..010 / EXE-001..010 / PG-001..008 / MECE-001..008 / PC-001..008 gates remain unchanged);
* tighten specialization validation (held under CR-BP-92 §21);
* modify any canonical record.

This document is the **normative prose layer**. Schema, validator, test, and record reconciliation follow in CR-BP-94..99.

---

## 15. See also

* [`docs/architecture.md`](architecture.md) - the reader-facing decomposition overview.
* [`docs/semantic-contract.md`](semantic-contract.md) - the characterization-half of the catalog's semantic contract.
* [`docs/identity.md`](identity.md) - the process-identity contract.
* [`docs/classification.md`](classification.md) - the Intent / Classification reconciliation.
* [`docs/conformance-pipeline.md`](conformance-pipeline.md) - the 10-step CI pipeline.
* [`change-requests/CR-BP-92-recon-decomposition-and-execution-boundary-hardening.md`](../change-requests/CR-BP-92-recon-decomposition-and-execution-boundary-hardening.md) - the recon programme that establishes this contract.
* [`change-requests/CR-BP-93-decomposition-semantic-contract.md`](../change-requests/CR-BP-93-decomposition-semantic-contract.md) - the carrier CR for this document.
