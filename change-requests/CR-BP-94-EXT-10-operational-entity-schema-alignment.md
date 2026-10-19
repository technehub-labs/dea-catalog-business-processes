# CR-BP-94-EXT-10: Operational Entity Schema Alignment

Status: Proposed
Programme: CR-BP-94 Documentation Extension
Parent: CR-BP-94
Predecessors: CR-BP-94-EXT-08, CR-BP-94-EXT-09
Target repository: technehub-labs/dea-catalog-business-processes
Proposed path: change-requests/CR-BP-94-EXT-10-operational-entity-schema-alignment.md

1. Executive Summary

This CR aligns the Business Process catalogue’s canonical entity representation with the approved Operational Documentation Semantic Contract established by EXT-09.

The catalogue already contains operational properties, including inputs, transformation, outputs, responsibility, and boundary. This CR does not presume that these properties are deficient or that additional top-level fields are required.

It establishes a controlled schema assessment and extension process to ensure that:

* Each operational concept has one authoritative representation.
* Existing fields retain their established meaning unless explicitly migrated.
* Structured information is represented as structured data rather than embedded in prose.
* Entity YAML remains the authoritative source for canonical entity facts.
* Documentation-only metadata does not contaminate the canonical business entity model.
* New structures are backward compatible and validated consistently.

The outcome is an approved, decomposition-aware operational schema that supports subsequent authoring, generation, validation, and catalogue backfill.

2. Problem Statement

The existing Business Process template provides an initial operational structure, but the semantic contract identifies additional distinctions that may require structured representation.

These include triggers, preconditions, consumers, interfaces, dependencies, outcomes, roles, accountability, business rules, controls, exceptions, evidence, and provenance.

Introducing these properties without a schema-level reconciliation could result in:

1. Duplicate fields representing the same concept.
2. Different meanings being assigned to the same property.
3. Operational details being stored inconsistently as prose, YAML, and README content.
4. L0-L4 entities receiving fields that are inappropriate for their decomposition level.
5. Catalogue-specific structures duplicating concepts already governed by the OpenDEA metamodel.
6. Incompatible changes to existing records and generation scripts.

3. Objectives

This CR SHALL:

1. Inventory all existing entity schemas, templates, examples, and operational properties.
2. Map each EXT-09 concept to its current canonical representation, if one exists.
3. Identify genuine structural gaps.
4. Define the canonical data boundary between entity YAML and documentation metadata.
5. Establish common conventions for identifiers, references, descriptions, and enumerations.
6. Introduce only justified schema extensions.
7. Preserve existing records through backward-compatible migration.
8. Establish schema validation and migration tests.
9. Provide the structural foundation for EXT-11 through EXT-15.

4. Scope

Included

* L0-L4 entity schema and template review.
* Operational property inventory.
* YAML representation and cardinality decisions.
* Local identifiers and cross-entity references.
* Reconciliation with canonical OpenDEA entity and relationship definitions.
* Schema validation and migration.
* Documentation manifest boundary.
* Compatibility and deprecation policy.

Excluded

* Catalogue-wide content enrichment.
* Detailed operational authoring methodology.
* Workflow orchestration or execution models.
* Re-definition of Business Process, Activity, or Task.
* Changes to Business Capability, Business Function, Information System, or Metric metamodels.
* Automatic inference of operational data.

5. Required Schema Inventory

Before modifying schemas, implementation MUST inventory:

* All L0-L4 templates.
* All JSON Schema or equivalent validation definitions.
* Existing YAML entity records.
* README generator inputs.
* Documentation manifests and profile definitions.
* Existing metadata and relationship conventions.
* CI validation scripts and fixtures.
* Relevant metamodel definitions and approved ADRs.

The inventory MUST identify, for each property:

Attribute	Required finding
Property name	Existing canonical name
Entity levels	Where it currently appears
Data type	Scalar, object, array, reference, or other
Cardinality	Required, optional, repeatable
Meaning	Current documented semantics
Consumers	Generator, validator, tooling, other catalogues
Compatibility	Existing usage and migration impact
Disposition	Retain, clarify, extend, deprecate, or reject

6. Canonical Representation Decisions

The following are requirements for the schema design. They are not permission to introduce every suggested field without the inventory and metamodel review.

6.1 Existing fields

The existing properties MUST be evaluated first:

* inputs
* transformation
* outputs
* responsibility
* boundary

Their existing names and meanings MUST be preserved unless a documented migration is approved.

In particular, responsibility MUST NOT be silently replaced by a new roles object, and inputs or outputs MUST NOT be duplicated inside a new operational namespace.

6.2 Structured versus descriptive information

Use structured YAML when information needs to be:

* Referenced by another entity.
* Validated against a controlled vocabulary.
* Queried or filtered.
* Reused by generators or downstream tooling.
* Individually governed or assigned a lifecycle state.

Use descriptive prose where the information is explanatory and does not require independent identity or machine processing.

6.3 Candidate operational structures

The schema review MUST evaluate the following candidate structures:

Concern	Schema design question
Trigger	Is it an entity property, a relationship, or a documented invocation condition?
Preconditions	Are these structured conditions or descriptive constraints?
Inputs	Can the existing inputs structure express type, source, and validation?
Transformation	Is the current narrative field sufficient?
Outputs	Can the existing outputs structure express type, consumer, and acceptance criteria?
Outcomes	Does the concept already exist in the metamodel or another catalogue?
Interfaces	Are these canonical entities, typed references, or documentation assertions?
Dependencies	Which are canonical relationships and which are explanatory dependencies?
Roles	Are roles canonical entities or scoped operational assignments?
Accountability	How is authority represented without duplicating responsibility?
Rules	Are rules independently governed entities or references?
Controls	Are controls independently governed entities or references?
Exceptions	Are exception definitions reusable entities or process-specific assertions?
Evidence	Does evidence belong in the entity record or a documentation manifest?
Provenance	Can existing metadata support provenance, or is an assertion-level structure required?

6.4 Canonical entity data versus documentation metadata

The implementation MUST establish two explicit boundaries:

Canonical entity data

Contains stable, reusable business semantics and approved relationships that belong to the entity model.

Documentation and assertion metadata

Contains information about how an assertion was researched, sourced, reviewed, approved, inherited, or rendered.

Evidence provenance and editorial status MUST NOT be added as business semantics merely because they are useful for documentation.

The implementation MUST inspect existing metadata conventions before creating new structures.

7. Identifier and Reference Conventions

1. Every repeatable structured property MUST have a stable identifier within its defined scope.
2. Identifiers MUST follow existing repository conventions.
3. Local identifiers MUST be distinguishable from globally addressable entity IDs.
4. Cross-entity references MUST use canonical entity identifiers where those entities exist.
5. Free-text references MUST be visibly distinguishable from canonical references.
6. A reference MUST NOT be treated as valid merely because its string is syntactically valid.
7. Referential validation MUST distinguish missing references from unresolved external references.
8. Entity IDs and relationship types MUST remain consistent with the OpenDEA metamodel.

8. Decomposition-Level Schema Strategy

The schema architecture MUST support different operational properties by level.

Level	Schema responsibility
L0	Process scope, boundary, context and governed L0-specific metadata
L1	Process grouping, membership and grouping rationale
L2	Full Business Process operational transformation
L3	Activity-level contribution and operational semantics
L4	Bounded task action, expected result and verification

The implementation SHOULD use shared definitions for genuinely common structures while retaining level-specific requirements.

A shared schema component MUST NOT force an L0 or L1 entity to carry executable process fields.

9. Compatibility and Migration

All changes MUST follow an additive-first strategy.

* Existing valid entity YAML MUST continue to validate.
* New optional properties MUST have documented defaults or absence semantics.
* Existing property meanings MUST NOT change silently.
* Deprecated properties MUST have a migration path and deprecation notice.
* No bulk entity rewrite may occur without a deterministic migration and review.
* Schema versioning MUST follow repository conventions.
* Migration scripts MUST be repeatable and safe to rerun.
* A migration MUST NOT create placeholder business facts.

If a breaking change is genuinely necessary, it requires an explicit ADR, migration plan, compatibility window, and rollback procedure.

10. Repository Changes

Expected artefacts:

* schemas/: reconciled entity schemas and shared definitions.
* templates/: aligned L0-L4 YAML templates.
* docs/: schema mapping and operational data model guidance.
* scripts/: schema validation and migration tooling, where required.
* tests/: schema fixtures and backward-compatibility tests.
* change-requests/: this CR and updated CR register.

Exact filenames MUST follow the repository’s existing conventions rather than introducing a parallel schema directory.

11. Testing Requirements

The implementation MUST test:

1. Every existing entity YAML record against the proposed schemas.
2. Every L0-L4 template against its corresponding schema.
3. Required and optional property behaviour.
4. Array item and identifier uniqueness.
5. Valid and invalid canonical references.
6. Unknown or unsupported relationship types.
7. Backward compatibility with existing records.
8. Deterministic serialization and generation.
9. Repeated execution of migration scripts.
10. Invalid values and unsupported enumerations.
11. Separation of canonical entity data from documentation metadata.
12. No accidental requirement for operational properties at L0/L1.

12. Acceptance Criteria

* AC-01: An inventory of existing operational properties and their usage is published.
* AC-02: Every EXT-09 semantic concept has an explicit schema disposition.
* AC-03: Existing fields are retained, clarified, extended, or deprecated through documented decisions.
* AC-04: Duplicate representations are eliminated or explicitly governed.
* AC-05: Canonical entity data and documentation metadata have defined boundaries.
* AC-06: L0-L4 schema applicability is explicit.
* AC-07: Identifier and reference conventions are documented.
* AC-08: All existing valid records continue to validate or have approved migration dispositions.
* AC-09: Schema validation is integrated into the repository’s CI pipeline.
* AC-10: Migration scripts are repeatable and tested.
* AC-11: No workflow execution model is introduced.
* AC-12: The schema is ready for EXT-11 profile implementation.

13. Dependencies

* EXT-08: programme reconciliation.
* EXT-09: semantic contract.
* Existing OpenDEA metamodel definitions and approved relationship vocabulary.
* Existing repository schema and CI conventions.

14. Risks

Risk	Mitigation
Duplicate operational structures	Property inventory and semantic mapping before schema changes
Breaking existing records	Additive-first migration and regression tests
Documentation metadata enters the business model	Explicit data-boundary decision
L0/L1 become executable entities	Level-specific schema constraints
Cross-catalogue references become inconsistent	Canonical ID and relationship validation
Schema over-engineering	Introduce only structures with demonstrated reuse or validation need

15. Completion Definition

EXT-10 is complete when the catalogue has an approved, validated, backward-compatible operational schema aligned with EXT-09 and the OpenDEA metamodel.

The resulting schema MUST be suitable for level-specific profile enforcement and subsequent operational enrichment.