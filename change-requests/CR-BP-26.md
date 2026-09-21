# CR-BP-26: First Release Cut (v0.1.0)

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Accepted
**Layer**: Process Catalog (release / governance)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-09
**Depends on**: CR-BP-25 (Phase 20 governance approval, closed 2026-09-09); `docs/versioning.md` (release-cut discipline); CR-BP-24 (programme closure reconciliation)
**Related**: CR-BP-21a..21f.1 (landing series, PRs #48-#60); CR-BP-22 (register audit); CR-BP-23 (ECF v2.5.0); CR-BP-25 (Phase 20 closure); dea-metaframework tag `v2.5.0` (ECF vocabulary source of truth)

## 1. Purpose

Cut the first release tag of `dea-catalog-processes` at the snapshot
produced by CR-BP-25 (Phase 20 governance approval closed). Per
`docs/versioning.md`, this is a release-cut event, not a per-CR event:
the CHANGELOG `[Unreleased]` section moves to a dated `v0.1.0` section
and the tag is cut at that exact snapshot. The tag becomes the
durable reference for downstream consumers of the catalogue
(assessment models, federation tooling, the catalogue-as-data
publishing path).

This CR ships the CHANGELOG conversion and the post-cut updates
(`docs/versioning.md` rewritten to "post-release" state; `CITATION.cff`
versioned; index rows updated to reflect the released artefact).
The actual `git tag v0.1.0` and `gh release create v0.1.0` are
performed after this PR merges to `main` — release tags live on
`main`, not on a feature branch.

## 2. What this CR does

| # | Surface | Change |
|---|---|---|
| 1 | `CHANGELOG.md` | New `## [v0.1.0] - 2026-09-09` section containing the four landing-series programmes that accumulated under `[Unreleased]` since 2026-09-08 (CR-BP-21a..21f.1, CR-BP-22, CR-BP-23, CR-BP-24, CR-BP-25). Fresh empty `## [Unreleased]` section at the top. |
| 2 | `CITATION.cff` | NEW (was missing). `version: 0.1.0`, `date-released: 2026-09-09`, title + message + author for the dea-catalog-processes artefact (distinct from `dea-metaframework`'s CITATION.cff which cites the ECF itself). |
| 3 | `docs/versioning.md` | Re-titled "Why no tag today" -> "Pre-release history" (the catalogue is now tagged; the section is historical context, not a current rule). The `1.0.0` row in the bump table is updated to reflect that `1.0.0` is the canonical-status gate, not the first-cut gate. New "v0.1.0" row in the bump table. |
| 4 | `change-requests/README.md` and root `README.md` | New CR-BP-26 row marked **Merged** (PR #64) once the cut lands. The CR-BP-25 row remains "closed by CR-BP-25". The `v0.1.0` row references the GitHub release. |

**Non-goals (explicit).**

- The tag and the `gh release create` happen **post-merge** in a separate
  step on `main`. The PR itself contains no tag push.
- No entity, schema, validator-rule, CI-pipeline, or governance-decision
  change. The release cut is a snapshot, not a change.
- No version bump. `v0.1.0` is the first tag; the next cut will be
  `v0.2.0` (or `v0.1.1` if it's a hotfix).

## 3. Why v0.1.0 and not v1.0.0

Per CR-BP-25 §4 and the live `README.md` Current Status, the catalogue
is at the architecture-inception stage: governance approval is
**closed** for the landing-programme scope, but downstream
`0.x` evolution (new admission waves, new ECF enums, new
conformance rules) is expected and explicitly unblocked by this
release. The `0.x` SemVer discipline (`docs/versioning.md`) reserves
`1.0.0` for the moment the catalogue is stable in a stronger sense
than "Phase 20 closed for one programme" — that is, the moment the
ECF itself stops shifting under the catalogue. Today's upstream
ECF vocabulary is `v2.5.0` (`dea-metaframework`); if the ECF moves
to `v3.0.0` the catalogue's `1.0.0` will likely follow.

`v0.1.0` accurately represents: "landing programme closed, first
durable snapshot, downstream may pin to this".

## 4. Tag and release (post-merge)

After PR #64 merges to `main`:

1. `git tag -s v0.1.0 -m "v0.1.0" <merge-commit-sha>` on `main`.
2. `git push --tags` to `origin`.
3. `gh release create v0.1.0 --repo technehub-labs/dea-catalog-processes
   --title "v0.1.0" --notes-file <CHANGELOG-v0.1.0-section.md>`.

The release notes are the new `## [v0.1.0] - 2026-09-09` section,
stripped of the heading and presented verbatim. Tag and release
operations are not part of this PR; the user performs the `Merge`
trigger, and the next step is the tag cut.

## 5. Acceptance criteria

1. `CHANGELOG.md` has a `## [v0.1.0] - 2026-09-09` section containing
   the landing-series content; a fresh empty `## [Unreleased]` is at
   the top.
2. `CITATION.cff` exists with `version: 0.1.0` and
   `date-released: 2026-09-09`.
3. `docs/versioning.md` reflects the post-release state (no "no tag
   today" framing; bump table includes v0.1.0 row).
4. The CR-BP-26 row appears in both CR indexes.
5. CI on PR #64 is green (no entity, schema, or validator change, so
   expected PASS is trivial).
6. After merge, a `v0.1.0` tag is cut on `main` and a
   `v0.1.0` GitHub release is published.
