# CR-BP-03A — Legacy Field Migration

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status:** Proposed (2026-09-03)
**Type:** Migration / Schema Correction / Validator
**Priority:** High
**Repository:** `technehub-labs/dea-catalog-processes`
**Depends On:** CR-BP-03 (this repo; merged PR #15)
**Refines:** CR-BP-03 §6, §7, §11 (legacy fields; canonical
relationships)

---

## 1. Intent

CR-BP-03A resolves three issues with the CR-BP-03 schema that came
to light during implementation:

1. **Shape mismatch**: CR-BP-03's `relationships` was declared as
   a **structured object** with `composes` / `realizes` keys. The
   authoritative OpenDEA metamodel declares `relationships` as a
   **flat array of typed relationship instances** (referencing
   `schemas/relationships/relationship-instance.json` in
   `dea-metamodel`). CR-BP-03A fixes the catalog's `relationships`
   shape to match the metamodel.

2. **`parent_process` / `child_processes` are NOT metamodel
   fields**. On review, these were **catalog inventions from
   CR-BP-01** (the wrong-premise implementation, since reverted).
   The metamodel's `process.json` does not declare them. CR-BP-03A
   marks these fields for **removal** (not migration), with a
   migration validator that surfaces any entries that still
   declare them.

3. **`capabilities_delivered` is a metamodel field** (a simple
   array of strings), but the canonical OpenDEA form for
   capability realization is `relationships[relationship_type=realizes]`.
   CR-BP-03A migrates `capabilities_delivered` to the canonical
   form, with a migration validator that surfaces any entries
   that still use the legacy field.

**No breaking changes to current data**: the catalog's
`entities/v1-alpha/` is empty by design (CR-BP-02 §22). The
migration validator is forward-looking — it acts on future
entries that use the legacy fields.

## 2. Background: what the metamodel actually says

The authoritative schema is
`technehub-labs/dea-metamodel/schemas/entities/process.json`. The
key declarations:

```json
"relationships": {
  "type": "array",
  "items": {
    "$ref": "../relationships/relationship-instance.json"
  }
}
```

Each relationship is an **instance** with full CR-002 provenance,
CR-6 lifecycle, and effective_from/to temporal validity:

```json
{
  "source_id": "dea:bp:manage-customer",
  "target_id": "dea:bp:manage-enterprise-customer",
  "relationship_type": "composes",
  "direction": "source-to-target",
  "status": "active",
  "asserted_by": "<contributor>",
  "rationale": "<why this relationship exists>",
  "provenance": {
    "type": "manual",
    "asserted_by": "<contributor>",
    "asserted_at": "<YYYY-MM-DD>"
  }
}
```

The metamodel's `process.json` does **not** declare
`parent_process` or `child_processes`. It only declares
`capabilities_delivered` (a simple array of strings, as a
backward-compat shim). The canonical form is
`relationships[relationship_type=realizes]`.

## 3. CR-BP-03 corrections (the schema changes)

### 3.1 `relationships` shape

**Before (CR-BP-03)**:
```yaml
relationships:
  composes:
    - dea:bp:other
  realizes:
    - dea:capability:other
```

**After (CR-BP-03A)**:
```yaml
relationships:
  - source_id: dea:bp:manage-customer
    target_id: dea:bp:manage-enterprise-customer
    relationship_type: composes
    status: active
    rationale: L1 Process Group composes L2 Business Process
    provenance:
      type: manual
      asserted_by: <contributor>
      asserted_at: <YYYY-MM-DD>
  - source_id: dea:bp:manage-customer
    target_id: dea:capability:manage-customer
    relationship_type: realizes
    status: active
    rationale: Business Process realizes Business Capability
    provenance:
      type: manual
      asserted_by: <contributor>
      asserted_at: <YYYY-MM-DD>
```

The `relationships` field is an **array of relationship
instances** conforming to
`technehub-labs/dea-metamodel/schemas/relationships/relationship-instance.json`.
The metamodel is authoritative on the field shape; the catalog
profiles the source_id and target_id to the catalog's process id
namespace (`dea:bp:...`).

### 3.2 `parent_process` / `child_processes` — REMOVED (validator-enforced)

**These fields were catalog inventions from CR-BP-01** (the
wrong-premise implementation, since reverted). The metamodel
`process.json` does not declare them. CR-BP-03A removes them
**as authoritative** from the catalog schema (the schema is
permissive at the JSON-Schema level; the migration validator is
the authoritative gate). Any future entry that declares them
will be **rejected** by the migration validator with
BP-MIG-001 / BP-MIG-002, and a migration recommendation will
be emitted.

The rationale for the permissive-schema + strict-validator
pattern: the catalog's `entities/v1-alpha/` is empty by design
(CR-BP-02 §22); the migration validator is forward-looking on
future entries. A future CR (CR-BP-03B or later) may add
`additionalProperties: false` to the schema once the migration
is complete.

### 3.3 `capabilities_delivered` — migrated to `relationships[realizes]`

The metamodel's `process.json` still declares
`capabilities_delivered` as a simple array of strings (a
backward-compat shim). CR-BP-03A keeps this field declared in
the catalog schema (for backward-compat with metamodel entries)
but marks it as **soft-deprecated**: the canonical form is
`relationships[relationship_type=realizes]`.

The migration validator surfaces entries that declare
`capabilities_delivered` (BP-MIG-002) and emits a migration
recommendation showing the equivalent
`relationships[relationship_type=realizes]` form.

## 4. Migration validator (BP-MIG-001..005)

A new validator `scripts/check_legacy_migration.py` enforces
the migration discipline:

| Rule | Description |
|---|---|
| BP-MIG-001 | `parent_process` is not declared (the field has been removed; no entry may declare it). |
| BP-MIG-002 | `child_processes` is not declared (the field has been removed; no entry may declare it). |
| BP-MIG-003 | `capabilities_delivered` is empty (the canonical form is `relationships[relationship_type=realizes]`; this field is soft-deprecated). |
| BP-MIG-004 | `relationships` array entries are well-formed (each entry has `source_id`, `target_id`, `relationship_type`; `source_id` matches the entry's `id`). |
| BP-MIG-005 | Migration report: for any entry that triggers BP-MIG-001..003, emit a structured migration recommendation showing the canonical form. |

The validator is **non-blocking on auto-migration**: it emits a
migration recommendation with a confidence score, but the
catalog does not auto-rewrite. The migration flow is
**contribution-driven** (see `docs/relandscape.md`); the
contributor updates the proposed_entry to use the canonical
form, re-runs CI, and the reviewer approves.

## 5. Migration recommendation format

A migration recommendation is a structured object:

```yaml
target: dea:bp:manage-customer
suggestion_type: migration
current_state:
  parent_process: dea:bp:other
  child_processes:
    - dea:bp:child-1
  capabilities_delivered:
    - dea:capability:manage-customer
suggested_state:
  relationships:
    - source_id: dea:bp:manage-customer
      target_id: dea:bp:other
      relationship_type: composed-by
      ...
    - source_id: dea:bp:manage-customer
      target_id: dea:bp:child-1
      relationship_type: composes
      ...
    - source_id: dea:bp:manage-customer
      target_id: dea:capability:manage-customer
      relationship_type: realizes
      ...
confidence: 0.95
rationale: |
  parent_process and child_processes are catalog inventions from
  CR-BP-01; the canonical OpenDEA form is relationships of type
  composes (parent is a `composed-by` view of a child-process
  composes; the canonical is one direction). capabilities_delivered
  is soft-deprecated; the canonical form is relationships of type
  realizes.
status: pending
```

The contributor addresses the recommendation by updating the
proposed_entry, and the migration validator re-runs on the
updated entry.

## 6. Repository changes

### 6.1 `schemas/entity.schema.json` (updated)

- `relationships` shape corrected: array of relationship
  instances (per metamodel `relationship-instance.json`).
- `parent_process` and `child_processes` removed from the
  schema.
- `capabilities_delivered` retained but documented as
  soft-deprecated; the canonical form is
  `relationships[relationship_type=realizes]`.
- `id` pattern unchanged (allows `dea:bp:...` two-colon ids).

### 6.2 `schemas/contribution.schema.json` (updated)

- The `proposed_entry.relationships` shape corrected to match
  the metamodel relationship-instance shape.

### 6.3 `contributions/processes/PROCESS-CONTRIBUTION-TEMPLATE.yaml` (updated)

- The template's `proposed_entry` updated to use the
  relationship-instance shape.

### 6.4 `scripts/check_legacy_migration.py` (new)

- The migration validator enforcing BP-MIG-001..005.
- Built-in `--self-test` (tmpdir scaffold; broken catalog
  triggers all 5 rules; fixed catalog returns zero errors).

### 6.5 `docs/relandscape.md` (updated)

- Documents the migration validator alongside the contribution
  validator.

### 6.6 `.github/workflows/ci.yml` (updated)

- Adds the Legacy Migration gate step (after the Process
  Identity gate).

## 7. Acceptance criteria

### Schema corrections

- [x] `relationships` is an array of relationship instances
  (per metamodel `relationship-instance.json`).
- [x] `parent_process` is removed from the schema.
- [x] `child_processes` is removed from the schema.
- [x] `capabilities_delivered` is retained but documented as
  soft-deprecated.

### Migration validator

- [x] `scripts/check_legacy_migration.py` enforces
  BP-MIG-001..005.
- [x] Built-in `--self-test` exercises all 5 rules on a
  broken catalog; fixed catalog returns zero errors.
- [x] Validator is wired into CI.

### Migration recommendations

- [x] For each entry that triggers BP-MIG-001..003, a structured
  migration recommendation is emitted with the canonical form
  and a confidence score.
- [x] The migration recommendation is contribution-driven: the
  contributor updates the proposed_entry, re-runs CI, and the
  reviewer approves.

### Documentation

- [x] `docs/relandscape.md` documents the migration
  mechanism.
- [x] `change-requests/README.md` adds the CR-BP-03A row.
- [x] `CHANGELOG.md` adds the CR-BP-03A entry.

## 8. Honest scoping notes

- **No breaking changes to current data**: the catalog's
  `entities/v1-alpha/` is empty (CR-BP-02 §22). The migration
  validator is forward-looking.
- **`parent_process` / `child_processes` are NOT metamodel
  fields**; they were catalog inventions from CR-BP-01. Their
  removal is a correction of an historical error, not a
  deprecation of a metamodel-standard field.
- **`capabilities_delivered` IS a metamodel field** (a
  backward-compat shim); CR-BP-03A keeps it in the schema for
  backward-compat but marks it as soft-deprecated.
- **The relationship-instance shape is more verbose** than the
  structured-object shape (CR-BP-03's original). This is the
  trade-off for metamodel alignment: the metamodel's shape
  carries full provenance, lifecycle, and temporal validity.
- **The migration is contribution-driven**, not in-tree. The
  catalog does not auto-rewrite; the contributor updates the
  proposed_entry.

## 9. Follow-on CRs

- **CR-BP-03B**: Tooling for auto-generating the migration
  recommendation from an existing legacy entry (e.g. a CLI
  that takes a legacy entry file and emits the canonical
  form).
- **CR-BP-04**: Activity Model.
- **CR-BP-05**: Execution Boundary.
