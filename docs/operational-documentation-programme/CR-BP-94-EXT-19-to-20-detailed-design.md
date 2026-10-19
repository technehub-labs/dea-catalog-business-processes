Let’s take EXT-19 and EXT-20 forward as a focused implementation tranche: L2 Business Process enrichment first, followed by L3 Activity enrichment.

The two CRs below are expanded into standalone implementation specifications. I’ve strengthened the acceptance criteria around inventory, entity-level disposition, evidence coverage, parent-child reconciliation and generated documentation. This is important because simply populating additional YAML fields would not demonstrate that the operational model is coherent.

CR specifications ready

CR-BP-94-EXT-19 :  L2 Business Process Operational Documentation Backfill

Proposed filename: CR-BP-94-EXT-19-l2-business-process-operational-documentation-backfill.md

Attribute	Value
CR identifier	CR-BP-94-EXT-19
Programme	CR-BP-94 :  Process Decomposition and Operational Documentation
Repository	technehub-labs/dea-catalog-business-processes
Change type	Catalogue enrichment, documentation and data quality
Target decomposition level	L2 :  Business Process
Priority	Critical
Depends on	EXT-15, EXT-16, EXT-17, EXT-18
Enables	EXT-20 :  L3 Activity Backfill
Implementation approach	Inventory, assess, enrich, validate, review and report




1. Executive summary

This Change Request establishes the systematic operational documentation backfill of all in-scope L2 Business Process entities in the Business Process catalogue.

L2 is the principal decomposition level at which a complete business transformation is represented. Its documentation must therefore establish a sufficiently clear understanding of:

* What business purpose the process serves.
* What transformation it performs.
* Where its operational boundaries lie.
* What triggers or conditions initiate it.
* What information and other business objects it consumes.
* What outputs it produces.
* Which roles and authorities are responsible.
* Which rules, controls and exceptions apply.
* Which business and information-system interfaces support it.
* How its performance can be measured.
* How its decomposition into L3 Activities contributes to the transformation.

The backfill shall use canonical entity data as its source of truth. README documentation shall be generated from that data using the approved documentation templates and tooling.

The CR does not authorize the invention of undocumented operating procedures or the creation of unsupported process semantics.

2. Background and rationale

The Business Process catalogue has an established decomposition structure:

Level	Entity type	Primary purpose
L0	Process Context	Establish the process landscape and scope
L1	Process Group	Organize related processes
L2	Business Process	Represent a complete business transformation
L3	Activity	Represent a cohesive body of work contributing to a process
L4	Task	Represent a bounded, independently understandable unit of work

Existing entity records and README documentation do not necessarily provide consistent operational detail.

The preceding CRs establish the prerequisites for resolving this:

* EXT-10 establishes schema alignment.
* EXT-11 establishes decomposition-aware documentation profiles.
* EXT-12 establishes input, output and interface semantics.
* EXT-13 establishes responsibility and accountability semantics.
* EXT-14 establishes business rule, control and exception semantics.
* EXT-15 establishes evidence, provenance and confidence.
* EXT-16 establishes the research and authoring methodology.
* EXT-17 establishes enrichment and validation tooling.
* EXT-18 validates the approach through a controlled pilot.

EXT-19 applies those standards to the L2 catalogue.

3. Objectives

The implementation shall:

1. Establish a complete inventory of L2 Business Process entities.
2. Assess every in-scope entity against the approved L2 documentation profile.
3. Enrich operational information using credible evidence.
4. Establish clear process boundaries and business transformations.
5. Identify and document relevant operational inputs and outputs.
6. Establish process responsibility and accountability where supported.
7. Identify applicable rules, controls, exceptions and dependencies.
8. Establish traceability to relevant enterprise architecture entities.
9. Reconcile each process with its L3 Activity decomposition.
10. Generate consistent README documentation.
11. Establish an auditable catalogue-level completion report.

4. Scope

4.1 In scope

All L2 Business Process entities identified through the repository inventory.

The inventory shall establish:

* Entity identifier.
* Entity name.
* Parent L1 Process Group, where applicable.
* Existing child L3 Activities.
* Existing README.
* Existing operational fields.
* Existing references to other catalogues.
* Current schema and documentation conformance.
* Evidence and review status.
* Backfill priority and disposition.

4.2 Out of scope

This CR shall not:

* Redesign the business process taxonomy.
* Change the fundamental meaning of existing process entities.
* Create unsupported operating procedures.
* Introduce workflow execution semantics.
* Redefine Business Functions or Business Capabilities.
* Duplicate Information System or Information Systems Function definitions.
* Replace authoritative policy, risk, control or metric catalogues.
* Automatically create missing L3 or L4 entities.
* Force every L2 entity to contain every optional operational field.

Structural changes identified during backfill shall be recorded and addressed through the appropriate CR.

5. Normative implementation requirements

REQ-19-01 :  L2 catalogue inventory

Produce an authoritative inventory of all L2 Business Process entities.

The inventory must be derived from the repository, not from a manually assembled or assumed list.

Each entity shall receive a unique inventory record or equivalent traceable reference.

REQ-19-02 :  Profile assessment

Every in-scope entity shall be assessed against the approved L2 documentation profile from EXT-11.

The assessment shall distinguish:

* Required content.
* Conditional content.
* Optional content.
* Not-applicable content.
* Inherited or referenced content.

A field shall not be treated as missing merely because it is not applicable.

REQ-19-03 :  Process identity and purpose

Each L2 entity shall have an operationally meaningful description of its business purpose.

The description must communicate the business need or result served by the process.

A restatement of the entity name is insufficient.

REQ-19-04 :  Business transformation

Each L2 entity shall describe its transformation.

The transformation must explain what business-relevant change, assessment, decision, service or result the process produces.

It must not merely list activities or tasks.

The transformation should identify, where applicable:

* The starting business condition.
* The business object or subject being transformed.
* The nature of the transformation.
* The resulting business state or deliverable.
* The value or business purpose of the transformation.

This description must not imply a mandatory execution sequence.

REQ-19-05 :  Process scope and boundary

Each L2 process shall have a clearly understood boundary.

The documentation shall assess:

* Included business responsibilities.
* Excluded responsibilities.
* Starting boundary.
* Ending boundary.
* Upstream dependencies.
* Downstream consumers or dependencies.
* Relationship to the parent L1 Process Group.

The process boundary must not be defined solely by the organisational department that currently performs the work.

REQ-19-06 :  Trigger and preconditions

Where applicable and supported by evidence, document:

* Initiating events.
* Business triggers.
* Preconditions.
* Eligibility or authorization conditions.
* Relevant timing or periodicity.

Triggers and preconditions must remain distinct.

A process trigger is not necessarily the first execution step.

REQ-19-07 :  Inputs

Each process shall be assessed for relevant inputs.

Where applicable, input documentation should identify:

* Name and description.
* Input type.
* Source.
* Business purpose.
* Required or conditional status.
* Acceptance criteria.
* Validation expectations.
* Provenance.

Inputs must be distinguished from:

* Resources.
* Applications.
* Infrastructure.
* Organizational roles.
* Upstream process dependencies.

Existing inputs fields must be reconciled with the approved EXT-10 schema rather than duplicated.

REQ-19-08 :  Transformation

The transformation description shall explain the substantive business activity represented by the process.

Where the process performs multiple related transformations, the description must represent the coherent business transformation without turning into an activity inventory.

The L3 decomposition should provide the supporting work structure.

REQ-19-09 :  Outputs

Each process shall be assessed for its produced outputs.

Where applicable, document:

* Output name.
* Description.
* Output type.
* Intended consumer.
* Acceptance criteria.
* Relevant quality characteristics.
* Provenance.

Outputs must be distinguished from wider business outcomes.

REQ-19-10 :  Outcomes

Where the process contributes to a measurable or identifiable business outcome, document the relationship.

An outcome must not be represented as a direct process output unless it is genuinely produced by the process.

Where outcome attribution is shared across multiple processes, avoid claiming exclusive causation.

REQ-19-11 :  Business interfaces

Identify relevant interfaces with:

* Other Business Processes.
* Business Functions.
* Business Capabilities.
* Organizational roles or units.
* External parties.
* Other relevant business entities.

The catalogue shall use canonical references where the target entities exist.

REQ-19-12 :  Information and system interfaces

Identify relevant information and system interactions where evidence supports them.

These may include:

* Information Systems.
* Information Systems Functions.
* Data entities or information products.
* Integration interfaces.
* External system interactions.

System names shall not be used as substitutes for process descriptions.

Information Systems and Information Systems Functions must be referenced using their canonical entities when available.

REQ-19-13 :  Dependencies

Document material dependencies where they are relevant to understanding the process.

Distinguish:

* Structural decomposition.
* Business dependency.
* Information dependency.
* System dependency.
* Resource dependency.
* External dependency.

Dependencies must not be represented as parent-child decomposition relationships unless they actually are part of the decomposition structure.

REQ-19-14 :  Responsibility and accountability

Assess and document:

* Process owner.
* Responsible roles.
* Accountable authority.
* Relevant performers.
* Decision authorities.
* Consulted and informed parties, where applicable.

Use the canonical EXT-13 model.

Do not confuse:

* Role with organizational unit.
* Performer with accountable authority.
* Responsibility with accountability.
* Business Function with individual role.

Where ownership cannot be established, record the gap explicitly.

REQ-19-15 :  Business rules

Identify applicable business rules and constraints.

Where relevant, reference canonical policy, regulatory or business-rule entities.

Do not reproduce an authoritative policy or rule in the process entity where a reference is sufficient.

REQ-19-16 :  Controls

Identify relevant controls where they apply to the process.

Document or reference:

* Control objective.
* Relevant risk or obligation.
* Control mechanism.
* Control type.
* Scope.
* Responsible authority.
* Evidence expectations.

Use the EXT-14 semantics.

A process must not be declared compliant merely because a control is referenced.

REQ-19-17 :  Exceptions

Where applicable, identify recognized exceptions and their governing conditions.

Distinguish an authorized exception from an observed deviation.

Do not imply that every exception represents a control failure.

REQ-19-18 :  Performance measures

Identify relevant canonical Metric entities where available.

A process may be associated with measures covering:

* Quality.
* Cost.
* Time.
* Throughput.
* Reliability.
* Compliance.
* Customer or stakeholder outcomes.
* Risk exposure.

The process catalogue shall reference canonical Metric entities rather than independently redefining their measurement semantics.

Do not invent performance targets or claim that a metric is currently measured without evidence.

REQ-19-19 :  L3 decomposition reconciliation

Every L2 entity shall be reconciled with its available L3 Activities.

The reconciliation shall assess:

* Whether each Activity contributes to the process purpose.
* Whether the Activity falls within the process boundary.
* Whether the decomposition contains duplication.
* Whether the decomposition contains apparent gaps.
* Whether Activities are assigned to the correct parent.
* Whether the decomposition is coherent and understandable.

Missing Activities must be recorded as potential taxonomy or decomposition gaps, not automatically created.

REQ-19-20 :  Evidence and provenance

Apply EXT-15 to material operational assertions.

Record evidence source, provenance, confidence and verification status as required by the approved schema.

AI-assisted research shall not be treated as authoritative evidence.

REQ-19-21 :  Unknown and deferred information

Where information cannot be established, record the appropriate state:

* Unknown.
* Not assessed.
* Not applicable.
* Deferred.
* Inherited or referenced.
* Conflicting.
* Confirmed absence.

Do not use fabricated values or misleading placeholder prose.

REQ-19-22 :  Canonical entity update

All accepted operational facts shall be stored in the canonical L2 entity representation.

The existing fields inputs, transformation, outputs, responsibility and boundary shall be retained or migrated according to the approved schema decisions.

Do not introduce parallel fields with overlapping semantics.

REQ-19-23 :  README generation

Generate each L2 README from canonical entity data using the approved documentation generator.

Generated documentation shall:

* Reflect the approved L2 profile.
* Preserve existing useful documentation content.
* Clearly represent applicable evidence status.
* Avoid presenting unverified assertions as established facts.
* Include relevant canonical cross-references.
* Identify documented gaps where appropriate.

REQ-19-24 :  Entity-level disposition

Every L2 entity shall receive an explicit backfill disposition.

The controlled disposition vocabulary shall support:

* verified_complete
* verified_with_gaps
* awaiting_evidence
* awaiting_owner_review
* requires_structural_remediation
* not_applicable
* deferred_with_approval

These are proposed programme-level status values. Their final representation must follow the repository’s canonical schema and governance conventions.

REQ-19-25 :  Catalogue reporting

Publish an L2 backfill report covering:

* Total L2 entities.
* Entities assessed.
* Entities enriched.
* Entities verified.
* Entities with documented gaps.
* Entities awaiting evidence.
* Entities awaiting owner review.
* Entities requiring structural remediation.
* Profile conformance.
* Evidence coverage.
* Cross-reference validity.
* Parent-child reconciliation status.
* Outstanding issues.

6. Implementation work packages

Work package	Deliverable
WP-19-01	L2 inventory and baseline
WP-19-02	L2 profile assessment
WP-19-03	Process purpose, transformation and boundary enrichment
WP-19-04	Inputs, outputs, outcomes and interface enrichment
WP-19-05	Responsibility and accountability enrichment
WP-19-06	Rules, controls, exceptions and dependencies
WP-19-07	Metrics and cross-catalogue references
WP-19-08	Evidence and provenance validation
WP-19-09	L2-to-L3 reconciliation
WP-19-10	README generation and validation
WP-19-11	Human review and disposition
WP-19-12	Catalogue-level reporting

7. Quality gates

Gate 19-A :  Inventory completeness

All L2 entities in scope are identified and accounted for.

Gate 19-B :  Semantic completeness

All applicable L2 profile concepts have been assessed.

Gate 19-C :  Evidence integrity

Material assertions have appropriate provenance and confidence classification.

Gate 19-D :  Decomposition integrity

The relationship between L2 processes and their L3 Activities has been reconciled.

Gate 19-E :  Documentation integrity

Generated README content is consistent with canonical entity data.

Gate 19-F :  Review and disposition

All entities have an approved disposition and unresolved issues have documented owners or deferral rationale.

8. Testing requirements

The implementation must demonstrate:

* All L2 entities can be inventoried.
* Valid L2 entities pass applicable schema and profile validation.
* Invalid or unsupported assertions are flagged.
* Existing operational fields retain their intended semantics.
* Evidence references resolve or have explicit unresolved status.
* Cross-catalogue references validate.
* Parent-child relationships are coherent.
* README generation is reproducible.
* Migration is idempotent.
* No existing entity identifier is unintentionally changed.
* Existing documentation is not silently discarded.

9. Risks and mitigations

Risk	Mitigation
Insufficient source material	Record evidence gaps and prioritize owner confirmation
Overly broad process descriptions	Apply transformation and boundary criteria
Duplication of catalogue concepts	Require canonical references
Inconsistent process ownership	Apply EXT-13
Incorrect activity decomposition	Require L2-to-L3 reconciliation
AI-generated inaccuracies	Apply EXT-15 and EXT-16
Forced completion	Use explicit dispositions
Documentation drift	Generate README from canonical data

10. Acceptance criteria

* [ ]	Complete L2 inventory produced.
* [ ]	All in-scope entities assessed.
* [ ]	Approved L2 profile applied.
* [ ]	Process purpose documented where evidence permits.
* [ ]	Business transformation documented.
* [ ]	Process boundaries reconciled.
* [ ]	Triggers and preconditions assessed.
* [ ]	Inputs and outputs assessed.
* [ ]	Outcomes distinguished from outputs.
* [ ]	Business and information-system interfaces assessed.
* [ ]	Dependencies assessed.
* [ ]	Responsibility and accountability assessed.
* [ ]	Business rules, controls and exceptions assessed.
* [ ]	Relevant Metrics referenced canonically.
* [ ]	Evidence and provenance captured.
* [ ]	L2-to-L3 reconciliation completed.
* [ ]	Canonical entities updated.
* [ ]	README files generated.
* [ ]	Validation and review completed.
* [ ]	Every entity has an explicit disposition.
* [ ]	Catalogue-level L2 report published.
* [ ]	No unsupported operational claims presented as verified.

11. Completion definition

EXT-19 is complete when every in-scope L2 Business Process entity has been assessed, enriched to its evidence-supported level, reconciled with its L3 decomposition, validated, reviewed where required and assigned a documented disposition.

EXT-19 completion authorizes progression to EXT-20 for the relevant L3 population.




CR-BP-94-EXT-20 :  L3 Activity Operational Documentation Backfill

Proposed filename: CR-BP-94-EXT-20-l3-activity-operational-documentation-backfill.md

Attribute	Value
CR identifier	CR-BP-94-EXT-20
Programme	CR-BP-94 :  Process Decomposition and Operational Documentation
Repository	technehub-labs/dea-catalog-business-processes
Change type	Catalogue enrichment, decomposition integrity and documentation
Target decomposition level	L3 :  Activity
Priority	High
Depends on	EXT-15, EXT-16, EXT-17, EXT-18, EXT-19
Enables	EXT-21 :  L4 Task Backfill
Implementation approach	Parent readiness, reconciliation, enrichment, validation and review




1. Executive summary

This Change Request establishes the systematic operational documentation backfill of L3 Activity entities.

L3 Activities represent cohesive bodies of work contributing to an L2 Business Process.

Their documentation must establish:

* The purpose of the Activity.
* Its relationship to the parent Business Process.
* Its scope and boundaries.
* The business contribution it makes.
* Its relevant inputs and outputs.
* Its responsibilities and performers.
* Its applicable rules and controls.
* Its dependencies and interfaces.
* Its relationship to L4 Tasks where applicable.

The L3 layer must provide a meaningful decomposition of the parent process while avoiding duplication of L2 content or inappropriate expansion into L4 execution detail.

2. Background and rationale

The L2 backfill under EXT-19 establishes the business transformation and operational boundaries of the parent processes.

L3 enrichment must build on that foundation.

An Activity cannot be documented accurately in isolation because its purpose and contribution are determined partly by the business transformation it supports.

The programme must therefore maintain a strong relationship between:

* L2 Business Process.
* L3 Activity.
* L4 Task.

EXT-20 is responsible for establishing the L3 operational layer and preparing the catalogue for subsequent task-level enrichment.

3. Objectives

1. Establish a complete L3 Activity inventory.
2. Validate all L3-to-L2 parent relationships.
3. Document Activity purpose and business contribution.
4. Establish meaningful Activity boundaries.
5. Document relevant operational inputs and outputs.
6. Identify applicable responsibilities and controls.
7. Establish evidence and provenance for operational assertions.
8. Assess Activity cohesion and sibling differentiation.
9. Reconcile L3 decomposition with the L2 parent.
10. Prepare L3 entities for L4 Task enrichment.
11. Generate consistent Activity README documentation.

4. Scope

4.1 In scope

All L3 Activity entities in the approved backfill population.

The inventory shall include:

* Activity identifier.
* Activity name.
* Parent L2 Business Process.
* Existing child L4 Tasks.
* Existing README.
* Existing operational fields.
* Existing cross-catalogue references.
* Evidence and review status.
* Profile completeness.
* Backfill disposition.

4.2 Out of scope

This CR shall not:

* Redefine L2 business transformations.
* Introduce new L2 processes without an approved taxonomy change.
* Define detailed L4 task execution.
* Introduce mandatory workflow sequencing.
* Define runtime state, branching or orchestration.
* Invent roles, controls or operational dependencies.
* Duplicate canonical Business Function, Business Capability, Information System or Metric entities.
* Require every Activity to have a fixed number of Tasks.

5. Normative implementation requirements

REQ-20-01 :  L3 inventory

Produce an authoritative inventory of all L3 Activity entities.

The inventory must be derived from the actual repository contents.

Every Activity must be associated with its parent L2 entity or explicitly classified as requiring structural remediation.

REQ-20-02 :  Parent readiness

Before an Activity is enriched, its parent L2 Business Process must:

* Have been assessed under EXT-19.
* Have an accepted operational description.
* Have a sufficiently clear transformation and boundary.
* Have an explicit disposition.
* Have no unresolved parent-level issue that makes the Activity’s scope indeterminate.

An approved exception may allow enrichment to proceed, but the exception and its rationale must be recorded.

REQ-20-03 :  Activity identity and purpose

Every Activity shall have a meaningful description of its purpose.

The description must identify the cohesive body of work represented by the Activity.

It must not merely repeat the Activity name or describe a department, system or job title.

REQ-20-04 :  Parent relationship

Every Activity shall reference its canonical parent L2 Business Process.

The relationship must be validated against the repository’s identifier and hierarchy conventions.

An Activity must not be assigned to a parent solely because the names appear similar.

REQ-20-05 :  Business contribution

Describe how the Activity contributes to the parent’s business transformation.

The contribution should explain, where supported:

* What business responsibility the Activity fulfils.
* What aspect of the transformation it advances.
* What relevant intermediate result it produces.
* How its output contributes to the parent process.

The description must not imply exclusive responsibility for a shared business outcome without evidence.

REQ-20-06 :  Activity boundary

Each Activity shall be assessed for:

* Included work.
* Excluded work.
* Scope.
* Relevant business object or subject.
* Inputs and outputs.
* Relationship to sibling Activities.
* Relationship to its parent L2 boundary.

The boundary must distinguish the Activity from adjacent work.

REQ-20-07 :  Cohesion

An Activity shall represent a coherent body of work.

The assessment must consider whether the Activity:

* Has a clear purpose.
* Contributes to its parent process.
* Has an understandable scope.
* Is distinguishable from sibling Activities.
* Can be decomposed into Tasks where appropriate.
* Avoids grouping unrelated work merely for administrative convenience.

REQ-20-08 :  Inputs and working objects

Identify relevant Activity inputs and working objects where applicable.

These may include:

* Information.
* Business records.
* Requests.
* Documents.
* Data products.
* Materials.
* Other business objects.

Distinguish these from resources, systems and organizational roles.

Where an input is already represented at L2, the Activity should reference or contextualize it rather than duplicate it unnecessarily.

REQ-20-09 :  Outputs

Document outputs produced by the Activity where applicable.

The output description should identify its contribution to the parent process.

Distinguish:

* Activity-level outputs.
* Parent process outputs.
* Wider business outcomes.

Do not assume every Activity produces a separate externally consumable deliverable.

REQ-20-10 :  Responsibility and performers

Identify applicable roles, responsible parties, performers and decision authorities.

Apply the canonical EXT-13 model.

An Activity may involve multiple roles.

Do not infer individual accountability solely from the presence of a performer.

REQ-20-11 :  Business rules

Identify relevant business rules and constraints.

Where a rule applies to the parent process and also constrains the Activity, reference the canonical rule and establish its applicability.

Do not create a second version of the rule at L3.

REQ-20-12 :  Controls

Identify relevant controls where the Activity is within their scope.

Distinguish controls that operate at:

* Parent process level.
* Activity level.
* Task level.

Do not assume that a parent process control applies identically to every Activity.

REQ-20-13 :  Exceptions

Identify relevant Activity-level exceptions where they are supported by evidence.

Distinguish recognized exceptions from deviations.

Do not duplicate parent-level exceptions unless their applicability to the Activity is meaningful.

REQ-20-14 :  Interfaces and dependencies

Identify relevant interfaces and dependencies with:

* Other Activities.
* Other Business Processes.
* Business Functions.
* Business Capabilities.
* Information Systems.
* Information Systems Functions.
* External parties.
* Relevant information products.

The relationship must use approved canonical references and metamodel relationship types.

Do not represent a dependency as decomposition unless it is structurally a parent-child relationship.

REQ-20-15 :  L4 Task relationships

Where L4 Tasks exist, reconcile the Task population with the Activity.

The reconciliation shall assess:

* Whether each Task contributes to the Activity purpose.
* Whether each Task falls within the Activity boundary.
* Whether Tasks overlap.
* Whether Task descriptions are sufficiently bounded.
* Whether the Activity has unexplained decomposition gaps.

This CR shall not prescribe the detailed Task schema or require every Activity to have Tasks.

Those matters are addressed by EXT-21.

REQ-20-16 :  Evidence and provenance

Apply EXT-15 to material L3 operational assertions.

Record source, provenance, confidence and verification status as required.

AI-generated suggestions must not be presented as verified Activity facts.

REQ-20-17 :  Inherited and contextual information

Where information is available at L2 and applies to L3, determine whether it should be:

* Referenced.
* Contextualized.
* Explicitly restated because it is materially different.
* Marked as not applicable.

Do not blindly copy parent content into every child entity.

The source and applicability of inherited information must remain traceable.

REQ-20-18 :  Canonical entity update

Update canonical L3 entity data using the approved schema.

Preserve existing entity identifiers, established references and repository conventions.

Do not create overlapping operational fields or duplicate parent process data.

REQ-20-19 :  README generation

Generate each Activity README from canonical entity data.

The README shall:

* Use the approved L3 documentation profile.
* Explain the Activity’s purpose and parent contribution.
* Represent relevant inputs and outputs.
* Show appropriate responsibility and control references.
* Communicate relevant evidence status.
* Identify unresolved gaps where appropriate.
* Provide relevant L4 references.

REQ-20-20 :  Entity-level disposition

Every in-scope Activity shall receive an explicit backfill disposition.

The programme-level status vocabulary shall support:

* verified_complete
* verified_with_gaps
* awaiting_evidence
* awaiting_owner_review
* requires_structural_remediation
* not_applicable
* deferred_with_approval

Final representation must follow the approved repository schema.

REQ-20-21 :  Catalogue reporting

Publish an L3 backfill report including:

* Total L3 Activities.
* Activities assessed.
* Activities enriched.
* Activities verified.
* Activities with documented gaps.
* Activities awaiting evidence.
* Activities awaiting review.
* Activities requiring structural remediation.
* Parent L2 readiness.
* Activity cohesion status.
* L4 reconciliation status.
* Cross-reference validity.
* Evidence coverage.
* Outstanding issues.

6. Implementation work packages

Work package	Deliverable
WP-20-01	L3 inventory and baseline
WP-20-02	Parent L2 readiness assessment
WP-20-03	L3-to-L2 hierarchy validation
WP-20-04	Activity purpose and contribution enrichment
WP-20-05	Activity boundary and cohesion assessment
WP-20-06	Inputs, outputs and working-object enrichment
WP-20-07	Responsibility and accountability enrichment
WP-20-08	Rules, controls, exceptions and dependencies
WP-20-09	L3-to-L4 reconciliation
WP-20-10	Evidence and provenance validation
WP-20-11	README generation and validation
WP-20-12	Human review and disposition
WP-20-13	Catalogue-level reporting

7. Quality gates

Gate 20-A :  Inventory completeness

All L3 entities are identified and accounted for.

Gate 20-B :  Parent readiness

Every Activity has a valid and sufficiently documented L2 parent, or an approved exception.

Gate 20-C :  Activity integrity

Each Activity has a defensible purpose, scope and contribution to its parent.

Gate 20-D :  Operational completeness

Applicable operational concepts have been assessed against the L3 profile.

Gate 20-E :  Decomposition integrity

The L3-to-L4 relationships have been reconciled to the extent required by the approved L3 profile.

Gate 20-F :  Evidence and documentation integrity

Material assertions have provenance, and generated READMEs reflect canonical entity data.

Gate 20-G :  Review and disposition

Every entity has an explicit disposition and outstanding issues have documented owners or approved deferral.

8. Testing requirements

The implementation shall demonstrate:

* L3 inventory completeness.
* Valid parent L2 relationships.
* Detection of orphaned Activities.
* Detection of invalid or ambiguous references.
* Detection of Activities outside parent boundaries.
* Activity cohesion and sibling differentiation checks, where automatable.
* Evidence and provenance validation.
* Cross-catalogue reference validation.
* Correct treatment of inherited information.
* Correct L4 child relationship validation.
* README generation consistency.
* Idempotent migration and generation.
* Preservation of existing identifiers and valid documentation.

9. Risks and mitigations

Risk	Mitigation
L2 parent is incomplete	Enforce parent readiness gate or approved exception
Activity duplicates parent	Apply purpose and contribution tests
Activity groups unrelated work	Apply cohesion review
Activity is merely an organizational unit	Enforce semantic distinction
L3 becomes workflow documentation	Prohibit execution sequencing and runtime semantics
Parent information is copied unnecessarily	Apply explicit inheritance and reference rules
L4 decomposition is prematurely prescribed	Leave detailed Task requirements to EXT-21
Unsupported roles or controls are invented	Require provenance and qualified review

10. Acceptance criteria

* [ ]	Complete L3 inventory produced.
* [ ]	Every Activity has a valid parent relationship or explicit remediation status.
* [ ]	Parent L2 readiness assessed.
* [ ]	Activity purpose documented where evidence permits.
* [ ]	Contribution to parent transformation established.
* [ ]	Activity boundary documented.
* [ ]	Cohesion and sibling differentiation assessed.
* [ ]	Inputs and working objects assessed.
* [ ]	Outputs and contribution assessed.
* [ ]	Responsibility and accountability assessed.
* [ ]	Rules, controls and exceptions assessed.
* [ ]	Interfaces and dependencies assessed.
* [ ]	L4 child relationships reconciled.
* [ ]	Evidence and provenance captured.
* [ ]	Inherited information is traceable and not blindly duplicated.
* [ ]	Canonical L3 entities updated.
* [ ]	READMEs generated from canonical data.
* [ ]	Validation and review completed.
* [ ]	Every Activity has an explicit disposition.
* [ ]	Catalogue-level L3 report published.
* [ ]	No unsupported operational claims presented as verified.

11. Completion definition

EXT-20 is complete when all in-scope L3 Activities have been assessed, enriched to their evidence-supported level, reconciled with their parent L2 processes, validated and reviewed as required.

EXT-20 completion establishes the operational documentation foundation for EXT-21 :  L4 Task Operational Documentation Backfill.

Implementation sequence and controls

EXT-19 :  L2 first

Precondition for L3

* Establish the L2 inventory.
* Enrich business transformation, boundaries, inputs and outputs.
* Reconcile L2 process ownership and controls.
* Validate the L2-to-L3 structure.
* Publish the L2 disposition report.
    EXT-20 :  L3 second
* Confirm parent L2 readiness.
* Enrich Activity purpose, scope and contribution.
* Reconcile sibling Activities and child Tasks.
* Validate evidence and cross-catalogue references.
* Publish the L3 disposition report.

One important implementation decision

I would make the L2-to-L3 reconciliation matrix a mandatory deliverable of EXT-19, then extend it into an L2-to-L3-to-L4 traceability matrix during EXT-20 and EXT-21.

That matrix will reveal three important classes of problems:

* L2 processes with missing or inadequate Activity decomposition.
* Activities that do not contribute clearly to their assigned parent process.
* Tasks that do not clearly contribute to their assigned Activity.

It gives us a structural quality mechanism across the entire decomposition model, rather than treating documentation completeness as the only measure of success.

My recommendation for the next implementation step is to inspect the actual repository structure and current L2/L3 entities before finalizing file paths, field mappings and the backfill population. That will let us turn these two specifications into repository-conformant CRs without assuming that proposed schema fields or tooling already exist.