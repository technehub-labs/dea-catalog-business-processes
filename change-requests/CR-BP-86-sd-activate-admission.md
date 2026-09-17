# CR-BP-86 - SD.Activate Admission Tranche (Institutionalize Regulated Strategic Plan)

**Status**: Proposed
**Layer**: L2
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-16
**Carrier**: Eighth discovery-driven admission under the CR-BP-62 escape-clause method; first canonical admission at the StrategyAndDirection x Activate coordinate. Lands the PC + PG + BP stack, the L2 admission deposition, the register cell flip, ADM-001 authority extension, and reconciliation artifacts. L3 decomposition follows as CR-BP-87.
**Depends on**: CR-BP-19 (register v2 deferral); CR-BP-62 (discovery method, BP-LIFE-001..015); CR-BP-63 (first Activate/Retire exercise); CR-BP-80 (escape-clause exercise at five backlog-deferred cells); CR-BP-71/-73/-75/-78/-81/-82/-83 (admission tranche precedents).
**Lands against**: 47 PC records, 47 PG records, 138 BP records (was 137), 537 Activity records; 24-gate suite CONFORMANT; CR-META 0 new findings; Discovery gate 23 records checked (unchanged).

---

## 1. Change Request

Land the canonical PC + PG + BP stack at the StrategyAndDirection x Activate coordinate, admitted from the CR-BP-80 escape-clause recommendation `Institutionalize Regulated Strategic Plan` (9/10 ADMIT-CANONICAL).

The BP identity:
- **id**: `dea:process-institutionalize-regulated-strategic-plan` (preserved unchanged from the CR-BP-80 discovery recommendation)
- **name**: `Institutionalize Regulated Strategic Plan` (verb + object form; satisfies BP-ARC-ID-001)
- **process_type**: `management`
- **process_intent**: `manage`
- **ECF coordinate**: `StrategyAndDirection x Activate`; identifier `ecf:strategyDirection.activate`

The trigger is a board-approved regulated strategic plan that must be filed with or activated under the supervision of a competent regulator (Basel ICAAP / SAA approval by PRA / ECB; BRRD recovery-plan activation under SRB / national-resolution-authority supervision; NHS trust 5-year strategy approval by NHS England / Department of Health; PUC integrated resource plan and strategic-plan filing before state public utility commissions; bank recovery and resolution plan activation under FDIC or SRB). The outcome is the regulated strategic plan formally activated with the supervisor's acknowledgement on record, the filing receipt preserved, the operational monitoring framework live, and the plan's obligations binding on the regulated entity under the regulator's continuing supervision.

## 2. Slice Mechanics

- **Land the stack together**: PC (`contexts/v1-alpha/dea-pc-sd-activate.yaml`), PG (`entities/v1-alpha/dea:group-regulated-strategic-plan-activation/...`), BP (`entities/v1-alpha/dea:process-institutionalize-regulated-strategic-plan/...`) in one commit. Research deposition at `entities/v1-alpha/dea:process-institutionalize-regulated-strategic-plan/research/l2-admission-deposition.yaml`.
- **Register flip** at SDAct cell: `disposition: ratified-accepted`, `audit_status: landed`, `ratified_by/at`, `landed_by/at`, `cr: CR-BP-86`, `applied_pr: TBD` (back-fill in next slice), and `admission_note` citing the CR-BP-80 discovery evidence. Carry-forward `deferral_reason` content retained per CR-BP-19 register methodology.
- **Register version**: v15 -> v16 (CR-BP-86 ratified; `ratified_accepted: 46 -> 47`; `backlog_deferred: 3 -> 2`).
- **Register the admission authority**: extend ADM-001 regex with `CR-BP-86`.
- **Locked reconciliation registers**: append new RETAIN entry to `reconciliation/dispositions/register.yaml`; insert `sd-act.86` tranche block in `reconciliation/tranches/plan.yaml` (records + `records_per_tranche: sd-act.86: 1` + `review_checkpoints: sd-act.86: 1`).
- **Discovery-side `admission` block** on the CR-BP-80 escape record's ADMIT-CANONICAL candidate: `status: admitted, admitted_by: CR-BP-86, admitted_as: dea:process-institutionalize-regulated-strategic-plan, admitted_at: '2026-09-16'`. Without this block, DISC-007 fires red on the escape record (canonical BP now exists with the same name).
- **BP context block** canonicalized to `context: [{ref: dea:pc-sd-activate}]` (BP-SEM-007 enforcement; replaces legacy scalar `process_context:`).
- **BP identity sub-block** added: `identity: {verb, object, scope, outcome_statement, evidence_links}` (BP-C1..C4 enforcement) with evidence_links as `type/ref` objects.
- **Count-assertion sweep**: 16 sites bumped across 10 test files (BP 137 -> 138; PG/PC 46 -> 47; report 769 -> 772; EXE 722 -> 724; L4 dict `{0:0, 1:0, 2:0, 3:2, 4:770}`).
- **Carrier CR + README row** at `change-requests/CR-BP-86-sd-activate-admission.md` (this file); README row inserted before the `## Cross-repo context` anchor.
- **Regen cascade** post-commit (per skill): CATALOG regenerated, open_change_requests 94 -> 95.

## 3. Gate Posture

After this slice:

- `python3 scripts/check_process_context.py`: PASS (PC-001..008)
- `python3 scripts/check_process_group.py`: PASS (PG-001..008)
- `python3 scripts/check_process_identity.py`: PASS (with suggestions; BP-ARC-ID-001..005 satisfied)
- `python3 scripts/check_process_semantics.py`: CONFORMANT (BP-SEM-001..014)
- `python3 scripts/check_lifecycle_discovery.py`: CONFORMANT, 23 records, 0 findings (DISC-001..008 all green)
- `python3 scripts/check_admission_gate.py --strict-provenance`: CONFORMANT-WITH-WARNINGS (CI-only mode; ADM-001 + ADM-008 enforced)
- `python3 scripts/check_dispositions.py`: DISP-OK (0 errors; 20 dispositions checked)
- `python3 scripts/check_cr_metadata.py`: 0 NEW findings
- `python3 scripts/conformance_result.py`: 24 gates CONFORMANT (0 blocking, 0 advisory)
- pytest 10-file core: 227/227 PASS

## 4. Repo Changes

| Path | Change |
|---|---|
| `contexts/v1-alpha/dea-pc-sd-activate.yaml` | NEW (PC at SD x Activate coordinate; PC-001..008 schema-compliant; admission block cites CR-BP-80) |
| `entities/v1-alpha/dea:group-regulated-strategic-plan-activation/dea:group-regulated-strategic-plan-activation.yaml` | NEW (PG; functional kind; scope includes Basel ICAAP / SAA, BRRD Article 5, NHS trust 5-year strategy, PUC integrated resource plan, bank recovery and resolution plan; E5 + E4 evidence) |
| `entities/v1-alpha/dea:process-institutionalize-regulated-strategic-plan/dea:process-institutionalize-regulated-strategic-plan.yaml` | NEW (BP; management type; canonical `context:` block; `identity` sub-block; 4 evidence_links; change_history) |
| `entities/v1-alpha/dea:process-institutionalize-regulated-strategic-plan/research/l2-admission-deposition.yaml` | NEW (research deposition citing CR-BP-80 discovery; admission_decision with evidence_base + bp_identity + boundary_clarity) |
| `entities/v1-alpha/dea:process-institutionalize-regulated-strategic-plan/research/README.md` | NEW (research README with L3 decomposition preview; 4 Activity candidates) |
| `discovery/v1-alpha/strategy-and-direction-activate-escape.yaml` | MOD (added `admission: {status: admitted, ...}` block on the ADMIT-CANONICAL candidate to close DISC-007) |
| `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml` | MOD (v15 -> v16; SDAct cell flipped to ratified-accepted/landed; v15_to_v16_note; counter `ratified_accepted: 46 -> 47`, `backlog_deferred: 3 -> 2`) |
| `scripts/check_admission_gate.py` | MOD (extended _ADMISSION_CR_RE regex with CR-BP-86) |
| `reconciliation/dispositions/register.yaml` | MOD (appended new RETAIN record for `dea:process-institutionalize-regulated-strategic-plan`; back-fill related_records: [CR-BP-80, CR-BP-86]) |
| `reconciliation/tranches/plan.yaml` | MOD (inserted `sd-act.86` tranche block; +1 to `records_per_tranche.sd-act.86: 1` and `review_checkpoints.sd-act.86: 1`; total_records 134 -> 135; total_tranches 73 -> 74) |
| `reconciliation/inventory.yaml` | MOD (regenerated) |
| `reconciliation/baseline/v1.yaml` | MOD (regenerated) |
| `reconciliation/conformance_report.yaml` | MOD (regenerated; 769 -> 772 records; levels {0:0, 1:0, 2:0, 3:3, 4:769}) |
| `tests/test_check_activity_model.py` | MOD (count assertions 138 -> 139) |
| `tests/test_check_execution_boundary.py` | MOD (count assertions 722 -> 724; docstring narrative) |
| `tests/test_check_intent_purposive.py` | MOD (count 138 -> 139) |
| `tests/test_check_l2_qualification.py` | MOD (count 138 -> 139) |
| `tests/test_check_lifecycle_state.py` | MOD (count 138 -> 139) |
| `tests/test_check_semantic_identity_version.py` | MOD (count 138 -> 139) |
| `tests/test_reconciliation_baseline.py` | MOD (BPs 138 -> 139; PGs 47 -> 48; PCs 47 -> 48) |
| `tests/test_architectural_regression.py` | MOD (total 769 -> 772; L4 dict updated) |
| `tests/test_cr_bp16_gates.py` | MOD (candidate_count 138 -> 139; comment enumerates CR-BP-86) |
| `change-requests/CR-BP-86-sd-activate-admission.md` | NEW (this file) |
| `change-requests/README.md` | MOD (CR-BP-86 row added before `## Cross-repo context`) |
| `CATALOG.yaml` | MOD (regenerated; `open_change_requests` 94 -> 95) |

## 5. NOT-List (Out of Scope)

- **No L3 decomposition in this slice.** Activity records land in CR-BP-87 (next slice), following the established admission -> L3 decomposition cadence.
- **No register mutation beyond the SDAct cell.** AOAct (CR-BP-81), EOAct (CR-BP-82), FAAct (CR-BP-83) each remain landed; SDAct becomes the fourth and last admitted cell of the five-cell programme; SDRet is closed without admission (CR-BP-80 escape record documented DEFER).
- **No new L0 records.** Discovery-side admission block appended on the existing escape record; no new discovery files.
- **No specialization.** ADMIT-SPECIALIZATION remains unauthorized per program governance (CR-BP-62 section 30).
- **No cross-repo work.** Stays in `dea-catalog-processes`; per-thread scope lock.

## 6. Acceptance Criteria

1. PC, PG, BP, and research deposition land together in one commit.
2. SDAct register cell flips from `backlog-deferred` to `ratified-accepted/landed` with `applied_pr: TBD` (back-fill in next slice after PR merges).
3. Register version advances v15 -> v16; counters updated.
4. ADM-001 regex extended with `CR-BP-86`; provenance check passes for the new BP.
5. Discovery-side `admission` block appended on the escape record's ADMIT-CANONICAL candidate; DISC-007 reports 0 findings.
6. Canonical `context:` block (BP-SEM-007) on the BP; legacy scalar `process_context:` removed.
7. BP `identity` sub-block added (BP-C1..C4) with object-shaped evidence_links.
8. Sixteen-site count-assertion sweep updated; 227/227 pytest PASS.
9. 24-gate conformance_result suite CONFORMANT (0 blocking, 0 advisory).
10. CATALOG.yaml regenerated; `open_change_requests` 94 -> 95.

## 7. Result

First canonical admission at the StrategyAndDirection x Activate coordinate. The 2024-2026 supervisor-acknowledged strategic-plan landscape (Basel ICAAP / SAA approval; BRRD Article 5 recovery-plan activation; NHS trust 5-year strategy approval; PUC integrated resource plan and strategic-plan filing; bank recovery and resolution plan activation) establishes that supervisor-acknowledged strategic-plan filing creates a distinct activation step with supervisor's review completion, filing receipt preservation, and operational monitoring framework launch under the regulator's continuing supervision: distinct from strategy build (Build coordinate) and from steady-state strategy execution (Operate coordinate). The cell's deferral rationale ("Activate and Retire are lifecycle transition stages, not stable Process Group operating scopes") is superseded by the universal-sector supervisor-acknowledged strategic-plan regime.

Discovery-program posture after this slice: of the 5 backlog-deferred cells identified in CR-BP-80, **AOAct, EOAct, FAAct, SDAct are now landed**; **SDRet is documented DEFER and closes the discovery loop without admission**. **All 5 backlog-deferred cells now have outcomes; L3 decomposition tranche for the 4 admitted BPs remains (CR-BP-87).**