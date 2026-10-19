# Enrichment Tooling and Backfill Orchestration (CR-BP-94-EXT-17)

**Status**: Normative (proposed for adoption under CR-BP-94-EXT-17)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-19
**Source CR**: CR-BP-94-EXT-17 (Enrichment Tooling and Backfill Orchestration)
**Parent programme**: DEA-PROCESS-ENRICH-000
**Predecessors**: EXT-10 through EXT-16 (all SEALED)
**Tranche**: Engineering and governance readiness tranche (EXT-15..18) - THIRD SLICE
**Enables**: EXT-18 (pilot), then EXT-19+ (catalogue enrichment)
**Repository**: technehub-labs/dea-catalog-business-processes

---

## 1. Purpose

This document is the **EXT-17 tooling inventory and orchestration contract**. It establishes the repository tooling required to execute operational documentation enrichment at scale. The tooling supports controlled authoring, schema validation, evidence validation, README generation, parent-child reconciliation, migration and backfill reporting.

It works with the repository's existing CI and automation architecture rather than introducing a competing toolchain.

---

## 2. The 15 normative requirements (per the EXT-17 CR)

### REQ-17-01: Tooling inventory

Before implementation, inspect and document:

- Existing schema and template locations
- Existing entity formats and conventions
- README generation mechanisms
- Existing scripts and command interfaces
- CI workflows and validation stages
- Existing test frameworks
- Existing migration utilities
- Repository contribution and release practices

No replacement tooling is introduced until the existing mechanisms have been assessed.

### REQ-17-02: Canonical source

Entity data remains the canonical source for operational facts. README files are generated from canonical entity data and approved templates. Where README files contain manually maintained content that cannot be represented in the entity model, the implementation identifies and governs that content explicitly rather than silently overwriting it.

### REQ-17-03: Deterministic generation

Given identical entity data, schema version, profile version and generator version, documentation generation produces equivalent output. Generation does not depend on undocumented environmental state or uncontrolled external services.

### REQ-17-04: The 9 validation layers

1. **Syntax validation**: YAML or other source format is parseable
2. **Schema validation**: Fields and data structures conform to the canonical schema
3. **Profile validation**: Applicable L0 to L4 documentation requirements are satisfied
4. **Semantic validation**: Concept distinctions and value constraints are respected
5. **Evidence validation**: Required provenance and verification metadata are present
6. **Reference validation**: Referenced entities and identifiers resolve
7. **Hierarchy validation**: Parent-child relationships are coherent
8. **Documentation validation**: Generated README reflects canonical data
9. **Governance validation**: Required review or approval conditions are satisfied

A single generic pass/fail result does not conceal the category of failure.

### REQ-17-05: Severity model

Validation findings support:

- `error`: invalid or unsafe state that blocks acceptance
- `warning`: quality concern requiring review
- `info`: advisory observation
- `deferred`: recognized incomplete requirement with an accepted disposition

Warnings are not silently converted into successful compliance.

### REQ-17-06: Dry-run support

Backfill and migration utilities support a dry-run mode that reports proposed changes without modifying repository files. Reports identify:

- Entities examined
- Fields or structures affected
- Existing content retained
- Proposed changes
- Validation findings
- Unresolved references
- Entities requiring human review

### REQ-17-07: Idempotency

Migration and generation operations are idempotent. Repeated execution against unchanged source data does not introduce duplicate fields, duplicate records, reordered content without reason or repeated migration effects.

### REQ-17-08: Safe migration

Migration tooling:

- Preserves existing identifiers
- Preserves existing semantic meaning
- Avoids overwriting manually authored content without explicit rules
- Provides pre-migration and post-migration validation
- Supports a documented recovery or rollback strategy
- Records migration version and results where appropriate

### REQ-17-09: Profile-aware generation

The generator uses the correct L0 to L4 profile. It does not generate operational sections that are inappropriate to the entity's decomposition level.

### REQ-17-10: Evidence-aware generation

Generated documentation distinguishes verified, provisional, unverified, disputed and deferred assertions where the profile requires that distinction. It does not render unverified material as established fact.

### REQ-17-11: Cross-reference validation

Where an entity references another catalogue entity, validation confirms:

- The reference follows the canonical identifier convention
- The target exists or is explicitly marked as an approved unresolved dependency
- The relationship is permitted by the metamodel
- The referenced entity is not confused with a similarly named entity

### REQ-17-12: Reporting

Provide reports at both entity and catalogue levels. Catalogue-level reporting includes:

- Total entities examined by level
- Profile completeness
- Evidence coverage
- Verification status distribution
- Outstanding warnings and errors
- Broken references
- Parent-child reconciliation status
- Entities awaiting owner review
- Backfill completion status

### REQ-17-13: CI integration

Integrate the validation stages into the existing CI pipeline. The implementation identifies which checks are blocking at initial rollout and which become blocking only after the relevant backfill or migration gate is passed.

### REQ-17-14: No automatic semantic invention

The tooling may identify missing information and propose candidate enrichment actions. It does not create operational assertions merely to satisfy required-field checks.

### REQ-17-15: Contributor usability

Provide clear commands or documented execution procedures for:

- Validating one entity
- Validating a selected set
- Validating the entire catalogue
- Generating one README
- Generating all applicable READMEs
- Running a migration in dry-run mode
- Producing a backfill report

Exact commands follow the repository's established tooling conventions.

---

## 3. The 9 logical components (per the EXT-17 CR)

The implementation provides these logical capabilities, whether as separate scripts or integrated modules:

| Component | Responsibility |
|---|---|
| Entity validator | Syntax and schema conformance |
| Profile validator | L0 to L4 requirements |
| Evidence validator | Provenance and verification |
| Reference validator | Canonical identifier resolution |
| Hierarchy validator | Parent-child integrity |
| README generator | Canonical data to documentation |
| Migration utility | Controlled schema/data migration |
| Backfill orchestrator | Controlled execution across entity sets |
| Quality reporter | Entity and catalogue status reporting |

These are logical components, not mandatory filenames or a prescription to create unnecessary separate executables.

---

## 4. Existing tooling inventory (per REQ-17-01)

The dea-catalog-processes repository already has the following scripts:

| Script | Component | EXT source |
|---|---|---|
| `scripts/validate_process_entries.py` | Entity validator | pre-existing |
| `scripts/check_l2_qualification.py` | Profile validator (L2) | CR-BP-34a |
| `scripts/check_intent_purposive.py` | Semantic validator | CR-BP-34b |
| `scripts/check_lifecycle_state.py` | Lifecycle validator | CR-BP-34c |
| `scripts/check_semantic_identity_version.py` | Semantic validator | CR-BP-34d |
| `scripts/check_activity_model.py` | Activity model | CR-BP-32 |
| `scripts/check_execution_boundary.py` | Execution boundary | CR-BP-33 |
| `scripts/check_mece.py` | MECE coverage | CR-BP-36 |
| `scripts/check_canonical_serves.py` | Canonical serves | CR-BP-31 |
| `scripts/check_entity_system.py` | Entity system | CR-BP-123/125 |
| `scripts/validate_readme_structure.py` | Documentation validator (EXT-04) | CR-BP-94-EXT-04 |
| `scripts/check_decomposition_reconciliation.py` | Hierarchy validator (EXT-05) | CR-BP-94-EXT-05 |
| `scripts/check_profile_registry_ext11.py` | Profile validator (EXT-11) | CR-BP-94-EXT-11 |
| `scripts/check_inputs_outputs_interfaces_ext12.py` | Evidence validator (EXT-12) | CR-BP-94-EXT-12 |
| `scripts/check_responsibility_accountability_ext13.py` | Evidence validator (EXT-13) | CR-BP-94-EXT-13 |
| `scripts/check_business_rules_controls_exceptions_ext14.py` | Evidence validator (EXT-14) | CR-BP-94-EXT-14 |
| `scripts/check_evidence_provenance_ext15.py` | Evidence validator (EXT-15) | CR-BP-94-EXT-15 |
| `scripts/check_authoring_methodology_ext16.py` | Governance validator (EXT-16) | CR-BP-94-EXT-16 |
| `scripts/generate_readmes.py` | README generator | CR-BP-94-EXT-07 |
| `scripts/conformance_result.py` | Orchestrator (gates [1]-[41]) | CR-BP-16 §18 |

**This inventory is the EXT-17 source of truth.** EXT-17 does NOT introduce competing tooling; it provides the orchestration and reporting layer that consumes the existing scripts.

---

## 5. The new tooling components (EXT-17 lands these)

| Component | Script | Purpose |
|---|---|---|
| Backfill orchestrator | `scripts/orchestrate_backfill.py` | Drives the EXT-16 metadata.authoring state machine; selects entities by state; runs the relevant validators; emits the EXT-19 backfill progress report |
| Catalogue-level reporter | `scripts/report_catalogue_status.py` | Implements REQ-17-12 (per-level counts, profile completeness, evidence coverage, verification status distribution, outstanding findings, broken references, parent-child reconciliation, entities awaiting owner review, backfill completion) |

The orchestrator and reporter consume the existing validators; they do not duplicate them. The orchestrator's job is to:
1. Walk the catalogue
2. For each entity, determine the EXT-16 metadata.authoring.state
3. Select the appropriate validators based on the state
4. Aggregate findings with the EXT-17 severity model (error / warning / info / deferred)
5. Emit a per-entity report and a catalogue-level report
6. Support dry-run (no file writes) and live-run (the EXT-19 backfill)

The reporter's job is to surface the EXT-17 REQ-17-12 reporting dimensions in a single command, for both entity-level and catalogue-level views.

---

## 6. The 7 contributor commands (REQ-17-15)

The EXT-17 contributor commands:

```bash
# Validate one entity
python3 scripts/conformance_result.py --entity <id>

# Validate a selected set
python3 scripts/conformance_result.py --catalog-root entities/v1-alpha/<cell>/

# Validate the entire catalogue
python3 scripts/conformance_result.py

# Generate one README
python3 scripts/generate_readmes.py --entity <id>

# Generate all applicable READMEs
python3 scripts/generate_readmes.py --force

# Run a migration in dry-run mode
python3 scripts/orchestrate_backfill.py --dry-run

# Produce a backfill report
python3 scripts/report_catalogue_status.py
```

These are the established repository commands. The orchestrator and reporter extend the existing toolchain; they do not replace it.

---

## 7. Compatibility and migration

EXT-17 is **additive**:

- The existing `scripts/conformance_result.py` orchestrator (gates [1]-[41]) is preserved.
- The new `orchestrate_backfill.py` and `report_catalogue_status.py` are added.
- No existing validator is changed.
- The EXT-16 metadata.authoring state (already established in PR #185) is the input the orchestrator consumes.

The 244 existing records have **0** `metadata.authoring` blocks (per the EXT-16 inventory). The EXT-19 L2 backfill tranche is the work that populates them; the orchestrator will then process them in dependency order.

---

## 8. Validator and manifest

EXT-17 lands:

- `scripts/orchestrate_backfill.py` (the orchestrator; ~the EXT-17 REQ-17-06 dry-run + REQ-17-07 idempotency + REQ-17-12 reporting consumer)
- `scripts/report_catalogue_status.py` (the reporter; the EXT-17 REQ-17-12 implementation)
- `reconciliation/tooling-manifest.json` (per-record manifest of the orchestrator's findings)
- `gate [42] Enrichment Tooling` wired ADVISORY in `scripts/conformance_result.py`
- `tests/test_enrichment_tooling_ext17.py` (unit + integration)

The orchestrator enforces:

- **OR-001**: dry-run mode does not modify repository files (idempotency)
- **OR-002**: per-record selection by `metadata.authoring.state` (the 9-value vocabulary)
- **OR-003**: per-record execution of the relevant validators (state-driven)
- **OR-004**: severity mapping (error / warning / info / deferred)
- **OR-005**: no automatic invention (REQ-17-14; the orchestrator only reports, it does not write content)

The reporter enforces:

- **RP-001**: per-level counts (49 L0 + 50 L1 + 145 L2 = 244)
- **RP-002**: profile completeness (per-level)
- **RP-003**: evidence coverage (the EXT-15 fields per record)
- **RP-004**: verification status distribution (the EXT-15 verification_status per record)
- **RP-005**: outstanding warnings and errors (per validator)
- **RP-006**: broken references (the EXT-12 source/consumer cross-references)
- **RP-007**: parent-child reconciliation status
- **RP-008**: entities awaiting owner review (the EXT-16 metadata.authoring.state = `under_review`)
- **RP-009**: backfill completion status (per-level count of records with `state: published`)

---

## 9. References

- `scripts/orchestrate_backfill.py` (the orchestrator)
- `scripts/report_catalogue_status.py` (the reporter)
- `scripts/conformance_result.py` (the existing orchestrator; gates [1]-[41])
- `templates/business-process.yaml` (the L2 template; consumes the EXT-17 tooling)
- `change-requests/CR-BP-94-EXT-17-enrichment-tooling-and-backfill-orchestration.md` (the EXT-17 CR)
- `docs/operational-documentation-programme/CR-BP-94-EXT-15-to-18-detailed-design.md` (the detailed design; preserved user submission)
- `docs/operational-authoring-methodology.md` (EXT-16; the methodology the orchestrator consumes)
- `docs/evidence-provenance-confidence.md` (EXT-15; the evidence framework the orchestrator consumes)
- `docs/inputs-outputs-interface-semantics.md` (EXT-12)
- `docs/responsibility-accountability-model.md` (EXT-13)
- `docs/business-rules-controls-exceptions.md` (EXT-14)
- `reconciliation/programme-register.json` (the 17-CR register)
- `reconciliation/tooling-manifest.json` (EXT-17 manifest)
