# CR-CATALOG-STRUCT-02: Process Catalog Adoption (Three-Step Migration)

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Proposed
**Layer**: L1 (Process Catalog)
**Owner**: TechNeHub Labs
**Depends on**: CR-CATALOG-STRUCT-01 (merged; PR #10), CR-CATALOG-STRUCT-06a (merged; PR #11), CR-CATALOG-STRUCT-06b (merged; PR #12)
**Supersedes**: none
**Related**: CR-CATALOG-STRUCT-03..05 (other catalog adoptions); CR-CATALOG-STRUCT-07 (cross-repo consumer)
**Authority**: Mandatory; enforced by CI on every PR

---

## 1. Purpose

Bring `technehub-labs/dea-catalog-processes` into conformance with the catalog repository standard (CR-CATALOG-STRUCT-01). The standard defines a per-entity subtree shape (`entities/v1-alpha/<entity-id>/{canonical, research, candidates, retired}`), a machine-generated `CATALOG.yaml` index, a CI gate, and a cross-repo conformance suite (CST-001..CST-016).

This is the **first adoption CR** among STRUCT-02..05. It runs the standard's three-step migration (layout, research distribution, contribution flow codification) end-to-end on the existing catalog's two entities.

## 2. Scope

**In scope**:

- **Step 1: adopt the layout**. Move `entities/v1-alpha/<flat>.yaml` files into per-entity subtrees with `research/`, `candidates/`, `retired/` state directories (initially empty `.gitkeep` placeholders).
- **Step 2: distribute research**. Move `docs/research/*` files into the per-entity `research/` subdirectories that own them. Write a provenance `README.md` per subtree recording origin, governing CRs, and why each subtree owns its research.
- **Step 3: codify the contribution flow**. The existing `contributions/processes/` intake queue and template stay in place (per the migration's Q3 decision); the contribution-report workflow is unchanged.
- **`CATALOG.yaml` index**. Generate, validate, and commit the machine-generated index.
- **`metamodel-pointer.yaml` augmentation**. Add the canonical top-level `id`/`name`/`abbreviation`/`version`/`status`/`metamodel_version`/`description`/`owner` keys the regenerator reads. Existing nested `metamodel:` and `catalog:` blocks remain unchanged.
- **CI workflow update**. Replace the existing schema-dispatch-only workflow with one that runs regenerator + gate + schema validation + 7 validators + conformance suite.
- **Bug fix in `scripts/check_ecf_conformance.py`**: skip files under `research/`, `candidates/`, `retired/` (state-directory artifacts are not catalog entries and are not required to carry the `ecfConformance` block).
- **Vendored regenerator + gate + schema**. Per CST-013/CST-014: the catalog must carry `scripts/regenerate_catalog.py`, `scripts/check_catalog_index.py`, and `catalog-index-schema/catalog-index-schema.json`. Vendored from `dea-metaframework/tools/` at this CR's authoring time.

**Out of scope**:

- New entities or content changes. The migration is purely structural.
- Renaming the contribution queue (Q3 decision: keep `contributions/processes/`).
- Migrating other catalog repos (STRUCT-03..05).
- The cross-repo consumer (STRUCT-07).

## 3. Definitions

- **Per-entity subtree**: `entities/v1-alpha/<entity-id>/`. Contains one canonical YAML at the root and four state directories (`research/`, `candidates/`, `retired/`, plus the canonical file).
- **State directory file**: any YAML or Markdown file under a subtree's `research/`, `candidates/`, or `retired/` directory. State-directory files are research, candidate, or retired artifacts, NOT catalog entries. They are not validated against the entity schema.
- **Hand-rolled adoption**: this CR authors files directly rather than running `bootstrap_catalog_repo.py` against the existing catalog. The standard's §13 retroactive schedule allows hand-rolling; CST-016 emits a warning rather than an error when a catalog's `TEMPLATE_VERSION` matches the template's current version but the catalog predates the bootstrap script.
- **`TEMPLATE_VERSION`**: a single-line semver file. This catalog's version is `0.1.0`, matching the canonical template at the time of this CR.

## 4. Design

### 4.1 Step 1: layout migration

Two entity subtrees are created. Each subtree has the canonical file at its root plus empty `research/`, `candidates/`, and `retired/` directories with `.gitkeep` placeholders so git tracks them.

| Before | After |
|---|---|
| `entities/v1-alpha/dea_bp_manage-customer-relationship.yaml` | `entities/v1-alpha/dea:process-manage-customer-relationship/dea:process-manage-customer-relationship.yaml` |
| `entities/v1-alpha/dea_group-customer-lifecycle-management.yaml` | `entities/v1-alpha/dea:group-customer-lifecycle-management/dea:group-customer-lifecycle-management.yaml` |

The `dea_bp_*` legacy file names were renamed to `dea:process-*` form (canonical per CR-BP-04) at the same time as the move. The git history preserves the rename via `git mv`; the file content is unchanged. The `entities/v1-alpha/README.md` index file is preserved as-is.

### 4.2 Step 2: research distribution

The 3 research files in `docs/research/` are about **L1 Process Groups** (the 49-coordinate Domain x Lifecycle matrix and the 38 accepted / 11 deferred / 102 candidates disposition). They land in the L1 entity's research subtree:

| Before | After |
|---|---|
| `docs/research/l1-register.yaml` | `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml` |
| `docs/research/l1-candidate-universe.yaml` | `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-candidate-universe.yaml` |
| `docs/research/L1-REGISTER-v0.1.md` | `entities/v1-alpha/dea:group-customer-lifecycle-management/research/L1-REGISTER-v0.1.md` |

The empty `docs/research/` directory is removed. A `research/README.md` per subtree records provenance (origin path, governing CR, migration date) and explains why each subtree owns its research.

The L2 entity (`dea:process-manage-customer-relationship`) gets an empty `research/` subdirectory with a `README.md` recording the governing CRs (BP-03, BP-03A, BP-04, BP-12) and noting that L2-specific evidence has not yet been accumulated.

### 4.3 Step 3: contribution flow codification

The existing `contributions/processes/` intake queue stays in place. It carries:

- `PROCESS-CONTRIBUTION-TEMPLATE.yaml` (CR-BP-03 §9): the per-entity-type template.
- `README.md`: contributor instructions.
- `dea_bp_manage-customer-relationship.yaml` + `.report.md`: the canonical sample contribution from CR-BP-03C.

The template's filename (`PROCESS-CONTRIBUTION-TEMPLATE.yaml`) is more specific than the standard's `CONTRIBUTION-TEMPLATE.yaml`. The standard does not enforce the filename; CST-016 does not check it; renaming would break 8 documented references across `README.md`, `CHANGELOG.md`, `docs/`, `change-requests/`, and `.github/workflows/`. The migration keeps the existing name; the standard's intent ("one per-entity-type template per catalog") is satisfied.

The contribution-report workflow (`.github/workflows/process-contribution-report.yml`) is unchanged. It already runs the contribution-report logic correctly; the CI changes in §4.5 are additive.

### 4.4 metamodel-pointer.yaml augmentation

The regenerator reads top-level `id`, `name`, `abbreviation`, `version`, `status`, `metamodel_version`, `description`, and `owner` keys. The existing pointer file's metadata is nested under `metamodel:` and `catalog:` blocks; the regenerator's defaults produce ugly doubled values (`dea:catalog-dea-catalog-processes`).

The fix is purely additive: insert a labeled top-level metadata block before `metamodel:`. The values mirror the existing nested `catalog:` block's identity fields; the nested blocks remain untouched. A code comment in the pointer file explicitly notes the duplication and the constraint that the two MUST stay in sync.

### 4.5 CI workflow update

The existing workflow `validate` is extended to run, in order:

1. **Regenerator check** (`python scripts/regenerate_catalog.py --check --schema catalog-index-schema/catalog-index-schema.json`). Fails if the committed `CATALOG.yaml` is stale.
2. **Gate** (`python scripts/check_catalog_index.py --strict --schema ...`). Fails if schema or structural sanity checks fail.
3. **Per-file schema validation** (existing inline Python; filtered to skip state-directory files).
4. **The six existing catalog validators** (CR-ECF-CG-004, CR-BP-SPEC-BP-01, CR-BP-02, CR-BP-03, CR-BP-03A, CR-BP-12).
5. **Cross-repo conformance suite** (`python .metaframework/tools/conformance_test_catalog_structure.py --catalog-root . --template-root .metaframework/tools/catalog-repo-template --strict`).

The conformance suite fetches `dea-metaframework` as a sibling checkout at CI time; the catalog's vendored scripts are the source of truth for local development and offline use. The two paths stay in sync via the dea-metaframework pull (re-cp the scripts when bumping `TEMPLATE_VERSION`).

The `process-contribution-report.yml` workflow is unchanged.

### 4.6 Vendored regenerator + gate

CST-013 requires `scripts/regenerate_catalog.py`; CST-014 requires `scripts/check_catalog_index.py`. The schema lives at `catalog-index-schema/catalog-index-schema.json` (a sibling directory to keep the catalog root clean and parallel to the standard's `tools/` layout).

This CR vendors the canonical implementations from `dea-metaframework/tools/` at authoring time. Future bumps to the metaframework's regenerator or gate require re-vendoring; the CR includes a note that the vendored copies should track `dea-metaframework` `main` at template-version bumps.

### 4.7 Bug fix: ecf_conformance scans state-directory files

`scripts/check_ecf_conformance.py` walks every YAML under `entities/v1-alpha/**/*.yaml` recursively. Before this CR, that glob matched only the two flat files at the directory root. After Step 1, the layout has 2 canonical files plus 3 research files; the validator started flagging research files as missing the `ecfConformance` block.

Research files are not catalog entries and do not carry `ecfConformance`. The fix is in `scripts/check_ecf_conformance.py`: skip files under `research/`, `candidates/`, or `retired/` per the standard's §5 distinction between canonical entries and state-directory artifacts. The CI workflow's per-file schema dispatch gets the same filter.

## 5. Files

**Modified** (10):

- `entities/v1-alpha/dea:process-manage-customer-relationship/dea:process-manage-customer-relationship.yaml` (moved from `entities/v1-alpha/dea_bp_manage-customer-relationship.yaml`).
- `entities/v1-alpha/dea:group-customer-lifecycle-management/dea:group-customer-lifecycle-management.yaml` (moved from `entities/v1-alpha/dea_group-customer-lifecycle-management.yaml`).
- `entities/v1-alpha/dea:group-customer-lifecycle-management/research/{l1-register.yaml, l1-candidate-universe.yaml, L1-REGISTER-v0.1.md}` (moved from `docs/research/`).
- `metamodel-pointer.yaml` (additive top-level metadata block; nested blocks unchanged).
- `scripts/check_ecf_conformance.py` (skip state-directory files).
- `.github/workflows/ci.yml` (regenerator + gate + conformance steps; filter state-directory files in per-file dispatch).

**New** (8):

- `CATALOG.yaml` (machine-generated; 1.9 KB).
- `TEMPLATE_VERSION` (`0.1.0`).
- `scripts/regenerate_catalog.py` (vendored copy; 25 KB).
- `scripts/check_catalog_index.py` (vendored copy; 11 KB).
- `catalog-index-schema/catalog-index-schema.json` (vendored copy; 7 KB).
- `entities/v1-alpha/dea:group-customer-lifecycle-management/research/README.md` (provenance).
- `entities/v1-alpha/dea:process-manage-customer-relationship/research/README.md` (provenance + governing CRs).
- `change-requests/CR-CATALOG-STRUCT-02.md` (this document).

**Removed**: `docs/research/` (empty after the three research files moved out; the directory itself is removed).

**Documentation housekeeping** (3):

- `CHANGELOG.md` (`[Unreleased]` entry).
- `change-requests/README.md` (row for CR-CATALOG-STRUCT-02; flips CR-CATALOG-STRUCT-06b from Proposed to Merged).
- `docs/standards/catalog-repository-pattern-adoption.md` (this row's status flips to `in-progress` while PR is open, `conforming` after merge).

## 6. Conformance contract

This CR is conformant iff:

1. All 6 existing catalog validators (`check_ecf_conformance`, `check_legacy_migration`, `check_process_context`, `check_process_group`, `check_process_identity`, `check_process_specialization`) PASS.
2. `python scripts/regenerate_catalog.py --check --schema catalog-index-schema/catalog-index-schema.json` exits 0.
3. `python scripts/check_catalog_index.py --strict --schema ...` exits 0.
4. `python /path/to/dea-metaframework/tools/conformance_test_catalog_structure.py --catalog-root . --template-root .../tools/catalog-repo-template --strict` exits 0 with 0 warnings (because `TEMPLATE_VERSION` matches and the layout is conformant).
5. `git diff --check` clean.
6. Dash-clean on all new prose.
7. No secrets introduced.

## 7. Decisions log

### D-STRUCT-02-001: research under L1 entity

Per the planning conversation's Q1 decision (b): research is about L1 Process Groups; the L1 entity owns its research. The 3 research files from CR-BP-11 land under `dea:group-customer-lifecycle-management/research/`. The L2 entity's research subtree is empty (with a README recording governing CRs and explaining the absence).

### D-STRUCT-02-002: hand-roll, no bootstrap script

Per the planning conversation's Q2 decision (a): the migration is surgical and step-by-step. The bootstrap script would rewrite every file in the catalog with new timestamps and lose the BP-11/BP-04/BP-12 commit history attribution. `TEMPLATE_VERSION` is written manually as `0.1.0`; CST-016 reports "in sync" because the value matches the canonical template.

### D-STRUCT-02-003: keep `contributions/processes/` + existing template name

Per the planning conversation's Q3 decision (a): the catalog hosts one entity type (Process); the directory name encodes that. Renaming `PROCESS-CONTRIBUTION-TEMPLATE.yaml` to `CONTRIBUTION-TEMPLATE.yaml` would break 8 documented references. The migration keeps both the directory and the template name.

### D-STRUCT-02-004: catalog index schema in `catalog-index-schema/`

The standard's regenerator reads the schema at `--schema catalog-index-schema/catalog-index-schema.json`. The schema lives in a sibling directory of `scripts/` rather than in `schemas/` to keep catalog-level index machinery separate from entity-level schemas.

### D-STRUCT-02-005: regenerate on every PR, conformance on every PR

Both the regenerator check (fast; filesystem-only) and the conformance suite (subprocess of regenerator + gate + CSTs) run on every PR. The combined runtime is under 30 seconds.

## 8. Usage

After this CR merges:

```bash
# Verify conformance locally
python /path/to/dea-metaframework/tools/conformance_test_catalog_structure.py \
    --catalog-root . \
    --template-root /path/to/dea-metaframework/tools/catalog-repo-template \
    --strict

# Refresh CATALOG.yaml after adding/removing entities
python scripts/regenerate_catalog.py --schema catalog-index-schema/catalog-index-schema.json

# Validate the committed index
python scripts/check_catalog_index.py --strict --schema catalog-index-schema/catalog-index-schema.json

# Run the full local validator suite
for v in check_ecf_conformance check_legacy_migration check_process_context \
         check_process_group check_process_identity check_process_specialization; do
    python scripts/${v}.py
done
```

CI runs the same steps on every PR; failures block merge.

## 9. Out of scope (deferred)

- **STRUCT-03..05**: adoption CRs for the other 3 catalog repos.
- **STRUCT-07**: cross-repo consumer.

## 10. Acceptance criteria

1. All 6 existing validators PASS.
2. Regenerator --check exits 0.
3. Gate --strict exits 0.
4. Conformance --strict exits 0 with 0 warnings.
5. CR doc is dash-clean.
6. No secrets introduced (verified by per-file staged-file scan).
7. CHANGELOG, CR README, and adoption tracker updated.
8. CI on the branch is green.

## 11. Risks

- **R-STRUCT-02-001**: Vendored regenerator/gate drift from `dea-metaframework` `main`. Mitigation: re-vendor on every `TEMPLATE_VERSION` bump; CI fetches and re-runs the suite as a freshness check.
- **R-STRUCT-02-002**: Future research distribution to wrong subtree. Mitigation: `research/README.md` per subtree records provenance and ownership rationale.
- **R-STRUCT-02-003**: `metamodel-pointer.yaml` top-level vs nested blocks drift. Mitigation: pointer file comment explicitly notes the duplication and the sync requirement; a future CR can add a validator that checks both forms agree.

## 12. Open questions

None at authoring time. Resolved during planning:

- Research under L1 (D-001).
- Hand-roll vs bootstrap (D-002).
- Keep contribution queue name (D-003).

## 13. Related

- CR-CATALOG-STRUCT-01 (merged): the standard this CR implements.
- CR-CATALOG-STRUCT-06a (merged): the regenerator + gate + schema.
- CR-CATALOG-STRUCT-06b (merged): the conformance suite + template + bootstrap.
- CR-BP-11 (merged): the 49-coordinate L1 disposition register whose files move in Step 2.
- CR-BP-12 (merged): the Process Group profile that first established `dea:group-customer-lifecycle-management` as a canonical record.
- CR-BP-04 (merged): id-family reconciliation that locked the canonical `dea:process-*` form (which the rename in Step 1 applies).

---

## Appendix A: Per-file migration map

| Before path | After path | Reason |
|---|---|---|
| `entities/v1-alpha/dea_bp_manage-customer-relationship.yaml` | `entities/v1-alpha/dea:process-manage-customer-relationship/dea:process-manage-customer-relationship.yaml` | Step 1: move into per-entity subtree; rename to canonical `dea:process-*` form (CR-BP-04). |
| `entities/v1-alpha/dea_group-customer-lifecycle-management.yaml` | `entities/v1-alpha/dea:group-customer-lifecycle-management/dea:group-customer-lifecycle-management.yaml` | Step 1: move into per-entity subtree. |
| `docs/research/l1-register.yaml` | `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml` | Step 2: research about L1 lands under L1 entity. |
| `docs/research/l1-candidate-universe.yaml` | `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-candidate-universe.yaml` | Step 2. |
| `docs/research/L1-REGISTER-v0.1.md` | `entities/v1-alpha/dea:group-customer-lifecycle-management/research/L1-REGISTER-v0.1.md` | Step 2. |
| (n/a; new) | `entities/v1-alpha/dea:group-customer-lifecycle-management/research/README.md` | Step 2: provenance. |
| (n/a; new) | `entities/v1-alpha/dea:process-manage-customer-relationship/research/README.md` | Step 2: provenance + governing CRs. |
| (n/a; new) | `CATALOG.yaml` | Machine-generated by the regenerator. |
| (n/a; new) | `TEMPLATE_VERSION` | Matches template at authoring time. |
| (n/a; new) | `scripts/regenerate_catalog.py` | CST-013. |
| (n/a; new) | `scripts/check_catalog_index.py` | CST-014. |
| (n/a; new) | `catalog-index-schema/catalog-index-schema.json` | Schema consumed by the regenerator and gate. |
| (n/a; modified) | `metamodel-pointer.yaml` | Additive top-level metadata block. |
| (n/a; modified) | `scripts/check_ecf_conformance.py` | Skip state-directory files. |
| (n/a; modified) | `.github/workflows/ci.yml` | Regenerator + gate + conformance steps; state-directory filter. |
