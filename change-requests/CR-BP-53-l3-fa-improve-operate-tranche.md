# CR-BP-53: L3 Activity FA Improve + Operate Tranche (FinanceAndAccounting domain completion)

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
**Date**: 2026-09-13
**Carrier**: Twelfth L3 (Activity) contribution slice; completes the FinanceAndAccounting domain's L3 coverage (Conceive + Design + Build: CR-BP-52; this slice: Improve + Operate).
**Depends on**: CR-BP-32 (Activity Model; ACT-001..010), CR-BP-42 (pilot), CR-BP-52 (FA Conceive + Design + Build tranche)
**Lands against**: 126 canonical BP records, 35 canonical PG records, 35 canonical PC records, 309 canonical Activity records; 23 conformance gates CONFORMANT; v0.3.0 tagged (CR-BP-41)

---

## 1. Change Request

Land L3 Activity decompositions for the 11 Business Processes of FinanceAndAccounting's Improve and Operate stages, completing the domain's L3 coverage (5/5 stages).

Per-BP depositions (4 Activities each, 44 total):

| Coordinate | Business Process | Activities |
|---|---|---|
| FA / Improve | `dea:process-conduct-cost-optimization-review` | Assemble Cost Signals; Form Cost Review Findings; Route Findings to Financial Tracks; Commit Cost Review Outcomes |
| FA / Improve | `dea:process-evolve-treasury-and-funding-model` | Monitor Market and Funding Shifts; Review Treasury Exposures; Design Model Evolutions; Commit Model Evolutions |
| FA / Improve | `dea:process-refine-financial-controls-and-policies` | Analyze Control Findings; Design Control Refinements; Commit Refinements; Measure Refinement Effectiveness |
| FA / Operate | `dea:process-execute-payroll` | Calculate Compensation; Compute Withholdings; Disburse Payroll; Produce Statutory Filings |
| FA / Operate | `dea:process-manage-cash-and-liquidity` | Monitor Cash Positions; Forecast Liquidity; Execute Investment Decisions; Report Treasury Position |
| FA / Operate | `dea:process-manage-tax-compliance-and-filings` | Prepare Tax Returns; Schedule Tax Payments; Monitor Tax Exposures; Maintain Filing Record |
| FA / Operate | `dea:process-operate-financial-reporting-and-disclosure` | Prepare Financial Statements; Prepare Footnotes and Disclosures; Review Reporting Package; Deliver Reports and Disclosures |
| FA / Operate | `dea:process-operate-general-ledger` | Process Journal Entries; Maintain Account Integrity; Coordinate Subledger Flows; Monitor Ledger Health |
| FA / Operate | `dea:process-perform-financial-close` | Execute Period-End Entries; Execute Reconciliations; Produce Management Reports; Certify Period Close |
| FA / Operate | `dea:process-run-accounts-payable` | Match Invoices; Record Payment Approvals; Execute Payments to Plan; Maintain Payables Record |
| FA / Operate | `dea:process-run-accounts-receivable` | Issue Customer Invoices; Manage Collections; Apply Cash to Ledger; Maintain Receivables Record |

Every candidate was tested against the four L2 criteria (CR-BP-32 §5); all 44 FAIL Standalone Executability and Resource Dedication and classify as Activities. Cohesion scores (§6) are recorded per candidate in each research deposition.

## 2. Deposition mechanics (pattern per CR-BP-42 §2)

1. **Research deposition** per BP at `entities/v1-alpha/dea:process-<bp>/research/l3-candidate-universe.yaml` (+ state-directory README.md).
2. **Canonical landing**: one record per Activity, conforming to `schemas/entities/activity.schema.json`; `ecfConformance` blocks inherit each BP's own canonical coordinate identifier (read from the BP record, not assumed). All 44 records pass Draft-07 validation.
3. **Decomposition boundary**: all records carry `decomposition_boundary: l4-reached` (CR-BP-32 §12).
4. **Bidirectional traceability (ACT-010)**: each parent BP gains `metadata.activity_references[]` and a CR-BP-53 `change_history` entry. Nine BPs of the CR-BP-21e.1 era carry the legacy shape (top-level `change_history`, no `metadata` block); these gained a `metadata` block containing `established_by` / `established_at` (preserving CR-BP-21e.1 provenance) plus `activity_references[]`, with the change entry appended to their existing top-level `change_history` in native style, matching CR-BP-48/49/52 section 2.4 handling. All 11 patched records pass `schemas/entity.schema.json` validation. Versions unchanged per SIV-004.
5. **Reconciliation artifacts**: baseline and conformance report regenerated (549 records, all at L4).
6. **Count assertion updates**: ACT suite 309 -> 353; EXE suite 470 -> 514; conformance-report test 505 -> 549.

## 3. Gate posture

- Gate [15] ACT-001..010 live run: **CONFORMANT, 353 Activity records, 0 findings**.
- Gate [8] ECF conformance: **514 entries conform** (was 470).
- Full suite: **23 gates, 0 blocking, 0 advisory failures**.

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `entities/v1-alpha/dea:activity-*/` (44 dirs) | NEW | Canonical Activity records (4 per BP) |
| `entities/v1-alpha/dea:process-<bp>/research/` (x11) | NEW | Depositions + READMEs |
| `entities/v1-alpha/dea:process-<bp>/dea:process-<bp>.yaml` (x11) | MOD | `metadata.activity_references[]` + CR-BP-53 change_history (9 legacy-shape records handled per section 2.4) |
| `tests/test_check_activity_model.py` | MOD | Count assertions: 353 Activity records |
| `tests/test_check_execution_boundary.py` | MOD | Count assertions: 514 records checked |
| `tests/test_architectural_regression.py` | MOD | Conformance report: 549 records, all L4 |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated (11 mutated parent BP hash lines) |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated by gate [10]; 549 records |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 64 -> 65 |
| `change-requests/CR-BP-53-l3-fa-improve-operate-tranche.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-53 row added |

## 5. What this CR is NOT

- **NOT a Task (L4) landing.** All Activities terminate at `l4-reached`.
- **NOT a schema, validator-rule, CI, or gate change.** Wiring from CR-BP-42 is reused unchanged; the shared entity schema already permits `metadata` on legacy-shape records.
- **NOT an L3 sweep of other domains.** After this slice, five domains are fully L3-covered (PR, EO, GE, PV, FA); PeopleAndCulture plus the strategy-direction coordinates remain.
- **NOT a remediation of the dangling `dea:process-frame-financial-policy-thesis` composes reference** (queued separately).

## 6. Acceptance criteria

1. All 44 new Activity records validate against `schemas/entities/activity.schema.json` (Draft-07).
2. `python3 scripts/check_activity_model.py` runs CONFORMANT: 353 Activity records, 0 findings.
3. Each of the 11 parent BPs declares its 4 Activity ids in `metadata.activity_references[]` (ACT-010).
4. The 9 legacy-shape BP records validate against `schemas/entity.schema.json` after gaining `metadata`.
5. `python3 scripts/check_ecf_conformance.py` reports 514 entries conform.
6. `python3 scripts/build_inventory.py --self-test --strict` passes after regeneration.
7. Full pytest suite passes; `scripts/conformance_result.py` remains CONFORMANT (23 gates).
8. `python3 scripts/check_cr_metadata.py` reports 0 new findings.
9. `python3 scripts/check_catalog_index.py --strict` passes (all 11 new research/ state directories carry README.md).
10. No validator-rule, schema, CI, or governance-decision change.

## 7. Result

CR-BP-53 completes the FinanceAndAccounting domain's L3 coverage: 44 new canonical Activity records across 11 Business Processes in the Improve and Operate stages, bringing the catalog to 353 Activity records at 0 findings against gate [15]. FinanceAndAccounting is the fifth fully L3-covered domain (5/5 coordinates, 20 BPs, 80 Activities), joining PartyAndRelationship (36), EnablementAndOperations (113), GovernanceAndExistence (60), and ProductAndValue (64). 88 of 126 BPs are now L3-decomposed. The structured deposition pattern has held across twelve slices without modification.
