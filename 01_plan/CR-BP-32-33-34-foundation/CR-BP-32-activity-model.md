# CR-BP-32 — Activity Model

> **Renumbering note.** This CR was authored by eaojnr on 2026-09-10 under the title "CR-BP-04 — Activity Model". Renumbered to **CR-BP-32** on landing because `CR-BP-04` is already MERGED (PR #19; "Business Process Identity & ID-Family Reconciliation"; commit `2c0e62f`). All internal cross-references in the user's payload (CR-BP-01..06 sequencing) are preserved as the **original ordering** in §27 of CR-BP-34; the renumbering only renames the carrier IDs (32/33/34) to avoid collision with the existing canonical sequence.
>
> **Sequence status.** The user's payload assumes these CRs land BEFORE CR-BP-07 (Catalog Architecture) and CR-BP-12 (Process Group Profile). The actual landing order in `main` is the inverse: CR-BP-07, CR-BP-12, CR-BP-13..16, CR-BP-22, CR-BP-23 are all already MERGED. CR-BP-32/33/34 therefore land as **post-hoc foundational audits** that strengthen, rather than restructure, the catalog. The "Result" section at the bottom of CR-BP-32/33/34 closes with a note acknowledging the historical inversion and reframing the rules as **retroactive conformance additions** to the existing CR-BP-16 conformance gate.

**Status**: Proposed (carrier CR — knowledge harvest + positioning; awaiting user direction on execution order)
**Layer**: L3 (Business Process)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-09-10
**Original author**: eaojnr
**Source document**: `/home/hermes/.hermes/profiles/coder/cache/documents/doc_cf6fc6bb9e80_CR-BP-04_06.md` (lines 15-393)
**Depends on (logical, in user's intended sequence)**: CR-BP-01, CR-BP-02, CR-BP-03
**Lands against (actual current state)**: CR-BP-01..03 MERGED; CR-BP-12 (Process Group Profile) MERGED; CR-BP-14 (Process Semantic Reconciliation) MERGED; CR-BP-15 (Process Catalog Reconciliation) MERGED; CR-BP-16 (Conformance Gate) MERGED; 196 canonical records (126 L2 BPs / 35 L1 Groups / 35 Process Contexts); conformance level L4

---

CR-BP-32 — Activity Model

CR-BP-04 — Activity Model

Status: Proposed
Type: Process Architecture / Semantic Profile / Catalog
Priority: High
Depends On: CR-BP-01, CR-BP-02, CR-BP-03
Target Repository: technehub-labs/dea-catalog-processes

⸻

1. Change Request

Establish the Activity Model for the OpenDEA Business Process Architecture.

The change shall define the semantic and architectural role of Activity as the intermediate logical decomposition of a Business Process between the canonical L2 Business Process and the atomic L4 Task.

The resulting decomposition shall be:

Process Context
      │
      ▼
L0 Process Scope
      │
      ▼
L1 Process Group
      │
      ▼
L2 Business Process
      │
      ▼
L3 Activity
      │
      ▼
L4 Task

The Activity Model shall provide a disciplined boundary between a Business Process and its constituent logical work groupings without converting the process catalog into an implementation or workflow repository.

⸻

2. Motivation

The Business Process Architecture requires sufficient decomposition to make a Business Process understandable, analyzable, traceable and consumable by humans, systems and AI agents.

However, decomposition must not become an unrestricted descent into implementation detail.

The established process design therefore distinguishes:

* L2 Business Process as the definitive process;
* L3 Activity as a cohesive logical grouping of work;
* L4 Task as an atomic work unit;
* implementation detail below L4 as outside the Business Process Catalog.

The source design explicitly establishes Activity as a logical task grouping and Task as the lowest defined level, with objective cohesion and atomicity criteria.

⸻

3. Architectural Decision

3.1 Activity is a Process Decomposition Construct

An Activity is a logical grouping of work that forms part of a Business Process but does not itself satisfy the complete criteria required for an L2 Business Process.

Activity therefore exists primarily to explain the internal structure of a Business Process.

It shall not automatically be interpreted as:

* a Business Process;
* a Business Function;
* a Workflow;
* a Task;
* an organizational unit;
* an executable system operation.

⸻

4. Activity Definition

Activity

A cohesive grouping of work within a Business Process that provides a meaningful logical unit of process structure without constituting an independently defined Business Process.

An Activity shall normally:

1. belong to an L2 Business Process;
2. contribute to the Business Process outcome;
3. contain one or more Tasks;
4. have identifiable work cohesion;
5. have a meaningful logical boundary;
6. remain subordinate to its parent Business Process.

⸻

5. Activity Versus Business Process

An apparent work grouping shall be classified as an L2 Business Process rather than an Activity when it satisfies the established Business Process criteria.

The four mandatory L2 criteria are:

1. Input–Output Transformation
2. Objective Contribution
3. Standalone Executability
4. Resource Dedication

The source design establishes these as the necessary and sufficient criteria for determining whether a unit qualifies as an L2 Process.

Therefore:

Candidate Work Unit
        │
        ├── satisfies L2 criteria ──► Business Process
        │
        └── does not satisfy L2 criteria
                    │
                    ▼
                 Activity

This distinction prevents the catalog from promoting every meaningful work grouping into a Business Process.

⸻

6. Activity Cohesion

Each Activity shall be evaluated for cohesion.

The initial catalog profile shall retain the established 0–9 Cohesion Evaluation Score as a validation mechanism.

The score shall assess whether the constituent work belongs together as a meaningful logical unit.

A low-cohesion grouping shall be:

* decomposed differently;
* reassigned;
* absorbed into an adjacent Activity; or
* retained at the parent Process level when no meaningful Activity boundary exists.

The numerical threshold shall be governed by the conformance specification rather than embedded as an informal naming convention.

⸻

7. Activity Composition

The canonical structural relationship shall be:

BusinessProcess
      │
      │ dea:composes
      ▼
Activity
      │
      │ dea:composes
      ▼
Task

The catalog shall use dea:composes rather than introducing competing relationships such as:

* parent_activity;
* child_activities;
* decomposes;
* contains_activity.

The decomposition relation expresses structural composition only.

It does not imply:

* execution order;
* temporal sequence;
* organizational ownership;
* automation;
* system implementation.

⸻

8. Activity and Task

Activity and Task have distinct semantic roles.

Construct	Role
Business Process	Definitive outcome-producing process
Activity	Logical grouping of process work
Task	Atomic defined work unit

A Task shall represent the smallest work unit that the Business Process Catalog formally models.

The source design defines Task atomicity using:

1. Indivisibility;
2. Single-Role Execution;
3. Bounded Duration;
4. Verifiable Completion.

These criteria shall be carried forward into CR-BP-06 conformance validation.

⸻

9. Activity Naming

Activity names shall describe the logical work being performed.

The catalog shall prefer a consistent gerund or equivalent activity-oriented form where appropriate.

Examples:

Validate Order
Assess Customer Eligibility
Prepare Fulfilment
Confirm Delivery

Naming conventions shall not determine semantic classification by themselves. Semantic tests take precedence over lexical form.

⸻

10. Activity Boundary

An Activity boundary is justified when:

* the constituent Tasks exhibit meaningful cohesion;
* the grouping contributes a recognizable portion of the Process outcome;
* the grouping improves process comprehension;
* the grouping provides a stable analytical boundary;
* the grouping does not merely reproduce an organizational department;
* the grouping does not represent system implementation detail.

An Activity shall not be introduced merely to increase decomposition depth.

⸻

11. Activity and Execution

Activity structure shall remain independent from executable process behaviour.

An Activity may later be realized through:

* one Workflow;
* multiple Workflows;
* manual work;
* automated work;
* a combination of human and system execution.

Therefore:

Process Architecture
        │
        ├── Business Process
        │      └── Activity
        │             └── Task
        │
        └── Execution Architecture
               └── Workflow
                      └── executable Task flow

The execution relationship is governed separately by CR-BP-05.

⸻

12. Decomposition Boundary

The Business Process Catalog shall formally terminate at L4:

L2 Business Process
        ↓
L3 Activity
        ↓
L4 Task
        ↓
STOP

Anything below L4 belongs to implementation-specific detail such as:

* system operations;
* API calls;
* scripts;
* procedures;
* work instructions;
* technical execution steps.

The source design explicitly identifies content below L4 as implementation detail outside the Business Process Framework.

⸻

13. Out of Scope

CR-BP-04 shall not:

* create a new normative dea:Activity unless separately approved;
* redefine Workflow;
* redefine Task;
* define execution sequence;
* define BPMN semantics;
* define system implementation;
* define organizational ownership;
* establish automation semantics;
* establish MECE validation in full;
* modify the ECF;
* redefine Business Process.

⸻

14. Repository Changes

The process repository shall establish:

architecture/
    decomposition.yaml
    activity-model.yaml
schemas/
    activity.schema.json
validation/
    activity/
        l2-boundary.yaml
        cohesion.yaml
        task-boundary.yaml
docs/
    activity-model.md

Existing process records shall progressively conform to the Activity Model.

⸻

15. Conformance Rules

Initial rules:

ACT-001 — Every Activity belongs to a Business Process.

ACT-002 — An Activity shall not be represented as an L2 Business Process unless it satisfies the L2 Process criteria.

ACT-003 — Every Activity shall have a meaningful cohesion rationale.

ACT-004 — An Activity shall contain at least one defined Task where decomposition reaches L4.

ACT-005 — Activity composition shall use dea:composes.

ACT-006 — Activity decomposition shall not imply execution sequence.

ACT-007 — Activity shall not be used as a synonym for Business Function.

ACT-008 — Activity shall not represent implementation detail below the Task boundary.

ACT-009 — Activity shall not introduce an independent execution model.

ACT-010 — Activity definitions shall remain traceable to their parent Business Process.

⸻

16. Acceptance Criteria

CR-BP-04 is accepted when:

* Activity has a stable architectural definition;
* L2/L3 boundary is objectively defined;
* cohesion evaluation is machine-representable;
* L3/L4 structural semantics are explicit;
* Task remains distinct from Activity;
* dea:composes is the canonical structural relationship;
* execution semantics remain outside the Activity Model;
* L4 is established as the catalog decomposition boundary;
* schemas and validation rules exist;
* documentation reflects the model;
* no competing foundational metamodel concept is introduced without a separate CR.

⸻

17. Result

CR-BP-04 establishes the logical structure of Business Process decomposition.

It answers:

What is the internal logical structure of a Business Process?

It deliberately does not answer:

How is that structure executed?

That question belongs to CR-BP-05.

⸻

## Result (as authored)

CR-BP-04 establishes the logical structure of Business Process decomposition.

It answers:

What is the internal logical structure of a Business Process?

It deliberately does not answer:

How is that structure executed?

That question belongs to CR-BP-33 (formerly CR-BP-05).

⸻

## Result (post-landing — added by Coder on 2026-09-10)

**Historical-context note.** When the user authored this CR on 2026-09-10, they intended CR-BP-32/33/34 to be the foundational sequence that precedes CR-BP-07 (Catalog Architecture) and the catalog population. In the actual landing order in `main`, that foundational sequence was **inverted**: the catalog was populated first (PR #22..#60) under the looser CR-BP-12 (Process Group Profile) + CR-BP-14 (Semantic Reconciliation) + CR-BP-15 (Catalog Reconciliation) + CR-BP-16 (Conformance Gate) regime, and 196 canonical records are now live at conformance level L4.

**Implication for CR-BP-32.** The Activity Model — L3 logical decomposition beneath L2 Business Process — is **not** yet instantiated in the catalog. The schema for `dea:Activity` does not exist; the `relationships.composes` instances in current BP records terminate at `dea:BusinessProcess` siblings, not at `dea:Activity` children. Land CR-BP-32 means:

1. **Add `dea:Activity` to `metamodel-pointer.yaml`** as an `lifecycle: proposed` specialization under `dea:Process` (mirroring how `dea:BusinessProcess` is registered; see `dea-metamodel/metamodel/registry/entities.yaml`).
2. **Add an Activity schema** (`schemas/entities/activity.schema.json`) parallel to `process-context.schema.json` / `process-group.schema.json`.
3. **Add a first-class Activity record type** at `entities/v1-alpha/dea:activity-*/` with the structure laid out in §14 of the user's CR body.
4. **Add Activity-level validation rules** (ACT-001..010) to the conformance suite. These become **additive** rules on the existing CR-BP-16 gate; existing records stay conformant because Activity is a new layer beneath them, not a constraint on the existing L2 layer.
5. **No retroactive decomposition of existing 126 L2 BPs into Activities.** Activities are introduced as a **new authorial affordance** for contributors who want to model the internal structure of a Business Process; existing BPs without Activity decomposition are valid (and remain at L4 conformance) until/unless a contributor explicitly adds Activity children.

**Sequence recommendation.** Land CR-BP-32 first (L3 Activity, no entity mutation), then CR-BP-33 (Execution Boundary, no entity mutation), then CR-BP-34 (Process Conformance Profile, **additive rules only**). Each is independently mergeable. Activities and Workflow references stay optional; the catalog's existing 196 records remain authoritative and conformant throughout.
