# CR-BP-94-EXT-16: Operational Authoring and Research Methodology

**Status**: Proposed (awaiting Proceed)
**Programme**: CR-BP-94 Documentation Extension
**Parent**: CR-BP-94
**Predecessors**: CR-BP-94-EXT-10, CR-BP-94-EXT-11, CR-BP-94-EXT-12, CR-BP-94-EXT-13, CR-BP-94-EXT-14, CR-BP-94-EXT-15
**Enables**: CR-BP-94-EXT-17 and CR-BP-94-EXT-18
**Type**: Authoring standards, research methodology and governance
**Priority**: Critical
**Target repository**: technehub-labs/dea-catalog-business-processes
**Proposed path**: change-requests/CR-BP-94-EXT-16-operational-authoring-and-research-methodology.md

## 1. Executive Summary

This CR establishes a repeatable methodology for researching, authoring, reviewing and maintaining operational documentation for Business Process catalogue entities. The methodology ensures that different contributors can enrich process entities consistently without introducing unsupported operational assumptions, duplicating information or confusing decomposition levels.

## 2. Problem Statement

The schema and documentation profiles establish what can be represented. They do not, by themselves, establish how contributors should discover and validate the information.

Without a common methodology, contributors may:

- Infer operating procedures from process names
- Confuse a business process with its activities or tasks
- Describe a presumed ideal process rather than actual organisational practice
- Duplicate responsibilities already represented elsewhere
- Invent inputs, outputs, controls or system dependencies
- Treat an AI-generated description as evidence
- Enrich child entities without validating their parent process

## 3. Objectives

1. Define a standard research and authoring lifecycle
2. Establish source prioritisation and research methods
3. Define decomposition-aware authoring guidance
4. Establish human review and approval responsibilities
5. Define how gaps and uncertainties are documented
6. Prevent unsupported operational claims
7. Establish quality criteria for accepting enriched entities
8. Create repeatable guidance for human and AI-assisted contributors

## 4. Scope

### In scope

- Research planning
- Source discovery and evaluation
- Process owner and subject-matter expert engagement
- Entity authoring
- Evidence capture
- Decomposition and parent-child reconciliation
- Review and approval
- AI-assisted research and authoring
- Documentation quality assurance
- Maintenance and change management

### Out of scope

- Replacing enterprise process management practices
- Mandating one process-modelling notation
- Defining operational workflows for the organisation
- Establishing an organisation-wide process redesign methodology

## 5. Normative Requirements

### REQ-16-01: Standard authoring lifecycle

Every enrichment activity follows a documented lifecycle:

1. Select entity and establish scope
2. Inspect current entity and its parent/child relationships
3. Identify information gaps against the applicable profile
4. Develop a research plan
5. Identify and assess available sources
6. Capture evidence and provenance
7. Draft operational assertions
8. Validate semantic distinctions
9. Reconcile with related catalogue entities
10. Obtain required review and approval
11. Update canonical entity data
12. Generate documentation
13. Execute validation and quality checks
14. Submit changes through the repository's established review process

### REQ-16-02: Source prioritisation

Authors prefer sources in the following general order, subject to the authority and relevance of the source:

1. Approved organisational policies and procedures
2. Authorized process owner confirmation
3. Controlled operational documentation
4. Verified system and architecture records
5. Direct observation and validated operational records
6. Qualified subject-matter expert confirmation
7. Authoritative external regulations and standards
8. Credible secondary research
9. Analyst inference

This ordering is guidance, not an automatic authority ranking. A source may be authoritative for one assertion and irrelevant to another.

### REQ-16-03: Actual practice versus target practice

Authors distinguish:

- Current operating practice
- Approved documented practice
- Intended or target operating practice
- Proposed future-state practice
- External normative requirements

A target-state description must not be presented as the current operational process. Where documented practice and observed practice differ, record the discrepancy and its evidence rather than silently reconciling the two.

### REQ-16-04: Decomposition-aware authoring

Authoring respects the L0 to L4 distinctions established in EXT-11:

- L0 describes process scope and context
- L1 describes process grouping and membership
- L2 describes the business transformation and its operational boundaries
- L3 describes cohesive bodies of work contributing to an L2 process
- L4 describes bounded, independently understandable tasks

L0 and L1 are not treated as executable operational units. L4 does not become a workflow-engine specification.

### REQ-16-05: L2-first enrichment

Operational enrichment normally begins at L2. The L2 process provides the transformation context against which L3 activities and L4 tasks can be assessed. An exception may be made for a child entity where there is a specific research or remediation reason, but its parent relationship and unresolved dependencies must be recorded.

### REQ-16-06: Semantic distinction checklist

Authors validate that the following distinctions are preserved:

| Concept A | Concept B | Required distinction |
|---|---|---|
| Input | Resource | Information or object entering a transformation versus capacity used to perform work |
| Output | Outcome | Produced deliverable versus resulting business effect |
| Transformation | Workflow | Business change versus execution sequence |
| Role | Organizational unit | Responsibility-bearing position versus organisational structure |
| Responsibility | Accountability | Performing or contributing versus answerability and authority |
| Rule | Control | Requirement or constraint versus mechanism that manages compliance or risk |
| Control | Evidence | Mechanism versus proof of design or operation |
| Exception | Deviation | Recognized permitted variation versus departure from expected practice |
| Trigger | Precondition | Initiating event versus condition required for work to proceed |
| Dependency | Decomposition | Reliance on another entity versus structural parent-child relationship |

### REQ-16-07: Gap recording

Authors do not fill unknown fields with invented content. Where information is unavailable, use the appropriate status from the approved schema and profile. For material gaps, record:

- What is unknown
- Why it matters
- Research already performed
- Sources consulted
- Who can resolve the gap
- Whether the gap blocks publication, approval or only full operational completeness

### REQ-16-08: Review roles

The methodology distinguishes:

- Author
- Domain reviewer
- Process owner or authorized approver
- Catalogue maintainer
- Schema or metamodel reviewer, where applicable

Not every entity requires every role to be a separate person. However, the approval authority must be clear.

### REQ-16-09: AI-assisted authoring

AI tools may assist with:

- Source discovery
- Document summarisation
- Candidate assertion extraction
- Terminology harmonisation
- Gap analysis
- Drafting
- Structural validation

AI tools do not independently:

- Confirm actual organisational practice
- Approve process ownership or accountability
- Establish an authoritative control
- Convert an assumption into a verified fact
- Invent source references
- Resolve conflicting evidence without human authorization

### REQ-16-10: Authoring records

Each enrichment change is traceable through the repository's established change-management mechanism. Where the existing entity schema supports it, relevant metadata should include author, reviewer, review date, source references and change rationale. Avoid duplicating Git history or CR governance metadata unnecessarily.

### REQ-16-11: Quality review

Every enriched entity is reviewed for:

- Semantic correctness
- Decomposition-level appropriateness
- Evidence quality
- Parent-child consistency
- Cross-catalogue reference validity
- Completeness against its profile
- Publication safety
- README and entity consistency

### REQ-16-12: Reproducibility

The methodology and templates are sufficiently explicit that another qualified contributor can understand why an assertion was made and how it was validated.

## 6. Deliverables

- Operational authoring handbook
- Research planning template
- Source assessment guidance
- Entity enrichment checklist
- Process owner review checklist
- AI-assisted research and validation guidance
- Gap and uncertainty recording guidance
- L0 to L4 authoring examples
- Review and approval workflow documentation

## 7. Acceptance Criteria

- [ ] Standard authoring lifecycle documented
- [ ] Source evaluation methodology established
- [ ] Current, target and proposed practice distinguished
- [ ] L0 to L4 authoring guidance aligned with EXT-11
- [ ] L2-first enrichment rule documented
- [ ] Semantic distinction checklist implemented in guidance
- [ ] Gap recording methodology defined
- [ ] Review and approval responsibilities established
- [ ] AI-assisted research boundaries documented
- [ ] Authoring and review checklists available
- [ ] Pilot contributors can apply the methodology consistently
- [ ] No conflict with the canonical provenance framework

## 8. Completion Definition

EXT-16 is complete when the authoring methodology, templates, research guidance and review criteria are published and can be applied consistently in the enrichment tooling and pilot.

## 9. References

- `change-requests/CR-BP-94-EXT-16-operational-authoring-and-research-methodology.md` (this CR)
- `docs/operational-documentation-programme/CR-BP-94-EXT-15-to-18-detailed-design.md` (the detailed design; preserved user submission)
- `templates/documentation-profile-ext11-v3.yaml` (EXT-11; L0-L4 profile)
- `docs/evidence-provenance-confidence.md` (EXT-15; the upstream evidence/provenance contract)
