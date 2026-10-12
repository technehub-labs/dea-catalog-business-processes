# CR-BP-106 — AgencyAndOrganization Regulator-Tied Admission Tranche (5 cells, additive)

**Status**: Proposed (this PR)
**Layer**: L2 (Business Process admission)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-22
**Lands against**: 5 L2 BP admissions; 30 conformance gates (all PASS, 0 blocking, 0 advisory); MECE-001..008 CONFORMANT (0 findings); IDM-001..007 CONFORMANT; LCM-001..005 CONFORMANT; ACT-001..010 CONFORMANT; BP-C1..C4 + BP-QUAL-001..012 CONFORMANT.

## 1. Goal

Admit 5 regulator-tied Business Processes as additional L2 records at the AgencyAndOrganization x {Conceive, Design, Build, Operate, Improve} ECF cells. Each regulator-tied BP is admitted alongside the substrate-neutral general-case BPs that already exist at those cells; the regulator-tied specialization adds a distinct group-level concern (regulator-controlled scope, fitness-and-propriety attestation, supervised-training completion, continuing-supervisor notification) without displacing the substrate-neutral BPs.

Each admission is governed by the CR-BP-105 escape-clause discovery outcome (10/10, ADMIT-CANONICAL recommendation) under the CR-BP-62 method. The combined single-PR cadence mirrors the CR-BP-87 precedent (combined L3/L4 decomposition tranche for the 4 Activate Business Processes) and the CR-BP-mv1 precedent (combined org-wide id-system migration).

> **Correction note (2026-09-22):** An earlier draft of this CR proposed a slice that replaced each cell's existing Process Group with a regulator-tied specialization PG (dropping the substrate-neutral BPs from `composes:`). That draft created 18 orphan-BP findings (MECE-008) and was rejected in pre-push review. The current slice is **additive**: each cell's existing Process Group keeps its cell-level substrate-neutral name and definition; the regulator-tied BP is appended to the existing PG's `composes:` and `canonical_processes:`; no substrate-neutral BP is displaced. The earlier draft's carrier claim "substrate-neutral general-case BPs are NOT displaced" is now backed by structural reality.

## 2. The 5 Regulator-Tied Business Processes

| Cell | New BP id | Verb + Object | Discovery | Score |
|---|---|---|---|---|
| ao-conceive | `processes:process-ao-conceive-pnrhem` | Conceive + Licensed or Regulated Agent Capacity | dea:discovery-agency-and-organization-conceive-escape | 10/10 |
| ao-design | `processes:process-ao-design-2fkvhx` | Design + Regulated Role Architecture | dea:discovery-agency-and-organization-design-escape | 10/10 |
| ao-build | `processes:process-ao-build-9my4jr` | Build + Regulated Agent Pool | dea:discovery-agency-and-organization-build-escape | 10/10 |
| ao-operate | `processes:process-ao-operate-ba8scr` | Operate + Regulated Performance Oversight | dea:discovery-agency-and-organization-operate-escape | 10/10 |
| ao-improve | `processes:process-ao-improve-qqxe4d` | Improve + Regulated Workforce Capability | dea:discovery-agency-and-organization-improve-escape | 10/10 |

### Evidence anchors (no TMForum; primary regulator rules only)

- **Banking:** FCA SMCR (CF1..CF11, SYSC 25, COCON, FIT); FINRA Rule 3110; SEC Rule 17a-3; Basel BCBS
- **Healthcare:** US state licensure registries (FSMB, Nursys, NABP, ARRT, ARDMS, NBRC); The Joint Commission credentialing-and-privileging
- **Insurance:** NAIC Producer Licensing Model Act; NMLS
- **Professional services:** UK SRA regulated-professionals regime; US state bar admissions; MCLE / CME continuing-competence regimes
- **Telecoms / aviation:** FAA Part 61/63/117; Part 121 subpart Y; EASA Part-FCL / Part-ORO
- **AI-system providers/deployers:** EU AI Act (Regulation (EU) 2024/1689) Articles 9 (risk classification), 14 (human-oversight), 26 (post-market monitoring)
- **Sanctions / AML / KYC:** OFAC SDN (31 CFR 501); Bank Secrecy Act (31 USC 5311); FinCEN AML/KYC guidance; FCRA (15 USC 1681); ADA (42 USC 12102)

### A&O regulator-tied chain (now complete end-to-end)

Conceive (CR-BP-106) -> Design (CR-BP-106) -> Build (CR-BP-106) -> **existing Activate (PR #122 / CR-BP-81: Mobilize Licensed Workforce)** -> Operate (CR-BP-106) -> Improve (CR-BP-106) -> **existing Retire (PR #114 / CR-BP-73: Conduct Regulated Workforce Wind-Down)**.

A&O is the first domain with regulator-tied coverage across all 7 stages.

## 3. Slice Mechanics

- **5 BP additions** at `entities/v1-alpha/<cell>/<cell>-<pg-hash>/<cell>-<bp-hash>/processes-process-<cell>-<bp-hash>.yaml`. Each carries `identity.verb`, `identity.object`, `trigger`, `outcome`, `evidence_links[]` (drawn from primary regulator rules), `context: [{ref: pc}]`, and `relationships: [{source_id, target_id, relationship_type: serves, target_id: ecf-coord}]`.
- **5 BP READMEs** for IDM-007 (`every entity dir has README.md`).
- **5 PG modifications** (NOT replacements) at `entities/v1-alpha/<cell>/<cell>-<pg-hash>/processes-group-<cell>-<pg-hash>.yaml`. Each existing cell-level PG keeps its substrate-neutral name and definition; the new BP is appended to `composes:` (with provenance referencing CR-BP-106) and to `canonical_processes:`; a `change_history` entry is added.
- **5 escape-discovery admission updates**: each `discovery/v1-alpha/agency-and-organization-{stage}-escape.yaml` gains an `admission:` block under `disposition:` referencing the new BP id, CR-BP-106, and `admitted_at: '2026-09-22'`.
- **PCs unchanged.** The 5 PC files at `entities/v1-alpha/<cell>/processes-pc-<cell>-<pc-hash>.yaml` are cell-level and already cover the substrate-neutral scope; the regulator-tied BP works under the same PC (same coordinate). No PC file is modified.
- **Test fixtures updated**: `tests/test_check_lifecycle_discovery.py` (23 -> 28 records + 7-stage coverage); `tests/test_check_lifecycle_state.py` (record count assertions remain at 140); `tests/test_check_l2_qualification.py` (record count assertions remain at 140); `tests/test_check_activity_model.py` (Activity + BP count assertions bumped to 560/145); `tests/test_check_task_model.py` (record count assertions remain at 2800).
- **CATALOG.yaml** regenerated: 3602 canonical / 3603 entities / 121 open_change_requests.

### NOT in scope

- **No substrate-neutral BP displacement.** The 5 existing substrate-neutral general-case BPs (ao-conceive-{e3u8s2,ruxjvh,z6m6p5}, ao-design-{34e95r,7dkbur,8fzp2b,rve8j5}, ao-build-{b38bkg,w2qurd}, ao-operate-{38qyc6,87q5mk,bd7mef,dg9q4h,g4wp63}, ao-improve-{edjyha,h3vgyf,xfh8na,xs59e2}) remain composed by their respective PGs. The regulator-tied BPs are added to the existing PGs; nothing is removed.
- **No PG replacement.** The existing PGs (Organization and Agent Conception, Organization and Role Design, Agent Acquisition and Onboarding, Agent Operations, Agent and Organization Improvement) retain their cell-level substrate-neutral names and definitions.
- **No new escape-clause discoveries.** The 5 admission tranches use the existing CR-BP-105 escape-clause recommendations; no new discovery records.
- **No specialized BP authority (BP-QUAL-011 deferred under CR-BP-92 §21).** The 5 regulator-tied BPs are admitted as management-type BPs under the existing `process_specialization: []` field; no specialized BP authorization is created.
- **No MECE-008 introduction.** The 5 new BPs are composed by their respective PGs in the same commit; no orphans are introduced. (An earlier draft introduced 18 orphan-BP findings; that draft was not pushed.)

## 4. Slice Notes

The five new BPs are admitted **alongside** the pre-existing substrate-neutral general-case BPs at each cell. The substrate-neutral BPs remain in place; the regulator-tied BP is added to the cell-level PG's `composes:` and `canonical_processes:`. No entity records are removed or displaced; no id changes; no register mutations.

The repo's existing convention for regulator-tied specialization in the same cell is demonstrated by the AO-Activate cell (PR #122 / CR-BP-81, "Mobilize Licensed Workforce") which is the sole regulator-tied admission to date. The AO-Activate cell has no substrate-neutral counterpart (it was admitted as the only PG from the start). For the 5 cells in this slice, both substrate-neutral and regulator-tied BPs coexist under the same cell-level PG; the PG's name describes the cell, not any single BP.

## 5. Conformance + Test Posture

After this slice lands:

- `python3 scripts/check_lifecycle_discovery.py` reports 28 records (23 existing + 5 new escape), 0 findings.
- `python3 scripts/check_id_system.py` reports CONFORMANT (IDM-001..007) with 3603 records checked.
- `python3 scripts/check_mece.py` reports CONFORMANT (MECE-001..008) with 0 findings.
- `python3 scripts/check_lifecycle_state.py` reports CONFORMANT (LCM-001..005) with 140 records checked.
- `python3 scripts/check_activity_model.py` reports CONFORMANT (ACT-001..010 + ACT-011..015 advisory) with 560 Activities + 145 BPs.
- `python3 scripts/check_l2_qualification.py` reports CONFORMANT (BP-C1..C4 + BP-QUAL-001..012) with 140 records checked.
- `python3 scripts/check_process_semantics.py` reports CONFORMANT (S21).
- `python3 scripts/check_task_model.py` reports CONFORMANT (TASK-001..005) with 2800 Tasks.
- `python3 scripts/conformance_result.py` reports CONFORMANT: 30 gates evaluated, 0 blocking failures, 0 advisory failures.
- Targeted pytest (233 tests across `test_check_mece`, `test_check_activity_model`, `test_check_lifecycle_state`, `test_check_l2_qualification`, `test_check_lifecycle_discovery`, `test_check_process_semantics`, `test_check_process_scope`, `test_check_l0_l1_cardinality`, `test_check_reconciliation_matrix`, `test_check_process_group_pg95`): 233/233 PASS.

## 6. Repo Changes

| Path | Change |
|---|---|
| `entities/v1-alpha/ao-conceive/ao-conceive-bwjhgd/ao-conceive-pnrhem/processes-process-ao-conceive-pnrhem.yaml` | NEW (BP) |
| `entities/v1-alpha/ao-conceive/ao-conceive-bwjhgd/ao-conceive-pnrhem/README.md` | NEW (BP README) |
| `entities/v1-alpha/ao-conceive/ao-conceive-bwjhgd/processes-group-ao-conceive-bwjhgd.yaml` | MOD (PG: +1 compose, +1 change_history) |
| `entities/v1-alpha/ao-design/ao-design-pjrfr9/ao-design-2fkvhx/...` | MOD + NEW (3 files) |
| `entities/v1-alpha/ao-design/ao-design-pjrfr9/processes-group-ao-design-pjrfr9.yaml` | MOD (PG: +1 compose, +1 change_history) |
| `entities/v1-alpha/ao-build/ao-build-m6fmyx/ao-build-9my4jr/...` | MOD + NEW (3 files) |
| `entities/v1-alpha/ao-build/ao-build-m6fmyx/processes-group-ao-build-m6fmyx.yaml` | MOD (PG: +1 compose, +1 change_history) |
| `entities/v1-alpha/ao-operate/ao-operate-35gmps/ao-operate-ba8scr/...` | MOD + NEW (3 files) |
| `entities/v1-alpha/ao-operate/ao-operate-35gmps/processes-group-ao-operate-35gmps.yaml` | MOD (PG: +1 compose, +1 change_history) |
| `entities/v1-alpha/ao-improve/ao-improve-su4c8p/ao-improve-qqxe4d/...` | MOD + NEW (3 files) |
| `entities/v1-alpha/ao-improve/ao-improve-su4c8p/processes-group-ao-improve-su4c8p.yaml` | MOD (PG: +1 compose, +1 change_history) |
| `discovery/v1-alpha/agency-and-organization-{conceive,design,build,operate,improve}-escape.yaml` | MOD (5 escape records: +admission block) |
| `tests/test_check_lifecycle_discovery.py` | MOD (record count + 7-stage coverage) |
| `tests/test_check_lifecycle_state.py` | MOD (record count assertions) |
| `tests/test_check_l2_qualification.py` | MOD (record count assertions) |
| `tests/test_check_activity_model.py` | MOD (Activity + BP count assertions) |
| `CATALOG.yaml` | MOD (regenerated; 3602 canonical / 3603 entities / 121 open_change_requests) |
| `CHANGELOG.md` | MOD (`[Unreleased]` entry added) |
| `change-requests/README.md` | MOD (CR row added) |
| `reconciliation/conformance_report.yaml` | MOD (regenerated) |

**15 entity files + 5 test files + 3 catalog/index files + 1 carrier CR = 24 files** (5 new BP yaml + 5 new BP README + 5 PG mods + 5 escape mod + 4 test mod + CATALOG + CHANGELOG + README + recon + this CR = 25 files total).

## 7. Dash Discipline

This slice introduces zero en/em-dash characters (U+2013 / U+2014) in newly authored or modified content. The 5 PC files and 5 PG files that I touched are dash-clean; the new BP yaml files and READMEs are dash-clean; the carrier CR is dash-clean. (CHANGELOG.md and change-requests/README.md have 93 and 1 pre-existing dash violations respectively; these predate this slice and are out of scope under surgical-change discipline.)

## 8. Acceptance Criteria

1. 5 new BPs + 5 BP READMEs exist (10 new files).
2. Each BP has a valid `id` matching the id-system entropy alphabet `[a-z minus i,l,o] + [2-9]`.
3. Each BP has a `context:` block with a `ref` to its parent PC.
4. Each BP has an `evidence_links[]` list of primary regulator rules (no TMForum references).
5. Each cell's existing PG has the new BP appended to `composes:` (5 PG mods, each gaining 1 compose entry).
6. Each cell's existing PG keeps its substrate-neutral name and definition (no PG rename).
7. Each cell's existing substrate-neutral BPs remain composed by their PG (no displacement; 18 existing substrate-neutral BPs preserved).
8. Each escape-discovery record carries an `admission:` block referencing the new BP id.
9. `python3 scripts/check_lifecycle_discovery.py` reports 0 findings.
10. `python3 scripts/check_id_system.py` reports 0 findings.
11. `python3 scripts/check_mece.py` reports 0 findings (no MECE-008 introduction).
12. `python3 scripts/check_lifecycle_state.py` reports 0 findings.
13. `python3 scripts/check_activity_model.py` reports 0 findings.
14. `python3 scripts/check_l2_qualification.py` reports 0 findings.
15. `python3 scripts/check_process_semantics.py` reports 0 findings.
16. `python3 scripts/check_task_model.py` reports 0 findings.
17. `python3 scripts/conformance_result.py` reports CONFORMANT (0 blocking, 0 advisory).
18. Targeted pytest (233 tests) PASS.
19. `CATALOG.yaml` regenerated; `open_change_requests: 120 -> 121`; canonical 3597 -> 3602; entities 3598 -> 3603.
20. Zero TMForum references introduced (CR-BP-TMF-EMBARGO compliance continues; zero new TMForum cites).
21. Zero en/em-dash characters introduced (dash discipline preserved).

## 9. Result

The 5 regulator-tied AgencyAndOrganization ECF cells (Conceive, Design, Build, Operate, Improve) each gain a regulator-tied Business Process admission as an additional L2 record alongside the substrate-neutral general-case BPs. A&O is now the first domain with regulator-tied coverage across all 7 stages: Conceive (regulated-scope declaration) -> Design (regulator-tied role catalogue) -> Build (regulator-ready candidate pool) -> existing Activate (PR #122 licensed-workforce mobilization) -> Operate (regulator-aligned continuing-compliance oversight) -> Improve (regulator-tied capability improvement) -> existing Retire (PR #114 regulated-workforce wind-down).

L3 Activity and L4 Task decomposition lands in **CR-BP-111** (deferred follow-on tranche).

## Cross-repo context

No cross-repo coordination required. This slice is scoped to `technehub-labs/dea-catalog-processes` only.

---

## Trigger

- Open PR, halt for `Merge` per phase-pr-slice-cadence.
- After merge, **CR-BP-111** (L3+L4 decomposition of the 5 regulator-tied BPs) is the queued next slice. CR-BP-111 can now proceed because the 5 L2 BP parents exist on `main`.