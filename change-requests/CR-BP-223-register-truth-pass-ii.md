# CR-BP-223: Change-Request Register Truth Pass II (Evidence-Gated Status Backfill)

**Status**: Accepted (this PR)
**Layer**: Cross-cutting (catalog governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-04
**Depends on**: CR-BP-133 (Register Truth Pass I; the precedent — this pass reaches the era gap it could not), CR-BP-221/222 (the immediate demonstration that post-merge status backfill discipline works)

> **Scope.** Mechanically backfills **132 open-class CR statuses to Accepted** under a five-source evidence rule, with per-CR evidence committed as `reconciliation/closure/register-truth-2026-11-04.json`. **4 CRs stay open** on declared human gates. CATALOG.yaml regenerates: `open_change_requests` 136 → **4**, and the repo's own open-count sanity test (`test_live_count_is_reasonable`, pinning `< 100`) passes again for the first time since the register rot began. Zero entity changes; zero gate changes; the counter's semantics are unchanged — only the inputs (stale statuses) are corrected.

---

## 1. Background and Authority

CR-BP-133's truth pass corrected 26 post-merge markers and the register's structural corruption, but the file-header rot reaches further back than its evidence sources did: **136 of 183 CR files carried open-class `Status:` lines while the great majority of their scopes were landed, cited as authorities by gates and records, and registered as closed**. The consequence is the counter drift flagged in the 2026-10-28 repo-health review and witnessed mechanically by `tests/test_regenerate_catalog_open_count.py` failing on main (`open_count < 100` vs 136).

## 2. The Evidence Rule (five independent sources; flip on ANY)

| Source | Meaning |
|---|---|
| `changelog-landed-entry` | A `### CR-<id>:` entry exists in CHANGELOG.md (the house landing record) |
| `register-row-closed` | The CR's register row already carries a closed-class status (row/file mismatch — the classic rot) |
| `entity-change-history-citations` | ≥ 3 canonical records' `metadata.change_history` cite the CR via `cr: <id>` (change_history is a landing record by construction) |
| `implementation-cited-in-code` | The CR id is cited in `scripts/` or `tests/` headers/constants (the gate/tool it spawned exists and names it) |
| `implementation-co-landed-in-pr` | A commit touching the CR file also touched implementation paths (entities/scripts/tests/schemas/.github) — the CR landed *with* its scope |

Per-CR evidence for all 132 flips is committed at `reconciliation/closure/register-truth-2026-11-04.json` (includes the five ambiguous cases resolved individually: CR-BP-94-EXT-04/-05 landed via PR #177's wire commit; EXT-15 via PR #184 with EXT-16/17/18 as drafts; EXT-11's decomposition-level profiles live in the generator + validator; CR-BP-129/130/131 co-landed with `scripts/dea_uri_resolver.py` via PRs #170–#172).

## 3. Stay-Open (4) — declared human gates

| CR | Why it stays |
|---|---|
| CR-BP-30 (release-package carrier) | Status declares **awaiting user input on §3 decisions** — a standing design gate |
| CR-BP-94-EXT-16 (authoring methodology) | **awaiting Proceed** |
| CR-BP-94-EXT-17 (enrichment tooling) | **awaiting Proceed** |
| CR-BP-94-EXT-18 (documentation pilot) | **awaiting Proceed** |

A Status parenthetical that declares a human gate is authoritative over mechanical evidence: co-landing proves a *file* entered the repo, not that the *work* was authorized.

## 4. What Does NOT Change

- No entity record, schema, gate, or CI change. The counter's CLOSED/OPEN status sets are untouched.
- No CR body text is edited — only the `**Status**:` metadata line and the register row's status cell.
- Genuinely-landed CRs that already read closed are untouched.
- The four stay-open CRs are untouched.

## 5. Verification / Acceptance Criteria

1. `open_change_requests` regenerates to **4**; `tests/test_regenerate_catalog_open_count.py` passes (`< 100`).
2. Per-CR evidence manifest committed; every flip carries ≥ 1 non-CODE evidence source; the CODE-only class is empty.
3. `check_cr_metadata.py --strict` and `check_cr_readme.py` (CRR-001..003) CONFORMANT across the full 184-file register.
4. Freshness gate green post-commit (regen + amend discipline).
