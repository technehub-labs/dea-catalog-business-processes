# CR-BP-95: L0/L1 Conformance Gate

**Status**: Proposed
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-18
**Carrier**: Recon-programme implementation slice that lands the L0 Process Scope and L1 Process Group conformance gate. Establishes the L0 schema + validator + gate (PSCOPE-001..008) and extends the existing L1 gate with PG-009 (grouping_basis) and PG-010 (membership_criteria). Back-compat with all 48 existing PG records (the new L1 fields are OPTIONAL).
**Recon programme**: CR-BP-92 (Decomposition and Execution Boundary Hardening) §10; CR-BP-93 (Decomposition Semantic Contract) for normative-prose basis.
**Depends on**: CR-BP-12 (L1 Process Group validation baseline), CR-BP-92 (recon programme), CR-BP-93 (decomposition semantic contract).
**Lands against**: 48 canonical PG records, 139 canonical BP records, 35 canonical PC records, 553 canonical Activity records; 24 conformance gates CONFORMANT; v0.4.0 tagged; v0.4.0+3 commits on main (CR-BP-91 / -92 / -93).

---

## 1. Change Request

Land the L0/L1 conformance gate as the **schema + validator + tests + gate wire** for the recon-programme L0/L1 layer. Five distinct artifacts:

| Artifact | Status | Notes |
|---|---|---|
| `schemas/entities/process-scope.schema.json` | NEW | Draft-07 JSON Schema for L0 Process Scope entries. Mirrors the L1 PG schema shape; additionalProperties: false; discriminator `type: ProcessScope`. |
| `schemas/entities/process-group.schema.json` | MOD | Extended with OPTIONAL `grouping_basis` and `membership_criteria` blocks (PG-009, PG-010). |
| `scripts/check_process_scope.py` | NEW | L0 validator implementing PSCOPE-001..008. Honest no-records-found pass when the catalog has 0 L0 records. Self-test fixture covers bad + good + empty catalogs. |
| `scripts/check_process_group.py` | MOD | Extended with PG-009 (grouping_basis structure check) and PG-010 (membership_criteria structure check). Both OPTIONAL; existing 48 PG records remain conformant. Docstring updated; print line updated to `PASS (PG-001..010)`. |
| `scripts/conformance_result.py` | MOD | Wires new advisory **gate [20] Process Scope (PSCOPE-001..008)**. |
| `tests/test_check_process_scope.py` | NEW | 11 tests: pure-function unit, run_checks integration, live catalog assertion, CLI self-test. |
| `tests/test_check_process_group_pg95.py` | NEW | 8 tests for PG-009/010 back-compat + happy paths + failure paths. |
| `change-requests/CR-BP-95-l0-l1-conformance-gate.md` | NEW | Slice carrier CR (this document). |
| `change-requests/README.md` | MOD | CR-BP-95 row added. |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 103 -> 104. |

## 2. Deposition mechanics

1. **Schema-first.** The L0 schema lands before the L0 validator, mirroring the existing PG-schema-then-checker pattern. The PG schema extension lands before the PG checker extension.
2. **Validator second.** `check_process_scope.py` mirrors `check_process_group.py` shape: PSCOPE-001..008 mirror PG-001..008 with appropriate id-pattern + target-id adjustments.
3. **Tests third.** Lock the validator behaviour with two test files: 11 PSCOPE tests + 8 PG-009/010 tests = 19 new tests.
4. **Gate wire last.** `conformance_result.py` wires gate [20] as **advisory** (matches the spec: L0 has no records yet, so blocking is inappropriate; the gate is non-vacuous because it reports the honest no-records-found message rather than passing silently).
5. **Self-test.** `scripts/check_process_scope.py --self-test` exercises PSCOPE-001..008 on a deliberately broken catalog, then a fixed one, then an empty one. All three scenarios must return 0.
6. **Reconciliation artifacts.** No record-level changes; baseline and conformance report regenerate unchanged.
7. **Count assertions.** None changed.

## 3. Gate posture

- Gate [7] MECE (Process Group, CR-BP-12): **CONFORMANT, PASS (PG-001..010)** (extended baseline).
- Gate [20] Process Scope (PSCOPE-001..008, CR-BP-95): **CONFORMANT, no ProcessScope entries found; L0 layer intentionally pre-population per CR-BP-95; 48 Process Group records present and conformant under PG-001..010** (new advisory gate).
- Full suite: **20 gates, 0 blocking, 0 advisory failures**.

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `schemas/entities/process-scope.schema.json` | NEW | L0 Process Scope schema (Draft-07) |
| `schemas/entities/process-group.schema.json` | MOD | + `grouping_basis` + `membership_criteria` (OPTIONAL) |
| `scripts/check_process_scope.py` | NEW | PSCOPE-001..008 validator (18 KB) |
| `scripts/check_process_group.py` | MOD | + PG-009, + PG-010 |
| `scripts/conformance_result.py` | MOD | + Gate [20] Process Scope (advisory) |
| `tests/test_check_process_scope.py` | NEW | 11 tests |
| `tests/test_check_process_group_pg95.py` | NEW | 8 tests for PG-009/010 |
| `change-requests/CR-BP-95-l0-l1-conformance-gate.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-95 row added |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 103 -> 104 |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated (no record-level changes; SHA may differ on commit timestamp only) |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated by gate [10]; 788 records (unchanged) |

No canonical-record mutation. No BP identity change. No Activity record change. No count-assertion change.

## 5. What this CR is NOT

- **NOT a population slice.** No L0 canonical records land in CR-BP-95. The L0 layer is intentionally pre-population per the CR-BP-92 / CR-BP-93 design intent; population is the work of a future tranche.
- **NOT a re-opening of CR-BP-20 Option A.** The PG-009/010 vocabulary mirrors the existing `process_group_kind` vocabulary (CR-BP-12 §6) without changing it.
- **NOT a tightening of specialization validation.** Held under CR-BP-92 §21.
- **NOT a count-assertion update.** Counts unchanged.
- **NOT a backfill of the new PG fields.** Existing 48 PG records remain conformant without `grouping_basis` or `membership_criteria` (PG-009/010 are OPTIONAL). Backfill is the work of a future record-reconciliation slice (CR-BP-99 or a dedicated L1 enrichment tranche).

## 6. Acceptance criteria

1. `schemas/entities/process-scope.schema.json` exists and validates against Draft-07 (`additionalProperties: false`).
2. `scripts/check_process_scope.py` runs against the live catalog and reports the honest no-records-found message: `Process Scope validation: PASS (no ProcessScope entries found; L0 layer intentionally pre-population per CR-BP-95; 48 Process Group records present and conformant under PG-001..010).`
3. `scripts/check_process_scope.py --self-test` returns exit code 0 and the three self-test scenarios (bad catalog, fixed catalog, empty catalog) all pass.
4. `scripts/check_process_group.py` runs against the live catalog and reports `PASS (PG-001..010)`.
5. The 48 existing PG records remain conformant after the PG-009/010 extension (back-compat assertion: live catalog test in `test_check_process_group_pg95.py`).
6. `scripts/conformance_result.py` wires gate [20] as advisory; full suite reports 20 gates, 0 blocking, 0 advisory failures.
7. 19 new tests pass (`tests/test_check_process_scope.py` + `tests/test_check_process_group_pg95.py`).
8. CR-META gate reports 0 new findings on CR-BP-95.
9. Em-dash / en-dash audit: 0 violations in new prose (the GitHub language rule excludes fenced code blocks and inline code spans).

## 7. Result

CR-BP-95 lands the L0 Process Scope schema + validator + tests + gate wire, and extends the L1 Process Group validator with PG-009 (grouping_basis) and PG-010 (membership_criteria). Back-compat with all 48 existing PG records (the new L1 fields are OPTIONAL). The L0 layer is intentionally pre-population; population is the work of a future tranche. Gate [20] Process Scope is wired as advisory and reports the honest no-records-found message rather than passing silently. The 20-gate suite remains CONFORMANT (0 blocking, 0 advisory); `open_change_requests` 103 -> 104.
