# CR-BP-94-EXT-15: Evidence, Provenance and Confidence Framework

**Status**: Proposed
**Layer**: Process Catalog (Cross-Cutting Documentation)
**Owner**: Emmanuel A. Otchere
**Programme**: CR-BP-94 Documentation Extension
**Parent**: CR-BP-94
**Predecessors**: CR-BP-94-EXT-09, CR-BP-94-EXT-10, CR-BP-94-EXT-11, CR-BP-94-EXT-12, CR-BP-94-EXT-13, CR-BP-94-EXT-14
**Enables**: CR-BP-94-EXT-16, CR-BP-94-EXT-17, CR-BP-94-EXT-18 and subsequent catalogue backfill
**Type**: Data semantics, governance and documentation integrity
**Priority**: Critical
**Target repository**: technehub-labs/dea-catalog-business-processes
**Proposed path**: change-requests/CR-BP-94-EXT-15-evidence-provenance-and-confidence-framework.md

## 1. Executive Summary

This CR establishes a consistent framework for recording the evidential basis, provenance, confidence and review status of operational assertions within Business Process catalogue entities.

The framework ensures that operational documentation is:

- Traceable to identifiable sources
- Explicit about what is known, inferred, assumed or unknown
- Distinguishable from unverified or provisional content
- Reviewable by an appropriately qualified person
- Safe to publish without exposing confidential operational evidence
- Consistent across L0 to L4 decomposition levels

This CR prevents the enrichment programme from turning plausible descriptions into unsupported representations of actual organisational operations.

## 2. Problem Statement

Operational documentation may be derived from different sources, including:

- Published policies and procedures
- Process owner interviews
- Business function and capability documentation
- Enterprise architecture artefacts
- Information system and integration documentation
- Regulatory and industry requirements
- Existing process documentation
- Direct observation and validated operational records
- Expert interpretation where direct evidence is unavailable

These sources have different authority, currency, reliability and scope. Without a common provenance model, the catalogue cannot reliably distinguish an approved operating fact from an analyst interpretation or an AI-generated suggestion.

A process entity may consequently appear complete while containing assertions that are unsupported, outdated or incorrectly generalized.

## 3. Objectives

1. Establish a canonical evidence and provenance model
2. Distinguish source records from the assertions they support
3. Introduce confidence and verification classifications
4. Support multiple sources and conflicting evidence
5. Establish review and approval requirements
6. Preserve source references without unnecessarily copying sensitive material
7. Integrate evidence status into documentation generation and CI validation
8. Support progressive enrichment without requiring every fact to be fully evidenced before an entity can be documented

## 4. Scope

### In scope

- Provenance metadata for operational assertions
- Source classification and authority
- Confidence classification
- Verification and review status
- Evidence-to-assertion relationships
- Conflicting or superseded evidence
- Evidence freshness and review dates
- AI-assisted research disclosure
- Evidence validation and reporting
- L0 to L4 applicability

### Out of scope

- Replacing the organisation's records-management platform
- Storing complete audit evidence or confidential operational records in the public catalogue
- Establishing a new enterprise risk or compliance repository
- Treating confidence scores as statistical probabilities without a defined statistical basis
- Automatically approving AI-generated assertions

## 5. Normative Requirements

### REQ-15-01: Assertion provenance

Every operational assertion that requires evidence must be capable of being associated with one or more provenance records. An assertion may be represented directly within an entity field or as a structured item within an approved collection. The implementation follows the schema decisions established in EXT-10.

### REQ-15-02: Source classification

The framework supports a controlled source classification. At minimum:

| Source class | Description |
|---|---|
| `authoritative_document` | Approved policy, procedure, standard or controlled document |
| `system_documentation` | Verified system, integration or architecture documentation |
| `owner_confirmation` | Confirmation from an appropriately authorized process owner |
| `subject_matter_expert` | Confirmation from a qualified domain expert |
| `direct_observation` | Directly observed operational practice |
| `operational_record` | Validated operational record or measurement |
| `external_authority` | Applicable regulation, standard or authoritative external source |
| `secondary_reference` | Industry research or other secondary material |
| `analyst_inference` | Explicitly identified interpretation by the author |
| `ai_assisted_research` | AI-assisted discovery or synthesis requiring independent validation |

The list is maintained as a controlled vocabulary and extended only through governed changes.

### REQ-15-03: Provenance record

The implementation supports the following conceptual attributes, subject to the canonical schema established in EXT-10:

- Provenance identifier
- Source title or description
- Source class
- Source owner or issuing authority, where known
- Source location or reference
- Relevant section, page, record or fragment reference, where available
- Publication or effective date, where known
- Date accessed or reviewed
- Source version, where applicable
- Assertions supported
- Evidence limitations
- Confidentiality or publication classification
- Reviewer and review status, where applicable

The catalogue retains a reference to evidence rather than reproducing sensitive evidence content.

### REQ-15-04: Confidence classification

A controlled qualitative confidence classification:

| Classification | Meaning |
|---|---|
| `high` | Directly supported by current authoritative evidence or independently validated confirmation |
| `medium` | Supported by credible evidence, but with limitations in scope, currency or completeness |
| `low` | Based on indirect evidence, incomplete corroboration or a qualified interpretation |
| `unverified` | No sufficient supporting evidence has been established |
| `conflicting` | Available evidence contains unresolved material contradictions |

Confidence must not be presented as a numerical probability. A confidence classification describes the strength of the evidence supporting an assertion, not the importance of the assertion or the quality of the process itself.

### REQ-15-05: Verification status

Confidence and verification status remain separate concepts. The implementation supports at least:

- `not_reviewed`
- `under_review`
- `verified`
- `rejected`
- `superseded`
- `disputed`

A high-confidence assertion is not automatically approved. Verification requires an appropriate review process.

### REQ-15-06: Explicit uncertainty

The framework distinguishes:

- Unknown because information has not been obtained
- Not applicable to the entity or decomposition level
- Not yet assessed
- Inherited from a parent entity
- Deferred for a documented reason
- Conflicting evidence
- Confirmed absence of a characteristic

These states must not be represented by an empty string or silently omitted where doing so would imply completeness.

### REQ-15-07: Evidence conflict resolution

Where sources conflict:

1. Preserve the conflicting source references
2. Identify the affected assertion
3. Record the nature of the conflict
4. Identify the authority responsible for resolution
5. Record the resolution and rationale when established
6. Retain the superseded assertion or evidence history where repository conventions permit

The author must not silently select whichever source produces the most convenient description.

### REQ-15-08: Freshness

Evidence records support source currency and review dates. The implementation permits future policies for periodic review; this CR does not impose a universal expiry period on all evidence types. A regulation, an organisational procedure and an interview confirmation have different currency characteristics.

### REQ-15-09: AI-assisted research

AI-generated content is treated as a research aid, not as authoritative evidence. Where AI assistance materially contributes to an operational assertion:

- The assertion must be independently validated
- The underlying source references must be recorded
- The author or reviewer must remain identifiable through the repository's established governance mechanism
- AI-generated interpretation must not be represented as direct owner confirmation
- Unverifiable claims must remain unverified or be excluded

### REQ-15-10: Publication safety

Evidence records must not expose confidential personal data, commercially sensitive information, credentials, restricted system details or protected operational records. Where necessary, use controlled references, redacted descriptions or approved external evidence locations.

### REQ-15-11: Documentation generation

Generated READMEs communicate evidence status where relevant. They must not expose internal evidence payloads or imply that an assertion is verified merely because it appears in generated documentation.

### REQ-15-12: Cross-catalogue provenance

Evidence references may support relationships with Business Functions, Business Capabilities, Information Systems, Information Systems Functions, policies, controls, risks and metrics. Such relationships use canonical entities and metamodel-approved relationship types. This CR does not introduce new cross-catalogue relationship semantics independently.

## 6. Implementation Requirements

The repository implementation shall:

1. Inspect the existing entity schema and metadata conventions
2. Establish the canonical location for provenance and evidence references
3. Introduce controlled vocabularies and validation rules
4. Define how assertions link to evidence
5. Define the representation of unresolved conflicts
6. Update applicable L0 to L4 templates
7. Update README generation to render appropriate evidence status
8. Add schema and semantic validation tests
9. Provide migration support for existing entities
10. Document how evidence references are maintained and reviewed

Exact file names and locations follow the existing repository structure.

## 7. Acceptance Criteria

- [ ] Canonical provenance structure is defined and implemented
- [ ] Source classifications are controlled and documented
- [ ] Confidence and verification status are distinct
- [ ] Unknown, deferred, inherited, not-applicable and conflicting states are distinguishable
- [ ] Multiple sources can support one assertion
- [ ] Conflicting sources can be represented without silent overwriting
- [ ] Evidence freshness is represented where applicable
- [ ] AI-assisted research is explicitly distinguishable from authoritative evidence
- [ ] Sensitive evidence is not copied into public catalogue content
- [ ] README generation can communicate evidence status
- [ ] Schema and semantic validation tests pass
- [ ] Existing entities remain valid or have a documented migration path
- [ ] EXT-16 can use the framework without introducing another provenance model

## 8. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Excessive evidence overhead | Apply evidence requirements according to assertion significance and profile |
| False confidence | Keep confidence qualitative and distinct from approval |
| Stale sources | Record review dates and source currency |
| Conflicting documentation | Preserve conflicts and require explicit resolution |
| AI-generated inaccuracies | Require source-based validation and accountable human review |
| Sensitive evidence exposure | Store references and approved metadata, not restricted payloads |

## 9. Completion Definition

EXT-15 is complete when the evidence and provenance model is implemented, documented, validated and usable by entity templates, README generation and subsequent authoring processes.

## 10. References

- `change-requests/CR-BP-94-EXT-15-evidence-provenance-and-confidence-framework.md` (this CR)
- `docs/operational-documentation-programme/CR-BP-94-EXT-15-to-18-detailed-design.md` (the detailed design; preserved user submission)
- `docs/operational-documentation-semantic-contract.md` (EXT-09; the upstream semantic contract)
- `docs/operational-schema-inventory.md` (EXT-10; the schema inventory + routed-gap table)
- `docs/evidence-provenance-confidence.md` (the EXT-15 normative contract)
- `reconciliation/programme-register.json` (the 17-CR register)
