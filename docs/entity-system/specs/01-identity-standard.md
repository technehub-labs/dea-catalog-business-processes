# Entity Identity Standard

> **CR-BP-122 Stage 2 output 1.** Normative spec for the General Entity System's identity discipline in `dea-catalog-business-processes`. Foundation: [00-charter.md](../00-charter.md), [02-normative-design-proposal.md §1](../02-normative-design-proposal.md). Companion: [CR-012 EGV-002..004](../../../../dea-governance/change-requests/CR-012-org-wide-entity-governance.md).

## 1. Scope

This spec codifies the **identity discipline** for every governed entity in `dea-catalog-business-processes`. The discipline is built on three CR-012 normative requirements: **EGV-002 (Stable Identity)**, **EGV-003 (Identifier and Namespace Governance)**, **EGV-004 (Identity Continuity)**.

The discipline covers:
- The canonical identifier format.
- The namespace ownership and allocation policy.
- The identity-continuity rules (renames, reclassifications, relocations, splits, mergers, supersession, retirement).
- The legacy id handling.
- The cross-catalog reference resolution (deferred to T8; this spec codifies the deferred status).

## 2. Normative rules

### IS-001 (canonical format) - blocking

> Every governed entity in `dea-catalog-processes` SHALL possess a persistent identifier that distinguishes it from other entities within its declared identity scope. The canonical identifier format is `processes:<token>-<descriptor>-<base32hash>` (per CR-BP-mv1, IDM-001..008).
>
> The `dea:` family is reserved for:
> - The metamodel's entity-type definitions (per EGV-001; the `dea:` family is the metamodel's identifier space).
> - Legacy migration references (per CR-BP-04; the 4 canonical id families are `dea:process-*`, `dea:pc-*`, `dea:group-*`, `dea:scope-*`).

**Source rules**: IDM-001 (pattern), IDM-004 (BASE32 strict alphabet), IDM-005 (filename + cell segment + depth validation), IDM-006 (legacy id regex), IDM-007 (research dir requirement), IDM-008 (cross-repo coherence). **Verification**: `scripts/check_id_system.py`.

### IS-002 (namespace ownership) - blocking

> The `processes:` namespace is owned by `dea-catalog-processes`. Allocation authority is the catalog's admission gate (ADM-001..008). No other repository SHALL allocate identifiers in the `processes:` namespace; no entity in this catalog SHALL use a different namespace.
>
> Cross-namespace references (e.g. a BP record's `relationships[].target` pointing at a `dea-catalog-business-capabilities` id) SHALL carry an `identity_scope` declaration: `scope: dea-catalog-business-capabilities`.

**Source rules**: EGV-001 (canonical governance authority), EGV-003 (identifier and namespace governance), EGV-009 (catalog conformance). **Verification**: the new entity-system umbrella gate (Stage 3-4, CR-BP-123) checks identity_scope presence on every cross-namespace reference.

### IS-003 (identity continuity) - blocking

> Changes to an entity's mutable attributes (name, description, hierarchy position, classification, intent, framework coordinate) SHALL NOT, by themselves, create a new entity identity. Entity renaming, reclassification, relocation, restructuring, and other revisions SHALL preserve identity where the underlying entity remains the same.
>
> The hash-suffix stability rule applies: the 6-character BASE32 entropy suffix on a record's id is stable across renames AND content edits; it is assigned at canonicalization, not recomputed live. Provenance lives in `reconciliation/migration-id-map.yaml`.

**Source rules**: EGV-004 (identity continuity), IDM-006 (legacy id regex for migration tail). **Verification**: the entity-system umbrella gate asserts that the hash-suffix is unchanged across the per-record change_history; the `migration-id-map.yaml` registry carries the per-id provenance.

### IS-004 (legacy id handling) - blocking

> Legacy `dea:` identifiers in `entities/v1-alpha/` (35 records; the post-mv1 migration tail) SHALL be grandfathered as historical record. New records MUST use the `processes:` family.
>
> The grandfathered legacy tail is documented in `reconciliation/migration-id-map.yaml` with: `old_id`, `new_id` (or `grandfathered`), `disposition` (one of: grandfathered / admit-with-override / require-migration / retire / accept-residual), `provenance` (the CR that introduced the legacy id), `cr` (the entity-system carrier CR that codified the disposition).

**Source rules**: EGV-004 (identity continuity), EGV-012 (legacy reconciliation), CR-BP-04 (id-family reconciliation), CR-BP-mv1 (entity storage and id migration). **Verification**: the entity-system umbrella gate asserts every record's id is either `processes:`-prefixed (canonical) or carries a `grandfathered` disposition in `reconciliation/migration-id-map.yaml`.

### IS-005 (split / merge / supersession) - blocking

> When an entity is split, merged, superseded, replaced, or determined to be semantically distinct, the applicable transition SHALL be explicitly recorded in the carrier CR + the entity's `lifecycle` block + the `relationships[]` entries that point at the new/old entities. The new identity is a new record; the old identity is either:
>
> - `superseded` (terminal; the successor carries the identity forward; no resurrection; per EGV-004), OR
> - `retired` (the entity is removed from active use; the record remains for historical traceability; per the Lifecycle Standard).
>
> Identifiers SHALL NOT be silently reassigned to different entities.

**Source rules**: EGV-004 (identity continuity), the Lifecycle Standard (§4 below). **Verification**: the entity-system umbrella gate asserts the `superseded` state is terminal (no transitions out of `superseded`); the `retired` state is terminal with the entity removed from active composition.

### IS-006 (cross-catalog references; deferred) - informational

> Cross-catalog references (a BP record's `relationships[].target` pointing at a record in `dea-catalog-business-capabilities`, `-organizational-units`, or any other catalog) carry an `identity_scope` declaration. The canonical reference form is:
>
> ```yaml
> relationships:
>   - relationship_type: realizes
>     target: <id>
>     identity_scope: <catalog-namespace>  # e.g. dea-catalog-business-capabilities
> ```
>
> The cross-catalog URI form (U-01 in the Gap Register) is **deferred to T8 of the umbrella programme** (Legacy ID reconciliation). Today's references use the target id + scope; URL-based URIs are a future enhancement.
>
> Per EGV-006 (relationship and reference integrity), references SHALL resolve to valid entities within the declared identity scope. A reference whose target id does not exist in the declared scope is a NON-CONFORMANT finding.

**Source rules**: EGV-006 (relationship and reference integrity), U-01 in the Gap Register. **Verification**: the entity-system umbrella gate (Stage 3-4) asserts the target id resolves; the cross-catalog resolution registry (Stage 5) declares the per-catalog id scope.

## 3. Worked example

A business process named "Manage Customer Relationship" with the canonical id `processes:process-manage-customer-relationship-f3n8wb` and a relationship to a capability:

```yaml
id: processes:process-manage-customer-relationship-f3n8wb
type: Process
name: Manage Customer Relationship
definition: |
  The L2 Business Process that realises the customer-relationship
  management capability for an enterprise customer base.
description: |
  Operates within the dea:pc-pr-operate Cell Charter. See trigger
  and outcome for the bounded work definition.
lifecycle:
  status: admitted
  admitted_at: '2026-08-15'
  admitted_by: CR-BP-03C
relationships:
  - relationship_type: realizes
    target: capabilities:capability-manage-customer-relationship-m6fmyx
    identity_scope: dea-catalog-business-capabilities
classifications:
  - process_type: operational
  - process_intent: deliver
  - ecf_coordinate:
      domain: customer-relationship
      stage: operate
provenance:
  admitted_by_cr: CR-BP-03C
  change_history:
    - cr: CR-BP-03C
      date: '2026-08-15'
      change: initial admission
    - cr: CR-BP-117c
      date: '2026-09-15'
      change: folder rename to human-readable form (C-1)
```

This example demonstrates:
- IS-001: the id is `processes:`-prefixed, follows the canonical format.
- IS-002: the cross-catalog relationship carries `identity_scope: dea-catalog-business-capabilities`.
- IS-003: the entity survived the CR-BP-117c folder rename; the id is unchanged; the `change_history` records the rename.
- IS-004: N/A (this is a canonical-form record).
- IS-005: N/A (no split / merge / supersession).
- IS-006: the cross-catalog reference resolves to a valid `dea-catalog-business-capabilities` id; the resolution mechanism is the cross-catalog resolution registry (T8 of the umbrella programme).

## 4. Acceptance criteria

- AC-IS-01 Every record in `entities/v1-alpha/` and `contexts/v1-alpha/` carries a `processes:`-prefixed id OR is in `reconciliation/migration-id-map.yaml` as `grandfathered`.
- AC-IS-02 Every cross-namespace reference carries an `identity_scope` declaration.
- AC-IS-03 Every record's `lifecycle.status` is one of the 5 states (proposed / admitted / deprecated / retired / superseded).
- AC-IS-04 The `superseded` state is terminal: no record carries a non-terminal transition out of `superseded`.
- AC-IS-05 The `reconciliation/migration-id-map.yaml` registry documents every legacy `dea:` id with a disposition.
- AC-IS-06 The hash-suffix stability rule holds: the 6-character BASE32 suffix on a record's id is unchanged across the per-record `change_history` (no recomputation on content edits).

## 5. Cross-references

- CR-012 EGV-002..004 (the org-wide normative requirements)
- CR-BP-mv1 (entity storage and id system migration; the IDM-001..008 rules)
- CR-BP-04 (id-family reconciliation; the four canonical id families)
- CR-BP-117a (entity-identity clarity; the EID-001..004 diagnostic gates)
- CR-BP-117c (folder/path clarity; the human-readable directory rename)
- The Lifecycle Standard (§4 of CR-BP-122's specs) for the lifecycle state machine
- The Relationship Standard (§3 of CR-BP-122's specs) for the cross-catalog reference resolution
