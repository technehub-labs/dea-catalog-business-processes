
> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.
The next CR should now operationalize CR-BP-14 rather than introduce another semantic concept. CR-BP-15 should reconcile the existing catalog against the newly established semantic contract, while preserving traceability and avoiding destructive edits.

CR-BP-15 — Process Catalog Reconciliation

**Status**: Accepted
**Layer**: L1
**Owner**: TechNeHub Labs
**Type**: Architectural Reconciliation / Catalog Governance
**Scope**: dea-catalog-processes
**Depends On**: CR-BP-14 — Process Semantic Reconciliation
**Precedes**: CR-BP-13A and subsequent Process Admission CRs

⸻

1. Purpose

Reconcile all existing canonical Process Catalog records against the semantic contract established by CR-BP-14.

The objective is to ensure that the existing catalog is:

* semantically coherent;
* non-duplicative;
* consistently classified;
* correctly contextualized;
* correctly specialized;
* structurally conformant;
* traceable to its evidence and governing decisions;
* suitable for continued canonical admission.

This CR is a catalog reconciliation, not a catalog expansion.

No new ECF-derived Process tranche SHALL be admitted as canonical under this CR.

⸻

2. Architectural Principle

CR-BP-15 establishes:

The canonical catalog is governed as a coherent architecture, not as an accumulation of individually acceptable process records.

Therefore, a process SHALL NOT remain canonical merely because it individually passes schema validation.

It must also fit correctly within:

Process Context
      ↓
Process Scope
      ↓
Process Group
      ↓
Business Process
      ↓
Intent
      ↓
Classification
      ↓
Specialization
      ↓
Relationships
      ↓
Sibling Boundary

⸻

3. Reconciliation Scope

The reconciliation SHALL cover all currently canonical records in:

entities/
schemas/
classifications/
contexts/
groups/
research/
contributions/

and any other directory containing records participating in the canonical catalog.

The reconciliation SHALL include, at minimum:

1. Process Contexts;
2. Process Scopes;
3. Process Groups;
4. Business Processes;
5. Process Intent;
6. Process Classification;
7. Process Specialization;
8. Process Audience;
9. Process Relationships;
10. canonical identifiers;
11. decomposition references;
12. evidence references;
13. ECF coordinates;
14. cross-references;
15. README and architectural documentation.

⸻

4. Reconciliation Is Not Renaming

A naming correction SHALL NOT automatically be treated as a semantic correction.

The reconciliation SHALL distinguish:

Name Problem
    ≠
Identity Problem
    ≠
Classification Problem
    ≠
Specialization Problem
    ≠
Boundary Problem

A process may therefore retain its canonical identity while its:

* name;
* intent;
* classification;
* contextual relationship;
* description

is corrected.

A new process identity SHALL be introduced only where the underlying semantic unit of work has materially changed.

⸻

5. Reconciliation Outcomes

Every existing canonical record SHALL receive exactly one primary disposition:

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

These dispositions SHALL be mutually exclusive as the primary outcome, although an implementation MAY record secondary corrective actions.

⸻

6. RETAIN

Use RETAIN when the record:

* represents a valid Business Process;
* has a stable identity;
* has appropriate decomposition;
* has a valid Context;
* has valid Intent;
* has valid Classification;
* has valid Specialization where applicable;
* does not materially overlap a sibling;
* has adequate evidence.

A retained record SHALL require no semantic change.

Minor documentation corrections MAY still be applied.

⸻

7. RENAME

Use RENAME when:

* the underlying process identity remains valid;
* the current name does not accurately express the process;
* the new name better follows the canonical naming contract.

Example:

Current:
Customer Management
Candidate:
Manage Customer Relationship

A rename SHALL preserve the canonical identifier unless the identity itself changes.

⸻

8. RECLASSIFY

Use RECLASSIFY when the Business Process is valid but its Process Classification is incorrect.

Example:

process_intent: manage
process_classification: support

may be correct for an internal workforce process even though its intent is manage.

The reconciliation SHALL never change Intent merely to make it agree lexically with Classification.

⸻

9. RECONTEXTUALIZE

Use RECONTEXTUALIZE when the process is valid but its relationship to:

* Process Context;
* ECF Domain;
* Lifecycle Stage

is incomplete or incorrect.

This disposition SHALL also be used where process_audience is incorrectly being used as a substitute for Process Context.

Target state:

context:
  - ref: <process-context>
relationships:
  - relationship_type: serves
    target: <ecf-domain>

The process MAY have multiple contextual relationships where justified by evidence.

⸻

10. RESPECIALIZE

Use RESPECIALIZE where:

* the parent process is incorrect;
* specialization direction is reversed;
* specialization is too broad;
* specialization is actually a contextual relationship;
* the process has been incorrectly modeled as independent when it is semantically a specialization.

The specialization hierarchy SHALL represent semantic refinement rather than organizational decomposition.

Example:

Manage Customer Relationship
        │
        ├── Manage Enterprise Customer Relationship
        └── Manage Consumer Customer Relationship

A process SHALL NOT be made a specialization merely because it happens to operate in the same organizational area as another process.

⸻

11. MERGE

Two or more processes SHALL be merged where evidence establishes that they represent the same semantic unit of work.

Indicators include:

* identical outcome;
* materially identical boundary;
* materially identical trigger;
* materially identical object;
* no meaningful specialization distinction;
* duplication caused by ECF coordinate generation;
* duplication caused by terminology differences.

The surviving record SHALL retain canonical identity where possible.

The merge SHALL preserve:

* source provenance;
* historical identifiers;
* evidence;
* superseded relationships;
* affected references.

No provenance SHALL be lost.

⸻

12. SPLIT

A process SHALL be split where one existing record contains multiple independently coherent units of work.

Indicators include:

* materially different triggers;
* materially different outcomes;
* independent ownership;
* distinct lifecycle behavior;
* distinct inputs/outputs;
* different specialization patterns;
* inability to describe a single coherent process boundary.

A split SHALL create new canonical identities only after each resulting process independently satisfies the Process Identity Contract.

⸻

13. MOVE

Use MOVE when the process itself remains valid but belongs under a different:

* Process Scope;
* Process Group;
* Process Context.

A move SHALL NOT automatically create a new Business Process identity.

This reinforces:

Architectural location is not Process Identity.

⸻

14. DEFER

Use DEFER where the candidate has insufficient evidence or unresolved architectural ambiguity.

Examples:

* unclear Process boundary;
* uncertain distinction from another process;
* unresolved specialization;
* insufficient evidence;
* unresolved Context;
* unresolved classification.

Deferred records SHALL remain traceable but SHALL NOT be presented as canonical.

⸻

15. RETIRE

Use RETIRE where the record is demonstrated to be:

* obsolete;
* duplicate with no remaining independent semantic value;
* outside the catalog specialization;
* invalid under the current ontology;
* superseded by a canonical process.

Retired records SHALL remain historically traceable.

They SHALL NOT be physically deleted merely because they are no longer canonical.

⸻

16. Business Process Identity Reconciliation

Every existing Business Process SHALL be evaluated using the identity contract:

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
Boundary

The review SHALL determine whether the record describes one coherent unit of work.

The following SHALL be treated as warning indicators:

* noun-only names;
* department names;
* capability names;
* product names without process semantics;
* ECF cell names;
* overly broad enterprise responsibilities;
* compound processes containing multiple independent outcomes.

⸻

17. Intent Reconciliation

Every canonical Business Process SHALL receive exactly one primary Process Intent unless the schema explicitly establishes a justified multi-intent mechanism.

The approved vocabulary from CR-BP-14 is:

govern
manage
operate
deliver
support
develop
transform

Intent SHALL be determined from the process meaning.

It SHALL NOT be inferred from:

* Process Classification;
* Process Group;
* ECF Domain;
* organizational owner;
* process name alone.

⸻

18. Classification Reconciliation

Every canonical Business Process SHALL receive the appropriate Process Classification:

strategic
management
core
support
standardization

Classification SHALL be evaluated independently of Intent.

The reconciliation SHALL specifically identify cases where:

process_intent == process_classification

because lexical equality may indicate overlap in the model.

However:

Lexical equality is a review signal, not an automatic validation failure.

For example:

process_intent: support
process_classification: support

may be legitimate if evidence shows that the process is both supportive in purpose and supportive in landscape position.

⸻

19. Context Reconciliation

Each Business Process SHALL be evaluated against its Process Context.

The reconciliation SHALL determine:

1. whether the Context exists;
2. whether the ECF coordinate is valid;
3. whether the process genuinely belongs in that context;
4. whether multiple contexts are required;
5. whether process_audience has been incorrectly used to represent Context.

The ECF coordinate SHALL be treated as contextual evidence, not as proof of process existence.

⸻

20. Process Group Reconciliation

Each Process Group SHALL be evaluated against:

Process Scope
     ↓
Process Group
     ↓
Business Processes

The review SHALL verify:

* coherent grouping rationale;
* non-overlapping sibling Groups;
* appropriate child processes;
* absence of Business Functions masquerading as Process Groups;
* absence of capabilities masquerading as Process Groups;
* absence of generic organizational categories masquerading as Process Groups.

A Process Group SHALL exist to organize related processes, not merely to provide a convenient folder.

⸻

21. Decomposition Reconciliation

The canonical decomposition remains:

L0 — Process Scope
L1 — Process Group
L2 — Business Process
L3 — Activity
L4 — Task

Every existing record SHALL be checked against this hierarchy.

The reconciliation SHALL specifically detect:

Capability → Process
Function → Process
Process Group → Business Process
Activity → Business Process
Task → Business Process
ECF Cell → Business Process

misclassification.

No alternative decomposition hierarchy SHALL be introduced through this CR.

⸻

22. Sibling Boundary Analysis

The reconciliation SHALL evaluate neighboring Business Processes for overlap.

For each Process Group:

Business Process A
Business Process B
Business Process C
...

the review SHALL assess:

* trigger;
* object;
* transformation;
* outcome;
* boundary;
* responsibility;
* specialization.

The objective is not artificial exclusivity.

The objective is:

Every canonical sibling should have a defensible semantic reason for existing independently.

⸻

23. MECE Assessment

The catalog SHALL apply MECE at the appropriate architectural level.

Mutually Exclusive

Sibling processes SHALL have sufficiently distinguishable responsibilities.

Collectively Exhaustive

A Process Group SHOULD provide meaningful coverage of its declared scope.

However:

MECE SHALL NOT be interpreted as requiring every ECF coordinate to contain a process.

An empty coordinate is legitimate where no distinct process is warranted.

⸻

24. ECF Coverage Reconciliation

The reconciliation SHALL distinguish:

ECF Coverage
      ≠
Process Completeness

A Process Context MAY contain:

* multiple processes;
* one process;
* no canonical process;
* deferred candidates.

The existence of an ECF coordinate SHALL never be used as evidence that a missing process must be created.

⸻

25. Evidence Reconciliation

Each canonical record SHALL have sufficient provenance to answer:

Why does this process exist?
Why is it named this way?
Why is it classified this way?
Why is it in this Context?
Why is it separate from its siblings?
Why does it specialize its parent?

Evidence MAY originate from:

* authoritative semantic models;
* accepted industry references;
* research findings;
* domain analysis;
* approved contributions;
* architectural reasoning.

Research SHALL support admission but SHALL NOT automatically create canonical records.

⸻

26. Provenance Preservation

When a record is:

* renamed;
* merged;
* split;
* moved;
* retired;
* specialized;

the repository SHALL preserve its historical provenance.

The preferred pattern is:

provenance:
  predecessor:
    - <identifier>
  supersedes:
    - <identifier>
  derived_from:
    - <identifier>

The exact schema SHALL follow the repository’s established provenance model.

Historical identifiers SHALL remain resolvable where technically practical.

⸻

27. Canonical Identity Stability

The reconciliation SHALL prefer correction over identity churn.

Therefore:

Wrong classification
       ↓
Correct classification

rather than:

Wrong classification
       ↓
Delete process
       ↓
Create replacement

unless the underlying process identity has actually changed.

This principle is critical for downstream consumers.

⸻

28. Machine-Readable Reconciliation Register

The implementation SHALL introduce a reconciliation register.

Recommended structure:

reconciliation_id: BP-REC-XXXX
subject:
  type: BusinessProcess
  id: <canonical-id>
current_state:
  name: <current-name>
  intent: <current-intent>
  classification: <current-classification>
  context: <current-context>
  specialization: <current-specialization>
assessment:
  identity: pass|review|fail
  boundary: pass|review|fail
  intent: pass|review|fail
  classification: pass|review|fail
  context: pass|review|fail
  specialization: pass|review|fail
  evidence: pass|review|fail
  mece: pass|review|fail
disposition:
  action: retain|rename|reclassify|recontextualize|respecialize|merge|split|move|defer|retire
rationale: <required>
evidence:
  - <reference>
approved_by:
  - <governance-reference>

The exact implementation MAY differ, but the semantic information SHALL be preserved.

⸻

29. Reconciliation Matrix

The implementation SHALL generate a machine-readable and human-readable reconciliation matrix.

Minimum columns:

Field	Required
Current ID	Yes
Current Name	Yes
Level	Yes
Parent	Yes
Process Context	Yes
Current Intent	Yes
Target Intent	Yes
Current Classification	Yes
Target Classification	Yes
Current Specialization	Yes
Target Specialization	Yes
Disposition	Yes
Rationale	Yes
Evidence	Yes
Affected References	Yes
Approval State	Yes

⸻

30. Validation Gate

CI SHALL validate the reconciled catalog.

At minimum:

BP-REC-001  Canonical ID uniqueness
BP-REC-002  Valid process level
BP-REC-003  Valid parent reference
BP-REC-004  Valid Process Context
BP-REC-005  Valid Process Intent
BP-REC-006  Valid Process Classification
BP-REC-007  Valid Specialization reference
BP-REC-008  No invalid specialization cycles
BP-REC-009  Referential integrity
BP-REC-010  Legacy field detection
BP-REC-011  Provenance integrity
BP-REC-012  Required evidence
BP-REC-013  Reconciliation disposition
BP-REC-014  Retired record protection
BP-REC-015  Canonical naming conformance

Warnings MAY be generated for:

* lexical Intent/Classification overlap;
* potentially duplicate names;
* unusually broad process boundaries;
* multiple Contexts;
* missing optional relationships.

Warnings SHALL NOT automatically fail CI unless the governance policy explicitly promotes the warning to an error.

⸻

31. Documentation Reconciliation

The reconciliation SHALL update:

README.md
docs/architecture.md
docs/identity.md
docs/classification.md
docs/context.md
docs/specialization.md
docs/reconciliation.md

The documentation SHALL consistently represent:

OpenDEA Process Kernel
        ↓
Business Process Specialization
        ↓
Canonical Business Process Catalog

No superseded architecture SHALL remain presented as normative.

⸻

32. Repository Status Model

The repository SHALL distinguish:

Candidate
Research
Proposed
Canonical
Deferred
Retired
Superseded

A record in Canonical status SHALL have passed the applicable reconciliation and admission gates.

A research candidate SHALL NOT appear indistinguishably alongside canonical processes.

⸻

33. Admission Gate

Following CR-BP-15, a candidate Business Process SHALL pass:

Research Evidence
       ↓
Semantic Identity
       ↓
Process Context
       ↓
Process Group Fit
       ↓
Boundary Test
       ↓
Intent
       ↓
Classification
       ↓
Specialization
       ↓
MECE Review
       ↓
Schema Validation
       ↓
Governance Approval
       ↓
CANONICAL

This becomes the standard admission pattern for CR-BP-13A and all subsequent admission CRs.

⸻

34. No Automatic ECF Expansion

CR-BP-15 SHALL NOT:

* create a process for every uncovered ECF coordinate;
* treat ECF coverage as a completeness metric by itself;
* manufacture process names from ECF labels;
* promote research candidates automatically;
* create artificial process distinctions solely to achieve coverage.

The canonical catalog SHALL optimize for semantic integrity, not matrix density.

⸻

35. Expected Reconciliation Results

At completion, each existing canonical record SHALL fall into one of the following states:

                    Existing Record
                           │
              ┌────────────┴────────────┐
              │                         │
        Semantically Valid        Requires Action
              │                         │
           RETAIN              ┌────────┴─────────┐
                               │                  │
                         Correctable        Structural
                               │              Change
                         ┌─────┴─────┐       ┌───┴────┐
                         │           │       │        │
                      Rename     Reclassify  Merge   Split
                      Context    Specialize  Move    Retire

No canonical record SHALL remain in an indeterminate state.

⸻

36. Deliverables

Implementation SHALL produce:

1. reconciled canonical entity records;
2. reconciliation register;
3. reconciliation matrix;
4. updated schemas;
5. updated controlled vocabularies;
6. migration handling for legacy fields;
7. CI validation rules;
8. updated architecture documentation;
9. updated README;
10. updated CR register;
11. provenance mappings for changed records;
12. reconciliation report summarizing all dispositions.

⸻

37. Acceptance Criteria

CR-BP-15 is complete only when:

Catalog

* [ ]	Every existing canonical Business Process has been assessed.
* [ ]	Every Process Group has been assessed.
* [ ]	Every Process Context has been assessed.
* [ ]	Every record has a reconciliation disposition.
* [ ]	No unresolved canonical record remains.

Semantics

* [ ]	Intent is distinct from Classification.
* [ ]	Classification is distinct from Context.
* [ ]	Specialization is distinct from decomposition.
* [ ]	Audience is no longer used as an implicit substitute for Context.
* [ ]	Process identity remains stable wherever the semantic unit has not changed.

Architecture

* [ ]	L0–L4 remains the only normative process decomposition.
* [ ]	Process Group remains catalog-owned.
* [ ]	Business Process remains the canonical L2 specialization.
* [ ]	ECF remains contextual rather than generative.

Governance

* [ ]	All merges and splits have documented rationale.
* [ ]	All renames preserve identity where appropriate.
* [ ]	Retired records preserve provenance.
* [ ]	Deferred records remain traceable.
* [ ]	Canonical admission requires evidence and governance approval.

Implementation

* [ ]	Reconciliation register exists.
* [ ]	Reconciliation matrix exists.
* [ ]	CI validates reconciliation invariants.
* [ ]	Referential integrity passes.
* [ ]	Documentation is synchronized with the actual CR state.

⸻

38. Non-Goals

CR-BP-15 SHALL NOT:

* introduce a new process ontology;
* modify the OpenDEA Process kernel;
* expand the ECF;
* populate new ECF coordinates;
* create new Process Groups solely for coverage;
* admit CR-BP-13A candidates;
* define Activity or Task semantics;
* define process execution/workflow semantics;
* redefine Business Capability;
* redefine Business Function.

⸻

39. Relationship to CR-BP-13

CR-BP-13 remains the ratified research baseline.

Its accepted and deferred findings SHALL be preserved.

CR-BP-15 does not invalidate that research.

Instead:

CR-BP-13
Research Ratification
       │
       ▼
CR-BP-14
Semantic Reconciliation
       │
       ▼
CR-BP-15
Existing Catalog Reconciliation
       │
       ▼
CR-BP-13A+
Canonical Admission

This sequence prevents research evidence from being confused with canonical architecture.

⸻

40. Relationship to CR-BP-13A

CR-BP-13A SHALL remain the next Business Process admission tranche after the reconciliation gate.

However, it SHALL be implemented only after CR-BP-15 reaches its acceptance criteria.

CR-BP-13A candidates SHALL then be evaluated against the same semantic and admission contract.

⸻

41. Definitive Governance Rule

CR-BP-15 establishes:

Canonicality is a property of architectural conformance, not merely record existence.

A Business Process becomes canonical only when:

Identity
+
Context
+
Boundary
+
Intent
+
Classification
+
Specialization
+
Evidence
+
Relationships
+
Governance

are sufficiently established and internally coherent.

⸻

42. Decision

Adopt CR-BP-15 as the mandatory reconciliation gate for the existing Business Process Catalog.

CR-BP-15 shall be completed before further canonical process admission.

Following completion, the catalog may resume the CR-BP-13A Party & Relationship admission programme under the reconciled semantic contract.

The resulting architecture establishes a controlled progression:

DEFINE
  ↓
RECONCILE
  ↓
VALIDATE
  ↓
ADMIT
  ↓
EVOLVE

rather than:

RESEARCH
  ↓
ADD PROCESS
  ↓
ADD PROCESS
  ↓
REPAIR ARCHITECTURE

The former SHALL be the governing pattern for the OpenDEA Business Process Catalog.

This gives us the second half of the reconciliation gate. CR-BP-14 defines what the concepts mean; CR-BP-15 determines whether the records already in the repository actually conform to those meanings. Only after that should CR-BP-13A resume.

The particularly important architectural outcome is that we now have a closed governance loop:

research → semantic reconciliation → catalog reconciliation → admission → validation → evolution.

For the next artifact, should I produce  CR-BP-15 implementation decomposition or  CR-BP-16 Conformance Gate?