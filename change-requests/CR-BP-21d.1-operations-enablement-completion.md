# CR-BP-21d.1: EnablementAndOperations Completion (ECF v2.4.0 — Register Gap Closure)

**Status**: Accepted
**Admission authority**: yes
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-08
**Depends on**: CR-BP-19 (register v2); CR-BP-20 (alignment); CR-BP-21d (EnablementAndOperations landing); CR-BP-21a.1 (completion-tranche pattern); CR-BP-22 (register audit-status)
**Related**: dea-metaframework/framework/domain-grounding.md §3.6; CR-BP-21e.1 (final completion tranche, planned)

## 1. What this CR is

The fourth domain-completion tranche of the CR-BP-21 series — the
largest of the five, reflecting OE's position as the execution core
of the framework. CR-BP-21d landed the OE Conceive-cell L1 group
plus 1 L2 per ratified cell; the register v3 audit records the OE
Design/Build/Operate/Improve cells as `ratified-pending-landing` with
`planned_tranche: CR-BP-21d.1`. This CR closes that gap: it lands the
4 remaining OE Process Groups and the 23 remaining register v2 L2
candidates (Conceive 3, Design 4, Build 4, Operate 8, Improve 4),
and extends the existing Conceive group's composes edges to the 3
new Conceive-cell L2s.

## 2. The 4 new Process Groups (L1)

- `dea:group-process-and-enablement-design` — OE x Design. Composes
  design-operations-model (landed CR-BP-21d) + design-delivery-model,
  design-technology-platform-architecture,
  design-facility-and-asset-blueprint, design-logistics-and-routing.
- `dea:group-operations-and-enablement-build` — OE x Build. Composes
  build-delivery-capability (landed CR-BP-21d) +
  stand-up-production-line, build-logistics-network,
  acquire-and-install-technology-assets, acquire-and-provision-facilities.
- `dea:group-execution-and-fulfillment` — OE x Operate. Composes
  operate-service-delivery (landed CR-BP-21d) + run-production-line,
  operate-logistics, operate-warehouse-and-inventory,
  operate-quality-control, operate-technology-platforms,
  operate-facility-management, operate-asset-maintenance,
  operate-procurement-cycle.
- `dea:group-operations-and-enablement-improvement` — OE x Improve.
  Composes conduct-operations-performance-review (landed CR-BP-21d) +
  conduct-logistics-optimization, conduct-lean-six-sigma-programme,
  optimize-asset-utilization, improve-technology-platforms.

The existing `dea:group-operations-model-conception` (Conceive) gains
composes edges to the 3 new Conceive-cell L2s
(frame-delivery-model-conception, frame-technology-enablement-approach,
frame-physical-asset-approach).

## 3. The 23 new L2 Business Processes

All land as `lifecycle_status: candidate`. `process_type` follows
the cell pattern (management for Conceive/Design/Improve; core for
Build/Operate, except improve-technology-platforms which is
standardization per the BP-ARC-ID-004 keyword-density gate — the
outcome statement centres on "improve").

| L2 ID | Cell | process_intent | process_type |
|---|---|---|---|
| dea:process-frame-delivery-model-conception | OE/Conceive | develop | management |
| dea:process-frame-technology-enablement-approach | OE/Conceive | develop | management |
| dea:process-frame-physical-asset-approach | OE/Conceive | develop | management |
| dea:process-design-delivery-model | OE/Design | develop | management |
| dea:process-design-technology-platform-architecture | OE/Design | develop | management |
| dea:process-design-facility-and-asset-blueprint | OE/Design | develop | management |
| dea:process-design-logistics-and-routing | OE/Design | develop | management |
| dea:process-commission-production-line | OE/Build | develop | core |
| dea:process-build-logistics-network | OE/Build | develop | core |
| dea:process-acquire-technology-assets | OE/Build | develop | core |
| dea:process-provision-facilities | OE/Build | develop | core |
| dea:process-run-production-line | OE/Operate | operate | core |
| dea:process-operate-logistics | OE/Operate | operate | core |
| dea:process-operate-warehouse-and-inventory | OE/Operate | operate | core |
| dea:process-operate-quality-control | OE/Operate | operate | core |
| dea:process-operate-technology-platforms | OE/Operate | operate | core |
| dea:process-operate-facility-management | OE/Operate | operate | core |
| dea:process-operate-asset-maintenance | OE/Operate | operate | core |
| dea:process-operate-procurement-cycle | OE/Operate | operate | core |
| dea:process-conduct-logistics-optimization | OE/Improve | develop | management |
| dea:process-conduct-lean-six-sigma-programme | OE/Improve | develop | management |
| dea:process-optimize-asset-utilization | OE/Improve | develop | management |
| dea:process-improve-technology-platforms | OE/Improve | develop | standardization |

## 4. In-place edits to existing records

- `dea:group-operations-model-conception`: +3 composes edges, +1
  change_history entry (surgical text patches, per the CR-BP-21a.1
  precedent).
- `dea-pc-oe-{conceive,design,build,operate,improve}` contexts:
  `processes:` lists extended (PC-008), +1 change_history entry each.

No schema, validator, or CI surface changes, except one gate-UX fix:
`check_admission_gate.py` now prints a per-rule finding-count
breakdown before the truncated first-10 window, so specific ADM codes
remain greppable when one rule class saturates the window. This was
surfaced by this tranche's alphabetically-early records pushing the
fixture-test finding out of the window.

## 4a. Naming notes (identity schema conformance)

Three register v2 candidates are renamed to satisfy the identity
schema verb pattern (`^[A-Z][a-z]+$`, single TitleCase word; the name
must equal `<verb> <object>` per BP-ARC-ID-001):

- "Stand up production line" → `dea:process-commission-production-line`
  (verb Commission)
- "Acquire and install technology assets" →
  `dea:process-acquire-technology-assets` (verb Acquire)
- "Acquire and provision facilities" → `dea:process-provision-facilities`
  (verb Provision)

Precedent: CR-BP-21b renamed "Source and recruit human talent" →
"Acquire Agents" under the same substrate-neutral naming discipline.

## 5. Register v3 audit impact

OE Design/Build/Operate/Improve flip from `ratified-pending-landing`
to `landed`: **31 landed / 4 ratified-pending-landing / 14
backlog-deferred**. The only remaining pending cells are the
FinanceAndAccounting non-Conceive cells (planned CR-BP-21e.1).

## 6. What this CR does NOT do

- CR-BP-21e.1 (FinanceAndAccounting completion) — its own PR.
- Activate/Retire cells — register v2 keeps these deferred.
- L2 candidates beyond register v2 (new discovery is a separate
  admission-gate flow).

## 7. Verification

- All 15 conformance gates pass (CONFORMANT).
- pytest 148 pass / 1 pre-existing failure.
- check_process_identity 0 blocking findings.
- check_process_group PG-001..008 PASS (4 new groups).
- Admission gate `--strict-provenance`: exit 0.
- Register audit: OK (31 landed / 4 pending / 14 deferred).
- Consumer drift detector (dea-metamodel): 0 hard failures.
- CATALOG.yaml `--check` OK.
