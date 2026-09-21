# CR-BP-48: L3 Activity GE Conceive + Design + Build Tranche

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
**Carrier**: Seventh L3 (Activity) contribution slice; first of two tranches completing the GovernanceAndExistence domain's L3 coverage (this slice: Conceive + Design + Build; Improve + Operate follow as CR-BP-49).
**Depends on**: CR-BP-32 (Activity Model; ACT-001..010), CR-BP-42 (pilot), CR-BP-43..47 (scaled tranches)
**Lands against**: 126 canonical BP records, 35 canonical PG records, 35 canonical PC records, 149 canonical Activity records; 23 conformance gates CONFORMANT; v0.3.0 tagged (CR-BP-41)

---

## 1. Change Request

Land L3 Activity decompositions for the 8 live Business Processes of GovernanceAndExistence's Conceive, Design, and Build stages.

**Scope exclusion**: `dea:process-develop-governance-strategy` (GE/Conceive) is `lifecycle_status: deprecated` (parked per the CR-BP-20 Option A split) and is exempt from L3 decomposition under the same MECE-008 logic that exempts deprecated records from composition gates. GE/Conceive therefore contributes 2 live BPs to this tranche.

Per-BP depositions (4 Activities each, 32 total):

| Coordinate | Business Process | Activities |
|---|---|---|
| GE / Conceive | `dea:process-frame-risk-framework-direction` | Articulate Risk Appetite; Define Tolerance Bands; Frame Governance Posture for Risk; Commit Risk Framework Direction |
| GE / Conceive | `dea:process-initiate-policy-and-charter` | Bound Policy Scope; Propose Authority and Decision Rights; Draft Initial Policy Document; Commit Policy Initiation |
| GE / Design | `dea:process-design-governance-system` | Articulate Governance Bodies; Design Authority Delegations; Specify Decision Rights; Commit Governance System Design |
| GE / Design | `dea:process-design-policies-and-controls` | Design Policy Artifacts; Define Control Objectives; Design Compliance Regime; Commit Policy and Control Design |
| GE / Design | `dea:process-design-risk-framework` | Design Risk Taxonomy; Design Assessment Scales; Design Governance Integration; Commit Risk Framework Design |
| GE / Build | `dea:process-codify-charters-and-policies` | Codify Charters; Codify Policies; Codify Standard Artifacts; Publish Codified Instruments |
| GE / Build | `dea:process-establish-governance-bodies` | Constitute Bodies; Establish Operating Cycles; Equip Bodies with Instruments; Verify Body Readiness |
| GE / Build | `dea:process-establish-risk-and-control-apparatus` | Establish Risk Registers; Deploy Monitoring Tooling; Establish Reporting Lines; Verify Apparatus Readiness |

Every candidate was tested against the four L2 criteria (CR-BP-32 §5); all 32 FAIL Standalone Executability and Resource Dedication and classify as Activities. Cohesion scores (§6) are recorded per candidate in each research deposition.

## 2. Deposition mechanics (pattern per CR-BP-42 §2)

1. **Research deposition** per BP at `entities/v1-alpha/dea:process-<bp>/research/l3-candidate-universe.yaml` (+ state-directory README.md).
2. **Canonical landing**: one record per Activity, conforming to `schemas/entities/activity.schema.json`; `ecfConformance` blocks inherit each BP's coordinate (`ecf:governanceExistence.conceive` / `.design` / `.build`). All 32 records pass Draft-07 validation.
3. **Decomposition boundary**: all records carry `decomposition_boundary: l4-reached` (CR-BP-32 §12).
4. **Bidirectional traceability (ACT-010)**: each parent BP gains `metadata.activity_references[]` and a CR-BP-48 `change_history` entry. Three BPs of the CR-BP-21f.1 era (`frame-risk-framework-direction`, `design-risk-framework`, `establish-risk-and-control-apparatus`) carry the legacy shape (top-level `change_history`, no `metadata` block); these gained a `metadata` block containing `established_by` / `established_at` (preserving CR-BP-21f.1 provenance) plus `activity_references[]`, with the change entry appended to their existing top-level `change_history` in native style. Legacy layout otherwise preserved (append-only). All 8 patched records pass `schemas/entity.schema.json` validation. Versions unchanged per SIV-004.
5. **Reconciliation artifacts**: baseline and conformance report regenerated (377 records, all at L4).
6. **Count assertion updates**: ACT suite 149 -> 181; EXE suite 310 -> 342; conformance-report test 345 -> 377.

## 3. Gate posture

- Gate [15] ACT-001..010 live run: **CONFORMANT, 181 Activity records, 0 findings**.
- Gate [8] ECF conformance: **342 entries conform** (was 310).
- Full suite: **23 gates, 0 blocking, 0 advisory failures**.

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `entities/v1-alpha/dea:activity-*/` (32 dirs) | NEW | Canonical Activity records (4 per BP) |
| `entities/v1-alpha/dea:process-<bp>/research/` (x8) | NEW | Depositions + READMEs |
| `entities/v1-alpha/dea:process-<bp>/dea:process-<bp>.yaml` (x8) | MOD | `metadata.activity_references[]` + CR-BP-48 change_history (3 legacy-shape records handled per §2.4) |
| `tests/test_check_activity_model.py` | MOD | Count assertions: 181 Activity records |
| `tests/test_check_execution_boundary.py` | MOD | Count assertions: 342 records checked |
| `tests/test_architectural_regression.py` | MOD | Conformance report: 377 records, all L4 |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated (8 mutated parent BP hash lines) |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated by gate [10]; 377 records |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 59 -> 60 |
| `change-requests/CR-BP-48-l3-ge-conceive-design-build-tranche.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-48 row added |

## 5. What this CR is NOT

- **NOT a Task (L4) landing.** All Activities terminate at `l4-reached`.
- **NOT a schema, validator-rule, CI, or gate change.** Wiring from CR-BP-42 is reused unchanged; the shared entity schema already permits `metadata` on legacy-shape records.
- **NOT a decomposition of the deprecated `dea:process-develop-governance-strategy`** (excluded per §1).
- **NOT the complete GovernanceAndExistence L3 sweep.** Improve + Operate (7 live BPs) follow as CR-BP-49.
- **NOT a remediation of the dangling `dea:process-frame-financial-policy-thesis` composes reference** (queued separately).

## 6. Acceptance criteria

1. All 32 new Activity records validate against `schemas/entities/activity.schema.json` (Draft-07).
2. `python3 scripts/check_activity_model.py` runs CONFORMANT: 181 Activity records, 0 findings.
3. Each of the 8 parent BPs declares its 4 Activity ids in `metadata.activity_references[]` (ACT-010).
4. The 3 legacy-shape BP records validate against `schemas/entity.schema.json` after gaining `metadata`.
5. `python3 scripts/check_ecf_conformance.py` reports 342 entries conform.
6. `python3 scripts/build_inventory.py --self-test --strict` passes after regeneration.
7. Full pytest suite passes; `scripts/conformance_result.py` remains CONFORMANT (23 gates).
8. `python3 scripts/check_cr_metadata.py` reports 0 new findings.
9. `python3 scripts/check_catalog_index.py --strict` passes (all 8 new research/ state directories carry README.md).
10. No validator-rule, schema, CI, or governance-decision change.

## 7. Result

CR-BP-48 lands L3 coverage for GovernanceAndExistence's Conceive, Design, and Build stages: 32 new canonical Activity records across 8 live Business Processes, bringing the catalog to 181 Activity records at 0 findings against gate [15]. The deprecated `develop-governance-strategy` BP is excluded from decomposition. After this slice, GovernanceAndExistence has L3 coverage in 3 of 5 stages; Improve + Operate complete the domain as CR-BP-49. The structured deposition pattern has held across seven slices without modification.
