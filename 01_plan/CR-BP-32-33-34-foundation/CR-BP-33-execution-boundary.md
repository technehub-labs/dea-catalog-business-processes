CR-BP-05 — Execution Boundary

# CR-BP-33 — Execution Boundary

> **Renumbering note.** Authored by eaojnr on 2026-09-10 as "CR-BP-05 — Execution Boundary". Renumbered to **CR-BP-33** because `CR-BP-05` is unused but would collide with the user's intended sequencing in CR-BP-34 §27. CR-BP-33 preserves the original content verbatim and adds the post-landing historical-context note at the bottom. See `CR-BP-32-activity-model.md` for the full renumbering rationale.

**Status**: Proposed (carrier CR — knowledge harvest + positioning; awaiting user direction on execution order)
**Layer**: L3 (Business Process) → L4 (Execution Boundary)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-09-10
**Original author**: eaojnr
**Source document**: `/home/hermes/.hermes/profiles/coder/cache/documents/doc_cf6fc6bb9e80_CR-BP-04_06.md` (lines 395-871)
**Depends on (logical)**: CR-BP-32 (Activity Model)
**Lands against (actual current state)**: Same as CR-BP-32; no entity mutation; no schema change.

---

CR-BP-05 should be particularly strict because this is where process architecture can otherwise collapse into workflow/BPM implementation. The current OpenDEA metamodel already distinguishes Business Process, Workflow, and Task, so the CR should exploit those existing concepts rather than creating another process-execution ontology.

CR-BP-33 — Execution Boundary

Status: Proposed
Type: Process Architecture / Execution Semantics
Priority: High
Depends On: CR-BP-01, CR-BP-02, CR-BP-03, CR-BP-32 (formerly CR-BP-04)
Target Repository: technehub-labs/dea-catalog-processes

⸻

1. Change Request

Establish the Execution Boundary between OpenDEA Business Process Architecture and executable process behaviour.

The change shall formally distinguish:

PROCESS ARCHITECTURE
        │
        ▼
Business Process
        │
        ▼
Activity
        │
        ▼
Task
        │
        │ realized / executed through
        ▼
EXECUTION MODEL
        │
        ▼
Workflow
        │
        ▼
Execution Steps

The purpose is to ensure that structural process decomposition is not incorrectly interpreted as executable sequencing.

⸻

2. Motivation

A Business Process describes an enterprise work construct and its contribution to an intended outcome.

A Workflow describes an ordered composition of work and decisions toward an outcome.

These are related but not identical concepts.

The Business Process Catalog must therefore be capable of representing:

* what the enterprise process is;
* how the process is logically decomposed;
* how that process may be executed;

without collapsing all three concerns into one model.

⸻

3. Architectural Decision

3.1 Structural and Execution Semantics Are Separate

The repository shall maintain two distinct semantic layers.

Structural Layer

Business Process
       │
       └── composes
              ↓
           Activity
              │
              └── composes
                     ↓
                    Task

Execution Layer

Business Process
       │
       └── may be realized/executed through
                       ↓
                    Workflow
                       │
                       ↓
                 ordered work
                 and decisions

The structural layer defines architectural composition.

The execution layer defines executable behaviour.

Neither shall be treated as a substitute for the other.

⸻

4. Execution Boundary

The Execution Boundary is the semantic boundary at which an architectural description of process work becomes an executable or operational representation of how that work is performed.

The boundary shall separate:

Architectural Questions

* What Business Process exists?
* What outcome does it produce?
* What Activities constitute it?
* What Tasks form those Activities?
* What capability does it realize?
* What actors, objects and resources are involved?

from:

Execution Questions

* In what order are Tasks performed?
* What decisions control execution?
* What conditions trigger paths?
* Which actor performs a particular execution step?
* Which system performs it?
* What happens when execution fails?
* Which alternative path is followed?
* What state transition occurs?

⸻

5. Workflow Relationship

Workflow shall remain the execution-oriented construct.

The existing OpenDEA semantic definition of Workflow is the appropriate conceptual boundary for ordered task and decision composition.

The Business Process Catalog shall therefore reference Workflow rather than redefine it.

Conceptually:

Business Process
       │
       ├── structurally composes
       │       └── Activity
       │              └── Task
       │
       └── may be operationalized through
               └── Workflow
                       ├── Task
                       ├── Decision
                       └── Execution Path

A Business Process may therefore have:

* zero Workflows;
* one Workflow;
* multiple Workflows.

A Workflow may also represent only a particular execution scenario or implementation of a Business Process.

⸻

6. Structural Composition Does Not Imply Sequence

The following inference shall be explicitly prohibited:

A composes B
+
B composes C
≠
A → B → C executes in that order

dea:composes establishes structural part-whole semantics.

It does not establish:

* before/after;
* precedence;
* conditional branching;
* parallelism;
* synchronization;
* repetition;
* exception handling.

These belong to execution semantics.

⸻

7. Task Boundary

Task is the lowest formal decomposition level of the Business Process Catalog.

A Task describes a defined unit of work.

However, the same Task concept may participate in different execution representations.

For example:

Business Process
      │
      ▼
Activity
      │
      ├── Task A
      ├── Task B
      └── Task C

does not prescribe:

A → B → C

A Workflow may instead define:

A
│
▼
Decision
├── B
└── C

or:

A
├── B
└── C
     ↓
   Join

The architectural process model therefore remains stable while execution models vary.

⸻

8. Execution Realization

A Business Process may be executed through different modes:

* human execution;
* system-supported execution;
* automated execution;
* AI-agent execution;
* hybrid human/system execution.

Execution mode shall not redefine the Business Process itself.

For example, a Customer Order Fulfilment Business Process may remain semantically identical whether:

human → system → human

or:

AI agent → system → autonomous service

performs the work.

This preserves process identity while allowing execution technology to evolve.

⸻

9. Actor and Resource Semantics

Execution responsibility shall be represented through existing OpenDEA concepts.

Where appropriate, the execution model may reference:

* Actor;
* Task;
* System;
* Resource;
* Information;
* Data;
* Service.

The process repository shall not create duplicate actor, system or resource semantics.

⸻

10. Trigger and Outcome

The Business Process may define:

* trigger;
* inputs;
* outputs;
* outcome;
* relevant conditions.

However, a process trigger is not equivalent to an execution event sequence.

Likewise:

Process Outcome

is not equivalent to:

Workflow Completion Event

The former describes the architectural purpose/result of the process.

The latter describes execution behaviour.

⸻

11. Multiple Execution Realizations

The architecture shall permit one Business Process to have multiple execution realizations.

Example:

Customer Order Fulfilment
       │
       ├── Standard Fulfilment Workflow
       │
       ├── Exception Fulfilment Workflow
       │
       └── Assisted Fulfilment Workflow

These shall not become separate Business Processes merely because their execution paths differ.

A separate Business Process is justified only where the underlying process identity and established L2 criteria support that distinction.

⸻

12. Execution Versus Implementation

The Execution Boundary shall also prevent uncontrolled descent into technology implementation.

The process catalog shall not become a repository for:

* API sequences;
* database procedures;
* application-specific control flow;
* infrastructure operations;
* scripts;
* code;
* technical runbooks.

Such information may be referenced by an execution or implementation model but shall not redefine the Business Process Architecture.

⸻

13. Process and Workflow Traceability

Where Workflow is represented, the repository shall support traceability:

Business Process
      │
      └── Workflow
             │
             ├── Task
             ├── Decision
             ├── Condition
             └── Execution Path

The relationship shall identify whether the Workflow is:

* reference execution;
* operational execution;
* scenario-specific execution;
* implementation-specific execution.

The exact controlled vocabulary shall be finalized in the repository profile.

⸻

14. No New Normative Execution Ontology

CR-BP-05 shall not introduce competing concepts such as:

* Process Flow;
* Execution Process;
* Process Instance;
* Execution Process Group;
* Workflow Process;
* Process Sequence.

Where an existing OpenDEA metamodel concept is sufficient, the repository shall reference it.

Where an additional concept is genuinely required, it shall be proposed through a separate metamodel CR.

⸻

15. Execution Conformance Rules

EXE-001 — Structural decomposition shall not encode execution sequence.

EXE-002 — dea:composes shall not be interpreted as execution ordering.

EXE-003 — Workflow shall remain distinct from Business Process.

EXE-004 — A Business Process may have multiple execution Workflows.

EXE-005 — Different Workflow implementations shall not automatically create different Business Processes.

EXE-006 — Execution actors shall reference existing Actor semantics.

EXE-007 — Execution systems shall reference existing System semantics.

EXE-008 — Execution logic shall not redefine process identity.

EXE-009 — Implementation detail shall remain outside the Business Process decomposition model.

EXE-010 — Every catalogued Workflow reference shall identify its relationship to the associated Business Process.

⸻

16. Repository Changes

The repository shall establish:

architecture/
    execution-boundary.yaml
    execution-model.yaml
schemas/
    workflow-reference.schema.json
    execution-reference.schema.json
validation/
    execution/
        structural-separation.yaml
        workflow-reference.yaml
        implementation-boundary.yaml
docs/
    execution-boundary.md
    workflow-and-process.md

⸻

17. Acceptance Criteria

CR-BP-05 is accepted when:

* structural and execution semantics are explicitly separated;
* Business Process and Workflow are clearly distinguished;
* Task can participate in both structural and execution representations without semantic duplication;
* structural composition does not imply sequence;
* multiple execution realizations are supported;
* actor and system semantics reference existing OpenDEA constructs;
* implementation detail is excluded from the process architecture;
* workflow references are traceable to Business Processes;
* execution validation rules are machine-readable;
* no duplicate normative execution ontology is introduced.

⸻

18. Result

CR-BP-05 establishes the answer to:

How can a Business Process be executed without redefining what the Business Process is?

The resulting architecture is:

             BUSINESS PROCESS ARCHITECTURE
                         │
                         ▼
                 Business Process
                         │
                    composes
                         ▼
                      Activity
                         │
                    composes
                         ▼
                       Task
                         │
              ───────────┼───────────
                  EXECUTION BOUNDARY
                         │
                         ▼
                      Workflow
                         │
                         ▼
              Ordered Work + Decisions

This separation allows OpenDEA to represent both stable enterprise architecture and changing execution technology.

---

## Result (post-landing — added by Coder on 2026-09-10)

**Implication for CR-BP-33.** The Execution Boundary — separating structural process decomposition from executable process behaviour — is **not** codified in the catalog today. `dea:Workflow` and `dea:Task` exist in `dea-metamodel/metamodel/registry/entities.yaml` with `lifecycle: proposed` and `catalog_repo: null`, but no catalog has adopted them. The 196 canonical records in `dea-catalog-processes` carry **no Workflow references**, **no execution semantics**, and **no Task decomposition**. The conformance gate (CR-BP-16) does not currently check for `dea:composes`-as-execution-order violations because no execution-bearing relationships exist to violate.

**Land CR-BP-33 means:**

1. **Reference `dea:Workflow` and `dea:Task` from `metamodel-pointer.yaml`** (currently absent). Add them with `lifecycle: proposed` and a note that this catalog references but does not instantiate them yet.
2. **Add EXE-001..010 validation rules** to `scripts/check_process_semantics.py` (the most natural home — it already handles structural decomposition checks). These become **additive** rules: a Business Process that has no Workflow reference is valid (Execution mode = unmodelled), but a Business Process that references a Workflow must do so via a typed `references` relationship and the structural decomposition must not be reinterpreted as execution order.
3. **No retroactive Workflow instantiation.** Existing BPs stay at L4 conformance with no execution references. Workflow adoption is opt-in for new BPs that explicitly need an execution model.
4. **Cross-repo dependency.** CR-BP-33 stays internal to this catalog. If a sibling catalog (e.g. a future `dea-catalog-workflows`) wants to instantiate `dea:Workflow`, the cross-repo reference contract is CR-BP-09 (the user's CR-BP-09 → would become CR-BP-37 in our sequence) from CR-BP-34 §27.

**Sequence recommendation.** Land CR-BP-33 immediately after CR-BP-32. They are independent — CR-BP-32 introduces L3 Activity (internal structure); CR-BP-33 introduces the L4 Execution Boundary (orthogonal axis). Both are optional authorial affordances. Existing records are unaffected.

⸻
