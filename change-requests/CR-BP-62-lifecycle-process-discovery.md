# CR-BP-62: Lifecycle Process Discovery & Canonical Process Evaluation

**Status**: Proposed
**Layer**: Process Catalog (lifecycle discovery)
**Owner**: eaojnr (raised); Coder (landing)
**Date**: 2026-09-14
**Carrier**: Normative discovery/governance CR. Establishes the lifecycle process-discovery method, the canonical-process evaluation test battery (BP-LIFE-001..015), the Process Pattern model, the disposition model, and the machine-readable discovery record; lands the structural validator (DISC-001..008) as advisory gate [19].
**Depends on**: CR-BP-02; CR-BP-03; CR-BP-12; CR-BP-14; CR-BP-32
**Lands against**: 126 canonical BP records (125 active + 1 deprecated), 35 canonical PG records, 35 canonical PC records, 501 canonical Activity records; 23 conformance gates CONFORMANT; L3 program complete across all 7 domains
**Type**: Architecture / Process Discovery / Catalog Governance
**Scope**: Business Process Catalog
**Primary concern**: ECF Lifecycle Stage process discovery
**Priority**: High

---

---

1. Executive Summary

CR-BP-62 establishes a normative method for determining whether an Enterprise Concept Framework (ECF) Lifecycle Stage contains one or more canonical Business Processes, canonical process patterns, specialized processes, or no canonical process.

The change addresses an architectural ambiguity in the current Business Process Catalog:

An ECF intersection is a Process Context and does not automatically constitute a Business Process.

This principle remains unchanged.

However, the absence of an automatically generated process from an ECF Context must not be interpreted as evidence that the Context contains no stable or universal Business Process.

In particular, lifecycle-boundary stages such as Activate and Retire must be evaluated through the same evidence-based process-discovery discipline as all other lifecycle stages.

CR-BP-62 therefore establishes:

1. a lifecycle process-discovery method;
2. a canonical-process admission test;
3. a process-pattern evaluation model;
4. a cross-domain applicability test;
5. a semantic-stability test;
6. a process-boundary and stage-span test;
7. a duplicate/overlap test;
8. an evidence and confidence model;
9. explicit admission, specialization, deferment and rejection dispositions;
10. a repeatable discovery record suitable for human and machine evaluation.

The change does not require every ECF cell to contain a process.

---

2. Problem Statement

The ECF provides a matrix of Enterprise Domains × Lifecycle Stages.

The Business Process Catalog correctly interprets an ECF intersection as a Process Context, rather than automatically treating the intersection as a Business Process.

The current architecture therefore avoids the invalid assumption:

Domain × Lifecycle Stage = Business Process

However, an additional assumption can inadvertently emerge:

```text
Lifecycle Stage with transitional semantics
        ↓
No universal Business Process
```

That inference is not valid.

A lifecycle stage may contain:

* no canonical process;
* one canonical process;
* several canonical processes;
* a reusable process pattern;
* domain-specific specializations of a canonical process;
* processes that span multiple lifecycle stages;
* processes whose canonical home lies elsewhere but which contribute to the Context.

Consequently:

Process absence must be established through discovery and evaluation, not inferred from the nature of the lifecycle stage.

This is especially relevant to Activate and Retire.

---

3. Architectural Principle

CR-BP-62 establishes the following principle:

An ECF Lifecycle Stage has no process-population obligation. However, absence of a canonical Business Process shall be an evidence-based discovery outcome and shall not be presumed from the lifecycle stage semantics alone.

A second principle follows:

Lifecycle transition semantics do not disqualify a candidate from being a canonical Business Process. A process shall be admitted when a stable enterprise transformation, trigger, outcome, boundary and semantic identity can be demonstrated across relevant contexts.

A third principle is required:

The ECF provides the contextual coordinate; the Business Process Catalog determines process identity and structure.

Therefore:

```text
ECF Context
     │
     ▼
Discovery
     │
     ▼
Candidate Process / Pattern
     │
     ├── Canonical Process
     ├── Specialization
     ├── Cross-stage Process
     ├── Contextual Contribution
     ├── Deferred Candidate
     └── Rejected Candidate
```

---

4. Scope

CR-BP-62 applies to:

* all seven ECF Lifecycle Stages;
* all ECF Domains;
* Process Contexts;
* candidate Business Processes;
* canonical process patterns;
* specialized Business Processes;
* processes spanning multiple lifecycle stages;
* process discovery and re-landscape decisions.

The method shall be applied particularly to:

* Activate
* Retire

because these stages represent lifecycle boundaries and are particularly susceptible to incorrect assumptions about process universality.

---

5. Non-Goals

CR-BP-62 does not:

1. require every ECF cell to contain a Business Process;
2. create one process per ECF cell;
3. create processes named after ECF coordinates;
4. equate Lifecycle Stage with Process;
5. create a new top-level ontology entity called LifecycleProcess;
6. require every lifecycle transition to become a separate process;
7. duplicate a canonical process merely because it participates in multiple ECF contexts;
8. redefine the OpenDEA Process kernel;
9. prescribe workflow or task-level implementation;
10. assume that Activate and Retire necessarily contain canonical processes.

---

6. Key Terminology

6.1 Lifecycle Context

The ECF Lifecycle Stage in which a particular enterprise responsibility is examined.

Examples:

* Conceive
* Design
* Build
* Activate
* Operate
* Improve
* Retire

---

6.2 Process Context

The combination of:

Enterprise Domain × Lifecycle Stage

It establishes the semantic boundary for process discovery.

It is not itself a process.

---

6.3 Candidate Process

A proposed process identified during discovery but not yet admitted as canonical.

---

6.4 Canonical Process

A Business Process that has passed the catalog's identity, semantic, boundary, evidence and uniqueness tests and has been accepted as the authoritative process representation within the Business Process specialization.

---

6.5 Process Pattern

A recurring and sufficiently stable enterprise transformation that may manifest as multiple domain-specific Business Processes.

A Process Pattern is initially a discovery and analytical concept, not necessarily a new OpenDEA metamodel entity.

Example:

```text
Transition to Service
       │
       ├── Transition Product to Service
       ├── Transition Technology to Service
       ├── Transition Facility to Service
       └── Transition Capability to Service
```

The pattern identifies common semantics without forcing all manifestations into one operational process.

---

6.6 Specialized Process

A process that semantically refines an existing canonical process.

Example:

```text
Transition to Service
        │
        └── Transition Digital Service to Operation
```

---

6.7 Lifecycle-Spanning Process

A single Business Process whose execution legitimately contributes to more than one ECF Lifecycle Stage.

Example:
```text

Deploy New Service
Build ─────────────── Activate
```

The process shall not be duplicated solely because it crosses lifecycle boundaries.

---

7. Core Discovery Principle

Process discovery shall begin with enterprise work, not with ECF cell names.

The discovery question is:

What repeatable enterprise responsibility, transformation or value-producing/control-producing work occurs in this Context?

Not:

"What process should we invent for this ECF cell?"

Therefore:

```text
ECF Context
    ↓
Enterprise concern
    ↓
Observed/referenced work
    ↓
Candidate transformation
    ↓
Candidate process
    ↓
Semantic evaluation
    ↓
Canonical / specialization / other disposition
```

---

8. Lifecycle Process Discovery Dimensions

Every Lifecycle Stage shall be evaluated against the following dimensions.

8.1 Trigger

What event causes the work to begin?

Examples:

* approved decision;
* readiness threshold reached;
* service approved for launch;
* retirement decision;
* contract expiry;
* replacement available;
* regulatory requirement;
* performance threshold;
* customer request.

A candidate without a meaningful trigger shall not normally qualify as a Business Process.

---

8.2 Input

What information, object, decision, capability, obligation or state enters the process?

---

8.3 Transformation

What materially changes?

This is the central discovery question.

A candidate must demonstrate an enterprise transformation rather than merely describe:

* a state;
* a subject area;
* a responsibility;
* an organizational unit;
* an ECF coordinate;
* a capability;
* a policy.

---

8.4 Outcome

What stable result does the process produce?

The outcome must be observable or logically determinable.

Examples:

* service is accepted into operation;
* customer relationship is established;
* obsolete asset is decommissioned;
* responsibility is transferred;
* contractual obligation is closed;
* data is retained or disposed according to policy.

---

8.5 Actors / Responsibility

Who or what performs, governs or participates in the work?

This shall not be confused with organizational ownership.

---

8.6 Controls

What policies, approvals, risks, compliance obligations or decision rights constrain the process?

---

8.7 Evidence

What evidence demonstrates that the process is real, repeatable and semantically stable?

Evidence may include:

* authoritative enterprise process models;
* recognized industry process models;
* standards;
* regulatory processes;
* operating-model documentation;
* multiple independent enterprise implementations;
* existing OpenDEA catalog evidence;
* authoritative reference architectures;
* established business-process literature.

---

8.8 Boundary

Where does the process begin and end?

A candidate without a defensible boundary shall remain a candidate rather than being admitted canonically.

---

9. Canonical Process Evaluation Test

A candidate shall be evaluated against the following tests.

BP-LIFE-001: Process Reality Test

The candidate must represent actual or established enterprise work.

Pass condition:

There is evidence that the work is performed, governed, or recognized as a repeatable enterprise responsibility.

---

BP-LIFE-002: Transformation Test

The candidate must transform an input state into an outcome state.

```text
Input / Trigger
       ↓
   Transformation
       ↓
     Outcome
```

A mere classification, state or responsibility fails this test.

---

BP-LIFE-003: Trigger Test

The candidate must have a meaningful initiating condition.

---

BP-LIFE-004: Outcome Test

The candidate must produce a distinguishable outcome.

---

BP-LIFE-005: Boundary Test

The candidate must have a stable beginning and ending boundary.

---

BP-LIFE-006: Semantic Identity Test

The candidate must satisfy the repository's existing process identity contract:

Verb
Object
Scope
Trigger
Outcome
Evidence

The candidate must not rely on its ECF coordinate to establish identity.

---

BP-LIFE-007: Cross-Context Stability Test

The candidate shall be tested across multiple relevant contexts.

The question is:

Does the underlying enterprise transformation remain semantically recognizable when the domain or implementation changes?

The implementation may vary.

The semantic identity must remain sufficiently stable.

---

BP-LIFE-008: Domain Independence Test

A candidate is stronger when its semantic identity remains valid across multiple enterprise domains.

This does not mean that every canonical process must be universal.

The test distinguishes:

Cross-domain canonical process

from:

Domain-specific specialization

---

BP-LIFE-009: ECF Independence Test

The candidate's identity must survive removal of its ECF coordinate.

If:

"Activate Technology"

only makes sense because the word Activate comes from the ECF, it is probably not a process identity.

If:

"Transition Technology Service to Operation"

has a recognizable business transformation independent of the ECF label, it is a stronger candidate.

---

BP-LIFE-010: Duplication Test

The candidate must not duplicate an existing canonical process.

The evaluation must search:

* same verb/object;
* equivalent transformation;
* equivalent trigger/outcome;
* existing specialization;
* existing cross-stage process;
* existing process with different naming.

---

BP-LIFE-011: Composition Test

The candidate must be evaluated against existing L1/L2/L3 structures.

The question is:

Is this actually a Business Process, a Process Group, an Activity, or a Task?

This prevents process inflation.

---

BP-LIFE-012: Capability Distinction Test

The candidate must not simply restate a Business Capability.

Capability = ability
Process = transformation / work

A candidate such as:

"Service Management"

may represent a capability or process family.

A candidate such as:

"Resolve Service Incident"

is more clearly process-oriented.

---

BP-LIFE-013: Governance Distinction Test

A policy, decision, approval or control shall not automatically be treated as a Business Process.

However, if a repeatable governance workflow exists with trigger, transformation and outcome, it may qualify.

---

BP-LIFE-014: Lifecycle-Span Test

The candidate shall be evaluated across all lifecycle stages in which it participates.

The catalog shall prefer:

one canonical process
+
multiple lifecycle relationships

over:

duplicate process per lifecycle stage

when semantic identity remains stable.

---

10. Canonicality Scoring

For practical discovery, each candidate should be assessed across five dimensions.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Process Reality | speculative | limited evidence | established |
| Semantic Stability | variable | partially stable | highly stable |
| Cross-Domain Applicability | single domain | several related domains | broad |
| Boundary Clarity | unclear | workable | strong |
| Evidence Strength | weak | moderate | authoritative/multiple |

Maximum:

10 points

Suggested interpretation:

| Score | Disposition |
|---|---|
| 8-10 | Strong canonical candidate |
| 6-7 | Candidate requiring review |
| 4-5 | Prefer specialization/pattern/defer |
| 0-3 | Reject as canonical process |

The score is decision support, not an automatic admission mechanism.

Human/catalog governance remains authoritative.

---

11. Process Pattern Evaluation

A recurring transformation may be highly reusable without being appropriate as one concrete Business Process.

Therefore candidates shall additionally be tested for:

Pattern Test A: Stable transformation

Does the underlying transformation recur?

Pattern Test B: Variable implementation

Do domain implementations differ materially?

Pattern Test C: Stable outcome

Does the resulting enterprise outcome remain substantially equivalent?

Pattern Test D: Specialization opportunity

Can the pattern provide a meaningful parent for specialized processes?

If all four are satisfied, record the candidate as a Process Pattern and determine whether:

1. a canonical parent process is appropriate;
2. domain-specific specializations should be created;
3. the pattern should remain informative only.

---

12. Activate Discovery Profile

Activate shall be evaluated as a lifecycle transition into an operationally valid state.

Candidate discovery shall consider, without presuming adoption:

* readiness validation;
* acceptance;
* deployment;
* cutover;
* operational handover;
* ownership transfer;
* service commencement;
* production authorization;
* stabilization;
* stakeholder/customer transition;
* migration into the target operating environment.

Potential canonical candidates include:

Transition to Service

Potential semantic structure:

Trigger:
Approved object is ready for operational transition.
Input:
Validated product/service/capability/system/facility.
Transformation:
Move the object from prepared state into operational service
with required ownership, controls and operational readiness.
Outcome:
Object is accepted into operational service.

Accept into Operation

Potentially a specialization or alternative formulation where acceptance itself represents the stable enterprise transformation.

Deploy / Cut Over

Potentially canonical in some contexts but must be tested against Build, Activate and Operate boundaries.

The repository shall not automatically admit these candidates.

They must pass the full evaluation.

---

13. Retire Discovery Profile

Retire shall be evaluated as a controlled transition out of an existing enterprise state or service relationship.

Candidate discovery shall consider:

* retirement decision;
* dependency analysis;
* migration;
* transition;
* customer/user communication;
* responsibility transfer;
* access withdrawal;
* decommissioning;
* asset recovery;
* contractual closure;
* data retention;
* archival;
* disposal;
* residual obligation resolution.

Potential candidates include:

Transition Out of Service

Trigger:
Approved retirement decision.
Input:
Active enterprise object/service.
Transformation:
Move the object from operational use toward controlled exit.
Outcome:
Object is no longer operationally relied upon.

Decommission

Potentially a distinct canonical process if its transformation and boundaries are sufficiently stable.

Close Enterprise Obligation

Potentially a broader cross-domain candidate but requires careful boundary testing.

Again, no candidate is admitted solely because it belongs to Retire.

---

14. Special Activate/Retire Rule

Activate and Retire shall receive enhanced discovery scrutiny, not automatic process creation and not automatic process exclusion.

The governing rule is:

Lifecycle-boundary stages are presumed worthy of investigation because state transitions frequently create repeatable cross-domain enterprise work; they are not presumed to contain canonical processes.

This establishes a neutral architectural position.

---

15. Process Absence Test

A Process Context may legitimately have no canonical Business Process.

However, the following must be recorded before declaring the Context process-empty:

1. Context concerns were identified;
2. candidate processes were considered;
3. adjacent Contexts were reviewed;
4. existing canonical processes were searched;
5. lifecycle-spanning processes were considered;
6. capability/process distinctions were tested;
7. process-pattern candidates were considered;
8. evidence was assessed;
9. the reason for non-admission was recorded.

The valid conclusion is therefore:

No canonical Business Process identified after evaluation.

Not:

No process exists because this lifecycle stage is Activate/Retire.

---

16. Disposition Model

Every candidate shall receive one of the following dispositions.

ADMIT-CANONICAL

The candidate satisfies the canonical process tests.

---

ADMIT-SPECIALIZATION

The candidate is a semantic refinement of an existing canonical process.

---

ADMIT-CROSS-STAGE

The candidate is canonical but participates in multiple Lifecycle Stages.

---

RECORD-PATTERN

The transformation is reusable, but the implementation should remain represented through specialized processes.

---

DEFER

Evidence is insufficient to establish canonicality.

---

MERGE

The candidate duplicates or overlaps an existing process.

---

RECLASSIFY

The candidate is actually:

* Capability;
* Process Group;
* Activity;
* Governance construct;
* lifecycle state;
* policy;
* decision;
* other semantic entity.

---

REJECT

The candidate fails the process identity or semantic tests.

---

17. Required Discovery Record

Each lifecycle discovery exercise shall produce a machine-readable or structured record containing:

```yaml
discovery:
  id:
  ecf_context:
    domain:
    lifecycle_stage:
  candidate:
    name:
    proposed_identity:
      verb:
      object:
      scope:
    trigger:
    inputs:
    transformation:
    outcome:
    boundary:
    actors:
    controls:
  evidence:
    sources: []
    evidence_strength:
  evaluation:
    process_reality:
    transformation:
    trigger:
    outcome:
    boundary:
    semantic_identity:
    cross_context_stability:
    cross_domain_applicability:
    ecf_independence:
    duplication:
    composition:
    capability_distinction:
    governance_distinction:
    lifecycle_span:
  scoring:
    total:
    rationale:
  disposition:
    type:
    canonical_process_ref:
    specialization_of:
    related_contexts: []
  rationale:
    included:
    excluded:
    unresolved:
```

---

18. Required Discovery Workflow

The normative workflow is:

```text
1. Select ECF Process Context
          ↓
2. Define context boundary
          ↓
3. Identify enterprise concerns
          ↓
4. Identify recurring work
          ↓
5. Identify transformations
          ↓
6. Generate candidate processes
          ↓
7. Search existing catalog
          ↓
8. Test existing process reuse
          ↓
9. Evaluate process identity
          ↓
10. Evaluate cross-domain stability
          ↓
11. Evaluate lifecycle span
          ↓
12. Evaluate specialization
          ↓
13. Evaluate process-pattern status
          ↓
14. Score / review evidence
          ↓
15. Assign disposition
          ↓
16. Update catalog / defer / reject
```

---

19. Relationship to Existing Catalog Architecture

CR-BP-62 does not replace the existing architecture.

It strengthens the existing flow:

```text
ECF Domain × Lifecycle
          ↓
Process Context
          ↓
Process Group
          ↓
Business Process
          ↓
Activity
```

The new discovery layer becomes:

```text
ECF Context
     ↓
Process Discovery
     ↓
Candidate
     ↓
Evaluation
     ↓
Disposition
     ↓
Canonical Process Architecture
```

This preserves the distinction between context and process.

---

20. Contribution and CI Integration

The existing contribution-driven re-landscape mechanism shall remain authoritative.

CR-BP-62 adds the following expectations to the contribution process:

A contribution proposing a lifecycle-boundary process shall identify:

1. ECF Context(s);
2. process identity;
3. trigger;
4. outcome;
5. transformation;
6. boundary;
7. evidence;
8. cross-domain applicability;
9. existing-process search;
10. lifecycle-span assessment;
11. specialization assessment;
12. discovery disposition.

CI should validate structural completeness where practical.

CI should not automatically admit or reject canonicality solely from the score.

The contribution report should surface:

Candidate
Context
Evidence
Evaluation
Potential duplicates
Potential parent process
Potential lifecycle span
Suggested disposition

Catalog maintainers remain responsible for final canonical admission.

---

21. Conformance Rules

The following rules are introduced.

BP-LIFE-001

Every lifecycle discovery must begin from a Process Context rather than a process name.

BP-LIFE-002

An ECF Context shall not automatically generate a Business Process.

BP-LIFE-003

A candidate must demonstrate a transformation.

BP-LIFE-004

A candidate must have a trigger.

BP-LIFE-005

A candidate must have a distinguishable outcome.

BP-LIFE-006

A candidate must have a defensible boundary.

BP-LIFE-007

A candidate must satisfy the existing process identity contract.

BP-LIFE-008

Existing canonical processes must be searched before creating a new process.

BP-LIFE-009

Lifecycle-spanning candidates must not be duplicated solely because they cross Lifecycle Stages.

BP-LIFE-010

Domain-specific manifestations shall be represented through specialization where appropriate.

BP-LIFE-011

Process Patterns may be recorded without automatically becoming Business Processes.

BP-LIFE-012

Activate and Retire shall undergo explicit candidate discovery.

BP-LIFE-013

No lifecycle stage shall be presumed process-empty solely from its name or lifecycle semantics.

BP-LIFE-014

A process-empty Context shall retain a documented discovery rationale.

BP-LIFE-015

Canonical admission requires evidence sufficient to support semantic stability.

---

22. Acceptance Criteria

CR-BP-62 is complete when:

* [ ] a normative lifecycle process-discovery method exists;
* [ ] the distinction between Context and Process remains explicit;
* [ ] canonical-process admission criteria are defined;
* [ ] Process Pattern evaluation is defined;
* [ ] cross-domain applicability is defined;
* [ ] lifecycle-spanning process treatment is defined;
* [ ] duplicate detection is defined;
* [ ] specialization treatment is defined;
* [ ] process absence requires documented evaluation;
* [ ] Activate has an explicit discovery profile;
* [ ] Retire has an explicit discovery profile;
* [ ] contribution records can capture discovery evidence;
* [ ] CI can validate structural discovery requirements where practical;
* [ ] canonical admission remains governed rather than automatically generated;
* [ ] no requirement exists to populate every ECF cell.

---

23. Expected Initial Research Candidates

CR-BP-62 should initiate, but not predetermine, investigation of at least the following candidate patterns.

Activate

| Candidate | Initial hypothesis |
|---|---|
| Transition to Service | Strong canonical candidate |
| Accept into Operation | Possible specialization / canonical candidate |
| Deploy / Cut Over | Requires Build/Activate boundary analysis |
| Mobilize Capability | Requires domain-independence testing |
| Commence Service | Possible specialization |
| Transfer to Operational Ownership | Potentially cross-domain |

Retire

| Candidate | Initial hypothesis |
|---|---|
| Transition Out of Service | Strong canonical candidate |
| Decommission | Strong candidate; requires boundary analysis |
| Migrate / Transfer | Potential cross-stage/cross-domain candidate |
| Close Enterprise Relationship | Requires semantic boundary analysis |
| Recover / Reclaim | Potential specialization |
| Resolve Residual Obligations | Potential cross-domain candidate |

These are discovery hypotheses, not catalog decisions.

---

24. Expected Architectural Outcome

The expected result is not:

Activate = processes
Retire   = processes

Nor:

Activate = no processes
Retire   = no processes

The desired model is:

```text
                 ECF Lifecycle Context
                         │
                         ▼
                 Evidence-based
                  Process Discovery
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
          Canonical   Pattern     No Canonical
           Process                Process
             │           │             │
             ▼           ▼             ▼
        Reusable      Specialized   Documented
        enterprise    processes     absence
        semantics
```

This makes the catalog discovery-driven rather than matrix-driven.

---

25. Architectural Rationale

The principal rationale for CR-BP-62 is:

The ECF is a contextual architecture, not a process taxonomy. Therefore process existence cannot be inferred from coordinates. Conversely, process absence cannot be inferred from coordinates either.

Activate and Retire are particularly important because they represent enterprise state transitions.

State transitions frequently generate recurring work involving:

* readiness;
* acceptance;
* authorization;
* deployment;
* handover;
* migration;
* withdrawal;
* decommissioning;
* recovery;
* closure;
* residual obligation management.

These activities may not always constitute canonical Business Processes. But their transitional nature is insufficient grounds for excluding them.

The correct architectural treatment is therefore evidence-based discovery followed by semantic evaluation.

---

26. Design Principle Established by CR-BP-62

CR-BP-62 establishes the following reusable OpenDEA principle:

Context Does Not Imply Process -- and Context Does Not Exclude Process.

An ECF coordinate establishes where a responsibility is examined.

Process architecture establishes what repeatable enterprise transformation occurs.

Canonical process status is determined by:

semantic identity
+
transformation
+
trigger
+
outcome
+
boundary
+
evidence
+
reusability
+
non-duplication

not by:

ECF coordinate

This principle shall apply to all current and future ECF Lifecycle Stages.
---

## Annex A. Author's Implementation Recommendation

I would make CR-BP-62 a governance/discovery CR first, rather than immediately adding Transition to Service or Decommission to the canonical catalog.

That gives a much stronger sequence:

```text
CR-BP-62 -> establish discovery/evaluation machinery -> execute discovery -> admit only proven candidates.
```

It also fits the repository's existing contribution-driven model, where a new process is proposed and reviewed rather than automatically inserted into the canonical landscape.

The particularly important refinement is the new distinction between canonical process, process pattern, and specialization. That prevents the Activate/Retire debate from becoming a binary argument. It allows the catalog to discover something like Transition to Service as a stable semantic pattern while still determining whether the canonical L2 process should be generic or whether the actual canonical records should be specialized.

CR-BP-63 is the actual Activate/Retire discovery exercise, applying this CR mechanically across the relevant 14 ECF contexts and producing an evidence-backed disposition for every candidate. That gives a defensible answer to the original question rather than merely an architectural opinion.

---

## 27. Slice Landing Surface (CR-BP-62)

This CR lands as the governance/discovery slice: the normative method plus the structural machinery, with zero discovery records and zero catalog record changes.

| Path | Status | Notes |
|---|---|---|
| `change-requests/CR-BP-62-lifecycle-process-discovery.md` | NEW | This normative specification |
| `schemas/discovery/lifecycle-discovery.schema.json` | NEW | JSON Schema for the section-17 discovery record |
| `scripts/check_lifecycle_discovery.py` | NEW | Structural validator (DISC-001..008); CLI `--self-test` / `--strict` / `--json` |
| `scripts/check_documentation_conformance.py` | MOD | DOC-003 compound allowlist extended with this CR's defined terms (Candidate Process, Canonical Process, Specialized Process, Process Pattern, Process Absence, Lifecycle-Spanning Process; sections 6.3-6.7, 11, 15) |
| `tests/test_check_lifecycle_discovery.py` | NEW | Rule-level + CLI tests |
| `scripts/conformance_result.py` | MOD | Advisory gate [19] wired |
| `.github/workflows/ci.yml` | MOD | Discovery gate step added |
| `README.md` | MOD | Discovery doctrine noted in the decomposition section |
| `docs/architecture.md` | MOD | Discovery layer added to the structural architecture |
| `change-requests/README.md` | MOD | CR-BP-62 row |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 74 -> 75 |

Discovery records (section 17) live at `discovery/v1-alpha/<domain-slug>-<stage-slug>.yaml`, one record per discovery exercise per ECF context. The directory is introduced by this slice and populated by CR-BP-63. The schema generalizes section 17's single-candidate sketch to `candidates[]` (an exercise evaluates the whole candidate universe for the context) and promotes the section-15 process-absence checklist to a required `context_evaluation` block; no evaluation dimension is added or removed.

Machine-checkable structural rules (DISC-001..008) operationalize what CI can honestly verify of BP-LIFE-001..015:

| Rule | Predicate |
|---|---|
| DISC-001 | Record validates against `schemas/discovery/lifecycle-discovery.schema.json` |
| DISC-002 | `ecf_context.domain` and `ecf_context.lifecycle_stage` resolve to the canonical ECF vocabulary |
| DISC-003 | `candidate.proposed_identity` carries a non-empty `verb` and `object` (identity contract, BP-LIFE-006/007 structural face) |
| DISC-004 | `disposition.type` is one of the eight section-16 dispositions |
| DISC-005 | Disposition-conditional rationale: REJECT/DEFER/RECLASSIFY require `rationale.excluded` or `rationale.unresolved`; ADMIT-CANONICAL requires `disposition.canonical_process_ref`; ADMIT-SPECIALIZATION requires `disposition.specialization_of` |
| DISC-006 | ADMIT-CANONICAL requires non-empty `evidence.sources` (BP-LIFE-015 structural face) |
| DISC-007 | ADMIT-CANONICAL candidate name must not duplicate an existing canonical BP record name (BP-LIFE-008/010 structural face) |
| DISC-008 | `scoring.total` is an integer 0-10 with all five section-10 dimensions scored |

The gate lands advisory (False) in `conformance_result.py`, consistent with section 20: CI validates structural completeness; it never admits or rejects canonicality.

## 28. Next Slice (CR-BP-63): Activate/Retire Discovery Exercise

CR-BP-63 applies this method mechanically across the 14 backlog-deferred Activate/Retire ECF contexts (7 domains x 2 stages), producing one discovery record per context with evidence-backed dispositions for the section-12/13/23 candidate hypotheses. That exercise replaces the register's uniform deferral rationale with per-cell documented evaluation outcomes, per section 15: a process-empty Context retains a documented discovery rationale.

## 29. Coverage on the Live Catalog

Zero discovery records exist at landing: the validator is a regression guard (0 records checked, 0 findings). The gate becomes exercised by CR-BP-63's 14 records. Record counts unchanged (ACT 501 / EXE 662 / report 697). Gate count becomes 23 -> 24 (10 blocking + 14 advisory). Advisory documentation-gate accounting: living docs (README.md, docs/) carry zero new DOC findings from this slice; the CR file itself carries 3 DOC-003 advisories on its definitional statements (the section-26 principle sentence and the section-9 capability/process equation), accepted as deliberate normative language.

## 30. What This CR Is NOT (additions to section 5)

- NOT an admission of any Activate/Retire process. No candidate listed in sections 12/13/23 is admitted by this CR.
- NOT a register reversal. The L1 register's backlog-deferred disposition stands until CR-BP-63's evidence-backed outcomes justify per-cell changes via the contribution flow.
- NOT a specialization authorization. Specialization work remains unauthorized per program governance until L0-L4 is stabilized in the universal sense; section 16's ADMIT-SPECIALIZATION disposition is a recording construct, not a license to create specialization records.
- NOT an L4 pivot. The decomposition scope remains L3; L4 awaits the metamodel-owned `dea:Task`.
- NOT a count-assertion change. ACT/EXE/report counts are untouched.
