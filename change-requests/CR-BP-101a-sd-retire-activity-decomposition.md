# CR-BP-101a: SD/Retire Activity Decomposition Tranche

**Status**: Proposed
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-19
**Carrier**: L3 Activity decomposition tranche for the SD/Retire Business Process (dea:process-sunset-regulated-strategic-plan) admitted under CR-BP-101 (PR #142).
**Depends on**: CR-BP-32 (Activity model + ACT-001..015), CR-BP-86 / CR-BP-87 (SD/Activate BP-only admission + L3 decomposition precedent), CR-BP-101 (SD/Retire BP-only admission), CR-BP-97 (ACT-011..015 advisory).
**Lands against**: 49 PCs / 49 PGs / 140 BPs / 553 → **560 Activities** / 0 ProcessScope records; v0.4.0+12 commits on main.

---

## 1. Change Request

Decompose the `dea:process-sunset-regulated-strategic-plan` Business Process into 7 canonical Activity records (L3) per the BP's `process_scope.includes[]` enumeration. This slice completes the L3 layer for the SD/Retire coordinate, mirroring the CR-BP-86 / CR-BP-87 precedent at SD/Activate.

| Artifact | Status | Notes |
|---|---|---|
| `entities/v1-alpha/dea:activity-receive-regulator-sunset-directive/dea:activity-receive-regulator-sunset-directive.yaml` | NEW | Activity 1 of 7. Records the regulator directive or rejection notice (failed stress test triggers plan replacement; bank recovery-plan rejection by the SRB; FDIC directive to retire an inadequate resolution plan; state PUC retraction of an approved strategic plan; NHS England directive to retire a non-viable 5-year strategy). |
| `entities/v1-alpha/dea:activity-identify-superseded-regulated-strategic-plan/dea:activity-identify-superseded-regulated-strategic-plan.yaml` | NEW | Activity 2 of 7. Identifies the superseded or replaced plan on the regulated strategic-plan record; preserves the replacement plan's status. |
| `entities/v1-alpha/dea:activity-update-filings-register-regulated-strategic-plan/dea:activity-update-filings-register-regulated-strategic-plan.yaml` | NEW | Activity 3 of 7. Updates the regulated-entity filings register; the regulator identifier, directive date, and effective-retirement date recorded; transmitted to the supervisor under continuing supervision. |
| `entities/v1-alpha/dea:activity-execute-communications-plan-regulated-strategic-plan-sunset/dea:activity-execute-communications-plan-regulated-strategic-plan-sunset.yaml` | NEW | Activity 4 of 7. Executes the regulated-entity communications plan for the regulated strategic-plan sunset under the regulator's continuing supervision. |
| `entities/v1-alpha/dea:activity-preserve-regulator-acknowledged-sunset-record/dea:activity-preserve-regulator-acknowledged-sunset-record.yaml` | NEW | Activity 5 of 7. Preserves the regulator-acknowledged sunset record on the regulated strategic-plan record for the regulated-entity retention policy. |
| `entities/v1-alpha/dea:activity-execute-retained-records-plan-regulated-entity/dea:activity-execute-retained-records-plan-regulated-entity.yaml` | NEW | Activity 6 of 7. Executes the retained-records plan per the regulated-entity retention policy (regulator-prescribed retention period; retired plan's records catalogued). |
| `entities/v1-alpha/dea:activity-notify-affected-business-units-regulator-continuing-supervision/dea:activity-notify-affected-business-units-regulator-continuing-supervision.yaml` | NEW | Activity 7 of 7. Notifies affected business units under the regulator's continuing supervision (regulator-prescribed notification list; cadence; acknowledgement recorded). |
| `entities/v1-alpha/dea:process-sunset-regulated-strategic-plan/dea:process-sunset-regulated-strategic-plan.yaml` | MOD | Adds `metadata.activity_references[]` listing the 7 Activity ids (per CR-BP-86/87 precedent); adds CR-BP-101a entry to `change_history[]` documenting additive metadata-only change (SIV-004: version unchanged). |
| `tests/test_check_activity_model.py` | MOD | Test assertions 553 → 560 Activities; 139 → 140 BP records (live catalog count refresh post-CR-BP-101 + CR-BP-101a). |
| `change-requests/CR-BP-101a-sd-retire-activity-decomposition.md` | NEW | Slice carrier CR (this document). |
| `change-requests/README.md` | MOD | CR-BP-101a row added. |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 114 → 115; entity count 742 → 749. |

## 2. Deposition mechanics

1. **CR-BP-32 §5 classification.** Each of the 7 Activity records fails standalone executability and resource dedication. They are logical units of process structure that compose into the parent BP, not independently-defined Business Processes.
2. **CR-BP-32 §12 decomposition boundary.** Each Activity carries `decomposition_boundary: l4-reached`, indicating the boundary marker pending Task records (dea:Task lifecycle: proposed; first L4 tranche is downstream).
3. **ACT-010 bidirectional traceability.** The parent BP's `metadata.activity_references[]` lists all 7 Activity ids; each Activity record's `belongs_to_business_process` field references the parent BP id. ACT-010 enforces both directions.
4. **ECF conformance.** All 7 Activity records carry the canonical `ecfConformance` block referencing the SD.Retire coordinate (`ecf:strategyDirection.retire`); ECF conformance goes from 743 → 750.
5. **Activity Model (ACT-001..015).** All 7 pass the mandatory ACT-001..010 checks; the OPTIONAL ACT-011..015 fields (Inputs/Outputs, Outcome contribution, Boundary and exclusions, Sibling distinction) are deliberately absent on the new records per CR-BP-97 design intent (OPTIONAL fields backfilled as separate scope).

## 3. Cell evidence summary (CR-BP-80 escape-clause)

Each Activity is grounded in established regulated-entity sunset practices across sectors:

| Sector | Regulator | Mechanism | Activity alignment |
|---|---|---|---|
| Banking | FDIC | FDICIA Section 131 prompt-corrective-action recovery-plan replacement | Activity 1 (directive), Activity 2 (supersession) |
| Banking | SRB | Bank recovery-plan rejection directive | Activity 1 (directive), Activity 4 (communications) |
| Banking | Bank of England PRA | SS9/17 recovery and resolution planning | Activity 1 (directive), Activity 5 (sunset record) |
| Utilities | US state PUC | Integrated resource plan and strategic-plan retraction | Activity 1 (directive), Activity 3 (filings register) |
| Healthcare | NHS England / DoH | Trust 5-year strategy directive | Activity 1 (directive), Activity 7 (BU notification) |

The regulated-entity retention policy (Activity 5 + Activity 6) is universal across the regulated landscape; the supervisor's continuing supervision is the cross-sector governance frame (Activities 3, 4, 7).

## 4. Gate posture

- Gate [3] Process Context (PC-001..PC-008): **CONFORMANT, PASS** (49 records; unchanged).
- Gate [7] MECE (Process Group, PG-001..010): **CONFORMANT, PASS** (49 records; unchanged).
- Gate [8] Provenance (ECF conformance): **PASS** (750 entries, was 743; +7 for the new Activities).
- Gate [10] Activity Model (ACT-001..010 + CR-BP-97 ACT-011..015): **CONFORMANT** (560 records, was 553).
- Full suite: **28 gates, 0 blocking, 0 advisory failures**.

## 5. What this CR is NOT

- **NOT a population tranche for new cells.** No new L0/L1/L2 records land. SD/Retire is already complete at L0 (CR-BP-101) and L1 (CR-BP-101 via PG), and at L2 (CR-BP-101 via BP). This slice completes L3.
- **NOT a removal of the BP-only admission pattern.** CR-BP-86 / CR-BP-87 established that BPs admit first; Activities follow. CR-BP-101a mirrors that pattern for SD/Retire.
- **NOT a backfill of ACT-011..015 OPTIONAL fields.** Per CR-BP-97 design intent, the OPTIONAL fields (Inputs/Outputs, Outcome contribution, Boundary and exclusions, Sibling distinction) are deliberately absent on the new records; backfill is a separate scope (matrix-015).
- **NOT a relaxation of the decomposition boundary.** All 7 records carry `decomposition_boundary: l4-reached`; the L4 Task records are downstream.
- **NOT a tightening of any blocking gate.** All gates remain advisory where they were advisory; no new blocking promotion.

## 6. Acceptance criteria

1. `tests/test_check_activity_model.py` passes all 46 tests including the live-count assertions (560 Activities / 140 BPs).
2. `scripts/check_activity_model.py` runs against the live catalog and reports `Activity Model (CR-BP-32 ACT-001..010 + CR-BP-97 ACT-011..015): CONFORMANT` with 560 Activity records.
3. `scripts/conformance_result.py` reports 28 gates, 0 blocking, 0 advisory failures.
4. CR-META gate reports 0 new findings on CR-BP-101a.
5. Em-dash / en-dash audit: 0 violations in new prose.
6. Each of the 7 Activity records carries `decomposition_boundary: l4-reached`, references the parent BP via `belongs_to_business_process: dea:process-sunset-regulated-strategic-plan`, and carries the canonical SD.Retire `ecfConformance` block.

## 7. Result

CR-BP-101a decomposes the `dea:process-sunset-regulated-strategic-plan` Business Process into 7 canonical Activity records, completing the L3 layer for the SD/Retire coordinate. The 7 activities are: Receive Regulator Sunset Directive; Identify Superseded Regulated Strategic Plan; Update Filings Register; Execute Communications Plan; Preserve Regulator-Acknowledged Sunset Record; Execute Retained-Records Plan; Notify Affected Business Units. Each Activity is grounded in established regulated-entity sunset practices (FDICIA Section 131, SRB rejection, PRA SS9/17, state PUC retraction, NHS England directive). Activity Model conformance: 553 → **560** records. ECF conformance: 743 → **750** entries. The 28-gate suite remains CONFORMANT (0 blocking, 0 advisory); `open_change_requests` 114 → 115. The SD/Retire cell is now complete at L0 / L1 / L2 / L3 (L4 remains at 0; first L4 tranche is downstream). The decomposition boundary marker `l4-reached` is preserved on every record, signalling the L4 layer as the next logical admission target.

### Counts (post-merge)

| Metric | Before (PR #142 / pre-CR-BP-101a) | After (this slice) |
|---|---|---|
| Process Contexts (L0) | 49 | 49 (unchanged) |
| Process Groups (L1) | 49 | 49 (unchanged) |
| Business Processes (L2) | 140 | 140 (unchanged) |
| Activity records (L3) | 553 | **560** (+7) |
| L4 Task records | 0 | 0 (unchanged; downstream) |
| ProcessScope records | 0 | 0 (dormant-by-design) |
| Entities (catalog index) | 742 | **749** (+7) |
| Conformance report total | 792 | **799** (+7) |
| ECF entries | 743 | **750** (+7) |
| `open_change_requests` | 114 | **115** |