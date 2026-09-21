# CR-BP-57: L3 Activity A&O Improve + Operate Tranche

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
**Date**: 2026-09-14
**Carrier**: Sixteenth L3 (Activity) contribution slice; second of two tranches for the AgencyAndOrganization domain (this slice: Improve + Operate; completes the domain's L3 coverage, 5/5 stages, and with it full L0-to-L3 coverage of all seven ECF domains).
**Depends on**: CR-BP-32 (Activity Model; ACT-001..010), CR-BP-42 (pilot), CR-BP-43..56 (scaled tranches)
**Lands against**: 126 canonical BP records, 35 canonical PG records, 35 canonical PC records, 465 canonical Activity records; 23 conformance gates CONFORMANT; v0.3.0 tagged (CR-BP-41)

---

## 1. Change Request

Land L3 Activity decompositions for the 9 Business Processes of AgencyAndOrganization's Improve and Operate stages.

Per-BP depositions (4 Activities each, 36 total):

| Coordinate | Business Process | Activities |
|---|---|---|
| A&O / Improve | `dea:process-develop-agents-and-organization` | Gather Development Drivers; Plan Agent Development; Execute Development Actions; Review Development Outcomes |
| A&O / Improve | `dea:process-conduct-engagement-and-alignment-review` | Collect Engagement Signals; Assess Agent Alignment; Formulate Engagement Findings; Commit Engagement Review Findings |
| A&O / Improve | `dea:process-conduct-capability-gap-analysis` | Baseline Population Competencies; Identify Capability Gaps; Prioritize Capability Gaps; Commit Gap Priorities |
| A&O / Improve | `dea:process-reorganize-structures` | Bound Reorganization Scope; Sequence Structure Transition; Execute Structure Transition; Record Accountability Handovers |
| A&O / Operate | `dea:process-operate-agent-performance` | Set Performance Expectations; Monitor Agent Performance; Address Performance Exceptions; Review Agent Performance Cycles |
| A&O / Operate | `dea:process-operate-payroll-and-benefits` | Compute Cycle Payroll; Execute Disbursements; Administer Benefits; File Statutory Returns |
| A&O / Operate | `dea:process-operate-time-and-attendance` | Capture Time and Attendance; Validate Attendance Records; Resolve Attendance Exceptions; Feed Payroll Time Data |
| A&O / Operate | `dea:process-operate-learning-and-development` | Schedule Development Programmes; Deliver Learning Sessions; Record Programme Completion; Evaluate Programme Effectiveness |
| A&O / Operate | `dea:process-coordinate-collaboration` | Provision Collaboration Workspaces; Maintain Interaction Norms; Facilitate Cross-Team Interactions; Resolve Collaboration Frictions |

Every candidate was tested against the four L2 criteria (CR-BP-32 §5); all 36 FAIL Standalone Executability and Resource Dedication and classify as Activities. Cohesion scores (§6) are recorded per candidate in each research deposition.

## 2. Deposition mechanics (pattern per CR-BP-42 §2)

1. **Research deposition** per BP at `entities/v1-alpha/dea:process-<bp>/research/l3-candidate-universe.yaml` (+ state-directory README.md).
2. **Canonical landing**: one record per Activity, conforming to `schemas/entities/activity.schema.json`; `ecfConformance` blocks inherit each BP's own canonical coordinate identifier (read from the BP record, not assumed). All 36 records pass Draft-07 validation.
3. **Decomposition boundary**: all records carry `decomposition_boundary: l4-reached` (CR-BP-32 §12).
4. **Bidirectional traceability (ACT-010)**: each parent BP gains `metadata.activity_references[]` and a CR-BP-57 `change_history` entry. All 9 parent records carry the current metadata shape. Versions unchanged per SIV-004.
5. **Reconciliation artifacts**: baseline and conformance report regenerated (697 records, all at L4).
6. **Count assertion updates**: ACT suite 465 -> 501; EXE suite 626 -> 662; conformance-report test 661 -> 697.

## 3. Gate posture

- Gate [15] ACT-001..010 live run: **CONFORMANT, 501 Activity records, 0 findings**.
- Gate [8] ECF conformance: **662 entries conform** (was 626).
- Full suite: **23 gates, 0 blocking, 0 advisory failures**.

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `entities/v1-alpha/dea:activity-*/` (36 dirs) | NEW | Canonical Activity records (4 per BP) |
| `entities/v1-alpha/dea:process-<bp>/research/` (x9) | NEW | Depositions + READMEs |
| `entities/v1-alpha/dea:process-<bp>/dea:process-<bp>.yaml` (x9) | MOD | `metadata.activity_references[]` + CR-BP-57 change_history |
| `tests/test_check_activity_model.py` | MOD | Count assertions: 501 Activity records |
| `tests/test_check_execution_boundary.py` | MOD | Count assertions: 662 records checked |
| `tests/test_architectural_regression.py` | MOD | Conformance report: 697 records, all L4 |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated (9 mutated parent BP hash lines) |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated by gate [10]; 697 records |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 68 -> 69 |
| `change-requests/CR-BP-57-l3-ao-improve-operate-tranche.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-57 row added |

## 5. What this CR is NOT

- **NOT a Task (L4) landing.** All Activities terminate at `l4-reached`.
- **NOT a schema, validator-rule, CI, or gate change.** Wiring from CR-BP-42 is reused unchanged.
- **NOT a remediation of the dangling `dea:process-frame-financial-policy-thesis` composes reference** (queued separately; it sits in FinanceAndAccounting).

## 6. Acceptance criteria

1. All 36 new Activity records validate against `schemas/entities/activity.schema.json` (Draft-07).
2. `python3 scripts/check_activity_model.py` runs CONFORMANT: 501 Activity records, 0 findings.
3. Each of the 9 parent BPs declares its 4 Activity ids in `metadata.activity_references[]` (ACT-010).
4. `python3 scripts/check_ecf_conformance.py` reports 662 entries conform.
5. `python3 scripts/build_inventory.py --self-test --strict` passes after regeneration.
6. Full pytest suite passes; `scripts/conformance_result.py` remains CONFORMANT (23 gates).
7. `python3 scripts/check_cr_metadata.py` reports 0 new findings.
8. `python3 scripts/check_catalog_index.py --strict` passes (all 9 new research/ state directories carry README.md).
9. No validator-rule, schema, CI, or governance-decision change.

## 7. Result

CR-BP-57 lands L3 coverage for AgencyAndOrganization's Improve and Operate stages: 36 new canonical Activity records across 9 Business Processes, bringing the catalog to 501 Activity records at 0 findings against gate [15]. AgencyAndOrganization is the seventh and final fully L3-covered domain (5/5 coordinates, 18 BPs, 72 Activities): all seven ECF domains now carry full L0-to-L3 coverage (126 BPs, 501 Activities). The structured deposition pattern has held across sixteen slices without modification.
