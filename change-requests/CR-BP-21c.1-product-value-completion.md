# CR-BP-21c.1: ProductAndValue Completion (ECF v2.4.0 — Register Gap Closure)

**Status**: Accepted
**Admission authority**: yes
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-08
**Depends on**: CR-BP-19 (register v2); CR-BP-20 (alignment); CR-BP-21c (ProductAndValue landing); CR-BP-21a.1 (completion-tranche pattern); CR-BP-22 (register audit-status)
**Related**: dea-metaframework/framework/domain-grounding.md §3.5; CR-BP-21d.1..e.1 (remaining completion tranches, planned)

## 1. What this CR is

The third domain-completion tranche of the CR-BP-21 series, mirroring
the CR-BP-21a.1 / 21b.1 pattern. CR-BP-21c landed the PV Conceive-cell
L1 group plus 1 L2 per ratified cell; the register v3 audit records
the PV Design/Build/Operate/Improve cells as
`ratified-pending-landing` with `planned_tranche: CR-BP-21c.1`. This
CR closes that gap: it lands the 4 remaining PV Process Groups and
the 11 remaining register v2 L2 candidates, and extends the existing
Conceive group's composes edges to the 2 new Conceive-cell L2s.

## 2. The 4 new Process Groups (L1)

- `dea:group-proposition-design` — PV x Design. Composes
  design-product-and-service-propositions (landed CR-BP-21c),
  design-packaging-and-configuration, design-innovation-experiment.
- `dea:group-product-development` — PV x Build. Composes
  develop-product-variants (landed CR-BP-21c),
  build-service-capability, build-innovation-prototype,
  prepare-market-readiness.
- `dea:group-portfolio-management-operation` — PV x Operate.
  Composes operate-product-catalogue (landed CR-BP-21c),
  manage-portfolio-performance, manage-proposition-lifecycle.
- `dea:group-product-evolution` — PV x Improve. Composes
  conduct-proposition-performance-review (landed CR-BP-21c),
  evolve-products-and-services, rationalize-portfolio.

The existing `dea:group-proposition-conception` (Conceive) gains
composes edges to the 2 new Conceive-cell L2s
(frame-portfolio-direction, frame-innovation-thesis).

## 3. The 11 new L2 Business Processes

All land as `lifecycle_status: candidate`. `process_type` follows
the cell pattern (management for Conceive/Design/Improve; core for
the Build capability/prototype processes).

| L2 ID | Cell | process_intent | process_type |
|---|---|---|---|
| dea:process-frame-portfolio-direction | PV/Conceive | develop | management |
| dea:process-frame-innovation-thesis | PV/Conceive | develop | management |
| dea:process-design-packaging-and-configuration | PV/Design | develop | management |
| dea:process-design-innovation-experiment | PV/Design | develop | management |
| dea:process-build-service-capability | PV/Build | develop | core |
| dea:process-build-innovation-prototype | PV/Build | develop | core |
| dea:process-prepare-market-readiness | PV/Build | develop | management |
| dea:process-manage-portfolio-performance | PV/Operate | operate | management |
| dea:process-manage-proposition-lifecycle | PV/Operate | operate | management |
| dea:process-evolve-products-and-services | PV/Improve | develop | management |
| dea:process-rationalize-portfolio | PV/Improve | develop | management |

## 4. In-place edits to existing records

- `dea:group-proposition-conception`: +2 composes edges, +1
  change_history entry (surgical text patches, per the CR-BP-21a.1
  precedent).
- `dea-pc-pv-{conceive,design,build,operate,improve}` contexts:
  `processes:` lists extended (PC-008), +1 change_history entry each.

No schema, validator, or CI surface changes.

## 5. Register v3 audit impact

PV Design/Build/Operate/Improve flip from `ratified-pending-landing`
to `landed`: **27 landed / 8 ratified-pending-landing / 14
backlog-deferred**. The remaining pending cells are the non-Conceive
cells of OE and FA (planned CR-BP-21d.1 and CR-BP-21e.1).

## 6. What this CR does NOT do

- The other two domains' completion tranches (CR-BP-21d.1, 21e.1) —
  each gets its own PR.
- Activate/Retire cells — register v2 keeps these deferred.
- L2 candidates beyond register v2 (new discovery is a separate
  admission-gate flow).

## 7. Verification

- All 15 conformance gates pass (CONFORMANT).
- pytest 148 pass / 1 pre-existing failure.
- check_process_identity 0 blocking findings.
- check_process_group PG-001..008 PASS (4 new groups).
- Admission gate `--strict-provenance`: exit 0.
- Register audit: OK (27 landed / 8 pending / 14 deferred).
- CATALOG.yaml `--check` OK.
