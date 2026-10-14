# CR-BP-21a.1: StrategyAndDirection Completion (ECF v2.4.0 — Register Gap Closure)

**Status**: Accepted
**Admission authority**: yes
**Layer**: Process Catalog
**Owner**: Emmanuel A. Otchere
**Date**: 2026-09-08
**Depends on**: CR-BP-19 (register v2); CR-BP-20 (alignment); CR-BP-21a (StrategyAndDirection landing); CR-BP-22 (register audit-status)
**Related**: dea-metaframework/framework/domain-grounding.md §3.2; CR-BP-21b.1..e.1 (remaining domain completion tranches, planned)

## 1. What this CR is

The first domain-completion tranche of the CR-BP-21 series. CR-BP-21a
landed the StrategyAndDirection Conceive-cell L1 group plus 1 L2 per
ratified cell; the register v3 audit (`audit_status` axis, CR-BP-22)
records the SD Design/Build/Operate/Improve cells as
`ratified-pending-landing` with `planned_tranche: CR-BP-21a.1`. This CR
closes that gap: it lands the 4 remaining SD Process Groups and the 14
remaining register v2 L2 candidates, and extends the existing
Conceive group's composes edges to the 3 new Conceive-cell L2s.

After this landing, every SD cell has its L1 Process Group and every
register v2 SD L2 candidate is landed. The SD domain is complete at
the register v2 scope.

## 2. The 4 new Process Groups (L1)

- `dea:group-strategic-choices-design` — SD x Design. Composes
  design-strategic-options (landed CR-BP-21a), evaluate-strategic-
  alternatives, design-objectives-and-targets, design-strategic-scenarios.
- `dea:group-strategic-plan-build` — SD x Build. Composes
  build-strategic-plan (landed CR-BP-21a), build-strategic-roadmap,
  translate-strategic-choices-into-initiatives,
  set-resource-allocation-priorities.
- `dea:group-strategic-steering-operation` — SD x Operate. Composes
  monitor-strategic-performance (landed CR-BP-21a),
  sense-environmental-signals, steer-initiative-portfolio,
  operate-strategic-review-cycle.
- `dea:group-strategic-adaptation` — SD x Improve. Composes
  adapt-strategic-direction (landed CR-BP-21a),
  refresh-objectives-and-targets, review-strategy-effectiveness.

The existing `dea:group-strategy-direction-conception` (Conceive)
gains composes edges to the 3 new Conceive-cell L2s
(define-enterprise-purpose-and-ambition, conceive-strategic-intent,
frame-strategic-horizons).

## 3. The 14 new L2 Business Processes

All land as `lifecycle_status: candidate`, `process_type: strategic`
(consistent with the 5 landed SD L2s; the keyword-density gate
BP-ARC-ID-004 confirms strategic-type outcome statements).

| L2 ID | Cell | process_intent | process_type |
|---|---|---|---|
| dea:process-define-enterprise-purpose-and-ambition | SD/Conceive | develop | strategic |
| dea:process-conceive-strategic-intent | SD/Conceive | develop | strategic |
| dea:process-frame-strategic-horizons | SD/Conceive | develop | strategic |
| dea:process-evaluate-strategic-alternatives | SD/Design | develop | strategic |
| dea:process-design-objectives-and-targets | SD/Design | develop | strategic |
| dea:process-design-strategic-scenarios | SD/Design | develop | strategic |
| dea:process-build-strategic-roadmap | SD/Build | develop | strategic |
| dea:process-translate-strategic-choices-into-initiatives | SD/Build | develop | strategic |
| dea:process-set-resource-allocation-priorities | SD/Build | develop | strategic |
| dea:process-sense-environmental-signals | SD/Operate | operate | strategic |
| dea:process-steer-initiative-portfolio | SD/Operate | operate | strategic |
| dea:process-operate-strategic-review-cycle | SD/Operate | operate | strategic |
| dea:process-refresh-objectives-and-targets | SD/Improve | develop | strategic |
| dea:process-review-strategy-effectiveness | SD/Improve | develop | strategic |

## 4. In-place edits to existing records

- `dea:group-strategy-direction-conception`: +3 composes edges,
  +1 change_history entry. Applied as surgical text patches; a YAML
  round-trip was rejected because it strips authored comment blocks
  and re-wraps folded scalars.
- `dea-pc-sd-{conceive,design,build,operate,improve}` contexts:
  `processes:` lists extended with the new cell L2s (PC-008), +1
  change_history entry each. Same surgical-patch rationale.

No schema, validator, or CI surface changes.

## 5. Register v3 audit impact

SD Design/Build/Operate/Improve flip from `ratified-pending-landing`
to `landed`: **19 landed / 16 ratified-pending-landing / 14
backlog-deferred**. The remaining pending cells are the non-Conceive
cells of AO, PV, OE, FA (planned CR-BP-21b.1..e.1).

## 6. What this CR does NOT do

- The other four domains' completion tranches (CR-BP-21b.1..e.1) —
  each gets its own PR.
- Activate/Retire cells — register v2 keeps these deferred.
- L2 candidates beyond register v2 (new discovery is a separate
  admission-gate flow).

## 7. Verification

- All 15 conformance gates pass (CONFORMANT).
- pytest 148 pass / 1 pre-existing failure.
- check_process_identity 0 blocking findings.
- check_process_group PG-001..008 PASS (4 new groups).
- Admission gate `--strict-provenance`: exit 0; the 18 new entries
  (14 L2s + 4 L1 groups) all carry the CR-BP-21a.1 reference.
- Register audit: OK (19 landed / 16 pending / 14 deferred).
- CATALOG.yaml `--check` OK.
