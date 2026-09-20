# CR-BP-54: L3 Activity S&D Conceive + Design + Build Tranche

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
**Carrier**: Thirteenth L3 (Activity) contribution slice; first of two tranches for the StrategyAndDirection domain (this slice: Conceive + Design + Build; Improve + Operate follow as CR-BP-55).
**Depends on**: CR-BP-32 (Activity Model; ACT-001..010), CR-BP-42 (pilot), CR-BP-43..53 (scaled tranches)
**Lands against**: 126 canonical BP records, 35 canonical PG records, 35 canonical PC records, 353 canonical Activity records; 23 conformance gates CONFORMANT; v0.3.0 tagged (CR-BP-41)

---

## 1. Change Request

Land L3 Activity decompositions for the 12 Business Processes of StrategyAndDirection's Conceive, Design, and Build stages.

Per-BP depositions (4 Activities each, 48 total):

| Coordinate | Business Process | Activities |
|---|---|---|
| S&D / Conceive | `dea:process-conceive-strategic-intent` | Sense Intent Imperatives; Frame Strategic Intent Narrative; Scope Intent Trade-offs; Commit Strategic Intent |
| S&D / Conceive | `dea:process-define-enterprise-purpose-and-ambition` | Sense Purpose Imperatives; Frame Purpose Statement; Frame Ambition Envelope; Commit Purpose and Ambition |
| S&D / Conceive | `dea:process-develop-corporate-strategy` | Synthesize Strategic Direction; Articulate Strategic Trajectory; Choose Strategic Trajectory; Commit Corporate Strategy |
| S&D / Conceive | `dea:process-frame-strategic-horizons` | Bound Horizon Timeframes; Anchor Horizon Milestones; Align Horizons with Intent; Commit Strategic Horizons |
| S&D / Design | `dea:process-design-objectives-and-targets` | Bound Objectives Scope; Draft Objectives and Targets; Assign Target Ownership; Commit Objectives and Targets |
| S&D / Design | `dea:process-design-strategic-options` | Bound Option Design Space; Draft Strategic Options; Frame Option Evaluation Criteria; Commit Strategic Option Designs |
| S&D / Design | `dea:process-design-strategic-scenarios` | Bound Scenario Assumptions; Draft Strategic Scenarios; Design Scenario Signposts; Commit Strategic Scenarios |
| S&D / Design | `dea:process-evaluate-strategic-alternatives` | Bound Evaluation Scope; Execute Strategic Comparison; Articulate Strategic Preference; Commit Strategic Preference |
| S&D / Build | `dea:process-build-strategic-plan` | Bound Plan Version; Assemble Strategic Plan; Review Strategic Plan; Commit Strategic Plan |
| S&D / Build | `dea:process-build-strategic-roadmap` | Sequence Strategic Initiatives; Anchor Roadmap Milestones; Assemble Strategic Roadmap; Commit Strategic Roadmap |
| S&D / Build | `dea:process-set-resource-allocation-priorities` | Bound Allocation Envelopes; Allocate Resources to Initiatives; Prioritize Allocation Decisions; Commit Allocation Priorities |
| S&D / Build | `dea:process-translate-strategic-choices-into-initiatives` | Bound Initiative Scope; Draft Strategic Initiatives; Review Strategic Fit; Commit Strategic Initiatives |

Every candidate was tested against the four L2 criteria (CR-BP-32 §5); all 48 FAIL Standalone Executability and Resource Dedication and classify as Activities. Cohesion scores (§6) are recorded per candidate in each research deposition.

## 2. Deposition mechanics (pattern per CR-BP-42 §2)

1. **Research deposition** per BP at `entities/v1-alpha/dea:process-<bp>/research/l3-candidate-universe.yaml` (+ state-directory README.md).
2. **Canonical landing**: one record per Activity, conforming to `schemas/entities/activity.schema.json`; `ecfConformance` blocks inherit each BP's own canonical coordinate identifier (read from the BP record, not assumed). All 48 records pass Draft-07 validation.
3. **Decomposition boundary**: all records carry `decomposition_boundary: l4-reached` (CR-BP-32 §12).
4. **Bidirectional traceability (ACT-010)**: each parent BP gains `metadata.activity_references[]` and a CR-BP-54 `change_history` entry. All 12 parent records carry the current metadata shape. Versions unchanged per SIV-004.
5. **Reconciliation artifacts**: baseline and conformance report regenerated (597 records, all at L4).
6. **Count assertion updates**: ACT suite 353 -> 401; EXE suite 514 -> 562; conformance-report test 549 -> 597.

## 3. Gate posture

- Gate [15] ACT-001..010 live run: **CONFORMANT, 401 Activity records, 0 findings**.
- Gate [8] ECF conformance: **562 entries conform** (was 514).
- Full suite: **23 gates, 0 blocking, 0 advisory failures**.

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `entities/v1-alpha/dea:activity-*/` (48 dirs) | NEW | Canonical Activity records (4 per BP) |
| `entities/v1-alpha/dea:process-<bp>/research/` (x12) | NEW | Depositions + READMEs |
| `entities/v1-alpha/dea:process-<bp>/dea:process-<bp>.yaml` (x12) | MOD | `metadata.activity_references[]` + CR-BP-54 change_history |
| `tests/test_check_activity_model.py` | MOD | Count assertions: 401 Activity records |
| `tests/test_check_execution_boundary.py` | MOD | Count assertions: 562 records checked |
| `tests/test_architectural_regression.py` | MOD | Conformance report: 597 records, all L4 |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated (12 mutated parent BP hash lines) |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated by gate [10]; 597 records |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 65 -> 66 |
| `change-requests/CR-BP-54-l3-sd-conceive-design-build-tranche.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-54 row added |

## 5. What this CR is NOT

- **NOT a Task (L4) landing.** All Activities terminate at `l4-reached`.
- **NOT a schema, validator-rule, CI, or gate change.** Wiring from CR-BP-42 is reused unchanged.
- **NOT the complete StrategyAndDirection L3 sweep.** Improve + Operate (7 BPs) follow as CR-BP-55.
- **NOT an L3 sweep of AgencyAndOrganization** (18 BPs, queued as a future tranche set).
- **NOT a remediation of the dangling `dea:process-frame-financial-policy-thesis` composes reference** (queued separately; it sits in FinanceAndAccounting).

## 6. Acceptance criteria

1. All 48 new Activity records validate against `schemas/entities/activity.schema.json` (Draft-07).
2. `python3 scripts/check_activity_model.py` runs CONFORMANT: 401 Activity records, 0 findings.
3. Each of the 12 parent BPs declares its 4 Activity ids in `metadata.activity_references[]` (ACT-010).
4. `python3 scripts/check_ecf_conformance.py` reports 562 entries conform.
5. `python3 scripts/build_inventory.py --self-test --strict` passes after regeneration.
6. Full pytest suite passes; `scripts/conformance_result.py` remains CONFORMANT (23 gates).
7. `python3 scripts/check_cr_metadata.py` reports 0 new findings.
8. `python3 scripts/check_catalog_index.py --strict` passes (all 12 new research/ state directories carry README.md).
9. No validator-rule, schema, CI, or governance-decision change.

## 7. Result

CR-BP-54 lands L3 coverage for StrategyAndDirection's Conceive, Design, and Build stages: 48 new canonical Activity records across 12 Business Processes, bringing the catalog to 401 Activity records at 0 findings against gate [15]. After this slice, StrategyAndDirection has L3 coverage in 3 of 5 stages; Improve + Operate complete the domain as CR-BP-55. The structured deposition pattern has held across thirteen slices without modification.