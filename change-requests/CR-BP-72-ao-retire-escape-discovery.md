# CR-BP-72 - A&O Retire escape-clause discovery (mass-layoff regulated wind-down)

**Status**: Proposed
**Layer**: Process Catalog (lifecycle discovery)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-15

## 1. Change Request

Targeted escape-clause discovery for the AgencyAndOrganization x Retire
register cell, the second item in the Option B backlog-deferred sequence.
The cell's escape condition reads verbatim:

> defer until a regulated wind-down (e.g. mass layoff) requires a
> dedicated L1 group

The prior CR-BP-63 discovery (dea:discovery-agency-and-organization-retire)
recorded 6 candidates with one MERGE and no ADMIT-CANONICAL: the escape
clause was not yet evidenced at exercise time. This slice re-evaluates
the cell against the escape clause specifically, producing one targeted
discovery record (`dea:discovery-agency-and-organization-retire-escape`).
The CR-BP-63 baseline record remains in place; the two are complementary,
not superseding.

## 2. Method

The CR-BP-62 lifecycle discovery method (BP-LIFE-001..015 battery, eight
dispositions, the schema-bound discovery record) is the contract. CR-BP-72
is not a re-derivation; it is one targeted exercise over one cell's escape
clause, following the backlog-deferred procedure in the
`dea-catalog-discovery-exercise` skill.

Three candidates evaluated:

- Conduct Regulated Workforce Wind-Down (the escape-clause hypothesis)
- Decommission Agent or Workforce Cohort (CR-BP-63 RECORD-PATTERN carry-forward)
- Retire Knowledge Assets of Decommissioned Workforce (CR-BP-63 RECORD-PATTERN carry-forward)

Disposition rationale (per CR-BP-62 §16):

- **ADMIT-CANONICAL** when the candidate satisfies the canonical process
  tests against the escape clause with authoritative evidence.
- **DEFER** when the boundary remains unresolved after targeted evaluation.
- **RECLASSIFY** when the candidate is execution-level work under another
  process.

## 3. Outcome

| Candidate | Score | Disposition | Rationale |
|---|---|---|---|
| Conduct Regulated Workforce Wind-Down | 9/10 | ADMIT-CANONICAL | Legally mandated across regulated jurisdictions (WARN 29 USC 2100 et seq.; 20 CFR Part 639; EU Directive 98/59/EC; ILO C158 and C135; OECD Employment Outlook); strong boundary against Operate and E&O x Retire; cross-domain breadth limited to regulated jurisdictions, holding the total at 9. |
| Decommission Agent or Workforce Cohort | 2/10 | RECLASSIFY | Execution-level cohort step; reclassify as Activity under agent operations or under the regulated wind-down process when statutory thresholds apply. |
| Retire Knowledge Assets of Decommissioned Workforce | 3/10 | RECLASSIFY | Operational concern subsumed by the regulated wind-down transition supports; reclassify as Activity under knowledge management or under the wind-down process. |

Cell posture flips from `process_empty: true` (CR-BP-63) to
`process_empty: false` (CR-BP-72) on the strength of the escape-clause
evidence. **No entity records admitted in this slice.** Admission of the
recommended candidate is the next governed step (a follow-on admission
tranche with PC + PG + BP stack and register flip), per the
`catalog-validator-harvest` admission-slice recipe and CR-BP-62 §18 step 16.

## 4. Recommended admission

`dea:process-conduct-regulated-workforce-wind-down` at AgencyAndOrganization
x Retire, identity object "Regulated Workforce Wind-Down", score 9/10.
Cross-domain breadth is concentrated in regulated jurisdictions (US WARN,
EU member-state implementations of Directive 98/59/EC, ILO member-state
implementations of C158); the identity holds across organizational-unit
decommission, agent-team dissolution, and divestiture-induced workforce
reduction even where the regulatory apparatus is jurisdiction-specific.

## 5. Evidence base

Authoritative statutory and standards sources; publication-level citations
(no fabricated section numbers):

- U.S. WARN Act (29 U.S.C. § 2101 et seq.; 20 CFR Part 639): 60-day
  advance notice for plant closings and mass layoffs; thresholds;
  notice to employees, representatives, state dislocated worker unit,
  local chief elected official.
- EU Council Directive 98/59/EC on collective redundancies: information
  and consultation obligations with workers' representatives; thresholds;
  aim of reaching agreement on ways to avoid or reduce redundancies.
- ILO Termination of Employment Convention, 1982 (No. 158) and ILO
  Workers' Representatives Convention, 1971 (No. 135): consultation and
  fair-selection standards.
- OECD Employment Outlook: mass-layoff obligations and transition
  supports universal across OECD economies.
- Jurisdiction-specific statutes implementing the EU directive (UK TULRCA
  s.188; German Betriebsverfassungsgesetz § 17).
- APQC PCF and SHRM body of practice: large-organization HR universally
  operates a documented wind-down process distinct from steady-state HR
  operation.

## 6. Gate posture

- DISC-001..008 CONFORMANT on the live catalog; record count 15 -> 16.
- The DISC-007 admission-resolution sub-check accepts the escape-clause
  record's `canonical_process_ref` pointer against the unknown-canonical
  target without firing duplicate-name errors.
- pytest disc suite green after count-assertion bump.
- No entity records, no register mutation, no schema changes.

## 7. Repository changes

- `discovery/v1-alpha/agency-and-organization-retire-escape.yaml` - new
  discovery record (escape-clause exercise)
- `tests/test_check_lifecycle_discovery.py` - count assertions 15 -> 16
  (3 sites)
- `change-requests/README.md` - index row
- CATALOG.yaml regenerated (open_change_requests 82 -> 83)

## 8. What this CR does NOT do

- Does not admit `dea:process-conduct-regulated-workforce-wind-down`; the
  discovery slice recommends only. Admission is the next governed tranche.
- Does not mutate the register (slice scope: evidence; the disposition
  register flips only when the follow-on admission lands).
- Does not introduce a new entity kind or schema.
- Does not exercise specialization, cross-stage, or new-domain admission.
- Does not stack on open PRs; branch is cut from origin/main post-#112.

## 9. Acceptance criteria

- [x] Discovery record validates against
      `schemas/discovery/lifecycle-discovery.schema.json` (Draft-07, 0
      errors).
- [x] `check_lifecycle_discovery.py` CONFORMANT on live catalog (16
      records, 0 findings).
- [x] DISC-007 admission-resolution accepts the
      `canonical_process_ref: dea:process-conduct-regulated-workforce-wind-down`
      pointer; the id is currently unknown to the catalog, which is the
      correct posture for a recommendation.
- [x] Full pytest suite green; 24-gate suite CONFORMANT (0 blocking,
      0 advisory); CR-META 0 new.
- [x] CATALOG.yaml regenerated and current.

## 10. Next step (separate slice)

The recommended admission is the natural follow-on: an admission tranche
that lands `dea:pc-ao-retire` (PC), a Process Group, and
`dea:process-conduct-regulated-workforce-wind-down` (BP), flips the register
cell to `ratified-accepted` with the escape-clause evidence cited, and
extends ADM-001 to register CR-BP-73. That slice uses the established
admission flow (CR-BP-64/65/66/67/71 pattern).
