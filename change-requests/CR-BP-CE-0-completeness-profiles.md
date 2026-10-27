# CR-BP-CE-0: Catalog Completeness Programme — Profiles, Gate, and Tranche Sequence

**Status**: Proposed
**Layer**: Process Catalog (Cross-Cutting Documentation)
**Owner**: Emmanuel A. Otchere
**Depends on**: CR-BP-106

## Status

| Field | Value |
|---|---|
| CR id | CR-BP-CE-0 (umbrella for CR-BP-CE-L1..L4, CR-BP-CE-RL) |
| Status | draft (awaiting maintainer ratification) |
| Type | additive + governance (no semantic rewrites of existing entries) |
| Scope | whole `entities/v1-alpha/` tree + `contributions/processes/` |
| Related | CR-BP-03 (architecture), CR-BP-14 (semantics), CR-BP-44 (L3 decomposition), CR-BP-94-EXT-* (methodology) |

## §2 Motivation

The catalog schema (`schemas/entity.schema.json`, 25 properties) is materially ahead of the data: 7 operational fields (`owner`, `stakeholders`, `actors`, `kpis`, `services_provided`, `components_involved`, `specialization_pattern`) are unpopulated in every record; 14 of 17 relationship types are never exercised; and one canonical form (`process_classification`) is unadopted. "Completeness" is currently undefined per level — this CR ratifies it.

## §3 Completeness profiles (normative)

"Complete" means: **every field in the level's profile is present, non-empty, and evidence-consistent**. Fields not in a level's profile are *prohibited* at that level (existing deliberate omissions — e.g. `type`/`version` on L1 PCs — are reaffirmed, not fixed).

### L1 — Process Context (49 records)

| Field | Status | Rule |
|---|---|---|
| `id`, `domain`, `lifecycle_stage`, `name` | required | already canonical (id system gate) |
| `definition` | required | non-empty; references absorbed domains where applicable |
| `scope.includes` / `scope.excludes` | required | >=3 each; boundary statements must name the *neighbor cell* absorbing each exclusion (CE-L1-003) |
| `outcomes` | required | >=3; each begins with a state-change verb phrase |
| `adjacent_contexts` | required | exactly the 4 same-domain adjacent-stage PC ids — **bidirectional**: each adjacent PC must reciprocally list this cell (CE-L1-004) |
| `processes[]` | required | must equal the set of L3 records physically located under this cell (cross-checked with the allocation matrix job) |
| `cell_charter` | required | all 7 sub-fields present and consistent with `scope` + `outcomes` (duplicated content must not drift — CE-L1-005) |
| `lifecycle_status`, `status`, `established_by/at`, `change_history[]`, `links[]` | required | every record carries >=1 CR `links` entry |
| `type`, `version`, `process_intent`, `process_audience` | prohibited | reaffirms the mv1 PC profile |

### L2 — Process Group (49 records)

| Field | Status | Rule |
|---|---|---|
| `id`, `name`, `type`, `version` | required | |
| `description` | required | states the grouping *basis* (what makes these L3s a group — not a restatement of the cell) |
| `context` | required | >=1 `ref:` to the parent PC |
| `relationships` | required | >=N `composes` instances, one per child L3, with provenance (CE-L2-002) |
| `owner` | required | knowledge-dependent -> admitted as `status: proposed` candidate during tranche (see §5) |
| `metadata.scope` | required | L0 scope reference consistent with the parent PC's `scope.includes` |

### L3 — Business Process (140 records)

| Field | Status | Rule |
|---|---|---|
| Schema-required 5 (`id`, `name`, `type`, `version`, `process_intent`) | required | canonical intent vocabulary only (no `operational`/`management` aliases) |
| `process_classification` | required (NEW adoption) | canonical block; legacy `process_type` retained until CR-BP-CE-RL closure |
| `context` | required | >=1 PC ref; multi-context only where BP-SEM-012 evidence exists |
| `trigger`, `outcome`, `identity.*` | required | BP-ARC-ID-001..005 already enforced |
| `relationships` | required | >=1 `realizes` + >=1 `serves`; `composes` toward parent group |
| `owner`, `actors`, `stakeholders` | required | org-awareness fields; candidates admitted per §5 |
| `kpis` | recommended | >=2; flagged, not blocked, when empty (CE-L3-006) |
| `services_provided`, `components_involved` | recommended | >=1 each where the process is externally observable |
| `specialization_pattern` | recommended | when `process_specialization` non-empty |
| `capabilities_delivered` | prohibited | soft-deprecated (BP-MIG-002) |

### L4 — Activity (560) / Task (2,800)

| Field | Status | Rule |
|---|---|---|
| `id`, `name`, `type`, `version` | required | |
| `trigger`, `outcome` | required | template-derived from parent L3 identity; must not merely restate the parent (CE-L4-002: leaf-specificity check) |
| `relationships` | required | >=1 `composes` to parent; task->activity `flows-to` chain where sequential semantics are established |
| Task verb | fixed | the 5 standard verbs only (intake/record/transform/confirm/verify) — no enrichment may alter |
| `actors` | recommended | |
| L2/L3-only fields (`kpis`, `process_classification`, ...) | prohibited at L4 | |

## §4 New gate: `scripts/check_completeness.py`

Runs in CI (`.github/workflows/catalog-conformance.yml`), PR-scoped:

| Rule | Check |
|---|---|
| CE-000 | record's level is inferable (id family + placement); profile applied accordingly |
| CE-1xx/2xx/3xx/4xx | per-level profile rules above |
| CE-900 | summary artifact `reconciliation/completeness-report.yaml`: per-level, per-domain completeness % — baseline for the tranche sequence |
| Mode | `--advisory` for the first N PRs (report-only), `--strict` after CR-BP-CE-L1 lands |

New MECE validator (separate, CR-BP-CE-RL): `scripts/check_relationship_consistency.py` — rejects overlapping `composes`/`flows-to`/`produces` assertions between the same pair and dangling relationship targets.

## §5 Provenance policy for generated values (critical)

All programme-generated field values land with explicit provenance:

```yaml
provenance:
  type: inference          # or discovery | migration | manual
  asserted_by: dea-completeness-programme
  asserted_at: '2026-10-26'
  reference: change-requests/CR-BP-CE-0-completeness-profiles.md
```

- Knowledge-dependent fields (`owner`, `actors`, `stakeholders`, `kpis`) land with `status: proposed`; the completeness report marks them **candidate — awaiting ratification**.
- Derivable fields (classification blocks, `context` refs, structural `composes`) land with `status: active`, `type: migration`.
- No generated value may satisfy `identity.evidence_links` (BP-ARC-ID-005 remains human/evidence-bound).

## §6 Tranche sequencing (dependency-ordered)

1. **CR-BP-CE-L1** — land this CR + gate in advisory mode; 49 L1 batches.
2. **CR-BP-CE-L2** — 49 group records; uses L1 charters for grouping-basis derivation.
3. **CR-BP-CE-L3** — 140 processes; 7 per-domain sub-tranches (pilot: `pr-`); gate -> strict for L1/L2.
4. **CR-BP-CE-L4** — 3,360 activity/task records; templated from landed L3 identities.
5. **CR-BP-CE-RL** — cross-level relationship graph (`flows-to`, `produces`/`consumes`), MECE validator, closure audit.

## §7 Landing conventions

- Completeness contributions are batch files under `contributions/processes/ce-l1-<cell>.yaml` (one per ECF cell), diff-style: only fields that change are asserted.
- PR slicing: one PR per ECF domain (7 PRs per tranche) to keep review burden manageable.
- Every batch carries a `cr:` reference to its tranche CR (CR Metadata Gate).
