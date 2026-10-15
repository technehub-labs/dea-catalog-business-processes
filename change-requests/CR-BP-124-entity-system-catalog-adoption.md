# CR-BP-124: Entity System Stage 5 (Catalog Adoption + Disposition Register)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance) - pinned rule
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-13
**Depends on**: CR-BP-121 (Stage 1); CR-BP-122 (Stage 2 Specifications); CR-BP-123 (Stage 3-4 Umbrella Gate)
**Companion**: CR-BP-125 (Stage 6 Institutionalisation)

## 1. Purpose

This is the Stage 5 slice of the General Entity System institutionalisation in `dea-catalog-business-processes`. Stages 1-4 (CR-BP-121, -122, -123) produced the 4 doc outputs + 5 normative spec docs + the 5-rule umbrella gate. This slice files the per-record disposition for the ~8700 advisory findings, the cross-catalog resolution registry, and the migration id map (already in place from CR-BP-mv1).

After this slice: the entity-system gate can be promoted to blocking in Stage 6 (CR-BP-125) without false-positive churn. The disposition register documents the per-finding disposition so the gate's promotion is a one-line change in `scripts/conformance_result.py` (from `blocking: False` to `blocking: True` for the entity-system gate at [33]).

## 2. The 3 deliverables

### 2.1 The disposition register

`reconciliation/entity-system-disposition-register.yaml` - the per-rule, per-pattern disposition for the gate's advisory findings. Two layers:

- **Class-level dispositions** (the bulk): for each (rule, pattern, field) tuple, a disposition: `grandfathered` / `admit-with-override` / `require-migration` / `retire` / `accept-residual`. The class-level dispositions cover the ~8700 advisory findings.
- **Per-record dispositions** (the specific cases): for any record that needs individual treatment. The register is currently empty; the class-level dispositions cover all current findings.

The 4 class-level dispositions:

| Rule | Pattern | Field | Disposition | Rationale |
|---|---|---|---|---|
| ES-002 | `processes:process-**` | `*` | `accept-residual` | Admitted BP / PG / Activity / Task records that predate the entity-system standard; missing envelope fields are documented backward-incompatibilities. Future records MUST conform (the gate is promoted to blocking in Stage 6). |
| ES-002 | `processes:pc-**` | `*` | `grandfathered` | ProcessContext records use the slim profile (id + name); pre-admission PC records may not have both yet. |
| ES-003 | `**` | `*` | `accept-residual` | Records with non-canonical relationship types (e.g. `serves`, `governs`) are valid per the existing BP-SEM-001..014 and related pre-entity-system rules. The vocabulary migration is a T8 follow-on. |
| ES-004 | `processes:pc-**` | `*` | `grandfathered` | ProcessContext records don't have a lifecycle state machine; the slim profile exempts them from ES-004. |

### 2.2 The migration id map

`reconciliation/migration-id-map.yaml` - the per-record migration registry (already in place from CR-BP-mv1, 3640 lines as of 2026-10-13). Every legacy `dea:` id in `entities/v1-alpha/` (35 records) is documented with a `processes:` id and a disposition. No bulk renames (per EGV-012).

### 2.3 The cross-catalog resolution registry

`reconciliation/cross-catalog-resolution.yaml` - the per-catalog identity-scope declaration. 7 catalogs declared: dea-catalog-business-capabilities, dea-catalog-business-objects, dea-catalog-organizational-units, dea-catalog-actors, dea-catalog-stakeholders, dea-metamodel, dea-architecture-framework. The `realizes` relationship from BP records in this catalog to BC records in `dea-catalog-business-capabilities` is the primary cross-catalog relationship in the live tree.

## 3. The exception mechanism (the EGV-011 escape hatch)

The disposition register is the per-record class-level exception registry. The gate's exception mechanism (CS-008/CS-009) consults the disposition register via the `reconciliation/normalization.yaml` review-retained verdicts. The class-level dispositions are NOT loaded into the exception registry (the exception registry is per-record; the disposition register is per-class). A specific record can be added to the exception registry with a review-retained verdict if the class-level disposition is not appropriate.

For Stage 5 (this PR), the gate's exception mechanism continues to consult `reconciliation/normalization.yaml`. The disposition register is a separate registry that documents the class-level dispositions.

## 4. Per-Stage-5 acceptance criteria

- AC-01 The disposition register is filed under `reconciliation/entity-system-disposition-register.yaml`.
- AC-02 The disposition register documents the per-rule, per-pattern disposition for the gate's advisory findings.
- AC-03 The migration id map is in place (per CR-BP-mv1; 3640 lines; 35 legacy `dea:` ids).
- AC-04 The cross-catalog resolution registry is filed under `reconciliation/cross-catalog-resolution.yaml`.
- AC-05 The 4 class-level dispositions cover the 4 rule-pattern classes (ES-002 BP, ES-002 PC, ES-003, ES-004 PC).
- AC-06 No bulk renames (per EGV-012); every legacy id is grandfathered.
- AC-07 The gate's advisory findings are documented; per-record dispositions are added as specific records are migrated.
- AC-08 D-004 (no en/em-dash, no U+2E3B) is clean across all new/modified files.
- AC-09 118a/118b/118c/123 authorship + entity-system gates remain CONFORMANT or advisory.
- AC-10 Stage 6 (CR-BP-125) can promote the entity-system gate to blocking without churn (the disposition register documents the per-finding resolution).

## 5. Repository changes

| Path | Status | Notes |
|---|---|---|
| `reconciliation/entity-system-disposition-register.yaml` | NEW | The per-rule, per-pattern disposition; 4 class-level dispositions covering the ~8700 advisory findings |
| `reconciliation/migration-id-map.yaml` | (existing) | 3640 lines from CR-BP-mv1; no changes |
| `reconciliation/cross-catalog-resolution.yaml` | NEW | 7 catalogs with identity-scope declarations; rules section |
| `change-requests/CR-BP-124-entity-system-catalog-adoption.md` | NEW | This file (the carrier CR) |
| `change-requests/README.md` | MOD | New row at top of table |
| `CHANGELOG.md` | MOD | [Unreleased] entry |
| `CATALOG.yaml` | MOD | Regenerator bump |

## 6. Test posture (live, 2026-10-13)

```
$ python3 scripts/check_entity_system.py --strict
Entity System Gate (CR-BP-123): NON-CONFORMANT
... (live tree findings; the disposition register documents the resolutions)
```

The gate continues to report the ~8700 advisory findings; the disposition register documents the per-finding resolution. The gate is NOT yet promoted to blocking (that happens in Stage 6, CR-BP-125).

## 7. What this CR is NOT

- **NOT the institutionalisation.** The cardinal-rules update + CONTRIBUTING + envelope template ship as CR-BP-125 (Stage 6).
- **NOT the gate promotion.** The entity-system gate stays advisory in Stage 5; the promotion to blocking is in Stage 6.
- **NOT a sweep.** No entity, schema, or id changes.
- **NOT a bulk rename.** Per EGV-012, no existing records are renumbered.
- **NOT a metamodel change.** Out of scope (different repo).
- **NOT a cross-catalog URI resolution.** U-01 is deferred to T8.

## 8. Out-of-scope follow-ons

- **CR-BP-125** (Stage 6): the doctrine doc + cardinal-rules update + CONTRIBUTING + envelope template + exception process. Promotes the gate from advisory to blocking.
- **T7 of umbrella programme** (Cross-repo cascade): 11 sibling repos get per-repo entity-system CR docs.
- **T8 of umbrella programme** (Legacy ID reconciliation): per-repo disposition registers + cross-catalog URI form (U-01 resolution) + IDM-001 pattern fix.
- **IDM-001 pattern fix**: the existing `check_id_system.py` has the old (broken) pattern. The fix is a follow-on.

## 9. Cross-references

- **CR-BP-121** (Stage 1): the 4 doc outputs.
- **CR-BP-122** (Stage 2): the 5 normative spec docs.
- **CR-BP-123** (Stage 3-4): the 5-rule umbrella gate.
- **CR-BP-mv1**: the entity storage and id migration; 3640-line migration id map.
- **CR-BP-118a/b/c**: the authorship cardinal rule (cross-references for EGV-008).
- **DEA-ID-000**: `dea-governance/docs/design/entity-system-foundation.md` (the foundation paper).
- **CR-012**: `dea-governance/change-requests/CR-012-org-wide-entity-governance.md` (the org-wide governance CR).
