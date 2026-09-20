# CR-BP-79 - L3 Activity G&E-Retire Admission Tranche (Regulator-Mandated Governance Unwind)

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
**Date**: 2026-09-16
**Carrier**: Fourth L3 (Activity) tranche landing after CR-BP-77; closes the final L3 gap created by the CR-BP-78 admission tranche at the GovernanceAndExistence x Retire coordinate.
**Depends on**: CR-BP-32 (Activity Model; ACT-001..010), CR-BP-42 (pilot), CR-BP-43..57 (per-stage L3 tranches), CR-BP-69 (first admitted-BP decomposition tranche), CR-BP-77 (second admitted-BP decomposition tranche), CR-BP-70/-72/-74/-76 (escape-c discoveries at P&R Activate, A&O Retire, F&A Retire, G&E Retire), CR-BP-71/-73/-75/-78 (admission tranches at the four discovery-driven cells).
**Lands against**: 135 canonical BP records, 44 canonical PG records, 537 canonical Activity records, 18 canonical Discovery records; full pytest suite + CR-META + catalog-index gates CONFORMANT.

---

## 1. Change Request

Land L3 Activity decompositions for the Business Process admitted by the G&E x Retire admission tranche (CR-BP-78) and not yet decomposed to Activities. The BP gains 4 Activity records derived from the BP's trigger and outcome text using the L2 criteria in CR-BP-32 section 5. Every candidate FAILS Standalone Executability and Resource Dedication and therefore classifies as an Activity, not a BP. Cohesion score 9/9 on each (single concern, single input class, single output).

The four Activity records are:

| Activity | Source clause (BP outcome) |
|---|---|
| Assess Regulator Or Court Order Scope | "binding regulator or court order"; interpretive concern at intake |
| Reduce Governance To Wind-Down Quorum | "Governance bodies are reduced to a wind-down quorum"; "Policy instruments are sunset or superseded by wind-down procedures" |
| Submit Statutory Dissolution Filings | "Statutory dissolution filings ... are submitted to the relevant regulator or court" |
| Assign Retained-Records Custodianship | "Retained-records custodianship is assigned" |

## 2. Slice Mechanics

- **Deposition first**: `entities/v1-alpha/dea:process-effect-regulator-mandated-governance-unwind/research/l3-candidate-universe.yaml` + `research/README.md` (one BP, four candidates).
- **Canonical landing**: 4 Activity YAML records under `entities/v1-alpha/dea:activity-<slug>/dea:activity-<slug>.yaml`. Each Activity inherits the parent BP's `ecfConformance` block (GovernanceAndExistence x Retire; identifier `ecf:governanceExistence.retire`).
- **Parent BP patch**: `metadata.activity_references[]` (4 entries) inserted immediately after `established_at:`; a new `change_history` entry appended to `metadata.change_history[]` immediately before the top-level `links:` block. Version UNCHANGED per SIV-004 (additive metadata-only).
- **Count-assertion sweep**: ACT-001..010, EXE-001..010, ECF conformance, conformance_report triple; 7 sites bumped (test_check_activity_model ×3, test_check_execution_boundary ×3, test_architectural_regression ×2).
- **Carrier CR + README row**: `change-requests/CR-BP-79-l3-ge-retire-admission.md` (this file); README row inserted before the `## Cross-repo context` anchor.
- **Regen cascade**: `build_inventory.py` → `build_inventory.py --self-test --strict` PASS → `build_conformance_report.py` → `regenerate_catalog.py --schema catalog-index-schema/catalog-index-schema.json` → post-commit regen + amend.

## 3. Gate Posture

- ACT-001..010 (Activity Model): CONFORMANT, 537 Activity records, 135 BP records, 0 findings.
- EXE-001..010 (Execution Boundary): CONFORMANT, 716 records, 0 findings.
- ECF conformance: PASS, 716 conform entries.
- CR-META: 0 NEW findings (19 pre-existing legacy unchanged).
- Schema catalog-index: PASS (716 entities).
- Schema validate-process-entries: PASS.
- 24-gate conformance_result suite: CONFORMANT, 0 blocking, 0 advisory.
- targeted pytest (5 files): 99/99 PASS.

## 4. Repo Changes

| Path | Change |
|---|---|
| `entities/v1-alpha/dea:activity-assess-regulator-order-scope/dea:activity-assess-regulator-order-scope.yaml` | new Activity |
| `entities/v1-alpha/dea:activity-reduce-governance-to-wind-down-quorum/dea:activity-reduce-governance-to-wind-down-quorum.yaml` | new Activity |
| `entities/v1-alpha/dea:activity-submit-statutory-dissolution-filings/dea:activity-submit-statutory-dissolution-filings.yaml` | new Activity |
| `entities/v1-alpha/dea:activity-assign-retained-records-custodianship/dea:activity-assign-retained-records-custodianship.yaml` | new Activity |
| `entities/v1-alpha/dea:process-effect-regulator-mandated-governance-unwind/research/l3-candidate-universe.yaml` | new research deposition |
| `entities/v1-alpha/dea:process-effect-regulator-mandated-governance-unwind/research/README.md` | new research README (overwritten with L3 summary; L2-admission-deposition untouched) |
| `entities/v1-alpha/dea:process-effect-regulator-mandated-governance-unwind/dea:process-effect-regulator-mandated-governance-unwind.yaml` | `metadata.activity_references[]` + new `change_history` entry (version UNCHANGED) |
| `reconciliation/inventory.yaml` | regenerated |
| `reconciliation/baseline/v1.yaml` | regenerated (immutable SHA unchanged) |
| `reconciliation/conformance_report.yaml` | regenerated (756 -> 760 records) |
| `CATALOG.yaml` | regenerated (712 -> 716 entities; open_change_requests 90 -> 91) |
| `tests/test_check_activity_model.py` | count assertions 533 -> 537; docstring narrative |
| `tests/test_check_execution_boundary.py` | count assertions 710 -> 716; docstring narrative |
| `tests/test_architectural_regression.py` | 756 -> 760 |
| `change-requests/CR-BP-79-l3-ge-retire-admission.md` | new (this file) |
| `change-requests/README.md` | row added for CR-BP-79 |

## 5. NOT-List (Out of Scope)

- **L4 Task records.** `dea:Task` is metamodel-owned, lifecycle: proposed; CR-BP-79 sets `decomposition_boundary: l4-reached` on each Activity per ACT-004.
- **Discovery-record mutations.** No new discovery files; no flip of any cell in the L1 register; no dispositions register or tranches plan changes (these were settled in CR-BP-76/-78).
- **Specialization.** No `process_specialization` entries added (no pattern-based refinement candidates).
- **PG/PC stack.** The PC + PG + BP stack landed in CR-BP-78; CR-BP-79 only adds L3 decomposition.

## 6. Acceptance Criteria

- 4 Activity records land with cohesion 9/9, all FAIL standalone executability + resource dedication per CR-BP-32 section 5.
- Parent BP record's `metadata.activity_references[]` lists exactly the 4 new Activity ids; `metadata.change_history[]` gains a CR-BP-79 entry; `version: 1.0.0` UNCHANGED.
- ACT-001..010 CONFORMANT 0 findings; EXE-001..010 CONFORMANT 0 findings; ECF conformance PASS.
- Count assertions bumped (Activity 533 -> 537; EXE 710 -> 716; conformance report 756 -> 760).
- All seven canonical domains covered end-to-end at L0-L3.
- 24-gate conformance_result suite: CONFORMANT, 0 blocking, 0 advisory.
- targeted pytest: 99/99 PASS.
- CATALOG regenerated; `open_change_requests` 90 -> 91.

## 7. Result

**L0-L3 coverage:** 7/7 domains fully populated. The four discovery-driven admission tranches (CR-BP-71 P&R Activate, CR-BP-73 A&O Retire, CR-BP-75 F&A Retire, CR-BP-78 G&E Retire) each have L3 Activity decompositions under CR-BP-77 (12 records, three BPs) and CR-BP-79 (4 records, one BP). The Process Catalog now has the maximum cells populated end-to-end at every layer (L0 Discovery, L1 PC + PG, L2 BP, L3 Activity).