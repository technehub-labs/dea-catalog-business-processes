Agreed. The recon shows that the repository is architecturally mature enough that the next CR should be a reconciliation contract, not another feature CR. In particular, the current repository still explicitly defines four axes where process_intent and process_type overlap semantically, while process_audience is modeled as an intrinsic classification even though the ECF Context is the stronger architectural relationship. 

I would therefore establish the following as CR-BP-14, with the CR itself becoming the normative bridge between the existing CR lineage and the subsequent catalog-reconciliation work.

# CR-BP-14 — Process Semantic Reconciliation

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Accepted
**Layer**: L1
**Owner**: TechNeHub Labs
**Type**: Architectural Reconciliation
**Scope**: dea-catalog-processes
**Depends On**: CR-BP-SPEC-BP-01, CR-BP-02, CR-BP-03, CR-BP-03A, CR-BP-03C, CR-BP-11, CR-BP-12, CR-BP-13
Precedes: CR-BP-15, CR-BP-13A and subsequent Process Admission CRs

⸻

1. Purpose

Establish the definitive semantic contract for the OpenDEA Business Process Catalog so that every process can be described, positioned and related without semantic overlap between:

* Process Context
* Process Scope
* Process Group
* Business Process
* Process Intent
* Process Classification
* Process Specialization
* Process relationships

This CR reconciles the architectural evolution established by prior CRs without redefining the OpenDEA Process kernel or introducing new ontology entities.

The objective is to make the Business Process Catalog suitable as a canonical, machine-validatable and independently referenceable Business Process specialization catalog.

⸻

2. Problem Statement

The current catalog architecture is fundamentally sound, but successive CRs introduced several concepts at different stages of architectural maturity.

The current four-axis model defines:

Axis	Current field	Current purpose
Intent	process_intent	Nature of work
Type	process_type	Position in process landscape
Specialization	process_specialization	Refinement of another process
Audience	process_audience	ECF domain served

The distinction is directionally correct, but the current vocabulary creates semantic overlap.

In particular:

1. process_intent and process_type both contain concepts such as management and support.
2. process_audience behaves more like a relationship to enterprise context than an intrinsic property of process identity.
3. Process Context and Audience can be confused even though Context is a Domain × Lifecycle construct.
4. The repository documentation contains historical terminology that predates the kernel/specialization architecture.
5. The catalog requires an explicit rule distinguishing what a process is, why it exists, where it is positioned, and what it specializes.
6. Existing process entries must be reconciled before further admission tranches multiply the inconsistency.

The repository currently identifies the Business Process as the L2 semantic level, with Process Scope and Process Group serving as conceptual L0/L1 topology constructs. This CR preserves that architecture.

⸻

3. Architectural Decision

The Business Process Catalog SHALL use the following semantic separation:

Process Context establishes where enterprise process responsibility is being examined. Process Scope and Process Group establish architectural organization. Business Process identifies a coherent unit of enterprise work. Process Intent describes why that work exists in terms of its work purpose. Process Classification describes how that process is positioned in the enterprise process landscape. Process Specialization describes what more general process it refines.

These concepts SHALL NOT be treated as interchangeable.

⸻

4. Definitive Process Architecture

The canonical architecture is:

Enterprise Concept Framework
        │
        │ Domain × Lifecycle Stage
        ▼
Process Context
        │
        ▼
L0 — Process Scope
        │
        ▼
L1 — Process Group
        │
        ▼
L2 — Business Process
        │
        ├───────────────┐
        │               │
        ▼               ▼
Process Intent    Process Classification
        │
        ▼
Process Specialization
        │
        ▼
Process Relationships

The decomposition hierarchy and process characterization dimensions are separate concerns.

⸻

5. Process Context

5.1 Definition

A Process Context is the semantic boundary established by:

ECF Domain × Lifecycle Stage

It establishes the enterprise concern and lifecycle concern within which processes are identified and evaluated.

A Process Context is not itself:

* a Business Process;
* a Process Group;
* a Business Function;
* a Business Capability;
* a process classification;
* a process intent.

5.2 Normative Rule

An ECF intersection SHALL NOT generate a process automatically.

The catalog SHALL continue to enforce:

ECF provides context; Process Architecture provides process structure.

⸻

6. Process Scope — L0

Process Scope is the highest catalog topology construct within a Process Context.

It answers:

What coherent enterprise responsibility is being organized within this context?

Process Scope SHALL:

* establish a stable semantic boundary;
* organize related process responsibilities;
* avoid sibling overlap;
* provide a basis for Process Group decomposition.

Process Scope SHALL NOT be treated as a Business Process.

⸻

7. Process Group — L1

Process Group organizes related Business Processes within a Process Scope.

It answers:

How are related process responsibilities grouped within the process architecture?

Process Group SHALL:

* have a coherent grouping rationale;
* have a distinct boundary;
* organize one or more lower-level process responsibilities;
* support systematic decomposition.

Process Group SHALL NOT be interpreted as:

* Business Function;
* Business Capability;
* Process Intent;
* Process Classification;
* Business Process.

The catalog may maintain Process Group as a catalog construct without asserting it as a new OpenDEA metamodel entity.

⸻

8. Business Process — L2

Business Process is the canonical semantic process element of this catalog specialization.

It answers:

What coherent unit of enterprise work is performed?

A Business Process SHALL represent a bounded unit of work that:

1. transforms defined inputs into outputs;
2. contributes distinctly to an enterprise objective;
3. can be understood as a coherent unit of work;
4. has identifiable responsibility for the resources, capabilities, roles or means required for execution.

An element failing these criteria SHALL be considered for classification as another concept or decomposition level.

Possible alternatives include:

* Process Group;
* Activity;
* Task;
* Business Function;
* Business Capability;
* another OpenDEA concept.

⸻

9. Process Intent

9.1 Definition

Process Intent describes the purposeful nature of the work performed by the process.

It answers:

Why does this work exist in terms of the kind of enterprise work it performs?

Process Intent SHALL describe the work purpose rather than the organizational location of the process.

9.2 Definitive Vocabulary

The initial controlled vocabulary SHALL be:

Intent	Definition
govern	Establish, direct, assure or enforce enterprise direction, policy, authority or compliance
manage	Plan, coordinate, monitor, control or optimize an enterprise responsibility
operate	Perform recurring enterprise work that produces or maintains an operational result
deliver	Produce, provision or transfer an intended product, service, experience or outcome
support	Enable other enterprise responsibilities through internal services or resources
develop	Create, improve or evolve an enterprise asset, offering, capability or outcome
transform	Change an existing enterprise state, capability, model or operating condition

This vocabulary is intentionally purpose-oriented.

It SHALL NOT be derived from organizational position.

⸻

10. Process Classification

10.1 Definition

Process Classification describes the position of a Business Process within the enterprise process landscape.

It answers:

How is this process positioned within the enterprise’s process architecture?

Classification SHALL NOT describe the work’s intrinsic purpose.

10.2 Definitive Vocabulary

The existing five-value landscape classification SHALL be retained:

Classification	Meaning
strategic	Enterprise direction, strategic decisions and strategic outcomes
management	Coordination and control of enterprise responsibilities and resources
core	Direct contribution to externally realized enterprise value
support	Internal enablement of enterprise operations
standardization	Cross-cutting consistency, assurance, compliance or improvement

The classification vocabulary remains catalog-controlled.

It does not create corresponding OpenDEA ontology entities.

⸻

11. Intent ≠ Classification

The following distinction is normative:

Process Intent
    = nature / purpose of the work
Process Classification
    = architectural position of the process

Therefore combinations such as the following are valid:

Process	Intent	Classification
Manage Customer Relationship	manage	core
Manage Workforce	manage	support
Govern Enterprise Risk	govern	strategic
Operate Service Platform	operate	core
Manage Service Quality	manage	standardization
Develop Product Offering	develop	core

No classification value SHALL be used merely because its lexical form resembles the process intent.

The fact that a process is management classified does not imply that its intent must be manage, and the fact that its intent is support does not imply that its classification must be support.

⸻

12. Process Specialization

12.1 Definition

Process Specialization expresses semantic refinement of another process.

It answers:

What more general process does this process refine?

Example:

Manage Customer Relationship
        │
        ├── Manage Enterprise Customer Relationship
        ├── Manage Consumer Customer Relationship
        └── Manage Partner Customer Relationship

The specialized process inherits the semantic pattern of the parent while introducing a materially distinguishing scope, subject, regime or context.

12.2 Specialization Requirements

A specialization SHALL identify:

* the parent process;
* the specialization basis;
* the distinguishing semantic property.

Valid specialization bases may include:

* customer segment;
* geography;
* product;
* service;
* channel;
* regulatory regime;
* operating model;
* lifecycle condition;
* organizational context.

The catalog SHALL reject specialization relationships that merely rename the parent without introducing a meaningful semantic distinction.

⸻

13. Process Context Relationship

A Business Process SHALL NOT use process_audience as a substitute for Process Context.

The distinction is:

Process Context
    Domain × Lifecycle Stage
    = where the process responsibility is examined
Process Relationship
    serves / contributes-to / operates-within
    = how the process relates to enterprise context

The existing process_audience concept SHALL therefore be treated as a legacy catalog classification pending migration.

For new canonical entries, contextual relationships SHALL be preferred.

The target representation is:

relationships:
  - relationship_type: serves
    target: <ecf-domain>

Where lifecycle-specific placement is required:

context:
  - ref: <process-context-id>

A process MAY relate to multiple contexts.

A process MUST NOT be forced into a single audience merely because it participates in more than one enterprise concern.

⸻

14. Canonical Process Characterization

The canonical characterization of a Business Process SHALL therefore be:

Business Process
│
├── Identity
│
├── Intent
│
├── Classification
│
├── Specialization
│
├── Context
│
└── Relationships

These dimensions have distinct responsibilities:

Dimension	Question
Identity	What coherent process is this?
Intent	What kind of purposeful work does it perform?
Classification	Where is it positioned in the process landscape?
Specialization	What general process does it refine?
Context	Within what enterprise context is it defined or used?
Relationships	What enterprise concepts does it interact with or serve?

⸻

15. Identity Independence

Process identity SHALL NOT depend upon:

* Process Intent;
* Process Classification;
* Process Audience;
* Process Context;
* organizational ownership.

Identity SHALL continue to be established through the existing identity contract:

Verb
+
Object
+
Optional Scope
+
Trigger
+
Outcome
+
Evidence

Classification and contextual information may change without necessarily creating a new Process identity.

A semantic change to the process itself may require a new identity or specialization.

⸻

16. Naming Contract

Business Process names SHALL follow:

<Verb> <Object> [<Scope>]

Examples:

Manage Customer Relationship
Develop Product Offering
Operate Service Platform
Govern Enterprise Risk
Deliver Customer Service
Support Workforce

Names SHALL:

* use an imperative action verb;
* identify the principal object of the action;
* optionally identify a meaningful scope;
* avoid organizational department names;
* avoid lifecycle-stage names unless semantically necessary;
* avoid ECF cell names;
* avoid classification vocabulary as a substitute for process meaning.

The ECF matrix SHALL never be used as a mechanical process-name generator.

⸻

17. Migration of Existing process_intent

Existing entries using:

process_intent:
  - operational
  - support
  - management

SHALL be migrated to the new semantic vocabulary.

The mapping SHALL be evidence-based.

Initial migration guidance:

Existing	Candidate New Intent
operational	operate or deliver
support	support
management	manage or govern

The mapping MUST NOT be performed mechanically where the process meaning indicates another intent.

For example:

Govern Enterprise Risk

should become:

process_intent: govern

rather than:

process_intent: manage

when governance is the defining purpose.

⸻

18. Migration of process_type

process_type SHALL remain as the enterprise landscape classification.

No semantic replacement is required.

However:

1. process_type SHALL no longer be described as a synonym for process intent.
2. process_type SHALL not determine process_intent.
3. process_intent SHALL not determine process_type.
4. Validation MAY identify implausible combinations for review but SHALL NOT infer one dimension from the other.

The current default of core SHALL be reviewed as part of CR-BP-15 rather than silently retained as a semantic assumption.

⸻

19. Migration of process_audience

Existing:

process_audience:

entries SHALL remain readable during migration.

However:

* new entries SHOULD use Process Context and relationship semantics;
* process_audience SHALL be marked as a migration alias;
* the catalog SHALL provide a deterministic migration validator;
* removal SHALL occur only after all canonical entries have migrated.

This prevents a breaking migration while eliminating the conceptual ambiguity.

⸻

20. Schema Changes

The implementation SHALL introduce or reconcile schemas so that:

identity:
  ...
process_intent: <controlled vocabulary>
process_classification:
  type: <controlled vocabulary>
process_specialization:
  ...
context:
  ...
relationships:
  ...

The implementation MAY retain:

process_type:
process_audience:

as backward-compatible aliases during the migration period.

However, the documentation SHALL identify the canonical semantic concepts rather than the legacy field names.

Where the existing schema requires preservation of process_type, the implementation SHALL retain the field name until a separately governed schema migration is approved.

⸻

21. Validation Rules

The following rules SHALL be introduced.

BP-SEM-001 — Intent Vocabulary

process_intent MUST contain only an approved intent value.

BP-SEM-002 — Classification Vocabulary

Process classification MUST use the approved landscape vocabulary.

BP-SEM-003 — Intent Independence

Validation MUST NOT infer Process Intent from Process Classification.

BP-SEM-004 — Classification Independence

Validation MUST NOT infer Process Classification from Process Intent.

BP-SEM-005 — Specialization Validity

Every specialization reference MUST resolve to an existing process.

BP-SEM-006 — Specialization Differentiation

A specialized process MUST contain a semantic distinction from its parent.

BP-SEM-007 — Context Distinction

A Process Context MUST NOT be represented solely through process_audience.

BP-SEM-008 — Context Reference Integrity

Every declared Process Context reference MUST resolve to a valid Process Context.

BP-SEM-009 — Identity Independence

Changes to intent, classification or context SHALL NOT automatically create a new process identity.

BP-SEM-010 — Legacy Detection

Legacy process_intent and process_audience forms SHALL generate migration findings.

BP-SEM-011 — Classification Collision

Identical vocabulary appearing in Intent and Classification SHALL NOT be treated as semantic equivalence.

BP-SEM-012 — Context Multiplicity

A Business Process MAY participate in multiple Process Contexts where evidence establishes legitimate cross-context responsibility.

⸻

22. Documentation Reconciliation

The following documents SHALL be reconciled:

README.md
docs/classification.md
docs/architecture.md
docs/identity.md
docs/relandscape.md
schemas/*
classifications/*
change-requests/*

All superseded statements SHALL be removed or explicitly marked historical.

In particular, the repository SHALL no longer contain contradictory descriptions implying:

Business Process = Process Kernel

The definitive statement SHALL remain:

The Business Process Catalog is a specialization catalog of the OpenDEA Process kernel.

⸻

23. CR Register Reconciliation

The CR register SHALL become the authoritative source for implementation status.

README change-programme statements SHALL be synchronized with the actual CR status.

Historical status SHALL NOT be presented as current status.

The implementation SHALL establish a clear distinction between:

Implemented
Accepted
Proposed
Deferred
Superseded
Retired

⸻

24. Catalog Population Freeze

Until CR-BP-14 is implemented:

No new canonical Business Process admission tranche SHALL be considered architecturally final.

Research and candidate contributions MAY continue.

Canonical admission SHOULD resume only after:

1. semantic vocabulary is reconciled;
2. schemas are updated;
3. validators are implemented;
4. documentation is reconciled;
5. existing entries are assessed.

This does not invalidate CR-BP-13 research.

CR-BP-13 remains the research and ratification baseline.

⸻

25. Conformance Matrix

Every canonical Business Process SHALL ultimately be testable against:

Dimension	Required Question
Identity	Is this a distinct coherent unit of work?
Context	Where is its enterprise responsibility situated?
Scope	Does it belong to the declared architectural boundary?
Intent	What purposeful work does it perform?
Classification	How is it positioned in the enterprise landscape?
Specialization	Does it refine another process?
Boundary	Is its responsibility distinct from siblings?
Evidence	Is there sufficient evidence for admission?
MECE	Does it add unique coverage without creating unacceptable overlap?
Metamodel	Does it conform to the OpenDEA semantic model?

⸻

26. Acceptance Criteria

CR-BP-14 is complete only when all of the following are true.

Architecture

* [ ]	Process Context semantics are explicitly separated from Business Process semantics.
* [ ]	L0/L1/L2/L3/L4 semantics are internally consistent.
* [ ]	Process Group remains a catalog architecture construct and is not incorrectly promoted into the metamodel.
* [ ]	Business Process remains the canonical L2 semantic specialization.

Semantics

* [ ]	Process Intent has an approved controlled vocabulary.
* [ ]	Process Classification has an approved controlled vocabulary.
* [ ]	Intent and Classification have formally distinct semantics.
* [ ]	Process Specialization is explicitly defined as semantic refinement.
* [ ]	Process Context is distinct from Process Audience.
* [ ]	Process relationships are available for contextual participation.

Schema

* [ ]	Canonical schema representation is defined.
* [ ]	Legacy fields remain readable during migration.
* [ ]	Migration aliases are documented.
* [ ]	Referential integrity is validated.

Validation

* [ ]	BP-SEM-001 through BP-SEM-012 are implemented or formally mapped to existing validators.
* [ ]	CI detects semantic collisions.
* [ ]	CI detects unresolved specialization references.
* [ ]	CI detects invalid contexts.
* [ ]	CI reports legacy fields requiring migration.

Documentation

* [ ]	README is reconciled.
* [ ]	docs/classification.md is reconciled.
* [ ]	docs/architecture.md is reconciled.
* [ ]	docs/identity.md is reconciled.
* [ ]	CR status is synchronized.
* [ ]	No superseded semantic contract remains presented as normative.

Governance

* [ ]	Existing canonical entries have been identified for migration.
* [ ]	No new admission tranche is marked final until reconciliation is complete.
* [ ]	CR-BP-15 is established as the follow-on catalog reconciliation activity.

⸻

27. Non-Goals

CR-BP-14 SHALL NOT:

* redefine the OpenDEA Process kernel;
* introduce new OpenDEA ontology entities;
* populate the remaining ECF matrix;
* admit new Business Process tranches;
* perform the complete migration of existing catalog entries;
* redefine Business Capability;
* redefine Business Function;
* define Activities or Tasks;
* establish execution/workflow semantics.

Those concerns remain governed by their respective architectures and future CRs.

⸻

28. Follow-On Work

CR-BP-15 SHALL perform the actual catalog reconciliation.

Its scope SHALL include:

Existing Process Entries
        │
        ▼
Semantic Assessment
        │
        ├── RETAIN
        ├── RECLASSIFY
        ├── RENAME
        ├── SPECIALIZE
        ├── MERGE
        ├── SPLIT
        ├── MOVE
        ├── DEFER
        └── RETIRE

Only after CR-BP-15 has reconciled the existing canonical set should the CR-BP-13 research findings proceed into subsequent admission tranches.

⸻

29. Architectural Principle Established

CR-BP-14 establishes the following definitive rule for the Business Process Catalog:

Context tells us where to look. Scope tells us what responsibility is being organized. Group tells us how related responsibilities are organized. Process tells us what work is performed. Intent tells us why that work exists. Classification tells us how that work is positioned in the enterprise process landscape. Specialization tells us what more general process it refines. Relationships tell us what other enterprise concepts it serves, realizes, depends upon or interacts with.

No one of these concepts SHALL be used as a substitute for another.

⸻

30. Decision

Adopt CR-BP-14 as the semantic reconciliation gate for the OpenDEA Business Process Catalog.

The catalog SHALL remain architecturally open to further specialization and contribution, but canonical process admission SHALL proceed under the reconciled semantic contract established by this CR.

Next CR: CR-BP-15 — Process Catalog Reconciliation

This is deliberately not CR-BP-15 yet. CR-BP-14 establishes the semantic constitution; CR-BP-15 should then be an evidence-driven reconciliation of every existing canonical entry against that constitution. That sequencing avoids baking today’s ambiguities into the Party & Relationship admission tranche. The current repository’s own architecture already gives us the necessary L0–L4 and contribution machinery to execute that cleanly.  

The one change I would treat as particularly important is the shift from the current three-value operational/support/management intent vocabulary to the more orthogonal govern/manage/operate/deliver/support/develop/transform vocabulary. It removes the direct lexical collision with the existing five-value process-landscape classification while preserving the information that the old intent field was trying to express. 

Next step should therefore be implementation decomposition of CR-BP-14 itself, followed by the actual CR-BP-15 reconciliation—not further process admission yet.