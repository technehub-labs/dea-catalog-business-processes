# Release History Archive

## Status: Fossilised (CR-BP-116, 2026-10-13)

This document is the **fossilised record** of releases that were
withdrawn or abandoned. The withdrawal logic lives in
`change-requests/CR-BP-116-release-history-reset.md`; this document
is the historical reference. The current `Release history` section
in `docs/versioning.md` is the policy view; the prior-cut history
table in `docs/versioning.md` §3 is the live record of successful
cuts.

The four rows below are deliberately NOT in the prior-cut history
table. The table records *successful* cuts; this archive records
withdrawals and abandoned cuts.

## v0.1.0 (cut 2026-09-09; withdrawn 2026-10-13)

- **Tag**: `v0.1.0` (annotated)
- **Tag SHA**: `3abe3bb13e1d895d028b23d68efaee37dc30a573` (dereferences to `f284242ff447fa2d3acbfd858c8270df383e0b45`)
- **GitHub Release**: `https://github.com/technehub-labs/dea-catalog-business-processes/releases/tag/v0.1.0`
- **Published**: 2026-09-09T12:38:35Z
- **Carrier CR**: `change-requests/CR-BP-26-v010-release-cut.md`
- **Status**: **Withdrawn 2026-10-13** by CR-BP-116 §2.1.

### Why withdrawn

The user directive 2026-10-13, eaojnr: "For now can we remove all
what's in the release, to pave way for a clean release plan? I
consider the previous releases immature to put out." The
catalogue at `v0.1.0` was the first tagged release after the
seven-domain landing programme (CR-BP-15 Phase 20 closure, 196
records at L4 conformance, 0 findings, register audit 35 / 0 /
14). The withdrawal is a release-layer reset, not a content
rejection. The carrier CR-BP-26 is **Merged** (PR #51) and
remains in `change-requests/` with a one-line addendum noting
the withdrawal.

### Body excerpt (preserved verbatim)

> "First tagged release. Closes the CR-BP-15 Phase 20 governance
> gate (CR-BP-25, 2026-09-09) and freezes the post-landing-
> programme snapshot. The catalogue at this tag is the artefact
> downstream may pin to: 196/196 records at CR-BP-16 conformance
> level L4; 0 findings (blocking and advisory); register audit
> 35 landed / 0 ratified-pending-landing / 14 backlog-deferred;
> dispositions 107 RETAIN / 18 RECLASSIFY / 1 MOVE.
>
> Carrier: CR-BP-26. The four sub-programmes accumulated under
> this release, in landing order..."

The full body is in the deletion log (see the CR-BP-116 PR body
for the verbatim transcript) and was previously in the GitHub
Release notes.

## v0.2.0 (abandoned 2026-09-09; carrier merged 2026-09-09; abandoned 2026-10-13)

- **Tag**: none (never cut)
- **Tag SHA**: n/a
- **GitHub Release**: n/a
- **Carrier CR**: `change-requests/CR-BP-29-v020-release-cut.md`
- **Status**: **Abandoned 2026-09-09** (per user directive "ignore
  the cut"); explicitly withdrawn 2026-10-13 by CR-BP-116.

### Why abandoned

The `## [v0.2.0] - 2026-09-09` block in `CHANGELOG.md` and the
`version: 0.2.0` / `date-released: 2026-09-09` state in
`CITATION.cff` were the only physical artifacts. The carrier PR
(CR-BP-29, PR #66) merged but the tag was never cut per user
directive 2026-09-12 ("ignore the cut"). The CHANGELOG block
and the CITATION state were removed by CR-BP-116 §4-5.

### Why it was a no-content cut

Register v3 -> v4 re-derivation against ECF v2.5.0 (CR-BP-28);
content unchanged from v0.1.0; register-version stamp only. The
0.1.0 -> 0.2.0 bump was the register-version stamp, not a content
change. Downstream consumers of the L1 register itself should
have pinned to `v0.2.0` for register-v4 fidelity, but the cut
was abandoned.

## v0.3.0 (cut 2026-09-12; withdrawn 2026-10-13)

- **Tag**: `v0.3.0` (annotated)
- **Tag SHA**: `7e68e42d25daca2ff78d9a2666a6f22ac7cb6230` (dereferences to `3280e1320f43639e41b6056050bf053d038a3161`)
- **GitHub Release**: `https://github.com/technehub-labs/dea-catalog-business-processes/releases/tag/v0.3.0`
- **Published**: 2026-09-13T07:54:32Z
- **Carrier CR**: `change-requests/CR-BP-30-release-package.md`
- **Status**: **Withdrawn 2026-10-13** by CR-BP-116 §2.2.

### Why withdrawn

Same user directive as v0.1.0: "For now can we remove all what's
in the release, to pave way for a clean release plan? I consider
the previous releases immature to put out." The catalogue at
`v0.3.0` was materially different from v0.1.0 in every dimension
that downstream consumers care about (17 commits; 5 new
conformance gates; the BP-32/33/34 tranche plan; the XRI asset
+ gate promotion; the CHANGELOG + README reconciliation; the
ECF v2.3.0/v2.4.0/v2.5.0 cascade). The withdrawal is a
release-layer reset, not a content rejection.

### Body excerpt (preserved verbatim)

> "Third tagged release. Captures the entire post-v0.1.0 work as
> a single versioned snapshot: the ECF v2.3.0/v2.4.0/v2.5.0
> cascade (CR-BP-17, -18, -23), the BP-32/33/34 tranche plan
> (CR-BP-32, -33, -34a-d, -35, -36, -37, -38), the XRI asset +
> gate promotion (CR-BP-37 + CR-BP-40), the CHANGELOG + README
> reconciliation (CR-BP-39), and the carrier CRs (CR-BP-30, -31).
> The catalogue at v0.3.0 is materially different from v0.1.0 in
> every dimension that downstream consumers care about.
>
> Per `docs/versioning.md` §"What triggers a version bump", this
> is a **minor bump** capturing a canonical admission wave + a
> Domain rename cascade (ECF v2.3.0/v2.4.0/v2.5.0). Not patch
> (those are reserved for documentation / governance-artifact
> reconciliations); not major (those require ECF stability +
> sustained conformance)."

The full body is in the deletion log (see the CR-BP-116 PR body
for the verbatim transcript) and was previously in the GitHub
Release notes.

## v0.4.0 (abandoned 2026-09-17; carrier merged; abandoned 2026-10-13)

- **Tag**: none (never cut)
- **Tag SHA**: n/a
- **GitHub Release**: n/a
- **Carrier CR**: `change-requests/CR-BP-90-v040-release-cut.md`
- **Status**: **Abandoned 2026-10-13** by CR-BP-116.

### Why abandoned

The carrier PR `CR-BP-90-v040-release-cut.md` merged (it is on
main), no tag pushed, no GitHub release. CHANGELOG had an empty
`## [v0.4.0] - 2026-09-17` placeholder at line 61. CITATION.cff
was last bumped to `version: 0.4.0` / `date-released: 2026-09-17`
but never tagged. The CHANGELOG placeholder and the CITATION
state were removed by CR-BP-116 §4-5.

### Why it was a no-content cut

Same shape as v0.2.0: a release-cut artifact without a tag. The
catalogue content at the proposed v0.4.0 was the same as v0.3.0
modulo documentation / governance-artifact reconciliations (which
the version-trigger table classifies as a patch, not a minor).
The 0.3.0 -> 0.4.0 bump was a patch-class increment, but the
cut was abandoned.

## How to read this archive

When a downstream consumer asks "what was the v0.1.0 / v0.2.0 /
v0.3.0 / v0.4.0 release?", point them at this archive. The
catalogue content at those versions is recoverable from git
history at the recorded tag SHAs; the withdrawal is a
release-layer fact, not a content fact.

When a future cut lands, the entry in this archive is NOT
updated; the prior-cut history table in `docs/versioning.md` §3
is the live record of successful cuts. This archive is the
fossil record of the ones that didn't make it.
