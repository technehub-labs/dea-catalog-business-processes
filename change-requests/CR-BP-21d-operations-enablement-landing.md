# CR-BP-21d: EnablementAndOperations Landing (ECF v2.4.0 — Fourth Unadmitted Domain)

**Status**: Accepted
**Admission authority**: yes
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-08
**Depends on**: CR-BP-19 (register v2); CR-BP-20 (alignment); CR-BP-21a (StrategyAndDirection landing); CR-BP-21b (AgencyAndOrganization landing); CR-BP-21c (ProductAndValue landing)
**Related**: dea-metaframework/framework/domain-grounding.md §3.6; CR-BP-21e (FinanceAndAccounting, remaining unadmitted domain, planned)

## 1. What this CR is

Fourth landing tranche of the CR-BP-21 series. Lands
EnablementAndOperations against the rediscovered register v2 cells
(Conceive / Design / Build / Operate / Improve). The Activate / Retire
cells remain deferred register-wide per CR-BP-19.

v2.4.0 (CR-ECF-006) dissolved the v2.3.0 "Supply & Resources" domain
and redistributed its concerns: physical and virtual resources moved to
Enablement & Operations as enablers of execution; supplier
relationships moved to Party & Relationship; financial resources moved
to Finance & Accounting. This landing therefore absorbs execution-side
sourcing/asset conception, asset/facility blueprint design, asset
acquisition and facility provisioning, procurement execution, facility
operation, asset maintenance, asset utilization improvement, and asset
disposal scoping from the dissolved domain (per register v2
migration_notes, grounded in domain-grounding.md §3.6).

## 2. The 5 process contexts

- `dea:pc-oe-conceive` — Operations Model & Enablement Conception
- `dea:pc-oe-design` — Enablement & Operations Design
- `dea:pc-oe-build` — Enablement & Operations Build
- `dea:pc-oe-operate` — Execution, Technology & Asset Operation
- `dea:pc-oe-improve` — Enablement & Operations Improvement

The Activate / Retire cells (per register v2) remain deferred.

## 3. The 1 Process Group (L1)

- `dea:group-operations-model-conception` — Process Group for
  EnablementAndOperations x Conceive. Composes the 4 L2s of the
  Conceive cell (Frame operations strategy, Frame delivery model
  conception, Frame technology enablement approach, Frame physical
  asset approach).

  Naming note: the L1 group covers the full Conceive cell (Operations
  Model Conception + Enablement Conception). The id surfaces
  "operations model" as the principal L1 candidate; the group scope
  covers both L1 candidates as a single bounded Process Group per
  CR-BP-12 §4 (group id is domain-scoped, not cell-component-scoped).

## 4. The 5 L2 Business Processes

One L2 per ratified cell. Per CR-BP-19,
all land as `lifecycle_status: candidate`.

| L2 ID | Cell | process_intent | process_type |
|---|---|---|---|
| dea:process-frame-operations-strategy | OE/Conceive | develop | management |
| dea:process-design-operations-model | OE/Design | develop | management |
| dea:process-build-delivery-capability | OE/Build | develop | core |
| dea:process-operate-service-delivery | OE/Operate | operate | core |
| dea:process-conduct-operations-performance-review | OE/Improve | develop | management |

The 4-L2 Conceive cell (operations strategy, delivery model, technology
enablement, physical asset approach) lands 1 L2 (operations strategy;
remaining 3 in CR-BP-21d.1). The 5-L2 Design cell (operations model,
delivery model, technology platform architecture, facility blueprint,
logistics and routing) lands 1 L2 (operations model; remaining 4 in
CR-BP-21d.1). The 5-L2 Build cell (production line, delivery
capability, logistics network, technology assets, facilities) lands 1
L2 (delivery capability; remaining 4 in CR-BP-21d.1). The 9-L2 Operate
cell (production, service delivery, logistics, warehouse, quality,
technology platforms, facilities, asset maintenance, procurement)
lands 1 L2 (service delivery; remaining 8 in CR-BP-21d.1). The 5-L2
Improve cell (performance review, logistics optimization, lean
programme, asset utilization, technology platforms) lands 1 L2
(performance review; remaining 4 in CR-BP-21d.1).

## 5. Boundary discipline (dissolved Supply & Resources absorption)

The v2.4.0 redistribution is exercised concretely in this landing:

- Execution-side sourcing and asset concerns land here (OE), not in
  Party & Relationship. Supplier *relationship* conception,
  onboarding, performance, and consolidation remain in
  party-relationship per register v2 migration_notes.
- Procurement *execution* is OE/Operate; supplier relationship
  management is PR/Operate. The boundary rule (domain-grounding.md
  §3.6): OE owns the transformation; PR owns the relationship.
- Technology is positioned as an enabler of execution (Technology
  Enablement sub-concern), not a standalone domain.

## 6. Provenance + classification (per the landed-population pattern)

- `lifecycle_status: candidate` for all 5 L2s and the 1 L1 group.
- `process_intent` / `process_type` from canonical vocabularies
  (CR-BP-14 §10). `process_type` aligned to outcome keyword density
  (BP-ARC-ID-004): the two Build/Operate L2s land as `core` (delivery
  and operation verbs dominate); Conceive/Design/Improve land as
  `management`.
- `metadata.change_history` carries the CR-BP-21d entry on every
  entry with phase-7 marker, `cr: CR-BP-21d`, the date, and the
  rationale (grounds the change in domain-grounding.md §3.6).
- `metadata.cross_context_overlap: []` (no cross-cell overlap;
  MECE for the OE cells is verified in the register v2).

## 7. What this CR does NOT do

- The remaining unadmitted v2.4.0 domain (FinanceAndAccounting) —
  lands in CR-BP-21e.
- The remaining L2s of the OE cells — follow-up CR-BP-21d.1 when
  more L2 material is ready.
- OE/Activate and OE/Retire cells — register v2 keeps these
  deferred.
- Cross-repo BC capability-operations re-affiliation — out of scope
  here.

## 8. Verification

- All 15 conformance gates pass (CONFORMANT).
- pytest 148 pass / 1 pre-existing failure.
- check_process_identity 0 blocking findings.
- Admission gate `--strict-provenance`: exit 0; the 6 new entries
  (5 L2s + 1 L1 group) all carry the CR-BP-21d reference.
- Fresh-clone reproduction (with `git remote set-url origin ...git`
  normalization per `.github/workflows/ci.yml`):
  `python scripts/regenerate_catalog.py --check` OK.
