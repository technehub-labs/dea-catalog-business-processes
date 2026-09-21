# CR-BP-36: MECE Validation (MECE-001..008)

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Proposed
**Layer**: Cross-cutting
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-12
**Carrier**: Seventh execution slice of the BP-32/33/34 tranche plan; first slice of Phase 5 (CR-BP-36 — MECE Validation). See `01_plan/CR-BP-32-33-34-foundation/POSITIONING.md` §5/§7.
**Depends on**: CR-BP-12 (PG-006 intra-context MECE), CR-BP-16 (conformance gate), CR-BP-22 (audit_status axis)
**Lands against**: 126 canonical BP records, 35 canonical PG records, 35 canonical PC records, 1 register file (CR-BP-22 ratified-accepted v4); conformance level L4

---

## 1. Change Request

Codify catalog-wide MECE (Mutually Exclusive, Collectively Exhaustive) checks as machine-testable rules. CR-BP-16 implements *Conformance* (is this artifact structurally and semantically valid?); CR-BP-36 implements *MECE* (is the catalog collectively exhaustive and mutually exclusive?). These are orthogonal concerns (CR-BP-34 §4).

Gate [7] (check_process_group.py, PG-006) covers intra-context MECE for Process Groups (no two PGs share an L2 process in the same context). CR-BP-36 covers the catalog-wide MECE that gate [7] does NOT cover: cross-coordinate coverage, register-to-catalog alignment, BP semantic uniqueness, and orphan detection.

The eight rules:

| # | Rule | Machine-checkable |
|---|---|---|
| **MECE-001** | **Coordinate coverage (PC existence).** | Every register-landed coordinate (Domain x Lifecycle Stage with `audit_status: landed`) has a canonical PC record on disk. Matching is by `(domain, lifecycle_stage)` coordinate, NOT by raw PC id string. |
| **MECE-002** | **Group coverage per context.** | Every canonical Process Context record has at least one canonical Process Group whose `process_context` field references it. |
| **MECE-003** | **BP coverage per group.** | Every canonical Process Group composes at least one canonical Business Process (via `composes[].target_id` matching a `dea:process-*` record on disk). |
| **MECE-004** | **BP semantic uniqueness.** | No two canonical Business Process records share the same normalized `(identity.verb, identity.object)` pair. |
| **MECE-005** | **Group coordinate uniqueness.** | No two canonical Process Groups share the same `(process_context, normalized name)` pair. |
| **MECE-006** | **Register-to-catalog alignment (group coverage).** | Every register-landed coordinate has at least one canonical Process Group on disk (cross-check register vs catalog). |
| **MECE-007** | **Orphan detection (PG → PC).** | Every canonical Process Group references a Process Context that exists on disk. |
| **MECE-008** | **Orphan detection (BP → PG).** | Every canonical (non-deprecated) Business Process is composed by at least one Process Group. |

## 2. Why this CR matters

The existing CR-BP-16 conformance gate answers "is this artifact valid?" but defers MECE (CR-BP-34 §4). Gate [7]'s PG-006 covers intra-context MECE. The catalog-wide MECE gaps that remain:

1. **Register-to-catalog drift.** The CR-BP-19 register (v2 / ratified-accepted v4 per CR-BP-22 + CR-BP-28) declares 35 landed coordinates. PC records exist on disk for 35 coordinates, but the register references 10 of them via the full-word PC id convention (`dea:pc-ge-conceive`) while the actual PC records use the abbreviated convention (`dea:pc-ge-c`). This is a known legacy drift from CR-BP-13 (pre-CR-BP-20 alignment). The MECE validator matches on `(domain, lifecycle_stage)` coordinates to bridge the convention drift.
2. **BP semantic duplication.** Two BPs with the same normalized `(verb, object)` are semantic duplicates even if their ids differ. Today all 126 BPs have unique pairs; the validator is a regression guard.
3. **Group coordinate duplication.** Two PGs in the same context with the same name create user-facing confusion. The validator catches this.
4. **Orphan detection.** A BP that is listed in a PC's `processes:` list but not in any PG's `composes[]` is an inconsistency. A PG that references a PC that does not exist is an orphan. The CR-BP-36 slice found one such orphan: `dea:process-secure-funding-facilities` was listed in `dea:pc-fa-build.processes` but missing from `dea:group-financial-build.composes`. The fix is bundled in this slice (see §5).

## 3. Coverage on the live catalog (2026-09-12, pre-slice)

Initial run found **1 MECE-008 violation**:

```
[MECE-008] BP 'dea:process-secure-funding-facilities' is not composed by any Process Group (orphan; lifecycle_status='candidate')
```

The BP was listed in `dea:pc-fa-build.processes` but missing from `dea:group-financial-build.composes[]`. This is the kind of inconsistency CR-BP-36 is designed to catch.

A second potential finding (`dea:process-develop-governance-strategy`) was correctly excluded: that record has `lifecycle_status: deprecated` and is intentionally not composed by any PG (it has been superseded by `dea:process-develop-corporate-strategy` per CR-BP-21a).

## 4. The remediation (bundled in this slice)

`entities/v1-alpha/dea:group-financial-build/dea:group-financial-build.yaml` gains:

- A new `composes[]` entry: `source_id: dea:group-financial-build` → `target_id: dea:process-secure-funding-facilities` (relationship_type: composes, status: active, provenance: CR-BP-36).
- A `change_history` entry: `cr: CR-BP-36, date: 2026-09-12, change: "MECE-008 remediation: added dea:process-secure-funding-facilities to composes[]. Composes 4 L2 processes."`

After the remediation, all 8 MECE rules pass with **0 findings** on the live catalog.

## 5. Repository changes

| Path | Status | Notes |
|---|---|---|
| `scripts/check_mece.py` | NEW | MECE-001..008 validator; coordinate-based matching; CLI mirrors prior slices |
| `tests/test_check_mece.py` | NEW | 23 tests; rule-level + CLI + live catalog + orphan-remediation regression |
| `entities/v1-alpha/dea:group-financial-build/dea:group-financial-build.yaml` | MOD | Adds MECE-008 remediation: composes[] entry for `dea:process-secure-funding-facilities`; change_history entry for CR-BP-36 |
| `scripts/conformance_result.py` | MOD | Gate [17] MECE-001..008 (advisory) |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 46 → 47 |
| `change-requests/README.md` | MOD | CR-BP-36 row added |
| `change-requests/CR-BP-36-mece-validation.md` | NEW | Slice carrier CR |

## 6. Tranche plan status

| Phase | Slice | Status |
|---|---|---|
| 1 | CR-BP-32/33/34 foundation carrier | Merged (PR #69, `f40a45c`) |
| 2 | CR-BP-34a L2 Qualification | Merged (PR #70, gate [11]) |
| 2 | CR-BP-34b Intent Purposive | Merged (PR #71, gate [12]) |
| 2 | CR-BP-34c Lifecycle State-Machine | Merged (PR #72, gate [13]) |
| 2 | CR-BP-34d Semantic Identity vs Version | Merged (PR #73, gate [14]) |
| 3 | CR-BP-32 Activity Model | Merged (PR #74, gate [15]) |
| 4 | CR-BP-33 Execution Boundary | Merged (PR #75, gate [16]) |
| **5** | **CR-BP-36 MECE Validation (MECE-001..008)** | **This slice; gate [17]** |
| 5 | CR-BP-35 / CR-BP-37 / CR-BP-38 (documentation retrospectives) | Next per user direction |

## 7. What this CR is NOT

- **NOT a metamodel CR.** MECE is a catalog-internal property; no metamodel entities are modified.
- **NOT a register re-derivation.** The CR-BP-19 / CR-BP-22 register v2 (ratified-accepted v4 per CR-BP-28) is unchanged.
- **NOT a record mutation.** Only one record (`dea:group-financial-build`) gains a missing `composes[]` entry; no records are created, deleted, or restructured.
- **NOT a conformance-gate replacement.** MECE is orthogonal to Conformance (CR-BP-34 §4). Gate [17] is advisory and layered on the existing 16-gate suite.
- **NOT a future MECE programme.** CR-BP-36 covers the eight rules above; deeper MECE (e.g. cross-domain overlap, semantic-cluster coverage) is deferred to a follow-on CR if needed.

## 8. Acceptance criteria

1. `scripts/check_mece.py` runs on the live catalog with 0 findings after remediation.
2. `scripts/check_mece.py --self-test` passes (14 cases).
3. `tests/test_check_mece.py` passes (23 tests).
4. `scripts/conformance_result.py` runs with gate [17] added; final verdict remains CONFORMANT.
5. `dea:group-financial-build.composes[]` includes `dea:process-secure-funding-facilities` with provenance `CR-BP-36`.
6. No record, schema, or validator-rule change outside the additive changes listed in §5.

## 9. Result

CR-BP-36 establishes the MECE Validation gate (gate [17]) as the catalog-wide complement to gate [7]'s intra-context PG-006 check. The 8-rule validator emits 0 findings on the live catalog after bundling the MECE-008 remediation for `dea:process-secure-funding-facilities`. The validator is forward-looking for future contributions and serves as a regression guard for all 8 MECE dimensions.
