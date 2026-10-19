# CR-BP-94-EXT-22 and EXT-23: Process Decomposition Reconciliation and Structural Integrity

**Source**: the user-submitted `CR-BP-EXT-22.md` and `CR-BP-EXT-23.md` (2026-10-19)
**Programme**: CR-BP-94 (Process Decomposition and Operational Documentation)
**Repository**: technehub-labs/dea-catalog-business-processes

**Note on the two attachments**: the `CR-BP-EXT-23.md` attachment is a variant of the
EXT-22 CR. It carries an additional preamble (reproduced in section 1 below) and an
additional closing section, *Recommended programme decision* (reproduced in section 19
below). The CR body is otherwise identical to `CR-BP-EXT-22.md`. The attachment does
not contain a distinct EXT-23 specification.

---

## 1. The EXT-23 attachment preamble (verbatim)

EXT-22 should close the decomposition-backfill phase by reconciling the process hierarchy across L2 Business Processes, L3 Activities and L4 Tasks, while also resolving the contextual integrity of L0 Process Scopes and L1 Process Groups.

The key distinction is that EXT-22 is not another enrichment exercise. EXT-19, EXT-20 and EXT-21 enrich entities at their respective levels. EXT-22 verifies that those entities form a coherent, complete and defensible decomposition: every child contributes to its parent, every parent is adequately represented by its children, and structural anomalies are explicitly resolved or dispositioned.

I recommend making the L2-L4 Reconciliation Matrix a mandatory controlled programme artefact, rather than treating it as an optional report. It becomes the evidence base for determining whether the process catalogue is ready for conformance enforcement under EXT-23.

---

## 2. The CR-BP-EXT-22 specification (verbatim)

CR-BP-EXT-22  -  Process Decomposition Reconciliation and Structural Integrity

Attribute	Value
CR ID	CR-BP-EXT-22
Title	Process Decomposition Reconciliation and Structural Integrity
Programme	Operational Documentation Framework Extension
Status	Proposed
Priority	Critical
Change Type	Catalogue governance, structural integrity, semantic reconciliation
Depends On	EXT-08 through EXT-21, particularly EXT-10, EXT-11, EXT-15, EXT-17, EXT-18, EXT-19, EXT-20 and EXT-21
Enables	EXT-23  -  Operational Documentation Conformance Gates
Scope	L0 Process Scope, L1 Process Group, L2 Business Process, L3 Activity, L4 Task




1. Executive Summary

This Change Request establishes a systematic reconciliation process for the complete Business Process catalogue hierarchy, ensuring that its decomposition is structurally valid, semantically coherent, sufficiently complete and traceable across all levels.

The preceding CRs establish operational documentation and enrichment at individual decomposition levels:

* EXT-19: L2 Business Process enrichment.
* EXT-20: L3 Activity enrichment.
* EXT-21: L4 Task enrichment.

However, enriching each level independently does not guarantee that the relationships between levels are correct.

For example:

* An L2 Business Process may have Activities that do not collectively represent its intended transformation.
* An L3 Activity may exist under an L2 Process but contribute little or nothing to its purpose.
* An L3 Activity may contain Tasks that collectively fail to represent the Activity’s intended work.
* A Task may be assigned to an Activity that does not logically own its responsibility.
* A Process, Activity or Task may be duplicated under different names.
* A decomposition may contain structural gaps, orphaned entities or inappropriate granularity.
* An L1 Process Group may contain Processes that do not satisfy its grouping rationale.
* An L0 Process Scope may fail to account for relevant L1 groups or may have unclear boundaries.

EXT-22 addresses these issues through a controlled, evidence-based reconciliation of the hierarchy.

Its central deliverable is the L2-L4 Reconciliation Matrix, supported by an L0-L1 contextual reconciliation and a catalogue-wide structural integrity assessment.

The outcome must be a defensible process decomposition, not merely a catalogue in which every entity has a populated README.

2. Problem Statement

The Business Process catalogue uses a hierarchical decomposition:

Level	Entity	Primary purpose
L0	Process Scope	Establishes the overall scope and boundaries of a process domain or process landscape.
L1	Process Group	Organises related Business Processes into meaningful groups.
L2	Business Process	Represents a complete business transformation or coherent business result-producing process.
L3	Activity	Represents a cohesive body of work contributing to a Business Process.
L4	Task	Represents a bounded, independently understandable unit of work contributing to an Activity.

The hierarchy is intended to provide progressively more detailed representations of business work.

However, structural parent-child relationships alone do not demonstrate that the decomposition is meaningful.

A valid hierarchy requires two complementary forms of reconciliation:

Top-down decomposition integrity

The parent must be adequately represented by its children. The children must collectively account for the parent’s scope, responsibilities and intended contribution.

Bottom-up semantic integrity

Every child must have a defensible relationship to its parent. Its purpose and contribution must be explainable in the context of the parent’s purpose and boundaries.

Both directions are necessary.

A decomposition can be structurally complete but semantically invalid. Equally, individual entities can be well documented while the overall decomposition remains incomplete.

EXT-22 introduces explicit reconciliation rules and evidence requirements to address this gap.

3. Objectives

The objectives are to:

1. Establish a consistent reconciliation methodology across L0-L4.
2. Verify that each L2 Business Process is adequately represented by its L3 Activities.
3. Verify that each L3 Activity is adequately represented by its L4 Tasks where further decomposition is appropriate.
4. Confirm that each Activity contributes meaningfully to its assigned Business Process.
5. Confirm that each Task contributes meaningfully to its assigned Activity.
6. Identify missing, orphaned, duplicated, misplaced or inconsistently defined entities.
7. Identify decomposition that is too broad, too narrow or unnecessarily granular.
8. Identify Activities or Tasks that have been decomposed according to execution sequence rather than functional responsibility.
9. Verify alignment between parent and child boundaries, inputs, outputs, responsibilities, rules, controls and dependencies.
10. Reconcile L0 Process Scopes and L1 Process Groups with the L2 process landscape.
11. Establish explicit disposition and remediation requirements for unresolved structural or semantic gaps.
12. Produce a traceable reconciliation baseline for EXT-23 conformance enforcement.

4. Scope

4.1 In scope

The CR covers:

* All existing L0 Process Scope entities.
* All existing L1 Process Group entities.
* All existing L2 Business Process entities.
* All existing L3 Activity entities.
* All existing L4 Task entities.
* Parent-child relationships.
* Entity membership and classification.
* Decomposition adequacy and completeness.
* Semantic contribution and alignment.
* Entity boundaries and ownership.
* Inputs, outputs and transformation relationships.
* Responsibilities and accountability.
* Rules, controls and exceptions.
* Dependencies and interfaces.
* Metric and evidence references where applicable.
* Duplicate and overlapping entities.
* Orphaned and misplaced entities.
* Granularity and decomposition quality.
* Cross-level consistency.
* Reconciliation evidence and approval.
* Catalogue-wide reporting.

4.2 Out of scope

EXT-22 does not:

* Redesign the complete Business Process metamodel.
* Introduce new decomposition levels.
* Redefine the semantics of L0-L4.
* Replace EXT-19, EXT-20 or EXT-21 enrichment activities.
* Introduce mandatory workflow sequencing or orchestration.
* Convert the process hierarchy into a workflow execution model.
* Automatically merge or delete entities.
* Invent missing operational facts.
* Automatically infer authoritative parent-child relationships from naming similarity.
* Introduce new cross-catalogue relationship types without metamodel approval.
* Make unsupported claims of completeness where evidence is unavailable.

Where an issue requires changes outside this CR, it must be recorded and routed through the appropriate CR or ADR.

5. Governing Decomposition Principles

5.1 Functional decomposition, not execution sequencing

The hierarchy represents progressively decomposed business responsibility and work.

It does not inherently represent:

* Execution order.
* Workflow steps.
* Branching logic.
* Runtime orchestration.
* State transitions.
* Scheduling.
* Queue management.
* Retry behaviour.

A Task can contribute to an Activity without the catalogue prescribing when it must execute relative to another Task.

5.2 Parent-child contribution

Every child must have an explainable contribution to its parent.

The relationship must be supported by the child’s purpose, scope and operational description.

A child should not be retained solely because it is historically present or has a plausible name.

5.3 Parent coverage

A parent must be adequately represented by its children where decomposition is required.

The presence of multiple children does not, by itself, demonstrate adequate coverage.

5.4 Decomposition is not determined by arbitrary counts

No fixed number of Activities per Business Process or Tasks per Activity shall be imposed.

A Business Process with two Activities may be valid. Another may require many more.

Likewise, an Activity may legitimately have one Task or several Tasks, depending on its scope and the nature of the work.

The decision must be based on semantic completeness, cohesion, boundaries and operational usefulness.

5.5 Evidence-based reconciliation

Reconciliation must distinguish:

* Verified structural facts.
* Verified operational facts.
* Inferred relationships.
* Proposed corrections.
* Unresolved questions.
* Confirmed absences.
* Approved exceptions.

The absence of evidence must not be treated as evidence of absence.

5.6 Canonical source of truth

Entity YAML or the repository’s established canonical entity representation remains the authoritative source of entity facts and relationships.

README documentation is generated or maintained according to the approved documentation architecture. It must not become an independent source of conflicting operational truth.

6. Reconciliation Requirements

REQ-22-01  -  Catalogue-wide entity inventory

The implementation shall identify and inventory all L0-L4 entities within the catalogue.

For each entity, the inventory shall capture, where supported by the existing model:

* Canonical identifier.
* Entity type.
* Decomposition level.
* Name and description.
* Parent reference.
* Child references.
* Entity status.
* Documentation status.
* Evidence and verification status.
* Existing operational documentation disposition.
* Repository location.

The inventory must identify entities with missing, invalid or ambiguous hierarchy references.

REQ-22-02  -  Structural hierarchy validation

The implementation shall validate the structural integrity of the decomposition.

It must identify:

* L2 entities without valid L1 membership where L1 membership is required.
* L3 Activities without valid L2 parents.
* L4 Tasks without valid L3 parents.
* Invalid parent entity types.
* Invalid child entity types.
* Broken or unresolved references.
* Duplicate parent-child relationships.
* Circular references, if supported by the underlying relationship representation.
* Entities whose declared level conflicts with their actual relationships.
* Entities not included in the expected catalogue hierarchy.

A structural anomaly must be recorded and dispositioned.

REQ-22-03  -  L2-to-L3 decomposition reconciliation

Every L2 Business Process shall be assessed against its assigned L3 Activities.

The reconciliation shall establish:

1. Whether the Activities collectively represent the Business Process’s intended scope.
2. Whether all material functional responsibilities are represented.
3. Whether the Activities have clear and distinct purposes.
4. Whether any significant part of the Business Process remains unrepresented.
5. Whether Activities are duplicated or materially overlapping.
6. Whether Activities have been assigned to the correct parent.
7. Whether Activity boundaries are consistent with the Business Process boundary.
8. Whether Activity inputs and outputs are compatible with the parent process transformation.
9. Whether Activity responsibilities are consistent with the parent responsibility and accountability model.
10. Whether applicable rules, controls, exceptions and dependencies are coherently represented.
11. Whether the decomposition is sufficiently detailed to support the intended catalogue use.

The reconciliation must identify missing functional coverage separately from missing documentation.

REQ-22-04  -  L3-to-L4 decomposition reconciliation

Every L3 Activity shall be assessed against its assigned L4 Tasks.

The reconciliation shall establish:

1. Whether the Tasks adequately represent the Activity’s intended work.
2. Whether each Task has a clear contribution to its parent Activity.
3. Whether Task boundaries are sufficiently clear.
4. Whether Tasks represent bounded units of work rather than vague responsibilities.
5. Whether expected results and completion conditions are understandable.
6. Whether Task responsibilities and relevant authorization requirements are represented where known.
7. Whether applicable inputs, outputs, rules, controls and evidence are consistent with the Activity.
8. Whether Tasks are duplicated or unnecessarily fragmented.
9. Whether significant Activity work remains unrepresented.
10. Whether the Activity should be further decomposed or legitimately retained without further decomposition.

An Activity shall not be considered incomplete merely because it has no Tasks. Its decomposition readiness and disposition must determine whether additional decomposition is warranted.

REQ-22-05  -  Child-to-parent contribution validation

Every L3 Activity and L4 Task shall have an explicit, explainable contribution to its immediate parent.

The contribution should answer:

* What responsibility or work does this child represent?
* Why does this work belong to this parent?
* Which part of the parent’s purpose or transformation does it support?
* What would be missing from the parent if this child were removed?

The answer must be supported by the canonical entity description and available evidence.

A child with no defensible contribution must be flagged for review.

REQ-22-06  -  Parent-to-child coverage validation

Every decomposed parent shall be assessed for coverage of its material scope and responsibilities.

For L2, this concerns the completeness of the Activity decomposition.

For L3, this concerns the completeness of the Task decomposition where Tasks are applicable.

The assessment must identify:

* Covered responsibilities.
* Partially covered responsibilities.
* Uncovered responsibilities.
* Responsibilities requiring additional evidence.
* Responsibilities intentionally excluded.
* Approved gaps or exceptions.

The reconciliation must not assume that a list of children automatically constitutes complete coverage.

REQ-22-07  -  Functional responsibility integrity

The reconciliation shall distinguish:

* Functional responsibility.
* Functional composition.
* Functional dependency.
* Execution sequence.
* Lifecycle relationship.

The existence of a relationship between two Activities or Tasks must not automatically imply that one executes before the other.

The reconciliation must identify cases where entities appear to have been decomposed according to:

* A presumed execution sequence.
* A chronological narrative.
* A system navigation path.
* A workflow implementation.
* A departmental organisation chart.

These may be useful contextual references, but they do not independently establish valid functional decomposition.

REQ-22-08  -  Boundary and scope consistency

Parent and child boundaries shall be compared.

The reconciliation must identify:

* Child scope outside the parent’s boundary.
* Parent responsibilities not represented by children.
* Overlapping boundaries between siblings.
* Unclear ownership of shared responsibilities.
* Duplicated responsibility across separate branches.
* Inconsistent inclusion and exclusion statements.
* Unresolved boundary dependencies.

Where responsibilities legitimately span multiple parents, the relationship must be represented using an approved metamodel mechanism rather than by creating an ambiguous or misleading hierarchy.

REQ-22-09  -  Input, output and transformation consistency

The reconciliation shall compare relevant operational semantics across the hierarchy.

It must distinguish:

* Inputs from resources.
* Outputs from outcomes.
* Transformation from workflow.
* Interfaces from dependencies.
* Internal work products from externally consumed outputs.

For example, an Activity’s outputs should be explainable in the context of its parent Business Process. Similarly, Task results should contribute to the Activity’s intended work.

The reconciliation must identify contradictory or unexplained operational definitions.

REQ-22-10  -  Responsibility and accountability consistency

The reconciliation shall assess whether responsibility and accountability are coherent across levels.

It must identify:

* Children with responsibilities unrelated to the parent.
* Conflicting ownership assignments.
* Unclear accountability boundaries.
* Inconsistent performer and owner definitions.
* Unsubstantiated inheritance of parent responsibilities.
* Responsibilities assigned to inappropriate entity types.

The rules established under EXT-13 remain authoritative.

No automatic inheritance of responsibility or accountability shall be introduced through reconciliation.

REQ-22-11  -  Rules, controls and exception consistency

The reconciliation shall identify inconsistencies in the representation of:

* Business rules.
* Controls.
* Control ownership.
* Exceptions.
* Deviations.
* Evidence requirements.

It must not assume that every parent rule applies to every child.

Applicability must be established or explicitly recorded as unresolved.

EXT-14 remains the authoritative semantic basis for these concepts.

REQ-22-12  -  Duplicate and overlapping entity detection

The implementation shall identify potential duplicates and materially overlapping entities.

Detection may use:

* Canonical identifiers.
* Names and aliases.
* Purpose and descriptions.
* Functional responsibility.
* Boundaries.
* Inputs and outputs.
* Parent-child context.
* Operational evidence.

The system may flag potential duplicates, but it must not automatically merge or delete entities based solely on similarity.

Each case must be reviewed and dispositioned.

REQ-22-13  -  Orphaned and misplaced entity resolution

The reconciliation shall identify entities that:

* Have no valid parent.
* Have an inappropriate parent.
* Are referenced by no expected parent.
* Are included in multiple incompatible hierarchy branches.
* Are incorrectly classified by decomposition level.
* Have become disconnected from their intended process scope.

Each identified entity must be assigned an approved remediation or disposition.

REQ-22-14  -  Granularity and decomposition quality assessment

The reconciliation shall assess whether decomposition is at an appropriate level of detail.

Indicators of potential problems include:

Overly broad Activity

* Represents several unrelated responsibilities.
* Has unclear boundaries.
* Contains multiple independently meaningful bodies of work.
* Cannot be adequately understood or assessed as a cohesive unit.

Overly narrow Activity

* Represents a single trivial action better understood as a Task.
* Has no meaningful independent functional identity.
* Exists primarily to accommodate an artificial hierarchy.

Overly broad Task

* Combines several independently meaningful units of work.
* Has multiple unrelated completion conditions.
* Cannot be independently understood or verified.

Overly narrow Task

* Represents an insignificant sub-action without independent business meaning.
* Exists solely because of implementation or workflow sequencing.
* Creates unnecessary catalogue complexity.

These indicators trigger review; they are not automatic deletion or restructuring rules.

REQ-22-15  -  L0 Process Scope reconciliation

Every L0 Process Scope shall be assessed against the L1 Process Groups and associated L2 Business Processes.

The reconciliation shall establish:

* Scope purpose.
* Included and excluded areas.
* L1 membership.
* Coverage of relevant process domains.
* Overlaps with other scopes.
* Unrepresented areas.
* Ambiguous or conflicting boundaries.

The assessment must determine whether the scope remains meaningful and whether its constituent groups adequately represent it.

REQ-22-16  -  L1 Process Group reconciliation

Every L1 Process Group shall be assessed against its member L2 Business Processes.

The assessment shall establish:

* Grouping rationale.
* Membership criteria.
* Process inclusion and exclusion.
* Internal coherence of the group.
* Duplicate or overlapping membership.
* Processes assigned to inappropriate groups.
* Unassigned L2 Processes.
* Potential gaps in the process landscape.

A Process Group is a classification and organisational construct, not an executable process.

REQ-22-17  -  Reconciliation disposition

Every in-scope entity and every identified reconciliation issue shall receive an explicit disposition.

The programme shall support the following proposed disposition vocabulary:

Disposition	Meaning
verified_complete	Reconciliation completed and no material unresolved gap remains.
verified_with_gaps	Reconciliation completed, with identified gaps accepted or retained for subsequent action.
awaiting_evidence	Additional evidence is required before a defensible conclusion can be reached.
awaiting_owner_review	Business owner or authorised reviewer confirmation is outstanding.
requires_structural_remediation	Structural changes are required.
not_applicable	A reconciliation requirement does not apply, with rationale.
deferred_with_approval	Work is intentionally deferred with an approved rationale and accountable authority.

The disposition of an entity must not obscure the disposition of individual issues affecting it.

REQ-22-18  -  Evidence and provenance

All material reconciliation decisions must be traceable to evidence or an explicitly recorded rationale.

The framework established under EXT-15 shall be reused.

Evidence shall support:

* Parent-child assignment.
* Functional contribution.
* Decomposition completeness.
* Duplicate resolution.
* Boundary decisions.
* Granularity decisions.
* Structural remediation.
* Approved exceptions.

AI-assisted identification or similarity detection may support review, but cannot independently verify business semantics or approve changes.

REQ-22-19  -  Reconciliation reporting

The catalogue shall provide a consolidated reconciliation report.

The report must include:

* Total entities by level.
* Valid and invalid hierarchy references.
* L2 processes assessed.
* L3 Activities assessed.
* L4 Tasks assessed.
* L2 processes with inadequate Activity decomposition.
* Activities with inadequate Task decomposition.
* Children with unclear parent contribution.
* Orphaned entities.
* Potential duplicates.
* Boundary conflicts.
* Granularity issues.
* Outstanding evidence requirements.
* Owner-review requirements.
* Approved deferrals.
* Structural remediation actions.
* Overall reconciliation completion status.

Where possible, the report should distinguish structural completeness from semantic completeness and documentation completeness.

REQ-22-20  -  Canonical entity and documentation alignment

Approved reconciliation changes shall be reflected in the canonical entity representation.

The corresponding documentation must be generated or updated using the approved EXT-10, EXT-11 and EXT-17 architecture.

The implementation must not introduce conflicting information between:

* Entity YAML.
* README documentation.
* Catalogue indexes.
* Relationship references.
* Reconciliation reports.

REQ-22-21  -  Controlled remediation

All structural and semantic corrections shall follow repository governance.

Remediation must:

* Preserve canonical identifiers unless an approved change requires otherwise.
* Maintain valid references.
* Record material changes.
* Preserve evidence and provenance.
* Update affected parent and child entities.
* Regenerate affected documentation.
* Pass the applicable validation checks.
* Receive the required review and approval.

No destructive merge, deletion or reassignment shall occur without an explicit approved decision.

REQ-22-22  -  EXT-23 readiness assessment

The reconciliation shall produce a formal readiness assessment for EXT-23.

The assessment must identify:

* Requirements that can be enforced automatically.
* Requirements that require human review.
* Requirements that can only be assessed through evidence.
* Requirements that remain deferred.
* Known limitations.
* Approved exceptions.
* Residual structural and semantic risks.

EXT-23 must not introduce automated enforcement of unresolved semantic rules simply because they have been expressed as requirements in EXT-22.

7. Mandatory L2-L4 Reconciliation Matrix

7.1 Purpose

The L2-L4 Reconciliation Matrix is the principal controlled artefact of this CR.

It provides a consolidated view of the relationship between Business Processes, Activities and Tasks.

It must support both top-down and bottom-up assessment.

7.2 Required logical structure

The matrix must support, at minimum, the following information:

Field	Description
Reconciliation ID	Unique identifier for the reconciliation record.
L2 Process ID	Canonical identifier of the Business Process.
L2 Process Name	Business Process name.
L2 Purpose	Concise statement of the intended transformation or result.
L2 Boundary	Relevant process scope and boundaries.
L3 Activity ID	Canonical identifier of the Activity.
L3 Activity Name	Activity name.
L3 Purpose	Intended Activity contribution.
L3 Parent Contribution	Explanation of how the Activity contributes to the L2 Process.
L3 Coverage Assessment	Assessment of how the Activity contributes to the parent process coverage.
L4 Task ID	Canonical identifier of the Task.
L4 Task Name	Task name.
L4 Purpose	Intended bounded unit of work.
L4 Parent Contribution	Explanation of how the Task contributes to its Activity.
L4 Coverage Assessment	Assessment of how Tasks collectively represent the Activity where applicable.
Boundary Alignment	Alignment between parent and child boundaries.
Operational Alignment	Alignment of relevant inputs, outputs, responsibilities and other operational semantics.
Structural Status	Valid, invalid or unresolved hierarchy relationship.
Semantic Status	Verified, partially verified, unresolved or conflicting.
Granularity Assessment	Appropriate, potentially broad, potentially narrow or unresolved.
Evidence References	References to evidence supporting the assessment.
Identified Issues	Reconciliation issues associated with the relationship.
Required Action	Remediation or follow-up action.
Issue Owner	Responsible party for resolution.
Disposition	Approved reconciliation disposition.
Review Status	Review and approval state.

The matrix may use multiple linked records or normalised datasets rather than a single flat spreadsheet, provided all required relationships and assessments remain accessible.

7.3 Matrix coverage rules

The matrix must support these scenarios:

Scenario A  -  L2 with multiple L3 Activities and multiple L4 Tasks

All Activities and Tasks must be traceable through their immediate parents to the L2 Process.

Scenario B  -  L2 with Activities but no Tasks

The Activities must still be reconciled with the Business Process. Task-level absence must be evaluated through EXT-20 decomposition readiness and EXT-21 findings.

Scenario C  -  L3 Activity with no L4 Tasks

The Activity must have an explicit decomposition disposition. It must not be automatically treated as structurally defective.

Scenario D  -  L2 without L3 Activities

The Business Process must be flagged for structural and semantic assessment. A legitimate exception requires explicit justification and approval.

Scenario E  -  L3 Activity with no clear contribution to its L2 parent

The Activity must be flagged for reassignment, clarification, structural remediation or another approved disposition.

Scenario F  -  L4 Task with no clear contribution to its L3 parent

The Task must be reviewed for misclassification, reassignment, duplication or removal.

Scenario G  -  Potentially duplicated Activities or Tasks

The matrix must link the affected entities and record the decision, without automatically merging them.

Scenario H  -  Shared or cross-cutting responsibility

The matrix must identify the relationship and determine whether the existing metamodel supports an appropriate cross-reference without compromising the hierarchy.

7.4 Matrix as a controlled artefact

The matrix must have:

* A defined canonical location in the repository or approved programme documentation area.
* A documented schema or column contract.
* A version and generation date.
* A traceable source entity inventory.
* Reconciliation ownership.
* A defined update and review process.
* Reproducible generation where tooling supports it.

The matrix must not become a manually maintained alternative source of truth for process entity data.

Where generated, it must be reproducible from canonical entities and controlled reconciliation records.

8. Reconciliation Methodology

The implementation shall follow the sequence below.

Phase 1  -  Establish baseline

1. Inventory all L0-L4 entities.
2. Extract parent-child relationships.
3. Identify structural anomalies.
4. Record current entity and documentation status.
5. Establish baseline counts and known issues.

Phase 2  -  Reconcile L2-L3

1. Select an L2 Business Process.
2. Review its purpose, scope, boundaries and operational semantics.
3. Identify all assigned L3 Activities.
4. Assess each Activity’s contribution.
5. Assess collective Activity coverage.
6. Identify missing responsibilities and overlaps.
7. Record evidence and unresolved questions.
8. Assign issue dispositions and remediation actions.

Phase 3  -  Reconcile L3-L4

1. Select an L3 Activity.
2. Review its purpose, boundaries and contribution to its parent.
3. Identify assigned L4 Tasks.
4. Assess each Task’s contribution.
5. Assess collective Task coverage where decomposition is applicable.
6. Identify Tasks that are too broad, too narrow or misplaced.
7. Identify Activities requiring further decomposition.
8. Record evidence, gaps and disposition.

Phase 4  -  Reconcile operational semantics

Compare parent and child representations of:

* Inputs.
* Transformation.
* Outputs.
* Outcomes.
* Interfaces.
* Dependencies.
* Responsibilities.
* Accountability.
* Rules.
* Controls.
* Exceptions.
* Metrics.
* Evidence.

The comparison must respect the applicability of each concept at each decomposition level.

Phase 5  -  Reconcile L0-L1 context

1. Review each L0 Process Scope.
2. Review its constituent L1 Process Groups.
3. Verify the relationship between groups and L2 Processes.
4. Identify missing or inappropriate membership.
5. Review overlapping scopes and groupings.
6. Confirm the process landscape is meaningfully represented.

Phase 6  -  Remediate and validate

1. Prioritise identified issues.
2. Obtain required business and domain reviews.
3. Approve structural changes.
4. Update canonical entities and references.
5. Regenerate documentation.
6. Run structural and semantic validation.
7. Update reconciliation dispositions.
8. Recalculate catalogue-wide reports.

Phase 7  -  Programme closure and EXT-23 readiness

1. Review unresolved issues.
2. Confirm approved deferrals and exceptions.
3. Evaluate reconciliation completeness.
4. Assess conformance automation readiness.
5. Produce the EXT-23 readiness report.
6. Obtain programme closure approval.

9. Work Packages

Work Package	Description	Primary output
WP-22-01	Catalogue inventory and baseline	L0-L4 inventory and baseline report
WP-22-02	Structural hierarchy validation	Structural integrity report
WP-22-03	L2-L3 reconciliation	L2-L3 reconciliation records
WP-22-04	L3-L4 reconciliation	L3-L4 reconciliation records
WP-22-05	Operational semantic alignment	Parent-child semantic assessment
WP-22-06	Duplicate and overlap analysis	Duplicate and overlap register
WP-22-07	Orphan and misplaced entity resolution	Structural remediation register
WP-22-08	Granularity assessment	Decomposition quality register
WP-22-09	L0-L1 reconciliation	Process landscape reconciliation report
WP-22-10	Canonical updates and remediation	Updated entity representations
WP-22-11	Matrix and reporting implementation	L2-L4 Reconciliation Matrix
WP-22-12	Validation and EXT-23 readiness	Final reconciliation and readiness report

10. Tooling and Automation Requirements

The implementation shall reuse the tooling established under EXT-17 wherever possible.

New tooling should be introduced only where a verified gap exists.

10.1 Automated checks

The implementation should automate checks that can be evaluated deterministically, including:

* Entity existence.
* Canonical identifier uniqueness.
* Parent reference validity.
* Allowed parent-child entity types.
* Missing required references.
* Duplicate relationship records.
* Invalid decomposition-level declarations.
* Broken cross-references.
* Required reconciliation fields.
* Disposition completeness.
* Evidence reference integrity.
* README and canonical entity alignment.

10.2 Assisted semantic checks

Tooling may assist with:

* Similarity detection.
* Potential duplicate identification.
* Parent-child contribution prompts.
* Missing coverage indicators.
* Boundary overlap indicators.
* Potential granularity issues.
* Operational semantic inconsistency detection.

These checks must be treated as review prompts, not authoritative conclusions.

10.3 Human review

Human review is mandatory for:

* Business meaning.
* Functional contribution.
* Completeness of responsibility coverage.
* Duplicate resolution.
* Reassignment of entities.
* Granularity decisions.
* Boundary decisions.
* Approved exceptions.
* Final reconciliation approval.

10.4 Reporting

The tooling should produce a machine-readable report and a human-readable summary.

The report should support filtering by:

* Decomposition level.
* Parent process.
* Entity.
* Structural issue.
* Semantic issue.
* Evidence status.
* Disposition.
* Review status.
* Remediation owner.

11. Quality Gates

The following gates govern acceptance.

Gate	Description	Exit condition
G22-01	Inventory completeness	All in-scope L0-L4 entities inventoried.
G22-02	Structural integrity	All structural anomalies identified and dispositioned.
G22-03	L2-L3 reconciliation	Every in-scope L2 Process assessed against its Activities.
G22-04	L3-L4 reconciliation	Every in-scope Activity assessed against its Tasks or explicitly dispositioned.
G22-05	Semantic consistency	Material parent-child inconsistencies identified and dispositioned.
G22-06	Duplicate and granularity review	All identified material cases reviewed and dispositioned.
G22-07	Contextual reconciliation	L0 and L1 scope and membership reconciled.
G22-08	Evidence and approval	Material decisions supported by evidence or approved rationale.
G22-09	Canonical consistency	Entity representations, references and documentation aligned.
G22-10	EXT-23 readiness	Conformance requirements and unresolved limitations documented.

An unresolved issue may remain only where its status, impact, owner, rationale and approved disposition are recorded.

12. Acceptance Criteria

EXT-22 shall be considered complete when:

AC-22-01  -  A complete inventory of all in-scope L0-L4 entities exists.

AC-22-02  -  Structural parent-child integrity has been assessed across the catalogue.

AC-22-03  -  Every in-scope L2 Business Process has an L2-L3 decomposition assessment.

AC-22-04  -  Every in-scope L3 Activity has an L3-L4 decomposition assessment or an explicit approved disposition explaining why further decomposition is not applicable or is deferred.

AC-22-05  -  Every L3 Activity has a defensible contribution to its assigned L2 Business Process, or an explicitly recorded issue and disposition.

AC-22-06  -  Every L4 Task has a defensible contribution to its assigned L3 Activity, or an explicitly recorded issue and disposition.

AC-22-07  -  Parent-to-child coverage gaps have been identified and assessed.

AC-22-08  -  Material boundary and operational semantic inconsistencies have been identified and dispositioned.

AC-22-09  -  Potential duplicates and overlapping entities have been reviewed, with approved outcomes recorded.

AC-22-10  -  Orphaned and misplaced entities have been resolved or formally dispositioned.

AC-22-11  -  Granularity concerns have been assessed without imposing arbitrary entity-count requirements.

AC-22-12  -  L0 Process Scopes and L1 Process Groups have been reconciled with the L2 process landscape.

AC-22-13  -  The L2-L4 Reconciliation Matrix is available as a controlled and traceable programme artefact.

AC-22-14  -  Material reconciliation decisions have evidence, provenance or approved rationale.

AC-22-15  -  Canonical entity representations and generated documentation reflect approved reconciliation decisions.

AC-22-16  -  Structural and deterministic validation checks pass, except for explicitly approved and documented exceptions.

AC-22-17  -  Outstanding issues have accountable owners, impact assessments and dispositions.

AC-22-18  -  An EXT-23 readiness assessment has been completed and reviewed.

AC-22-19  -  The final reconciliation report demonstrates the status of the entire catalogue rather than reporting only successfully completed entities.

13. Risks and Mitigations

Risk	Impact	Mitigation
Artificial decomposition to satisfy hierarchy expectations	Unnecessary catalogue complexity	Do not mandate minimum child counts.
Incorrect automated semantic inference	Invalid business model	Require human review and evidence.
Duplicate entities merged prematurely	Loss of traceability and meaning	Require explicit approval and migration records.
README and YAML become inconsistent	Conflicting sources of truth	Preserve canonical entity data and deterministic generation.
Parent-child relationships imply execution order	Workflow semantics contaminate the model	Explicitly distinguish functional decomposition from sequencing.
Incomplete evidence is mistaken for completeness	False assurance	Use explicit uncertainty and disposition states.
Excessive remediation scope	Programme delay	Prioritise material issues and use approved deferrals.
Inconsistent treatment of shared responsibilities	Incorrect ownership and hierarchy	Use metamodel-approved cross-references.
Existing repository conventions are overlooked	Unnecessary schema and tooling changes	Inventory current implementation before prescribing changes.

14. Dependencies and Related CRs

CR	Relationship
EXT-08	Documentation architecture reconciliation
EXT-09	Operational documentation semantic contract
EXT-10	Operational entity schema alignment
EXT-11	Decomposition-level documentation profiles
EXT-12	Inputs, outputs and interface semantics
EXT-13	Responsibility and accountability model
EXT-14	Rules, controls and exception semantics
EXT-15	Evidence, provenance and confidence
EXT-16	Operational authoring and research methodology
EXT-17	Enrichment tooling and backfill orchestration
EXT-18	Operational documentation pilot
EXT-19	L2 Business Process backfill
EXT-20	L3 Activity backfill
EXT-21	L4 Task backfill
EXT-22	Cross-level decomposition reconciliation
EXT-23	Operational documentation conformance gates
EXT-24	Catalogue closure and continuous governance

15. ADR Considerations

EXT-22 should reuse the decisions established under the operational documentation ADR series.

Any new architectural decision identified during implementation should be raised separately rather than embedded as an undocumented implementation assumption.

Potential ADR subjects include:

* Whether reconciliation records are stored as canonical repository entities, controlled programme artefacts or generated reports.
* Whether parent-child contribution assessments require a controlled vocabulary.
* Whether decomposition coverage can be represented through explicit responsibility-to-child mappings.
* Whether reconciliation status is stored on canonical entities or maintained in a separate governance record.
* Whether approved exceptions have a standard lifecycle and review period.

These decisions must be assessed against the existing metamodel and repository architecture before new structures are introduced.

16. Expected Deliverables

The implementation must produce:

1. Complete L0-L4 entity inventory.
2. Baseline structural integrity report.
3. L2-L3 reconciliation records.
4. L3-L4 reconciliation records.
5. L2-L4 Reconciliation Matrix.
6. L0-L1 contextual reconciliation report.
7. Duplicate and overlap register.
8. Orphaned and misplaced entity register.
9. Decomposition granularity assessment.
10. Parent-child semantic consistency report.
11. Structural remediation register.
12. Approved reconciliation decisions and evidence references.
13. Updated canonical entity representations where required.
14. Regenerated documentation where affected.
15. Automated validation results.
16. Catalogue-wide reconciliation status report.
17. EXT-23 readiness assessment.

17. Definition of Done

EXT-22 is complete when the catalogue has been assessed as a connected process decomposition rather than a collection of individually documented entities.

Every in-scope entity must have a verified or explicitly dispositioned place in the hierarchy.

Every material parent-child relationship must have a defensible semantic basis.

Every decomposed parent must have an assessed level of child coverage.

Every structural, semantic, duplication, granularity and boundary issue must be resolved or explicitly dispositioned.

The reconciliation matrix must provide a traceable record of these decisions.

The resulting catalogue must be suitable for the introduction of EXT-23 conformance gates without concealing unresolved semantic or structural weaknesses.

The completion of EXT-22 establishes the first programme-wide reconciled baseline of the Business Process catalogue.




18. Implementation Recommendation

Implement EXT-22 in the following order:

1. Inventory before modification: establish the actual repository structure, canonical entity representation, existing parent-child references, generation tooling and validation conventions.
2. Build the reconciliation dataset: extract L0-L4 entities and relationships without modifying source entities.
3. Run structural checks: identify invalid references, orphans, duplicate identifiers and level mismatches.
4. Generate the initial L2-L4 Reconciliation Matrix: establish a complete baseline before conducting semantic review.
5. Conduct L2-L3 review: validate Business Process coverage and Activity contribution.
6. Conduct L3-L4 review: validate Activity coverage and Task contribution.
7. Reconcile L0-L1: validate scope and group membership.
8. Resolve issues: update canonical entities only after the relevant decisions are approved.
9. Regenerate and validate: ensure all affected documentation and references remain consistent.
10. Produce the closure report: establish the final catalogue baseline and EXT-23 readiness.

Important implementation constraint

Do not start by creating a new reconciliation schema or introducing additional fields into every process entity.

First establish whether the existing entity model, evidence framework, repository metadata and CI tooling can already support the required reconciliation records.

Only introduce new canonical fields, schemas or relationship types where an explicit gap has been demonstrated and the change has been approved.

This prevents EXT-22 from creating a parallel governance model that duplicates the work of EXT-10 through EXT-17.

---

## 19. The recommended programme decision (from the EXT-23 attachment, verbatim)

Recommended programme decision

I recommend treating EXT-22 as a mandatory exit gate between enrichment and conformance enforcement.

There is one particularly important distinction to preserve: a catalogue can pass structural validation while still having poor functional decomposition. EXT-23 should therefore enforce deterministic structural rules automatically, but semantic adequacy should remain evidence-led and subject to appropriate human review.

The next logical step is EXT-23, but before drafting it, the reconciliation matrix’s canonical storage and generation approach should be settled against the actual repository conventions. That avoids designing conformance gates around a reporting artefact that has not yet been operationalised.