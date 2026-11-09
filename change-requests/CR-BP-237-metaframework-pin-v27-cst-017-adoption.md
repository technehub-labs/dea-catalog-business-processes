# CR-BP-237: Metaframework Toolchain Pin v2.6.0 -> v2.7.0 (CST-017 Adoption)

**Status**: Proposed
**Layer**: Cross-cutting
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-10
**Depends on**: CR-CATALOG-STRUCT-11 (dea-metaframework PR #61, tagged v2.7.0: the CST-017 directory-entry-cap invariant)

> **Scope.** Toolchain-pin maintenance: the CI checkout of `dea-metaframework` (`.github/workflows/ci.yml`, the fetch the cross-repo conformance suite step runs from) moves v2.6.0 -> v2.7.0 so this repo's PR-time conformance gate picks up CST-017, the org-wide directory-entry cap (no directory holds 800+ tracked entries; entity-storage-layout §4; the org-level counterpart is reconciler rule R5, dea-governance CR-019). This repo is the suite's first live adopter of the new invariant. No record, id, gate, or layout changes.

## 1. Why

The owner's 2026-11-09 directive: an org-wide audit and enforcement scheme for directories nearing GitHub's 1,000-entry listing cap, remediated the metrics/processes way when tripped. The metaframework half landed as CST-017 in the conformance suite; it only reaches a consumer repo when that repo deliberately bumps its pin. This repo already runs the suite in CI as its final step (`--strict`), so a pin bump is the whole adoption. The 2026-11-09 audit census found this repo's worst directory at `change-requests/` 194 flat CR files (under both the 500 watch tier and the 800 trigger; the org-level audit watches it), so the gate lands green here and tightens from here.

## 2. What changes

| Site | Change |
|---|---|
| `.github/workflows/ci.yml` fetch step | `ref: v2.6.0` -> `ref: v2.7.0` |
| `.github/workflows/ci.yml` header comment | "CST-001..CST-016" -> "CST-001..CST-017" |

## 3. Verification

- `python tools/conformance_test_catalog_structure.py --catalog-root . --cst CST-017` (v2.7.0 suite) exits 0 against this repo's working tree.
- The full suite (CST-001..CST-017) passes at v2.7.0 locally; no warnings beyond the pre-existing advisories.
- `scripts/check_cr_metadata.py` passes for the new CR.

## 4. NOT-List

- No CR file moves or renames: `change-requests/` stays flat in this change (194 entries; a shard, if ever needed, is its own CR with its own gate updates).
- No vendored tool changes: the regenerator/gate/schema vendored copies are untouched; the fetch step prefers them as before.
- No record, schema, or CATALOG.yaml changes.

## 5. Acceptance criteria

1. CI green on this PR with the suite step running the v2.7.0 toolchain (17 CSTs).
2. `check_cr_metadata.py` exit 0.
