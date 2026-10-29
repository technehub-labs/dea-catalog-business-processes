# CR-BP-133: Change-Request Register Truth Pass

**Status**: Accepted
**Layer**: Process Catalog (Governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-29
**Depends on**: CR-BP-113 (mv1 migration completion; register repair precedent), CR-BP-116 (release-history reset; BP-90 withdrawal authority)

> **Scope.** Mechanical register-integrity pass, the same class as the CR-BP-113 §e repair: deduplicate surviving duplicate rows, correct stale status cells against file statuses, normalize two Status-line format variants that the open-change-requests counter cannot parse, and flip 26 post-merge "(this PR)" markers to Landed. No entity-record, schema, gate, or CI changes; no CR content is rewritten — statuses and rows only.

---

## 1. Findings and corrections

| # | Finding | Correction |
|---|---|---|
| 1 | CR-BP-90 row appears 4 times (3 exact-duplicate rows survived the CR-BP-113 §e repair that removed 139 of the original 148) | 3 duplicate rows removed; the surviving row's status cell corrected from "**Proposed (this PR)**" to "Superseded (withdrawn; tag withdrawn per CR-BP-116)" — matching the file's status and the WITHDRAWN marker already in the title |
| 2 | CR-BP-102 row appears twice | 1 duplicate row removed |
| 3 | CR-BP-EXT-23 row says "**Proposed (PR #192)**" but the file says Accepted | Status cell corrected to "Accepted (PR #192; file status Accepted)" |
| 4 | 26 rows carry "**Proposed (this PR)**" markers left over from their landing PRs (the register convention never updates them post-merge) | All flipped to "**Landed**" — every file is in the tree on main |
| 5 | CR-BP-03 and CR-BP-03C use the `**Status:**` (colon-inside-bold) variant, which the regenerator's status parser cannot read — both are conservatively counted open | Format normalized to `**Status**:` (no content change) |
| 6 | Un-landed CR drafts (112/113/114 variants from the October 13 handoff) existed only as untracked files in the working clone | Confirmed never in the repository (git ls-files); removed from the clone. No repo change needed — recorded here because their existence prompted this pass |

## 2. What this CR does NOT do

- Does not flip the Status lines inside the 46 remaining file-level "Proposed" CRs whose CHANGELOG sections do not exist — those may be genuinely open proposals; bulk-flipping them without per-CR landing evidence would be the fabrication this register exists to prevent.
- Does not fix the vendored regenerator's `count_open_change_requests` (the Merged-only closed-set defect documented in the capabilities repo as CR-DEA-BC-38 and in the [[regenerator-open-cr-bug-family]] finding): that is a separately governed code change.
- Does not renumber anything: the 112/113/114 "collisions" were never in the repository.

## 3. Verification

`check_cr_metadata.py --strict` CONFORMANT (176 CR files); `check_cr_readme.py --strict` CONFORMANT (in-repo uniqueness passes after dedup); CATALOG.yaml regenerated (the two format-normalized CRs leave the conservative-open set; `open_change_requests` drops by 2).
