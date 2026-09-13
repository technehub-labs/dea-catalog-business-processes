# OpenDEA Business Process Catalog

## Purpose

The **OpenDEA Business Process Catalog** establishes the canonical,
structured and machine-consumable foundation for the **Business Process
specialization** of the OpenDEA Process kernel.

The catalog supports the **Business Architecture** and **Business
Operations** use cases (CR-MM-PROC-01; CR-AR-FMWK-01; CR-BP-SPEC-BP-01).
It is **one of potentially several** Process-specialization catalogs in
the OpenDEA ecosystem. Other specializations (Operational, Engineering,
etc.) will have their own catalogs when their use cases emerge.

The Process discipline is a **kernel + specializations** model: WSF is
authoritative on the Process concept; DEA inherits via specialization;
`dea:BusinessProcess` is the first specialization context (Business
Architecture + Business Operations). The catalog itself covers only
the Business Process specialization; it does not redefine the kernel.

The governing principle is:

> **One kernel. Many valid specializations. One canonical home per
> specialization.**

---

# Reading This Repository

Two documents orient a new reader before the detailed architecture:

* [`docs/semantic-contract.md`](docs/semantic-contract.md): what a
  Business Process record in this catalog means; the six
  characterization dimensions and the separations that are always true.
* [`docs/governance/reconciliation-programme.md`](docs/governance/reconciliation-programme.md):
  how the catalog is governed over time; the research-to-canonical
  loop, the reconciliation dispositions, and the conformance gate.

---

# Architectural Position

The Business Process Catalog is grounded in the OpenDEA conceptual architecture.

The OpenDEA Enterprise Concept Framework (ECF) provides the primary organizing structure for understanding the enterprise. The ECF establishes a matrix formed by the intersection of Enterprise Domains and Lifecycle Stages.

The Business Process Catalog uses this structure as its contextual foundation.

```text
Enterprise Domain × Lifecycle Stage
                │
                ▼
          Process Scope / Context
                │
                ▼
       Process Architecture
                │
                ▼
        Process Decomposition
```

An ECF intersection does not automatically represent a business process.

Instead, each intersection defines the **Process Context** within which the relevant business processes are identified, analysed and validated.

This distinction is fundamental to the architecture of the catalog.

> **The ECF provides the contextual coordinate. The Business Process Architecture provides the process structure.**

---

# Process Architecture (CR-BP-03; reconciled by CR-BP-14)

CR-BP-03 establishes the **Business Process architecture** within the
enterprise process landscape. The architecture rests on **three
pillars**: a 4-axis classification, a process-identity contract, and
a contribution-driven re-landscape mechanism. CR-BP-14 reconciles
the architecture by separating Process Intent and Process
Classification as formally distinct dimensions (CR-BP-14 §10, §11);
see `docs/semantic-contract.md` for the normative constitution and
`docs/classification.md` for the current narrative.

## 1. Enterprise Process Landscape

The enterprise process landscape is organized through five process
types (per Mintzberg's five-component model), each associated with a
primary organizational component:

| Process Type | Primary Organizational Component | Primary Purpose |
|---|---|---|
| **Strategic** Process | Strategic Apex | Enterprise direction, vision, goals, and strategic decisions |
| **Management** Process | Middle Line | Plan, monitor, and control resource allocation to achieve strategic goals |
| **Core** Process | Operating Core | Direct value creation; products and services delivered to external customers |
| **Support** Process | Support Staff | Internal-to-enterprise services that keep the organization running |
| **Standardization** Process | Technostructure | Cross-cutting overlay for compliance, consistency, continuous improvement, and quality |

These five process types describe **the character and primary
organizational locus of enterprise work**. They do **not** constitute
competing foundational OpenDEA process entities.

> **`dea:BusinessProcess` remains the canonical OpenDEA semantic
> entity** for Business Processes regardless of `process_type`. The
> classification is a catalog-controlled vocabulary at
> `classifications/process-types.yaml`, not a new ontology.

The vocabulary is enforced by
`scripts/check_process_identity.py` (BP-ARC-ID-004) when a
contribution is submitted.

## 2. Four Distinct Process Axes

CR-BP-03 introduces a **4-axis classification** that separates four
distinct concerns. Each axis answers a different question;
conflating them is the historical source of much process-catalog
confusion. CR-BP-14 §11 formalizes the Intent vs Classification
distinction: the two vocabularies are independent; neither dimension
may be inferred from the other; identical tokens across the two
(`support`; legacy `management` vs canonical `manage`) are a lexical
coincidence, not a semantic equivalence (BP-SEM-011).

| Axis | Field | Vocabulary | Question it answers |
|---|---|---|---|
| **Intent** | `process_intent` (canonical CR-BP-14 vocabulary; legacy aliases readable) | govern / manage / operate / deliver / support / develop / transform | **Why does this work exist?** The purposeful nature of the work. |
| **Classification** | `process_type` (canonical block form `process_classification`) | strategic / management / core / support / standardization | **Where is this process positioned in the process landscape?** The 5-component classification (Mintzberg). |
| **Specialization** | `process_specialization` | list of parent process ids | **What is this process a specialization of?** Semantic refinement (CR-BP-14 §12). |
| **Context** | `context` (canonical CR-BP-14 block; legacy `process_audience` is a migration alias) | array of `{ref: dea:pc-*}` + `serves` / `contributes-to` relationships toward ECF coordinates | **Where is the responsibility examined?** ECF Domain × Lifecycle Stage. |

The four axes are **additive** and **optional individually**; entries
can declare any subset. `process_type` defaults to `core` when the
entry is a Business Process. See [`docs/classification.md`](docs/classification.md)
for the full classification narrative.

## 3. Process Decomposition (L0 / L1 / L2: conceptual)

The Business Process catalog decomposes the enterprise process
landscape through a conceptual L0 / L1 / L2 hierarchy. **L0 and L1
are catalog topology constructs; L2 is the canonical semantic
level** (`dea:BusinessProcess`).

```text
ECF Domain × Lifecycle Stage
         │
         ▼
   Process Context          (CR-BP-02; contexts/v1/)
         │   conceptual L0 (Process Scope)
         ▼
   Process Group            (conceptual L1; documented; not
         │       a separate directory)
         ▼
   Business Process         (L2; entities/v1/; dea:BusinessProcess)
         │
         ▼
   Activity                 (CR-BP-04; future)
         │
         ▼
   Workflow / Task          (CR-BP-05; future; authoritative
                             metamodel)
```

**Process Group is NOT equivalent to Business Function.** A Business
Function is an OpenDEA semantic concept concerned with organizational
grouping of capabilities and ownership. Process Group is concerned
with organizing processes. They answer different questions and live
at different modeling concerns.

**No separate top-level directories** for L0 / L1 / L2. L0 / L1 are
**conceptual constructs** documented here + [`docs/architecture.md`](docs/architecture.md).
The L2 entries live at `entities/v1/` (currently `v1-alpha/`).

## 4. Structural Composition

Process decomposition uses the authoritative OpenDEA relationship
`dea:composes`. Structural composition means:

- part-of structure;
- containment within the process architecture;
- hierarchical decomposition;
- **no implied sequence**;
- **no implied execution**;
- **no implied organizational ownership**.

In the schema, structural composition is captured in
`relationships.composes` (canonical). The legacy `parent_process` /
`child_processes` fields are preserved as migration aliases and are
not authoritative.

## 5. Capability Realization

Capability realization is captured in `relationships.realizes`
(canonical). The legacy `capabilities_delivered` field is preserved
as a migration alias.

```text
              ┌───────────────┐
              │ Business      │
              │ Capability    │
              └───────▲───────┘
                      │
                   realizes
                      │
              ┌───────┴───────┐
              │ Business      │
              │ Process       │
              └───────┬───────┘
                      │
                   composes
                      │
                      ▼
              Business Process
```

## 6. Process Identity

A process is tested by **name + description + trigger + outcome +
evidence, not by name alone**. The identity sub-block
(`schemas/identity.schema.json`) is the contract:

```yaml
identity:
  verb: Manage           # action verb (imperative; singular)
  object: Customer       # the noun being acted on
  scope: <optional>      # optional scope qualifier
  outcome_statement: |
    Customer relationships are maintained, escalated where
    required, and renewed or terminated per policy.
  evidence_links:
    - type: documentation
      ref: docs/processes/manage-customer.md
    - type: governance
      ref: governance/process-manage-customer.md
```

The validator `scripts/check_process_identity.py` enforces
**BP-ARC-ID-001..BP-ARC-ID-005**:

- BP-ARC-ID-001: name matches identity verb + object (+ optional scope).
- BP-ARC-ID-002: trigger is non-empty.
- BP-ARC-ID-003: outcome is non-empty and consistent with `outcome_statement`.
- BP-ARC-ID-004: `process_type` is consistent with `outcome_statement`.
- BP-ARC-ID-005: `evidence_links` is non-empty.

A process that violates one or more of these rules is **flagged
for review** by the contribution report (see §7). The catalog does
**not** auto-rewrite. See [`docs/identity.md`](docs/identity.md).

## 7. Re-landscape (Contribution-Driven)

A new process is **not** added directly to `entities/v1/`; the
contributor submits a **Process Contribution** to
`contributions/processes/`, and the **CI contribution report
workflow** generates a reclassification recommendation.

```text
contribution submitted
   │  (PR to contributions/processes/<id>.yaml)
   ▼
CI report generated
   │  (artifact: contributions/processes/<id>.report.md)
   │  (PR comment)
   ▼
Reviewer reviews
   │
   ├── accept  → land in entities/v1-alpha/<id>.yaml
   │
   ├── re-classify → contributor updates proposed_entry
   │                and re-runs CI
   │
   └── reject → PR closed; contribution archived
```

The re-landscape mechanism is **contribution-driven** (not in-tree)
and **CI-piped** (the report is generated as a PR artifact). The
catalog does not auto-rewrite; a catalog maintainer reviews the
recommendation. See [`docs/relandscape.md`](docs/relandscape.md).

## 8. No Breaking Changes

CR-BP-03 introduces new fields additively. CR-BP-14 reconciles the
semantic contract while keeping all canonical and legacy fields
readable throughout the migration period: the three-value
`process_intent` vocabulary (operational / support / management) is
retained as deprecated migration aliases alongside the canonical
seven-value vocabulary; `process_type` is retained unchanged; the
legacy scalar `process_context` and the `process_audience` field
are both retained as migration aliases superseded by the canonical
`context:` block (CR-BP-14 §20).

Existing canonical entries continue to validate; the BP-SEM-001..012
validator (CR-BP-14 §21) records legacy findings as warnings until
CR-BP-15 reconciliation closes the migration.

---

# Enterprise Concept Framework

The Enterprise Concept Framework provides a holistic and structured representation of the enterprise through the intersection of:

* Enterprise Domains
* Lifecycle Stages

Each intersection represents a distinct enterprise context.

```text
ECF Cell

Domain
   ×
Lifecycle Stage
   │
   ▼
Enterprise Context
```

Within the Business Process Catalog, an ECF cell is interpreted as a **Process Context**.

A Process Context defines the conceptual boundary within which one or more business process elements may be identified.

The Process Context is therefore not automatically equivalent to:

* a Business Process;
* a Business Function;
* a Business Capability;
* a Process Group; or
* a process decomposition level.

The Process Context provides the semantic and architectural boundary for determining which business processes belong within the Domain and Lifecycle intersection.

---

# Canonical Process Context

Each Process Context is defined by a unique combination of:

```text
Domain
Lifecycle Stage
```

Conceptually:

```text
Process Context
├── Domain
├── Lifecycle Stage
├── Scope
├── Included Concerns
├── Excluded Concerns
├── Adjacent Contexts
└── Process Elements
```

The catalog carries a **Process Context Register** at
`contexts/v1-alpha/` (CR-BP-02). Each entry conforms to
`schemas/entities/process-context.schema.json` and is validated by
`scripts/check_process_context.py` (rules PC-001..PC-008).

**The matrix is empty by design.** CR-BP-02 explicitly defers
population until the architecture is established; populating the
49-cell matrix belongs to subsequent CRs (CR-BP-10 and onwards).

Every Process Context should establish:

* what enterprise concerns belong within the context;
* what outcomes or transformations must be addressed;
* what concerns are explicitly outside the context;
* which adjacent ECF contexts may have closely related responsibilities; and
* the criteria used to determine the placement of process elements.

This provides the basis for maintaining clear boundaries throughout the catalog.

> **Important:** A Process Context is **NOT** a Business Process. The
> Context provides the semantic boundary for process discovery; the
> Business Process (this catalog's specialization of the OpenDEA
> Process kernel) provides the structured process elements.
> CR-BP-02 / PC-007 enforces this distinction.

---

# Business Process Architecture

The Business Process Catalog establishes a structured decomposition architecture.

The intended topology is:

```text
Process Context
       │
       ▼
L0 ── Process Scope
       │
       ▼
L1 ── Process Group
       │
       ▼
L2 ── Business Process
       │
       ▼
L3 ── Activity
       │
       ▼
L4 ── Task
```

The precise normative semantics of these levels will be aligned with the OpenDEA Metamodel.

The current architecture treats the levels as follows.

## L0: Process Scope / Process Context

L0 establishes the highest-level scope within which a coherent set of related process concerns is organized.

L0 provides the conceptual entry point for process decomposition within a Process Context.

An L0 element must:

* represent a coherent and stable enterprise responsibility;
* have a clear semantic boundary;
* contribute uniquely to the coverage of its Process Context;
* avoid overlap with sibling L0 elements; and
* provide a meaningful basis for decomposition.

An ECF Process Context may contain one or more L0 elements.

An L0 element is not assumed to be synonymous with an ECF Domain or Lifecycle Stage.

---

## L1: Process Group

L1 represents a coherent grouping of related processes within an L0 Process Scope.

A Process Group organizes related process responsibilities that share a meaningful functional or operational relationship.

An L1 element must:

* have a clear purpose within its parent L0;
* establish a non-overlapping boundary relative to sibling groups;
* provide a meaningful grouping for lower-level processes; and
* support systematic decomposition.

The precise relationship between Process Group, Business Function and other OpenDEA concepts will be governed by the normative OpenDEA Metamodel.

The Business Process Catalog must not independently redefine Business Function.

---

## L2: Business Process

L2 represents the first level at which an element is treated as an independently meaningful Business Process.

An L2 Business Process must satisfy the normative criteria established for a Business Process.

The intended validation criteria include:

1. **Input and Output Transformation**
   The process transforms defined inputs into defined outputs.

2. **Objective Contribution**
   The process makes a distinct contribution toward a defined business or enterprise objective.

3. **Standalone Executability**
   The process can be understood and executed as a coherent unit of work.

4. **Resource Responsibility**
   The process has identifiable responsibility for the resources, capabilities, roles or means required for its execution.

An element that does not satisfy the required criteria should not be classified as an L2 Business Process.

It may instead represent:

* a Process Group;
* an Activity;
* a Task;
* a Business Function;
* a Capability; or
* another OpenDEA concept.

---

## L3: Activity

L3 represents a cohesive grouping of work that contributes to an L2 Business Process but does not independently satisfy the criteria required for an L2 Business Process.

An Activity provides logical structure within a Business Process.

Activities should be evaluated according to their:

* cohesion;
* contribution to the parent process;
* boundary clarity;
* independence from sibling activities; and
* appropriateness as a grouping of tasks.

The formal cohesion model and scoring criteria will be defined as part of the repository validation architecture.

---

## L4: Task

L4 represents the lowest defined level of business process decomposition within the catalog.

A Task is an actionable unit of work that contributes to the completion of an Activity.

A Task should satisfy the intended atomicity criteria:

1. **Indivisibility**
   The task represents a sufficiently atomic unit of work within the Business Process Architecture.

2. **Single Responsibility**
   The task has a clear primary execution responsibility.

3. **Bounded Execution**
   The task represents a bounded unit of work.

4. **Verifiable Completion**
   Completion of the task can be determined.

Work below the approved decomposition boundary is treated as implementation detail, system behaviour, workflow logic or work instruction unless explicitly modelled by another OpenDEA framework.

The normative decomposition stopping rule will be established through OpenDEA governance.

---

# Process Discovery Method

Business processes are not created by mechanically combining Domain and Lifecycle terminology.

The catalog does not treat the ECF matrix as a process name generator.

Instead, process elements are derived through structured semantic analysis.

The governing principle is:

> **Processes are discovered from the meaning of the enterprise context, not constructed through word combinations.**

For each Process Context, the following method is applied.

## 1. Establish the Context

Determine the meaning of:

```text
Domain
+
Lifecycle Stage
=
Process Context
```

The analysis must establish what the intersection means from an enterprise perspective.

---

## 2. Define the Cell Charter

Each Process Context should establish a Cell Charter describing:

* the enterprise concern;
* the lifecycle concern;
* the combined semantic meaning;
* expected outcomes;
* relevant transformations;
* inclusions;
* exclusions; and
* adjacent boundaries.

The Cell Charter establishes the basis for process identification.

---

## 3. Identify Coverage Concerns

Before identifying processes, determine the complete set of concerns that must be addressed within the Process Context.

These concerns represent semantic coverage requirements.

They are not automatically process elements.

This prevents the premature acceptance of the first plausible process name.

---

## 4. Identify Candidate Processes

Candidate processes should be derived from:

* recognised business process concepts;
* established management and operational disciplines;
* enterprise architecture;
* industry practices;
* authoritative process frameworks; and
* the semantic requirements of the Process Context.

The preferred approach is to identify established and recognisable business process concepts.

Artificially constructed names should be avoided.

---

## 5. Evaluate Process Candidates

Each candidate is evaluated against:

* semantic fit;
* Process Context coverage;
* uniqueness of contribution;
* process criteria;
* boundary clarity;
* overlap with other candidates; and
* compatibility with the OpenDEA Metamodel.

A candidate must not be accepted simply because it appears linguistically appropriate.

---

## 6. Establish the Canonical Set

The accepted set of process elements must collectively address the Process Context.

The objective is to identify the smallest coherent set that provides complete coverage without unnecessary duplication.

This may result in:

* one process element;
* multiple process elements; or
* further architectural analysis where the Process Context has not yet been sufficiently understood.

---

# MECE and Holistic Coverage

The Business Process Catalog applies Mutually Exclusive and Collectively Exhaustive principles across multiple architectural scopes.

MECE is not treated as a single validation exercise.

## Process Context MECE

Within a Domain × Lifecycle Process Context:

* sibling process elements must not duplicate responsibility;
* every accepted element must provide unique coverage; and
* the complete set must collectively address the defined Cell Charter.

---

## Domain MECE

Across all Lifecycle Stages within an Enterprise Domain:

* process responsibilities must be lifecycle-specific;
* the same process should not be independently recreated across multiple stages;
* lifecycle transitions must have clear boundaries.

---

## Lifecycle MECE

Across all Enterprise Domains within a Lifecycle Stage:

* each Domain must maintain a distinct enterprise concern;
* processes must not duplicate responsibilities already owned by another Domain;
* cross-domain dependencies must be represented as relationships rather than duplicate process definitions.

---

## Enterprise Matrix MECE

Across the complete ECF matrix:

* each process element must have one canonical conceptual home;
* duplicate process definitions must be prevented;
* related processes may exist across contexts without representing the same process;
* relationships must not be confused with ownership.

The governing principle is:

> **One canonical home. Many valid relationships.**

---

## Hierarchical MECE

At every level of decomposition:

```text
Parent
 ├── Child A
 ├── Child B
 └── Child C
```

the children must:

* collectively cover the intended scope of the parent; and
* maintain clear, non-overlapping boundaries.

A decomposition must not merely restate the parent at increasing levels of detail.

Each level must introduce a meaningful structural distinction.

---

# Canonical Identity

Every canonical process element will have a stable identifier.

Names and descriptions may evolve through governed change, but identity must remain stable.

Downstream OpenDEA repositories should reference canonical process identifiers rather than reproduce independent copies of process definitions.

Conceptually:

```text
Canonical Process
        │
        ├── Capability Relationship
        ├── Function Relationship
        ├── Value Stream Relationship
        ├── Information Relationship
        ├── Policy Relationship
        ├── Organization Relationship
        ├── Role Relationship
        ├── Product Relationship
        ├── Service Relationship
        ├── Workflow Relationship
        ├── Agent Relationship
        └── System Relationship
```

The existence of a relationship does not create another canonical definition of the same process.

---

# Relationship with the OpenDEA Metamodel

The Business Process Catalog is not an independent ontology.

The normative definition of Business Process and its relationships are governed by the OpenDEA Metamodel.

The repository may define catalog structures, decomposition profiles, validation rules and controlled representations required to manage the Business Process Architecture.

Where the Business Process Architecture identifies a missing foundational concept or relationship, the change must be assessed against the OpenDEA Metamodel.

The expected evolution path is:

```text
Architectural Requirement
        │
        ▼
Conceptual Analysis
        │
        ▼
OpenDEA Metamodel Assessment
        │
        ├── Existing Semantic Support
        │         │
        │         ▼
        │    Catalog Implementation
        │
        └── Semantic Gap
                  │
                  ▼
             Change Request
                  │
                  ▼
        Metamodel Evolution
                  │
                  ▼
        Derived Schema Evolution
                  │
                  ▼
        Catalog Implementation
```

The catalog must not introduce local semantic constructs that conflict with or bypass the normative OpenDEA Metamodel.

---

# Relationship with Business Capabilities and Functions

Business Process must maintain conceptual separation from related OpenDEA concepts.

In particular:

* **Business Capability** represents what an enterprise is able to do.
* **Business Function** represents a logical grouping of responsibilities or areas of work.
* **Business Process** represents a structured transformation of inputs into outcomes.
* **Activity** represents a cohesive component of a Business Process.
* **Task** represents an actionable unit of work.

These distinctions are governed by the OpenDEA conceptual and normative metamodels.

The Business Process Catalog must therefore not absorb Business Functions, Capabilities or other concepts merely because their names resemble processes.

Where a classification ambiguity exists, the element must be analysed against the applicable semantic criteria before acceptance into the catalog.

---

# Validation Architecture

The repository is intended to evolve toward programmatic validation.

Validation will include the following categories.

## Structural Validation

Validates:

* Process Context structure;
* permitted decomposition paths;
* parent and child relationships;
* level integrity;
* orphan elements; and
* invalid hierarchy transitions.

---

## Semantic Validation

Validates whether an element satisfies the criteria associated with its declared type and level.

For example, an L2 Business Process must satisfy the normative Business Process criteria.

---

## Naming Validation

Validates naming conventions appropriate to the process level and concept type.

Naming conventions will be designed to ensure:

* semantic clarity;
* grammatical consistency;
* level consistency;
* avoidance of unnecessary synonym duplication; and
* stable terminology.

---

## Boundary Validation

Validates:

* inclusion;
* exclusion;
* adjacency;
* duplicate responsibility; and
* canonical placement.

---

## MECE Validation

Validates process completeness and non-overlap:

* within a Process Context;
* within an Enterprise Domain;
* within a Lifecycle Stage;
* across the ECF matrix; and
* within every decomposition hierarchy.

---

## Referential Integrity Validation

Validates that references from other OpenDEA repositories resolve to valid canonical process identifiers and compatible process levels.

---

# Repository Evolution

The Business Process Catalog will evolve incrementally.

The initial priority is not the rapid population of process entries.

The initial priority is the establishment of a sound conceptual, architectural and validation foundation.

The evolution sequence is:

## Phase 0: Structural Reconnaissance

Establish the current state of:

* the OpenDEA Metaframework;
* the Enterprise Concept Framework;
* the OpenDEA Metamodel;
* the Business Process Catalog;
* existing process definitions;
* existing relationships; and
* existing schema and validation mechanisms.

Identify structural inconsistencies, semantic gaps and required architectural decisions.

---

## Phase 1: Canonical Process Foundation

Establish:

* Process Context semantics;
* Business Process semantics;
* Function and Process boundaries;
* decomposition semantics;
* level definitions;
* naming conventions;
* canonical identity; and
* validation principles.

---

## Phase 2: Foundational Alignment

Assess the Process Architecture against the normative OpenDEA Metamodel.

Where necessary:

* define a Change Request;
* evolve the metamodel;
* update derived schemas;
* establish conformance rules; and
* update the catalog architecture.

---

## Phase 3: ECF Process Matrix

Establish the authoritative Process Context matrix.

For every Domain × Lifecycle intersection, define:

* Process Context;
* Cell Charter;
* scope;
* exclusions;
* coverage concerns;
* adjacent boundaries; and
* candidate process evidence.

---

## Phase 4: L0 Discovery

Identify the canonical L0 process scopes for each Process Context.

Each L0 candidate must be evaluated for:

* semantic validity;
* contextual fit;
* unique contribution;
* boundary clarity; and
* MECE compliance.

Process discovery proceeds systematically through the ECF matrix.

---

## Phase 5: Controlled Decomposition

Once the L0 architecture is stable:

```text
L0
↓
L1
↓
L2
↓
L3
↓
L4
```

Each decomposition is validated before subsequent levels are introduced.

---

## Phase 6: Programmatic Validation

Implement machine-readable validation for:

* topology;
* semantic criteria;
* naming;
* boundaries;
* MECE;
* decomposition;
* canonical identity; and
* referential integrity.

---

# Governance and Architectural Decisions

Architectural and semantic decisions that materially affect the Business Process Architecture must be recorded and governed.

Examples include:

* the definition of Process Context;
* the normative meaning of each decomposition level;
* the distinction between Function and Process;
* the decomposition stopping rule;
* canonical identity conventions;
* MECE validation criteria; and
* cross-repository process relationships.

Where a decision affects the normative OpenDEA semantic model, it must be progressed through the appropriate OpenDEA Change Request process.

The catalog must remain aligned with the normative model as it evolves.

---

# Current Change Programme

The Business Process catalog is governed by a sequence of Change
Requests (CRs). Each CR lands verbatim and is reviewed before
merge.

| CR | Title | Status | Scope |
|---|---|---|---|
| [CR-BP-01](change-requests/CR-BP-01.md) | Process Semantic Baseline | **Superseded** by CR-BP-SPEC-BP-01 | Original (wrong-premise) implementation; assumed `dea:BusinessProcess` was the sole canonical Process identity. Reverted. |
| [CR-BP-SPEC-BP-01](change-requests/CR-BP-SPEC-BP-01.md) | Business Process Specialization Catalog | **Merged** (PR #12) | Re-anchors the catalog on the **kernel + specializations** discipline (CR-MM-PROC-01; CR-AR-FMWK-01; WSF). Pointer declares both `dea:BusinessProcess` (specialization) and `dea:entity-process` (kernel). New validator enforces `BP-SPEC-01-001..007`. |
| [CR-BP-02](change-requests/CR-BP-02.md) | Establish Process Context | **Merged** (PR #14) | Establishes the **Process Context register + Cell Charter schema** on top of the kernel + specialization tranche. Each context is `Domain x Lifecycle Stage` with a Cell Charter. PC-001..PC-008 validator. Matrix empty by design (CR-BP-02 §22). |
| [CR-BP-03](change-requests/CR-BP-03-business-process-architecture.md) | Business Process Architecture | **Merged** (PR #15) | Establishes the **4-axis classification** (intent / type / specialization / audience) with no breaking changes. Introduces `process_type` (5-value Mintzberg vocabulary) + `process_specialization` (inheritance / pattern-based refinement). Refines the L0/L1/L2 hierarchy as a **conceptual model** (not separate top-level directories). Introduces the **process-identity contract** (verb + object + outcome_statement + evidence_links) and **contribution-driven re-landscape**. |
| [CR-BP-03A](change-requests/CR-BP-03A-legacy-migration.md) | Legacy Field Migration | **Merged** (PR #16) | Corrects the CR-BP-03 schema: `relationships` shape fixed to array-of-relationship-instances; `parent_process` / `child_processes` removed; `capabilities_delivered` soft-deprecated. BP-MIG-001..005 validator. |
| [CR-BP-03C](change-requests/CR-BP-03C-sample-process-contribution.md) | Sample Business Process Contribution | **Merged** (PR #17) | Lands the first Business Process entry (`dea:process-manage-customer-relationship`) walking the full contribution flow end-to-end. |
| [CR-BP-11](change-requests/CR-BP-11-l1-process-group-discovery.md) | L1 Process Group Discovery Across the 49 ECF Coordinates | **Merged** (PR #18) | Research register only: 49-coordinate disposition (38 accepted, 11 deferred). No canonical L1 records; Process Group remains catalog-owned. |
| [CR-BP-04](change-requests/CR-BP-04-id-family-reconciliation.md) | Business Process Identity and ID-Family Reconciliation | **Merged** (PR #19) | Locks the four canonical ID families (`dea:process-*`, `dea:pc-*`, `dea:group-*`, `dea:scope-*`) plus the legacy `dea:bp:*` family. Documentation-first; no schema, validator, or entity change. |
| [CR-BP-12](change-requests/CR-BP-12-process-group-profile.md) | L1 Process Group Profile, Schema, and Validator | **Merged** (PR #20) | First-class catalog-owned Process Group record type; PG-001..PG-008 validator; per-file schema dispatch in CI. |
| [CR-BP-13](change-requests/CR-BP-13-research-ratification.md) | L1 Process Group Research Ratification | **Merged** (PR #22) | Ratifies the 49-coordinate register: 38 `ratified-accepted`, 11 `backlog-deferred`. Idempotent ratification tool `tools/ratify_research_register.py`. |
| [CR-BP-13a](change-requests/CR-BP-13a-customer-and-demand-admission.md) | PartyAndRelationship Admission Tranche | **Merged** (PR #23) | 16 canonical entries across 4 PartyAndRelationship coordinates (Process Context cells, Process Groups, L2 Processes). |
| [CR-BP-13b](change-requests/CR-BP-13b-governance-and-existence-admission.md) | GovernanceAndExistence Admission Tranche | **Merged** (PR #24) | 19 canonical entries across 5 GovernanceAndExistence coordinates (Process Context cells, Process Groups, L2 Processes). |
| [CR-BP-14](change-requests/CR-BP-14-process-semantic-reconciliation.md) | Process Semantic Reconciliation | **Implemented** (landing PR #25; Phase 1 PR #26; Phase 2 PR #28; Phase 3 PR #29; Phase 4 PR #30) | Semantic reconciliation gate: separates Context / Scope / Group / Process / Intent / Classification / Specialization / Relationships; replaces the three-value `process_intent` vocabulary with the seven-value purpose-oriented vocabulary (govern / manage / operate / deliver / support / develop / transform); `process_audience` becomes a legacy migration alias; validators BP-SEM-001..012; canonical admission freeze until implemented. Precedes CR-BP-15 (catalog reconciliation). |
| [CR-BP-15](change-requests/CR-BP-15-process-catalog-reconciliation.md) | Process Catalog Reconciliation | **Implemented** (CR-BP-15-IMP PRs #31-#38; Phase 20 governance approval **closed** by CR-BP-25, 2026-09-09) | Reconciles all existing canonical records against the CR-BP-14 contract; one primary disposition per record (RETAIN / RENAME / RECLASSIFY / RECONTEXTUALIZE / RESPECIALIZE / MERGE / SPLIT / MOVE / DEFER / RETIRE) with full provenance. Reconciliation register + matrix + BP-REC-001..015 gate + repository status model + standard admission gate. |
| [CR-BP-16](change-requests/CR-BP-16-process-catalog-conformance-gate.md) | Process Catalog Conformance Gate (with CR-BP-15-IMP) | **Implemented** (PRs #38-#42; gate live in CI) | CR-BP-15-IMP: 20-phase implementation programme for CR-BP-15. CR-BP-16: the permanent conformance gate (five conformance dimensions, change-type gates, admission gate, CI pipeline, conformance levels L0-L4, regression detection, quality dashboard). Canonical status = conformance + governance approval. |
| [CR-BP-17](change-requests/CR-BP-17-ecf-domain-enum-migration.md) | ECF Domain Enum v2.3.0 Migration | **Merged** (PR #44) | Carries CR-ECF-006 + ADR-ECF-001 into the catalog: five Domains renamed; one replaced. 109 files re-keyed. |
| [CR-BP-18](change-requests/CR-BP-18-ecf-domain-enum-agency-migration.md) | ECF Domain Enum v2.4.0 Migration | **Merged** (PR #45) | Domain 3 rename `PeopleAndOrganization` -> `AgencyAndOrganization` per CR-ECF-007 + ADR-ECF-002. |
| [CR-BP-19](change-requests/CR-BP-19-l1-register-rederivation-ecf-v240.md) | L1 Register Re-derivation (ECF v2.4.0) | **Merged** (PR #46) | Register v2: 35 ratified-accepted / 14 backlog-deferred. Supersedes v1 (38/11). |
| [CR-BP-20](change-requests/CR-BP-20-l1-l2-alignment-ecf-v240.md) | L1/L2 Alignment to Register v2 | **Merged** (PR #47) | Aligns existing L1/L2 records to register v2 after the v2.3.0/v2.4.0 migrations. |
| [CR-BP-21 series](change-requests/README.md) | Seven-Domain Landing (21a..21e + 21a.1..21f.1) | **Merged** (PRs #48-#60) | Lands all 35 ratified coordinates: 5 admission tranches + 6 domain-completion tranches. Register audit closes at 35 landed / 0 pending / 14 deferred. |
| [CR-BP-22](change-requests/CR-BP-22-register-audit-status.md) | Register Audit-Status Reconciliation | **Merged** (PR #50) | Adds the `audit_status` axis (landed / ratified-pending-landing / backlog-deferred) orthogonal to `disposition`. |
| [CR-BP-23](change-requests/CR-BP-23.md) | ECF Domain Enum v2.5.0 Migration | **Merged** (PR #61) | Domain 6 rename `OperationsAndEnablement` -> `EnablementAndOperations` per CR-ECF-008 + ADR-ECF-003. 129 files re-keyed. |
| [CR-BP-24](change-requests/CR-BP-24-programme-closure-reconciliation.md) | Programme Closure Reconciliation | **Merged** (PR #62) | Reconciles tracking artifacts (tranche plan, CR indexes, versioning doc) with catalog reality at programme closure. No entity or schema change. |
| [CR-BP-25](change-requests/CR-BP-25-phase-20-governance-review.md) | Phase 20 Governance Review (CR-BP-15 closure) | **Merged** (PR #63) | Closes the Phase 20 governance gate on CR-BP-15 §22. Records the review (196/196 conformance L4, 35/0/14 register audit, 0 findings, 5-of-5 criteria met). Unblocks the first release cut per `docs/versioning.md`. No entity, schema, or validator change. |
| [CR-BP-26](change-requests/CR-BP-26.md) | First Release Cut (v0.1.0) | **Merged** (PR #64) | Converts the CHANGELOG to a `v0.1.0` snapshot, authors `CITATION.cff`, transitions `docs/versioning.md` to post-release. Tag + GitHub release are post-merge on `main`. |
| [CR-BP-28](change-requests/CR-BP-28.md) | Register v4 Re-derivation (ECF v2.5.0) | **Merged** (PR #65) | Re-derives the register against ECF v2.5.0 as `version: 4`. No-op for the disposition axis: the v2.5.0 transition was a label-only rename of Domain 6; 35 / 0 / 14 audit unchanged. Bookkeeping-grade slice; carries v0.2.0 release candidate. |
| [CR-BP-29](change-requests/CR-BP-29.md) | Second Release Cut (v0.2.0) | **Merged** (PR #66) | Carrier CR for v0.2.0 release cut. CHANGELOG `[Unreleased]` -> `[v0.2.0] - 2026-09-09` (carries CR-BP-28's v4 ratification); `CITATION.cff` version bumped; `docs/versioning.md` bump-table extended. No entity, schema, or validator change. Tag + GitHub release are post-merge on `main`. |
| [CR-BP-32](change-requests/CR-BP-32-activity-model.md) | Activity Model Validators (ACT-001..010) | **Merged** (PR #74) | First execution slice of Phase 3. Codifies CR-BP-32 §15 as ten machine-testable rules (ACT-001..010). New `scripts/check_activity_model.py` + 34 tests; new `schemas/entities/activity.schema.json`; `metamodel-pointer.yaml` registers `dea:Activity` additively. Wired into gate **[15] Activity Model** (advisory). 0 findings by construction (type-discriminator filter). Forward-looking regression guard for the first Activity contribution. Activity is catalog-owned (mirrors `dea:ProcessGroup`). |
| [CR-BP-33](change-requests/CR-BP-33-execution-boundary.md) | Execution Boundary Validators (EXE-001..010) | **Merged** (PR #75) | First execution slice of Phase 4. Codifies CR-BP-33 §15 as ten machine-testable rules (EXE-001..010). New `scripts/check_execution_boundary.py` + 32 tests; `metamodel-pointer.yaml` references `dea:Workflow` / `dea:Task` additively from the dea-metamodel registry. Wired into gate **[16] Execution Boundary** (advisory). 161 records checked, 0 opted-in, 0 findings. Forward-looking regression guard for the first Workflow / Execution contribution. Workflow / Task remain metamodel-owned. |
| [CR-BP-36](change-requests/CR-BP-36-mece-validation.md) | MECE Validation (MECE-001..008) | **Merged** (PR #76) | First execution slice of Phase 5. Codifies catalog-wide MECE as eight machine-testable rules (MECE-001..008); coordinate-based matching bridges the legacy full-word vs abbreviated PC id convention drift. New `scripts/check_mece.py` + 23 tests. Wired into gate **[17] MECE Validation** (advisory). Pre-slice run found 1 MECE-008 violation (`dea:process-secure-funding-facilities`); remediated in-slice. Post-remediation: 0 findings. Deprecated records correctly exempt from MECE-008. |
| [CR-BP-35](change-requests/CR-BP-35-process-catalog-architecture.md) | Process Catalog Architecture Retrospective | **Merged** (PR #77) | Second execution slice of Phase 5. Documentation-only retrospective of the architecture as it has actually landed in `main`. Surfaces four deltas from the original CR-BP-07 framing (landing-order inversion, L0..L4 conformance levels, kernel + specialization discipline, validator library). Documents eight-slot decomposition, six characterization dimensions, cross-repo contracts, ECF version history. No validator, no schema, no record mutation. |
| [CR-BP-37](change-requests/CR-BP-37-cross-repo-integrity.md) | Cross-Repository Integrity (XRI-001..005) | **Merged** (PR #78) | Third execution slice of Phase 5. Documents the catalog's cross-repo surface (canonical lineage: CR-MM-PROC-01 / CR-AR-FMWK-01; ECF conformance: CR-ECF-CG-001..004 + CR-ECF-006/007/008; companion catalogs: CR-BC-ECF-03 / CR-BO-02 / CR-OU-02; WSF: wsf:Process) and codifies five invariants (XRI-001..005). New `scripts/check_cross_repo_integrity.py` + 23 tests; runtime asset (NOT a CI gate). 0 findings on the live catalog. |
| [CR-BP-38](change-requests/CR-BP-38-ecf-matrix-population-retrospective.md) | ECF Matrix Population Retrospective | **Merged** (PR #79) | Tenth and final execution slice of the BP-32/33/34 tranche plan; fourth and last slice of Phase 5. Documentation-only retrospective of how the ECF matrix (7 domains × 7 stages = 49 coordinates) was discovered, ratified, and populated through 11 CR tranches (CR-BP-11, -12, -13, -14, -17, -18, -19, -21a-f + a.1/b.1/c.1/d.1/e.1, -22, -23, -28). Current state: 35 ratified + 14 backlog-deferred = 49 coordinates; 162 PGs, 36 PCs, 161 BPs at L4 conformance. Closes the tranche plan. |
| [CR-BP-39](change-requests/CR-BP-39-changelog-readme-reconciliation.md) | CHANGELOG + README + docs Reconciliation | **Merged** (PR #80) | First post-tranche slice. Reconciles tracking artifacts (`CHANGELOG.md`, root `README.md`, `change-requests/README.md`) with `main` at `e371cff6` after the BP-32/33/34 tranche plan closure. Adds 7 missing `[Unreleased]` CHANGELOG entries; corrects stale "Proposed (this PR)" status rows in both READMEs. No entity, schema, validator, or gate change. |
| [CR-BP-40](change-requests/CR-BP-40-xri-gate-promotion.md) | Cross-Repository Integrity Gate Promotion (XRI-001..005 → Gate [18]) | **Merged** (PR #81) | Second post-tranche slice. Promotes `scripts/check_cross_repo_integrity.py` (the CR-BP-37 runtime asset) to a conformance gate wired into `scripts/conformance_result.py` as gate **[18] Cross-Repository Integrity (XRI-001..005)** (advisory; non-blocking). Adds one entry to the GATES list; runtime asset is unchanged. Repo totals post-slice: 23 conformance gates (was 22); 10 blocking + 13 advisory. No entity, schema, validator-rule, or canonical-record change. |
| [CR-BP-41](change-requests/CR-BP-41-v030-release-cut.md) | Third Release Cut (v0.3.0) | **Proposed (this PR)** | Third post-tranche slice. Cuts the v0.3.0 git tag at `main @ 254678e6` (post-#81). Captures the entire post-v0.1.0 work as a single versioned snapshot: ECF v2.3.0/v2.4.0/v2.5.0 cascade; BP-32/33/34 tranche plan; XRI asset + gate promotion; CHANGELOG + README reconciliation. New `## [v0.3.0] - 2026-09-12` CHANGELOG section; `CITATION.cff` bumped `0.2.0 → 0.3.0`; `docs/versioning.md` bump table extended. Tag push + GitHub release are post-merge on `main`. 17 commits since v0.1.0; 23 conformance gates (10 blocking + 13 advisory). |

---

# Conformance Principle

The process catalog does **not** create a parallel enterprise
ontology. It profiles and catalogs canonical OpenDEA entities
within an explicit process architecture while preserving the
separation between:

- enterprise context;
- process structure;
- process semantics;
- capability realization;
- organizational responsibility;
- process behaviour;
- execution.

A Business Process catalog entry is a **catalog profile of
`dea:BusinessProcess`**, not a new foundational entity. The
catalog can classify a process by `process_type` (the 5-value
Mintzberg vocabulary), but the classification does not promote
to a new metamodel entity.

The four axes (intent / type / specialization / audience) operate
independently: each captures a distinct concern, and a single
Business Process can have any combination of values across the
four axes.

The re-landscape mechanism is **contribution-driven** and
**human-reviewed**: the catalog does not auto-rewrite. The CI
contribution report workflow surfaces a reclassification
recommendation, and a catalog maintainer decides.

---

# Design Principles

The Business Process Catalog is governed by the following principles.

## Context Before Classification

Understand the Domain × Lifecycle intersection before identifying processes.

## Meaning Before Naming

A process name must follow semantic analysis.

It must not be produced through terminology combination.

## Established Before Invented

Prefer established and recognisable business process concepts over artificial terminology.

## Boundary Before Decomposition

Define what a process includes and excludes before decomposing it.

## One Canonical Home

Every canonical process element has one authoritative conceptual location.

## Many Valid Relationships

A process may participate in multiple enterprise relationships without being duplicated.

## MECE by Design

Completeness and non-overlap must be considered throughout the architecture, not only during final review.

## Metamodel First

The Business Process Catalog must align with the normative OpenDEA Metamodel.

## Machine-Testable Where Possible

Semantic, structural and validation rules should progressively become machine-readable and executable.

## Controlled Evolution

The architecture may evolve, but foundational changes must be explicit, governed and traceable.

---

# Current Status

The repository is undergoing architectural inception and evolution.

The current focus is to establish the canonical Business Process Architecture before substantial catalog population.

Current work includes:

* reconciliation of existing Process definitions;
* alignment with the normative OpenDEA Metamodel;
* definition of Process Context;
* analysis of decomposition semantics;
* clarification of Business Function and Business Process boundaries;
* definition of MECE validation scopes; and
* design of the future validation architecture.

No substantial process population should be considered authoritative until the foundational architecture and normative alignment have been established.

---

# Intended Outcome

The intended outcome is an authoritative OpenDEA Business Process Architecture and Catalog that provides:

* holistic enterprise process coverage;
* rigorous Domain × Lifecycle contextual organization;
* controlled process decomposition;
* explicit semantic boundaries;
* MECE validation;
* stable canonical identity;
* machine-readable representation;
* cross-repository referential integrity; and
* a durable foundation for process modelling, workflow derivation, automation, autonomous operations, AI and agentic systems.

# ECF Conformance

The catalog declares its ECF conformance posture through the `ecfConformance` block on each canonical entry (when populated; Phase 2 deferred) and through this repository-level declaration.

**Profile**: `dea:ecf@1.0.0`. **Status**: CONFORMANT-WITH-EXTENSION (CG-001 §4). The catalog specializes ECF semantics for its own methodology (the Process Context interpretation of an ECF Coordinate; the L0-L4 decomposition rules; the `process_audience` single-axis audience classification). The extensions do not redefine any ECF Domain, Stage, or Coordinate.

**Governance decision (CG-004 §10)**: the existing `process_audience` field is a single-axis audience classification; it is **not** an ECF Domain. Both use the same kebab-case vocabulary by coincidence of display labelling. The conformance gate (`scripts/check_ecf_conformance.py`) rejects any canonical reference that uses a kebab-case value in the Domain slot; canonical references must use PascalCase enum values (`GovernanceAndExistence` etc.). See `docs/governance/process-audience-vs-ecf-domain.md` for the full decision record.

**Conformance gate**: `scripts/check_ecf_conformance.py`. The script reports PASS when `entities/` is empty (Phase 2 deferred); when entries appear, it validates each block against the canonical contract.

**ECF Conformance CI (consumer side)**: `.github/workflows/ecf-conformance-consumer.yml` (CR-ECF-CG-006). On every PR and push to `main`, the workflow clones `dea-metamodel` and `dea-metaframework`, then runs `scripts/detect_drift.py` from the metamodel against this catalog. The metamodel-side workflow owns the consolidated conformance report; this hook owns the per-consumer drift verdict.

The Business Process Catalog is therefore intended to become a foundational component of the OpenDEA ecosystem through which business process knowledge can be consistently defined, validated, reused and evolved.

> **The objective is not to create the largest catalog of processes.**
>
> **The objective is to establish the most coherent, grounded and structurally reliable process architecture from which the enterprise process landscape can be systematically derived.**

# Sample entry

The catalog's **first** Business Process entry —
`dea:process-manage-customer-relationship` ("Manage Customer
Relationship"): lands with this tranche (CR-BP-03C). It
exercises every part of the machinery: 4-axis
classification, identity contract, canonical relationships,
L0/L1/L2 conceptual hierarchy, Process Context reference,
and ECF Conformance Gate. Future contributors should
**pattern-match against this entry**.

See [`docs/examples/manage-customer-relationship.md`](docs/examples/manage-customer-relationship.md)
for the full walk-through.

# Contributing a new Business Process entry

To contribute a new Business Process entry:

1. Read [`docs/architecture.md`](docs/architecture.md),
   [`docs/classification.md`](docs/classification.md),
   [`docs/identity.md`](docs/identity.md),
   [`docs/relandscape.md`](docs/relandscape.md).
2. **Pattern-match against
   [`docs/examples/manage-customer-relationship.md`](docs/examples/manage-customer-relationship.md)**.
3. Copy
   [`contributions/processes/PROCESS-CONTRIBUTION-TEMPLATE.yaml`](contributions/processes/PROCESS-CONTRIBUTION-TEMPLATE.yaml)
   to `contributions/processes/<your-id>.yaml` and fill in
   the proposed_entry.
4. Run the validators locally:
   `python scripts/check_process_identity.py`,
   `python scripts/check_legacy_migration.py`,
   `python scripts/check_ecf_conformance.py`.
5. Open a PR. The Process Contribution Report workflow will
   generate a reclassification recommendation and post it
   as a PR comment.
6. A catalog maintainer reviews the contribution and either
   accepts, requests re-landscape, or rejects.

See [`docs/examples/README.md`](docs/examples/README.md)
for the full contributor guide.
