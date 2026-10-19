# Operational Authoring and Research Methodology (CR-BP-94-EXT-16)

**Status**: Normative (proposed for adoption under CR-BP-94-EXT-16)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-19
**Source CR**: CR-BP-94-EXT-16 (Operational Authoring and Research Methodology)
**Parent programme**: DEA-PROCESS-ENRICH-000
**Predecessors**: EXT-10, EXT-11, EXT-12, EXT-13, EXT-14, EXT-15
**Tranche**: Engineering and governance readiness tranche (EXT-15..18)
**Enables**: EXT-17 (tooling), EXT-18 (pilot)
**Repository**: technehub-labs/dea-catalog-business-processes

---

## 1. Purpose

This document is the **EXT-16 methodology handbook** for researching, authoring, reviewing and maintaining operational documentation for Business Process catalogue entities. The methodology ensures that different contributors can enrich process entities consistently without introducing unsupported operational assumptions, duplicating information, or confusing decomposition levels.

The methodology is the bridge between the EXT-15 evidence/provenance framework and the EXT-17 tooling: the per-record `metadata.authoring` block (defined here) is what the EXT-17 tooling will read to drive batch orchestration and reporting.

---

## 2. The 14-step authoring lifecycle (REQ-16-01)

Every enrichment activity follows a documented lifecycle:

1. **Select entity** and establish scope
2. **Inspect current entity** and its parent/child relationships
3. **Identify information gaps** against the applicable profile
4. **Develop a research plan**
5. **Identify and assess available sources** (using the source prioritisation below)
6. **Capture evidence and provenance** (per EXT-15)
7. **Draft operational assertions**
8. **Validate semantic distinctions** (using the checklist below)
9. **Reconcile with related catalogue entities**
10. **Obtain required review and approval** (per the review roles below)
11. **Update canonical entity data**
12. **Generate documentation** (per EXT-17 tooling)
13. **Execute validation and quality checks** (per the 8 quality dimensions below)
14. **Submit changes** through the repository's established review process

The lifecycle is a checklist, not a strict ordering: a contributor may iterate between steps 6, 7, 8 and 9 multiple times before reaching step 10. The intent is to ensure all 14 steps are documented in the `metadata.authoring` block.

---

## 3. The 9-value authoring state (per `metadata.authoring.state`)

The `metadata.authoring.state` field tracks where the entity is in the lifecycle:

| State | Description |
|---|---|
| `not_started` | The entity is in the inventory but no enrichment has begun |
| `planning` | A research plan is being developed (steps 1-4) |
| `researching` | Sources are being consulted and evidence captured (steps 5-6) |
| `drafted` | Operational assertions are drafted (steps 7-9) |
| `under_review` | The draft is under review (step 10) |
| `approved` | The draft is approved by the process owner and reviewer (step 10) |
| `published` | The canonical entity data is updated and the README is generated (steps 11-12) |
| `rejected` | The draft is rejected and a new draft must be produced |
| `withdrawn` | The enrichment is withdrawn (the entity is back to `not_started` or a future planned state) |

A state transition must be recorded in the entity's `metadata.change_history` (the existing ADM-001..008 governance trail). The transition to `published` is the final step; the entity is then ready for the EXT-19+ backfill tranches.

---

## 4. Source prioritisation (REQ-16-02)

Authors prefer sources in the following general order. The order is guidance, not an automatic authority ranking; a source may be authoritative for one assertion and irrelevant to another.

| Priority | Source | EXT-15 `source.class` mapping |
|---|---|---|
| 1 | Approved organisational policies and procedures | `authoritative_document` |
| 2 | Authorised process owner confirmation | `owner_confirmation` |
| 3 | Controlled operational documentation | `authoritative_document` or `operational_record` |
| 4 | Verified system and architecture records | `system_documentation` |
| 5 | Direct observation and validated operational records | `direct_observation` or `operational_record` |
| 6 | Qualified subject-matter expert confirmation | `subject_matter_expert` |
| 7 | Authoritative external regulations and standards | `external_authority` |
| 8 | Credible secondary research | `secondary_reference` |
| 9 | Analyst inference | `analyst_inference` |

The `metadata.authoring.source_priority_used` field records the order consulted. The validator (AM-009) confirms the field is in the controlled vocabulary.

---

## 5. Actual practice vs target practice (REQ-16-03)

Authors distinguish:

- **Current operating practice** : what is done today
- **Approved documented practice** : what the policy says should be done
- **Intended or target operating practice** : what management intends
- **Proposed future-state practice** : what is being designed
- **External normative requirements** : what regulators or standards require

A target-state description must NOT be presented as the current operational process. Where documented practice and observed practice differ, the discrepancy and its evidence are recorded.

---

## 6. Decomposition-aware authoring (REQ-16-04)

Authoring respects the L0 to L4 distinctions:

- L0 describes process scope and context
- L1 describes process grouping and membership
- L2 describes the business transformation and its operational boundaries
- L3 describes cohesive bodies of work contributing to an L2 process
- L4 describes bounded, independently understandable tasks

L0 and L1 are NOT treated as executable operational units. L4 does NOT become a workflow-engine specification.

The validator (AM-010) confirms L0/L1 records do NOT carry `metadata.authoring` (they inherit from L2 per EXT-15 + EXT-11).

---

## 7. L2-first enrichment (REQ-16-05)

Operational enrichment normally begins at L2. The L2 process provides the transformation context against which L3 activities and L4 tasks can be assessed.

An exception may be made for a child entity where there is a specific research or remediation reason, but its parent relationship and unresolved dependencies must be recorded in `metadata.authoring.evidence_inheritance`.

The EXT-19 (L2 backfill) → EXT-20 (L3 backfill) → EXT-21 (L4 backfill) sequencing is the standard sequence. Out-of-order enrichment is permitted only when the parent context is already established.

---

## 8. Semantic distinction checklist (REQ-16-06)

Authors validate that the following 10 distinctions are preserved:

| Concept A | Concept B | Required distinction |
|---|---|---|
| Input | Resource | Information or object entering a transformation versus capacity used to perform work |
| Output | Outcome | Produced deliverable versus resulting business effect |
| Transformation | Workflow | Business change versus execution sequence |
| Role | Organizational unit | Responsibility-bearing position versus organisational structure |
| Responsibility | Accountability | Performing or contributing versus answerability and authority |
| Rule | Control | Requirement or constraint versus mechanism that manages compliance or risk |
| Control | Evidence | Mechanism versus proof of design or operation |
| Exception | Deviation | Recognized permitted variation versus departure from expected practice |
| Trigger | Precondition | Initiating event versus condition required for work to proceed |
| Dependency | Decomposition | Reliance on another entity versus structural parent-child relationship |

The validator (AM-008) confirms the 8 `quality_dimensions` (which include `semantic_correctness` and `decomposition_appropriateness`) are recorded.

---

## 9. Gap recording (REQ-16-07)

Authors do NOT fill unknown fields with invented content. Where information is unavailable, use the appropriate `uncertainty_state` from EXT-15 (`unknown` / `not_yet_assessed` / `deferred_with_reason` / `not_applicable` / etc.).

For material gaps, the `metadata.authoring.research_plan.gaps_identified[]` field records:

- What is unknown
- Why it matters
- Research already performed (the `sources_consulted[]` field)
- Who can resolve the gap
- Whether the gap blocks publication, approval or only full operational completeness

---

## 10. Review roles (REQ-16-08)

The methodology distinguishes:

- **Author** : the contributor who drafts the enrichment
- **Domain reviewer** : the subject-matter expert who validates semantic correctness
- **Process owner or authorized approver** : the role that has accountability for the process
- **Catalogue maintainer** : the role that owns the schema and the registry
- **Schema or metamodel reviewer** : the role that reviews schema-level changes (only when fields are added/removed)

Not every entity requires every role to be a separate person. However, the approval authority must be clear (the `metadata.authoring.reviewer` field).

---

## 11. AI-assisted authoring (REQ-16-09)

AI tools may assist with:

- `source_discovery`
- `summarisation`
- `extraction` (candidate assertion extraction)
- `harmonisation` (terminology harmonisation)
- `gap_analysis`
- `drafting`
- `structural_validation`

AI tools do NOT independently:

- Confirm actual organisational practice
- Approve process ownership or accountability
- Establish an authoritative control
- Convert an assumption into a verified fact
- Invent source references
- Resolve conflicting evidence without human authorization

The `metadata.authoring.ai_assistance` block records:

- `used`: `true` or `false`
- `tool`: the tool name
- `role`: the role from the controlled vocabulary above
- `validation`: `independently_validated` (the AI output has been validated by a human) or `pending_validation`

The validator (AM-007) confirms that when `ai_assistance.used` is `true`, `ai_assistance.validation` is one of the two controlled values.

---

## 12. Authoring records (REQ-16-10)

Each enrichment change is traceable through the repository's established change-management mechanism. The per-record `metadata.authoring` block carries:

- `author` (the role or person)
- `author_date`
- `reviewer` (the role or person)
- `review_date`
- `review_outcome` (`approved` / `rejected` / `revisions_required`)
- `state` (the 9-value lifecycle state)
- `methodology_version` (the EXT-16 methodology version; currently `1.0.0`)

The validator (AM-002 through AM-005) confirms the field structure.

---

## 13. Quality review dimensions (REQ-16-11)

Every enriched entity is reviewed for 8 dimensions. The `metadata.authoring.quality_dimensions` block records pass/fail/n_a for each:

| Dimension | Description |
|---|---|
| `semantic_correctness` | Are the operational concepts represented correctly? |
| `decomposition_appropriateness` | Does the entity describe the correct level of work? |
| `evidence_quality` | Can material assertions be traced to credible sources? |
| `parent_child_consistency` | Do L3/L4 entities align with their parent context? |
| `cross_catalogue_validity` | Are related entities referenced correctly? |
| `profile_completeness` | Is the profile completeness sufficient? |
| `publication_safety` | Is the content safe to publish? |
| `readme_consistency` | Does the generated README match the canonical entity data? |

The validator (AM-008) confirms all 8 dimensions are recorded.

---

## 14. Reproducibility (REQ-16-12)

The methodology is sufficiently explicit that another qualified contributor can understand why an assertion was made and how it was validated. The `metadata.authoring` block, combined with the EXT-15 `provenance[]` records, provides the trail.

The `methodology_version` field references the EXT-16 handbook version. As the methodology evolves, the field references the version under which the enrichment was performed.

---

## 15. L0-L4 applicability

| Concern | L0 ProcessContext | L1 ProcessGroup | L2 BusinessProcess | L3 Activity | L4 Task |
|---|---|---|---|---|---|
| `metadata.authoring` | (inherits from L2) | (inherits from L2) | (canonical) | (inherits from L2; may have its own) | (inherits from L2/L3; may have its own) |

L0 and L1 are non-executable (per EXT-11); they do not carry `metadata.authoring`. They inherit from L2.

The validator (AM-010) confirms L0/L1 do NOT carry `metadata.authoring`.

---

## 16. Compatibility and migration

EXT-16 is **additive**:

- Existing records that do not declare `metadata.authoring` continue to validate (the field is optional).
- The 9-value `state` vocabulary is the new lifecycle state; the existing `lifecycle_status` field (LCM-001..005) is preserved as the record's overall lifecycle.
- The 8 `quality_dimensions` are advisory when the field is unpopulated.
- The 9-value `source_priority_used` vocabulary is the EXT-16 source prioritisation; it is distinct from the EXT-15 `source.class` vocabulary (EXT-15 is the *type* of source; EXT-16 is the *order* consulted).

The 145 existing L2 records have **0** of the new fields populated (per the EXT-10 inventory; the CR-BP-96 advisory policy passes vacuously). The EXT-19 L2 backfill tranche is the work that populates them.

---

## 17. Validator and manifest

EXT-16 lands:

- `scripts/check_authoring_methodology_ext16.py` (the validator; AM-001..AM-010 rules)
- `reconciliation/authoring-manifest.json` (per-record manifest)
- `gate [41] Authoring Methodology` wired ADVISORY in `scripts/conformance_result.py`
- `tests/test_authoring_methodology_ext16.py` (unit + integration)

The validator enforces:

- **AM-001**: `metadata.authoring` is a dict with the EXT-16 attributes when present
- **AM-002**: `metadata.authoring.methodology_version` is non-empty
- **AM-003**: `metadata.authoring.state` is in the 9-value vocabulary
- **AM-004**: `metadata.authoring.author` is non-empty when `state` is `drafted` or later
- **AM-005**: `metadata.authoring.reviewer` is non-empty when `state` is `under_review` or later
- **AM-006**: `metadata.authoring.ai_assistance.used` is a boolean
- **AM-007**: when `ai_assistance.used` is `true`, `ai_assistance.validation` is in the 2-value vocabulary
- **AM-008**: `metadata.authoring.quality_dimensions` covers the 8 EXT-16 review dimensions
- **AM-009**: `metadata.authoring.source_priority_used` is in the 9-value vocabulary
- **AM-010**: L0/L1 do NOT carry `metadata.authoring` (non-executable per EXT-11 + EXT-16 §15)

---

## 18. References

- `templates/business-process.yaml` (the L2 template; EXT-16 extensions documented inline)
- `change-requests/CR-BP-94-EXT-16-operational-authoring-and-research-methodology.md` (the EXT-16 CR)
- `docs/operational-documentation-programme/CR-BP-94-EXT-15-to-18-detailed-design.md` (the detailed design; preserved user submission)
- `docs/operational-documentation-semantic-contract.md` (EXT-09; the upstream semantic contract)
- `docs/operational-schema-inventory.md` (EXT-10; the schema inventory)
- `docs/evidence-provenance-confidence.md` (EXT-15; the evidence/provenance framework that EXT-16 builds on)
- `templates/documentation-profile-ext11-v3.yaml` (EXT-11; the v3 profile)
- `reconciliation/programme-register.json` (the 17-CR register)
- `reconciliation/authoring-manifest.json` (EXT-16 manifest; the per-record authoring state)
- `reconciliation/evidence-manifest.json` (EXT-15 manifest)
- `reconciliation/profile-manifest.json` (EXT-11 manifest)
