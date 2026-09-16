# CR-BP-80 - L0 Escape-Clause Discovery Exercise for the Five Backlog-Deferred Cells

**Status**: Proposed
**Layer**: L0
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-16
**Carrier**: Fifth discovery-driven escape-clause exercise under the CR-BP-62 method; targets the five ECF cells still backlog-deferred after CR-BP-63 (Activate/Retire first-pass exercise) and the four subsequent cell flips (CR-BP-71/-73/-75/-78).
**Depends on**: CR-BP-19 (register v2 deferral normalization); CR-BP-62 (discovery method, BP-LIFE-001..015 test battery); CR-BP-63 (first Activate/Retire discovery exercise); CR-ECF-001..008 (framework axiom-derivation, domain grounding, lifecycle grounding, orthogonality).
**Lands against**: 18 discovery records (after this slice; +5); 1 carrier CR; 1 README row; 5 baseline records preserved; ECF cell semantics per `dea-metaframework/framework/matrix.md`; 24-gate suite still CONFORMANT.

---

## 1. Change Request

Re-evaluate, under the CR-BP-62 escape-clause method, the five ECF cells whose disposition remained `backlog-deferred` after CR-BP-63 and the four subsequent cell-flip tranches (CR-BP-71 P&R Activate, CR-BP-73 A&O Retire, CR-BP-75 F&A Retire, CR-BP-78 G&E Retire). Each cell receives one new escape-clause record at `discovery/v1-alpha/<domain>-<stage>-escape.yaml` testing one regulated-sector candidate per the established escape pattern (the precedent for the four successful flips was: a candidate BP that arises from a regulator- or court-mandated context distinct from the general cell-typical work).

The five backlog-deferred cells and their escape hypotheses are:

| Cell | Framework's typical work (matrix.md) | Escape hypothesis (2026-era evidence) | Predicted disposition |
|---|---|---|---|
| StrategyAndDirection/Activate | "Launch direction" | "Institutionalize Strategic Plan in Regulated Sector" (Basel ICAAP/SAA approval, NHS trust 5-year strategy approval, utilities rate-case strategic plan filing, bank recovery and resolution plan activation) | ADMIT-CANONICAL (score 8-9) |
| StrategyAndDirection/Retire | "Strategic renewal" | "Sunset Strategic Plan Under Regulatory Mandate" (failed stress test triggers plan replacement, bank recovery plan directive, regulator-ordered strategic plan retraction) | ADMIT-CANONICAL (score 7-8) or DEFER |
| AgencyAndOrganization/Activate | "Mobilize" | "Mobilize Licensed or Regulated Workforce" (banking licensed roles, healthcare credentialing, licensed professional services, telco licensed engineers, aviation crew licensing) | ADMIT-CANONICAL (score 8-9) |
| EnablementAndOperations/Activate | "Cut-over" | "Activate Operations Capability Under Regulatory Authorization" (AOC issue, payments-license activation, manufacturing GMP certification, bank operational risk authorization, telco operations license activation) | ADMIT-CANONICAL (score 8-9) |
| FinanceAndAccounting/Activate | "Billing activation" | "Activate Billing Capability Under Regulatory Framework" (insurance statutory accounting activation, IFRS 17 transition to active, bank treasury activation under capital rules, utility rate-effective billing activation) | ADMIT-CANONICAL (score 8-9) |

Per the established escape-pattern precedent (CR-BP-70/-72/-74/-76), each record is evaluated against the full BP-LIFE-001..015 battery; scoring uses the canonical five-axis rubric (process_reality + semantic_stability + cross_domain_applicability + boundary_clarity + evidence_strength); disposition is one of ADMIT-CANONICAL / RECORD-PATTERN / MERGE / RECLASSIFY / DEFER / process_empty.

## 2. Slice Mechanics

- **Five new escape-clause records** at `discovery/v1-alpha/<domain>-<stage>-escape.yaml`, each with one regulated-sector candidate. Records follow the precedent shape (`party-and-relationship-activate-escape.yaml`); same schema constraints; same evaluation battery.
- **Baseline records preserved** at `discovery/v1-alpha/<domain>-<stage>.yaml` (the v1 CR-BP-63 evaluations stay as the cell's evidence base for non-regulated candidates).
- **Register cells remain `backlog-deferred`** at this point; any flip to `ratified-accepted` or `landed` happens only when the escape record lands a canonical-admission tranche (separate follow-on slices: CR-BP-81..83 admission tranches, then CR-BP-84..85 L3 decomposition tranches).
- **Carrier CR + README row** at `change-requests/CR-BP-80-l0-discovery-five-backlog-cells.md` (this file); README row inserted before the `## Cross-repo context` anchor.

## 3. Gate Posture

After this slice:

- `python3 scripts/check_lifecycle_discovery.py` reports 23 records checked (18 baseline + 5 new escape), 0 findings.
- All 14 baseline + 5 escape records schema-valid (DISC-001); all `evaluation` blocks carry the 14 fields including `ecf_independence` (not `ecf_conf`); `evidence.evidence_strength` present on every candidate; `evidence.sources` items are strings (not objects).
- 24-gate `conformance_result.py` suite CONFORMANT, 0 blocking, 0 advisory.
- CR-META 0 NEW findings (pre-existing legacy unchanged).
- CATALOG regenerated; `open_change_requests` 91 -> 92.

## 4. Repo Changes

| Path | Change |
|---|---|
| `discovery/v1-alpha/strategy-and-direction-activate-escape.yaml` | NEW (SD.Activate escape: Institutionalize Strategic Plan in Regulated Sector) |
| `discovery/v1-alpha/strategy-and-direction-retire-escape.yaml` | NEW (SD.Retire escape: Sunset Strategic Plan Under Regulatory Mandate) |
| `discovery/v1-alpha/agency-and-organization-activate-escape.yaml` | NEW (AO.Activate escape: Mobilize Licensed or Regulated Workforce) |
| `discovery/v1-alpha/enablement-and-operations-activate-escape.yaml` | NEW (EO.Activate escape: Activate Operations Capability Under Regulatory Authorization) |
| `discovery/v1-alpha/finance-and-accounting-activate-escape.yaml` | NEW (FA.Activate escape: Activate Billing Capability Under Regulatory Framework) |
| `change-requests/CR-BP-80-l0-discovery-five-backlog-cells.md` | NEW (this file) |
| `change-requests/README.md` | MOD (CR-BP-80 row) |
| `CATALOG.yaml` | MOD (regenerated; `open_change_requests` 91 -> 92; discovery-record count 18 -> 23) |

## 5. NOT-List (Out of Scope)

- **No canonical admission.** Escape records recommend; admission lands through separate governed contribution flow CRs (CR-BP-81 AO.Activate, CR-BP-82 EO.Activate, CR-BP-83 FA.Activate, plus L3 decomposition follow-ons).
- **No register mutation.** L1 register cells stay `backlog-deferred` until escape-flipped cells land their admission tranche.
- **No new L1/L2/L3 records.** This slice is discovery-only; PC + PG + BP + Activity records land in separate admission tranches.
- **No specialization authorization.** No ADMIT-SPECIALIZATION disposition; specialization remains unauthorized per program governance (CR-BP-62 §30).
- **No SD.Act / SD.Ret full L1-L3 stack.** If SD.Act and/or SD.Ret flip ADMIT-CANONICAL in this slice, their admission + L3 tranches are follow-on slices triggered after this discovery slice lands (per the user's established slice-cadence doctrine; one combined PR for escape records, separate per-cell admission PRs).

## 6. Acceptance Criteria

1. 5 escape-clause records exist, one per backlog-deferred cell, all schema-valid (DISC-001).
2. Each record tests exactly one regulated-sector escape candidate against BP-LIFE-001..015.
3. Each record's scoring uses the canonical five-axis rubric; disposition is one of the six standard dispositions.
4. `python3 scripts/check_lifecycle_discovery.py` reports 23 records checked (18 baseline + 5 new), 0 findings.
5. Full pytest suite passes; `scripts/conformance_result.py` remains CONFORMANT (24 gates).
6. `python3 scripts/check_cr_metadata.py` reports 0 new findings.
7. CATALOG.yaml current after regen; `open_change_requests` 91 -> 92.
8. No entity record modified; baseline records preserved unchanged.

## 7. Result

The five remaining backlog-deferred cells each receive an evidence-backed escape-clause evaluation per the established CR-BP-62 method. Predictions (to be validated by the record): SD.Activate, AO.Activate, EO.Activate, FA.Activate are likely ADMIT-CANONICAL candidates (regulated-sector pattern matches the four prior successful escape flips); SD.Retire is likely DEFER or RECORD-PATTERN (the regulated-retire evidence is thinner; this may stay `backlog-deferred`).

Program posture after this slice lands: the L0 discovery method has been applied to every one of the 49 ECF cells. Cells that flipped ADMIT-CANONICAL move to admission tranches; cells that remained DEFER or RECORD-PATTERN are documented as evidence-based outcomes (not deferred by stage-semantics doctrine). The L0 layer is then stabilized pending any future escape-clause evidence.