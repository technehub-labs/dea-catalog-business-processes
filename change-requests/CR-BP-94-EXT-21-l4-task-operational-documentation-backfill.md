# CR-BP-94-EXT-21: L4 Task Operational Documentation Backfill

**Status**: Proposed
**Layer**: Process Catalog (Cross-Cutting Documentation)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-19
**Source CR**: CR-BP-94-EXT-21 (L4 Task Operational Documentation Backfill)
**Parent programme**: CR-BP-94: Process Decomposition and Operational Documentation (DEA-PROCESS-ENRICH-000)
**Repository**: technehub-labs/dea-catalog-business-processes
**Change type**: Catalogue enrichment, decomposition integrity and documentation
**Target decomposition level**: L4: Task
**Priority**: High
**Depends on**: CR-BP-94-EXT-15, CR-BP-94-EXT-16, CR-BP-94-EXT-17, CR-BP-94-EXT-18, CR-BP-94-EXT-19, CR-BP-94-EXT-20
**Enables**: EXT-22 (L0/L1 Context Reconciliation)
**Implementation approach**: Parent readiness, decomposition validation, enrichment, validation and review

---

## 1. Executive summary

This Change Request establishes the systematic operational documentation backfill of L4 Task entities.

L4 Tasks represent bounded, independently understandable units of work within an L3 Activity.

Their documentation must establish:

- What the Task does and why it exists
- Its relationship to the parent L3 Activity
- Its own boundary
- Its trigger and its outcome
- Who performs it
- What evidence supports it
- How it contributes to the parent Activity's purpose

The L4 layer is the most heavily populated layer in the catalogue (2,900 records) and the layer where over-decomposition and phase-pattern rigidity are the principal risks. The backfill must preserve the existing decomposition structure while bringing the L4 layer into the canonical EXT-15/EXT-16 evidence and authoring framework.

---

## 2. Background and rationale

The L2 backfill (EXT-19) establishes the business transformation of the parent processes. The L3 backfill (EXT-20) establishes the Activity purpose, contribution and boundary. The L4 backfill establishes the bounded work units that realise the Activity.

The existing L4 population was deposited under CR-BP-102 using a canonical 5-phase verb-object decomposition pattern. Each L3 Activity carries exactly 5 L4 Tasks, one per phase:

| Phase | Responsibility | Count |
|---|---|---|
| Intake | designated intake custodian | 580 |
| Processing | processing custodian | 580 |
| Verification | verification custodian | 580 |
| Confirmation | confirmation custodian | 580 |
| Record | records custodian | 580 |

The existing L4 records already carry: `definition`, `trigger`, `outcome`, `responsibility` (plain-string form), `boundary` (with `inclusions` and `exclusions`), and `evidence[]` (the pre-EXT-15 form with `source`, `claim`, `strength`).

The EXT-21 work reconciles that existing structure with the canonical framework established by EXT-15 and EXT-16, and validates the decomposition coherence of the 2,900 records.

---

## 3. Objectives

1. Establish a complete L4 Task inventory
2. Validate all L4-to-L3 parent relationships
3. Validate the 5-phase decomposition coherence per parent Activity
4. Confirm the Task boundary is explicit (inclusions and exclusions)
5. Reconcile the pre-EXT-15 `evidence[]` form with the canonical `provenance[]`
6. Establish entity-level dispositions across the L4 population
7. Generate consistent Task README documentation
8. Publish the L4-to-L3 traceability matrix (the final slice of the L2-to-L3-to-L4 matrix)

---

## 4. Scope

### 4.1 In scope

All L4 Task entities in the approved backfill population (2,900 records).

The inventory shall include:

- Task identifier
- Task name
- Decomposition phase
- Parent L3 Activity
- Existing README
- Existing operational fields
- Existing evidence records
- Evidence and review status
- Profile completeness
- Backfill disposition

### 4.2 Out of scope

This CR shall not:

- Redefine L3 Activity purposes or L2 business transformations
- Introduce new L4 Tasks without an approved decomposition change
- Change the 5-phase decomposition pattern for existing records
- Introduce mandatory execution sequencing or runtime semantics
- Invent responsibilities, controls or operational dependencies
- Duplicate canonical Business Function, Business Capability, Information System or Metric entities
- Require every Task to have a different number of siblings

---

## 5. Normative implementation requirements

### REQ-21-01: L4 inventory

Produce an authoritative inventory of all L4 Task entities, derived from the actual repository contents.

### REQ-21-02: Parent L3 readiness

Before a Task is enriched, its parent L3 Activity must:

- Have been assessed under EXT-20
- Have an accepted operational description
- Have an explicit disposition
- Have no unresolved parent-level issue that makes the Task's scope indeterminate

An approved exception may allow enrichment to proceed, but the exception and its rationale must be recorded.

### REQ-21-03: Parent relationship

Every Task shall reference its canonical parent L3 Activity. The relationship must be validated against the repository's identifier and hierarchy conventions.

### REQ-21-04: Decomposition coherence

Where a parent Activity's Task population follows a recognised decomposition pattern, the Task population shall be validated against that pattern. A parent whose Task population deviates from the pattern shall be recorded for structural review rather than silently corrected.

### REQ-21-05: Task identity and purpose

Every Task shall have a meaningful definition identifying the bounded unit of work it represents. A restatement of the Task name is insufficient.

### REQ-21-06: Task boundary

Every Task shall have an explicit boundary with both inclusions and exclusions. A boundary with inclusions only does not establish what the Task excludes.

### REQ-21-07: Trigger

Every Task shall document the condition under which it is initiated. A Task trigger is not necessarily the parent's first execution step.

### REQ-21-08: Outcome

Every Task shall document what it produces or accomplishes. A Task outcome is not necessarily the parent Activity's outcome.

### REQ-21-09: Responsibility

Every Task shall document who performs the work. The L4 plain-string responsibility form is valid at this level.

### REQ-21-10: Evidence and provenance

Apply EXT-15 to material L4 operational assertions. The existing pre-EXT-15 `evidence[]` record shall be reconciled with the canonical `provenance[]` structure. AI-generated suggestions must not be presented as verified Task facts.

### REQ-21-11: Authoring metadata

Apply EXT-16 to the L4 population. The `metadata.authoring` block shall be populated with the authoring state, source priority used, AI-assistance disclosure and review outcome.

### REQ-21-12: Canonical entity update

Update canonical L4 entity data using the approved schema. Preserve existing entity identifiers, established references and repository conventions. Do not create overlapping operational fields.

### REQ-21-13: README generation

Generate each Task README from canonical entity data using the approved documentation generator. The README shall use the approved L4 documentation profile, represent the evidence status, and identify unresolved gaps where appropriate.

### REQ-21-14: Entity-level disposition

Every in-scope Task shall receive an explicit backfill disposition from the 7-value programme vocabulary (verified_complete, verified_with_gaps, awaiting_evidence, awaiting_owner_review, requires_structural_remediation, not_applicable, deferred_with_approval).

### REQ-21-15: L4-to-L3 traceability matrix

Publish the L4-to-L3 traceability matrix, completing the L2-to-L3-to-L4 traceability matrix. The matrix shall reveal:

- L2 processes with missing or inadequate Activity decomposition
- Activities that do not contribute clearly to their assigned parent process
- Tasks that do not clearly contribute to their assigned Activity

### REQ-21-16: Catalogue reporting

Publish an L4 backfill report including: total L4 Tasks, Tasks assessed, Tasks enriched, Tasks verified, Tasks with documented gaps, Tasks awaiting evidence, Tasks awaiting review, Tasks requiring structural remediation, parent L3 readiness, decomposition coherence status, evidence coverage, cross-reference validity and outstanding issues.

---

## 6. Implementation work packages

| Work package | Deliverable |
|---|---|
| WP-21-01 | L4 inventory and baseline |
| WP-21-02 | Parent L3 readiness assessment |
| WP-21-03 | L4-to-L3 hierarchy validation |
| WP-21-04 | 5-phase decomposition coherence assessment |
| WP-21-05 | Task definition, boundary, trigger, outcome and responsibility enrichment |
| WP-21-06 | Evidence and provenance reconciliation (pre-EXT-15 to canonical) |
| WP-21-07 | Authoring metadata and disposition |
| WP-21-08 | README generation and validation |
| WP-21-09 | L4-to-L3 traceability matrix |
| WP-21-10 | Human review and disposition |
| WP-21-11 | Catalogue-level reporting |

---

## 7. Quality gates

- Gate 21-A: Inventory completeness
- Gate 21-B: Parent readiness
- Gate 21-C: Decomposition coherence
- Gate 21-D: Operational completeness
- Gate 21-E: Evidence and documentation integrity
- Gate 21-F: Review and disposition

---

## 8. Testing requirements

The implementation shall demonstrate:

- L4 inventory completeness
- Valid parent L3 relationships
- Detection of orphaned Tasks
- Detection of invalid references
- Detection of incoherent decomposition patterns
- Task boundary completeness (inclusions and exclusions)
- Evidence and provenance validation
- Correct treatment of inherited information
- README generation consistency
- Idempotent migration and generation
- Preservation of existing identifiers and valid documentation

---

## 9. Risks and mitigations

| Risk | Mitigation |
|---|---|
| L3 parent is incomplete | Enforce parent readiness gate or approved exception |
| Rigid phase pattern is applied indiscriminately | Validate the pattern, do not force it |
| Task duplicates the parent Activity | Apply the boundary and contribution tests |
| Pre-EXT-15 evidence is lost in migration | Preserve the existing evidence content; map, do not discard |
| Phase pattern mistaken for workflow sequencing | Document the pattern as a decomposition convention, not an execution order |
| Over-decomposition at L4 | Record the deviation; do not create or remove Tasks |

---

## 10. Acceptance criteria

- Complete L4 inventory produced
- Every Task has a valid parent relationship or explicit remediation status
- Parent L3 readiness assessed
- Task definitions meaningful
- Task boundaries explicit (inclusions and exclusions)
- Triggers and outcomes documented
- Responsibilities documented
- Decomposition coherence assessed
- Evidence and provenance reconciled with the canonical form
- Authoring metadata populated
- Canonical L4 entities updated
- READMEs generated from canonical data
- Validation and review completed
- Every Task has an explicit disposition
- Catalogue-level L4 report published
- L4-to-L3 traceability matrix published
- No unsupported operational claims presented as verified

---

## 11. Completion definition

EXT-21 is complete when all in-scope L4 Tasks have been assessed, enriched to their evidence-supported level, reconciled with their parent L3 Activities, validated and reviewed as required.

EXT-21 completion establishes the operational documentation foundation for EXT-22: L0/L1 Context Reconciliation.

---

## 12. References

- `change-requests/CR-BP-94-EXT-19-l2-business-process-operational-documentation-backfill.md` (EXT-19)
- `change-requests/CR-BP-94-EXT-20-l3-activity-operational-documentation-backfill.md` (EXT-20)
- `change-requests/CR-BP-94-EXT-15-evidence-provenance-and-confidence-framework.md` (EXT-15)
- `change-requests/CR-BP-94-EXT-16-operational-authoring-and-research-methodology.md` (EXT-16)
- `change-requests/CR-BP-94-EXT-17-enrichment-tooling-and-backfill-orchestration.md` (EXT-17)
- `change-requests/CR-BP-94-EXT-18-operational-documentation-pilot.md` (EXT-18 + GO decision)
- `docs/operational-documentation-programme/CR-BP-94-EXT-19-to-20-detailed-design.md` (the detailed design)
- `docs/evidence-provenance-confidence.md` (EXT-15)
- `docs/operational-authoring-methodology.md` (EXT-16)
- `docs/enrichment-tooling-orchestration.md` (EXT-17)
- `reconciliation/l4-to-l3-traceability-matrix.json` (the EXT-21 traceability matrix)
- `reconciliation/programme-register.json` (the 17-CR register)
