# CR-ECF-CG-004: Business Process Catalog Conformance

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

| Field | Value |
|-------|-------|
| **CR** | CR-ECF-CG-004 |
| **Title** | Business Process Catalog Conformance |
| **Status** | Proposed |
| **Type** | Catalog Conformance |
| **Repository** | technehub-labs/dea-catalog-processes |
| **Implements** | CR-ECF-CG-001 |
| **Depends On** | CR-ECF-005, CR-ECF-CG-002 |
| **Author** | Coder (for eaojnr) |
| **Date** | 2026-09-01 |

## 1. Purpose

Verify that the Business Process Catalog correctly specializes ECF Coordinates into Process Context without conflating ECF coordinates with business processes or process decomposition levels.

This one is especially important because the Process Catalog has already developed the correct conceptual distinction.

## 2. Canonical Relationship

The repository shall preserve:

ECF Coordinate
      ↓
Process Context
      ↓
L0 Process Scope
      ↓
L1 Process Group
      ↓
L2 Business Process
      ↓
L3 Activity
      ↓
L4 Task

## 3. Process Context

Process Context is the catalog-specific interpretation of an ECF Coordinate for process architecture.

It is not itself a Business Process.

Therefore:

Process Context ≠ Business Process

## 4. Coordinate Cardinality

An ECF Coordinate may have:

zero
one
many

associated L0 Process Scopes.

The catalog shall not require one process per coordinate.

## 5. Process Decomposition

ECF shall provide contextual grounding.

The Process Catalog shall own process decomposition rules.

Therefore:

ECF Coordinate
    does not determine
L0-L4 decomposition

L0-L4 shall remain governed by the Process Catalog methodology.

## 6. Cross-Context Processes

Where a business process legitimately spans multiple ECF contexts, the model shall preserve process identity and represent contextual relationships rather than duplicating the process merely to populate cells.

## 7. Boundary Validation

The repository shall explicitly distinguish:

Process Scope
Process Group
Business Process
Activity
Task
Capability
Function
Workflow

## 8. Acceptance Criteria

- [ ] Process Context is distinct from Business Process.
- [ ] Canonical ECF Coordinate references resolve.
- [ ] No one-process-per-coordinate assumption exists.
- [ ] L0-L4 decomposition remains catalog-governed.
- [ ] Cross-coordinate processes retain identity.
- [ ] Process/Capability/Function boundaries are preserved.
- [ ] Documentation and schemas conform to CR-ECF-001..005.

## 9. Definition of Done (this proposal PR)

Two files: this CR (verbatim against the source tranche) and the change-requests index row. Implementation PR (schema addition of optional `ecfConformance` block, conformance gate, governance decision record, README profile declaration) ships on subsequent acceptance.

## 10. Governance Decision: `process_audience` is NOT an ECF Coordinate

Recorded for explicit ratification. The catalog's existing `process_audience` field uses the same 7 kebab-case enum as the capability catalog's `ecf.primary.domain`:

| Aspect | `process_audience` | ECF Domain |
|---|---|---|
| Cardinality | single value | one axis of (Domain x Stage) ordered pair |
| Semantic axis | "who does this process serve?" (audience classification) | "in which enterprise function does this concept primarily operate?" (contextual placement) |
| Catalog-specific? | yes (Process Catalog methodology) | no (canonical ECF semantics) |
| Resolves to canonical PascalCase enum? | no (display label, not a reference) | yes (must be `GovernanceAndExistence` etc.) |

The gate must not collapse these. Both use the same kebab-case vocabulary by *coincidence of display labelling*: the canonical semantic axis is different. The conformance block on each process entry will reference canonical ECF identifiers where applicable, and carry `process_audience` as an internal field that does not get mis-promoted.

## 11. References

CR-ECF-CG-001 (gate definition); CR-ECF-CG-002 (metamodel conformance); `dea-catalog-processes` metamodel pointer (entity_id `dea:entity-process`); CR-DEA-BC-04 (specialization framework, parallel precedent in capability catalog).