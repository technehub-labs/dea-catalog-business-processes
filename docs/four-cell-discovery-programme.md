# Four-Cell Discovery Programme

**Status**: Active (closed; documented 2026-09-17)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-17 (post-CR-BP-87)
**Carrier CR**: CR-BP-89 (this file's authoring CR)

---

## 1. Context

The Process Catalog's ECF matrix (7 domains x 7 stages = 49 coordinates) has been progressively populated since 2026-09-05. The Phase 1 (CR-BP-11..-13) discovery ratified 38 coordinates; the Phase 2 (CR-BP-14..-28) reconciliation cascade brought the catalog to register v4 with 35 / 0 / 14 split (35 ratified-accepted / 0 ratified-with-caveats / 14 backlog-deferred). All 14 backlog-deferred coordinates were Activate or Retire stages — the lifecycle transition stages that were documented DEFER because their operating scope was "different from stable process group operating scopes" (per CR-BP-11 §3.4).

By 2026-09-14 (register v9), the catalog had:

- 137 canonical Business Processes
- 47 canonical Process Groups
- 47 canonical Process Contexts
- 537 canonical Activities (after the L3 EO/PR/GE/PV/FA/S&D/A&O domain tranches)
- 14 backlog-deferred cells (all Activate/Retire)
- 18 Discovery records

The four-cell discovery programme opened on 2026-09-14 to close the Activate/Retire backlog through a documented lifecycle-stage method.

## 2. Method

### 2.1 BP-LIFE-001..015 lifecycle criteria

The 15 lifecycle criteria codify what it means for a process to live at the Activate or Retire stage. They are:

**BP-LIFE-001..005 (trigger criteria)**: a lifecycle-stage process must trigger when a regulated entity's scope-of-authorization boundary changes (BP-LIFE-001 - supervisory boundary), when the entity's capability is materially altered (BP-LIFE-002 - capability shift), when a regulator-issued authorization is required (BP-LIFE-003 - authorization gate), when the entity enters a wind-down state (BP-LIFE-004 - wind-down trigger), or when external change mandates closure (BP-LIFE-005 - external mandate).

**BP-LIFE-006..010 (gate criteria)**: a lifecycle-stage process must gate on regulator acknowledgement (BP-LIFE-006), supervisory notification (BP-LIFE-007), capability demonstration (BP-LIFE-008), wind-down quorum (BP-LIFE-009), or closure filing (BP-LIFE-010).

**BP-LIFE-011..015 (outcome criteria)**: a lifecycle-stage process must terminate in either (b) a regulated entity's ongoing authorization under continuing supervision (BP-LIFE-011 / -012), (b) a fully wound-down entity with retained records under regulatory access (BP-LIFE-013 / -014), or (b) a closure-of-record with no further obligation (BP-LIFE-015).

### 2.2 Escape-clause discovery method

For each backlog-deferred coordinate, an escape record is constructed at `discovery/v1-alpha/<domain>-<stage>-escape.yaml`. The escape record tests one regulated-sector candidate against BP-LIFE-001..015. Disposition is scored on a 0..10 scale:

- **10/10 ADMIT-CANONICAL** - all 15 lifecycle criteria met; canonical PC + PG + BP stack emerges.
- **9/10 ADMIT-CANONICAL** - all 15 criteria met with one minor caveat (e.g. one criterion met by a minor stakeholder's industry framework rather than the candidate's primary framework).
- **6..8/10 DEFER-WITH-LINK** - 6-8 criteria met; cross-link to a downstream admission recommended.
- **<6/10 DEFER** - <6 criteria met; out of scope for the canonical Activate/Retire stack at this stage.

### 2.3 Disc-gate suite (DISC-001..008)

The disc-gate suite enforces:

- DISC-001 (escape-record structure)
- DISC-002 (BP-LIFE-001..015 compliance)
- DISC-003 (disposition vocabulary)
- DISC-004 (evidence citation form)
- DISC-005 (cross-link integrity)
- DISC-006 (register sync)
- DISC-007 (admission block structure)
- DISC-008 (defer-with-link rationale form)

Wired into `conformance_result.py` as gate [19].

## 3. Lineage (25 CRs)

### Phase 1 - Method codification (CR-BP-62)

- CR-BP-62: lifecycle process discovery method + DISC-001..008 gate (PR #103; 2026-09-14)

### Phase 2 - First Activate/Retire exercise (CR-BP-63)

- CR-BP-63: Activate/Retire lifecycle discovery exercise (PR #104; 2026-09-14)

### Phase 3 - First admission tranche wave (CR-BP-64..67)

- CR-BP-64: P&V Activate + Retire admission tranche (PR #105; 2026-09-14)
- CR-BP-65: G&E Activate admission tranche - Bring into Force (PR #106; 2026-09-14)
- CR-BP-66: E&O Retire admission tranche - Decommission (PR #107; 2026-09-14)
- CR-BP-67: P&R Retire admission tranche - Close Enterprise Relationship (PR #108; 2026-09-14)

### Phase 4 - First admitted-BP L3 tranche (CR-BP-69)

- CR-BP-69: admitted-BP L3 decomposition tranche (PR #110; 2026-09-15) - 5 BPs -> 20 Activities

### Phase 5 - Second admission tranche wave (CR-BP-70..79)

- CR-BP-70: P&R Activate escape-clause discovery (KYC) (PR #111; 2026-09-15)
- CR-BP-71: P&R Activate admission tranche - Onboard Regulated Party Relationship (PR #112; 2026-09-15)
- CR-BP-72: A&O Retire escape-clause discovery - mass-layoff regulated wind-down (PR #113; 2026-09-15)
- CR-BP-73: A&O Retire admission tranche - Conduct Regulated Workforce Wind-Down (PR #114; 2026-09-15)
- CR-BP-74: F&A Retire escape-clause discovery - Regulated Run-Off (PR #115; 2026-09-15)
- CR-BP-75: F&A Retire admission tranche - Conclude Regulated Run-Off (PR #116; 2026-09-15)
- CR-BP-77: L3 Activity Admitted-Regulated-BP Tranche (PR #117; 2026-09-16) - 3 BPs -> 12 Activities
- CR-BP-76: G&E Retire escape-clause discovery - regulator-mandated governance unwind (PR #118; 2026-09-16)
- CR-BP-78: G&E Retire admission tranche - Effect Regulator-Mandated Governance Unwind (PR #119; 2026-09-16)
- CR-BP-79: L3 Activity G&E-Retire admission tranche (PR #120; 2026-09-16) - 1 BP -> 4 Activities

### Phase 6 - Five-cell escape-clause discovery exercise (CR-BP-80)

- CR-BP-80: L0 escape-clause discovery for the five backlog-deferred cells (PR #121; 2026-09-16)

### Phase 7 - Four-cell discovery programme admissions (CR-BP-81..86)

- CR-BP-81: AO.Activate admission tranche - Mobilize Licensed Workforce (PR #122; 2026-09-16)
- CR-BP-82: EO.Activate admission tranche - Activate Operations Capability (PR #123; 2026-09-16)
- CR-BP-83: FA.Activate admission tranche - Activate Billing Capability (PR #124; 2026-09-16)
- CR-BP-86: SD.Activate admission tranche - Institutionalize Regulated Strategic Plan (PR #125; 2026-09-17)

### Phase 8 - Combined L3 decomposition tranche (CR-BP-87)

- CR-BP-87: L3 Activity Admitted-Activate-BP Decomposition Tranche (PR #126; 2026-09-17) - 4 BPs -> 16 Activities

### Phase 9 - Post-programme documentation (CR-BP-88..89)

- CR-BP-88: Post-v0.3.0 Reconciliation (54 PRs [Unreleased] + status rows) (PR #127; 2026-09-17)
- CR-BP-89: this slice (forthcoming)

## 4. Cell-by-cell dispositions

Per `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml`:

| # | Cell | First captured at | Disposition | Final status |
|---|---|---|---|---|
| 1 | P&V.Activate | CR-BP-63 | 10/10 ADMIT-CANONICAL | LANDED CR-BP-64 (Bring into Force) |
| 2 | P&V.Retire | CR-BP-63 | 10/10 ADMIT-CANONICAL | LANDED CR-BP-64 (Decommission) |
| 3 | G&E.Activate | CR-BP-63 | 10/10 ADMIT-CANONICAL | LANDED CR-BP-65 (Bring into Force) |
| 4 | E&O.Retire | CR-BP-63 | 10/10 ADMIT-CANONICAL | LANDED CR-BP-66 (Decommission) |
| 5 | P&R.Retire | CR-BP-63 | 10/10 ADMIT-CANONICAL | LANDED CR-BP-67 (Close Enterprise Relationship) |
| 6 | P&R.Activate | CR-BP-70 | 10/10 ADMIT-CANONICAL | LANDED CR-BP-71 (Onboard Regulated Party Relationship) |
| 7 | A&O.Retire | CR-BP-72 | 10/10 ADMIT-CANONICAL | LANDED CR-BP-73 (Conduct Regulated Workforce Wind-Down) |
| 8 | F&A.Retire | CR-BP-74 | 10/10 ADMIT-CANONICAL | LANDED CR-BP-75 (Conclude Regulated Run-Off) |
| 9 | G&E.Retire | CR-BP-76 | 10/10 ADMIT-CANONICAL | LANDED CR-BP-78 (Effect Regulator-Mandated Governance Unwind) |
| 10 | AO.Activate | CR-BP-80 | 10/10 ADMIT-CANONICAL | LANDED CR-BP-81 (Mobilize Licensed Workforce) |
| 11 | EO.Activate | CR-BP-80 | 10/10 ADMIT-CANONICAL | LANDED CR-BP-82 (Activate Operations Capability) |
| 12 | FA.Activate | CR-BP-80 | 10/10 ADMIT-CANONICAL | LANDED CR-BP-83 (Activate Billing Capability) |
| 13 | SD.Activate | CR-BP-80 | 9/10 ADMIT-CANONICAL | LANDED CR-BP-86 (Institutionalize Regulated Strategic Plan) |
| 14 | SD.Retire | CR-BP-80 | 6/10 DEFER | DEFER without admission |

13 of 14 backlog-deferred cells ADMIT-CANONICAL; 1 DEFER. All 13 admitted cells have canonical PC + PG + BP stacks with `identity` sub-blocks (BP-C1..C4) carrying object-shaped `evidence_links`.

## 5. L3 decomposition

The 13 admitted BPs have been decomposed to 4 Activity records each (52 total) across three admitted-BP L3 tranches:

- CR-BP-69 (5 BPs from wave 1: 20 Activity records)
- CR-BP-77 (3 BPs from wave 2: 12 Activity records)
- CR-BP-79 (1 BP from wave 2: 4 Activity records)
- CR-BP-87 (4 BPs from four-cell programme: 16 Activity records)

The four-cell programme's L3 tranche (CR-BP-87) was Option A: combined PR. Each BP gains `metadata.activity_references[]` (4 ids) + CR-BP-87 change_history entry. Versions unchanged per SIV-004.

## 6. Discovery-programme closure

The SD.Retire cell (`dea:process-sunset-regulated-strategic-plan`) is documented DEFER (6/10) at CR-BP-80. The rationale: volume-lower cross-domain concern. The regulated entity's strategic plan sunset is governed by FDICIA Section 131 / SRB / PRA SS9/17 / PUC retraction processes; the operating scope is "below" the cross-domain PF-level concern, not at the canonical SD.Retire coordinate. The cell is closed without admission (status: backlog-deferred).

The four-cell programme's closure: all 5 backlog-deferred cells from CR-BP-80 are closed (4 ADMIT-CANONICAL + 1 DEFER).

## 7. What this programme is NOT

- **NOT a release cut.** No tag push, no `gh release create`, no version bump.
- **NOT a v0.2.0 cut completion.** The stranded `## [v0.2.0]` block remains in place per user directive.
- **NOT a record, schema, validator-rule, or conformance-gate change.**
- **NOT a discovery exercise.** All 23 escape records were landed by CR-BP-63 / CR-BP-70-78 individual / CR-BP-80.
- **NOT an admission or reclassification of any Business Process.** The 13 admitted BPs were admitted by the relevant admission tranches.
- **NOT an L3 decomposition.** The 52 Activity records were landed by CR-BP-69 / CR-BP-77 / CR-BP-79 / CR-BP-87.
- **NOT an authorisation of specialization.** Governance directive: decomposition only until L0-L4 stabilizes universally.

## 8. References

### Internal

- CR-BP-62 (lifecycle process discovery method + DISC-001..008 gate)
- CR-BP-63 / CR-BP-70 / CR-BP-72 / CR-BP-74 / CR-BP-76 / CR-BP-80 (5 discovery exercises)
- CR-BP-64..67 / CR-BP-71 / CR-BP-73 / CR-BP-75 / CR-BP-78 / CR-BP-81..83 / CR-BP-86 (13 admission tranches)
- CR-BP-69 / CR-BP-77 / CR-BP-79 / CR-BP-87 (4 admitted-BP L3 tranches)
- CR-BP-88 (post-v0.3.0 reconciliation)
- CR-BP-89 (this slice's authoring CR)
- CR-BP-35 (process catalog architecture retrospective)
- CR-BP-38 (ECF matrix population retrospective)
- CR-BP-19 (L1 register re-derivation against ECF v2.4.0; 35/14 baseline)

### Cross-repo

- CR-MM-ECF-01 (lifecycle process metamodel)
- CR-ECF-CG-001..004 (ECF conformance gate)
- CR-AR-FMWK-01 (architecture framework)

### Registry state

- `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml` (v21)
- `reconciliation/dispositions/register.yaml` (139 dispositions)
- `reconciliation/tranches/plan.yaml` (74 tranches)
- `reconciliation/conformance_report.yaml` (788 records; L4 = 785)

### Discovery exercise outputs

- 23 escape records at `discovery/v1-alpha/<domain>-<stage>-escape.yaml`
- 13 ADMIT-CANONICAL; 9 DEFER-WITH-LINK; 1 DEFER

---

## Appendix A - Activity naming collision

In CR-BP-87's combined L3 decomposition tranche, two Activities share the conceptual name "Activate Continuing-Supervisor Notification" (EO + FA). To preserve Activity-id uniqueness across the catalog, the FA Activity carries the qualifier `(Billing)` in its display name and the slug `dea:activity-activate-continuing-supervisor-notification-fa`. The EO Activity retains the bare name. Both share canonical semantics but resolve to distinct entities.

## Appendix B - Discovery exercise lineage (23 records)

| # | CR | Cell | Disposition | Admission CR |
|---|---|---|---|---|
| 1 | CR-BP-63 | P&V.Activate | 10/10 ADMIT-CANONICAL | CR-BP-64 |
| 2 | CR-BP-63 | P&V.Retire | 10/10 ADMIT-CANONICAL | CR-BP-64 |
| 3 | CR-BP-63 | G&E.Activate | 10/10 ADMIT-CANONICAL | CR-BP-65 |
| 4 | CR-BP-63 | E&O.Retire | 10/10 ADMIT-CANONICAL | CR-BP-66 |
| 5 | CR-BP-63 | P&R.Retire | 10/10 ADMIT-CANONICAL | CR-BP-67 |
| 6 | CR-BP-63 | S&D.Activate | 7/10 DEFER-WITH-LINK | (not admitted) |
| 7 | CR-BP-63 | S&D.Retire | 7/10 DEFER-WITH-LINK | (not admitted) |
| 8 | CR-BP-70 | P&R.Activate | 10/10 ADMIT-CANONICAL | CR-BP-71 |
| 9 | CR-BP-72 | A&O.Retire | 10/10 ADMIT-CANONICAL | CR-BP-73 |
| 10 | CR-BP-74 | F&A.Retire | 10/10 ADMIT-CANONICAL | CR-BP-75 |
| 11 | CR-BP-76 | G&E.Retire | 10/10 ADMIT-CANONICAL | CR-BP-78 |
| 12 | CR-BP-80 | AO.Activate | 10/10 ADMIT-CANONICAL | CR-BP-81 |
| 13 | CR-BP-80 | EO.Activate | 10/10 ADMIT-CANONICAL | CR-BP-82 |
| 14 | CR-BP-80 | FA.Activate | 10/10 ADMIT-CANONICAL | CR-BP-83 |
| 15 | CR-BP-80 | SD.Activate | 9/10 ADMIT-CANONICAL | CR-BP-86 |
| 16 | CR-BP-80 | SD.Retire | 6/10 DEFER | (not admitted) |
| 17-23 | CR-BP-63 / CR-BP-70 / CR-BP-72 / CR-BP-74 / CR-BP-76 / CR-BP-80 | Auxiliary cells (cross-link DEFER-WITH-LINK) | various | (not admitted) |