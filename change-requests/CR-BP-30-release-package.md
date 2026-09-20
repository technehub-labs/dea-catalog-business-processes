# CR-BP-30: Release Package for `dea-catalog-processes`

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Proposed (carrier CR — discussion + design-decision lock; **awaiting user input on §3 decisions**)
**Layer**: Process Catalog (release / governance)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-10
**Depends on**: `v0.2.0` snapshot on `main` (CR-BP-29, PR #66 MERGED, commit `903e3b3`); CR-BP-31 migration-pair closure (PR #67 MERGED, commit `991faa3`); `generate_capability_map.py` (proven pattern in `dea-catalog-business-capabilities`); the canonical YAML substrate in `entities/v1-alpha/`
**Related**: CR-DEA-BC-05 (versioning discipline), CR-DEA-BC-11 (release-pipeline consolidation in the BC catalog); CR-BP-03C (contribution flow); CR-BP-15-IMP Phase 3 (disposition register); CR-BP-16 (conformance gate, 196/196 at L4); `docs/versioning.md`

---

## 0. Decisions requested at merge time (TL;DR)

This CR documents the full artifact family + CI shape (§1–§7). Before approval, **six decisions** need to be locked. Each is presented below with the **recommended default**; the user can override any of them inline in the merge conversation.

| # | Decision | Recommended | Why this default |
|---|---|---|---|
| D1 | §3.1 Map shape | **A** (ECF 7×7 grid overlay) | ECF is the federation's navigational idiom; BC catalog already uses this pattern. |
| D2 | §3.2 XLSX sheet count | **6 sheets** (records / lineage / dispositions / register_audit / change_requests / contributions) | Flat view + sidecar graph + audit axes; aligns with the "versions of processes" column on Sheet 1. |
| D3 | §3.3 BPMN shape | **A** (seed library: `bpmn-library.bpmn` with one diagram per BP) | Zero-install; works in every BPMN 2.0 reader; modelers clone-and-extend. |
| D4 | §3.4 Decisions log | **A** (curated `decisions.md` + verbatim `dispositions/` folder) | Reader-friendly narrative + raw data preserved; matches BC's release-notes pattern. |
| D5 | §3.5 `dependencies.yaml` adoption | **Adopt now** | Proven BC pattern; lets federation consumers pin to a specific artifact version. |
| D6 | §3.6 Artifact version independence | **A** (lockstep — every tag = full zip) | Simpler governance; BC uses the same shape; we can split later if a real consumer asks. |

**Decision syntax** (inline in the merge message):
- `Approve all defaults` (or simply `Merge`) → locks D1–D6 as recommended.
- `Approve all defaults except D3 = B` (etc.) → overrides one or more.

Full discussion follows in §1–§7.

---

## 1. Why a release package (the "why" before the "what")

`dea-catalog-processes` is an **L1 governance catalog** in the OpenDEAM federation. The canonical product is a substrate-neutral, machine-checked vocabulary of 196 records (Process Contexts, Process Groups, Business Processes) under the ECF 7×7 matrix, with conformance at L4 and zero blocking findings.

The two tagged releases to date (`v0.1.0` and the paperwork-only `v0.2.0`) deliver **metadata only**: the YAML substrate, the CHANGELOG, and `CITATION.cff`. That works for federation tooling that already parses YAML and reads the metamodel contract. It does NOT serve four practical consumer surfaces that real downstream work needs:

| Consumer surface | Today's gap | Why it matters |
|---|---|---|
| Human stakeholder / architect | No visual map. A stakeholder cannot "see" the 196 records without reading 196 YAML files or running tooling locally. | Adoption gates — a catalog that cannot be *seen* does not get adopted by the people who would use it. |
| Data / landscape analyst | No structured spreadsheet. The dispositions, lineage edges, register audit, and CR index live across five separate files (`reconciliation/dispositions/register.yaml`, `entities/.../*.yaml`, `change-requests/*.md`, `reconciliation/conformance_report.yaml`, `reconciliation/inventory.yaml`). | Any landscape analysis (e.g. "show me every L2 process that crossed a Domain boundary in v2.4.0") requires manual collation. |
| Process modeler (BPMN-side) | No BPMN-consumable artifact. A modeler using bpmn.io / Camunda / Signavio cannot import the catalog as a starting palette or as a seed library. | Integration cost — every modeling team would re-key the catalog by hand. |
| Auditor / archivist | No "decisions log" surface. The evidence and votes that produced each disposition (CR-BP-15-IMP Phase 3) live across `reconciliation/dispositions/register.yaml`, `reconciliation/inventory.yaml`, `change-requests/`, and per-CR provenance blocks. | Governance transparency — a release without provenance is a black box to the next reviewer. |

The release package is the bridge from **machine-checked governance artifact** to **consumable artifact family for humans and downstream tooling**. The BC catalog proved the pattern with `capability-map.html` + `capability-map-a3.png` + release zip; the process catalog needs the same pattern **plus the three additional surfaces** (XLSX, BPMN plugin, decisions log) that the BC catalog does not ship.

**What this CR is NOT.** This CR is not "ship artifacts." It is **the discussion document that defines the artifact family, the per-artifact responsibility, and the CI shape required to produce them on tag push.** Implementation CRs (CR-BP-30a, 30b, ...) follow after this one is approved, each with its own PR.

---

## 2. The artifact family (the "what")

The release package is a single zip produced at tag-push time by a new `publish-versioned.yml` workflow. The zip contains **one canonical artifact per consumer surface** (Section 1). The package is the zip; the artifacts inside it are the consumer surfaces.

| # | Artifact | File | Purpose | Provenance / source on disk |
|---|---|---|---|---|
| 1 | **Process map (HTML)** | `process-map.html` | L0 ⊃ L1 ⊃ L2 CSS-grid map of the catalog on the ECF 7×7 matrix, with cells = Process Contexts and overlay ribbons for Process Groups and Business Processes | Adapted from BC's `generate_capability_map.py` (framework Python) |
| 2 | **Process map (PNG)** | `process-map-a3.png` | A3 landscape @ 300 DPI raster of the same | Rendered via `weasyprint` (HTML→PDF) + `pdftoppm` (PDF→PNG), same as BC |
| 3 | **Structured Excel workbook** | `catalog.xlsx` | Multi-sheet XLSX for landscape analysis (see §3) | New `scripts/build_catalog_xlsx.py` |
| 4 | **BPMN-consumable artifact** | `bpmn-plugin/` (folder) or `bpmn-library.bpmn` (file) — see §4 | Catalog as BPMN palette entries (plugin) OR as a BPMN 2.0 XML seed library | New `scripts/build_bpmn_artifact.py` |
| 5 | **Contributions folder** | `contributions/` (folder) | Verbatim export of `contributions/processes/` from the tagged commit, including the per-entry `.report.md` reclassification reports | Direct copy from `contributions/processes/` |
| 6 | **Decisions log** | `decisions.md` + `dispositions/` (folder) | Curated decisions surface: per-record dispositions, register audit, CR index, per-CR evidence and provenance | Aggregated from `reconciliation/`, `change-requests/`, `entities/.../change_history` |
| 7 | **Release note** | `RELEASE-NOTES.md` | Human-readable narrative of what landed in this tag (CRs, register audit, conformance, evidence) | Generated from CHANGELOG + CR-BP index |
| 8 | **Manifest** | `MANIFEST.md` | Per-file: source path on disk, generation script + commit SHA, schema/version, bytes, sha256 | Generated by the workflow |
| 9 | **YAML substrate** | `entities/**/*.yaml` (folder) | The canonical catalog verbatim (so the zip is self-contained — a consumer who downloaded only the zip has the full source) | Direct copy from `entities/v1-alpha/` |

**Self-contained principle.** The zip must be **complete** — a consumer who downloads only the zip and discards the repo must still be able to (a) render the map (HTML+PNG), (b) load the data (XLSX+YAML), (c) understand the decisions (`decisions.md` + `dispositions/`), and (d) audit provenance (`MANIFEST.md` + per-file SHA256).

**Provenance principle.** Every artifact in the zip carries a generation footer with: source path on disk, generating script + its commit SHA, schema version, and a per-file SHA256 in `MANIFEST.md`. This makes the zip self-auditable without external context.

---

## 3. Design decisions needing your input (the "decide before building")

These are not implementation details. They shape the artifact family and should be resolved before any code lands. Each has a default leaning; please confirm or redirect.

### 3.1 Map shape — ECF-grid-overlay vs hierarchical tree

**Option A (lean: this one).** Render the ECF 7×7 matrix as the primary surface. Each cell = one Process Context (35 visible cells; 14 backlog-deferred cells rendered greyed-out with a `backlog-deferred` badge). Each non-empty cell overlays its Process Groups as ribbons (one ribbon per Group, vertically stacked within the cell), and each Group lists its L2 Business Processes as sub-rows. Hover/click reveals evidence and dispositions.

- Pro: ECF is the navigational idiom the federation speaks; the 7×7 grid is already the lingua franca across the seven catalog repos.
- Pro: Maps naturally to the L0 ⊃ L1 ⊃ L2 CSS-grid pattern BC already proves.
- Con: 14 backlog-deferred cells is non-trivial visual noise; needs a clear legend.

**Option B.** Render a hierarchical Process-Group tree with ECF coordinates as a sideband. Each Process Group is a node; L2 Business Processes are leaves; the ECF coordinate is a small badge on each node.

- Pro: Easier to read for someone unfamiliar with the 7×7 matrix.
- Con: Hides the orthogonality property (Domain ⊥ Lifecycle Stage) that the ECF is built around; consumers must learn it again.

**Decision needed:** A or B?

### 3.2 Excel workbook structure — one workbook, how many sheets?

**Default lean (please confirm):** One workbook, six sheets:

| Sheet | Rows | Source |
|---|---|---|
| `01_records` | 196 (one per canonical record) | `entities/v1-alpha/**/*.yaml` |
| `02_lineage` | edges (group→process; context→group; group→capability; etc.) | derived from `relationships[]` blocks |
| `03_dispositions` | 18 (one per Business Process) | `reconciliation/dispositions/register.yaml` |
| `04_register_audit` | 49 (one per ECF coordinate) | `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml` |
| `05_change_requests` | N (one per CR) | `change-requests/*.md` |
| `06_contributions` | N (one per pending contribution) | `contributions/processes/*.yaml` + `*.report.md` |

Sheet 1 columns: `id, name, type, domain, lifecycle_stage, process_context, process_group, version, status, lifecycle_status, disposition, last_modified`. **Lineage** is a separate sheet because it is a graph view; **versions** are a column on Sheet 1 (the user explicitly asked for "versions of processes" in the request).

**Alternatives.** One-sheet workbook (rejected — too wide, ~30+ columns). Or seven sheets (splitting `01_records` into `process_contexts`, `process_groups`, `business_processes` — cleaner data-model-wise but breaks the "flat view" intent).

**Decision needed:** confirm the six-sheet structure (or specify a variant).

### 3.3 BPMN-consumable artifact shape — plugin vs seed library

**Option A (lean: seed library).** A single `bpmn-library.bpmn` file containing one BPMN 2.0 Process per canonical Business Process (196 diagrams). Each diagram is a single Pool + single Task named after the BP, with metadata (ECF coordinate, Process Context, Process Group) as `<bpmn:documentation>` elements. Consumes natively in bpmn.io / Camunda Modeler / Signavio without any plugin install — the consumer just `File → Open` the file.

- Pro: Zero-install for the consumer; works in every BPMN tool that reads BPMN 2.0 XML.
- Pro: The diagram is the artifact — modelers can clone-and-extend.
- Con: 196 trivial "one-task" diagrams is noisy; could be a folder `bpmn-library/<id>.bpmn` instead, with a `bpmn-library.bpmn` index.

**Option B.** A bpmn.io Importer plugin — a small JS package that adds an "Import from OpenDEA Process Catalog" action to bpmn.io Modeler, which loads the catalog and adds each Business Process as a draggable palette entry. Consumes only in bpmn.io (not Camunda/Signavio) and requires the consumer to install the plugin.

- Pro: Best UX for bpmn.io users; palette entries carry ECF coordinates and can be dragged onto any canvas.
- Con: Bpmn.io-only; vendor-specific; not consumable as plain BPMN XML.

**Decision needed:** A (seed library) or B (bpmn.io plugin)?

### 3.4 Decisions log — verbatim export vs curated

**Option A (lean: curated).** `decisions.md` is a curated narrative: per-disposition table (record_id, disposition, rationale, evidence_links, change_history) + per-register-coordinate audit_status + per-CR one-paragraph summary. `dispositions/` folder contains the full `reconciliation/dispositions/register.yaml` (18 entries) verbatim as YAML.

- Pro: A reader who only opens `decisions.md` gets the story; the YAML folder is there for the reader who wants the raw data.
- Pro: Aligns with the BC catalog's "release notes + manifest" pattern.

**Option B.** Pure verbatim export of `reconciliation/` + `change-requests/` + `contributions/processes/` + per-record `change_history` blocks into the zip. No curated narrative.

- Pro: Provably faithful; no editorial layer.
- Con: A reader must open dozens of files to understand a single disposition.

**Decision needed:** A (curated) or B (verbatim)?

### 3.5 `dependencies.yaml` self-reference adoption

The BC catalog has it (proven pattern for federation consumers to pin `dea:catalog/business-capabilities@v1-alpha.4`). The process catalog does not.

**Lean:** adopt it in CR-BP-30 alongside the artifact family. The manifest pins to `v0.2.0` initially and advances with each tag.

**Decision needed:** adopt now (recommended) or defer to a later CR?

### 3.6 Artifact version independence

The BC catalog ships 2 files per tag and the artifacts are bumped in lockstep with the catalog version. We're proposing ~6 artifact types. Two options:

**Option A (lean).** All artifacts versioned together; every tag produces a complete new zip.

**Option B.** The BPMN plugin (if we go 3.3 = B) or the XLSX could be versioned separately — they evolve on their own cadence (a modeler might want the latest BPMN palette without re-pinning the whole catalog).

**Lean:** A. Same-shape-with-BC. Simpler governance. We can introduce B later if a real consumer asks.

**Decision needed:** A (lockstep) or B (independent)?

---

## 4. CI / GitHub Actions shape (the "how we produce it")

The plan does not commit code, but it locks the **CI surface** so we can validate the artifact family in CI before any tag push fires it.

### 4.1 New workflow: `.github/workflows/publish-versioned.yml`

Mirror BC's `publish-versioned.yml` (which I just audited; 107 lines, well-scoped). Trigger: `push: tags: ['v*']`. Permissions: `contents: write`. Concurrency group: `publish-versioned` (serial).

Job `publish-versioned` steps (in order):

1. Checkout (`actions/checkout@v4`, `fetch-depth: 0`).
2. Setup Python (`.python-version` pin).
3. Install: `pyyaml`, `weasyprint`, `openpyxl` (for XLSX), `lxml` (for BPMN XML construction), `poppler-utils` (system, for `pdftoppm`).
4. **Validate the substrate** — run all existing conformance scripts (the `ci.yml` gate must be green on the tagged commit; if not, abort). This is the "no release on a non-conformant snapshot" rule.
5. Generate `process-map.html` + `process-map-a3.png` via adapted `generate_process_map.py`.
6. Generate `catalog.xlsx` via `build_catalog_xlsx.py`.
7. Generate `bpmn-library.bpmn` (or `bpmn-plugin/`) via `build_bpmn_artifact.py` (per §3.3 decision).
8. Copy `entities/v1-alpha/**/*.yaml` to the zip root (so the zip is self-contained).
9. Copy `contributions/processes/**/*.yaml` + `*.report.md` to `contributions/` in the zip.
10. Generate `decisions.md` + copy `reconciliation/dispositions/*.yaml` to `dispositions/` (per §3.4 decision).
11. Generate `RELEASE-NOTES.md` from CHANGELOG + CR index.
12. Generate `MANIFEST.md` with per-file `source_path, generated_by, sha256, bytes`.
13. Re-zip: `cd out/${VERSION_LABEL} && zip -qr ../${VERSION_LABEL}.zip .`.
14. Upload workflow-run artifact (debug, 30-day retention).
15. Create or update GitHub Release (mirror BC's `gh release create` / `gh release upload --clobber` shape).

### 4.2 New workflow: `.github/workflows/validate-release-package.yml`

A pull-request-time gate that runs the **same generation steps** as 4.1 (steps 5-11) into a temp directory and **compares the artifact set against a known-good manifest** (via sha256). This catches:
- Schema changes that silently break the BPMN XML.
- New disposition rules that change the Excel output unexpectedly.
- ECF enum drift that changes the HTML map.

The workflow does NOT push to a release; it only validates that `git diff --quiet` succeeds between the PR's generated artifacts and the previous main commit's manifest. On drift, it posts a PR comment listing the changed files.

### 4.3 New scripts under `scripts/`

| Script | Inputs | Outputs | Provenance |
|---|---|---|---|
| `generate_process_map.py` | `entities/v1-alpha/`, ECF axis, version label | `process-map.html`, `process-map-a3.png` | Adapted from BC's `generate_capability_map.py` |
| `build_catalog_xlsx.py` | `entities/`, `reconciliation/dispositions/`, `change-requests/`, `contributions/processes/`, `l1-register.yaml` | `catalog.xlsx` (6 sheets) | New; uses `openpyxl` |
| `build_bpmn_artifact.py` | `entities/v1-alpha/**/business-process.yaml` (filter by `type: Process`) | `bpmn-library.bpmn` (or `bpmn-plugin/`) | New; uses `lxml` (or `bpmn-js` for plugin) |
| `build_release_notes.py` | `CHANGELOG.md` + `change-requests/` index | `RELEASE-NOTES.md` | New; pure text templating |
| `build_manifest.py` | every artifact in `out/<label>/` | `MANIFEST.md` with sha256 | New; uses `hashlib` |

All scripts must be **deterministic** (sorted YAML load, stable iteration order) so the PR-time gate and the tag-push run produce byte-identical output for the same substrate.

### 4.4 New manifest file: `dependencies.yaml`

Mirrors BC's 29-line file. Holds `ecf_contract`, `metamodel_pin`, and a `catalogs` self-reference block. Adopted per §3.5 decision.

### 4.5 What does NOT change in this CR

- No entity, schema, validator-rule, or governance-decision change.
- No conformance-gate change (the existing `ci.yml` is the gate; `publish-versioned.yml` runs only after the gate is green).
- No new domain, no new process, no new ECF coordinate.

---

## 5. Implementation phasing (the "how we cut this into PRs")

This CR is the discussion document only. After approval, the implementation slices are:

| PR | Title | Scope | Est. size |
|---|---|---|---|
| CR-BP-30 | **This document** (Discussion + decision) | Plan + decisions on §3 | Docs only |
| CR-BP-30a | Map generator adaptation | Port `generate_capability_map.py` to `generate_process_map.py`; first artifact | ~600 LOC + tests |
| CR-BP-30b | XLSX builder | New `build_catalog_xlsx.py`; 6-sheet workbook | ~400 LOC + tests |
| CR-BP-30c | BPMN artifact (per §3.3 decision) | New `build_bpmn_artifact.py` | ~300 LOC (seed lib) / ~600 LOC (plugin) |
| CR-BP-30d | Decisions log + release notes | `build_release_notes.py` + curated `decisions.md` template | ~200 LOC + content |
| CR-BP-30e | `dependencies.yaml` adoption | Per §3.5 | ~30 LOC + 1 carrier PR |
| CR-BP-30f | `publish-versioned.yml` workflow | Mirror BC; wire all generators | ~150 LOC |
| CR-BP-30g | `validate-release-package.yml` workflow | PR-time gate | ~80 LOC |
| CR-BP-30h | First release cut with the full package | Tag `v0.2.0` (or `v0.3.0`) with all artifacts | Workflow run + verification |

Each implementation PR is self-contained, ships its own tests, and bumps a minor version on the artifact type when it lands. None of them requires the next to merge — they can land in any order, except CR-BP-30f (workflow), which needs at least one generator to exist to validate.

---

## 6. Why this matters (restated for the record)

A catalog that cannot be **seen**, **queried as data**, **imported into a modeling tool**, or **audited for its decisions** is a catalog that downstream consumers will not adopt. The BC catalog proved the artifact shape; the process catalog's richer entity model (Process Context ⊃ Process Group ⊃ Business Process, with dispositions + lineage + register audit + contribution reports) needs the same shape plus three additional surfaces (XLSX, BPMN, decisions log) that turn a governance artifact into a usable product.

This CR does not ship those surfaces. It locks the plan, the CI shape, and the per-artifact decision space so the implementation PRs (30a..30h) can land incrementally with each one independently reviewable and revertable.

---

## 7. Acceptance criteria for this CR

1. The five §3 design decisions are resolved (map shape, Excel sheets, BPMN shape, decisions log shape, dependencies.yaml adoption).
2. The §3.6 lockstep-vs-independent question is resolved.
3. The §4 CI surface is approved (workflows + scripts).
4. The §5 implementation phasing is approved (PR-by-PR cut).
5. CHANGELOG + CITATION.cff unchanged from `v0.2.0` (this CR is discussion-only).
6. No code, no schema, no validator change in this PR.

When this CR is approved, CR-BP-30a (the map generator adaptation) is the natural next slice.
