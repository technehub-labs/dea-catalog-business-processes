# Entity Lifecycle Standard

> **CR-BP-122 Stage 2 output 4.** Normative spec for the General Entity System's lifecycle discipline in `dea-catalog-business-processes`. Foundation: [00-charter.md](../00-charter.md), [02-normative-design-proposal.md §4](../02-normative-design-proposal.md). Companion: [CR-012 EGV-004, EGV-007, EGV-011](../../../../dea-governance/change-requests/CR-012-org-wide-entity-governance.md).

## 1. Scope

This spec codifies the **lifecycle discipline** for every governed entity in `dea-catalog-processes`. The discipline is built on CR-012 normative requirements **EGV-004 (Identity Continuity)**, **EGV-007 (Version and Lifecycle Separation)**, and **EGV-011 (Change Enforcement)**.

The discipline covers:
- The 5-state lifecycle machine.
- The per-transition rules.
- The identity-continuity rules during transitions.
- The version-separation discipline (entity identity vs entity revision vs schema version vs catalog release).
- The provenance requirements per transition.

## 2. The 5-state lifecycle machine

```
                +-----------+
                | proposed  |  (documented, not yet admitted)
                +-----+-----+
                      |
                      v
                +-----------+      +-----------+
                | admitted  |----->| superseded|  (terminal; no resurrection)
                +-----+-----+      +-----------+
                      |
                      v
                +-----------+
                |deprecated |  (no longer recommended; successor exists)
                +-----+-----+
                      |
                      v
                +-----------+
                |  retired  |  (removed from active use; record remains)
                +-----------+
```

### LS-001 (states) - blocking

> Every record's `lifecycle.status` SHALL be one of the 5 governed states:
>
> - `proposed`: documented but not yet admitted; created via the contribution workflow (`contributions/processes/`).
> - `admitted`: canonical; the record is in `entities/v1-alpha/`, satisfies the gate roster, and is referenced from other records.
> - `deprecated`: no longer the recommended choice; a successor exists; the record remains in the catalog; new records should reference the successor.
> - `retired`: removed from active use; the record remains in the catalog for historical traceability; the gate roster continues to validate it.
> - `superseded`: terminal; the entity has been replaced; the successor carries the identity forward; no resurrection.
>
> A `lifecycle.status` value not in the 5-state set is a NON-CONFORMANT finding.

**Source rules**: EGV-007 (version and lifecycle separation), CR-BP-14 (semantic reconciliation; the 6-dimension semantic contract). **Verification**: the entity-system umbrella gate (Stage 3-4, CR-BP-123) asserts the `lifecycle.status` value is in the canonical set.

### LS-002 (transitions) - blocking

> The transitions are:
>
> | From | To | Rule |
> |---|---|---|
> | (none) | `proposed` | The record is created via the contribution workflow. |
> | `proposed` | `admitted` | The CR is approved; the record satisfies the gate roster; the `lifecycle.admitted_at` and `lifecycle.admitted_by` fields are set. |
> | `admitted` | `superseded` | A new record (the successor) is admitted; the successor's `relationships[]` includes `relationship_type: specializes` (or a documented successor relationship); the superseded record's `lifecycle.superseded_at` field is set. |
> | `admitted` | `deprecated` | The entity is no longer the recommended choice; a successor exists or will exist; the `lifecycle.deprecated_at` field is set. |
> | `admitted` | `retired` | The entity is removed from active use; the record remains for historical traceability; the `lifecycle.retired_at` field is set. |
> | `deprecated` | `retired` | The deprecated entity is retired; the record remains. |
> | `superseded` | (any) | **Terminal. No transitions out of `superseded`.** A record's `lifecycle.status` once `superseded` stays `superseded` forever. |
> | `retired` | (any) | Terminal. No transitions out of `retired`. |
>
> A transition not in the table is a NON-CONFORMANT finding (e.g. `proposed` -> `retired` directly is rejected; the record must first be `admitted`).

**Source rules**: EGV-007, EGV-011 (change enforcement), the legacy migration discipline (CR-BP-mv1). **Verification**: the entity-system umbrella gate asserts the per-record transition is in the table.

### LS-003 (identity continuity) - blocking

> A transition SHALL NOT change the entity's id (per EGV-004: identity continuity). The id is stable across all transitions; the lifecycle block records the transitions.
>
> An exception: a `superseded` transition MAY introduce a NEW id (the successor's id) and a `supersedes` relationship entry; the superseded record keeps its original id (the id is preserved for historical traceability; the successor carries the identity forward per EGV-004).
>
> A transition that changes the id without introducing a successor is a NON-CONFORMANT finding (silent reassignment per EGV-004: "Identifiers SHALL NOT be silently reassigned to different entities").

**Source rules**: EGV-004 (identity continuity), the IS-001 + IS-003 rules in the Identity Standard. **Verification**: the entity-system umbrella gate asserts the id is unchanged across transitions; the `provenance.change_history[]` entries record the transitions.

### LS-004 (terminal states) - blocking

> The `superseded` and `retired` states are terminal: no transitions out of these states. A record in `superseded` or `retired` is preserved in the catalog for historical traceability; the gate roster continues to validate it; new records MUST NOT reference the superseded/retired record as the active choice.
>
> Resurrection (moving a record from `superseded` or `retired` back to `admitted`) is rejected. If the entity needs to be re-introduced, a NEW record is admitted with a new id; the old record stays in `superseded` or `retired` for historical traceability.

**Source rules**: EGV-004, EGV-007. **Verification**: the entity-system umbrella gate asserts no transition out of `superseded` or `retired`.

### LS-005 (provenance per transition) - blocking

> Every transition SHALL add an entry to the record's `provenance.change_history[]` block. The entry carries: `cr` (the carrier CR), `date` (the transition date; ISO-8601), `change` (a human-readable description of the transition).
>
> A transition without a corresponding `change_history[]` entry is a NON-CONFORMANT finding.

**Source rules**: EGV-008 (provenance and traceability), CR-BP-31 (ECF conformance block; the change_history requirement), CR-BP-113 (the `change:` key requirement). **Verification**: the entity-system umbrella gate asserts every transition has a `change_history[]` entry; the CR-BP-113 gate (already in place) asserts every entry has the `change:` key.

## 3. The version-separation discipline (per EGV-007)

### LS-006 (four distinct concepts) - blocking

> The governance model distinguishes:
>
> - **Entity identity**: the persistent id of the entity (per IS-001 in the Identity Standard).
> - **Entity revision**: a particular state or revision of the entity; not encoded in the id; recorded in `provenance.change_history[]`.
> - **Schema version**: the version of the structural contract used to represent the entity; recorded in `schemas/entities/<type>.schema.json` (the per-type schema's `$id` or version field).
> - **Catalog release**: the published state of the catalog containing the entity; recorded in CHANGELOG.md and the release tags.
>
> These concepts SHALL NOT be conflated in identifier allocation. The `processes:` id identifies the entity identity; the schema version is separate; the catalog release is separate. A schema version bump or a catalog release cut does NOT create a new entity identity.

**Source rules**: EGV-007 (version and lifecycle separation), the `processes:` namespace discipline. **Verification**: the entity-system umbrella gate asserts the id format does not encode schema version or catalog release; the per-type schema's version field is separate.

### LS-007 (revision vs identity) - blocking

> An entity's revision changes when its content changes (a field is updated, a relationship is added, etc.). The revision is recorded in `provenance.change_history[]`; the entity identity is unchanged.
>
> A revision is NOT a transition (LS-002). A revision is an in-place update; a transition is a state change in the lifecycle machine.

**Source rules**: EGV-007, the `provenance.change_history[]` discipline. **Verification**: the entity-system umbrella gate distinguishes revisions (in-place updates) from transitions (lifecycle state changes).

## 4. Worked example

A record's lifecycle block, demonstrating all 5 states over time:

```yaml
id: processes:process-manage-customer-relationship-f3n8wb
type: Process
name: Manage Customer Relationship
definition: |
  The L2 Business Process that realises the customer-relationship
  management capability for an enterprise customer base.
lifecycle:
  status: superseded
  admitted_at: '2026-08-15'
  admitted_by: CR-BP-03C
  deprecated_at: '2026-09-15'
  superseded_at: '2026-10-01'
provenance:
  change_history:
    - cr: CR-BP-03C
      date: '2026-08-15'
      change: |
        Initial admission as the canonical Manage Customer
        Relationship BP (proposed -> admitted).
    - cr: CR-BP-117c
      date: '2026-09-15'
      change: |
        Folder rename to human-readable form (CR-BP-117c C-1);
        no identity change (LS-003).
    - cr: CR-BP-119
      date: '2026-09-15'
      change: |
        Deprecated in favour of the new process decomposition
        (admitted -> deprecated); successor is processes:process-
        manage-customer-relationship-f3n8wb-v2 (admitted via
        CR-BP-119).
    - cr: CR-BP-122
      date: '2026-10-01'
      change: |
        Superseded by the new process decomposition (deprecated
        -> superseded); the successor is the v2 record.
```

This example demonstrates:
- LS-001: the `lifecycle.status` is `superseded` (one of the 5 governed states).
- LS-002: the transitions are `proposed -> admitted` (CR-BP-03C), `admitted -> deprecated` (CR-BP-119), `deprecated -> superseded` (CR-BP-122); all transitions are in the table.
- LS-003: the id is stable across all transitions.
- LS-004: the `superseded` state is terminal; no further transitions.
- LS-005: every transition has a `change_history[]` entry.
- LS-006: the id does not encode the schema version or catalog release.
- LS-007: the CR-BP-117c folder rename is a revision (in-place update), not a transition.

## 5. Acceptance criteria

- AC-LS-01 Every record's `lifecycle.status` is one of the 5 governed states.
- AC-LS-02 Every transition is in the LS-002 transition table; no transition out of `superseded` or `retired`.
- AC-LS-03 Every transition has a `provenance.change_history[]` entry with `cr`, `date`, `change` keys.
- AC-LS-04 The `superseded` and `retired` states are terminal: no record carries a non-terminal transition out of these states.
- AC-LS-05 The id format does not encode schema version or catalog release (per LS-006).
- AC-LS-06 The deprecated exemption (MECE-008) is honored: deprecated BPs are intentionally not composed.

## 6. Cross-references

- CR-012 EGV-004, EGV-007, EGV-011 (the org-wide normative requirements)
- CR-BP-14 (semantic reconciliation; the lifecycle state machine)
- CR-BP-31 (ECF conformance block; the change_history requirement)
- CR-BP-113 (the `change:` key requirement; the change_history backfill discipline)
- CR-BP-115 (admission-authority marker; the per-CR admission discipline)
- MECE-001..008 (the composition + cardinality rules)
- LCM-001..005 (the existing lifecycle state-machine gate)
- The Identity Standard (§1) for the id stability rule
- The Entity Contract Standard (§2) for the `lifecycle` block schema
- The Conformance Standard (§5) for the per-transition gate assertions
