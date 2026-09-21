# CR-BP-29: Second Release Cut (v0.2.0)

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Proposed
**Layer**: Process Catalog (release / governance)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-09
**Depends on**: CR-BP-28 (register v4 re-derivation, PR #65 MERGED); v0.1.0 baseline (CR-BP-26, PR #64 MERGED, tag `v0.1.0`)
**Related**: `docs/versioning.md` (release-cut discipline); dea-metaframework tag `v2.5.0` (ECF vocabulary source of truth, unchanged since v0.1.0)

## 1. Purpose

Cut the second release tag of `dea-catalog-processes` at the snapshot produced by CR-BP-28 (register v4 re-derivation against ECF v2.5.0, merged to `main` immediately before this CR). Per `docs/versioning.md`, this is a release-cut event, not a per-CR event: the CHANGELOG `[Unreleased]` section moves to a dated `v0.2.0` section and the tag is cut at that exact snapshot.

`v0.2.0` is the smallest possible post-v0.1.0 evolution bump. CR-BP-28 was a bookkeeping-grade slice (no entity, schema, validator, or CI change); the bump reflects the formal register ratification from `v3` to `v4`, not new catalogue content. Per the bump table in `docs/versioning.md`, a register-version stamp on an unchanged-content register is a minor bump (0.1.0 -> 0.2.0), not a patch.

This CR ships the CHANGELOG conversion and the post-cut updates (`docs/versioning.md` revised; `CITATION.cff` version bumped; index rows updated). The actual `git tag v0.2.0` and `gh release create v0.2.0` are performed after this PR merges to `main`, per the standing discipline.

## 2. What this CR does

| # | Surface | Change |
|---|---|---|
| 1 | `CHANGELOG.md` | New `## [v0.2.0] - 2026-09-09` section containing the single CR-BP-28 paragraph that has accumulated under `[Unreleased]` since v0.1.0 was cut (2026-09-09). Fresh empty `## [Unreleased]` section at the top. |
| 2 | `CITATION.cff` | `version: 0.1.0 -> 0.2.0`; `date-released: 2026-09-09 -> 2026-09-09`; `url` -> `releases/tag/v0.2.0`. Message, title, authors, keywords, license unchanged. |
| 3 | `docs/versioning.md` | New `v0.2.0` row in the bump table (cut 2026-09-09, CR-BP-29; registers the formal v4 ratification). The `0.x.y` (x >= 2) row remains valid; the `1.0.0` row text is unchanged. "Pre-release history (now closed)" section stays closed (no new pre-release state). |
| 4 | `change-requests/README.md` and root `README.md` | New CR-BP-29 row. CR-BP-28 row remains "Merged (PR #65)". |
| 5 | `CATALOG.yaml` | Regenerated: `open_change_requests` 27 -> 28 (CR-BP-29 carrier). |

**Non-goals (explicit).**

- The tag and the `gh release create` happen **post-merge** in a separate step on `main`. The PR itself contains no tag push.
- No entity, schema, validator-rule, CI-pipeline, or governance-decision change.
- No new canonical content. `v0.2.0` is the same catalogue as `v0.1.0` plus a version-stamp on the register.

## 3. Why v0.2.0 and not v0.1.1

Per `docs/versioning.md` §"What triggers a version bump":

> minor on a canonical admission wave or a Domain rename; patch on a documentation / governance-artifact reconciliation.

CR-BP-28 is not a documentation / governance-artifact reconciliation (those would be the v0.1.x patch tier, e.g. README pointer fixes or CHANGELOG wording repair). It is the **formal re-derivation of the L1 register against the upstream ECF v2.5.0 vocabulary**, recorded as `ratification.version: 4` in both `l1-register.yaml` and `l1-candidate-universe.yaml` and as a new status line in `L1-REGISTER-v0.1.md`. Even though the disposition axis is a no-op (35 / 0 / 14 unchanged), the register version itself moves 3 -> 4, and that is the durable surface downstream consumers of the register will read.

`v0.2.0` (minor) accurately represents: "register ratified against the current ECF vocabulary; canonical content unchanged; downstream may pin to this for register-version fidelity".

## 4. Tag and release (post-merge)

After this PR merges to `main`:

1. `git tag -s v0.2.0 -m "v0.2.0" <merge-commit-sha>` on `main`.
2. `git push --tags` to `origin`.
3. `gh release create v0.2.0 --repo technehub-labs/dea-catalog-processes --title "v0.2.0" --notes-file <CHANGELOG-v0.2.0-section.md>`.

The release notes are the new `## [v0.2.0] - 2026-09-09` section, stripped of the heading and presented verbatim. Tag and release operations are not part of this PR; the user performs the `Merge` trigger, and the next step is the tag cut.

## 5. Acceptance criteria

1. `CHANGELOG.md` has a `## [v0.2.0] - 2026-09-09` section containing the CR-BP-28 paragraph; a fresh empty `## [Unreleased]` is at the top.
2. `CITATION.cff` carries `version: 0.2.0`, `date-released: 2026-09-09`, `url` pointing at the v0.2.0 release.
3. `docs/versioning.md` includes the new `v0.2.0` row in the bump table.
4. The CR-BP-29 row appears in both CR indexes (proposed → merged).
5. CI on the carrier PR is green (no entity, schema, or validator change, so expected PASS is trivial).
6. After merge, a `v0.2.0` tag is cut on `main` and a `v0.2.0` GitHub release is published.
