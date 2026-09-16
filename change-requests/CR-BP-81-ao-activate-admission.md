# CR-BP-81 - AO.Activate Admission Tranche (Mobilize Licensed Workforce)

**Status**: Proposed
**Layer**: L2
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-16
**Carrier**: Fifth discovery-driven admission under the CR-BP-62 escape-clause method; first canonical admission at the AgencyAndOrganization x Activate coordinate. Lands the PC + PG + BP stack, the L2 admission deposition, the register cell flip, ADM-001 authority extension, and reconciliation artifacts. L3 decomposition follows as CR-BP-87.
**Depends on**: CR-BP-19 (register v2 deferral); CR-BP-62 (discovery method, BP-LIFE-001..015); CR-BP-63 (first Activate/Retire exercise); CR-BP-80 (escape-clause exercise at five backlog-deferred cells); CR-BP-71/-73/-75/-78 (admission tranche precedents).
**Lands against**: 44 PC records, 44 PG records, 135 BP records (was 134), 533 Activity records; 24-gate suite CONFORMANT; CR-META 0 new findings; Discovery gate 18 + 5 =23 records checked (was 22).

---

## 1. Change Request

Land the canonical PC + PG + BP stack at the AgencyAndOrganization x Activate coordinate, admitted from the CR-BP-80 escape-clause recommendation `Mobilize Licensed Workforce` (10/10 ADMIT-CANONICAL).

The BP identity:
- **id**: `dea:process-mobilize-licensed-workforce` (preserved unchanged from the CR-BP-80 discovery recommendation)
- **name**: `Mobilize Licensed Workforce` (verb + object form; satisfies BP-ARC-ID-001)
- **process_type**: `management`
- **process_intent**: `manage`
- **ECF coordinate**: `AgencyAndOrganization x Activate`; identifier `ecf:agencyOrganization.activate`

The trigger is the enterprise's regulated-entity approval for a licensed role (banking controlled functions under FCA SMCR CF1..CF11, healthcare practitioners under US state healthcare licensure, licensed professional services under UK SRA / US state bar admissions, telecommunications licensed engineers under FCC commercial-operator regime, aviation crew under FAA / EASA type-rating, insurance producers under NAIC Producer Licensing Model Act and state producer licensing). The outcome is the live-readiness activation of the licensed role with the supervisor-controlled scope preserved (signing authority or controlled-function designation), fitness-and-propriety attestation recorded, supervised-training completion preserved, and continuing-supervisor notification activated.

## 2. Slice Mechanics

- **Land the stack together**: PC (`contexts/v1-alpha/dea-pc-ao-activate.yaml`), PG (`entities/v1-alpha/dea:group-licensed-workforce-mobilization/...`), BP (`entities/v1-alpha/dea:process-mobilize-licensed-workforce/...`) in one commit. Research deposition at `entities/v1-alpha/dea:process-mobilize-licensed-workforce/research/l2-admission-deposition.yaml`.
- **Register flip** at AOAct cell: `disposition: ratified-accepted`, `audit_status: landed`, `ratified_by/at`, `landed_by/at`, `cr: CR-BP-81`, `applied_pr: TBD` (back-fill in next slice), and `admission_note` citing the CR-BP-80 discovery evidence.
- **Register version**: v12 -> v13 (CR-BP-81 ratified; `ratified_accepted: 43 -> 44`; `backlog_deferred: 6 -> 5`).
- **Register the admission authority**: extend ADM-001 regex with `CR-BP-81`.
- **Locked reconciliation registers**: append new RETAIN entry to `reconciliation/dispositions/register.yaml`; insert `ao-act.81` tranche block in `reconciliation/tranches/plan.yaml` (records + `records_per_tranche: ao-act.81: 1` + `review_checkpoints: ao-act.81: 1`).
- **Discovery-side `admission` block** on the CR-BP-80 escape record's ADMIT-CANONICAL candidate: `status: admitted, admitted_by: CR-BP-81, admitted_as: dea:process-mobilize-licensed-workforce, admitted_at: '2026-09-16'`. Without this block, DISC-007 fires red on the escape record (canonical BP now exists with the same name).
- **Count-assertion sweep**: 14 sites bumped across 8 test files.
- **Carrier CR + README row** at `change-requests/CR-BP-81-ao-activate-admission.md` (this file); README row inserted before the `## Cross-repo context` anchor.
- **Regen cascade** post-commit (per skill): CATALOG regenerated, open_change_requests 91 -> 92.

## 3. Gate Posture

After this slice:

- `python3 scripts/check_process_context.py`: PASS (PC-001..008)
- `python3 scripts/check_process_group.py`: PASS (PG-001..008)
- `python3 scripts/check_process_identity.py`: PASS (with suggestions; BP-ARC-ID-001..005 satisfied; identity sub-block present on the new BP)
- `python3 scripts/check_lifecycle_discovery.py`: CONFORMANT, 23 records (was 22; +1 escape record's admission block resolved DISC-007), 0 findings
- `python3 scripts/check_admission_gate.py --strict-provenance`: CONFORMANT-WITH-WARNINGS (CI-only mode; ADM-001 + ADM-008 enforced; my new BP satisfies ADM-001 with the regex extended with CR-BP-81; ADM-005 fires +2 over the baseline 224 per the established nested-trigger pattern)
- `python3 scripts/check_dispositions.py`: DISP-OK (0 errors; 18 dispositions checked)
- `python3 scripts/check_cr_metadata.py`: 0 NEW findings (19 pre-existing legacy unchanged)
- `python3 scripts/conformance_result.py`: 24 gates CONFORMANT (0 blocking, 0 advisory)
- pytest 10-file core: 227/227 PASS

## 4. Repo Changes

| Path | Change |
|---|---|
| `contexts/v1-alpha/dea-pc-ao-activate.yaml` | NEW (PC at A&O x Activate coordinate; 7-field cell_charter + admission block + change_history) |
| `entities/v1-alpha/dea:group-licensed-workforce-mobilization/dea:group-licensed-workforce-mobilization.yaml` | NEW (PG; cross-cutting kind; functional scope; E5 + E4 evidence) |
| `entities/v1-alpha/dea:process-mobilize-licensed-workforce/dea:process-mobilize-licensed-workforce.yaml` | NEW (BP; management type; identity sub-block; 5 evidence_links; change_history) |
| `entities/v1-alpha/dea:process-mobilize-licensed-workforce/research/l2-admission-deposition.yaml` | NEW (research deposition citing CR-BP-80 discovery; admission_decision with evidence_base + bp_identity + boundary_clarity) |
| `entities/v1-alpha/dea:process-mobilize-licensed-workforce/research/README.md` | NEW (research README with L3 decomposition preview) |
| `discovery/v1-alpha/agency-and-organization-activate-escape.yaml` | MOD (added `admission: {status: admitted, ...}` block on the ADMIT-CANONICAL candidate to close DISC-007) |
| `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml` | MOD (v12 -> v13; AOAct cell flipped to ratified-accepted/landed; v12_to_v13_note; counter `ratified_accepted: 43 -> 44`, `backlog_deferred: 6 -> 5`) |
| `scripts/check_admission_gate.py` | MOD (extended _ADMISSION_CR_RE regex with CR-BP-81) |
| `reconciliation/dispositions/register.yaml` | MOD (appended new RETAIN record for `dea:process-mobilize-licensed-workforce`; back-fill related_records: [CR-BP-80]) |
| `reconciliation/tranches/plan.yaml` | MOD (inserted `ao-act.81` tranche block; +2 to `records_per_tranche.ao-act.81: 1` and `review_checkpoints.ao-act.81: 1`) |
| `reconciliation/inventory.yaml` | MOD (regenerated; baseline v1 unchanged SHA) |
| `reconciliation/baseline/v1.yaml` | MOD (regenerated; SHA captures the 4 new files: PC, PG, BP, deposition) |
| `reconciliation/conformance_report.yaml` | MOD (regenerated; 760 -> 763 records; levels {0:0, 1:0, 2:0, 3:0, 4:763}) |
| `tests/test_check_activity_model.py` | MOD (count assertions 135 -> 136) |
| `tests/test_check_execution_boundary.py` | MOD (count assertions 716 -> 718; docstring narrative) |
| `tests/test_check_intent_purposive.py` | MOD (count 135 -> 136) |
| `tests/test_check_l2_qualification.py` | MOD (count 135 -> 136) |
| `tests/test_check_lifecycle_state.py` | MOD (count 135 -> 136) |
| `tests/test_check_semantic_identity_version.py` | MOD (count 135 -> 136) |
| `tests/test_reconciliation_baseline.py` | MOD (BPs 135 -> 136; PGs 44 -> 45; PCs 44 -> 45) |
| `tests/test_architectural_regression.py` | MOD (total 760 -> 763; L4 dict) |
| `tests/test_cr_bp16_gates.py` | MOD (candidate_count 135 -> 136; comment enumerates CR-BP-81) |
| `change-requests/CR-BP-81-ao-activate-admission.md` | NEW (this file) |
| `change-requests/README.md` | MOD (CR-BP-81 row added before `## Cross-repo context`) |
| `CATALOG.yaml` | MOD (regenerated; `open_change_requests` 91 -> 92) |

## 5. NOT-List (Out of Scope)

- **No L3 decomposition in this slice.** Activity records land in CR-BP-87 (next slice), following the established admission -> L3 decomposition cadence (CR-BP-71 -> CR-BP-77; CR-BP-73 -> CR-BP-77; CR-BP-75 -> CR-BP-77; CR-BP-78 -> CR-BP-79).
- **No register mutation beyond the AOAct cell.** EO.Activate, FA.Activate, SD.Activate remain backlog-deferred pending their own admission tranches (CR-BP-82/-83/-86 per program structure).
- **No new L0 records.** Discovery-side admission block appended on the existing escape record; no new discovery files.
- **No specialization.** ADMIT-SPECIALIZATION remains unauthorized per program governance (CR-BP-62 section 30).
- **No cross-repo work.** Stays in `dea-catalog-processes`; per-thread scope lock.

## 6. Acceptance Criteria

1. PC, PG, BP, and research deposition land together in one commit.
2. AOAct register cell flips from `backlog-deferred` to `ratified-accepted/landed` with `applied_pr: TBD` (back-fill in next slice after PR merges).
3. Register version advances v12 -> v13; counters updated.
4. ADM-001 regex extended with `CR-BP-81`; provenance check passes for the new BP.
5. Discovery-side `admission` block appended on the escape record's ADMIT-CANONICAL candidate; DISC-007 reports 0 findings.
6. Eight-site count-assertion sweep updated; 227/227 pytest PASS.
7. 24-gate conformance_result suite CONFORMANT (0 blocking, 0 advisory).
8. CATALOG.yaml regenerated; `open_change_requests` 91 -> 92.

## 7. Result

First canonical admission at the AgencyAndOrganization x Activate coordinate. The 2024-2026 supervised-individual-licensing landscape (FCA SMCR, US state healthcare licensure, NAIC Producer Licensing, EASA/FAA crew licensing, UK SRA / US state bar admissions) establishes that licensed-workforce mobilization is a distinct enterprise concern with regulator-controlled scope, fitness-and-propriety attestation, supervised-training completion, and continuing-supervisor notification -- distinct from general workforce build (Build coordinate) and from steady-state workforce performance management (Operate coordinate). The cell's deferral rationale ("workforce activation is often an attribute of build") is superseded by the regulated-sector evidence.

Discovery-program posture after this slice: of the 5 backlog-deferred cells identified in CR-BP-80, AOAct is now landed; EOAct, FAAct, SDAct each carry an ADMIT-CANONICAL recommendation pending their own admission tranche; SDRet is documented DEFER (volume-6-lower cross-domain evidence) and closes the discovery loop without admission.