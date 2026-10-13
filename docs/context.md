# Process Context

**CR-BP-02; CR-BP-14 §5, §13; CR-ECF-CG-004 §10.**

A Process Context is the semantic boundary within which a Business
Process is identified, evaluated and reused. The catalog treats a
Process Context as a first-class record at
`entities/v1-alpha/<cell>/processes-pc-<cell>-<hash>.yaml`,
identified by a canonical `processes:pc-<cell>-<hash>` id and
backed by a Cell Charter. Pre-mv1 the records lived at
`contexts/v1-alpha/dea-pc-<cell>.yaml`; the CR-BP-mv1 migration
(2026-09-20) retired that directory and rewrote every reference
through `reconciliation/migration-id-map.yaml`.

## Definition

A Process Context is the intersection of:

- an **ECF Domain** (`dea:ecf:*`); and
- a **Lifecycle Stage** (`dea:ecf-stage:*`).

The intersection establishes the enterprise concern and the lifecycle
concern within which processes are identified.

## What a Process Context is not

A Process Context is not itself:

- a Business Process;
- a Process Group;
- a Business Function;
- a Business Capability;
- a process classification;
- a process intent.

## Normative rule

An ECF intersection never generates a process by itself. The catalog
enforces:

> ECF provides context; Process Architecture provides process structure.

## Canonical placement on a Business Process

The canonical representation of Process Context placement on a
Business Process is the `context:` block:

```yaml
context:
  - ref: processes:pc-pr-operate-pwue5a   # Process Context reference
  - ref: processes:pc-pr-improve-k8phkn   # multiplicity is permitted where evidence justifies
```

Pre-mv1 the same block used the `dea:pc-*` id family (`dea:pc-pr-op`,
`dea:pc-pr-im`); the CR-BP-mv1 migration (2026-09-20) replaced them
with the canonical `processes:pc-<cell>-<hash>` form. The migration
id map (`reconciliation/migration-id-map.yaml`) is the audit trail.

CR-BP-14 §13 / BP-SEM-008 enforce that every declared reference
resolves to a canonical Process Context entry. CR-BP-14 §13 / BP-SEM-007
forbid `process_audience` as a substitute.

## Contextual relationships

Where a Business Process interacts with ECF context at the Domain or
Domain × Lifecycle level without belonging to a specific Process
Context, the canonical expression is a `serves` or `contributes-to`
relationship toward the canonical ECF identifier
(`ecf:<lowerCamelDomain>` or `ecf:<lowerCamelDomain>.<lowerCamelStage>`,
the CG-003 form). The legacy `process_audience` value is a migration
alias and is never a substitute for either a Process Context
reference or a contextual relationship.

## Process Context multiplicity

A Business Process MAY participate in multiple Process Contexts where
evidence establishes legitimate cross-context responsibility
(CR-BP-14 §13; BP-SEM-012). A process is never forced into a single
audience merely because it participates in more than one enterprise
concern.

## See also

- [`docs/semantic-contract.md`](semantic-contract.md): Context tells us
  where to look (CR-BP-14 §29)
- [`docs/architecture.md`](architecture.md): the L0-L4 decomposition
- [`classifications/process-contexts.yaml`](../schemas/entities/process-context.schema.json):
  the schema (referenced for completeness; the canonical Process
  Context register lives in `contexts/v1-alpha/`)
- [`change-requests/CR-BP-02.md`](../change-requests/CR-BP-02.md):
  the Process Context register + Cell Charter schema
- [`change-requests/CR-BP-14-process-semantic-reconciliation.md`](../change-requests/CR-BP-14-process-semantic-reconciliation.md):
  §5, §13