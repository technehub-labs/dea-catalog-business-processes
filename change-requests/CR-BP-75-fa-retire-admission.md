# CR-BP-75 - F&A Retire admission tranche (Regulated Run-Off)

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
**Date**: 2026-09-15

## 1. Change Request

Governed admission of the CR-BP-74 escape-clause recommendation at the
FinanceAndAccounting x Retire coordinate, landing the canonical
PC + PG + BP stack:
- dea:pc-fa-retire (Process Context)
- dea:group-regulated-run-off (Process Group, cross-cutting kind)
- dea:process-conclude-regulated-run-off (Business Process)

The register v2 cell's verbatim escape condition
("defer until a regulated unwind (e.g. mutual insurer run-off)
requires a standalone group") is activated by CR-BP-74 discovery
evidence: PRA PS20/24 (UK, in force 30 June 2026), FSB Final
Guidance on Insurance Resolution Strategies 2025, NAIC Model 901,
IFRS 17 (effective 2023), IFRS 5, ASC 205-30 Liquidation Basis
(FASB ASU 2013-07), ASC 944, IRO Best Practice Guidance 2024.

Register v10 -> v11: F&A x Retire flips from backlog-deferred to
ratified-accepted/landed; v10_to_v11_note documents the activation.
Counts 42/7 -> 43/6 ratified-accepted/backlog-deferred.

ADM-001 admission-authority regex extended to include CR-BP-75.
Disposition register: RETAIN entry appended (134 dispositions;
the A&O BP's CR-BP-73 entry had been displaced during the
CR-BP-73 amend cycle and was re-inserted before this F&A entry
during CR-BP-75 wiring; both BP entries are now in canonical
order). Tranche plan: fa-ret.75 appended; total 72/133 -> 73/134;
fa-ret.75 added to records_per_tranche and review_checkpoints;
ao-ret.73 retained at applied_pr '113'.

BP-ARC-ID-001 satisfied: name "Conclude a Regulated Run-Off" is
verb + object form; id preserved unchanged from the CR-BP-74
discovery recommendation. Process Identity gate verifies 0
errors on the new BP.

## 2. Scope contract (PC charter, BP-LIFE-009 / MECE-007)

In scope at dea:pc-fa-retire:
- Regulator-acknowledged run-off authorisation (PRA, FCA, NAIC,
  IAIS, EIOPA member authorities)
- Run-off plan submission within the controlling regulator's
  window (28-day window under PRA PS20/24)
- Statutory accounting basis transition: going-concern to
  liquidation-basis (ASC 205-30) or fulfillment-measurement
  (IFRS 17 run-off treatment)
- Reserving, capital adequacy, and asset-liability matching
  throughout the run-off period
- Policyholder priority creditor treatment and policyholder
  claim adjudication and payment
- Communications to policyholders and stakeholders
- Retained-records and service-of-process obligations
- Tax-clearance and statutory liability settlement
- Solvent exit certification (PRA) or run-off completion
  certification (FSB)

Out of scope (boundary explicit):
- Pre-run-off financial stewardship (F&A x Operate)
- Physical asset decommissioning (EnablementAndOperations x
  Retire; CR-BP-66)
- Counterparty and agent relationship closure
  (PartyAndRelationship x Retire; CR-BP-67)
- Product line retirement (ProductAndValue x Retire)
- Non-insurance regulated wind-downs (banks under PRA BRRD /
  FDIC OLA, pension funds under PBGC termination) -- deferred
  to a future CR
- Investment disposal as a standalone Process (subsumed as an
  Activity under this cell's BP; CR-BP-74 candidate 3)
- Impairment and exit-liability recognition as a standalone
  Process (subsumed as an Activity under this cell's BP;
  CR-BP-74 candidate 4)

## 3. Repository changes

New:
- contexts/v1-alpha/dea-pc-fa-retire.yaml (PC charter; cell_charter
  block satisfies PC-006)
- entities/v1-alpha/dea:group-regulated-run-off/... (PG with
  cross_coordinate_doctrine omitted for schema compliance;
  CR-BP-73 CI-driven fix-applied)
- entities/v1-alpha/dea:process-conclude-regulated-run-off/...
  (BP with identity block, evidence_links in schema-compliant
  vocabulary [regulation/standard], relationships block, ECF
  conformance, full metadata and links to PC + PG + discovery
  + register)
- entities/v1-alpha/dea:process-conclude-regulated-run-off/research/README.md
  (research subtree README required by catalog-index gate)
- entities/v1-alpha/dea:process-conclude-regulated-run-off/research/l2-admission-deposition.yaml
  (admission deposition mirror of CR-BP-71/73 shape)
- change-requests/CR-BP-75-fa-retire-admission.md (this file)

Modified:
- entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml
  v10 -> v11; F&A x Retire cell flipped; v10_to_v11_note added;
  carry-forward candidates retained in l2_candidates for
  traceability (Operate financial wind-down DEFER 5/10; Dispose
  of investments and Recognize impairment and exit liabilities
  RECLASSIFY 3/10 each, to be Activity-decomposed at L3 in
  CR-BP-7x+)
- scripts/check_admission_gate.py ADM-001 regex extended to
  include CR-BP-75
- reconciliation/dispositions/register.yaml RETAIN entry appended
  (133 -> 134 dispositions; the A&O BP's CR-BP-73 entry was
  re-inserted in canonical order alongside the F&A BP's
  CR-BP-75 entry)
- reconciliation/tranches/plan.yaml fa-ret.75 tranche block;
  totals 72/133 -> 73/134; fa-ret.75 in records_per_tranche
  and review_checkpoints
- reconciliation/baseline/v1.yaml (regenerated sha256 for the
  new PC file)
- discovery/v1-alpha/finance-and-accounting-retire-escape.yaml
  candidate[0] admission block appended (closes the
  recommendation loop, satisfying DISC-007 admission-resolution)
- tests/* count assertions updated
  - BP 133 -> 134 (test_check_activity_model, test_cr_bp16_gates)
  - PG/PC 42 -> 43 (test_reconciliation_baseline)
  - EXE 696 -> 698 (test_check_execution_boundary)
  - report 738 -> 741 (test_architectural_regression, both
    total_records and conformance_levels L4 assertion)
  - dispositions 72 -> 73 (test_dispositions)
  - ADM candidate_count 133 -> 134 (4 JSON-payload tests)
  - Records-checked 133 -> 134 across 4 validator tests
  - baseline sha256 regenerated
- CATALOG.yaml regenerated (open_change_requests 84 -> 85)
- conformance_report.yaml regenerated (741 records, all L4)

## 4. Verified

- check_process_context.py PASS (PC-001..PC-008)
- check_process_group.py PASS (PG-001..PG-008)
- check_process_semantics.py CONFORMANT (BP-SEM-008 fixed by
  restricting context ref to PC only, BP-SEM-012 is a permissible
  cross-context warning)
- check_process_identity.py 0 errors on the new BP
- check_process_specialization.py PASS
- check_architectural_regression.py CONFORMANT (BP-AR-001..007)
- check_admission_gate.py CR-BP-75 registered; gate passes
- check_dispositions.py DISP-OK (0 errors, 113 warnings all
  pre-existing)
- check_lifecycle_discovery.py CONFORMANT (17 records, 0 findings)
- check_ecf_conformance.py 698 entries conform (PC + BP enter the
  EXE ledger; PG does not)
- check_activity_model.py CONFORMANT (Activity 521, BP 134)
- check_execution_boundary.py CONFORMANT (Records 698)
- check_lifecycle_state / check_intent_purposive /
  check_l2_qualification / check_semantic_identity_version:
  CONFORMANT, all 134 BPs
- check_process_context_relationships.py PASS (evidence_links
  schema-compliant; trigger and outcome trimmed under 500-char
  limits)
- check_catalog_index.py --strict PASS (697 entities)
- regenerate_catalog.py --check PASS
- build_conformance_report.py: 741 records (all L4); CR-BP-75
  PG/PC/BP all at L4 with change_history_admission evidence
- 24-gate suite CONFORMANT (0 blocking, 0 advisory)
- CR-META 0 new findings
- pytest 383/0
- reconciliation/baseline/v1.yaml sha256 matches live catalog

## 5. NOT-list

- No L3 Activities (separate slice; CR-BP-7x+)
- No other register cell flips
- No specialization, cross-stage, or new-domain admission
- Not stacked on open PRs (branch cut from origin/main post-#115)
- No change to PG kind (cross-cutting, mirroring CR-BP-73
  Regulated Workforce Wind-Down)
- Trigger and outcome trimmed under 500-char limit (the ao BP's
  244-char trigger and 340-char outcome are unaffected; CI-driven
  schema-validity fix)

## 6. Next step (separate slice)

G&E x Retire (regulator-mandated unwind), the fourth item in
the Option B backlog-deferred sequence. The G&E x Retire register
v2 cell has the verbatim deferral "Retirement of governance is
rare and largely an attribute of operating-model retirement; defer
until a sector example (e.g. regulator-mandated unwind) requires
it." CR-BP-76 (escape-clause discovery) and CR-BP-77 (admission
tranche) are the projected workstreams.
