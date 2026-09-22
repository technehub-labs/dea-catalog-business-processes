# CR-BP-04: Business Process Identity & ID-Family Reconciliation

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

Status: Baseline
Program: Business Process Catalog
Parent: CR-BP-03-business-process-architecture
Related: CR-BP-03A-legacy-migration, CR-BP-03C-sample-process-contribution,
         CR-BP-SPEC-BP-01, CR-BP-02, CR-BP-11-l1-process-group-discovery
Date: 2026-09-04
Author: Coder

## 1. Summary

Establishes the canonical ID-family contract for Business Process catalog identifiers, reconciles the apparent drift between the `dea:bp-*` and `dea:process-*` prefixes, and locks the L0/L1 ID conventions introduced in CR-BP-03C and CR-BP-11. No canonical entity is created or modified by this CR. No schema or validator is added. The CR is documentation-first; it makes the existing implicit rules explicit and forbids three patterns that contributors will otherwise reach for.

## 2. Problem statement

The catalog has been authored incrementally across CR-BP-02, CR-BP-03, CR-BP-03A, CR-BP-03C, and CR-BP-11. The following prefix families appear in different parts of the catalog without a single document that explains which prefix means what:

- `dea:bp-*`: appears in legacy-migration fields and in validator self-test fixtures.
- `dea:process-*`: appears in the live canonical entity and in the Process Context schema's `processes` array.
- `dea:pc-*`: appears in Process Context entity IDs.
- `dea:scope-*`: appears as a label on the live L2 entity's metadata.
- `dea:group-*`: appears as a label on the live L2 entity's metadata and is the documented L1 family in CR-BP-11.

A new contributor reading `schemas/contribution.schema.json` can plausibly conclude that `dea:bp:manage-customer-relationship` is a valid canonical ID; it is not. This CR removes that ambiguity.

## 3. Scope

### 3.1 In scope

- The four canonical ID families used by the catalog: `dea:process-*`, `dea:pc-*`, `dea:scope-*`, `dea:group-*`.
- The legacy-migration `dea:bp-*` family, retained as a transition aid only.
- The self-test fixture convention inside validator scripts.
- The cross-references that bind these families together (Process Context `processes`, legacy `parent_process`, L0/L1 metadata labels).
- Documentation updates to `docs/identity.md`, `change-requests/README.md`, and `CHANGELOG.md`.

### 3.2 Out of scope

- Any schema change (the existing schemas are already consistent with the rule).
- Any validator change (the existing validators already enforce the rule).
- Any entity rename or migration (no live entity uses the `dea:bp-*` canonical prefix).
- Any L1 Process Group profile (CR-BP-12 will land that; CR-BP-04 only declares the ID family).
- Process Group promotion to OpenDEA Core (CR-BP-14, future, conditional).
- Capability Catalog ID families (separate catalogue, separate CR family).

## 4. Canonical ID-family contract

The catalog uses four canonical families and one legacy-migration family. Each family has a single reserved prefix, a single reserved separator, and an explicit purpose.

| Family | Prefix | Separator | Purpose | Population rule |
|---|---|---|---|---|
| Business Process | `dea:process` | `-` | Canonical L2 Business Process entries (and their specializations) | One entity per specialization; specialization IDs are siblings of the root, not nested |
| Process Context | `dea:pc` | `-` | Canonical Process Context entities (Domain x Lifecycle Stage cells) | 49 maximum (7 domains x 7 lifecycle stages); zero, one, or many per coordinate |
| Process Group | `dea:group` | `-` | Catalog-owned L1 Process Group labels and (later) first-class records | One label per accepted group; governed by CR-BP-11 and the BP-12 schema |
| Process Scope | `dea:scope` | `-` | Catalog-owned L0 scope labels (no first-class entity) | Zero or more per process; recorded in `metadata` only |
| Legacy Business Process | `dea:bp` | `:` (colon) | Legacy-migration reference only; appears in `legacy_ids` arrays and in self-test fixtures | Never as a canonical entity id; legacy_ids must reference a known prior external identifier |

The colon-vs-dash distinction is intentional. `dea:bp:*` is a deliberately alien-looking identifier that signals "this is a foreign legacy reference" to any reader; contributors cannot confuse it with `dea:process-*`.

## 5. Reconciliation findings

The apparent `dea:bp-*` vs `dea:process-*` drift collapses on close reading. The two prefixes occupy three distinct roles:

### 5.1 Role 1: Legacy migration reference (intentional)

`schemas/entity.schema.json` line 35 (`legacy_ids`) and `schemas/contribution.schema.json` line 73 (`legacy_ids`) define a `dea:bp:*` pattern. This is the legacy-migration escape hatch introduced by CR-BP-03A and is preserved verbatim. A `legacy_ids` entry must reference a known prior external identifier (e.g. an APQC process code). It is **not** a canonical catalog identifier.

### 5.2 Role 2: Canonical Business Process (intentional)

The live canonical entity `dea:process-manage-customer-relationship`, the Process Context schema's `processes:` array (`schemas/entities/process-context.schema.json` line 96), and the `check_process_context.py` validator (line 150) all use the `dea:process-*` prefix. This is the canonical form.

### 5.3 Role 3: Validator self-test fixture (intentional)

`scripts/check_legacy_migration.py` (lines 209, 219, 220) and `scripts/check_process_identity.py` (lines 269, 288, 306) declare `dea:bp-bad-1`, `dea:bp-bad-2`, `dea:bp-bad-4`, `dea:bp-bad-mig`, `dea:bp-parent`, and `dea:bp-child-*` as deliberate broken-input examples that exercise the validators' failure paths. These IDs do not represent catalog content; they are synthetic and are not validated by the production catalog's id-pattern check.

### 5.4 No role-4 conflict exists

There is no catalog file that uses `dea:bp-*` as a canonical Business Process id. The "drift" is a documentation gap, not a content drift.

## 6. L0/L1 ID conventions

The L2 entity at `dea:process-manage-customer-relationship` carries two metadata labels:

- `dea:scope-customer-facing-operations`: the L0 scope label.
- `dea:group-customer-lifecycle-management`: the L1 Process Group label.

These are recorded under the entity's `metadata` block and are not first-class entities. CR-BP-11 locks `dea:group-*` as the Process Group ID family. This CR confirms that decision and extends the contract:

- `dea:scope-*` labels live in `metadata` only.
- `dea:group-*` labels live in `metadata` until CR-BP-12 lands the first-class Process Group record; after BP-12 the same label becomes the first-class record id (a 1:1 rename with no migration of any L2 entity).
- `dea:scope-*` and `dea:group-*` are catalog-scoped families; they do not appear in the OpenDEA Core metamodel.

## 7. Rules for new contributors

A new contribution must obey the following rules. The validators already enforce most of them; the rules below are the contributor-readable contract.

1. Use `dea:process-<kebab-name>` for any canonical Business Process id (L2 root or specialization).
2. Use `dea:pc-<domain-abbr>-<stage-abbr>` for any canonical Process Context id (Domain x Lifecycle Stage cell).
3. Use `dea:group-<kebab-name>` for any Process Group label or (later) first-class record id.
4. Use `dea:scope-<kebab-name>` for any Process Scope label (metadata only).
5. Use `dea:bp:<external-system>:<code>` (colon separator) only inside a `legacy_ids` array, and only when referencing a known prior external identifier.
6. Never use `dea:bp-*` (dash separator): it is reserved for validator self-test fixtures and is not a valid production identifier under any schema.
7. Never introduce a new ID-family prefix without an accompanying CR that documents the family, the separator, and the population rule.
8. Never record a `dea:group-*` or `dea:scope-*` label under any field other than `metadata` (BP-12 may add a `relationships` block once the first-class record lands; nothing else).
9. A Process Context's `processes:` array must reference `dea:process-*` ids only.
10. A Process's `legacy_ids` array must use the colon-separated `dea:bp:*` form only.

## 8. Validator contract (informative; existing)

The following validators already enforce the rules above. This CR makes the contract explicit; it does not modify the validators.

| Validator | Rule id(s) | Pattern enforced |
|---|---|---|
| `check_process_identity.py` | BP-ARC-ID-001..005 | Entity `id` matches `^dea:process-[a-z0-9-]+$` (live entry conforms; legacy `dea:bp-bad-*` fixtures deliberately fail) |
| `check_process_context.py` | PC-007, PC-008 | Process Context id matches `^dea:pc-[a-z0-9-]+$`; `processes:` array entries match `^dea:process-[a-z0-9-]+$` |
| `check_legacy_migration.py` | BP-MIG-001..005 | `legacy_ids` entries match `^dea:bp:[a-z0-9-]+$` (colon-separated legacy reference) |
| `check_ecf_conformance.py` | EC-001..EC-005 | ECF coordinate references use the `ecf:<domain>.<stage>` form, not a `dea:*` family |

## 9. Acceptance criteria

- This CR document is indexed in `change-requests/README.md` with status Baseline.
- The CHANGELOG `[Unreleased]` section gains an entry for CR-BP-04.
- `docs/identity.md` gains a new section that restates the four-family contract verbatim.
- The five local validators continue to pass on `main` after merge.
- The ECF drift detector reports zero new hard failures.

## 10. Risk and rollback

### 10.1 Risk

The only risk is that a contributor interprets `dea:bp-bad-*` validator fixtures as a hint that `dea:bp-*` is canonical and proposes a CR to "fix" the schema. This CR mitigates that risk by publishing the four-family contract and the colon-vs-dash distinction.

### 10.2 Rollback

This CR adds documentation only. There is no code path to roll back; the only artifact to revert on rollback is the CHANGELOG entry, the `change-requests/README.md` row, and the new section in `docs/identity.md`. None of these artifacts have downstream consumers; rollback is `git revert <merge-commit>`.

## 11. Related work

- CR-BP-02 establishes the Process Context register (`dea:pc-*` family).
- CR-BP-03 defines the L0/L1/L2 hierarchy and the metadata label fields.
- CR-BP-03A introduces the legacy-migration escape hatch (`dea:bp:*` colon-separated references).
- CR-BP-03C exercises the canonical L2 entry shape with `dea:process-manage-customer-relationship`.
- CR-BP-SPEC-BP-01 defines the specialization contract (`dea:process-*` siblings, no nesting).
- CR-BP-11 reserves the `dea:group-*` family for Process Groups and records 102 L1 candidates.

## 12. Open questions

1. Should the validator self-test fixtures rename their `dea:bp-bad-*` ids to `dea:_test-bp-bad-*` to make the synthetic-prefix nature unmistakable? (Deferred to CR-BP-15.)
2. Should `dea:bp:*` legacy references carry an `external_system` qualifier (e.g. `dea:bp:apqc:4.1.1`) so the foreign-system provenance is machine-readable? (Deferred to CR-BP-16.)
3. Should CR-BP-12 require that first-class Process Group records inherit the existing `dea:group-*` label 1:1, or permit a rename with a `previous_ids` migration array? (Recommendation: 1:1 inherit; no rename. Track in CR-BP-12.)

## 13. Sources

- `technehub-labs/dea-catalog-processes/schemas/entity.schema.json`
- `technehub-labs/dea-catalog-processes/schemas/contribution.schema.json`
- `technehub-labs/dea-catalog-processes/schemas/entities/process-context.schema.json`
- `technehub-labs/dea-catalog-processes/entities/v1-alpha/dea_bp_manage-customer-relationship.yaml`
- `technehub-labs/dea-catalog-processes/scripts/check_process_identity.py`
- `technehub-labs/dea-catalog-processes/scripts/check_process_context.py`
- `technehub-labs/dea-catalog-processes/scripts/check_legacy_migration.py`
- `technehub-labs/dea-catalog-processes/scripts/check_ecf_conformance.py`
- `technehub-labs/dea-catalog-processes/change-requests/CR-BP-03-business-process-architecture.md`
- `technehub-labs/dea-catalog-processes/change-requests/CR-BP-03A-legacy-migration.md`
- `technehub-labs/dea-catalog-processes/change-requests/CR-BP-03C-sample-process-contribution.md`
- `technehub-labs/dea-catalog-processes/change-requests/CR-BP-11-l1-process-group-discovery.md`