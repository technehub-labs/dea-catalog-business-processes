# CR-BP-94-EXT-14: Business Rules, Controls and Exception Semantics

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