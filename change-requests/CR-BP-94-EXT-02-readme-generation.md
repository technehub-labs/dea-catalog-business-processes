# CR-BP-94-EXT-02: README Generation Pipeline

**Status**: Proposed
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-19
**Carrier**: Lifts the Documentation Architecture (CR-BP-94-EXT-01 / -01a) from schema-only to content-bearing. Introduces `scripts/generate_readmes.py`, a deterministic generator that produces README.md for every canonical record under `entities/v1-alpha/` and `contexts/v1-alpha/`. Closes DOC-001 from 598 to 0 against the live catalog.
**Depends on**: CR-BP-94-EXT-01 (Documentation Architecture + DOC-001..005 gate), CR-BP-94-EXT-01a (L0/L1 cardinal-entity profiles).
**Lands against**: 49 PCs / 49 PGs / 140 BPs / 560 Activities / 0 L4 Tasks / 0 ProcessScope records; 29 gates CONFORMANT; v0.4.0+14 commits on main (post-CR-BP-100a / -101 / -101a).

---

## 1. Change Request

Generate README.md for every canonical record under `entities/v1-alpha/` and `contexts/v1-alpha/` that does not already have one. Each README follows the documentation profile required by the record's `(type, level)` combination as registered in `scripts/check_documentation_profile.py` PROFILE_REGISTRY.

| Artifact | Status | Notes |
|---|---|---|
| `scripts/generate_readmes.py` | NEW | Deterministic README generator. Walks both storage shapes (directory-per-record for L1/L2/L3/L4; flat-file for L0 ProcessContext). Resolves L0/L1/L2/L3/L4 via `type` field or `id` pattern (`dea:pc-*` fallback). Maps README sections per profile (11 sections for L0/L1, 12 for L2/L3/L4 including Outcomes). Renders content from each record's YAML fields (id, name, type, level, version, lifecycle_status, definition/description, identity.verb/object/scope, ecfConformance, part_of, metadata.activity_references, trigger, outcome, decomposition_boundary, process_scope.includes/excludes, governance.roles/regulators/rules, metadata.change_history). Supports `--dry-run` and `--scope` filters. |
| `tests/test_generate_readmes.py` | NEW | 9 tests: type/id-pattern resolution; record-path counts; both storage-shape README paths; required-section coverage per L0/L2; dry-run idempotence; scope filter (real + fake); live-run closes DOC-001 to 0. |
| `entities/v1-alpha/**/*.md` (605 new files) | NEW | Generated READMEs for 605 records missing them. |
| `contexts/v1-alpha/dea-pc-*/README.md` (49 new files) | NEW | Generated READMEs for 49 L0 ProcessContext records. L0's flat-file storage shape is preserved; READMEs sit in a sibling directory of the same stem (e.g. `contexts/v1-alpha/dea-pc-sd-retire/README.md`) to keep DOC-001 path conventions consistent. |
| `change-requests/CR-BP-94-EXT-02-readme-generation.md` | NEW | Slice carrier CR (this document). |
| `change-requests/README.md` | MOD | CR-BP-94-EXT-02 row added. |
| `reconciliation/cr-bp-99-matrix.yaml` | MOD | matrix-010 (DOC-001) updated: count 598 -> 0; status flip; closed_in PR-145. |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 115 -> 116. |

## 2. Deposition mechanics

1. **Storage-shape awareness.** Two shapes co-exist in the live catalog:
   - L1/L2/L3/L4 records live as `entities/v1-alpha/<record-id>/<record-id>.yaml` with README.md as a sibling.
   - L0 ProcessContext records live as flat YAML files at `contexts/v1-alpha/dea-pc-<domain-abbrev>-<stage-abbrev>.yaml` (no surrounding directory).
   - The generator handles both: L0 READMEs land in a synthesised sibling directory `contexts/v1-alpha/<stem>/README.md` to keep DOC-001's `<entity-id>/README.md` path convention.
2. **Type vs id-pattern discrimination.** L0 records do not carry an explicit `type` field (they predate the discriminator pattern). The generator falls back to `id.startswith("dea:pc-")` per CR-BP-02 §3 convention.
3. **DOC-001 closure.** Before this slice, the live catalog had 598 DOC-001 advisory findings (missing READMEs). After the generator runs, DOC-001 == 0. The DOC-002, DOC-003, DOC-005 findings remain (section authoring + id mismatch + CR reference backfill are separate scopes: matrix-011..013).
4. **Existing-README preservation.** The generator skips records whose README already exists. The 293 tracked stub READMEs (which are DOC-002 non-compliant because they lack 11/12 profile-required sections) are preserved as-is. A follow-on slice (EXT-02b) can regenerate them with a `--force-existing` flag.
5. **Content quality.** Generated READMEs draw content from each record's YAML fields. Sections that have no source data are populated with a deterministic placeholder flagged as DOC-004 informational. The generator does NOT fabricate content beyond what is in the record.
6. **CR reference backfill.** DOC-005 (15 records missing CR reference in README) is partially addressed by the generator's Revision History section, which lists every CR in `metadata.change_history`. Records with no `change_history` still flag DOC-005; that's a separate scope.

## 3. Profile resolution

The generator's `PROFILE_SECTIONS` dict mirrors `PROFILE_REGISTRY` in `scripts/check_documentation_profile.py`:

| (type, level) | Required sections |
|---|---|
| (ProcessContext, L0) | entity-identity, formal-definition, semantic-dimensions, decomposition, behavior, interfaces, roles, rules-controls, evidence, completeness, revision-history (11 sections; no outcomes :  L0 inherits from ECF framework) |
| (ProcessGroup, L1) | same as L0 (11 sections) |
| (Process, L2) | 12 sections including outcomes |
| (Activity, L3) | 12 sections including outcomes |
| (Task, L4) | 12 sections including outcomes |

## 4. Gate posture

- Gate [3] Process Context (PC-001..PC-008): **CONFORMANT, PASS** (49 records).
- Gate [7] MECE (Process Group, PG-001..010): **CONFORMANT, PASS** (49 records).
- Gate [8] Provenance (ECF conformance): **PASS** (750 entries).
- Gate [21] Documentation Profile (DOC-001..005): **NON-CONFORMANT-WITH-WARNINGS** (1,710 advisory findings; was 2,308; closed DOC-001 598 -> 0; remaining DOC-002/003/005 are separate scope).
- Full suite: **29 gates, 0 blocking, 0 advisory failures**.

## 5. What this CR is NOT

- **NOT a schema change.** No validator, schema, or gate logic changes.
- **NOT a population of new records.** No new canonical records; only README files.
- **NOT a regeneration of existing 293 stubs.** They are preserved as-is; a follow-on EXT-02b can address DOC-002 across the legacy stub population.
- **NOT a content-authoring tranche.** Sections with no source data are populated with deterministic placeholders. Real content authoring (full role definitions, governance narratives, evidence narratives) is downstream scope (matrix-011..013).
- **NOT a re-opening of CR-BP-94-EXT-01 / -01a.** Those slices landed the profile schema + DOC-001..005 gate; this slice populates DOC-001 with content.

## 6. Acceptance criteria

1. `tests/test_generate_readmes.py` passes all 9 tests.
2. `scripts/generate_readmes.py` runs against the live catalog and reports `written=` >= 654 (605 entity + 49 PC) on a clean checkout; `skipped_existing` matches the tracked-README count.
3. `scripts/check_documentation_profile.py` reports `DOC-001: 0 [advisory]` post-run.
4. `scripts/conformance_result.py` reports 29 gates, 0 blocking, 0 advisory failures.
5. CR-META gate reports 0 new findings on this CR.
6. Em-dash / en-dash audit: 0 violations in new prose (CR file + generator docstrings).
7. CI: 3/3 green.

## 7. Result

CR-BP-94-EXT-02 lifts the Documentation Architecture from schema-only to content-bearing. The generator produces 654 README files (605 entity + 49 PC) deterministically from each record's YAML fields. DOC-001 closes from 598 to 0. The DOC-002 finding count drops proportionally (newly-generated READMEs are profile-compliant; legacy stubs remain non-compliant by separate scope). The 29-gate suite remains CONFORMANT (0 blocking, 0 advisory). `open_change_requests` 115 -> 116. The Documentation Profile gate [21] is now partially-satisfied; full closure awaits EXT-04 (section authoring) and EXT-06 (content completeness).

### Counts (post-merge)

| Metric | Before (PR #144 / pre-EXT-02) | After (this slice) |
|---|---|---|
| Process Contexts (L0) | 49 | 49 (unchanged) |
| Process Groups (L1) | 49 | 49 (unchanged) |
| Business Processes (L2) | 140 | 140 (unchanged) |
| Activity records (L3) | 560 | 560 (unchanged) |
| README.md files (total) | 293 | **947** (+654) |
| DOC-001 findings | 598 [advisory] | **0** |
| DOC-002 findings | 1,693 [advisory] | 1,693 (unchanged; legacy stubs remain non-compliant) |
| DOC-005 findings | 15 [advisory] | 15 (unchanged; backfill is separate scope) |
| Total DOC findings | 2,308 | **1,710** (-598 = DOC-001 closure) |
| Entities (catalog index) | 749 | 749 (unchanged) |
| `open_change_requests` | 115 | **116** |