# CR-BP-239: ECF Catalogue Publication Asset Suite

**Status**: Proposed
**Layer**: Cross-cutting
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-26
**Depends on**: CR-BP-238 (canonical inventory and lifecycle reconciliation), CR-BP-30/30a..30h (release package), CR-BP-116 (release discipline), CR-BP-94-EXT-08..24 (documentation and operational governance), CR-ECF-CG-004 (ECF conformance), dea-metaframework v2.7.0 (`tools/ecf_coordinates.py`)

> **Scope.** Establish one verified, versioned publication model from which the ECF process-map poster, self-contained HTML catalogue, machine-readable JSON export and enriched Excel workbook are generated. The assets shall accompany every eligible catalogue release and publication. This CR evolves the existing `scripts/generate_entity_map.py` renderer; it does not create a competing interpretation of ECF coordinates or redefine canonical process semantics.

---

## 1. Executive decision

The catalogue shall publish one coherent representation of its canonical process architecture in four complementary forms:

1. **Poster** — a high-quality, print-ready ECF 7×7 map for executive, architecture and operational use.
2. **HTML** — a self-contained, offline-capable catalogue browser with search, filtering, hierarchy navigation and rich entity detail.
3. **JSON** — a versioned, machine-readable publication model suitable for integrations, analysis and agent consumption.
4. **Excel** — an enriched, navigable workbook for business analysis, architecture assessment, operational design and controlled reuse.

All four formats shall be rendered from one canonical publication model generated from the same tagged source commit. No renderer may independently reinterpret entity hierarchy, ECF coordinates, lifecycle state or process semantics.

The publication model is a derived view, not a new source of truth. Canonical entity records remain authoritative.

## 2. Existing implementation and findings

### 2.1 Existing renderers

- `scripts/generate_process_map.py` is the original CR-BP-30a L0-L2 matrix renderer. It provides a basic HTML grid and optional A3 PNG conversion.
- `scripts/generate_entity_map.py` is the advanced renderer and the implementation foundation for this CR. It supports L0-L1 and L0-L2 poster depths, PDF/PNG rasterisation, placement auditing, and per-cell L2-L4 drill-down pages.
- `scripts/build_catalog_xlsx.py` produces the existing six-sheet workbook.
- `scripts/build_manifest.py` records generated artefact hashes and generator provenance.

### 2.2 Gaps to resolve

1. The advanced map derives ECF position from entity parent references, correctly avoiding an unsupported `ecf.primary` field, but its domain ordering is alphabetical rather than the normative ECF order.
2. Duplicate entity IDs are collapsed by dictionary construction in the map assembly path; duplicate coordinates and duplicate placements need explicit findings rather than silent merging.
3. The current poster is a compact overview. It does not provide a complete business-process publication experience.
4. The drill-down pages expose names, IDs, intent and process type, but omit the rich description, definition, example uses, trigger, outcomes, inputs, outputs, responsibility, controls and provenance already held by the entity records.
5. The map's generated-at wall-clock timestamp makes output vary between executions, contrary to the release package's deterministic-build contract.
6. The existing map and workbook read the entity tree independently. They can therefore drift in field coverage, filtering or counts.
7. The existing workbook is a six-sheet governance-oriented workbook, not a complete operationally useful catalogue workbook. It does not provide a dedicated, consistently structured view of all L0-L4 entity details and I/O declarations.
8. The release package currently lacks a canonical JSON publication model and an explicit schema for that model.
9. Release-package validation does not yet assert that the poster, HTML, JSON and workbook represent the same model digest and entity population.

These are publication-tooling gaps. They do not invalidate the canonical entity records or justify speculative enrichment.

## 3. Normative publication model

### 3.1 Source and authority

The publication builder shall consume:

- canonical entity records under `entities/v1-alpha/`;
- the current commit-addressed inventory baseline and lifecycle/ownership registers;
- the canonical ECF domain and lifecycle-stage ordering contract;
- the versioned dependency and schema/profile pins required to interpret the records.

The builder shall not infer missing entity content from names, directory structure, adjacent records or generic process patterns. Missing values remain explicitly absent and are surfaced as data-quality information.

### 3.2 Model structure

The versioned JSON model shall include:

- release and source provenance: catalogue version, source commit, ECF contract version, metamodel pin, schema/profile pins, build-tool version and model digest;
- inventory totals by L0-L4, lifecycle state, ECF domain and lifecycle stage;
- all 49 ECF cells with their L0 Process Context, L1 Process Group, L2 Business Processes and descendant L3 Activities and L4 Tasks;
- canonical IDs, names, definitions, descriptions and versions;
- process intent, specialization, classification, purpose, trigger, preconditions, outcomes and scope;
- inputs and outputs, preserving item names, descriptions, types, references and evidence where present;
- responsibility, accountability, owner, actors and stakeholders where declared;
- business rules, controls, exceptions, measures and evidence/provenance where declared;
- explicit parent/child and other supported relationships;
- lifecycle state and governed disposition;
- source file paths and field-level source provenance;
- data-quality coverage indicators, with absent fields distinguished from empty-but-declared fields.

The JSON Schema shall be versioned independently from the catalogue release version and validated in CI.

### 3.3 Identity and ECF placement

- ECF cell placement is resolved from canonical references and the L0 Process Context's `domain` and `lifecycle_stage`.
- L1 placement resolves through `process_context` to its L0 Process Context.
- L1-to-L2 containment resolves from the L1 Process Group's canonical `composes[]` assertions (source = L1 group, target = L2 process). Do not infer this relationship from directory nesting or from the L2 `context[]` field.
- Each L2 process independently resolves its ECF cell through `context[].ref` to the L0 Process Context. The resolved L0 context must agree with the L0 context of every asserted L1 parent. Missing, multiple or conflicting group compositions are explicit findings.
- L3 containment resolves through `belongs_to_business_process`; L4 containment resolves through `belongs_to_activity`.
- The model shall preserve each asserted relationship and its resolution status. The publication builder shall distinguish the L2-to-L0 context reference from the L1-to-L2 composition relationship; they are complementary assertions, not interchangeable parent fields.
- A record with missing, ambiguous or invalid placement is reported; it is never silently assigned by path or name.
- Domain and stage order shall be taken from the ECF contract, not alphabetical sorting or an independently maintained renderer-specific order.
- For the current pinned ECF contract in dea-metaframework v2.7.0, the domain-major order is: Governance & Existence; Strategy & Direction; Agency & Organization; Party & Relationship; Product & Value; Enablement & Operations; Finance & Accounting. The stage-minor order is: Conceive; Design; Build; Activate; Operate; Improve; Retire. The renderer shall import or verify against `tools/ecf_coordinates.py` rather than re-declare these arrays independently.
- Canonical identities must be unique. Duplicate IDs, multiple cell placements, orphaned children and unexpected ECF coordinates are publication-blocking findings.

## 4. Publication asset requirements

### 4.1 Poster

Produce a designed, print-ready ECF 7×7 poster with:

- all 49 cells in normative ECF order;
- clear domain and lifecycle-stage axes;
- L0 Process Context and L1 Process Group names;
- L2 Business Process names and cell-level counts;
- a legible hierarchy and typographic scale, restrained colour system and deliberate whitespace;
- catalogue/release version, source commit, ECF contract version, population counts and generation provenance;
- a compact legend and explicit statement of the levels shown;
- accessible contrast and legibility at the selected print size.

The poster shall be delivered as PDF and PNG. A1 landscape is the preferred initial target for the L0-L2 view carrying all 145 L2 names; A2 may be selected only if measured print tests demonstrate equivalent legibility. Never shrink content to force a nominal page size. The release gate shall verify that the poster is a single intended poster page and that the PNG is rasterised from that same PDF.

The poster is an overview, not a substitute for the detailed catalogue. It shall not attempt to print all L3/L4 descriptions or all I/O content.

### 4.2 Self-contained HTML catalogue

The HTML edition shall work locally without network access or external runtime dependencies. It shall embed the publication JSON and provide:

- ECF matrix overview and navigation;
- search by entity name, canonical ID and supported semantic terms;
- filters by ECF domain, lifecycle stage, level, intent, specialization, classification and lifecycle state;
- drill-down from L0 to L4 and navigable parent/child relationships;
- rich detail panels for formal and plain-language definitions/descriptions, business purpose, practical context, worked examples, triggers, outcomes, scope, inputs, outputs, responsibility, accountability, rules, controls, exceptions and provenance;
- clear display of unavailable or undeclared fields, rather than fabricated examples;
- summary counts and data-quality coverage indicators;
- print styles for the overview and individual entity details;
- keyboard-accessible controls and semantic HTML.

The HTML must not load JavaScript, fonts, stylesheets, images or data from a CDN or remote host.

### 4.3 JSON publication model

Deliver a standalone JSON file and its JSON Schema. The JSON shall be:

- deterministic and stable in key/array ordering;
- UTF-8, human-readable and valid against the versioned schema;
- explicit about null, empty, not-declared and not-applicable distinctions where the source contract supports them;
- self-describing through schema version, catalogue version, source commit and dependency pins;
- complete for the canonical publication scope, without embedding research or candidate artefacts as canonical entities.

### 4.4 Excel workbook

Deliver an enriched workbook with filters, freeze panes, wrapped text, sensible column widths, hyperlinks for canonical IDs and source paths, structured tables and print settings.

Minimum worksheet family:

1. **Overview** — release metadata, inventory counts, ECF coverage and data-quality summary.
2. **ECF Matrix** — 49 cells, their L0/L1 structure, L2 counts and cell-level navigation.
3. **L0 Contexts** — all Process Context records and charter fields.
4. **L1 Groups** — all Process Group records and composition/ownership information.
5. **L2 Processes** — complete business-process identity, purpose, intent, specialization, classification, definition, description, example use, trigger, outcomes, scope, responsibility, accountability and lifecycle metadata.
6. **L3 Activities** — activity definitions, descriptions, parent process and declared inputs/outputs.
7. **L4 Tasks** — task definitions, descriptions, parent activity and declared inputs/outputs.
8. **Inputs** — normalized input declarations with owning entity and source references.
9. **Outputs** — normalized output declarations with owning entity and source references.
10. **Rules and Controls** — business rules, controls, exceptions and applicable entity links.
11. **Relationships** — canonical hierarchy and other supported relationship assertions.
12. **Evidence and Provenance** — provenance, source paths, review and evidence references.
13. **Taxonomy and Reference** — controlled values and interpretation notes used by the publication model.

Additional sheets may be included where they improve analysis, but the workbook shall not duplicate conflicting entity facts across independently authored data sources.

## 5. Shared model and rendering architecture

The target pipeline is:

```text
Canonical entity records + governed registers + ECF contract
                         |
                         v
             Inventory and integrity gate
                         |
                         v
              Canonical publication model
                         |
             +-----------+-----------+-----------+
             |           |           |           |
             v           v           v           v
           Poster      HTML        JSON        Excel
             |           |           |           |
             +-----------+-----------+-----------+
                         |
                         v
              Release manifest + hashes
                         |
                         v
             Versioned release publication
```

The publication model is the single semantic input to all renderers. The poster, HTML and workbook may have different presentation structures, but their identities, counts, ECF coordinates and source content must agree with the JSON model.

## 6. Release package contract

Every eligible release package shall include:

- `process-catalogue-poster.pdf`
- `process-catalogue-poster.png`
- `process-catalogue.html`
- `process-catalogue.json`
- `process-catalogue.schema.json`
- `process-catalogue.xlsx`
- existing BPMN library, curated release notes, decisions/dispositions, canonical source snapshot and MANIFEST.

The legacy `process-map.html`, `process-map-a3.png` and `catalog.xlsx` names may be retained as compatibility aliases for one transition release, but they must point to the same generated artefacts and must not be independently rendered.

All files must identify the same release version, source commit and publication-model digest. MANIFEST shall record each asset's byte length, SHA-256, generator and model digest. The release ZIP shall be reproducible, including normalized entry ordering, timestamps and permissions.

The publication assets shall be attached to the GitHub Release and included in the downloadable versioned package. Repository publication pages may link to the same versioned assets but must not regenerate a second, divergent view.

## 7. Implementation slices

### Slice A — Publication model and schema

- Define the publication-model JSON Schema and versioning policy.
- Implement a deterministic builder that consumes canonical records and governed registers.
- Resolve hierarchy and ECF placement with explicit findings.
- Preserve rich source fields and field-level provenance.
- Add tests for completeness, relationships, duplicates, invalid placement, field fidelity, deterministic ordering and schema validation.
- Generate a small fixture model for renderer tests.

### Slice B — Poster and HTML publication

- Refactor `generate_entity_map.py` into a renderer over the shared publication model.
- Apply normative ECF domain/stage ordering.
- Correct duplicate/placement audit weaknesses and remove wall-clock output from deterministic artefacts.
- Produce the print-ready poster PDF/PNG.
- Build the self-contained interactive HTML catalogue with rich entity details and offline operation.
- Retain the current overview/drill-down concepts where they improve usability, but remove duplicated source interpretation.

### Slice C — Enriched Excel publication

- Replace the six-sheet-only consumer view with the minimum worksheet family in §4.4 while retaining useful governance sheets.
- Read exclusively from the shared publication model.
- Add navigability, filters, readable layouts, cell formats, print areas and deterministic workbook metadata.
- Validate sheet names, row counts, links, I/O fidelity and workbook determinism.

### Slice D — Release integration and publication

- Integrate all four formats into the CR-BP-30 release pipeline.
- Include schema and model digest in the release manifest.
- Verify cross-format counts and source-commit consistency.
- Upload all publication assets to the GitHub Release and versioned archive.
- Preserve the current v0.5.0 release as immutable history.
- Require the CR-BP-238 inventory gate to pass before rendering and publication.

### Slice E — Documentation, adoption and deprecation

- Document asset purposes, audiences, navigation and offline use.
- Publish examples and a reproducible local build command.
- Retire the superseded independent map-generation path only after all compatibility and release tests pass.
- Record deprecation and migration in CHANGELOG and release notes.

## 8. Acceptance criteria

1. One publication model and one source commit drive all four asset families.
2. All 49 ECF cells appear in normative order, with no missing or duplicated coordinate.
3. All 3,723 canonical records in the current reconciled baseline are accounted for by level and lifecycle state.
4. Every canonical L2 process and all its declared L3/L4 descendants are navigable in HTML and represented in JSON and Excel.
5. L2 formal and plain-language descriptions, business purpose, practical context, worked examples, inputs and outputs are carried through from source records without invention or silent truncation.
6. All absent or undeclared information is visibly distinguished from empty or not-applicable values.
7. HTML works offline with network access disabled.
8. PDF is one intentional poster page at its declared print size; PNG is rendered from that PDF.
9. Workbook sheets, rows, filters, hyperlinks, detail fields and I/O declarations reconcile to JSON.
10. JSON validates against the published schema.
11. Model and artifact generation is deterministic; repeated builds from the same commit produce byte-identical JSON, HTML, XLSX, PDF and normalized release archive. If a rendering library makes PNG bytes platform-sensitive, the rasterizer and container image are pinned and the policy is explicit.
12. CI blocks publication on missing entities, duplicate IDs, unresolved hierarchy, invalid ECF placement, schema failure, model digest mismatch or cross-format count drift.
13. Every release contains the complete publication asset family and a manifest with hashes and provenance.

## 9. Governance boundaries

- No canonical entity semantics, IDs, or ECF coordinate assertions are changed merely to improve presentation.
- No examples, I/O, definitions or responsibilities are fabricated to fill gaps.
- Publication-only enrichment is not written back to canonical entity records.
- The publication model is derived and versioned; it does not supersede the entity catalog.
- Any semantic source change remains subject to its own scoped CR and applicable upstream contracts.
- The first complete publication release shall be cut only after CR-BP-238 inventory reconciliation and strict conformance are established.
