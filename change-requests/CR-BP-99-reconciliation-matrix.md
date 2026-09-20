# CR-BP-99: Schema/Validator/Documentation/Records Reconciliation Matrix

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Proposed
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-18
**Recon programme parents**: CR-BP-92 §16 (recon programme closure), CR-BP-91..98 + EXT-01..01a.
**Sub-pipeline**: CR-BP-99 (this slice). EXT-02..06 are downstream.
**Lands against**: 740 entities / 789 conformance records / 28 gates CONFORMANT / v0.4.0 tagged.

---

## 1. Change Request

Establish the **canonical reconciliation matrix** that catalogues every advisory finding + pre-existing inconsistency surfaced during CR-BP-91..98 + EXT-01..01a, and assigns each row a disposition (backfill / defer / accept_as_is / relax_rule) with an owner CR / EXT / future slice.

### 1.1 What this slice lands

1. **`reconciliation/cr-bp-99-matrix.yaml`** (NEW, ~440 lines): the matrix itself.
   - 20 rows total: 9 backfills (matrix-001..009), 7 deferrals (matrix-010..016), 4 accept_as_is certifications (matrix-017..020).
   - `summary` block with by_disposition + by_status + open_owners.
   - 7 invariants that future slices must honour (e.g., matrix-001..009 MUST be `status: closed` after CR-BP-99 lands).

2. **9 ACT-011 backfills** on the Activity records identified by the matrix:
   - `dea:activity-calculate-compensation`: definition 113 -> 182 chars
   - `dea:activity-commit-agent-topology`: 117 -> 172 chars
   - `dea:activity-commit-role-catalogue`: 117 -> 172 chars
   - `dea:activity-disburse-payroll`: 116 -> 178 chars
   - `dea:activity-execute-payments-to-plan`: 114 -> 178 chars
   - `dea:activity-fit-out-facilities`: 114 -> 170 chars
   - `dea:activity-manage-collections`: 119 -> 162 chars
   - `dea:activity-resolve-attendance-exceptions`: 115 -> 178 chars
   - `dea:activity-score-finding-severity`: 112 -> 174 chars
   - Each record's `metadata.change_history` carries a `CR-BP-99` entry at the top documenting the backfill.

3. **`scripts/check_reconciliation_matrix.py`** (NEW, ~440 lines, RCM-001..010): matrix validator with self-test, JSON mode, and live-matrix mode. Ten rules lock the schema, the row fields, the disposition / status / category enums, the row id format, the row uniqueness, the closed-row requirement, the summary-count consistency, and the invariant presence.

4. **Gate [23] Reconciliation Matrix (RCM-001..010)** in `scripts/conformance_result.py`. The gate is **advisory** because the matrix is informational: errors are blocking, warnings are advisory. Today the matrix has 0 errors and 0 warnings.

5. **37 new tests** in `tests/test_check_reconciliation_matrix.py`: constants, helper checks, per-rule tests, aggregate `evaluate()` + `verdict()`, CLI self-test, JSON shape, live-matrix integrity (row count, summary counts, ACT-011 backfill coverage).

### 1.2 What this slice does NOT land

- **NOT an EXT-06 slice.** Documentation authoring (closing the 2,306 DOC-001/002/003/005 advisory hits) belongs to EXT-06. CR-BP-99 only catalogues those findings and assigns them to EXT-06.
- **NOT a fix for the pre-existing test_dispositions drift.** The `78 vs 73` assertion drift on `test_tranche_count_is_ten` is recorded in matrix-016 as `pre_existing / defer / future_slice`. The repair is a separate Process-Catalog-layer CR (surgical-change discipline).
- **NOT a tightening of specialization validation.** Held under CR-BP-92 §21.
- **NOT a backfill of OPTIONAL fields.** BP-QUAL-003/004/005/008/009 and ACT-012/013/014/015 have 0 advisory findings; the OPTIONAL fields are absent but the records are conformant per the back-compat pattern (CR-BP-95/96/97). Field population belongs to EXT-06 or a future content tranche.
- **NOT a count-assertion change.** No new canonical-entity records are introduced. The 9 ACT-011 backfills only expand existing `definition` strings.

## 2. Deposition mechanics (pattern per CR-BP-92 §16)

1. **Matrix is authoritative prose** (`reconciliation/cr-bp-99-matrix.yaml`). The validator enforces the schema-derived invariants. Future slices MUST honour the matrix's disposition + owner assignments.
2. **Validator is advisory** (gate [23]). Errors block; warnings do not. Today the matrix has 0 errors / 0 warnings.
3. **Backfill is content.** Each of the 9 ACT-011 backfills is a natural-language elaboration that preserves the original meaning while raising the definition to the 120-char minimum.
4. **No count-assertion change.** `open_change_requests` 110 -> 111.

## 3. Matrix composition (20 rows)

| Id range | Category | Disposition | Owner | Count |
|---|---|---|---|---|
| matrix-001..009 | act_backfill | backfill | CR-BP-99 (this slice) | 9 (closed) |
| matrix-010..013 | doc_deferred | defer | EXT-06 | 4 (open) |
| matrix-014 | bp_qual_deferred | accept_as_is | CR-BP-96 | 1 (open) |
| matrix-015 | act_optional_deferred | accept_as_is | CR-BP-97 | 1 (open) |
| matrix-016 | pre_existing | defer | future_slice | 1 (open) |
| matrix-017 | pg_conformant | accept_as_is | CR-BP-95 | 1 (closed) |
| matrix-018 | pscope_conformant | accept_as_is | CR-BP-95 | 1 (closed) |
| matrix-019 | task_conformant | accept_as_is | CR-BP-98 | 1 (closed) |
| matrix-020 | doc_validator_state | accept_as_is | CR-BP-94-EXT-01 | 1 (closed) |

By status: 13 closed (this slice landed), 7 open (downstream).
By disposition: 9 backfill, 5 defer, 6 accept_as_is.

## 4. Gate posture

- Gate [23] Reconciliation Matrix (RCM-001..010): **CONFORMANT** (PASS/ADVISORY). 0 errors / 0 warnings.
- Full suite: **28 gates, 0 blocking, 0 advisory** failures.
- CR-META: 0 new findings.

## 5. Repository changes

| Path | Status | Notes |
|---|---|---|
| `reconciliation/cr-bp-99-matrix.yaml` | NEW | Reconciliation matrix (~440 lines, 20 rows, 7 invariants) |
| `entities/v1-alpha/dea:activity-calculate-compensation/dea:activity-calculate-compensation.yaml` | MOD | ACT-011 backfill (definition 113 -> 182 chars) |
| `entities/v1-alpha/dea:activity-commit-agent-topology/dea:activity-commit-agent-topology.yaml` | MOD | ACT-011 backfill (117 -> 172 chars) |
| `entities/v1-alpha/dea:activity-commit-role-catalogue/dea:activity-commit-role-catalogue.yaml` | MOD | ACT-011 backfill (117 -> 172 chars) |
| `entities/v1-alpha/dea:activity-disburse-payroll/dea:activity-disburse-payroll.yaml` | MOD | ACT-011 backfill (116 -> 178 chars) |
| `entities/v1-alpha/dea:activity-execute-payments-to-plan/dea:activity-execute-payments-to-plan.yaml` | MOD | ACT-011 backfill (114 -> 178 chars) |
| `entities/v1-alpha/dea:activity-fit-out-facilities/dea:activity-fit-out-facilities.yaml` | MOD | ACT-011 backfill (114 -> 170 chars) |
| `entities/v1-alpha/dea:activity-manage-collections/dea:activity-manage-collections.yaml` | MOD | ACT-011 backfill (119 -> 162 chars) |
| `entities/v1-alpha/dea:activity-resolve-attendance-exceptions/dea:activity-resolve-attendance-exceptions.yaml` | MOD | ACT-011 backfill (115 -> 178 chars) |
| `entities/v1-alpha/dea:activity-score-finding-severity/dea:activity-score-finding-severity.yaml` | MOD | ACT-011 backfill (112 -> 174 chars) |
| `scripts/check_reconciliation_matrix.py` | NEW | RCM-001..010 matrix validator (~440 lines) |
| `scripts/conformance_result.py` | MOD | + gate [23] Reconciliation Matrix (advisory) |
| `tests/test_check_reconciliation_matrix.py` | NEW | 37 tests |
| `change-requests/CR-BP-99-reconciliation-matrix.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-99 row added before `## Cross-repo context` |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 110 -> 111 |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated (no entity-level changes; +0 entities; +0 conformance records; only `definition` expansions on 9 existing Activity records) |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated |

No canonical-entity mutation. No new entity records. No schema change.

## 6. Acceptance criteria

1. `reconciliation/cr-bp-99-matrix.yaml` is well-formed and parses via `yaml.safe_load`.
2. Matrix has 20 rows; 9 backfills / 5 defers / 6 accept_as_is; 13 closed / 7 open.
3. `scripts/check_reconciliation_matrix.py --self-test` passes.
4. `scripts/check_reconciliation_matrix.py` against the live matrix returns CONFORMANT (0 errors / 0 warnings).
5. Gate [23] Reconciliation Matrix is wired as **advisory** in `scripts/conformance_result.py`; the suite remains CONFORMANT (28 gates, 0 blocking, 0 advisory failures).
6. ACT-011 advisory findings on the 9 backfilled records drop from 9 to 0 (live catalog assertion).
7. `tests/test_check_reconciliation_matrix.py` reports 37 tests pass.
8. CR-BP-99 carrier CR is filed in `change-requests/`.
9. README row + CATALOG regen is committed.
10. Em-dash / en-dash audit: 0 violations in new prose.
11. Full pytest suite passes (pre-existing `test_dispositions::test_tranche_count_is_ten` failure unchanged; NOT introduced by this slice; recorded in matrix-016 as `pre_existing / defer / future_slice`).
12. Each of the 9 backfilled records carries a CR-BP-99 entry in `metadata.change_history`.

## 7. Result

CR-BP-99 closes the recon programme reconciliation work. The matrix is the authoritative catalogue of advisory findings + dispositions; the 9 ACT-011 backfills land in this slice; the 7 deferred items have explicit owners (EXT-06, CR-BP-96, CR-BP-97, future_slice). The 28-gate suite remains CONFORMANT. `open_change_requests` 110 -> 111. The recon programme (CR-BP-91..99 + EXT-01..01a) is now complete; the open work belongs to the documentation sub-pipeline (EXT-02..06) and any future content / repair CRs.