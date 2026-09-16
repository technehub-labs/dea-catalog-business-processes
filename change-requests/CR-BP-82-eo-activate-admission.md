# CR-BP-82 - EO.Activate Admission Tranche (Activate Operations Capability)

**Status**: Proposed
**Layer**: L2
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-16
**Carrier**: Sixth discovery-driven admission under the CR-BP-62 escape-clause method; first canonical admission at the EnablementAndOperations x Activate coordinate. Lands the PC + PG + BP stack, the L2 admission deposition, the register cell flip, ADM-001 authority extension, and reconciliation artifacts. L3 decomposition follows as CR-BP-87.
**Depends on**: CR-BP-19 (register v2 deferral); CR-BP-62 (discovery method, BP-LIFE-001..015); CR-BP-63 (first Activate/Retire exercise); CR-BP-80 (escape-clause exercise at five backlog-deferred cells); CR-BP-71/-73/-75/-78/-81 (admission tranche precedents).
**Lands against**: 45 PC records, 45 PG records, 136 BP records (was 135), 537 Activity records; 24-gate suite CONFORMANT; CR-META 0 new findings; Discovery gate 23 records checked (was 22).

---

## 1. Change Request

Land the canonical PC + PG + BP stack at the EnablementAndOperations x Activate coordinate, admitted from the CR-BP-80 escape-clause recommendation `Activate Operations Capability` (10/10 ADMIT-CANONICAL).

The BP identity:
- **id**: `dea:process-activate-operations-capability` (preserved unchanged from the CR-BP-80 discovery recommendation)
- **name**: `Activate Operations Capability` (verb + object form; satisfies BP-ARC-ID-001)
- **process_type**: `management`
- **process_intent**: `manage`
- **ECF coordinate**: `EnablementAndOperations x Activate`; identifier `ecf:enablementAndOperations.activate`

The trigger is the regulator's authorization or certification gating live service (Air Operator Certificate under EASA Part-OR / FAA Part 119; PSD2 / ECB / PRA payment-institution authorization under PSD2 Articles 11 and 28; EMA / FDA / MHRA GMP certification; MiCA Article 59 crypto-asset-service-provider authorization; ORR / ERA rail safety-case authorization; nuclear operations authorization). The outcome is the operations capability formally activated with the regulator's authorization on record, operations manuals and runbooks live, operational controls (incident management, capacity, security, compliance) live, and the supervisor's continuing-oversight relationship active on the regulated operations record.

## 2. Slice Mechanics

- **Land the stack together**: PC (`contexts/v1-alpha/dea-pc-oe-activate.yaml`), PG (`entities/v1-alpha/dea:group-regulated-operations-activation/...`), BP (`entities/v1-alpha/dea:process-activate-operations-capability/...`) in one commit. Research deposition at `entities/v1-alpha/dea:process-activate-operations-capability/research/l2-admission-deposition.yaml`.
- **Register flip** at OEAct cell: `disposition: ratified-accepted`, `audit_status: landed`, `ratified_by/at`, `landed_by/at`, `cr: CR-BP-82`, `applied_pr: TBD` (back-fill in next slice), and `admission_note` citing the CR-BP-80 discovery evidence. Carry-forward `deferral_reason` content retained per CR-BP-19 register methodology.
- **Register version**: v13 -> v14 (CR-BP-82 ratified; `ratified_accepted: 44 -> 45`; `backlog_deferred: 5 -> 4`).
- **Register the admission authority**: extend ADM-001 regex with `CR-BP-82`.
- **Locked reconciliation registers**: append new RETAIN entry to `reconciliation/dispositions/register.yaml`; insert `oe-act.82` tranche block in `reconciliation/tranches/plan.yaml` (records + `records_per_tranche: oe-act.82: 1` + `review_checkpoints: oe-act.82: 1`).
- **Discovery-side `admission` block** on the CR-BP-80 escape record's ADMIT-CANONICAL candidate: `status: admitted, admitted_by: CR-BP-82, admitted_as: dea:process-activate-operations-capability, admitted_at: '2026-09-16'`. Without this block, DISC-007 fires red on the escape record (canonical BP now exists with the same name).
- **BP context block** canonicalized to `context: [{ref: dea:pc-oe-activate}]` (BP-SEM-007 enforcement; replaces legacy scalar `process_context:`).
- **BP identity sub-block** added: `identity: {verb, object, scope, outcome_statement, evidence_links}` (BP-C1..C4 enforcement).
- **Count-assertion sweep**: 14 sites bumped across 8 test files (BP 136 -> 137; PG/PC 45 -> 46; report 763 -> 766; EXE 718 -> 720; L4 dict `{0:0, 1:0, 2:0, 3:1, 4:765}`).
- **Carrier CR + README row** at `change-requests/CR-BP-82-eo-activate-admission.md` (this file); README row inserted before the `## Cross-repo context` anchor.
- **Regen cascade** post-commit (per skill): CATALOG regenerated, open_change_requests 92 -> 93.

## 3. Gate Posture

After this slice:

- `python3 scripts/check_process_context.py`: PASS (PC-001..008)
- `python3 scripts/check_process_group.py`: PASS (PG-001..008)
- `python3 scripts/check_process_identity.py`: PASS (with suggestions; BP-ARC-ID-001..005 satisfied)
- `python3 scripts/check_process_semantics.py`: CONFORMANT (BP-SEM-001..014)
- `python3 scripts/check_lifecycle_discovery.py`: CONFORMANT, 23 records, 0 findings (DISC-001..008 all green)
- `python3 scripts/check_admission_gate.py --strict-provenance`: CONFORMANT-WITH-WARNINGS (CI-only mode; ADM-001 + ADM-008 enforced; my new BP satisfies ADM-001 with the regex extended with CR-BP-82; ADM-005 fires +2 over the baseline 224 per the established nested-trigger pattern)
- `python3 scripts/check_dispositions.py`: DISP-OK (0 errors; 18 dispositions checked)
- `python3 scripts/check_cr_metadata.py`: 0 NEW findings (19 pre-existing legacy unchanged)
- `python3 scripts/conformance_result.py`: 24 gates CONFORMANT (0 blocking, 0 advisory)
- pytest 10-file core: 227/227 PASS

## 4. Repo Changes

| Path | Change |
|---|---|
| `contexts/v1-alpha/dea-pc-oe-activate.yaml` | NEW (PC at OE x Activate coordinate; PC-001..008 schema-compliant; admission block cites CR-BP-80) |
| `entities/v1-alpha/dea:group-regulated-operations-activation/dea:group-regulated-operations-activation.yaml` | NEW (PG; functional kind; scope includes AOC / PSD2 / GMP / FAA Part 119 / MiCA / ORR-ERA / nuclear; E5 + E4 evidence) |
| `entities/v1-alpha/dea:process-activate-operations-capability/dea:process-activate-operations-capability.yaml` | NEW (BP; management type; canonical `context:` block; `identity` sub-block; 5 evidence_links; change_history) |
| `entities/v1-alpha/dea:process-activate-operations-capability/research/l2-admission-deposition.yaml` | NEW (research deposition citing CR-BP-80 discovery; admission_decision with evidence_base + bp_identity + boundary_clarity) |
| `entities/v1-alpha/dea:process-activate-operations-capability/research/README.md` | NEW (research README with L3 decomposition preview; 4 Activity candidates) |
| `discovery/v1-alpha/enablement-and-operations-activate-escape.yaml` | MOD (added `admission: {status: admitted, ...}` block on the ADMIT-CANONICAL candidate to close DISC-007) |
| `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml` | MOD (v13 -> v14; OEAct cell flipped to ratified-accepted/landed; v13_to_v14_note; counter `ratified_accepted: 44 -> 45`, `backlog_deferred: 5 -> 4`) |
| `scripts/check_admission_gate.py` | MOD (extended _ADMISSION_CR_RE regex with CR-BP-82) |
| `reconciliation/dispositions/register.yaml` | MOD (appended new RETAIN record for `dea:process-activate-operations-capability`; back-fill related_records: [CR-BP-80, CR-BP-82]) |
| `reconciliation/tranches/plan.yaml` | MOD (inserted `oe-act.82` tranche block; +2 to `records_per_tranche.oe-act.82: 1` and `review_checkpoints.oe-act.82: 1`) |
| `reconciliation/inventory.yaml` | MOD (regenerated; baseline v1 unchanged SHA) |
| `reconciliation/baseline/v1.yaml` | MOD (regenerated; SHA captures the 4 new files: PC, PG, BP, deposition) |
| `reconciliation/conformance_report.yaml` | MOD (regenerated; 763 -> 766 records; levels {0:0, 1:0, 2:0, 3:1, 4:765}) |
| `tests/test_check_activity_model.py` | MOD (count assertions 136 -> 137) |
| `tests/test_check_execution_boundary.py` | MOD (count assertions 718 -> 720; docstring narrative) |
| `tests/test_check_intent_purposive.py` | MOD (count 136 -> 137) |
| `tests/test_check_l2_qualification.py` | MOD (count 136 -> 137) |
| `tests/test_check_lifecycle_state.py` | MOD (count 136 -> 137) |
| `tests/test_check_semantic_identity_version.py` | MOD (count 136 -> 137) |
| `tests/test_reconciliation_baseline.py` | MOD (BPs 136 -> 137; PGs 45 -> 46; PCs 45 -> 46) |
| `tests/test_architectural_regression.py` | MOD (total 763 -> 766; L4 dict updated) |
| `tests/test_cr_bp16_gates.py` | MOD (candidate_count 136 -> 137; comment enumerates CR-BP-82) |
| `change-requests/CR-BP-82-eo-activate-admission.md` | NEW (this file) |
| `change-requests/README.md` | MOD (CR-BP-82 row added before `## Cross-repo context`) |
| `CATALOG.yaml` | MOD (regenerated; `open_change_requests` 92 -> 93) |

## 5. NOT-List (Out of Scope)

- **No L3 decomposition in this slice.** Activity records land in CR-BP-87 (next slice), following the established admission -> L3 decomposition cadence (CR-BP-71 -> CR-BP-77; CR-BP-73 -> CR-BP-77; CR-BP-75 -> CR-BP-77; CR-BP-78 -> CR-BP-79).
- **No register mutation beyond the OEAct cell.** EOAct, FAAct, SDAct remain backlog-deferred pending their own admission tranches (CR-BP-82/-83/-86 per program structure).
- **No new L0 records.** Discovery-side admission block appended on the existing escape record; no new discovery files.
- **No specialization.** ADMIT-SPECIALIZATION remains unauthorized per program governance (CR-BP-62 section 30).
- **No cross-repo work.** Stays in `dea-catalog-processes`; per-thread scope lock.

## 6. Acceptance Criteria

1. PC, PG, BP, and research deposition land together in one commit.
2. OEAct register cell flips from `backlog-deferred` to `ratified-accepted/landed` with `applied_pr: TBD` (back-fill in next slice after PR merges).
3. Register version advances v13 -> v14; counters updated.
4. ADM-001 regex extended with `CR-BP-82`; provenance check passes for the new BP.
5. Discovery-side `admission` block appended on the escape record's ADMIT-CANONICAL candidate; DISC-007 reports 0 findings.
6. Canonical `context:` block (BP-SEM-007) on the BP; legacy scalar `process_context:` removed.
7. BP `identity` sub-block added (BP-C1..C4).
8. Eight-site count-assertion sweep updated; 227/227 pytest PASS.
9. 24-gate conformance_result suite CONFORMANT (0 blocking, 0 advisory).
10. CATALOG.yaml regenerated; `open_change_requests` 92 -> 93.

## 7. Result

First canonical admission at the EnablementAndOperations x Activate coordinate. The 2024-2026 regulator-issued authorization landscape (EASA / FAA AOC under Part-OR / Part 119; PSD2 Articles 11 and 28 payment-institution authorization; EMA / FDA / MHRA GMP; MiCA Article 59 crypto-asset-service-provider authorization; ORR / ERA rail safety-case; nuclear operations authorization) establishes that regulator-issued authorization or certification creates a distinct activation step with continuing-supervisor notification, operations manuals and runbooks live, and operational controls (incident management, capacity, security, compliance) live on the regulated operations record: distinct from capability build (Build coordinate) and from steady-state operation (Operate coordinate). The cell's deferral rationale ("operations-capability activation is often an attribute of build or steady-state operation") is superseded by the universal-sector regulator-authorized activation regime.

Discovery-program posture after this slice: of the 5 backlog-deferred cells identified in CR-BP-80, OEAct is now landed; AOAct, FAAct, SDAct each carry an ADMIT-CANONICAL recommendation pending their own admission tranche; SDRet is documented DEFER (volume-lower cross-domain evidence) and closes the discovery loop without admission.

## 8. Mid-Flight Repairs (transparency)

Five mid-flight repairs were required during this slice (recipe-driven, not content changes):

1. **PC file wrote with truncated content** (163 bytes): my first PC `dea-pc-eo-activate` had `parameters containing a ... truncation` issue. Rewrote with full content directly.
2. **PC shape error** (PC-001..006 findings): the AO PC precedent used `cell_charter: {enterprise_concern, lifecycle_concern, combined_semantic_meaning, expected_outcomes, inclusions, exclusions, adjacent_boundaries}` not my initial `{purpose, scope.includes/excludes}`. Rewrote PC with the correct shape.
3. **EO ID ordering bug**: I used `dea:pc-eo-activate` but the v2 register and all other EO cells use `dea:pc-oe-activate` (with `oe` ordering). Renamed file and updated all references in PG/BP/deposition.
4. **ADM-001 BLOCKING on BP**: my BP change_history has `cr: CR-BP-82` but the regex didn't include CR-BP-82. Extended regex.
5. **BP-SEM-007 BLOCKING** + **BP-C1..C4 ADVISORY**: missing canonical `context:` block and `identity` sub-block. Added both; removed legacy scalar `process_context:` to satisfy test_reconciliation_baseline (which asserts `with_ctx_scalar == 0` after the migration contract landed).
6. **DISC-007 duplicate-name**: same as CR-BP-81 — appended `admission:` block on the escape record's ADMIT-CANONICAL candidate.
7. **Trigger/outcome length**: drafted <500 chars each from the start (AO BP precedent had triggered this on its slice; lesson carried forward).
8. **Em-dash sweep**: 2 violations in PG scope.excludes and research README caught and fixed before commit.