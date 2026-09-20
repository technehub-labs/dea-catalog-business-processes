# CR-BP-78 - G&E Retire Admission Tranche (Regulator-Mandated Governance Unwind)

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Proposed
**Layer**: L2
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-16
**Carrier**: Fourth discovery-driven admission tranche under the CR-BP-62 escape-clause method; lands the canonical PC + PG + BP stack at the GovernanceAndExistence x Retire coordinate after the CR-BP-76 escape-clause exercise (candidate 1 ADMIT-CANONICAL recommendation at 9/10).
**Depends on**: CR-BP-62 (lifecycle process discovery method + DISC-001..008 gate), CR-BP-63 (Activate/Retire discovery exercise), CR-BP-70/-72/-74/-76 (escape-clause discoveries at P&R Activate, A&O Retire, F&A Retire, G&E Retire), CR-BP-71/-73/-75 (admission tranches at the first three cells), CR-BP-19 (v2 escape-clause register), CR-BP-04 (Business Process Identity & ID-Family Reconciliation).
**Lands against**: 134 canonical BP records, 43 canonical PG records, 533 canonical Activity records, 18 canonical Discovery records; full pytest suite + CR-META + catalog-index gates CONFORMANT.

---

## 1. Change Request

Land the canonical Process Context, Process Group, and Business Process records for the GovernanceAndExistence x Retire coordinate, activating the register v2 verbatim escape clause "defer until a sector example (e.g. regulator-mandated unwind) requires it" against the CR-BP-76 escape-clause discovery exercise. The cell reverses from backlog-deferred to ratified-accepted/landed in register v12. The carrier CR lands:

- one Process Context: `dea:pc-ge-retire`
- one Process Group: `dea:group-regulated-governance-unwind`
- one Business Process: `dea:process-effect-regulator-mandated-governance-unwind`

with the corresponding `admission` block on the candidate-1 record of `discovery/v1-alpha/governance-and-existence-retire-escape.yaml`, the register v11-to-v12 ratification flip in `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml`, the dispositions register RETAIN record, and the tranches plan `ge-ret.78` block (and corrects the A&O admission `applied_pr: 113` -> `114`).

This is the second discovery-driven admission at a Retire coordinate (after CR-BP-73 and CR-BP-75) and the fourth overall under the CR-BP-62 method. The discovery record scored 9/10 ADMIT-CANONICAL on the register v2 cell's verbatim escape condition. Evidence base: UK FCA Wind-Down Planning Group supervisory framework, California Corporations Code sections 5033-5034 (US nonprofit dissolution), IRS 501(c)(3) federal tax-exempt dissolution obligations, state attorney-general charity oversight and asset-disposition review, federal banking regulator cease-and-desist authority, US federal and state court receivership authority.

## 2. Scope

### In scope

- Regulator- or court-mandated governance unwind (the only governed trigger).
- Governance body reduction to wind-down quorum under the controlling statute or regulator or court order.
- Policy instrument sunset or supersession by wind-down procedures.
- Statutory dissolution filings (Form 990-N/990 for IRS 501(c)(3) status termination, California Secretary of State Form DISS for corporate dissolution, Attorney General notifications for charity asset disposition, court reports for receivership termination, FCA S60.060 Form A notification for authorisation surrender).
- Retained-records custodianship assignment for the statutorily required period (California Corp Code 6323, FTC/DOJ obligations, IRS recordkeeping under Treas. Reg. 1.6001-1).
- Surrender of authorisation or cancellation of permission per the regulator or court determination.

### Out of scope (reserved)

- Asset and capability retirement (lives at EnablementAndOperations x Retire).
- Voluntary governance sunset absent regulator or court mandate (reserved for a future G&E x Improve coordinate charter extension).
- Counterparty closure (lives at PartyAndRelationship x Retire).
- Workforce wind-down (lives at AgencyAndOrganization x Retire via CR-BP-73).
- Regulated entity run-off (lives at FinanceAndAccounting x Retire via CR-BP-75).

## 3. Cell Charter Summary

The `dea:pc-ge-retire` Process Context covers the bounded regulator- or court-mandated governance unwind work a Process owning the GovernanceAndExistence lifecycle stage's Retire transition can own. The voluntary governance sunset absent regulator or court mandate is explicitly reserved for a future G&E x Improve coordinate charter extension; that exclusion is recorded in `l2-candidate-universe.yaml` and `l2-admission-deposition.yaml` so it is discoverable from the cell charter. The Process Group owns the regulator- and court-anchored evidence base; the BP owns the testable outcome (the governance regime is wound down under the controlling regulator or court authority).

## 4. Files Touched

| Path | Change |
|---|---|
| `contexts/v1-alpha/dea-pc-ge-retire.yaml` | new PC |
| `entities/v1-alpha/dea:group-regulated-governance-unwind/dea:group-regulated-governance-unwind.yaml` | new PG |
| `entities/v1-alpha/dea:process-effect-regulator-mandated-governance-unwind/dea:process-effect-regulator-mandated-governance-unwind.yaml` | new BP |
| `entities/v1-alpha/dea:process-effect-regulator-mandated-governance-unwind/research/l2-admission-deposition.yaml` | new research deposition |
| `entities/v1-alpha/dea:process-effect-regulator-mandated-governance-unwind/research/README.md` | new research README |
| `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml` | register v11 -> v12; G&E x Retire cell flipped |
| `reconciliation/dispositions/register.yaml` | new RETAIN record for the BP; back-fill `applied_pr` for CR-BP-71/-73/-75 |
| `reconciliation/tranches/plan.yaml` | new `ge-ret.78` block; back-fill `applied_pr: 113` -> `114` for CR-BP-73 |
| `discovery/v1-alpha/governance-and-existence-retire-escape.yaml` | add `admission` block to candidate 1 |
| `scripts/check_admission_gate.py` | extend ADM-001 regex with CR-BP-78 |
| `reconciliation/inventory.yaml` | regenerated |
| `reconciliation/baseline/v1.yaml` | regenerated (immutable SHA unchanged) |
| `reconciliation/conformance_report.yaml` | regenerated (753 -> 756 records) |
| `CATALOG.yaml` | regenerated (710 -> 712 entities; open_change_requests 89 -> 90) |
| `tests/test_check_activity_model.py` | count assertions 134 -> 135; docstring narrative |
| `tests/test_check_intent_purposive.py` | count assertions 134 -> 135 |
| `tests/test_check_l2_qualification.py` | count assertions 134 -> 135 |
| `tests/test_check_lifecycle_state.py` | count assertions 134 -> 135 |
| `tests/test_check_semantic_identity_version.py` | count assertions 134 -> 135 |
| `tests/test_architectural_regression.py` | 753 -> 756 |
| `tests/test_reconciliation_baseline.py` | business_processes 134 -> 135; process_groups 43 -> 44; process_contexts 43 -> 44 |
| `tests/test_cr_bp16_gates.py` | candidate_count 134 -> 135 (per BP comment update) |

## 5. Gates Posture

- DISC-001..008: CONFORMANT, 18 records, 0 findings (DISC-007 duplicate-name face resolved by admission block).
- Process Identity: PASS (BP-ARC-ID-001/003/004; BP-ARC-ID-003 outcome_mismatch advisory).
- CR-META: 0 NEW findings (19 pre-existing legacy unchanged).
- Schema catalog-index: PASS (712 entities).
- Schema validate-process-entries: PASS.
- 24-gate conformance_result suite: CONFORMANT, 0 blocking, 0 advisory.
- pytest targeted suite (10 files): 195/195 PASS.

## 6. Follow-On

- L3 Activity decomposition for the new BP (likely 4 Activity records, mirroring the CR-BP-77 pattern): `CR-BP-79` candidate.
- Discovery record dispositions register: candidate 2 (Operate Governance Sunset Procedures, DEFER 5/10) remains pending a future G&E x Improve coordinate charter extension; candidates 3-4 (Document Governance Wind-Down Plan, File Statutory Governance Dissolution Filings, RECLASSIFY 3/10 each) are reserved as Activity-level decomposition candidates for the CR-BP-79 tranche or later.