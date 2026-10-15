# Cross-Catalog URI Standard (U-01; CR-BP-126)

> **CR-BP-126 Stage deliverable.** The canonical URI form for cross-catalog references. Companion: the Identity Standard IS-006 (cross-catalog identity_scope), the Relationship Standard RS-004 (cross-catalog reference resolution), the cross-catalog resolution registry at `reconciliation/cross-catalog-resolution.yaml`.

## 1. Purpose

This standard resolves the U-01 open question from the CR-BP-121 Gap Register. When a relationship in catalog A references an entity in catalog B, the reference MUST be in a canonical URI form that:

1. Is human-readable (a developer can paste it into a browser and land on the entity).
2. Is machine-resolvable (a tool can fetch the entity's YAML via the URI).
3. Is scope-bound (the URI carries the `identity_scope` declaration).
4. Is version-stable (the URI does not change when the entity's lifecycle state changes).

## 2. The canonical URI form

```
dea://{scope}/{id}
```

Where:
- `dea://` is the canonical URI scheme (registered per the OpenDEAM URI plan; placeholder for the future IANA registration).
- `{scope}` is the catalog's identity_scope (e.g., `dea-catalog-business-capabilities`).
- `{id}` is the canonical entity id (e.g., `capabilities:capability-workforce-planning-b43rhm`).

Example:
```
dea://dea-catalog-business-capabilities/capabilities:capability-workforce-planning-b43rhm
```

The canonical URI form is the **identifier** of the reference; it is NOT directly resolvable. To resolve the URI, the tool consults the cross-catalog resolution registry at `reconciliation/cross-catalog-resolution.yaml` to get the repository, version, and file path.

## 3. The resolvable form

For tools that need a directly-fetchable URL, the resolvable form is the GitHub URL:

```
https://github.com/technehub-labs/{repo}/blob/{ref}/entities/{path-to-entity-yaml}
```

Where:
- `{repo}` is the catalog's repository (from the cross-catalog resolution registry).
- `{ref}` is the git ref (default: `main`; can be a tag, branch, or SHA).
- `{path-to-entity-yaml}` is the file path within the catalog.

Example (the workforce-planning capability):
```
https://github.com/technehub-labs/dea-catalog-business-capabilities/blob/main/entities/v1-alpha/workforce-planning-b43rhm/capabilities-capability-workforce-planning-b43rhm.yaml
```

The resolvable form is **derived** from the canonical URI form via the cross-catalog resolution registry. The derivation is deterministic and reproducible.

## 4. The relationship entry

In a relationship entry (per RS-001..RS-005), a cross-catalog reference carries:

```yaml
relationships:
  - relationship_type: realizes
    target: capabilities:capability-workforce-planning-b43rhm
    identity_scope: dea-catalog-business-capabilities
    # The canonical URI form is derived: dea://{identity_scope}/{target}
    # The resolvable form is derived from the cross-catalog resolution registry.
```

The `target` is the canonical id; the `identity_scope` is the catalog scope; the canonical URI form is `dea://{identity_scope}/{target}`; the resolvable form is derived from the registry.

## 5. The cross-catalog resolution registry

The registry at `reconciliation/cross-catalog-resolution.yaml` maps each scope to its repository, id format, and inverse relationship types. The registry is the single source of truth for cross-catalog resolution.

For each catalog:

```yaml
- scope: dea-catalog-business-capabilities
  repository: technehub-labs/dea-catalog-business-capabilities
  id_format: "capabilities:capability-<token>-<base32hash>"
  legacy_id_format: "dea:capability-*"
  # The path template for the resolvable form
  path_template: "entities/v1-alpha/{slug}/{filename}.yaml"
  default_ref: main
```

The path template is the rule for deriving the file path from the entity's id. For BC, the path template is:

```
entities/v1-alpha/{slug}/capabilities-capability-{descriptor}-{hash}.yaml
```

Where `{slug}` is a kebab-case version of the descriptor (e.g., `workforce-planning-b43rhm` → `workforce-planning-b43rhm`); `{filename}` is `capabilities-capability-{descriptor}-{hash}`.

## 6. Resolution algorithm

Given a canonical URI `dea://{scope}/{id}`:

1. Look up `{scope}` in the cross-catalog resolution registry.
2. If the scope is not found, the reference is NON-CONFORMANT (RS-004 / ES-003 finding).
3. Extract the repository, id_format, legacy_id_format, path_template, and default_ref from the registry entry.
4. Look up the entity's file path using the path_template + the entity's id.
5. Fetch the file from the repository at the default_ref (or the specified ref).
6. Verify the entity's id matches the URI's id.
7. If the entity is not found, the reference is NON-CONFORMANT.

The algorithm is deterministic and reproducible. The entity-system gate (ES-003) implements a simplified version that verifies the scope + id form, not the full path resolution (the full resolution is a tool-side operation).

## 7. The legacy id form

Legacy `dea:` ids (the 35 records in `entities/v1-alpha/` grandfathered per EGV-012) carry the legacy id form:

```
dea://{scope}/dea:{legacy-id}
```

Example:
```
dea://dea-catalog-business-processes/dea:process-manage-customer-relationship
```

The legacy URI form is resolvable via the migration id map at `reconciliation/migration-id-map.yaml` (CR-BP-mv1; 3640 lines). The migration id map maps the legacy id to the canonical `processes:` id; the canonical URI form is the resolvable form.

## 8. Version-stable references

The canonical URI form is version-stable: the URI does not change when the entity's lifecycle state changes (admitted / deprecated / retired / superseded). The reference is to the IDENTITY, not the state. The lifecycle state is a property of the record, not a property of the URI.

This is critical for cross-catalog references: a BP record in this catalog can reference a BC record in `dea-catalog-business-capabilities` even after the BC record is deprecated or retired. The reference remains valid; the lifecycle state is metadata.

## 9. The future: dea:// URI scheme registration

The `dea://` scheme is currently a placeholder. The future work (T8 follow-on or T9) is to register the scheme with IANA (per RFC 7595) and publish the registry. For now, the canonical URI form is used internally; the resolvable form is the GitHub URL.

## 10. Examples

| Reference | Canonical URI | Resolvable URL |
|---|---|---|
| BP record realizes BC record | `dea://dea-catalog-business-capabilities/capabilities:capability-workforce-planning-b43rhm` | `https://github.com/technehub-labs/dea-catalog-business-capabilities/blob/main/entities/v1-alpha/workforce-planning-b43rhm/capabilities-capability-workforce-planning-b43rhm.yaml` |
| Legacy `dea:` id | `dea://dea-catalog-business-processes/dea:process-manage-customer-relationship` | (via migration id map to `processes:process-manage-customer-relationship-f3n8wb`) |
| Cross-catalog Activity | `dea://dea-catalog-business-capabilities/capabilities:capability-financial-stewardship-c7xtfk` | `https://github.com/technehub-labs/dea-catalog-business-capabilities/blob/main/entities/v1-alpha/financial-stewardship-c7xtfk/capabilities-capability-financial-stewardship-c7xtfk.yaml` |

## 11. Cross-references

- **Identity Standard IS-006**: cross-catalog identity_scope declaration.
- **Relationship Standard RS-004**: cross-catalog reference resolution.
- **EGV-006** in CR-012: relationship and reference integrity.
- **EGV-012** in CR-012: legacy reconciliation (no bulk renames).
- **`reconciliation/cross-catalog-resolution.yaml`**: the resolution registry.
- **`reconciliation/migration-id-map.yaml`**: the 3640-line legacy id migration registry.
- **CR-BP-121** Gap Register §5.2 U-01: the open question that this standard resolves.
- **CR-BP-122** Identity Standard IS-001..IS-006: the parent standard.
