# CR-BP-CE-0: Catalog Completeness Programme -- Profiles, Gate, and Tranche Sequence

**Status**: Proposed
**Layer**: Process Catalog (Cross-Cutting Documentation)
**Owner**: Emmanuel A. Otchere

> **Reconciliation (recon 2026-10-22, against the live canonical schemas and the
> 3,723-record population).** This CR is the user-submitted draft, reconciled to
> the canonical schemas under `schemas/entities/*.schema.json` and
> `schemas/entity.schema.json` (the authoritative surfaces). The draft's intent
> is preserved; its schema-level errors are corrected, and every correction is
> recorded in `§R Reconciliation` so the divergence is auditable, not silent.
> The seven corrections that change normative content are flagged there.

---

## §R Reconciliation (normative -- read before §3)

The draft was authored against a partially assumed schema. Measured against the
canonical schemas and the live population on 2026-10-22, seven corrections are
required. The gate in §4 is built against the RECONCILED profiles, not the
draft text.

- **R1 -- Level model.** The draft numbers the levels L1-L4. The canonical model
  is L0-L4, and existing gates (id system, EXT-05 decomposition, EXT-19/20/21
  inventories) already enforce it. The mapping is: draft L1 -> canonical
  **ProcessContext (L0)**; draft L2 -> **ProcessGroup (L1)**; draft L3 ->
  **Process (L2)**; draft L4 conflates two canonical levels, **Activity (L3)**
  and **Task (L4)**. The gate is level-aware by record TYPE, not by the L-number,
  so the numbering difference is a display concern only.
- **R2 -- Stale counts.** The draft cites 140 Process / 560 Activity / 2,800 Task.
  The live population is 145 / 580 / 2,900. The difference is exactly the
  CR-BP-106 regulator-tied tranche (5 BPs + 20 Activities + 100 Tasks), which
  post-dates the draft.
- **R3 -- ProcessGroup field names.** The draft profiles ProcessGroup with
  `context`, `description`, `relationships[]`, and `metadata.scope`. The
  canonical schema declares `process_context`, `definition`, top-level
  `composes`, and top-level `scope`. The gate uses the canonical names.
- **R4 -- Activity trigger/outcome.** The draft's L4 profile requires
  `trigger`/`outcome` on Activity. The canonical `activity.schema.json` does NOT
  declare these; only `task.schema.json` does. The requirement is removed from
  the Activity profile and retained on Task.
- **R5 -- Relationship vocabulary.** The draft says "14 of 17 relationship types
  are never exercised." The canonical `entity.schema.json` enumerates 17 types;
  only 2 are exercised (`serves` 150, `realizes` 1), so **15 of 17** are dormant.
  Separately, `composes` is a top-level field on 629 records, distinct from the
  `relationships[]` array.
- **R6 -- Workflow name.** The draft's §4 names a `catalog-conformance.yml`
  workflow that does not exist. The gate actually runs through the aggregate
  `conformance_result.py` step in `.github/workflows/ci.yml`, where it is
  registered as advisory gate [50].
- **R7 -- CE-900 was not delivered as specified.** §4 requires the summary
  artifact to carry "per-level, per-domain completeness %". The landed gate
  emitted per-level counts and a per-domain *finding count* only, and that
  finding count was attributed with a narrower domain resolution than the
  denominator it was meant to divide. **3,674 of 3,723 records carry no
  top-level `domain`** (every ProcessGroup, Process, Activity, and Task);
  their domain is only reachable through
  `ecfConformance.canonicalReferences[0].domain`, which resolves all 3,674.
  The finding counter did not use that fallback, so **870 of 871 findings were
  attributed to the pseudo-domain `?`** and the per-domain signal that the
  tranche sequence uses to prioritise was unusable. The per-domain denominator
  was computed and then dropped from the report. This slice fixes the
  resolution (one `domain_of()` helper, used by both counters) and emits the
  per-domain totals and completeness percentages that CE-900 actually
  specifies.

Two draft claims were verified CORRECT and are adopted as the programme's core
thesis: the seven operational fields (`owner`, `stakeholders`, `actors`,
`kpis`, `services_provided`, `components_involved`, `specialization_pattern`)
are declared in `entity.schema.json` but populated in **0 of 3,723** records;
and `process_classification` is declared but populated in **0** records (the
legacy `process_type` is populated in 145).

---

## §1 Status

| Field | Value |
|---|---|
| CR id | CR-BP-CE-0 (umbrella for CR-BP-CE-L0..L4, CR-BP-CE-RL; numbering reconciled by CR-BP-CE-REC-1) |
| Status | draft (awaiting maintainer ratification) |
| Type | additive + governance (no semantic rewrites of existing entries) |
| Scope | whole `entities/v1-alpha/` tree + `contributions/processes/` |
| Related | CR-BP-03 (architecture), CR-BP-14 (semantics), CR-BP-44 (L3 decomposition), CR-BP-94-EXT-* (methodology) |


> **Numbering reconciliation (CR-BP-CE-REC-1).** This CR was originally
> drafted with the levels numbered L1..L4. The canonical model is L0..L4
> (Process Context = L0), which the gate rule ids and the landed tranche
> CRs (CR-BP-CE-L0/L1/L2/L4) follow. The labels, rule references, and
> population counts in this document are reconciled to the canonical
> model; no normative profile content changes.


## §2 Motivation

The catalog schema (`schemas/entity.schema.json`, 25 properties) is materially
ahead of the data: of the schema's properties, 7 operational fields (`owner`,
`stakeholders`, `actors`, `kpis`, `services_provided`, `components_involved`,
`specialization_pattern`) are unpopulated in every record; 15 of 17 relationship
types are never exercised in the `relationships[]` array; and one canonical form
(`process_classification`) is unadopted. "Completeness" is currently undefined
per level -- this CR ratifies it.

Measured baseline (recon 2026-10-22): against the canonical per-level schemas'
own `required` lists, the catalogue is 100% complete at ProcessGroup, Process,
Activity, and Task. The only schema-required gaps are **8 ProcessContext
records** -- all escape-clause Activate/Retire cells -- missing
`adjacent_contexts`, `definition`, `outcomes`, `scope` (and 7 of the 8 missing
`status`). The completeness deficit is therefore concentrated in (a) those 8
ProcessContext records and (b) the optional/adopted fields the schemas declare
but nothing populates.

## §3 Completeness profiles (normative)

"Complete" means: **every field in the level's profile is present, non-empty, and evidence-consistent**. Fields not in a level's profile are *prohibited* at that level (existing deliberate omissions — e.g. `type`/`version` on L0 PCs — are reaffirmed, not fixed).

### L0 — Process Context (49 records)

| Field | Status | Rule |
|---|---|---|
| `id`, `domain`, `lifecycle_stage`, `name` | required | already canonical (id system gate) |
| `definition` | required | non-empty; references absorbed domains where applicable |
| `scope.includes` / `scope.excludes` | required | >=3 each; boundary statements must name the *neighbor cell* absorbing each exclusion (CE-L0-003) |
| `outcomes` | required | >=3; each begins with a state-change verb phrase |
| `adjacent_contexts` | required | exactly the 4 same-domain adjacent-stage PC ids — **bidirectional**: each adjacent PC must reciprocally list this cell (CE-L0-004) |
| `processes[]` | required | must equal the set of L2 records physically located under this cell (cross-checked with the allocation matrix job) |
| `cell_charter` | required | all 7 sub-fields present and consistent with `scope` + `outcomes` (duplicated content must not drift — CE-L0-005) |
| `lifecycle_status`, `status`, `established_by/at`, `change_history[]`, `links[]` | required | every record carries >=1 CR `links` entry |
| `type`, `version`, `process_intent`, `process_audience` | prohibited | reaffirms the mv1 PC profile |

### L1 — Process Group (49 records)

| Field | Status | Rule |
|---|---|---|
| `id`, `name`, `type`, `version` | required | |
| `description` | required | states the grouping *basis* (what makes these L2 children a group — not a restatement of the cell) |
| `context` | required | >=1 `ref:` to the parent PC |
| `relationships` | required | >=N `composes` instances, one per child L2 process, with provenance (CE-L1 required-fields family) |
| `owner` | required | knowledge-dependent -> admitted as `status: proposed` candidate during tranche (see §5) |
| `metadata.scope` | required | L0 scope reference consistent with the parent PC's `scope.includes` |

### L2 — Business Process (145 records)

| Field | Status | Rule |
|---|---|---|
| Schema-required 5 (`id`, `name`, `type`, `version`, `process_intent`) | required | canonical intent vocabulary only |
| `process_classification` | adopted (NEW) | canonical block; legacy `process_type` retained until CR-BP-CE-RL closure |
| `context` | required | >=1 PC ref; multi-context only where evidence exists |
| `trigger`, `outcome`, `identity.*` | required | identity block per `entity.schema.json` (`verb`, `object`, `outcome_statement`) |
| `relationships` | required | >=1 `realizes` + >=1 `serves`; `composes` toward parent group |
| `owner`, `actors`, `stakeholders` | required | org-awareness fields; candidates admitted per §5 |
| `kpis` | recommended | >=2; flagged, not blocked, when empty (CE-L2-006) |
| `services_provided`, `components_involved` | recommended | >=1 each where the process is externally observable |
| `specialization_pattern` | recommended | when `process_specialization` non-empty |
| `capabilities_delivered` | prohibited | soft-deprecated (BP-MIG-002) |

### L3 — Activity (580) / L4 — Task (2,900)

| Field | Status | Rule |
|---|---|---|
| `id`, `name`, `type`, `version` | required | |
| `trigger`, `outcome` | required | template-derived from parent L3 activity identity; must not merely restate the parent (CE-L4-002: leaf-specificity check) |
| `relationships` | required | >=1 `composes` to parent; task->activity `flows-to` chain where sequential semantics are established |
| Task verb | fixed | the 5 standard verbs only (intake/record/transform/confirm/verify) — no enrichment may alter |
| `actors` | recommended | |
| L2-only fields (`kpis`, `process_classification`, ...) | prohibited at L4 | |

## §4 New gate: `scripts/check_completeness.py`

Runs in CI via the `conformance_result.py` gate registry (gate [50], advisory; `.github/workflows/ci.yml`), PR-scoped:

| Rule | Check |
|---|---|
| CE-000 | record's level is inferable (id family + placement); profile applied accordingly |
| CE-0xx/1xx/2xx/3xx/4xx | per-level profile rules above (L0..L4) |
| CE-900 | summary artifact `reconciliation/completeness-report.yaml`: per-level, per-domain completeness % — baseline for the tranche sequence |
| Mode | `--advisory` for the first N PRs (report-only), `--strict` after the level tranches land (CR-BP-CE-RL) |

New MECE validator (separate, CR-BP-CE-RL):
`scripts/check_relationship_consistency.py` -- rejects overlapping
`composes`/`flows-to`/`produces` assertions between the same pair and dangling
relationship targets.

## §5 Provenance policy for generated values (critical)

All programme-generated field values land with explicit provenance:

```yaml
provenance:
  type: inference          # or discovery | migration | manual
  asserted_by: dea-completeness-programme
  asserted_at: '2026-10-22'
  reference: change-requests/CR-BP-CE-0-completeness-profiles.md
```

- Knowledge-dependent fields (`owner`, `actors`, `stakeholders`, `kpis`) land
  with `status: proposed`; the completeness report marks them
  **candidate -- awaiting ratification**.
- Derivable fields (classification blocks, `context` refs, structural
  `composes`) land with `status: active`, `type: migration`.
- No generated value may satisfy `identity.evidence_links`; evidence stays
  human/evidence-bound.

## §6 Tranche sequencing (dependency-ordered)

1. **CR-BP-CE-L0** — 8 escape-clause ProcessContext repairs (MERGED, PR #202).
2. **CR-BP-CE-L1** — 49 ProcessGroup owner candidates (MERGED, PR #204).
3. **CR-BP-CE-L2** — 145 Processes; classification + owner candidates (MERGED, PR #206).
4. **CR-BP-CE-L4** — custodian vocabulary normalization, 580 Tasks (MERGED, PR #208).
5. **CR-BP-CE-RL** — cross-level relationship graph (`flows-to`, `produces`/`consumes`), MECE validator, closure audit.

## Next steps

1. Land this reconciliation of CR-BP-CE-0 (R1-R7) with the per-domain
   reporting fix in `scripts/check_completeness.py`.
2. Open CR-BP-CE-L3 (580 Activity records; leaf-specificity audit).
3. Open CR-BP-CE-L4 (2,900 Task records; the 5-phase custodian vocabulary
   audit).
4. Open CR-BP-CE-RL (cross-level relationship graph + the MECE relationship
   validator `scripts/check_relationship_consistency.py`).
5. Flip the gate to `--strict` once the adopted-field tranches have landed and
   the remaining advisory findings are dispositioned.
