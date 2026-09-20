# CR-BP-18: ECF Domain Enum v2.4.0 Migration (Agency & Organization)

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Accepted
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-07
**Depends on**: CR-BP-17 (v2.3.0 migration carrier); dea-metaframework CR-ECF-007; dea-metamodel CR-MM-ECF-02
**Related**: dea-metaframework ADR-ECF-002; dea-catalog-business-capabilities CR-CATALOG-STRUCT-09

## 1. What this CR is

This CR is the **v2.4.0 migration carrier** for `technehub-labs/dea-catalog-processes`. ECF Domain 3 is renamed from `PeopleAndOrganization` (v2.3.0) to `AgencyAndOrganization` (v2.4.0), driven by the Substrate Independence Stress Test (`dea-metaframework` ADR-ECF-002 §5; CR-ECF-007). The domain must remain semantically valid whether the enterprise's internal agents are biological (humans), artificial (AI systems, autonomous software agents), or hybrid.

The change is a **single Domain rename**; the other six Domains and the cardinality of the seven-Domain × seven-Stage matrix are unchanged. No content redistribution is required (CR-ECF-007 §6.3): all content that previously belonged to `People & Organization` remains in `Agency & Organization`.

## 2. Mapping

| Old form (v2.3.0) | New form (v2.4.0) |
|---|---|
| `PeopleAndOrganization` (PascalCase) | `AgencyAndOrganization` |
| `people-organization` (kebab-case) | `agency-organization` |
| `peopleOrganization` (lowerCamelCase) | `agencyOrganization` |
| `po` (DOMAIN_NAMES abbreviation key) | `ag` |

## 3. Files changed

- **3 schemas**: `schemas/entity.schema.json`, `schemas/contribution.schema.json`, `schemas/entities/process-context.schema.json` (kebab-case domain enum values).
- **3 check scripts**: `scripts/check_ecf_conformance.py` (canonical domain set), `scripts/check_process_context.py`, `tools/build_bp13a_tranche.py` (DOMAIN_NAMES key `po` -> `ag`).
- **1 contribution template**: `contributions/processes/PROCESS-CONTRIBUTION-TEMPLATE.yaml`.
- **3 research files** under `entities/v1-alpha/dea:group-customer-lifecycle-management/research/` (L1 register, L1 candidate universe, register notes).
- **1 docs file**: `docs/classification.md`.
- **5 CR records** touched by the rename (CR-BP-03, CR-BP-11, CR-BP-13a, CR-BP-13b, CR-BP-17).
- **1 new CR record**: this file (CR-BP-18).
- **Reconciliation**: `reconciliation/inventory.yaml` + `reconciliation/baseline/v1.yaml` regenerated (SHA256s changed).

Total: **16 files modified** + 1 new CR + reconciliation regeneration.

## 4. Verification

- `scripts/check_ecf_conformance.py`: **PASS** (28 entries conform to ECF Conformance Gate).
- `scripts/check_process_context.py`: **PASS** (PC-001..PC-008).
- `scripts/check_process_semantics.py`: **CONFORMANT** (CR-BP-14 S21).
- Full test suite: **144 pass, 5 fail — all 5 failures pre-existing** (verified via `git stash` against unmodified main: identical failure set).
  - Pre-existing failures: `test_conformance_result_runs_on_live`, `test_conformance_result_json_shape`, `test_cr_meta_strict_passes_when_no_new_failures`, `test_check_struct_clean_repo_passes`, `test_regenerate_catalog_check_passes_on_committed_tree`.

## 5. What did NOT change

- The cardinality of the seven Domains (7), the matrix M = D × S (49 coordinates), and the no-cell-filling rule are unchanged.
- The v2.3.0 renames (CR-BP-17) are unchanged.
- No process-context YAML files are renamed (none used the `po` mid-segment in `dea-pc-*` IDs).
- No content redistribution is required (CR-ECF-007 §6.3).

## 6. Backward compatibility

`dea-metaframework` v2.4.0 preserves the deprecated identifiers in `tools/ecf_coordinates.py:DOMAIN_ALIASES` for at least 2 release cycles.
