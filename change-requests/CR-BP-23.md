# CR-BP-23: ECF Domain Enum v2.5.0 Migration (Domain 6 Enablement & Operations)

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
**Date**: 2026-09-08
**Depends on**: CR-BP-17 (v2.3.0 migration carrier); CR-BP-18 (v2.4.0 migration carrier); dea-metaframework CR-ECF-008; dea-metamodel CR-MM-ECF-03
**Related**: dea-metaframework ADR-ECF-003; dea-catalog-business-capabilities CR-BC-ECF-03

## 1. What this CR is

This CR is the **v2.5.0 migration carrier** for `technehub-labs/dea-catalog-processes`. ECF Domain 6 is renamed from `OperationsAndEnablement` (v2.4.0) to `EnablementAndOperations` (v2.5.0), driven by the Domain/Stage Orthogonality Stress Test (`dea-metaframework` ADR-ECF-003 §5; CR-ECF-008). The Domain 6 name shared a lexical root with Stage 5 `Operate`, obscuring the orthogonality that the ECF requires between the Domain axis and the Stage axis. The rename swaps the two nouns: `Enablement` now leads (lexically distinct from any Stage name) and `Operations` trails (the sustained day-to-day concern, not the lifecycle Stage).

The change is a **single Domain rename**; the other six Domains and the cardinality of the seven-Domain × seven-Stage matrix are unchanged. No content redistribution is required (CR-ECF-008 §3.5): all content that previously belonged to `Operations & Enablement` remains in `Enablement & Operations`. **All 4 OE Process Groups and 23 OE L2 candidates that landed in PR #57 (CR-BP-21d.1) are now renamed in-place** — their entity ids, group ids, and process-context references are unchanged; only the `domain` field and the coordinate identifier suffix change.

## 2. Mapping

| Old form (v2.4.0) | New form (v2.5.0) |
|---|---|
| `OperationsAndEnablement` (PascalCase canonical domain value) | `EnablementAndOperations` |
| `operations-enablement` (kebab-case in enum) | `enablement-operations` |
| `operationsEnablement` (lowerCamelCase identifier suffix in `ecf:operationsEnablement.<stage>`) | `enablementAndOperations` |
| `Operations & Enablement` (display form) | `Enablement & Operations` |
| `oe` (DOMAIN_NAMES abbreviation key — kept from v2.4.0; stable; not re-keyed) | `oe` |

## 3. Files changed

- **3 schemas**: `schemas/entity.schema.json`, `schemas/contribution.schema.json`, `schemas/entities/process-context.schema.json` (kebab-case domain enum values).
- **3 check scripts**: `scripts/check_ecf_conformance.py` (canonical domain set), `scripts/check_process_context.py` (no domain key change), `scripts/check_register_audit.py` (no key change).
- **4 group entity directories**: `entities/v1-alpha/dea:group-operations-and-enablement-build/`, `entities/v1-alpha/dea:group-operations-and-enablement-improvement/`, `entities/v1-alpha/dea:group-process-and-enablement-design/` — group ids unchanged (no rename of group ids per CR-ECF-008 §18 non-goal: "no content redistribution"); the `domain` field and the `process_context` reference are updated.
- **23 OE L2 entity YAMLs**: in-place update of `domain: EnablementAndOperations` + `ecfConformance.canonicalReferences[].identifier: ecf:enablementAndOperations.<stage>` (was `ecf:operationsEnablement.<stage>`).
- **5 PC records**: `dea:pc-oe-c`, `dea:pc-oe-d`, `dea:pc-oe-b`, `dea:pc-oe-o`, `dea:pc-oe-im` — `domain` field updated; `abbreviation` field unchanged (`oe`).
- **3 research files** under `entities/v1-alpha/dea:group-customer-lifecycle-management/research/`: `l1-register.yaml` (Domain 6 cell key), `l1-candidate-universe.yaml`, `L1-REGISTER-v0.1.md` (narrative).
- **1 contribution template**: `contributions/processes/PROCESS-CONTRIBUTION-TEMPLATE.yaml` (kebab-case enum).
- **15 CR records** touched by the rename (CR-BP-03, CR-BP-11, CR-BP-13, CR-BP-13a, CR-BP-13b, CR-BP-17, CR-BP-18, CR-BP-19, CR-BP-20, CR-BP-21c.1, CR-BP-21d, CR-BP-21d.1, CR-BP-21e, CR-BP-21e.1, CR-BP-21f.1, CR-BP-22) — narrative + references updated.
- **1 new CR record**: this file (CR-BP-23).
- **Reconciliation**: `reconciliation/inventory.yaml` + `reconciliation/baseline/v1.yaml` regenerated (SHA256s changed); `reconciliation/dispositions/register.yaml` updated.

Total: **129 files modified** + 1 new CR + reconciliation regeneration.

## 4. Verification

- `scripts/check_ecf_conformance.py`: **PASS** (161 entries conform to ECF Conformance Gate).
- `scripts/check_process_context.py`: **PASS** (PC-001..PC-008).
- `scripts/check_process_specialization.py`: **PASS** (BP-SPEC-01-001..007).
- `scripts/check_process_group.py`: **PASS** (PG-001..008).
- `scripts/check_register_audit.py`: **PASS** (35 landed / 0 ratified-pending-landing / 14 backlog-deferred).
- `scripts/regenerate_catalog.py --check`: **PASS** (no drift).
- `scripts/detect_drift.py` (cross-repo consumer of dea-metaframework): **PASS** (every kebab-case value in this catalog resolves 1:1 to the canonical PascalCase enum, including via `DOMAIN_ALIASES`).

## 5. What did NOT change

- **Group ids unchanged**: `dea:group-operations-and-enablement-build` and the other 3 OE groups keep their entity ids per CR-ECF-008 §18 non-goal ("no content redistribution"). The "Operations & Enablement" string in the entity id is a stable identifier, not the domain name.
- **Process context ids unchanged**: `dea:pc-oe-*` keeps the `oe` abbreviation (stable; not re-keyed).
- **CR-BP-21d.1 (PR #57) is unchanged in scope**: the 4 OE Process Groups and 23 OE L2 candidates that landed in PR #57 are renamed in-place (domain field only), not re-scoped.
- **Catalog id abbreviation**: `oe` (stable; not re-keyed per CR-ECF-008 §17).
- **No content redistribution** (CR-ECF-008 §3.5).
- **Domain number (6), matrix position, semantic anchor (`Execution`), seven-Domain partition, seven lifecycle Stages, Stage 5 name (`Operate`)**: all unchanged.

## 6. Backward compatibility

`dea-metaframework` v2.5.0 preserves the deprecated identifiers in `tools/ecf_coordinates.py:DOMAIN_ALIASES` for at least 2 release cycles (CR-ECF-008 §17):
- `OperationsAndEnablement`
- `operationsAndEnablement`
- `operations-enablement`
- `Operations & Enablement`
- `operations_and_enablement`

The metamodel's drift detector uses `resolve_domain_alias()` to canonicalize every kebab-case / PascalCase / lowerCamelCase reference before validating against the 49-space. Downstream consumers that have not yet migrated may resolve the alias and use the canonical value.

The catalog's own `scripts/check_ecf_conformance.py` enforces the canonical domain set directly (no alias support); consumers that import this catalog's data should consult the metaframework's alias resolver if they need to support legacy inputs.

## 7. Companion CRs (downstream cascade)

- `dea-metaframework` CR-ECF-008 (PR #30) — merged 2026-09-08
- `dea-metamodel` CR-MM-ECF-03 (PR #167) — depends on this PR landing
- `dea-catalog-business-capabilities` CR-BC-ECF-03 — planned (48 file footprint)
- `dea-catalog-business-objects` CR-BO-02 — planned (4 file footprint)
- `dea-catalog-organizational-units` CR-OU-02 — planned (3 file footprint)

Repos audited as having zero footprint (no migration needed): `dea-catalog-actors`, `dea-catalog-stakeholders`, `dea-catalog-digital-business-service-factory`, `dea-architecture-framework`.