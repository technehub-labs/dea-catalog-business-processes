# CR-BP-94-EXT-18: Operational Documentation Pilot

**Status**: Proposed (awaiting Proceed)
**Layer**: Process Catalog (Cross-Cutting Documentation)
**Owner**: Emmanuel A. Otchere
**Programme**: CR-BP-94 Documentation Extension
**Parent**: CR-BP-94
**Predecessors**: CR-BP-94-EXT-10 through CR-BP-94-EXT-17
**Enables**: CR-BP-94-EXT-19 and subsequent catalogue-wide backfill
**Type**: Pilot, validation and implementation readiness
**Priority**: Critical
**Target repository**: technehub-labs/dea-catalog-business-processes
**Proposed path**: change-requests/CR-BP-94-EXT-18-operational-documentation-pilot.md

## 1. Executive Summary

This CR executes a controlled pilot to validate the operational documentation model, authoring methodology, evidence framework and tooling before large-scale catalogue enrichment. The pilot tests the entire process from research through canonical entity update, generated README, validation and review.

## 2. Objectives

1. Validate the model against real catalogue entities
2. Test whether the L0 to L4 profiles are practical
3. Validate evidence and provenance requirements
4. Assess the usability of the authoring methodology
5. Validate tooling and CI integration
6. Identify schema or semantic defects before bulk backfill
7. Establish a measurable quality baseline
8. Produce a formal go/no-go recommendation for EXT-19

## 3. Pilot Selection

The pilot uses representative entities selected from the actual repository after inventory. The selection must cover, where available:

- At least one L2 Business Process
- Its relevant L3 Activities
- At least one L4 Task under a selected Activity
- Relevant L0/L1 context or grouping records
- At least one entity with strong existing documentation
- At least one entity with incomplete or uncertain operational information
- At least one entity with meaningful cross-catalogue references

The pilot does not select only the easiest or best-documented entities. Exact entity identifiers are recorded in the pilot plan after repository inspection.

## 4. Pilot Execution

### Phase 1: Baseline

Record the pre-pilot state:

- Existing entity content
- README state
- Schema conformance
- Profile completeness
- Evidence coverage
- Cross-reference validity
- Existing CI findings

### Phase 2: Research and enrichment

Apply the EXT-16 methodology. Capture source material and provenance according to EXT-15. Do not use inferred or AI-generated content as verified operational fact.

### Phase 3: Canonical updates

Update entity data using the approved EXT-10 schema and EXT-11 profile. Preserve existing identifiers and relationships.

### Phase 4: Documentation generation

Generate the corresponding READMEs using EXT-17 tooling. Review the generated documentation against the canonical source.

### Phase 5: Validation

Run all applicable validation layers. Record errors, warnings, deferred items and unresolved questions.

### Phase 6: Human review

Obtain review from appropriately qualified domain reviewers and process owners where required. Record approval and unresolved issues.

### Phase 7: Pilot assessment

Evaluate the results and identify defects requiring remediation.

## 5. Pilot Quality Dimensions

The pilot assesses:

| Dimension | Evaluation question |
|---|---|
| Semantic integrity | Are operational concepts represented correctly? |
| Evidence quality | Can material assertions be traced to credible sources? |
| Decomposition integrity | Does each entity describe the correct level of work? |
| Parent-child consistency | Do L3 and L4 entities align with their parent context? |
| Cross-catalogue integrity | Are related entities referenced correctly? |
| Documentation quality | Is the generated README accurate and useful? |
| Tooling reliability | Are validation and generation repeatable? |
| Contributor usability | Can contributors follow the methodology without ambiguity? |
| Governance | Are review and approval responsibilities clear? |
| Maintainability | Can the content be updated without duplication or fragile manual work? |

## 6. Mandatory Pilot Outcomes

The pilot produces:

1. A list of pilot entities and their pre-pilot state
2. Enriched canonical entity records
3. Generated README documentation
4. Validation reports
5. Evidence and provenance records
6. Review and approval records
7. A defect and remediation register
8. A measurement of enrichment effort and recurring bottlenecks
9. Recommended changes to schema, profiles, methodology or tooling
10. A formal go/no-go recommendation

## 7. Go/No-Go Criteria

A go decision requires:

- No unresolved critical schema defects
- No known systematic semantic ambiguity
- No material unsupported operational assertions presented as verified
- Successful README generation
- Successful validation of the pilot's accepted entities
- Parent-child relationships reconciled for the pilot scope
- Evidence and provenance traceability demonstrated
- Human review completed where required
- Tooling sufficiently reliable for controlled batch execution
- Any residual issues documented with approved dispositions

A failed pilot triggers corrective CRs or revisions to the preceding CRs. It is not treated as permission to proceed with bulk backfill regardless.

## 8. Acceptance Criteria

- [ ] Pilot entities selected and justified
- [ ] Baseline recorded
- [ ] EXT-16 methodology applied
- [ ] EXT-15 evidence model applied
- [ ] Canonical entity data updated
- [ ] READMEs generated from canonical data
- [ ] All validation layers executed
- [ ] Review and approval records captured
- [ ] Defects and remediation actions documented
- [ ] Pilot effort and quality metrics recorded
- [ ] Go/no-go decision approved
- [ ] Required upstream corrections identified and assigned

## 9. Completion Definition

EXT-18 is complete only when the pilot has been evaluated and a formal decision authorizes, restricts or rejects progression to L2 backfill.

## 10. References

- `change-requests/CR-BP-94-EXT-18-operational-documentation-pilot.md` (this CR)
- `docs/operational-documentation-programme/CR-BP-94-EXT-15-to-18-detailed-design.md` (the detailed design; preserved user submission)
- `docs/evidence-provenance-confidence.md` (EXT-15; the upstream evidence contract)
- `docs/operational-authoring-methodology.md` (EXT-16; the methodology contract; land in EXT-16 PR)
- `reconciliation/profile-manifest.json` (EXT-11; the L0-L4 profiles used by the pilot)
- `reconciliation/inputs-outputs-manifest.json` (EXT-12)
- `reconciliation/responsibility-accountability-manifest.json` (EXT-13)
- `reconciliation/governance-manifest.json` (EXT-14)
- `reconciliation/evidence-manifest.json` (EXT-15; the per-record evidence manifest)
