# CR-BP-134: Realizes Exemplar Retarget (Cross-Catalog Id Currency)

**Status**: Accepted
**Layer**: Process Catalog (Cross-catalog semantics)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-29
**Depends on**: CR-BP-mv1 (id system migration), CR-BP-126 (IDM-001 pattern correction)

> **Scope.** Single-record retarget of the one live `realizes` cross-catalog relationship. The exemplar's `target_id` predates both catalogs' identity migrations (`dea:entity-capability:manage-customer-relationship` — a pre-mv1 BC form, not the capabilities catalog's post-mv1 `capabilities:capability-<slug>-<hash>` form). This CR aligns the target to the canonical id, making the assertion resolvable by the capabilities catalog's BC-57 mining pass. Zero content or semantic changes beyond the target id and its prose echo.

---

## 1. The retarget

| Field | Before | After |
|---|---|---|
| `target_id` | `dea:entity-capability:manage-customer-relationship` | `capabilities:capability-customer-management-f3n8wb` |
| `rationale` prose echo | `` `Manage Customer Relationship` `` | `` `Customer Management` `` (the canonical name) |
| `identity_scope` | `dea-catalog-business-capabilities` | unchanged (the scope id is the repo name, not an entity id; correct as-is) |

## 2. Authority

The mapping `manage-customer-relationship → capabilities:capability-customer-management-f3n8wb` is a **name-to-id resolution**, not a semantic inference: the process record `processes:process-pr-operate-bbe384` is named "Manage Customer Relationship", and the capabilities catalog contains exactly one capability whose aliases include "Manage Customer Relationship" (`Customer Management`, admitted as the 8th first-order capability, with alias `Manage Customer Relationship` in its `aliases` list). The mapping is unique — no other capability matches. The `identity_scope` already names the correct catalog.

## 3. What this does NOT do

- Does not add new realizes assertions (the processes-side coverage gap is a programme, not a fix — recorded as the RES-2 upstream dependency in the capabilities catalog's BC-60 closure).
- Does not change any other record, schema, gate, or CI behavior.
- Does not touch the `composes[]` decomposition blocks (those use `dea:composes` type tokens; separately addressed).

## 4. Verification

The edited record passes `check_id_system.py --strict` (the target id is a valid canonical capabilities id per IDM-001's cross-catalog pattern). The entity-system gate ES-003 remains CONFORMANT (the `realizes` type is in the registry's canonical set; the `target_identity_scopes` constraint already permits `dea-catalog-business-capabilities`). CATALOG.yaml regenerated (one entity last_modified bump).
