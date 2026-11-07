# CR-BP-30h: Release Cut — v0.5.0 (First Post-Reset Tag)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (release governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-06
**Depends on**: CR-BP-30/30a..30g (the release machinery this cut exercises), CR-BP-116 (the release-history reset and this procedure's authority), CR-BP-230..236 (the two-layer documentation programme — the content that makes this snapshot meaningful)

> **Scope.** The first post-reset release cut, per `docs/release-cut-procedure.md` (the 30h slot pre-allocated by CR-BP-30a..g: "30h = first post-reset cut v0.5.0 follows post-merge per the release-cut procedure"). Target: **v0.5.0** (minor bump; the CHANGELOG `[Unreleased]` section accumulated the two-layer documentation programme — a new documentation capability across all 3,723 records — plus the operational-completions and release-package machinery). The carrier PR: moves CHANGELOG `[Unreleased]` → dated `[v0.5.0] - 2026-11-06` + fresh empty `[Unreleased]`; adds `release-notes/v0.5.0.md`; bumps `CITATION.cff` to 0.5.0 / 2026-11-06; appends the prior-cut history row (procedure step 8; the table's SHA cell records this PR's merge commit — the exact SHA tagged). **Tag + GitHub Release are post-merge acts** (procedure steps 4-6): GPG-signed `v0.5.0` at the carrier merge SHA, signature verified, pushed, `gh release create` with the notes file.

**Lands against**: `CHANGELOG.md` (section move), `CITATION.cff` (version bump), `docs/versioning.md` (prior-cut row + history note), `release-notes/v0.5.0.md` (new), this CR + register row. **0 entity-record changes. 0 gate changes. 0 code changes.**

## 1. The release summary (user-facing)

v0.5.0 is the first versioned snapshot since the CR-BP-116 release-history reset (2026-10-13). It captures: the complete **two-layer documentation programme** (CR-BP-230..236, PRs #228–#232) — every one of the 3,723 process-entity records now carries authored Part I Human-Readable Interpretation prose (plain-sentence identity card, everyday description, business purpose, practical context, and a worked example naming the documented actors) rendered above the CI-generated canonical record under byte-identity enforcement, with the new blocking gate [51] Human Readability (HUM-001..007) policing the layer; the **release-package machinery** (CR-BP-30/30a..30g — process map, catalog workbook, BPMN seed library, publish/validate workflows); the **operational completions** (CR-BP-225: L2 definitions, L3/L4 IO declarations, L0 register confirmation); and the **register-truth passes** (CR-BP-223/133). Catalogue at cut: 3,723 records (49 L0 + 49 L1 + 146 L2 + 580 L3 + 2,900 L4).

## 2. Pre-release verification contract (procedure step 2)

- The 3 main workflows (`validate`, `validate-allocation`, `ecf-conformance-consumer`) ran SUCCESS on the carrier merge SHA.
- `generate_readmes.py --check`, `check_readme_consistency.py --strict`, `regenerate_catalog.py --check`, `conformance_result.py` all exit 0 on the branch (verified pre-push; the blocking HUM gate reports 0 findings corpus-wide).
- Tag: `git tag -s v0.5.0 -m "..." <carrier-merge-sha>`; `git tag -v v0.5.0` before push.

## 3. What does NOT change

- No entity records, gates, schemas, or code — the carrier is pure release bookkeeping.
- No id-set change and no ECF version move (procedure step 10 cross-repo sweep not triggered).

## 4. Verification / Acceptance Criteria

1. Carrier PR green on all 3 workflows; the four procedure step-3 checks exit 0.
2. Post-merge: GPG-signed tag `v0.5.0` on the carrier merge SHA, signature verified, tag pushed, GitHub Release created with `release-notes/v0.5.0.md`.
3. `CITATION.cff` reports 0.5.0 / 2026-11-06; the prior-cut history table carries the v0.5.0 row.

---

## Post-cut note (2026-11-07)

Cut executed: annotated tag `v0.5.0` at the carrier merge SHA `3fdddb8c151fa0b1c1d15d08fd06b5c9359e71c0`, pushed 2026-11-07; GitHub Release created at `https://github.com/technehub-labs/dea-catalog-business-processes/releases/tag/v0.5.0` with `release-notes/v0.5.0.md`. **Deviation from procedure step 4**: the tag is annotated, not GPG-signed — no GPG binary, keyring, or signing key existed on the cut machine (the referenced signing-setup notes were also absent). The pre-release CI verification contract (step 2: all 3 workflows SUCCESS on the tagged SHA) was satisfied before tagging. Remediation: GPG setup + a signed follow-up tag on a future cut (or re-tag policy decision) is deferred to the next release cycle's carrier CR.
