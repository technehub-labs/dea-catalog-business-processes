# CR-BP-70 - Escape-clause discovery for PartyAndRelationship x Activate (KYC)

**Status**: Proposed
**Layer**: Process Catalog (lifecycle discovery)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-15

## 1. Change Request

Targeted escape-clause discovery for the PartyAndRelationship x Activate
register cell, the strongest of the 9 backlog-deferred cells per the prior
recommendation ordering. The cell's escape condition reads verbatim:

> defer until a regulated onboarding (e.g. KYC for financial services)
> requires a distinct group

The prior CR-BP-63 discovery (dea:discovery-party-and-relationship-activate)
recorded 7 candidates with two DEFER outcomes and no ADMIT-CANONICAL: the
escape clause was not yet evidenced at exercise time. This slice re-evaluates
the cell against the escape clause specifically, producing one targeted
discovery record (`dea:discovery-party-and-relationship-activate-escape`).
The CR-BP-63 baseline record remains in place; the two are complementary, not
superseding.

## 2. Method

The CR-BP-62 lifecycle discovery method (BP-LIFE-001..015 battery, eight
dispositions, the schema-bound discovery record) is the contract. CR-BP-70 is
not a re-derivation; it is one targeted exercise over one cell's escape
clause, following the backlog-deferred procedure in the
`dea-catalog-discovery-exercise` skill.

Three candidates evaluated:

- Onboard Regulated Party Relationship (the escape-clause hypothesis)
- Commence Relationship (CR-BP-63 DEFER carried forward)
- Activate Customer Journeys (CR-BP-63 RECLASSIFY carried forward)

Disposition rationale (per CR-BP-62 §16):

- **ADMIT-CANONICAL** when the candidate satisfies the canonical process
  tests against the escape clause with authoritative evidence.
- **DEFER** when the boundary remains unresolved after targeted evaluation.
- **RECLASSIFY** when the candidate is execution-level work under another
  process.

## 3. Outcome

| Candidate | Score | Disposition | Rationale |
|---|---|---|---|
| Onboard Regulated Party Relationship | 9/10 | ADMIT-CANONICAL | Legally mandated; authoritative regulatory evidence (FATF R.10, FinCEN CDD 31 CFR 1010.230, AMLD, BCBS, Wolfsberg); strong boundary against Operate; cross-domain breadth limited to regulated sectors, holding the total at 9. |
| Commence Relationship | 5/10 | DEFER | Real contract-effectiveness work; boundary against catalogued relationship-establishment processes remains unresolved for the non-regulated case; CR-BP-63 deferral stands. |
| Activate Customer Journeys | 2/10 | RECLASSIFY | Execution-level release step; reclassify as Activity under the owning transition/release process. |

Cell posture flips from `process_empty: true` (CR-BP-63) to
`process_empty: false` (CR-BP-70) on the strength of the escape-clause
evidence. **No entity records admitted in this slice.** Admission of the
recommended candidate is the next governed step (a follow-on admission
tranche with PC + PG + BP stack and register flip), per the
`catalog-validator-harvest` admission-slice recipe and CR-BP-62 §18 step 16.

## 4. Recommended admission

`dea:process-onboard-regulated-party-relationship` at PartyAndRelationship x
Activate, identity object "Regulated Party Relationship", score 9/10.
Cross-domain breadth is concentrated in regulated sectors (financial services,
telecoms subscriber registration, gambling, crypto asset services); the
identity holds outside finance (supplier sanctions screening, partner vetting)
even where the regulatory apparatus is sector-specific.

## 5. Evidence base

Authoritative regulatory and standards sources; publication-level citations
(no fabricated section numbers):

- FATF Recommendation 10: customer due diligence when establishing business
  relationships (identification, verification, beneficial ownership,
  purpose-and-nature)
- FinCEN Customer Due Diligence Rule (31 CFR 1010.230, 2016) and Customer
  Identification Program rules: onboarding-time identification and
  verification with beneficial-ownership resolution
- EU Anti-Money-Laundering Directives (AMLD4/AMLD5/AMLD6): CDD obligation
  triggered on establishing a business relationship
- Basel Committee BCBS guidelines on the sound management of ML/FT risks
  (customer acceptance policy)
- Wolfsberg Group guidance on customer onboarding and due diligence

## 6. Gate posture

- DISC-001..008 CONFORMANT on the live catalog; record count 14 -> 15.
- The DISC-007 admission-resolution sub-check (added by CR-BP-67) accepts
  the escape-clause record's `canonical_process_ref` pointer against the
  unknown-canonical target without firing duplicate-name errors.
- pytest disc suite green after count-assertion bump.
- No entity records, no register mutation, no schema changes.

## 7. Repository changes

- `discovery/v1-alpha/party-and-relationship-activate-escape.yaml` - new
  discovery record (escape-clause exercise)
- `tests/test_check_lifecycle_discovery.py` - count assertions 14 -> 15
  (3 sites)
- `change-requests/README.md` - index row
- CATALOG.yaml regenerated (open_change_requests 80 -> 81)

## 8. What this CR does NOT do

- Does not admit `dea:process-onboard-regulated-party-relationship`; the
  discovery slice recommends only. Admission is the next governed tranche.
- Does not mutate the register (slice scope: evidence; the disposition
  register flips only when the follow-on admission lands).
- Does not introduce a new entity kind or schema.
- Does not exercise specialization, cross-stage, or new-domain admission.
- Does not stack on open PRs; branch is cut from origin/main post-#110.

## 9. Acceptance criteria

- [x] Discovery record validates against
      `schemas/discovery/lifecycle-discovery.schema.json` (Draft-07, 0
      errors).
- [x] `check_lifecycle_discovery.py` CONFORMANT on live catalog (15
      records, 0 findings).
- [x] DISC-007 admission-resolution accepts the
      `canonical_process_ref: dea:process-onboard-regulated-party-relationship`
      pointer; the id is currently unknown to the catalog, which is the
      correct posture for a recommendation.
- [x] Full pytest suite green; 24-gate suite CONFORMANT (0 blocking,
      0 advisory); CR-META 0 new.
- [x] CATALOG.yaml regenerated and current.

## 10. Next step (separate slice)

The recommended admission is the natural follow-on: an admission tranche
that lands `dea:pc-pr-activate` (PC), a Process Group, and
`dea:process-onboard-regulated-party-relationship` (BP), flips the register
cell to `ratified-accepted` with the escape-clause evidence cited, and
extends ADM-001 to register CR-BP-71. That slice uses the established
admission flow (CR-BP-64/65/66/67 pattern).
