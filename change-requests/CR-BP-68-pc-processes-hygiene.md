# CR-BP-68 - Process Context processes-list hygiene + PC-008 resolution gate

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
**Date**: 2026-09-15

## 1. Change Request

A state audit of the post-CR-BP-67 catalog (main @ `4983056`) surfaced two
pre-existing legacy defects that no gate can see. This slice repairs both and
extends PC-008 so the defect class becomes machine-visible.

Defect 1: five legacy Process Context records (CR-BP-02 era) carry a YAML
continuation-indent error in their `processes:` lists. The first entry is a
proper list item; the remaining ids were indented beneath it and folded into a
single concatenated scalar. Affected cells (23 process ids effectively
unlisted):

- `dea:pc-fa-build` (4 ids)
- `dea:pc-fa-design` (4 ids)
- `dea:pc-fa-improve` (3 ids)
- `dea:pc-fa-operate` (8 ids)
- `dea:pc-sd-conceive` (4 ids)

Defect 2: `dea:group-customer-lifecycle-management` carries an evidence
`reference: docs/research/L1-REGISTER-v0.1.md`, a path retired by
CR-CATALOG-STRUCT-02 (the file moved under the record's own `research/`
directory). The reference dangles.

## 2. Mechanics

1. Repair the five `processes:` lists: each process id becomes its own list
   item, order preserved exactly as originally authored. No id added, removed,
   or renamed. No other field touched.
2. Point the dangling evidence reference at the post-CR-CATALOG-STRUCT-02
   location: `entities/v1-alpha/dea:group-customer-lifecycle-management/research/L1-REGISTER-v0.1.md`.
3. Extend `scripts/check_process_context.py` PC-008 with two sub-checks:
   - Shape: a `processes:` entry must be a single string identifier; an entry
     containing multiple `dea:process-` occurrences (the concatenation
     signature) or a non-string item is a violation.
   - Resolution: each `dea:process-*` entry must resolve to an existing
     canonical Business Process record in `entities/v1-alpha/`. The check is
     skipped when the catalog under test has no entities tree (fixture
     catalogs), preserving the validator's existing fixture behaviour.
4. Extend the validator self-test: an entities fixture plus two new broken
   contexts (concatenated scalar, dangling reference) and a positive
   `processes:` entry on the fixed context.

## 3. Gate posture

PC-008 runs inside the existing Process Context gate. The extension makes the
repaired defect class a regression guard: any future indentation slip or
renamed/retired BP referenced from a context fails the gate. Live catalog
after repair: PASS (PC-001..PC-008), self-test PASS.

## 4. Repository changes

- `contexts/v1-alpha/dea-pc-fa-build.yaml` - processes list repaired (4 ids)
- `contexts/v1-alpha/dea-pc-fa-design.yaml` - processes list repaired (4 ids)
- `contexts/v1-alpha/dea-pc-fa-improve.yaml` - processes list repaired (3 ids)
- `contexts/v1-alpha/dea-pc-fa-operate.yaml` - processes list repaired (8 ids)
- `contexts/v1-alpha/dea-pc-sd-conceive.yaml` - processes list repaired (4 ids)
- `entities/v1-alpha/dea:group-customer-lifecycle-management/dea:group-customer-lifecycle-management.yaml` - evidence reference repointed
- `scripts/check_process_context.py` - PC-008 shape + resolution sub-checks, self-test fixtures
- `change-requests/README.md` - index row
- `CATALOG.yaml` - regenerated (open_change_requests 79 -> 80)

## 5. What this CR does NOT do

- Does not add, remove, rename, or re-classify any process assignment; the
  repairs restore the originally authored membership verbatim.
- Does not change any entity version (membership repair is defect correction,
  not semantic revision).
- Does not alter PC-001..PC-007 semantics.
- Does not touch the deprecated `dea:process-develop-governance-strategy`
  record (see CR-BP-21a; exclusion rationale unchanged).
- Does not change record counts; no test count-assertion sites move.

## 6. Acceptance criteria

- [x] All five repaired lists parse to the exact originally authored id sets.
- [x] Evidence reference resolves to an existing file.
- [x] `check_process_context.py --self-test` passes with the new fixtures.
- [x] `check_process_context.py` on the live catalog: PASS, 0 findings.
- [x] Full pytest suite green; conformance suite CONFORMANT with no new
      findings; CR-META 0 new findings.
- [x] CATALOG.yaml regenerated and current.

## 7. Result

Landed as PR #109. The five cells declare their true membership (23 ids
restored), the register evidence trail resolves again, and PC-008 now guards
both the concatenation defect class and dangling process references.
