# CR-BP-47: L3 Activity EO Build + Improve Tranche (EnablementAndOperations domain completion)

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
**Carrier**: Sixth L3 (Activity) contribution slice; completes the EnablementAndOperations domain's L3 coverage (Operate: CR-BP-42/43; Conceive + Design: CR-BP-46; this slice: Build + Improve).
**Depends on**: CR-BP-32 (Activity Model; ACT-001..010), CR-BP-42 (pilot), CR-BP-43 (EO/Operate tranche), CR-BP-46 (EO Conceive + Design tranche)
**Lands against**: 126 canonical BP records, 35 canonical PG records, 35 canonical PC records, 109 canonical Activity records; 23 conformance gates CONFORMANT; v0.3.0 tagged (CR-BP-41)

---

## 1. Change Request

Land L3 Activity decompositions for the 10 Business Processes of EnablementAndOperations' Build and Improve stages, completing the domain's L3 coverage (5/5 stages).

Per-BP depositions (4 Activities each, 40 total):

| Coordinate | Business Process | Activities |
|---|---|---|
| EO / Build | `dea:process-acquire-technology-assets` | Procure Hardware and Software; Install Technology Assets; Commission Technology Assets; Register Acquired Assets |
| EO / Build | `dea:process-build-delivery-capability` | Stand Up Delivery Components; Integrate Delivery Capability; Verify Delivery Capability; Hand Over Delivery Capability to Operations |
| EO / Build | `dea:process-build-logistics-network` | Establish Network Nodes; Contract Carriers; Provision Warehouse Capacity; Verify Network Readiness |
| EO / Build | `dea:process-commission-production-line` | Install Line Equipment; Configure Line Controls; Run Line Trials; Certify Line for Production |
| EO / Build | `dea:process-provision-facilities` | Secure Facility Sites; Fit Out Facilities; Commission Facility Services; Hand Over Facilities to Operations |
| EO / Improve | `dea:process-conduct-lean-six-sigma-programme` | Select Improvement Projects; Deliver Improvement Projects; Sustain Improvement Gains; Develop Improvement Capability |
| EO / Improve | `dea:process-conduct-logistics-optimization` | Analyze Routing Performance; Design Route and Network Changes; Commit Logistics Changes; Measure Optimization Outcomes |
| EO / Improve | `dea:process-conduct-operations-performance-review` | Assemble Performance Evidence; Form Review Findings; Route Findings to Improvement Tracks; Commit Review Outcomes |
| EO / Improve | `dea:process-improve-technology-platforms` | Analyze Platform Gaps; Design Platform Upgrades; Commit Platform Upgrades; Measure Platform Improvement |
| EO / Improve | `dea:process-optimize-asset-utilization` | Analyze Asset Utilization; Design Redeployment Options; Commit Redeployment Decisions; Measure Utilization Outcomes |

Every candidate was tested against the four L2 criteria (CR-BP-32 §5); all 40 FAIL Standalone Executability and Resource Dedication and classify as Activities. Cohesion scores (§6) are recorded per candidate in each research deposition.

## 2. Deposition mechanics (pattern per CR-BP-42 §2)

1. **Research deposition** per BP at `entities/v1-alpha/dea:process-<bp>/research/l3-candidate-universe.yaml` (+ state-directory README.md).
2. **Canonical landing**: one record per Activity, conforming to `schemas/entities/activity.schema.json`; `ecfConformance` blocks inherit each BP's coordinate (`ecf:enablementAndOperations.build` / `.improve`). All 40 records pass Draft-07 validation.
3. **Decomposition boundary**: all records carry `decomposition_boundary: l4-reached` (CR-BP-32 §12).
4. **Bidirectional traceability (ACT-010)**: each parent BP gains `metadata.activity_references[]` and a CR-BP-47 `change_history` entry. Versions unchanged per SIV-004.
5. **Reconciliation artifacts**: baseline and conformance report regenerated (345 records, all at L4).
6. **Count assertion updates**: ACT suite 109 -> 149; EXE suite 270 -> 310; conformance-report test 305 -> 345.

## 3. Gate posture

- Gate [15] ACT-001..010 live run: **CONFORMANT, 149 Activity records, 0 findings**.
- Gate [8] ECF conformance: **310 entries conform** (was 270).
- Full suite: **23 gates, 0 blocking, 0 advisory failures**.

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `entities/v1-alpha/dea:activity-*/` (40 dirs) | NEW | Canonical Activity records (4 per BP) |
| `entities/v1-alpha/dea:process-<bp>/research/` (x10) | NEW | Depositions + READMEs |
| `entities/v1-alpha/dea:process-<bp>/dea:process-<bp>.yaml` (x10) | MOD | `metadata.activity_references[]` + CR-BP-47 change_history |
| `tests/test_check_activity_model.py` | MOD | Count assertions: 149 Activity records |
| `tests/test_check_execution_boundary.py` | MOD | Count assertions: 310 records checked |
| `tests/test_architectural_regression.py` | MOD | Conformance report: 345 records, all L4 |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated (10 mutated parent BP hash lines) |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated by gate [10]; 345 records |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 58 -> 59 |
| `change-requests/CR-BP-47-l3-eo-build-improve-tranche.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-47 row added |

## 5. What this CR is NOT

- **NOT a Task (L4) landing.** All Activities terminate at `l4-reached`.
- **NOT a schema, validator-rule, CI, or gate change.** Wiring from CR-BP-42 is reused unchanged.
- **NOT an L3 sweep of other domains.** After this slice, PartyAndRelationship (5/5) and EnablementAndOperations (5/5) are fully L3-covered; 25 coordinates across the remaining 5 domains await tranches.
- **NOT a remediation of the dangling `dea:process-frame-financial-policy-thesis` composes reference** (queued separately).

## 6. Acceptance criteria

1. All 40 new Activity records validate against `schemas/entities/activity.schema.json` (Draft-07).
2. `python3 scripts/check_activity_model.py` runs CONFORMANT: 149 Activity records, 0 findings.
3. Each of the 10 parent BPs declares its 4 Activity ids in `metadata.activity_references[]` (ACT-010).
4. `python3 scripts/check_ecf_conformance.py` reports 310 entries conform.
5. `python3 scripts/build_inventory.py --self-test --strict` passes after regeneration.
6. Full pytest suite passes; `scripts/conformance_result.py` remains CONFORMANT (23 gates).
7. `python3 scripts/check_cr_metadata.py` reports 0 new findings.
8. `python3 scripts/check_catalog_index.py --strict` passes (all 10 new research/ state directories carry README.md).
9. No validator-rule, schema, CI, or governance-decision change.

## 7. Result

CR-BP-47 completes the EnablementAndOperations domain's L3 coverage: 40 new canonical Activity records across 10 Business Processes in the Build and Improve stages, bringing the catalog to 149 Activity records at 0 findings against gate [15]. EnablementAndOperations is the second fully L3-covered domain (5/5 coordinates, 28 BPs, 113 Activities); PartyAndRelationship was first (5/5, 9 BPs, 36 Activities). 37 of 126 BPs are now L3-decomposed. The structured deposition pattern has held across six slices without modification.
