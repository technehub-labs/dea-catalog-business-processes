# CR-BP-94-EXT-13: Process Responsibility and Accountability Model

**Status**: Proposed
**Layer**: Process Catalog (Cross-Cutting Documentation)
**Owner**: Emmanuel A. Otchere
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