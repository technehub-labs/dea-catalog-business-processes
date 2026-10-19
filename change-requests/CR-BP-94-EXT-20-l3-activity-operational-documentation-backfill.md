# CR-BP-94-EXT-20: L3 Activity Operational Documentation Backfill

**Status**: Normative (proposed for adoption under CR-BP-94-EXT-20)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-19
**Source CR**: CR-BP-94-EXT-20 (L3 Activity Operational Documentation Backfill)
**Parent programme**: CR-BP-94: Process Decomposition and Operational Documentation (DEA-PROCESS-ENRICH-000)
**Repository**: technehub-labs/dea-catalog-business-processes
**Change type**: Catalogue enrichment, decomposition integrity and documentation
**Target decomposition level**: L3: Activity
**Priority**: High
**Depends on**: EXT-15, EXT-16, EXT-17, EXT-18, EXT-19
**Enables**: EXT-21 (L4 Task Backfill)
**Implementation approach**: Parent readiness, reconciliation, enrichment, validation and review

---

## 1. Executive summary

This Change Request establishes the systematic operational documentation backfill of L3 Activity entities.

L3 Activities represent cohesive bodies of work contributing to an L2 Business Process.

Their documentation must establish:

- The purpose of the Activity
- Its relationship to the parent Business Process
- Its scope and boundaries
- The business contribution it makes
- Its relevant inputs and outputs
- Its responsibilities and performers
- Its applicable rules and controls
- Its dependencies and interfaces
- Its relationship to L4 Tasks where applicable

The L3 layer must provide a meaningful decomposition of the parent process while avoiding duplication of L2 content or inappropriate expansion into L4 execution detail.

---

## 2. Background and rationale

The L2 backfill under EXT-19 establishes the business transformation and operational boundaries of the parent processes.

L3 enrichment must build on that foundation.

An Activity cannot be documented accurately in isolation because its purpose and contribution are determined partly by the business transformation it supports.

The programme must therefore maintain a strong relationship between:

- L2 Business Process
- L3 Activity
- L4 Task

EXT-20 is responsible for establishing the L3 operational layer and preparing the catalogue for subsequent task-level enrichment.

---

## 3. Objectives

1. Establish a complete L3 Activity inventory
2. Validate all L3-to-L2 parent relationships
3. Document Activity purpose and business contribution
4. Establish meaningful Activity boundaries
5. Document relevant operational inputs and outputs
6. Identify applicable responsibilities and controls
7. Establish evidence and provenance for operational assertions
8. Assess Activity cohesion and sibling differentiation
9. Reconcile L3 decomposition with the L2 parent
10. Prepare L3 entities for L4 Task enrichment
11. Generate consistent Activity README documentation

---

## 4. Scope

### 4.1 In scope

All L3 Activity entities in the approved backfill population.

The inventory shall include:

- Activity identifier
- Activity name
- Parent L2 Business Process
- Existing child L4 Tasks
- Existing README
- Existing operational fields
- Existing cross-catalogue references
- Evidence and review status
- Profile completeness
- Backfill disposition

### 4.2 Out of scope

This CR shall not:

- Redefine L2 business transformations
- Introduce new L2 processes without an approved taxonomy change
- Define detailed L4 task execution
- Introduce mandatory workflow sequencing
- Define runtime state, branching or orchestration
- Invent roles, controls or operational dependencies
- Duplicate canonical Business Function, Business Capability, Information System or Metric entities
- Require every Activity to have a fixed number of Tasks

---

## 5. Normative implementation requirements

### REQ-20-01: L3 inventory

Produce an authoritative inventory of all L3 Activity entities.

The inventory must be derived from the actual repository contents.

Every Activity must be associated with its parent L2 entity or explicitly classified as requiring structural remediation.

### REQ-20-02: Parent readiness

Before an Activity is enriched, its parent L2 Business Process must:

- Have been assessed under EXT-19
- Have an accepted operational description
- Have a sufficiently clear transformation and boundary
- Have an explicit disposition
- Have no unresolved parent-level issue that makes the Activity's scope indeterminate

An approved exception may allow enrichment to proceed, but the exception and its rationale must be recorded.

### REQ-20-03: Activity identity and purpose

Every Activity shall have a meaningful description of its purpose.

The description must identify the cohesive body of work represented by the Activity.

It must not merely repeat the Activity name or describe a department, system or job title.

### REQ-20-04: Parent relationship

Every Activity shall reference its canonical parent L2 Business Process.

The relationship must be validated against the repository's identifier and hierarchy conventions.

An Activity must not be assigned to a parent solely because the names appear similar.

### REQ-20-05: Business contribution

Describe how the Activity contributes to the parent's business transformation.

The contribution should explain, where supported:

- What business responsibility the Activity fulfils
- What aspect of the transformation it advances
- What relevant intermediate result it produces
- How its output contributes to the parent process

The description must not imply exclusive responsibility for a shared business outcome without evidence.

### REQ-20-06: Activity boundary

Each Activity shall be assessed for:

- Included work
- Excluded work
- Scope
- Relevant business object or subject
- Inputs and outputs
- Relationship to sibling Activities
- Relationship to its parent L2 boundary

The boundary must distinguish the Activity from adjacent work.

### REQ-20-07: Cohesion

An Activity shall represent a coherent body of work.

The assessment must consider whether the Activity:

- Has a clear purpose
- Contributes to its parent process
- Has an understandable scope
- Is distinguishable from sibling Activities
- Can be decomposed into Tasks where appropriate
- Avoids grouping unrelated work merely for administrative convenience

### REQ-20-08: Inputs and working objects

Identify relevant Activity inputs and working objects where applicable.

These may include:

- Information
- Business records
- Requests
- Documents
- Data products
- Materials
- Other business objects

Distinguish these from resources, systems and organizational roles.

Where an input is already represented at L2, the Activity should reference or contextualize it rather than duplicate it unnecessarily.

### REQ-20-09: Outputs

Document outputs produced by the Activity where applicable.

The output description should identify its contribution to the parent process.

Distinguish:

- Activity-level outputs
- Parent process outputs
- Wider business outcomes

Do not assume every Activity produces a separate externally consumable deliverable.

### REQ-20-10: Responsibility and performers

Identify applicable roles, responsible parties, performers and decision authorities.

Apply the canonical EXT-13 model.

An Activity may involve multiple roles.

Do not infer individual accountability solely from the presence of a performer.

### REQ-20-11: Business rules

Identify relevant business rules and constraints.

Where a rule applies to the parent process and also constrains the Activity, reference the canonical rule and establish its applicability.

Do not create a second version of the rule at L3.

### REQ-20-12: Controls

Identify relevant controls where the Activity is within their scope.

Distinguish controls that operate at:

- Parent process level
- Activity level
- Task level

Do not assume that a parent process control applies identically to every Activity.

### REQ-20-13: Exceptions

Identify relevant Activity-level exceptions where they are supported by evidence.

Distinguish recognized exceptions from deviations.

Do not duplicate parent-level exceptions unless their applicability to the Activity is meaningful.

### REQ-20-14: Interfaces and dependencies

Identify relevant interfaces and dependencies with:

- Other Activities
- Other Business Processes
- Business Functions
- Business Capabilities
- Information Systems
- Information Systems Functions
- External parties
- Relevant information products

The relationship must use approved canonical references and metamodel relationship types.

Do not represent a dependency as decomposition unless it is structurally a parent-child relationship.

### REQ-20-15: L4 Task relationships

Where L4 Tasks exist, reconcile the Task population with the Activity.

The reconciliation shall assess:

- Whether each Task contributes to the Activity purpose
- Whether each Task falls within the Activity boundary
- Whether Tasks overlap
- Whether Task descriptions are sufficiently bounded
- Whether the Activity has unexplained decomposition gaps

This CR shall not prescribe the detailed Task schema or require every Activity to have Tasks. Those matters are addressed by EXT-21.

### REQ-20-16: Evidence and provenance

Apply EXT-15 to material L3 operational assertions.

Record source, provenance, confidence and verification status as required.

AI-generated suggestions must not be presented as verified Activity facts.

### REQ-20-17: Inherited and contextual information

Where information is available at L2 and applies to L3, determine whether it should be:

- Referenced
- Contextualized
- Explicitly restated because it is materially different
- Marked as not applicable

Do not blindly copy parent content into every child entity.

The source and applicability of inherited information must remain traceable.

### REQ-20-18: Canonical entity update

Update canonical L3 entity data using the approved schema.

Preserve existing entity identifiers, established references and repository conventions.

Do not create overlapping operational fields or duplicate parent process data.

### REQ-20-19: README generation

Generate each Activity README from canonical entity data.

The README shall:

- Use the approved L3 documentation profile
- Explain the Activity's purpose and parent contribution
- Represent relevant inputs and outputs
- Show appropriate responsibility and control references
- Communicate relevant evidence status
- Identify unresolved gaps where appropriate
- Provide relevant L4 references

### REQ-20-20: Entity-level disposition

Every in-scope Activity shall receive an explicit backfill disposition.

The programme-level status vocabulary shall support:

- verified_complete
- verified_with_gaps
- awaiting_evidence
- awaiting_owner_review
- requires_structural_remediation
- not_applicable
- deferred_with_approval

Final representation must follow the approved repository schema.

### REQ-20-21: Catalogue reporting

Publish an L3 backfill report including:

- Total L3 Activities
- Activities assessed
- Activities enriched
- Activities verified
- Activities with documented gaps
- Activities awaiting evidence
- Activities awaiting review
- Activities requiring structural remediation
- Parent L2 readiness
- Activity cohesion status
- L4 reconciliation status
- Cross-reference validity
- Evidence coverage
- Outstanding issues

---

## 6. Implementation work packages

| Work package | Deliverable |
|---|---|
| WP-20-01 | L3 inventory and baseline |
| WP-20-02 | Parent L2 readiness assessment |
| WP-20-03 | L3-to-L2 hierarchy validation |
| WP-20-04 | Activity purpose and contribution enrichment |
| WP-20-05 | Activity boundary and cohesion assessment |
| WP-20-06 | Inputs, outputs and working-object enrichment |
| WP-20-07 | Responsibility and accountability enrichment |
| WP-20-08 | Rules, controls, exceptions and dependencies |
| WP-20-09 | L3-to-L4 reconciliation |
| WP-20-10 | Evidence and provenance validation |
| WP-20-11 | README generation and validation |
| WP-20-12 | Human review and disposition |
| WP-20-13 | Catalogue-level reporting |

---

## 7. Quality gates

- Gate 20-A: Inventory completeness (all L3 entities identified)
- Gate 20-B: Parent readiness (every Activity has valid L2 parent or approved exception)
- Gate 20-C: Activity integrity (defensible purpose, scope and parent contribution)
- Gate 20-D: Operational completeness (applicable operational concepts assessed)
- Gate 20-E: Decomposition integrity (L3-to-L4 relationships reconciled)
- Gate 20-F: Evidence and documentation integrity (material assertions have provenance)
- Gate 20-G: Review and disposition (every entity has explicit disposition)

---

## 8. Testing requirements

The implementation shall demonstrate:

- L3 inventory completeness
- Valid parent L2 relationships
- Detection of orphaned Activities
- Detection of invalid or ambiguous references
- Detection of Activities outside parent boundaries
- Activity cohesion and sibling differentiation checks, where automatable
- Evidence and provenance validation
- Cross-catalogue reference validation
- Correct treatment of inherited information
- Correct L4 child relationship validation
- README generation consistency
- Idempotent migration and generation
- Preservation of existing identifiers and valid documentation

---

## 9. Risks and mitigations

| Risk | Mitigation |
|---|---|
| L2 parent is incomplete | Enforce parent readiness gate or approved exception |
| Activity duplicates parent | Apply purpose and contribution tests |
| Activity groups unrelated work | Apply cohesion review |
| Activity is merely an organizational unit | Enforce semantic distinction |
| L3 becomes workflow documentation | Prohibit execution sequencing and runtime semantics |
| Parent information is copied unnecessarily | Apply explicit inheritance and reference rules |
| L4 decomposition is prematurely prescribed | Leave detailed Task requirements to EXT-21 |
| Unsupported roles or controls are invented | Require provenance and qualified review |

---

## 10. Acceptance criteria

- Complete L3 inventory produced
- Every Activity has a valid parent relationship or explicit remediation status
- Parent L2 readiness assessed
- Activity purpose documented where evidence permits
- Contribution to parent transformation established
- Activity boundary documented
- Cohesion and sibling differentiation assessed
- Inputs and working objects assessed
- Outputs and contribution assessed
- Responsibility and accountability assessed
- Rules, controls and exceptions assessed
- Interfaces and dependencies assessed
- L4 child relationships reconciled
- Evidence and provenance captured
- Inherited information is traceable and not blindly duplicated
- Canonical L3 entities updated
- READMEs generated from canonical data
- Validation and review completed
- Every Activity has an explicit disposition
- Catalogue-level L3 report published
- No unsupported operational claims presented as verified

---

## 11. Completion definition

EXT-20 is complete when all in-scope L3 Activities have been assessed, enriched to their evidence-supported level, reconciled with their parent L2 processes, validated and reviewed as required.

EXT-20 completion establishes the operational documentation foundation for EXT-21: L4 Task Operational Documentation Backfill.

---

## 12. References

- `docs/operational-documentation-programme/CR-BP-94-EXT-19-to-20-detailed-design.md` (the detailed design)
- `change-requests/CR-BP-94-EXT-19-l2-business-process-operational-documentation-backfill.md` (EXT-19)
- `change-requests/CR-BP-94-EXT-15-evidence-provenance-and-confidence-framework.md` (EXT-15)
- `change-requests/CR-BP-94-EXT-16-operational-authoring-and-research-methodology.md` (EXT-16)
- `change-requests/CR-BP-94-EXT-17-enrichment-tooling-and-backfill-orchestration.md` (EXT-17)
- `change-requests/CR-BP-94-EXT-18-operational-documentation-pilot.md` (EXT-18 + GO decision)
- `docs/operational-documentation-pilot.md` (EXT-18)
- `docs/operational-authoring-methodology.md` (EXT-16)
- `docs/evidence-provenance-confidence.md` (EXT-15)
- `docs/enrichment-tooling-orchestration.md` (EXT-17)
- `reconciliation/programme-register.json` (the 17-CR register)
