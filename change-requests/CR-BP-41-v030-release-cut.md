# CR-BP-41: Third Release Cut (v0.3.0)

**Status**: Proposed
**Layer**: Process Catalog (release / governance)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-12
**Depends on**: v0.1.0 baseline (CR-BP-26, PR #64 MERGED, tag `v0.1.0`); CR-BP-28 (register v4 re-derivation); CR-BP-39 (CHANGELOG + README + docs Reconciliation); CR-BP-40 (XRI Gate Promotion); plus the entire BP-32/33/34 tranche plan (PRs #69–81)
**Related**: `docs/versioning.md` (release-cut discipline); `dea-metaframework` ECF v2.5.0 vocabulary source of truth (unchanged since v0.1.0); the stranded `## [v0.2.0]` CHANGELOG block (per user directive 2026-09-12: "ignore the cut"; left in place as a historical artifact)

---

## 1. Purpose

Cut the second tagged release of `dea-catalog-processes` (the third per the version-history discipline that the in-place `## [v0.2.0]` CHANGELOG block represents, even though that v0.2.0 tag was never pushed). This release captures the entire post-v0.1.0 work: the ECF v2.3.0/v2.4.0/v2.5.0 cascade, the BP-32/33/34 tranche plan (CR-BP-32, -33, -34a-d, -35, -36, -37, -38), the XRI asset + gate promotion (CR-BP-37 + CR-BP-40), the CHANGELOG + README reconciliation (CR-BP-39), and the carrier CRs (CR-BP-30, -31).

Per `docs/versioning.md`, this is a release-cut event, not a per-CR event: the CHANGELOG `[Unreleased]` section moves to a dated `v0.3.0` section and the tag is cut at that exact snapshot.

`v0.3.0` is the second-largest post-v0.1.0 evolution bump. Per the bump table in `docs/versioning.md`:

> minor on a canonical admission wave or a Domain rename; patch on a documentation / governance-artifact reconciliation.

This release is **substantially more than a register-version stamp**: it captures 17 commits, 5 new conformance gates ([14]–[18]), the ECF version cascade, the XRI asset + gate, and the BP-32/33/34 tranche plan. Bumping from `v0.2.0` (the stranded CITATION.cff state, never tagged) directly to `v0.3.0` is appropriate: the catalogue at v0.3.0 is materially different from v0.1.0 in every dimension that downstream consumers care about (gate count, ECF version stability, cross-repo integrity assurance, MECE validation).

This CR ships the CHANGELOG conversion and the post-cut updates (`docs/versioning.md` revised; `CITATION.cff` version bumped; index rows updated). The actual `git tag v0.3.0` and `gh release create v0.3.0` are performed after this PR merges to `main`, per the standing discipline.

## 2. What this CR does

| # | Surface | Change |
|---|---|---|
| 1 | `CHANGELOG.md` | New `## [v0.3.0] - 2026-09-12` section containing the 14 `[Unreleased]` entries that have accumulated since v0.1.0 was cut (CR-BP-30 introduced; CR-BP-31 implementation; CR-BP-32/33/34 introduced; CR-BP-34a/b/c/d implementations; CR-BP-32, -33, -36 implementations; CR-BP-35, -37, -38, -40 retrospectives / promotions). Fresh empty `## [Unreleased]` section at the top. The stranded `## [v0.2.0]` block remains in place per user directive (2026-09-12: "ignore the cut"); it is no longer referenced from `## [Unreleased]`. |
| 2 | `CITATION.cff` | `version: 0.2.0 -> 0.3.0`; `date-released: 2026-09-09 -> 2026-09-12`; `url` -> `releases/tag/v0.3.0`. Message, title, authors, keywords, license unchanged. |
| 3 | `docs/versioning.md` | New `v0.3.0` row in the bump table (cut 2026-09-12, CR-BP-41; substantial content). The `v0.2.0` row text is updated to note that the v0.2.0 tag was abandoned (per user directive 2026-09-12: "ignore the cut"). The `0.x.y` (x >= 3) row remains valid; the `1.0.0` row text is unchanged. "Pre-release history (now closed)" section stays closed. |
| 4 | `change-requests/README.md` and root `README.md` | New CR-BP-41 row. CR-BP-40 row remains "Proposed (this PR)". CR-BP-39 status corrected to "Merged (PR #80)". |
| 5 | `CATALOG.yaml` | Regenerated: `open_change_requests` 52 → 53 (CR-BP-41 carrier). |

**Non-goals (explicit).**

- The tag and the `gh release create` happen **post-merge** in a separate step on `main`. The PR itself contains no tag push.
- No entity, schema, validator-rule, CI-pipeline, or governance-decision change.
- **No retrospective v0.2.0 tag push.** The stranded v0.2.0 state (CITATION.cff version + CHANGELOG block) is left as a historical artifact per user directive. The first tag after v0.1.0 is v0.3.0.
- The `## [v0.2.0]` CHANGELOG block stays in place; no retroactive edit to it.

## 3. Why v0.3.0 and not v0.1.1, v0.2.0, or v0.2.1

Per `docs/versioning.md` §"What triggers a version bump":

> minor on a canonical admission wave or a Domain rename; patch on a documentation / governance-artifact reconciliation.

This release contains:

- **Five new conformance gates** ([14] Semantic Identity vs Version; [15] Activity Model; [16] Execution Boundary; [17] MECE Validation; [18] Cross-Repository Integrity). Gate count: 15 → 23 (+8 from the prior 15-gate baseline). Each gate is a substantive new validator with its own tests.
- **ECF v2.3.0 + v2.4.0 + v2.5.0 cascade** (CR-BP-17, -18, -23). The catalog's ECF vocabulary is now stably at v2.5.0.
- **BP-32/33/34 tranche plan** (CR-BP-32/33/34 carrier + CR-BP-34a/b/c/d + CR-BP-32 Activity + CR-BP-33 Execution + CR-BP-36 MECE + CR-BP-35/-37/-38 retrospectives). Adds the L3 Activity, L4 Execution, and MECE machinery.
- **XRI asset (CR-BP-37) + XRI gate promotion (CR-BP-40)**. The catalog now has a CI-runnable regression guard for cross-repo reference drift.
- **17 commits since v0.1.0** (~1.6× the v0.1.0 → v0.2.0 delta).

A patch bump (`v0.1.x` or `v0.2.x`) is far too small for this scope. A minor bump from `v0.2.0` to `v0.3.0` accurately represents: "tranche plan closure; ECF version stable at v2.5.0; cross-repo integrity validated by gate [18]; MECE validated by gate [17]; 23 conformance gates; downstream may pin to this for the full post-v0.1.0 surface".

A major bump to `1.0.0` would require: "the catalogue is stable in a stronger sense than 'Phase 20 closed for one programme': the upstream ECF is also at a stable point and a sustained conformance pass is observed" (`docs/versioning.md`). ECF v2.6.0 work is a separate workstream and the catalogue has not yet seen sustained conformance across multiple ECF versions. `v0.3.0` is the correct landing.

## 4. Tag and release (post-merge)

After this PR merges to `main`:

1. `git tag -s v0.3.0 -m "v0.3.0" <merge-commit-sha>` on `main`.
2. `git push --tags` to `origin`.
3. `gh release create v0.3.0 --repo technehub-labs/dea-catalog-processes --title "v0.3.0" --notes-file <CHANGELOG-v0.3.0-section.md>`.

The release notes are the new `## [v0.3.0] - 2026-09-12` section, stripped of the heading and presented verbatim. Tag and release operations are not part of this PR; the user performs the `Merge` trigger, and the next step is the tag cut.

## 5. Acceptance criteria

1. `CHANGELOG.md` has a `## [v0.3.0] - 2026-09-12` section containing all 14 accumulated entries; a fresh empty `## [Unreleased]` is at the top.
2. `CITATION.cff` carries `version: 0.3.0`, `date-released: 2026-09-12`, `url` pointing at `releases/tag/v0.3.0`.
3. `docs/versioning.md` includes the new `v0.3.0` row in the bump table; the `v0.2.0` row text is updated to note the abandoned tag.
4. The CR-BP-41 row appears in both CR indexes (proposed → merged).
5. CI on the carrier PR is green (no entity, schema, or validator change, so expected PASS is trivial).
6. After merge, a `v0.3.0` tag is cut on `main` and a `v0.3.0` GitHub release is published.

## 6. Result

CR-BP-41 closes the BP-32/33/34 tranche plan + post-tranche closure + gate-promotion work by capturing it as a versioned release. `v0.3.0` is the second git tag of the catalog (after `v0.1.0`; the in-place `## [v0.2.0]` CHANGELOG block represents a never-tagged release state per user directive). The catalogue at v0.3.0 is materially different from v0.1.0 in every dimension that downstream consumers care about.