# CR-BP-EXT-23: Operational Documentation Conformance Framework and Automated Quality Gates

**Source**: the user-submitted `CR-BP-EXT-23.md` (2026-10-20)
**Status**: supersedes the previously authored CR-BP-EXT-23 (the interim gate-posture CR)
**Programme**: Business Process Operational Documentation Extension (DEA-PROCESS-ENRICH-000)
**Repository**: technehub-labs/dea-catalog-business-processes

---

## 0. Preamble (verbatim from the submission)

EXT-23 is the transition from reconciled catalogue quality to enforceable catalogue governance.

EXT-22 establishes whether the L0-L4 hierarchy is structurally and semantically coherent. EXT-23 must now translate the approved requirements from EXT-08 through EXT-22 into a layered conformance framework: machine-enforced checks where rules are deterministic, evidence-based checks where assertions require substantiation, and human approval where business judgement is necessary.

A critical design principle is that passing automated validation must not be represented as proof that a process is operationally correct. EXT-23 must distinguish structural validity, schema compliance, semantic consistency, evidence sufficiency, documentation quality and governance approval.

---

CR-BP-EXT-23  -  Operational Documentation Conformance Framework and Automated Quality Gates

Attribute	Value
CR ID	CR-BP-EXT-23
Title	Operational Documentation Conformance Framework and Automated Quality Gates
Programme	Business Process Operational Documentation Extension
Status	Proposed
Priority	Critical
Change Type	Governance, validation architecture, CI/CD integration, quality assurance
Depends On	EXT-08 through EXT-22
Primary Dependencies	EXT-10, EXT-11, EXT-15, EXT-17, EXT-18, EXT-19, EXT-20, EXT-21 and EXT-22
Enables	EXT-24  -  Catalogue Closure and Continuous Governance
Scope	Business Process catalogue, L0-L4 entities, operational documentation, relationships, evidence, reconciliation and repository validation




1. Executive Summary

This Change Request establishes a formal conformance framework for the Business Process catalogue.

The preceding CRs establish the semantic model, documentation architecture, enrichment methodology, tooling and reconciliation requirements necessary to create a comprehensive operationally meaningful process catalogue.

However, the quality achieved through enrichment and reconciliation cannot be sustained without systematic validation and governance.

Without enforceable conformance controls, the catalogue is vulnerable to:

* Introduction of invalid entities.
* Incomplete or inconsistent operational documentation.
* Broken parent-child relationships.
* Unsupported business assertions.
* Incorrect decomposition.
* Invalid cross-catalogue references.
* Inconsistent application of decomposition-level requirements.
* Uncontrolled vocabulary and metadata drift.
* Documentation becoming inconsistent with canonical entity data.
* Reintroduction of previously corrected defects.
* Unapproved changes to process semantics.
* Inconsistent treatment of deferred or incomplete entities.

EXT-23 introduces a layered conformance framework that defines what must be validated, how validation is performed, what constitutes failure, how exceptions are governed and when changes may be accepted into the catalogue.

The framework shall integrate with the repository’s existing validation and CI mechanisms, extending them only where necessary.

It shall establish five complementary validation domains:

1. Structural conformance  -  whether the entity model, identifiers and relationships are structurally valid.
2. Semantic conformance  -  whether entity descriptions and relationships respect the approved process semantics.
3. Evidence conformance  -  whether material assertions have appropriate provenance, confidence and verification status.
4. Documentation conformance  -  whether documentation is complete, consistent and generated according to the approved documentation architecture.
5. Governance conformance  -  whether required reviews, approvals, dispositions and exceptions are properly recorded.

The resulting framework shall distinguish deterministic machine validation from semantic assessment and human approval.

The objective is not merely to make CI pass. It is to establish a sustainable quality assurance mechanism that protects the integrity, reliability and evolution of the Business Process catalogue.

2. Problem Statement

The operational documentation programme introduces multiple dimensions of quality.

An entity may be syntactically valid but semantically incorrect.

An entity may satisfy its documentation profile but contain unsupported claims.

An entity may have valid parent-child references while its children do not meaningfully contribute to the parent.

A README may be complete while the canonical YAML remains incomplete.

A reconciliation issue may have been identified but never formally resolved.

A change may pass technical checks without having received the required business review.

These conditions demonstrate that no single validation mechanism can establish full catalogue conformance.

EXT-23 must therefore define an explicit relationship between:

* Requirements.
* Canonical entity representations.
* Decomposition profiles.
* Controlled vocabularies.
* Relationships.
* Evidence and provenance.
* Documentation generation.
* Reconciliation records.
* Validation rules.
* Review and approval.
* Repository contribution controls.

It must also establish a consistent interpretation of conformance across L0-L4.

3. Objectives

EXT-23 shall:

1. Establish a formal operational documentation conformance model.
2. Translate approved CR requirements into testable validation rules.
3. Define validation categories, severity levels and outcomes.
4. Establish decomposition-level conformance profiles.
5. Automate deterministic structural and schema checks.
6. Introduce semantic consistency checks where deterministic validation is possible.
7. Identify assertions that require evidence or human verification.
8. Validate parent-child integrity using EXT-22 reconciliation requirements.
9. Validate canonical entity and generated README consistency.
10. Validate cross-catalogue references against approved metamodel relationships.
11. Establish controlled handling of incomplete, deferred and not-applicable information.
12. Introduce governed exception and waiver management.
13. Integrate conformance checks into existing repository CI processes.
14. Prevent invalid changes from being accepted without an approved disposition.
15. Establish repeatable validation reports and catalogue-level quality metrics.
16. Support controlled evolution of schemas, profiles and validation rules.
17. Provide a conformance baseline for the continuous governance activities under EXT-24.

4. Scope

4.1 In scope

The CR covers:

* L0-L4 entity validation.
* YAML and other canonical representation validation.
* Entity schemas.
* Decomposition-level profiles.
* Controlled vocabularies.
* Identifier and reference integrity.
* Parent-child structural relationships.
* Semantic validation rules.
* Evidence and provenance requirements.
* Documentation generation and validation.
* Reconciliation matrix validation.
* Cross-catalogue relationship integrity.
* Repository CI integration.
* Validation reporting.
* Review and approval controls.
* Exceptions and waivers.
* Validation rule versioning.
* Regression testing.
* Catalogue-wide conformance assessment.

4.2 Out of scope

EXT-23 does not:

* Redesign the Business Process metamodel.
* Introduce new decomposition levels.
* Replace EXT-10 through EXT-22.
* Guarantee that an operational process is effective merely because its documentation conforms.
* Automatically approve business semantics.
* Automatically verify that documented practice matches actual organisational practice.
* Introduce workflow execution or runtime orchestration.
* Replace organisational audit, risk or compliance assurance.
* Create new cross-catalogue relationship types without metamodel approval.
* Automatically delete or rewrite non-conforming entities.
* Introduce arbitrary minimum entity counts or mandatory field populations where the approved semantic profile does not require them.

5. Conformance Architecture

5.1 Conformance dimensions

The framework shall implement the following validation dimensions.

Dimension	What is validated	Primary validation mechanism
Structural	Entity identity, types, references, hierarchy and relationships	Automated
Schema	Data types, permitted structures, required properties and constraints	Automated
Profile	Level-specific documentation and semantic applicability requirements	Automated, with controlled exceptions
Semantic	Consistency of meaning, responsibility, boundaries and decomposition	Automated where deterministic; human review otherwise
Evidence	Provenance, confidence, verification, freshness and source suitability	Automated metadata checks plus human assessment
Documentation	README completeness, generation, consistency and presentation	Automated
Cross-catalogue	References and relationship validity across catalogues	Automated where source information is available
Reconciliation	Completion and disposition of EXT-22 requirements	Automated status checks plus human approval
Governance	Review, approval, exception and change-control requirements	Automated metadata checks plus human approval

These dimensions are independent.

A successful result in one dimension must not imply successful conformance in another.

5.2 Validation layers

The implementation shall organise checks into the following layers.

Layer 1  -  Repository integrity

Validates:

* Expected repository structure.
* File naming and placement conventions.
* Entity discovery.
* Required repository metadata.
* Duplicate files and identifiers.
* Unexpected or unsupported entity representations.

Layer 2  -  Syntax and schema

Validates:

* YAML or other canonical representation syntax.
* Schema conformity.
* Field data types.
* Permitted values.
* Required fields.
* Collection structures.
* Identifier formats.
* Unknown or unsupported properties, according to the approved schema policy.

Layer 3  -  Entity and profile conformance

Validates:

* Entity type.
* Decomposition level.
* Applicable documentation profile.
* Required and conditional information.
* Field applicability.
* Completeness classification.
* Level-specific constraints.

Layer 4  -  Relationship and hierarchy integrity

Validates:

* Parent-child references.
* Permitted relationship types.
* Canonical identifiers.
* Broken references.
* Orphaned entities.
* Duplicate relationships.
* Hierarchy consistency.
* Cross-catalogue references.

Layer 5  -  Semantic conformance

Validates, where possible:

* Distinction between inputs, resources, outputs and outcomes.
* Transformation semantics.
* Functional contribution.
* Responsibility and accountability.
* Boundary consistency.
* Rules, controls and exceptions.
* Decomposition appropriateness.
* Prohibited workflow semantics.

Layer 6  -  Evidence and provenance

Validates:

* Evidence metadata.
* Source classification.
* Confidence classification.
* Verification status.
* Required evidence references.
* Unresolved conflicts.
* Stale evidence.
* AI-assisted research disclosure and review status.

Layer 7  -  Documentation conformance

Validates:

* README presence.
* README generation.
* Canonical source consistency.
* Required documentation sections.
* Links and references.
* Correct level-specific presentation.
* Absence of unresolved generation placeholders.

Layer 8  -  Governance and approval

Validates:

* Required review status.
* Approval evidence.
* Reconciliation disposition.
* Approved exceptions.
* Deferred work.
* Change traceability.
* Required programme gates.

6. Conformance Requirements

REQ-23-01  -  Formal conformance rule catalogue

The implementation shall establish a controlled catalogue of conformance rules.

Every rule shall have:

* Unique rule identifier.
* Rule name.
* Description.
* Requirement or ADR traceability.
* Applicable entity types.
* Applicable decomposition levels.
* Validation dimension.
* Validation method.
* Severity.
* Rule version.
* Expected result.
* Remediation guidance.
* Exception eligibility.
* Test coverage.
* Rule lifecycle status.

The rule catalogue shall be version-controlled.

Rules must not exist solely as undocumented conditions inside scripts.

REQ-23-02  -  Requirement-to-rule traceability

Every enforceable requirement from EXT-08 through EXT-22 shall be mapped to one or more conformance rules or explicitly classified as non-automatable.

The mapping must identify:

* Source CR.
* Requirement identifier.
* Conformance rule identifier.
* Validation dimension.
* Enforcement mechanism.
* Applicable levels.
* Test evidence.
* Responsible owner.

A requirement without an implemented rule must have an explicit status:

* automated
* human_review
* evidence_assessment
* deferred
* not_enforceable
* not_applicable

The programme must be able to demonstrate which requirements are enforced and which remain dependent on governance or human review.

REQ-23-03  -  Structural conformance

The framework shall validate structural integrity for all in-scope entities.

Checks shall include:

* Entity existence.
* Identifier uniqueness.
* Entity type validity.
* Decomposition level validity.
* Canonical file location.
* Parent-child relationship validity.
* Broken references.
* Invalid relationship types.
* Circular references where relevant.
* Duplicate relationships.
* Required entity metadata.
* Repository consistency.

Structural rules must be deterministic wherever possible.

REQ-23-04  -  Schema conformance

The framework shall validate canonical entity representations against the approved schema.

It shall check:

* Valid syntax.
* Correct field types.
* Required properties.
* Permitted properties.
* Allowed enumerations.
* Correct nested structures.
* Identifier formats.
* Reference formats.
* Deprecated fields.
* Unsupported properties.
* Schema version compatibility.

Schema validation must use the authoritative schemas approved under EXT-10.

The framework must not independently redefine entity semantics through validation scripts.

REQ-23-05  -  Decomposition profile conformance

The framework shall validate entities against the appropriate L0-L4 profile established under EXT-11.

It shall distinguish:

* required
* conditional
* optional
* not_applicable
* inherited

Validation must respect the profile applicable to the entity type and decomposition level.

The framework must not require every operational property to be populated at every level.

For example:

* An L1 Process Group must not be treated as an executable Business Process.
* An L3 Activity must not automatically be required to have all the operational attributes of an L2 Business Process.
* An L4 Task must not be required to define workflow orchestration or execution sequence.

REQ-23-06  -  Explicit completeness and information-state validation

The framework shall distinguish the state of information from its value.

Where supported by the approved schema, the framework shall recognise:

* Known and documented.
* Unknown.
* Not assessed.
* Not applicable.
* Inherited.
* Deferred.
* Awaiting evidence.
* Awaiting owner review.
* Conflicting.
* Confirmed absent.

An empty value must not automatically be interpreted as any of these states.

The framework must flag ambiguous empty or missing information where the applicable profile requires explicit disposition.

REQ-23-07  -  Controlled vocabulary conformance

The framework shall validate controlled values against approved vocabularies.

This includes, where defined:

* Entity types.
* Decomposition levels.
* Entity status.
* Disposition.
* Evidence source classifications.
* Confidence classifications.
* Verification status.
* Responsibility assignment types.
* Exception classifications.
* Validation outcomes.
* Relationship types.

The validation system must use the authoritative vocabulary definitions.

New values must not be introduced informally through individual entity files.

REQ-23-08  -  Identifier and reference integrity

The framework shall validate canonical identifiers and references.

It must identify:

* Missing referenced entities.
* Invalid identifiers.
* Duplicate identifiers.
* References to unsupported entity types.
* Invalid relationship direction or cardinality where defined.
* Stale references.
* References to deprecated or superseded entities.
* Cross-catalogue references that cannot be resolved.

Where the referenced catalogue is unavailable, the framework must distinguish an unverified external reference from a confirmed invalid reference.

REQ-23-09  -  Parent-child hierarchy conformance

The framework shall validate the hierarchy established under the decomposition model.

Permitted parent-child relationships shall be governed by the approved model:

Parent	Permitted child
L0 Process Scope	L1 Process Group
L1 Process Group	L2 Business Process
L2 Business Process	L3 Activity
L3 Activity	L4 Task

The framework shall detect:

* Invalid parent-child level combinations.
* Missing parent references.
* Multiple conflicting immediate parents where prohibited by the model.
* Invalid child membership.
* Orphaned entities.
* Broken hierarchy paths.
* Duplicate hierarchy relationships.

Cross-cutting associations must be represented separately from decomposition parentage where the metamodel permits them.

REQ-23-10  -  Semantic consistency conformance

The framework shall validate semantic distinctions established by EXT-09 through EXT-14.

At minimum, the rules shall protect the distinction between:

* Inputs and resources.
* Outputs and outcomes.
* Transformation and workflow.
* Trigger and precondition.
* Interface and dependency.
* Responsibility and accountability.
* Performer and owner.
* Business rule and control.
* Control and evidence.
* Exception and deviation.
* Business Process and Activity.
* Activity and Task.
* Functional decomposition and execution sequencing.

Where semantic correctness cannot be established deterministically, the framework shall produce a review requirement rather than a false automated pass.

REQ-23-11  -  Functional decomposition conformance

The framework shall implement the structural and review controls arising from EXT-20, EXT-21 and EXT-22.

It shall assess or require recorded assessments for:

* Activity contribution to its parent Business Process.
* Task contribution to its parent Activity.
* Parent coverage by children.
* Child-to-parent functional relevance.
* Decomposition readiness.
* Missing decomposition coverage.
* Duplicate or overlapping responsibilities.
* Inappropriate granularity.
* Unresolved boundary conflicts.

Automated checks may detect missing assessments and inconsistencies in recorded relationships.

They must not automatically conclude that a Business Process or Activity is functionally complete based solely on child counts, naming similarity or the existence of documentation.

REQ-23-12  -  Prohibited workflow semantics

The framework shall protect the process catalogue against the unintended introduction of workflow-engine concepts into the L0-L4 decomposition.

The validation system shall identify inappropriate use of:

* Mandatory sequence numbers.
* Workflow step ordering.
* Branching definitions.
* Runtime state transitions.
* Retry definitions.
* Queue and scheduling semantics.
* Workflow execution identifiers.
* Runtime instance identifiers.
* Orchestration configuration.
* Execution timestamps used as process model attributes.

The framework must distinguish legitimate business concepts from workflow implementation terminology.

A word such as “sequence” or “step” may be valid in explanatory prose or an external reference. Detection must therefore be contextual and must not automatically reject every occurrence of such terminology.

Where a prohibited construct is confirmed, the issue shall be reported with a clear remediation recommendation.

REQ-23-13  -  Evidence and provenance conformance

The framework shall validate evidence requirements established under EXT-15.

It shall check:

* Required evidence metadata.
* Source classification.
* Confidence classification.
* Verification status.
* Source reference integrity.
* Evidence attribution.
* Conflicting evidence status.
* Freshness metadata where required.
* AI-assisted research disclosure where applicable.
* Review requirements for inferred assertions.

The framework must distinguish confidence from verification status.

For example, a claim marked high confidence must not automatically be treated as verified.

Likewise, the existence of a source reference must not automatically establish that the source supports the associated assertion.

The latter requires substantive review.

REQ-23-14  -  Evidence sufficiency and approval

The framework shall identify assertions that require additional verification or approval.

It shall support review outcomes such as:

* not_reviewed
* under_review
* verified
* rejected
* superseded
* disputed

The validation framework must not allow an unreviewed assertion to be presented as verified merely because its metadata is populated.

Where owner confirmation or subject matter expert approval is required, the relevant approval record must be traceable.

REQ-23-15  -  README and documentation conformance

The framework shall validate generated documentation against the approved documentation architecture.

Checks shall include:

* README existence where required.
* Correct entity identification.
* Correct decomposition-level template.
* Required sections.
* Required content.
* Correct canonical references.
* Valid internal and external links.
* No broken generated references.
* No unresolved mandatory placeholders.
* Consistency with canonical entity data.
* Correct rendering and presentation conventions.

The framework shall identify whether documentation is:

* Generated and current.
* Generated but outdated.
* Manually maintained where generation is required.
* Missing.
* Inconsistent with the canonical entity representation.

README files must not be used to conceal missing canonical information.

REQ-23-16  -  Cross-catalogue conformance

The framework shall validate relationships to other catalogues and metamodel entities where relevant.

Potential referenced catalogues include:

* Business Capabilities.
* Business Functions.
* Information Systems.
* Information Systems Functions.
* Metrics.
* Policies.
* Risks.
* Controls.
* Organisational entities.
* Agent and automation entities.

Validation shall confirm:

* Referenced entity existence where accessible.
* Canonical identifier correctness.
* Approved relationship type.
* Appropriate entity type.
* Valid relationship direction.
* No unsupported local relationship vocabulary.
* No conflicting or duplicated references.

If the external catalogue cannot be accessed during CI, the framework must report the reference as externally unverified rather than silently treating it as valid.

REQ-23-17  -  EXT-22 reconciliation conformance

The framework shall validate the existence and integrity of the reconciliation artefacts established under EXT-22.

It shall check:

* Entity reconciliation coverage.
* Reconciliation record identity.
* Parent-child references.
* Disposition values.
* Issue ownership.
* Evidence references.
* Review status.
* Approved deferrals.
* Unresolved structural issues.
* Unresolved semantic issues.
* Reconciliation matrix freshness.

An entity that has not undergone required reconciliation must not be represented as reconciled.

REQ-23-18  -  Governance conformance

The framework shall validate governance requirements associated with entity changes.

It shall check, where applicable:

* Required review.
* Approval status.
* Reviewer identity or approved reference.
* Change rationale.
* Evidence of material decisions.
* Exception approval.
* Deferral approval.
* Deprecation and supersession records.
* Traceability to an approved CR or other change authority.

The framework must not infer approval from the presence of a commit or successful CI execution.

REQ-23-19  -  Conformance severity model

The implementation shall define a controlled severity model.

Severity	Meaning	Default handling
error	A mandatory conformance requirement has failed.	Blocks acceptance unless an explicitly permitted exception applies.
warning	A quality concern or potential inconsistency requires review.	Requires disposition according to the applicable policy.
info	Advisory observation or improvement opportunity.	Recorded; does not block acceptance.
deferred	A requirement or assessment is formally deferred.	Requires approved disposition and accountable ownership.

The framework shall not use severity inconsistently across validation scripts.

Severity must be determined by the rule definition and its impact.

REQ-23-20  -  Conformance outcomes

Every validation run shall produce an explicit result.

The framework shall support:

* passed
* passed_with_warnings
* failed
* blocked
* not_assessed
* passed_with_approved_exceptions

The result must include the scope of the validation and the rules executed.

A partial validation must never be represented as a full conformance pass.

REQ-23-21  -  Exception and waiver management

The framework shall provide controlled exception management.

An exception record shall include, where supported by the approved governance architecture:

* Exception identifier.
* Affected entity or rule.
* Requirement reference.
* Description.
* Reason.
* Risk or impact.
* Compensating controls where applicable.
* Responsible owner.
* Approving authority.
* Approval date.
* Expiry or review date.
* Current status.
* Evidence references.

Exceptions must be:

* Explicitly approved.
* Limited to a defined scope.
* Traceable.
* Reviewable.
* Revocable.
* Time-bound where appropriate.

An exception must not silently alter the underlying conformance requirement.

The system must distinguish an approved exception from a validation rule that does not apply.

REQ-23-22  -  Controlled deferral

Deferred work must have an explicit reason and accountable owner.

A deferred item must not be reported as complete.

The framework shall identify:

* Deferred requirement.
* Affected entity.
* Reason.
* Impact.
* Owner.
* Approval.
* Planned review date.
* Current status.

Expired deferrals shall be flagged.

REQ-23-23  -  CI integration

The framework shall integrate conformance validation into the repository’s existing CI pipeline.

The implementation must first inspect and reuse existing workflows, scripts and validation conventions.

It shall establish appropriate checks for:

* Pull requests.
* Entity additions.
* Entity modifications.
* Entity deletions.
* Relationship changes.
* Schema changes.
* Documentation changes.
* Controlled vocabulary changes.
* Validation rule changes.
* Periodic catalogue-wide validation.

The implementation shall not create duplicate CI mechanisms where existing tools can be extended.

REQ-23-24  -  Change-impact validation

Validation shall consider the impact of a proposed change beyond the modified file.

For example, a change to:

* An L2 Process may affect its L3 Activities and L1 membership.
* An L3 Activity may affect its L2 parent and L4 Tasks.
* An L4 Task may affect its L3 Activity and the parent L2 process reconciliation.
* A controlled vocabulary may affect all entities using that vocabulary.
* A schema may affect all entities of the relevant type.
* A relationship definition may affect multiple catalogues.

The implementation shall identify affected entities and execute relevant regression checks.

REQ-23-25  -  Validation reporting

Every validation run shall generate a machine-readable result and a human-readable summary.

The report must include:

* Validation run identifier.
* Timestamp.
* Repository revision or commit reference.
* Validation framework version.
* Schema version.
* Profile version.
* Rule catalogue version.
* Scope of validation.
* Rules executed.
* Results by severity.
* Results by conformance dimension.
* Affected entities.
* Identified defects.
* Approved exceptions.
* Deferred requirements.
* Overall outcome.
* Remediation guidance.

Reports must be reproducible and traceable to the repository revision being assessed.

REQ-23-26  -  Catalogue-level conformance dashboard

The framework shall produce catalogue-wide conformance information.

At minimum, it must report:

* Total entities by decomposition level.
* Percentage of entities structurally valid.
* Percentage conforming to their schema.
* Percentage meeting applicable profile requirements.
* Percentage with required evidence metadata.
* Percentage with verified material assertions where review is required.
* Percentage with current generated documentation.
* Percentage with valid parent-child relationships.
* Percentage reconciled under EXT-22.
* Number of open errors.
* Number of warnings.
* Number of approved exceptions.
* Number of deferred items.
* Number of overdue review actions.

The dashboard must not collapse distinct quality dimensions into a single score without exposing their component measures.

REQ-23-27  -  Validation framework versioning

The validation framework shall be version-controlled.

Versioning shall cover:

* Schemas.
* Decomposition profiles.
* Controlled vocabularies.
* Validation rules.
* Documentation templates.
* Conformance policies.
* Exception policies.

A change to a rule must include:

* Change rationale.
* Impact assessment.
* Compatibility assessment.
* Regression tests.
* Approval where required.

Historical validation reports must retain the version information needed to interpret their results.

REQ-23-28  -  Backward compatibility and progressive enforcement

The implementation shall distinguish:

* Existing catalogue baseline defects.
* Newly introduced defects.
* Defects resolved by the current change.
* Approved exceptions.
* Deferred remediation.

The framework shall not make all historical defects blocking immediately without a controlled migration and remediation strategy.

A progressive enforcement model shall be used where necessary:

1. Discovery and reporting.
2. Warning-only validation.
3. Blocking for newly introduced defects.
4. Remediation of historical defects.
5. Full enforcement of approved mandatory rules.

This must not become a permanent mechanism for concealing unresolved defects.

REQ-23-29  -  False-positive and false-negative management

The framework shall support the identification and review of incorrect validation outcomes.

It shall provide a controlled mechanism to:

* Report false positives.
* Identify false negatives.
* Update rule definitions.
* Improve test coverage.
* Record affected historical results.
* Re-run validation where necessary.

Changes to validation rules must not silently invalidate previous governance decisions.

REQ-23-30  -  Validation security and data protection

The framework shall ensure that validation reports and evidence references do not expose sensitive operational information unnecessarily.

It shall avoid:

* Embedding confidential evidence payloads in public reports.
* Exposing credentials or secrets.
* Publishing restricted source documents.
* Including sensitive personal or organisational data without authorisation.

Reports should reference controlled evidence locations where necessary.

REQ-23-31  -  Contributor feedback and remediation guidance

Conformance failures shall provide actionable explanations.

Each failed rule should communicate:

* What failed.
* Why it matters.
* Which entity is affected.
* Which requirement is involved.
* How the issue can be resolved.
* Whether human review is necessary.
* Whether an exception is permitted.

The objective is to make conformance useful to contributors, not merely punitive.

REQ-23-32  -  Continuous validation

The framework shall support both change-triggered and periodic validation.

Change-triggered validation shall run when relevant entities or supporting artefacts are modified.

Periodic validation shall detect issues arising from:

* External reference changes.
* Schema evolution.
* Controlled vocabulary changes.
* Expired exceptions.
* Stale evidence.
* Outdated documentation.
* Reconciliation drift.
* Changes in linked catalogues.

The frequency and execution mechanism shall be defined during implementation.

7. Conformance Profiles

The framework shall implement level-aware conformance profiles.

These profiles shall reuse EXT-11 and must not create a competing definition of decomposition semantics.

7.1 L0  -  Process Scope

Validation shall cover:

* Entity identity and classification.
* Scope purpose.
* Scope boundaries.
* Included and excluded areas.
* L1 relationships.
* Scope membership integrity.
* Overlaps and gaps.
* Documentation and evidence requirements.

L0 entities shall not be required to provide executable process definitions.

7.2 L1  -  Process Group

Validation shall cover:

* Entity identity and classification.
* Grouping purpose.
* Membership criteria.
* L2 Business Process references.
* Membership integrity.
* Duplicate and overlapping membership.
* Grouping rationale.
* Documentation and evidence requirements.

L1 entities shall not be treated as executable processes.

7.3 L2  -  Business Process

Validation shall cover:

* Process purpose.
* Process boundary.
* Transformation.
* Inputs.
* Outputs.
* Outcomes where applicable.
* Responsibilities and accountability.
* Triggers and preconditions where applicable.
* Interfaces and dependencies.
* Rules, controls and exceptions.
* Metrics and evidence.
* L3 decomposition.
* Reconciliation disposition.

7.4 L3  -  Activity

Validation shall cover:

* Activity purpose.
* Parent Business Process.
* Functional contribution.
* Cohesion.
* Boundaries.
* Relevant working objects, inputs and outputs.
* Responsibility.
* Applicable rules and controls.
* Dependencies and interfaces.
* L4 decomposition readiness.
* Reconciliation disposition.

7.5 L4  -  Task

Validation shall cover:

* Task purpose.
* Parent Activity.
* Bounded work description.
* Working object or input where applicable.
* Expected result.
* Completion condition.
* Verification evidence where applicable.
* Responsibility or performer where known.
* Relevant authorization.
* Rules, controls and exceptions.
* Dependencies and interfaces where applicable.
* Reconciliation disposition.

L4 validation must explicitly protect against the introduction of workflow execution semantics.

8. Validation Rule Classification

Every conformance rule shall be classified by its validation capability.

Class	Name	Description	Example
C1	Deterministic	Can be conclusively checked using available structured data.	A referenced parent entity exists.
C2	Rule-assisted	Can be evaluated through defined semantic constraints or pattern detection.	A Task appears to contain a prohibited runtime attribute.
C3	Evidence-dependent	Requires examination of source material or substantiation.	A process input is supported by authoritative documentation.
C4	Human-judgement	Requires business or domain interpretation.	Activities collectively cover the Business Process responsibility.
C5	Governance-controlled	Requires authorised review or approval.	An exception has been approved by the accountable authority.

The classification determines how a result may be reported.

A C2, C3, C4 or C5 rule must not be reported as conclusively passed merely because a script completed successfully.

9. CI/CD Enforcement Model

9.1 Pull request validation

Every relevant pull request shall execute the applicable conformance checks.

The implementation should validate:

1. Changed entities.
2. Their immediate parents.
3. Their immediate children.
4. Affected cross-references.
5. Related schemas and vocabularies where changed.
6. Generated documentation.
7. Relevant reconciliation records.

The validation scope shall be expanded where the change has broader impact.

9.2 Blocking policy

The default blocking policy shall be:

Finding	Default pull request outcome
New structural error	Block
New schema error	Block
Invalid canonical identifier	Block
Broken required reference	Block
Invalid decomposition-level relationship	Block
Missing mandatory profile requirement	Block, unless explicitly dispositioned
Missing required approval	Block
Invalid evidence metadata where mandatory	Block
Unresolved semantic review requirement	Block where approval is required
Potential duplicate	Warning or review gate
Potential boundary overlap	Warning or review gate
Advisory improvement	Informational
Approved exception	Allow within its approved scope
Approved deferral	Allow only under the applicable deferral policy

The implementation must distinguish pre-existing baseline defects from newly introduced defects.

9.3 Main-branch protection

The repository shall use the available platform mechanisms to ensure that mandatory conformance checks cannot be bypassed through ordinary contribution processes.

Administrative overrides, if available, must remain subject to repository governance and auditability.

9.4 Full catalogue validation

A full catalogue validation shall be available independently of pull request validation.

It shall assess the complete repository and produce a baseline report.

This validation must detect problems that are not visible when only changed files are checked.

10. Exception Management Model

10.1 Exception categories

The implementation should distinguish:

* Technical exception: a technical constraint prevents a requirement from being satisfied.
* Semantic exception: a requirement is not applicable to a particular entity because of its business meaning.
* Evidence exception: the necessary evidence is unavailable or restricted.
* Governance exception: an authorised decision permits a defined deviation.
* Migration exception: a historical entity requires temporary treatment while being migrated.

These categories must not be confused with ordinary incomplete documentation.

10.2 Exception lifecycle

The proposed lifecycle is:

proposed → under_review → approved / rejected → active → expired / revoked / closed

Only approved active exceptions may affect enforcement.

The lifecycle and allowed transitions shall be implemented consistently with the existing repository governance conventions.

10.3 Exception constraints

An exception:

* Must refer to a specific requirement or rule.
* Must identify its scope.
* Must have a rationale.
* Must identify its accountable owner.
* Must identify its approving authority.
* Must be reviewable.
* Must not change the underlying rule.
* Must not automatically propagate to child entities.

An exception on an L2 Process does not automatically exempt its L3 Activities or L4 Tasks.

11. Conformance Reporting and Quality Measures

11.1 Required reporting dimensions

The framework shall report quality independently across the conformance dimensions.

Measure	Purpose
Structural validity	Measures integrity of identifiers and hierarchy references.
Schema compliance	Measures conformity to canonical data structures.
Profile completeness	Measures satisfaction of applicable level-specific requirements.
Semantic review completion	Measures completion of required semantic assessments.
Evidence verification	Measures substantiation and review of material assertions.
Documentation currency	Measures alignment of generated documentation with canonical data.
Relationship integrity	Measures validity of internal and external references.
Reconciliation coverage	Measures completion of EXT-22 assessments.
Governance completion	Measures required review, approval and exception controls.

11.2 Avoid misleading aggregate scores

A single aggregate conformance percentage may conceal serious deficiencies.

For example, an entity could have excellent documentation but invalid parent references.

Therefore:

* Report each dimension separately.
* Identify critical failures independently.
* Do not average away blocking defects.
* Distinguish measured completeness from verified business correctness.
* Report the population and denominator used for every percentage.

11.3 Catalogue quality trend

Where historical reports are retained, the framework should support trends showing:

* Defects introduced.
* Defects resolved.
* Open defects.
* Defect ageing.
* Exceptions granted and expired.
* Documentation drift.
* Evidence review backlog.
* Reconciliation progress.
* Conformance rule effectiveness.

12. Work Packages

Work Package	Description	Primary output
WP-23-01	Existing validation and CI inventory	Validation architecture baseline
WP-23-02	Requirement-to-rule traceability	Conformance requirement matrix
WP-23-03	Conformance rule catalogue	Versioned rule register
WP-23-04	Schema and profile validation	L0-L4 profile validators
WP-23-05	Structural and relationship validation	Structural validation suite
WP-23-06	Semantic validation	Semantic rule and review framework
WP-23-07	Evidence validation	Evidence conformance checks
WP-23-08	Documentation validation	README and generation checks
WP-23-09	EXT-22 reconciliation validation	Reconciliation validator
WP-23-10	Exception and deferral governance	Exception management mechanism
WP-23-11	CI integration	Pull request and full catalogue validation
WP-23-12	Reporting and dashboard	Conformance reports and metrics
WP-23-13	Regression and quality testing	Validation test suite
WP-23-14	Progressive enforcement	Approved enforcement policy
WP-23-15	Operational readiness	Conformance framework deployment report

13. Testing Requirements

The implementation must include automated tests for the conformance framework itself.

13.1 Positive tests

Verify that:

* Valid L0-L4 entities pass applicable structural checks.
* Valid parent-child relationships are accepted.
* Valid references are resolved.
* Correctly populated profile requirements pass.
* Approved exceptions are respected within scope.
* Approved deferrals are reported correctly.
* Generated documentation passes consistency checks.
* Reconciliation records with valid evidence and dispositions are accepted.

13.2 Negative tests

Verify that:

* Invalid YAML is rejected.
* Duplicate canonical identifiers are detected.
* Broken parent references are detected.
* Invalid decomposition relationships are rejected.
* Unsupported vocabulary values are rejected.
* Mandatory information is missing and not explicitly dispositioned.
* Invalid evidence metadata is detected.
* Required approvals are absent.
* README and canonical entity data conflict.
* Prohibited workflow constructs are detected where their semantics are confirmed.
* Expired exceptions are flagged.
* Unapproved deferrals are rejected.
* Reconciliation records reference nonexistent entities.

13.3 Boundary and edge-case tests

Test:

* L3 Activities with no Tasks but approved decomposition dispositions.
* L2 Processes with approved exceptions.
* Entities with unresolved evidence.
* Conflicting source records.
* External references unavailable during CI.
* Historical baseline defects.
* Deprecated vocabulary values.
* Schema migration.
* Multiple parent-child relationships where permitted.
* Shared functional responsibilities.
* Changes affecting multiple levels.
* Documentation generated from partially enriched entities.

13.4 Regression tests

Every material change to schemas, profiles or rules must run the relevant regression suite.

A change to the validation framework must not silently cause valid historical entities to fail without an identified reason and migration strategy.

14. Acceptance Criteria

EXT-23 shall be considered complete when:

AC-23-01  -  A formal conformance architecture covering all required validation dimensions is documented and approved.

AC-23-02  -  Every enforceable requirement from EXT-08 through EXT-22 has an explicit traceability status.

AC-23-03  -  A version-controlled conformance rule catalogue exists.

AC-23-04  -  Each rule has a unique identifier, classification, severity, applicability and remediation guidance.

AC-23-05  -  L0-L4 entities are validated against their applicable schemas and decomposition profiles.

AC-23-06  -  Structural and relationship integrity checks are implemented.

AC-23-07  -  Semantic distinctions established under EXT-09 through EXT-14 are represented in the conformance framework.

AC-23-08  -  Functional decomposition checks are aligned with EXT-22.

AC-23-09  -  Evidence metadata and verification requirements are validated.

AC-23-10  -  Documentation consistency and generation checks are implemented.

AC-23-11  -  Cross-catalogue references are validated wherever source information is available.

AC-23-12  -  Reconciliation records and dispositions are validated.

AC-23-13  -  Exception and deferral management is implemented or integrated with an approved existing governance mechanism.

AC-23-14  -  Pull request validation is integrated with existing CI processes.

AC-23-15  -  Full catalogue validation is available independently of pull request validation.

AC-23-16  -  The validation system distinguishes new defects from historical baseline defects.

AC-23-17  -  Automated checks do not misrepresent semantic or evidence-dependent review as completed.

AC-23-18  -  Machine-readable and human-readable validation reports are generated.

AC-23-19  -  Catalogue-wide quality measures are available by conformance dimension.

AC-23-20  -  Positive, negative, edge-case and regression tests are implemented.

AC-23-21  -  Validation rules and profiles are version-controlled and change-managed.

AC-23-22  -  The progressive enforcement strategy is documented and approved.

AC-23-23  -  False-positive and false-negative management is documented.

AC-23-24  -  Security and information disclosure considerations are addressed.

AC-23-25  -  The framework has been tested against a representative catalogue population.

AC-23-26  -  Known limitations, unresolved rules, exceptions and deferrals are documented.

AC-23-27  -  The conformance framework is approved for operational use.

AC-23-28  -  The final implementation report establishes readiness for EXT-24 continuous governance.

15. Risks and Mitigations

Risk	Impact	Mitigation
Excessive automated enforcement	Valid entities rejected	Classify rules by determinism and applicability.
Semantic rules reduced to text matching	False positives and incorrect conclusions	Use contextual checks and human review.
Inconsistent validation logic	Different results across tools	Maintain a central rule catalogue.
Historical defects block all contributions	Repository becomes difficult to maintain	Introduce progressive enforcement.
Exceptions become permanent loopholes	Quality deterioration	Require ownership, review and expiry.
Documentation becomes a separate source of truth	Data inconsistency	Validate against canonical entity representations.
External references cannot be resolved	False invalid-reference findings	Distinguish unresolved from invalid references.
CI performance degrades	Slow contribution workflow	Use change-impact analysis and scheduled full validation.
Rule changes invalidate historical reports	Loss of auditability	Version schemas, profiles and rule catalogues.
Passing CI is interpreted as business assurance	False confidence	Explicitly communicate the limits of automated validation.
AI-generated assessments are treated as verified	Unsupported assertions	Require evidence and authorised human approval.
Too many warning-level findings	Warning fatigue	Prioritise findings and periodically review rule quality.

16. Dependencies and Related CRs

CR	Contribution to EXT-23
EXT-08	Documentation architecture and source-of-truth alignment
EXT-09	Operational documentation semantic contract
EXT-10	Canonical entity schema
EXT-11	L0-L4 documentation profiles
EXT-12	Input, output and interface semantics
EXT-13	Responsibility and accountability
EXT-14	Rules, controls and exceptions
EXT-15	Evidence, provenance and confidence
EXT-16	Authoring and research methodology
EXT-17	Tooling and validation architecture
EXT-18	Pilot validation evidence
EXT-19	L2 enrichment baseline
EXT-20	L3 enrichment baseline
EXT-21	L4 enrichment baseline
EXT-22	Cross-level reconciliation and structural integrity
EXT-23	Conformance framework and quality gates
EXT-24	Continuous governance and catalogue closure

17. ADR Considerations

The implementation must reuse existing ADR decisions wherever they address the relevant concerns.

The following additional ADRs may be required if those decisions have not already been established.

ADR-BP-CONF-001  -  Conformance Rule Architecture

Determine how rules are represented, organised, versioned and executed.

Decision considerations:

* Declarative versus programmatic rules.
* Rule identifiers and metadata.
* Shared versus level-specific rules.
* Traceability to CR requirements.
* Rule testing and versioning.

ADR-BP-CONF-002  -  Validation Outcome and Severity Model

Establish the authoritative severity and outcome vocabularies.

Decision considerations:

* Blocking versus non-blocking findings.
* Partial validation.
* Historical baseline defects.
* Approved exceptions.
* Deferred findings.
* Reporting semantics.

ADR-BP-CONF-003  -  Exception and Waiver Governance

Determine whether exception records are maintained within the process catalogue, a shared governance repository or an existing organisational control mechanism.

Decision considerations:

* Ownership.
* Approval authority.
* Expiry.
* Scope.
* Auditability.
* Cross-catalogue reuse.

ADR-BP-CONF-004  -  Progressive Enforcement Strategy

Establish the migration from reporting-only validation to mandatory conformance gates.

Decision considerations:

* Existing defect baseline.
* Blocking thresholds.
* Historical remediation.
* New defect prevention.
* Administrative overrides.

ADR-BP-CONF-005  -  Validation Report and Metrics Architecture

Determine how machine-readable validation results, historical reports and dashboards are maintained.

Decision considerations:

* Repository storage versus external reporting.
* Report retention.
* Historical comparison.
* Dashboard data source.
* Traceability to commits and rule versions.

ADR-BP-CONF-006  -  Semantic Validation and Human Review Boundary

Establish the authoritative boundary between automated validation and human judgement.

Decision considerations:

* Deterministic semantic rules.
* Assisted detection.
* Evidence assessment.
* Required reviewer roles.
* Approval traceability.
* AI-assisted assessment disclosure.

These ADRs should only be created where an existing decision does not already settle the matter.

18. Implementation Sequence

The recommended implementation order is:

Sequence	Activity	Dependency
1	Inspect existing schemas, scripts, workflows and CI	Repository baseline
2	Establish requirement-to-rule traceability	EXT-08-EXT-22
3	Establish the rule catalogue and severity model	Step 2
4	Implement schema and profile validation	EXT-10, EXT-11
5	Implement structural and relationship validation	EXT-10, EXT-22
6	Implement semantic validation and review prompts	EXT-09, EXT-12-EXT-14
7	Implement evidence and provenance validation	EXT-15
8	Implement documentation consistency validation	EXT-17
9	Implement reconciliation validation	EXT-22
10	Implement exception and deferral governance	Approved ADRs
11	Integrate with CI and repository contribution controls	Existing CI baseline
12	Implement reporting and catalogue metrics	Steps 3-11
13	Test against representative and historical entities	Complete validation suite
14	Apply progressive enforcement	Approved enforcement policy
15	Produce operational readiness assessment	All preceding steps

19. Definition of Done

EXT-23 is complete when the Business Process catalogue has an operational, version-controlled and maintainable conformance framework.

The framework must be able to determine whether an entity or proposed repository change:

* Is structurally valid.
* Conforms to the canonical schema.
* Satisfies its applicable decomposition profile.
* Uses valid identifiers and relationships.
* Respects approved semantic constraints.
* Has appropriate evidence and provenance.
* Maintains documentation consistency.
* Satisfies applicable reconciliation requirements.
* Has the required governance approvals.
* Has no unresolved blocking defects or unapproved exceptions.

The framework must also be able to explain the result, identify the failed requirements, provide remediation guidance and preserve the history of validation decisions.

A successful automated validation result must not be presented as proof that the documented business process is effective or that every operational assertion reflects actual organisational practice.

EXT-23 establishes the enforceable quality baseline for the Business Process catalogue and makes sustained conformance a controlled part of the repository lifecycle.




20. Final Implementation Directive

The implementation team shall begin by examining the actual repository and its existing automation.

The first implementation activity is an inventory of:

1. Existing schemas and entity templates.
2. Existing YAML and metadata validation.
3. Existing README generation.
4. Existing CI workflows.
5. Existing identifier and reference checks.
6. Existing cross-catalogue validation.
7. Existing tests and reporting mechanisms.
8. Existing exception or governance conventions.

The implementation must extend these mechanisms where possible rather than creating a parallel validation architecture.

The initial delivery should establish the conformance rule catalogue, requirement traceability matrix and baseline validation report before enabling blocking gates.

This sequence is essential: the programme must understand the current quality baseline before it can introduce fair, consistent and sustainable enforcement.

Final programme outcome: the Business Process catalogue becomes continuously validated, traceable, reviewable and governed, with a clear distinction between machine-verifiable correctness and business-semantic assurance.

Important design decisions for EXT-23

There are five architectural decisions I would preserve throughout implementation:

* No single conformance score: structural, semantic, evidence, documentation and governance quality must remain separately visible.
* No false semantic automation: scripts can detect missing assessments and suspicious patterns, but cannot certify that a decomposition represents the real business.
* No permanent grandfathering: historical defects can be migrated progressively, but new defects must be prevented and old defects must have an accountable remediation path.
* No parallel source of truth: validation rules must consume the canonical schemas, profiles and controlled vocabularies.
* No ungoverned exceptions: waivers must have owners, scope, approval and review dates.

Recommended next step

Before EXT-24, I recommend a focused implementation-design exercise for EXT-23: establish the CR-to-Conformance Rule Traceability Matrix, mapping every requirement from EXT-08 through EXT-23 to its validation rule, enforcement method, severity, test case and evidence of compliance.

That matrix will expose any requirement that has been specified but never operationalised, and it will provide the foundation for EXT-24’s ongoing governance.