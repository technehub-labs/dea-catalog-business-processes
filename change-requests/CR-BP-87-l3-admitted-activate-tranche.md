# CR-BP-87 - L3 Activity Admitted-Activate-BP Decomposition Tranche

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
**Date**: 2026-09-17
**Carrier**: Fourth L3 (Activity) tranche landing after CR-BP-69 / CR-BP-77 / CR-BP-79; closes the final four L0-L3 gaps created by the CR-BP-81 / CR-BP-82 / CR-BP-83 / CR-BP-86 admission tranches at the four ADMIT-CANONICAL Activate cells (AO.Activate, EO.Activate, FA.Activate, SD.Activate). Single combined PR (Option A): 4 BPs decomposed to 16 Activities in one commit.
**Depends on**: CR-BP-32 (Activity Model; ACT-001..010), CR-BP-42 (pilot), CR-BP-43..57 (per-stage L3 tranches), CR-BP-69 (first admitted-BP decomposition tranche), CR-BP-77 (second admitted-BP tranche), CR-BP-79 (G&E Retire L3 tranche precedent), CR-BP-80 (escape-clause exercise at five backlog-deferred cells), CR-BP-81/-82/-83/-86 (admission tranches).
**Lands against**: 139 canonical BP records, 48 canonical PG records, 553 canonical Activity records (was 537), 23 canonical Discovery records; full pytest suite + CR-META + catalog-index gates CONFORMANT.

---

## 1. Change Request

Land L3 Activity decompositions for the four Business Processes admitted by the Activate admission tranches (CR-BP-81 / CR-BP-82 / CR-BP-83 / CR-BP-86). Each BP gains 4 Activity records (16 total), derived from the BP's trigger and outcome text using the L2 criteria in CR-BP-32 section 5. Every candidate FAILS Standalone Executability and Resource Dedication and therefore classifies as an Activity, not a BP. Cohesion scores are recorded per candidate in each research deposition.

| Coordinate | Parent BP | Activities |
|---|---|---|
| AgencyAndOrganization x Activate | `dea:process-mobilize-licensed-workforce` | Verify Regulator Licence Or Registration; Attest Fitness And Propriety; Record Supervised-Training Completion; Activate Signing Authority Or Controlled-Function Designation |
| EnablementAndOperations x Activate | `dea:process-activate-operations-capability` | Acquire Regulator-Issued Operations Authorization; Activate Continuing-Supervisor Notification; Bring Operations Manuals and Runbooks Live; Bring Operational Controls Live on the Regulated Operations Record |
| FinanceAndAccounting x Activate | `dea:process-activate-billing-capability` | Acquire Regulator-Acknowledged Accounting or Rate Framework; Acquire Tariff or Pricing Approval; Activate Continuing-Supervisor Notification (Billing); Bring Operational Controls Live on the Regulated Billing Record |
| StrategyAndDirection x Activate | `dea:process-institutionalize-regulated-strategic-plan` | File Supervisor-Acknowledged Strategic-Plan Submission; Complete Supervisor Review and Obtain Acknowledgement on Record; Launch Operational Monitoring Framework; Activate Communications Plan Under Regulator Continuing Supervision |

Activity semantics derive from each parent BP's trigger and outcome text. Definitions and out-of-scope lists cite the parent BP evidence per candidate.

Note on FA Activity #3 — two candidates share the same Activity name "Activate Continuing-Supervisor Notification" because the work is the same supervisory-notification concern at different coordinates. To preserve Activity-id uniqueness across the catalog, the FA Activity carries the qualifier `(Billing)` in its display name and the slug `dea:activity-activate-continuing-supervisor-notification-fa`. The EO Activity retains the bare name. Both share the canonical semantics but resolve to distinct entities.

## 2. Deposition mechanics (pattern per CR-BP-42 section 2)

1. Research deposition per BP at `entities/v1-alpha/dea:process-<bp>/research/l3-candidate-universe.yaml` plus state-directory `README.md`. The existing `research/README.md` per BP is updated to mark CR-BP-87 as landed (replacing the "(forthcoming)" placeholder from the admission tranches).
2. Canonical landing: one record per Activity, conforming to `schemas/entities/activity.schema.json`; `ecfConformance` blocks inherit each BP's coordinate exactly. All 16 records pass Draft-07 validation.
3. Decomposition boundary: all records carry `decomposition_boundary: l4-reached` (CR-BP-32 section 12).
4. Bidirectional traceability (ACT-010): each parent BP gains `metadata.activity_references[]` (4 ids) and a CR-BP-87 `change_history` entry. Versions unchanged per SIV-004 (additive metadata-only).
5. Reconciliation artifacts: `scripts/build_inventory.py` baseline + `scripts/build_conformance_report.py` regenerated.
6. Count assertion updates: Activity records 537 -> 553; EXE records 724 -> 740; conformance-report total_records 772 -> 788 (L4 dict 767+18 -> 785; L3 stays at 3 PCs unchanged).

## 3. Gate posture

- Gate [15] ACT-001..010 live run: CONFORMANT, 553 Activity records (was 537), 0 findings.
- Gate [8] ECF conformance: 740 entries conform (was 724).
- Gate [16] EXE-001..010: CONFORMANT, 740 records checked (was 724), 0 findings.

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `entities/v1-alpha/dea:activity-*/` (16 dirs) | NEW | Canonical Activity records (4 per BP) |
| `entities/v1-alpha/dea:process-<bp>/research/l3-candidate-universe.yaml` (x4) | NEW | Candidate-universe depositions for the four Activate cells |
| `entities/v1-alpha/dea:process-<bp>/dea:process-<bp>.yaml` (x4) | MOD | `metadata.activity_references[]` (4 ids) + CR-BP-87 change_history entry; version unchanged |
| `entities/v1-alpha/dea:process-<bp>/research/README.md` (x4) | MOD | "(forthcoming)" -> "(landed)" for the CR-BP-87 reference |
| `tests/test_check_activity_model.py` | MOD | Count assertions: 537 -> 553 Activity records; docstring tally + CR-BP-87 entry |
| `tests/test_check_execution_boundary.py` | MOD | Count assertions: 724 -> 740 records checked; docstring tally + CR-BP-87 entry |
| `tests/test_architectural_regression.py` | MOD | Conformance report: 772 -> 788 records; L4 dict 769 -> 785 |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated (4 mutated parent BP hash lines) |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated by gate [10]; 788 records |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 96 -> 97 |
| `change-requests/CR-BP-87-l3-admitted-activate-tranche.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-87 row added before `## Cross-repo context` anchor |

## 5. What this CR is NOT

- NOT a Task (L4) landing. All Activities terminate at `l4-reached`.
- NOT a schema, validator-rule, CI, or gate change. Wiring from the pilot and CR-BP-42..77 is reused unchanged.
- NOT an admission, deprecation, reclassification, or rename of any Business Process; the four parents were admitted by CR-BP-81/-82/-83/-86 and are unchanged in identity.
- NOT a discovery exercise; the escape-clause and admission records (CR-BP-80, CR-BP-81/-82/-83/-86) are unchanged and remain the canonical evidence base for the parent BPs.
- NOT an authorisation of specialization (governance directive: decomposition only until L0-L4 stabilizes universally).
- NOT a register flip (no backlog-deferred cell changes; all four parents were already ratified-accepted/landed in registers v13..v16 by CR-BP-81/-82/-83/-86).

## 6. Acceptance criteria

1. All 16 new Activity records validate against `schemas/entities/activity.schema.json` (Draft-07, 0 invalid).
2. `python3 scripts/check_activity_model.py` runs CONFORMANT: 553 Activity records, 0 findings.
3. Each of the four parent BPs declares its 4 Activity ids in `metadata.activity_references[]` (ACT-010).
4. `python3 scripts/check_execution_boundary.py` runs CONFORMANT: 740 records checked, 0 findings.
5. `python3 scripts/check_ecf_conformance.py` reports 740 entries conform.
6. `python3 scripts/build_inventory.py --self-test --strict` passes after regeneration.
7. Full pytest suite passes; CR-META 0 new findings; CATALOG index strict mode passes.
8. No validator-rule, schema, CI, or governance-decision change.
9. BP / PG / PC counts unchanged (no admission surface; only Activity decomposition).
10. All four BP `research/README.md` files updated to reflect CR-BP-87 (landed) instead of "(forthcoming)".

## 7. Result

L3 coverage closed across the four remaining Activate L0-L3 gaps admitted by the CR-BP-81 / CR-BP-82 / CR-BP-83 / CR-BP-86 tranches. Catalog coverage reaches 139 BPs / 553 Activities (16 added by CR-BP-87, +3.0% growth); the four Activate cells (AO.Activate, EO.Activate, FA.Activate, SD.Activate) now carry full L0 to L3 stacks (PC + PG + BP + 4 Activities each).

Discovery-program closure: the five backlog-deferred cells identified in CR-BP-80 are now ALL closed. AOAct, EOAct, FAAct, SDAct are landed (BPs + L3 stacks now in place); SDRet is documented DEFER and remains closed without admission. The discovery loop is fully closed; the four admission tranches (CR-BP-81/-82/-83/-86) and this decomposition tranche (CR-BP-87) jointly complete the Option B programme.

Next slice candidates (per trigger grammar `Proceed`):
- Post-tranche reconciliation slice (CHANGELOG [Unreleased] entries, README "Proposed (this PR)" -> "Merged (PR #N)" status corrections)
- Tranche-close documentation retrospective (catalog status, tranche-plan summary, four-cell programme closure doc)
- ECF conformance audit on the four new cell L4 stacks (run detect_drift.py from dea-metamodel against the four admitted cells)
- L4 Task decomposition for the 16 new Activities (separate program governance required; not in scope of L3-stabilizes-universally directive)