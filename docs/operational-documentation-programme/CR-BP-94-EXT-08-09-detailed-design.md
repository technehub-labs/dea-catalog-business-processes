<!--
Source: User submission "CR-BP-94-EXT-8_and_9.md" (detailed design for CR-BP-94-EXT-08 and CR-BP-94-EXT-09).
The user supplied this as a single file with both CRs in sequence plus a preamble explaining the rationale. The preamble captures the user's reasoning for the CR architecture and the correction to the existing roadmap.
Preserved here for traceability. The two CRs have been split into separate files:
- change-requests/CR-BP-94-EXT-08-documentation-roadmap-reconciliation.md
- change-requests/CR-BP-94-EXT-09-operational-documentation-semantic-contract.md
D-004 cleanup applied: em-dashes, en-dashes, and three-em-dashes (U+2E3B) replaced with colons, hyphens, and "---" respectively.
-->

The two documents will be CR-BP-94-EXT-08 and CR-BP-94-EXT-09, continuing the existing documentation extension series.

The current repository reveals an important issue that these CRs must resolve before any backfill begins: EXT-04 already exists as the Generation and Validation Pipeline, while the generated READMEs still say operational details are pending backfill at EXT-04. The current L2 profile also already recognises curated inputs/outputs, roles, rules and controls, and the Business Process template has optional operational fields. So the work must reconcile the documentation roadmap and the existing model, not introduce a duplicate operational-data structure.

I have also confirmed the distinction between the two kinds of deferred work:

* L2-L4 operational documentation: the README template expects curated business meaning, but the existing generator cannot safely invent it. This belongs in the content-authoring and rollout work, principally EXT-06, after the model and authoring contract are agreed.
* L0 metrics and cell-charter details: EXT-07 and EXT-04 explicitly define placeholders and validation findings for these. They need their own treatment and must not be conflated with L2 process inputs, outputs, roles or controls.

EXT-08 therefore establishes the authoritative roadmap and disposition of existing work. EXT-09 then establishes the semantic contract that subsequent schema, authoring, tooling and backfill work must follow.

CR-BP-94-EXT-08: Documentation Extension Roadmap Reconciliation and Deferred-Work Disposition

CR-BP-94-EXT-08: Documentation Extension Roadmap Reconciliation and Deferred-Work Disposition

Status: Proposed
Layer: Process Catalog
Owner: Emmanuel A. Otchere
Date: 2026-10-19
Parent: CR-BP-94 (Decomposition Record Templates)
Related CRs: CR-BP-94-EXT-01, CR-BP-94-EXT-01a, CR-BP-94-EXT-02, CR-BP-94-EXT-04, CR-BP-94-EXT-05, CR-BP-94-EXT-06, CR-BP-94-EXT-07
Sub-pipeline position: First reconciliation slice following EXT-07 and the existing EXT-04 proposal
Target repository: technehub-labs/dea-catalog-business-processes
Proposed path: change-requests/CR-BP-94-EXT-08-documentation-roadmap-reconciliation.md

---

1. Executive Summary

This Change Request reconciles the CR-BP-94 documentation extension programme into one authoritative, dependency-aware implementation roadmap.

The documentation extension series has evolved through several architectural and implementation proposals. The current repository contains multiple generations of documentation profiles, README generators, validation requirements, and backfill references. These are not yet expressed as one consistent and unambiguous delivery sequence.

A material inconsistency exists in the generated entity READMEs:

Operational Details fields are described as pending backfill at EXT-04.

However, EXT-04 is already defined as the Generation and Validation Pipeline. Its stated responsibility is to validate documentation and publish findings. EXT-06 is identified as the pilot and catalogue rollout that reconciles documentation content.

Consequently, the README placeholder creates an incorrect implementation instruction. It directs contributors towards a pipeline-validation CR for work that requires semantic research, authoring, evidence, review, and controlled publication.

This CR establishes the authoritative disposition:

1. EXT-04 is the documentation validation and pipeline workstream. It is not the operational-content backfill workstream.
2. EXT-05 is the decomposition documentation reconciliation workstream.
3. EXT-06 is the pilot, content enrichment, and catalogue rollout workstream.
4. EXT-07 is the consolidated README template and generator workstream.
5. EXT-08 reconciles the programme, its terminology, dependencies, and deferred-work references.
6. EXT-09 establishes the operational documentation semantic contract.
7. Subsequent CRs establish the data model, documentation profiles, evidence methodology, authoring process, automation, pilot, backfill, and conformance closure.

No operational content is to be fabricated merely to remove a placeholder. A record can be incomplete, not applicable, awaiting evidence, or genuinely unknown. These states must remain distinguishable.

2. Problem Statement

2.1 Conflicting extension references

The current extension programme contains the following relevant CRs:

CR	Existing responsibility	Reconciliation required
EXT-01	Documentation architecture	Retain as foundational architecture
EXT-01a	L0/L1 documentation profiles	Retain as cardinal-entity profile extension
EXT-02	README generation pipeline	Treat as historical generator design superseded by EXT-07
EXT-03	Documentation manifest and coverage model	Its implementation status and dependency relationship require explicit reconciliation
EXT-04	Generation and validation pipeline	Retain as validation and pipeline work, not content backfill
EXT-05	Decomposition reconciliation	Retain as parent-child documentation reconciliation
EXT-06	Pilot and catalogue rollout	Make this the controlled operational-content authoring and backfill delivery workstream
EXT-07	README template consolidation and Generator V2	Retain as the current consolidated README structure and generation baseline

The programme must not silently redefine existing CR identifiers or assign an existing identifier to a different scope.

2.2 Incorrect operational backfill instruction

A generated L2 README currently contains statements equivalent to:

## Operational Details
**Inputs / Outputs**: _(pending; backfill at EXT-04)_
**Roles and Responsibilities**: _(pending; backfill at EXT-04)_
**Business Rules and Controls**: _(pending; backfill at EXT-04)_

This is problematic for four reasons:

1. EXT-04 does not own business-content research or approval.
2. The existing YAML model already permits some operational properties.
3. The documentation profile identifies these sections as curated semantic content.
4. A placeholder does not communicate whether the information is unknown, unresearched, not applicable, inherited, or awaiting approval.

The placeholder therefore conflates a missing model value with a missing documentation activity and a missing evidence or approval state.

2.3 Existing model structures must be respected

The current Business Process template already contains optional operational fields, including:

* inputs
* transformation
* outputs
* responsibility
* boundary

The existing L2 documentation profile also identifies inputs, outputs, interfaces, roles, responsibilities, accountability, business rules, and controls as semantic documentation concerns.

EXT-08 must not introduce competing structures or redefine these fields. Their semantics, relationships, cardinality, and authoritative location will be resolved under EXT-09 and subsequent approved CRs.

3. Objectives

This CR SHALL:

1. Establish an authoritative register of the EXT documentation workstream.
2. Resolve conflicting references to EXT-04 and EXT-06.
3. Distinguish documentation generation, structural validation, semantic validation, decomposition reconciliation, and content backfill.
4. Define the dependency order for all remaining documentation work.
5. Establish the disposition of existing placeholders.
6. Identify the repository artefacts requiring correction.
7. Prevent duplicate schemas, fields, validators, and documentation sources of truth.
8. Establish explicit exit criteria before operational-content backfill begins.
9. Ensure the extension programme remains compatible with the current L0-L4 decomposition model and the canonical entity storage layout.

4. Scope

4.1 Included

* Reconciliation of EXT-01 through EXT-07.
* Correction of inaccurate placeholder instructions.
* Definition of the remaining extension roadmap.
* Identification of missing or unverified CR artefacts.
* Reconciliation of EXT-03 dependencies and implementation status.
* Definition of workstream ownership and dependency gates.
* Alignment with the existing generator, profiles, validator, and conformance pipeline.
* Backfill sequencing and readiness requirements.

4.2 Excluded

* Introducing new operational entity concepts.
* Defining the detailed operational semantic model.
* Changing the canonical Process metamodel.
* Adding operational fields to entity schemas.
* Performing catalogue-wide operational-content backfill.
* Rewriting existing READMEs manually.
* Changing L0 metrics semantics.
* Changing the decomposition hierarchy.
* Making advisory documentation findings blocking.

These are governed by subsequent CRs.

5. Normative Programme Decisions

5.1 Canonical source of truth

The canonical entity YAML remains the authoritative source for structured entity facts.

The README is a human-readable documentation projection of the canonical record, supplemented by curated semantic content where the canonical record or an approved documentation asset does not yet express the necessary explanation.

A README MUST NOT become an independent competing source of truth for structured operational properties.

A documentation manifest, where adopted, MUST identify the source and status of curated content and MUST NOT silently override canonical entity values.

5.2 Responsibilities of the existing extension CRs

The following responsibility assignments are authoritative for this programme:

Workstream	Responsibility
EXT-01 / EXT-01a	Documentation architecture and five-level profile coverage
EXT-02	Historical README generator design
EXT-03	Documentation manifest and coverage model; implementation status to be reconciled
EXT-04	Documentation generation/validation pipeline and structural findings
EXT-05	Parent-child documentation and decomposition reconciliation
EXT-06	Pilot, semantic authoring, operational-content backfill, and catalogue rollout
EXT-07	Consolidated README template and Generator V2
EXT-08	Programme reconciliation and roadmap governance
EXT-09	Operational documentation semantic contract

The scope of EXT-04 is not expanded to include manual or AI-assisted business-content research.

5.3 EXT-04 and EXT-06 distinction

EXT-04 SHALL validate the presence and structure of documentation artefacts and publish findings.

EXT-06 SHALL coordinate the content-enrichment process that resolves findings requiring substantive business or operational knowledge.

The distinction is:

Canonical entity YAML
        |
        v
README Generator
        |
        v
Generated README
        |
        v
EXT-04: Structural validation
        |
        v
EXT-05: Decomposition reconciliation
        |
        v
EXT-06: Semantic research and content backfill
        |
        v
Human review and approval
        |
        v
Canonical source update / approved documentation update
        |
        v
README regeneration and conformance validation

This diagram represents programme responsibilities, not an execution sequence that overrides the detailed dependencies of existing CRs.

5.4 Placeholder disposition

The phrase pending; backfill at EXT-04 MUST NOT be used to direct operational-content authoring.

For L1-L4 operational details, the placeholder MUST be replaced through the approved documentation profile and generator design with a status that identifies the actual disposition.

For L0 metrics and cell-charter fields, existing EXT-07 and EXT-04 provisions remain subject to their own reconciliation. This CR does not move L0 metrics into the L2-L4 operational model.

A placeholder MUST never be interpreted as evidence that the field is semantically required for every entity level.

5.5 No automatic semantic inference

The following rules are mandatory:

* An input MUST NOT be inferred merely from a trigger.
* An output MUST NOT be inferred merely from an outcome.
* A resource MUST NOT be classified as an input without semantic justification.
* A role MUST NOT be inferred from a process name or ECF coordinate.
* A control MUST NOT be inferred from a regulatory domain alone.
* A metric MUST NOT be treated as an approved target without governance evidence.
* A system interaction MUST NOT be invented from a process description.
* A parent entity’s content MUST NOT be copied into a child entity without an explicit inheritance relationship and applicability assessment.

6. Authoritative Extension Roadmap

The following roadmap is the programme baseline. Proposed future CRs are not represented as already existing or approved repository artefacts.

Sequence	CR	Title	Primary output
1	EXT-08	Documentation Roadmap Reconciliation	Authoritative programme baseline
2	EXT-09	Operational Documentation Semantic Contract	Normative semantic definitions
3	EXT-10	Operational Entity Schema Alignment	Approved canonical YAML/schema representation
4	EXT-11	Decomposition-Level Documentation Profiles	L0-L4 applicability and requirements
5	EXT-12	Process Inputs, Outputs and Interface Semantics	Interface and transformation semantics
6	EXT-13	Responsibility and Accountability Semantics	Role and accountability model
7	EXT-14	Business Rules, Controls and Exception Semantics	Rule, control and exception model
8	EXT-15	Evidence, Provenance and Confidence Framework	Evidence and assertion lifecycle
9	EXT-16	Operational Authoring and Research Methodology	Repeatable content research method
10	EXT-17	Enrichment Tooling and Backfill Orchestration	Controlled authoring and review tooling
11	EXT-18	Operational Documentation Pilot	Validated representative pilot
12	EXT-19	L2 Business Process Catalogue Backfill	L2 operational enrichment
13	EXT-20	L3 Activity Catalogue Backfill	L3 operational enrichment
14	EXT-21	L4 Task Catalogue Backfill	L4 operational enrichment, when canonical L4 records exist
15	EXT-22	L0/L1 Context and Process Group Documentation Reconciliation	Cardinal-entity documentation
16	EXT-23	Operational Documentation Conformance Gates	Approved conformance enforcement
17	EXT-24	Catalogue Closure and Continuous Governance	Closure evidence and ongoing governance

The EXT-10 through EXT-24 identifiers are proposed programme allocations. Before creating each CR, the repository CR register MUST be checked for collisions and existing commitments.

EXT-03 remains a separate reconciliation item. Its original reserved scope MUST be preserved and its actual implementation status recorded before EXT-04 dependencies are declared complete.

7. Dependency and Readiness Gates

Gate G1: Programme architecture reconciled

Requires:

* EXT-08 approved.
* EXT-01 and EXT-01a retained as the profile architecture baseline.
* EXT-07 identified as the current README structure and generator design.
* EXT-04 and EXT-06 responsibilities unambiguously separated.
* EXT-03 status and dependency implications documented.

Gate G2: Semantic model approved

Requires:

* EXT-09 approved.
* EXT-10 schema alignment approved.
* EXT-11 profile requirements approved.
* No unresolved duplicate operational properties.
* No unapproved changes to canonical metamodel semantics.

Gate G3: Authoring and evidence ready

Requires:

* EXT-12 through EXT-16 approved.
* Evidence and provenance requirements implemented.
* Research and review responsibilities established.
* Level-specific applicability rules documented.

Gate G4: Tooling ready

Requires:

* EXT-17 approved and implemented.
* Existing generator remains deterministic.
* Content changes can be traced to their source and approval.
* Backfill operations are repeatable and auditable.

Gate G5: Pilot approved

Requires:

* EXT-18 completed.
* Pilot records pass semantic review.
* Generator output and structural validation are conformant.
* No unsupported assumptions remain.
* Pilot methodology is repeatable.

Gate G6: Catalogue backfill complete

Requires:

* EXT-19 through EXT-22 completed or explicitly dispositioned.
* Every in-scope record has a documented completeness state.
* Not-applicable and inherited dispositions are justified.
* No placeholder is falsely represented as completed content.

Gate G7: Governance closure

Requires:

* EXT-23 conformance requirements approved and implemented.
* EXT-24 closure evidence published.
* Ownership and review cadence established.

8. Repository Changes

The following repository artefacts are in scope.

Path	Change
docs/process-documentation-architecture.md	Reconcile extension roadmap and references
docs/decomposition-template-guide.md	Correct backfill guidance and clarify operational-content authoring
change-requests/README.md	Add EXT-08 and update programme register
change-requests/CR-BP-94-EXT-08-documentation-roadmap-reconciliation.md	Add this CR
reconciliation/	Add or update a machine-readable extension roadmap/disposition register
scripts/	No generator or validator implementation change required by this CR
templates/	No operational schema extension required by this CR

The reconciliation register SHOULD contain:

* CR identifier.
* Current title.
* Existing repository path.
* Original scope.
* Current disposition.
* Dependencies.
* Superseded artefacts.
* Open decisions.
* Completion evidence.
* Next action.

It MUST distinguish proposed, implemented, merged, superseded, deferred, and closed states according to the repository’s established governance vocabulary.

9. Migration and Compatibility

1. Existing entity YAML records MUST remain valid.
2. Existing README files MUST remain readable.
3. No existing CR identifier may be repurposed.
4. No entity identifier or content-derived hash may be changed solely to correct documentation wording.
5. Generator output changes MUST be deterministic.
6. Historical CR references MUST remain traceable.
7. Any change to generated README wording MUST be reflected in generator tests.
8. Existing advisory findings MUST not be silently deleted or suppressed.

10. Test and Validation Requirements

The implementation of this CR MUST verify:

* All existing CR identifiers remain unique.
* EXT-01 through EXT-07 have one documented disposition each.
* EXT-03 is not treated as completed without implementation evidence.
* EXT-04 does not claim ownership of semantic content backfill.
* EXT-06 explicitly owns content-enrichment and rollout activities.
* No README operational placeholder directs contributors to EXT-04 for content authoring.
* L0 metrics placeholders remain distinct from L1-L4 operational-content placeholders.
* The documentation architecture and decomposition template guide do not contradict the CR register.
* CR metadata checks pass.
* Existing catalogue conformance gates remain conformant.

11. Acceptance Criteria

* AC-01: The extension programme has one authoritative reconciled roadmap.
* AC-02: EXT-01, EXT-01a, EXT-02, EXT-03, EXT-04, EXT-05, EXT-06 and EXT-07 each have an explicit disposition.
* AC-03: EXT-04 is explicitly limited to its generation/validation responsibilities.
* AC-04: EXT-06 explicitly owns the semantic content backfill and catalogue rollout.
* AC-05: The distinction between L0 metrics and L1-L4 operational details is documented.
* AC-06: The phrase pending; backfill at EXT-04 is no longer used as an operational-content implementation instruction.
* AC-07: No duplicate operational data structures are introduced.
* AC-08: EXT-03 implementation status and dependency implications are recorded.
* AC-09: The extension roadmap register is machine-readable or otherwise auditable.
* AC-10: CR metadata validation passes.
* AC-11: Existing entity records, IDs, and decomposition relationships remain unchanged.
* AC-12: The programme is ready to proceed to EXT-09.

12. Risks and Mitigations

Risk	Mitigation
Existing CRs contradict the new roadmap	Preserve historical scope and record explicit dispositions
EXT-03 is assumed complete without evidence	Require implementation verification
EXT-04 absorbs business research responsibilities	Maintain strict validation versus authoring separation
Operational fields are duplicated	Require EXT-09 semantic review before schema changes
README placeholders are removed without content	Replace with explicit completeness dispositions
Backfill becomes uncontrolled mass editing	Require pilot and evidence-based approval
L0 metrics are mixed with process-level metrics	Retain separate level-specific treatment

13. Rollback

This CR is principally a governance and documentation reconciliation.

If implementation introduces regressions:

1. Revert only the affected documentation and roadmap changes.
2. Preserve existing generator and validator behaviour.
3. Restore the prior CR register and documentation architecture if necessary.
4. Do not remove historical CR records or alter entity records.
5. Re-run CR metadata and conformance validation.

14. Completion Definition

EXT-08 is complete when the extension programme has a reconciled, auditable roadmap and the repository no longer directs operational-content backfill to the wrong CR.

EXT-08 does not itself backfill any Business Process, Activity, Task, Process Group, or Process Context.

Its output is the approved governance baseline for EXT-09 and the subsequent operational documentation workstream.

CR-BP-94-EXT-09: Operational Documentation Semantic Contract

CR-BP-94-EXT-09: Operational Documentation Semantic Contract

Status: Proposed
Layer: Process Catalog
Owner: Emmanuel A. Otchere
Date: 2026-10-19
Parent: CR-BP-94 (Decomposition Record Templates)
Programme predecessor: CR-BP-94-EXT-08 (Documentation Roadmap Reconciliation and Deferred-Work Disposition)
Related CRs: CR-BP-93, CR-BP-94, CR-BP-95, CR-BP-96, CR-BP-97, CR-BP-98, CR-BP-99, CR-BP-94-EXT-01, CR-BP-94-EXT-01a, CR-BP-94-EXT-04, CR-BP-94-EXT-05, CR-BP-94-EXT-06, CR-BP-94-EXT-07
Target repository: technehub-labs/dea-catalog-business-processes
Proposed path: change-requests/CR-BP-94-EXT-09-operational-documentation-semantic-contract.md

---

1. Executive Summary

This Change Request establishes the normative semantic contract for operational documentation across the Business Process Catalog.

The purpose is to define what the catalogue means when it documents:

* Inputs.
* Outputs.
* Transformation.
* Triggers and preconditions.
* Interfaces and dependencies.
* Roles and responsibilities.
* Accountability.
* Business rules.
* Controls.
* Exceptions and deviations.
* Evidence and provenance.
* Operational completeness.

The current documentation profiles identify these concerns, and the Business Process template already provides optional operational fields. However, the programme requires a common semantic contract before it can safely expand schemas, enrich entity records, generate documentation, or backfill the catalogue.

This CR establishes the following architectural principle:

Operational documentation describes the semantics of enterprise work. It is not a workflow engine, an organizational chart, an application inventory, or a substitute for the canonical OpenDEA metamodel.

The contract applies across L0-L4, but the applicability and depth of each concern differ by decomposition level.

The contract also establishes a strict separation between:

1. Canonical entity facts.
2. Curated operational assertions.
3. Evidence supporting those assertions.
4. Documentation generated from the canonical model.
5. Documentation completeness and approval status.

The CR does not immediately add new fields to the entity schema. That is the responsibility of EXT-10 after the semantic model is agreed.

2. Problem Statement

The current documentation model identifies inputs, outputs, roles, responsibilities, controls, and other operational concerns as documentation sections. The canonical Business Process template also contains optional properties for inputs, transformation, outputs, responsibility, and boundary.

Without a normative semantic contract, several inconsistencies are possible:

* An outcome may be incorrectly treated as an output.
* A resource may be incorrectly treated as an input.
* A trigger may be confused with a precondition.
* A role may be confused with a Business Function or organizational unit.
* A business rule may be confused with a control.
* A control may be confused with evidence of control operation.
* An exception may be confused with an ordinary workflow branch.
* An Activity may be documented as an independent Business Process.
* A Task may be expanded into an execution workflow.
* Inherited information may be copied without confirming its applicability.

These inconsistencies would make catalogue-wide backfill unreliable and undermine the value of the resulting operational documentation.

3. Objectives

This CR SHALL:

1. Define the semantics of operational documentation concepts.
2. Define their relationships and boundaries.
3. Establish applicability by decomposition level.
4. Define the distinction between model-derived and curated content.
5. Establish the minimum semantic quality expected for each operational assertion.
6. Define how unknown, pending, inherited, not-applicable, and approved information is represented.
7. Define the rules for evidence and provenance.
8. Prevent the creation of duplicate concepts already governed by the OpenDEA metamodel.
9. Provide the semantic foundation for EXT-10 through EXT-17.
10. Establish a consistent basis for EXT-18 pilot and EXT-19 onwards backfill.

4. Architectural Principles

4.1 Model-first principle

Canonical YAML is the authoritative representation of structured entity facts.

Where an operational assertion is approved as a canonical entity property, it MUST be stored in the appropriate canonical YAML structure and validated against its schema.

Where an assertion is explanatory or evidence-oriented and does not belong in the entity schema, it MAY be maintained in an approved documentation asset or manifest.

A README MUST NOT become a competing structured-data repository.

4.2 Semantic non-equivalence

The concepts defined in this CR are distinct. They MUST NOT be substituted for one another merely because they are related in an operational narrative.

4.3 Evidence-based authoring

A field MUST NOT be populated simply because its presence makes a README appear complete.

An assertion must be supported by one or more of:

* Canonical entity data.
* Approved enterprise policy or procedure.
* Approved process documentation.
* Regulatory or contractual source.
* Verified system or interface documentation.
* Interview or workshop evidence reviewed by an accountable subject-matter expert.
* Other traceable evidence approved under the evidence framework.

4.4 Decomposition-aware semantics

The same operational concept may be applicable at multiple decomposition levels, but the expected semantic depth differs.

An L2 Business Process describes an independently meaningful transformation.

An L3 Activity describes a cohesive body of work within that process.

An L4 Task describes a bounded, actionable, independently verifiable unit of work.

L0 Process Scope and L1 Process Group are architectural organization constructs and MUST NOT be documented as executable transformations.

4.5 No implicit workflow semantics

The presence of inputs, outputs, relationships, responsibilities, or dependencies does not establish execution sequence.

Sequencing, branching, orchestration, workflow instances, and execution events remain outside the semantic scope of the Task entity and belong to their separately governed workflow constructs.

5. Normative Semantic Definitions

5.1 Trigger

A Trigger is the event, condition, or recognized business circumstance that causes a Business Process or other applicable unit of work to be invoked.

A trigger answers:

What causes this unit of work to be initiated?

A trigger is not necessarily an input. A trigger may cause work to begin without itself being transformed.

Examples:

* A customer submits a service request.
* A policy review date is reached.
* A new product proposal is approved for assessment.
* A financial reporting period closes.

A trigger MUST describe an invocation condition, not merely restate the process purpose.

5.2 Preconditions

A Precondition is a condition that must hold before a particular unit of work can validly begin or proceed.

A precondition answers:

What must already be true for this work to be validly performed?

Examples:

* A customer account exists.
* A required authorization has been granted.
* A source record has passed validation.
* A required regulatory approval is in force.

A precondition is not automatically a trigger. It may be satisfied long before the process is invoked.

5.3 Inputs

An Input is an information object, business object, decision, request, material, or other defined item that is consumed, assessed, transformed, or used by the process in producing its outputs.

An input answers:

What does the process receive or use as part of its transformation?

Each documented input SHOULD identify:

* Stable local identifier.
* Name.
* Description.
* Source or origin.
* Input type or classification, where useful.
* Required or optional status, where established.
* Validation or acceptance criteria, where applicable.
* Evidence or provenance.

An input MUST NOT be used as a generic label for every resource needed by the process.

Distinctions:

Concept	Meaning
Input	Item entering or used in the transformation
Resource	Means required to perform the work
Trigger	Invocation condition
Precondition	Condition that must already hold
Dependency	Another entity, service, or condition on which the work relies

A system, employee, facility, or budget is ordinarily a resource or dependency, not an input.

5.4 Transformation

A Transformation is the substantive conversion, assessment, decision, combination, validation, or other change through which inputs and relevant resources produce outputs.

A transformation answers:

What does the process actually do to produce its result?

The transformation MUST describe the business semantics of the work, not merely name a system operation or reproduce a sequence of tasks.

Examples:

* Evaluate an investment proposal against approved strategic and financial criteria.
* Validate a customer request against eligibility and contractual requirements.
* Consolidate financial transactions into a reconciled reporting position.

Transformation is not synonymous with workflow sequence.

5.5 Outputs

An Output is a result, artefact, information object, decision, service result, or changed business object produced by the transformation.

An output answers:

What does the work produce?

Each output SHOULD identify:

* Stable local identifier.
* Name.
* Description.
* Consumer or destination.
* Output type, where useful.
* Acceptance or quality criteria, where established.
* Evidence or provenance.

An output MUST be distinguishable from an outcome.

5.6 Outcomes

An Outcome is the meaningful state, effect, or result achieved through the use or consumption of outputs.

An outcome answers:

What meaningful result is achieved because the output is used?

For example:

* Output: An approved customer credit decision.
* Outcome: The customer’s credit eligibility is determined and an authorized offer can be made.

The existence of an output does not prove that the intended outcome has been achieved.

5.7 Consumers

A Consumer is the entity, role, process, service, or external party that receives or uses an output.

A consumer answers:

Who or what uses the output?

A consumer MUST NOT be assumed to be the same as the output’s immediate recipient or system destination where those are different.

5.8 Interfaces

An Interface is a defined point of interaction through which an entity exchanges information, materials, decisions, services, or other operational objects with another entity.

An interface answers:

Where and how does this entity interact with another entity or boundary?

An interface may be human, organizational, procedural, contractual, physical, or system-mediated.

A system interface is a specialization of an interface, not the definition of all interfaces.

5.9 Dependencies

A Dependency is an entity, capability, service, resource, decision, condition, or external arrangement whose availability or state materially affects the performance or result of the documented work.

A dependency answers:

What must this entity rely on to perform or complete its work?

Dependencies MUST be distinguished from structural decomposition relationships.

A dependency MUST NOT be represented as composes unless it is genuinely a structural part-of relationship under the canonical metamodel semantics.

6. Roles, Responsibility and Accountability

6.1 Role

A Role is a defined responsibility-bearing position or function performed by an actor in relation to a unit of work.

A role answers:

What responsibility-bearing part does an actor perform?

A role may be performed by:

* An individual.
* A team.
* An organizational unit.
* An authorized agent.
* A software agent, where explicitly recognized and governed.

A role is not automatically an organizational unit, job title, Business Function, Business Capability, or actor entity.

6.2 Responsibility

Responsibility identifies the role, capability, or accountable operational arrangement that is charged with ensuring that specified work is performed.

Responsibility answers:

Who is responsible for ensuring this work is performed?

The existing Business Process responsibility property MUST be preserved pending an explicit schema and metamodel alignment decision.

This CR does not authorize replacing it with a new role hierarchy.

6.3 Accountability

Accountability identifies the authority or party answerable for the result, decision, or compliance obligation.

Accountability answers:

Who is answerable for the result or decision?

Responsibility and accountability may be assigned to the same party, but they are not semantically identical.

6.4 Performer

A Performer is the actor that actually carries out a specified unit of work.

A performer answers:

Who or what executes the work?

A performer may differ from the accountable party.

6.5 Organizational and enterprise concept boundaries

The documentation MUST preserve these distinctions:

Concept	Concern
Business Function	Organizational grouping of business responsibilities and capabilities
Business Capability	What the enterprise is able to do
Business Process	What coherent work is performed
Process Group	How related processes are organized
Role	What responsibility-bearing part is performed
Actor	Who or what performs an action
Organizational Unit	Formal organizational structure
Responsibility	Who is charged with ensuring work is performed
Accountability	Who is answerable for the result

Cross-references MUST use canonical entity relationships where available. They MUST NOT be represented as containment merely to make the README appear structurally complete.

7. Business Rules, Controls and Exceptions

7.1 Business Rule

A Business Rule is an authoritative constraint, policy, decision criterion, or condition that governs business behaviour or determines whether an action or result is valid.

A business rule answers:

What must, must not, or may happen under defined business conditions?

Examples:

* A customer must satisfy defined eligibility conditions before approval.
* A transaction must be reconciled before it is included in a reporting position.
* An authorization must be granted by an appropriately delegated authority.

A business rule is not automatically a control.

7.2 Control

A Control is a defined mechanism, activity, or arrangement designed to prevent, detect, correct, or otherwise manage a specified risk, error, or non-compliance condition.

A control answers:

What mechanism ensures that a relevant requirement or risk condition is managed?

A control SHOULD identify:

* Control identifier.
* Control objective.
* Risk or obligation addressed.
* Control activity or mechanism.
* Control owner or accountable role.
* Frequency or triggering condition, where applicable.
* Evidence of operation.
* Failure or escalation response.
* Source of authority.

A control MUST NOT be inferred solely from a business rule.

7.3 Control evidence

Control Evidence is the traceable record demonstrating that a control was designed, performed, reviewed, or operated.

Control evidence answers:

What demonstrates that the control exists or operated?

A policy document may demonstrate control design but does not necessarily demonstrate operational execution.

7.4 Exception

An Exception is a recognized condition in which normal requirements, acceptance criteria, or expected operating conditions cannot be met or are intentionally varied.

An exception answers:

What happens when normal conditions or requirements are not satisfied?

An exception record SHOULD identify:

* Triggering condition.
* Nature of deviation.
* Permitted or prohibited disposition.
* Required authority.
* Escalation path.
* Required evidence.
* Closure criteria.

7.5 Deviation

A Deviation is an observed departure from an approved requirement, process condition, rule, or control.

An exception may be authorized in advance. A deviation may be discovered after the departure has occurred.

The terms MUST NOT be treated as synonyms.

8. Metrics and Performance

A Metric is a defined measure used to quantify an observable property, state, event, or result.

A metric answers:

What is being measured, and how is it quantified?

A metric is not automatically a KPI, KRI, KCI, target, or objective.

These distinctions MUST be preserved:

Concept	Meaning
Metric	Defined quantitative or qualitative measure
KPI	Metric adopted to assess performance against an objective
KRI	Metric adopted to monitor exposure to risk
KCI	Metric adopted to assess control or compliance effectiveness
Target	Approved desired value or range
Threshold	Value that triggers attention or action
Actual	Observed measurement
Frequency	Measurement or reporting interval

The existing EXT-07 L0 metrics block is not to be generalized automatically to L1-L4.

Any cross-level metric model must be separately governed and aligned with the canonical OpenDEA Metric concept and the relevant catalogue/metamodel work.

No target, threshold, or performance commitment may be represented as approved without evidence of governance adoption.

9. Evidence, Provenance and Confidence

9.1 Assertion

An Assertion is a documented statement about an entity, its behaviour, its operational semantics, or its relationships.

Every curated operational assertion MUST be traceable to its source or explicitly classified as an assumption awaiting validation.

9.2 Evidence

Evidence is a source or artefact that supports, qualifies, challenges, or establishes an assertion.

Evidence types MAY include:

* Canonical model.
* Approved policy.
* Procedure.
* Contract.
* Regulation.
* System documentation.
* Operational record.
* Interview.
* Workshop outcome.
* Expert review.
* External standard.

9.3 Provenance

Provenance identifies where an assertion originated, who supplied or reviewed it, and how it entered the canonical catalogue.

Provenance MUST be retained when content is updated, inherited, or superseded.

9.4 Confidence

Confidence describes the degree to which an assertion has been verified and supported by evidence.

Confidence MUST NOT be used as a substitute for approval status.

A highly plausible assertion is not necessarily an approved business fact.

9.5 Assumptions

An assumption MUST:

* Be explicitly marked.
* Identify the reason it is necessary.
* Identify its source or rationale.
* Identify who must validate it.
* Have a review or expiry condition where appropriate.

An assumption MUST NOT be rendered as an established fact.

10. Completeness and Information Lifecycle

Every applicable operational documentation concern MUST have an explicit disposition.

The following states are normative:

State	Meaning
not_started	No assessment or authoring has been performed
research_required	The subject requires investigation
in_progress	Authoring or validation is underway
pending_evidence	A proposed assertion lacks sufficient supporting evidence
pending_review	Content is ready for accountable review
approved	Content has passed the required review
inherited	Content is supplied by an identified authoritative source
not_applicable	The concern does not apply to this entity
unknown	The concern is relevant but its value is not known
rejected	A proposed assertion was reviewed and rejected
superseded	The assertion has been replaced by a newer approved assertion

The following rules apply:

1. unknown MUST NOT be treated as not_applicable.
2. not_started MUST NOT be treated as approved.
3. pending_evidence MUST NOT be rendered as established fact.
4. inherited MUST identify the authoritative source and applicability.
5. superseded MUST preserve historical traceability.
6. A record may be structurally conformant while its operational documentation remains incomplete.
7. Completeness MUST be evaluated against the applicable profile and lifecycle state.

11. Decomposition-Level Applicability

The semantic contract applies differently across L0-L4.

Concern	L0 Process Scope	L1 Process Group	L2 Business Process	L3 Activity	L4 Task
Identity and definition	Required	Required	Required	Required	Required
Trigger	Not applicable	Not applicable	Required where process is invoked	Conditional	Conditional
Preconditions	Not applicable	Not applicable	Applicable	Applicable	Applicable
Inputs	Not applicable	Not applicable	Required where transformation has inputs	Applicable	Applicable
Transformation	Not applicable	Not applicable	Required	Describes cohesive work	Describes bounded action
Outputs	Not applicable	Not applicable	Required where produced	Applicable	Applicable
Outcomes	Not applicable	Not applicable	Required	Contributes to parent outcome	Contributes to Activity result
Interfaces	Contextual	Contextual	Applicable	Applicable	Applicable
Dependencies	Contextual	Contextual	Applicable	Applicable	Applicable
Roles	Contextual	Contextual	Applicable	Applicable	Applicable
Responsibility	Contextual	Contextual	Applicable	Applicable	Applicable
Accountability	Contextual	Contextual	Applicable	Applicable	Applicable
Business rules	Contextual	Contextual	Applicable	Applicable	Applicable
Controls	Contextual	Contextual	Applicable	Applicable	Applicable
Exceptions	Not executable	Not executable	Applicable	Applicable	Applicable
Metrics	L0-specific profile treatment	Profile-dependent	Through governed measurement relationships	Through governed measurement relationships	Not assumed
Evidence	Required	Required	Required	Required	Required

The table establishes semantic applicability, not an instruction to add every field to every schema.

11.1 L0 Process Scope

L0 is a non-executable architectural boundary.

It MUST NOT be documented as performing work or possessing operational inputs, outputs, triggers, or transformations.

L0 documentation concerns:

* Scope definition.
* Inclusions and exclusions.
* Architectural boundary.
* Contextual purpose.
* Decomposition basis.
* Governance and evidence.
* L0-specific metrics where governed by the existing model.

11.2 L1 Process Group

L1 organizes related Business Processes.

It MUST NOT be represented as an executable transformation.

Its documentation concerns:

* Grouping rationale.
* Membership criteria.
* Scope and boundary.
* Relationships to contained Business Processes.
* Governance and evidence.

11.3 L2 Business Process

L2 is the principal operational transformation level.

Its documentation MUST explain:

* Why the process exists.
* What invokes it.
* What inputs it uses.
* What transformation it performs.
* What outputs it produces.
* What outcomes it contributes to.
* Which roles and responsibilities are involved.
* Which rules and controls govern it.
* Which interfaces and dependencies are material.

The level of detail must support independent understanding of the Business Process without turning the README into a procedural manual.

11.4 L3 Activity

L3 describes a cohesive body of work within one Business Process.

Its documentation MUST explain:

* Its purpose within the parent process.
* Its cohesion rationale.
* Its contribution to the parent process.
* Relevant inputs and outputs.
* Relevant roles, rules, controls, and evidence.

An Activity MUST NOT be documented as an independent L2 Business Process.

11.5 L4 Task

L4 describes a bounded, actionable, independently verifiable unit of work.

Its documentation MUST explain:

* The bounded action.
* The relevant input or working object.
* The expected result or completion condition.
* Applicable responsibility and controls.
* Verification evidence.

L4 MUST NOT become a workflow engine or carry sequencing, branching, orchestration, or workflow-instance semantics.

12. Canonical Relationship Boundaries

Operational documentation must preserve the distinction between the following relationship concerns:

Relationship concern	Meaning
composes	Structural part-of decomposition
realizes	Business Process realization of a Business Capability
specializes	Semantic refinement or kind-of relationship
serves	Process relationship to an ECF coordinate
depends-on	Operational dependency, subject to canonical relationship governance
consumes	Consumption of a defined input or output
produces	Production of a defined output

The table is a semantic classification, not an authorization to introduce all these relationship types into the canonical metamodel.

EXT-10 MUST verify the authoritative relationship vocabulary and its permitted use against the current OpenDEA metamodel.

Until that verification is complete, any non-canonical relationship terminology MUST remain documentation-level descriptive language and MUST NOT be inserted into canonical relationships arrays as if it were already an approved relationship type.

13. Separation from Adjacent Enterprise Concepts

The operational documentation model MUST preserve the following boundaries:

13.1 Business Functions

A Business Function represents an organizational business responsibility or grouping of capabilities. It is not a process, process group, or role.

13.2 Business Capabilities

A Business Capability expresses what the enterprise is able to do. A Business Process describes work through which capabilities may be realized.

13.3 Information Systems and Information Systems Functions

An Information System is not an input, output, process, or role merely because it participates in an operational interaction.

An Information Systems Function describes a system-level functional responsibility and MUST remain distinct from a Business Function and a Business Process.

System interactions and dependencies should be traceable to canonical Information Systems and Information Systems Function concepts where those concepts exist and are approved.

13.4 Metrics

Metrics are governed measurement concepts. They must not be recreated as free-text operational fields merely to populate README tables.

13.5 Agentic systems

Where an AI agent or software agent performs a role or task, its participation must be explicit and governed. It MUST NOT be silently represented as a human organizational role.

14. Documentation Representation Rules

The README generator and documentation profiles MUST follow these rules:

1. Canonical entity identity and relationships are generated from the canonical YAML.
2. Curated semantic prose is identified as curated content.
3. Inherited content identifies its source.
4. Assumptions are visibly marked.
5. Evidence references are traceable.
6. Completeness states are explicit.
7. Not-applicable concerns are not presented as missing required data.
8. Unknown concerns are not silently omitted.
9. Generated sections are not manually edited in ways that will be overwritten by regeneration.
10. The same semantic assertion MUST NOT be maintained independently in YAML and README without a defined authority and synchronization rule.

The exact storage and rendering implementation is governed by EXT-10, EXT-11, EXT-15, and EXT-17.

15. Schema and Template Implications

This CR establishes semantics only.

It does not authorize immediate schema changes.

EXT-10 MUST evaluate the existing fields and determine whether they are sufficient, require clarification, or require additive extension.

At minimum, the review MUST cover:

* inputs
* transformation
* outputs
* responsibility
* boundary
* trigger
* outcome
* identity
* relationships
* metadata
* Existing documentation profile and manifest structures.

The review MUST explicitly determine:

1. Whether responsibility remains a scalar prose field or requires a structured representation.
2. Whether inputs and outputs require controlled type classifications.
3. Whether input and output identifiers are local or globally addressable.
4. How consumers and sources reference canonical entities.
5. How business rules and controls are represented.
6. Whether operational dependencies are canonical relationships or documentation-level references.
7. How evidence and provenance are represented without duplicating existing governance metadata.
8. How inherited information is represented.
9. How completeness states are stored.
10. Which concerns belong in the canonical entity record versus a documentation manifest.

Any schema change MUST remain additive and backward compatible unless a separately approved migration explicitly authorizes otherwise.

16. Required Downstream CRs

The following CRs are enabled by this semantic contract:

CR	Required work
EXT-10	Align canonical YAML and schemas with the semantic contract
EXT-11	Define level-specific operational documentation profiles
EXT-12	Formalize input, output, transformation, interface, and dependency structures
EXT-13	Formalize role, responsibility, performer, and accountability representation
EXT-14	Formalize rules, controls, exceptions, and deviations
EXT-15	Formalize evidence, provenance, confidence, assumptions, and assertion lifecycle
EXT-16	Establish the research and authoring method
EXT-17	Implement controlled enrichment and backfill tooling
EXT-18	Execute the representative pilot
EXT-19	Backfill L2 Business Processes
EXT-20	Backfill L3 Activities
EXT-21	Backfill L4 Tasks where canonical records exist
EXT-22	Reconcile L0/L1 documentation
EXT-23	Establish conformance requirements
EXT-24	Close the programme and establish continuous governance

17. Repository Changes

Path	Change
docs/operational-documentation-semantic-contract.md	NEW normative semantic contract
change-requests/CR-BP-94-EXT-09-operational-documentation-semantic-contract.md	NEW this CR
change-requests/README.md	Add EXT-09 entry
docs/process-documentation-architecture.md	Link to the semantic contract and update roadmap
docs/decomposition-template-guide.md	Add operational semantic guidance and link to this contract
templates/business-process.yaml	No schema mutation in this CR; add a reference to the semantic contract if appropriate
templates/activity.yaml	No schema mutation in this CR
templates/task.yaml	No schema mutation in this CR
schemas/	No schema mutation in this CR
scripts/	No implementation mutation in this CR

The new semantic contract MUST be linked from the repository README and the documentation architecture.

18. Validation and Test Requirements

The implementation MUST verify:

* Every normative term in this CR has one unambiguous definition.
* Input and output semantics are distinct from trigger, precondition, resource, dependency, and outcome.
* Role, responsibility, accountability, performer, Business Function, and actor are distinct.
* Business rule, control, control evidence, exception, and deviation are distinct.
* L0 and L1 are not represented as executable transformations.
* L2, L3, and L4 have distinct operational documentation expectations.
* No new relationship type is introduced without metamodel authority.
* Existing YAML fields are not duplicated by new structures.
* The documentation architecture and template guide reference the semantic contract.
* The CR metadata validator passes.
* Existing entity and catalogue conformance gates remain conformant.

19. Acceptance Criteria

* AC-01: A normative operational documentation semantic contract is published.
* AC-02: Inputs, outputs, transformation, outcomes, triggers, preconditions, interfaces, and dependencies are explicitly distinguished.
* AC-03: Roles, performers, responsibility, accountability, actors, Business Functions, and Business Capabilities are explicitly distinguished.
* AC-04: Business rules, controls, control evidence, exceptions, and deviations are explicitly distinguished.
* AC-05: Metric, KPI, KRI, KCI, target, threshold, actual, and frequency are distinguished.
* AC-06: L0-L4 applicability is documented.
* AC-07: L0 and L1 are explicitly non-executable architectural constructs.
* AC-08: L4 is explicitly prohibited from carrying workflow orchestration semantics.
* AC-09: Evidence, provenance, confidence, assumptions, and completeness states are defined.
* AC-10: Canonical entity data and curated documentation have explicit authority boundaries.
* AC-11: Relationship terminology is constrained by the authoritative metamodel.
* AC-12: No schema or entity migration is introduced by this CR.
* AC-13: The documentation architecture and authoring guide link to the semantic contract.
* AC-14: Existing conformance gates remain conformant.
* AC-15: EXT-10 through EXT-17 have a stable semantic foundation.

20. Risks and Mitigations

Risk	Mitigation
Semantic terms are overloaded	Maintain explicit normative definitions
Existing schema fields are duplicated	Require EXT-10 field-by-field reconciliation
Documentation becomes a second source of truth	Enforce model-first and manifest authority rules
L0/L1 are incorrectly treated as executable	Explicit non-executable level constraints
L4 becomes a workflow representation	Preserve CR-BP-98 execution boundary
Unsupported relationship types are introduced	Require metamodel verification
AI-generated content is accepted without evidence	Require assertion provenance and accountable review
Metrics are duplicated across levels	Align with the canonical Metric concept

21. Rollback

This CR is a semantic and documentation governance change.

If implementation reveals contradictions with the canonical OpenDEA metamodel or existing approved CRs:

1. Suspend downstream schema changes.
2. Record the contradiction and affected semantic definitions.
3. Reconcile through an ADR or superseding CR.
4. Preserve existing canonical entity records.
5. Do not silently alter existing field meanings.
6. Re-run semantic and conformance checks after resolution.

22. Completion Definition

EXT-09 is complete when the repository has an approved operational documentation semantic contract that can be used consistently by schema designers, documentation authors, reviewers, generators, validators, and backfill tooling.

EXT-09 does not itself add fields, enrich records, or backfill READMEs.

It establishes the normative meaning that all subsequent operational documentation implementation must follow.

Implementation order and immediate next steps

These are document proposals, not repository commits. I have not created or modified files in GitHub.

Order	Action	Reason
1	Review and approve EXT-08	Reconcile existing extension responsibilities and correct the backfill roadmap
2	Review and approve EXT-09	Establish the semantic contract before modifying schemas
3	Produce EXT-10	Reconcile existing fields against the new semantics and decide canonical data structures
4	Produce EXT-11	Finalize L0-L4 operational documentation requirements
5	Produce EXT-12 through EXT-15	Define the detailed semantic models and evidence framework
6	Produce EXT-16 and EXT-17	Establish research, authoring, and controlled enrichment mechanisms
7	Execute EXT-18	Validate the method against representative records before bulk backfill

One important implementation constraint: EXT-10 should not simply add roles, rules, controls, and interfaces as new top-level fields. It must first inspect the existing entity schema, the current templates, the documentation manifest design, and the OpenDEA metamodel to determine which concepts already have canonical homes. This is the key safeguard against creating a second operational ontology inside the Business Process catalogue.

The next logical document is CR-BP-94-EXT-10: Operational Entity Schema Alignment.