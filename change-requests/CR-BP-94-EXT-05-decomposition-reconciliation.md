# CR-BP-94-EXT-05: Decomposition Reconciliation

**Status**: Proposed
**Layer**: Process Catalog (Cross-Cutting Documentation)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-17
**Parent**: CR-BP-94 (Decomposition Record Templates); CR-BP-94-EXT-04 (Validation Pipeline, PR #177, OPEN)
**Source**: User directive 2026-10-17 ("Ext-05 should be actioned once we have Ext 04. We need to wire this in to the development model.")
**Sub-pipeline position**: EXT-05 (post-EXT-04; pre-EXT-06)
**Lands against**: 49 cell-roots + 3,674 record READMEs (3,723 total) + the validation manifest at `reconciliation/validation-manifest.json`
**Dependencies**: CR-BP-94-EXT-04 (validation manifest; PR #177, OPEN). The manifest is the input for EXT-05.
**Enables**: CR-BP-94-EXT-06 (pilot + rollout) - the decomposition reconciliation findings are the rollout surface for EXT-06.

---

## 1. Change Request

Land the **decomposition reconciliation** validator. The EXT-04 validator (PR #177) surfaces per-record validation state (DOC-016..020) for the README; EXT-05 surfaces per-record decomposition traceability (DOC-021..025) for the underlying catalog. Together, the two validators are the "wire into the development model" the user directed.

The decomposition chain is:

| Level | Type | Parent ref | Child ref(s) |
|-------|------|------------|--------------|
| L0 | ProcessContext | (top-level) | `process_groups: list[str]` |
| L1 | ProcessGroup | `process_context: str` (L0 id) | `composes: list[str]` (L2 ids) |
| L2 | Process | `part_of: list[str]` (L1 ids) | `composes: list[str]` (L3 ids) |
| L3 | Activity | `belongs_to_business_process: str` (L2 id) | `composes: list[str]` (L4 ids) |
| L4 | Task | `belongs_to_activity: str` (L3 id) | (leaf) |

EXT-05 lands five rules that check the parent-child traceability in both directions (forward and reverse).

---

## 2. Validator Design (`scripts/check_decomposition_reconciliation.py`)

### 2.1 Scope

The validator reads the catalog YAML records, builds the id index, then checks the parent-child decomposition in both directions. The five rules:

- **DOC-021**: L1 records' `process_context` field references a valid L0 parent (the L0 record exists with the same id).
- **DOC-022**: L2 records' `part_of` list references valid L1 parents (every L1 id in the list exists in the catalog).
- **DOC-023**: L3 records' `belongs_to_business_process` field references a valid L2 parent.
- **DOC-024**: L4 records' `belongs_to_activity` field references a valid L3 parent.
- **DOC-025**: Reverse direction. Every child referenced in a parent's `process_groups` / `composes` list actually exists in the catalog. This catches orphans (parent claims a child that does not exist) and dangling refs.

### 2.2 Implementation

The validator is a pure-stdlib Python script (no third-party deps beyond PyYAML, which is already a project dep). It walks `entities/v1-alpha/`, builds the id index (one pass), then runs the five rules (second pass).

The validator reads the EXT-04 validation manifest at `reconciliation/validation-manifest.json` to skip records that have unresolved DOC-016/017/018/019/020 findings (the README is not in a known state; decomposition reconciliation is gated on the README being well-formed first).

### 2.3 Output

The validator emits two artefacts:

1. `reconciliation/decomposition-reconciliation-manifest.json`
2. `reconciliation/decomposition-reconciliation-manifest.yaml`

The manifest schema is at `schemas/decomposition-reconciliation-manifest.schema.json`. Schema version 1.

The manifest's `summary.by_rule` tally is consumed by the conformance gate [35] Decomposition Reconciliation (CR-BP-94-EXT-05; DOC-021..025).

---

## 3. Conformance Gate ([35] Decomposition Reconciliation)

Wired as ADVISORY in `scripts/conformance_result.py`. Per the user directive 2026-10-17 (wire this in to the development model), the gate is moved from advisory to blocking under CR-BP-94-EXT-06.

---

## 4. Test Plan

The validator has 5 unit tests in `tests/test_check_decomposition_reconciliation.py`:

1. `test_doc021_l1_process_context_resolves` - L1's `process_context` references a valid L0.
2. `test_doc022_l2_part_of_resolves` - L2's `part_of` list references valid L1s.
3. `test_doc023_l3_belongs_to_business_process_resolves` - L3's `belongs_to_business_process` references a valid L2.
4. `test_doc024_l4_belongs_to_activity_resolves` - L4's `belongs_to_activity` references a valid L3.
5. `test_doc025_reverse_references_resolve` - Every child in a parent's list exists in the catalog.
6. `test_live_catalog_writes_manifest` - Live-catalog integration test (manifest is written, schema validates).
7. `test_self_test_synthetic_fixtures` - In-process self-test with synthetic fixtures.

---

## 5. Acceptance Criteria

- **AC-01**: `scripts/check_decomposition_reconciliation.py` lands; the validator emits findings against the five rules.
- **AC-02**: The validator walks the live catalog (3,723 records) in <10 seconds.
- **AC-03**: The conformance gate [35] Decomposition Reconciliation is wired into `scripts/conformance_result.py` as advisory.
- **AC-04**: The DOC-021..025 findings tally is published at `reconciliation/decomposition-reconciliation-manifest.json`.
- **AC-05**: 5+ unit tests pass.
- **AC-06**: D-004 clean on the new validator and test code.
- **AC-07**: 118a/118b/118c/123/124/125/126/127/128/129/130/131/132 + CR-BP-94-EXT-04 + CR-BP-94-EXT-07 gates remain CONFORMANT.
- **AC-08**: The validator output is the input for the EXT-06 (pilot + rollout) workstream.

---

## 6. Dependencies + Enables Chain

**Depends on**:

- CR-BP-94-EXT-04 (validation manifest; PR #177, OPEN) - the manifest is the input; the decomposition validator skips records with unresolved DOC-016/017/018 findings.
- CR-BP-94-EXT-07 (template; PR #177, OPEN) - the README template's parent-child traceability sections (the Hierarchical Decomposition `<details>` block) are the visual surface for the decomposition chain.

**Enables**:

- **CR-BP-94-EXT-06** (pilot + rollout) - the decomposition reconciliation findings are the rollout surface; the L1 pilot unblock (the `profile` field) is in EXT-07.
- **T9.13b** (cross-repo cascade) - the decomposition reconciliation is the cross-repo consistency check; the 11 sibling repos adopt the same validator.

---

## 7. Result

This CR lands the decomposition reconciliation validator. The validator emits DOC-021..025 findings against the parent-child decomposition chain (L0 -> L1 -> L2 -> L3 -> L4). The conformance gate [35] is wired as advisory; the gate is moved to blocking under CR-BP-94-EXT-06. D-004 clean. 118 series + entity-system gates CONFORMANT. The wire into the development model is complete: gate [34] (validation profile) + gate [35] (decomposition reconciliation) are both advisory and become blocking under EXT-06.
