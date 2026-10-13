# CR-BP-39: CHANGELOG + README + docs Reconciliation (Post-Tranche Closure)

**Status**: Proposed
**Layer**: Cross-cutting
**Owner**: Emmanuel A. Otchere
**Date**: 2026-09-12
**Carrier**: First execution slice after the BP-32/33/34 tranche plan closure (CR-BP-32 → CR-BP-38 across PRs #69–79). Reconciles tracking artifacts with `main` at `e371cff6`. No entity, schema, validator, or gate change.
**Depends on**: CR-BP-24 (programme closure reconciliation); CR-BP-25 (Phase 20 governance review); CR-BP-26 (first release cut); CR-BP-29 (second release cut carrier); CR-BP-32 (Activity Model); CR-BP-33 (Execution Boundary); CR-BP-34a/b/c/d (Phase 2 conformance validators); CR-BP-35 (architecture retrospective); CR-BP-36 (MECE validation); CR-BP-37 (cross-repo integrity); CR-BP-38 (ECF matrix population retrospective)

---

## 1. Change Request

Reconcile three drift surfaces against `main` at `e371cff6`:

1. **`CHANGELOG.md`** — `[Unreleased]` is missing entries for seven CR-BP-32/33/34-tranche slices that landed between 2026-09-10 and 2026-09-12 (PRs #70–73, #74–79). The `[Unreleased]` block currently stops at CR-BP-34c.
2. **`README.md` (root)** — six CR rows show stale "**Proposed (this PR)**" status (CR-BP-24, CR-BP-25, CR-BP-29, and the placeholder rows for Activity Model / Execution Boundary). All are merged in `main`.
3. **`change-requests/README.md`** — six CR rows show stale "**Proposed (this PR)**" status (CR-BP-30, CR-BP-34a, CR-BP-34b, CR-BP-34c, CR-BP-34d). All merged.

The stranded `## [v0.2.0]` section in `CHANGELOG.md` and the v0.2.0 stamp in `CITATION.cff` are **explicitly out of scope** for this slice per user direction (2026-09-12): "ignore the cut". No tag operations; no version-stamp changes; no `docs/versioning.md` edits.

## 2. The drift surfaces

### 2.1 `CHANGELOG.md` — `[Unreleased]` entries missing

| Slice | PR | Status |
|---|---|---|
| CR-BP-32/33/34 foundation carrier | #69 | Listed (introduced) |
| CR-BP-30 release-package carrier | — | Listed (introduced) |
| CR-BP-31 PR-canonical serves migration | #67 | Listed (implementation) |
| CR-BP-34a L2 Qualification | #70 | Listed |
| CR-BP-34b Intent Purposive | #71 | Listed |
| CR-BP-34c Lifecycle State-Machine | #72 | Listed |
| **CR-BP-34d Semantic Identity vs Version** | **#73** | **MISSING** |
| **CR-BP-32 Activity Model** | **#74** | **MISSING** |
| **CR-BP-33 Execution Boundary** | **#75** | **MISSING** |
| **CR-BP-36 MECE Validation** | **#76** | **MISSING** |
| **CR-BP-35 Architecture retrospective** | **#77** | **MISSING** |
| **CR-BP-37 Cross-Repo Integrity** | **#78** | **MISSING** |
| **CR-BP-38 ECF Matrix Population retrospective** | **#79** | **MISSING (just merged)** |

Seven entries to add under `[Unreleased]`. None move `[Unreleased]` to a dated release — per user direction (ignore the v0.2.0 cut), the unreleased block remains in place for the future v0.3.0 release-cut CR.

### 2.2 `README.md` (root) — stale status rows

| Row | Current | Correct |
|---|---|---|
| CR-BP-24 (line 1042) | "**Proposed (this PR)**" | "**Merged** (PR #62)" |
| CR-BP-25 (line 1043) | "**Proposed (this PR)**" | "**Merged** (PR #63)" |
| CR-BP-29 (line 1046) | "**Proposed (this PR)**" | "**Merged** (PR #66)" |
| Activity Model placeholder | "**Future**" | Reference CR-BP-32 row (PR #74) |
| Execution Boundary placeholder | "**Future**" | Reference CR-BP-33 row (PR #75) |

### 2.3 `change-requests/README.md` — stale status rows

| Row | Current | Correct |
|---|---|---|
| CR-BP-30 | "**Proposed (this PR)**" | "**Merged** (PR #68)" |
| CR-BP-34a | "**Proposed (this PR)**" | "**Merged** (PR #70)" |
| CR-BP-34b | "**Proposed (this PR)**" | "**Merged** (PR #71)" |
| CR-BP-34c | "**Proposed (this PR)**" | "**Merged** (PR #72)" |
| CR-BP-34d | "**Proposed (this PR)**" | "**Merged** (PR #73)" |
| CR-BP-32 | "**Merged** (PR #74)" (already correct after #74) | (no change) |
| CR-BP-33 | "**Merged** (PR #75)" (already correct after #75) | (no change) |
| CR-BP-36 | "**Merged** (PR #76)" (already correct after #76) | (no change) |
| CR-BP-35 | "**Merged** (PR #77)" (already correct after #77) | (no change) |
| CR-BP-37 | "**Merged** (PR #78)" (already correct after #78) | (no change) |
| CR-BP-38 | "**Proposed (this PR)**" (was the slice I just merged; the row in change-requests/README.md will be updated to "**Merged** (PR #79)" by this slice) | "**Merged** (PR #79)" |

## 3. What this slice does NOT do

- **NOT a release cut.** No tag push, no `gh release create`, no version bump.
- **NOT a v0.2.0 cut completion.** The stranded `## [v0.2.0]` block and `CITATION.cff` v0.2.0 stamp are out of scope per user direction (2026-09-12: "ignore the cut").
- **NOT a `docs/versioning.md` edit.** The bump table is unchanged; v0.2.0 row remains "**cut** 2026-09-09 (CR-BP-29)" as authored, even though the tag was never cut.
- **NOT a CHANGELOG `[Unreleased]` → dated release conversion.** The unreleased block stays in place; the future v0.3.0 release-cut CR (a separate slice) will perform that conversion.
- **NOT a record, schema, validator-rule, or conformance-gate change.**

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `CHANGELOG.md` | MOD | Seven new `### CR-BP-XX implementation` blocks added under `[Unreleased]` (CR-BP-34d, -32, -33, -36, -35, -37, -38). The `[Unreleased]` block stays in place. |
| `README.md` | MOD | Five row-status corrections (CR-BP-24, CR-BP-25, CR-BP-29, Activity Model, Execution Boundary). |
| `change-requests/README.md` | MOD | Six row-status corrections (CR-BP-30, CR-BP-34a/b/c/d, CR-BP-38) plus a new CR-BP-39 row. |
| `change-requests/CR-BP-39-changelog-readme-reconciliation.md` | NEW | Slice carrier CR (this file). |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 50 → 51. |

## 5. Acceptance criteria

1. `CHANGELOG.md` `[Unreleased]` contains the seven new entries (CR-BP-34d, -32, -33, -36, -35, -37, -38).
2. `README.md` shows the corrected status for CR-BP-24, CR-BP-25, CR-BP-29 (now `**Merged**` with PR numbers), and the Activity Model / Execution Boundary placeholder rows reference the merged slices.
3. `change-requests/README.md` shows corrected status for CR-BP-30, CR-BP-34a/b/c/d, CR-BP-38.
4. `change-requests/CR-BP-39-changelog-readme-reconciliation.md` exists.
5. `CATALOG.yaml` reflects `open_change_requests: 51` (was 50).
6. `python3 -m pytest tests/` still passes.
7. `python3 scripts/conformance_result.py` still 22 gates CONFORMANT.
8. `python3 scripts/check_cr_metadata.py` shows 0 new findings.
9. No canonical record, schema, validator-rule, or conformance-gate change.

## 6. Slice ordering rationale

This slice is intentionally first after the BP-32/33/34 tranche plan closure:

- **All seven missing CHANGELOG entries** refer to slices that already merged. Adding them now ensures any future release cut (v0.3.0 or later) starts from a complete `[Unreleased]` block.
- **README status rows** are stale relative to `main`; correcting them aligns the README pointer block with the actual state of the repo.
- **`change-requests/README.md` corrections** restore fidelity to the per-CR status pointers that the catalog maintainers rely on.

It is documentation-only; ~150 LOC equivalent (table rows + paragraph entries); no functional change.

## 7. Tranche plan status (post-#79, with this slice pending)

| Phase | Slice | Status |
|---|---|---|
| 1 | CR-BP-32/33/34 foundation carrier | Merged (PR #69) |
| 2 | CR-BP-34a/b/c/d | Merged (PRs #70–73) |
| 3 | CR-BP-32 Activity Model | Merged (PR #74) |
| 4 | CR-BP-33 Execution Boundary | Merged (PR #75) |
| 5 | CR-BP-36 MECE Validation | Merged (PR #76) |
| 5 | CR-BP-35 Architecture retrospective | Merged (PR #77) |
| 5 | CR-BP-37 Cross-Repo Integrity | Merged (PR #78) |
| 5 | CR-BP-38 ECF Matrix Population retrospective | Merged (PR #79) |
| **Post-tranche** | **CR-BP-39 CHANGELOG + README + docs Reconciliation** | **This slice (first post-tranche)** |

## 8. Result

After this slice lands:

- `CHANGELOG.md` `[Unreleased]` is complete for the entire BP-32/33/34 tranche plan (CR-BP-32/33/34 introduced + CR-BP-30 introduced + CR-BP-31 implementation + CR-BP-34a/b/c/d implementations + CR-BP-32/-33/-36 implementations + CR-BP-35/-37/-38 retrospectives).
- `README.md` (root) reflects the actual state of all CR rows.
- `change-requests/README.md` reflects the actual state of all per-CR status pointers.
- `CATALOG.yaml` `open_change_requests` advances 50 → 51.

The catalog is ready for a future v0.3.0 release-cut CR (a separate slice) when the user chooses to perform it.