# CR-BP-42: L3 Activity Pilot Deposition (dea:process-operate-quality-control)

**Status**: Proposed
**Layer**: L3
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-13
**Carrier**: First L3 (Activity) contribution slice; applies the structured deposition pattern (research deposition -> canonical landing) one layer below L2, mirroring the CR-BP-11 L1 candidate-universe approach. Follows CR-BP-32 (Activity Model, gate [15]).
**Depends on**: CR-BP-32 (Activity Model; ACT-001..010; `schemas/entities/activity.schema.json`), CR-BP-21d.1 (parent BP landing), CR-BP-16 (conformance gate)
**Lands against**: 126 canonical BP records, 35 canonical PG records, 35 canonical PC records; 0 Activity records pre-slice; 23 conformance gates CONFORMANT

---

## 1. Change Request

Land the first L3 Activity records in the catalog using the structured deposition approach: a research deposition (candidate universe with L2-criteria tests, cohesion scores, and dispositions) followed by canonical Activity records, under a single pilot Business Process.

Pilot BP: `dea:process-operate-quality-control` (EnablementAndOperations / Operate; PG `dea:group-execution-and-fulfillment`). Chosen because it is well-bounded (trigger and outcome explicitly reference per-batch inspection and disposition), carries `process_type: core` in the thickest ECF coordinate (9 BPs), and has strong external-framework anchoring (APQC PCF, ISO 9001:2015 clause 8.7, ISO 2859/ISO 3951).

Five Activities land:

| # | Activity id | Name | Cohesion (0-9) |
|---|---|---|---|
| 1 | `dea:activity-plan-quality-inspection` | Plan Quality Inspection | 8 |
| 2 | `dea:activity-execute-inspection-and-testing` | Execute Inspection and Testing | 9 |
| 3 | `dea:activity-record-inspection-results` | Record Inspection Results | 8 |
| 4 | `dea:activity-disposition-nonconforming-output` | Disposition Nonconforming Output | 9 |
| 5 | `dea:activity-report-quality-performance` | Report Quality Performance | 7 |

Each candidate was tested against the four L2 criteria (CR-BP-32 §5: Input-Output Transformation, Objective Contribution, Standalone Executability, Resource Dedication). All five FAIL Standalone Executability and Resource Dedication and therefore classify as Activities, not Business Processes.

## 2. Deposition mechanics

1. **Research deposition** at `entities/v1-alpha/dea:process-operate-quality-control/research/l3-candidate-universe.yaml`: 5 candidates with per-candidate L2-criteria test results, cohesion scores, in/out-of-scope boundaries, evidence, and dispositions (`landed`). Mirrors the CR-BP-11 `l1-candidate-universe.yaml` shape one layer down.
2. **Canonical landing**: one record per Activity at `entities/v1-alpha/dea:activity-<id>/dea:activity-<id>.yaml`, conforming to `schemas/entities/activity.schema.json` (`additionalProperties: false`). All 5 records pass Draft-07 validation.
3. **Decomposition boundary**: no Task records exist yet (`dea:Task` is metamodel-owned, `lifecycle: proposed`), so each Activity carries `decomposition_boundary: l4-reached` (CR-BP-32 §12; accepted by ACT-004 as the alternative to a non-empty `composes[]`).
4. **Bidirectional traceability (ACT-010)**: the parent BP gains `metadata.activity_references[]` listing all 5 Activity ids and a `change_history` entry. The change is additive and metadata-only; BP identity and semantics are unchanged, so the BP version remains 1.0.0 per SIV-004 (CR-BP-34d).
5. **ECF conformance manifest**: each Activity record carries an `ecfConformance` block (CR-ECF-CG-001..004) inheriting the parent BP coordinate (`ecf:enablementAndOperations.operate`, `affiliation: inherits-catalog`). `schemas/entities/activity.schema.json` is extended additively with an optional `ecfConformance` property (mirrored from `schemas/entity.schema.json`) so the block is schema-legal under `additionalProperties: false`. Gate [8] requires the block on every canonical entity file.
6. **CI schema dispatch**: `.github/workflows/ci.yml` per-file dispatch (CR-BP-12) gains the mapping `type: Activity -> schemas/entities/activity.schema.json`; without it, Activity records fall back to `schemas/entity.schema.json` and fail on the BP-mandatory `process_intent` field.
7. **Reconciliation baseline**: `reconciliation/baseline/v1.yaml` regenerated via `scripts/build_inventory.py` (deterministic; strict self-test passes). Diff is exactly one hash line (the mutated parent BP). Activity records are not inventory-counted record types (BP/PG/PC counts unchanged at 126/35/35).
8. **Vacuity test updates**: three test suites carried assertions that locked the pre-contribution empty state (0 Activity records; 161/196 record counts). They now assert the post-pilot reality: `test_check_activity_model.py` (5 Activity records, 0 findings), `test_check_execution_boundary.py` (166 records checked, 0 opted-in), `test_architectural_regression.py` (conformance report 201 records, all at L4).

## 3. Gate posture

Gate [15] Activity Model (ACT-001..010) transitions from vacuous (0 Activity records) to exercised:

- Pre-patch live run: exactly 5 findings, all ACT-010 (parent BP missing back-references). The validator caught the incomplete bidirectional traceability by design.
- Post-patch live run: **CONFORMANT, 0 findings** across ACT-001..010.
- `--self-test`: PASS (20 cases).

All other gates unchanged: no blocking-gate impact; 18-gate suite remains CONFORMANT.

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `entities/v1-alpha/dea:process-operate-quality-control/research/l3-candidate-universe.yaml` | NEW | Research deposition: 5 L3 candidates, L2-criteria tests, cohesion scores, dispositions |
| `entities/v1-alpha/dea:activity-plan-quality-inspection/dea:activity-plan-quality-inspection.yaml` | NEW | Canonical Activity record |
| `entities/v1-alpha/dea:activity-execute-inspection-and-testing/dea:activity-execute-inspection-and-testing.yaml` | NEW | Canonical Activity record |
| `entities/v1-alpha/dea:activity-record-inspection-results/dea:activity-record-inspection-results.yaml` | NEW | Canonical Activity record |
| `entities/v1-alpha/dea:activity-disposition-nonconforming-output/dea:activity-disposition-nonconforming-output.yaml` | NEW | Canonical Activity record |
| `entities/v1-alpha/dea:activity-report-quality-performance/dea:activity-report-quality-performance.yaml` | NEW | Canonical Activity record |
| `entities/v1-alpha/dea:process-operate-quality-control/dea:process-operate-quality-control.yaml` | MOD | Adds `metadata.activity_references[]` (5 ids) + CR-BP-42 `change_history` entry; version unchanged (1.0.0) per SIV-004 |
| `entities/v1-alpha/dea:process-operate-quality-control/research/README.md` | NEW | Research state-directory README (catalog-index strict-mode requirement) |
| `schemas/entities/activity.schema.json` | MOD | Additive: optional `ecfConformance` property (mirrored from `schemas/entity.schema.json`) so Activity records can carry the gate-[8] manifest under `additionalProperties: false` |
| `.github/workflows/ci.yml` | MOD | Per-file schema dispatch gains `type: Activity -> schemas/entities/activity.schema.json` (CR-BP-12 dispatch) |
| `tests/test_check_activity_model.py` | MOD | Vacuity assertions updated: 5 Activity records, 0 findings (was 0 records) |
| `tests/test_check_execution_boundary.py` | MOD | Record-count assertions updated: 166 records (was 161) |
| `tests/test_architectural_regression.py` | MOD | Conformance-report assertions updated: 201 records, all L4 (was 196) |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated; one hash line (parent BP) |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated by gate [10]; 201 records, all at conformance level L4 |
| `change-requests/CR-BP-42-l3-activity-pilot.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-42 row added |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 52 -> 53 |

## 5. What this CR is NOT

- **NOT a Task (L4) landing.** `dea:Task` remains metamodel-owned (`lifecycle: proposed`); Activities terminate at the `l4-reached` boundary marker (CR-BP-32 §12).
- **NOT a full-ECF L3 sweep.** This is the pilot slice on one BP. Per-coordinate or per-domain L3 tranches are follow-on CRs patterned on this slice.
- **NOT a validator-rule change.** ACT-001..010 and all other gate rules are unchanged. The only schema change is the additive optional `ecfConformance` property on `activity.schema.json`, and the only CI change is wiring the existing schema into the per-file dispatch; both are first-contribution wiring, not rule changes.
- **NOT an execution-semantics change.** No execution-ordering, implementation-detail, or execution-model fields on any Activity (ACT-006/008/009 clean; CR-BP-33 owns execution).
- **NOT a remediation of the dangling `dea:process-frame-financial-policy-thesis` composes reference** in `dea:group-financial-model-conception` (surfaced 2026-09-13 during L2 coverage analysis). That is a separate, queued item requiring its own slice.

## 6. Acceptance criteria

1. All 5 Activity records validate against `schemas/entities/activity.schema.json` (Draft-07), including the new optional `ecfConformance` property.
2. `python3 scripts/check_activity_model.py` runs CONFORMANT with 0 findings on the live catalog.
3. `python3 scripts/check_activity_model.py --self-test` passes (20 cases).
4. Parent BP declares all 5 Activity ids in `metadata.activity_references[]` (ACT-010); BP version unchanged (SIV-004 clean).
5. `python3 scripts/check_ecf_conformance.py` reports 166 entries conform (was 161; the 5 new Activity records carry the manifest).
6. `python3 scripts/build_inventory.py --self-test --strict` passes after regeneration.
7. Full pytest suite passes; `scripts/conformance_result.py` remains CONFORMANT (23 gates).
8. `python3 scripts/check_cr_metadata.py` reports 0 new findings.
9. `python3 scripts/check_catalog_index.py --strict` passes (research/ state directory carries a README.md).
10. No entity, validator-rule, or governance-decision change outside the additive changes listed in §4.

## 7. Result

CR-BP-42 lands the first L3 Activity records in the catalog (5 Activities under `dea:process-operate-quality-control`) using the structured deposition approach, exercising gate [15] (ACT-001..010) with real records for the first time. The pilot validates the deposition mechanics (research candidate universe, schema-conformant canonical records, ACT-010 bidirectional traceability, reconciliation-baseline regeneration) as the repeatable pattern for subsequent per-coordinate L3 tranches.
