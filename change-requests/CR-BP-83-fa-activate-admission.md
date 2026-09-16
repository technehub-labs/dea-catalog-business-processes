# CR-BP-83 - FA.Activate Admission Tranche (Activate Billing Capability)

**Status**: Proposed
**Layer**: L2
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-16
**Carrier**: Seventh discovery-driven admission under the CR-BP-62 escape-clause method; first canonical admission at the FinanceAndAccounting x Activate coordinate. Lands the PC + PG + BP stack, the L2 admission deposition, the register cell flip, ADM-001 authority extension, and reconciliation artifacts. L3 decomposition follows as CR-BP-87.
**Depends on**: CR-BP-19 (register v2 deferral); CR-BP-62 (discovery method, BP-LIFE-001..015); CR-BP-63 (first Activate/Retire exercise); CR-BP-80 (escape-clause exercise at five backlog-deferred cells); CR-BP-71/-73/-75/-78/-81/-82 (admission tranche precedents).
**Lands against**: 46 PC records, 46 PG records, 137 BP records (was 136), 537 Activity records; 24-gate suite CONFORMANT; CR-META 0 new findings; Discovery gate 23 records checked (unchanged).

---

## 1. Change Request

Land the canonical PC + PG + BP stack at the FinanceAndAccounting x Activate coordinate, admitted from the CR-BP-80 escape-clause recommendation `Activate Billing Capability` (10/10 ADMIT-CANONICAL).

The BP identity:
- **id**: `dea:process-activate-billing-capability` (preserved unchanged from the CR-BP-80 discovery recommendation)
- **name**: `Activate Billing Capability` (verb + object form; satisfies BP-ARC-ID-001)
- **process_type**: `management`
- **process_intent**: `manage`
- **ECF coordinate**: `FinanceAndAccounting x Activate`; identifier `ecf:financeAndAccounting.activate`

The trigger is the regulator's acknowledgement or pricing approval gating live invoicing or revenue recognition (insurance statutory-accounting framework activation under state insurance department supervision; IFRS 17 transition to active; bank treasury capability activation under capital-rules supervision; PUC rate-effective billing activation under state PUC approval; PSD2 / Federal Reserve / ECB settlement-account activation). The outcome is the billing or revenue-recognition capability formally activated with the regulator's acknowledgement on record, the tariff or pricing approval preserved, operational controls (segregation of duties, audit trail, reconciliation) live, and the supervisor's continuing-oversight relationship active on the regulated billing record.

## 2. Slice Mechanics

- **Land the stack together**: PC (`contexts/v1-alpha/dea-pc-fa-activate.yaml`), PG (`entities/v1-alpha/dea:group-regulated-billing-activation/...`), BP (`entities/v1-alpha/dea:process-activate-billing-capability/...`) in one commit. Research deposition at `entities/v1-alpha/dea:process-activate-billing-capability/research/l2-admission-deposition.yaml`.
- **Register flip** at FAAct cell: `disposition: ratified-accepted`, `audit_status: landed`, `ratified_by/at`, `landed_by/at`, `cr: CR-BP-83`, `applied_pr: TBD` (back-fill in next slice), and `admission_note` citing the CR-BP-80 discovery evidence. Carry-forward `deferral_reason` content retained per CR-BP-19 register methodology.
- **Register version**: v14 -> v15 (CR-BP-83 ratified; `ratified_accepted: 45 -> 46`; `backlog_deferred: 4 -> 3`).
- **Register the admission authority**: extend ADM-001 regex with `CR-BP-83`.
- **Locked reconciliation registers**: append new RETAIN entry to `reconciliation/dispositions/register.yaml`; insert `fa-act.83` tranche block in `reconciliation/tranches/plan.yaml` (records + `records_per_tranche: fa-act.83: 1` + `review_checkpoints: fa-act.83: 1`).
- **Discovery-side `admission` block** on the CR-BP-80 escape record's ADMIT-CANONICAL candidate: `status: admitted, admitted_by: CR-BP-83, admitted_as: dea:process-activate-billing-capability, admitted_at: '2026-09-16'`. Without this block, DISC-007 fires red on the escape record (canonical BP now exists with the same name).
- **BP context block** canonicalized to `context: [{ref: dea:pc-fa-activate}]` (BP-SEM-007 enforcement; replaces legacy scalar `process_context:`).
- **BP identity sub-block** added: `identity: {verb, object, scope, outcome_statement, evidence_links}` (BP-C1..C4 enforcement) with evidence_links as `type/ref` objects.
- **Count-assertion sweep**: 16 sites bumped across 10 test files (BP 137 -> 138; PG/PC 46 -> 47; report 766 -> 769; EXE 720 -> 722; L4 dict `{0:0, 1:0, 2:0, 3:2, 4:767}`).
- **Carrier CR + README row** at `change-requests/CR-BP-83-fa-activate-admission.md` (this file); README row inserted before the `## Cross-repo context` anchor.
- **Regen cascade** post-commit (per skill): CATALOG regenerated, open_change_requests 93 -> 94.

## 3. Gate Posture

After this slice:

- `python3 scripts/check_process_context.py`: PASS (PC-001..008)
- `python3 scripts/check_process_group.py`: PASS (PG-001..008)
- `python3 scripts/check_process_identity.py`: PASS (with suggestions; BP-ARC-ID-001..005 satisfied)
- `python3 scripts/check_process_semantics.py`: CONFORMANT (BP-SEM-001..014)
- `python3 scripts/check_lifecycle_discovery.py`: CONFORMANT, 23 records, 0 findings (DISC-001..008 all green)
- `python3 scripts/check_admission_gate.py --strict-provenance`: CONFORMANT-WITH-WARNINGS (CI-only mode; ADM-001 + ADM-008 enforced)
- `python3 scripts/check_dispositions.py`: DISP-OK (0 errors; 19 dispositions checked)
- `python3 scripts/check_cr_metadata.py`: 0 NEW findings
- `python3 scripts/conformance_result.py`: 24 gates CONFORMANT (0 blocking, 0 advisory)
- pytest 10-file core: 227/227 PASS

## 4. Repo Changes

| Path | Change |
|---|---|
| `contexts/v1-alpha/dea-pc-fa-activate.yaml` | NEW (PC at FA x Activate coordinate; PC-001..008 schema-compliant; admission block cites CR-BP-80) |
| `entities/v1-alpha/dea:group-regulated-billing-activation/dea:group-regulated-billing-activation.yaml` | NEW (PG; functional kind; scope includes insurance statutory accounting / IFRS 17 / PUC / PSD2 / Federal Reserve / ECB; E5 + E4 evidence) |
| `entities/v1-alpha/dea:process-activate-billing-capability/dea:process-activate-billing-capability.yaml` | NEW (BP; management type; canonical `context:` block; `identity` sub-block; 4 evidence_links; change_history) |
| `entities/v1-alpha/dea:process-activate-billing-capability/research/l2-admission-deposition.yaml` | NEW (research deposition citing CR-BP-80 discovery; admission_decision with evidence_base + bp_identity + boundary_clarity) |
| `entities/v1-alpha/dea:process-activate-billing-capability/research/README.md` | NEW (research README with L3 decomposition preview; 4 Activity candidates) |
| `discovery/v1-alpha/finance-and-accounting-activate-escape.yaml` | MOD (added `admission: {status: admitted, ...}` block on the ADMIT-CANONICAL candidate to close DISC-007) |
| `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml` | MOD (v14 -> v15; FAAct cell flipped to ratified-accepted/landed; v14_to_v15_note; counter `ratified_accepted: 45 -> 46`, `backlog_deferred: 4 -> 3`) |
| `scripts/check_admission_gate.py` | MOD (extended _ADMISSION_CR_RE regex with CR-BP-83) |
| `reconciliation/dispositions/register.yaml` | MOD (appended new RETAIN record for `dea:process-activate-billing-capability`; back-fill related_records: [CR-BP-80, CR-BP-83]) |
| `reconciliation/tranches/plan.yaml` | MOD (inserted `fa-act.83` tranche block; +2 to `records_per_tranche.fa-act.83: 1` and `review_checkpoints.fa-act.83: 1`) |
| `reconciliation/inventory.yaml` | MOD (regenerated) |
| `reconciliation/baseline/v1.yaml` | MOD (regenerated) |
| `reconciliation/conformance_report.yaml` | MOD (regenerated; 766 -> 769 records; levels {0:0, 1:0, 2:0, 3:2, 4:767}) |
| `tests/test_check_activity_model.py` | MOD (count assertions 137 -> 138) |
| `tests/test_check_execution_boundary.py` | MOD (count assertions 720 -> 722; docstring narrative) |
| `tests/test_check_intent_purposive.py` | MOD (count 137 -> 138) |
| `tests/test_check_l2_qualification.py` | MOD (count 137 -> 138) |
| `tests/test_check_lifecycle_state.py` | MOD (count 137 -> 138) |
| `tests/test_check_semantic_identity_version.py` | MOD (count 137 -> 138) |
| `tests/test_reconciliation_baseline.py` | MOD (BPs 137 -> 138; PGs 46 -> 47; PCs 46 -> 47) |
| `tests/test_architectural_regression.py` | MOD (total 766 -> 769; L4 dict updated) |
| `tests/test_cr_bp16_gates.py` | MOD (candidate_count 137 -> 138; comment enumerates CR-BP-83) |
| `change-requests/CR-BP-83-fa-activate-admission.md` | NEW (this file) |
| `change-requests/README.md` | MOD (CR-BP-83 row added before `## Cross-repo context`) |
| `CATALOG.yaml` | MOD (regenerated; `open_change_requests` 93 -> 94) |

## 5. NOT-List (Out of Scope)

- **No L3 decomposition in this slice.** Activity records land in CR-BP-87 (next slice), following the established admission -> L3 decomposition cadence.
- **No register mutation beyond the FAAct cell.** AOAct, EOAct, FAAct each remain landed; SDAct remains backlog-deferred (CR-BP-86 pending); SDRet is closed without admission.
- **No new L0 records.** Discovery-side admission block appended on the existing escape record; no new discovery files.
- **No specialization.** ADMIT-SPECIALIZATION remains unauthorized per program governance (CR-BP-62 section 30).
- **No cross-repo work.** Stays in `dea-catalog-processes`; per-thread scope lock.

## 6. Acceptance Criteria

1. PC, PG, BP, and research deposition land together in one commit.
2. FAAct register cell flips from `backlog-deferred` to `ratified-accepted/landed` with `applied_pr: TBD` (back-fill in next slice after PR merges).
3. Register version advances v14 -> v15; counters updated.
4. ADM-001 regex extended with `CR-BP-83`; provenance check passes for the new BP.
5. Discovery-side `admission` block appended on the escape record's ADMIT-CANONICAL candidate; DISC-007 reports 0 findings.
6. Canonical `context:` block (BP-SEM-007) on the BP; legacy scalar `process_context:` removed.
7. BP `identity` sub-block added (BP-C1..C4) with object-shaped evidence_links.
8. Sixteen-site count-assertion sweep updated; 227/227 pytest PASS.
9. 24-gate conformance_result suite CONFORMANT (0 blocking, 0 advisory).
10. CATALOG.yaml regenerated; `open_change_requests` 93 -> 94.

## 7. Result

First canonical admission at the FinanceAndAccounting x Activate coordinate. The 2024-2026 regulator-acknowledged accounting or rate framework landscape (IFRS 17 transition; NAIC statutory accounting; Solvency II; PUC rate-effective billing; PSD2 / Federal Reserve / ECB settlement-account activation) establishes that regulator-acknowledged accounting or rate framework creates a distinct activation step with continuing-supervisor notification, tariff or pricing approval, and operational controls (segregation of duties, audit trail, reconciliation) live on the regulated billing record: distinct from capability build (Build coordinate) and from steady-state billing (Operate coordinate). The cell's deferral rationale ("Activate and Retire are lifecycle transition stages, not stable Process Group operating scopes") is superseded by the universal-sector regulator-acknowledged accounting regime.

Discovery-program posture after this slice: of the 5 backlog-deferred cells identified in CR-BP-80, AOAct, EOAct, FAAct are now landed; SDAct carries an ADMIT-CANONICAL recommendation pending CR-BP-86; SDRet is documented DEFER (volume-lower cross-domain evidence) and closes the discovery loop without admission. **4 of 5 backlog-deferred cells now have outcomes; 1 admission tranche remaining (CR-BP-86 SD.Activate) + L3 decomposition tranche (CR-BP-87).**