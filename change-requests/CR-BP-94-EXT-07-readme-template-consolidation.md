# CR-BP-94-EXT-07: README Template Consolidation + Generator V2

**Status**: Proposed
**Layer**: Process Catalog (Cross-Cutting Documentation)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-17
**Parent**: CR-BP-94 (Decomposition Record Templates, PR #134); CR-BP-94-EXT-01 (Documentation Architecture, PR #137); CR-BP-94-EXT-01a (L0/L1 Cardinal Entity Documentation Profiles, PR #138); CR-BP-94-EXT-02 (README Generation Pipeline)
**Source**: User-attached design brief (CR-BP-120, 2026-10-17) + consolidated with T9.13 (card 373) and EXT-02 (in main)
**Recon programme parents**: CR-BP-92 (Process Catalog layer), CR-BP-93 (decomposition semantic contract), CR-BP-99 (reconciliation matrix; 2,306 advisory findings)
**Supersedes**: CR-BP-94-EXT-02's 13-section template (in `scripts/generate_readmes.py`)
**Sub-pipeline position**: EXT-07 (post-EXT-02; pre-EXT-04 / EXT-06)
**Lands against**: 49 cell-root + 3,674 record READMEs; L0/L1/L2/L3/L4 profiles; `dea/v1` schema

---

## 1. Change Request

Consolidate the three competing README designs that have accumulated during the EXT documentation workstream into a single superseding template + generator. Add the `metrics` schema block (KPI/KRI/KCI) to support the EXT-04 + EXT-06 workstreams. Add the `profile` field to the L1 (ProcessGroup) schema as the L1-pilot unblock that EXT-06 needs as a prerequisite.

The three source designs:

- **T9.13 (card 373)**: 7-section progressive disclosure (Identity, Intent, Definition, Description, Properties, Relationships, Provenance, +Cell Charter for L0). Strength: strict data-type view; properties + relationships as tables. Gap: drops 6 of 13 EXT-02 sections; no governance/metrics/styling.
- **EXT-02 (in main)**: 13 sections (Entity Identity, Formal Definition, Canonical Semantic Dimensions, Decomposition, Behavior, Inputs/Outputs/Interfaces, Roles/Responsibilities, Business Rules/Controls, Outcomes, Evidence, Documentation Completeness, Revision History, Path Scheme). Strength: architecture-derived; deterministic. Gap: raw dict dumps; path scheme buried at section 13; section numbering skips 8 to 10 (bug); no metrics; no governance-first framing.
- **CR-BP-120 (user-attached, 2026-10-17)**: 6 sections (Header & Identity Table, Governance & Provenance, Behavioral Boundaries, Hierarchical Decomposition, Operational/Control/Metrics Details, Technical Metadata). Strength: governance-first; metrics block; emoji tabular boundaries; collapsible HTML tree; regulatory evidence base. Gap: no Properties table; no Relationships table; no Intent paragraph.

The consolidated design takes the strongest element from each.

---

## 2. The Consolidated README Structure

### 2.1 L0 ProcessContext README (8 sections)

L0 is the most-read surface (governance context). Gets the full treatment.

1. **Header & Identity Table** - Domain / Lifecycle / Level / Status / Version / Schema (from CR-BP-120)
2. **Executive Summary / Intent** - 1 paragraph: what + why the entity exists (from T9.13)
3. **Governance & Provenance** - admission score, regulatory evidence base, change history (from CR-BP-120)
4. **Behavioral Boundaries** - `cell_charter` rendered as table with In Scope / Out of Scope / Adjacent rows (from CR-BP-120; replaces the raw dict dump)
5. **Hierarchical Decomposition** - L1-L4 tree inside `<details>` HTML block (from CR-BP-120; replaces the buried section 13 of EXT-02)
6. **Properties & Relationships** - full property table + relationships table (from T9.13; NEW addition; surfaces every YAML field deterministically)
7. **Operational, Control & Metrics Details** - Inputs/Outputs, Roles, Business Rules + the new `metrics` table categorised by KPI / KRI / KCI (from CR-BP-120; the metrics sub-table is the EXT-04 authoring target)
8. **Technical Metadata** - source YAML link, register version, audit status (from CR-BP-120)

### 2.2 L1-L4 record README (7 sections)

L1-L4 are operational records. Leaner than L0.

1. Header & Identity Table
2. Intent + Definition (combined)
3. Governance & Provenance (lighter: admission + change history; no regulatory evidence base)
4. Properties & Relationships (full table)
5. Hierarchical Decomposition
6. Operational Details (no metrics at L1-L4; metrics are L0-level concerns)
7. Technical Metadata

### 2.3 What this slice supersedes

- The 13 sections of EXT-02 are reorganised into the 7-8 section structure above.
- The 7 sections of T9.13 are a strict subset of the new structure; their numbering changes (Identity is 1, not a/b/c; Properties + Relationships are merged into section 6; Provenance is split between Governance and Technical Metadata).
- The 6 sections of CR-BP-120 are extended by the addition of "Intent" (T9.13) and "Properties & Relationships" (T9.13).

### 2.4 Specific bug fix

EXT-02's section numbering skips from section 8 to section 10 (the "Outcomes" section is missing the explicit 9-numbering; it appears as 9 in the heading but the prior 8 is the Business Rules section). This CR fixes the numbering by replacing the numeric prefix with descriptive headings in the new structure (no numeric prefix on L1-L4 sections; numbered 1-8 on L0 for scanability).

---

## 3. YAML Schema Extension (`dea/v1`)

### 3.1 The `metrics` block (OPTIONAL, L0 only)

Per CR-BP-120 section 3.2, add an OPTIONAL `metrics` block at L0. The block has three sub-blocks keyed by category, each containing a list of `{name, target, frequency}` records.

```yaml
metrics:
  performance:  # KPIs (Key Performance Indicators)
    - name: Mean Time to Activate (MTTA)
      target: "< 48 hours"
      frequency: Weekly
  risk:         # KRIs (Key Risk Indicators)
    - name: Fitness-and-Propriety Bypass Rate
      target: "0%"
      frequency: Continuous
  compliance:   # KCIs (Key Compliance Indicators)
    - name: Expired Licence Mobilization Count
      target: "0 (Hard block)"
      frequency: Continuous
```

The block is OPTIONAL. Records without a `metrics` block render the `*(Pending EXT-04)*` placeholder. The structural validator (EXT-04, separate CR) surfaces records that have an empty `metrics` block as DOC-004 advisory findings (not blocking).

The block is L0-only. Lower levels (L1-L4) do not carry metrics; their operational state is described in the Operational Details section.

### 3.2 The `profile` field on L1 (ProcessGroup)

The L1 pilot attempted in CR-BP-94-EXT-01a was rejected because `schemas/entities/process-group.schema.json` declares `additionalProperties: false` and the `composes` field is constrained to a non-empty array. The pilot on `dea:group-customer-insight-and-retention` could not be re-composed.

This CR unblocks the L1 pilot by adding a new OPTIONAL `profile` field to the L1 schema. The `profile` field is a string-typed slug that allows an L1 record to carry its pilot profile identifier without affecting the `composes` array. The `additionalProperties: false` constraint remains; the `profile` field is added to the allowed properties list (not yet in `required`).

```json
"profile": {"type": ["string", "null"], "description": "L1 pilot profile slug (CR-BP-94-EXT-07 unblock for L1 pilot admission)."}
```

The dea-metamodel canonical source is unchanged: the `profile` field is a dea-catalog-processes-specific schema extension, not a metamodel-level field. The metamodel records no knowledge of L1's `profile` field; the field is opaque to the metamodel layer.

---

## 4. Generator Changes (`scripts/generate_readmes.py`)

### 4.1 Section structure

Replace `PROFILE_SECTIONS` and `SECTION_HEADINGS` with the consolidated structure:

```python
PROFILE_SECTIONS: dict[tuple[str, str], list[str]] = {
    ("ProcessContext", "L0"): [
        "header-identity-table", "executive-summary", "governance-provenance",
        "behavioral-boundaries", "hierarchical-decomposition",
        "properties-relationships", "operational-metrics", "technical-metadata",
    ],
    ("ProcessGroup", "L1"): [
        "header-identity-table", "intent-definition", "governance-provenance",
        "properties-relationships", "hierarchical-decomposition",
        "operational-details", "technical-metadata",
    ],
    ("Process", "L2"): [...],   # same as L1
    ("Activity", "L3"): [...],  # same as L1
    ("Task", "L4"): [...],      # same as L1
}

SECTION_HEADINGS: dict[str, str] = {
    "header-identity-table": "## Header and Identity Table",
    "executive-summary": "## 1. Executive Summary / Intent",
    "governance-provenance": "## 2. Governance and Provenance",
    "behavioral-boundaries": "## 3. Behavioral Boundaries (Cell Charter)",
    "hierarchical-decomposition": "## 4. Hierarchical Decomposition (Path Scheme)",
    "properties-relationships": "## 5. Properties and Relationships",
    "operational-metrics": "## 6. Operational, Control and Metrics Details",
    "operational-details": "## 6. Operational Details",
    "technical-metadata": "## 7. Technical Metadata",  # L1-L4
    "technical-metadata-l0": "## 8. Technical Metadata",  # L0
    "intent-definition": "## 1. Intent and Definition",
}
```

### 4.2 New renderers

- `header-identity-table`: a Markdown table with 2 columns of 3 attribute/value rows each (Domain + Lifecycle, Level + Status, Version + Schema).
- `governance-provenance`: admission score (numeric), regulatory evidence base (list of domains with emojis per CR-BP-120 example), change history table.
- `behavioral-boundaries`: 3-row table with In Scope (with checkmark), Out of Scope (with x), Adjacent (with link). Renders from `record.cell_charter.inclusions`, `exclusions`, `adjacent_boundaries`.
- `hierarchical-decomposition`: `<details><summary>` HTML block wrapping the directory tree. Replaces the bare `path-scheme` section.
- `properties-relationships`: two tables. Properties table (name / type / required / description). Relationships table (kind / target id / cardinality).
- `operational-metrics`: four subsections (Inputs/Outputs, Roles, Business Rules, Target Metrics). Target Metrics renders the `metrics` block as a KPI / KRI / KCI table; if absent, renders `*(Pending EXT-04)*`.
- `operational-details`: same minus the metrics sub-section (L1-L4 only).
- `technical-metadata`: source YAML link, register version, documentation completeness checklist.
- `executive-summary`: 1-paragraph Intent from `record.definition` or `record.description`.
- `intent-definition`: combined L1-L4 intent + definition.

### 4.3 Emoji styling

Per CR-BP-120 example:
- In Scope: checkmark emoji
- Out of Scope: x emoji
- Adjacent: link emoji

Rendered in the behavioral-boundaries table only. No emoji elsewhere (D-004 hygiene; emoji are not in the D-004 denylist of U+2013, U+2014, U+2E3B but are kept minimal to avoid styling drift).

### 4.4 Section numbering fix

Remove the hard-coded numeric prefixes in the EXT-02 headings. The new headings are descriptive without a numeric prefix on L1-L4; L0 uses 1-8 for executive-summary through technical-metadata (8 sections, scanable from the top).

### 4.5 Backward compatibility

The generator changes are deterministic and additive to the Markdown output. Existing YAML records without a `metrics` block render the `(Pending EXT-04)` placeholder. The `behavioral-boundaries` renderer falls back to a `(Cell charter pending; backfill at EXT-04)` message if the record has no `cell_charter` block. Records with no `properties-relationships` content render a minimal table with one row `(no additional properties)`. The dry-run flag is preserved.

---

## 5. Regeneration Sweep

After the generator update, all 49 cell-root READMEs and all 3,674 record READMEs are regenerated. The sweep is one commit (per CR-BP-118a precedent). The DOC-001 to DOC-005 advisory findings drop to 0 for the new sections; new DOC-004 findings appear for records that have no `metrics` block (these are the EXT-04 authoring target, not a regression).

The `RDM-001` and `RDM-002` gates (in `scripts/check_readme_consistency.py`) verify that the rendered Markdown is consistent with the record YAML (no drift). The `check_readme_consistency` test suite (15 tests) must remain green.

---

## 6. Cross-Repo Cascade (T9.13b follow-on)

This CR lands the wave-0 implementation in `technehub-labs/dea-catalog-processes`. The other 11 sibling repos receive the same template + generator as a follow-on programme (T9.13b), sequenced for the next release cycle (T9.12, deferred). The wave plan:

- **Wave 1**: dea-catalog-business-capabilities, dea-catalog-business-objects, dea-catalog-organizational-units (the 3 catalog siblings with the same record model)
- **Wave 2**: dea-metamodel, dea-metaframework, dea-architecture-framework (the upstream metamodel; carries the dea/v1 schema)
- **Wave 3**: dea-release-package, technehub-labs.github.io (the downstream portal and release packaging)
- **Wave 4**: dea-governance, remaining

The wave-0 deliverable in this repo is the proof; the other 11 repos adopt the same `generate_readmes.py` + `PROFILE_SECTIONS` shape (with profile-specific tweaks).

---

## 7. Acceptance Criteria

- **AC-01**: The 8-section L0 template and the 7-section L1-L4 template are landed in `scripts/generate_readmes.py`.
- **AC-02**: The 49 cell-root READMEs are regenerated to the new template.
- **AC-03**: The 3,674 record READMEs are regenerated to the new template.
- **AC-04**: The `metrics` block schema extension is documented; existing L0 records without a `metrics` block render the `(Pending EXT-04)` placeholder.
- **AC-05**: The `profile` field is added to `schemas/entities/process-group.schema.json`; the L1 pilot can be re-attempted under EXT-06.
- **AC-06**: The RDM-001/002 gates (in `scripts/check_readme_consistency.py`) are green.
- **AC-07**: The `test_generate_readmes.py` test suite is extended with 5+ new tests (header-identity table; governance-provenance; behavioral-boundaries with the 3-row table; hierarchical-decomposition with `<details>` block; properties-relationships with both tables).
- **AC-08**: D-004 clean on the new generator code and the regenerated READMEs.
- **AC-09**: 118a / 118b / 118c / 123 / 124 / 125 / 126 / 127 / 128 / 129 / 130 / 131 / 132 / EXT-02 authorship + entity-system gates remain CONFORMANT.
- **AC-10**: The section numbering skip (8 to 10) is fixed; sections are numbered sequentially 1-8 on L0 or use descriptive headings without numbers on L1-L4.

---

## 8. Dependencies + Enables Chain

**Depends on**:

- CR-BP-94-EXT-01 (PR #137, MERGED) - the documentation architecture
- CR-BP-94-EXT-01a (PR #138, MERGED) - the L0/L1 cardinal entity profiles
- CR-BP-94-EXT-02 (status row ambiguous; to be verified) - the previous generator

**Enables**:

- **CR-BP-94-EXT-04** (Validation Pipeline) - the structural validator reads the new template; depends on EXT-03 (manifest schema) which is a separate CR
- **CR-BP-94-EXT-06** (Pilot + Rollout) - the catalog-wide regeneration; depends on EXT-04 + EXT-05 (separate CRs)

**External (NOT in this CR)**:

- **CR-BP-94-EXT-03** (manifest schema) - author as a separate CR; the validator (EXT-04) needs the manifest format
- **CR-BP-94-EXT-05** (decomposition reconciliation) - author as a separate CR after EXT-04 lands; the pilot (EXT-06) needs the parent-child traceability

---

## 9. Test Plan

The `test_generate_readmes.py` test suite is extended with 5 new tests:

1. `test_header_identity_table_renders_table` - verify the 6-row attribute table is rendered with the correct keys.
2. `test_governance_provenance_renders_change_history` - verify the change history table is rendered from `change_history` records.
3. `test_behavioral_boundaries_renders_three_row_table` - verify the In Scope / Out of Scope / Adjacent rows are present with the correct emoji.
4. `test_hierarchical_decomposition_uses_details_block` - verify the `<details><summary>` HTML is present in the rendered Markdown.
5. `test_properties_relationships_renders_both_tables` - verify the property table + relationships table are both rendered.
6. `test_metrics_block_renders_or_placeholder` - verify a record with a `metrics` block renders the KPI/KRI/KCI table; verify a record without renders `(Pending EXT-04)`.
7. `test_section_numbering_continuous` - verify L0 has sections 1-8 with no skips; verify L1-L4 uses descriptive headings without numeric prefix.

The end-to-end test (`test_generate_readmes_end_to_end`) runs the generator against the live catalog and verifies that DOC-001 to DOC-005 advisory findings drop to 0 for the new sections.

---

## 10. Result

This CR supersedes the 13-section EXT-02 template with the consolidated 8+7 structure, adds the `metrics` block to support the EXT-04 authoring workstream, and adds the L1 `profile` field as the unblock for the L1 pilot in EXT-06. The generator (`scripts/generate_readmes.py`) is rewritten with the new renderers, the section numbering skip is fixed, and the full 49+3674 record set is regenerated. The cross-repo cascade (T9.13b) is a follow-on programme. D-004 clean. 118 series + entity-system gates CONFORMANT.
