# CR-BP-73 - A&O Retire admission tranche (Regulated Workforce Wind-Down)

**Status**: Proposed
**Layer**: L2
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-15

## 1. Change Request

Governed admission of the CR-BP-72 escape-clause recommendation at the
AgencyAndOrganization x Retire coordinate, landing the canonical
PC + PG + BP stack:
- dea:pc-ao-retire (Process Context)
- dea:group-regulated-workforce-wind-down (Process Group,
  cross-cutting kind)
- dea:process-conduct-regulated-workforce-wind-down (Business Process)

The register v2 cell's verbatim escape condition ("defer until a
regulated wind-down (e.g. mass layoff) requires a dedicated L1 group")
is activated by CR-BP-72 discovery evidence: U.S. WARN Act
(29 U.S.C. 2101 et seq.; 20 CFR Part 639), EU Council Directive
98/59/EC, ILO Conventions 158 (1982) and 135 (1971), OECD Employment
Outlook, UK TULRCA s.188, German BetrVG section 17.

Register v10: A&O x Retire flips from backlog-deferred to
ratified-accepted/landed; v9_to_v10_note documents the activation.
Counts 41/8 -> 42/7 ratified-accepted/backlog-deferred.

ADM-001 admission-authority regex extended to include CR-BP-73.
Disposition register: RETAIN entry appended (133 dispositions).
Tranche plan: ao-ret.73 appended; total 71/132 -> 72/133; pr-act.71
applied_pr updated null -> '112' to reflect the merged #112.

BP-ARC-ID-001 satisfied: name "Conduct Regulated Workforce Wind-Down"
is verb + object form; id preserved unchanged from the CR-BP-72
discovery recommendation. Process Identity gate verifies 0 errors
on the new BP.

## 2. Scope contract (PC charter, BP-LIFE-009 / MECE-007)

In scope at dea:pc-ao-retire:
- Statutory advance notice to affected employees (WARN 60-day rule;
  jurisdictional equivalents)
- Information and consultation with workers' representatives (EU
  Directive 98/59/EC; jurisdictional works-council obligations)
- Fair-selection criteria (anti-discrimination, statutory exclusions)
- Severance, benefits continuation, and recorded statutory liability
- Transition supports: state dislocated-worker referral, training,
  health-care continuation, outplacement

Out of scope (boundary explicit):
- Steady-state offboarding of individual agents (AgencyAndOrganization
  x Operate)
- Non-regulated cohort decommission (Operate coordinate or Activity
  under agent operations)
- Asset retirement, decommissioning, and shutdown
  (EnablementAndOperations x Retire; CR-BP-66)
- Relationship close-out and regulated offboarding
  (PartyAndRelationship x Retire; CR-BP-67)
- Knowledge archival absent regulated wind-down triggers (Operate
  coordinate or Activity under knowledge management)

## 3. Repository changes

New:
- contexts/v1-alpha/dea-pc-ao-retire.yaml (PC charter; cell_charter
  block satisfies PC-006)
- entities/v1-alpha/dea:group-regulated-workforce-wind-down/...
  (PG with change_history block, cross_coordinate_doctrine,
  invariants, identity_keys, mece_coordinates, admission metadata)
- entities/v1-alpha/dea:process-conduct-regulated-workforce-wind-down/...
  (BP with identity block, evidence_links in schema-compliant
  vocabulary [documentation/governance/interview/artifact/standard/
  regulation], relationships block, ECF conformance, full metadata
  and links to PC + PG + discovery + register)
- entities/v1-alpha/dea:process-conduct-regulated-workforce-wind-down/research/README.md
  (research subtree README required by catalog-index gate)
- entities/v1-alpha/dea:process-conduct-regulated-workforce-wind-down/research/l2-admission-deposition.yaml
  (admission deposition mirror of CR-BP-71 shape)
- change-requests/CR-BP-73-ao-retire-admission.md (this file)

Modified:
- entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml
  v9 -> v10; A&O x Retire cell flipped; v9_to_v10_note added
- scripts/check_admission_gate.py ADM-001 regex extended to include
  CR-BP-73
- reconciliation/dispositions/register.yaml RETAIN entry appended
  (133 dispositions)
- reconciliation/tranches/plan.yaml ao-ret.73 tranche block; totals
  71/132 -> 72/133; review_checkpoints updated; pr-act.71
  applied_pr updated null -> '112'
- discovery/v1-alpha/agency-and-organization-retire-escape.yaml
  candidate[0] admission block appended (closes the recommendation
  loop, satisfying DISC-007 admission-resolution)
- tests/* count assertions updated
  - BP 132 -> 133 (test_check_activity_model, test_cr_bp16_gates)
  - PG/PC 41 -> 42 (test_reconciliation_baseline)
  - EXE 694 -> 696 (test_check_execution_boundary)
  - report 735 -> 738 (test_architectural_regression)
  - dispositions 71 -> 72 (test_dispositions)
  - ADM candidate_count 132 -> 133 (4 JSON-payload tests)
  - Records-checked counts 132 -> 133 (4 validator tests)
  - baseline sha256 regenerated
- CATALOG.yaml regenerated (open_change_requests 83 -> 84)

## 4. Verified

- check_process_context.py PASS (PC-001..PC-008)
- check_process_group.py PASS (PG-001..PG-008)
- check_process_semantics.py CONFORMANT (BP-SEM-008 fixed by
  restricting context ref to PC only, BP-SEM-012 is a permissible
  cross-context warning)
- check_process_identity.py 0 errors on the new BP
- check_process_specialization.py PASS
- check_architectural_regression.py CONFORMANT (BP-AR-001..007)
- check_admission_gate.py CR-BP-73 registered; gate passes
- check_dispositions.py DISP-OK (0 errors, 113 warnings all pre-existing)
- check_lifecycle_discovery.py CONFORMANT (16 records, 0 findings)
- check_ecf_conformance.py 696 entries conform (PC + BP enter the
  EXE ledger; PG does not)
- check_activity_model.py CONFORMANT (Activity 521, BP 133)
- check_execution_boundary.py CONFORMANT (Records 696)
- check_lifecycle_state / check_intent_purposive /
  check_l2_qualification / check_semantic_identity_version:
  CONFORMANT, all 133 BPs
- check_process_context_relationships.py PASS (evidence_links
  schema-compliant)
- check_catalog_index.py --strict PASS (696 entities)
- regenerate_catalog.py --check PASS
- build_conformance_report.py: 738 records (all L4); CR-BP-73 PG/PC/BP
  all at L4 with change_history_admission evidence
- 24-gate suite CONFORMANT (0 blocking, 0 advisory)
- CR-META 0 new findings
- pytest 383/0
- reconciliation/baseline/v1.yaml sha256 matches live catalog

## 5. NOT-list

- No L3 Activities (separate slice; CR-BP-74+)
- No other register cell flips
- No specialization, cross-stage, or new-domain admission
- Not stacked on open PRs (branch cut from origin/main post-#113)
- No change to PG kind (cross-cutting, mirroring CR-BP-71 Regulated
  Onboarding)

## 6. Next step (separate slice)

F&A x Retire (mutual insurer run-off), the third item in the Option B
backlog-deferred sequence. The carry-forward candidates (Manage
redundancy, Offboard departing agents, Decommission artificial
agents, Decommission organizational unit) remain in l2_candidates
of the A&O x Retire register cell for traceability but are now
subsumed by the admitted BP and the Operate coordinate.
