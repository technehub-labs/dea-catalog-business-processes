<!--
Source: User submission "CR-BP-94-EXT-10_to_14.md" (detailed design for CR-BP-94-EXT-10 through CR-BP-94-EXT-14; the semantic-model implementation tranche).
The user supplied this as a single file with all 5 CRs in sequence plus a preamble explaining the rationale and dependency map. Preserved here for traceability. The 5 CRs have been split into separate files:
- change-requests/CR-BP-94-EXT-10-operational-entity-schema-alignment.md
- change-requests/CR-BP-94-EXT-11-decomposition-level-documentation-profiles.md
- change-requests/CR-BP-94-EXT-12-process-inputs-outputs-and-interface-semantics.md
- change-requests/CR-BP-94-EXT-13-process-responsibility-and-accountability-model.md
- change-requests/CR-BP-94-EXT-14-business-rules-controls-and-exception-semantics.md
D-004 cleanup applied: em-dashes, en-dashes, and three-em-dashes (U+2E3B) replaced with colons, hyphens, and "---" respectively.
-->

The next five documents are CR-BP-94-EXT-10 through EXT-14. They form the semantic-model implementation tranche: first reconcile the existing entity schema, then establish level-specific documentation profiles, and finally formalize process interfaces, accountability, and governance controls.

The dependency is deliberate: EXT-10 and EXT-11 establish the structural foundation; EXT-12, EXT-13 and EXT-14 define the operational domains that will populate it. These CRs assume EXT-08 and EXT-09 have been reviewed and approved. They are proposed specifications, not claims that repository changes have already been implemented.

CR-BP-94-EXT-10: Operational Entity Schema Alignment

CR-BP-94-EXT-10: Operational Entity Schema Alignment

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

CR-BP-94-EXT-11: Decomposition-Level Operational Documentation Profiles

CR-BP-94-EXT-11: Decomposition-Level Operational Documentation Profiles

Status: Proposed
Programme: CR-BP-94 Documentation Extension
Parent: CR-BP-94
Predecessors: EXT-08, EXT-09, EXT-10
Target repository: technehub-labs/dea-catalog-business-processes
Proposed path: change-requests/CR-BP-94-EXT-11-decomposition-level-documentation-profiles.md

1. Executive Summary

This CR defines the operational documentation requirements for each decomposition level from L0 to L4.

The purpose is to prevent the catalogue from applying one generic operational documentation template to entities with fundamentally different responsibilities.

L0 and L1 are architectural organization constructs. L2 is the principal Business Process transformation level. L3 represents cohesive Activities within a Business Process. L4 represents bounded Tasks.

Each level therefore requires a distinct documentation profile, with shared semantic components only where their meaning is genuinely common.

The profiles will govern:

* Required documentation sections.
* Conditional sections.
* Not-applicable sections.
* Expected semantic depth.
* Parent-child contribution.
* Completeness states.
* Evidence and review requirements.
* README generation and validation.

2. Problem Statement

A generic README template risks treating all entity levels as if they execute operational transformations.

This can result in:

* Inputs and outputs being requested from non-executable L0/L1 entities.
* L2 Business Processes being documented without their actual transformation.
* L3 Activities becoming duplicate Business Processes.
* L4 Tasks becoming procedural workflow definitions.
* Parent-level content being copied into children without applicability.
* Validators treating intentionally inapplicable information as missing.

The catalogue requires profile-driven documentation requirements rather than universal field presence.

3. Objectives

This CR SHALL:

1. Define a profile for each L0-L4 entity level.
2. Define required, conditional, optional, and not-applicable concerns.
3. Define minimum documentation depth.
4. Establish profile-aware README generation.
5. Establish profile-aware validation.
6. Define parent-child documentation consistency requirements.
7. Define how profile versions are identified and evolved.
8. Prevent a single profile from imposing inappropriate operational semantics across all levels.

4. Profile Model

A documentation profile is a governed specification of what documentation is expected for a particular entity type or decomposition level.

A profile MUST identify:

* Profile identifier.
* Profile version.
* Applicable entity type and level.
* Required sections.
* Conditional sections.
* Optional sections.
* Not-applicable sections.
* Semantic requirements.
* Evidence requirements.
* Validation rules.
* Rendering instructions.
* Applicable lifecycle states.

A profile defines documentation expectations; it does not redefine the entity’s canonical metamodel type.

5. Requirement Classification

Every profile requirement MUST use one of the following classifications:

Classification	Meaning
required	Must be present for a conformant entity
conditional	Required when a documented applicability condition holds
optional	May be supplied when useful and supported
not_applicable	Not applicable to this entity level or context
inherited	May be supplied from an authoritative parent or referenced source, subject to applicability validation

A required section may still have an incomplete lifecycle state. Structural presence and semantic approval are separate validation dimensions.

6. L0 Process Scope Profile

L0 establishes the overall scope and boundary of the process architecture.

Required

* Entity identity and definition.
* Scope purpose.
* Scope boundary.
* Inclusions and exclusions.
* Decomposition rationale.
* Relationships to relevant L1 groups.
* Source and governance metadata.

Conditional

* Strategic context.
* Enterprise-wide measurement context.
* External obligations.
* Scope-level assumptions and limitations.

Not applicable

* Operational inputs.
* Executable transformation.
* Process outputs.
* Performer assignments.
* Task-level controls.
* Workflow sequencing.

L0 MUST NOT be represented as executing a Business Process.

7. L1 Process Group Profile

L1 groups related Business Processes.

Required

* Entity identity and definition.
* Grouping purpose.
* Membership rationale.
* Scope and boundary.
* Member Business Processes.
* Grouping criteria.
* Governance and source metadata.

Conditional

* Shared business rules.
* Shared governance arrangements.
* Cross-process dependencies.
* Group-level performance context.

Not applicable

* Independent operational transformation.
* Executable task instructions.
* Process-level input/output contracts unless they are explicitly group-level interfaces governed by another approved model.

An L1 group MUST NOT acquire operational properties merely by aggregating the properties of its member processes.

8. L2 Business Process Profile

L2 is the principal operational transformation level.

Required

* Entity identity and definition.
* Business purpose.
* Scope and boundary.
* Parent L1 relationship where applicable.
* Trigger or invocation condition, where established.
* Inputs and their sources, where the process has inputs.
* Transformation.
* Outputs and consumers, where the process produces outputs.
* Responsibility.
* Decomposition into L3 Activities, where decomposed.
* Evidence and provenance for curated operational assertions.

Conditional

* Preconditions.
* Outcomes.
* Interfaces.
* Dependencies.
* Roles and performers.
* Accountability.
* Business rules.
* Controls.
* Exceptions.
* Measures and performance relationships.

Not applicable

No operational section is automatically mandatory merely because it exists in the shared semantic vocabulary. Applicability must be assessed and recorded.

The L2 README MUST enable a reader to understand the process’s purpose, boundary, transformation, and principal operational relationships without requiring them to reconstruct its meaning from its Activity list.

9. L3 Activity Profile

L3 describes a cohesive body of work within an L2 Business Process.

Required

* Entity identity and definition.
* Parent Business Process.
* Activity purpose.
* Cohesion rationale.
* Scope and boundary.
* Contribution to the parent transformation.
* Description of the Activity’s work.
* Relevant inputs and outputs, where applicable.
* Evidence and provenance for curated assertions.

Conditional

* Trigger or activation condition.
* Preconditions.
* Roles and performers.
* Responsibility and accountability.
* Business rules.
* Controls.
* Exceptions.
* Dependencies and interfaces.
* Completion or acceptance criteria.

An Activity MUST NOT simply repeat the complete operational description of its parent process.

It MUST describe the work that differentiates it within the parent’s transformation.

10. L4 Task Profile

L4 describes a bounded, actionable, independently verifiable unit of work.

Required

* Entity identity and definition.
* Parent Activity.
* Bounded action description.
* Relevant working object or input, where applicable.
* Expected result or completion condition.
* Verification or acceptance evidence.
* Relevant responsibility or performer, where established.

Conditional

* Preconditions.
* Business rules.
* Controls.
* Exceptions.
* Dependencies.
* Required authorization.
* Evidence artefacts.

Prohibited

* Workflow instance identifiers.
* Runtime execution state.
* Orchestration configuration.
* Sequence or branching logic.
* Retry policy.
* Runtime event history.
* Workflow-engine implementation details.

These belong in separately governed execution or workflow models.

11. Parent-Child Documentation Consistency

The profiles MUST support reconciliation between parent and child entities.

11.1 Parent purpose and child contribution

Each child entity MUST explain how it contributes to the parent’s purpose.

11.2 Decomposition completeness

Where an entity is decomposed, the documentation SHOULD identify the decomposition coverage and any known gaps.

11.3 No automatic inheritance

A child MUST NOT automatically inherit all parent inputs, outputs, rules, controls, roles, or dependencies.

Inheritance requires:

1. An identifiable authoritative source.
2. A semantic reason for inheritance.
3. Applicability to the child.
4. An explicit inheritance disposition.
5. A traceable reference.

11.4 Reconciliation findings

The documentation system SHOULD identify:

* Parent assertions not addressed by children.
* Child assertions not aligned with parent semantics.
* Duplicated assertions.
* Conflicting definitions.
* Missing decomposition coverage.
* Unjustified inherited content.

These findings must be reviewable and must not automatically rewrite entity content.

12. Profile and Generator Integration

The README generator MUST select the appropriate profile based on canonical entity type and decomposition level.

It MUST:

* Render only applicable sections.
* Display conditional sections when applicable.
* Distinguish missing content from not-applicable content.
* Display inherited content with its source.
* Avoid presenting unapproved assertions as approved facts.
* Preserve consistent section ordering.
* Remain deterministic.

The validator MUST distinguish:

1. Structural profile conformance.
2. Semantic completeness.
3. Evidence completeness.
4. Approval status.
5. Parent-child consistency.

A single pass/fail indicator MUST NOT conceal these distinct dimensions.

13. Profile Versioning

Each profile MUST be versioned independently or through an established repository-wide profile versioning mechanism.

Changes to required fields, applicability, or semantic expectations MUST be versioned and documented.

Existing entity records MUST identify or resolve to the profile version used for their validation.

A profile update MUST NOT silently make previously valid records invalid without a migration or transition policy.

14. Repository Changes

Expected artefacts:

* docs/decomposition-level-documentation-profiles.md
* profiles/ or the existing profile directory, using repository conventions.
* L0, L1, L2, L3 and L4 profile definitions.
* Profile validation fixtures.
* README generator profile selection updates.
* Profile-aware validation tests.
* Updated decomposition template guide.
* CR register entry.

No parallel profile directory should be created if the repository already has an authoritative location.

15. Testing Requirements

* Every entity level resolves to exactly one applicable profile version.
* Required and conditional sections behave correctly.
* Not-applicable fields are not reported as missing.
* L0/L1 are not required to provide executable transformation data.
* L2 requires a meaningful transformation description.
* L3 identifies its parent and contribution.
* L4 identifies a bounded action and completion condition.
* Parent-child inheritance is explicit and traceable.
* Generator output is deterministic.
* Profile upgrades do not silently break existing records.
* Existing catalogue records remain readable and migratable.

16. Acceptance Criteria

* AC-01: L0-L4 profiles are defined and versioned.
* AC-02: Each profile has required, conditional, optional, and not-applicable classifications.
* AC-03: L0 and L1 are explicitly non-executable.
* AC-04: L2 documents the principal process transformation.
* AC-05: L3 documents cohesive work and contribution to its parent.
* AC-06: L4 documents bounded work and verification.
* AC-07: No L4 workflow orchestration semantics are introduced.
* AC-08: Inheritance requires explicit source and applicability.
* AC-09: Generator profile selection is deterministic.
* AC-10: Validation distinguishes structural, semantic, evidence, and approval status.
* AC-11: Profile versioning and transition rules are documented.
* AC-12: The profiles support the operational domains in EXT-12 through EXT-15.

17. Dependencies and Completion

EXT-11 depends on approved EXT-09 semantics and EXT-10 schema decisions.

EXT-11 is complete when all five profiles are implemented, validated, linked from the documentation architecture, and usable by the README generator and validator.

CR-BP-94-EXT-12: Process Inputs, Outputs and Interface Semantics

CR-BP-94-EXT-12: Process Inputs, Outputs and Interface Semantics

Status: Proposed
Programme: CR-BP-94 Documentation Extension
Parent: CR-BP-94
Predecessors: EXT-08, EXT-09, EXT-10, EXT-11
Target repository: technehub-labs/dea-catalog-business-processes
Proposed path: change-requests/CR-BP-94-EXT-12-process-inputs-outputs-and-interface-semantics.md

1. Executive Summary

This CR formalizes how the Business Process catalogue describes the operational interfaces through which processes receive information and other business objects, transform them, and produce outputs.

It establishes a consistent model for:

* Triggers.
* Preconditions.
* Inputs.
* Input sources.
* Transformations.
* Outputs.
* Output consumers.
* Outcomes.
* Interfaces.
* Dependencies.
* Acceptance and validation criteria.

The objective is to make the operational boundaries of a Business Process explicit and traceable, while preserving the distinction between business semantics, system interfaces, workflow execution, and organizational responsibilities.

The existing inputs, transformation, and outputs properties remain the starting point. This CR extends their semantic precision and determines what additional structures are justified by the approved schema architecture.

2. Problem Statement

A process catalogue that only names inputs and outputs is insufficient for reliable enterprise analysis if it does not explain:

* Where inputs originate.
* Whether an input is mandatory.
* What the process does with it.
* What constitutes an acceptable input.
* What output is produced.
* Who or what consumes the output.
* Which external interactions are required.
* Which dependencies can affect the process.
* How outputs relate to intended outcomes.

Inconsistent treatment also creates confusion between:

* Inputs and resources.
* Triggers and inputs.
* Preconditions and triggers.
* Outputs and outcomes.
* Consumers and recipients.
* Interfaces and dependencies.
* Business interfaces and technical system interfaces.

This CR establishes the operational interface contract needed for process analysis, capability traceability, information-system mapping, process improvement, and eventual automation analysis.

3. Objectives

This CR SHALL:

1. Define a consistent operational input/output representation.
2. Clarify the relationship between inputs, transformation, outputs, and outcomes.
3. Establish source and consumer traceability.
4. Define trigger and precondition representation.
5. Distinguish business interfaces from system interfaces.
6. Establish dependency documentation rules.
7. Define input acceptance and output quality requirements.
8. Support L2, L3, and L4 profiles without forcing L0/L1 execution semantics.
9. Enable future traceability to Business Capabilities, Information Systems, Information Systems Functions, and Metrics through approved canonical relationships.
10. Provide a basis for operational process analysis without introducing workflow-engine semantics.

4. Conceptual Operational Contract

The documented process transformation MUST be understandable through the following conceptual relationship:

Trigger / Invocation Condition
             |
             v
       Preconditions
             |
             v
      Input Acquisition
             |
             v
       Transformation
             |
             v
       Output Production
             |
             v
       Output Consumption
             |
             v
       Intended Outcome

This is a semantic model, not a required execution sequence. Actual processes may involve iterative, concurrent, or conditional work. This CR does not define workflow orchestration.

5. Trigger and Preconditions

5.1 Trigger representation

Where supported by the schema, a trigger SHOULD identify:

* Trigger identifier.
* Trigger name.
* Trigger description.
* Trigger type or category.
* Trigger source.
* Applicability.
* Supporting evidence.

Trigger categories MAY include:

* Event-driven.
* Time-driven.
* Request-driven.
* Condition-driven.
* Decision-driven.
* External obligation-driven.

The categories are proposed classifications. Their final controlled vocabulary must be agreed during implementation.

A trigger MUST identify the circumstance that invokes the process, not simply describe what the process achieves.

5.2 Preconditions

A precondition SHOULD identify:

* The condition that must hold.
* The scope in which it applies.
* The entity or source that establishes the condition.
* The means by which it is verified, where established.
* The consequence if it is not satisfied.

Preconditions MUST NOT be conflated with input validation rules.

5.3 Missing or unknown trigger information

Where a trigger is not known, the entity MUST record the appropriate documentation state rather than inventing a generic trigger such as “business requirement received”.

Where a process is continuously operating or invoked through multiple mechanisms, the documentation SHOULD explain that invocation model rather than force one artificial trigger.

6. Input Model

6.1 Input definition

An input is a business object, information object, request, decision, material, or other item consumed, assessed, transformed, or used by the process.

6.2 Required input attributes

Each structured input SHOULD support:

Attribute	Purpose
id	Stable local identifier
name	Human-readable name
description	Business meaning
source	Origin or supplying entity
type	Classification, where governed
required	Whether it is mandatory
acceptance_criteria	Conditions for acceptable use
validation	Applicable validation requirements
provenance	Source of the assertion

The implementation MUST reconcile these attributes with the existing template and schema before adopting them.

6.3 Input classifications

The schema design SHOULD consider whether the following classifications are useful:

* Information.
* Business object.
* Request.
* Decision.
* Transaction.
* Material.
* Document or record.
* External data.
* Prior process output.

These classifications MUST remain extensible and MUST NOT imply that every input requires a new canonical entity type.

6.4 Input versus resource

The following distinction is mandatory:

Item	Treatment
Customer application	Input
Customer record being assessed	Input or working object, depending on context
Employee performing assessment	Performer/resource
CRM platform	System dependency/resource
Regulatory requirement	Rule or constraint, potentially also a referenced source
Submission deadline	Precondition or temporal constraint
Approval event invoking review	Trigger

The same real-world object may play different roles in different process contexts. Classification must follow its function in the documented transformation.

7. Transformation Model

The existing transformation property remains the primary description of what the Business Process does.

The transformation description MUST:

1. Express the business change, assessment, decision, or service activity.
2. Explain how relevant inputs are used.
3. Explain the business logic or governing principles at an appropriate level.
4. Describe the nature of the resulting outputs.
5. Avoid duplicating a detailed task sequence.
6. Avoid merely restating the process title.
7. Avoid embedding system implementation details unless they are essential to the business semantics.

A transformation MAY be expressed as structured narrative or a more formal representation if the schema and metamodel justify it.

This CR does not require every process to have a mathematically formal transformation function.

8. Output Model

8.1 Output definition

An output is a result, artefact, decision, service result, information object, or changed business object produced by the process.

8.2 Required output attributes

Each structured output SHOULD support:

Attribute	Purpose
id	Stable local identifier
name	Human-readable name
description	Business meaning
consumer	Entity, role, process, or party using the output
type	Classification, where governed
acceptance_criteria	Conditions defining acceptable output
quality_attributes	Relevant quality expectations
provenance	Source of the assertion

The implementation MUST reconcile these attributes with the existing schema.

8.3 Output versus outcome

Every output must be described as a produced result. An outcome describes the effect achieved through its use.

For example:

* Process: Manage Customer Relationship.
* Output: Updated customer relationship record and approved engagement plan.
* Consumer: Account management function or downstream process.
* Outcome: Improved continuity and effectiveness of customer engagement.

These are illustrative distinctions, not assertions about the actual operation of any particular catalogue entity.

8.4 Output consumers

A consumer MAY be:

* Another Business Process.
* An Activity or Task.
* A Business Function.
* An organizational role.
* An Information System.
* An external party.
* A customer or supplier.

A consumer reference MUST use the canonical entity identifier when the referenced entity exists in the governed model.

9. Outcomes

An outcome SHOULD identify:

* Desired business effect.
* Beneficiary or stakeholder.
* Relevant output or outputs.
* Conditions required to realize the outcome.
* Measurement relationship, where governed.
* Evidence or source.

The catalogue MUST NOT claim that an outcome has been achieved merely because an output exists.

Outcome documentation MUST distinguish intended outcomes from measured outcomes.

10. Interface Model

10.1 Business interface

A business interface is a defined point of interaction between business entities or participants.

Examples include:

* Customer submission channel.
* Supplier hand-off.
* Approval authority interaction.
* Internal service request.
* Regulatory submission.
* Handover to another Business Process.

10.2 Information interface

An information interface defines the exchange of information or records between participants or entities.

It SHOULD identify:

* Information exchanged.
* Sending party.
* Receiving party.
* Exchange purpose.
* Relevant format or standard, where established.
* Exchange conditions.
* Evidence or source.

10.3 System interface

A system interface is an interface mediated by an Information System or technical service.

Where canonical Information System and Information Systems Function entities exist, the process catalogue SHOULD reference them through approved relationships or references.

A system interface MUST NOT be represented as a Business Process input or output merely because an application transmits the data.

10.4 Interface classification

The implementation SHOULD support a governed classification such as:

* Human.
* Organizational.
* Information.
* System.
* Physical.
* Contractual.
* Regulatory.

The final vocabulary must be approved and versioned.

11. Dependencies

Dependencies MUST identify material reliance on another entity, resource, service, decision, or condition.

A dependency SHOULD capture:

* Dependent entity.
* Dependency target.
* Dependency type.
* Business consequence of unavailability or failure.
* Criticality, where governed.
* Source or evidence.

The schema MUST distinguish dependency references from decomposition relationships.

No new canonical relationship type may be introduced by this CR without confirmation from the OpenDEA metamodel.

12. L2-L4 Application

Concern	L2 Business Process	L3 Activity	L4 Task
Trigger	Process invocation	Activity activation, where meaningful	Task initiation condition, where meaningful
Preconditions	Process conditions	Activity conditions	Task conditions
Inputs	Process-level business inputs	Activity working inputs	Task working objects
Transformation	Full process transformation	Cohesive activity work	Bounded action
Outputs	Process outputs	Activity results	Task result
Outcomes	Process-level intended outcomes	Contribution to parent outcome	Contribution to Activity result
Interfaces	Principal business interfaces	Relevant hand-offs	Specific interaction where relevant
Dependencies	Material process dependencies	Activity dependencies	Task dependencies

A child input or output MUST NOT automatically be copied from the parent.

Where a child uses a parent-level input, the relationship must be made explicit and the child’s actual use described.

13. Documentation and Generator Requirements

The README generator MUST:

* Render input and output definitions consistently.
* Distinguish canonical references from free-text sources.
* Display consumers and sources when available.
* Distinguish outputs from outcomes.
* Render interface and dependency information only when applicable.
* Display evidence or provenance according to the approved profile.
* Avoid rendering unknown values as factual content.
* Preserve stable ordering for repeatable structures.

The validator SHOULD detect:

* Duplicate local IDs.
* Missing required descriptions.
* Unresolved canonical references.
* Invalid input/output classifications.
* Outputs without meaningful descriptions.
* Consumers that do not resolve where canonical resolution is required.
* Inconsistent parent-child assertions.
* Unsupported relationship types.

14. Repository Changes

Expected artefacts:

* docs/operational-input-output-interface-model.md
* Schema definitions or shared structures approved under EXT-10.
* Updated L2, L3 and L4 templates where required.
* Updated documentation profiles where required.
* Generator rendering updates.
* Input/output and reference validation tests.
* Representative examples.
* Updated decomposition template guide.

15. Testing Requirements

Tests MUST cover:

1. Input and output identifiers.
2. Source and consumer references.
3. Input/output classification.
4. Acceptance criteria.
5. Trigger and precondition distinction.
6. Output/outcome distinction.
7. Business and system interface distinction.
8. Dependency versus decomposition relationship.
9. L2-L4 applicability.
10. Invalid and unresolved references.
11. README rendering.
12. Existing records without new optional properties.
13. Deterministic output generation.

16. Acceptance Criteria

* AC-01: Input, transformation, output, and outcome semantics are implemented consistently.
* AC-02: Trigger and precondition semantics are represented distinctly.
* AC-03: Input source and output consumer traceability are supported.
* AC-04: Input and output acceptance requirements are supported where applicable.
* AC-05: Business interfaces are distinguished from system interfaces.
* AC-06: Dependencies are distinguished from decomposition relationships.
* AC-07: L2, L3 and L4 applicability is implemented.
* AC-08: Existing inputs, transformation, and outputs fields are reconciled rather than duplicated.
* AC-09: Canonical references are validated.
* AC-10: Generator output is deterministic.
* AC-11: Existing entity records remain backward compatible.
* AC-12: No workflow orchestration semantics are introduced.

17. Dependencies and Completion

EXT-12 depends on EXT-10 and EXT-11.

It is complete when the catalogue has a validated, profile-aware representation of operational inputs, transformations, outputs, outcomes, interfaces, and dependencies, with traceable sources and consumers.

CR-BP-94-EXT-13: Process Responsibility and Accountability Model

CR-BP-94-EXT-13: Process Responsibility and Accountability Model

Status: Proposed
Programme: CR-BP-94 Documentation Extension
Parent: CR-BP-94
Predecessors: EXT-08, EXT-09, EXT-10, EXT-11
Target repository: technehub-labs/dea-catalog-business-processes
Proposed path: change-requests/CR-BP-94-EXT-13-process-responsibility-and-accountability-model.md

1. Executive Summary

This CR establishes a consistent model for documenting the human, organizational, and automated responsibility arrangements associated with Business Processes, Activities, and Tasks.

It formalizes the distinction between:

* Role.
* Actor.
* Performer.
* Responsibility.
* Accountability.
* Organizational Unit.
* Business Function.
* Business Capability.
* Process ownership.
* Decision authority.

The existing Business Process responsibility property is retained as the starting point. Its meaning must not be silently changed or replaced.

The objective is to make it possible to understand who performs work, who is responsible for ensuring that it is performed, who is answerable for the result, and who has authority to make relevant decisions.

This model must support human and AI-agent participation without conflating software agents with organizational roles or legal accountability.

2. Problem Statement

Operational documentation often uses “owner”, “responsible”, “accountable”, “role”, and “performer” interchangeably.

This creates ambiguity in process ownership, governance, operational design, control assignment, and automation assessment.

For example:

* The Business Function that owns a business responsibility may not perform every Activity.
* The person performing a Task may not be accountable for the process outcome.
* A process owner may govern the process but not execute it.
* An AI agent may perform an authorized task without holding organizational accountability.
* A Business Capability may be realized by several processes without being the responsible actor.

The catalogue needs a consistent representation of these distinctions.

3. Objectives

This CR SHALL:

1. Define responsibility and accountability semantics.
2. Establish the relationship between roles and actors.
3. Distinguish process ownership from task performance.
4. Support multiple performers and responsibility assignments.
5. Support human, organizational, and software-agent participation.
6. Establish assignment scope at L2-L4.
7. Provide traceability to Business Functions and other canonical enterprise concepts.
8. Prevent duplicate organizational models within the Process catalogue.
9. Provide a basis for future RACI or equivalent responsibility views without requiring RACI as the canonical data model.

4. Normative Definitions

4.1 Actor

An Actor is an individual, group, organization, external party, or governed software agent capable of participating in or performing an action.

An Actor answers: Who or what participates?

4.2 Role

A Role is a responsibility-bearing part performed by an Actor in relation to a unit of work.

A Role answers: What part does the participant perform?

A role may be assigned to different actors in different organizational contexts.

4.3 Performer

A Performer is the Actor that actually performs a defined unit of work.

A Performer answers: Who or what carries out the work?

4.4 Responsibility

Responsibility is the obligation or assignment to ensure that specified work is performed.

It answers: Who is charged with ensuring that the work is performed?

4.5 Accountability

Accountability is the obligation to answer for a result, decision, obligation, or compliance condition.

It answers: Who is answerable?

Accountability MUST be assigned to an appropriately authorized human or organizational authority under the enterprise governance model. A software agent MUST NOT be represented as the legally or organizationally accountable authority merely because it performs work.

4.6 Process Owner

A Process Owner is the designated governance authority responsible for the ongoing definition, fitness, performance oversight, and improvement of a Business Process.

Process ownership is not equivalent to performing every Activity or Task within the process.

4.7 Decision Authority

Decision Authority is the role or authority empowered to make or approve a specified business decision.

Decision authority MUST be distinguished from the performer who prepares or executes the decision.

5. Relationship to Existing Enterprise Concepts

Concept	Relationship to this model
Business Function	May provide an organizational responsibility context
Business Capability	Describes enterprise ability, not an actor assignment
Business Process	Defines the work to which responsibility assignments relate
Organizational Unit	May be assigned a role or accountability
Actor	Participates in the work
Role	Defines the participant’s part
Information System	May support or mediate work
Information Systems Function	Defines system-level functional responsibility
AI Agent	May act as a governed performer
Process Owner	Holds process governance responsibility

The Process catalogue MUST reference existing canonical enterprise concepts where available instead of recreating them as process-specific entities.

6. Assignment Model

The implementation SHOULD support a responsibility assignment with the following conceptual attributes:

Attribute	Purpose
Assignment ID	Stable identifier
Role	Responsibility-bearing role
Actor or actor reference	Assigned participant, where known
Work scope	L2, L3, L4 or defined operational scope
Assignment type	Performer, responsible, accountable, consulted, informed, owner, or decision authority
Authority	Basis for the assignment
Validity	Applicable period or status, where governed
Source	Evidence supporting the assignment
Approval state	Whether the assignment has been validated

The final property names and cardinalities MUST be established under EXT-10 schema conventions.

The implementation MUST NOT assume that a single role or actor is sufficient for every process.

7. Responsibility Assignment Types

The following assignment types SHOULD be considered:

* process_owner
* responsible
* accountable
* performer
* decision_authority
* consulted
* informed

These are proposed classifications.

The implementation MUST decide whether the catalogue uses a RACI-compatible model, a more expressive assignment model, or references an existing enterprise responsibility model.

RACI is a possible reporting view, not an automatic canonical schema requirement.

7.1 Multiple assignments

A process may have multiple performers and responsible parties for different scopes.

However, the catalogue MUST make accountability unambiguous for each governed decision or accountability scope.

If an enterprise arrangement legitimately has shared accountability, it must be explicitly documented rather than inferred from multiple assignments.

7.2 Scope inheritance

A parent responsibility assignment MUST NOT automatically be treated as an assignment to every child Activity and Task.

Inheritance requires:

* Explicit source assignment.
* Defined scope.
* Applicability to the child.
* No conflicting local assignment.
* Traceability.

A child may have additional performers or delegated responsibility without changing the parent process owner.

8. L2-L4 Assignment Requirements

L2 Business Process

The L2 profile SHOULD identify:

* Process Owner.
* Principal responsible role or authority.
* Accountability for significant process outcomes.
* Principal decision authorities.
* Material external or cross-functional participants.

L3 Activity

The L3 profile SHOULD identify:

* Roles involved in the Activity.
* Responsible party for the Activity.
* Performers where known and meaningful.
* Relevant decision authority.
* Any delegated or inherited assignments.

L4 Task

The L4 profile SHOULD identify:

* Performer or performer role where established.
* Relevant authorization.
* Verification responsibility where distinct.
* Escalation authority where applicable.

The catalogue MUST NOT invent individual names or organizational assignments to satisfy profile requirements.

9. Human and AI-Agent Participation

Where software agents participate in process work, the documentation MUST distinguish:

1. Agent identity or reference.
2. Agent role in the work.
3. Permitted actions.
4. Human or organizational authority responsible for oversight.
5. Decision boundaries.
6. Escalation conditions.
7. Evidence and audit requirements.

An AI agent may be a performer or participant where the enterprise model permits it.

An AI agent MUST NOT automatically be designated as Process Owner, accountable authority, or legal decision-maker.

Where an agent performs work on behalf of a human or organizational role, the delegation and oversight arrangement SHOULD be documented.

10. Authorization and Control Alignment

Responsibility assignments MUST be traceable to relevant authorization and control requirements where those exist.

The model SHOULD support relationships between:

* Role and permitted activity.
* Actor and assigned role.
* Decision authority and decision type.
* Control owner and control.
* Process owner and process.
* Performer and task.
* Accountable authority and outcome.

EXT-13 does not define the control model itself; EXT-14 governs rules and controls.

11. Documentation and Rendering

The README generator SHOULD render responsibility information in a consistent table or structured section.

The rendered information SHOULD distinguish:

* Process ownership.
* Responsible roles.
* Accountable authority.
* Performers.
* Decision authority.
* Consulted and informed participants, where useful.

The generator MUST NOT render an unverified assignment as an approved organizational fact.

The documentation MUST identify inherited assignments and their source.

12. Validation Requirements

Validation SHOULD detect:

* Assignment without a role or defined assignment type.
* Invalid canonical actor references.
* Unresolved organizational references.
* Duplicate assignment identifiers.
* Conflicting accountability assignments.
* Unjustified inheritance.
* AI agents assigned human-only accountability.
* Child assignments inconsistent with parent scope.
* Decision authority without a defined decision scope where one is required.

Validation MUST distinguish missing information from a genuine contradiction.

13. Repository Changes

Expected artefacts:

* docs/process-responsibility-and-accountability-model.md
* Updated operational schema definitions, subject to EXT-10.
* Updated L2-L4 profiles, subject to EXT-11.
* Responsibility assignment examples.
* README rendering updates.
* Validation fixtures and tests.
* Updated decomposition template guide.

Any new role or actor entity type must be justified against the canonical OpenDEA metamodel and other catalogue ownership boundaries.

14. Testing Requirements

Tests MUST cover:

1. Multiple performers.
2. Distinct responsible and accountable parties.
3. Process Owner versus performer.
4. Decision authority versus execution.
5. Inherited assignments.
6. Child-level overrides and additions.
7. Organizational references.
8. AI-agent performer representation.
9. Human accountability for agent-performed work.
10. Invalid and conflicting assignments.
11. README rendering.
12. Backward compatibility with existing responsibility values.

15. Acceptance Criteria

* AC-01: Actor, role, performer, responsibility, accountability, Process Owner, and decision authority are distinct.
* AC-02: Existing responsibility semantics are preserved or migrated through an explicit decision.
* AC-03: Multiple assignments can be represented where justified.
* AC-04: Accountability is unambiguous within each governed scope.
* AC-05: L2-L4 assignment expectations are defined.
* AC-06: Inherited assignments identify their source and applicability.
* AC-07: Business Functions and Business Capabilities are not misrepresented as roles or actors.
* AC-08: AI agents may be represented as performers where governed.
* AC-09: AI agents are not automatically treated as accountable human or organizational authorities.
* AC-10: Responsibility assignments are traceable and validated.
* AC-11: README rendering distinguishes assignment types.
* AC-12: Existing catalogue records remain backward compatible.

16. Dependencies and Completion

EXT-13 depends on EXT-10 and EXT-11 and must align with EXT-14 control ownership requirements.

It is complete when the catalogue supports consistent, traceable, level-appropriate responsibility and accountability documentation without duplicating the enterprise organizational model.

CR-BP-94-EXT-14: Business Rules, Controls and Exception Semantics

CR-BP-94-EXT-14: Business Rules, Controls and Exception Semantics

Status: Proposed
Programme: CR-BP-94 Documentation Extension
Parent: CR-BP-94
Predecessors: EXT-08, EXT-09, EXT-10, EXT-11
Related CR: EXT-13 (Process Responsibility and Accountability Model)
Target repository: technehub-labs/dea-catalog-business-processes
Proposed path: change-requests/CR-BP-94-EXT-14-business-rules-controls-and-exception-semantics.md

1. Executive Summary

This CR establishes a structured and governed approach to documenting the business rules, controls, exceptions, and deviations that constrain or govern Business Processes, Activities, and Tasks.

It ensures the catalogue can explain:

* Which rules govern operational behaviour.
* Which controls manage relevant risks and obligations.
* Who owns or performs those controls.
* What evidence demonstrates control design or operation.
* What happens when normal conditions cannot be met.
* How deviations are identified, authorized, escalated, and resolved.

The CR explicitly distinguishes a business rule from a control and both from evidence of control operation.

It does not create a new risk-management, compliance, audit, or workflow platform. It defines the process catalogue’s representation and traceability requirements and requires references to authoritative external governance models where those exist.

2. Problem Statement

The current documentation approach identifies “Business Rules and Controls” as a combined operational documentation concern.

Although convenient as a README section, the two concepts are not equivalent.

A rule establishes what is required or permitted. A control establishes a mechanism for managing a risk, obligation, or failure condition.

Evidence demonstrates whether a control has been designed or operated.

An exception describes an authorized or recognized departure from normal conditions. A deviation describes an observed departure.

Without these distinctions, the catalogue may:

* Treat every policy as a control.
* Treat every validation step as a control without identifying its objective.
* Claim control effectiveness without evidence.
* Assign control ownership to an inappropriate role.
* Confuse a permitted exception with a control failure.
* Duplicate the enterprise risk and compliance models.

3. Objectives

This CR SHALL:

1. Establish a structured distinction between business rules and controls.
2. Define how rules relate to processes and their decomposition.
3. Define control objectives, activities, ownership, and evidence.
4. Distinguish control design evidence from operating evidence.
5. Define exception and deviation documentation.
6. Support control assignment and accountability traceability.
7. Support references to authoritative risk, policy, regulatory, and audit sources.
8. Establish validation and evidence requirements.
9. Avoid duplicating risk, compliance, audit, or policy catalogues.
10. Enable meaningful operational documentation and future assurance analysis.

4. Scope

Included

* Business rule representation.
* Control representation.
* Control objectives and risk/obligation references.
* Control ownership and performer references.
* Control evidence.
* Exception and deviation semantics.
* Process-level applicability.
* Rule and control references across L2-L4.
* README rendering and validation.

Excluded

* Defining enterprise risk taxonomies.
* Creating a complete regulatory obligation catalogue.
* Replacing policy management.
* Replacing internal audit systems.
* Defining a control testing platform.
* Defining workflow execution and exception routing.
* Defining the enterprise risk appetite or control effectiveness methodology.

5. Business Rule Model

A Business Rule is an authoritative constraint, condition, decision criterion, or policy governing business behaviour.

A rule SHOULD support:

Attribute	Purpose
Rule ID	Stable identifier or canonical reference
Name	Human-readable title
Statement	Clear normative rule
Rationale	Why the rule exists
Scope	Entity or activity to which it applies
Authority source	Policy, regulation, contract, or approved authority
Applicability	Conditions under which it applies
Effective status	Current, pending, superseded, or other governed state
Owner	Authority responsible for the rule, where known
Evidence	Source supporting the assertion

The schema MUST determine whether rules are independently governed entities or process-scoped assertions.

Where an enterprise rule catalogue exists, the process catalogue SHOULD reference the canonical rule rather than copy its full definition.

5.1 Rule categories

The implementation SHOULD consider categories such as:

* Policy rule.
* Regulatory rule.
* Contractual rule.
* Eligibility rule.
* Decision rule.
* Validation rule.
* Calculation rule.
* Authorization rule.
* Operational constraint.

The final controlled vocabulary MUST be governed and extensible.

5.2 Rule expression

A rule statement SHOULD be unambiguous and testable where possible.

Statements such as “ensure compliance” or “follow company policy” are insufficient without a specific authority or defined requirement.

The catalogue SHOULD identify the authoritative source rather than paraphrase a rule in a way that changes its meaning.

6. Control Model

A Control is a mechanism designed to prevent, detect, correct, or otherwise manage a specified risk, error, or non-compliance condition.

A control SHOULD support:

Attribute	Purpose
Control ID	Stable identifier or canonical reference
Name	Human-readable title
Objective	What the control is intended to achieve
Risk or obligation	What condition it manages
Mechanism	How the control operates
Control type	Preventive, detective, corrective, or other approved type
Scope	Process, Activity, Task, or other governed scope
Owner	Accountable control owner
Performer	Party carrying out the control, where distinct
Frequency	When or how often it operates, where applicable
Evidence	What demonstrates design or operation
Failure response	Escalation or remediation arrangement
Authority	Source establishing the control

The schema MUST reconcile this model with existing enterprise control and risk structures before adding new entity types.

6.1 Control categories

The initial model SHOULD support:

* Preventive.
* Detective.
* Corrective.

Additional categories such as directive or compensating may be adopted if they are already used by the enterprise governance model.

6.2 Rule-to-control relationship

A rule may be supported by multiple controls.

A control may support multiple rules or obligations.

A control may address a risk that is not directly represented as a business rule.

Therefore, rule-to-control relationships MUST support many-to-many traceability where the canonical model permits it.

The catalogue MUST NOT infer that a control exists simply because a rule exists.

7. Control Evidence

Evidence MUST distinguish control design from control operation.

7.1 Design evidence

Design evidence demonstrates that the control has been defined and established.

Examples:

* Approved control description.
* Policy or procedure.
* Delegation of authority.
* System configuration specification.
* Approved control matrix.

7.2 Operating evidence

Operating evidence demonstrates that the control operated for a relevant instance or period.

Examples:

* Completed review record.
* Approval log.
* Reconciliation report.
* Exception register.
* Control test result.
* Audit trail.

7.3 Evidence attributes

Evidence references SHOULD identify:

* Evidence identifier or URI.
* Evidence type.
* Source or repository.
* Related control.
* Evidence period or instance, where relevant.
* Owner or custodian.
* Review status.
* Retention or access constraints where governed.

The Process catalogue SHOULD reference evidence rather than duplicate sensitive operational records.

No sensitive customer, employee, financial, or regulated evidence payload should be copied into a public catalogue repository.

8. Exceptions and Deviations

8.1 Exception

An exception is a recognized condition in which normal requirements or operating conditions cannot be met or are intentionally varied.

An exception definition SHOULD identify:

* Exception type.
* Triggering condition.
* Applicable scope.
* Permitted or prohibited disposition.
* Authorization requirement.
* Responsible authority.
* Required evidence.
* Resolution or closure criteria.

8.2 Deviation

A deviation is an observed departure from an approved rule, control, process condition, or expected operating requirement.

A deviation record SHOULD identify:

* Requirement or control affected.
* Observed departure.
* Detection source.
* Impact or risk assessment reference.
* Responsible authority.
* Corrective action or disposition.
* Closure evidence.

8.3 Exception versus deviation

Dimension	Exception	Deviation
Nature	Recognized variation or special condition	Observed departure
Timing	May be authorized in advance	Often identified during or after occurrence
Authorization	May be explicitly permitted	Requires assessment and disposition
Evidence	Approval or exception basis	Detection and resolution evidence
Relationship to control	May be governed by a control	May indicate control failure or process non-conformance

A permitted exception MUST NOT automatically be classified as a control failure.

A deviation MUST NOT be converted into an authorized exception retrospectively without the appropriate governance decision.

9. Relationship to Responsibility and Accountability

EXT-13 governs role and accountability semantics.

EXT-14 MUST use those definitions and MUST NOT create a separate competing role model.

A control SHOULD identify:

* Control Owner.
* Control Performer, where distinct.
* Accountable authority.
* Escalation authority, where applicable.

A Business Process Owner is not automatically the owner of every control associated with that process.

Likewise, a Task performer is not automatically accountable for the design or effectiveness of a control.

10. L2-L4 Application

L2 Business Process

The L2 profile SHOULD identify material rules and controls governing the process, including their principal scope and accountable ownership.

L3 Activity

The L3 profile SHOULD identify rules and controls that materially constrain or govern the Activity.

Parent-level rules may apply, but applicability must be explicit.

L4 Task

The L4 profile SHOULD identify task-specific authorization, validation, verification, or control requirements where material.

It MUST NOT become a runtime control-execution record or audit log.

L0 and L1

L0 and L1 may reference scope-level or group-level governance obligations where appropriate. They MUST NOT be required to enumerate the operational controls of every descendant process.

11. Cross-Catalogue Traceability

The implementation MUST determine how to reference:

* Policies.
* Regulatory obligations.
* Risks.
* Controls.
* Audit findings.
* Business Functions.
* Roles and accountability.
* Information Systems.
* Information Systems Functions.
* Metrics and control indicators.

Where canonical catalogues exist, references SHOULD use canonical IDs and approved relationship types.

This CR MUST NOT establish new cross-catalogue relationship types without metamodel authority.

12. Documentation and Generator Requirements

The README generator SHOULD render:

* Relevant business rules.
* Relevant controls.
* Control objectives.
* Accountable owner or role.
* Evidence references.
* Exception and deviation handling summaries.

It MUST distinguish:

* Rule from control.
* Control design from operating evidence.
* Authorized exception from deviation.
* Approved content from pending or assumed content.

The README MUST NOT expose confidential evidence or sensitive operational records.

13. Validation Requirements

Validation SHOULD detect:

* Rule without an authoritative source where one is required.
* Control without an objective.
* Control without a defined risk or obligation where applicable.
* Missing ownership or accountability where required by profile.
* Control evidence with no traceable control.
* Unsupported control classifications.
* Duplicate identifiers.
* Unresolved canonical references.
* Exception without an applicable authorization disposition.
* Deviation without a disposition or review state.
* Inconsistent rule or control applicability across parent and child entities.

The validator MUST distinguish structural defects from missing business evidence.

14. Repository Changes

Expected artefacts:

* docs/business-rules-controls-and-exceptions-model.md
* Schema extensions approved under EXT-10.
* L2-L4 profile updates under EXT-11.
* Rule, control, exception, and deviation examples.
* Generator rendering changes.
* Validation rules and fixtures.
* Updated documentation guide.
* CR register entry.

The implementation MUST follow the existing repository structure and avoid creating a parallel governance catalogue.

15. Testing Requirements

Tests MUST cover:

1. Business rule structure and source references.
2. Control objective and mechanism.
3. Rule-to-control many-to-many relationships where supported.
4. Control ownership and performer distinction.
5. Design versus operating evidence.
6. Exception versus deviation.
7. L2-L4 applicability.
8. Parent-child rule and control applicability.
9. Sensitive evidence exclusion.
10. Invalid and unresolved references.
11. README rendering.
12. Existing entity compatibility.

16. Acceptance Criteria

* AC-01: Business Rules and Controls are distinct semantic concepts.
* AC-02: Rules can be traced to authoritative sources.
* AC-03: Controls identify their objectives and relevant risks or obligations.
* AC-04: Control ownership, performance, and accountability are distinguishable.
* AC-05: Design evidence and operating evidence are distinct.
* AC-06: Exceptions and deviations have separate definitions and dispositions.
* AC-07: L2-L4 applicability is documented.
* AC-08: Parent-level rules and controls are not blindly copied into child entities.
* AC-09: Canonical cross-catalogue references are supported where available.
* AC-10: Sensitive evidence is not duplicated in the public catalogue.
* AC-11: README rendering preserves semantic distinctions.
* AC-12: Validation identifies structural and traceability defects.
* AC-13: Existing entity records remain backward compatible.
* AC-14: The model is ready for evidence and provenance formalization under EXT-15.

17. Dependencies and Completion

EXT-14 depends on EXT-10 and EXT-11 and must align with EXT-13 responsibility assignments.

It is complete when the Process catalogue can document rules, controls, exceptions, deviations, ownership, and evidence references consistently and without duplicating enterprise governance systems.

Consolidated dependency and implementation order

The five CRs should be implemented in this order:

* EXT-10: Schema alignment
    Inventory the current schema, templates, fields and metamodel relationships. Approve the canonical representation before adding new structures.
    Foundation
* EXT-11: Documentation profiles
    Define exactly what L0, L1, L2, L3 and L4 must document. Implement profile-aware generation and validation.
    Foundation
* EXT-12: Inputs, outputs and interfaces
    Establish the operational transformation and interaction model, including source, consumer and dependency traceability.
* EXT-13: Responsibility and accountability
    Establish who performs, owns, is responsible for, and is accountable for the work.
* EXT-14: Rules, controls and exceptions
    Establish the governance constraints, control mechanisms, exception handling and evidence references.

Dependency map

flowchart TD
    A["EXT-08<br/>Roadmap Reconciliation"] --> B["EXT-09<br/>Semantic Contract"]
    B --> C["EXT-10<br/>Schema Alignment"]
    C --> D["EXT-11<br/>L0-L4 Documentation Profiles"]
    D --> E["EXT-12<br/>Inputs, Outputs & Interfaces"]
    D --> F["EXT-13<br/>Responsibility & Accountability"]
    D --> G["EXT-14<br/>Rules, Controls & Exceptions"]
    C --> E
    C --> F
    C --> G
    F --> G
    E --> H["EXT-15<br/>Evidence, Provenance & Confidence"]
    F --> H
    G --> H

Important implementation gates

Gate	Required outcome
G1: Schema	Existing fields reconciled; no duplicate operational structures
G2: Profiles	Five level-specific profiles validated
G3: Operational interfaces	Inputs, outputs, transformations and dependencies traceable
G4: Accountability	Roles and assignments unambiguous within their scopes
G5: Governance	Rules, controls and exceptions traceable to authoritative sources

Do not begin bulk catalogue backfill after EXT-14 alone. EXT-15 must establish evidence, provenance and confidence handling, and EXT-16 must establish the research and authoring methodology. Otherwise, the catalogue risks accumulating plausible-looking but unverified operational assertions.

What these five CRs establish

At the end of EXT-14, the Business Process catalogue should have a coherent operational documentation architecture covering:

* Structure: where operational information belongs.
* Applicability: what each decomposition level needs to document.
* Transformation: what enters, what happens, and what is produced.
* Organization: who performs and who is accountable.
* Governance: what rules and controls constrain the work and how exceptions are treated.

The next logical CR is CR-BP-94-EXT-15: Evidence, Provenance and Confidence Framework. It will complete the semantic governance foundation before we define the research, authoring and backfill machinery in EXT-16 and EXT-17.