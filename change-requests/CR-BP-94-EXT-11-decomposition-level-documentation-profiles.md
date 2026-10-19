# CR-BP-94-EXT-11: Decomposition-Level Operational Documentation Profiles

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