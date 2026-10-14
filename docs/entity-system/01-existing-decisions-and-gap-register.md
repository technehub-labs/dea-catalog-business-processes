# Existing Decisions and Gap Register

> **Stage 1 output 2 of CR-BP-121 (renumbered from CR-BP-16).**
> What is already established in `dea-catalog-processes`, what is missing, and what disposition is recommended.
> Foundation: [00-charter.md](00-charter.md). Cross-references: [DEA-ID-000](../../../../dea-governance/docs/design/entity-system-foundation.md), [CR-012](../../../../dea-governance/change-requests/CR-012-org-wide-entity-governance.md).

This register walks the existing change-request baseline (CR-BP-01 through CR-BP-118c, the ADRs in `dea-architecture-framework`, and the ECF / metamodel artifacts) and classifies each decision as:

- **R** (Retained): already aligned with the General Entity System; no change required.
- **H** (Historical-only): pre-Entity-System decision; the rule stays as historical record; future records are governed by the new standard.
- **N** (Needs framing): requires a follow-up CR to reconcile the existing decision with the Entity System standard.
- **U** (Unresolved): an open question that the Stage 2 normative design proposal must resolve.

## 1. Identity decisions

| Decision | CR / ADR | Classification | Notes |
|---|---|---|---|
| IDM-001..008 (id-system coherence) | CR-BP-mv1, CR-BP-04 | **R** | The `processes:<token>-<descriptor>-<base32hash>` format and the BASE32 strict alphabet are the canonical id format. IDM-008 cross-repo coherence gate is in place. **G-01 (Identity Standard)**: this needs a normative spec doc, not a behaviour change. |
| IDM-004 strict BASE32 alphabet | CR-BP-mv1 | **R** | Enforced by `scripts/check_id_system.py`. |
| IDM-005 filename + cell segment + depth validation | CR-BP-mv1 | **R** | Filename stability is the foundation of cross-version reference integrity. |
| Hash-suffix stability | CR-BP-mv1 | **R** | The content-addressed entropy suffix on a record id is stable across renames AND content edits. **G-01 norm**: codify this in the Identity Standard spec. |
| IDM-001 pattern: `^[a-z]+:[a-z]+-[a-z]{2,3}-[a-z]+(-[a-z]+)*-[a-z2-9]{6}$` | CR-BP-mv1 | **R** | The four canonical ID families (`dea:process-*`, `dea:pc-*`, `dea:group-*`, `dea:scope-*`) plus the post-mv1 `processes:` family. **G-01 norm**: explicitly document the family list. |
| Legacy `dea:bp:*` migration | CR-BP-04 | **R** | Treated as legacy migration reference; live content uses canonical families. **G-07 (Legacy ID Reconciliation)**: 35 `dea:` legacy tails in entities/v1-alpha/ need a disposition register. |
| Entity-identity clarity (EID-001..004) | CR-BP-117a | **R** | EID-001 same-level identity collisions (0 hits; advisory); EID-002/003 README identity (0 hits; advisory); EID-004 cross-level reuses (22 hits; informational inventory). |
| Folder/path clarity | CR-BP-117c | **R** | C-1 dir rename; C-3 path-scheme documentation. |
| CR-BP-116 (release-history reset) | CR-BP-116 (parked) | **H** | The release-history reset is a separate concern from identity governance. The Charter retains the v0.1.0 / v0.3.0 abandoned tags as historical record (per user directive 2026-09-12). |

## 2. Semantics decisions

| Decision | CR / ADR | Classification | Notes |
|---|---|---|---|
| Process-kernel + Business-Process specialisation | CR-BP-SPEC-BP-01, ADR-0006 | **R** | The `dea:entity-process` kernel + the `dea:entity-business-process` first Core specialisation. The catalog instantiates the specialisation. |
| Process Context register + Cell Charter | CR-BP-02 | **R** | The 49-cell ECF matrix (7 domains x 7 lifecycle stages) gives the catalog its cardinal structure. |
| Process Group profile | CR-BP-12 | **R** | First-class L1 Process Group record type; per-file schema dispatch. |
| 4-axis classification (intent / type / specialisation / audience) | CR-BP-03 | **R** | The `process_type` (Mintzberg 5-value) + `process_intent` (7-value purpose-oriented) + `process_specialization` (inheritance / pattern-based) + `process_audience` (legacy migration alias). |
| Process semantic reconciliation | CR-BP-14 | **R** | The 6-dimension semantic contract; replaces the legacy 3-value intent vocabulary. |
| ECF conformance block | CR-BP-31 | **R** | The `framework: EnterpriseConceptFramework` (not `ECF`); `contractVersion: '1.0.0'`; `profile: dea:ecf@1.0.0`; `status: conformant`; `affiliation: inherits-catalog`; `canonicalReferences` carrying `{kind: coordinate, domain, stage, identifier: ecf:<domainToken>.<stageToken>}`. |
| EGV-005 (canonical entity contract) | CR-012 | **N** | The common entity envelope is not codified in this catalog today. The per-record-type schema (PG, BP, Activity, Task) implements the contract implicitly; an explicit common envelope spec doc is needed. **G-02 (Entity Contract Standard)**: Stage 2 output. |
| Type-discrimination | BP-ARC-ID-001..005, CR-BP-03 | **R** | Process records are distinguished by `type: Process`; the schema enforces the discriminator. |

## 3. Relationship decisions

| Decision | CR / ADR | Classification | Notes |
|---|---|---|---|
| Composition (L1 group --composes--> L2 process) | CR-BP-12 | **R** | The canonical containment direction; `part-of` is the derived inverse (not in the metamodel relationship-type enum). |
| Process Contribution Record | CR-BP-03C, the contribution workflow | **R** | A new process contribution is submitted to `contributions/processes/`; a report is generated; the report is piped through CI. |
| Realisation (BP --realises--> Capability) | CR-BP-03A | **R** | The `realizes` relationship type; the migration from `capabilities_delivered` (soft-deprecated). |
| Specialisation (BP --specialises--> BP) | CR-BP-SPEC-BP-01 | **R** | The `specializes` relationship type; the kernel + specialisation discipline. |
| Cross-catalog references (e.g. BP --realises--> BC capability) | (implicit) | **N** | Today's BP records carry `relationships[].target` entries that may point at `dea-catalog-business-capabilities` ids. The resolution mechanism (which catalog owns the target; what the resolution semantics are) is not codified. **G-06 (Cross-Catalog Reference Standard)**: Stage 2 output. |
| metamodel-pointer.yaml | (org-level) | **R** | The catalog declares both `dea:BusinessProcess` (specialization) and `dea:entity-process` (kernel; `discriminator: process-kernel`). |
| EGV-006 (relationship and reference integrity) | CR-012 | **N** | The validation is partially in place (BP-SEM-001..014, BP-SPEC-01-001..007, MECE-001..008) but the umbrella rule (all relationships resolve to valid entities within declared identity scope) is not codified. **G-03 (Relationship Standard)**: Stage 2 output. |

## 4. Lifecycle decisions

| Decision | CR / ADR | Classification | Notes |
|---|---|---|---|
| Admission-authority marker (CR-BP-115) | CR-BP-115 | **R** | The data-driven mechanism: every CR file carrying `**Admission authority**: yes` registers itself; `_load_admission_authorities()` walks CR files. The old `_ADMISSION_CR_RE` regex is deleted. |
| Admission gate (ADM-001..008) | CR-BP-115 | **R** | The 8-rule gate: required fields, schema validity, ECF conformance, change history, etc. |
| LCM-001..005 (lifecycle state-machine) | CR-BP-34c | **R** | The 5-rule gate; LCM-005 forward-only (no retired records today). |
| CR-META-001..006 (CR metadata gate) | (multiple) | **R** | The 6-rule gate; strict mode is a regression trap. |
| Provenance / change_history | CR-BP-31 (ECF), CR-BP-03 (identity) | **R** | The `change:` key is required on every `change_history[]` entry (provenance: CR-BP-113). |
| DOC-001..005 (documentation conformance) | CR-BP-94-EXT-01, CR-BP-94-EXT-01a | **R** | The L0/L1/L2/L3/L4 documentation profile registry. |
| Supersession (MECE-008 exempts `lifecycle_status: deprecated`) | CR-BP-36 | **R** | Deprecated BPs are intentionally not composed. |
| EGV-007 (version and lifecycle separation) | CR-012 | **N** | The four concepts (entity identity / entity revision / schema version / catalog release) are not always separated in the current implementation. **G-04 (Lifecycle Standard)**: Stage 2 output. |
| EGV-008 (provenance and traceability) | CR-012 | **R** | The authorship cardinal rule (CR-BP-118a/b/c) implements the authorship half of EGV-008. The CR-provenance half is implemented by the CR-META gate + the change_history block. **G-04**: codify the lifecycle state machine + identity-continuity rules. |

## 5. Conformance decisions

| Decision | CR / ADR | Classification | Notes |
|---|---|---|---|
| Conformance pipeline (the 30+ gate roster) | CR-BP-16 S18 | **R** | The single CONFORMANCE RESULT verdict; one of CONFORMANT / CONFORMANT-WITH-WARNINGS / NON-CONFORMANT. The canonical pre-merge verdict source. |
| CI workflow (`ci.yml`) | (multiple) | **R** | The validate workflow fetches the catalog index machinery from `dea-metaframework`, runs the gate roster, and produces the verdict. |
| Authorship cardinal rule gate (AUT-001..003) | CR-BP-118a | **R** | The metadata-field authorship gate; the new wire-up at the 118b/118c cascade. |
| Prose authorship gate (PROSE-001..002) | CR-BP-118c | **R** | The content-field authorship gate with the `Agent` allowlist. |
| HREF / TPL / CRR drift gates (CR-BP-113) | CR-BP-113 | **R** | The 3 new gates + 3 repair scripts shipped atomically. |
| README regeneration triad (CR-BP-114) | CR-BP-114 | **R** | The generator + repair + drift gate triad for the 3,405+ READMEs. |
| EGV-010 (machine-verifiable conformance) | CR-012 | **N** | The umbrella entity-system gate does not exist today. The component gates (one per concern) are in place; the umbrella gate is the Stage 3-4 output. **G-05 (Conformance Standard)**: Stage 2 spec; **G-05 gate**: Stage 3-4 implementation. |
| EGV-011 (change enforcement) | CR-012 | **R** | The CI workflow enforces the gate roster; non-conformant PRs cannot merge (the schema-validation phase-2 early-exit is a documented exception). |

## 6. Cross-cutting decisions

| Decision | CR / ADR | Classification | Notes |
|---|---|---|---|
| Admission freeze (CR-BP-14 §22) | CR-BP-14 | **R** | The canonical admission freeze is in effect until the BP-15 evidence-driven reconciliation lands. |
| Recovery appendix doctrine | CR-BP-31, slice skill | **R** | Before any destructive op, capture the pre-deletion state into a recovery appendix on the carrier CR file. |
| D-004 (no en/em-dash, no U+2E3B) | (org-wide) | **R** | Enforced by the cardinal-rule gate; checked at every CR doc. |
| CR-118 (authorship cardinal rule) | CR-BP-118a/b/c | **R** | Already implemented + cascaded to 12 repos. |
| EGV-009 (catalog conformance) | CR-012 | **N** | The adoption CR for THIS catalog is CR-BP-121 (this CR); the cascade to other 11 repos is T7 of the umbrella programme. **G-09 codification**: this Stage 1 CR is the adoption CR; the umbrella gate is the conformance mechanism. |
| EGV-012 (legacy reconciliation) | CR-012 | **N** | The 35 `dea:` legacy tail in entities/v1-alpha/ needs a disposition register. The 7 repos from the 118b cascade (BC, BO, OU, MF, MM, AF, ACT, STAKE) also have legacy tails. **G-07**: per-record disposition register + reconciliation mappings. **T8 of umbrella programme**: cross-repo reconciliation. |

## 7. Open questions (U)

These are questions the Stage 2 Normative Design Proposal must resolve.

- **U-01** What is the canonical URI form for a cross-catalog reference? `dea:<catalog>:<id>`? A URL? An opaque URN?
- **U-02** What is the lifecycle state machine? `proposed / admitted / deprecated / retired`? Or finer-grained?
- **U-03** How are `provenance: {cr, date, change}` and `change_history: [{cr, date, change}]` related? Are they the same? Different?
- **U-04** Should the entity-system gate be advisory or blocking? (The 118a/118b/118c gates are blocking under --strict; the legacy components are mixed.)
- **U-05** How does the entity-system gate interact with the conformance rollup? (The 30-gate rollup is the canonical pre-merge verdict; should the entity-system gate be a separate rollup row, or fold into the existing rollup?)
- **U-06** What is the "exception mechanism" under EGV-011? The 118a/118b/118c work has a "review-retained" pattern in `catalog-research/normalization.yaml`. Is this the precedent?
- **U-07** How does the General Entity System interact with the OpenDEAM Authority Chain (CR-001..008, CR-9.1..9.10, CR-10, CR-11, CR-AM-01)? Are the 12 EGV-001..012 requirements ratified under that chain, or as a separate authority track?

## 8. Disposition register (per EGV-012)

| Repo / area | Legacy tail | Disposition | Owner |
|---|---|---|---|
| `entities/v1-alpha/` (this catalog) | 35 `dea:` ids | Document in `reconciliation/migration-id-map.yaml`; treat as grandfathered historical record; new records MUST use the canonical `processes:` family | T8 of umbrella programme |
| `dea-catalog-business-capabilities` | 3 `dea:` legacy | Same; already documented in BC's reconciliation register | T7 cascade |
| `dea-catalog-business-objects` | 2 `dea:` legacy | Same | T7 cascade |
| `dea-catalog-organizational-units` | 2 `dea:` legacy | Same | T7 cascade |
| `dea-catalog-actors` | 2 `dea:` legacy | Same | T7 cascade |
| `dea-catalog-stakeholders` | 2 `dea:` legacy | Same | T7 cascade |
| `dea-metamodel` | 458 `dea:` + 1 `dmm:` + 1 `dmmv5:` | The metamodel's `dea:` family is canonical for entity-type definitions; not a legacy tail per EGV-001 | T8 (cross-reference) |
| 5 gate-only repos (blueprints, concepts, tenets, etc.) | 0 | No legacy tail | T7 cascade (gate-only) |

## 9. Summary

- **15 decisions** retained (R) - no change.
- **2 decisions** historical-only (H) - leave as-is.
- **9 decisions** need framing (N) - Stage 2 outputs (G-01..G-07).
- **7 open questions** (U) - Stage 2 norm design proposal resolves.
- **6 legacy-tail repos** - per-repo disposition register under EGV-012.

The catalog's existing gate roster is substantial and largely aligned with the General Entity System. The Stage 2 norm design proposal is the codification work: making the 9 N-classification decisions explicit, normative specs.
