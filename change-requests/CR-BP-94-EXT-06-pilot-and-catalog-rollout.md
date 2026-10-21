# CR-BP-94-EXT-06: Pilot and Catalog Rollout

**Status**: Accepted
**Layer**: Process Catalog (Cross-Cutting Documentation)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-17
**Parent**: CR-BP-94 (Decomposition Record Templates); CR-BP-94-EXT-07 (README Template, PR #177, OPEN); CR-BP-94-EXT-04 (Validation Pipeline, PR #177, OPEN); CR-BP-94-EXT-05 (Decomposition Reconciliation, PR #177, OPEN)
**Source**: User directive 2026-10-17 ("Let's address the README Restructure + Owner Section Removal, and in addition what is the situation with EXT-04 Backfilling? ... EXT-06 ... wire this in to the development model")
**Sub-pipeline position**: EXT-06 (post-EXT-04 + EXT-05; final slice of the EXT documentation workstream)
**Lands against**: 49 cell-roots + 3,674 record READMEs (3,723 total) + the L1 pilot record at `entities/v1-alpha/pr-improve/Customer-Insight-and-Retention/processes-group-pr-improve-zpb8e3.yaml`
**Dependencies**: CR-BP-94-EXT-07 (PR #177, OPEN) + CR-BP-94-EXT-04 (PR #177, OPEN) + CR-BP-94-EXT-05 (PR #177, OPEN)
**Gates**: moves gates [34] + [35] from ADVISORY to BLOCKING per the user directive 2026-10-17

---

## 1. Change Request

Land the **rollout** slice of the EXT documentation workstream. The three predecessor slices (EXT-07 generator, EXT-04 validator, EXT-05 decomposition reconciliation) all live in PR #177. This CR lands four things:

1. **L1 pilot re-attempt** under the new `profile` field (the unblock that CR-BP-94-EXT-07 added to the L1 schema).
2. **EXT-07 generator v2.1**: the L0 cell-root template now emits a Relationships table (process_groups + processes). The 49 L0 DOC-018 findings from EXT-04 drop to 0.
3. **EXT-07 generator v2.1**: the L1+ relation-key emission now uses `target_id` (the actual field name in `composes` list items). The L1 Relationships table now surfaces real target ids (no more `?`).
4. **Gate [34] + [35] move from ADVISORY to BLOCKING** in `scripts/conformance_result.py`. Per the user directive 2026-10-17 ("wire this in to the development model"). The conformance_result post-processor reads the manifest's `summary.total_findings` and fails the gate if findings > 0.

The 9 ACT-011 content backfills from CR-BP-99 section 3 are human content authoring; they are sequenced in a follow-up slice (not part of this generator-driven rollout).

---

## 2. L1 Pilot: `processes:group-pr-improve-zpb8e3`

The L1 pilot record at `entities/v1-alpha/pr-improve/Customer-Insight-and-Retention/processes-group-pr-improve-zpb8e3.yaml` (canonical id `processes:group-pr-improve-zpb8e3`) is augmented with the new `profile` field:

```yaml
process_group_kind: end-to-end
profile: l1-pilot-customer-insight-and-retention   # CR-BP-94-EXT-06 L1 pilot profile slug
status: accepted
```

The `profile` field is dea-catalog-processes-specific; the dea-metamodel canonical source is unchanged. The pilot is the proof that the L1 schema can host pilot records under the new `profile` field. The pilot record is admitted under the `profile` slug; the L1 schema is the carrier for the EXT-06 catalog-wide rollout.

---

## 3. EXT-07 Generator v2.1

The generator's `_properties_relationships()` function is updated to:

1. Add `process_groups` and `processes` to the recognized relation keys (L0 cell-root child fields).
2. Try `target_id` first, then `target`, then `id` when extracting a target id from a dict-typed relation item (L1+ `composes` lists use `target_id`; L0 `process_groups` use `id`).

After the patch + regeneration, the 3,723 READMEs are re-emitted:

- The 49 L0 cell-roots now have a Relationships table with `process_groups` (L1 child id) and `processes` (L2 child id) rows.
- The L1+ records now have populated target ids in their Relationships table (no more `?`).

The EXT-04 validator's live-catalog state confirms:

| Rule | Before EXT-06 | After EXT-06 |
|------|---------------|--------------|
| DOC-016 | 3 | 3 |
| DOC-017 | 0 | 0 |
| DOC-018 | 49 | **0** |
| DOC-019 | 0 | 0 |
| DOC-020 | 0 | 0 |
| **Total** | **52** | **3** |

The remaining 3 findings are the 3 unclassifiable `dea:contrib-*` records (DOC-016); they are not EXT-06 scope.

---

## 4. Gate Posture: ADVISORY -> BLOCKING

`scripts/conformance_result.py` is updated to:

1. Mark gates [34] and [35] as `blocking=True` in the GATES list.
2. Post-process the gate's return code: if the gate is blocking and the validator's manifest has `summary.total_findings > 0`, the gate's return code is flipped to 1 and the verdict line is annotated with the finding count.

This is the "wire into the development model" the user directed on 2026-10-17. The block is enforced at the gate level (not the validator level), so the validators can still be run independently with rc=0 for development workflows.

### Live-catalog gate state (after EXT-06)

| Gate | Pre-EXT-06 | Post-EXT-06 |
|------|------------|-------------|
| [34] EXT-04 Validation Profile | ADVISORY (52 findings) | **BLOCKING (3 findings)** |
| [35] EXT-05 Decomposition Reconciliation | ADVISORY (0 findings) | **BLOCKING (0 findings)** |
| Conformance verdict | CONFORMANT-WITH-WARNINGS | **NON-CONFORMANT (3 findings)** |

The 3 unclassifiable `dea:contrib-*` records (DOC-016) cause gate [34] to fail in strict mode. These records are out of scope for the EXT workstream; they are flagged for follow-up under a separate CR.

---

## 5. Acceptance Criteria

- **AC-01**: L1 pilot record `processes:group-pr-improve-zpb8e3` is augmented with the `profile` field. DONE.
- **AC-02**: L1 README for the pilot record is regenerated to the EXT-07 v2.1 template. DONE.
- **AC-03**: The EXT-04 validator findings are reconciled: DOC-018 drops from 49 to 0. DONE.
- **AC-04**: Gate [34] + [35] are moved from ADVISORY to BLOCKING in `scripts/conformance_result.py`. DONE.
- **AC-05**: The conformance_result post-processor reads the manifest's `summary.total_findings` and fails the gate if findings > 0. DONE.
- **AC-06**: 3,723 READMEs regenerated with the EXT-07 v2.1 template. DONE.
- **AC-07**: D-004 clean. DONE.
- **AC-08**: 118a/118b/118c/123/124/125/126/127/128/129/130/131/132 + EXT-02 + EXT-04 + EXT-07 + EXT-05 + EXT-06 gates remain CONFORMANT (in non-strict mode; in strict mode the 3 DOC-016 findings cause gate [34] to fail, which is the wire into the development model). DONE.

---

## 6. Dependencies + Enables Chain

**Depends on**:

- CR-BP-94-EXT-07 (README Template Consolidation; PR #177, OPEN) - the template final.
- CR-BP-94-EXT-04 (Validation Pipeline; PR #177, OPEN) - the manifest + gate [34].
- CR-BP-94-EXT-05 (Decomposition Reconciliation; PR #177, OPEN) - the manifest + gate [35].

**Enables**:

- The first stable release (T9.12, deferred per user directive 2026-10-15): the EXT-06 rollout is the prerequisite for the release.
- T9.13b cross-repo cascade: gates [34] + [35] are the cross-repo consistency check; the 11 sibling repos adopt the same generators + validators.

---

## 7. Status

This CR is **implemented** in PR #177 as the 5th commit. The L1 pilot unblock (the `profile` field) is added to the record. The EXT-07 generator v2.1 fix is applied; the 49 L0 DOC-018 findings are reconciled. Gates [34] + [35] are moved to BLOCKING. The 3 remaining DOC-016 findings (unclassifiable `dea:contrib-*` records) are flagged for follow-up.

D-004 clean. CR-BP-118 R1/R2 cardinal rules respected. 118 series + entity-system gates CONFORMANT. The wire into the development model is complete and enforced.
