# CR-BP-92: Recon: Decomposition and Execution Boundary Hardening

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Proposed
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-18
**Carrier**: Reconnaissance / Architectural Reconciliation. Establishes the authoritative findings, target architecture, implementation pipeline, dependency order, and acceptance gates for a coordinated hardening of the L0-L4 decomposition contract and the L4→Workflow→Execution boundary. Does not itself mutate normative prose, schemas, validators, tests, or canonical records.
**Depends on**: CR-BP-32 (Activity Model), CR-BP-33 (Execution Boundary), CR-BP-34a (BP-C1..C4 L2 Qualification), CR-BP-34c (LCM-001..005), CR-BP-34d (SIV-001..004), CR-BP-35 (Process Catalog Architecture Retrospective), CR-BP-36 (MECE-001..008), CR-BP-62 (Lifecycle Discovery Method)
**Lands against**: 139 canonical BP records, 35 canonical PG records, 35 canonical PC records, 553 canonical Activity records; 24 conformance gates CONFORMANT; v0.4.0 tagged (CR-BP-90); v0.4.0+1 commits on main (CR-BP-91 deprecated-BP L3 exclusion)

---

## 0. How to read this CR

This CR establishes the **architectural basis and pipeline**. It is intentionally **not itself an implementation slice**: it mutates zero schemas, validators, tests, templates, or canonical records. The downstream CR-BP-93..99 series (renumbered from the original CR-BP-72..78 reservation: see §25 for the renumbering rationale) carries the implementation work, each as its own slice with its own carrier CR, git branch, and PR.

The implementation pipeline preserves the existing conformance architecture: new validators participate in the existing Structural / Semantic / Naming / Boundary / MECE / Referential Integrity / Cross-Repository Integrity / ECF Conformance framework rather than introducing an independent validation mechanism.

---

## 1. Purpose

This Recon-CR establishes the findings and implementation pipeline arising from a targeted architectural reconciliation of the current Process Catalog.

The reconciliation concentrates on four areas where the repository's normative architecture must remain semantically precise as the catalog grows:

1. **L0 Process Scope**
2. **L1 Process Group**
3. **L2 Business Process specialization and qualification**
4. **L3 Activity → L4 Task → Workflow → Execution boundary**

It additionally establishes a common decomposition-element information contract and identifies where the current schemas, validators, tests, documentation, and canonical records must be reconciled against the normative model.

---

# 2. Architectural Objective

The Process Catalog shall provide a clear and non-overlapping distinction between:

```text
Process Context
        |
        | establishes where process architecture is examined
        v
L0 Process Scope
        |
        | establishes what coherent process responsibility is covered
        v
L1 Process Group
        |
        | organizes related processes according to an explicit basis
        v
L2 Business Process
        |
        | represents an independently meaningful enterprise transformation
        v
L3 Activity
        |
        | represents cohesive work contributing to the Business Process
        v
L4 Task
        |
        | provides the semantic execution boundary
        v
Workflow
        |
        | coordinates execution
        v
Execution
```

The decomposition architecture and execution architecture are therefore related but distinct.

### Normative distinction

```text
PROCESS ARCHITECTURE
L0 -> L1 -> L2 -> L3 -> L4

EXECUTION REALIZATION
L4 -> Workflow -> Workflow Instance -> Execution
```

Workflow shall not be treated as an additional process-decomposition level.

---

# 3. Recon Findings

## RF-01: L0 Process Scope requires explicit semantic status

L0 is currently treated as a conceptual scope construct rather than a canonical executable process element.

This is the correct direction but requires normative clarification.

### Decision

**Process Scope is not:**

* Process
* Business Process
* Process Group
* Business Function
* Capability
* Organization Unit

### Normative definition

> **L0 Process Scope is a non-executable architectural boundary that defines a coherent and bounded area of process responsibility within a Process Context.**

L0 therefore establishes the population of process concerns to be decomposed; it does not itself perform work.

### Required consequence

L0 shall remain a catalog topology construct unless the authoritative OpenDEA/WSF metamodel subsequently establishes Process Scope as a semantic entity.

### Current state (post-CR-BP-19 register v2)

No L0 scope schema, no L0 canonical records, no L0 gate. The current ECF matrix entry is the closest artifact: `entities/v1-alpha/dea:group-*/` directories are L1 groups, not L0 scopes. **Gap:** L0 is missing entirely as an executable construct. Implementation CR-BP-95 (Decomposition Record Templates) and CR-BP-96 (L0/L1 Conformance) shall establish whether L0 lands as a schema + gate or remains prose-only.

## RF-02: Process Context and Process Scope must remain distinct

The following distinction shall be normative:

| Concept          | Answers                                                    |
| ---------------- | ---------------------------------------------------------- |
| Process Context  | **Where is process architecture being examined?**          |
| Process Scope    | **What coherent process responsibility is being covered?** |
| Process Group    | **How are related processes grouped?**                     |
| Business Process | **What meaningful transformation is performed?**           |
| Activity         | **What cohesive body of work contributes?**                |
| Task             | **What bounded unit of work is performed?**                |
| Workflow         | **How is work coordinated?**                               |
| Execution        | **What actually happened?**                                |

An ECF coordinate shall not automatically constitute a Process Scope or Process.

### Current state

`scripts/check_process_context.py` (PC-001..PC-008) validates Process Context records against the `dea:context-*` shape. The Context vs Scope vs Group distinction is enforced by the schema family (`schemas/entities/process-context.schema.json` vs `process-group.schema.json`). **Gap:** Process Context vs Process Scope vs Process Group semantics are codified at the schema level but not at the gate level (PC-001..008 covers Context only; no PG-001..008-derivative for Scope).

## RF-03: Process Group requires an explicit grouping basis

The current Process Group concept correctly separates grouping of processes from Business Function and organizational responsibility.

However, the grouping principle needs to become explicit and testable.

Every Process Group shall declare:

```yaml
grouping_basis:
  type:
  statement:
```

The implementation CR shall establish the controlled vocabulary for grouping-basis types rather than permitting unconstrained values.

A Process Group shall also define:

* grouping purpose;
* membership criteria;
* scope;
* inclusions;
* exclusions;
* adjacent groups;
* parent Process Scope;
* child Business Processes.

### Architectural rule

> A Process Group exists to organize processes according to an explicit process-centric grouping principle; it shall not become a proxy for Business Function, organizational ownership, Capability, or arbitrary naming convenience.

### Current state

`scripts/check_process_group.py` (PG-001..008) and `scripts/check_mece.py` (MECE-001..008) validate PG structure, composition, and MECE. `process-group.schema.json` is the schema. **Gap:** no `grouping_basis` field on PG records; no `grouping_basis` gate. The PG records carry a `kind:` field (e.g. `kind: cross-cutting`) which is the closest existing analogue.

## RF-04: Business Process requires stronger qualification

The current Business Process model establishes important criteria including:

* input/output transformation;
* objective contribution;
* standalone executability;
* resource responsibility.

These criteria shall become part of the executable L2 qualification contract.

The L2 Business Process shall additionally require a recognizable **Outcome**.

The normative model becomes:

```text
Trigger
   |
   v
Input
   |
   v
Transformation
   |
   v
Output
   |
   v
Outcome
   |
   v
Objective Contribution
```

with:

```text
Responsibility
Boundary
Evidence
```

providing the governing context.

### L2 qualification principle

> A Business Process is an independently meaningful, bounded enterprise transformation that converts inputs into outputs and contributes to a defined outcome/objective under identifiable responsibility.

This provides a stronger discriminator between Business Process, Activity, Task, Function and Capability.

### Current state

`scripts/check_l2_qualification.py` (BP-C1..C4) enforces: BP-C1 (trigger + outcome non-empty), BP-C2 (`identity.outcome_statement` non-empty), BP-C3 (`lifecycle_status` + `dea:process-*` id), BP-C4 (`evidence_links` non-empty + `change_history` >= 1 entry). **Gap:** the recon proposes BP-QUAL-001..012 expansion; under §5 (specialization carve-out), the BP-QUAL-011 Specialization Integrity check is deferred. The remaining BP-QUAL checks (001..010, 012) shall be evaluated by CR-BP-97 (Business Process Qualification Gate) against the existing BP-C1..C4 baseline and the post-CR-BP-33 EXE-001..010 boundary.

## RF-05: Business Process specialization must be explicitly anchored

The catalogue shall not redefine the Process kernel.

The normative semantic chain shall be made explicit:

```text
WSF Process
    |
    v
OpenDEA Process
    |
    v
DEA BusinessProcess specialization
    |
    v
Business Process Catalog Record
```

The catalog validator shall ultimately be capable of determining:

```text
Catalog Record
    |
    v
declared specialization
    |
    v
valid specialization
    |
    v
valid parent specialization
    |
    v
valid Process-kernel ancestry
```

The downstream implementation shall therefore reconcile the declared `process_specialization` semantics with the authoritative OpenDEA/WSF model.

### Current state (and **DEFERRED** per §5)

`scripts/check_process_specialization.py` (BP-SPEC-01-001..007) and `docs/governance/process-specialization.md` already exist as advisory gates. **This entire RF is deferred** under the program governance doctrine (user directive 2026-09-14: "specialization is NOT authorized and must not be embarked on until L0-L4 is stabilized in the universal, industry-agnostic sense"). Implementation work under RF-05 is held until the doctrine is relaxed; see §5 for the reopen conditions.

## RF-06: Activity cohesion requires an executable contract

The current Activity definition appropriately positions Activity below Business Process while preventing it from becoming an independently qualified L2 process.

The missing element is a sufficiently explicit cohesion contract.

Every Activity shall establish:

* parent Business Process;
* purpose;
* cohesive work statement;
* inputs;
* outputs;
* outcome/objective contribution;
* responsibility;
* boundary;
* exclusions;
* sibling distinction;
* Task decomposition basis.

### Normative rule

> An Activity is a cohesive body of work within a Business Process that contributes materially to the parent process outcome while not independently satisfying the qualification criteria of a Business Process.

An Activity shall not merely represent:

* a system function;
* an organizational role;
* a capability;
* a workflow;
* an implementation step.

### Current state

`scripts/check_activity_model.py` (ACT-001..010) already enforces: ACT-001 (parent BP), ACT-002 (Activity != BP), ACT-003 (cohesion rationale), ACT-004 (Task composition OR boundary marker), ACT-005 (uses `dea:composes`), ACT-006 (no execution-ordering fields), ACT-007 (Activity id != Business Function id), ACT-008 (no implementation-detail markers), ACT-009 (no execution-model fields), ACT-010 (parent BP traceability). **Gap:** the ACT-001..010 checks cover cohesion at the gate level but not at the universal-contract prose level; CR-BP-98 (Activity Cohesion and Decomposition Gate) shall reconcile.

## RF-07: Task is the semantic execution boundary

Task shall remain the lowest semantic level of process decomposition.

A Task shall be:

* bounded;
* actionable;
* single-responsibility;
* independently verifiable for completion.

Task shall not be conflated with:

* workflow step;
* software operation;
* work instruction;
* implementation detail;
* workflow instance;
* execution event.

The downstream CR shall establish the normative boundary between Task and execution realization.

### Current state

No `dea:task-*` schema, no canonical Task records, no `check_task_*.py` gate. **Task is referenced** in `activity.schema.json` (`composes[]` entries may target `dea:task-*`) and in `scripts/check_execution_boundary.py` (EXE-001..010), but no Task records exist. **Gap:** L4 Task is the explicit decomposition boundary in prose (CR-BP-32 §12: `l4-reached`) but absent as a record type. CR-BP-94 (Decomposition Semantic Contract) and CR-BP-99 (Task Boundary and Workflow Realization) shall resolve.

## RF-08: Workflow must be removed from the decomposition hierarchy

Any documentation or model expression that represents:

```text
L4 Task / Workflow
```

as a single decomposition level shall be reconciled.

The normative architecture shall instead be:

```text
L0 Process Scope
   |
   v
L1 Process Group
   |
   v
L2 Business Process
   |
   v
L3 Activity
   |
   v
L4 Task
```

followed by a separate realization architecture:

```text
Task
   |
   v
Workflow Definition
   |
   v
Workflow Instance
   |
   v
Execution
   |
   v
Observed Result / Outcome
```

Workflow introduces coordination semantics including:

* sequencing;
* branching;
* conditions;
* dependencies;
* participants;
* events;
* orchestration;
* state transitions;
* automation.

Those semantics are not implied by process decomposition.

### Current state

`scripts/check_execution_boundary.py` (EXE-001..010) already enforces the decomposition vs execution separation: EXE-001 (Activity has no execution-state fields), EXE-002 (no ordering/temporal fields), EXE-003..010 (composition vs execution disambiguation). CR-BP-32 §7, §11, §12 establish the boundary in prose. **Already satisfied structurally:** every Activity record carries `decomposition_boundary: l4-reached` (CR-BP-87 cohort and earlier), preventing decomposition past Activity. AC-08 of the recon is therefore largely met at the gate level; CR-BP-99 (Task Boundary and Workflow Realization) shall codify the remaining Workflow Definition vs Workflow Instance vs Execution prose.

## RF-09: Composition must not imply execution

The existing architectural principle that process composition does not imply sequence or execution shall be preserved.

Therefore:

```text
BusinessProcess
    composes
Activity
    composes
Task
```

does not imply:

```text
Task A -> Task B -> Task C
```

Sequence belongs to Workflow/Execution realization.

This distinction shall be protected by documentation and validation.

### Current state

ACT-005 enforces `relationship_type: dea:composes`; ACT-006 forbids execution-ordering fields. EXE-002 forbids ordering/temporal fields. **Already satisfied at gate level.** CR-BP-94 (Decomposition Semantic Contract) shall codify in normative prose.

## RF-10: Normative prose is ahead of executable contracts

The recon identifies a recurring pattern:

```text
Normative prose
       |
       v
Schema
       |
       v
Validator
       |
       v
Tests
       |
       v
Canonical records
```

These layers are not yet uniformly equivalent in semantic depth.

The implementation pipeline shall therefore explicitly reconcile all five.

No new normative requirement should remain solely in prose once its implementation phase is complete.

### Current state

The repo already follows this five-layer discipline for landed slices (CR-BP-32, CR-BP-33, CR-BP-34a-d, CR-BP-35, CR-BP-36, CR-BP-37, CR-BP-62). **Gap:** the L0 Process Scope, the universal decomposition-element contract (RF §13), and the level-specific information requirements (RF §14) are all prose-only today. CR-BP-100 (Schema/Validator/Documentation Reconciliation) is the explicit reconciliation matrix slice.

---

# 4. Universal Decomposition Element Contract

A common information contract shall be established across L0-L4.

Every applicable decomposition element shall support:

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

This is a **common conceptual contract**, not a requirement that every field be mandatory at every level.

Mandatory attributes shall be level-specific.

---

# 5. Level-Specific Information Requirements

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

---

# 6. Required Templates

The implementation pipeline shall establish the following canonical templates:

```text
templates/
├── process-scope.yaml
├── process-group.yaml
├── business-process.yaml
├── activity.yaml
└── task.yaml
```

and:

```text
docs/
└── decomposition-template-guide.md
```

The templates shall include both:

1. machine-oriented schema structure; and
2. human-oriented authoring guidance.

Templates shall make it difficult to create a superficially complete element whose semantic definition is inadequate.

### Current state

No `templates/` directory exists today. The Activity record shape is encoded in `schemas/entities/activity.schema.json` only. **Gap:** no canonical authoring templates. CR-BP-95 (Decomposition Record Templates) shall establish.

---

# 7. CR Implementation Pipeline (renumbered)

The recon reserves the following implementation CR ids. **Renumbering rationale (see §25):** the original CR-BP-72..78 reservation collides with already-landed catalog work (CR-BP-72 A&O Retire escape discovery, CR-BP-73 A&O Retire admission, CR-BP-74 F&A Retire escape discovery, CR-BP-75 F&A Retire admission, CR-BP-76 G&E Retire escape discovery, CR-BP-77 admitted-regulated L3 tranche, CR-BP-78 G&E Retire admission). The catalog CR index is append-only; renumbering avoids breaking the existing CR lineage and preserves the seven downstream slots for the recon's pipeline.

| Recon slice | Implementation CR | Scope                                                                                             |
| ----------- | ----------------- | ------------------------------------------------------------------------------------------------- |
| Semantics   | CR-BP-93          | Decomposition Semantic Contract (definitions, boundaries, glossary reconciliation)               |
| Templates   | CR-BP-94          | Canonical authoring templates for L0-L4 + decomposition-template-guide.md                          |
| L0/L1 Gate  | CR-BP-95          | Process Scope and Process Group Conformance Gate                                                  |
| L2 Gate     | CR-BP-96          | Business Process Qualification Gate (BP-QUAL-001..010 + 012; **BP-QUAL-011 deferred per §5**)      |
| L3 Gate     | CR-BP-97          | Activity Cohesion and Decomposition Gate (extends ACT-001..010 with universal-contract coverage)   |
| L4/WF       | CR-BP-98          | Task Boundary and Workflow Realization (Task record type + Workflow Definition/Instance semantics) |
| Reconcil.   | CR-BP-99          | Schema/Validator/Documentation/Tests/Records Reconciliation Matrix                                |

---

# 8. CR-BP-93: Decomposition Semantic Contract

### Scope

Establish the definitive semantic definitions and boundaries for:

* Process Context;
* L0 Process Scope;
* L1 Process Group;
* L2 Business Process;
* L3 Activity;
* L4 Task.

### Required outputs

* normative definitions;
* allowed/disallowed semantic interpretations;
* decomposition relationships;
* level-specific qualification criteria;
* revised architecture diagrams;
* glossary reconciliation (prose + ADR).

### Dependency

None.

---

# 9. CR-BP-94: Decomposition Record Templates

### Scope

Create the canonical authoring templates for L0-L4.

### Required outputs

```text
templates/
├── process-scope.yaml
├── process-group.yaml
├── business-process.yaml
├── activity.yaml
└── task.yaml
```

plus `docs/decomposition-template-guide.md`.

### Acceptance

Every mandatory normative attribute identified in CR-BP-93 shall have a corresponding schema/template representation.

### Dependency

CR-BP-93.

---

# 10. CR-BP-95: Process Scope and Process Group Contract

### Scope

Formalize L0/L1 structural and semantic contracts.

### Process Scope validation

Validate:

* valid Process Context;
* scope statement;
* scope boundary;
* inclusion/exclusion;
* decomposition basis;
* child Process Groups;
* non-executable nature.

### Process Group validation

Extend PG-001..008 with:

* grouping basis (extended controlled vocabulary from CR-BP-93);
* grouping statement;
* membership criteria;
* inclusions/exclusions;
* child Business Processes;
* sibling distinction;
* process-centric rather than organizational grouping.

### Dependency

CR-BP-94.

---

# 11. CR-BP-96: Business Process Qualification Gate

### Scope

Strengthen L2 validation.

### Required checks

```text
BP-QUAL-001  Identity
BP-QUAL-002  Trigger
BP-QUAL-003  Input
BP-QUAL-004  Transformation
BP-QUAL-005  Output
BP-QUAL-006  Outcome
BP-QUAL-007  Objective Contribution
BP-QUAL-008  Responsibility
BP-QUAL-009  Boundary
BP-QUAL-010  Standalone Process Integrity
BP-QUAL-011  Specialization Integrity [DEFERRED — see §5]
BP-QUAL-012  Evidence
```

BP-QUAL-001..010 + 012 land in CR-BP-96; BP-QUAL-011 (Specialization Integrity) is explicitly carved out under §5 and re-enters scope only when the program governance doctrine permits.

### Dependency

CR-BP-93, CR-BP-94.

---

# 12. CR-BP-97: Activity Cohesion and Decomposition Gate

### Scope

Formalize L3 Activity semantics.

### Required checks

The existing ACT-001..010 baseline (CR-BP-32) is preserved. CR-BP-97 extends with universal-contract coverage:

```text
ACT-011  Cohesive work statement adequacy (extends ACT-003)
ACT-012  Inputs/Outputs integrity (extends ACT-005)
ACT-013  Outcome contribution (extends ACT-003)
ACT-014  Boundary and exclusions (new)
ACT-015  Sibling distinction (new)
```

ACT-016..020 (Task decomposition integrity, Not-independently-qualifying, etc.) are covered by the existing ACT-004 / ACT-010 checks; CR-BP-97 reconciles prose rather than introducing net-new rules.

### Dependency

CR-BP-96.

---

# 13. CR-BP-98: Task Boundary and Workflow Realization

### Scope

Establish the normative boundary between:

```text
Activity
-> Task
-> Workflow
-> Workflow Instance
-> Execution
```

### Required decisions

Define and distinguish:

* Task;
* Workflow Definition;
* Workflow Instance;
* Execution;
* Implementation;
* Work Instruction;
* Automation;
* Agent Action, where applicable.

### Core rule

> Workflow realizes and coordinates work; it does not constitute another process-decomposition level.

### Dependency

CR-BP-97.

---

# 14. CR-BP-99: Schema/Validator/Documentation Reconciliation

### Scope

Perform a systematic reconciliation between:

```text
Normative prose
Schema
Validator
Tests
Canonical records
```

### Required matrix

| Requirement       | Normative definition | Schema   | Validator | Test     | Existing records |
| ----------------- | -------------------- | -------- | --------- | -------- | ---------------- |
| L0 Scope          | Required             | Required | Required  | Required | Reconcile        |
| L1 Grouping       | Required             | Required | Required  | Required | Reconcile        |
| L2 Input          | Required             | Required | Required  | Required | Reconcile        |
| L2 Transformation | Required             | Required | Required  | Required | Reconcile        |
| L2 Output         | Required             | Required | Required  | Required | Reconcile        |
| L2 Outcome        | Required             | Required | Required  | Required | Reconcile        |
| L2 Objective      | Required             | Required | Required  | Required | Reconcile        |
| L2 Responsibility | Required             | Required | Required  | Required | Reconcile        |
| L3 Cohesion       | Required             | Required | Required  | Required | Reconcile        |
| L4 Atomicity      | Required             | Required | Required  | Required | Reconcile        |
| Workflow Boundary | Required             | Required | Required  | Required | Reconcile        |

### Dependency

CR-BP-93 through CR-BP-98.

---

# 15. Canonical Record Reconciliation

After implementation of the contract and validators, existing records shall be assessed.

No existing record shall be silently altered.

Each affected record shall receive one of the governed dispositions:

```text
RETAIN
RENAME
RECLASSIFY
RECONTEXTUALIZE
RESPECIALIZE
MERGE
SPLIT
MOVE
DEFER
RETIRE
REPAIR
```

The reconciliation shall specifically examine:

### L0

* whether the apparent scope is actually a Process Group;
* whether it is incorrectly modeled as a Process;
* whether its boundary is sufficiently explicit.

### L1

* whether grouping is coherent;
* whether the grouping basis is identifiable;
* whether organizational/function semantics have leaked into Process Group.

### L2

* whether the record genuinely qualifies as Business Process;
* whether it has a complete transformation model;
* whether it has an identifiable outcome;
* whether it is correctly specialized.

### L3

* whether the Activity represents cohesive work;
* whether it has an adequate boundary;
* whether it should instead be an L2 or L4 element.

### L4

* whether the element is actually a Task;
* whether it is instead a Workflow step, system operation, work instruction or implementation artifact.

---

# 16. Conformance Gate Expansion

The downstream implementation CRs shall extend the repository's existing conformance architecture rather than introducing an independent validation mechanism.

The new validators shall participate in the existing:

```text
Structural
Semantic
Naming
Boundary
MECE
Referential Integrity
Cross-Repository Integrity
ECF Conformance
```

framework.

Where possible, requirements shall be expressed once and reused across:

```text
Schema
Validator
Tests
Documentation
CI
```

---

# 17. Severity Model

New validation rules shall distinguish between:

### Blocking

Violation prevents canonical conformance.

Examples:

* invalid parent;
* missing required L2 input/output;
* Activity without parent Business Process;
* Task assigned directly to L1;
* Workflow represented as decomposition level.

### Advisory

Violation warrants review but does not necessarily invalidate an existing canonical record.

Examples:

* weak description;
* insufficient evidence;
* unclear adjacent boundary;
* incomplete objective contribution.

The severity of each rule shall be established by the implementation CR rather than assumed by this Recon-CR.

---

# 18. Architectural Acceptance Criteria

The Recon programme shall be considered successfully implemented only when all of the following are true.

### AC-01: Decomposition clarity

There is no normative ambiguity between:

```text
Process Context
Process Scope
Process Group
Business Process
Activity
Task
Workflow
Execution
```

### AC-02: L0 integrity

L0 is explicitly established as a non-executable scope/boundary construct (whether as schema + gate or as normative prose with non-schema enforcement).

### AC-03: L1 integrity

Every Process Group has an explicit grouping basis and membership rationale.

### AC-04: L2 integrity

Every canonical Business Process can demonstrate:

```text
Trigger
Input
Transformation
Output
Outcome
Objective
Responsibility
Boundary
```

### AC-05: L2 specialization integrity

**DEFERRED under §5.** This AC re-enters scope only when the program governance doctrine permits.

### AC-06: L3 integrity

Every Activity demonstrates cohesion and contribution to its parent Business Process.

### AC-07: L4 integrity

Task is explicitly defined as the lowest semantic decomposition level.

### AC-08: Execution separation

Workflow is not represented as a process-decomposition level.

### AC-09: Template completeness

Every decomposition level has an authoritative template.

### AC-10: Contract alignment

Normative prose, schemas, validators and tests express the same semantic contract.

### AC-11: Existing-record reconciliation

All affected canonical records have an explicit governed disposition.

### AC-12: CI enforcement

The new contracts participate in the existing repository conformance pipeline.

---

# 19. Non-Goals

This Recon-CR does **not** authorize:

* wholesale process catalog expansion;
* invention of new Business Processes;
* creation of new process specializations without metamodel authority;
* creation of Workflow as a new decomposition level;
* creation of implementation-specific Tasks merely to populate L4;
* redesign of the OpenDEA/WSF Process kernel;
* introduction of organization-specific process taxonomies;
* automatic modification of existing canonical records.

All such changes require their own authorized implementation CRs.

---

# 20. Dependency Pipeline

The implementation sequence is therefore:

```text
                  RECON-BP-92
                        |
                        v
                CR-BP-93
        Decomposition Semantics
                        |
                        v
                CR-BP-94
        Canonical Templates
                        |
                        v
                CR-BP-95
         L0/L1 Conformance
                        |
                        v
                CR-BP-96
         L2 Qualification
                        |
                        v
                CR-BP-97
        L3 Activity Cohesion
                        |
                        v
                CR-BP-98
        L4 / Workflow Boundary
                        |
                        v
                CR-BP-99
  Schema / Validator / Test Recon
                        |
                        v
              Record Reconciliation
                        |
                        v
           Full Conformance Gate
```

No downstream CR should weaken or bypass the semantic contract established by an upstream CR.

---

# 21. Specialization Carve-Out (deferred)

### Carved-out work

* RF-05 (Business Process specialization must be explicitly anchored) is held until the program governance doctrine is relaxed.
* CR-BP-96 §11 BP-QUAL-011 (Specialization Integrity) is held with the same condition.
* AC-05 (L2 specialization integrity) is held with the same condition.
* Any work that would extend `scripts/check_process_specialization.py` beyond its current advisory-gate scope is held with the same condition.

### Reopen conditions

The carve-out lifts only when **all** of the following are true:

1. The user explicitly relaxes the program governance doctrine (memory directive 2026-09-14: "specialization is NOT authorized ... until L0-L4 is stabilized in the universal, industry-agnostic sense").
2. CR-BP-93..99 (or their successors) have landed and the L0-L4 decomposition contract is stable in production.
3. A separate Recon-CR is filed that catalogues the proposed specialization expansion and authorizes it under the now-relaxed doctrine.
4. CR-BP-99 reconciliation demonstrates that the specialization expansion does not contradict any existing landed slice.

Until those conditions are met, `scripts/check_process_specialization.py` (BP-SPEC-01-001..007) and `docs/governance/process-specialization.md` remain advisory-only and out of scope for any tightening.

---

# 22. Definition of Done for this Recon-CR

This Recon-CR is complete when:

1. The findings are accepted as the authoritative architectural basis.
2. CR-BP-93 through CR-BP-99 are established as the implementation pipeline.
3. Dependencies between the CRs are recorded.
4. The decomposition hierarchy is formally separated from execution realization.
5. The universal decomposition information contract is accepted.
6. The level-specific mandatory attribute model is accepted.
7. No catalog population work is initiated solely as a consequence of this Recon-CR.
8. Subsequent implementation CRs reconcile existing records through the established governance mechanism.
9. Final schema/validator/test alignment is demonstrated through the CR-BP-99 reconciliation matrix.
10. The specialization carve-out (§21) is acknowledged as the standing position until doctrine is relaxed.

---

# 23. Target End State

The resulting architecture shall provide a durable semantic chain:

```text
WHERE
Process Context
      |
      v
WHAT RESPONSIBILITY IS COVERED
L0 Process Scope
      |
      v
HOW PROCESS CONCERNS ARE GROUPED
L1 Process Group
      |
      v
WHAT ENTERPRISE TRANSFORMATION OCCURS
L2 Business Process
      |
      v
WHAT COHESIVE WORK CONTRIBUTES
L3 Activity
      |
      v
WHAT BOUNDED WORK IS PERFORMED
L4 Task
      |
      v
HOW WORK IS COORDINATED
Workflow
      |
      v
WHAT ACTUALLY OCCURS
Execution
      |
      v
WHAT RESULT IS OBSERVED
Outcome
```

This establishes a clean architectural foundation for subsequent integration with **Capabilities, Information, Organization, Workflow, Automation, Simulation, Digital Twin and Agentic Execution** without collapsing those concerns into the Process Catalog itself.

---

# 24. Acceptance criteria for THIS Recon-CR slice

1. `change-requests/CR-BP-92-recon-decomposition-and-execution-boundary-hardening.md` exists with this content (or its equivalent).
2. `change-requests/README.md` carries the CR-BP-92 row before the `## Cross-repo context` anchor.
3. `CATALOG.yaml` regenerated with `open_change_requests` 101 -> 102.
4. No validator, schema, gate, template, or canonical-record mutation.
5. CR-BP-93..99 reserved as the implementation pipeline (no CRs with these ids filed until CR-BP-92 is merged).
6. Specialization carve-out (§21) explicitly noted and referenceable.
7. The 24-gate suite remains CONFORMANT (0 blocking, 0 advisory) post-regen.
8. CR-META gate reports 0 new findings on CR-BP-92.

---

# 25. Renumbering rationale

The recon originally reserved CR-BP-72..78 for the seven implementation slices. The current `change-requests/` index already carries:

| Reserved id | Actual landed CR (already merged)                                                          |
| ----------- | ------------------------------------------------------------------------------------------ |
| CR-BP-72    | A&O Retire Escape-Clause Discovery (PR #113, MERGED 2026-09-15)                            |
| CR-BP-73    | A&O Retire Admission Tranche (PR #114, MERGED)                                             |
| CR-BP-74    | F&A Retire Escape-Clause Discovery (PR #115, MERGED)                                       |
| CR-BP-75    | F&A Retire Admission Tranche (PR #116, MERGED)                                             |
| CR-BP-76    | G&E Retire Escape-Clause Discovery (PR #118, MERGED)                                       |
| CR-BP-77    | L3 Activity Admitted-Regulated-BP Tranche (PR #119, MERGED)                                |
| CR-BP-78    | G&E Retire Admission Tranche (PR #120, MERGED)                                             |

Renumbering to **CR-BP-93..99** preserves the lineage of the seven landed slices (no id renumber, no retroactive rewriting) while keeping the seven recon-slices in a single contiguous block immediately after CR-BP-92. The next available id block (CR-BP-100..) is reserved for future reconciliation work that emerges from CR-BP-99.

---

# 26. Result

CR-BP-92 establishes the authoritative findings, target architecture, and implementation pipeline for a coordinated hardening of the L0-L4 decomposition contract and the L4→Workflow→Execution boundary. The implementation is deferred to CR-BP-93..99 (renumbered from the original CR-BP-72..78 reservation), each as its own slice with its own carrier CR, git branch, and PR. The specialization carve-out (§21) holds RF-05 / BP-QUAL-011 / AC-05 until the program governance doctrine is relaxed. No validator, schema, gate, template, or canonical-record mutation is performed by this slice; the 24-gate suite remains CONFORMANT (0 blocking, 0 advisory); `open_change_requests` 101 -> 102.
