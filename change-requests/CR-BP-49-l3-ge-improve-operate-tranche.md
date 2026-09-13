# CR-BP-49: L3 Activity GE Improve + Operate Tranche (GovernanceAndExistence domain completion)

**Status**: Proposed
**Layer**: L3
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-13
**Carrier**: Eighth L3 (Activity) contribution slice; completes the GovernanceAndExistence domain's L3 coverage (Conceive + Design + Build: CR-BP-48; this slice: Improve + Operate).
**Depends on**: CR-BP-32 (Activity Model; ACT-001..010), CR-BP-42 (pilot), CR-BP-48 (GE Conceive + Design + Build tranche)
**Lands against**: 126 canonical BP records, 35 canonical PG records, 35 canonical PC records, 181 canonical Activity records; 23 conformance gates CONFORMANT; v0.3.0 tagged (CR-BP-41)

---

## 1. Change Request

Land L3 Activity decompositions for the 7 Business Processes of GovernanceAndExistence's Improve and Operate stages, completing the domain's L3 coverage (5/5 stages; the deprecated `develop-governance-strategy` BP remains excluded per CR-BP-48 §1).

Per-BP depositions (4 Activities each, 28 total):

| Coordinate | Business Process | Activities |
|---|---|---|
| GE / Improve | `dea:process-improve-policy-and-control-framework` | Measure Policy Gaps; Update Policy Standards; Strengthen Compliance Posture; Commit Framework Improvements |
| GE / Improve | `dea:process-review-governance-effectiveness` | Measure Governance Performance; Capture Lessons Learned; Formulate Effectiveness Recommendations; Deliver Effectiveness Reviews |
| GE / Improve | `dea:process-score-audit-findings` | Score Finding Severity; Assess Finding Recurrence; Measure Findings Against Standards; Report Quality Trends |
| GE / Operate | `dea:process-audit-policy-compliance` | Plan Compliance Audits; Execute Compliance Audits; Report Audit Findings; Track Follow-Up Actions |
| GE / Operate | `dea:process-conduct-assurance-review` | Assemble Assurance Evidence; Measure Evidence Against Standards; Report Assurance Findings; Maintain Audit Quality |
| GE / Operate | `dea:process-operate-enterprise-risk-oversight` | Execute Risk Reviews; Surface Risk Exposures; Deliver Mitigations to Bodies; Maintain Risk Registers |
| GE / Operate | `dea:process-operate-governance-oversight` | Run Board and Committee Cycles; Facilitate Governance Decisions; Record Governance Decisions; Maintain Governance Machinery |

Every candidate was tested against the four L2 criteria (CR-BP-32 §5); all 28 FAIL Standalone Executability and Resource Dedication and classify as Activities. Cohesion scores (§6) are recorded per candidate in each research deposition.

## 2. Deposition mechanics (pattern per CR-BP-42 §2)

1. **Research deposition** per BP at `entities/v1-alpha/dea:process-<bp>/research/l3-candidate-universe.yaml` (+ state-directory README.md).
2. **Canonical landing**: one record per Activity, conforming to `schemas/entities/activity.schema.json`; `ecfConformance` blocks inherit each BP's coordinate (`ecf:governanceExistence.improve` / `.operate`). All 28 records pass Draft-07 validation.
3. **Decomposition boundary**: all records carry `decomposition_boundary: l4-reached` (CR-BP-32 §12).
4. **Bidirectional traceability (ACT-010)**: each parent BP gains `metadata.activity_references[]` and a CR-BP-49 `change_history` entry. Four BPs of the CR-BP-21f.1 era (`improve-policy-and-control-framework`, `score-audit-findings`, `conduct-assurance-review`, `operate-enterprise-risk-oversight`) carry the legacy shape (top-level `change_history`, no `metadata` block); these gained a `metadata` block containing `established_by` / `established_at` (preserving CR-BP-21f.1 provenance) plus `activity_references[]`, with the change entry appended to their existing top-level `change_history` in native style, matching CR-BP-48 section 2.4 handling. All 7 patched records pass `schemas/entity.schema.json` validation. Versions unchanged per SIV-004.
5. **Reconciliation artifacts**: baseline and conformance report regenerated (405 records, all at L4).
6. **Count assertion updates**: ACT suite 181 -> 209; EXE suite 342 -> 370; conformance-report test 377 -> 405.

## 3. Gate posture

- Gate [15] ACT-001..010 live run: **CONFORMANT, 209 Activity records, 0 findings**.
- Gate [8] ECF conformance: **370 entries conform** (was 342).
- Full suite: **23 gates, 0 blocking, 0 advisory failures**.

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `entities/v1-alpha/dea:activity-*/` (28 dirs) | NEW | Canonical Activity records (4 per BP) |
| `entities/v1-alpha/dea:process-<bp>/research/` (x7) | NEW | Depositions + READMEs |
| `entities/v1-alpha/dea:process-<bp>/dea:process-<bp>.yaml` (x7) | MOD | `metadata.activity_references[]` + CR-BP-49 change_history (4 legacy-shape records handled per §2.4) |
| `tests/test_check_activity_model.py` | MOD | Count assertions: 209 Activity records |
| `tests/test_check_execution_boundary.py` | MOD | Count assertions: 370 records checked |
| `tests/test_architectural_regression.py` | MOD | Conformance report: 405 records, all L4 |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated (7 mutated parent BP hash lines) |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated by gate [10]; 405 records |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 60 -> 61 |
| `change-requests/CR-BP-49-l3-ge-improve-operate-tranche.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-49 row added |

## 5. What this CR is NOT

- **NOT a Task (L4) landing.** All Activities terminate at `l4-reached`.
- **NOT a schema, validator-rule, CI, or gate change.** Wiring from CR-BP-42 is reused unchanged.
- **NOT a decomposition of the deprecated `dea:process-develop-governance-strategy`** (excluded per CR-BP-48 §1).
- **NOT an L3 sweep of other domains.** After this slice, PartyAndRelationship, EnablementAndOperations, and GovernanceAndExistence are fully L3-covered; the remaining 4 domains (ProductAndValue, FinanceAndAccounting, PeopleAndCulture, plus the strategy-direction coordinates) await tranches.
- **NOT a remediation of the dangling `dea:process-frame-financial-policy-thesis` composes reference** (queued separately).

## 6. Acceptance criteria

1. All 28 new Activity records validate against `schemas/entities/activity.schema.json` (Draft-07).
2. `python3 scripts/check_activity_model.py` runs CONFORMANT: 209 Activity records, 0 findings.
3. Each of the 7 parent BPs declares its 4 Activity ids in `metadata.activity_references[]` (ACT-010).
4. The 4 legacy-shape BP records validate against `schemas/entity.schema.json` after gaining `metadata`.
5. `python3 scripts/check_ecf_conformance.py` reports 370 entries conform.
6. `python3 scripts/build_inventory.py --self-test --strict` passes after regeneration.
7. Full pytest suite passes; `scripts/conformance_result.py` remains CONFORMANT (23 gates).
8. `python3 scripts/check_cr_metadata.py` reports 0 new findings.
9. `python3 scripts/check_catalog_index.py --strict` passes (all 7 new research/ state directories carry README.md).
10. No validator-rule, schema, CI, or governance-decision change.

## 7. Result

CR-BP-49 completes the GovernanceAndExistence domain's L3 coverage: 28 new canonical Activity records across 7 Business Processes in the Improve and Operate stages, bringing the catalog to 209 Activity records at 0 findings against gate [15]. GovernanceAndExistence is the third fully L3-covered domain (5/5 coordinates, 15 live BPs, 60 Activities), joining PartyAndRelationship (9 BPs, 36 Activities) and EnablementAndOperations (28 BPs, 113 Activities). 52 of 126 BPs are now L3-decomposed. The structured deposition pattern has held across eight slices without modification.
