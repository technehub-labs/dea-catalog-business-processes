# CR-BP-11: L1 Process Group Discovery Across the 49 ECF Coordinates

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Accepted (baseline ratified by CR-BP-13)
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
Program: Business Process Catalog
Parent: CR-BP-03-business-process-architecture
Related: CR-BP-03-business-process-architecture; CR-BP-02; CR-BP-03C-sample-process-contribution; CR-DEA-BC-04 (Business Capability Catalog ECF Overlay v0.2)
Decision Type: Architectural (research register)
Implementation: Research register only; no canonical entities in this CR.

---

## 1. Decision Statement

The Business Process Catalog shall establish a **research register of candidate L1 Process Groups across all 49 ECF coordinates**, with an explicit disposition per coordinate (`accepted`, `deferred`, `unresolved`, or `no-candidate`), before any further canonical population of the catalog proceeds.

The governing principle is:

> **A Process Context is a bounded interpretation of an ECF coordinate; L1 Process Groups are catalog-topology records that group related L2 Business Processes beneath an L0 scope; ECF coordinates carry zero, one, or many L1 groups; matrix coverage is a research question, not a population rule.**

The register therefore:

- records every coordinate with its semantic interpretation, in-scope concerns, out-of-scope concerns, candidate L0/L1/L2 elements, evidence, and disposition;
- preserves internal OpenDEA canon (ECF grounding, BC catalog overlay v0.2, CR-BP-03 hierarchy, the existing L2 sample) as the authority;
- uses external process frameworks (APQC, eTOM, BIAN, SCOR, ITIL, ISO 37000, ISO 22301, ISO 56002) as candidate-process and boundary evidence, never as canonical authority;
- does not in this CR create canonical L1 records or canonical L2 entries; both are deferred to CR-BP-12 and CR-BP-13 respectively.

---

## 2. Why This Decision Is Necessary

The architecture addresses four irreducible requirements:

1. The 7x7 ECF matrix is a coverage space, not a cell-filling template; every coordinate must carry an explicit disposition.
2. The existing catalog carries one canonical L2 process at `dea:process-manage-customer-relationship` with a `metadata.group` label that is ungoverned; before the catalog scales, L1 must become governed or the labels drift.
3. ECF coordinates legitimate-absent clauses (proven on CAND-019 Technology Management in CR-DEA-BC-04 R-004) must be honoured: a coordinate may legitimately contain zero L1 candidates.
4. The CR-BP-03 hierarchy (Context / L0 scope / L1 group / L2 process / L3 activity / L4 task) must be exercised end-to-end at least once with evidence before being promoted to the metamodel.

Without this register:

- the catalog risks manufacturing one L2 process per coordinate, inflating the catalog with thin evidence and locking the matrix into a 49-process commitment the catalog cannot defend;
- the L1 "group" label drifts across entries (Customer Lifecycle Management vs Customer Management vs Customer Operations) with no governance;
- the existing ID-family drift between `dea:process-*` and `dea:bp-*` propagates into the L1 reference field and compounds the inconsistency;
- the metamodel evidence base remains too thin to justify promoting Process Group to OpenDEA Core.

---

## 3. Decision Drivers

The L1 Process Group discovery addresses:

- governance of catalog-topology groupings beneath each Process Context;
- traceability of every L2 candidate back to a coordinate disposition;
- preservation of internal OpenDEA canon as authority (ECF grounding, BC overlay v0.2, CR-BP-03, the L2 sample);
- evidence policy that uses external frameworks as candidate sources, not authority;
- explicit recording of empty, deferred, and unmapped coordinates;
- MECE-by-construction at the L1 level (each L1 group must have non-overlapping scope with peer groups in the same context);
- a controlled upgrade path: research register; catalog-owned record schema (BP-12); seven-domain admission tranches (BP-13+);
- boundary evidence for cross-domain patterns (Change, Partner, Resilience, Innovation, Analytics) without forcing duplicate cells;
- conformance with the ECF canonical-identifier contract (`ecf:<domain>.<stage>`);
- conformance with the existing contribution-driven re-landscape pattern;
- conformance with the existing process identity, boundary, MECE, and metamodel gates;
- rejection of manufactured content: every L1 candidate is evidence-bound;
- explicit deferral reasons for every `deferred` disposition;
- an honest total: 49 coordinates recorded with dispositions, no `no-candidate` or `unresolved` entries hidden;
- a portable audit trail (the register, the L1 candidate universe YAML, this CR, the Locked-Picks log).

---

## 4. The Coordinate Universe

The ECF matrix is the 7-domain by 7-stage Cartesian product.

Domains (canonical order): GovernanceAndExistence, StrategyAndDirection, AgencyAndOrganization, PartyAndRelationship, ProductAndValue, EnablementAndOperations, FinanceAndAccounting.

Stages (canonical order): Conceive, Design, Build, Activate, Operate, Improve, Retire.

Total coordinates: `|D| x |S| = 7 x 7 = 49`.

Each coordinate carries:

- `process_context`: a candidate Process Context id of the form `dea:pc-<domain-token>-<stage-token>`;
- `l1_candidates`: candidate L1 Process Group names with non-overlapping scope;
- `l2_candidates`: candidate L2 Business Process names that would realize each L1 group;
- `in_scope`: a one-sentence summary of the concerns this coordinate covers;
- `out_of_scope`: a list of concerns explicitly excluded (boundary evidence);
- `evidence`: the source-of-truth files and standards that ground the disposition;
- `disposition`: one of `accepted`, `deferred`, `unresolved`, or `no-candidate`;
- `deferral_reason` (when `disposition=deferred`): a one-sentence rationale explaining what would re-open the disposition.

---

## 5. The Disposition Policy

Every coordinate receives exactly one disposition. The disposition is set by the following policy:

- `accepted`: the coordinate has at least one candidate L1 Process Group supported by internal OpenDEA canon or by external-framework evidence E3+ (independent corroboration);
- `deferred`: the coordinate has zero, weak, or overlapping candidates and the L1 group cannot be defensibly bounded yet; deferral reason is mandatory;
- `unresolved`: internal evidence contradicts itself or boundary overlap is unresolved; carries the conflicting pair;
- `no-candidate`: the coordinate legitimately carries no L1 group (ECF legitimately-absent clause; precedent: CAND-019 Technology Management in CR-DEA-BC-04 R-004).

In v0.1, no coordinate carries `unresolved` or `no-candidate`. Coordinates in the deferred bucket carry one of two deferral patterns:

- rare-event coordinates (e.g. governance-existence x retire, finance-and-value x retire, supply-and-resources x retire) where the event exists in some industries but is not enterprise-generality-strong;
- operational-overlap coordinates (e.g. agency-organization x activate) where the candidate group is an attribute of an adjacent group rather than a standalone L1.

---

## 6. The Evidence Policy

The register is grounded in three evidence tiers.

### Tier 1: Internal OpenDEA canon (authoritative)

- `dea-metaframework/framework/domain-grounding.md`, `lifecycle-grounding.md`, `matrix.md`, `constructs.md`
- `dea-metaframework/specification/ecf-coordinates.md`
- `dea-catalog-business-capabilities/docs/research/ecf-overlay-v0.2.yaml`
- `dea-catalog-processes/change-requests/CR-BP-03-business-process-architecture.md`
- `dea-catalog-processes/change-requests/CR-BP-02.md`
- `dea-catalog-processes/entities/v1-alpha/dea_bp_manage-customer-relationship.yaml`
- `dea-catalog-processes/docs/architecture.md`

### Tier 2: Internal sibling catalogs (corroborative)

- `dea-catalog-business-capabilities/entities/v1-alpha/capability-*.yaml` (BC catalog admitted capabilities)
- `dea-catalog-business-capabilities/docs/research/normalization.yaml` (N-001..N-007)
- `dea-catalog-business-capabilities/docs/research/candidates.yaml` (CAND-001..029)
- `dea-catalog-business-capabilities/docs/research/evidence-register.yaml`

### Tier 3: External frameworks (candidate sources only)

- APQC Process Classification Framework (PCF) 7.0
- TM Forum enhanced Telecom Operations Map (eTOM) and Customer Journey Management
- BIAN Service Landscape
- ASCM SCOR Digital Standard
- ITIL 4 Service Value System
- ISO 37000:2021 Governance of Organizations
- ISO 22301:2019 Security and Resilience
- ISO 56002:2019 Innovation Management

External frameworks contribute candidate processes, naming, and boundary evidence. They never override the disposition set by Tier 1.

---

## 7. The Boundary Discipline

L1 Process Groups must be MECE within their Process Context. The boundary discipline enforces:

1. Two L1 candidates in the same Process Context SHALL NOT have overlapping `in_scope` summaries.
2. The `out_of_scope` list for an L1 candidate SHALL reference peer groups or other contexts whose work it disclaims.
3. Cross-domain processes (Change Management, Partner Management, Resilience, Innovation, Analytics) are recorded once at their earliest-legitimate-initiation coordinate and referenced from peer coordinates; they are not duplicated as separate L1 cells.
4. Technology Management carries no ECF coordinate per CR-DEA-BC-04 N-006 / R-004; L1 candidates that touch technology must declare a domain (enablement-operations x operate for runtime; strategy-direction x operate for build/asset) and a technology-bearing relationship, not a standalone cell.
6. Customer-facing operations (which have already been adopted as `dea:scope-customer-facing-operations` in the L2 sample) continue to be referenced from party-relationship x operate; the existing L0 scope is honoured.

---

## 8. The Disposition Register

The disposition register totals 49 coordinates with the following distribution:

| Domain | Accepted | Deferred | Total |
|---|---:|---:|---:|
| GovernanceAndExistence | 5 | 2 | 7 |
| StrategyAndDirection | 6 | 1 | 7 |
| AgencyAndOrganization | 5 | 2 | 7 |
| PartyAndRelationship | 5 | 2 | 7 |
| ProductAndValue | 6 | 1 | 7 |
| EnablementAndOperations | 6 | 1 | 7 |
| FinanceAndAccounting | 5 | 2 | 7 |
| **Total** | **38** | **11** | **49** |

Coordinate-level entries live in `01_plan/research-register/l1-register.yaml`. The flattened L1 candidate universe lives in `01_plan/research-register/l1-candidate-universe.yaml` (102 L1 candidates across 49 coordinates). The persona-readable summary lives in `01_plan/research-register/REGISTER-v0.1.md`.

---

## 9. The Cross-Domain Findings

Five cross-domain findings are recorded alongside the disposition register.

### Finding C1: Technology Management

CAND-019 (dea-catalog-business-capabilities) is held unmapped per N-006 / R-004. Technology is an L5 layer concern, not an ECF domain. No ECF coordinate carries Technology Management. The 49-coordinate register does not include a Technology cell; process candidates touching technology declare their domain (enablement-operations x operate for runtime; strategy-direction x operate for build/asset) and a technology-bearing relationship. (CR-DEA-BC-04 R-004.)

### Finding C2: Change Management is cross-cutting

CR-DEA-BC-04 R-005: earliest legitimate initiation is governance-existence x improve. The 49-coordinate matrix lists Change Management as the cross-cutting pattern at governance-existence x improve and references it from peer coordinates that carry change-execution work (enablement-operations x improve, strategy-direction x build, party-relationship x improve, finance-and-value x improve). Not duplicated as separate L1 cells.

### Finding C3: Partner Management dual-home

CR-DEA-BC-04 R-001: Partner Management initiated at party-relationship x conceive (where partner engagement is initiated); supply-side operation is legitimate participation. Treated as one L1 candidate at party-relationship x conceive with a cross-reference to strategy-direction x operate for partner operations.

### Finding C4: Resilience, Innovation, Analytics

CR-DEA-BC-04 R-006, R-007, R-008 lifted three deferrals. Their process surfaces now sit under:

- governance-existence x improve for Resilience;
- product-value x conceive for Innovation;
- enablement-operations x operate for Analytics.

Recorded once at the primary coordinate; not duplicated.

### Finding C5: Marketing placement

CR-DEA-BC-04 N-002: Marketing is distinct from Customer Management. Customer-demand x conceive carries the Marketing candidate; party-relationship x operate carries the Customer Relationship Management candidate. Distinct L1 groups.

---

## 10. The L1 Group Identity Convention

Until CR-BP-12 lands, L1 Process Group names are recorded as `dea:group-<domain>-<stage>-<n>` placeholders. The live L1 record schema (BP-12) will formalize:

- `id`: `dea:group-<kebab-name>` (catalog-scoped ID family, not a metamodel entity);
- `type`: `ProcessGroup` (catalog-owned record type, not a metamodel entity);
- `profile`: `dea-catalog-processes/process-group/v1` (explicit catalog profile);
- `process_context`: the Process Context the group belongs to;
- `l0_scope`: the L0 scope beneath which the group sits;
- `definition`, `purpose`, `in_scope`, `out_of_scope`, `evidence`;
- `relationships[]`: `L1 group --composes--> L2 process` (canonical containment);
- `lifecycle_status`: `candidate` | `accepted` | `deprecated` | `retired`.

The L1 record is governed by the catalog, not by OpenDEA Core. Process Group promotion to OpenDEA Core is a separate CR (BP-14, future) requiring at least two independent downstream consumers.

---

## 11. The Containment Discipline

The canonical containment direction is `L1 group --composes--> L2 process`. The inverse `L2 --part-of--> L1` is a derived query view, not a second independent source of truth.

A temporary `parent_group_id` field MAY be added to L2 contributions and entities before the full relationship-graph admission; this is a migration bridge, not the final architecture. The L2 entry that already exists at `dea:process-manage-customer-relationship` carries a `metadata.group: dea:group-customer-lifecycle-management` label; BP-12 will promote that label to a governed record.

`part-of` is the inverse of `composes` per the metamodel relationship registry; the catalog SHALL NOT store `part-of` instances on L2 entries as a second membership source.

---

## 12. Process Group vs Business Function

Process Group and Business Function are distinct concepts:

- Process Group groups process responsibilities by a coherent process-architecture concern.
- Business Function groups capabilities by organizational function and ownership.

Both are catalog-topology constructs. Neither is a metamodel entity. They are not synonyms, not subtypes, not aliases. The catalog profile for Process Group MUST explicitly state this distinction.

The CR-DEA-BC-04 admitted capabilities sit under their declared organizational functions in the BC catalog. The L1 Process Group records in this catalog sit under Process Contexts in the ECF matrix. Where a Process Group and a Business Function share a name (e.g. "Financial Management"), the relationship is a `relates-to` reference, not an identity.

---

## 13. Conformance with Existing Gates

This CR ships no new validator, no new schema, no new entity directory, no new CI surface. It ships:

- the disposition register (research artefact);
- the L1 candidate universe (research artefact);
- a persona-readable Markdown twin;
- this CR document;
- a CHANGELOG entry.

The existing validators (process identity, process specialization, process context, legacy migration, ECF conformance, ECF drift detection) continue to apply unchanged to the existing L2 entry.

The dea-metamodel drift detector (`dea-metamodel/scripts/detect_drift.py`) requires no update: this CR adds no canonical `entities/v1-alpha/*.yaml` records. The first L1 governance schema and validator will land as CR-BP-12.

---

## 14. Deliverables

The following deliverables ship with this CR.

| Path | Type | Status |
|---|---|---|
| `change-requests/CR-BP-11-l1-process-group-discovery.md` | CR document (this file) | New |
| `docs/research/l1-register.yaml` | 49-coordinate disposition register (machine-readable) | New |
| `docs/research/l1-candidate-universe.yaml` | L1 candidate universe (machine-readable) | New |
| `docs/research/L1-REGISTER-v0.1.md` | Persona-readable summary | New |
| `change-requests/README.md` | Index row for CR-BP-11 | Updated |
| `README.md` | Status pointer | Updated |
| `CHANGELOG.md` | Entry for CR-BP-11 | Updated |

No canonical entity, no schema, no validator, no CI surface is added in this CR.

---

## 15. Acceptance Criteria

This CR is accepted when:

1. The 49-coordinate disposition register is present in `docs/research/l1-register.yaml`.
2. The L1 candidate universe is present in `docs/research/l1-candidate-universe.yaml` with 102 candidates across 49 coordinates and five cross-domain findings.
3. The persona-readable summary is present in `docs/research/L1-REGISTER-v0.1.md`.
4. The CR document is present in `change-requests/CR-BP-11-l1-process-group-discovery.md` and indexed in `change-requests/README.md`.
5. The CHANGELOG records the CR.
6. The existing local validators continue to pass (`check_process_identity.py`, `check_process_specialization.py`, `check_process_context.py`, `check_legacy_migration.py`, `check_ecf_conformance.py`).
7. The ECF drift detector reports zero new hard failures.
8. The dea-catalog-processes `main` branch state remains: 0 open PRs, 1 canonical L2 entry (`dea:process-manage-customer-relationship`), 1 Process Context (`dea:pc-pr-op`).

---

## 16. Consequences

### Positive

- The 49-coordinate matrix carries no manufactured content; 38 accepted coordinates are evidence-bound; 11 deferred coordinates carry explicit deferral reasons.
- The five cross-domain findings (Technology, Change, Partner, Resilience/Innovation/Analytics, Marketing) are recorded once and referenced from peer coordinates.
- L1 Process Group identity has a portable, evidence-bound candidate list ahead of the BP-12 governance schema.
- The existing L2 sample at `dea:process-manage-customer-relationship` remains the only canonical entity; no canonical expansion pressure in BP-11.
- The Process Group concept remains catalog-owned; metamodel contamination is avoided.
- The boundary discipline (MECE within Process Context, cross-domain patterns not duplicated) is established for BP-12 and BP-13.
- The audit trail is durable: CR, register, candidate universe, persona summary, locked picks log.

### Negative

- Two phases of work remain before any canonical L1 group exists: BP-12 (L1 record schema) and BP-13 (seven-domain admission tranches).
- The existing `metadata.group` label on the L2 sample remains ungoverned until BP-12.
- The `dea:bp-*` versus `dea:process-*` ID-family drift is still latent in the repo and will block BP-12 if not reconciled first; a separate CR-BP-04 reconciliation CR is required.
- External-framework evidence remains Tier 3 and is not authoritative; this is a deliberate restraint, but it lengthens the research register because each disposition must defend against foreign assumptions.
- Some L1 candidates (e.g. governance-existence x activate, agency-organization x activate, party-relationship x activate) carry weak or overlapping evidence and remain deferred; downstream work may revisit them.

### Forecloses

- Promotion of Process Group to OpenDEA Core until at least two independent downstream consumers require cross-repository identity.
- A wholesale rewrite of the existing entity.schema.json or contribution.schema.json in this CR.
- Authoring of the Process Group validator, the L1 entity directory, or the L1 governance schema in this CR.
- Bulk canonical population of L2 entries across the 49 coordinates.

---

## 17. Rejected Alternatives

### A : 49-cell L2 implementation PR

The naive approach is to write one L2 Business Process entry per coordinate, plus a L1 label per group, in one implementation PR.

Rejected because:

- it manufactures content with thin evidence and locks the matrix into a 49-process commitment the catalog cannot defend;
- it bypasses the CR-DEA-BC-04 admission gate discipline (evidence registers, normalization, deferrals);
- it skips the cross-domain-pattern recording (Technology, Change, Partner, Resilience/Innovation/Analytics, Marketing) that BC has already established;
- it overloads one PR with schema, contribution flow, validator, and CI surface changes that should be split.

### B : Direct promotion of Process Group to OpenDEA Core

Treat Process Group as a metamodel entity from day one, sibling to Business Capability and Business Function.

Rejected because:

- no independent downstream consumer requires cross-repository identity for Process Group;
- the metamodel currently carries no Process Group concept; adding it before evidence of independent semantics forces a CR in dea-metamodel and an explosion of consumers to migrate;
- CR-DEA-BC-04 has already shown the cost of orphan concepts at Core level;
- the catalog-owned alternative satisfies local referential integrity without metamodel contamination.

### C : Free-text L1 labels in L2 metadata

Keep L1 as a `metadata.group` label on each L2 entry, without a governed register.

Rejected because:

- no stable L1 identity;
- no MECE validation across groups;
- labels can drift: Customer Lifecycle vs Customer Management vs Customer Operations become ambiguous;
- removing a process does not affect the group;
- a later governed register would require parsing labels and migrating every affected L2 entry.

### D : Top-down population from external frameworks only

Use APQC, eTOM, BIAN, SCOR, or ITIL as the discovery authority for L1 groups.

Rejected because:

- external frameworks each carry their industry's blind spots;
- APQC describes its PCF as a customizable process taxonomy;
- TM Forum describes eTOM as a service-oriented framework; it is not a universal process architecture;
- BIAN describes its Service Landscape as a reference structure for banking service domains; it is not a universal process architecture;
- OpenDEA ECF and existing OpenDEA catalogs retain semantic authority per the user's evidence-policy selection.

### E : Skip the 49-coordinate coverage check entirely

Proceed directly to BP-12 (L1 governance schema) using only the existing L2 sample and the CR-BP-03 hierarchy definitions.

Rejected because:

- it accepts one sample as the entire evidence base;
- it does not surface the cross-domain patterns (Technology, Change, Partner, Resilience/Innovation/Analytics, Marketing) that BC has already discovered;
- it cannot defend a deferred-vs-accepted boundary on cells the catalog has never examined.

### F : Treat Process Group as a synonym for Business Function

Collapse Process Group into Business Function and adopt the BC catalog's organizational grouping.

Rejected because:

- Process Group groups process responsibilities by process-architecture concern;
- Business Function groups capabilities by organizational function and ownership;
- they are not synonyms, not subtypes, not aliases;
- collapsing them violates the ea-concept-classification MECE test and would force every Process Group to take on an organizational-ownership dimension it does not have.

---

## 18. Explicit Non-Decisions

This CR does NOT decide:

- the governance schema for L1 Process Group records (BP-12);
- the validator for L1 group composition and MECE (BP-12);
- the catalog-owned Process Group profile registry (BP-12);
- the L2 admission waves for the seven domains (BP-13+);
- the ID-family reconciliation between `dea:bp-*` and `dea:process-*` (CR-BP-04, separate);
- the promotion of Process Group to OpenDEA Core (BP-14, future, conditional);
- the boundary semantics between Process Group and Business Function beyond the explicit statement in section 12;
- the staging of any external framework as canonical authority;
- the runtime, viewer, or federation mapping of Process Group beyond what is implicit in the catalog profile.

---

## 19. Required Follow-On CRs

- CR-BP-04 (ID-family reconciliation): resolve `dea:bp-*` versus `dea:process-*` drift before BP-12 lands.
- CR-BP-12 (L1 Process Group profile + schema + validator): catalog-owned records, MECE validation, contribution flow.
- CR-BP-13 (Domain admission tranche 1 of 7): GovernanceAndExistence.
- CR-BP-14..BP-19 (Domain admission tranches 2..7): StrategyAndDirection, AgencyAndOrganization, PartyAndRelationship, ProductAndValue, EnablementAndOperations, FinanceAndAccounting.
- CR-BP-20 (conditional): promotion of Process Group to OpenDEA Core if two independent downstream consumers require it.

The chain closes at BP-19 under the current scoping; BP-20 is conditional and not part of the locked tranche.

---

*Status: Baseline. Parent: CR-BP-03-business-process-architecture. Implementation: research register only; no canonical entities in this CR.*