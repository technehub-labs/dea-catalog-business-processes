<!--
Source: User submission "DEA-PROCESS-ENRICH-000.md" (DEA-OpenDEA Business Process Operational Documentation and Catalogue Enrichment Change Request).
Preserved as the programme charter reference. The 17-CR programme is broken into discrete change requests:
- CR-BP-94-EXT-08 through CR-BP-94-EXT-24 (one CR per file in change-requests/)
- EXT-08 and EXT-09 are landed in this PR as the governance baseline
- EXT-10 through EXT-24 are reserved identifiers, pending their own CR drafts
This document is preserved here for traceability. D-004 cleanup applied: em-dashes, en-dashes, and three-em-dashes (U+2E3B) replaced with colons, hyphens, and "---" respectively.
-->

OpenDEA Business Process Operational Documentation and Catalogue Enrichment CR

Target repository: technehub-labs/dea-catalog-business-processes⁠

Parent programme: CR-BP-94: Decomposition Record Templates and Documentation Architecture.

Objective: Eliminate the operational-documentation gaps across the Business Process Catalogue by establishing a rigorous, evidence-backed, machine-readable operational semantics model, enriching the canonical entity records, regenerating their documentation, and introducing sustainable quality and governance controls.

I recommend treating this as a formal catalogue-enrichment programme, not simply a README improvement.

There is an important correction to the previous proposal: we should preserve the existing EXT-01 through EXT-07 identities. In particular, EXT-04 already has a documented role in the generation and validation pipeline. We should not create a new EXT-04-R or reuse that identifier for a different initiative.

The existing architecture provides a foundation:

* EXT-01: Documentation Architecture.
* EXT-02: README Profile and Template Standard.
* EXT-03: Documentation Manifest and Coverage Model.
* EXT-04: Generation and Validation Pipeline.
* EXT-05: Decomposition Reconciliation.
* EXT-06: Pilot and Catalogue Rollout.
* EXT-07: README Template Consolidation and Generator V2.

The new programme should complete and extend this architecture, resolving inconsistencies before large-scale enrichment begins.

1. Programme architecture

I propose six initiatives comprising 17 sequential CRs.

Operational documentation enrichment

Six initiatives · 17 proposed CRs · One governed implementation sequence

Initiative A: Governance and architectural reconciliation

CR-01 to CR-02

Establish the authoritative roadmap, resolve overlaps and approve the target architecture.

Initiative B: Operational semantic model

CR-03 to CR-07

Define inputs, outputs, transformations, responsibilities, rules, controls and evidence.

Initiative C: Documentation engineering

CR-08 to CR-10

Establish templates, evidence provenance, authoring methodology and enrichment tooling.

Initiative D: Pilot and backfill execution

CR-11 to CR-14

Pilot, then enrich L2, L3, L4 and L0/L1 records in controlled tranches.

Initiative E: Validation and conformance

CR-15 to CR-16

Implement operational quality gates and progressively enforce completeness.

Initiative F: Closure and continuous governance

CR-17

Establish catalogue-wide closure, lifecycle maintenance and ongoing quality management.

The CR numbers below are proposed programme identifiers. They should be checked against the repository’s CR register before deposition.

2. Master CR register and implementation sequence

Sequence	Proposed CR	Scope
01	CR-BP-94-EXT-08	Documentation Architecture Reconciliation
02	CR-BP-94-EXT-09	Operational Documentation Semantic Contract
03	CR-BP-94-EXT-10	Operational Entity Schema Extension
04	CR-BP-94-EXT-11	Operational Documentation Profiles
05	CR-BP-94-EXT-12	Process Inputs, Outputs and Interface Semantics
06	CR-BP-94-EXT-13	Process Responsibility and Accountability Model
07	CR-BP-94-EXT-14	Business Rules, Controls and Exception Semantics
08	CR-BP-94-EXT-15	Evidence, Provenance and Confidence Framework
09	CR-BP-94-EXT-16	Operational Authoring and Research Methodology
10	CR-BP-94-EXT-17	Enrichment Tooling and Backfill Orchestration
11	CR-BP-94-EXT-18	Operational Documentation Pilot
12	CR-BP-94-EXT-19	L2 Business Process Catalogue Backfill
13	CR-BP-94-EXT-20	L3 Activity Catalogue Backfill
14	CR-BP-94-EXT-21	L4 Task Catalogue Backfill
15	CR-BP-94-EXT-22	L0/L1 Context and Process Group Backfill
16	CR-BP-94-EXT-23	Operational Documentation Conformance Gates
17	CR-BP-94-EXT-24	Catalogue Closure and Continuous Governance

The sequence intentionally separates semantic design from implementation, implementation from population, and population from enforcement.

Initiative A: Governance and architectural reconciliation

CR-BP-94-EXT-08: Documentation Architecture and Extension Roadmap Reconciliation

Purpose

Establish one authoritative documentation architecture and resolve inconsistencies across the existing EXT workstream and related CRs.

Problem being addressed

The repository has accumulated multiple documentation designs and implementation descriptions. Examples include:

* EXT-01’s original architectural sequencing.
* EXT-02’s README structure.
* EXT-03’s documentation manifest.
* EXT-04’s generator and validation responsibilities.
* EXT-07’s revised README structure and metrics extension.
* CR-BP-96 and CR-BP-97’s optional operational fields.
* CR-BP-99’s reconciliation obligations.
* CR-BP-102’s references to legacy documentation and enrichment work.

Some of these documents refer to backfill as a future reconciliation activity, while others refer to it as EXT-04 authoring.

This must be reconciled.

Scope

* Inspect all existing CRs from CR-BP-94 onward.
* Identify which EXT workstreams have actually landed, which remain proposed, and which have been superseded.
* Reconcile the EXT-01 through EXT-07 dependency graph.
* Establish the authoritative responsibilities of:
    * Entity YAML.
    * Documentation profiles.
    * README templates.
    * Documentation manifests.
    * Generator.
    * Validators.
    * Enrichment research assets.
* Identify duplicated, overlapping and conflicting operational fields.
* Reconcile references to CR-BP-96, CR-BP-97, CR-BP-99, CR-BP-102 and CR-BP-120.
* Establish the new EXT-08 through EXT-24 programme roadmap.
* Update the CR register, catalogue metadata and dependency references.

Repository deliverables

* docs/operational-documentation-programme.md
* docs/process-documentation-architecture.md: reconciled revision.
* change-requests/CR-BP-94-EXT-08-documentation-architecture-reconciliation.md
* Updated change-requests/README.md
* Updated reconciliation matrix.
* Updated dependency register.

Acceptance criteria

* No conflicting definitions of EXT-04.
* Every existing CR has a documented disposition.
* Every new CR has an explicit predecessor and successor.
* No existing CR identifier is reused.
* All architectural responsibilities are unambiguous.
* The new programme is represented in the catalogue’s governance artefacts.

CR-BP-94-EXT-09: Operational Documentation Semantic Contract

Purpose

Define the meaning, boundaries, relationships and expected semantics of operational documentation across the process decomposition hierarchy.

This is arguably the most important CR in the programme.

We need a semantic contract before extending schemas or writing thousands of operational descriptions.

Scope

Establish formal definitions for:

* Process input.
* Process output.
* Transformation.
* Interface.
* Trigger.
* Preconditions.
* Postconditions.
* Responsibility.
* Accountability.
* Authority.
* Business rule.
* Control.
* Exception.
* Escalation.
* Evidence.
* Operational resource.
* Information object.
* System dependency.
* Handover.
* Outcome contribution.

Required semantic distinctions

The contract must explicitly distinguish:

Concepts	Required distinction
Input vs resource	Something consumed or acted upon versus something used to execute work
Output vs outcome	Produced artifact/state versus resulting business effect
Transformation vs workflow	Business-level transformation versus execution sequencing
Role vs organizational unit	Responsibility designation versus structural organization
Responsibility vs accountability	Execution obligation versus ultimate answerability
Business rule vs control	Governing decision logic versus mechanism that provides assurance
Control vs evidence	Mechanism versus proof of operation
Exception vs deviation	Recognized alternative condition versus departure from expected execution
Trigger vs precondition	Invocation event versus condition that must be satisfied

Decomposition-level semantics

The contract must establish:

* L2 describes the end-to-end business transformation.
* L3 describes cohesive bodies of work contributing to the L2 transformation.
* L4 describes bounded, independently verifiable units of work.
* L1 groups processes without pretending to execute their transformations.
* L0 establishes the process context and scope without inventing operational execution semantics.

Important architectural rule

Operational details at lower decomposition levels should refine and operationalize the parent semantics, not create contradictory independent definitions.

For example:

An L2 Business Process may consume a customer request and produce an approved customer-service resolution.

Its L3 Activities may validate the request, investigate the issue and formulate a resolution.

Its L4 Tasks may register the request, verify customer identity and record the decision.

These are related but not interchangeable representations.

Repository deliverables

* docs/operational-semantics-contract.md
* docs/operational-semantics-glossary.md
* docs/operational-decomposition-rules.md
* Semantic relationship matrix.
* Normative rules and anti-patterns.
* Corresponding ADRs for significant design decisions.

Acceptance criteria

* All operational terms have unambiguous definitions.
* Each concept has a defined applicable decomposition level.
* Inheritance and refinement rules are explicit.
* The contract does not conflict with CR-BP-93.
* No workflow orchestration semantics are inadvertently introduced into L4 Task records contrary to CR-BP-98.

Initiative B: Operational semantic model

CR-BP-94-EXT-10: Operational Entity Schema Extension

Purpose

Extend the canonical entity schemas to represent operational semantics as structured, machine-readable data.

The YAML entity record must become the authoritative location for operational facts that belong in the entity model.

Scope

Review and extend:

* schemas/entities/business-process.schema.json
* schemas/entities/activity.schema.json
* schemas/entities/task.schema.json
* Process Group and Process Context schemas where applicable.
* templates/business-process.yaml
* templates/activity.yaml
* templates/task.yaml
* Relevant L0/L1 templates and profiles.

Proposed canonical structures

The following is an illustrative target structure, subject to schema reconciliation.

operational:
  inputs:
    - id: input-customer-request
      name: Customer Request
      description: >
        A request submitted by a customer.
      source:
        type: external-party
        reference: null
  transformation:
    summary: >
      Validate and resolve the submitted request.
    steps:
      - id: validate-request
        description: Validate request completeness.
  outputs:
    - id: output-resolution
      name: Customer Resolution
      description: >
        A documented resolution of the request.
      consumer:
        type: downstream-process
        reference: null
  responsibilities:
    accountable:
      - role: Process Owner
    responsible:
      - role: Service Operations
  rules: []
  controls: []
  exceptions: []

This is a design proposal, not a declaration that these fields already exist.

Critical design decisions

* Decide whether existing top-level inputs, outputs, transformation and responsibility fields should remain canonical or be migrated into an operational namespace.
* Preserve compatibility with CR-BP-96 and CR-BP-97.
* Do not create duplicate representations.
* Define schema versioning and migration.
* Ensure references resolve where they claim to identify canonical entities.
* Allow external actors, systems, documents and information objects to be represented without requiring every one to become a catalogue entity.
* Define explicit null, absent, unknown and not-applicable semantics.
* Define stable IDs for individual operational elements.

Additional requirements

* JSON Schema validation.
* YAML examples.
* Negative validation examples.
* Backward-compatibility tests.
* Migration utilities.
* Schema documentation.

Acceptance criteria

* All affected entity schemas validate.
* Existing catalogue records remain valid.
* Existing optional fields retain a deterministic migration path.
* No duplicate canonical field definitions remain.
* All new structures have explicit semantics and validation rules.

CR-BP-94-EXT-11: Operational Documentation Profiles

Sequence 04

Purpose

Define exactly which operational information is required, optional, conditional, inherited or not applicable for every entity type and decomposition level.

Scope

Extend the documentation profile registry to cover all relevant combinations:

Profile	Required operational content
L0 Process Context	Contextual boundaries and scope
L1 Process Group	Grouping rationale, aggregate responsibility and constituent-process references
L2 Business Process	Full operational transformation
L3 Activity	Activity-level inputs, outputs, responsibility and applicable controls
L4 Task	Execution input, bounded action, completion outcome and verification

The profiles must define:

* Required fields.
* Optional fields.
* Conditional requirements.
* Inherited information.
* Not-applicable conditions.
* Evidence requirements.
* Minimum content expectations.
* Lifecycle-dependent obligations.

Specific design requirement

A missing field must not automatically mean the same thing in every situation.

We need explicit documentation states:

State	Meaning
not_started	No enrichment work undertaken
in_progress	Enrichment underway
partial	Some required content populated
complete	Required content meets acceptance criteria
not_applicable	Legitimately outside the entity’s responsibility
unknown	Insufficient evidence to establish the answer
inherited	Authoritatively derived from another entity
deferred	Explicitly postponed with an approved reason

The exact enum should be reconciled with the existing EXT-03 manifest lifecycle and EXT-07 documentation structure.

Deliverables

* Five profile definitions.
* Profile resolution rules.
* Profile validation tests.
* Documentation coverage matrix.
* Profile migration for existing records.

Acceptance criteria

No entity is assessed against an inappropriate operational documentation profile.

CR-BP-94-EXT-12: Process Inputs, Outputs and Interface Semantics

Sequence 05

Purpose

Establish a complete, consistent model for business process inputs, transformations, outputs and interfaces.

Scope

This CR implements the operational data contract for the transformation lifecycle.

Input model

Each input should support:

* Stable identifier.
* Name.
* Description.
* Source.
* Source type.
* Information or artifact type.
* Preconditions.
* Required attributes.
* Validation requirements.
* Mandatory/optional classification.
* Provenance.

Transformation model

Each transformation should support:

* Transformation purpose.
* Description.
* Input-to-output relationship.
* Major transformation responsibilities.
* Business-level conditions.
* Applicable rules.
* Expected completion state.

It must not become an alternative workflow engine.

Output model

Each output should support:

* Stable identifier.
* Name.
* Description.
* Output type.
* Producing entity.
* Consumer.
* Delivery or handover expectation.
* Quality criteria.
* Evidence of production.

Interface model

Interfaces should capture the contract between:

* Processes.
* Activities.
* Tasks.
* External parties.
* Internal organizational units.
* Information systems.
* External organizations.

Important distinction: An interface is the interaction contract between participants, not necessarily a software API.

Deliverables

* Input/output schema extensions.
* Transformation semantics.
* Interface relationship vocabulary.
* Referential integrity checks.
* Authoring examples.
* Tests and migration guidance.

Acceptance criteria

Every populated L2 transformation can be traced from its inputs through its outputs to its intended consumers.

CR-BP-94-EXT-13: Process Responsibility and Accountability Model

Sequence 06

Purpose

Establish a consistent representation of operational ownership and responsibility.

A simple text field such as:

responsibility: Service Operations

is insufficient for meaningful enterprise governance.

Scope

Introduce a structured responsibility model supporting:

Responsibility dimension	Meaning
Accountable	Ultimately answerable for the process
Responsible	Executes or ensures execution
Consulted	Provides required advice or input
Informed	Receives relevant information
Approver	Holds decision or authorization authority
Custodian	Maintains records or operational assets
Control Owner	Accountable for a specified control

The model must distinguish these responsibilities from actual named employees.

Additional requirements

* Role identity and description.
* Responsibility scope.
* Applicable entity.
* Relationship to parent and child responsibilities.
* Authority boundaries.
* Delegation.
* Substitution and escalation.
* Segregation of duties.
* Organizational unit references where available.

RACI may be used as a representation, but the canonical model must not be constrained to RACI alone.

Deliverables

* Responsibility schema.
* Role relationship vocabulary.
* Accountability semantics.
* Delegation rules.
* SoD validation design.
* Example mappings for L2, L3 and L4.

Acceptance criteria

Responsibility can be traced from the process owner through the constituent Activities and Tasks without implying that all entities share identical accountability.

CR-BP-94-EXT-14: Business Rules, Controls and Exception Semantics

Sequence 07

Purpose

Establish a comprehensive operational governance model.

Scope

Model three separate but interconnected concerns.

A. Business Rules

* Eligibility rules.
* Decision rules.
* Calculation rules.
* Prioritization rules.
* Thresholds.
* Policy constraints.
* Regulatory requirements.
* Time and service-level constraints.

B. Controls

* Preventive controls.
* Detective controls.
* Corrective controls.
* Authorization controls.
* Reconciliation controls.
* Segregation-of-duties controls.
* Monitoring controls.
* Evidence-retention controls.

Each control should identify:

* Control objective.
* Control owner.
* Execution responsibility.
* Frequency or trigger.
* Operating procedure.
* Evidence.
* Failure condition.
* Remediation or escalation.

C. Exceptions

* Exception condition.
* Detection mechanism.
* Classification.
* Responsible party.
* Escalation route.
* Resolution expectation.
* Permitted alternative outcome.
* Required evidence.

Cross-cutting requirement

Rules, controls and exceptions must be linked to the processes, Activities or Tasks where they apply.

A regulatory requirement should not be copied into hundreds of entities without identifying its authoritative source and inheritance relationship.

Deliverables

* Business rule schema.
* Control schema.
* Exception schema.
* Regulatory reference model.
* Rule-to-control relationship vocabulary.
* Validation tests.

Acceptance criteria

The model can identify which rules govern a process, which controls assure compliance and how exceptions are managed.

Initiative C: Documentation engineering

CR-BP-94-EXT-15: Evidence, Provenance and Confidence Framework

Sequence 08

Purpose

Ensure that operational documentation is defensible, traceable and distinguishable from assumptions.

Scope

Establish an evidence framework that supports:

* Authoritative enterprise policies.
* Regulatory instruments.
* Industry standards.
* Published operating procedures.
* Industry process frameworks.
* Credible research.
* Expert interviews.
* Subject-matter expert interpretation.
* Explicit architectural assumptions.

Required evidence metadata

evidence:
  - id: evidence-process-policy
    source_type: governance
    source_reference: null
    claim: >
      The process requires authorization before completion.
    authority: authoritative
    confidence: high
    verification_status: verified
    verified_at: null

This is illustrative and must be aligned with the existing evidence structures, including the L4 Task evidence model.

Evidence quality rules

* Every material operational assertion must have a traceable basis.
* A generic industry convention must not be represented as a confirmed enterprise operating policy.
* Regulatory requirements must identify the applicable jurisdiction and source.
* Expert interpretation must be distinguished from published requirements.
* Assumptions must be explicitly identified.
* Conflicting evidence must be recorded rather than silently resolved.
* Superseded sources must be identifiable.

Deliverables

* docs/operational-evidence-framework.md
* Evidence schema extensions.
* Source classification vocabulary.
* Evidence quality assessment rules.
* Provenance validation.
* Conflict resolution procedure.

Acceptance criteria

A reviewer can establish why an operational detail was included and whether it is authoritative, inferred, assumed or unverified.

CR-BP-94-EXT-16: Operational Authoring and Research Methodology

Sequence 09

Purpose

Establish a repeatable methodology for researching and authoring operational content across the entire catalogue.

The programme must avoid formulaic descriptions and artificial certainty.

Scope

Create a structured authoring methodology with the following stages:

* Resolve entity identity and classification.
* Examine parent and child entities.
* Review existing canonical YAML.
* Identify operational gaps.
* Research the relevant business domain.
* Identify authoritative evidence.
* Establish operational inputs and outputs.
* Define the transformation.
* Establish responsibility and accountability.
* Identify business rules and controls.
* Identify exceptions.
* Reconcile with related processes.
* Record evidence and assumptions.
* Obtain semantic review.
* Validate the YAML.
* Regenerate the README.
* Reconcile the documentation manifest.

Research methodology

Establish a repeatable research hierarchy:

Priority	Source
1	Approved enterprise policy and procedures
2	Applicable legislation and regulatory requirements
3	Authoritative industry standards
4	Established process frameworks
5	Credible domain-specific publications
6	Expert interpretation and reasoned architectural derivation

The methodology must also define what to do when enterprise-specific operating procedures are unavailable.

In that situation, produce a clearly labelled reference-model interpretation rather than claiming to describe an organization’s actual operating model.

Required documentation templates

* Research brief.
* Operational enrichment worksheet.
* Evidence register.
* Semantic review checklist.
* Backfill completion report.
* Unresolved-gap register.

Acceptance criteria

Two independent researchers should be able to produce operational documentation with comparable semantic quality using the same methodology.

CR-BP-94-EXT-17: Enrichment Tooling and Backfill Orchestration

Sequence 10

Purpose

Provide deterministic tools for catalogue analysis, enrichment preparation, validation and documentation regeneration.

Scope

Extend the existing repository CI and scripts rather than creating a parallel tooling ecosystem.

Required capabilities

1. Catalogue discovery

* Enumerate all canonical entities.
* Resolve entity types and levels.
* Identify operational fields already populated.
* Identify missing, partial and inconsistent fields.
* Identify parent-child relationships.

2. Enrichment planning

Generate a machine-readable work queue:

entity_id: processes:process-example
entity_type: Process
level: L2
enrichment:
  inputs: missing
  transformation: partial
  outputs: missing
  responsibilities: missing
  rules: unknown
  controls: missing
  evidence: partial
status: not_started

3. Enrichment execution

* Support controlled batches.
* Support dry-run.
* Preserve existing information.
* Detect conflicting content.
* Record change history.
* Prevent accidental overwrites.
* Support repeatable execution.

4. Validation

* Schema validation.
* Semantic checks.
* Relationship checks.
* Evidence checks.
* Parent-child reconciliation.
* Duplicate detection.

5. Documentation generation

* Regenerate affected READMEs.
* Preserve generated markers.
* Update documentation manifests.
* Produce coverage reports.

6. Reporting

Produce:

* Catalogue-wide completeness.
* Per-domain completeness.
* Per-entity-type completeness.
* Outstanding evidence gaps.
* Inconsistent operational relationships.
* Failed validation findings.

Acceptance criteria

The enrichment pipeline is deterministic, idempotent, auditable and integrated into the repository’s existing CI.

Initiative D: Pilot and backfill execution

CR-BP-94-EXT-18: Operational Documentation Pilot

Purpose

Demonstrate the complete operational documentation methodology against a representative sample before mass enrichment.

Scope

Use the existing Customer Insight and Retention process as the initial pilot, subject to confirming its current canonical identity and decomposition structure.

The pilot must cover:

* One L2 Business Process.
* Its associated L3 Activities.
* Its associated L4 Tasks.
* Relevant L1 Process Group.
* Relevant L0 Process Context.

Pilot requirements

* Establish the current baseline.
* Apply the new semantic contract.
* Populate the canonical YAML.
* Establish input/output relationships.
* Establish responsibilities.
* Establish rules and controls.
* Capture evidence.
* Reconcile the decomposition.
* Regenerate documentation.
* Validate all documentation profiles.
* Test the backfill tooling.
* Conduct independent semantic review.

Pilot evaluation dimensions

Dimension	Evaluation
Semantic correctness	Are the operational details meaningful and accurate?
Completeness	Are required fields populated?
Evidence	Can assertions be substantiated?
Consistency	Do parent and child records agree?
Usability	Can an enterprise architect understand the process?
Machine-readability	Can tools consume the structured data?
Maintainability	Can future changes be incorporated safely?

Deliverables

* Pilot enrichment records.
* Before-and-after comparison.
* Pilot evaluation report.
* Identified schema and tooling defects.
* Revised authoring methodology.
* Go/no-go recommendation for mass backfill.

Acceptance criteria

The pilot must pass all critical semantic and structural checks before CR-19 begins.

CR-BP-94-EXT-19: L2 Business Process Catalogue Backfill

Purpose

Populate operational semantics for all canonical L2 Business Process records.

This is the first major production backfill.

The current Business Process template already provides the foundations through CR-BP-96:

* inputs
* transformation
* outputs
* responsibility
* boundary

This CR must extend and reconcile those fields with the new contract rather than creating a parallel representation.

Scope

For every L2 Business Process:

* Identify the business transformation.
* Define its operational trigger.
* Identify inputs and their origins.
* Define the transformation.
* Identify outputs and their consumers.
* Define responsibility and accountability.
* Identify relevant business rules.
* Identify applicable controls.
* Identify exceptions.
* Record evidence and provenance.
* Reconcile with its parent Process Group.
* Reconcile with its child Activities.
* Update canonical YAML.
* Regenerate README.
* Update the documentation manifest.

Backfill segmentation

Execute by the seven ECF domains:

* Agency and Organization.
* Enablement and Operations.
* Finance and Accounting.
* Governance and Existence.
* Party and Relationship.
* Product and Value.
* Strategy and Direction.

The exact domain vocabulary and coordinates must be taken from the canonical ECF register.

Important quality constraint

The same input/output descriptions must not be mechanically copied across unrelated processes merely because they belong to the same domain.

Common definitions may be referenced where appropriate, but process-specific semantics must be independently justified.

Deliverables

* Enriched L2 YAML records.
* Regenerated L2 READMEs.
* Updated manifests.
* Domain completion reports.
* Evidence registers.
* Exception and unresolved-gap register.

Acceptance criteria

Every L2 record has either:

* Complete operational documentation.
* An explicitly justified not_applicable designation.
* An evidence-backed unknown state.
* An approved deferred item with an owner and resolution plan.

No record may silently retain a legacy pending marker as its completion state.

CR-BP-94-EXT-20: L3 Activity Catalogue Backfill

Sequence 13

Purpose

Enrich all canonical Activities with their operational semantics.

The Activity layer must demonstrate how the Business Process transformation is realized through cohesive bodies of work.

Scope

For every L3 Activity:

* Define Activity-level inputs.
* Define outputs.
* Identify contributing transformation.
* Define responsibility.
* Identify applicable rules.
* Identify applicable controls.
* Identify exception conditions.
* Establish evidence.
* Reconcile with the parent L2 Business Process.
* Reconcile with its L4 Tasks.

Specific requirements

* Activity inputs must be traceable to parent-process inputs or preceding Activity outputs.
* Activity outputs must contribute to the parent-process transformation.
* Responsibility must be bounded to the Activity.
* Controls must be assigned to the appropriate operational responsibility.
* Activity boundaries must remain cohesive.
* An Activity must not be elevated into an independent Business Process merely because it has an input and output.
* Existing cohesion rationale must be preserved and used in the enrichment assessment.

Deliverables

* Enriched Activity YAML.
* Updated Activity READMEs.
* Parent-child traceability report.
* Operational consistency report.
* Evidence register.

Acceptance criteria

Each Activity is operationally meaningful and contributes demonstrably to its parent Business Process.

CR-BP-94-EXT-21: L4 Task Catalogue Backfill

Sequence 14

Purpose

Complete operational documentation for all canonical L4 Tasks.

The Task layer must establish bounded, independently verifiable units of work.

Scope

For every Task:

* Define execution input.
* Define required information or artifacts.
* Define the bounded action.
* Define the expected completion state.
* Identify responsible role.
* Define verification requirements.
* Identify applicable controls.
* Identify evidence.
* Reconcile with the parent Activity.

Critical distinction

L4 Task documentation must not become a workflow definition.

The following remain outside the canonical Task semantics in accordance with CR-BP-98:

* Task sequencing.
* Branching.
* Workflow conditions.
* Orchestration.
* Choreography.
* State machines.
* Automation implementation.

A Task describes a bounded unit of work, not the workflow engine coordinating multiple Tasks.

Deliverables

* Enriched Task YAML.
* Updated Task READMEs.
* Activity-to-Task traceability.
* Verification and evidence definitions.
* Operational completeness reports.

Acceptance criteria

Every Task has a verifiable completion outcome, clear responsibility and bounded execution semantics.

CR-BP-94-EXT-22: L0/L1 Context and Process Group Backfill

Sequence 15

Purpose

Complete the contextual and grouping documentation surrounding the operational catalogue.

This is deliberately sequenced after the L2-L4 enrichment because those records provide the operational detail from which aggregate context and group-level explanations can be validated.

Scope

L0: Process Context

Document:

* Context purpose.
* Enterprise domain.
* Scope.
* Included responsibilities.
* Excluded responsibilities.
* Adjacent contexts.
* Governing policies and standards.
* Context ownership.
* Relevant cross-context relationships.

L1: Process Group

Document:

* Grouping rationale.
* Process membership.
* Shared business purpose.
* Aggregate outcomes.
* Group boundaries.
* Cross-process dependencies.
* Common responsibilities.
* Shared governance obligations.

Important rule

L0 and L1 must not be forced to populate executable inputs and outputs simply because L2-L4 records require operational documentation.

Where aggregate inputs or outputs are useful, they must be clearly identified as contextual or derived aggregates rather than independent operational interfaces.

Deliverables

* Enriched L0/L1 documentation.
* Updated Process Context and Process Group records where justified.
* Group-to-process consistency report.
* Context coverage report.
* Updated manifests and READMEs.

Acceptance criteria

Every Process Group and Process Context accurately represents its constituent catalogue and has no contradictory scope or grouping semantics.

Initiative E: Validation and conformance

CR-BP-94-EXT-23: Operational Documentation Conformance Gates

Purpose

Establish enforceable operational documentation quality across the repository.

The existing documentation profile validator and conformance pipeline should be extended rather than duplicated.

Scope

Introduce a structured gate family.

Gate family	Responsibility
OPR-001	Operational profile applicability
OPR-002	Required inputs
OPR-003	Required outputs
OPR-004	Transformation completeness
OPR-005	Input-output consistency
OPR-006	Responsibility completeness
OPR-007	Accountability consistency
OPR-008	Business rule structure
OPR-009	Control completeness
OPR-010	Exception handling
OPR-011	Evidence provenance
OPR-012	Parent-child operational traceability
OPR-013	Interface integrity
OPR-014	Not-applicable justification
OPR-015	Unknown and deferred state governance
OPR-016	README-to-YAML consistency
OPR-017	Manifest completeness
OPR-018	Lifecycle-specific requirements
OPR-019	Duplicate and contradictory semantics
OPR-020	Change-history traceability

These identifiers are proposed. They must be reconciled with existing gate families before implementation.

Enforcement strategy

Do not immediately turn all findings into blocking failures.

Use three stages:

Stage	Behaviour
Advisory	Findings are reported, but merges are not blocked
Transitional	Blocking for new or modified records, advisory for legacy records
Mandatory	Blocking for all applicable records

Required CI integration

* Schema validation.
* Operational semantic validation.
* Documentation generation consistency.
* Manifest validation.
* Evidence validation.
* Relationship integrity.
* Catalogue-wide reporting.

Acceptance criteria

* All gates have automated tests.
* Findings have stable identifiers.
* Existing gate results remain unaffected unless explicitly intended.
* Legacy exceptions are traceable.
* New and modified records cannot introduce new ungoverned operational gaps.
* Catalogue-wide enforcement is introduced only after backfill closure.

CR-BP-94-EXT-24: Catalogue Closure and Continuous Governance

Purpose

Make operational documentation a permanent part of catalogue governance and lifecycle management.

Scope

* Establish the authoritative catalogue-wide completion baseline.
* Verify all L0-L4 records against their applicable profiles.
* Close or explicitly disposition all outstanding backfill findings.
* Reconcile all manifests.
* Verify all generated READMEs.
* Confirm parent-child consistency.
* Establish ongoing ownership.
* Introduce change-triggered documentation review.
* Define periodic evidence review.
* Establish deprecation and retirement handling.
* Produce the final programme closure report.

Continuous governance requirements

An operationally meaningful change to an entity must trigger reassessment of affected documentation.

Examples:

* Input changes.
* Output changes.
* Transformation changes.
* Responsibility changes.
* New regulatory obligations.
* New controls.
* New exceptions.
* Parent-child decomposition changes.
* Changes to the associated system interface.

Documentation must not remain marked complete after its underlying semantics have materially changed.

Deliverables

* Catalogue-wide completion report.
* Outstanding findings disposition register.
* Documentation governance policy.
* Operational documentation ownership model.
* Change-trigger rules.
* Periodic review policy.
* Final programme closure report.

Acceptance criteria

The programme can be formally closed, with remaining exceptions explicitly governed and future documentation quality maintained through CI and lifecycle governance.

3. Supporting Architecture Decision Records

The programme should not put every significant design decision inside individual CRs. Several decisions will influence multiple implementation stages and should therefore be recorded as ADRs.

I recommend the following ADR series.

ADR	Decision
ADR-BP-OPR-001	Canonical location of operational semantics: top-level fields versus operational namespace
ADR-BP-OPR-002	Operational documentation as a decomposition-aware model
ADR-BP-OPR-003	Evidence provenance, confidence and assumption classification
ADR-BP-OPR-004	Parent-child inheritance versus explicit operational duplication
ADR-BP-OPR-005	Operational documentation completeness and lifecycle states
ADR-BP-OPR-006	Human-authored semantics versus AI-assisted enrichment
ADR-BP-OPR-007	Operational relationships with Information Systems, Business Functions and Capabilities
ADR-BP-OPR-008	Backward compatibility and progressive enforcement of operational schemas

Particularly important decisions

ADR-BP-OPR-001: Canonical data location

We must decide whether to retain existing top-level fields such as inputs, outputs and responsibility, or introduce an operational namespace.

My preference is to preserve existing canonical fields where they already have established consumers, unless a compelling metamodel alignment reason justifies migration.

ADR-BP-OPR-004: Inheritance and refinement

My recommendation is:

* L2 establishes the business transformation.
* L3 refines the transformation into cohesive bodies of work.
* L4 specifies bounded execution units.
* Child entities reference parent semantics where appropriate.
* Child entities only introduce additional detail where it genuinely belongs to their responsibility.

This avoids thousands of duplicated definitions.

ADR-BP-OPR-006: AI-assisted enrichment

AI can research, propose and structure operational details. However:

* AI-generated assumptions must be identifiable.
* Evidence must be recorded.
* Human review must be required for material business claims.
* AI must not invent organizational policies or actual operating arrangements.
* Approved content must be distinguishable from candidate enrichment.

This will be particularly useful when enriching the catalogue at scale.

4. Cross-repository initiatives

There is a further consideration: the Business Process Catalogue is part of a larger OpenDEA ecosystem.

Operational documentation should not become an isolated model.

I recommend four cross-repository initiatives.

Initiative	Related repository	Purpose
Cross-entity semantic alignment	dea-metamodel	Ensure operational attributes and relationships align with the OpenDEA metamodel
Information Systems traceability	Information Systems catalogue	Link processes to the systems supporting their execution
Business Function traceability	Business Functions catalogue	Connect operational responsibilities to organizational functions
Capability and Value Stream alignment	Business Capabilities and Agentic Value Stream catalogues	Trace process execution to capabilities and value realization

These should be managed through separate cross-repository CRs, triggered after the relevant canonical semantic contracts are established.

In particular, the Information Systems work should align with the Information Systems Functions investigation and its proposed CR-IS-CAT-01 series.

The desired eventual traceability is:

Business Capability

What the enterprise must be able to do

Business Process

What transformation is performed

Activity → Task

How the transformation is realized

Business Functions and Roles

Who is responsible for execution

Information Systems and Systems Functions

Which information-system services enable execution

Controls, Evidence and Metrics

How execution is governed and measured

This is a conceptual traceability view, not a proposed containment hierarchy. The canonical metamodel must determine the actual relationship types.

5. Implementation dependency and release gates

The 17 CRs should not simply be executed in numerical order without formal stage gates.

The following dependency structure is recommended.

Foundation

EXT-08 → EXT-09

Semantic model

EXT-10 → EXT-11 → EXT-12 → EXT-13 → EXT-14 → EXT-15

Engineering

EXT-16 → EXT-17

Pilot and enrichment

EXT-18 → EXT-19 → EXT-20 → EXT-21 → EXT-22

Conformance and closure

EXT-23 → EXT-24

The dependencies are primarily sequential, but some work can overlap after its prerequisites are satisfied.

Release gate	Required condition
G1: Architecture approved	EXT-08 and EXT-09 accepted
G2: Model approved	EXT-10 through EXT-15 accepted
G3: Tooling ready	EXT-16 and EXT-17 accepted
G4: Pilot approved	EXT-18 passes independent review
G5: Operational backfill	EXT-19 through EXT-22 completed
G6: Enforcement approved	EXT-23 passes migration and compatibility tests
G7: Programme closure	EXT-24 accepted

Important: Existing EXT-02, EXT-03, EXT-04, EXT-05, EXT-06 and EXT-07 implementation status must be checked during EXT-08. Already-landed functionality should be reused, not recreated. Outstanding original work must be incorporated into the dependency plan.

6. Backfill execution governance

I recommend adopting the following principles across all four backfill CRs.

A. No fabricated completeness

A record must not be marked complete merely because all YAML keys contain values.

Completeness must mean that the content is semantically meaningful, sufficiently specific and appropriately evidenced.

B. Preserve source history

Every enrichment must:

* Record its governing CR.
* Update metadata.change_history.
* Preserve existing valid semantics.
* Identify material semantic changes.
* Remain reproducible through the repository pipeline.

C. Separate completeness from confidence

A process can have all fields populated while still containing unverified assumptions.

Therefore, two separate dimensions must be reported:

* Documentation completeness.
* Evidence quality.

D. Establish a catalogue baseline

Before backfill, capture:

* Total entities by level.
* Existing operational-field coverage.
* Missing fields.
* Partial fields.
* Invalid or contradictory values.
* Existing documentation coverage.
* Existing evidence coverage.

The actual entity counts must be derived from the current repository, not inherited from historical CRs.

E. Use controlled tranches

For each domain, produce a reviewable batch with:

* Entity inventory.
* Enrichment proposals.
* Evidence register.
* YAML changes.
* Generated README changes.
* Validation report.
* Outstanding exceptions.

Do not make one enormous unreviewable catalogue-wide semantic change.

7. Programme-level definition of done

The programme should only be considered complete when all of the following are true.

Programme closure checklist

0/12 verified

Architecture

EXT roadmap, semantic contracts and ADRs are reconciled and approved.

Canonical model

All applicable operational attributes have authoritative schema definitions.

Profiles

L0-L4 have appropriate documentation obligations.

Inputs and outputs

Applicable entities have meaningful, traceable operational interfaces.

Responsibilities

Accountability and execution responsibility are properly distinguished.

Governance

Business rules, controls and exceptions are represented.

Evidence

Material assertions have appropriate provenance and confidence.

Research

A repeatable authoring and review methodology exists.

Automation

Enrichment and README generation are deterministic and auditable.

Backfill

L0-L4 catalogue enrichment is completed or explicitly dispositioned.

Validation

Operational conformance gates are implemented and enforced.

Governance lifecycle

Future semantic changes trigger appropriate documentation reassessment.

Reset checklist

8. Recommended execution order

My recommendation is to treat this as a formal programme with three separate approval points.

Approval 1: Architecture

Complete CR-BP-94-EXT-08 and EXT-09. Do not extend schemas until the semantic contract and roadmap are reconciled.

Approval 2: Canonical model

Complete EXT-10 through EXT-17. This establishes the data model, profiles, evidence methodology and automation needed for reliable enrichment.

Approval 3: Catalogue transformation

Execute EXT-18 through EXT-24. Pilot first, backfill in decomposition order, validate, then close.

One important sequencing choice is to enrich L2 before L3 and L4. The parent Business Process must establish the transformation contract that its Activities and Tasks subsequently refine. L0 and L1 follow to ensure their aggregate descriptions reflect the enriched catalogue.

9. Immediate next action

I recommend we now produce the actual CR documents, beginning with:

* CR-BP-94-EXT-08: Documentation Architecture and Extension Roadmap Reconciliation.
* CR-BP-94-EXT-09: Operational Documentation Semantic Contract.

These should be comprehensive, implementation-ready CRs, each containing:

* Background and problem statement.
* Normative requirements.
* Detailed scope and exclusions.
* Architectural decisions and constraints.
* Repository file changes.
* Schema and data migration implications.
* Validation and test requirements.
* CI/CD integration.
* Acceptance criteria.
* Dependencies and sequencing.
* Risks and mitigations.
* Rollback and backward-compatibility provisions.
* Follow-on CR references.

The governing principle should be that no operational enrichment is considered complete until its semantics, canonical representation, evidence, documentation and validation are all aligned.