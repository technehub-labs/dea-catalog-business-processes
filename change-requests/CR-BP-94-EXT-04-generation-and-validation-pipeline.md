# CR-BP-94-EXT-04: Generation & Validation Pipeline

**Status**: Proposed
**Layer**: Process Catalog (Cross-Cutting Documentation)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-17
**Parent**: CR-BP-94 (Decomposition Record Templates); CR-BP-94-EXT-07 (README Template Consolidation, PR #177, OPEN)
**Source**: User directive 2026-10-17 ("Let's address the README Restructure + Owner Section Removal, and in addition what is the situation with EXT-04 Backfilling? ... Ext-05 should be actioned once we have Ext 04. We need to wire this in to the development model.")
**Sub-pipeline position**: EXT-04 (post-EXT-07; pre-EXT-05 / EXT-06)
**Lands against**: 49 cell-roots + 3,674 record READMEs; the CR-BP-99 reconciliation matrix (2,306 advisory findings); the L0 metrics block from EXT-07
**Dependencies**: CR-BP-94-EXT-07 (template must be final) + CR-BP-94-EXT-03 (manifest schema; separate CR, NOT in this programme)
**Enables**: CR-BP-94-EXT-05 (decomposition reconciliation; user directive 2026-10-17: "Ext-05 should be actioned once we have Ext 04. We need to wire this in to the development model"); CR-BP-94-EXT-06 (pilot + rollout)

---

## 1. Change Request

Land the **validator half** of the EXT documentation workstream. The generator half is CR-BP-94-EXT-07 (README Template Consolidation; PR #177, OPEN). This CR adds:

1. A new structural validator (`scripts/validate_readme_structure.py`) that reads the EXT-07-generated READMEs and emits findings against the EXT-07 documentation profile.
2. A new conformance gate ([N] Documentation Profile - Generator and Validator) wired into `scripts/conformance_result.py`. Advisory (not blocking merge) per the EXT-01 section 3 pattern.
3. A wire into the standing development model: the validator is the input for the EXT-05 decomposition reconciliation slice.

The CR-BP-99 reconciliation matrix catalogues 2,306 advisory findings (matrix-010..013). The CR-BP-99 closure statement (section 3) says: "Documentation authoring (closing the 2,306 DOC-001/002/003/005 advisory hits) belongs to EXT-06." This CR (EXT-04) is the bridge: the validator surfaces the findings, the EXT-06 rollout reconciles them, the EXT-05 decomposition reconciles the parent-child traceability.

The "backfilling" the user asked about (2026-10-17) refers to the 2,306 advisory findings; EXT-04 is the validator that surfaces them deterministically; EXT-06 is the work that reconciles them.

---

## 2. Validator Design (`scripts/validate_readme_structure.py`)

### 2.1 Scope

The validator reads every generated README and emits findings against the EXT-07 documentation profile. The findings are categorised:

- **DOC-016**: Generated README has the EXT-07 section identifiers (the new 8 L0 / 7 L1-L4 set).
- **DOC-017**: Generated README has the required properties surfaced in the Properties table.
- **DOC-018**: Generated README has the required relationships surfaced in the Relationships table.
- **DOC-019**: L0 README has the `metrics` block (or the `(Pending EXT-04)` placeholder); L1-L4 do not.
- **DOC-020**: L0 README has the `cell_charter` In Scope / Out of Scope / Adjacent table populated (or the placeholder if no cell_charter).

### 2.2 Implementation

The validator is a pure-stdlib Python script (no third-party deps). It walks `entities/v1-alpha/` and `contexts/v1-alpha/` (the CR-BP-mv1 containment tree), reads each `README.md` and the corresponding YAML record, and emits findings as a JSON file at `reconciliation/validation-findings.json`.

The validator uses the same `PROFILE_REGISTRY` and `EXPECTED_HEADINGS` as `scripts/check_documentation_profile.py` (the existing gate). The new DOC-016..020 findings are additive to DOC-001..005 (which are already gated).

### 2.3 Output

```json
{
  "validation_findings": [
    {
      "record_id": "processes:pc-ao-activate-kusw2u",
      "level": "L0",
      "rule": "DOC-019",
      "severity": "advisory",
      "summary": "L0 record has no `metrics` block; renders (Pending EXT-04) placeholder",
      "yaml_field": "metrics",
      "remediation": "Author the KPI / KRI / KCI metrics under EXT-04 + EXT-06.",
    }
  ],
  "summary": {
    "total_records": 3723,
    "by_rule": {
      "DOC-016": 0,
      "DOC-017": 12,
      "DOC-018": 8,
      "DOC-019": 49,
      "DOC-020": 49
    }
  }
}
```

---

## 3. Conformance Gate ([N] Documentation Profile - Generator and Validator)

The new gate is wired into `scripts/conformance_result.py` as gate [N] where N is the next free slot after the existing gates (21 = Documentation Profile, advisory; 22+ are the next slots). The gate reads `reconciliation/validation-findings.json` and emits a per-rule tally.

The gate is **advisory** per the EXT-01 section 3 pattern: findings are surfaced but do NOT block merge. The blocking posture is the user's call (post-EXT-06 completion; per the user directive 2026-10-17 "We need to wire this in to the development model" the development model is the standing workflow; the blocking posture flips when sufficient README assets have been authored under EXT-06).

---

## 4. Test Plan

The validator has 5 unit tests in `tests/test_validate_readme_structure.py`:

1. `test_doc016_all_sections_present` - L0 + L1-L4 records all have the EXT-07 section IDs.
2. `test_doc017_properties_table_populated` - the Properties table has at least one row per record.
3. `test_doc018_relationships_table_populated` - the Relationships table is present (rows may be empty for L0 with no decomposes / part_of).
4. `test_doc019_metrics_placeholder_or_block` - L0 records have either a `metrics` block or the `(Pending EXT-04)` placeholder.
5. `test_doc020_cell_charter_table_or_placeholder` - L0 records have either the cell_charter table or the placeholder.

End-to-end: the validator runs against the live catalog and emits `validation-findings.json`. The conformance gate reads the JSON and emits a per-rule tally.

---

## 5. Acceptance Criteria

- **AC-01**: `scripts/validate_readme_structure.py` lands; the validator emits findings against the EXT-07 documentation profile.
- **AC-02**: The validator walks the live catalog (3,723 records) in <30 seconds.
- **AC-03**: The conformance gate ([N] Documentation Profile - Generator and Validator) is wired into `scripts/conformance_result.py` as advisory.
- **AC-04**: The DOC-016..020 findings tally is published at `reconciliation/validation-findings.json`.
- **AC-05**: 5+ unit tests pass.
- **AC-06**: D-004 clean on the new validator and test code.
- **AC-07**: 118a/118b/118c/123/124/125/126/127/128/129/130/131/132 + CR-BP-94-EXT-07 gates remain CONFORMANT.
- **AC-08**: The validator output is the input for the EXT-05 (decomposition reconciliation) slice, per the user directive 2026-10-17 ("Ext-05 should be actioned once we have Ext 04. We need to wire this in to the development model").

---

## 6. Dependencies + Enables Chain

**Depends on**:

- CR-BP-94-EXT-07 (README Template Consolidation; PR #177, OPEN) - the template must be final
- CR-BP-94-EXT-03 (manifest schema; separate CR, NOT in this programme) - the validator emits against a manifest format; the manifest schema is in EXT-03

**Enables**:

- **CR-BP-94-EXT-05** (decomposition reconciliation) - the validator output is the input for EXT-05; user directive 2026-10-17: "Ext-05 should be actioned once we have Ext 04. We need to wire this in to the development model"
- **CR-BP-94-EXT-06** (pilot + rollout) - the 2,306 advisory findings that the validator surfaces are the rollout surface for EXT-06

**External (NOT in this CR)**:

- **CR-BP-94-EXT-03** (manifest schema) - the validator's manifest format; the validator must be informed of the manifest shape; EXT-03 lands the manifest schema

---

## 7. Result

This CR lands the validator half of the EXT documentation workstream. The generator half is CR-BP-94-EXT-07 (PR #177). The validator emits DOC-016..020 findings against the EXT-07 documentation profile; the conformance gate surfaces the findings as advisory. The wire into the development model is the EXT-05 (decomposition reconciliation) follow-on, per the user directive 2026-10-17. D-004 clean. 118 series + entity-system gates CONFORMANT.
