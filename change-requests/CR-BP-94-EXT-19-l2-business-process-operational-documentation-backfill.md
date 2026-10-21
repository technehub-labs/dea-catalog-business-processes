# CR-BP-94-EXT-19: L2 Business Process Operational Documentation Backfill

**Status**: Proposed
**Layer**: Process Catalog (Cross-Cutting Documentation)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-19
**Source CR**: CR-BP-94-EXT-19 (L2 Business Process Operational Documentation Backfill)
**Parent programme**: CR-BP-94: Process Decomposition and Operational Documentation (DEA-PROCESS-ENRICH-000)
**Repository**: technehub-labs/dea-catalog-business-processes
**Change type**: Catalogue enrichment, documentation and data quality
**Target decomposition level**: L2: Business Process
**Priority**: Critical
**Depends on**: CR-BP-94-EXT-15, CR-BP-94-EXT-16, CR-BP-94-EXT-17, CR-BP-94-EXT-18
**Enables**: EXT-20 (L3 Activity Backfill)
**Implementation approach**: Inventory, assess, enrich, validate, review and report

---

## 1. Executive summary

This Change Request establishes the systematic operational documentation backfill of all in-scope L2 Business Process entities in the Business Process catalogue.

L2 is the principal decomposition level at which a complete business transformation is represented. Its documentation must therefore establish a sufficiently clear understanding of:

- What business purpose the process serves
- What transformation it performs
- Where its operational boundaries lie
- What triggers or conditions initiate it
- What information and other business objects it consumes
- What outputs it produces
- Which roles and authorities are responsible
- Which rules, controls and exceptions apply
- Which business and information-system interfaces support it
- How its performance can be measured
- How its decomposition into L3 Activities contributes to the transformation

The backfill shall use canonical entity data as its source of truth. README documentation shall be generated from that data using the approved documentation templates and tooling.

The CR does not authorize the invention of undocumented operating procedures or the creation of unsupported process semantics.

---

## 2. Background and rationale

The Business Process catalogue has an established decomposition structure:

| Level | Entity type | Primary purpose |
|---|---|---|
| L0 | Process Context | Establish the process landscape and scope |
| L1 | Process Group | Organize related processes |
| L2 | Business Process | Represent a complete business transformation |
| L3 | Activity | Represent a cohesive body of work contributing to a process |
| L4 | Task | Represent a bounded, independently understandable unit of work |

Existing entity records and README documentation do not necessarily provide consistent operational detail.

The preceding CRs establish the prerequisites for resolving this:

- EXT-10 establishes schema alignment
- EXT-11 establishes decomposition-aware documentation profiles
- EXT-12 establishes input, output and interface semantics
- EXT-13 establishes responsibility and accountability semantics
- EXT-14 establishes business rule, control and exception semantics
- EXT-15 establishes evidence, provenance and confidence
- EXT-16 establishes the research and authoring methodology
- EXT-17 establishes enrichment and validation tooling
- EXT-18 validates the approach through a controlled pilot (the GO decision authorised EXT-19 on 2026-10-19)

EXT-19 applies those standards to the L2 catalogue.

---

## 3. Objectives

The implementation shall:

1. Establish a complete inventory of L2 Business Process entities
2. Assess every in-scope entity against the approved L2 documentation profile
3. Enrich operational information using credible evidence
4. Establish clear process boundaries and business transformations
5. Identify and document relevant operational inputs and outputs
6. Establish process responsibility and accountability where supported
7. Identify applicable rules, controls, exceptions and dependencies
8. Establish traceability to relevant enterprise architecture entities
9. Reconcile each process with its L3 Activity decomposition
10. Generate consistent README documentation
11. Establish an auditable catalogue-level completion report

---

## 4. Scope

### 4.1 In scope

All L2 Business Process entities identified through the repository inventory.

The inventory shall establish:

- Entity identifier
- Entity name
- Parent L1 Process Group, where applicable
- Existing child L3 Activities
- Existing README
- Existing operational fields
- Existing references to other catalogues
- Current schema and documentation conformance
- Evidence and review status
- Backfill priority and disposition

### 4.2 Out of scope

This CR shall not:

- Redesign the business process taxonomy
- Change the fundamental meaning of existing process entities
- Create unsupported operating procedures
- Introduce workflow execution semantics
- Redefine Business Functions or Business Capabilities
- Duplicate Information System or Information Systems Function definitions
- Replace authoritative policy, risk, control or metric catalogues
- Automatically create missing L3 or L4 entities
- Force every L2 entity to contain every optional operational field

Structural changes identified during backfill shall be recorded and addressed through the appropriate CR.

---

## 5. Normative implementation requirements

### REQ-19-01: L2 catalogue inventory

Produce an authoritative inventory of all L2 Business Process entities.

The inventory must be derived from the repository, not from a manually assembled or assumed list.

Each entity shall receive a unique inventory record or equivalent traceable reference.

### REQ-19-02: Profile assessment

Every in-scope entity shall be assessed against the approved L2 documentation profile from EXT-11.

The assessment shall distinguish:

- Required content
- Conditional content
- Optional content
- Not-applicable content
- Inherited or referenced content

A field shall not be treated as missing merely because it is not applicable.

### REQ-19-03: Process identity and purpose

Each L2 entity shall have an operationally meaningful description of its business purpose.

The description must communicate the business need or result served by the process.

A restatement of the entity name is insufficient.

### REQ-19-04: Business transformation

Each L2 entity shall describe its transformation.

The transformation must explain what business-relevant change, assessment, decision, service or result the process produces.

It must not merely list activities or tasks.

The transformation should identify, where applicable:

- The starting business condition
- The business object or subject being transformed
- The nature of the transformation
- The resulting business state or deliverable
- The value or business purpose of the transformation

This description must not imply a mandatory execution sequence.

### REQ-19-05: Process scope and boundary

Each L2 process shall have a clearly understood boundary.

The documentation shall assess:

- Included business responsibilities
- Excluded responsibilities
- Starting boundary
- Ending boundary
- Upstream dependencies
- Downstream consumers or dependencies
- Relationship to the parent L1 Process Group

The process boundary must not be defined solely by the organisational department that currently performs the work.

### REQ-19-06: Trigger and preconditions

Where applicable and supported by evidence, document:

- Initiating events
- Business triggers
- Preconditions
- Eligibility or authorization conditions
- Relevant timing or periodicity

Triggers and preconditions must remain distinct.

A process trigger is not necessarily the first execution step.

### REQ-19-07: Inputs

Each process shall be assessed for relevant inputs.

Where applicable, input documentation should identify:

- Name and description
- Input type
- Source
- Business purpose
- Required or conditional status
- Acceptance criteria
- Validation expectations
- Provenance

Inputs must be distinguished from:

- Resources
- Applications
- Infrastructure
- Organizational roles
- Upstream process dependencies

Existing inputs fields must be reconciled with the approved EXT-10 schema rather than duplicated.

### REQ-19-08: Transformation

The transformation description shall explain the substantive business activity represented by the process.

Where the process performs multiple related transformations, the description must represent the coherent business transformation without turning into an activity inventory.

The L3 decomposition should provide the supporting work structure.

### REQ-19-09: Outputs

Each process shall be assessed for its produced outputs.

Where applicable, document:

- Output name
- Description
- Output type
- Intended consumer
- Acceptance criteria
- Relevant quality characteristics
- Provenance

Outputs must be distinguished from wider business outcomes.

### REQ-19-10: Outcomes

Where the process contributes to a measurable or identifiable business outcome, document the relationship.

An outcome must not be represented as a direct process output unless it is genuinely produced by the process.

Where outcome attribution is shared across multiple processes, avoid claiming exclusive causation.

### REQ-19-11: Business interfaces

Identify relevant interfaces with:

- Other Business Processes
- Business Functions
- Business Capabilities
- Organizational roles or units
- External parties
- Other relevant business entities

The catalogue shall use canonical references where the target entities exist.

### REQ-19-12: Information and system interfaces

Identify relevant information and system interactions where evidence supports them.

These may include:

- Information Systems
- Information Systems Functions
- Data entities or information products
- Integration interfaces
- External system interactions

System names shall not be used as substitutes for process descriptions.

Information Systems and Information Systems Functions must be referenced using their canonical entities when available.

### REQ-19-13: Dependencies

Document material dependencies where they are relevant to understanding the process.

Distinguish:

- Structural decomposition
- Business dependency
- Information dependency
- System dependency
- Resource dependency
- External dependency

Dependencies must not be represented as parent-child decomposition relationships unless they actually are part of the decomposition structure.

### REQ-19-14: Responsibility and accountability

Assess and document:

- Process owner
- Responsible roles
- Accountable authority
- Relevant performers
- Decision authorities
- Consulted and informed parties, where applicable

Use the canonical EXT-13 model.

Do not confuse:

- Role with organizational unit
- Performer with accountable authority
- Responsibility with accountability
- Business Function with individual role

Where ownership cannot be established, record the gap explicitly.

### REQ-19-15: Business rules

Identify applicable business rules and constraints.

Where relevant, reference canonical policy, regulatory or business-rule entities.

Do not reproduce an authoritative policy or rule in the process entity where a reference is sufficient.

### REQ-19-16: Controls

Identify relevant controls where they apply to the process.

Document or reference:

- Control objective
- Relevant risk or obligation
- Control mechanism
- Control type
- Scope
- Responsible authority
- Evidence expectations

Use the EXT-14 semantics.

A process must not be declared compliant merely because a control is referenced.

### REQ-19-17: Exceptions

Where applicable, identify recognized exceptions and their governing conditions.

Distinguish an authorized exception from an observed deviation.

Do not imply that every exception represents a control failure.

### REQ-19-18: Performance measures

Identify relevant canonical Metric entities where available.

A process may be associated with measures covering:

- Quality
- Cost
- Time
- Throughput
- Reliability
- Compliance
- Customer or stakeholder outcomes
- Risk exposure

The process catalogue shall reference canonical Metric entities rather than independently redefining their measurement semantics.

Do not invent performance targets or claim that a metric is currently measured without evidence.

### REQ-19-19: L3 decomposition reconciliation

Every L2 entity shall be reconciled with its available L3 Activities.

The reconciliation shall assess:

- Whether each Activity contributes to the process purpose
- Whether the Activity falls within the process boundary
- Whether the decomposition contains duplication
- Whether the decomposition contains apparent gaps
- Whether Activities are assigned to the correct parent
- Whether the decomposition is coherent and understandable

Missing Activities must be recorded as potential taxonomy or decomposition gaps, not automatically created.

### REQ-19-20: Evidence and provenance

Apply EXT-15 to material operational assertions.

Record evidence source, provenance, confidence and verification status as required by the approved schema.

AI-assisted research shall not be treated as authoritative evidence.

### REQ-19-21: Unknown and deferred information

Where information cannot be established, record the appropriate state:

- Unknown
- Not assessed
- Not applicable
- Deferred
- Inherited or referenced
- Conflicting
- Confirmed absence

Do not use fabricated values or misleading placeholder prose.

### REQ-19-22: Canonical entity update

All accepted operational facts shall be stored in the canonical L2 entity representation.

The existing fields inputs, transformation, outputs, responsibility and boundary shall be retained or migrated according to the approved schema decisions.

Do not introduce parallel fields with overlapping semantics.

### REQ-19-23: README generation

Generate each L2 README from canonical entity data using the approved documentation generator.

Generated documentation shall:

- Reflect the approved L2 profile
- Preserve existing useful documentation content
- Clearly represent applicable evidence status
- Avoid presenting unverified assertions as established facts
- Include relevant canonical cross-references
- Identify documented gaps where appropriate

### REQ-19-24: Entity-level disposition

Every L2 entity shall receive an explicit backfill disposition.

The controlled disposition vocabulary shall support:

- verified_complete
- verified_with_gaps
- awaiting_evidence
- awaiting_owner_review
- requires_structural_remediation
- not_applicable
- deferred_with_approval

These are proposed programme-level status values. Their final representation must follow the repository's canonical schema and governance conventions.

### REQ-19-25: Catalogue reporting

Publish an L2 backfill report covering:

- Total L2 entities
- Entities assessed
- Entities enriched
- Entities verified
- Entities with documented gaps
- Entities awaiting evidence
- Entities awaiting owner review
- Entities requiring structural remediation
- Profile conformance
- Evidence coverage
- Cross-reference validity
- Parent-child reconciliation status
- Outstanding issues

---

## 6. Implementation work packages

| Work package | Deliverable |
|---|---|
| WP-19-01 | L2 inventory and baseline |
| WP-19-02 | L2 profile assessment |
| WP-19-03 | Process purpose, transformation and boundary enrichment |
| WP-19-04 | Inputs, outputs, outcomes and interface enrichment |
| WP-19-05 | Responsibility and accountability enrichment |
| WP-19-06 | Rules, controls, exceptions and dependencies |
| WP-19-07 | Metrics and cross-catalogue references |
| WP-19-08 | Evidence and provenance validation |
| WP-19-09 | L2-to-L3 reconciliation |
| WP-19-10 | README generation and validation |
| WP-19-11 | Human review and disposition |
| WP-19-12 | Catalogue-level reporting |

---

## 7. Quality gates

- Gate 19-A: Inventory completeness (all L2 entities identified)
- Gate 19-B: Semantic completeness (all applicable L2 profile concepts assessed)
- Gate 19-C: Evidence integrity (material assertions have provenance and confidence classification)
- Gate 19-D: Decomposition integrity (L2-to-L3 relationships reconciled)
- Gate 19-E: Documentation integrity (generated READMEs consistent with canonical entity data)
- Gate 19-F: Review and disposition (all entities have approved disposition)

---

## 8. Testing requirements

The implementation must demonstrate:

- All L2 entities can be inventoried
- Valid L2 entities pass applicable schema and profile validation
- Invalid or unsupported assertions are flagged
- Existing operational fields retain their intended semantics
- Evidence references resolve or have explicit unresolved status
- Cross-catalogue references validate
- Parent-child relationships are coherent
- README generation is reproducible
- Migration is idempotent
- No existing entity identifier is unintentionally changed
- Existing documentation is not silently discarded

---

## 9. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Insufficient source material | Record evidence gaps and prioritize owner confirmation |
| Overly broad process descriptions | Apply transformation and boundary criteria |
| Duplication of catalogue concepts | Require canonical references |
| Inconsistent process ownership | Apply EXT-13 |
| Incorrect activity decomposition | Require L2-to-L3 reconciliation |
| AI-generated inaccuracies | Apply EXT-15 and EXT-16 |
| Forced completion | Use explicit dispositions |
| Documentation drift | Generate README from canonical data |

---

## 10. Acceptance criteria

- Complete L2 inventory produced
- All in-scope entities assessed
- Approved L2 profile applied
- Process purpose documented where evidence permits
- Business transformation documented
- Process boundaries reconciled
- Triggers and preconditions assessed
- Inputs and outputs assessed
- Outcomes distinguished from outputs
- Business and information-system interfaces assessed
- Dependencies assessed
- Responsibility and accountability assessed
- Business rules, controls and exceptions assessed
- Relevant Metrics referenced canonically
- Evidence and provenance captured
- L2-to-L3 reconciliation completed
- Canonical entities updated
- README files generated
- Validation and review completed
- Every entity has an explicit disposition
- Catalogue-level L2 report published
- No unsupported operational claims presented as verified

---

## 11. Completion definition

EXT-19 is complete when every in-scope L2 Business Process entity has been assessed, enriched to its evidence-supported level, reconciled with its L3 decomposition, validated, reviewed where required and assigned a documented disposition.

EXT-19 completion authorizes progression to EXT-20 for the relevant L3 population.

---

## 12. References

- `docs/operational-documentation-programme/CR-BP-94-EXT-19-to-20-detailed-design.md` (the detailed design)
- `change-requests/CR-BP-94-EXT-09-operational-documentation-semantic-contract.md` (EXT-09 semantic distinctions)
- `change-requests/CR-BP-94-EXT-10-operational-entity-schema-alignment.md` (EXT-10 schema alignment)
- `change-requests/CR-BP-94-EXT-11-decomposition-level-documentation-profiles.md` (EXT-11 L0-L4 profiles)
- `change-requests/CR-BP-94-EXT-12-process-inputs-outputs-and-interface-semantics.md` (EXT-12 inputs/outputs/interfaces)
- `change-requests/CR-BP-94-EXT-13-process-responsibility-and-accountability-model.md` (EXT-13 responsibility/accountability)
- `change-requests/CR-BP-94-EXT-14-business-rules-controls-and-exception-semantics.md` (EXT-14 business rules/controls/exceptions)
- `change-requests/CR-BP-94-EXT-15-evidence-provenance-and-confidence-framework.md` (EXT-15 evidence/provenance)
- `change-requests/CR-BP-94-EXT-16-operational-authoring-and-research-methodology.md` (EXT-16 methodology)
- `change-requests/CR-BP-94-EXT-17-enrichment-tooling-and-backfill-orchestration.md` (EXT-17 tooling)
- `change-requests/CR-BP-94-EXT-18-operational-documentation-pilot.md` (EXT-18 pilot + GO decision)
- `docs/operational-authoring-methodology.md` (EXT-16)
- `docs/evidence-provenance-confidence.md` (EXT-15)
- `docs/enrichment-tooling-orchestration.md` (EXT-17)
- `docs/operational-documentation-pilot.md` (EXT-18)
- `reconciliation/programme-register.json` (the 17-CR register)
