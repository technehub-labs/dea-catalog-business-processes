# CR-BP-21e.1: FinanceAndAccounting Completion (ECF v2.4.0 — Final Register Gap Closure)

**Status**: Accepted
**Admission authority**: yes
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-08
**Depends on**: CR-BP-21e (merged, PR #53), CR-BP-19 (register v2.4.0)
**Closes**: Register v3 audit gap for the FinanceAndAccounting domain — **the last fully-ratified register gap**.

## 1. Background

CR-BP-21e (PR #53, merged `61847bd`) landed the FinanceAndAccounting
domain at the cell level: the Conceive-cell L1 group `dea:group-financial-model-conception`,
plus one L2 per non-Conceive cell (Design: `dea:process-design-financial-plan-structure`,
Operate: `dea:process-operate-general-ledger`, Improve: `dea:process-audit-policy-compliance`
and `dea:process-conduct-cost-optimization-review`). The register v3
audit recorded FA D/B/O/Im as `ratified-pending-landing` with
`planned_tranche: CR-BP-21e` (a stale pointer; the correct completion
tranche ID is `CR-BP-21e.1`).

The complete register v2 FA L2 candidate counts (Design 4, Build 3,
Operate 8, Improve 3) minus the 5 already-landed give **15 remaining
L2s** + **4 non-Conceive L1 Process Groups**.

## 2. Scope

Lands the **15 remaining register v2 FinanceAndAccounting L2 Business
Processes** and the **4 non-Conceive L1 Process Groups** that compose
them:

| Group (L1) | Stage | L2 count | L2s |
|---|---|---|---|
| `dea:group-financial-design` | Design | 4 | design-financial-controls-and-policies, design-tax-position-and-strategy, design-treasury-and-funding-model, design-financial-plan-structure (seeded 21e) |
| `dea:group-financial-build` | Build | 3 | implement-financial-systems-and-ledger, build-budgeting-and-forecasting-systems, onboard-tax-and-compliance-capability |
| `dea:group-financial-operate` | Operate | 8 | run-accounts-payable, run-accounts-receivable, execute-payroll, manage-cash-and-liquidity, perform-financial-close, manage-tax-compliance-and-filings, operate-financial-reporting-and-disclosure, operate-general-ledger (seeded 21e) |
| `dea:group-financial-improve` | Improve | 3 | refine-financial-controls-and-policies, evolve-treasury-and-funding-model, audit-policy-compliance + conduct-cost-optimization-review (seeded 21e) |

L2 naming follows the BP-ARC-ID-001 `<verb> <object>` contract and the
identity-schema verb pattern `^[A-Z][a-z]+$` (singular TitleCase; same
discipline as 21a.1/21b.1/21c.1/21d.1).

## 3. Process Type adjustments (BP-ARC-ID-004)

Two L2s needed `process_type` flips driven by outcome-keyword density:

- `dea:process-operate-financial-reporting-and-disclosure`: core
  (reporting is delivery; the "operate" verb reads as production
  language).
- `dea:process-onboard-tax-and-compliance-capability`: management
  (onboarding tax capability is governance work, not direct delivery).

Both passed BP-ARC-ID-004 keyword-density ≥ 0.3 on re-check.

## 4. In-place edits (surgical text patches)

- `dea:group-financial-model-conception` — +4 composes edges for the
  L2s seeded by 21e (one per non-Conceive cell); +1 `change_history`
  entry recording the upstream composes-edge expansion.
- 5 FA Process Contexts (`dea-pc-fa-{design,build,operate,improve}`):
  `processes:` lists extended in place with the 15 new L2 IDs.

No schema, validator, or CI surface changes.

## 5. Register v3 audit impact

FA D/B/O/Im flipped to `landed`. Register v3 final state:

| Status | Count |
|---|---|
| `landed` | **35** |
| `ratified-pending-landing` | **0** |
| `backlog-deferred` | 14 |
| **Total** | **49** |

**Register v2 scope is now fully landed.** Activate/Retire cells
remain `backlog-deferred` (CR-BP-19 doctrine: lifecycle transitions
are not stable Process Group operating states).

## 6. Bookkeeping

- Disposition register +15 RETAIN entries (tranche `cr-bp-21e.1`).
- Tranche plan 55 → 60 (new fa-c.1/d.1/b.1/op.1/im.1).
- Conformance report regenerated (190 records).
- Inventory + baseline regenerated.
- CATALOG.yaml regenerated post-commit (no amend needed for new entries;
  pre-commit blind-spot only affects MODIFIED files).
- Test counts updated (104 → 119 BPs, 31 → 35 groups, 55 → 60 tranches,
  170 → 190 conformance records).
- CHANGELOG + README updated (CR-BP-21d.1 flipped to Merged PR #57).
