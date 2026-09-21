# CR-BP-34d: Semantic-Identity-vs-Version Validators (SIV-001..004)

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Proposed
**Layer**: L2 (Business Process) — identity governance
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-11
**Carrier**: Fourth execution slice of CR-BP-34 (Process Conformance Profile; PR #69 MERGED, commit `f40a45c`); closes Phase 2 of the BP-32/33/34 additive harvest plan (`01_plan/CR-BP-32-33-34-foundation/POSITIONING.md` §5).
**Depends on**: CR-BP-03, CR-BP-14 (BP-SEM-001..014), CR-BP-16, CR-BP-34 §19 (Version Conformance), CR-BP-34a/b/c (PRs #70–72 MERGED).
**Lands against**: 126 canonical BP records; conformance level L4.

---

## 1. Change Request

Codify the four rules from CR-BP-34 §19 ("a version bump shall not silently create a new semantic identity; a semantic-identity change shall require an explicit governed change") as machine-testable validators, additive to the existing `scripts/check_process_identity.py` (BP-ARC-ID-001..005) and the conformance pipeline.

Today the discipline is enforced only by PR review and the cross-repo CR-META-006 rule (which checks cross-repo identifier integrity but does not catch silent version-vs-identity drift within this catalog). The 126 live records need a regression guard.

The four rules:

| # | Rule | Machine-checkable invariant |
|---|---|---|
| **SIV-001** | **Version is SemVer.** | `version` ∈ `^\d+\.\d+\.\d+$` (per `schemas/entity.schema.json`). 3 dot-separated integers. |
| **SIV-002** | **Version bump requires `change_history` evidence.** | For any record whose `version` is *not* `1.0.0` (i.e. MAJOR > 1, or MINOR > 0, or PATCH > 0), at least one entry in `change_history` must carry a non-empty `change` (or `description`) field that names the change. Empty `change_history` arrays on bumped records are forbidden. |
| **SIV-003** | **MAJOR bump requires a semantic-change marker.** | For any record whose `MAJOR` component > 1 (i.e. `version` starts with `2.` or higher), at least one `change_history` entry must contain a semantic-change marker (case-insensitive substring): one of `BREAKING`, `SEMANTIC`, `RENAME`, `REC-` (reconciliation id), `DEPRECATED` (transition event per LCM-003), `SUPERSEDED`, or a `CR-BP-` / `CR-` identifier. The marker establishes that the bump was *intentional*, not accidental. |
| **SIV-004** | **MINOR/PATCH bump shall not silently alter `identity.verb` or `identity.object`.** | For any record whose `MAJOR` == 1 but `MINOR > 0` or `PATCH > 0`, the record must carry a `previous_identity` sub-block (NEW field; optional in the schema) declaring the prior `verb` and `object`. If `previous_identity` is absent, the validator records an *advisory* finding ("MINOR/PATCH bump with no prior-identity record; spot-check identity stability") — not a failure. If `previous_identity` is present, `identity.verb` and `identity.object` must equal `previous_identity.verb` and `previous_identity.object`. This is the smallest machine-checkable form of "version change shall not silently create a new semantic identity" achievable today without a separate version-history file. |

## 2. Why this CR is paper-trail-only on the live catalog

The 126 canonical records distribute as:

| `version` | Count |
|---|---|
| `1.0.0` | 125 |
| `2.0.0` | 1 (`dea:process-develop-corporate-strategy`; CR-BP-21a / CR-BP-20 Option A) |

All 125 v1.0.0 records are exempt from SIV-002 / SIV-003 / SIV-004 (the rules only fire on bumped versions).

The single v2.0.0 record (`dea:process-develop-corporate-strategy`, promoted from the GE × Conceive cell to the SD × Conceive cell via CR-BP-21a, with rename from `dea:process-develop-governance-strategy`) carries its `change_history` under `metadata.change_history` (per the conventional location used across the 126 records — not at the top level), with 4 documented entries. The most recent entry describes the migration: *"L2 migration executed under CR-BP-21a. New id `dea:process-develop-corporate-strategy`; new context `dea:pc-sd-conceive`; new serves relationship `ecf:strategyDirection.conceive`; new Process Group `dea:group-strategy-direction-conception`. Version bumped to 2.0.0."*

That entry contains the `CR-BP-` marker, which is one of the approved semantic-change markers accepted by SIV-003. SIV-002 also passes because the entry text is non-empty.

**SIV-001 emits 0 findings.** All 126 records satisfy `^\d+\.\d+\.\d+$`.

**SIV-002 emits 0 findings.** The single bumped record has non-empty `metadata.change_history` with a documented change.

**SIV-003 emits 0 findings.** The single bumped record carries a `CR-BP-21a` marker in its `metadata.change_history[3]`.

**SIV-004 emits 0 findings.** The single bumped record is a MAJOR bump (v2.0.0), not a MINOR/PATCH bump on v1.x — so the rule does not apply.

Total findings on the live catalog: **0**. The validator ships as a pure regression guard — same posture as CR-BP-34a (BP-C1..C4), CR-BP-34b (PSP-001..003), and CR-BP-34c (LCM-001..005).

## 3. Implication

No record-level remediation is required. The CR is purely **validator-additive**:

- 1 new script (`scripts/check_semantic_identity_version.py`)
- 1 new test file (`tests/test_check_semantic_identity_version.py`)
- 1 new row in `scripts/conformance_result.py` (gate [14])
- 1 new row in `change-requests/README.md` (CR index)
- No entity, schema, validator-rule, or template change.

The 126 canonical records remain at conformance level L4 throughout. Future PRs that bump a version without documenting the corresponding identity change will be caught by gate [14] (advisory) at conformance time rather than at retrospective review.

## 4. Conformance integration: `scripts/conformance_result.py`

Adds one new gate row, placed after gate [13] (Lifecycle State-Machine; CR-BP-34c):

```python
("[14] Semantic Identity vs Version (SIV-001..004)",
 False, ["python", "scripts/check_semantic_identity_version.py", "--strict"]),
```

Marked `blocking=False` (advisory) per the established 34a/b/c pattern. Position [14] is reserved for future identity-governance gates.

## 5. Why this is additive-only

The four rules derive from CR-BP-34 §19 (the canonical process-conformance profile) and the existing `schemas/entity.schema.json` SemVer pattern. The validator reads fields already present (`version`, `change_history`, `identity.verb`, `identity.object`); the only **optional** new field it consults is `previous_identity` (under `identity`), which is schema-permitted today (the `identity` sub-block allows additional properties because the schema's `additionalProperties` is not set to `false` at that nesting depth).

The seed-finding remediation (Option B) edits one record's `change_history` array — purely additive content (no field is renamed or removed). The v2.0.0 record is the canonical example of a *legitimate* semantic-identity change (CR-BP-21a renamed it from `dea:process-develop-governance-strategy` to `dea:process-develop-corporate-strategy` and bumped MAJOR); the back-fill documents that event, which is exactly what `change_history` is for.

## 6. Acceptance criteria

1. `python3 scripts/check_semantic_identity_version.py --strict` exits 0 on the live catalog (Option B path).
2. The validator emits exactly 0 findings against the 126 canonical BPs after the seed remediation.
3. `python3 scripts/conformance_result.py` reports the new gate as `PASS/ADVISORY` (with 0 findings).
4. `python3 -m pytest tests/test_check_semantic_identity_version.py -q` reports all tests pass.
5. `python3 -m pytest tests/ -q` (full suite) reports no new failures.
6. `python3 scripts/check_cr_metadata.py --strict` reports 0 new findings.
7. `python3 scripts/regenerate_catalog.py --check --schema catalog-index-schema/catalog-index-schema.json` matches `CATALOG.yaml`.
8. `python3 scripts/check_lifecycle_state.py --strict` continues to pass (126/126).
9. `python3 scripts/check_process_identity.py` continues to pass (BP-ARC-ID-001..005; 126/126).

## 7. What this is NOT

- **Not a version-bump enforcement policy.** SIV-001..004 catch silent identity drift; they do not prescribe when to bump MAJOR vs MINOR vs PATCH. That policy lives in the contribution-guide docs (CR-BP-03 §6, CR-BP-15 §10).
- **Not a migration.** No `dea:bp-*` records are touched. No id renames. The seed remediation is content-additive only.
- **Not a MECE validation.** CR-BP-34 §23 separates conformance from MECE; MECE is CR-BP-36 (renumbered CR-BP-08).
- **Not a CR-META replacement.** Cross-repo identifier integrity remains CR-META-001..006's job; SIV-001..004 are intra-repo (within `dea-catalog-processes`).

## 8. Result

CR-BP-34d closes the last additive conformance gap identified in CR-BP-34 §19 — the semantic-identity-vs-version discipline. The 126 canonical records remain at conformance level L4 throughout. After this CR lands, every future PR that bumps a version without documenting the corresponding identity change will be caught at conformance time (gate [14]) rather than at retrospective review.

This closes Phase 2 of the BP-32/33/34 additive harvest plan (POSITIONING.md §7). Phase 3 (CR-BP-32: Activity Model) follows per the user's recommended-order directive.

---

## Appendix A — Coverage matrix

| Rule | Records evaluated | Pass | Fail | Notes |
|---|---|---|---|---|
| SIV-001 (SemVer) | 126 | 126 | 0 | All `1.0.0` or `2.0.0` |
| SIV-002 (bump ⇒ change_history) | 1 (v2.0.0) | 1 | 0 | `dea:process-develop-corporate-strategy` carries `metadata.change_history` with the CR-BP-21a migration note |
| SIV-003 (MAJOR ⇒ semantic-change marker) | 1 (v2.0.0) | 1 | 0 | Same record; entry contains `CR-BP-21a` marker |
| SIV-004 (MINOR/PATCH ⇒ previous_identity stability) | 0 | n/a | n/a | No MAJOR==1 bumped records exist |
| **Total** | **126** | **126** | **0** | Pure regression guard |

## Appendix B — Cross-references

- CR-BP-34 §19 (Version Conformance) — normative source.
- CR-BP-03 §6 (process-identity contract) — `identity` sub-block schema.
- CR-BP-15 §10 (version discipline on reconciled records) — companion policy.
- CR-BP-16 §S18 (conformance gate) — execution surface.
- CR-META-006 — cross-repo identifier integrity (separate; complementary).
- `01_plan/CR-BP-32-33-34-foundation/POSITIONING.md` §4.3 — harvestable insight this CR codifies.
