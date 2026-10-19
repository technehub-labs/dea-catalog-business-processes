# Evidence, Provenance and Confidence Framework (CR-BP-94-EXT-15)

**Status**: Normative (proposed for adoption under CR-BP-94-EXT-15)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-19
**Source CR**: CR-BP-94-EXT-15 (Evidence, Provenance and Confidence Framework)
**Parent programme**: DEA-PROCESS-ENRICH-000
**Predecessors**: EXT-09 (semantic contract), EXT-10 (schema inventory), EXT-11 (L0-L4 profiles), EXT-12 (inputs/outputs/interfaces), EXT-13 (responsibility/accountability), EXT-14 (rules/controls/exceptions)
**Tranche**: Engineering and governance readiness tranche (EXT-15..18)
**Enables**: EXT-16, EXT-17, EXT-18, and subsequent catalogue backfill
**Repository**: technehub-labs/dea-catalog-business-processes

---

## 1. Purpose

This document is the **EXT-15 schema extension and semantic contract** for the evidence, provenance, confidence, and verification model. It implements the EXT-15 CR's design and establishes the framework that EXT-16 (authoring methodology), EXT-17 (tooling), EXT-18 (pilot), and EXT-19+ (backfill) all build upon.

The framework ensures that operational documentation is:

- Traceable to identifiable sources
- Explicit about what is known, inferred, assumed or unknown
- Distinguishable from unverified or provisional content
- Reviewable by an appropriately qualified person
- Safe to publish without exposing confidential operational evidence
- Consistent across L0 to L4 decomposition levels

This document prevents the enrichment programme from turning plausible descriptions into unsupported representations of actual organisational operations.

---

## 2. The conceptual model

EXT-15 distinguishes three concepts:

| Concept | Definition | Lives on |
|---|---|---|
| **Provenance record** | The traceable evidence record: source, location, date, reviewer, classification, limitations | `provenance[]` (top-level L2 field) |
| **Confidence** | The qualitative strength of the evidence supporting an assertion | `provenance.confidence` (per-assertion) |
| **Verification status** | The explicit review/approval state of the assertion | `provenance.verification_status` (per-assertion) |

A **provenance record** is the evidence: who/what/when/where the assertion is based on. **Confidence** describes the strength of that evidence. **Verification status** describes the review state of the assertion (independent of how strong the evidence is).

A high-confidence assertion is NOT automatically verified. Verification requires an appropriate review process. Confidence and verification are distinct concepts that may diverge.

---

## 3. Source classification (controlled vocabulary)

Per REQ-15-02:

| Value | Description |
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

The list is maintained as a controlled vocabulary and extended only through governed changes. The vocabulary distinguishes evidence (top half) from inference (bottom half: `analyst_inference`, `ai_assisted_research`).

---

## 4. Confidence classification (controlled vocabulary)

Per REQ-15-04:

| Value | Meaning |
|---|---|
| `high` | Directly supported by current authoritative evidence or independently validated confirmation |
| `medium` | Supported by credible evidence, but with limitations in scope, currency or completeness |
| `low` | Based on indirect evidence, incomplete corroboration or a qualified interpretation |
| `unverified` | No sufficient supporting evidence has been established |
| `conflicting` | Available evidence contains unresolved material contradictions |

Confidence must NOT be presented as a numerical probability. A confidence classification describes the strength of the evidence supporting an assertion, not the importance of the assertion or the quality of the process itself.

---

## 5. Verification status (controlled vocabulary)

Per REQ-15-05:

| Value | Description |
|---|---|
| `not_reviewed` | The assertion has not been reviewed |
| `under_review` | A reviewer is currently assessing the assertion |
| `verified` | The assertion has been reviewed and approved |
| `rejected` | The assertion has been reviewed and rejected (the rejection is recorded) |
| `superseded` | The assertion has been replaced by a newer assertion |
| `disputed` | The assertion is in dispute (the dispute is recorded) |

A high-confidence assertion is not automatically approved. Verification requires an appropriate review process.

---

## 6. Uncertainty state (controlled vocabulary)

Per REQ-15-06 (explicit acknowledgement of what is known, what is not, and why):

| Value | Description |
|---|---|
| `unknown` | Information has not been obtained |
| `not_applicable` | The assertion is not applicable to this entity |
| `not_yet_assessed` | The assertion has not yet been researched |
| `inherited` | The assertion is inherited from a parent entity |
| `deferred_with_reason` | The assertion is deferred (the reason is recorded) |
| `conflicting` | The evidence contains unresolved material contradictions |
| `confirmed_absence` | The characteristic has been confirmed as absent |

These states must NOT be represented by an empty string or silently omitted where doing so would imply completeness. A "confirmed_absence" is itself an assertion requiring evidence.

---

## 7. Confidentiality classification (controlled vocabulary)

Per REQ-15-10 (publication safety):

| Value | Description |
|---|---|
| `public` | Safe to publish externally |
| `internal` | Safe to publish within the organisation |
| `confidential` | Restricted; references only, not the source content |
| `restricted` | Highly restricted; reference-only with redacted descriptions |

The catalogue retains a reference to evidence rather than reproducing sensitive evidence content. The `confidentiality` field tells the README generator how to render the evidence reference.

---

## 8. The provenance record (top-level L2 field)

EXT-15 introduces the new optional L2 top-level field `provenance[]` (array of structured entries). Per REQ-15-03:

```yaml
provenance:
  - id: <provenance-id>
    source:
      title: <source title or description>
      source_class: authoritative_document | system_documentation | owner_confirmation | subject_matter_expert | direct_observation | operational_record | external_authority | secondary_reference | analyst_inference | ai_assisted_research
      owner: <source owner or issuing authority>
      location: <uri or location>
      section: <section, page, or fragment reference>
      publication_date: <YYYY-MM-DD>
      accessed_date: <YYYY-MM-DD>
      source_version: <version>
      confidentiality: public | internal | confidential | restricted
    assertions_supported:
      - <assertion text or id>
    evidence_limitations: |
      <Limitations on the source's evidence.>
    reviewer: <role or person>
    review_status: not_reviewed | under_review | verified | rejected | superseded | disputed
    review_date: <YYYY-MM-DD>
```

### 8.1 Multiple sources

Multiple provenance records may support a single assertion (REQ-15-07: evidence-to-assertion relationships). The `assertions_supported[]` field links the source to the assertions.

### 8.2 Conflicting evidence

Where sources conflict:

1. Preserve the conflicting source references (each as a separate entry in `provenance[]`)
2. Identify the affected assertion (via `assertions_supported[]`)
3. Record the nature of the conflict (in `evidence_limitations` or in the `provenance.uncertainty_state` field on the per-assertion sub-structure)
4. Identify the authority responsible for resolution (in `reviewer`)
5. Record the resolution and rationale when established
6. Retain the superseded assertion or evidence history where repository conventions permit

The author MUST NOT silently select whichever source produces the most convenient description.

### 8.3 AI-assisted research

Per REQ-15-09: AI-generated content is treated as a research aid, NOT as authoritative evidence. Where AI assistance materially contributes to an operational assertion:

- The assertion must be independently validated
- The underlying source references must be recorded
- The author or reviewer must remain identifiable through the repository's established governance mechanism
- AI-generated interpretation must NOT be represented as direct owner confirmation
- Unverifiable claims must remain unverified or be excluded

The `source_class: ai_assisted_research` value is the marker. The validator (EV-005) confirms AI-assisted sources are flagged.

---

## 9. The per-assertion sub-structure (EXT-12 extension)

The existing EXT-12 sub-structures (`inputs[].provenance`, `outputs[].provenance`, `interfaces[].source`, `dependencies[].source`, `business_rules[].source_ref`, `controls[].evidence`, etc.) MAY carry two additional fields per EXT-15:

- `confidence`: the qualitative strength of the evidence (5-value vocabulary)
- `verification_status`: the review state of the assertion (6-value vocabulary)
- `uncertainty_state`: the explicit acknowledgement of what is known or not known (7-value vocabulary)

```yaml
inputs:
  - id: <input-id>
    name: <input name>
    description: |
      <What this input represents.>
    source: <source entity id or free-text origin>
    provenance:
      source: <provenance-id referencing provenance[] above OR a free-text source description>
      confidence: high
      verification_status: verified
      verification_date: <YYYY-MM-DD>
      verification_reviewer: <role or person>
      uncertainty_state: not_applicable
```

The per-assertion `provenance.source` field MAY reference a `provenance[]` entry by id (canonical cross-reference) or be a free-text source description (ad-hoc reference for simple cases).

---

## 10. L0-L4 applicability

| Concern | L0 ProcessContext | L1 ProcessGroup | L2 BusinessProcess | L3 Activity | L4 Task |
|---|---|---|---|---|---|
| Provenance records | (rare; mostly inherited) | (rare) | Material operational assertions | Activity-specific assertions | Task-specific assertions |
| Confidence | Inherited from L2 | Inherited from L2 | Per-assertion | Inherited from L2 or local | Inherited from L2/L3 or local |
| Verification status | Inherited | Inherited | Per-assertion | Inherited from L2 or local | Inherited from L2/L3 or local |
| Uncertainty state | Inherited | Inherited | Per-assertion | Inherited from L2 or local | Inherited from L2/L3 or local |

L0 and L1 are non-executable (per EXT-11); they typically inherit provenance/confidence/verification from L2. L2 is the principal level at which the catalogue describes a complete business transformation; it is the primary level for evidence records.

---

## 11. Compatibility and migration

EXT-15 is **additive**:

- Existing records that do not declare `provenance[]` continue to validate (the EXT-15 fields are all optional).
- The per-assertion `confidence` and `verification_status` fields are optional extensions to the EXT-12 sub-structures. Records without them remain conformant.
- The validator (EV-001..EV-010) enforces the structural and vocabulary requirements when the fields are populated.

The EXT-10 regression test (`tests/test_schema_inventory_ext10.py`) is updated to remove the L0/L1/L2 entries for `provenance` / `evidence` / `verification` / `confidence` from the EXT-10 Routed-gap list (these are now legitimately in the L2 template per EXT-15). The remaining gap concepts (metric, KPI, KRI, KCI, target, assumption) are still open for the next tranche (EXT-16+).

The 145 existing L2 records have **0** of the new fields populated (per the EXT-10 inventory; the CR-BP-96 advisory policy passes vacuously). The EXT-19 L2 backfill tranche is the work that populates them.

---

## 12. Validator and manifest

EXT-15 lands:

- `scripts/check_evidence_provenance_ext15.py` (the validator; EV-001..EV-010 rules)
- `reconciliation/evidence-manifest.json` (per-record manifest)
- `gate [40] Evidence/Provenance/Confidence` wired ADVISORY in `scripts/conformance_result.py`
- `tests/test_evidence_provenance_ext15.py` (unit + integration)

The validator enforces:

- **EV-001**: `provenance[]` entries have id + source.source_class + assertions_supported + review_status
- **EV-002**: `provenance[].source.source_class` is in the 10-value vocabulary
- **EV-003**: `provenance[].source.confidentiality` is in the 4-value vocabulary (or absent)
- **EV-004**: `provenance[].review_status` is in the 6-value vocabulary
- **EV-005**: AI-assisted sources (`source_class: ai_assisted_research`) MUST NOT be presented as authoritative evidence; the `evidence_limitations` field MUST be non-empty when the source is AI-assisted
- **EV-006**: per-assertion `provenance.confidence` (when present) is in the 5-value vocabulary
- **EV-007**: per-assertion `provenance.verification_status` (when present) is in the 6-value vocabulary
- **EV-008**: per-assertion `provenance.uncertainty_state` (when present) is in the 7-value vocabulary
- **EV-009**: multiple provenance records may exist for the same assertion (the `assertions_supported[]` field may overlap across records)
- **EV-010**: L0/L1 do NOT declare `provenance[]` as a top-level field; they inherit from L2 (per EXT-11 non-executable + EXT-15 §10)

---

## 13. References

- `templates/business-process.yaml` (the L2 template; EXT-15 extensions documented inline)
- `change-requests/CR-BP-94-EXT-15-evidence-provenance-and-confidence-framework.md` (the EXT-15 CR)
- `change-requests/CR-BP-94-EXT-16-operational-authoring-and-research-methodology.md` (the EXT-16 CR; awaits Proceed)
- `change-requests/CR-BP-94-EXT-17-enrichment-tooling-and-backfill-orchestration.md` (the EXT-17 CR; awaits Proceed)
- `change-requests/CR-BP-94-EXT-18-operational-documentation-pilot.md` (the EXT-18 CR; awaits Proceed)
- `docs/operational-documentation-programme/CR-BP-94-EXT-15-to-18-detailed-design.md` (the detailed design; preserved user submission)
- `docs/operational-documentation-semantic-contract.md` (EXT-09; the upstream semantic contract)
- `docs/operational-schema-inventory.md` (EXT-10; the schema inventory + routed-gap table)
- `templates/documentation-profile-ext11-v3.yaml` (EXT-11; the v3 profile that consumes the EXT-15 fields)
- `reconciliation/programme-register.json` (the 17-CR register)
- `reconciliation/profile-manifest.json` (EXT-11 manifest)
- `reconciliation/inputs-outputs-manifest.json` (EXT-12 manifest)
- `reconciliation/responsibility-accountability-manifest.json` (EXT-13 manifest)
- `reconciliation/governance-manifest.json` (EXT-14 manifest)
