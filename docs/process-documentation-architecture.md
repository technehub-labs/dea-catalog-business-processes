# Process Documentation Architecture

**Status**: Normative (proposed for adoption under CR-BP-94-EXT-01)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-18
**Recon programme parent**: CR-BP-92 (Process Catalog layer)
**Decomposition contract**: CR-BP-93 (`docs/decomposition-semantic-contract.md`)
**Template programme parent**: CR-BP-94 (Decomposition Record Templates, PR #134)
**Extension parent**: CR-BP-94-EXT-01 (this document)
**Depends on**: CR-BP-92, CR-BP-93, CR-BP-94, CR-BP-95, CR-BP-96, CR-BP-97.

---

## 1. Purpose

This document establishes the **Canonical Process Documentation Architecture** for the DEA Process Catalog. It answers the question:

> What documentation must every canonical process entity have, and how is that documentation produced, validated, and maintained?

The architecture is profile-driven, model-aligned, and lifecycle-aware. Every documentation asset is **derived from or validated against** the canonical YAML record; the YAML remains the authoritative model record and the documentation layer is a curated human-readable asset that references and validates the model rather than duplicating it as an independent source of truth.

The architecture lands in **phased implementation slices** under the CR-BP-94-EXT umbrella:

| Sub-CR | Title | Scope |
|---|---|---|
| EXT-01 (this slice) | Documentation Architecture | Contract + profile registry + README template structure + pilot scaffold + structural validator (DOC-001..005) |
| EXT-02 | README Profile & Template Standard | Concrete Markdown templates with section identifiers, profile-specific extensions, versioning |
| EXT-03 | Documentation Manifest & Coverage Model | Machine-readable documentation manifest schema, coverage dimension scoring, lifecycle rules |
| EXT-04 | Generation & Validation Pipeline | Profile-aware generator, structural validator, CI integration, evidence-state machine |
| EXT-05 | Decomposition Reconciliation | Parent-child documentation traceability, decomposition coverage reports, catalog-wide manifest |
| EXT-06 | Pilot & Catalog Rollout | Customer Insight and Retention pilot; then catalog-wide rollout of profile-driven documentation |

This slice (EXT-01) lands the architecture specification and the pilot scaffold; EXT-02..06 follow.

---

## 2. Architectural objective

```text
PROCESS CATALOG (authoritative model)
        │
        │ canonical YAML (entity record)
        ▼
CANONICAL ENTITY MODEL          <- Layer 1: machine-readable source of truth
        │
        │ referenced + validated
        ▼
CANONICAL DOCUMENTATION         <- Layer 2: human-readable README per entity
        │
        │ checked + traced
        ▼
VALIDATION & EVIDENCE           <- Layer 3: structural / semantic / relationship gates
```

The three layers MUST NOT collapse:

- **Layer 1 (Entity Model)** is the authoritative model. The canonical YAML record is the source of truth for identity, decomposition relationships, lifecycle, ECF alignment, and canonical relationships.
- **Layer 2 (Documentation)** explains the entity. It MUST reference the entity by canonical ID and MUST NOT duplicate identity, lifecycle, or relationship facts that are present in the YAML; where such facts appear, they are generated from the model and clearly marked.
- **Layer 3 (Validation)** checks structural conformance, semantic coherence, relationship consistency, decomposition coverage, and evidence provenance. It NEVER edits the documentation; it reports findings for human resolution.

---

## 3. Critical design decision: do not conflate entity type with decomposition level

**Rule:** An entity's `type` answers **what** it is in the model. Its `level` answers **where** it sits in the decomposition hierarchy (L0..L4).

- The README generator MUST obtain both classifications from the applicable schema (`schemas/entities/*.schema.json`) and vocabulary (`classifications/*.yaml`), not from the entity name.
- The profile resolver MUST select the documentation profile from `(entity.type, entity.level)` and MUST NOT infer entity type solely from a name pattern such as `dea:process-*` or `dea:activity-*`.
- Profile selectors MUST raise a validation failure when `(type, level)` is not a recognized combination under the controlled vocabulary.

Why this matters: the DEA catalog distinguishes between Business Process (L2 Process), Activity (L3 Activity), and Task (L4 Task) as **different entity types with different documentation obligations**. Treating a Process record as if it were an Activity: or vice versa: silently corrupts the documentation layer.

---

## 4. REQ-01: Canonical Documentation Contract

Every canonical process entity MUST have documentation that satisfies the following contract.

### 4.1 Required metadata (model-derived)

These fields are generated from the canonical YAML and MUST NOT be manually authored:

| Field | Source | Rationale |
|---|---|---|
| Canonical ID | `entity.id` | Identity cannot drift between model and docs |
| Name | `entity.name` | Same |
| Entity Type | `entity.type` | Discriminator (Process / Activity / Task / ProcessScope / ProcessGroup) |
| Decomposition Level | resolved from `(type, level_mapping)` | CR-BP-93 §3 normativity |
| Lifecycle Status | `entity.lifecycle_status` | Drives lifecycle-specific obligations (REQ-09) |
| Process Intent | `entity.process_intent` (when present) | Model-derived; emits `not_applicable` if absent |
| Process Type | `entity.process_type` (when present) | Model-derived; emits `not_applicable` if absent |
| Process Context | `entity.process_context` (when present) | Model-derived; emits `not_applicable` if absent |
| Governing CR | `entity.metadata.established_by` | Model-derived |
| Canonical Source | `entity.source_ref` (when present) | Model-derived; emits `pending` if absent |

### 4.2 Required semantic sections (human-authored)

These sections are authored by humans and express business / operational meaning that cannot safely be inferred from a name or identifier:

| Section | Required for | Rationale |
|---|---|---|
| `## Formal Definition and Scope` | all profiles | Definition cannot be derived from a name |
| `## Canonical Semantic Dimensions` | all profiles | The five-dimension framework (ontological / behavioral / structural / teleological / governance) |
| `## Decomposition and Composition` | L1 / L2 / L3 / L4 | Parent-child coverage is a business claim |
| `## Behavior and Workflow` | L2 / L3 / L4 | Triggers, main flow, exceptions are semantic |
| `## Inputs, Outputs, and Interfaces` | L2 / L3 / L4 | Interfaces are not derivable from id |
| `## Roles, Responsibilities, and Accountability` | L2 / L3 | Ownership is a business claim |
| `## Business Rules and Controls` | L2 / L3 (conditional on lifecycle) | Governance is conditional |
| `## Outcomes and Performance` | L2 (mandatory), L3 (conditional) | Outcome metrics are business commitments |
| `## Evidence and Traceability` | all profiles | Provenance is mandatory |
| `## Documentation Completeness` | all profiles | Self-reported status; layered with model-derived coverage |
| `## Revision History` | all profiles | Audit trail |

### 4.3 Conditional sections (when applicable)

These sections are required only when the entity has the relevant attribute or the lifecycle state demands it:

| Section | Trigger | Rationale |
|---|---|---|
| `## Alternative and Exception Flows` | Entity declares exception handling | Per CR-BP-96 BP-QUAL-009 boundary |
| `## Systems and Information` | Entity interacts with named systems | REQ-06 evidence provenance |
| `## Regulatory Controls` | Entity is in a regulated domain (F&A, PV, etc.) | Lifecycle-specific obligation |
| `## Human Approvals` | Entity triggers approvals | Conditional |
| `## Workflow Visualization` | Entity has BPMN or similar artifact | Optional elaboration |

### 4.4 Inherited content

Documentation MAY reference authoritative parent or sibling documentation for content that is duplicated across an entity family (e.g., a common regulatory framework). Inherited content MUST:

- Identify the authoritative source (parent entity id, external standard reference, or governance document).
- Carry a marker `> Inherited from: <source>` at the section opening.
- NOT be presented as independently validated detail at the child level.

### 4.5 Evidence requirements

Every documentation asset MUST reference its evidence:

- **Canonical model facts** are derived from the YAML record.
- **Business assumptions** are flagged with `> Assumption:` markers and require an evidence ref.
- **Externally sourced standards** (e.g., APQC PCF, IFRS, BPMN) are referenced with stable URIs.
- **Expert-authored interpretations** are marked with `> Expert:` markers.
- **Example values** (e.g., "target SLA 99.9%") MUST NOT be presented as approved enterprise targets without explicit governance adoption evidence.

---

## 5. REQ-02: Decomposition-Aware Documentation Profiles

A documentation profile is a machine-readable contract that specifies the documentation obligations for an `(entity.type, decomposition.level)` combination. The profile registry lives under `templates/documentation-profile-*.yaml` and is the source of truth for which sections are mandatory, conditional, or inherited at each level.

### 5.1 Profile registry (this slice)

| Profile ID | Entity Type | Level | Required sections | Conditional sections |
|---|---|---|---|---|
| `dea:profile-readme-l2-process-v1` | Process | L2 | All §4.2 sections | Workflow, Regulatory, Approvals |
| `dea:profile-readme-l3-activity-v1` | Activity | L3 | §4.2 with `Roles` + `Rules` mandatory; `Outcomes` conditional | Systems, Workflow |
| `dea:profile-readme-l4-task-v1` | Task | L4 | §4.2 with `Workflow` + `Execution steps` mandatory; `Outcomes` not_applicable | Approvals, Systems |

Profile records are added in EXT-02 (template standard) and the registry is enumerated by `scripts/check_documentation_profile.py` (this slice).

### 5.2 Critical anti-conflation rule

A record MUST NOT be matched to a profile by its `id` pattern alone. The profile resolver MUST consult:

1. `entity.type` from the YAML record (must be a discriminator value from the controlled vocabulary).
2. `entity.level` resolved via the L0..L4 mapping in `docs/decomposition-semantic-contract.md` §3.
3. The profile registry's `(type, level)` matching key.

If any of the three is missing or unrecognized, the resolver raises a validation failure (DOC-001, see §7).

---

## 6. REQ-03: Canonical README Template

### 6.1 Section identifier standard

Every section MUST have:

- A stable section identifier (HTML anchor) that does not change across revisions.
- A heading level consistent with the profile's section ordering.
- An optional marker that distinguishes generated from curated content.

### 6.2 Ordering (L2 Business Process profile)

```text
# Canonical Business Process: `{{entity.id}}`
## 1. Entity Identity and Classification            <- generated
## 2. Formal Definition and Scope                    <- curated
## 3. Canonical Semantic Dimensions                  <- curated
## 4. Decomposition and Composition                  <- generated (refs) + curated
## 5. Behavior and Workflow                          <- curated
## 6. Inputs, Outputs, and Interfaces                <- curated
## 7. Roles, Responsibilities, and Accountability    <- curated
## 8. Business Rules and Controls                    <- curated (conditional)
## 9. Outcomes and Performance                       <- curated
## 10. Evidence and Traceability                     <- curated (links to model)
## 11. Documentation Completeness                    <- generated (status + gaps)
## 12. Revision History                              <- generated (from model change_history)
```

The ordering is stable across revisions and across L2 / L3 / L4 profiles; profile-specific extensions append after §12 in the EXT-02 slice.

### 6.3 Generated vs curated markers

- Sections that are **generated from the YAML** carry a marker: `<!-- generated: do-not-edit -->`.
- Sections that are **curated by humans** carry: `<!-- curated: edit-here -->`.
- The structural validator (DOC-001..005, this slice) MUST NOT fail when generated sections contain `{{placeholder}}` tokens (they will be substituted by the EXT-04 generator).
- Curated sections that contain unresolved placeholders are flagged as DOC-002 findings.

---

## 7. REQ-04..REQ-05: Structural validator (this slice)

The validator `scripts/check_documentation_profile.py` enforces a minimum structural contract in **this slice**:

| Rule | Description |
|---|---|
| DOC-001 | README exists at `entities/v1-alpha/<entity-id>/README.md` |
| DOC-002 | README has the section identifiers mandated by the profile resolved from `(type, level)` |
| DOC-003 | README entity id matches the YAML `id` field |
| DOC-004 | Generated sections contain no unresolved `{{placeholder}}` tokens at `validated` lifecycle state |
| DOC-005 | README references the governing CR (from `metadata.established_by`) |

Future slices extend the rule set:

- DOC-006..010 (EXT-02): template-specific section ordering, profile-specific mandatory/conditional/inherited classification.
- DOC-011..015 (EXT-03): manifest + coverage dimension checks.
- DOC-016..020 (EXT-04): generation traceability, evidence provenance markers.
- DOC-021..025 (EXT-05): parent-child decomposition traceability.

The validator is wired as an **advisory gate** in this slice; it reports findings but does NOT block merge. The gate becomes blocking when a sufficient population of README assets has been authored (EXT-06 rollout).

---

## 8. REQ-09: Lifecycle-Specific Documentation Obligations

Documentation completeness is **not uniform** across lifecycle states. The architecture defines:

| Lifecycle | Documentation obligation | Allowed gaps |
|---|---|---|
| `research` | Identity + Definition + Research narrative; decomposition may be incomplete | Missing behavioral, structural, governance sections allowed; gaps documented in §11 |
| `candidate` | Identity + Definition + Decomposition + Behavior + Evidence; outcomes may be preliminary | Outcomes may be marked `pending`; governance conditional |
| `active` | All sections required; no `pending` states; review gate passed | None |
| `deprecated` | Identity + Definition + Decomposition + Retirement rationale | Behavioral / governance may be marked `not_applicable` |
| `retired` | Identity + Definition + Retirement rationale + historical preservation | All operational sections may be `not_applicable` |

The validator enforces DOC-005 only for `active` lifecycle in this slice; lifecycle-specific enforcement is added in EXT-04.

---

## 9. Documentation lifecycle states

Documentation passes through its own lifecycle, distinct from the entity lifecycle:

| State | Meaning |
|---|---|
| `not-started` | Documentation has not been initiated |
| `draft` | Documentation is being authored and may have incomplete required content |
| `structurally-complete` | Required sections and expected document structure are present |
| `semantically-reviewed` | Relevant content has undergone human review for meaning and consistency |
| `validated` | Automated checks and required review gates have passed |
| `published` | Documentation is accepted for its defined lifecycle state |
| `superseded` | Replaced by a newer approved documentation version |

A documentation lifecycle state MUST NOT automatically imply that the entity itself is active or approved. Process lifecycle and documentation lifecycle are **distinct dimensions**, even if coordinated by the CR pipeline.

---

## 10. Coverage model (REQ-05 stub)

Coverage is scored across six dimensions. Full scoring schema lands in EXT-03; this slice defines the dimensions and the stub-status reporting:

1. **Identity Coverage**: entity has canonical ID, name, type, level, lifecycle, source ref.
2. **Decomposition Coverage**: parent process documented; children documented or referenced.
3. **Behavioral Coverage**: triggers, flow, exceptions, completion criteria.
4. **Structural Coverage**: roles, systems, inputs, outputs, interfaces.
5. **Teleological Coverage**: purpose, outcomes, performance measures.
6. **Governance Coverage**: rules, controls, accountability, evidence.

Each dimension reports `complete` / `draft` / `pending` / `not_applicable` / `gap`. The full scoring algorithm is deferred to EXT-03.

---

## 11. Pilot: Customer Insight and Retention

The pilot entity is `dea:process-customer-insight-and-retention` (Operate Customer Retention Programs, established by CR-BP-13a, currently `candidate` lifecycle). The pilot demonstrates:

- The L2 profile applied to a real BP record.
- DOC-001..005 enforcement against the pilot's `entities/v1-alpha/dea:process-customer-insight-and-retention/README.md`.
- A documentation scaffold directory (`documentation/manifest.yaml`) introduced for this slice.

The pilot is **not** the full pilot implementation (that is EXT-06); it is a structural validation that the profile machinery resolves correctly for an L2 BP.

---

## 12. Extension CR roadmap

| Sub-CR | Status | Scope |
|---|---|---|
| CR-BP-94-EXT-01 (PR #137) | Merged | Architecture + profile registry (L2/L3/L4) + DOC-001..005 + pilot scaffold |
| CR-BP-94-EXT-01a (this slice) | Proposed (PR pending) | L0 ProcessContext + L1 ProcessGroup profile additions; validator profile registry extension; LEVEL_BY_TYPE extension |
| CR-BP-94-EXT-02 | Reserved | README Markdown template with section identifiers + profile-specific extensions + versioning |
| CR-BP-94-EXT-03 | Reserved | Documentation manifest schema + coverage dimension scoring + lifecycle rules |
| CR-BP-94-EXT-04 | Reserved | Profile-aware generator + structural validator + CI integration + evidence-state machine |
| CR-BP-94-EXT-05 | Reserved | Decomposition reconciliation + parent-child traceability + catalog-wide coverage report |
| CR-BP-94-EXT-06 | Reserved | Pilot completion + catalog-wide rollout |

## 13. Cardinal entities: L0 (ProcessContext) and L1 (ProcessGroup)

L0 (ProcessContext) and L1 (ProcessGroup) are cardinal entities per **CR-BP-92 §7** (decomposition matrix) and **CR-BP-93 §3** (semantic contract). They are catalog-owned types that pre-exist the L2 Business Process.

CR-BP-94-EXT-01 (PR #137) covered L2/L3/L4; CR-BP-94-EXT-01a (this slice) adds the L0 and L1 profiles:

| Profile ID | Type | Level | Required Sections | Notes |
|---|---|---|---|---|
| `dea:profile-readme-l0-process-context-v1` | `ProcessContext` | L0 | 11 | outcomes is conditional (inherited from ECF framework); not_applicable: execution-steps |
| `dea:profile-readme-l1-process-group-v1` | `ProcessGroup` | L1 | 11 | outcomes is conditional; not_applicable: execution-steps |

### Cardinal-entity constraints

1. **L0 ProcessContexts are not deprecated or retired.** Their lifecycle transitions are: candidate -> active -> reorganized. The `reorganized` state lands in EXT-04 (lifecycle coverage model).
2. **L1 ProcessGroups are not deprecated or retired.** Their lifecycle transitions are: candidate -> active -> reorganized. The `reorganized` state lands in EXT-04.
3. **Schema strictness differs by level.** The L1 PG schema (`schemas/entities/process-group.schema.json`) declares `additionalProperties: false` and requires 12 fields including `composes` and `process_group_kind`. The L2 BP schema (`schemas/entity.schema.json`) is permissive (`additionalProperties` not set; only 5 required fields). The L0 ProcessContext schema is permissive.
4. **Pilot manifests for L1 require a sibling-file pattern.** Because the L1 schema bans additional properties, the L1 documentation profile content lives in a sibling file (`docs/manifests/<id>-profile.yaml`) referenced from the manifest via a `links:` entry. The L2 BP pilot (EXT-01, PR #137) is structurally simpler because the BP schema is permissive.

### L1 pilot decision (EXT-01a)

The L1 pilot record on `dea:group-customer-insight-and-retention` is deferred to EXT-06 (pilot + catalog rollout). The pilot record would require schema gymnastics: empty `composes: []` would fail PG-002; non-empty would fail PG-006 MECE because the parent record already composes the same BP. EXT-06 lands the pilot at the L0/L1 level once the catalog-wide rollout scope is defined.

---

## 14. Acceptance criteria (this slice)

1. `docs/process-documentation-architecture.md` (this document) is published.
2. Five documentation profile templates exist under `templates/`: `documentation-profile-l0-process-context.yaml`, `documentation-profile-l1-process-group.yaml`, `documentation-profile-l2.yaml`, `documentation-profile-l3-activity.yaml`, `documentation-profile-l4-task.yaml`.
3. `scripts/check_documentation_profile.py` implements DOC-001..005.
4. Gate [21] Documentation Profile is wired as **advisory** in `scripts/conformance_result.py`.
5. `entities/v1-alpha/dea:process-customer-insight-and-retention/documentation/manifest.yaml` exists as the pilot scaffold.
6. `tests/test_check_documentation_profile.py` passes.
7. CR-BP-94-EXT-01 carrier CR is filed in `change-requests/`.
8. README row + CATALOG regen is committed.
9. Em-dash / en-dash audit: 0 violations in new prose.

---

## 14. What this slice is NOT

- **NOT a generator.** The README generator lands in EXT-04.
- **NOT a manifest schema.** The machine-readable documentation manifest schema lands in EXT-03.
- **NOT a catalog-wide rollout.** The pilot is a structural validation only; catalog-wide coverage is EXT-06.
- **NOT a re-opening of CR-BP-93.** The decomposition semantic contract is the source of truth for level mapping; this architecture references it without modifying it.
- **NOT a count-assertion change.** No canonical records are added or modified.
