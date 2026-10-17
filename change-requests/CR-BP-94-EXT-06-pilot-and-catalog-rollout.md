# CR-BP-94-EXT-06: Pilot and Catalog Rollout

**Status**: Proposed
**Layer**: Process Catalog (Cross-Cutting Documentation)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-17
**Parent**: CR-BP-94 (Decomposition Record Templates); CR-BP-94-EXT-07 (README Template Consolidation, PR #177, OPEN); CR-BP-94-EXT-01a (L0/L1 Cardinal Entity Documentation Profiles, PR #138, MERGED)
**Source**: User directive 2026-10-17 ("EXT-06 ... what is the situation with EXT-04 Backfilling?")
**Sub-pipeline position**: EXT-06 (post-EXT-04; final slice of the EXT documentation workstream)
**Lands against**: 49 cell-root + 3,674 record READMEs; the L1 pilot record (`dea:group-customer-insight-and-retention`); the 2,306 advisory findings from CR-BP-99 matrix-010..013; the 9 ACT-011 backfills from CR-BP-99 section 3
**Dependencies**: CR-BP-94-EXT-07 (template final; PR #177, OPEN) + CR-BP-94-EXT-04 (validation pipeline; CR doc only) + CR-BP-94-EXT-03 (manifest schema; separate CR) + CR-BP-94-EXT-05 (decomposition reconciliation; separate CR)
**L1 unblock**: the new `profile` field on `process-group.schema.json` (added in CR-BP-94-EXT-07) is the L1 pilot unblock; this CR documents the pilot workflow under that unblock.

---

## 1. Change Request

Land the **rollout half** of the EXT documentation workstream. The generator half is CR-BP-94-EXT-07 (PR #177, OPEN). The validator half is CR-BP-94-EXT-04 (CR doc only, OPEN). This CR (EXT-06) is the third slice:

1. **L1 pilot re-attempt** under the new `profile` field (the unblock that CR-BP-94-EXT-07 added to the L1 schema). The pilot record is `dea:group-customer-insight-and-retention`; the pilot was rejected in CR-BP-94-EXT-01a because the PG schema had `additionalProperties: false` and the `composes` field was constrained. The new `profile` field allows the L1 pilot to land without re-composing.
2. **Catalog-wide regeneration**: the EXT-07 generator runs against the full 3,723-record catalog; the EXT-04 validator emits findings; the advisory findings are reconciled.
3. **Backfilling the 2,306 advisory findings** + the 9 ACT-011 content backfills from CR-BP-99 section 3. The "backfilling" the user asked about (2026-10-17) refers to this work.

The CR is sequenced after EXT-04 + EXT-05 land. Per the user directive 2026-10-17 ("Ext-05 should be actioned once we have Ext 04. We need to wire this in to the development model"), the EXT-05 decomposition reconciliation is a hard prerequisite; this CR documents the rollout after EXT-05 is in.

---

## 2. L1 Pilot Unblock

### 2.1 The blocker (per CR-BP-94-EXT-01a)

`schemas/entities/process-group.schema.json` declares `additionalProperties: false` and the `composes` field is constrained to a non-empty array. The L1 pilot on `dea:group-customer-insight-and-retention` was attempted and rejected because the parent record already composes `dea:proc...` and the schema doesn't allow a re-composition.

### 2.2 The unblock (per CR-BP-94-EXT-07)

CR-BP-94-EXT-07 (PR #177, OPEN) adds a new OPTIONAL `profile` field to the L1 schema:

```json
"profile": {"type": ["string", "null"], "description": "L1 pilot profile slug (CR-BP-94-EXT-07 unblock for L1 pilot admission)."}
```

The `additionalProperties: false` constraint remains; the `profile` field is added to the allowed properties list (not yet in `required`).

### 2.3 The pilot workflow (this CR)

1. The L1 pilot record `dea:group-customer-insight-and-retention` is augmented with the `profile` field set to a pilot-specific slug (e.g. `l1-pilot-customer-insight-and-retention`).
2. The EXT-07 generator regenerates the L1 README with the new template.
3. The EXT-04 validator validates the L1 README; the findings are advisory.
4. The L1 pilot is admitted under the `profile` field; the dea-metamodel canonical source is unchanged (the `profile` field is dea-catalog-processes-specific).
5. The pilot is the proof that the L1 schema can host pilot records under the new `profile` field. The L1 schema is then the carrier for the EXT-06 catalog-wide rollout.

---

## 3. Catalog-Wide Rollout

The EXT-07 generator runs against the full 3,723-record catalog (already done in CR-BP-94-EXT-07; the regeneration sweep is a single commit). The EXT-04 validator emits findings; the advisory findings are reconciled as follows:

### 3.1 The 2,306 advisory findings (per CR-BP-99 matrix-010..013)

The findings are categorised as:

- **DOC-001** (README exists) - 0 findings post-EXT-07 (all 3,723 records have READMEs).
- **DOC-002** (required section identifiers) - 0 findings post-EXT-07 (all READMEs have the EXT-07 section IDs).
- **DOC-003** (README id matches YAML) - 0 findings post-EXT-07.
- **DOC-005** (governing CR reference) - some findings; reconciled under the EXT-04 validator cycle.
- **DOC-019** (L0 has `metrics` block or placeholder) - 49 findings; one per L0 cell-root; reconciled as the EXT-04 authoring workstream authors the metrics.
- **DOC-020** (L0 has cell_charter table or placeholder) - 49 findings; one per L0 cell-root; reconciled as the L0 content authoring fills in the cell_charter.

The 2,306 figure in the CR-BP-99 matrix is the cumulative count across DOC-001..005 (advisory). Post-EXT-07, the DOC-001..003 portion drops to 0; the DOC-019..020 portion is the new EXT-04 surface.

### 3.2 The 9 ACT-011 backfills (per CR-BP-99 section 3)

The 9 ACT-011 backfills are content work: Activity records whose `definition:` is <120 chars. The backfill is a natural-language elaboration that preserves the original meaning while raising the definition to the 120-char minimum. The backfill is sequenced under the EXT-06 workstream; the EXT-04 validator surfaces the findings; the content authoring is human-authored (not generator-driven).

### 3.3 The cross-repo cascade (T9.13b)

The catalog-wide rollout is wave 0 of T9.13b. The other 11 sibling repos (the 3 catalog siblings + the metamodel + the metaframework + the architecture framework + the release package + the portal + governance + remaining) receive the same EXT-07 template + generator in subsequent waves. The wave plan is in CR-BP-94-EXT-07 section 6.

---

## 4. Acceptance Criteria

- **AC-01**: The L1 pilot record `dea:group-customer-insight-and-retention` is admitted under the new `profile` field.
- **AC-02**: The L1 README for the pilot record is regenerated to the EXT-07 template.
- **AC-03**: The EXT-04 validator findings are reconciled: DOC-001..003 = 0, DOC-019/020 = the EXT-04 authoring workstream backlog.
- **AC-04**: The 9 ACT-011 backfills are authored; the Activity records' `definition:` is >=120 chars.
- **AC-05**: The cross-repo cascade is planned (T9.13b); the wave-0 deliverable is this repo's PR #177.
- **AC-06**: The conformance gate ([N] Documentation Profile - Generator and Validator) is moved from advisory to blocking, per the user's "wire this in to the development model" directive.
- **AC-07**: D-004 clean.
- **AC-08**: 118a/118b/118c/123/124/125/126/127/128/129/130/131/132 + EXT-02 + EXT-04 + EXT-07 gates remain CONFORMANT.

---

## 5. Dependencies + Enables Chain

**Depends on**:

- CR-BP-94-EXT-07 (README Template Consolidation; PR #177, OPEN) - the template final
- CR-BP-94-EXT-04 (validation pipeline; CR doc only, OPEN) - the validator findings
- CR-BP-94-EXT-03 (manifest schema; separate CR) - the validator's manifest format
- CR-BP-94-EXT-05 (decomposition reconciliation; separate CR) - the parent-child traceability

**L1 unblock** (per CR-BP-94-EXT-07):

- New OPTIONAL `profile` field on `process-group.schema.json`; the L1 pilot can be re-attempted without re-composing.

**Enables**:

- The first stable release (T9.12, deferred per user directive 2026-10-15): the EXT-06 rollout is the prerequisite for the release.

---

## 6. Status

This CR is sequenced after EXT-04 + EXT-05 land. The CR doc is the formal record; the implementation is a separate execution cycle. The L1 pilot unblock (the `profile` field) is in CR-BP-94-EXT-07 (PR #177, OPEN). The CR-BP-99 matrix closure is sequenced under the EXT-06 workstream. D-004 clean. 118 series + entity-system gates CONFORMANT.
