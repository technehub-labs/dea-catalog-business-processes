# CR-BP-21a: StrategyAndDirection Landing (ECF v2.4.0 — First Unadmitted Domain)

**Status**: Accepted
**Admission authority**: yes
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-07
**Depends on**: CR-BP-19 (register v2); CR-BP-20 (alignment; Option A split); CR-BP-13a/b (admission tranches, prior)
**Related**: dea-metaframework framework/domain-grounding.md §3.2; CR-BP-21b..e (remaining 4 unadmitted domains, planned)

## 1. What this CR is

The first landing tranche of the CR-BP-21 series, one per unadmitted v2.4.0
domain. Lands StrategyAndDirection against the rediscovered register v2 cells
(Conceive / Design / Build / Operate / Improve; Activate/Retire are deferred
register-wide per CR-BP-19). Executes the planned migration of
`dea:process-develop-governance-strategy` (marked `status: planned` in
CR-BP-20) from GovernanceAndExistence × Conceive to
StrategyAndDirection × Conceive — the migration is renamed
`dea:process-develop-corporate-strategy` per the register v2 L2 candidate list.

## 2. The 5 process contexts

- `dea:pc-sd-conceive` — Purpose and Ambition Conception
- `dea:pc-sd-design` — Strategic Choices Design
- `dea:pc-sd-build` — Strategic Plan Build
- `dea:pc-sd-operate` — Strategic Steering Operation
- `dea:pc-sd-improve` — Strategic Adaptation

The Activate/Retire cells (per register v2) remain deferred at the
research-register level; the Process Context files for those stages are
NOT created in this CR (consistency with the register's disposition
rationale). They would land only if a sector example requires a stable
Activate/Retire process identity (see CR-BP-19 deferred_rationale).

## 3. The 1 Process Group (L1)

- `dea:group-strategy-direction-conception` — Process Group for
  StrategyAndDirection × Conceive. Composes the 4 L2s of the
  Conceive cell (purpose, strategic intent, strategic horizons, corporate
  strategy). This is the receiving group for the migrated L2
  `dea:process-develop-corporate-strategy` (formerly
  `dea:process-develop-governance-strategy` in GE-Conceive).

  Naming note: the v2.4.0 L1 group covers the full Conceive cell
  (Purpose, Intent, Horizons, Corporate Strategy), not strategy-conception
  alone. The id is `dea:group-strategy-direction-conception` to match the
  domain (per CR-BP-12 §4: group id is domain-scoped, not
  cell-component-scoped). This matches the BC catalog's strategy-cluster
  grouping precedent (`dea:group-customer-strategy-conception` followed
  the same pattern).

## 4. The 5 L2 Business Processes

One L2 per ratified cell. Per the user's CR-BP-19 guidance
("lifecycle_status: candidate" until end-to-end MECE validation in a
follow-up admission tranche), all land as candidates:

| L2 ID | Cell | process_intent | process_type | process_specialization |
|---|---|---|---|---|
| dea:process-develop-corporate-strategy | SD/Conceive | develop | management | strategy |
| dea:process-design-strategic-options | SD/Design | develop | management | strategy |
| dea:process-build-strategic-plan | SD/Build | develop | management | strategy |
| dea:process-monitor-strategic-performance | SD/Operate | operate | core | strategy |
| dea:process-adapt-strategic-direction | SD/Improve | develop | management | strategy |

The 4-L2 Conceive cell (Purpose, Intent, Horizons, Corporate Strategy)
initially has only 1 L2 landing here (the migration target).
The remaining 3 are recorded as a follow-up tranche (CR-BP-21a.1)
when richer registry material is available. The 4-L2 Design cell
(Options, Alternatives, Objectives, Scenarios) lands 1 L2 (Strategic
Options) and the others in CR-BP-21a.1.

## 5. The L2 migration (Option A split execution)

- `dea:process-develop-governance-strategy` (GE × Conceive; status:
  planned under CR-BP-20) becomes `dea:process-develop-corporate-strategy`
  in SD × Conceive. New id, new context, new composition.
- The previous L2 entry is marked `status: migrated` in change_history
  and `lifecycle_status: deprecated`; its `dea:group-governance-conception`
  composes edge (status: planned) is removed.
- The new L2 lands with `lifecycle_status: candidate`, fresh
  change_history entries, the new id, the new `part_of` / `serves`
  relationship toward `dea:pc-sd-conceive` /
  `ecf:strategyAndDirection.conceive`.
- A new READMEs is created at the previous directory's location as a
  redirect pointer (`dea:process-develop-governance-strategy/README.md`)
  referencing the new id, so any external link survives with a clear
  deprecation note.

## 6. Provenance + classification (per the landed-population pattern)

- `lifecycle_status: candidate` for all 5 L2s and the 1 L1 group.
- `process_intent` / `process_type` from the canonical vocabularies
  (CR-BP-14 §10, classifications/process-types.yaml,
  classifications/process-intents.yaml).
- `process_specialization: strategy` (per CR-BP-19 register; consistent
  with the BC catalog's `capability-strategy` specialization).
- `metadata.change_history` carries the CR-BP-21a entry on every entry
  with a phase-7 marker, a `cr: CR-BP-21a`, the date, and the rationale
  (grounds the change in domain-grounding.md §3.2).
- `metadata.cross_context_overlap: []` (no cross-cell overlap; MECE
  for the SD cells is verified in the register v2).

## 7. What this CR does NOT do

- The remaining 4 unadmitted v2.4.0 domains (AgencyAndOrganization,
  ProductAndValue, EnablementAndOperations, FinanceAndAccounting) —
  each gets its own CR-BP-21b..e landing tranche.
- The remaining 3 L2s of the SD/Conceive cell (Purpose, Intent, Horizons)
  and 3 of the SD/Design cell (Alternatives, Objectives, Scenarios) —
  follow-up CR-BP-21a.1 when more L2 material is ready.
- SD/Activate and SD/Retire cells — register v2 keeps these deferred.
- Cross-repo BC capability-strategy re-affiliation from
  governance-existence to strategy-direction — out of scope here
  (will require a CR-DEA-BC-08 / CR-BC-STRUCT-10 follow-up in
  dea-catalog-business-capabilities; called out as related work).

## 8. Verification

- All 15 conformance gates pass (CONFORMANT).
- pytest 148 pass / 1 pre-existing failure.
- check_process_identity 0 outcome_mismatch findings.
- CR-META `--strict-provenance`: 0 new findings; CR-BP-21a
  change_history entries are read at `metadata.change_history`.
- Admission gate `--strict-provenance`: exit 0; the 6 new entries
  (5 L2s + 1 L1 group) all carry the CR-BP-21a reference.
- Fresh-clone reproduction (with `git remote set-url origin ...git`
  normalization per `.github/workflows/ci.yml`):
  `python scripts/regenerate_catalog.py --check` OK.
