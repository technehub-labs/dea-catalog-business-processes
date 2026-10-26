# CR-BP-94-EXT-22: Process Decomposition Reconciliation and Structural Integrity

**Status**: Proposed
**Layer**: Process Catalog (Cross-Cutting Documentation)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-19
**Source CR**: CR-BP-EXT-22 (Process Decomposition Reconciliation and Structural Integrity)
**Parent programme**: CR-BP-94: Process Decomposition and Operational Documentation (DEA-PROCESS-ENRICH-000)
**Repository**: technehub-labs/dea-catalog-business-processes
**Change type**: Catalogue governance, structural integrity, semantic reconciliation
**Priority**: Critical
**Depends on**: CR-BP-94-EXT-08 through CR-BP-94-EXT-21, particularly CR-BP-94-EXT-10, CR-BP-94-EXT-11, CR-BP-94-EXT-15, CR-BP-94-EXT-17, CR-BP-94-EXT-18, CR-BP-94-EXT-19, CR-BP-94-EXT-20, CR-BP-94-EXT-21
**Enables**: EXT-23 (Operational Documentation Conformance Gates)
**Target scope**: L0 Process Scope, L1 Process Group, L2 Business Process, L3 Activity, L4 Task
**Implementation approach**: Inventory before modification, dataset extraction, structural checks, matrix generation, closure report

---

## 1. Executive summary

This Change Request establishes a systematic reconciliation process for the complete Business Process catalogue hierarchy, ensuring that its decomposition is structurally valid, semantically coherent, sufficiently complete and traceable across all levels.

The preceding CRs establish operational documentation and enrichment at individual decomposition levels:

- EXT-19: L2 Business Process enrichment
- EXT-20: L3 Activity enrichment
- EXT-21: L4 Task enrichment

However, enriching each level independently does not guarantee that the relationships between levels are correct.

EXT-22 addresses these issues through a controlled, evidence-based reconciliation of the hierarchy. Its central deliverable is the L2-L4 Reconciliation Matrix, supported by an L0-L1 contextual reconciliation and a catalogue-wide structural integrity assessment.

The outcome must be a defensible process decomposition, not merely a catalogue in which every entity has a populated README.

---

## 2. Problem statement

The Business Process catalogue uses a hierarchical decomposition:

| Level | Entity | Primary purpose |
|---|---|---|
| L0 | Process Scope | Establishes the overall scope and boundaries of a process domain or process landscape |
| L1 | Process Group | Organises related Business Processes into meaningful groups |
| L2 | Business Process | Represents a complete business transformation or coherent business result-producing process |
| L3 | Activity | Represents a cohesive body of work contributing to a Business Process |
| L4 | Task | Represents a bounded, independently understandable unit of work contributing to an Activity |

A valid hierarchy requires two complementary forms of reconciliation:

**Top-down decomposition integrity.** The parent must be adequately represented by its children. The children must collectively account for the parent's scope, responsibilities and intended contribution.

**Bottom-up semantic integrity.** Every child must have a defensible relationship to its parent. Its purpose and contribution must be explainable in the context of the parent's purpose and boundaries.

Both directions are necessary. A decomposition can be structurally complete but semantically invalid. Equally, individual entities can be well documented while the overall decomposition remains incomplete.

---

## 3. Objectives

1. Establish a consistent reconciliation methodology across L0-L4.
2. Verify that each L2 Business Process is adequately represented by its L3 Activities.
3. Verify that each L3 Activity is adequately represented by its L4 Tasks where further decomposition is appropriate.
4. Confirm that each Activity contributes meaningfully to its assigned Business Process.
5. Confirm that each Task contributes meaningfully to its assigned Activity.
6. Identify missing, orphaned, duplicated, misplaced or inconsistently defined entities.
7. Identify decomposition that is too broad, too narrow or unnecessarily granular.
8. Identify Activities or Tasks that have been decomposed according to execution sequence rather than functional responsibility.
9. Verify alignment between parent and child boundaries, inputs, outputs, responsibilities, rules, controls and dependencies.
10. Reconcile L0 Process Scopes and L1 Process Groups with the L2 process landscape.
11. Establish explicit disposition and remediation requirements for unresolved structural or semantic gaps.
12. Produce a traceable reconciliation baseline for EXT-23 conformance enforcement.

---

## 4. Scope

### 4.1 In scope

All L0-L4 entities; parent-child relationships; entity membership and classification; decomposition adequacy and completeness; semantic contribution and alignment; entity boundaries and ownership; inputs, outputs and transformation relationships; responsibilities and accountability; rules, controls and exceptions; dependencies and interfaces; metric and evidence references where applicable; duplicate and overlapping entities; orphaned and misplaced entities; granularity and decomposition quality; cross-level consistency; reconciliation evidence and approval; catalogue-wide reporting.

### 4.2 Out of scope

EXT-22 does not:

- Redesign the complete Business Process metamodel
- Introduce new decomposition levels
- Redefine the semantics of L0-L4
- Replace EXT-19, EXT-20 or EXT-21 enrichment activities
- Introduce mandatory workflow sequencing or orchestration
- Convert the process hierarchy into a workflow execution model
- Automatically merge or delete entities
- Invent missing operational facts
- Automatically infer authoritative parent-child relationships from naming similarity
- Introduce new cross-catalogue relationship types without metamodel approval
- Make unsupported claims of completeness where evidence is unavailable

---

## 5. Governing decomposition principles

### 5.1 Functional decomposition, not execution sequencing

The hierarchy represents progressively decomposed business responsibility and work. It does not inherently represent execution order, workflow steps, branching logic, runtime orchestration, state transitions, scheduling, queue management or retry behaviour.

### 5.2 Parent-child contribution

Every child must have an explainable contribution to its parent, supported by the child's purpose, scope and operational description. A child should not be retained solely because it is historically present or has a plausible name.

### 5.3 Parent coverage

A parent must be adequately represented by its children where decomposition is required. The presence of multiple children does not, by itself, demonstrate adequate coverage.

### 5.4 Decomposition is not determined by arbitrary counts

No fixed number of Activities per Business Process or Tasks per Activity shall be imposed. The decision must be based on semantic completeness, cohesion, boundaries and operational usefulness.

### 5.5 Evidence-based reconciliation

Reconciliation must distinguish verified structural facts, verified operational facts, inferred relationships, proposed corrections, unresolved questions, confirmed absences and approved exceptions. The absence of evidence must not be treated as evidence of absence.

### 5.6 Canonical source of truth

Entity YAML remains the authoritative source of entity facts and relationships. README documentation is generated according to the approved documentation architecture. It must not become an independent source of conflicting operational truth.

---

## 6. Reconciliation requirements

The 22 normative requirements (REQ-22-01 through REQ-22-22) and the 19 acceptance criteria (AC-22-01 through AC-22-19) are specified in the user-submitted specification, preserved at `docs/operational-documentation-programme/CR-BP-94-EXT-22-to-23-detailed-design.md`.

The implementation in this slice covers the deterministic subset:

| Requirement | Implementation in this slice |
|---|---|
| REQ-22-01 | `reconciliation/reconciliation-matrix.json` + the catalogue inventory in the EXT-22 manifest |
| REQ-22-02 | R22-02 structural hierarchy validation |
| REQ-22-03 | R22-04 + the L3 rows of the reconciliation matrix |
| REQ-22-04 | R22-05 + the L4 rows of the reconciliation matrix |
| REQ-22-05 | The L3/L4 parent-contribution columns of the matrix (evidence-led assessment pending) |
| REQ-22-06 | The coverage-assessment columns of the matrix |
| REQ-22-07 | R22-11 functional decomposition integrity |
| REQ-22-08 | The boundary-alignment column (assessment pending) |
| REQ-22-09 | The operational-alignment column (assessment pending) |
| REQ-22-10 | Deferred to the EXT-19/EXT-20/EXT-21 content backfills |
| REQ-22-11 | Deferred to the EXT-19/EXT-20/EXT-21 content backfills |
| REQ-22-12 | R22-10 duplicate and overlapping entity detection |
| REQ-22-13 | R22-03, R22-04, R22-05, R22-06 + the orphan register |
| REQ-22-14 | R22-09 granularity assessment + the granularity register |
| REQ-22-15 | R22-07, R22-08, R22-12 + the L0-L1 reconciliation report |
| REQ-22-16 | R22-06 + the L0-L1 reconciliation report |
| REQ-22-17 | The disposition vocabulary + the matrix disposition column |
| REQ-22-18 | The evidence-references column of the matrix |
| REQ-22-19 | The EXT-22 manifest + the structural integrity report |
| REQ-22-20 | The matrix is a generated view; no canonical entity is modified |
| REQ-22-21 | Governed by the repository's PR + review process |
| REQ-22-22 | `reconciliation/ext23-readiness-assessment.json` |

---

## 7. The mandatory L2-L4 Reconciliation Matrix

### 7.1 Purpose

The matrix is the principal controlled artefact of this CR. It provides a consolidated view of the relationship between Business Processes, Activities and Tasks. It supports both top-down and bottom-up assessment.

### 7.2 The required field contract

The matrix carries all 26 fields specified in the user-submitted CR §7.2:

| Field | Matrix key |
|---|---|
| Reconciliation ID | `reconciliation_id` |
| L2 Process ID | `l2_process_id` |
| L2 Process Name | `l2_process_name` |
| L2 Purpose | `l2_purpose` |
| L2 Boundary | `l2_boundary` |
| L3 Activity ID | `l3_activity_id` |
| L3 Activity Name | `l3_activity_name` |
| L3 Purpose | `l3_purpose` |
| L3 Parent Contribution | `l3_parent_contribution` |
| L3 Coverage Assessment | `l3_coverage_assessment` |
| L4 Task ID | `l4_task_id` |
| L4 Task Name | `l4_task_name` |
| L4 Purpose | `l4_purpose` |
| L4 Parent Contribution | `l4_parent_contribution` |
| L4 Coverage Assessment | `l4_coverage_assessment` |
| Boundary Alignment | `boundary_alignment` |
| Operational Alignment | `operational_alignment` |
| Structural Status | `structural_status` |
| Semantic Status | `semantic_status` |
| Granularity Assessment | `granularity_assessment` |
| Evidence References | `evidence_references` |
| Identified Issues | `identified_issues` |
| Required Action | `required_action` |
| Issue Owner | `issue_owner` |
| Disposition | `disposition` |
| Review Status | `review_status` |

### 7.3 Scenario coverage

The matrix supports the 8 scenarios in the user-submitted CR §7.3. The current catalogue exercises:

| Scenario | Count |
|---|---|
| A: L2 with L3 Activities and L4 Tasks | 2,900 |
| B: L2 with Activities but no Tasks | 0 |
| C: L3 Activity with no L4 Tasks | 0 |
| D: L2 without L3 Activities | 1 |
| E: L3 with no clear parent contribution | 0 (semantic assessment pending) |
| F: L4 with no clear parent contribution | 0 (semantic assessment pending) |
| G: Potentially duplicated Activities or Tasks | 0 |
| H: Shared or cross-cutting responsibility | 0 |

### 7.4 The matrix as a controlled artefact

The matrix is a **generated view** over the canonical entity data, not a manually maintained alternative source of truth. It is regenerated by `scripts/check_reconciliation_ext22.py` and carries a version, generation date, generator identity, parent CR and a traceable source entity inventory. It does not introduce new canonical entity fields.

---

## 8. Reconciliation methodology

The 7-phase methodology of the user-submitted CR §8 is implemented as follows:

| Phase | Implementation |
|---|---|
| 1. Establish baseline | The catalogue walk + the EXT-22 manifest + the structural integrity report |
| 2. Reconcile L2-L3 | R22-04 + the L3 rows of the matrix |
| 3. Reconcile L3-L4 | R22-05 + the L4 rows of the matrix |
| 4. Reconcile operational semantics | The operational-alignment column (evidence-led; assessment pending) |
| 5. Reconcile L0-L1 context | R22-07, R22-08, R22-12 + the L0-L1 reconciliation report |
| 6. Remediate and validate | The EXT-22 manifest + the 4 registers |
| 7. Programme closure and EXT-23 readiness | The EXT-23 readiness assessment |

---

## 9. Work packages

| Work package | Deliverable | Status in this slice |
|---|---|---|
| WP-22-01 | L0-L4 inventory and baseline report | DELIVERED |
| WP-22-02 | Structural integrity report | DELIVERED |
| WP-22-03 | L2-L3 reconciliation records | DELIVERED |
| WP-22-04 | L3-L4 reconciliation records | DELIVERED |
| WP-22-05 | Parent-child semantic assessment | DEFERRED (evidence-led) |
| WP-22-06 | Duplicate and overlap register | DELIVERED |
| WP-22-07 | Orphan and misplaced entity register | DELIVERED |
| WP-22-08 | Decomposition quality register | DELIVERED |
| WP-22-09 | Process landscape reconciliation report | DELIVERED |
| WP-22-10 | Canonical updates and remediation | DEFERRED (requires approved decisions) |
| WP-22-11 | L2-L4 Reconciliation Matrix | DELIVERED |
| WP-22-12 | Validation and EXT-23 readiness | DELIVERED |

---

## 10. Quality gates

- Gate 22-A: Inventory completeness (all in-scope L0-L4 entities inventoried)
- Gate 22-B: Structural integrity (all structural anomalies identified and dispositioned)
- Gate 22-C: L2-L3 reconciliation (every in-scope L2 assessed against its Activities)
- Gate 22-D: L3-L4 reconciliation (every in-scope Activity assessed against its Tasks or explicitly dispositioned)
- Gate 22-E: Semantic consistency (material parent-child inconsistencies identified and dispositioned)
- Gate 22-F: Duplicate and granularity review (all identified material cases reviewed and dispositioned)
- Gate 22-G: Contextual reconciliation (L0 and L1 scope and membership reconciled)
- Gate 22-H: Evidence and approval (material decisions supported by evidence or approved rationale)
- Gate 22-I: Canonical consistency (entity representations, references and documentation aligned)
- Gate 22-J: EXT-23 readiness (conformance requirements and unresolved limitations documented)

---

## 11. The 12 deterministic rules (R22-01..R22-12)

| Rule | Description | Findings on the current catalogue |
|---|---|---|
| R22-01 | Catalogue-wide entity inventory completeness (L0-L4) | 0 |
| R22-02 | Structural hierarchy validation: parent reference validity, allowed parent-child entity types, level consistency | 0 |
| R22-03 | Duplicate canonical identifier detection | 0 |
| R22-04 | L2-to-L3 decomposition coverage | 1 |
| R22-05 | L3-to-L4 decomposition coverage | 0 |
| R22-06 | L1-to-L2 membership | 1 |
| R22-07 | L0-L1 contextual consistency | 6 |
| R22-08 | L0 materialisation | 0 |
| R22-09 | Granularity assessment (review prompt) | 16 |
| R22-10 | Duplicate / overlapping entity detection (review prompt) | 0 |
| R22-11 | Functional-decomposition integrity (the 5-phase pattern) | 0 |
| R22-12 | L0-L1 landscape coverage | 0 |
| | **Total** | **8 errors + 16 review prompts** |

---

## 12. The 8 structural findings

| # | Finding | Severity | Disposition |
|---|---|---|---|
| 1 | `processes:process-ge-conceive-e6jx6s` (Develop Governance Strategy) has no L3 Activity decomposition (R22-04) | error | requires_structural_remediation |
| 2 | `processes:process-ge-conceive-e6jx6s` is not composed by any L1 Process Group (R22-06) | error | requires_structural_remediation |
| 3-8 | 6 L1-to-L2 compositions carry an L0 context mismatch (R22-07): `processes:group-fa-conceive-9xzf3b` composes 5 L2 processes from other cells, and `processes:group-fa-improve-hvq8u8` composes `processes:process-ge-operate-hxxyc9` | error | requires_structural_remediation |

The 16 R22-09 findings are review prompts, not defects: 16 L1 Process Groups have exactly one L2 member, which may be a valid grouping or an under-developed decomposition. They carry no fixed-count requirement (principle 5.4).

---

## 13. The EXT-23 readiness assessment (REQ-22-22)

`reconciliation/ext23-readiness-assessment.json` classifies the requirements into:

- **Automatically enforceable**: R22-01, R22-02, R22-03, R22-04, R22-05, R22-06, R22-07, R22-08, R22-12
- **Requires human review**: R22-09, R22-10, R22-11, parent-child contribution adequacy, parent-to-child coverage adequacy, boundary and operational semantic alignment
- **Evidence assessment only**: semantic contribution status, operational alignment status
- **Deferred**: the EXT-15 canonical provenance[] migration on the L4 population, the EXT-16 metadata.authoring migration on the L4 population
- **Known limitations**: the semantic status and operational alignment remain unresolved in the initial matrix baseline; boundary alignment is not machine-comparable between L2, L3 and L4 in the current canonical representation
- **Residual risks**: the 8 structural findings, the 2,900 L4 records with the pre-EXT-15 evidence form

---

## 14. Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Artificial decomposition to satisfy hierarchy expectations | Unnecessary catalogue complexity | Do not mandate minimum child counts |
| Incorrect automated semantic inference | Invalid business model | Require human review and evidence |
| Duplicate entities merged prematurely | Loss of traceability and meaning | Require explicit approval and migration records |
| README and YAML become inconsistent | Conflicting sources of truth | Preserve canonical entity data and deterministic generation |
| Parent-child relationships imply execution order | Workflow semantics contaminates the model | Explicitly distinguish functional decomposition from sequencing |
| Incomplete evidence is mistaken for completeness | False assurance | Use explicit uncertainty and disposition states |
| Excessive remediation scope | Programme delay | Prioritise material issues and use approved deferrals |
| Inconsistent treatment of shared responsibilities | Incorrect ownership and hierarchy | Use metamodel-approved cross-references |
| Existing repository conventions are overlooked | Unnecessary schema and tooling changes | Inventory the current implementation before prescribing changes |

---

## 15. Acceptance criteria

The 19 acceptance criteria (AC-22-01 through AC-22-19) are specified in the user-submitted specification. The 19th criterion is decisive: **the final reconciliation report demonstrates the status of the entire catalogue rather than reporting only successfully completed entities.** The EXT-22 manifest reports all 8 findings, including the 2 that concern the same deprecated L2 process.

---

## 16. Definition of done

EXT-22 is complete when the catalogue has been assessed as a connected process decomposition rather than a collection of individually documented entities. Every in-scope entity must have a verified or explicitly dispositioned place in the hierarchy. Every material parent-child relationship must have a defensible semantic basis. Every decomposed parent must have an assessed level of child coverage. Every structural, semantic, duplication, granularity and boundary issue must be resolved or explicitly dispositioned. The reconciliation matrix must provide a traceable record of these decisions. The resulting catalogue must be suitable for the introduction of EXT-23 conformance gates without concealing unresolved semantic or structural weaknesses.

---

## 17. References

- `docs/operational-documentation-programme/CR-BP-94-EXT-22-to-23-detailed-design.md` (the user-submitted specification)
- `change-requests/CR-BP-EXT-23-operational-documentation-conformance-framework-and-automated-quality-gates.md` (EXT-23)
- `change-requests/CR-BP-94-EXT-19-l2-business-process-operational-documentation-backfill.md` (EXT-19)
- `change-requests/CR-BP-94-EXT-20-l3-activity-operational-documentation-backfill.md` (EXT-20)
- `change-requests/CR-BP-94-EXT-21-l4-task-operational-documentation-backfill.md` (EXT-21)
- `scripts/check_reconciliation_ext22.py` (the EXT-22 validator)
- `scripts/check_decomposition_reconciliation.py` (the EXT-05 decomposition validator)
- `reconciliation/reconciliation-matrix.json` (the L2-L4 Reconciliation Matrix)
- `reconciliation/structural-integrity-report.json`
- `reconciliation/ext23-readiness-assessment.json`
- `reconciliation/programme-register.json` (the 17-CR register)
