
> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.
The attached material confirms an important point for CR-BP-02: the intended Business Process repository is explicitly supposed to use the ECF Domain × Lifecycle structure as its organizing foundation, with the top-level process meaning derived from the confluence of those dimensions rather than from simple terminology combinations. Pasted markdown.md

However, our earlier Phase 0 analysis also established that we should not prematurely turn the ECF cell itself into a Business Process entity. The CR therefore needs to formalize the contextual layer first.

CR-BP-02 — Establish Process Context

Status: Proposed
Type: Foundational Architecture
Priority: P0
Programme: OpenDEA Business Process Architecture Evolution
Depends On: CR-MM-PROC-01 (dea-metamodel PR #163) + CR-AR-FMWK-01 (dea-architecture-framework PR #10 + tag v0.6.0) + CR-BP-SPEC-BP-01 (dea-catalog-processes PR #12)
Blocks: CR-BP-03, CR-BP-07, CR-BP-10

Reframed (2026-09-03): CR-BP-02's predecessor is the kernel +
specialization tranche (CR-MM-PROC-01 / CR-AR-FMWK-01 / CR-BP-SPEC-BP-01),
NOT the now-superseded CR-BP-01. References to "canonical
dea:BusinessProcess established by CR-BP-01" below have been
re-anchored to the kernel + specialization discipline: the
Process Catalog covers the Business Process specialization
(`dea:entity-business-process` in the OpenDEAM root model v0.6.0;
`dea:BusinessProcess` in the metamodel Core; 1:1 LOSSLESS mapping per
CR-MM-PROC-01 §4); the Process kernel (`dea:entity-process` in the
root model; `dea:Process` in the metamodel) is not a catalog entity
and not a Process Context. PC-007 / PC-008 / AC-07 below refer to the
Business Process specialization id (`dea:BusinessProcess` /
`dea:entity-business-process`) per the corrected discipline.

⸻

1. Change Summary

Establish Process Context as the canonical contextual mechanism through which the Business Process Catalog is organized against the OpenDEA Enterprise Concepts Framework.

The Process Context is derived from:

ECF Domain
      ×
Lifecycle Stage
      │
      ▼
Process Context

It establishes the semantic boundary within which Business Process Architecture is discovered and organized.

The fundamental decision is:

An ECF Domain × Lifecycle Stage intersection defines a Process Context; it does not itself constitute a Business Process.

This distinction is essential to prevent the catalog from generating processes mechanically from ECF terminology.

The attached design material explicitly requires every matrix cell to be examined for holistic process coverage and warns against constructing processes through “word soups” or simply combining Domain and Lifecycle terminology. Pasted markdown.md

⸻

2. Problem Statement

The Business Process Catalog needs a stable contextual coordinate from which process discovery can proceed.

Without one, process discovery risks becoming:

Domain
   +
Lifecycle
   +
plausible noun phrase
       │
       ▼
"Process"

That is precisely the approach we are trying to eliminate.

The intended approach is:

Domain
   ×
Lifecycle
   │
   ▼
Semantic Interpretation
   │
   ▼
Process Context
   │
   ▼
Coverage Analysis
   │
   ▼
Candidate Business Processes

The attached design specifically states that establishing the correct L0 is critical and that each cell must be examined comprehensively before identifying its constituent process elements. Pasted markdown.md

⸻

3. Architectural Intent

Process Context is a contextual construct, not a synonym for:

* Business Process;
* Business Function;
* Business Capability;
* Process Group;
* Process Scope.

The conceptual architecture is:

┌─────────────────────────────┐
│ Enterprise Concepts         │
│ Framework                   │
└──────────────┬──────────────┘
               │
       Domain × Lifecycle
               │
               ▼
┌─────────────────────────────┐
│ Process Context             │
│                             │
│ • Domain                    │
│ • Lifecycle Stage           │
│ • Semantic Meaning          │
│ • Scope                     │
│ • Inclusion                 │
│ • Exclusion                 │
│ • Adjacent Contexts         │
└──────────────┬──────────────┘
               │
               ▼
      Business Process
       Architecture

⸻

4. Process Context Definition

For this CR, the working normative definition is:

A Process Context is the bounded enterprise context established by the intersection of an ECF Domain and Lifecycle Stage, within which Business Process responsibilities are identified, organized and validated.

This definition deliberately says within which rather than which represents.

That distinction is foundational.

An ECF cell may contain:

0
1
or
N

canonical Business Processes.

There must be no assumption that:

1 ECF Cell = 1 Business Process

⸻

5. Context Identity

Every Process Context must have a stable identity derived from its two authoritative dimensions.

Conceptually:

Process Context ID
=
ECF Domain ID
+
Lifecycle Stage ID

The exact identifier syntax should follow existing OpenDEA identity conventions and must be resolved during implementation.

For example:

ECF-D01 × LC-S01
        │
        ▼
Process Context

The identifier must remain stable even if the human-readable description is subsequently refined.

⸻

6. Process Context Properties

A Process Context should provide, at minimum:

Property	Purpose
id	Stable identity
domain	ECF Domain reference
lifecycle_stage	ECF Lifecycle reference
name	Human-readable context name
definition	Normative semantic meaning
scope	What the context covers
inclusions	Explicitly included concerns
exclusions	Explicitly excluded concerns
outcomes	Intended enterprise outcomes
adjacent_contexts	Related neighbouring contexts
processes	Canonical processes belonging to the context

The final schema should only contain properties justified by the normative architecture.

⸻

7. Cell Charter

Each Process Context shall have a Cell Charter.

The Cell Charter becomes the semantic foundation for process discovery.

It should establish:

Domain
Lifecycle Stage
       │
       ▼
Why does this intersection exist?
       │
       ▼
What enterprise concern does it represent?
       │
       ▼
What must be accomplished?
       │
       ▼
What is inside the boundary?
       │
       ▼
What is outside the boundary?

The charter is therefore not simply a description.

It is a discovery and validation instrument.

⸻

8. Process Discovery Rule

A Process Context must be interpreted before processes are proposed.

The required sequence is:

1. Identify Domain meaning
          ↓
2. Identify Lifecycle meaning
          ↓
3. Determine their semantic confluence
          ↓
4. Define Process Context
          ↓
5. Identify coverage concerns
          ↓
6. Search for established processes
          ↓
7. Evaluate candidate processes
          ↓
8. Accept canonical processes

The attached material expressly requires this kind of holistic analysis and gives the example that “Governance & Existence / Conceive” cannot be reduced mechanically to something such as “Enterprise Policy Definition.” Pasted markdown.md

⸻

9. Context Is Not Process

This CR establishes an explicit semantic separation.

Process Context
      │
      │ contains / scopes
      ▼
Business Process

It must not be interpreted as:

Process Context
      =
Business Process

Consequently, an ECF cell may produce:

Process Context
 ├── Business Process A
 ├── Business Process B
 └── Business Process C

where each process contributes uniquely to the collective coverage of the context.

Conversely, a context may ultimately contain a single comprehensive process if one established process adequately covers the semantic scope.

This aligns with the stated preference for a single well-known process where it genuinely encompasses the relevant cell, while allowing multiple processes where necessary. Pasted markdown.md

⸻

10. Contextual Boundary

Each Process Context must establish explicit boundaries.

Inclusion

What enterprise responsibilities belong inside the context?

Exclusion

What responsibilities belong elsewhere?

Adjacency

Which neighbouring contexts have legitimate relationships with this context?

This produces:

             Context A
          ┌──────────────┐
          │              │
          │   Scope      │
          │              │
          └──────┬───────┘
                 │
        ┌────────┴────────┐
        │                 │
   Context B          Context C

A relationship between contexts does not imply duplicated ownership.

⸻

11. Cross-Context Process Rule

A Business Process may legitimately interact with multiple Process Contexts.

However:

Interaction across contexts must not result in duplicate canonical process definitions.

Therefore:

Process Context A
       │
       └──────┐
              ▼
       Business Process X
              ▲
              │
       ┌──────┘
       │
Process Context B

must be represented through explicit relationships rather than by creating two independent definitions of Process X.

This establishes an early foundation for the cross-repository integrity requirement identified in the original design. Pasted markdown.md

⸻

12. ECF as Organizing Foundation

The Business Process Catalog will use the ECF as its organizing contextual framework.

The intended matrix is:

                  Lifecycle
             ┌───┬───┬───┬───┬───┬───┬───┐
             │   │   │   │   │   │   │   │
Domain       ├───┼───┼───┼───┼───┼───┼───┤
             │   │   │   │   │   │   │   │
             ├───┼───┼───┼───┼───┼───┼───┤
             │   │   │   │   │   │   │   │
             ├───┼───┼───┼───┼───┼───┼───┤
             │   │   │   │   │   │   │   │
             ├───┼───┼───┼───┼───┼───┼───┤
             │   │   │   │   │   │   │   │
             ├───┼───┼───┼───┼───┼───┼───┤
             │   │   │   │   │   │   │   │
             ├───┼───┼───┼───┼───┼───┼───┤
             │   │   │   │   │   │   │   │
             └───┴───┴───┴───┴───┴───┴───┘

Each cell becomes a Process Context.

The matrix therefore provides the coverage coordinate system, while the Business Process Architecture provides the process structure.

⸻

13. Critical Correction to Earlier L0 Thinking

The attached design originally describes L0 as a “CATEGORY (Enterprise Context)” and says that the top level embodies the confluence of Domain and Lifecycle Stage. Pasted markdown.md

CR-BP-02 now refines this architecture.

We should not equate L0 with the ECF cell itself.

Instead:

ECF Domain × Lifecycle
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

This is an important architectural improvement.

It preserves the original intent—that the ECF determines the top-level contextual organization—without forcing a framework coordinate to masquerade as a process.

⸻

14. L0 Consequence

CR-BP-02 therefore does not define L0 as a new normative OpenDEA entity.

Instead:

Process Context
      │
      └── contains
             │
             ▼
       L0 Process Scope

The exact semantics of L0 remain subject to CR-BP-03.

This allows CR-BP-03 to determine whether an L0 Process Scope is:

* a catalog construct;
* a classification;
* a structural grouping;
* or a first-class semantic entity.

We should not pre-empt that decision.

⸻

15. MECE Implications

Process Context establishes the first level of the MECE control system.

Context Coverage

The complete ECF matrix must eventually account for the intended enterprise semantic space.

Therefore:

All valid Domain × Lifecycle combinations
                    │
                    ▼
          Complete Process Context Set

must be collectively exhaustive.

Context Non-Overlap

Each cell has a unique coordinate:

Domain A × Lifecycle X
≠
Domain B × Lifecycle X
≠
Domain A × Lifecycle Y

The semantic interpretation of neighbouring contexts must nevertheless define their boundaries so that the process responsibilities do not unintentionally overlap.

The MECE property of the processes within the contexts will be formalized later by CR-BP-08.

⸻

16. Context Completeness

A Process Context is not considered complete merely because a cell exists.

It must have sufficient semantic definition to support process discovery.

Minimum completeness:

Domain identified
Lifecycle identified
Semantic confluence understood
Scope established
Boundary established
Coverage concerns identified
Adjacent contexts identified

Only then may process discovery proceed.

⸻

17. Process Context Lifecycle

Process Context itself should follow a controlled lifecycle:

Candidate
   ↓
Interpreted
   ↓
Defined
   ↓
Validated
   ↓
Established
   ↓
Revised
   ↓
Deprecated

A change in ECF Domain or Lifecycle semantics must trigger review of dependent Process Contexts.

A Process Context must never silently drift when its authoritative ECF coordinates change.

⸻

18. Metamodel Impact Assessment

This CR must explicitly determine whether ProcessContext needs to become a normative OpenDEA entity.

Current recommendation

Do not introduce dea:ProcessContext yet.

The immediate implementation should represent Process Context as a catalog/contextual construct referencing authoritative ECF dimensions.

Rationale:

1. The ECF already provides the authoritative coordinates.
2. Process Context primarily organizes discovery and catalog placement.
3. Introducing another normative entity prematurely could duplicate contextual semantics.
4. The requirement can initially be satisfied without modifying the normative metamodel.
5. Actual usage during catalog construction will provide evidence for whether first-class identity is necessary.

Therefore:

CR-BP-02
       │
       ▼
Catalog Context Construct
       │
       │ evidence gathered
       ▼
Future Metamodel Decision

If subsequent implementation demonstrates that Process Context requires independent semantic identity, relationships or reuse outside this repository, a dedicated metamodel CR can then be raised.

This is preferable to inventing a semantic entity before its necessity is demonstrated.

⸻

19. Required Repository Changes

CR-BP-02 should introduce the contextual architecture into the Business Process repository.

Conceptually:

catalog/
├── contexts/
│   ├── domain-01/
│   │   ├── lifecycle-01.yaml
│   │   ├── lifecycle-02.yaml
│   │   └── ...
│   ├── domain-02/
│   └── ...

The exact physical structure is an implementation decision, but every Process Context must be machine-readable.

A Process Context record should conceptually contain:

id: <stable-context-id>
domain: <canonical-ecf-domain-id>
lifecycle_stage: <canonical-lifecycle-id>
name: <context-name>
definition: <normative-definition>
scope:
  includes: []
  excludes: []
outcomes: []
adjacent_contexts: []
processes: []

The schema should reference canonical ECF identifiers rather than copying ECF definitions into the process repository.

⸻

20. Validation Requirements

CR-BP-02 should introduce the first Process Context validation rules.

PC-001 — Valid Coordinates

domain MUST reference an authoritative ECF Domain

PC-002 — Valid Lifecycle

lifecycle_stage MUST reference an authoritative Lifecycle Stage

PC-003 — Unique Coordinate

Domain × Lifecycle
MUST identify one unique Process Context

PC-004 — No Orphan Context

Every Process Context must resolve to valid ECF coordinates.

PC-005 — No Local ECF Definitions

The Process Catalog must not redefine the canonical ECF Domain or Lifecycle vocabulary.

PC-006 — Charter Completeness

An established Process Context must contain the required semantic charter fields.

PC-007 — No Automatic Process Equivalence

A Process Context must not be classified as dea:BusinessProcess.

PC-008 — Canonical Process References

Any process assigned to a context must resolve to the canonical
`dea:BusinessProcess` (metamodel Core) / `dea:entity-business-process`
(OpenDEAM root model v0.6.0) established by the kernel + specialization
tranche (CR-MM-PROC-01 + CR-AR-FMWK-01 + CR-BP-SPEC-BP-01).

⸻

21. Acceptance Criteria

CR-BP-02 is complete when:

AC-01

Every Business Process Catalog context is represented as:

ECF Domain × Lifecycle Stage

AC-02

The Process Context is explicitly distinguished from Business Process.

AC-03

The catalog references canonical ECF identifiers rather than maintaining duplicate ECF definitions.

AC-04

Each Process Context has a machine-readable Cell Charter.

AC-05

Each Cell Charter establishes:

* semantic meaning;
* scope;
* inclusion;
* exclusion;
* expected outcomes;
* adjacent contexts.

AC-06

A unique Process Context identity can be resolved from each Domain × Lifecycle coordinate.

AC-07

No Process Context is represented as a dea:BusinessProcess.

AC-08

No new dea:ProcessContext normative entity is introduced unless implementation evidence demonstrates that it is necessary.

AC-09

Automated validation detects invalid or duplicate Domain × Lifecycle coordinates.

AC-10

The repository README accurately reflects the Process Context architecture.

AC-11

Existing process records can be assessed against their appropriate Process Context without yet changing their decomposition topology.

AC-12

The implementation provides sufficient contextual structure to begin CR-BP-03.

⸻

22. Implementation Sequence

The implementation should proceed in this order:

1. Inventory authoritative ECF Domains
            ↓
2. Inventory authoritative Lifecycle Stages
            ↓
3. Establish the Domain × Lifecycle matrix
            ↓
4. Define Process Context schema
            ↓
5. Define Cell Charter schema
            ↓
6. Create context identifiers
            ↓
7. Validate matrix completeness
            ↓
8. Map existing processes provisionally
            ↓
9. Identify orphan / ambiguous processes
            ↓
10. Document boundary issues
            ↓
11. Validate against CR-BP-02

Do not yet populate the matrix with newly invented processes.

That belongs to CR-BP-10 after the architecture is established.

⸻

23. Expected Discovery Artifact

CR-BP-02 should produce a Process Context Register.

Conceptually:

Context ID	Domain	Lifecycle	Context Name	Status
PC-01	D01	L01	TBD	Defined
PC-02	D01	L02	TBD	Defined
…	…	…	…	…
PC-49	D07	L07	TBD	Defined

The register establishes the 7×7 coverage structure.

It does not yet assert the final Business Processes for each cell.

That distinction will prevent the repository from accumulating premature or ungrounded process definitions.

⸻

24. Architectural Outcome

After CR-BP-02, the Business Process repository will have this architecture:

                 ECF
                  │
          ┌───────┴────────┐
          │                │
       Domain          Lifecycle
          │                │
          └───────┬────────┘
                  │
                  ×
                  │
                  ▼
          PROCESS CONTEXT
                  │
          ┌───────┴────────┐
          │                │
        Scope           Charter
          │                │
          └───────┬────────┘
                  │
                  ▼
            L0 PROCESS SCOPE
                  │
                  ▼
            L1 PROCESS GROUP
                  │
                  ▼
          L2 BUSINESS PROCESS
                  │
             [CR-BP-03+]

This is the correct foundation for the next stage.

⸻

25. Important Discussion Items Resolved by This CR

CR-BP-02 deliberately resolves several questions while leaving others open.

Resolved

Q1. Does every ECF cell represent a process?

No.

Q2. Does every cell contain exactly one process?

No.

Q3. What does the ECF contribute?

Contextual organization and semantic coverage.

Q4. Can processes span contexts?

Yes, through explicit relationships, without duplicate canonical definitions.

Q5. Should the catalog redefine the ECF?

No.

Q6. Should Process Context initially become a new normative metamodel entity?

No; implement it as a catalog/context construct first.

Remains for CR-BP-03+

Q7. What exactly is L0?

CR-BP-03.

Q8. What exactly is L1?

CR-BP-03.

Q9. How does dea:composes implement process decomposition?

CR-BP-03.

Q10. What constitutes a valid Business Process?

CR-BP-06.

Q11. What is Activity?

CR-BP-04.

Q12. Where does Workflow/Task begin?

CR-BP-05.

⸻

26. Strategic Significance

This CR is more important than it might initially appear.

It establishes the difference between:

ECF
= enterprise semantic coordinate system

and:

Business Process Catalog
= process architecture organized by those coordinates

That allows us to preserve the original ambition of the repository: systematically work through every cell of the 7×7 ECF, derive comprehensive process coverage, and then rigorously decompose each accepted process. The uploaded design explicitly calls for proceeding cell-by-cell and validating each cell for completeness and non-overlap. Pasted markdown.md

It also means that when we eventually start the actual 49-cell discovery exercise, we will have a stable architectural object to work with:

             Process Context
                    │
                    ▼
             What does this
             intersection mean?
                    │
                    ▼
             What must be
             accomplished?
                    │
                    ▼
          Which established
          processes cover it?
                    │
                    ▼
             Are they MECE?
                    │
                    ▼
             Accept L0/L1
                    │
                    ▼
          Decompose through L2–L4

That is the point at which process discovery becomes an engineering activity rather than a naming exercise.

Recommended disposition

Approve CR-BP-02 for implementation.

After implementation, CR-BP-03 — Business Process Decomposition should be the next CR. That CR will reconcile the original L0–L4 topology against the actual OpenDEA dea:composes semantics and settle precisely what L0, L1, L2, L3 and L4 mean without contaminating the canonical BusinessProcess concept. Pasted markdown.md