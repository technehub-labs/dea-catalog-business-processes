# Worked example: `processes:process-pr-operate-bbe384`

This document walks the **canonical pattern** for a Business
Process entry in the catalog, post-mv1. Future contributors
should treat this as the **reference example**.

The record lives at
`entities/v1-alpha/pr-operate/Customer-Lifecycle-Management/Manage-Customer-Relationship/processes-process-pr-operate-bbe384.yaml`
and was admitted under the 2026-09-20 entity-storage + id-system
migration (CR-BP-mv1) from the legacy
`dea:process-manage-customer-relationship` form. The id map
(`reconciliation/migration-id-map.yaml`) is the audit trail.

## The entry at a glance

| Field | Value |
|---|---|
| **Id** | `processes:process-pr-operate-bbe384` |
| **Name** | Manage Customer Relationship |
| **Process context** | `processes:pc-pr-operate-pwue5a` (PartyAndRelationship x Operate) |
| **Process intent** | `manage` |
| **Process type** | (catalog classification; per CR-BP-14 S21) |
| **Process specialization** | `[]` (root; no parent) |
| **ECF conformance** | `conformant`; inherits-catalog |
| **Evidence** | [APQC PCF](https://www.apqc.org/resource-library/resource-collections/56391) |

## The identity contract

A Business Process entry must declare an `identity` sub-block
and `trigger` / `outcome` fields (BP-SEM-001..014, BP-C1..C4):

| Field | This entry |
|---|---|
| **`identity.verb`** | `manage` |
| **`identity.object`** | `customer relationship` |
| **`identity.scope`** | `(all customer segments)` |
| **`identity.outcome_statement`** | An active customer relationship is sustained across its lifecycle... |
| **`identity.evidence_links`** | `[APQC PCF](...)` |
| **`trigger`** | A customer enters the active relationship lifecycle... |
| **`outcome`** | An active customer relationship is sustained across its lifecycle... |

The name **must** match `identity.verb + identity.object +
identity.scope` (case-insensitive; BP-ARC-ID-001). The
outcome_statement's keyword density **must** be consistent
with `process_type` (BP-ARC-ID-004).

## The canonical relationships

The `relationships` field is an **array of relationship
instances** conforming to the metamodel's
`relationship-instance.json` shape (CR-BP-03A §3.1). Each
entry has `source_id`, `target_id`, `relationship_type`,
plus optional `direction`, `status`, `effective_from/to`,
`asserted_by`, `rationale`, `evidence`, and `provenance`.

This entry has **one** relationship:

```yaml
relationships:
  - source_id: processes:process-pr-operate-bbe384
    target_id: processes:process-pr-operate-bbe384   # placeholder; sibling BP id
    relationship_type: realizes
    status: active
    direction: outgoing
    rationale: |
      The Business Process realizes the Business Capability
      `Manage Customer Relationship`.
    asserted_by: DEa team
    asserted_at: '2026-09-03'
    provenance:
      type: manual
      asserted_by: DEa team
      asserted_at: '2026-09-03'
      evidence: https://www.apqc.org/resource-library/resource-collections/56391
```

The catalog primarily uses `composes` (structural composition)
and `realizes` (capability realization).

## The L0/L1/L2 conceptual hierarchy

The L0/L1/L2 hierarchy is a **conceptual model** documented in
[`docs/architecture.md`](../architecture.md). It is **NOT**
separate top-level directories and **NOT** separate catalog
entities.

For this entry:

| Level | Construct | Sample |
|---|---|---|
| **Context** | `processes:pc-pr-operate-pwue5a` (Cell Charter) | `PartyAndRelationship x Operate` |
| **Scope (L0)** | The bounded enterprise context | Customer-facing operations |
| **Group (L1)** | A loose grouping of related BPs | Customer Lifecycle Management |
| **Business Process (L2)** | `processes:process-pr-operate-bbe384` | Manage Customer Relationship (this entry) |

The Scope and Group are recorded in the entry's `metadata`
field as documentation; they are **NOT** promoted to separate
catalog entities (per CR-BP-03 §3: classification != ontology).

## The Process Context reference

The entry's `process_context` field references the Cell
Charter at
`entities/v1-alpha/pr-operate/processes-pc-pr-operate-pwue5a.yaml`.
The Cell Charter's `processes` array references this entry
back, forming a bidirectional reference (PC-008).

## The ECF Conformance Gate

The entry declares an `ecfConformance` block
(CR-ECF-CG-001..004; enforced by
`scripts/check_ecf_conformance.py`):

```yaml
ecfConformance:
  framework: EnterpriseConceptFramework
  contractVersion: '1.0.0'
  profile: dea:ecf@1.0.0
  status: conformant
  affiliation: inherits-catalog
  canonicalReferences:
    - kind: coordinate
      domain: PartyAndRelationship
      stage: Operate
      identifier: ecf:partyRelationship.operate
```

The entry **inherits the catalog's conformance posture**
(`affiliation: inherits-catalog`); the canonical references
resolve to the ECF Domain and Stage of the Process Context.

## Validators exercised (all PASS)

| Validator | Result |
|---|---|
| `check_process_semantics.py` (BP-SEM-001..014) | PASS |
| `check_process_specialization.py` (BP-SPEC-01-001..007) | PASS |
| `check_process_context.py` (PC-001..PC-008) | PASS |
| `check_legacy_migration.py` (BP-MIG-001..005) | PASS |
| `check_ecf_conformance.py` | PASS |
| `check_id_system.py` (IDM-001..007) | PASS |
| `validate_consumer.py` against `dea-architecture-framework@v0.6.0` | PASS |

## Files for this entry

| Path | Purpose |
|---|---|
| [`entities/v1-alpha/pr-operate/Customer-Lifecycle-Management/Manage-Customer-Relationship/processes-process-pr-operate-bbe384.yaml`](../../entities/v1-alpha/pr-operate/Customer-Lifecycle-Management/Manage-Customer-Relationship/processes-process-pr-operate-bbe384.yaml) | The canonical BP entry |
| [`entities/v1-alpha/pr-operate/processes-pc-pr-operate-pwue5a.yaml`](../../entities/v1-alpha/pr-operate/processes-pc-pr-operate-pwue5a.yaml) | The Cell Charter (Process Context) |
| [`contributions/processes/dea_bp_manage-customer-relationship.yaml`](../../contributions/processes/dea_bp_manage-customer-relationship.yaml) | The contribution record (retargeted under CR-BP-113 §8) |
| [`change-requests/CR-BP-03C-sample-process-contribution.md`](../../change-requests/CR-BP-03C-sample-process-contribution.md) | The CR that originally landed the entry |

## Legacy attribution (preserved for audit)

Pre-mv1, this record carried the id
`dea:process-manage-customer-relationship`, the process context
`dea:pc-pr-op`, and lived at
`entities/v1-alpha/dea_bp_manage-customer-relationship.yaml`
with the Cell Charter at `contexts/v1-alpha/dea-pc-pr-op.yaml`.
Those legacy ids live in `reconciliation/migration-id-map.yaml`
as the audit trail; the current-shape record is the
authoritative form for all forward-going work.

## See also

- [`docs/architecture.md`](../architecture.md) — the architectural narrative
- [`docs/classification.md`](../classification.md) — the 4-axis classification
- [`docs/identity.md`](../identity.md) — the process-identity contract
- [`docs/relandscape.md`](../relandscape.md) — the contribution-driven re-landscape
- [`README.md`](../../README.md) — the architectural statement
