# CR-BP-116: Release-History Reset (Path B) + Release-Discipline Extensions

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance) + release discipline
**Owner**: Coder (for eaojnr)
**Date**: 2026-10-13
**Trigger**: User directive 2026-10-13, eaojnr: "For now can we remove all what's in the release, to pave way for a clean release plan? I consider the previous releases immature to put out." Extension selected by user 2026-10-13: release-discipline hardening (A + B + D + F from the candidate list).
**Carrier**: Single PR, executed on a feature branch `release-history-reset` and merged via PR review (not direct-push). Recovery appendix (§2) is captured into this CR file before any destructive operation runs.

## 1. Scope

The minimal Path B is the release-history reset (withdraw v0.x tags/releases; rewrite CHANGELOG/CITATION/versioning surface; relabel abandoned-cut carriers). This CR extends that with four release-discipline hardenings from the candidate list (A + B + D + F), chosen because they strengthen the *forward* posture without coupling to a separate discipline rollout:

- **A  -  Pre-release CI verification contract**: the proposed tag SHA must carry a fresh CI run with all 3 workflows SUCCESS on the exact SHA, verified before `git tag -s`. Catches the v0.1.0 / v0.3.0 / v0.4.0-class race where web edits land after the carrier PR merges and the tag ends up pointing at a SHA the catalog was regenerated against a different version of.
- **B  -  Prior-cut history table**: `docs/versioning.md` gains a numbered, append-only table that records the date, cut CR, commit SHA, gate count, and post-mortem link for every release tag ever cut. Starts empty post-reset. New column-row pair per future cut.
- **D  -  GPG-signing procedure**: the release-cut step names the active key fingerprint (`B2FD3524B35CBDD34251ABE07969C942DB14B2F2`, per the secure-notes procedure note) and requires `git tag -v vN.M.P` verification immediately after signing. Verification status is added to the release manifest.
- **F  -  Doc split**: the release-cut procedure moves from `docs/versioning.md` into a new `docs/release-cut-procedure.md`; the pre-release history (now-removed) section is moved to `docs/release-history-archive.md` as a fossilised record. `docs/versioning.md` keeps the rules + version-trigger table + prior-cut history table from B.

A cross-repo dependency sweep (§3) and a sister-repo coordination note in the `dea-catalog-release-cut` skill (§11) are also in scope. C (pre-cut admission discipline) and G (tag-signing commit message template) are explicitly deferred to their own CRs (per the discussion thread).

## 2. Recovery appendix (captured BEFORE any destructive operation)

This appendix is the audit trail for what is being withdrawn. Captured into this CR file as the first concrete step on the feature branch, before any tag or release deletion runs. If the reset is wrong, the appendix is the recovery path.

### 2.1 v0.1.0 (cut 2026-09-09, tag SHA + GitHub Release notes)

To be filled in by the first execution step from the live `gh release view v0.1.0 --repo technehub-labs/dea-catalog-business-processes --json ...` and `git ls-remote origin --tags` outputs.

### 2.2 v0.3.0 (cut 2026-09-12, tag SHA + GitHub Release notes)

Same capture procedure as 2.1.

### 2.3 v0.2.0 (abandoned cut, 2026-09-09)

No tag was pushed; the `[v0.2.0] - 2026-09-09` CHANGELOG block and the `version: 0.2.0` CITATION.cff state are the only physical artifacts. Both withdrawn 2026-10-13 per user directive ("ignore the cut"). Audit references: CR-BP-29 carrier CR (now relabelled `release withdrawn 2026-10-13`); CHANGELOG `## [v0.2.0] - 2026-09-09` body; CITATION.cff historical.

### 2.4 v0.4.0 (abandoned cut, 2026-09-17)

Same shape as 2.3: carrier PR `CR-BP-90-v040-release-cut.md` merged (it is on main), no tag pushed, no GitHub release. CHANGELOG has an empty `## [v0.4.0] - 2026-09-17` placeholder at line 61. CITATION.cff was last bumped to `version: 0.4.0` / `date-released: 2026-09-17` but never tagged. Both withdrawn 2026-10-13.

## 3. Pre-execution cross-repo dependency sweep

Before any tag deletion, verify no sibling repo in the org pins `dea-catalog-processes@v0.1.0` or `@v0.3.0`:

```bash
gh search code "dea-catalog-processes@v0.1.0" --owner technehub-labs
gh search code "dea-catalog-processes@v0.3.0" --owner technehub-labs
# Sibling repos to consider explicitly:
# - technehub-labs/dea-metaframework
# - technehub-labs/dea-architecture-framework
# - technehub-labs/dea-catalog-business-capabilities
# - technehub-labs/dea-catalog-business-objects
# - technehub-labs/dea-catalog-organizational-units
# - technehub-labs/.github
```

If any hits surface, the affected sibling's owner is notified before the deletion runs; the cross-repo release-coordination note (§11) then references that coordination pattern for future cuts.

## 4. CHANGELOG.md rewrites

Drop the following sections in this exact order:

- `## [v0.4.0] - 2026-09-17` (line 61, empty placeholder).
- The duplicate `## [Unreleased]` at line 64 (latent bug from a prior merge that never got cleaned up; consolidate into the single top-of-file `[Unreleased]` block).
- `## [v0.3.0] - 2026-09-12` (line 559 onward, full historical section).
- `## [v0.2.0] - 2026-09-09` (line 1027 onward).
- `## [v0.1.0] - 2026-09-09` (line 1058 onward).

Keep:

- The single `## [Unreleased]` at the top of the file (with all current CR-BP entries through CR-BP-115).
- `## [2.3.0-migration] - 2026-09-07`, `## [2.4.0-migration] - 2026-09-07`, `## [2.5.0-conformance-gate] - 2026-09-08` (these are pre-v0.1.0 ECF migration prose, not release-layer; they describe how the repo responded to upstream vocabulary changes).

Result: a CHANGELOG that opens with `[Unreleased]` and has only pre-v0.1.0 migration prose beneath. The next release cut moves `[Unreleased]` to `[v0.x.y] - YYYY-MM-DD` and adds a fresh empty `[Unreleased]` block on top.

## 5. CITATION.cff reset

- `version: 0.4.0` -> `version: 0.0.0`
- Remove the `date-released: 2026-09-17` line entirely (no release exists; the field is not required by CFF 1.2.0 and the value is misleading).
- `url: https://github.com/technehub-labs/dea-catalog-processes/releases/tag/v0.4.0` -> `url: https://github.com/technehub-labs/dea-catalog-processes` (repo home; a release-URL will be set when the first real cut lands).

## 6. docs/versioning.md rewrites (release-history side)

Replace the section "Pre-release history (now closed)" with a "Release history" section that says, verbatim:

> **Release history**
>
> No prior releases. The carrier CRs CR-BP-26 (v0.1.0) and CR-BP-41 (v0.3.0) were withdrawn 2026-10-13 as pre-mature; CR-BP-29 (v0.2.0) and CR-BP-90 (v0.4.0) were never cut. See `change-requests/CR-BP-116-release-history-reset.md` for the rationale and audit trail. The first release of the catalogue will be cut at a future state when the version-trigger criteria in the table below are met, against the pre-release CI verification contract in `docs/release-cut-procedure.md`.

The version-trigger table stays. The "Cutting the next tag" section is removed from `docs/versioning.md` and replaced by a pointer to the new `docs/release-cut-procedure.md`.

## 7. docs/release-cut-procedure.md (new, from F)

The full release-cut procedure, including the extensions A + D:

1. Decide a target version per the version-trigger table in `docs/versioning.md`. Document the rationale in `change-requests/CR-BP-NNN.md` (the carrier CR).
2. The carrier PR adds a `release-notes/vN.M.P.md` file with: trigger CR reference, the 30-gate posture (blocking + advisory CONFORMANT counts), the proposed tag SHA, and a one-paragraph user-facing summary of the release.
3. **Pre-release CI verification contract (A)**: the proposed tag SHA is `git rev-parse origin/main` captured at the moment of tagging. A fresh CI run on that exact SHA (the carrier PR's push) must complete with all 3 workflows (`validate`, `validate-allocation`, `ecf-conformance-consumer`) SUCCESS. If any workflow is red, fix it before tagging; do not tag a red-SHA release.
4. `python3 scripts/generate_readmes.py --check` exit 0.
5. `python3 scripts/check_readme_consistency.py --strict` exit 0.
6. `python3 scripts/regenerate_catalog.py --check --schema catalog-index-schema/catalog-index-schema.json` exit 0.
7. `python3 scripts/conformance_result.py` exit 0, all 30 gates CONFORMANT.
8. **GPG-signing procedure (D)**: `gpg --list-secret-keys --keyid-format LONG` shows the active key fingerprint `B2FD3524B35CBDD34251ABE07969C942DB14B2F2` (per `~/.hermes/profiles/coder/secure-notes/gpg-signing-setup.md`). `git tag -s vN.M.P -m "<commit-message-template>" <carrier-merge-sha>` immediately followed by `git tag -v vN.M.P` to verify the signature. The verification status is added to the release manifest in step 11.
9. `git push --tags` to `origin`.
10. `gh release create vN.M.P --repo technehub-labs/dea-catalog-processes --title "vN.M.P" --notes-file release-notes/vN.M.P.md`.
11. Update the prior-cut history table in `docs/versioning.md` (§8) with the new row.
12. Cross-repo coordination: any release that lands a `processes:*` id set change or moves the ECF version triggers the sweep in §3 of CR-BP-116 for the next cut cycle.

The carrier PR is merged only after step 8 verification. The tag is cut only after the carrier PR is on main.

## 8. docs/versioning.md prior-cut history table (B)

A new table, immediately below the version-trigger table:

```
| version | date       | cut by CR        | commit SHA    | gates (blocking+advisory CONFORMANT) | post-mortem |
| ------- | ---------- | ---------------- | ------------- | ------------------------------------ | ----------- |
```

Starts empty. Append one row per future cut when the release lands. The post-mortem column is optional; if a cut later gets a retrospective, link it. (The v0.x withdrawals of CR-BP-116 deliberately do not appear here  -  this table records *successful* cuts, not withdrawals; the recovery appendix in §2 is the audit record for those.)

## 9. Carrier CR relabel (release-cut rows + Status headers)

`change-requests/README.md` rows for CR-BP-26, CR-BP-29, CR-BP-41, CR-BP-90 get a `[WITHDRAWN 2026-10-13  -  see CR-BP-116]` suffix in the title cell. The Status cell stays `**Merged**` (the PR did merge; the release it carried was later withdrawn  -  these are two different facts).

The carrier CR doc Status header on each of those four files gets a one-line addendum:

```
**Status**: Merged (PR #N); release withdrawn 2026-10-13, see CR-BP-116.
```

Body text otherwise untouched. The body is the historical truth at the time of writing and rewriting it is silent history destruction.

## 10. CHANGELOG entry for CR-BP-116 + CATALOG.yaml posture

CHANGELOG `[Unreleased]` gains a CR-BP-116 entry summarizing the withdrawal + the discipline extensions. CATALOG.yaml regenerated to include CR-BP-116 in `open_change_requests` (97 -> 98). All other counts unchanged.

## 11. Cross-repo coordination note (E, light, from candidate list)

The `dea-catalog-release-cut` skill (already in memory, edited under CR-BP-114) gains one new pitfall line: any release of `dea-catalog-processes` that lands a `processes:*` id set change or moves the ECF version triggers a sweep of sibling repos for downstream breaks; cf. CR-BP-37 (cross-repo integrity). This makes the cross-repo concern a recurring check.

## 12. Conformance + Test Posture

- 30-gate rollup CONFORMANT (no gate-count change; CR-BP-116 touches CHANGELOG, CITATION, docs, and the skill; the validator scripts are unchanged).
- `python3 scripts/generate_readmes.py --check` exit 0.
- `python3 scripts/check_readme_consistency.py --strict` exit 0.
- `python3 scripts/regenerate_catalog.py --check ...` exit 0.
- D-004 sweep on the new files: `docs/release-cut-procedure.md`, the CHANGELOG entry, the prior-cut history table, the CITATION.cff reset. No `;;;`, no en/em-dashes in the new content.
- No new tests (this CR is documentation + tag/release layer; the existing 45 tests + the 30-gate rollup cover the validator surface).

## 13. NOT-List

- No record-content changes. Entity records are untouched.
- No id changes. The repo's current `processes:*` id set is the source of truth for the first real cut.
- No gate-count changes. CR-BP-116 is doc + discipline + tag/release layer only.
- No cross-repo scope. Sibling repos are notified via the cross-repo coordination note (§11) but no sibling repo state is changed in this CR.
- No new release tag cut. The first real release is its own CR after this reset lands.
- C (pre-cut admission discipline) and G (tag-signing commit message template) deferred to their own CRs.

## 14. Acceptance Criteria

- All v0.x release-layer state withdrawn per §1-§9; recovery appendix (§2) complete and committed.
- `git ls-remote origin --tags` shows no `v0.1.0` / `v0.3.0` tags.
- `gh release list --repo technehub-labs/dea-catalog-business-processes` shows no `v0.1.0` / `v0.3.0` releases.
- `docs/versioning.md` has the new "Release history" section, the prior-cut history table (empty), and a pointer to `docs/release-cut-procedure.md`.
- `docs/release-cut-procedure.md` exists and contains the full procedure with steps A and D inlined.
- `CITATION.cff` has `version: 0.0.0`, no `date-released`, repo-home `url`.
- The four carrier CRs (CR-BP-26/-29/-41/-90) carry the withdrawal addendum on their Status header and the row title in `change-requests/README.md`.
- CHANGELOG.md has a single `[Unreleased]` at the top, no v0.x version sections, no duplicate `[Unreleased]`, and the CR-BP-116 entry.
- `CATALOG.yaml` regenerated; `open_change_requests` reflects CR-BP-116.
- 30-gate rollup CONFORMANT; CI green on the merged PR.
- `dea-catalog-release-cut` skill has the cross-repo coordination pitfall line.

## 15. Result

The catalogue's release-layer goes from a state of three pre-mature v0.x cuts and one abandoned v0.4.0 carrier to a clean slate: no prior releases, the carrier CRs clearly relabelled as withdrawn, and a forward-discipline package (pre-release CI verification, prior-cut history table, GPG-signing procedure, doc split) that prevents the v0.x-class incidents from recurring. The first real release can stand on its own.
