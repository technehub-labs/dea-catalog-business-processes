# CR-BP-mv1: Entity Storage and ID System Migration (Org-Wide, This Repo First)

**Status**: Merged (PR #149)
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-20
**Carrier**: Reconnaissance / Architectural Reconciliation slice. Establishes the org-wide id system and entity storage layout as the canonical contract for all DEA catalog repos, and migrates this repo (dea-catalog-business-processes) to the new contract.
**Depends on**: CR-BP-98 (Task schema + TASK-001..005 validator), CR-BP-102 (L4 Task decomposition pipeline; landed 2026-09-19, PR #146; produced 2,800 templated Tasks across 49 cells), CR-BP-L4-02 (P&R enrichment; landed 2026-09-20, PR #147), CR-BP-L4-03 (G&E enrichment; landed 2026-09-20, PR #148)
**Lands against**: 3,598 canonical records (49 PCs + 49 PGs + 140 BPs + 560 Activities + 2,800 Tasks); 29 conformance gates CONFORMANT; new IDM-001..007 gate wired as blocking; org-wide id map emitted at `reconciliation/migration-id-map.yaml`

---

## 1. Change Request

GitHub's web UI and Contents API truncate directory listings at 1,000 entries. `entities/v1-alpha/` held 3,549 entity dirs (2,800 task + 560 activity + 140 process + 49 group) — 3.5x over the limit, degrading browsing and tooling. The org-wide id system (`dea:*` prefix shared across all repos) could not distinguish a `dea:process-*` from this repo from a `dea:capability-*` from the capabilities repo — federation tooling and human review both relied on metadata lookup to disambiguate.

This CR migrates every canonical record to the org-wide id system and the L0-rooted containment tree:

- **Id system**: every record's `id:` field is rewritten from `dea:<level>-<slug>` to `<repo-namespace>:<level>-<domain>-<stage>[-<cell>] [-<kind>] [<hash-suffix>]`. The namespace token (`processes:`) is a stable logical name bound to this repo via the metamodel registry. The hash suffix is content-addressed (base32, 6 chars), stable across renames, verified at gate time.
- **Containment tree**: every entity directory moves from the flat pre-migration `entities/v1-alpha/dea:*` layout to `entities/v1-alpha/<pc-slug>/<pg-slug>/<bp-slug>/<activity-slug>/<task-slug>/`. The tree IS the decomposition hierarchy; containment on disk = `composes[]` in the records. Worst-case directory: ~15 entries (BP with the most Activities). Permanently under the GitHub limit.
- **Cross-reference rewriting**: every `belongs_to_*`, `composes[]`, evidence `source:`, `process_scope.*`, and change_history `cr:` field that names a record id is rewritten to the new id. Compound strings (id + prose) are rewritten with the prose preserved.
- **CI gate**: new `scripts/check_id_system.py` enforces 7 rules (IDM-001..007) as a blocking gate in `scripts/conformance_result.py` and `.github/workflows/ci.yml`.

**Per-level migration surface:**

| Level | Old id form | New id form | Records | New path |
|---|---|---|---|---|
| L0 PC | `dea:pc-<domain-ab>-<stage>` | `processes:pc-<domain>-<stage>-<hash>` | 49 | `entities/v1-alpha/<cell>/` |
| L1 PG | `dea:group-<descriptor>` | `processes:group-<domain>-<stage>-<hash>` | 49 | `entities/v1-alpha/<cell>/<pg-slug>/` |
| L2 BP | `dea:process-<verb>-<object>` | `processes:process-<domain>-<stage>-<hash>` | 140 | `entities/v1-alpha/<cell>/<pg-slug>/<bp-slug>/` |
| L3 Activity | `dea:activity-<verb>-<object>` | `processes:activity-<domain>-<stage>-<hash>` | 560 | `entities/v1-alpha/<cell>/<pg-slug>/<bp-slug>/<act-slug>/` |
| L4 Task | `dea:task-<parent-slug>-<phase>` | `processes:task-<domain>-<stage>-<phase>-<hash>` | 2,800 | `entities/v1-alpha/<cell>/<pg-slug>/<bp-slug>/<act-slug>/<task-slug>/` |

**Alias resolution**: 25 pre-existing reference aliases are normalized (e.g. `dea:pc-ge-improve` -> `dea:pc-ge-im`, `dea:pc-pr-ac` -> `dea:pc-pr-act`). These are references that use full stage names where the file uses abbreviations, or alternate abbreviations. The alias map is derived from the PC files' own `domain` + `lifecycle_stage` fields, not hardcoded.

**Pre-existing drift flagged (not fixed by this CR)**: `dea:group-strategy-and-governance-conception` (a dangling `supersedes` reference in `dea:group-governance-conception` to a historical id that no longer exists in the catalog). Skipped by the migration verify; flagged for a separate repair CR.

## 2. Migration mechanics

1. **Migration script** (`scripts/migrate_to_v3_layout.py`) loads every canonical record (3,549 from `entities/` + 49 from `contexts/`), computes the new id from the old id + record content (domain, stage, level, hash suffix), rewrites every cross-reference, computes the new filesystem path from the new id + parent chain, and writes every record to its new location. Idempotent on re-run.
2. **Hash suffix** is content-addressed: computed from the canonical YAML serialization at migration time, stable across renames, verified at gate time by recomputing and comparing.
3. **Cross-reference rewriting** handles two forms: exact match (the string IS the id) and embedded match (the string CONTAINS the id plus prose). Compound strings are rewritten with the prose preserved.
4. **Alias resolution** builds the alias map from PC files' own `domain` + `lifecycle_stage` fields, then adds explicit aliases for abbreviation variants (`dea:pc-pr-ac` -> `dea:pc-pr-act`, `dea:pc-ge-bu` -> `dea:pc-ge-b`, etc.).
5. **Path derivation** is deterministic: given a record's new id, the path is computable without external state. The CI gate enforces this.
6. **README migration**: existing README.md siblings move with their entity dirs. New level READMEs (PG, BP, Activity) are generated by the migration script's README pass; content-depth enrichment is downstream (EXT-04).

## 3. Gate posture

- Gate [22] L4 Task validation (CR-BP-98 TASK-001..005): **CONFORMANT, 2,800 records, 0 findings**.
- Gate [15] L3 Activity model (CR-BP-32 ACT-001..010 + CR-BP-97 ACT-011..015): **CONFORMANT, 560 Activity records, 0 findings**.
- Gate [23] Architectural regression (CR-BP-16 S21; BP-AR-001..007): **CONFORMANT, no architectural regressions detected**.
- Gate [23] Reconciliation matrix (CR-BP-99 RCM-001..010): **CONFORMANT, 22 rows, 0 findings**.
- New gate [30] ID System (CR-BP-mv1 IDM-001..007): **CONFORMANT, 3,598 records, 0 findings** (blocking).
- Full suite: **30 gates, 0 blocking, 0 advisory failures**.

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `scripts/migrate_to_v3_layout.py` | NEW | 400-line deterministic migration script; `--dry-run`, `--verify`, `--execute` flags; idempotent on re-run; alias resolution from PC file contents; embedded-reference rewriting with prose preservation |
| `scripts/check_id_system.py` | NEW | 250-line CI gate; 7 rules (IDM-001..007); blocking; wired into `conformance_result.py` GATES list |
| `entities/v1-alpha/` (3,549 dirs) | MOD | Flat pre-migration `dea:*` layout -> L0-rooted containment tree; every record's `id:` field rewritten; every cross-reference rewritten; every README.md moved |
| `contexts/v1-alpha/` (49 files, pre-migration location) | MOD | PC records moved to `entities/v1-alpha/<cell>/`; `id:` fields rewritten; cross-references rewritten |
| `reconciliation/migration-id-map.yaml` | NEW | Org-wide id map: every old `dea:*` id -> new `processes:*` id (3,623 entries including aliases) |
| `reconciliation/inventory.yaml` | MOD | Regenerated by `build_inventory.py` |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated by `build_inventory.py` |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated by `build_conformance_report.py` |
| `CATALOG.yaml` | MOD | Regenerated by `regenerate_catalog.py`; `open_change_requests` 119 -> 120 |
| `change-requests/CR-BP-mv1-entity-storage-and-id-system-migration.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-mv1 row added |
| `README.md` | MOD | id-system + layout summary box added |
| `CONTRIBUTING.md` | MOD | pointer to layout doc added |
| `docs/decomposition-semantic-contract.md` | MOD | example ids updated to new form |
| `docs/entity-storage-layout.md` | NEW | adapter doc referencing metamodel doc |
| `CHANGELOG.md` | MOD | structural breaking change entry |
| `.github/workflows/ci.yml` | MOD | `check_id_system.py` wired into `validate-process-entries` job |

## 5. What this CR is NOT

- **NOT a re-opening of CR-BP-98, CR-BP-102, CR-BP-L4-02, or CR-BP-L4-03.** The Task schema, the L4 decomposition pipeline, and the per-domain enrichment pattern are unchanged; this CR migrates their outputs to the new id system and layout.
- **NOT a schema, validator-rule, or record-content change.** No `_RULES` family extended; no gate added to `scripts/conformance_result.py` GATES list beyond the new IDM gate; no record's `name:`, `definition:`, `cohesion_rationale:`, or `evidence[]` content is modified. Only `id:` fields and cross-references change.
- **NOT a per-cell rather than per-domain slice.** The migration is a single coordinated change across all 49 cells; the id system and layout are org-wide contracts that cannot be partially applied.
- **NOT an L4 attestation.** Tasks remain at `lifecycle_status: candidate` / `status: candidate`; the candidate -> active transition is reserved for CR-BP-L4-15 after all 13 enrichment slices merge.
- **NOT a documentation pipeline slice.** Level READMEs are generated as structural baselines; content-depth enrichment is downstream (EXT-04).

## 6. Acceptance criteria

1. `python3 scripts/migrate_to_v3_layout.py --dry-run` reports `3,598 records would be migrated` with 0 errors.
2. `python3 scripts/migrate_to_v3_layout.py --verify` reports `VERIFY PASS: 3,598 records, 3,623 id mappings`.
3. `python3 scripts/migrate_to_v3_layout.py --execute` completes; 3,598 records migrated; `reconciliation/migration-id-map.yaml` emitted.
4. `python3 scripts/check_id_system.py` reports `CONFORMANT, 3,598 records, 0 findings`.
5. `python3 scripts/check_task_model.py` reports `Records checked: 2,800, Findings: 0, CONFORMANT`.
6. `python3 scripts/check_activity_model.py` reports `Activity records: 560, Findings: 0, CONFORMANT`.
7. `python3 scripts/check_architectural_regression.py` reports `CONFORMANT, no architectural regressions detected`.
8. `python3 scripts/check_reconciliation_matrix.py` reports 22 rows, 0 findings, matrix_version 5 unchanged.
9. Full pytest suite passes; `scripts/conformance_result.py` remains CONFORMANT (30 gates, 0 blocking, 0 advisory failures).
10. `python3 scripts/check_cr_metadata.py` reports 0 new findings on this CR (Process Catalog layer; standard 7-section header shape).
11. Em-dash / en-dash audit: 0 violations in new prose.
12. CI: 3/3 green (`conformance`, `validate-process-entries`, `allocation / validate`).
13. Idempotence: re-running `python3 scripts/migrate_to_v3_layout.py --execute` on the migrated tree produces no diff.
14. Rollback: `git revert` of the migration commit restores both id and path state; gates revert in the same commit.

## 7. Result

CR-BP-mv1 migrates the dea-catalog-business-processes repo to the org-wide id system and the L0-rooted containment tree. Every canonical record's `id:` field is rewritten from `dea:*` to `processes:*`, every cross-reference is rewritten to the new id form, every entity directory moves to the containment tree, and the new `check_id_system.py` gate enforces the contract as a blocking CI gate. The 30-gate suite remains CONFORMANT (0 blocking, 0 advisory). The migration id map is emitted at `reconciliation/migration-id-map.yaml` for auditability. Sibling repos (business-capabilities, business-services, actors, orgunits, objects, stakeholders) follow as Wave 2/3 migrations with the same recipe.

### Counts (post-merge)

| Metric | Before (PR #148) | After (this slice) |
|---|---|---|
| L0 Process Contexts | 49 | 49 (unchanged in count; ids rewritten) |
| L1 Process Groups | 49 | 49 (unchanged in count; ids rewritten) |
| L2 Business Processes | 140 | 140 (unchanged in count; ids rewritten) |
| L3 Activity records | 560 | 560 (unchanged in count; ids rewritten) |
| L4 Task records | 2,800 | 2,800 (unchanged in count; ids rewritten) |
| Entities (catalog index) | 3,549 | 3,549 (unchanged in count; paths changed) |
| ECF entries | 3,550 | 3,550 (unchanged in count; paths changed) |
| Matrix rows | 22 | 22 (unchanged) |
| Matrix rows closed | 16 | 16 (unchanged) |
| `open_change_requests` | 119 | **120** (+1) |

## 8. Cross-check stage (XC-01..11)

Per the org-wide structural-change cross-check directive (every historical artifact audited, not just live and future work), this CR carries the cross-check walk-down for the id-system migration. Mechanism: `scripts/cross_check_org_wide.py` (XC-A legacy path forms, XC-B legacy repo names, XC-C id resolution against the current catalog + migration id map). Report: `reconciliation/cross-check-org-wide.md`. Enforcement going forward: IDM-008 (PR-scoped coherence gate) in `scripts/check_id_system.py`, wired into `ci.yml` with a per-PR `id-system-coherence-report.md` artifact.

Historical-artifact treatment: no historical CR or ADR is rewritten. Each flagged artifact received a file-level `Layout note (CR-BP-mv1, 2026-09-20)` banner declaring its pre-migration framing; content stays verbatim. The checker honors the banner as the historical-framing declaration (bannered files report HISTORICAL-ONLY; unbannered legacy forms report NEEDS-FRAMING and block).

| Slot | Cohort | Count | Status | Evidence |
|---|---|---|---|---|
| XC-01 | Admission CRs (CR-BP-64..89 wave + CR-BP-101) | 19 CRs bannered | HISTORICAL-ONLY after banner | banner + XC report |
| XC-02 | Gate CRs (CR-BP-14, CR-BP-15, CR-BP-100) | 3 CRs bannered; CR-BP-16/40/95/100a CLEAN | HISTORICAL-ONLY after banner | banner + XC report |
| XC-03 | Slice CRs (CR-BP-34a..d, CR-BP-102) | 5 CRs bannered; CR-BP-98 CLEAN | HISTORICAL-ONLY after banner | banner + XC report |
| XC-04 | L4 pipeline CRs | CR-BP-L4-02 bannered; CR-BP-L4-03 bannered (PR #148 merged ahead of this slice; banner landed in this PR) | HISTORICAL-ONLY after banner | banner + XC report |
| XC-05 | Foundation, L3-tranche, hygiene, release, and reconciliation CRs (all remaining bannered CRs in this repo) | 49 CRs bannered | HISTORICAL-ONLY after banner | banner + XC report |
| XC-06 | Metaframework ADRs (`dea-metaframework/docs/adr/`) | ADR-ECF-003 flagged; banner rides PR #31 | HISTORICAL-ONLY | commit on `docs/id-system-and-entity-storage-layout` |
| XC-07 | Metamodel ADRs (`dea-metamodel/docs/adr/`) | 0 flagged | CLEAN | XC report |
| XC-08 | Architecture-framework ADRs (`dea-architecture-framework/docs/ADRs/`) | 0002 + 0006 flagged; banners in PR #14 | HISTORICAL-ONLY | PR #14 |
| XC-09 | Id-map provenance + known residuals | `reconciliation/migration-id-map.yaml` (3,623 entries); 1 documented dangling `supersedes` lineage ref (pre-existing on main; repair CR queued); register audit gate walker repaired for the containment tree (pre-existing flat-layout glob; gate not wired in CI, drift invisible) + AO x Retire cell `audit_status` corrected to `landed` (pre-existing drift on main) | COMPLETE + DOCUMENTED | IDM-004 well-formedness + uniqueness, 0 findings on 3,598 records; IDM-006 exempts only the documented residual value |
| XC-10 | PR #148 absorption | 340 enriched G&E Task YAMLs landed on main pre-migration-merge | COMPLETE: #148 merged 2026-09-20; absorbed into this branch via three-way splice (migration id/structure kept, #148 enriched definition/trigger/outcome/boundary/evidence spliced in, legacy `dea:*` references in spliced content rewritten through the id map); the earlier stacked-recovery plan is retired | merge commit on this branch + IDM-008 gate |
| XC-11 | Forward enforcement | every future CR/ADR/record PR | ENFORCED: IDM-008 blocking in CI; coherence report uploaded per PR | `ci.yml` IDM-008 step |

### XC-01: Admission CRs (19 bannered)

- `CR-BP-64-pv-activate-retire-admission.md`
- `CR-BP-65-ge-activate-admission.md`
- `CR-BP-66-eo-retire-admission.md`
- `CR-BP-67-pr-retire-admission.md`
- `CR-BP-68-pc-processes-hygiene.md`
- `CR-BP-69-admitted-bp-l3-decomposition.md`
- `CR-BP-71-pr-activate-admission.md`
- `CR-BP-73-ao-retire-admission.md`
- `CR-BP-75-fa-retire-admission.md`
- `CR-BP-77-l3-admitted-regulated-tranche.md`
- `CR-BP-78-ge-retire-admission.md`
- `CR-BP-79-l3-ge-retire-admission.md`
- `CR-BP-81-ao-activate-admission.md`
- `CR-BP-82-eo-activate-admission.md`
- `CR-BP-83-fa-activate-admission.md`
- `CR-BP-86-sd-activate-admission.md`
- `CR-BP-87-l3-admitted-activate-tranche.md`
- `CR-BP-89-four-cell-programme-retrospective.md`
- `CR-BP-101-sd-retire-admission.md`

### XC-02: Gate CRs (3 bannered)

- `CR-BP-14-process-semantic-reconciliation.md`
- `CR-BP-15-process-catalog-reconciliation.md`
- `CR-BP-100-l0-l1-cardinality-gate.md`

### XC-03: Slice CRs (5 bannered)

- `CR-BP-34a-l2-qualification-validators.md`
- `CR-BP-34b-intent-purposive-validators.md`
- `CR-BP-34c-lifecycle-state-machine.md`
- `CR-BP-34d-semantic-identity-vs-version.md`
- `CR-BP-102-l4-decomposition-pipeline.md`

### XC-04: L4 pipeline CRs (2 bannered)

- `CR-BP-L4-02-pr-domain-content-enrichment.md`
- `CR-BP-L4-03-ge-domain-content-enrichment.md` (bannered in this PR after #148 merged ahead of the migration)

### XC-05: Foundation, L3-tranche, hygiene, release, and reconciliation CRs (49 bannered)

- `CR-BP-02.md`
- `CR-BP-03-business-process-architecture.md`
- `CR-BP-03A-legacy-migration.md`
- `CR-BP-03C-sample-process-contribution.md`
- `CR-BP-04-id-family-reconciliation.md`
- `CR-BP-11-l1-process-group-discovery.md`
- `CR-BP-12-process-group-profile.md`
- `CR-BP-17-ecf-domain-enum-migration.md`
- `CR-BP-18-ecf-domain-enum-agency-migration.md`
- `CR-BP-19-l1-register-rederivation-ecf-v240.md`
- `CR-BP-20-l1-l2-alignment-ecf-v240.md`
- `CR-BP-22-register-audit-status.md`
- `CR-BP-23.md`
- `CR-BP-25-phase-20-governance-review.md`
- `CR-BP-26.md`
- `CR-BP-28.md`
- `CR-BP-29.md`
- `CR-BP-30-release-package.md`
- `CR-BP-36-mece-validation.md`
- `CR-BP-38-ecf-matrix-population-retrospective.md`
- `CR-BP-41-v030-release-cut.md`
- `CR-BP-42-l3-activity-pilot.md`
- `CR-BP-43-l3-eo-operate-tranche.md`
- `CR-BP-44-l3-pr-operate-improve-tranche.md`
- `CR-BP-45-l3-pr-conceive-design-build-tranche.md`
- `CR-BP-46-l3-eo-conceive-design-tranche.md`
- `CR-BP-47-l3-eo-build-improve-tranche.md`
- `CR-BP-48-l3-ge-conceive-design-build-tranche.md`
- `CR-BP-49-l3-ge-improve-operate-tranche.md`
- `CR-BP-50-l3-pv-conceive-design-build-tranche.md`
- `CR-BP-51-l3-pv-improve-operate-tranche.md`
- `CR-BP-52-l3-fa-conceive-design-build-tranche.md`
- `CR-BP-53-l3-fa-improve-operate-tranche.md`
- `CR-BP-54-l3-sd-conceive-design-build-tranche.md`
- `CR-BP-55-l3-sd-improve-operate-tranche.md`
- `CR-BP-56-l3-ao-conceive-design-build-tranche.md`
- `CR-BP-57-l3-ao-improve-operate-tranche.md`
- `CR-BP-58-pg-gate-repair-dangle-removal.md`
- `CR-BP-60-l3-docs-currency.md`
- `CR-BP-90-v040-release-cut.md`
- `CR-BP-91-deprecated-bp-l3-exclusion.md`
- `CR-BP-92-recon-decomposition-and-execution-boundary-hardening.md`
- `CR-BP-94-EXT-01-documentation-architecture.md`
- `CR-BP-94-EXT-02-readme-generation.md`
- `CR-BP-99-reconciliation-matrix.md`
- `CR-BP-101a-sd-retire-activity-decomposition.md`
- `CR-BP-SPEC-BP-01.md`
- `CR-CATALOG-STRUCT-02.md`
- `CR-ECF-CG-004.md`

### XC-06/07/08: Sibling-repo ADRs

- `dea-metaframework/docs/adr/ADR-ECF-003.md` (banner on `docs/id-system-and-entity-storage-layout`, rides PR #31)
- `dea-architecture-framework/docs/ADRs/0002-opendeam-v0-2-0-structural-upgrade.md` (PR #14)
- `dea-architecture-framework/docs/ADRs/0006-opendeam-v0.6.0-process-kernel-specialization.md` (PR #14)
- `dea-metamodel/docs/adr/`: 0 flagged, CLEAN

Final checker state at PR open: 145 artifacts scanned; 64 CLEAN; 81 HISTORICAL-ONLY (CR-BP-L4-03 included after PR #148 merged ahead of this slice); 0 NEEDS-FRAMING in this repo; 0 UNRESOLVED-REFS. (The three sibling-repo ADRs showed NEEDS-FRAMING until their banners landed; the report regenerates on the cross-check script's next run.)