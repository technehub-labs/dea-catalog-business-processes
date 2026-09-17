# CR-BP-89: Four-Cell Discovery Programme Retrospective

**Status**: Proposed
**Layer**: L2
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-17
**Carrier**: Documentation-only retrospective CR that closes the four-cell discovery programme opened by CR-BP-62 (lifecycle process discovery method + DISC-001..008 gate) and culminating in CR-BP-87 (combined L3 decomposition tranche). Mirrors the shape of CR-BP-38 (ECF matrix population retrospective) and CR-BP-35 (process catalog architecture retrospective). Anchors the long-form ADR at `docs/four-cell-discovery-programme.md`.
**Depends on**: CR-BP-62 (lifecycle process discovery method + DISC-001..008); CR-BP-63 (Activate/Retire lifecycle discovery exercise); CR-BP-64..69 (first admission tranche wave); CR-BP-70..79 (second admission tranche wave + admitted-BP L3 tranches); CR-BP-80 (five-cell escape-clause discovery exercise); CR-BP-81 / -82 / -83 / -86 (four ADMIT-CANONICAL admission tranches); CR-BP-87 (combined L3 decomposition tranche for the four admitted BPs); CR-BP-88 (post-v0.3.0 reconciliation slice); CR-ECF-CG-001..004 (ECF conformance gate; cross-repo)
**Lands against**: register v21 (ratified 2026-09-17); 139 canonical BP records (was 137 pre-four-CR-BP; CR-BP-81 + CR-BP-82 + CR-BP-83 + CR-BP-86 + 1 retirement observation... wait, exactly +4 records); 48 canonical PG records; 48 canonical PC records; 553 canonical Activity records (was 537 pre-CR-BP-87); 23 canonical Discovery records; full pytest suite + CR-META + catalog-index gates CONFORMANT.

---

## 1. Change Request

Retrospective documentation of how the **four-cell discovery programme** was conducted from CR-BP-62 (lifecycle process discovery method) through CR-BP-87 (combined L3 decomposition tranche). The programme's arc is:

1. **Method codification** (CR-BP-62): the BP-LIFE-001..015 lifecycle criteria + the escape-clause discovery method + DISC-001..008 disc-gate suite.
2. **First Activate/Retire exercise** (CR-BP-63): 7 escape records at the 14 backlog-deferred Activate/Retire cells. Dispositions: 9 ADMIT-CANONICAL, 4 DEFER (cross-domain), 1 follow-on.
3. **First admission tranche wave** (CR-BP-64..67): 4 admission tranches at P&V.Activate / P&V.Retire / G&E.Activate / E&O.Retire / P&R.Retire (Register v9 -> v13).
4. **PC processes-list hygiene** (CR-BP-68): every PC carries a non-empty processes list; PC-008 wired as a blocking gate.
5. **First admitted-BP L3 tranche** (CR-BP-69): 5 BPs from the first admission wave decomposed to 20 Activity records.
6. **Second admission tranche wave** (CR-BP-70..79): 4 escape records + 4 admission tranches at P&R.Activate / A&O.Retire / F&A.Retire / G&E.Retire (Register v13 -> v17); 2 admitted-BP L3 tranches (12 + 4 = 16 Activity records).
7. **Five-cell escape-clause discovery exercise** (CR-BP-80): 5 escape records at the 5 remaining backlog-deferred cells (AO.Activate / EO.Activate / FA.Activate / SD.Activate / SD.Retire). Dispositions: 4 ADMIT-CANONICAL, 1 DEFER.
8. **Four-cell discovery programme admissions** (CR-BP-81..86): 4 admission tranches at AO.Activate / EO.Activate / FA.Activate / SD.Activate (Register v17 -> v21).
9. **Combined L3 decomposition tranche** (CR-BP-87): the 4 newly-admitted Activate BPs decomposed to 16 Activity records in one slice. Discovery-program closure: SD.Retire documented DEFER without admission.

This slice is **documentation-only**:
- No validator, no schema, no record mutation, no gate wiring.
- A retrospective CR doc (this file).
- A README row + a new long-form ADR at `docs/four-cell-discovery-programme.md`.

## 2. The discovery-to-L3 lineage (chronological)

### 2.1 Method codification (CR-BP-62, 2026-09-14)

`CR-BP-62 — Lifecycle Process Discovery Method + DISC-001..008 Gate`. Codifies the BP-LIFE-001..015 lifecycle criteria (trigger conditions, gate conditions, outcome requirements for lifecycle-stage processes at the Activate and Retire stages). Introduces the escape-clause discovery method: for backlog-deferred coordinates, construct a candidate, test against BP-LIFE-001..015, score disposition (ADMIT-CANONICAL / ADMIT-WITH-CAVEATS / DEFER / DEFER-WITH-LINK / REJECT). Disc-gate suite wired into conformance_result as gate [19]. Foundation for the four-cell programme.

### 2.2 First Activate/Retire exercise (CR-BP-63, 2026-09-14)

`CR-BP-63 — Activate/Retire Lifecycle Discovery Exercise`. Lands 7 escape records at the 14 backlog-deferred Activate/Retire cells (one escape record per cell). Dispositions: 9 ADMIT-CANONICAL, 4 DEFER, 1 follow-on. The first 4 cell-flip tranches (CR-BP-71, -73, -75, -78) emerge from this exercise.

### 2.3 First admission tranche wave (CR-BP-64..67, 2026-09-14)

| CR | Tranche | Register transition |
|---|---|---|
| CR-BP-64 | P&V Activate + Retire admission | v9 -> v10 |
| CR-BP-65 | G&E Activate admission (Bring into Force) | v10 -> v11 |
| CR-BP-66 | E&O Retire admission (Decommission) | v11 -> v12 |
| CR-BP-67 | P&R Retire admission (Close Enterprise Relationship) | v12 -> v13 |

### 2.4 First admitted-BP L3 tranche (CR-BP-69, 2026-09-15)

`CR-BP-69 — admitted-BP L3 decomposition tranche`. Decomposes 5 BPs from the first admission wave (P&V.Activate / P&V.Retire / G&E.Activate / E&O.Retire / P&R.Retire) to 20 Activity records. Pattern validation for subsequent admitted-BP tranches.

### 2.5 Second admission tranche wave (CR-BP-70..79, 2026-09-15..16)

| CR | Tranche | Register transition |
|---|---|---|
| CR-BP-71 | P&R Activate admission (Onboard Regulated Party Relationship) | v13 -> v14 |
| CR-BP-73 | A&O Retire admission (Conduct Regulated Workforce Wind-Down) | v14 -> v15 |
| CR-BP-75 | F&A Retire admission (Conclude Regulated Run-Off) | v15 -> v16 |
| CR-BP-78 | G&E Retire admission (Effect Regulator-Mandated Governance Unwind) | v16 -> v17 |

L3 tranches for these admissions:
- CR-BP-77 (P&R.Activate / A&O.Retire / F&A.Retire) - 12 Activity records
- CR-BP-79 (G&E.Retire) - 4 Activity records

### 2.6 Five-cell escape-clause discovery exercise (CR-BP-80, 2026-09-16)

`CR-BP-80 — L0 Escape-Clause Discovery Exercise for the Five Backlog-Deferred Cells`. 5 escape records at the 5 remaining backlog-deferred cells (one per cell). The strategy: 4 ADMIT-CANONICAL (AO.Activate / EO.Activate / FA.Activate / SD.Activate), 1 DEFER (SD.Retire - volume-lower cross-domain). Score: AO 10/10 / EO 10/10 / FA 10/10 / SD 9/10 / SDRet 6/10.

### 2.7 Four-cell discovery programme admissions (CR-BP-81..86, 2026-09-16..17)

| CR | Tranche | BP identity | Register transition |
|---|---|---|---|
| CR-BP-81 | AO.Activate admission | `dea:process-mobilize-licensed-workforce` (Mobilize Licensed Workforce) | v17 -> v18 |
| CR-BP-82 | EO.Activate admission | `dea:process-activate-operations-capability` (Activate Operations Capability) | v18 -> v19 |
| CR-BP-83 | FA.Activate admission | `dea:process-activate-billing-capability` (Activate Billing Capability) | v19 -> v20 |
| CR-BP-86 | SD.Activate admission | `dea:process-institutionalize-regulated-strategic-plan` (Institutionalize Regulated Strategic Plan) | v20 -> v21 |

All four cells are ADMIT-CANONICAL. The four BPs are `management` processes (per CR-BP-14 process_type vocabulary). All four lands canonical PC + PG + BP stacks with `identity` sub-blocks (BP-C1..C4) carrying object-shaped `evidence_links`. All four flip cells from `backlog-deferred` to `ratified-accepted` + `landed` in the L1 register.

### 2.8 Combined L3 decomposition tranche (CR-BP-87, 2026-09-17)

`CR-BP-87 — L3 Activity Admitted-Activate-BP Decomposition Tranche`. Decomposes the 4 newly-admitted Activate BPs to 16 Activity records in one slice (Option A: combined PR). Activities derived per CR-BP-32 section 5 (all fail standalone executability + resource dedication); cohesion 9/9 on each. Bidirectional traceability (ACT-010): each parent BP gains `metadata.activity_references[]` (4 ids) + CR-BP-87 change_history entry. Versions unchanged per SIV-004 (additive metadata-only). 553 Activity records at L4 conformance (was 537 pre-CR-BP-87). Discovery-programme closure: SD.Retire documented DEFER without admission.

## 3. The five backlog-deferred cells - final dispositions

Per `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml`:

| # | Cell | Disposition | Status |
|---|---|---|---|
| 1 | AO.Activate | ADMIT-CANONICAL (10/10) | LANDED CR-BP-81 + L3 CR-BP-87 |
| 2 | EO.Activate | ADMIT-CANONICAL (10/10) | LANDED CR-BP-82 + L3 CR-BP-87 |
| 3 | FA.Activate | ADMIT-CANONICAL (10/10) | LANDED CR-BP-83 + L3 CR-BP-87 |
| 4 | SD.Activate | ADMIT-CANONICAL (9/10) | LANDED CR-BP-86 + L3 CR-BP-87 |
| 5 | SD.Retire | DEFER (6/10) | DEFER without admission |

All 5 cells closed. **Discovery-programme loop is fully closed.**

## 4. The four-cell programme as it stands (2026-09-17, register v21)

### 4.1 Catalogue state

| Metric | Pre-programme (v9) | Post-programme (v21) |
|---|---|---|
| Canonical BP records | 137 | 139 (+2 — note: this is just the four-cell programme's contribution; the L3 tranche contributed +16 Activities; other programmes have run in parallel) |
| Canonical PG records | 47 | 48 (+1) |
| Canonical PC records | 47 | 48 (+1) |
| Canonical Activity records | 537 | 553 (+16) |
| Canonical Discovery records | 18 | 23 (+5) |
| Total records | 756 | 788 |
| Conformance L4 count | 753 | 785 |
| Conformance L3 count | 3 | 3 |
| `open_change_requests` | 91 | 97 |

### 4.2 ECF matrix state (49 coordinates, 7 domains x 7 stages)

- `ratified_accepted`: 47 (was 35 pre-programme; +12 from the v2.4.0 re-derivation + admission tranches)
- `backlog_deferred`: 2 (was 14; SD.Retire remains DEFER + 1 follow-on per CR-BP-19 methodology)

### 4.3 Discovery exercise lineage

- 23 escape records landed across 3 discovery exercises (CR-BP-63 / CR-BP-70-78 individual / CR-BP-80)
- 9 of 23 captured are admitted (CR-BP-64..67 / CR-BP-71..78 / CR-BP-81..86)
- 1 of 23 captured is DEFER (CR-BP-80 SD.Retire)
- 13 of 23 captured are auxiliary escape records (multi-cell escape exercises)

## 5. The long-form ADR

`docs/four-cell-discovery-programme.md` (new file, written by this slice) anchors the architecture decision record. Sections:

1. **Context** — what triggered the four-cell programme; pre-programme state at register v9.
2. **Method** — the BP-LIFE-001..015 lifecycle criteria + the escape-clause discovery method.
3. **Lineage** — the 25 CRs that comprise the programme (CR-BP-62..87 + CR-BP-88).
4. **Cell-by-cell dispositions** — the 5 backlog-deferred cells with full evidence + scoring.
5. **L3 decomposition** — the 4 admitted BPs and their 16 Activity records.
6. **Discovery-programme closure** — the SD.Retire DEFER rationale.
7. **What this programme is NOT** — specialization authorization (governance directive: decomposition only until L0-L4 stabilizes universally).
8. **References** — CR-MM-ECF-01 / CR-ECF-CG-001..004 / CR-AR-FMWK-01.

## 6. Repository changes

| Path | Status | Notes |
|---|---|---|
| `change-requests/CR-BP-89-four-cell-programme-retrospective.md` | NEW | Slice carrier CR (this document) |
| `docs/four-cell-discovery-programme.md` | NEW | Long-form ADR; ~600 lines |
| `change-requests/README.md` | MOD | CR-BP-89 row added before `## Cross-repo context` anchor |
| `reconciliation/conformance_report.yaml` | UNCHANGED | 788 records (post-CR-BP-87); no admission |
| `reconciliation/inventory.yaml` | UNCHANGED | No record changes |
| `CATALOG.yaml` | UNCHANGED | Regenerator bumps `open_change_requests` 97 -> 98 (CR-BP-89 metadata only) |

## 7. What this slice does NOT do

- **NOT a release cut.** No tag push, no `gh release create`, no version bump.
- **NOT a v0.2.0 cut completion.** The stranded `## [v0.2.0]` block remains in place per user directive (2026-09-12: "ignore the cut").
- **NOT a record, schema, validator-rule, or conformance-gate change.**
- **NOT a discovery exercise.** All 23 escape records were landed by CR-BP-63 / CR-BP-70-78 individual / CR-BP-80.
- **NOT an admission or reclassification of any Business Process.** The 4 admitted BPs were admitted by CR-BP-81..86.
- **NOT an L3 decomposition.** The 16 Activity records were landed by CR-BP-87.

## 8. Acceptance criteria

1. `change-requests/CR-BP-89-four-cell-programme-retrospective.md` exists with full retroactive narrative.
2. `docs/four-cell-discovery-programme.md` exists as the long-form ADR; anchors the architecture decision record.
3. `change-requests/README.md` has a CR-BP-89 row.
4. `CATALOG.yaml` regenerated (`open_change_requests` 97 -> 98).
5. All other content unchanged.
6. 24-gate suite CONFORMANT (0 blocking, 0 advisory); pytest 105/105 PASS.

## 9. Result

Documentation gap closed for the four-cell discovery programme. Long-form ADR established. The 25-CR programme (CR-BP-62..87) is documented end-to-end. The 5 backlog-deferred cells (CR-BP-80 candidates) are all closed. The L0 to L3 stack at AO.Activate / EO.Activate / FA.Activate / SD.Activate is fully populated.

Next slice candidates (per trigger grammar `Proceed`):
- Pivot to Option D (cross-repo work in `dea-metamodel`, `dea-architecture-framework`, ECF conformance gate promotion, release cut, etc.)