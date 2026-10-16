# Versioning Policy

## Status: Active (CR-BP-116, 2026-10-13)

The catalogue versioning discipline is stated in this document. The
release-cut **procedure** lives at `docs/release-cut-procedure.md`
(per the F extension of CR-BP-116); this document is the policy +
the version-trigger table + the prior-cut history table.

CR-BP-116 (2026-10-13) reset the release history (Path B) and
extended the discipline with 4 hardenings (A + B + D + F from the
candidate list):

- A: pre-release CI verification contract (the proposed tag SHA
  must carry a fresh CI run with all 3 workflows SUCCESS).
- B: prior-cut history table (this document gains the table in
  §3 below; starts empty post-reset).
- D: GPG-signing procedure (the release-cut step names the active
  key fingerprint and requires `git tag -v vN.M.P` verification).
- F: doc split (the release-cut procedure moves from this
  document into `docs/release-cut-procedure.md`; the pre-release
  history (now-removed) section is moved to
  `docs/release-history-archive.md` as a fossilised record).

## Format

This repository follows
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) for
the `CHANGELOG.md` format. Versioning is SemVer once a tag is cut.

## 1. Version-trigger table

| Stage | When | Bump |
|---|---|---|
| `0.1.0` | **withdrawn** 2026-10-13 (CR-BP-116). Originally cut 2026-09-09 (CR-BP-26) as the first release. The first git tag after the reset will be a fresh `0.x.y`. | n/a (initial; withdrawn) |
| `0.2.0` | **abandoned** 2026-09-09 (CR-BP-29). Register v3 -> v4 re-derivation against ECF v2.5.0 (CR-BP-28); content unchanged from v0.1.0; register-version stamp only. The carrier CR-BP-29 (PR #66) merged but the tag was never cut per user directive 2026-09-12. CHANGELOG entry removed by CR-BP-116. | minor (register-version stamp); abandoned, no tag pushed |
| `0.3.0` | **withdrawn** 2026-10-13 (CR-BP-116). Originally cut 2026-09-12 (CR-BP-41). Substantial post-v0.1.0 evolution. CHANGELOG entry removed by CR-BP-116. | minor; withdrawn |
| `0.4.0` | **abandoned** 2026-09-17 (CR-BP-90). Carrier PR merged (CHANGELOG had an empty placeholder); no tag pushed. Both withdrawn 2026-10-13 per user directive. | minor; abandoned, no tag pushed |
| `0.x.y` (x >= 5) | `0.x` evolution: new admission waves, new conformance rules, documentation reconciliations | minor on a canonical admission wave or a Domain rename; patch on a documentation / governance-artifact reconciliation |
| `1.0.0` | The catalogue is stable in a stronger sense than "Phase 20 closed for one programme": the upstream ECF is also at a stable point and a sustained conformance pass is observed | major |

## 2. What triggers a version bump

Version bumps are **release-cut events**, not per-CR events. The
CR programme may land many Change Requests between two release cuts;
the CHANGELOG `[Unreleased]` section accumulates them and the
release cut fixes the version at that snapshot.

## 3. Prior-cut history table

This table records every successful release tag ever cut. It starts
empty post-reset. Append one row per future cut when the release
lands. The post-mortem column is optional; if a cut later gets a
retrospective, link it.

| version | date | cut by CR | commit SHA | gates (blocking+advisory CONFORMANT) | post-mortem |
| ------- | ---- | --------- | ---------- | ------------------------------------ | ----------- |
| _empty post-reset 2026-10-13_ | | | | | |

The v0.x withdrawals of CR-BP-116 deliberately do not appear here.
This table records *successful* cuts, not withdrawals; the recovery
appendix in CR-BP-116 §2 is the audit record for those.

## Release history

> **Release history**
>
> No prior releases. The carrier CRs CR-BP-26 (v0.1.0) and CR-BP-41
> (v0.3.0) were withdrawn 2026-10-13 as pre-mature; CR-BP-29 (v0.2.0)
> and CR-BP-90 (v0.4.0) were never cut. See
> `change-requests/CR-BP-116-release-history-reset.md` for the
> rationale and audit trail. The first release of the catalogue
> will be cut at a future state when the version-trigger criteria
> in the table above are met, against the pre-release CI
> verification contract in `docs/release-cut-procedure.md`.

## 4. The release-cut procedure

The full release-cut procedure, including the extensions A + D
from CR-BP-116, lives at `docs/release-cut-procedure.md`. That
document is the authoritative procedure; this document is the
policy + the trigger table + the prior-cut history.

The next release cut moves the CHANGELOG `[Unreleased]` section
to a dated `[vN.M.P]` section and adds a fresh empty `[Unreleased]`
block on top. The release cut then updates this document's
prior-cut history table (§3 above) with the new row.
