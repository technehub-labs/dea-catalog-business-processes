# CR-BP-52: L3 Activity FA Conceive + Design + Build Tranche

**Status**: Proposed
**Layer**: L3
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-13
**Carrier**: Eleventh L3 (Activity) contribution slice; first of two tranches completing the FinanceAndAccounting domain's L3 coverage (this slice: Conceive + Design + Build; Improve + Operate follow as CR-BP-53).
**Depends on**: CR-BP-32 (Activity Model; ACT-001..010), CR-BP-42 (pilot), CR-BP-43..51 (scaled tranches)
**Lands against**: 126 canonical BP records, 35 canonical PG records, 35 canonical PC records, 273 canonical Activity records; 23 conformance gates CONFORMANT; v0.3.0 tagged (CR-BP-41)

---

## 1. Change Request

Land L3 Activity decompositions for the 9 Business Processes of FinanceAndAccounting's Conceive, Design, and Build stages.

Per-BP depositions (4 Activities each, 36 total):

| Coordinate | Business Process | Activities |
|---|---|---|
| FA / Conceive | `dea:process-frame-finance-strategy` | Assess Finance Strategy Context; Frame Monetary Model; Frame Funding and Capital Approach; Commit Finance Strategy |
| FA / Design | `dea:process-design-financial-plan-structure` | Design Chart of Accounts; Design Cost Allocation Model; Design Financial Controls Framework; Commit Plan Structure |
| FA / Design | `dea:process-design-financial-controls-and-policies` | Analyze Control and Policy Gaps; Design Financial Control Objectives; Design Financial Policies; Commit Controls and Policies Design |
| FA / Design | `dea:process-design-tax-position-and-strategy` | Assess Tax Exposures; Document Tax Positions; Design Tax Strategy; Commit Tax Position and Strategy |
| FA / Design | `dea:process-design-treasury-and-funding-model` | Design Cash and Liquidity Policy; Design Funding Structure; Design Treasury Operating Model; Commit Treasury and Funding Model |
| FA / Build | `dea:process-build-budgeting-and-forecasting-systems` | Build Budget Models; Integrate Forecasting Integrations; Implement Planning Controls; Verify Planning System Readiness |
| FA / Build | `dea:process-implement-financial-systems-and-ledger` | Deploy Chart of Accounts; Configure Posting Rules; Deploy Financial Reports; Verify Ledger Implementation |
| FA / Build | `dea:process-onboard-tax-and-compliance-capability` | Execute Filings and Registrations; Implement Tax Controls; Establish Compliance Calendar; Verify Tax Capability Readiness |
| FA / Build | `dea:process-secure-funding-facilities` | Negotiate Funding Lines; Execute Funding Line Documentation; Stand Up Finance Function; Deploy ERP Finance Module |

Every candidate was tested against the four L2 criteria (CR-BP-32 §5); all 36 FAIL Standalone Executability and Resource Dedication and classify as Activities. Cohesion scores (§6) are recorded per candidate in each research deposition.

## 2. Deposition mechanics (pattern per CR-BP-42 §2)

1. **Research deposition** per BP at `entities/v1-alpha/dea:process-<bp>/research/l3-candidate-universe.yaml` (+ state-directory README.md).
2. **Canonical landing**: one record per Activity, conforming to `schemas/entities/activity.schema.json`; `ecfConformance` blocks inherit each BP's own canonical coordinate identifier (read from the BP record, not assumed). All 36 records pass Draft-07 validation.
3. **Decomposition boundary**: all records carry `decomposition_boundary: l4-reached` (CR-BP-32 §12).
4. **Bidirectional traceability (ACT-010)**: each parent BP gains `metadata.activity_references[]` and a CR-BP-52 `change_history` entry. Six BPs of the CR-BP-21e.1 era (`design-financial-controls-and-policies`, `design-tax-position-and-strategy`, `design-treasury-and-funding-model`, `build-budgeting-and-forecasting-systems`, `implement-financial-systems-and-ledger`, `onboard-tax-and-compliance-capability`) carry the legacy shape (top-level `change_history`, no `metadata` block); these gained a `metadata` block containing `established_by` / `established_at` (preserving CR-BP-21e.1 provenance) plus `activity_references[]`, with the change entry appended to their existing top-level `change_history` in native style, matching CR-BP-48/49 section 2.4 handling. All 9 patched records pass `schemas/entity.schema.json` validation. Versions unchanged per SIV-004.
5. **Reconciliation artifacts**: baseline and conformance report regenerated (505 records, all at L4).
6. **Count assertion updates**: ACT suite 273 -> 309; EXE suite 434 -> 470; conformance-report test 469 -> 505.

## 3. Gate posture

- Gate [15] ACT-001..010 live run: **CONFORMANT, 309 Activity records, 0 findings**.
- Gate [8] ECF conformance: **470 entries conform** (was 434).
- Full suite: **23 gates, 0 blocking, 0 advisory failures**.

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `entities/v1-alpha/dea:activity-*/` (36 dirs) | NEW | Canonical Activity records (4 per BP) |
| `entities/v1-alpha/dea:process-<bp>/research/` (x9) | NEW | Depositions + READMEs |
| `entities/v1-alpha/dea:process-<bp>/dea:process-<bp>.yaml` (x9) | MOD | `metadata.activity_references[]` + CR-BP-52 change_history (6 legacy-shape records handled per section 2.4) |
| `tests/test_check_activity_model.py` | MOD | Count assertions: 309 Activity records |
| `tests/test_check_execution_boundary.py` | MOD | Count assertions: 470 records checked |
| `tests/test_architectural_regression.py` | MOD | Conformance report: 505 records, all L4 |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated (9 mutated parent BP hash lines) |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated by gate [10]; 505 records |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 63 -> 64 |
| `change-requests/CR-BP-52-l3-fa-conceive-design-build-tranche.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-52 row added |

## 5. What this CR is NOT

- **NOT a Task (L4) landing.** All Activities terminate at `l4-reached`.
- **NOT a schema, validator-rule, CI, or gate change.** Wiring from CR-BP-42 is reused unchanged; the shared entity schema already permits `metadata` on legacy-shape records.
- **NOT the complete FinanceAndAccounting L3 sweep.** Improve + Operate (11 BPs) follow as CR-BP-53.
- **NOT a remediation of the dangling `dea:process-frame-financial-policy-thesis` composes reference** (queued separately).

## 6. Acceptance criteria

1. All 36 new Activity records validate against `schemas/entities/activity.schema.json` (Draft-07).
2. `python3 scripts/check_activity_model.py` runs CONFORMANT: 309 Activity records, 0 findings.
3. Each of the 9 parent BPs declares its 4 Activity ids in `metadata.activity_references[]` (ACT-010).
4. The 6 legacy-shape BP records validate against `schemas/entity.schema.json` after gaining `metadata`.
5. `python3 scripts/check_ecf_conformance.py` reports 470 entries conform.
6. `python3 scripts/build_inventory.py --self-test --strict` passes after regeneration.
7. Full pytest suite passes; `scripts/conformance_result.py` remains CONFORMANT (23 gates).
8. `python3 scripts/check_cr_metadata.py` reports 0 new findings.
9. `python3 scripts/check_catalog_index.py --strict` passes (all 9 new research/ state directories carry README.md).
10. No validator-rule, schema, CI, or governance-decision change.

## 7. Result

CR-BP-52 lands L3 coverage for FinanceAndAccounting's Conceive, Design, and Build stages: 36 new canonical Activity records across 9 Business Processes, bringing the catalog to 309 Activity records at 0 findings against gate [15]. After this slice, FinanceAndAccounting has L3 coverage in 3 of 5 stages; Improve + Operate complete the domain as CR-BP-53. The structured deposition pattern has held across eleven slices without modification.
