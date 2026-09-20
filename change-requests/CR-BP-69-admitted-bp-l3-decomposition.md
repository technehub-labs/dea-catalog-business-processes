# CR-BP-69 - Admitted-BP L3 decomposition tranche (Activate/Retire cells)

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Proposed
**Layer**: L3
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-15

## 1. Change Request

The CR-BP-64 through CR-BP-67 admission tranches landed five canonical
Business Processes at previously unpopulated Activate and Retire coordinates,
each with a full PC + PG + BP stack but no L3 decomposition. This tranche
completes L0 to L3 coverage for those five BPs with 4 Activity records each
(20 total), following the structured deposition pattern proven by CR-BP-42
through CR-BP-57.

## 2. Scope

| Parent BP | Coordinate | Activities |
|---|---|---|
| Transition Proposition to Service | ProductAndValue x Activate | Prepare Transition Readiness; Execute Service Cutover; Confirm Operational Acceptance; Stabilize Early Operations |
| Transition Proposition Out of Service | ProductAndValue x Retire | Plan Service Withdrawal; Execute Service Withdrawal; Resolve Residual Obligations; Confirm Retirement Closure |
| Bring Policy Instrument into Force | GovernanceAndExistence x Activate | Verify Commencement Conditions; Effect Instrument Commencement; Communicate Obligations and Rights; Establish Enforcement Baseline |
| Decommission Enterprise Asset | EnablementAndOperations x Retire | Plan Asset Retirement; Withdraw Asset from Operation; Execute Disposal Routes; Resolve Residual Value and Obligations |
| Close Enterprise Relationship | PartyAndRelationship x Retire | Plan Relationship Close-Out; Settle Outstanding Obligations; Resolve Records and Rights; Execute Evidenced Closure |

Activity semantics derive from each parent BP's trigger and outcome text, not
from boilerplate; the deposition cites the parent evidence per candidate.
Activate and Retire coordinates carry L3 coverage for the first time.

## 3. Mechanics

- One `entities/v1-alpha/dea:activity-*/dea:activity-*.yaml` per Activity
  (20 records), `ecfConformance` inheriting the parent coordinate exactly as
  the BP record declares it.
- One `research/l3-candidate-universe.yaml` per parent BP (5 depositions,
  riding the existing `research/README.md` from the admission tranches).
- Parent BP patch: `metadata.activity_references[]` plus one change_history
  entry; version unchanged per SIV-004 (additive metadata-only).
- Classification: every candidate FAILs standalone executability and resource
  dedication (CR-BP-32 section 5); all carry `decomposition_boundary:
  l4-reached` (CR-BP-32 section 12; dea:Task lifecycle: proposed).
- Cohesion: 10 candidates at 9/9, 10 at 8/9 (CR-BP-32 section 6).

## 4. Gate posture

- ACT-001..010: CONFORMANT, 0 findings; Activity records 501 -> 521.
- ECF conformance: 672 -> 692 entries conform.
- Execution boundary: Records checked 672 -> 692.
- Conformance report: 712 -> 732 records, all L4.
- No dual-composed BPs in scope; no deprecated BPs in scope.

## 5. Repository changes

- 20 new Activity records (Section 2).
- 5 research depositions under the admitted BPs' `research/` directories.
- 5 parent BP records patched (activity_references + change_history; version
  unchanged).
- Count-assertion updates: tests/test_check_activity_model.py (501 -> 521),
  tests/test_check_execution_boundary.py (672 -> 692),
  tests/test_architectural_regression.py (712 -> 732).
- Baseline + inventory + conformance report regenerated.
- change-requests/README.md row; CATALOG regenerated
  (open_change_requests 80 -> 81).

## 6. What this CR does NOT do

- Does not admit, deprecate, reclassify, or rename any Business Process; all
  five parents were admitted by CR-BP-64..67 and are unchanged in identity.
- Does not touch the register, the disposition register, or the tranche plan
  (no new BPs; admission arithmetic is untouched).
- Does not introduce L4 Task records (blocked on metamodel-owned dea:Task).
- Does not authorize or exercise specialization (governance directive:
  decomposition only until L0-L4 stabilizes universally).
- Does not stack on PR #109 (CR-BP-68); this branch is cut from origin/main
  post-#108. The README index row and CATALOG open_change_requests assume the
  #109 merge ordering; if #109 merges second, those two lines rebase-resolve
  per the documented stack pattern.

## 7. Acceptance criteria

- [x] 20 Activity records validate against schemas/entities/activity.schema.json
      (Draft-07, 0 invalid).
- [x] check_activity_model.py: CONFORMANT, 0 findings, 521 records.
- [x] check_ecf_conformance.py: 692 entries conform.
- [x] ACT-010 bidirectional integrity: 0 dangling references, 0 asymmetries.
- [x] Full pytest suite green; 24-gate suite CONFORMANT (0 blocking,
      0 advisory); CR-META 0 new findings.
- [x] CATALOG.yaml regenerated and current.

## 8. Result

Landed as PR #110. All five admitted Activate/Retire cells now carry full
L0 to L3 stacks; catalog coverage is 131 BPs / 521 Activities with the
Activate and Retire stages populated at L3 for the first time.
