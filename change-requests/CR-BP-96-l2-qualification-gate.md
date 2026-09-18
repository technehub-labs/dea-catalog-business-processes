# CR-BP-96: L2 Qualification Gate (BP-QUAL-001..012)

**Status**: Proposed
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-18
**Carrier**: Recon-programme implementation slice that extends the L2 Business Process qualification contract from BP-C1..C4 (CR-BP-34a) to BP-QUAL-001..012 (CR-BP-96). Six of the twelve BP-QUAL rules are aliases of the existing BP-C family; the remaining five (BP-QUAL-003/004/005/008/009) are advisory structure checks for OPTIONAL fields (inputs, transformation, outputs, responsibility, boundary). BP-QUAL-011 (Specialization Integrity) is deferred under CR-BP-92 §21.
**Recon programme**: CR-BP-92 §11; CR-BP-93 (decomposition semantic contract) §5.
**Depends on**: CR-BP-34a (BP-C1..C4 baseline), CR-BP-92 (recon programme), CR-BP-93 (decomposition semantic contract).
**Lands against**: 139 canonical BP records; 553 Activity records; 48 PG records; 35 PC records; 20 conformance gates CONFORMANT; v0.4.0 tagged; v0.4.0+5 commits on main (CR-BP-91 / -92 / -93 / -94 / -95).

---

## 1. Change Request

Extend the L2 qualification gate from BP-C1..C4 to BP-QUAL-001..012 per CR-BP-92 §11. The recon's 12 BP-QUAL rules map as follows:

| BP-QUAL rule | Recon scope | Mapping | Status |
| --- | --- | --- | --- |
| BP-QUAL-001 | Identity | alias of BP-C3 (Standalone Executability) | inherited |
| BP-QUAL-002 | Trigger | alias of BP-C1 (Input-Output Transformation) | inherited |
| BP-QUAL-003 | Input | new OPTIONAL field `inputs[]`; advisory structure check | NEW |
| BP-QUAL-004 | Transformation | new OPTIONAL field `transformation:`; advisory structure check | NEW |
| BP-QUAL-005 | Output | new OPTIONAL field `outputs[]`; advisory structure check | NEW |
| BP-QUAL-006 | Outcome | alias of BP-C1 (outcome) + BP-C2 (outcome_statement) | inherited |
| BP-QUAL-007 | Objective Contribution | alias of BP-C2 (Objective Contribution) | inherited |
| BP-QUAL-008 | Responsibility | new OPTIONAL field `responsibility:`; advisory structure check | NEW |
| BP-QUAL-009 | Boundary | new OPTIONAL field `boundary:`; advisory structure check | NEW |
| BP-QUAL-010 | Standalone Process Integrity | alias of BP-C3 | inherited |
| BP-QUAL-011 | Specialization Integrity | deferred under CR-BP-92 §21 | DEFERRED |
| BP-QUAL-012 | Evidence | alias of BP-C4 (Resource Dedication) | inherited |

The five new advisory checks (BP-QUAL-003/004/005/008/009) pass vacuously when the underlying field is absent on a BP record (back-compat rule per CR-BP-95). When the field IS present, structure is enforced.

## 2. Deposition mechanics (pattern per CR-BP-92 §11)

1. **Extend the existing BP-C1..C4 validator** (`scripts/check_l2_qualification.py`) rather than introduce a parallel script. The CR-BP-92 §16 conformance architecture requires new validators to participate in the existing Structural / Semantic / Naming / Boundary / MECE / Referential Integrity / Cross-Repository Integrity / ECF Conformance framework.
2. **Five new checks** added to `_RULES`: `_check_bp_qual_003` (inputs), `_check_bp_qual_004` (transformation), `_check_bp_qual_005` (outputs), `_check_bp_qual_008` (responsibility), `_check_bp_qual_009` (boundary).
3. **Six alias mappings** added to `_BP_QUAL_ALIASES`: BP-QUAL-001/002/006/007/010/012 inherit the BP-C family verdict without re-running.
4. **BP-QUAL-011 deferred** under CR-BP-92 §21 (specialization carve-out). Recon-side note in print output explicitly marks this.
5. **Advisory tagging** in `evaluate()`: BP-QUAL findings carry `advisory: True`; the `--strict` mode only fails on mandatory (BP-C) findings.
6. **Tests** extended: 14 new BP-QUAL test cases added to `tests/test_check_l2_qualification.py`; live-catalog assertion confirms 139 records emit zero findings across the extended rule set.
7. **Template** extended: `templates/business-process.yaml` documents the OPTIONAL `inputs` / `transformation` / `outputs` / `responsibility` / `boundary` blocks with BP-QUAL-003/004/005/008/009 rule citations.
8. **No schema, gate wire, or canonical-record mutation.** The BP records have no JSON Schema file today; the validator is the de-facto contract.
9. **No count-assertion change.** Counts unchanged.
10. **Reconciliation artifacts.** `baseline/v1.yaml` and `conformance_report.yaml` regenerate unchanged.

## 3. Gate posture

- Gate [11] L2 Qualification (CR-BP-34a BP-C1..C4 + CR-BP-96 BP-QUAL-001..012): **CONFORMANT, 139 records, 0 findings**.
- BP-QUAL alias map printed in validator output for transparency.
- BP-QUAL-011 (Specialization Integrity) explicitly marked DEFERRED in validator output.
- Full suite: **20 gates, 0 blocking, 0 advisory** (unchanged).
- CR-META: **0 new findings** (CR-BP-96 contributes 0 new findings).

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `scripts/check_l2_qualification.py` | MOD | + BP-QUAL-003/004/005/008/009 checks; + `_BP_QUAL_ALIASES` map; + advisory tagging in `evaluate()`; + alias/deferred reporting in `main()` |
| `tests/test_check_l2_qualification.py` | MOD | + 14 BP-QUAL test cases (vacuous, fail, pass) + alias map assertions + advisory tagging assertions; docstring + JSON payload assertion updated for the new rule family |
| `templates/business-process.yaml` | MOD | + OPTIONAL `inputs` / `transformation` / `outputs` / `responsibility` / `boundary` blocks with BP-QUAL-003/004/005/008/009 rule citations; docstring updated to cite CR-BP-96 |
| `change-requests/CR-BP-96-l2-qualification-gate.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-96 row added before `## Cross-repo context` |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 105 -> 106 |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated (no record-level changes) |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated by gate [10]; 788 records (unchanged) |

No canonical-record mutation. No gate wire change (existing gate [11] now reports BP-QUAL coverage; no new gate). No count-assertion change.

## 5. What this CR is NOT

- **NOT a canonical-record change.** No BP records are touched. The OPTIONAL fields are documented in the template but not backfilled across the existing 139 records.
- **NOT a re-opening of CR-BP-20 Option A.**
- **NOT a tightening of specialization validation.** BP-QUAL-011 deferred under CR-BP-92 §21.
- **NOT a schema change.** BP records have no JSON Schema file today; the validator is the de-facto contract.
- **NOT a count-assertion update.** Counts unchanged.

## 6. Acceptance criteria

1. `scripts/check_l2_qualification.py` runs against the live catalog and reports **CONFORMANT, 139 records, 0 findings** across BP-C1..C4 + BP-QUAL-001..012.
2. `scripts/check_l2_qualification.py --self-test` returns 0.
3. `scripts/check_l2_qualification.py --json` emits a payload whose `rules` array contains 9 entries: BP-C1..C4 + BP-QUAL-003/004/005/008/009.
4. BP-QUAL findings carry `advisory: True`; `--strict` does not exit non-zero when only advisory findings are present.
5. BP-QUAL-011 (Specialization Integrity) is explicitly marked DEFERRED in the validator output.
6. `tests/test_check_l2_qualification.py` reports 32 tests pass (existing 18 + 14 new BP-QUAL tests).
7. `templates/business-process.yaml` documents the OPTIONAL `inputs` / `transformation` / `outputs` / `responsibility` / `boundary` blocks with BP-QUAL-003/004/005/008/009 rule citations.
8. `python3 scripts/check_cr_metadata.py` reports 0 new findings on CR-BP-96.
9. Em-dash / en-dash audit: 0 violations in new prose.
10. Full pytest suite passes (pre-existing `test_dispositions::test_tranche_count_is_ten` failure unchanged; NOT introduced by this slice).

## 7. Result

CR-BP-96 extends the L2 Business Process qualification gate from BP-C1..C4 to BP-QUAL-001..012 per CR-BP-92 §11. Six of the twelve BP-QUAL rules are aliases of the existing BP-C family; five are advisory structure checks for OPTIONAL fields (BP-QUAL-003/004/005/008/009); one (BP-QUAL-011 Specialization Integrity) is deferred under CR-BP-92 §21. The 14 new BP-QUAL tests pass; the live catalog (139 records) emits zero findings across the extended rule set. The 20-gate suite remains CONFORMANT (0 blocking, 0 advisory); `open_change_requests` 105 -> 106.
