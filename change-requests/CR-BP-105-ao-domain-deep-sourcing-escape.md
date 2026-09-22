# CR-BP-105: AgencyAndOrganization Domain-Deep Sourcing Tranche — Escape-Clause Discovery for Conceive/Design/Build/Operate/Improve

**Status**: Proposed
**Layer**: Process Catalog (lifecycle discovery + L1 sourcing)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-22
**Parent doctrine**: CR-BP-62 (lifecycle process discovery method, BP-LIFE-001..015 test battery, DISC-001..008 advisory gate); CR-BP-80 (L0 escape-clause discovery for the five backlog-deferred cells); CR-BP-81 (AO.Activate escape admission, Mobilize Licensed Workforce); CR-BP-114 (AO.Retire escape admission, Conduct Regulated Workforce Wind-Down).
**Carrier**: Discovery-only slice. Produces 5 escape-clause discovery records (one per ECF cell) evaluating a regulator-tied agent-capacity candidate under the CR-BP-62 method. Lands zero new entity records, zero id changes, zero register mutations, zero count assertion moves. Five recommended ADMIT-CANONICAL dispositions; admission lands through separate per-cell tranches gated on this slice.
**Lands against**: 28 discovery records at `discovery/v1-alpha/` (23 baseline + 5 new escape); 25 conformance gates (10 blocking + 15 advisory); gate [19] Lifecycle Discovery CONFORMANT; 7 ECF cells at full L0-L3 coverage (unchanged); 132+ canonical BP records (unchanged); 521 Activities (unchanged).

---

## 1. Change Request

Apply the CR-BP-62 escape-clause method to the five unsourced AgencyAndOrganization ECF cells that have not yet been evaluated for regulated-sector escape variants beyond their existing substrate-neutral general-case BPs:

- `ao-conceive` — Conceive
- `ao-design` — Design
- `ao-build` — Build
- `ao-operate` — Operate
- `ao-improve` — Improve

For each cell, evaluate one regulator-tied candidate (the regulated-scope / regulator-tied / regulator-aligned specialization of the cell's general-case work) against BP-LIFE-001..015. Each record tests whether the regulator-tied variant is a distinct, evidence-authoritative, boundary-clear transformation that warrants its own canonical Business Process admission separate from the existing substrate-neutral general-case BP.

**Why AO now.** The Activate and Retire cells of AgencyAndOrganization already have regulated-escape variants admitted: AO.Activate `Mobilize Licensed Workforce` (PR #122 / CR-BP-81) and AO.Retire `Conduct Regulated Workforce Wind-Down` (PR #114 / CR-BP-73). The intervening five stages (Conceive, Design, Build, Operate, Improve) have only the substrate-neutral general-case BP per cell. The domain-deep sourcing pattern under Option C of the sourcing programme is to evaluate each cell for the regulator-tied specialization that naturally bridges between the upstream Activate licensed-workforce mobilization and the downstream Retire regulated-workforce wind-down.

**Why domain-deep, not stage-by-stage.** Per the user's programme doctrine (2026-09-22 directive, Option C), the A&O domain is the highest-leverage target for sourcing because (1) it is the most regulation-rich of the seven ECF domains — five of the seven catalog-wide escape recommendations to date came from A&O-adjacent territory; (2) domain-deep sourcing produces the cleanest learning per record because each cell's regulator-tied variant pairs naturally with the upstream Activate and downstream Retire escape admissions; and (3) the alternative — stage-by-stage (Conceive first across all domains, then Design, then Build, etc.) — fragments the regulated-scope storyline across cell boundaries and requires re-discovery at every stage.

## 2. The five regulator-tied candidates

Each candidate is a regulator-tied specialization of the cell's general-case work, with cited evidence drawn from the regulator's primary rules (FCA SMCR and Handbook SYSC 25, FINRA Rule 3110, FAA Part 117 / Part 121 subpart Y, EASA Part-FCL / Part-ORO, NAIC Producer Licensing Model Act, NMLS, EU AI Act Regulation (EU) 2024/1689 Articles 9 and 14, US state healthcare licensure regimes, US state bar admissions and MCLE regimes, OFAC Sanctions / 31 CFR 501, US Bank Secrecy Act / FinCEN AML guidance, US FCRA / EEOC / ADA, The Joint Commission credentialing-and-privileging standards).

| Cell | Candidate | Verb + Object | Evidence anchor (excerpts) | Predicted disposition |
|---|---|---|---|---|
| ao-conceive | Conceive Licensed or Regulated Agent Capacity | Conceive + Licensed or Regulated Agent Capacity | FCA SMCR CF1..CF11; state healthcare licensure scopes; EU AI Act Art. 9 risk classification; US state bar admissions | ADMIT-CANONICAL (10/10) |
| ao-design | Design Regulated Role Architecture | Design + Regulated Role Architecture | FCA SMCR SYSC 25 Annex 1; FAA Part 121 subpart Y CRM; EU AI Act Art. 14 human-oversight roles; The Joint Commission credentialing-and-privileging standards | ADMIT-CANONICAL (10/10) |
| ao-build | Build Regulated Agent Pool | Build + Regulated Agent Pool | FCA Financial Services Register; NMLS / NAIC Producer Database; FAA airmen certification database; OFAC SDN screening per 31 CFR 501; Bank Secrecy Act per 31 USC 5311; FCRA per 15 USC 1681; ADA per 42 USC 12102 | ADMIT-CANONICAL (10/10) |
| ao-operate | Operate Regulated Performance Oversight | Operate + Regulated Performance Oversight | FCA SMCR Conduct Rules (COCON); FINRA Rule 3110; FAA Part 117; state bar MCLE; state healthcare CME; NAIC CE; EU AI Act Art. 14 continuing-oversight | ADMIT-CANONICAL (10/10) |
| ao-improve | Improve Regulated Workforce Capability | Improve + Regulated Workforce Capability | FCA SMCR fit-and-proper annual assessment (FCA Handbook SYSC 25 / FIT); state bar MCLE; state healthcare CME; NAIC CE; FAA Part 121 subpart Y recurrent training; EU AI Act Art. 14 ongoing training | ADMIT-CANONICAL (10/10) |

Each record tests exactly one candidate against BP-LIFE-001..015, scores on the canonical five-axis rubric (process_reality + semantic_stability + cross_domain_applicability + boundary_clarity + evidence_strength), and records one ADMIT-CANONICAL disposition. The records follow the precedent shape (`agency-and-organization-activate-escape.yaml`); same schema constraints; same evaluation battery.

## 3. Slice Mechanics

- **Five new escape-clause records** at `discovery/v1-alpha/agency-and-organization-{conceive,design,build,operate,improve}-escape.yaml`, each with one regulator-tied candidate.
- **Baseline records preserved** at `discovery/v1-alpha/agency-and-organization-{conceive,design,build,operate,improve}.yaml` — these records do not yet exist (the five cells have not been evaluated for non-regulated candidates), but the substrate-neutral general-case BP at each cell is preserved and continues to be the canonical record for the general case.
- **Register cells remain `ratified-accepted` (general case)** at this point; any flip from "general case only" to "general + regulator-tied" happens only when the escape record lands its canonical-admission tranche (separate follow-on slices).
- **Carrier CR + README row** at `change-requests/CR-BP-105-ao-domain-deep-sourcing-escape.md` (this file); README row inserted before the Cross-repo context anchor.
- **CHANGELOG.md [Unreleased] entry** added.

## 4. Gate Posture

After this slice lands:

- `python3 scripts/check_lifecycle_discovery.py --strict` reports 28 records checked (23 existing + 5 new), 0 findings.
- All 28 records schema-valid (DISC-001); all `evaluation` blocks carry the 14 fields including `ecf_independence` (not `ecf_conf`); `evidence.evidence_strength` present on every candidate; `evidence.sources` items are strings (not objects).
- 25-gate `conformance_result.py` suite CONFORMANT (10 blocking + 15 advisory).
- `CATALOG.yaml` regenerated; `open_change_requests` 119 -> 120.

## 5. Repo Changes

| Path | Change |
|---|---|
| `discovery/v1-alpha/agency-and-organization-conceive-escape.yaml` | NEW (AO.Conceive escape: Conceive Licensed or Regulated Agent Capacity) |
| `discovery/v1-alpha/agency-and-organization-design-escape.yaml` | NEW (AO.Design escape: Design Regulated Role Architecture) |
| `discovery/v1-alpha/agency-and-organization-build-escape.yaml` | NEW (AO.Build escape: Build Regulated Agent Pool) |
| `discovery/v1-alpha/agency-and-organization-operate-escape.yaml` | NEW (AO.Operate escape: Operate Regulated Performance Oversight) |
| `discovery/v1-alpha/agency-and-organization-improve-escape.yaml` | NEW (AO.Improve escape: Improve Regulated Workforce Capability) |
| `change-requests/CR-BP-105-ao-domain-deep-sourcing-escape.md` | NEW (this file) |
| `change-requests/README.md` | MOD (CR-BP-105 row inserted before Cross-repo context anchor) |
| `CHANGELOG.md` | MOD (CR-BP-105 [Unreleased] entry) |
| `CATALOG.yaml` | MOD (regenerated; `open_change_requests` 119 -> 120) |

## 6. NOT-List (Out of Scope)

- **No canonical admission.** Escape records recommend; admission lands through separate governed contribution flow CRs (CR-BP-106..110 per-cell admission tranches, each landing a full PC + PG + BP stack).
- **No register mutation.** Existing general-case BPs at the five cells remain the canonical representation of the general case; no displacement.
- **No new L1/L2/L3 records.** This slice is discovery-only; PC + PG + BP + Activity records land in separate admission tranches.
- **No specialization authorization.** No ADMIT-SPECIALIZATION disposition; specialization remains unauthorized per program governance (CR-BP-62 section 30).
- **No AI Act-specific carve-out.** The EU AI Act (Regulation (EU) 2024/1689) is referenced as one of the cited regulators for high-risk AI-system providers and deployers, but this slice does not open a separate AI-system agent governance track — that track lands in a separate CR under the dea-catalog-organizational-units or dea-metamodel repo where the AI-system substrate-neutral kernel is owned.

## 7. Acceptance Criteria

1. 5 escape-clause records exist, one per AO cell, all schema-valid (DISC-001).
2. Each record tests exactly one regulator-tied candidate against BP-LIFE-001..015.
3. Each record's scoring uses the canonical five-axis rubric; disposition is ADMIT-CANONICAL (10/10).
4. `python3 scripts/check_lifecycle_discovery.py --strict` reports 28 records checked, 0 findings.
5. Full pytest suite passes; `scripts/conformance_result.py` remains CONFORMANT (25 gates).
6. `python3 scripts/check_cr_metadata.py` reports 0 new findings.
7. `CATALOG.yaml` regenerated; `open_change_requests` 119 -> 120.
8. No entity record modified; no id changes.
9. Each record's evidence.sources references primary regulator rules or guidance (not vendor SDO catalogues).
10. Zero TMForum references introduced (CR-BP-TMF-EMBARGO compliance continues; no new TMForum cites).

## 8. Result

The five unsourced AgencyAndOrganization ECF cells each receive an evidence-backed escape-clause evaluation per the CR-BP-62 method. All five recommend ADMIT-CANONICAL. The five regulator-tied candidates complete the upstream + downstream chain for A&O domain-deep sourcing: Conceive (regulated-scope declaration) -> Design (regulator-tied role catalogue) -> Build (regulator-ready candidate pool) -> existing Activate (PR #122 licensed-workforce mobilization) -> Operate (regulator-aligned continuing-compliance oversight) -> Improve (regulator-tied capability improvement) -> existing Retire (PR #114 regulated-workforce wind-down).

Program posture after this slice lands: the L0 discovery method has been applied to every one of the 49 ECF cells (CR-BP-63 + CR-BP-70 + CR-BP-72 + CR-BP-74 + CR-BP-76 + CR-BP-80 + this slice), and the AO domain is the first domain with an end-to-end regulator-tied candidate chain from Conceive to Retire. Admission tranches (CR-BP-106..110, one per cell) gate on this discovery slice landing.

---

## Cross-repo context

This slice is dea-catalog-processes-local. The A&O regulator-tied candidate chain may surface cross-repo interactions with the dea-catalog-organizational-units repo (for the regulated personnel record) and the dea-metamodel repo (for AI-system agent governance substrates); these cross-repo integrations land in separate follow-on CRs as the admission tranches unfold.
