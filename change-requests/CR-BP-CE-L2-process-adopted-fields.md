# CR-BP-CE-L2: Business Process Adopted-Fields Tranche (the 145 L2 records)

**Status**: Proposed
**Layer**: Process Catalog (Adopted-Field Population)
**Owner**: Emmanuel A. Otchere
**Depends on**: CR-BP-CE-0, CR-BP-CE-L0, CR-BP-CE-L1
**Companion to**: CR-BP-14, CR-BP-94-EXT-24

> **Scope.** This is the third level tranche of the completeness programme
> ratified under CR-BP-CE-0 §6 (item 4: "CR-BP-CE-L2 -- 145 Processes"). It
> lands the derivable and register-sourced L2 adopted fields. Post-tranche
> the gate [50] CE-L2 profile drops 580 -> **290 findings** (the deferred
> `actors`/`stakeholders` candidates); the programme total drops from
> 1,161 to **920** advisory findings (on the CE-L1 baseline).

---

## 1. Background

The CR-BP-CE-0 §3 L2 profile declares: `process_classification` adopted
(NEW, canonical block; legacy `process_type` retained until CR-BP-CE-RL
closure); `owner`, `actors`, `stakeholders` adopted (org-awareness fields;
candidates admitted per §5). The pre-tranche baseline: all 145 L2 records
missing `process_classification` (145 CE-L2-002) and the three
org-awareness fields (435 CE-L2-006 = 3 x 145).

## 2. What this tranche lands (normative)

### 2.1 `process_classification` (derivable; 145 CE-L2-002 -> 0)

The canonical classification block lands on every L2 record, derived from
the record's own legacy `process_type` (the schema-declared
backward-compatible alias; identical controlled vocabulary per
`classifications/process-types.yaml`). Per §5, derivable values land with
`status: active`, `type: migration`. The legacy `process_type` field is
RETAINED (per the profile: until CR-BP-CE-RL closure).

### 2.2 `owner` (knowledge-dependent; 145 of the CE-L2-006 -> proposed)

Each L2 record gains the owner candidate block carrying its EXT-24
ownership-register disposition: `value: awaiting_owner_confirmation`,
`status: proposed`, GOV-002 decision right, review due 2026-12-31. No owner
name is invented; the proposed -> confirmed transition is GOV-002's act.

### 2.3 `actors` / `stakeholders` (DEFERRED; 290 findings remain)

No evidence-bound source exists: the L3 Activity children carry no
responsibility/actor fields, and the EXT-24 ownership register carries no
actor or stakeholder data. Per §5 ("knowledge-dependent -> candidates")
and the D-004 discipline, inventing values is prohibited; the two fields
remain advisory findings (CE-L2-006) awaiting the human governance sweep,
explicitly recorded here as the CR-BP-CE-RL input.

### 2.4 The additive schema extensions

`schemas/entity.schema.json` (L2 Process):

- `process_classification` gains OPTIONAL `status` and `provenance`
  properties (`required: [type, provenance]`); zero pre-existing blocks
  exist, so the tightening is retro-safe. Back-compat: the block itself
  remains optional.
- `owner` becomes `oneOf [legacy plain string | candidate block]` -- the
  legacy plain-string form remains valid (backward compatible).

## 3. What is NOT changed

- No ProcessContext, ProcessGroup, Activity, or Task record is touched.
- On the 145 L2 records: `description`, `trigger`, `outcome`, `identity`,
  `context`, `relationships`, `process_specialization`, `links`,
  `metadata`, `ecfConformance`, and the legacy `process_type` are all
  untouched; the two new keys (`process_classification`, `owner`) are the
  only additions, inserted after the `process_type` anchor.
- No validator rule, gate registration, or template changes.
- No record is added or removed; the catalogue remains 3,723 records.

## 4. Verification

- All 145 L2 records validate against the extended `schemas/entity.schema.json`
  (Draft7 -- the exact CI dispatch).
- `python scripts/check_completeness.py` -- CE-L2: 580 -> **290**
  (145 CE-L2-002 + 145 owner CE-L2-006 resolved); 0 blocking; programme
  total 1,161 -> **920** advisory.
- `reconciliation/completeness-report.yaml` regenerated (adoption
  counters: `process_classification` 0 -> 145; `owner` 49 -> 194).

## 5. Out of scope / next steps

1. **The actors/stakeholders governance sweep** -- the human/CR-BP-CE-RL
   input for the remaining 290 CE-L2-006 findings.
2. **CR-BP-CE-L3/L4** -- the Activity/Task tranches (the remaining advisory
   findings).
3. **CR-BP-CE-RL** -- flip gate [50] to strict once the level tranches and
   the governance sweep close.

**D-004 clean.**
