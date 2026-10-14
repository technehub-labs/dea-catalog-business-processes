# Entity System Charter

> **Stage 1 output 1 of CR-BP-121 (renumbered from CR-BP-16).**
> The normative scope, principles, authority boundaries, and applicability of the General Entity System for `dea-catalog-business-processes`.
> Foundation: [DEA-ID-000](../../../../dea-governance/docs/design/entity-system-foundation.md).
> Normative standard: [CR-012](../../../../dea-governance/change-requests/CR-012-org-wide-entity-governance.md).

## 1. Purpose

This charter establishes the General Entity System as a first-class architectural concern for `dea-catalog-business-processes`. The entity system governs how every record in this catalog is **identified, typed, related, evolved, and validated** over time, independent of any particular catalog version or directory layout.

The catalog's existing structure (`entities/v1-alpha/`, `contexts/v1-alpha/`, the `processes-` / `dea:` id prefixes, the L0-L4 decomposition, the 49-cell ECF matrix, the Process Context / Process Group / Business Process / Activity / Task hierarchy) remains in place. The entity system is the governance layer that makes that structure durable, governable, and reusable across the `technehub-labs/*` portfolio.

## 2. Applicability

The General Entity System applies to:

- All entity records in `entities/v1-alpha/**`, `contexts/v1-alpha/**`, and any future `entities/<version>/` directories.
- All change requests in `change-requests/CR-*.md` whose body or header carries an entity-affecting change.
- All governance documents in `docs/governance/`, `docs/architecture/`, `docs/identity/`, `docs/identity.md`, `docs/classification.md`, `docs/relandscape.md`, and `docs/conformance.md`.
- The conformance pipeline (`scripts/conformance_result.py`, every gate listed therein, every CI workflow in `.github/workflows/`).
- The cross-repo references (ECF coordinates; cross-catalog `relationships[]` entries; the `metamodel-pointer.yaml`).
- Future catalog versions (`entities/v2-alpha/`, etc.) introduced through approved CRs.

The entity system does NOT apply to:

- Vendored content (e.g. `.metaframework/` from CI's checkout of `dea-metaframework`).
- The 01_plan/ directory (tranche planning documents; pre-decisional).
- Generated content (e.g. `reconciliation/conformance_report.yaml`; regenerated each gate run).
- Reconciliation and migration tooling (these are governed by their own change requests).

## 3. Authority boundaries (per DEA-ID-000 §2)

```
OpenDEAM Architecture Framework   (dea-architecture-framework)
  └─ Architectural authority: ADRs that resolve architecture-level conflicts
                                 (e.g. ADR-0001 governance, ADR-0004 v0.4.0 cleanup,
                                  ADR-0006 process-kernel specialisation)

ECF (dea-metaframework) + Canonical Metamodel (dea-metamodel)
  └─ Conceptual grounding, entity types, properties, relationships
      (e.g. dea:BusinessProcess, dea:ProcessContext, dea:ProcessGroup,
       dea:Activity, dea:Task specialisations on the dea:entity-process kernel)

General Entity System (dea-governance)
  └─ Identity, lifecycle, schemas, references, governance, conformance
      (EGV-001..012 in CR-012; this charter's subject)

Business Process Catalog (dea-catalog-processes; THIS REPO)
  └─ Process-specific profiles and instances
      (3,882 canonical records as of 2026-10-13)
```

`dea-catalog-processes` may define a business-process profile but must not redefine the canonical `BusinessProcess` concept. The catalog may choose its storage format and local file organisation within approved constraints, but must not create its own competing identity semantics.

## 4. Architectural principles

The General Entity System in this catalog is designed according to the principles in DEA-ID-000 §4 and CR-012 §3 (EGV-001..012). The five concerns of the system:

1. **Entity identity** (EGV-002..004): stable, persistent, scope-bound; not derived from mutable attributes; no silent reassignment.
2. **Entity semantics** (EGV-005): canonical type, definition, semantic constraints, specialisation, and authoritative metamodel references.
3. **Entity relationships** (EGV-006): typed references, composition, specialisation, realisation, dependency, association.
4. **Entity lifecycle** (EGV-007, EGV-011): admission, modification, reclassification, supersession, retirement, provenance.
5. **Entity conformance** (EGV-010, EGV-011): schema validation, semantic validation, naming rules, reference checks, change control, CI enforcement.

These five concerns are the governance discipline. The catalog's existing gates (ADM, BP-C, BP-SEM, BP-SPEC, BP-AR, MECE, ECF, IDM, HREF, TPL, CRR, RDM, EMB, DOC, EID, AUT) implement specific aspects of the discipline; the General Entity System is the umbrella that ties them together with explicit identity, lifecycle, and conformance rules.

## 5. Existing decisions retained

The following existing decisions in `dea-catalog-processes` are already aligned with the General Entity System and remain in force:

- **IDM-001..008** (id-system coherence; CR-BP-mv1): the `processes:<token>-<descriptor>-<base32hash>` format; the BASE32 strict alphabet (IDM-004); filename + cell segment + depth validation (IDM-005); cross-version migration via `reconciliation/migration-id-map.yaml`; admission-authority marker mechanism (CR-BP-115); cross-repo coherence gate (IDM-008).
- **CR-BP-04** (id-family reconciliation): the four canonical ID families (`dea:process-*`, `dea:pc-*`, `dea:group-*`, `dea:scope-*`) and the legacy `dea:bp:*` migration.
- **CR-BP-117a..c** (entity-identity clarity; folder/path clarity): EID-001..004 diagnostic gates; the human-readable directory rename; the path-scheme documentation.
- **CR-BP-31** (ECF conformance): the ECF block on PG and BP records; the `framework: EnterpriseConceptFramework` canonical shape.
- **CR-BP-115** (admission-authority marker): data-driven admission authority; the `**Admission authority**: yes` marker line in CR files.
- **CR-BP-118a/b/c** (authorship cardinal rule): the `**Owner**` / `**Author**` / `audit.author` / `authors[].name` / `name` / `definition` / `description` / `summary` allowlist + denylist; the per-repo authorship gate; the prose-field gate with the `Agent` allowlist.
- **CR-BP-112** (EMB reference embargo): the `check_reference_embargo.py` gate; the allowlist registry.
- **CR-BP-114** (README regeneration): the generator + repair + drift gate triad.
- **The 49-cell ECF matrix** (7 domains x 7 lifecycle stages): the canonical decomposition that gives the catalog its cardinal structure.

## 6. Identified gaps

The following decisions are MISSING from the current catalog state and must be made (Stage 2 outputs):

- **G-01 Identity standard**: an explicit identifier format policy. The current `processes:<token>-<descriptor>-<base32hash>` is enforced by IDM-001..008 but not documented as a normative standard. The format must be ratified under EGV-002..003.
- **G-02 Entity contract standard**: the common entity envelope (id, type, name, definition, description, relationships, classifications, provenance, lifecycle). Currently the entity schema is per-record-type; a common envelope is not codified.
- **G-03 Relationship standard**: the typed-relationship vocabulary. The metamodel defines the abstract relationships (`composes`, `realises`, etc.); the catalog needs a documented relationship-inventory that ties metamodel types to catalog instances.
- **G-04 Lifecycle standard**: the explicit admission / modification / reclassification / supersession / retirement transition rules. The admission gate (ADM) and the recovery register exist, but the lifecycle state machine is not codified.
- **G-05 Conformance standard**: the entity-system gate itself. Today's gates are component-level (one per concern); the entity system needs an umbrella gate that asserts all five concerns hold for every record.
- **G-06 Cross-catalog reference standard**: how the catalog's `relationships[]` entries that point at other catalogs (e.g. to `dea-catalog-business-capabilities`) resolve. The metamodel-pointer.yaml is a single catalog-level reference; per-record cross-catalog resolution is not codified.
- **G-07 Legacy ID reconciliation**: per EGV-012, the existing 35 `dea:` legacy tail in `entities/v1-alpha/` (post-mv1 migration) needs a documented disposition register.

## 7. Cross-cutting alignment

The General Entity System in this catalog aligns with:

- **DEA-ID-000** (foundation paper): the 5-concern taxonomy, the authority model, the 7-workstream taxonomy, the 4-phase adoption programme.
- **CR-012** (org-wide governance CR): the 12 EGV-001..012 normative requirements; the 8 deliverables; the 6 implementation stages.
- **CR-BP-16 / CR-BP-121** (this CR): the 6-stage pilot implementation in this catalog.
- **ADR-0001** (OpenDEAM governance): the OpenDEAM root model authority; the 6-layer ecosystem-on-top model.
- **ADR-0004** (v0.4.0 cleanup): the L2 cleanup + vocabulary purge; the catalog version discipline.
- **ADR-0006** (process-kernel + specialisation): the kernel + specialisation discipline that CR-BP-SPEC-BP-01 codifies for the catalog.

## 8. Charter adoption

This charter is adopted when:

1. The carrier CR (CR-BP-121) lands on `main`.
2. The Stage 1 outputs (this charter + the Existing Decisions and Gap Register + the Normative Design Proposal + the Implementation and Adoption Plan) are referenced from `change-requests/README.md`.
3. The Entity System Charter is referenced from `docs/governance/`.
4. Stage 2 (Specification and Approval) is opened as CR-BP-122 with a 5-spec deliverables scope.

Until then, the charter is provisional; the existing gate roster remains the source of truth for entity conformance.
