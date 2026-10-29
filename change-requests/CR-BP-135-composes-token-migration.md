# CR-BP-135: Composes Relationship-Type Token Migration (dea:composes → composes)

**Status**: Accepted
**Layer**: Process Catalog (Structural data model)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-29
**Depends on**: CR-BP-32 (Activity model; the dea:composes mandate), CR-BP-mv1 (id system migration; the composes type token is the last legacy-prefix artifact in live record content)

> **Scope.** Mechanical token migration across the `composes[]` decomposition blocks in live records (2,900 entries across ~580 files), plus the schema `const`, the activity-model gate's canonical constant, the L4 decomposer generator, and the mece gate's fixture writer. The migration completes the CR-BP-mv1 id-system migration's last live-content artifact: `relationship_type: dea:composes` → `relationship_type: composes`. The target_ids were already migrated to `processes:task-*` (the id part of mv1); only the type-token prefix remained. Zero semantic changes — `composes` and `dea:composes` name the same structural composition relationship (CR-BP-32 §7); the token is a label, not a different relationship. The entity-system registry's canonical_types already lists `composes` (not `dea:composes`); ES-003 does not read `composes[]` blocks (it reads the `relationships` key), so the gate is unaffected either way.

---

## 1. What changes

| Site | Change |
|---|---|
| 580 live records (`composes[].relationship_type`) | `dea:composes` → `composes` (2,900 entries) |
| `schemas/entities/activity.schema.json` | `"const": "dea:composes"` → `"const": "composes"` + description updated |
| `scripts/check_activity_model.py` | `CANONICAL_COMPOSITION_TYPE = "dea:composes"` → `"composes"` |
| `scripts/decompose_l4.py` | generator writes `composes` (was `dea:composes`) |
| `scripts/check_mece.py` | fixture-builder writes `composes` |
| `scripts/check_execution_boundary.py` | already accepts both forms — unchanged (belt + braces during transition; can be tightened later) |
| `scripts/migrate_to_v3_layout.py` | one-shot historical script; token reference updated for consistency (not executed) |
| `tests/test_check_execution_boundary.py` / `tests/test_check_mece.py` | fixture tokens aligned |

## 2. What does NOT change

- No target_id, source_id, definition, boundary, or any other record content.
- No relationship is added, removed, or retyped — the semantic relationship named `composes` is identical to `dea:composes` (same relationship, cleaner label).
- The entity-system registry and ES-003 are unaffected (they govern the `relationships` key, not the `composes` block).
- The `relationships[]` blocks in 141 records (150 `composes` + 150 `serves` + 1 `realizes`) already use the bare token — no change needed there.

## 3. Verification

All entity gates re-verified after migration; CATALOG.yaml regenerated (580 entity last_modified bumps). The check_execution_boundary gate accepts both forms so the transition is safe even if a PR lands mid-migration.
