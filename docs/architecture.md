# Process Architecture

**CR-BP-03 §1, §4, §5, §6, §7, §8, §10; CR-BP-14 §4, §5, §6, §7, §8, §13.**

This document captures the Business Process architecture established by
CR-BP-03 and reconciled by CR-BP-14. The catalog's primary subject is
the **L2 Business Process** (`dea:BusinessProcess`), a Core
specialization of the abstract OpenDEA Process kernel `dea:Process`
(CR-MM-PROC-01). The L0/L1 levels are conceptual and live in this
document + `README.md`; they are **not** separate top-level directories.

## Orientation

Two documents orient the reader before this detailed narrative:

- [`docs/semantic-contract.md`](semantic-contract.md): what a Business
  Process record means; the six characterization dimensions and the
  separations that are always true (the CR-BP-14 constitution).
- [`docs/governance/reconciliation-programme.md`](governance/reconciliation-programme.md):
  the closed governance loop; the CR lineage; the reconciliation
  dispositions; the conformance levels.

The CR-BP-14 semantic contract governs this document. Where earlier
prose conflicts with CR-BP-14, the CR governs.

## Decomposition

```text
ECF Domain × Lifecycle Stage
         │
         ▼
   Process Context          (CR-BP-02; contexts/v1-alpha/)
         │
         ▼
   L0 Process Scope         (conceptual; documented here)
         │
         ▼
   L1 Process Group         (canonical; entities/v1-alpha/;
         │       dea:group-*; PG-001..008)
         ▼
   L2 Business Process      (canonical; entities/v1-alpha/;
         │       dea:process-*)
         ▼
   L3 Activity              (canonical; CR-BP-32;
         │       entities/v1-alpha/; dea:activity-*;
         │       ACT-001..010)
         ▼
   Workflow / Task          (L4; future; authoritative
                             metamodel; dea:Task lifecycle:
                             proposed)
```

## Process Context

Established by CR-BP-02 and formalized by CR-BP-14 §5: represents
`ECF Domain × Lifecycle Stage` and provides the semantic boundary in
which processes are discovered, organized, and validated. It is
**not** itself a Business Process. The catalog carries Process Context
entries at `contexts/v1-alpha/` (currently `v1-alpha/` until the matrix
is populated per CR-BP-02 §22).

A Process Context is not itself: a Business Process, a Process Group,
a Business Function, a Business Capability, a process classification
or a process intent. An ECF intersection does not automatically
represent a business process. The catalog enforces:

> ECF provides context; Process Architecture provides process structure.

## L0 Process Scope

The highest catalog topology construct within a Process Context. It
answers: what coherent enterprise responsibility is being organized
within this context (CR-BP-14 §6)? Process Scope SHALL establish a
stable semantic boundary, organize related process responsibilities,
avoid sibling overlap, and provide a basis for Process Group
decomposition. Process Scope is not itself a Business Process.

Example (illustrative): within the Process Context `dea:pc-pr-op`
(PartyAndRelationship × Operate), an L0 Process Scope might be "Customer
Onboarding" (covering the area of bringing new customers into the
operating relationship).

## L1 Process Group

A coherent grouping of Business Processes within a Process Scope
(CR-BP-14 §7). A Process Group organizes related process
responsibilities that share a meaningful functional or operational
relationship. It SHALL have a coherent grouping rationale, a distinct
boundary, one or more lower-level process responsibilities, and
support for systematic decomposition. Process Group is NOT
equivalent to Business Function, Business Capability, Process Intent,
Process Classification or Business Process. The catalog maintains
Process Group as a catalog construct; it is not an OpenDEA metamodel
entity. Since the CR-BP-19 register landings (CR-BP-21a..21e), each
Process Group is a canonical record at `entities/v1-alpha/dea:group-*/`,
gated by PG-001..008.

The containment direction is `L1 group --composes--> L2 process`; the
inverse `part-of` view is generated at query time (see CR-BP-12
PG-004/PG-005). The L2-to-L3 linkage is bidirectional per ACT-010:
`metadata.activity_references[]` on the Business Process and
`belongs_to_business_process` on the Activity.

## L2 Business Process

The first canonical semantic entity: `dea:BusinessProcess`. All
L2 process definitions must conform to the authoritative OpenDEA
metamodel. The L2 entry lives in `entities/v1/` (currently
`v1-alpha/`).

## L3 Activity

The cohesive grouping of work within a Business Process (CR-BP-32;
ACT-001..010). An Activity fails standalone executability and resource
dedication (CR-BP-32 §5) and is therefore not itself a Business
Process. Every Activity record conforms to
`schemas/entities/activity.schema.json`, inherits its parent BP's ECF
coordinate, and carries `decomposition_boundary: l4-reached` pending
metamodel-owned Task records (CR-BP-32 §12). L3 coverage is complete
across all seven ECF domains: 501 canonical Activity records over 126
Business Processes (CR-BP-42 pilot; CR-BP-43..57 tranches).

## Structural composition

Process decomposition uses the authoritative OpenDEA relationship
`dea:composes`. Structural composition means:

- part-of structure;
- containment within the process architecture;
- hierarchical decomposition;
- **no implied sequence**;
- **no implied execution**;
- **no implied organizational ownership**.

```text
L1 Process Group
       │
       ▼
L2 Business Process
       │
       └── dea:composes ──► L2 Business Process
```

In the schema, structural composition is captured in the
`relationships` array (canonical; CR-BP-03 §6; CR-BP-03A §3.1).
Each relationship entry conforms to the metamodel's
`relationship-instance.json` shape with full provenance.

## Capability realization

Capability realization is captured in the `relationships` array
as relationship instances of type `realizes`. Each entry
conforms to the metamodel's `relationship-instance.json` shape.

```text
              ┌───────────────┐
              │ Business      │
              │ Capability    │
              └───────▲───────┘
                      │
                   realizes
                      │
              ┌───────┴───────┐
              │ Business      │
              │ Process       │
              └───────┬───────┘
                      │
                   composes
                      │
                      ▼
              Business Process
```

## Structural vs execution

```text
Structural architecture    Behaviour / execution
─────────────────────      ───────────────────
Context                   Business Process
   ↓                           ↓
Scope                       Activity
   ↓                           ↓
Group                       Workflow
   ↓                           ↓
Business Process             Task
```

These are different modeling dimensions. Workflow and Task
already exist in the OpenDEA metamodel and should not be
reinvented by the process catalog.

- **CR-BP-03** → structural process architecture (this document)
- **CR-BP-32** → Activity Model (landed; ACT-001..010; depends on the
  CR-BP-04 id-family contract)
- **CR-BP-33** → Execution Boundary (landed; EXE-001..010)

## The `relationships` shape (CR-BP-03A §3.1)

The `relationships` field is an **array of relationship
instances**, NOT a structured object. Each entry is a typed
relationship with full CR-002 provenance, CR-6 lifecycle, and
effective_from/to temporal validity:

```yaml
relationships:
  - source_id: dea:bp:manage-customer
    target_id: dea:bp:manage-enterprise-customer
    relationship_type: composes
    status: active
    rationale: "L2 Business Process structurally composes another L2."
    provenance:
      type: manual
      asserted_by: <contributor>
      asserted_at: <YYYY-MM-DD>
  - source_id: dea:bp:manage-customer
    target_id: dea:capability:manage-customer
    relationship_type: realizes
    status: active
    rationale: "Business Process realizes Business Capability."
    provenance:
      type: manual
      asserted_by: <contributor>
      asserted_at: <YYYY-MM-DD>
```

The catalog primarily uses `composes` (structural composition)
and `realizes` (capability realization). Other types
(`specializes`, `aggregates`, `depends-on`, etc.) are admitted
when the contributor can defend the choice.

The metamodel's `relationship-instance.json` is authoritative
on the relationship shape. The catalog profiles the source_id
and target_id to the catalog's process id namespace
(`dea:bp:...`).

## Legacy field migration (CR-BP-03A §3.2, §3.3)

Three legacy fields are addressed by CR-BP-03A:

1. **`parent_process`**: REMOVED. This was a catalog invention
   from CR-BP-01 (the wrong-premise implementation, since
   reverted). The metamodel's `process.json` does not declare
   it. The migration validator
   (`scripts/check_legacy_migration.py`; BP-MIG-001) surfaces
   any entry that declares it and emits a migration
   recommendation.
2. **`child_processes`**: REMOVED. Same as `parent_process`.
   The migration validator (BP-MIG-002) surfaces any entry that
   declares it.
3. **`capabilities_delivered`**: Soft-deprecated. The metamodel
   still declares this as a simple array of strings (a
   backward-compat shim). CR-BP-03A keeps the field in the
   schema but marks it as soft-deprecated. The canonical form
   is `relationships[relationship_type=realizes]` with full
   provenance. The migration validator (BP-MIG-003) surfaces
   any entry that declares it and emits a migration
   recommendation.

The migration is **contribution-driven**: the contributor
updates the proposed_entry to use the canonical form, re-runs
CI, and the reviewer approves. The catalog does not
auto-rewrite.

## See also

- [`README.md`](../README.md): the architectural statement
- [`docs/semantic-contract.md`](semantic-contract.md): the CR-BP-14
  semantic constitution
- [`docs/classification.md`](classification.md): the classification
  narrative (4 axes; CR-BP-14 §11 Intent != Classification)
- [`docs/context.md`](context.md): Process Context as canonical
  placement (CR-BP-14 §13)
- [`docs/specialization.md`](specialization.md): specialization as
  semantic refinement (CR-BP-14 §12)
- [`docs/identity.md`](identity.md): the process-identity contract
- [`docs/relandscape.md`](relandscape.md): the contribution-driven re-landscape mechanism
- [`docs/governance/reconciliation-programme.md`](governance/reconciliation-programme.md)
 : the closed governance loop (CR-BP-15, CR-BP-16)
- [`change-requests/CR-BP-03-business-process-architecture.md`](../change-requests/CR-BP-03-business-process-architecture.md)
- [`change-requests/CR-BP-03A-legacy-migration.md`](../change-requests/CR-BP-03A-legacy-migration.md)
- [`change-requests/CR-BP-14-process-semantic-reconciliation.md`](../change-requests/CR-BP-14-process-semantic-reconciliation.md)
