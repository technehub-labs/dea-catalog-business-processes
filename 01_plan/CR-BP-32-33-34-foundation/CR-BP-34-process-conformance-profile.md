# CR-BP-34 — Process Conformance Profile

> **Renumbering note.** Authored by eaojnr on 2026-09-10 as "CR-BP-06 — Process Conformance Profile". Renumbered to **CR-BP-34**. The original document contains a stray text fragment ("Pasted markdown.md" in the preamble paragraph and "Pasted markdown.md" after "This is where the original ambition...") — that fragment has been removed on landing as it appears to be a copy-paste artifact in the source document, not authored content.
>
> **Sequence status (same as CR-BP-32).** The user's payload assumes CR-BP-04..06 land BEFORE CR-BP-07 (Catalog Architecture) and the population. Actual landing order is the inverse. CR-BP-34 therefore lands as **additive conformance rules** layered on the existing CR-BP-16 conformance gate.

**Status**: Proposed (carrier CR — knowledge harvest + positioning; awaiting user direction on execution order)
**Layer**: All (cross-cutting conformance profile)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-09-10
**Original author**: eaojnr
**Source document**: `/home/hermes/.hermes/profiles/coder/cache/documents/doc_cf6fc6bb9e80_CR-BP-04_06.md` (lines 873-1578)
**Depends on (logical)**: CR-BP-32 (Activity Model), CR-BP-33 (Execution Boundary)
**Lands against (actual current state)**: CR-BP-16 conformance gate is MERGED. CR-BP-34 rules become **additive** validation rules layered on top of the existing 15-gate suite.

---

This is where the original ambition of making the repository authoritative and programmatically consumable becomes concrete. The attached design explicitly calls for objective, machine-testable validation rather than subjective classification.

CR-BP-34 should establish the conformance contract, but not absorb CR-BP-08's broader MECE validation programme. Conformance asks "is this artifact structurally and semantically valid?"; MECE asks "is the catalog collectively exhaustive and mutually exclusive?"

CR-BP-34 — Process Conformance Profile

Status: Proposed
Type: Conformance / Validation / Semantic Profile
Priority: High
Depends On: CR-BP-01, CR-BP-02, CR-BP-03, CR-BP-32, CR-BP-33
Prepares For: CR-BP-35, CR-BP-36, CR-BP-37, CR-BP-38
Target Repository: technehub-labs/dea-catalog-processes

⸻

1. Change Request

Establish the OpenDEA Business Process Conformance Profile as the normative validation contract for the Business Process Architecture and Reference Catalog.

The profile shall define machine-testable rules for:

* identity;
* structure;
* decomposition;
* semantic classification;
* process qualification;
* activity cohesion;
* task atomicity;
* execution separation;
* OpenDEA metamodel alignment;
* cross-repository references;
* lifecycle and version integrity.

The objective is to ensure that every published process artifact is structurally valid, semantically grounded and interoperable with the wider OpenDEA architecture.

⸻

2. Motivation

The Business Process repository is intended to become an authoritative engineering reference rather than a subjective collection of process names.

The source design explicitly establishes the goal of an authoritative, programmatically consumable representation and calls for objective, machine-testable validation criteria.

Conformance therefore becomes a first-class architectural concern.

Business Process Architecture
            │
            ▼
     Conformance Profile
            │
     ┌──────┼──────┐
     ▼      ▼      ▼
  Identity Structure Semantics
     │      │      │
     └──────┼──────┘
            ▼
        Validation
            │
            ▼
       Published Catalog

⸻

3. Conformance Principle

An artifact shall not be considered authoritative merely because it exists in the repository.

It must satisfy the applicable conformance rules.

Therefore:

Repository Presence
        ≠
Architectural Validity

and:

Architectural Validity
        +
Semantic Conformance
        +
Reference Integrity
        =
Published Process Artifact

⸻

4. Conformance Levels

The process repository shall distinguish the following validation dimensions.

Level A — Identity Conformance

Validates:

* canonical identity;
* identifier format;
* version;
* type;
* authority;
* reference integrity.

Level B — Architectural Conformance

Validates:

* Process Context;
* L0 Process Scope;
* L1 Process Group;
* L2 Business Process;
* L3 Activity;
* L4 Task;
* permitted structural relationships.

Level C — Semantic Conformance

Validates:

* Process Intent;
* Process Specialization;
* Process Classification;
* outcome;
* inputs/outputs;
* capability realization;
* semantic boundaries.

Level D — Decomposition Conformance

Validates:

* L2 Process qualification;
* Activity cohesion;
* Task atomicity;
* decomposition boundary.

Level E — Execution Conformance

Validates:

* separation of structure and execution;
* Workflow references;
* execution relationships;
* implementation boundary.

Level F — Ecosystem Conformance

Validates:

* OpenDEA metamodel references;
* ECF references;
* cross-repository identifiers;
* relationship integrity.

⸻

5. Canonical Identity

Every L2 process shall identify itself as:

type: dea:BusinessProcess

No repository-local equivalent shall become a competing canonical identity.

Legacy identifiers shall be handled through explicit mappings established by CR-BP-01.

⸻

6. Process Conformance Profile

Every Business Process shall have a semantic profile consisting of:

Business Process
│
├── Identity
│
├── Intent
│
├── Specialization
│
├── Classification
│
├── Context
│
├── Outcome
│
├── Inputs / Outputs
│
├── Realization
│
├── Decomposition
│
└── Execution References

⸻

7. Intent Conformance

Process Intent describes why the process exists.

The value shall come from the authoritative controlled vocabulary.

The profile shall prohibit using Process Intent as a substitute for:

* Process Specialization;
* Organizational Component;
* Process Domain;
* ECF Domain;
* Lifecycle Stage.

Rules:

PSP-001 — Intent shall be purposive.

PSP-002 — Intent shall use an approved vocabulary.

PSP-003 — Intent shall not encode organizational ownership.

⸻

8. Specialization Conformance

Process Specialization describes the kind of enterprise process represented.

The initial controlled specialization vocabulary shall be:

Business
Strategic
Management
Standardization
Support

These specializations remain profiles of the canonical Business Process rather than five competing normative process entities.

The primary organizational component association is:

Business         → Operating Core
Strategic        → Strategic Apex
Management       → Middle Line
Standardization  → Technostructure
Support          → Support Staff

This association is informative and classificatory rather than a cardinal identity rule.

⸻

9. Classification Conformance

Classification shall be multidimensional.

The initial profile shall support:

organizational_component
process_domain
value_stream
ecf_domain
lifecycle_stage

Classification dimensions shall remain independently meaningful.

No single classification dimension shall be treated as the semantic definition of the process.

⸻

10. Context Conformance

Every canonical catalog placement shall identify a valid Process Context.

The Process Context shall be derived from:

ECF Domain × Lifecycle Stage

The repository shall reference the authoritative ECF vocabulary.

It shall not redefine:

* ECF Domain;
* Lifecycle Stage;
* ECF coordinates.

A Process Context is an architectural context and shall not be treated as a Business Process.

⸻

11. L2 Business Process Conformance

A candidate L2 Process shall satisfy all four established criteria:

BP-C1 — Input–Output Transformation

The process transforms identifiable inputs into outputs or an equivalent defined result.

BP-C2 — Objective Contribution

The process makes a recognizable contribution to an enterprise objective or outcome.

BP-C3 — Standalone Executability

The process represents a coherent unit of work that can be independently identified and performed.

BP-C4 — Resource Dedication

The process requires identifiable resources or responsibility sufficient to constitute a distinct process boundary.

These four criteria form the mandatory L2 qualification test established by the process design.

A candidate failing the L2 test shall not be promoted to Business Process merely because it has a process-like name.

⸻

12. Activity Conformance

An Activity shall:

* belong to an L2 Business Process;
* represent a cohesive grouping of work;
* contribute to the parent process;
* avoid duplicating an L2 Business Process boundary;
* provide a defensible cohesion assessment.

The Activity cohesion model established by CR-BP-04 shall be machine-testable.

⸻

13. Task Conformance

A Task shall satisfy the four atomicity criteria:

1. Indivisibility
2. Single-Role Execution
3. Bounded Duration
4. Verifiable Completion

These criteria establish the formal L4 boundary.

A task that can be decomposed into further meaningful work units shall either:

* be reclassified as an Activity; or
* remain outside the formal catalog when the additional decomposition is implementation detail.

⸻

14. Structural Conformance

The canonical decomposition shall be:

Process Context
    ↓
L0 Process Scope
    ↓
L1 Process Group
    ↓
L2 Business Process
    ↓
L3 Activity
    ↓
L4 Task

The following rules apply:

CON-001 — Every L0 Scope belongs to a Process Context.

CON-002 — Every L1 Group belongs to an L0 Scope.

CON-003 — Every L2 Business Process belongs to a primary L1 Group.

CON-004 — Every L3 Activity belongs to an L2 Business Process.

CON-005 — Every L4 Task belongs to an Activity when an Activity decomposition exists.

CON-006 — Structural decomposition uses dea:composes.

CON-007 — Structural decomposition shall not introduce competing parent/child semantics.

CON-008 — The canonical primary process tree shall be acyclic.

The primary-tree constraint is a catalog architecture rule and shall not be interpreted as changing the global semantics or cardinality of dea:composes.

⸻

15. Realization Conformance

Business Process capability realization shall use:

BusinessProcess
        │
        │ dea:realizes
        ▼
BusinessCapability

The process repository shall not introduce a local equivalent such as:

capabilities_delivered

as a competing semantic relationship.

Additional capability relationships may be represented where supported by the normative OpenDEA metamodel.

⸻

16. Execution Conformance

Execution semantics shall comply with CR-BP-05.

Therefore:

CON-020 — dea:composes shall not represent execution order.

CON-021 — Workflow shall remain distinct from Business Process.

CON-022 — Workflow references shall be explicitly typed.

CON-023 — Multiple Workflows may realize the same Business Process.

CON-024 — Workflow variation shall not automatically imply Business Process variation.

⸻

17. Business Function Boundary

The conformance profile shall explicitly prevent:

Business Function = Process Group

from becoming a catalog equivalence.

A Process Group is a Business Process Architecture grouping construct.

A Business Function is an OpenDEA enterprise architecture concept.

They may be related, but one shall not silently replace the other.

⸻

18. Reference Conformance

Every reference to an external OpenDEA concept shall resolve against its authoritative source.

This includes references to:

* Business Capability;
* Business Function;
* Actor;
* Workflow;
* Task;
* System;
* Service;
* Business Object;
* ECF Domain;
* Lifecycle Stage.

Broken references shall fail conformance.

⸻

19. Version Conformance

Every published process artifact shall identify:

* semantic identity;
* artifact version;
* metamodel version;
* catalog version;
* status;
* provenance where required.

A version change shall not silently create a new semantic identity.

A semantic identity change shall require an explicit governed change.

⸻

20. Status Conformance

The catalog shall distinguish at minimum:

Draft
Proposed
Validated
Published
Deprecated
Retired

The exact lifecycle transition rules shall be governed by repository governance.

A Draft or Proposed artifact shall not be represented as an authoritative Published process.

⸻

21. Conformance Failure

A failed conformance test shall produce:

* rule identifier;
* artifact identifier;
* failed assertion;
* severity;
* diagnostic explanation;
* remediation guidance.

Example:

CON-BP-003
Artifact: dea:process-customer-order-fulfilment
Failure:
Candidate L2 Process does not provide evidence of
Standalone Executability.
Result:
NOT CONFORMANT

⸻

22. Machine-Readable Validation

The conformance profile shall be represented in machine-readable form.

Indicative structure:

validation/
├── identity/
├── architecture/
├── semantics/
├── decomposition/
├── execution/
├── references/
├── versioning/
└── conformance/

The exact implementation technology shall remain subordinate to the semantic contract.

⸻

23. Conformance Versus MECE

CR-BP-06 shall not attempt to solve the complete MECE problem.

The distinction is:

Conformance
    │
    └── Is this process definition valid?
MECE
    │
    └── Is the catalog collectively exhaustive
        and mutually exclusive?

Conformance provides the technical and semantic foundation required for the later MECE validation programme in CR-BP-08.

The source design explicitly calls for both machine-testable validation and a separate holistic/MECE validation loop.

⸻

24. Repository Changes

The repository shall establish:

validation/
├── identity/
├── architecture/
├── semantics/
├── decomposition/
├── execution/
├── references/
├── versioning/
└── conformance/
schemas/
    process-conformance.schema.json
architecture/
    conformance-profile.yaml
docs/
    conformance.md

The CI pipeline shall validate all published artifacts against the conformance profile.

⸻

25. Minimum Conformance Gate

A Business Process shall not be published as authoritative unless:

Identity       ✓
Context        ✓
Structure      ✓
L2 Criteria    ✓
Intent         ✓
Specialization ✓
Classification ✓
Relationships  ✓
Decomposition  ✓
References     ✓
Execution      ✓
Version        ✓

The exact implementation of the gate shall be established through repository implementation work after approval of this CR.

⸻

26. Acceptance Criteria

CR-BP-06 is accepted when:

* a complete Process Conformance Profile exists;
* L2 qualification is machine-testable;
* Activity cohesion is machine-testable;
* Task atomicity is machine-testable;
* Intent, Specialization and Classification are orthogonal and validated;
* Process Context references authoritative ECF semantics;
* structural relationships use canonical OpenDEA relationships;
* capability realization uses dea:realizes;
* Workflow remains distinct from structural process decomposition;
* Business Function and Process Group remain distinct;
* external references are resolvable;
* version and status are validated;
* conformance failures are diagnosable;
* CI can enforce the conformance profile;
* MECE remains explicitly separated for CR-BP-08.

⸻

27. Result

CR-BP-06 establishes the Business Process Catalog as a validated engineering asset rather than an uncontrolled taxonomy.

The resulting progression is:

CR-BP-01
Canonical Process Identity
        ↓
CR-BP-02
Process Context
        ↓
CR-BP-03
Process Architecture + Semantic Profile
        ↓
CR-BP-04
Activity Model
        ↓
CR-BP-05
Execution Boundary
        ↓
CR-BP-06
Conformance Profile
        ↓
CR-BP-07
Catalog Architecture
        ↓
CR-BP-08
MECE Validation
        ↓
CR-BP-09
Cross-Repository Integrity
        ↓
CR-BP-10
ECF Matrix Population

The six completed CRs therefore establish the complete semantic and structural spine of the Business Process repository before population begins.

Architectural consequence

I would now regard CR-BP-01 through CR-BP-06 as the foundational contract for the process repository.

The particularly important separation is:

ECF
 │
 ├── Domain
 └── Lifecycle
        │
        ▼
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

while execution is orthogonal:

Business Process
       │
       ▼
Workflow
       │
       ▼
ordered work + decisions

And the semantic profile cuts across that structure:

Business Process
├── Intent          → Why
├── Specialization  → What kind
└── Classification  → Where / how categorized

That gives us a much stronger architecture than the original L0/L1/L2/L3/L4 table alone. The original source correctly identified the need for objective L2, L3 and L4 tests and an explicit stopping boundary, but CR-BP-02/03 now prevent us from incorrectly equating those levels with the underlying enterprise ontology.

---

## Result (post-landing — added by Coder on 2026-09-10)

**Implication for CR-BP-34.** The Conformance Profile — the four-level A/B/C/D + E/F machine-testable validation contract — is **partially already enforced** by the existing CR-BP-16 conformance gate. Mapping the user's levels onto the existing gate:

| User level | User rule names | Existing CR-BP-16 coverage |
|---|---|---|
| **A — Identity** | (canonical id, version, type, authority) | **BP-SPEC-01-001..007** + `check_process_identity.py` (BP-ARC-ID-001..005). Covered. |
| **B — Architectural** | (Process Context → Scope → Group → BP → Activity → Task) | **PC-001..008** + **PG-001..008**. Context / Scope / Group covered; Activity / Task not yet covered because those record types don't exist (see CR-BP-32/33). |
| **C — Semantic** | (Intent, Specialization, Classification, outcome, capability) | **BP-SEM-001..012** (CR-BP-14 semantic contract). Covered. |
| **D — Decomposition** | (L2 criteria BP-C1..C4, Activity cohesion ACT-001..010, Task atomicity) | **BP-SEM-007..009** partially cover L2 criteria. Activity cohesion and Task atomicity are **new** (deferred to CR-BP-32). |
| **E — Execution** | (EXE-001..010, structural-vs-execution separation) | **Not covered**. No execution references exist today (see CR-BP-33). |
| **F — Ecosystem** | (OpenDEA metamodel references, ECF, cross-repo) | **ECF Conformance Gate** + `check_ecf_conformance.py` cover the ECF axis. Cross-repo identifier integrity covered by `check_cr_metadata.py` (CR-META-001..006). Metamodel reference integrity is partial. |

**Net harvestable rules from CR-BP-34 that can land as additive validators without entity mutation:**

- **PSP-001..003** (Intent conformance — purposive / approved vocabulary / no organizational ownership). The CR-BP-14 semantic contract already enforces a 7-value purpose-oriented vocabulary; PSP-001..003 strengthen it by forbidding organizational-domain substitutions. **Land as a `scripts/check_intent_purposive.py` validator with 3 rules.**
- **BP-C1..C4** (the four L2 qualification criteria). Today the catalog declares these in prose in `docs/architecture.md` and `docs/semantic-contract.md`, but does not enforce them as validators. **Land as `scripts/check_l2_qualification.py` with 4 rules.** BP-C3 (Standalone Executability) and BP-C4 (Resource Dedication) are the most novel — they close a real semantic gap.
- **CON-001..008** (structural decomposition rules). Most overlap with PG-001..008 / PC-001..008. **The new ones are CON-005 (Activity belongs to BP) and CON-006 (uses `dea:composes`).** Land as additions to `scripts/check_process_semantics.py`.
- **CON-020..024** (execution conformance). Blocked on CR-BP-33. Cannot land until Workflow references exist.
- **Status Conformance (§20)** — Draft / Proposed / Validated / Published / Deprecated / Retired lifecycle. The catalog already uses `status` and `lifecycle_status` fields; the **state-machine constraints** (Draft ≠ Published; status transitions must be governed) are partially enforced by `check_admission_gate.py` but not as a complete lifecycle state machine. **Land as `scripts/check_lifecycle_state_machine.py`** — closes a real governance gap.
- **Version Conformance (§19)** — version bump ≠ semantic identity change. Partially covered. **Strengthen with explicit semantic-identity-vs-version rules in `check_process_identity.py`.**

**Net harvestable rules that cannot land yet (blocked on CR-BP-32 / CR-BP-33):**

- ACT-001..010 (Activity rules) — blocked on CR-BP-32 (no Activity record type).
- EXE-001..010 (Execution Boundary rules) — blocked on CR-BP-33 (no Workflow references).

### **Renumbered CR-BP-35..38 mapping (per user's §27 sequence)**

The user's §27 names the post-CR-BP-34 follow-on sequence as CR-BP-07..10. Mapping onto our actual sequence space:

| User number | User title | **Our renumbered carrier ID** | Status (already merged or new?) |
|---|---|---|---|
| CR-BP-07 | Process Catalog Architecture | **CR-BP-35** | Partially shipped via CR-BP-12 (Process Group Profile), CR-BP-15 (Catalog Reconciliation), CR-BP-22 (Register Audit Reconciliation), CR-CATALOG-STRUCT-02. CR-BP-35 would consolidate + retro-document. |
| CR-BP-08 | MECE Validation | **CR-BP-36** | New. Real work; ~600 LOC + tests. The "register audit" tooling is a partial implementation. |
| CR-BP-09 | Cross-Repository Integrity | **CR-BP-37** | Partially shipped via cross-repo context block in `change-requests/README.md` and the PR-MERGE chain that included #45/#47 (metamodel + BC). CR-BP-37 would formalize as a contract. |
| CR-BP-10 | ECF Matrix Population | **CR-BP-38** | **Already done.** PR #46 (register v2), #48-60 (landing + completion), #65 (register v4). CR-BP-38 would be a documentation retrospective. |

### **Execution plan recommended by Coder**

**Phase 1 — Documentation carrier (this PR).** Land the four CRs in `01_plan/` as the knowledge-harvest record + write `POSITIONING-CR-BP-32-33-34-vs-merged-crs.md`. No code. Surfaces the harvestable insights, the rule-set mapping, and the renumbering decisions.

**Phase 2 — Additive conformance rules.** Open **CR-BP-34a** to land the harvestable rules as additive validators (PSP-001..003, BP-C1..C4, status state machine, semantic-identity-vs-version). One PR; ~400 LOC + tests. Does not require CR-BP-32 or CR-BP-33 to land.

**Phase 3 — L3 Activity.** Open **CR-BP-32** as the schema + record-type + ACT-001..010 validators. New `dea:Activity` specialization under `dea:Process` in `metamodel-pointer.yaml`. ~600 LOC + tests.

**Phase 4 — L4 Execution Boundary.** Open **CR-BP-33** to wire `dea:Workflow` / `dea:Task` references + EXE-001..010 validators. ~400 LOC + tests.

**Phase 5 — Renumbered follow-ons.** Open CR-BP-35..38 as the documentation/consolidation phase per user's §27.

This phasing keeps every PR additive (no entity mutation, no record restructure, no disposition-register change) and lets each be independently reverted if a downstream consumer pushes back.

