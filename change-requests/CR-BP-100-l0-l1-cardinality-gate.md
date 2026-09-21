# CR-BP-100: L0↔L1 Cardinality Gate + ProcessScope Dormancy

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
**Date**: 2026-09-19
**Carrier**: Recon-programme follow-up slice that codifies the L0↔L1 1:1 cardinality invariant as an automated gate and declares the ProcessScope layer (CR-BP-95) dormant by design.
**Doctrine** (eaojnr 2026-09-19): L0 = ProcessContext (the canonical ECF cell matrix in `contexts/v1-alpha/`); L1 = ProcessGroup (the 49 canonical groups in `entities/v1-alpha/`, one per ECF cell); canonical cardinality is exactly 1 L1 per L0 (and 1 L0 per L1). The ProcessScope layer (`dea:scope-*`) introduced by CR-BP-95 is a schema-only artifact that has never been instantiated; CR-BP-100 declares it dormant because L0 IS the Process Context matrix.
**Depends on**: CR-BP-02 (Process Context), CR-BP-12 (Process Group), CR-BP-95 (PSCOPE schema-only), CR-BP-99 (reconciliation matrix; back-compat pattern).
**Lands against**: 49 PCs / 49 PGs / 140 BPs / 553 Activities / 0 ProcessScope records; 29 gates CONFORMANT; v0.4.0+12 commits on main (post-CR-BP-101).

---

## 1. Change Request

Land the L0↔L1 cardinality gate as **schema + validator + tests + gate wire**, plus a reconciliation matrix extension row that records the ProcessScope dormancy. Four distinct artifacts:

| Artifact | Status | Notes |
|---|---|---|
| `scripts/check_l0_l1_cardinality.py` | NEW | L0L1-CARD-001..003 validator (13.5 KB). Builds `(process_context -> [group_ids])` and `(group_id -> process_context)` maps; enforces 1:1 cardinality both directions; flags any ProcessScope record as dormant-by-design violation. |
| `scripts/conformance_result.py` | MOD | Wires new advisory **gate [24] L0↔L1 Cardinality (L0L1-CARD-001..003)**. |
| `tests/test_check_l0_l1_cardinality.py` | NEW | 17 tests: 6 live-catalog exhaustive audits + 7 unit tests + 4 CLI integration tests. |
| `reconciliation/cr-bp-99-matrix.yaml` | MOD | +1 row: matrix-021 records the ProcessScope dormancy decision (closed_in CR-BP-100). |
| `change-requests/CR-BP-100-l0-l1-cardinality-gate.md` | NEW | Slice carrier CR (this document). |
| `change-requests/README.md` | MOD | CR-BP-100 row added. |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 113 → 114 (CR-BP-100a follow-up). |

## 2. Deposition mechanics

1. **Validator first.** `check_l0_l1_cardinality.py` mirrors the shape of `check_process_group.py` and `check_process_scope.py`: self-test fixture covers the happy path + every rule-path failure + the dormant-layer rule.
2. **Tests second (exhaustive).** The test file audits the live catalog row-by-row:
   - `test_live_total_counts` -- 49 PCs == 49 PGs.
   - `test_live_no_processscope_records` -- 0 ProcessScope records (CARD-003 dormant-by-design).
   - `test_live_pc_to_pg_map_is_total_and_one_to_one` -- every PC has exactly 1 PG; no PC has 0 or 2+.
   - `test_live_per_pc_audit` -- walks each of 49 PCs; fails with a per-PC diagnostic if cardinality slips.
   - `test_live_per_pg_audit` -- walks each of 49 PGs; fails with a per-PG diagnostic if `process_context` is malformed or unknown.
   - `test_live_no_orphan_pgs_or_pcs` -- explicit orphan/multi checks with debuggable failure messages.
   - 7 unit tests cover all rule paths on synthesised catalogs.
   - 4 CLI integration tests exercise `--self-test`, live run, output shape, and `--help`.
3. **Gate wire last.** `conformance_result.py` wires gate [24] as **advisory** (matches the pattern from CR-BP-95/96/97/EXT-01: new gates are advisory until they accumulate ≥ 1 release cycle of clean output). Promotion to blocking is a future slice.
4. **Reconciliation matrix addition.** One new row (`matrix-021`) records the dormancy decision with category `gate_dormant`, disposition `accept_as_is`, status `closed`, `closed_in: PR-141`. Total rows: 20 → 21.
5. **Self-test.** `scripts/check_l0_l1_cardinality.py --self-test` exercises every rule path on a synthesised fixture and returns 0.
6. **Count assertions.** None changed. 49 PCs / 49 PGs invariant is the assertion; the slice does not introduce or remove records. (Initial CR-BP-100 prose said 48; CR-BP-100a updated to 49 after CR-BP-101 SD/Retire admission landed.)

## 3. Rule definitions

| Rule | Description |
|---|---|
| L0L1-CARD-001 | Every Process Context has exactly one Process Group. Cells with 0 groups OR >1 groups fail. |
| L0L1-CARD-002 | Every Process Group references exactly one Process Context. The `process_context` field must match `^dea:pc-[a-z0-9-]+$` AND resolve to a known PC in `contexts/v1-alpha/`. Malformed or unknown values fail. |
| L0L1-CARD-003 | The ProcessScope layer (`dea:scope-*`) is dormant by design. Any ProcessScope record in `entities/v1-alpha/` fails. Admission requires an explicit CR justifying why the L0 layer is no longer identical to the Process Context matrix. |

## 4. Gate posture

- Gate [24] L0↔L1 Cardinality (L0L1-CARD-001..003, CR-BP-100): **CONFORMANT, PASS** (49 PCs / 49 PGs / 0 ProcessScope records).
- Full suite: **29 gates, 0 blocking, 0 advisory failures**.
- `open_change_requests`: 113 → 114 (CR-BP-100a follow-up).

## 5. What this CR is NOT

- **NOT a population slice.** No new records land. The 49 PCs and 49 PGs are unchanged by this slice (CR-BP-100a was the assertion-only update after CR-BP-101 SD/Retire admission).
- **NOT a removal of the ProcessScope layer.** CR-BP-95's schema + template + validator + doc profile remain in place. CR-BP-100 records dormancy, not deletion. Removal is a future slice.
- **NOT a tightening of the cardinality invariant into a blocking gate.** Gate [24] is advisory; promotion to blocking is a future slice after ≥ 1 release cycle.
- **NOT a re-opening of CR-BP-95.** The schema-only posture from CR-BP-95 §5 ("NOT a population slice") remains accurate; CR-BP-100 formalises the doctrinal consequence.
- **NOT a MECE stress test.** Each PC currently has exactly 1 PG by admission discipline; multi-PG cells would require CR-BP-02 §22 resolution first.

## 6. Acceptance criteria

1. `scripts/check_l0_l1_cardinality.py --self-test` returns exit code 0 and all 5 self-test scenarios pass.
2. `scripts/check_l0_l1_cardinality.py` against the live catalog reports `L0<->L1 cardinality (CR-BP-100; L0L1-CARD-001..003): PASS`.
3. `tests/test_check_l0_l1_cardinality.py` reports 17/17 passing, including 6 live-catalog exhaustive audits.
4. `scripts/conformance_result.py` reports 29 gates, 0 blocking, 0 advisory failures.
5. `reconciliation/cr-bp-99-matrix.yaml` carries 21 rows (was 20); `matrix-021` records ProcessScope dormancy.
6. CR-META gate reports 0 new findings on CR-BP-100.
7. Em-dash / en-dash audit: 0 violations in new prose.

## 7. Result

CR-BP-100 codifies the L0↔L1 1:1 cardinality invariant as an automated advisory gate (L0L1-CARD-001..003), wires it as gate [24] in the conformance pipeline, and declares the ProcessScope layer (CR-BP-95) dormant by design. (At land-time, the catalog carried 48 PCs / 48 PGs; CR-BP-100a refreshed the count assertions to 49/49 after CR-BP-101 SD/Retire admission closed the 7x7 = 49-cell matrix.) The slice introduces no records. The 29-gate suite remains CONFORMANT (0 blocking, 0 advisory); `open_change_requests` 113 → 114 (post-CR-BP-100a). The documentation pipeline (EXT-02..06) may now open with L0↔L1 cardinality guaranteed by automated enforcement against the live 49-cell state.