The next six CRs should establish the evidence and authoring discipline, prepare the enrichment pipeline, validate it through a controlled pilot, and then begin catalogue backfill in dependency order.

I recommend retaining the previously proposed sequence and scope:

CR	Focus	Principal outcome
EXT-15	Evidence, provenance and confidence	Every operational assertion has a defensible basis and known confidence
EXT-16	Operational authoring and research methodology	A repeatable, auditable method for researching and documenting process operations
EXT-17	Enrichment tooling and backfill orchestration	Controlled tooling for authoring, validation, generation and migration
EXT-18	Operational documentation pilot	Evidence that the model and process work on representative entities
EXT-19	L2 Business Process backfill	Enrich the canonical business-process layer first
EXT-20	L3 Activity backfill	Enrich activities against validated L2 parent processes

These are proposed CR documents, not claims that the files or changes have already been committed. The specifications below preserve the key architectural rule: entity data remains canonical; README documentation is generated from that data; and no operational detail is invented to satisfy completeness targets.

CR-BP-94-EXT-15 : Evidence, Provenance and Confidence Framework

Proposed file: change-requests/CR-BP-94-EXT-15-evidence-provenance-and-confidence-framework.md
Programme: CR-BP-94 : Process Decomposition and Operational Documentation
Type: Data semantics, governance and documentation integrity
Priority: Critical
Depends on: EXT-09, EXT-10, EXT-11, EXT-12, EXT-13, EXT-14
Enables: EXT-16, EXT-17, EXT-18 and subsequent catalogue backfill

1. Purpose

Establish a consistent framework for recording the evidential basis, provenance, confidence and review status of operational assertions within Business Process catalogue entities.

The framework must ensure that operational documentation is:

* Traceable to identifiable sources.
* Explicit about what is known, inferred, assumed or unknown.
* Distinguishable from unverified or provisional content.
* Reviewable by an appropriately qualified person.
* Safe to publish without exposing confidential operational evidence.
* Consistent across L0-L4 decomposition levels.

This CR prevents the enrichment programme from turning plausible descriptions into unsupported representations of actual organisational operations.

2. Problem statement

Operational documentation may be derived from different sources, including:

* Published policies and procedures.
* Process owner interviews.
* Business function and capability documentation.
* Enterprise architecture artefacts.
* Information system and integration documentation.
* Regulatory and industry requirements.
* Existing process documentation.
* Direct observation and validated operational records.
* Expert interpretation where direct evidence is unavailable.

These sources have different authority, currency, reliability and scope.

Without a common provenance model, the catalogue cannot reliably distinguish an approved operating fact from an analyst interpretation or an AI-generated suggestion.

A process entity may consequently appear complete while containing assertions that are unsupported, outdated or incorrectly generalized.

3. Objectives

1. Establish a canonical evidence and provenance model.
2. Distinguish source records from the assertions they support.
3. Introduce confidence and verification classifications.
4. Support multiple sources and conflicting evidence.
5. Establish review and approval requirements.
6. Preserve source references without unnecessarily copying sensitive material.
7. Integrate evidence status into documentation generation and CI validation.
8. Support progressive enrichment without requiring every fact to be fully evidenced before an entity can be documented.

4. Scope

In scope

* Provenance metadata for operational assertions.
* Source classification and authority.
* Confidence classification.
* Verification and review status.
* Evidence-to-assertion relationships.
* Conflicting or superseded evidence.
* Evidence freshness and review dates.
* AI-assisted research disclosure.
* Evidence validation and reporting.
* L0-L4 applicability.

Out of scope

* Replacing the organisation’s records-management platform.
* Storing complete audit evidence or confidential operational records in the public catalogue.
* Establishing a new enterprise risk or compliance repository.
* Treating confidence scores as statistical probabilities without a defined statistical basis.
* Automatically approving AI-generated assertions.

5. Normative requirements

REQ-15-01 : Assertion provenance

Every operational assertion that requires evidence must be capable of being associated with one or more provenance records.

An assertion may be represented directly within an entity field or as a structured item within an approved collection. The implementation must follow the schema decisions established in EXT-10.

REQ-15-02 : Source classification

The framework shall support a controlled source classification. At minimum:

Source class	Description
authoritative_document	Approved policy, procedure, standard or controlled document
system_documentation	Verified system, integration or architecture documentation
owner_confirmation	Confirmation from an appropriately authorized process owner
subject_matter_expert	Confirmation from a qualified domain expert
direct_observation	Directly observed operational practice
operational_record	Validated operational record or measurement
external_authority	Applicable regulation, standard or authoritative external source
secondary_reference	Industry research or other secondary material
analyst_inference	Explicitly identified interpretation by the author
ai_assisted_research	AI-assisted discovery or synthesis requiring independent validation

The list shall be maintained as a controlled vocabulary and extended only through governed changes.

REQ-15-03 : Provenance record

The implementation shall support the following conceptual attributes, subject to the canonical schema established in EXT-10:

* Provenance identifier.
* Source title or description.
* Source class.
* Source owner or issuing authority, where known.
* Source location or reference.
* Relevant section, page, record or fragment reference, where available.
* Publication or effective date, where known.
* Date accessed or reviewed.
* Source version, where applicable.
* Assertions supported.
* Evidence limitations.
* Confidentiality or publication classification.
* Reviewer and review status, where applicable.

The catalogue should retain a reference to evidence rather than reproduce sensitive evidence content.

REQ-15-04 : Confidence classification

Introduce a controlled qualitative confidence classification:

Classification	Meaning
high	Directly supported by current authoritative evidence or independently validated confirmation
medium	Supported by credible evidence, but with limitations in scope, currency or completeness
low	Based on indirect evidence, incomplete corroboration or a qualified interpretation
unverified	No sufficient supporting evidence has been established
conflicting	Available evidence contains unresolved material contradictions

Confidence must not be presented as a numerical probability.

A confidence classification describes the strength of the evidence supporting an assertion, not the importance of the assertion or the quality of the process itself.

REQ-15-05 : Verification status

Confidence and verification status shall remain separate concepts.

The implementation shall support at least:

* not_reviewed
* under_review
* verified
* rejected
* superseded
* disputed

A high-confidence assertion is not automatically approved. Verification requires an appropriate review process.

REQ-15-06 : Explicit uncertainty

The framework shall distinguish:

* Unknown because information has not been obtained.
* Not applicable to the entity or decomposition level.
* Not yet assessed.
* Inherited from a parent entity.
* Deferred for a documented reason.
* Conflicting evidence.
* Confirmed absence of a characteristic.

These states must not be represented by an empty string or silently omitted where doing so would imply completeness.

REQ-15-07 : Evidence conflict resolution

Where sources conflict:

1. Preserve the conflicting source references.
2. Identify the affected assertion.
3. Record the nature of the conflict.
4. Identify the authority responsible for resolution.
5. Record the resolution and rationale when established.
6. Retain the superseded assertion or evidence history where repository conventions permit.

The author must not silently select whichever source produces the most convenient description.

REQ-15-08 : Freshness

Evidence records shall support source currency and review dates.

The implementation should permit future policies for periodic review, but this CR shall not impose a universal expiry period on all evidence types.

A regulation, an organisational procedure and an interview confirmation have different currency characteristics.

REQ-15-09 : AI-assisted research

AI-generated content shall be treated as a research aid, not as authoritative evidence.

Where AI assistance materially contributes to an operational assertion:

* The assertion must be independently validated.
* The underlying source references must be recorded.
* The author or reviewer must remain identifiable through the repository’s established governance mechanism.
* AI-generated interpretation must not be represented as direct owner confirmation.
* Unverifiable claims must remain unverified or be excluded.

REQ-15-10 : Publication safety

Evidence records must not expose confidential personal data, commercially sensitive information, credentials, restricted system details or protected operational records.

Where necessary, use controlled references, redacted descriptions or approved external evidence locations.

REQ-15-11 : Documentation generation

Generated READMEs shall communicate evidence status where relevant.

They must not expose internal evidence payloads or imply that an assertion is verified merely because it appears in generated documentation.

REQ-15-12 : Cross-catalogue provenance

Evidence references may support relationships with Business Functions, Business Capabilities, Information Systems, Information Systems Functions, policies, controls, risks and metrics.

Such relationships must use canonical entities and metamodel-approved relationship types. This CR shall not introduce new cross-catalogue relationship semantics independently.

6. Implementation requirements

The repository implementation shall:

1. Inspect the existing entity schema and metadata conventions.
2. Establish the canonical location for provenance and evidence references.
3. Introduce controlled vocabularies and validation rules.
4. Define how assertions link to evidence.
5. Define the representation of unresolved conflicts.
6. Update applicable L0-L4 templates.
7. Update README generation to render appropriate evidence status.
8. Add schema and semantic validation tests.
9. Provide migration support for existing entities.
10. Document how evidence references are maintained and reviewed.

Exact file names and locations must follow the existing repository structure.

7. Acceptance criteria

* [ ]	Canonical provenance structure is defined and implemented.
* [ ]	Source classifications are controlled and documented.
* [ ]	Confidence and verification status are distinct.
* [ ]	Unknown, deferred, inherited, not-applicable and conflicting states are distinguishable.
* [ ]	Multiple sources can support one assertion.
* [ ]	Conflicting sources can be represented without silent overwriting.
* [ ]	Evidence freshness is represented where applicable.
* [ ]	AI-assisted research is explicitly distinguishable from authoritative evidence.
* [ ]	Sensitive evidence is not copied into public catalogue content.
* [ ]	README generation can communicate evidence status.
* [ ]	Schema and semantic validation tests pass.
* [ ]	Existing entities remain valid or have a documented migration path.
* [ ]	EXT-16 can use the framework without introducing another provenance model.

8. Risks and mitigations

Risk	Mitigation
Excessive evidence overhead	Apply evidence requirements according to assertion significance and profile
False confidence	Keep confidence qualitative and distinct from approval
Stale sources	Record review dates and source currency
Conflicting documentation	Preserve conflicts and require explicit resolution
AI-generated inaccuracies	Require source-based validation and accountable human review
Sensitive evidence exposure	Store references and approved metadata, not restricted payloads

9. Completion definition

EXT-15 is complete when the evidence and provenance model is implemented, documented, validated and usable by entity templates, README generation and subsequent authoring processes.

::

CR-BP-94-EXT-16 : Operational Authoring and Research Methodology

Proposed file: change-requests/CR-BP-94-EXT-16-operational-authoring-and-research-methodology.md
Type: Authoring standards, research methodology and governance
Priority: Critical
Depends on: EXT-10, EXT-11, EXT-12, EXT-13, EXT-14, EXT-15
Enables: EXT-17 and EXT-18

1. Purpose

Establish a repeatable methodology for researching, authoring, reviewing and maintaining operational documentation for Business Process catalogue entities.

The methodology shall ensure that different contributors can enrich process entities consistently without introducing unsupported operational assumptions, duplicating information or confusing decomposition levels.

2. Problem statement

The schema and documentation profiles establish what can be represented. They do not, by themselves, establish how contributors should discover and validate the information.

Without a common methodology, contributors may:

* Infer operating procedures from process names.
* Confuse a business process with its activities or tasks.
* Describe a presumed ideal process rather than actual organisational practice.
* Duplicate responsibilities already represented elsewhere.
* Invent inputs, outputs, controls or system dependencies.
* Treat an AI-generated description as evidence.
* Enrich child entities without validating their parent process.

3. Objectives

1. Define a standard research and authoring lifecycle.
2. Establish source prioritisation and research methods.
3. Define decomposition-aware authoring guidance.
4. Establish human review and approval responsibilities.
5. Define how gaps and uncertainties are documented.
6. Prevent unsupported operational claims.
7. Establish quality criteria for accepting enriched entities.
8. Create repeatable guidance for human and AI-assisted contributors.

4. Scope

In scope:

* Research planning.
* Source discovery and evaluation.
* Process owner and subject-matter expert engagement.
* Entity authoring.
* Evidence capture.
* Decomposition and parent-child reconciliation.
* Review and approval.
* AI-assisted research and authoring.
* Documentation quality assurance.
* Maintenance and change management.

Out of scope:

* Replacing enterprise process management practices.
* Mandating one process-modelling notation.
* Defining operational workflows for the organisation.
* Establishing an organisation-wide process redesign methodology.

5. Normative requirements

REQ-16-01 : Standard authoring lifecycle

Every enrichment activity shall follow a documented lifecycle:

1. Select entity and establish scope.
2. Inspect current entity and its parent/child relationships.
3. Identify information gaps against the applicable profile.
4. Develop a research plan.
5. Identify and assess available sources.
6. Capture evidence and provenance.
7. Draft operational assertions.
8. Validate semantic distinctions.
9. Reconcile with related catalogue entities.
10. Obtain required review and approval.
11. Update canonical entity data.
12. Generate documentation.
13. Execute validation and quality checks.
14. Submit changes through the repository’s established review process.

REQ-16-02 : Source prioritisation

Authors shall prefer sources in the following general order, subject to the authority and relevance of the source:

1. Approved organisational policies and procedures.
2. Authorized process owner confirmation.
3. Controlled operational documentation.
4. Verified system and architecture records.
5. Direct observation and validated operational records.
6. Qualified subject-matter expert confirmation.
7. Authoritative external regulations and standards.
8. Credible secondary research.
9. Analyst inference.

This ordering is guidance, not an automatic authority ranking. A source may be authoritative for one assertion and irrelevant to another.

REQ-16-03 : Actual practice versus target practice

Authors must distinguish:

* Current operating practice.
* Approved documented practice.
* Intended or target operating practice.
* Proposed future-state practice.
* External normative requirements.

A target-state description must not be presented as the current operational process.

Where documented practice and observed practice differ, record the discrepancy and its evidence rather than silently reconciling the two.

REQ-16-04 : Decomposition-aware authoring

Authoring shall respect the L0-L4 distinctions established in EXT-11.

* L0 describes process scope and context.
* L1 describes process grouping and membership.
* L2 describes the business transformation and its operational boundaries.
* L3 describes cohesive bodies of work contributing to an L2 process.
* L4 describes bounded, independently understandable tasks.

L0 and L1 shall not be treated as executable operational units.

L4 shall not become a workflow-engine specification.

REQ-16-05 : L2-first enrichment

Operational enrichment shall normally begin at L2.

The L2 process provides the transformation context against which L3 activities and L4 tasks can be assessed.

An exception may be made for a child entity where there is a specific research or remediation reason, but its parent relationship and unresolved dependencies must be recorded.

REQ-16-06 : Semantic distinction checklist

Authors shall validate that the following distinctions are preserved:

Concept A	Concept B	Required distinction
Input	Resource	Information or object entering a transformation versus capacity used to perform work
Output	Outcome	Produced deliverable versus resulting business effect
Transformation	Workflow	Business change versus execution sequence
Role	Organizational unit	Responsibility-bearing position versus organisational structure
Responsibility	Accountability	Performing or contributing versus answerability and authority
Rule	Control	Requirement or constraint versus mechanism that manages compliance or risk
Control	Evidence	Mechanism versus proof of design or operation
Exception	Deviation	Recognized permitted variation versus departure from expected practice
Trigger	Precondition	Initiating event versus condition required for work to proceed
Dependency	Decomposition	Reliance on another entity versus structural parent-child relationship

REQ-16-07 : Gap recording

Authors must not fill unknown fields with invented content.

Where information is unavailable, use the appropriate status from the approved schema and profile.

For material gaps, record:

* What is unknown.
* Why it matters.
* Research already performed.
* Sources consulted.
* Who can resolve the gap.
* Whether the gap blocks publication, approval or only full operational completeness.

REQ-16-08 : Review roles

The methodology shall distinguish:

* Author.
* Domain reviewer.
* Process owner or authorized approver.
* Catalogue maintainer.
* Schema or metamodel reviewer, where applicable.

Not every entity requires every role to be a separate person. However, the approval authority must be clear.

REQ-16-09 : AI-assisted authoring

AI tools may assist with:

* Source discovery.
* Document summarisation.
* Candidate assertion extraction.
* Terminology harmonisation.
* Gap analysis.
* Drafting.
* Structural validation.

AI tools shall not independently:

* Confirm actual organisational practice.
* Approve process ownership or accountability.
* Establish an authoritative control.
* Convert an assumption into a verified fact.
* Invent source references.
* Resolve conflicting evidence without human authorization.

REQ-16-10 : Authoring records

Each enrichment change shall be traceable through the repository’s established change-management mechanism.

Where the existing entity schema supports it, relevant metadata should include author, reviewer, review date, source references and change rationale.

Avoid duplicating Git history or CR governance metadata unnecessarily.

REQ-16-11 : Quality review

Every enriched entity shall be reviewed for:

* Semantic correctness.
* Decomposition-level appropriateness.
* Evidence quality.
* Parent-child consistency.
* Cross-catalogue reference validity.
* Completeness against its profile.
* Publication safety.
* README and entity consistency.

REQ-16-12 : Reproducibility

The methodology and templates must be sufficiently explicit that another qualified contributor can understand why an assertion was made and how it was validated.

6. Deliverables

* Operational authoring handbook.
* Research planning template.
* Source assessment guidance.
* Entity enrichment checklist.
* Process owner review checklist.
* AI-assisted research and validation guidance.
* Gap and uncertainty recording guidance.
* L0-L4 authoring examples.
* Review and approval workflow documentation.

7. Acceptance criteria

* [ ]	Standard authoring lifecycle documented.
* [ ]	Source evaluation methodology established.
* [ ]	Current, target and proposed practice distinguished.
* [ ]	L0-L4 authoring guidance aligned with EXT-11.
* [ ]	L2-first enrichment rule documented.
* [ ]	Semantic distinction checklist implemented in guidance.
* [ ]	Gap recording methodology defined.
* [ ]	Review and approval responsibilities established.
* [ ]	AI-assisted research boundaries documented.
* [ ]	Authoring and review checklists available.
* [ ]	Pilot contributors can apply the methodology consistently.
* [ ]	No conflict with the canonical provenance framework.

8. Completion definition

EXT-16 is complete when the authoring methodology, templates, research guidance and review criteria are published and can be applied consistently in the enrichment tooling and pilot.

::

CR-BP-94-EXT-17 : Enrichment Tooling and Backfill Orchestration

Proposed file: change-requests/CR-BP-94-EXT-17-enrichment-tooling-and-backfill-orchestration.md
Type: Repository engineering, automation and quality assurance
Priority: High
Depends on: EXT-10 through EXT-16
Enables: EXT-18 through EXT-24

1. Purpose

Establish the repository tooling required to execute operational documentation enrichment at scale.

The tooling shall support controlled authoring, schema validation, evidence validation, README generation, parent-child reconciliation, migration and backfill reporting.

It must work with the repository’s existing CI and automation architecture rather than introduce a competing toolchain.

2. Objectives

1. Make canonical entity data the source for generated documentation.
2. Reduce manual documentation duplication.
3. Provide deterministic validation and generation.
4. Support controlled batch enrichment.
5. Enable safe migration of existing entities.
6. Produce actionable quality and completeness reports.
7. Support staged rollout and rollback.
8. Preserve the repository’s established contribution workflow.

3. Scope

In scope:

* Schema validation.
* Profile-aware validation.
* Evidence and provenance validation.
* README generation.
* Parent-child consistency checks.
* Cross-reference validation.
* Migration and backfill scripts.
* Dry-run and reporting modes.
* CI integration.
* Error and warning reporting.
* Reproducibility and idempotency.

Out of scope:

* A new workflow execution engine.
* A new enterprise process-management platform.
* Automatic invention of missing operational content.
* A separate documentation database.
* Automatic approval of enriched entities.

4. Normative requirements

REQ-17-01 : Tooling inventory

Before implementation, inspect and document:

* Existing schema and template locations.
* Existing entity formats and conventions.
* README generation mechanisms.
* Existing scripts and command interfaces.
* CI workflows and validation stages.
* Existing test frameworks.
* Existing migration utilities.
* Repository contribution and release practices.

No replacement tooling shall be introduced until the existing mechanisms have been assessed.

REQ-17-02 : Canonical source

Entity data shall remain the canonical source for operational facts.

README files shall be generated from canonical entity data and approved templates.

Where README files contain manually maintained content that cannot be represented in the entity model, the implementation must identify and govern that content explicitly rather than silently overwrite it.

REQ-17-03 : Deterministic generation

Given identical entity data, schema version, profile version and generator version, documentation generation shall produce equivalent output.

Generation must not depend on undocumented environmental state or uncontrolled external services.

REQ-17-04 : Validation layers

Implement distinct validation layers:

1. Syntax validation: YAML or other source format is parseable.
2. Schema validation: Fields and data structures conform to the canonical schema.
3. Profile validation: Applicable L0-L4 documentation requirements are satisfied.
4. Semantic validation: Concept distinctions and value constraints are respected.
5. Evidence validation: Required provenance and verification metadata are present.
6. Reference validation: Referenced entities and identifiers resolve.
7. Hierarchy validation: Parent-child relationships are coherent.
8. Documentation validation: Generated README reflects canonical data.
9. Governance validation: Required review or approval conditions are satisfied.

A single generic pass/fail result must not conceal the category of failure.

REQ-17-05 : Severity model

Validation findings shall support:

* error: invalid or unsafe state that blocks acceptance.
* warning: quality concern requiring review.
* info: advisory observation.
* deferred: recognized incomplete requirement with an accepted disposition.

Warnings must not be silently converted into successful compliance.

REQ-17-06 : Dry-run support

Backfill and migration utilities shall support a dry-run mode that reports proposed changes without modifying repository files.

Reports shall identify:

* Entities examined.
* Fields or structures affected.
* Existing content retained.
* Proposed changes.
* Validation findings.
* Unresolved references.
* Entities requiring human review.

REQ-17-07 : Idempotency

Migration and generation operations must be idempotent.

Repeated execution against unchanged source data must not introduce duplicate fields, duplicate records, reordered content without reason or repeated migration effects.

REQ-17-08 : Safe migration

Migration tooling shall:

* Preserve existing identifiers.
* Preserve existing semantic meaning.
* Avoid overwriting manually authored content without explicit rules.
* Provide pre-migration and post-migration validation.
* Support a documented recovery or rollback strategy.
* Record migration version and results where appropriate.

REQ-17-09 : Profile-aware generation

The generator shall use the correct L0-L4 profile.

It must not generate operational sections that are inappropriate to the entity’s decomposition level.

REQ-17-10 : Evidence-aware generation

Generated documentation shall distinguish verified, provisional, unverified, disputed and deferred assertions where the profile requires that distinction.

It must not render unverified material as established fact.

REQ-17-11 : Cross-reference validation

Where an entity references another catalogue entity, validation shall confirm:

* The reference follows the canonical identifier convention.
* The target exists or is explicitly marked as an approved unresolved dependency.
* The relationship is permitted by the metamodel.
* The referenced entity is not confused with a similarly named entity.

REQ-17-12 : Reporting

Provide reports at both entity and catalogue levels.

Catalogue-level reporting shall include:

* Total entities examined by level.
* Profile completeness.
* Evidence coverage.
* Verification status distribution.
* Outstanding warnings and errors.
* Broken references.
* Parent-child reconciliation status.
* Entities awaiting owner review.
* Backfill completion status.

REQ-17-13 : CI integration

Integrate the validation stages into the existing CI pipeline.

The implementation must identify which checks are blocking at initial rollout and which become blocking only after the relevant backfill or migration gate is passed.

REQ-17-14 : No automatic semantic invention

The tooling may identify missing information and propose candidate enrichment actions.

It must not create operational assertions merely to satisfy required-field checks.

REQ-17-15 : Contributor usability

Provide clear commands or documented execution procedures for:

* Validating one entity.
* Validating a selected set.
* Validating the entire catalogue.
* Generating one README.
* Generating all applicable READMEs.
* Running a migration in dry-run mode.
* Producing a backfill report.

Exact commands shall follow the repository’s established tooling conventions.

5. Proposed implementation components

The implementation should provide the following logical capabilities, whether as separate scripts or integrated modules:

Component	Responsibility
Entity validator	Syntax and schema conformance
Profile validator	L0-L4 requirements
Evidence validator	Provenance and verification
Reference validator	Canonical identifier resolution
Hierarchy validator	Parent-child integrity
README generator	Canonical data to documentation
Migration utility	Controlled schema/data migration
Backfill orchestrator	Controlled execution across entity sets
Quality reporter	Entity and catalogue status reporting

These are logical components, not mandatory filenames or a prescription to create unnecessary separate executables.

6. Testing requirements

Tests shall include:

* Valid and invalid entity examples at every level.
* Missing and unknown values.
* Invalid confidence and verification classifications.
* Missing provenance where required.
* Conflicting evidence.
* Broken and valid cross-references.
* Incorrect parent-child assignments.
* README generation consistency.
* Repeated migration and generation.
* Dry-run non-mutation.
* Rollback or recovery behaviour.
* CI blocking and non-blocking conditions.

7. Acceptance criteria

* [ ]	Existing tooling and CI inventory completed.
* [ ]	Canonical entity-to-README generation established.
* [ ]	Deterministic generation demonstrated.
* [ ]	Validation layers implemented.
* [ ]	Severity model implemented.
* [ ]	L0-L4 profile selection works.
* [ ]	Evidence and reference validation works.
* [ ]	Parent-child validation works.
* [ ]	Dry-run and idempotent migration supported.
* [ ]	Catalogue-level reporting available.
* [ ]	CI integration tested.
* [ ]	No automatic invention of operational facts.
* [ ]	Documentation for contributors and maintainers published.
* [ ]	Pilot can be executed without manual reconstruction of the tooling.

8. Completion definition

EXT-17 is complete when the enrichment toolchain can validate, generate, migrate and report on a controlled set of process entities and is ready to support the pilot.

::

CR-BP-94-EXT-18 : Operational Documentation Pilot

Proposed file: change-requests/CR-BP-94-EXT-18-operational-documentation-pilot.md
Type: Pilot, validation and implementation readiness
Priority: Critical
Depends on: EXT-10 through EXT-17
Enables: EXT-19 and subsequent catalogue-wide backfill

1. Purpose

Execute a controlled pilot to validate the operational documentation model, authoring methodology, evidence framework and tooling before large-scale catalogue enrichment.

The pilot must test the entire process from research through canonical entity update, generated README, validation and review.

2. Objectives

1. Validate the model against real catalogue entities.
2. Test whether the L0-L4 profiles are practical.
3. Validate evidence and provenance requirements.
4. Assess the usability of the authoring methodology.
5. Validate tooling and CI integration.
6. Identify schema or semantic defects before bulk backfill.
7. Establish a measurable quality baseline.
8. Produce a formal go/no-go recommendation for EXT-19.

3. Pilot selection

The pilot shall use representative entities selected from the actual repository after inventory.

The selection must cover, where available:

* At least one L2 Business Process.
* Its relevant L3 Activities.
* At least one L4 Task under a selected Activity.
* Relevant L0/L1 context or grouping records.
* At least one entity with strong existing documentation.
* At least one entity with incomplete or uncertain operational information.
* At least one entity with meaningful cross-catalogue references.

The pilot must not select only the easiest or best-documented entities.

Exact entity identifiers shall be recorded in the pilot plan after repository inspection.

4. Pilot execution

Phase 1 : Baseline

Record the pre-pilot state:

* Existing entity content.
* README state.
* Schema conformance.
* Profile completeness.
* Evidence coverage.
* Cross-reference validity.
* Existing CI findings.

Phase 2 : Research and enrichment

Apply the EXT-16 methodology.

Capture source material and provenance according to EXT-15.

Do not use inferred or AI-generated content as verified operational fact.

Phase 3 : Canonical updates

Update entity data using the approved EXT-10 schema and EXT-11 profile.

Preserve existing identifiers and relationships.

Phase 4 : Documentation generation

Generate the corresponding READMEs using EXT-17 tooling.

Review the generated documentation against the canonical source.

Phase 5 : Validation

Run all applicable validation layers.

Record errors, warnings, deferred items and unresolved questions.

Phase 6 : Human review

Obtain review from appropriately qualified domain reviewers and process owners where required.

Record approval and unresolved issues.

Phase 7 : Pilot assessment

Evaluate the results and identify defects requiring remediation.

5. Pilot quality dimensions

The pilot shall assess:

Dimension	Evaluation question
Semantic integrity	Are operational concepts represented correctly?
Evidence quality	Can material assertions be traced to credible sources?
Decomposition integrity	Does each entity describe the correct level of work?
Parent-child consistency	Do L3 and L4 entities align with their parent context?
Cross-catalogue integrity	Are related entities referenced correctly?
Documentation quality	Is the generated README accurate and useful?
Tooling reliability	Are validation and generation repeatable?
Contributor usability	Can contributors follow the methodology without ambiguity?
Governance	Are review and approval responsibilities clear?
Maintainability	Can the content be updated without duplication or fragile manual work?

6. Mandatory pilot outcomes

The pilot shall produce:

1. A list of pilot entities and their pre-pilot state.
2. Enriched canonical entity records.
3. Generated README documentation.
4. Validation reports.
5. Evidence and provenance records.
6. Review and approval records.
7. A defect and remediation register.
8. A measurement of enrichment effort and recurring bottlenecks.
9. Recommended changes to schema, profiles, methodology or tooling.
10. A formal go/no-go recommendation.

7. Go/no-go criteria

A go decision requires:

* No unresolved critical schema defects.
* No known systematic semantic ambiguity.
* No material unsupported operational assertions presented as verified.
* Successful README generation.
* Successful validation of the pilot’s accepted entities.
* Parent-child relationships reconciled for the pilot scope.
* Evidence and provenance traceability demonstrated.
* Human review completed where required.
* Tooling sufficiently reliable for controlled batch execution.
* Any residual issues documented with approved dispositions.

A failed pilot shall trigger corrective CRs or revisions to the preceding CRs. It must not be treated as permission to proceed with bulk backfill regardless.

8. Acceptance criteria

* [ ]	Pilot entities selected and justified.
* [ ]	Baseline recorded.
* [ ]	EXT-16 methodology applied.
* [ ]	EXT-15 evidence model applied.
* [ ]	Canonical entity data updated.
* [ ]	READMEs generated from canonical data.
* [ ]	All validation layers executed.
* [ ]	Review and approval records captured.
* [ ]	Defects and remediation actions documented.
* [ ]	Pilot effort and quality metrics recorded.
* [ ]	Go/no-go decision approved.
* [ ]	Required upstream corrections identified and assigned.

9. Completion definition

EXT-18 is complete only when the pilot has been evaluated and a formal decision authorizes, restricts or rejects progression to L2 backfill.

::

CR-BP-94-EXT-19 : L2 Business Process Operational Documentation Backfill

Proposed file: change-requests/CR-BP-94-EXT-19-l2-business-process-operational-documentation-backfill.md
Type: Catalogue enrichment and data quality
Priority: Critical
Depends on: EXT-15, EXT-16, EXT-17, EXT-18
Enables: EXT-20 and subsequent L3/L4 enrichment

1. Purpose

Enrich the L2 Business Process catalogue with evidence-supported operational documentation using the approved schema, profiles, authoring methodology and tooling.

L2 is the principal level at which the catalogue describes a complete business transformation. It must therefore be sufficiently coherent before its child activities are enriched at scale.

2. Objectives

1. Establish a consistent operational description for every in-scope L2 process.
2. Document the business transformation and its boundaries.
3. Identify supported inputs, outputs and relevant interfaces.
4. Establish process ownership, responsibility and accountability where evidence permits.
5. Identify relevant rules, controls and exceptions.
6. Capture provenance, confidence and verification status.
7. Establish a reliable parent context for L3 Activity enrichment.
8. Avoid unsupported completeness claims.

3. Scope

All L2 Business Process entities in the repository’s approved backfill scope.

The scope must be established from an actual repository inventory. The CR must not assume that every entity in the repository is ready for immediate enrichment.

Out of scope:

* Rewriting the business process taxonomy without a separate approved change.
* Inventing standard operating procedures.
* Creating L3 or L4 entities solely to make a process appear complete.
* Replacing Business Function or Business Capability definitions.
* Replacing the authoritative policy, risk, control or system catalogues.

4. Required L2 operational content

Each L2 entity shall be assessed against its approved profile.

The enrichment shall address the following concepts where applicable and supported by evidence:

4.1 Identity and business purpose

* Process purpose.
* Business need or value contribution.
* Scope.
* Boundary.
* Inclusion and exclusion criteria.
* Relevant parent L1 grouping.
* Relevant L3 decomposition.

4.2 Operational transformation

Describe what business-relevant change, assessment, decision, service or result the process produces.

The transformation description must not merely restate the process name or list its activities.

4.3 Trigger and preconditions

Identify the event or condition that initiates the process where known.

Distinguish initiation from the conditions required for the process to proceed.

4.4 Inputs

Identify information, requests, materials or other business objects entering the process.

Where applicable, document source, description, acceptance criteria and validation expectations.

Do not conflate inputs with resources or systems used to perform the work.

4.5 Outputs and outcomes

Identify the outputs produced by the process and their relevant consumers.

Distinguish deliverables from the wider business outcomes they contribute to.

4.6 Interfaces and dependencies

Identify relevant business interfaces and dependencies.

Where supported, link to canonical Business Functions, Business Capabilities, Information Systems and Information Systems Functions.

Do not create duplicate system or function definitions inside the process catalogue.

4.7 Responsibility and accountability

Identify process ownership, responsible roles, accountable authority and decision authority where applicable.

Organisational units, roles and actors must remain semantically distinct.

4.8 Rules, controls and exceptions

Identify relevant business rules, controls and recognized exceptions.

Reference canonical policy, risk, control and compliance entities where available.

Do not duplicate the authoritative definition of those entities.

4.9 Measures

Where a process measure is already defined or can be validly referenced, link to the canonical Metric entity.

Do not create arbitrary performance targets or duplicate Metric definitions within the process record.

4.10 Evidence and confidence

Apply EXT-15 to material assertions.

Unverified and unresolved information must be represented explicitly.

5. Backfill execution model

Stage 1 : Inventory

* Enumerate L2 entities.
* Record current profile completeness.
* Identify existing README content.
* Identify parent and child relationships.
* Identify existing cross-catalogue references.
* Identify entities requiring priority attention.

Stage 2 : Prioritisation

Prioritise using a documented method considering:

* Business criticality, where established.
* Existing evidence availability.
* Dependency on the process for L3/L4 enrichment.
* Existing documentation gaps.
* Catalogue coverage and representativeness.
* Known owner availability.

Do not equate prioritisation with approval or completeness.

Stage 3 : Enrichment

Apply the approved research and authoring methodology.

Update canonical entity data, not just README files.

Stage 4 : Validation

Execute schema, profile, semantic, evidence, reference and hierarchy validation.

Stage 5 : Review

Obtain the required domain and process owner reviews.

Stage 6 : Documentation generation

Generate the README from canonical entity data.

Stage 7 : Reporting

Update the catalogue-level backfill report.

6. Acceptance criteria

* [ ]	Complete L2 inventory produced.
* [ ]	Every in-scope L2 entity assessed against the approved profile.
* [ ]	Business purpose and transformation documented where evidence permits.
* [ ]	Boundaries and scope reconciled.
* [ ]	Inputs and outputs assessed.
* [ ]	Triggers and preconditions assessed.
* [ ]	Interfaces and dependencies assessed.
* [ ]	Responsibility and accountability assessed.
* [ ]	Rules, controls and exceptions assessed.
* [ ]	Relevant metrics referenced canonically where available.
* [ ]	Provenance and confidence recorded.
* [ ]	Unknown and deferred items explicitly classified.
* [ ]	L2 parent-child decomposition reconciled.
* [ ]	READMEs generated from canonical entity data.
* [ ]	Validation results recorded.
* [ ]	Required reviews completed.
* [ ]	Outstanding issues have explicit dispositions.
* [ ]	Catalogue-level L2 report published.

An entity may be accepted as enriched with documented gaps where its applicable profile permits this. The programme must not manufacture information to achieve a nominal 100% completion score.

7. Completion definition

EXT-19 is complete when every in-scope L2 entity has been assessed, enriched to its approved and evidence-supported level, validated, reviewed as required and included in the catalogue-level backfill report.

::

CR-BP-94-EXT-20 : L3 Activity Operational Documentation Backfill

Proposed file: change-requests/CR-BP-94-EXT-20-l3-activity-operational-documentation-backfill.md
Type: Catalogue enrichment and decomposition integrity
Priority: High
Depends on: EXT-15, EXT-16, EXT-17, EXT-18, EXT-19
Enables: EXT-21 L4 Task backfill and EXT-22 L0/L1 reconciliation

1. Purpose

Enrich the L3 Activity catalogue with evidence-supported operational descriptions that are consistent with their parent L2 Business Processes.

The purpose is to describe cohesive bodies of work that contribute to the business transformation represented by the parent process.

L3 must provide a meaningful decomposition of the process without becoming a procedural workflow specification.

2. Objectives

1. Document the purpose and contribution of each in-scope Activity.
2. Establish clear parent L2 relationships.
3. Identify relevant work inputs and outputs.
4. Describe the activity’s operational responsibility and relevant controls.
5. Identify dependencies and interfaces where supported.
6. Preserve a coherent decomposition of the parent process.
7. Prepare the activity layer for L4 Task enrichment.
8. Prevent activity descriptions from duplicating the parent process or prematurely describing task execution.

3. Scope

All L3 Activity entities within the approved backfill scope.

The scope must be established by repository inventory and reconciliation with the L2 entities accepted under EXT-19.

Out of scope:

* Replacing the L2 business transformation description.
* Defining detailed L4 task execution.
* Introducing workflow sequencing, branching or orchestration.
* Inventing activity-level controls or roles.
* Creating new parent processes to accommodate an existing activity without an approved taxonomy change.

4. Required L3 operational content

Each Activity shall be assessed against the L3 profile.

4.1 Identity and purpose

Document:

* Activity name.
* Activity purpose.
* Parent L2 Business Process.
* Business contribution.
* Scope and boundaries.
* Relevant child L4 Tasks, where they exist.

The activity purpose must describe a cohesive body of work, not simply repeat its title.

4.2 Contribution to the parent process

Describe how the activity contributes to the transformation, outputs or outcomes of its parent L2 process.

The activity must have a defensible relationship to the parent process.

An activity that cannot be linked to the parent’s business transformation should be reviewed for misclassification, missing context or incorrect hierarchy.

4.3 Inputs and working objects

Identify relevant inputs, information or business objects used or transformed by the activity.

Distinguish these from resources, applications and infrastructure.

Where an input is inherited conceptually from the parent process, record the relationship and avoid unnecessary duplication.

4.4 Outputs and contribution

Describe relevant outputs produced by the activity.

Distinguish an activity’s immediate output from the final output or outcome of the parent L2 process.

4.5 Responsibility

Identify the relevant roles, performers, responsible parties or decision authorities where evidence permits.

Use the canonical responsibility and accountability model from EXT-13.

Do not create activity-specific interpretations of organizational roles.

4.6 Rules and controls

Identify applicable business rules and controls.

Where a control applies at the parent process level, determine whether the activity is genuinely within its scope before referencing it.

Do not duplicate the authoritative rule or control definition.

4.7 Exceptions and dependencies

Document relevant exceptions and dependencies where they are material and supported by evidence.

A dependency must not be represented as a parent-child relationship unless it is genuinely part of the decomposition hierarchy.

4.8 Evidence and provenance

Apply EXT-15.

Assertions must be traceable to appropriate evidence, with confidence and verification status recorded.

5. Parent-child reconciliation

This CR shall establish an explicit reconciliation between L2 processes and their L3 Activities.

For each parent L2:

* Identify all associated L3 Activities.
* Confirm each activity contributes to the parent’s business purpose.
* Identify gaps where expected work is not represented.
* Identify apparent duplication.
* Identify activities assigned to the wrong parent.
* Identify activities with ambiguous scope.
* Record unresolved decomposition decisions.

The reconciliation process must not create new activities automatically.

Any structural changes to the process taxonomy must be handled through the appropriate approved change process.

6. Activity cohesion and decomposition quality

An L3 Activity should:

* Represent a coherent body of work.
* Have a meaningful business purpose.
* Contribute to its parent L2 process.
* Be distinguishable from sibling activities.
* Have a sufficiently clear boundary.
* Be capable of being decomposed into L4 Tasks where such decomposition is appropriate.

An activity should not merely be:

* A department name.
* A job title.
* A system name.
* A single vague verb.
* A duplicate of its parent process.
* An arbitrary grouping of unrelated tasks.

The catalogue must not require every Activity to have a predetermined number of Tasks.

7. Backfill execution model

Stage 1 : Inventory

Enumerate all L3 entities and their parent L2 relationships.

Stage 2 : Parent readiness

Confirm that the relevant parent L2 has passed the EXT-19 acceptance requirements or has an explicitly approved exception.

Stage 3 : Reconciliation

Assess the completeness and coherence of the activity decomposition against the parent process.

Stage 4 : Enrichment

Research and update canonical L3 entity data using EXT-16.

Stage 5 : Evidence and validation

Apply EXT-15 and run EXT-17 validation.

Stage 6 : Review

Obtain appropriate activity-level and process-owner review.

Stage 7 : Documentation generation

Generate the Activity README from canonical entity data.

Stage 8 : Reporting

Update the L3 catalogue backfill and parent-child reconciliation reports.

8. Acceptance criteria

* [ ]	Complete L3 inventory produced.
* [ ]	Every in-scope Activity has a valid parent L2 relationship.
* [ ]	Parent L2 readiness confirmed or an approved exception recorded.
* [ ]	Activity purpose documented where evidence permits.
* [ ]	Activity scope and boundaries assessed.
* [ ]	Contribution to parent transformation established.
* [ ]	Inputs and outputs assessed.
* [ ]	Responsibility and accountability assessed.
* [ ]	Rules, controls and exceptions assessed.
* [ ]	Relevant dependencies and interfaces assessed.
* [ ]	Evidence and provenance recorded.
* [ ]	Unverified and deferred information explicitly classified.
* [ ]	Activity cohesion and sibling differentiation assessed.
* [ ]	Parent-child reconciliation completed.
* [ ]	READMEs generated from canonical entity data.
* [ ]	Validation and review completed.
* [ ]	Outstanding decomposition issues documented.
* [ ]	Catalogue-level L3 report published.

9. Completion definition

EXT-20 is complete when all in-scope L3 Activities have been assessed, enriched to their evidence-supported profile, reconciled with their L2 parents, validated and reviewed as required.

::

Programme-level sequencing and controls

1. Dependency sequence

The six CRs should be executed in the following order:

Sequence	CR	Exit gate
1	EXT-15	Evidence, provenance and confidence model approved and implemented
2	EXT-16	Authoring and research methodology published
3	EXT-17	Tooling and validation pipeline operational
4	EXT-18	Pilot passes and formal go/no-go decision issued
5	EXT-19	L2 backfill completed or formally dispositioned
6	EXT-20	L3 backfill completed or formally dispositioned

2. Dependency diagram

flowchart TD
    A[EXT-10 Schema Alignment] --> B[EXT-11 Documentation Profiles]
    B --> C[EXT-12 Inputs Outputs Interfaces]
    B --> D[EXT-13 Responsibility and Accountability]
    B --> E[EXT-14 Rules Controls Exceptions]
    C --> F[EXT-15 Evidence and Provenance]
    D --> F
    E --> F
    F --> G[EXT-16 Authoring and Research Methodology]
    G --> H[EXT-17 Enrichment Tooling]
    H --> I[EXT-18 Operational Pilot]
    I --> J{Pilot approved?}
    J -->|Go| K[EXT-19 L2 Backfill]
    J -->|No-go| R[Remediation of upstream CRs]
    K --> L[EXT-20 L3 Backfill]
    L --> M[EXT-21 L4 Task Backfill]
    M --> N[EXT-22 L0/L1 Context Reconciliation]
    N --> O[EXT-23 Conformance Gates]
    O --> P[EXT-24 Catalogue Closure and Governance]

3. Programme-wide non-negotiable controls

1. Canonical data first: Operational facts belong in canonical entity data, not independently maintained README prose.
2. Evidence before assertion: Unsupported assertions must remain unverified or be excluded.
3. L2 before L3 and L4: Child-level enrichment must be grounded in a coherent parent process.
4. No forced completeness: A documented unknown is better than invented operational content.
5. No workflow-engine drift: L3 and L4 documentation must not evolve into runtime orchestration definitions.
6. Canonical cross-catalogue references: Do not duplicate Business Function, Business Capability, Information System, Information Systems Function, Metric, Policy or Control entities.
7. Human accountability: AI may assist research and authoring, but cannot establish organisational authority or approve operational facts.
8. Incremental CI enforcement: Introduce blocking rules in line with approved migration gates, not by invalidating the entire existing catalogue prematurely.
9. Reproducible backfill: Every batch must be reviewable, repeatable and reportable.
10. Explicit disposition: Every unresolved issue must have an owner, status or documented reason for deferral.

4. Next logical CRs after EXT-20

The sequence should continue with:

* CR-BP-94-EXT-21 : L4 Task Operational Documentation Backfill: Complete bounded task-level documentation, expected results, completion conditions and verification evidence without introducing workflow runtime semantics.
* CR-BP-94-EXT-22 : L0/L1 Context and Process Group Reconciliation: Reconcile scope, grouping, membership and hierarchy against the enriched L2-L4 catalogue.
* CR-BP-94-EXT-23 : Operational Documentation Conformance Gates: Introduce progressive CI enforcement and catalogue-wide conformance reporting.
* CR-BP-94-EXT-24 : Catalogue Closure and Continuous Governance: Establish ongoing ownership, periodic review, change management and programme closure.

Programme decision: Do not commence full L2 backfill until EXT-15 through EXT-18 have passed their respective gates. Do not commence broad L3 backfill until the relevant L2 parent processes have been accepted under EXT-19.

Recommended execution order

I would treat EXT-15 to EXT-18 as the engineering and governance readiness tranche, and EXT-19 to EXT-20 as the first catalogue enrichment tranche.

One important control is that EXT-19 and EXT-20 should not be interpreted as requiring every entity to reach an artificially complete state. Each entity should instead receive a defensible disposition: enriched and verified, enriched with declared gaps, awaiting evidence, awaiting owner review, or structurally requiring remediation.

This gives the programme measurable progress without compromising the integrity of the catalogue.

Next step: I recommend producing EXT-21 through EXT-24 next, completing the CR-BP-94 operational documentation programme before treating the entire sequence as a formally approved implementation baseline.