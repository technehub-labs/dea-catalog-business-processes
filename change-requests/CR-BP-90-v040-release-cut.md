# CR-BP-90: Fourth Release Cut (v0.4.0)

**Status**: Proposed
**Layer**: Process Catalog (release / governance)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-17
**Depends on**: v0.3.0 baseline (CR-BP-41, PR #82 MERGED, tag `v0.3.0`); CR-BP-42..57 (L3 EO/PR/GE/PV/FA/S&D/A&O domain tranches); CR-BP-58..61 (gate / documentation repair); CR-BP-62..79 (lifecycle discovery + first + second admission tranche waves + admitted-BP L3 tranches); CR-BP-80 (five-cell escape-clause discovery exercise); CR-BP-81..86 (four-cell discovery programme admissions); CR-BP-87 (combined L3 decomposition tranche); CR-BP-88 (post-v0.3.0 reconciliation); CR-BP-89 (four-cell discovery programme retrospective)
**Related**: `docs/versioning.md` (release-cut discipline); `dea-metaframework` ECF v2.5.0 vocabulary source of truth (unchanged since v0.1.0); the stranded `## [v0.2.0]` CHANGELOG block (per user directive 2026-09-12: "ignore the cut"; left in place as a historical artifact)

---

## 1. Purpose

Cut the third tagged release of `dea-catalog-processes` (the fourth per the version-history discipline that the in-place `## [v0.2.0]` CHANGELOG block represents, even though that v0.2.0 tag was never pushed). This release captures the entire post-v0.3.0 work: the L3 EO/PR/GE/PV/FA/S&D/A&O domain tranches (CR-BP-42..57), gate / documentation repair (CR-BP-58..61), the lifecycle discovery method (CR-BP-62..63), the first + second admission tranche waves (CR-BP-64..79), the five-cell escape-clause discovery exercise (CR-BP-80), the four-cell discovery programme (CR-BP-81..87), and the post-programme documentation (CR-BP-88..89).

Per `docs/versioning.md`, this is a release-cut event, not a per-CR event: the CHANGELOG `[Unreleased]` section moves to a dated `v0.4.0` section and the tag is cut at that exact snapshot.

`v0.4.0` is the largest post-v0.3.0 evolution bump. Per the bump table in `docs/versioning.md`:

> minor on a canonical admission wave or a Domain rename; patch on a documentation / governance-artifact reconciliation.

This release is **substantially more than a register-version stamp**: it captures 54 commits, the 7-domain L3 coverage completion (all 7 canonical domains at L0-L3), the lifecycle-stage discovery method (DISC-001..008 gate [19]), the four-cell discovery programme closure (13 of 14 backlog-deferred cells ADMIT-CANONICAL), 553 canonical Activity records (was 0 at v0.1.0; +553 across the BP-32/33/34 tranche plan + the four-cell programme), and the full retroactive CHANGELOG + README reconciliation.

This CR ships the CHANGELOG conversion and the post-cut updates (`docs/versioning.md` revised; `CITATION.cff` version bumped; index rows updated). The actual `git tag v0.4.0` and `gh release create v0.4.0` are performed after this PR merges to `main`, per the standing discipline.

## 2. What this CR does

| # | Surface | Change |
|---|---|---|
| 1 | `CHANGELOG.md` | New `## [v0.4.0] - 2026-09-17` section containing the 55 `[Unreleased]` entries that have accumulated since v0.3.0 was cut (CR-BP-42..89). Fresh empty `## [Unreleased]` section at the top. The stranded `## [v0.2.0]` block remains in place per user directive (2026-09-12: "ignore the cut"); it is no longer referenced from `## [Unreleased]`. |
| 2 | `CITATION.cff` | `version: 0.3.0 -> 0.4.0`; `date-released: 2026-09-12 -> 2026-09-17`; `url` -> `releases/tag/v0.4.0`. Message, title, authors, keywords, license unchanged. |
| 3 | `docs/versioning.md` | New `v0.4.0` row in the bump table (cut 2026-09-17, CR-BP-90; substantial content). The `v0.2.0` row text unchanged. The `v0.3.0` row text remains valid. The `0.x.y` (x >= 3) row remains valid; the `1.0.0` row text is unchanged. |
| 4 | `change-requests/README.md` and root `README.md` | New CR-BP-90 row. CR-BP-88 / CR-BP-89 rows remain "Proposed (this PR)". |
| 5 | `CATALOG.yaml` | Regenerated: `open_change_requests` 98 → 99 (CR-BP-90 carrier). |

**Non-goals (explicit).**

- The tag and the `gh release create` happen **post-merge** in a separate step on `main`. The PR itself contains no tag push.
- No entity, schema, validator-rule, CI-pipeline, or governance-decision change.
- **No retrospective v0.2.0 tag push.** The stranded v0.2.0 state (CITATION.cff version + CHANGELOG block) is left as a historical artifact per user directive.
- The `## [v0.2.0]` CHANGELOG block stays in place; no retroactive edit to it.

## 3. Why v0.4.0 and not v0.3.1 or v0.3.x

Per `docs/versioning.md` §"What triggers a version bump":

> minor on a canonical admission wave or a Domain rename; patch on a documentation / governance-artifact reconciliation.

This release contains:

- **L3 EO/PR/GE/PV/FA/S&D/A&O domain tranches** (CR-BP-42..57). All 7 canonical domains are now covered end-to-end at L0-L3. 553 canonical Activity records (was 0 at v0.1.0; +553 across the BP-32/33/34 tranche plan + the four-cell programme).
- **Lifecycle discovery method + first + second admission tranche waves** (CR-BP-62..79). 14 backlog-deferred Activate/Retire cells across 7 domains. 9 of those cells admitted via two tranche waves.
- **Four-cell discovery programme closure** (CR-BP-80..87). 5 of 5 remaining backlog-deferred cells closed (4 ADMIT-CANONICAL + 1 DEFER). 13 canonical PC + PG + BP stacks + 16 Activity records.
- **Gate / documentation repair** (CR-BP-58..61). PG gate repair, catalog schema default path repair, documentation currency for the L3 layer, documentation gate precision repair (DOC-001/DOC-003).
- **Post-programme documentation** (CR-BP-88, -89). 54-PR [Unreleased] reconciliation + four-cell programme retrospective long-form ADR.
- **54 commits since v0.3.0** (~3.2× the v0.1.0 → v0.3.0 delta).

A patch bump (`v0.3.x`) is far too small for this scope. A minor bump from `v0.3.0` to `v0.4.0` accurately represents: "all 7 domains at L0-L3; lifecycle-stage method codification; 13 Activate/Retire BPs admitted; discovery-programme closure; post-programme documentation".

A major bump to `1.0.0` would require: "the catalogue is stable in a stronger sense than 'Phase 20 closed for one programme': the upstream ECF is also at a stable point and a sustained conformance pass is observed" (`docs/versioning.md`). ECF v2.6.0 work is a separate workstream and the catalogue has not yet seen sustained conformance across multiple ECF versions. `v0.4.0` is the correct landing.

## 4. Tag and release (post-merge)

After this PR merges to `main`:

1. `git tag -s v0.4.0 -m "v0.4.0" <merge-commit-sha>` on `main`.
2. `git push --tags` to `origin`.
3. `gh release create v0.4.0 --repo technehub-labs/dea-catalog-processes --title "v0.4.0" --notes-file <CHANGELOG-v0.4.0-section.md>`.

The release notes are the new `## [v0.4.0] - 2026-09-17` section, stripped of the heading and presented verbatim. Tag and release operations are not part of this PR; the user performs the `Merge` trigger, and the next step is the tag cut.

## 5. Acceptance criteria

1. `CHANGELOG.md` has a `## [v0.4.0] - 2026-09-17` section containing all 55 accumulated entries (CR-BP-42..89); a fresh empty `## [Unreleased]` is at the top.
2. `CITATION.cff` carries `version: 0.4.0`, `date-released: 2026-09-17`, `url` pointing at `releases/tag/v0.4.0`.
3. `docs/versioning.md` includes the new `v0.4.0` row in the bump table; the `v0.2.0` row text is unchanged.
4. The CR-BP-90 row appears in both CR indexes (proposed → merged).
5. CI on the carrier PR is green (no entity, schema, or validator change, so expected PASS is trivial).
6. After merge, a `v0.4.0` tag is cut on `main` and a `v0.4.0` GitHub release is published.

## 6. Result

CR-BP-90 closes the four-cell discovery programme + post-v0.3.0 reconciliation + retrospective work by capturing it as a versioned release. `v0.4.0` is the third git tag of the catalog (after `v0.1.0` and `v0.3.0`; the in-place `## [v0.2.0]` CHANGELOG block represents a never-tagged release state per user directive). The catalogue at v0.4.0 is materially different from v0.3.0 in every dimension that downstream consumers care about:

- 7-domain L3 coverage (was partial at v0.3.0; all 7 at L0-L3 now)
- 139 canonical BPs (was 137 at v0.3.0)
- 48 canonical PGs (was 47)
- 48 canonical PCs (was 47)
- 553 canonical Activity records (was 537)
- 23 canonical Discovery records (was 18)
- 788 total records (was 756)
- 24-gate suite (was 23; gate [19] Disc-gate added)
- 13 backlog-deferred Activate/Retire cells ADMIT-CANONICAL (was 0)
- 4 remaining backlog-deferred cells (was 14)
- 4 of 5 four-cell programme cells LANDED (AOAct / EOAct / FAAct / SDAct)

Downstream consumers can pin to `v0.4.0` for the full L0-L3 surface + lifecycle-stage discovery method + four-cell programme closure.