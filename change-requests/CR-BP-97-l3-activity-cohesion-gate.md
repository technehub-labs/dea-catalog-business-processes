# CR-BP-97: L3 Activity Cohesion and Decomposition Gate

**Status**: Proposed
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-18
**Carrier**: Recon-programme implementation slice that extends the L3 Activity Model gate from ACT-001..010 (CR-BP-32) to ACT-011..015 (CR-BP-97). Five new advisory structure checks for OPTIONAL fields on the Activity record: ACT-011 (cohesive work statement adequacy, definition >= 120 chars), ACT-012 (inputs/outputs integrity), ACT-013 (outcome contribution), ACT-014 (boundary and exclusions), ACT-015 (sibling distinction). ACT-016..020 from the recon are covered by existing ACT-004 / ACT-010; CR-BP-97 reconciles the prose rather than introducing net-new rules.
**Recon programme**: CR-BP-92 §12; CR-BP-93 (decomposition semantic contract) §6.
**Depends on**: CR-BP-32 (ACT-001..010 baseline), CR-BP-92 (recon programme), CR-BP-93 (decomposition semantic contract).
**Lands against**: 553 canonical Activity records; 139 canonical BP records; 48 canonical PG records; 35 canonical PC records; 20 conformance gates CONFORMANT; v0.4.0 tagged; v0.4.0+6 commits on main.

---

## 1. Change Request

Extend the L3 Activity Model gate from ACT-001..010 to ACT-011..015 per CR-BP-92 §12:

| ACT-011 rule | Recon scope | Status |
| --- | --- | --- |
| ACT-011 | Cohesive work statement adequacy (extends ACT-003; definition >= 120 chars; skips deprecated/retired) | NEW (advisory) |
| ACT-012 | Inputs/Outputs integrity (OPTIONAL `inputs[]` / `outputs[]`; structure check when present) | NEW (advisory) |
| ACT-013 | Outcome contribution (OPTIONAL `outcome_contribution:`; non-empty string when present) | NEW (advisory) |
| ACT-014 | Boundary and exclusions (OPTIONAL `boundary:`; non-empty string or object) | NEW (advisory) |
| ACT-015 | Sibling distinction (cross-record; duplicate name in same parent BP) | NEW (advisory) |

ACT-016..020 from the recon programme are covered by existing ACT-004 (Task decomposition integrity) and ACT-010 (Activity traceability); CR-BP-97 reconciles the prose rather than introducing net-new rules for these.

All five new ACT-011..015 checks are advisory; the underlying OPTIONAL fields are absent on all 553 existing Activity records (back-compat rule per CR-BP-95). The slice surfaces the documented advisory findings (9 existing Activity records have `definition:` < 120 chars) without blocking.

## 2. Deposition mechanics (pattern per CR-BP-92 §12)

1. **Extend the existing ACT-001..010 validator** (`scripts/check_activity_model.py`) rather than introduce a parallel script. The CR-BP-92 §16 conformance architecture requires new validators to participate in the existing Structural / Semantic / Naming / Boundary / MECE / Referential Integrity / Cross-Repository Integrity / ECF Conformance framework.
2. **Five new checks** added to `_RULES_RECORD`: `_check_act_011` (definition minimum), `_check_act_012` (inputs/outputs), `_check_act_013` (outcome_contribution), `_check_act_014` (boundary), `_check_act_015` (sibling distinction).
3. **Cross-record check (ACT-015).** The `evaluate()` function populates an in-memory `_SIBLING_INDEX` from the activity records themselves, then `_check_act_015` looks up duplicates by (parent_bp_id, activity_name).
4. **Advisory tagging** in `evaluate()`: ACT-011..015 findings carry `advisory: True`; the `--strict` mode only fails on mandatory findings.
5. **Verdict semantics updated.** `_verdict()` now filters to mandatory findings only; advisory findings are surfaced for transparency but do not change the verdict from CONFORMANT. This mirrors the BP-QUAL design from CR-BP-96.
6. **Tests** extended: 12 new ACT-011..015 test cases added to `tests/test_check_activity_model.py` (46 total); live-catalog assertion confirms 9 documented advisory ACT-011 findings; `--strict` does not exit non-zero.
7. **Template** extended: `templates/activity.yaml` documents the OPTIONAL `inputs` / `outputs` / `outcome_contribution` / `boundary` blocks with ACT-012/013/014 rule citations.
8. **No schema, gate wire, or canonical-record mutation.** Existing gate [15] (Activity Model) now reports ACT-011..015 coverage; no new gate.
9. **No count-assertion change.** Counts unchanged.
10. **Reconciliation artifacts.** `baseline/v1.yaml` and `conformance_report.yaml` regenerate unchanged.

## 3. Gate posture

- Gate [15] Activity Model (CR-BP-32 ACT-001..010 + CR-BP-97 ACT-011..015): **CONFORMANT** (advisory ACT-011 findings do not change the verdict).
- 9 documented advisory ACT-011 findings (existing Activity records whose `definition:` is < 120 chars) are surfaced for transparency. Backfill is the work of CR-BP-99.
- `--strict` exits 0 because all 9 findings are advisory (CR-BP-97 design intent).
- Full suite: **20 gates, 0 blocking, 0 advisory** (unchanged).
- CR-META: **0 new findings** (CR-BP-97 contributes 0 new findings).

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `scripts/check_activity_model.py` | MOD | + ACT-011..015 checks; + `_SIBLING_INDEX` cross-record index; + advisory tagging in `evaluate()`; + `_verdict()` filters mandatory findings; + `--strict` only fails on mandatory findings; + alias map / advisory markers in `main()` print output |
| `tests/test_check_activity_model.py` | MOD | + 12 ACT-011..015 test cases (vacuous, fail, pass, alias, advisory-tagging, live-catalog assertions); live-catalog assertion updated to expect the 9 documented advisory ACT-011 findings; rule-set metadata assertion extended |
| `templates/activity.yaml` | MOD | + OPTIONAL `inputs` / `outputs` / `outcome_contribution` / `boundary` blocks with ACT-012/013/014 rule citations; docstring updated to cite CR-BP-97 |
| `change-requests/CR-BP-97-l3-activity-cohesion-gate.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-97 row added before `## Cross-repo context` |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 106 -> 107 |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated (no record-level changes) |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated by gate [10]; 788 records (unchanged) |

No canonical-record mutation. No schema change. No gate wire change. No count-assertion change.

## 5. What this CR is NOT

- **NOT a canonical-record change.** No Activity records are touched. The OPTIONAL fields are documented in the template but not backfilled across the existing 553 records.
- **NOT a re-opening of CR-BP-20 Option A.**
- **NOT a tightening of specialization validation.** Held under CR-BP-92 §21.
- **NOT a schema change.** Activity records are governed by `schemas/entities/activity.schema.json`; no new schema fields introduced.
- **NOT a count-assertion update.** Counts unchanged.

## 6. Acceptance criteria

1. `scripts/check_activity_model.py` runs against the live catalog and reports **CONFORMANT** with 9 documented advisory ACT-011 findings.
2. `scripts/check_activity_model.py --strict` returns exit code 0 (advisory findings are non-blocking).
3. `scripts/check_activity_model.py --self-test` returns 0.
4. `scripts/check_activity_model.py --json` emits a payload whose `rules` array contains ACT-001..009 + ACT-011..015 (15 entries).
5. ACT-011..015 findings carry `advisory: True`; ACT-001..009 + ACT-010 findings are mandatory.
6. `tests/test_check_activity_model.py` reports 46 tests pass (existing 34 + 12 new ACT-011..015 tests).
7. `templates/activity.yaml` documents the OPTIONAL `inputs` / `outputs` / `outcome_contribution` / `boundary` blocks with ACT-012/013/014 rule citations.
8. `python3 scripts/check_cr_metadata.py` reports 0 new findings on CR-BP-97.
9. Em-dash / en-dash audit: 0 violations in new prose.
10. Full pytest suite passes (pre-existing `test_dispositions::test_tranche_count_is_ten` failure unchanged; NOT introduced by this slice).

## 7. Result

CR-BP-97 extends the L3 Activity Model gate from ACT-001..010 to ACT-011..015 per CR-BP-92 §12. Five new advisory structure checks for OPTIONAL fields (ACT-011/012/013/014/015); ACT-016..020 are covered by existing ACT-004/010. The 12 new ACT-011..015 tests pass; the live catalog (553 records) emits 9 documented advisory ACT-011 findings that do not change the CONFORMANT verdict. The 20-gate suite remains CONFORMANT (0 blocking, 0 advisory); `open_change_requests` 106 -> 107.
