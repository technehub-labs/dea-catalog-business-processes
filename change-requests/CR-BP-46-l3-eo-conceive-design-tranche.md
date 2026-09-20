# CR-BP-46: L3 Activity EO Conceive + Design Tranche (EnablementAndOperations completion, part 1 of 2)

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Proposed
**Layer**: L3
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-13
**Carrier**: Fifth L3 (Activity) contribution slice; first of two tranches completing the EnablementAndOperations domain's L3 coverage (Operate covered by CR-BP-42/43; this slice covers Conceive + Design; Build + Improve follow as CR-BP-47).
**Depends on**: CR-BP-32 (Activity Model; ACT-001..010), CR-BP-42 (pilot), CR-BP-43 (EO/Operate tranche), CR-BP-44, CR-BP-45
**Lands against**: 126 canonical BP records, 35 canonical PG records, 35 canonical PC records, 73 canonical Activity records; 23 conformance gates CONFORMANT; v0.3.0 tagged (CR-BP-41)

---

## 1. Change Request

Land L3 Activity decompositions for the 9 Business Processes of EnablementAndOperations' Conceive and Design stages.

Per-BP depositions (4 Activities each, 36 total):

| Coordinate | Business Process | Activities |
|---|---|---|
| EO / Conceive | `dea:process-frame-operations-strategy` | Assess Execution Engine Context; Bound Delivery Model Envelope; Frame Enablement and Asset Direction; Commit Operations Strategy |
| EO / Conceive | `dea:process-frame-delivery-model-conception` | Select Channel Patterns; Frame Service-Level Envelopes; Frame Fulfilment Patterns; Commit Delivery Model Conception |
| EO / Conceive | `dea:process-frame-physical-asset-approach` | Frame Footprint Principles; Bound Asset Lifecycle Envelopes; Assess Footprint Options; Commit Physical Asset Approach |
| EO / Conceive | `dea:process-frame-technology-enablement-approach` | Identify Platform Families; Frame Sourcing Principles; Assess Enablement Fit; Commit Technology Enablement Approach |
| EO / Design | `dea:process-design-operations-model` | Structure Operations Model; Integrate Model Components; Specify Operating Rhythms; Commit Operations Model Design |
| EO / Design | `dea:process-design-delivery-model` | Configure Channels; Design Service Levels; Design Fulfilment Flows; Commit Delivery Model Design |
| EO / Design | `dea:process-design-technology-platform-architecture` | Specify Platform Components; Design Integration Patterns; Define Deployment Topology; Commit Platform Architecture |
| EO / Design | `dea:process-design-facility-and-asset-blueprint` | Design Facility Layouts; Specify Equipment; Model Capacity Envelopes; Commit Facility Blueprint |
| EO / Design | `dea:process-design-logistics-and-routing` | Select Transport Modes; Design Routing Logic; Position Network Nodes; Commit Logistics Design |

Every candidate was tested against the four L2 criteria (CR-BP-32 §5); all 36 FAIL Standalone Executability and Resource Dedication and classify as Activities. Cohesion scores (§6) are recorded per candidate in each research deposition.

## 2. Deposition mechanics (pattern per CR-BP-42 §2)

1. **Research deposition** per BP at `entities/v1-alpha/dea:process-<bp>/research/l3-candidate-universe.yaml` (+ state-directory README.md).
2. **Canonical landing**: one record per Activity, conforming to `schemas/entities/activity.schema.json`; `ecfConformance` blocks inherit each BP's coordinate (`ecf:enablementAndOperations.conceive` / `.design`). All 36 records pass Draft-07 validation.
3. **Decomposition boundary**: all records carry `decomposition_boundary: l4-reached` (CR-BP-32 §12).
4. **Bidirectional traceability (ACT-010)**: each parent BP gains `metadata.activity_references[]` and a CR-BP-46 `change_history` entry. Versions unchanged per SIV-004.
5. **Reconciliation artifacts**: baseline and conformance report regenerated (305 records, all at L4).
6. **Count assertion updates**: ACT suite 73 -> 109; EXE suite 234 -> 270; conformance-report test 269 -> 305.

## 3. Gate posture

- Gate [15] ACT-001..010 live run: **CONFORMANT, 109 Activity records, 0 findings**.
- Gate [8] ECF conformance: **270 entries conform** (was 234).
- Full suite: **23 gates, 0 blocking, 0 advisory failures**.

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `entities/v1-alpha/dea:activity-*/` (36 dirs) | NEW | Canonical Activity records (4 per BP) |
| `entities/v1-alpha/dea:process-<bp>/research/` (x9) | NEW | Depositions + READMEs |
| `entities/v1-alpha/dea:process-<bp>/dea:process-<bp>.yaml` (x9) | MOD | `metadata.activity_references[]` + CR-BP-46 change_history |
| `tests/test_check_activity_model.py` | MOD | Count assertions: 109 Activity records |
| `tests/test_check_execution_boundary.py` | MOD | Count assertions: 270 records checked |
| `tests/test_architectural_regression.py` | MOD | Conformance report: 305 records, all L4 |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated (9 mutated parent BP hash lines) |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated by gate [10]; 305 records |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 57 -> 58 |
| `change-requests/CR-BP-46-l3-eo-conceive-design-tranche.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-46 row added |

## 5. What this CR is NOT

- **NOT a Task (L4) landing.** All Activities terminate at `l4-reached`.
- **NOT a schema, validator-rule, CI, or gate change.** Wiring from CR-BP-42 is reused unchanged.
- **NOT the complete EnablementAndOperations L3 sweep.** Build + Improve (10 BPs) follow as CR-BP-47.
- **NOT a remediation of the dangling `dea:process-frame-financial-policy-thesis` composes reference** (queued separately).

## 6. Acceptance criteria

1. All 36 new Activity records validate against `schemas/entities/activity.schema.json` (Draft-07).
2. `python3 scripts/check_activity_model.py` runs CONFORMANT: 109 Activity records, 0 findings.
3. Each of the 9 parent BPs declares its 4 Activity ids in `metadata.activity_references[]` (ACT-010).
4. `python3 scripts/check_ecf_conformance.py` reports 270 entries conform.
5. `python3 scripts/build_inventory.py --self-test --strict` passes after regeneration.
6. Full pytest suite passes; `scripts/conformance_result.py` remains CONFORMANT (23 gates).
7. `python3 scripts/check_cr_metadata.py` reports 0 new findings.
8. `python3 scripts/check_catalog_index.py --strict` passes (all 9 new research/ state directories carry README.md).
9. No validator-rule, schema, CI, or governance-decision change.

## 7. Result

CR-BP-46 lands L3 coverage for EnablementAndOperations' Conceive and Design stages: 36 new canonical Activity records across 9 Business Processes, bringing the catalog to 109 Activity records at 0 findings against gate [15]. After this slice, EnablementAndOperations has L3 coverage in 3 of 5 stages (Operate, Conceive, Design); Build + Improve complete the domain as CR-BP-47. The structured deposition pattern has now held across five slices without modification.
