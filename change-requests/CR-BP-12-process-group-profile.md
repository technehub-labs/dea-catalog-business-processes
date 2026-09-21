# CR-BP-12: L1 Process Group Profile, Schema, and Validator

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Accepted
**Layer**: L1
**Owner**: TechNeHub Labs
**Program**: Business Process Catalog
**Parent**: CR-BP-11-l1-process-group-discovery
**Related**: CR-BP-03-business-process-architecture, CR-BP-03A-legacy-migration,
         CR-BP-03C-sample-process-contribution, CR-BP-02, CR-BP-04,
         CR-BP-SPEC-BP-01
**Date**: 2026-09-04
**Author**: Coder

## 1. Summary

Lands the first-class Process Group record type for the Business Process catalog. Adds a Process Group schema, a controlled-vocabulary classification for Process Group kinds, a JSON Schema validator, a CI gate, and the first canonical Process Group entry. The Process Group remains a **catalog-owned** record; it is not promoted to the OpenDEA Core metamodel. The canonical containment direction `L1 group --composes--> L2 process` is now a typed relationship on the Process Group record itself.

## 2. Why this exists

CR-BP-11 established the 49-coordinate discovery register and reserved the `dea:group-*` ID family. CR-BP-03C landed the first canonical L2 entry, with a `metadata.group` label that pointed to `dea:group-customer-lifecycle-management` (a label only; no first-class record). Before any further L2 admission can land, three things must be true:

1. Process Groups must be governed records, not loose labels.
2. The `L1 --composes--> L2` containment direction must be a typed relationship on the Process Group record.
3. A validator must enforce the Process Group invariants (PG-001..PG-008) on every PR.

CR-BP-12 delivers all three.

## 3. Scope

### 3.1 In scope

- New schema: `schemas/entities/process-group.schema.json`.
- New controlled vocabulary: `classifications/process-group-kinds.yaml` (six values).
- New validator: `scripts/check_process_group.py` (PG-001..PG-008).
- New CI step in `.github/workflows/ci.yml`.
- New first-class Process Group record at `entities/v1-alpha/dea_group-customer-lifecycle-management.yaml`.
- Update to `entities/v1-alpha/dea_bp_manage-customer-relationship.yaml`:
  - The Process Group is no longer a `metadata.group` label; it is now an external first-class record referenced via a typed relationship.
  - The L2 entity's membership in the Process Group is NOT recorded as a stored relationship on the L2 side; the canonical direction is L1 --composes--> L2 (PG-004 / PG-005). The inverse `part-of` view is generated at query time per CR-002 §8 (Inverse views are generated, never stored).
- Update to `change-requests/README.md` and `CHANGELOG.md`.
- Update to `docs/identity.md` (no new section; one clarifying paragraph).

### 3.2 Out of scope

- Process Group promotion to the OpenDEA Core metamodel (CR-BP-14, future, conditional).
- Mass admission of canonical Process Group records across all 49 coordinates (CR-BP-13..BP-19).
- L1 Process Group contribution template (CR-BP-12 lands the schema and the record; the contribution template lands in CR-BP-13 alongside the first admission tranche).
- Process Scope (L0) first-class records (CR-BP-20, future).
- Any new ID-family prefix (CR-BP-04 locks the four canonical families; CR-BP-12 only uses the existing `dea:group-*` family).
- Cell Charter or Process Context schema changes (CR-BP-02 stands).

## 4. Design decision (locked)

- **Process Group is a catalog-owned record.** It is **not** an OpenDEA Core entity. The OpenDEAM root model (`dea-architecture-framework`) carries the `dea:entity-process` kernel and the `dea:entity-business-process` specialization; the Process Group does not appear there. The Process Group is a catalog-level grouping construct that exists to organize Business Process specializations within a Process Context.
- **ID family: `dea:group-*`.** No new family is introduced. The colon-vs-dash and the dash-vs-dash distinctions are governed by CR-BP-04 §4.
- **Canonical containment direction: `L1 group --composes--> L2 process`.** The `composes` relationship is recorded on the Process Group record (PG-004..PG-006 enforce). The inverse `part_of` view is exposed on the L2 process entity for navigation; it is a derived query view, not a second source of truth.
- **MECE within a Process Context.** Each L2 process belongs to exactly one Process Group within its Process Context (PG-006 enforces). Cross-context `composes` is permitted (a Process Group may include processes from adjacent contexts only when the cross-context pattern is intentional and documented).
- **Process Group kinds are six.** `end-to-end`, `functional`, `support`, `cross-cutting`, `governance`, `innovation`. The vocabulary is a controlled list (PG-007 enforces).
- **Process Group lifecycle is independent of Business Process lifecycle.** A Process Group may be `active` while one of its composed processes is `deprecated`; the deprecation is recorded on the L2 side and the relationship's `status` field.

## 5. Process Group schema (PG-001..PG-008)

The schema is at `schemas/entities/process-group.schema.json`. Required fields: `id`, `name`, `definition`, `process_context`, `scope`, `outcomes`, `composes`, `process_group_kind`, `status`, `lifecycle_status`, `version`. The `composes` array holds relationship instances conforming to `dea-metamodel/schemas/relationships/relationship-instance.json`. The `process_context` is a `dea:pc-*` reference. The `target_id` of every `composes` entry must match `^dea:process-[a-z0-9-]+$` and must resolve to a canonical L2 entity in `entities/v1-alpha/`.

### 5.1 Rule catalogue

| Rule | Description |
|---|---|
| PG-001 | ID matches `^dea:group-[a-z0-9-]+$`. |
| PG-002 | Required fields present (`id`, `name`, `definition`, `process_context`, `scope`, `outcomes`, `composes`, `process_group_kind`, `status`, `lifecycle_status`, `version`). |
| PG-003 | `process_context` resolves to a known `dea:pc-*` Process Context entity in `contexts/v1-alpha/`. |
| PG-004 | Every `composes[].target_id` matches `^dea:process-[a-z0-9-]+$`. |
| PG-005 | Every `composes[].target_id` resolves to a canonical L2 Business Process entity in `entities/v1-alpha/`. |
| PG-006 | MECE within a Process Context: no two Process Groups in the same Process Context share an L2 process in their `composes` list. Cross-context overlap is permitted only when the overlap is intentional and recorded in the `cross_context_overlap` metadata field. |
| PG-007 | `process_group_kind` is one of: `end-to-end`, `functional`, `support`, `cross-cutting`, `governance`, `innovation`. |
| PG-008 | `lifecycle_status` is one of: `candidate`, `active`, `deprecated`, `retired`. `active` requires at least one `composes` entry with `status: active`. `deprecated` and `retired` must reference at least one terminal-state L2 process in the `rationale` field. |

### 5.2 `part_of` on the L2 entity (deferred; generated view only)

The metamodel relationship-instance.json does not admit a `part-of` relationship_type. Per CR-002 §8 (Inverse views are generated, never stored), the inverse relationship is generated at query time, not stored. The L2 entity therefore carries no `part_of` relationship; instead, a contributor or downstream consumer queries the Process Group's `composes` array in reverse to derive the inverse. A future metamodel CR could admit `part-of` to the enum; until then, the L2 side records membership as a comment-only reference (see `entities/v1-alpha/dea_bp_manage-customer-relationship.yaml`).

## 6. Process Group kinds (controlled vocabulary)

| Kind | Definition | Example |
|---|---|---|
| `end-to-end` | A Process Group that captures a value-stream-spanning flow across multiple lifecycle stages. | Customer Lifecycle Management |
| `functional` | A Process Group that captures processes supporting a single organizational function. | Account Management |
| `support` | A Process Group that captures processes supporting the core without direct value-stream participation. | Customer Data Quality |
| `cross-cutting` | A Process Group that captures processes participating in multiple value streams. | Change Management |
| `governance` | A Process Group that captures processes enforcing governance obligations. | Risk and Compliance |
| `innovation` | A Process Group that captures processes generating new value-stream candidates. | Product Innovation |

The vocabulary lives at `classifications/process-group-kinds.yaml`. Additions go through CR-BP-12 minor revisions.

## 7. First canonical Process Group entry

`entities/v1-alpha/dea_group-customer-lifecycle-management.yaml` is the first Process Group record. It promotes the `metadata.group` label that lived on `dea:process-manage-customer-relationship` (CR-BP-03C) into a governed record. The Process Group:

- Has `id: dea:group-customer-lifecycle-management`.
- Has `process_context: dea:pc-pr-op` (the live Process Context).
- Has `process_group_kind: end-to-end`.
- Has a single `composes` relationship pointing at `dea:process-manage-customer-relationship`.
- Has `lifecycle_status: candidate` (the group is governed by CR-BP-12 but not yet validated end-to-end; promotion to `active` is gated on the CR-BP-13 admission tranche).

The L2 entity at `dea:process-manage-customer-relationship`:

- Loses the `metadata.group` block.
- Gains a `part_of` relationship pointing at `dea:group-customer-lifecycle-management`.

## 8. Validator contract

`scripts/check_process_group.py` enforces PG-001..PG-008 against every YAML/JSON file in `entities/v1-alpha/` whose `type: ProcessGroup`. The validator is non-blocking on auto-classification and emits re-landscape suggestions with confidence scores (mirroring `check_process_identity.py` BP-ARC-ID-*).

### 8.1 Built-in self-test

The validator carries a `--self-test` mode that exercises PG-001..PG-008 on a deliberately broken catalog, then on a fixed catalog, and verifies expected exit codes (mirroring the existing `check_process_identity.py` pattern).

### 8.2 CI integration

`.github/workflows/ci.yml` gains a new step that runs `python scripts/check_process_group.py` after the existing validator steps. Failure exits non-zero and fails the PR.

## 9. Relationship to other CRs

- **CR-BP-11** produced the 49-coordinate discovery register; CR-BP-12 turns one coordinate's accepted group into a first-class record.
- **CR-BP-03** defined the L0/L1/L2 conceptual hierarchy; CR-BP-12 promotes L1 from a metadata label to a first-class record.
- **CR-BP-03A** established the relationship-instance shape; CR-BP-12 reuses that shape verbatim.
- **CR-BP-03C** landed the first L2 entry with a `metadata.group` label; CR-BP-12 removes the label and replaces it with a typed `part_of` reference.
- **CR-BP-04** locked the ID-family contract; CR-BP-12 uses the existing `dea:group-*` family and does not introduce a new prefix.
- **CR-BP-SPEC-BP-01** established the kernel + specialization discipline; CR-BP-12 does not alter the kernel.
- **CR-BP-13..BP-19** (future) will admit the remaining 37 Process Group records across the seven ECF domains.

## 10. Acceptance criteria

- New schema: `schemas/entities/process-group.schema.json` is present and validates a representative Process Group record.
- New vocabulary: `classifications/process-group-kinds.yaml` is present and the validator enforces PG-007.
- New validator: `scripts/check_process_group.py` is present and runs cleanly against the first canonical Process Group record.
- New CI step: `.github/workflows/ci.yml` invokes the new validator.
- First canonical entry: `entities/v1-alpha/dea_group-customer-lifecycle-management.yaml` is present and validates against the new schema.
- L2 cleanup: `entities/v1-alpha/dea_bp_manage-customer-relationship.yaml` no longer carries the `metadata.group` block; the Process Group is now an external first-class record referenced via the Process Group's `composes` array.
- All five existing validators continue to PASS.
- ECF drift detector reports zero new hard failures.

## 11. Risk and rollback

### 11.1 Risk

The L2 cleanup (removing `metadata.group`) is a structural change to the live canonical L2 entry. The risk is that downstream consumers that read `metadata.group` would break. No consumer in this repo reads `metadata.group`. Consumers in `dea-architecture-framework` or `dea-catalog-business-capabilities` (if any) are out of scope for the surgical changes rule. CR-BP-12 announces the change in `CHANGELOG.md` and `change-requests/README.md` so downstream consumers have a heads-up.

### 11.2 Rollback

CR-BP-12 lands four artifacts and one cleanup edit. On rollback:

- The Process Group schema, vocabulary, and validator can stay without breaking anything (the L2 entry would revert to its prior shape).
- The first canonical Process Group entry can stay or be deleted; both are safe.
- The L2 cleanup reverts by re-adding the `metadata.group` block and removing the `part_of` field.

Rollback is a single `git revert <merge-commit>` per artifact group. The cleanup edit is the only piece that touches live catalog content; the other artifacts are additive.

## 12. Open questions

1. Should `part_of` be admitted to the metamodel relationship-type enum so that the L2 side can carry an explicit `part_of` reference for navigation, or should the inverse remain generated-only per CR-002 §8? (Drafted: generated only. The metamodel enum does not currently admit `part-of`; a future metamodel CR (CR-MM-PROC-02 candidate) could add it.)
2. Should the validator also enforce that `composes[].status` matches the L2 process's `lifecycle_status` (active -> active, deprecated -> deprecated)? (Recommendation: no. The Process Group's `lifecycle_status` is independent of any single L2 process's status. Track in CR-BP-15.)
3. Should the validator enforce that a Process Group's `process_context` matches the L2 process's `process_context`? (Recommendation: yes, with a documented exception for cross-context overlap. PG-006 covers the rule. Exception path lives in the `cross_context_overlap` metadata field.)

## 13. Sources

- `technehub-labs/dea-catalog-processes/change-requests/CR-BP-11-l1-process-group-discovery.md`
- `technehub-labs/dea-catalog-processes/change-requests/CR-BP-03-business-process-architecture.md`
- `technehub-labs/dea-catalog-processes/change-requests/CR-BP-03A-legacy-migration.md`
- `technehub-labs/dea-catalog-processes/change-requests/CR-BP-03C-sample-process-contribution.md`
- `technehub-labs/dea-catalog-processes/change-requests/CR-BP-04-id-family-reconciliation.md`
- `technehub-labs/dea-catalog-processes/entities/v1-alpha/dea_bp_manage-customer-relationship.yaml`
- `technehub-labs/dea-catalog-processes/contexts/v1-alpha/dea-pc-pr-op.yaml`
- `technehub-labs/dea-catalog-processes/schemas/entity.schema.json`
- `technehub-labs/dea-catalog-processes/schemas/entities/process-context.schema.json`
- `technehub-labs/dea-catalog-processes/schemas/identity.schema.json`
- `technehub-labs/dea-catalog-processes/scripts/check_process_identity.py`
- `technehub-labs/dea-metamodel/schemas/relationships/relationship-instance.json`
- `technehub-labs/dea-metaframework/specification/ecf-coordinates.md`
- `technehub-labs/dea-catalog-business-capabilities/docs/research/ecf-overlay-v0.2.yaml`