# CR-BP-94-EXT-12: Process Inputs, Outputs and Interface Semantics

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