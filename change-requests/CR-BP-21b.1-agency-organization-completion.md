# CR-BP-21b.1: AgencyAndOrganization Completion (ECF v2.4.0 — Register Gap Closure)

**Status**: Accepted
**Admission authority**: yes
**Layer**: Process Catalog
**Owner**: Emmanuel A. Otchere
**Date**: 2026-09-08
**Depends on**: CR-BP-19 (register v2); CR-BP-20 (alignment); CR-BP-21b (AgencyAndOrganization landing); CR-BP-21a.1 (completion-tranche pattern); CR-BP-22 (register audit-status)
**Related**: dea-metaframework/framework/domain-grounding.md §3.3; ADR-ECF-002 §5 (substrate independence); CR-BP-21c.1..e.1 (remaining completion tranches, planned)

## 1. What this CR is

The second domain-completion tranche of the CR-BP-21 series, mirroring
the CR-BP-21a.1 pattern. CR-BP-21b landed the AO Conceive-cell L1
group plus 1 L2 per ratified cell; the register v3 audit records the
AO Design/Build/Operate/Improve cells as `ratified-pending-landing`
with `planned_tranche: CR-BP-21b.1`. This CR closes that gap: it
lands the 4 remaining AO Process Groups and the 13 remaining register
v2 L2 candidates, and extends the existing Conceive group's composes
edges to the 2 new Conceive-cell L2s.

The substrate-neutral vocabulary from CR-BP-21b §5 governs all new
names and outcome statements ("agent" for all substrates; "workforce"
as process_specialization).

## 2. The 4 new Process Groups (L1)

- `dea:group-organization-and-role-design` — AO x Design. Composes
  design-organization-structure (landed CR-BP-21b),
  design-role-catalogue, design-competency-framework,
  design-agent-topology.
- `dea:group-agent-acquisition-and-onboarding` — AO x Build. Composes
  acquire-and-onboard-agents (landed CR-BP-21b; subsumes the register
  candidates "source and recruit", "provision artificial agents",
  "onboard and integrate" per the CR-BP-21b §5 umbrella), and
  build-contractor-and-partner-agent-pool.
- `dea:group-agent-operations` — AO x Operate. Composes
  operate-agent-performance (landed CR-BP-21b),
  operate-payroll-and-benefits, operate-time-and-attendance,
  operate-learning-and-development, coordinate-collaboration.
- `dea:group-agent-and-organization-improvement` — AO x Improve.
  Composes develop-agents-and-organization (landed CR-BP-21b),
  conduct-engagement-and-alignment-review,
  conduct-capability-gap-analysis, reorganize-structures.

The existing `dea:group-organization-and-agent-conception` (Conceive)
gains composes edges to the 2 new Conceive-cell L2s
(frame-organization-model, conceive-workforce-and-agent-mix).

## 3. The 13 new L2 Business Processes

All land as `lifecycle_status: candidate` with substrate-neutral
naming; `process_type` matches the cell pattern established in
CR-BP-21b (management for Conceive/Design/Improve cells; core for
Build/Operate, except coordinate-collaboration which is management
per the BP-ARC-ID-004 keyword-density gate).

| L2 ID | Cell | process_intent | process_type |
|---|---|---|---|
| dea:process-frame-organization-model | AO/Conceive | develop | management |
| dea:process-conceive-workforce-and-agent-mix | AO/Conceive | develop | management |
| dea:process-design-role-catalogue | AO/Design | develop | management |
| dea:process-design-competency-framework | AO/Design | develop | management |
| dea:process-design-agent-topology | AO/Design | develop | management |
| dea:process-build-contractor-and-partner-agent-pool | AO/Build | develop | core |
| dea:process-operate-payroll-and-benefits | AO/Operate | operate | core |
| dea:process-operate-time-and-attendance | AO/Operate | operate | core |
| dea:process-operate-learning-and-development | AO/Operate | operate | core |
| dea:process-coordinate-collaboration | AO/Operate | operate | management |
| dea:process-conduct-engagement-and-alignment-review | AO/Improve | develop | management |
| dea:process-conduct-capability-gap-analysis | AO/Improve | develop | management |
| dea:process-reorganize-structures | AO/Improve | develop | management |

## 4. In-place edits to existing records

- `dea:group-organization-and-agent-conception`: +2 composes edges,
  +1 change_history entry (surgical text patches, per the
  CR-BP-21a.1 precedent).
- `dea-pc-ao-{conceive,design,build,operate,improve}` contexts:
  `processes:` lists extended (PC-008), +1 change_history entry each.

No schema, validator, or CI surface changes.

## 5. Register v3 audit impact

AO Design/Build/Operate/Improve flip from `ratified-pending-landing`
to `landed`: **23 landed / 12 ratified-pending-landing / 14
backlog-deferred**. The remaining pending cells are the non-Conceive
cells of PV, OE, FA (planned CR-BP-21c.1..e.1).

## 6. What this CR does NOT do

- The other three domains' completion tranches (CR-BP-21c.1..e.1) —
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
- Register audit: OK (23 landed / 12 pending / 14 deferred).
- CATALOG.yaml `--check` OK.
