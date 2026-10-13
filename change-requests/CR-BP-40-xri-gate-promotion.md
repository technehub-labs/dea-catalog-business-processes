# CR-BP-40: Cross-Repository Integrity Gate Promotion (XRI-001..005 → Gate [18])

**Status**: Proposed
**Layer**: Cross-cutting
**Owner**: Emmanuel A. Otchere
**Date**: 2026-09-12
**Carrier**: Second post-tranche slice after CR-BP-39 (CHANGELOG + README + docs Reconciliation, PR #80 MERGED). Promotes the `scripts/check_cross_repo_integrity.py` runtime asset (landed in CR-BP-37, PR #78) to a conformance gate in `scripts/conformance_result.py`. Follows up on the explicit deferral in CR-BP-37 §3.
**Depends on**: CR-BP-37 (Cross-Repository Integrity, runtime asset); CR-BP-37 §3 ("promotion of XRI-001..005 to gate [18] deferred to a future CR"); CR-BP-39 (CHANGELOG + README + docs Reconciliation, PR #80 MERGED)

---

## 1. Change Request

Promote `scripts/check_cross_repo_integrity.py` from a **runtime asset** (manual invocation by the catalog maintainer) to a **conformance gate** wired into `scripts/conformance_result.py` as **gate [18] Cross-Repository Integrity (XRI-001..005)**, advisory, non-blocking.

This slice is **explicitly** the follow-on that CR-BP-37 §3 deferred:

> "**No CI gate wiring.** CR-BP-37 is documentation-heavy (per tranche plan, "~200 LOC + contracts"). The validator is a runtime / CI-runnable asset for the catalog maintainer; promoting it to a conformance gate is deferred to a future CR if needed."

The future CR is this one. Promotion is **advisory** (does not block the merge); XRI-005's design intent is forward-looking regression detection — the catalog currently passes all five rules, so the advisory status causes no spurious noise today; if/when XRI-005 fires (e.g. a sibling-repo CR adds a lineage reference without the corresponding local file), the gate surfaces the finding in CI without blocking.

## 2. What this slice does

1. Add **gate [18]** entry in `scripts/conformance_result.py` GATES list, immediately after gate [17] MECE Validation:
   ```python
   ("[18] Cross-Repository Integrity (XRI-001..005)",
    False, ["python", "scripts/check_cross_repo_integrity.py", "--strict"]),  # CR-BP-40; advisory (promoted from runtime asset per CR-BP-37 §3)
   ```
2. Author this CR doc.
3. Update `change-requests/README.md` to add the CR-BP-40 row.
4. Update root `README.md` to add the CR-BP-40 row.
5. Update `CHANGELOG.md` `[Unreleased]` with the CR-BP-40 implementation entry.
6. Regenerate `CATALOG.yaml` (`open_change_requests` 51 → 52).

## 3. What this slice does NOT do

- **NOT make the gate blocking.** XRI-005 is forward-looking (it's a regression guard for future sibling-repo CR additions); making it blocking would either (a) be a no-op today (all rules pass), or (b) block the first PR that adds an ungrounded companion CR. The advisory status lets CI surface the finding while the catalog maintainer decides.
- **NOT change `scripts/check_cross_repo_integrity.py`.** The runtime asset is unchanged — its `--strict` mode already returns exit 1 on any finding. The promotion is **purely additive** in the wiring layer.
- **NOT change `metamodel-pointer.yaml`, `change-requests/README.md`'s Cross-repo context block, or any canonical record.** No documentation mutation; only the gate roster grows.
- **NOT introduce a new conformance dimension.** XRI joins the existing roster of advisory gates [11]–[17] as a peer.
- **NOT add a validator to the BP-id-name contrast-fix or any other surface.** Out of scope.

## 4. Pre-promotion behavior (CR-BP-37 runtime asset)

`scripts/check_cross_repo_integrity.py --strict` already exists and is the gate's payload:

- **`--strict`** returns exit code 1 if any finding is emitted (per `check_cross_repo_integrity.py:402`).
- **`--self-test`** runs the 12-case self-test.
- **`--json`** emits structured output for CI consumers.

Gate `[18]` invokes the script with `--strict`, exactly as gates [11]–[17] do for their respective validators.

## 5. Promotion decision rationale

CR-BP-37 §3 deferred the promotion. Two signals now argue for promoting:

1. **The runtime asset is stable.** Since PR #78 merged, the validator has run 0 findings across XRI-001..005 on every CI invocation triggered by subsequent PRs (PRs #79, #80). No drift in the pointer or the README Cross-repo context block.
2. **The tranche plan is closed.** With CR-BP-39 (PR #80) merging, the post-tranche state of the catalog is stable enough that the next CI-driven drift is more likely to come from a sibling-repo CR addition than from a local pointer edit. XRI-005 is the explicit regression guard for that case.

Promoting the gate now means the first time a sibling-repo CR adds a companion reference without a local file, CI surfaces the finding rather than the maintainer discovering it post-merge.

## 6. Repository changes

| Path | Status | Notes |
|---|---|---|
| `scripts/conformance_result.py` | MOD | Add **gate [18]** to GATES list (1 line). |
| `change-requests/CR-BP-40-xri-gate-promotion.md` | NEW | Slice carrier CR (this file). |
| `change-requests/README.md` | MOD | Add CR-BP-40 row. |
| `README.md` (root) | MOD | Add CR-BP-40 row. |
| `CHANGELOG.md` | MOD | Add CR-BP-40 implementation entry under `[Unreleased]`. |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 51 → 52. |

**No validator, schema, or record change.** Pure additive wiring slice; ~10 LOC of code + ~200 LOC equivalent of paperwork.

## 7. Acceptance criteria

1. `scripts/conformance_result.py` GATES list contains gate `[18]` with the exact tuple: `("[18] Cross-Repository Integrity (XRI-001..005)", False, ["python", "scripts/check_cross_repo_integrity.py", "--strict"])`.
2. `python3 scripts/conformance_result.py` reports **23 gates evaluated** (was 22).
3. Gate `[18]` reports **CONFORMANT** with 0 findings on the live catalog.
4. `python3 -m pytest tests/` still passes (368 tests).
5. `python3 scripts/check_cr_metadata.py` shows 0 new findings.
6. `CATALOG.yaml` reflects `open_change_requests: 52`.
7. `change-requests/CR-BP-40-xri-gate-promotion.md` exists.
8. No canonical record, schema, or validator-rule change.

## 8. Slice ordering rationale

This slice is intentionally second after CR-BP-39 (PR #80):

- **CR-BP-39** closed the bookkeeping drift (CHANGELOG + README pointer block).
- **CR-BP-40** (this slice) promotes the runtime asset CR-BP-37 §3 deferred into a real CI gate.
- Together they close the post-tranche cleanup loop: bookkeeping first, then validator-promotion that exercises the bookkeeping's freshly-corrected pointers in CI.

Future slices (CR-BP-41+) are open-ended and depend on user direction:

- v0.3.0 release cut (stranded v0.2.0 / CITATION.cff decision deferred per CR-BP-39 §3)
- 14 backlog-deferred coordinates (CR-BP-19 §3; Activate/Retire policy reversal)
- ECF v2.6.0 cascade (cross-repo- coordination with `dea-metaframework`)
- Cross-catalog federation coordination (BC / BO / OU)

## 9. Tranche plan + post-tranche status (post-#80)

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
| Post-tranche | CR-BP-39 CHANGELOG + README + docs Reconciliation | Merged (PR #80) |
| **Post-tranche** | **CR-BP-40 XRI Gate Promotion** | **This slice** |

## 10. Result

After this slice lands:

- The catalog runs **23 conformance gates** (was 22), each evaluated on every CI invocation.
- Gate `[18] Cross-Repository Integrity (XRI-001..005)` is the explicit CI-runnable regression guard for cross-repo reference drift.
- The CR-BP-37 §3 deferral is closed.
- The catalog maintainer's CI noise floor rises by one advisory gate (CONFORMANT on the live catalog today; forward-looking guard).

No entity, schema, validator-rule, or governance-decision change.