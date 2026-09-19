# CR-BP-100a: L0↔L1 Cardinality Gate :  49-Cell Assertion Update

**Status**: Proposed
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-19
**Carrier**: Surgical atomic follow-up to CR-BP-100. Updates the cardinality gate's live-catalog test counts from 48 → 49 after CR-BP-101 (SD/Retire admission tranche) closed the 7x7 = 49-cell ECF matrix. Validator logic unchanged.
**Depends on**: CR-BP-100 (L0↔L1 cardinality gate; PR #141), CR-BP-101 (SD/Retire admission tranche; PR #142).
**Lands against**: 49 PCs / 49 PGs / 140 BPs / 553 Activities / 0 ProcessScope records; 29 gates CONFORMANT; v0.4.0+12 commits on main (post-CR-BP-101).

**Authoritative decomposition doctrine (eaojnr 2026-09-19):**
- L0 = Process Context (49 canonical cells: 7 ECF domains x 7 lifecycle stages).
- L1 = Process Group (49 canonical records; one per L0 cell; 1:1 cardinality is the canonical invariant).
- L2 = Business Process (140 canonical records; the L1's compose surfaces invert deployment per CR-BP-12 §4).
- L3 = Activity (553 canonical records; decomposition continues downstream of L2).
- L4 = Task (0 records; canonical shape established by CR-BP-98; first L4 tranche is downstream).
- The cardinality invariant is enforced by automated gate [24] (L0L1-CARD-001..003), which validates every PC and every PG pairwise in live tests against the 49-cell matrix.
- The ProcessScope (`dea:scope-*`) layer from CR-BP-95 is dormant by design (L0L1-CARD-003): zero records instantiated; admission requires an explicit CR.

---

## 1. Change Request

Update CR-BP-100's **test assertions** from 48 → 49 so the live-catalog exhaustive audits pass against the now-complete matrix. Validator logic, gate wiring, reconciliation matrix, and CLI behaviour are unchanged. Five distinct artifacts:

| Artifact | Status | Notes |
|---|---|---|
| `tests/test_check_l0_l1_cardinality.py` | MOD | `test_live_total_counts` asserts `len(pc_ids) == 49` and `len(groups) == 49` (was 48). Docstring + module docstring + coverage list updated 48 → 49 throughout. |
| `change-requests/CR-BP-100-l0-l1-cardinality-gate.md` | MOD | Prose counts and "Lands against" sentence updated 48 → 49. Doctrine paragraph notes "the 49 canonical groups in `entities/v1-alpha/`, one per ECF cell" (was 48). `open_change_requests` progression corrected 111 → 112 to 113 → 114. |
| `change-requests/CR-BP-100a-cardinality-49-update.md` | NEW | Slice carrier CR (this document). |
| `change-requests/README.md` | MOD | CR-BP-100 row updated; CR-BP-100a row added. |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 113 → 114. |

## 2. Deposition mechanics

1. **Cherry-pick first.** The CR-BP-100 work landed on PR #141 (`feature/cr-bp-100-l0-l1-cardinality-gate`) against the 48-cell pre-CR-BP-101 state. CR-BP-100a cherry-picks the commit onto current main (49-cell state) and updates the count assertions. The validator logic itself is identical :  the change is purely to the test-count assertions and prose references that became stale after CR-BP-101.
2. **Surgical atomicity.** Per the established surgical-change discipline (CR-BP-99 matrix-016), count-assertion drift is a separate scope from the validator work. CR-BP-100 = validator + tests + matrix + carrier CR; CR-BP-100a = assertion-only update + carrier CR.
3. **Test path integrity.** Before CR-BP-100a lands, `test_live_total_counts` fails with: `Expected 48 canonical Process Contexts, found 49. If a new PC was admitted, update this assertion...` :  self-explanatory failure message that points operators to this slice.
4. **PR #141 supersession.** PR #141 is the CR-BP-100 work against the pre-CR-BP-101 state. PR #143 (this slice) supersedes it. Both land the same validator + matrix + gate wiring; only the test counts and prose differ. **PR #141 will close as superseded once PR #143 lands.**

## 3. Rule definitions (unchanged from CR-BP-100)

| Rule | Description |
|---|---|
| L0L1-CARD-001 | Every Process Context has exactly one Process Group. Cells with 0 or 2+ groups fail. |
| L0L1-CARD-002 | Every Process Group references exactly one Process Context. The `process_context` field must match `^dea:pc-[a-z0-9-]+$` AND resolve to a known PC. Malformed/unknown values fail. |
| L0L1-CARD-003 | ProcessScope (`dea:scope-*`) is dormant by design. Any such record fails the gate and requires an explicit CR. |

## 4. Gate posture

- Gate [24] L0↔L1 Cardinality (L0L1-CARD-001..003, CR-BP-100 / CR-BP-100a): **CONFORMANT, PASS** (49 PCs / 49 PGs / 0 ProcessScope records; 49-of-49 pairwise verified).
- Full suite: **29 gates, 0 blocking, 0 advisory failures**.
- `open_change_requests`: 113 → 114.

## 5. What this CR is NOT

- **NOT a logic change.** The validator is byte-identical to CR-BP-100; only test assertions and prose are updated.
- **NOT a population slice.** No new records. 49 PCs and 49 PGs are unchanged by this slice.
- **NOT a removal of the ProcessScope layer.** Same dormancy declaration as CR-BP-100.
- **NOT a tightening of the cardinality invariant.** Gate [24] remains advisory.
- **NOT a re-opening of CR-BP-95 or CR-BP-100.** This is a follow-up slice with the same doctrine and a refreshed count.

## 6. Acceptance criteria

1. `tests/test_check_l0_l1_cardinality.py` passes all 17 tests, including the 6 live-catalog exhaustive audits against the 49-cell state.
2. `tests/test_check_reconciliation_matrix.py` passes all 37 tests.
3. `scripts/check_l0_l1_cardinality.py` runs against the live catalog and reports `L0<->L1 cardinality (CR-BP-100; L0L1-CARD-001..003): PASS`.
4. `scripts/conformance_result.py` reports 29 gates, 0 blocking, 0 advisory failures.
5. CR-META gate reports 0 new findings on CR-BP-100a.
6. Em-dash / en-dash audit: 0 violations in new prose.

## 7. Result

CR-BP-100a refreshes the cardinality gate's live-catalog test counts from 48 → 49 after CR-BP-101 (SD/Retire admission) closed the 7x7 = 49-cell ECF matrix. Validator logic is unchanged. The 29-gate suite remains CONFORMANT (0 blocking, 0 advisory); `open_change_requests` 113 → 114. PR #141 (CR-BP-100 against the pre-CR-BP-101 state) closes as superseded. The documentation pipeline (EXT-02..06) is fully unblocked: every L0 has its L1 pair, every L1 has its L0 pair, the matrix is complete, and the cardinality invariant is exhaustively tested against the live 49-cell state.

### Counts (post-merge)

- Process Context records: 49 (unchanged by this slice)
- Process Group records: 49 (unchanged by this slice)
- BP records: 140 (unchanged)
- Activity records: 553 (unchanged)
- L4 Task records: 0 (unchanged)
- ProcessScope records: 0 (dormant-by-design)
- Entities (catalog index): 742 (unchanged)
- Conformance report total: 792 (unchanged)
- `open_change_requests`: 113 → **114**