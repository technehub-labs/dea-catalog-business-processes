# Release-Cut Procedure

## Status: Active (CR-BP-116, 2026-10-13)

This document is the authoritative release-cut procedure for
`dea-catalog-processes`. It was carved out of `docs/versioning.md`
as part of the F extension of CR-BP-116 (doc split: policy stays
in `versioning.md`; procedure lives here). The version-trigger
table and the prior-cut history table remain in
`docs/versioning.md`.

## Pre-conditions

A release cut is appropriate when **all** of the following are true:

- The 30-gate rollup is CONFORMANT (blocking + advisory counts match
  the version-trigger table in `docs/versioning.md`).
- The CHANGELOG `[Unreleased]` section has accumulated enough
  changes that a snapshot is meaningful (operator judgement; the
  rule of thumb is "a new admission wave or a Domain rename
  cascade" for a minor bump, "a documentation / governance-artifact
  reconciliation" for a patch).
- The carrier CR has been authored and merged (see step 1 below).

## The 12-step procedure

### 1. Carrier CR

Author `change-requests/CR-BP-NNN-vNMP-release-cut.md` with:

- The target version.
- The trigger CR reference (the CR that triggered the bump).
- The 30-gate posture (blocking + advisory CONFORMANT counts).
- The proposed tag SHA.
- A one-paragraph user-facing summary of the release.

The carrier PR adds a `release-notes/vN.M.P.md` file with the same
content as the carrier CR's body.

### 2. Pre-release CI verification contract (A)

The proposed tag SHA is `git rev-parse origin/main` captured at
the moment of tagging. A fresh CI run on that exact SHA (the
carrier PR's push) must complete with all 3 workflows SUCCESS:

- `validate`
- `validate-allocation`
- `ecf-conformance-consumer`

If any workflow is red, fix it before tagging; do not tag a
red-SHA release.

### 3. Generated artifacts check

```bash
python3 scripts/generate_readmes.py --check
# exit 0

python3 scripts/check_readme_consistency.py --strict
# exit 0

python3 scripts/regenerate_catalog.py --check \
  --schema catalog-index-schema/catalog-index-schema.json
# exit 0

python3 scripts/conformance_result.py
# exit 0; all 30 gates CONFORMANT
```

### 4. GPG-signing procedure (D)

```bash
# Verify the active key fingerprint
gpg --list-secret-keys --keyid-format LONG
# Expected: B2FD3524B35CBDD34251ABE07969C942DB14B2F2 (keyid
# 7969C942DB14B2F2), per
# ~/.hermes/profiles/coder/secure-notes/gpg-signing-setup.md

# Sign the tag immediately followed by verification
git tag -s vN.M.P -m "<commit-message-template>" <carrier-merge-sha>
git tag -v vN.M.P
# Verification status is added to the release manifest in step 8.
```

### 5. Push tags

```bash
git push --tags
```

### 6. Create the GitHub Release

```bash
gh release create vN.M.P \
  --repo technehub-labs/dea-catalog-business-processes \
  --title "vN.M.P" \
  --notes-file release-notes/vN.M.P.md
```

### 7. CHANGELOG move

The carrier PR moves the CHANGELOG `[Unreleased]` section to a
dated `[vN.M.P] - YYYY-MM-DD` section and adds a fresh empty
`[Unreleased]` block on top. The carrier PR is merged only after
step 4 verification (the GPG signature is verifiable after the
tag is cut; the PR's merge commit is the SHA that goes into the
table).

### 8. Update the prior-cut history table

In `docs/versioning.md` §3, append a row:

```
| vN.M.P | YYYY-MM-DD | CR-BP-NNN | <carrier-merge-sha> | <blocking>+<advisory> | <post-mortem-link> |
```

### 9. Update CITATION.cff

```yaml
version: N.M.P
date-released: YYYY-MM-DD
url: "https://github.com/technehub-labs/dea-catalog-business-processes/releases/tag/vN.M.P"
```

### 10. Cross-repo coordination

Any release that lands a `processes:*` id set change or moves the
ECF version triggers the sweep in CR-BP-116 §3 for the next cut
cycle. Notify sibling repos if affected.

### 11. Announcement

Post a one-paragraph announcement on the project channel (#dea
on Discord; the project's GitHub Discussions; or a
`dea-announce@lists.technehub.com` mailing list when Option B from
the IANA-setup follow-on lands).

### 12. Archive

Append a one-line note to `docs/release-history-archive.md`
listing the new release's tag + date + carrier CR.

## The tag-signing commit message template (G; deferred)

The tag-signing commit message template is a separate discipline
(G in the CR-BP-116 candidate list) and is intentionally deferred
to a future CR. The current default is `vN.M.P` (the version
string); a richer template that records the trigger CR, the
gate posture, and the cross-repo sweep result is a follow-on.

## Cross-references

- `docs/versioning.md` - the policy + the version-trigger table +
  the prior-cut history table.
- `docs/release-history-archive.md` - the fossilised record of
  withdrawn releases (the CR-BP-26 / CR-BP-29 / CR-BP-41 / CR-BP-90
  carriers).
- `change-requests/CR-BP-116-release-history-reset.md` - the
  carrier for this procedure's separation from versioning.md.
- `~/.hermes/profiles/coder/secure-notes/gpg-signing-setup.md` -
  the GPG-signing procedure note (per memory #168, #171).
- CR-BP-114 - the record README regeneration, drift gate, and
  release-cut integration (the predecessor of this procedure).
