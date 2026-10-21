# CR-BP-94-EXT-17: Enrichment Tooling and Backfill Orchestration

**Status**: Proposed (awaiting Proceed)
**Layer**: Process Catalog (Cross-Cutting Documentation)
**Owner**: Emmanuel A. Otchere
**Programme**: CR-BP-94 Documentation Extension
**Parent**: CR-BP-94
**Predecessors**: CR-BP-94-EXT-10 through CR-BP-94-EXT-16
**Enables**: CR-BP-94-EXT-18 through CR-BP-94-EXT-24
**Type**: Repository engineering, automation and quality assurance
**Priority**: High
**Target repository**: technehub-labs/dea-catalog-business-processes
**Proposed path**: change-requests/CR-BP-94-EXT-17-enrichment-tooling-and-backfill-orchestration.md

## 1. Executive Summary

This CR establishes the repository tooling required to execute operational documentation enrichment at scale. The tooling supports controlled authoring, schema validation, evidence validation, README generation, parent-child reconciliation, migration and backfill reporting. It works with the repository's existing CI and automation architecture rather than introducing a competing toolchain.

## 2. Objectives

1. Make canonical entity data the source for generated documentation
2. Reduce manual documentation duplication
3. Provide deterministic validation and generation
4. Support controlled batch enrichment
5. Enable safe migration of existing entities
6. Produce actionable quality and completeness reports
7. Support staged rollout and rollback
8. Preserve the repository's established contribution workflow

## 3. Scope

### In scope

- Schema validation
- Profile-aware validation
- Evidence and provenance validation
- README generation
- Parent-child consistency checks
- Cross-reference validation
- Migration and backfill scripts
- Dry-run and reporting modes
- CI integration
- Error and warning reporting
- Reproducibility and idempotency

### Out of scope

- A new workflow execution engine
- A new enterprise process-management platform
- Automatic invention of missing operational content
- A separate documentation database
- Automatic approval of enriched entities

## 4. Normative Requirements

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

### REQ-17-04: Validation layers

Implement distinct validation layers:

1. Syntax validation: YAML or other source format is parseable
2. Schema validation: Fields and data structures conform to the canonical schema
3. Profile validation: Applicable L0 to L4 documentation requirements are satisfied
4. Semantic validation: Concept distinctions and value constraints are respected
5. Evidence validation: Required provenance and verification metadata are present
6. Reference validation: Referenced entities and identifiers resolve
7. Hierarchy validation: Parent-child relationships are coherent
8. Documentation validation: Generated README reflects canonical data
9. Governance validation: Required review or approval conditions are satisfied

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

## 5. Proposed Implementation Components

The implementation provides the following logical capabilities, whether as separate scripts or integrated modules:

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

## 6. Testing Requirements

Tests include:

- Valid and invalid entity examples at every level
- Missing and unknown values
- Invalid confidence and verification classifications
- Missing provenance where required
- Conflicting evidence
- Broken and valid cross-references
- Incorrect parent-child assignments
- README generation consistency
- Repeated migration and generation
- Dry-run non-mutation
- Rollback or recovery behaviour
- CI blocking and non-blocking conditions

## 7. Acceptance Criteria

- [ ] Existing tooling and CI inventory completed
- [ ] Canonical entity-to-README generation established
- [ ] Deterministic generation demonstrated
- [ ] Validation layers implemented
- [ ] Severity model implemented
- [ ] L0 to L4 profile selection works
- [ ] Evidence and reference validation works
- [ ] Parent-child validation works
- [ ] Dry-run and idempotent migration supported
- [ ] Catalogue-level reporting available
- [ ] CI integration tested
- [ ] No automatic invention of operational facts
- [ ] Documentation for contributors and maintainers published
- [ ] Pilot can be executed without manual reconstruction of the tooling

## 8. Completion Definition

EXT-17 is complete when the enrichment toolchain can validate, generate, migrate and report on a controlled set of process entities and is ready to support the pilot.

## 9. References

- `change-requests/CR-BP-94-EXT-17-enrichment-tooling-and-backfill-orchestration.md` (this CR)
- `docs/operational-documentation-programme/CR-BP-94-EXT-15-to-18-detailed-design.md` (the detailed design; preserved user submission)
- `scripts/conformance_result.py` (the existing gate orchestrator; EXT-17 may extend)
- `scripts/generate_readmes.py` (the existing generator; EXT-17 will document the canonical source contract)
- `scripts/validate_readme_structure.py` (the EXT-04 validator; EXT-17 will document the validation layer hierarchy)
