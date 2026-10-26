# CR-BP-CE-L0: Process Context Completeness Tranche (the 8 escape-clause cells)

**Status**: Proposed
**Layer**: Process Catalog (Canonical Record Remediation)
**Owner**: Emmanuel A. Otchere
**Depends on**: CR-BP-CE-0
**Companion to**: CR-BP-81, CR-BP-78, CR-BP-101

> **Scope.** This is the first level tranche of the completeness programme
> ratified under CR-BP-CE-0 (`change-requests/CR-BP-CE-0-completeness-profiles.md`
> §6, item 2: "CR-BP-CE-L0 -- the 8 gappy ProcessContext records (the
> escape-clause cells)"). It lands the CE-L0 remediation: the 43 blocking
> findings (42 CE-L0-001 required-field gaps + 1 CE-L0-006 prohibited-field
> finding) on the 8 escape-clause ProcessContext records, plus the CE-L0-004
> bidirectionality closure of `adjacent_contexts` across the affected
> same-domain siblings. Post-tranche the gate [50] CE-L0 profile is at
> **0 blocking findings** across all 49 ProcessContext records.

---

## 1. Background

The 8 escape-clause ProcessContext records were admitted through the Option B
escape-clause discovery sequence (CR-BP-65, CR-BP-73, CR-BP-75, CR-BP-78,
CR-BP-80/81, CR-BP-101) carrying the admission-era field set:
`scope_summary` + `cell_charter` + `admission`, but **not** the canonical
L0 profile fields (`definition`, `scope`, `outcomes`, `adjacent_contexts`,
top-level `status`; and for 3 of the 8, top-level `processes`). One record
(`pc-sd-retire-zxnc3c`) additionally carried the prohibited `version` field
(CE-L0-006).

The CR-BP-CE-0 baseline (`reconciliation/completeness-report.yaml`, CE-900)
counted exactly these as the 43 blocking findings: **8 records across 7
coordinates** (ao-activate, ao-retire, eo-activate, fa-activate, fa-retire,
ge-retire, sd-activate, sd-retire).

## 2. What this tranche lands (normative)

### 2.1 The 8 record remediations (CE-L0-001)

For each of the 8 records, the canonical required fields are added at the
top level, in canonical schema order (`id, domain, lifecycle_stage, name,
definition, scope, outcomes, adjacent_contexts, processes, cell_charter,
status`), **derived from each record's own authoritative
`cell_charter` and `process_context.scope_summary`** -- no new semantic
content is invented; the charter prose is normalized into the canonical
field structure:

| Record | Coordinate | Fields added | Source of content |
|---|---|---|---|
| `processes:pc-ao-activate-kusw2u` | A&O x Activate | definition, scope, outcomes, adjacent_contexts, status | charter (CR-BP-81) |
| `processes:pc-ao-retire-3kqe9c` | A&O x Retire | definition, scope, outcomes, adjacent_contexts, status | charter (CR-BP-73) |
| `processes:pc-eo-activate-xdfscw` | E&O x Activate | definition, scope, outcomes, adjacent_contexts, processes, status | charter (CR-BP-65-era escape) |
| `processes:pc-fa-activate-yrhcfm` | F&A x Activate | definition, scope, outcomes, adjacent_contexts, processes, status | charter (escape) |
| `processes:pc-fa-retire-64q5p9` | F&A x Retire | definition, scope, outcomes, adjacent_contexts, status | charter (CR-BP-75) |
| `processes:pc-ge-retire-kndw6x` | G&E x Retire | definition, scope, outcomes, adjacent_contexts, status | charter (CR-BP-78) |
| `processes:pc-sd-activate-ghaub8` | S&D x Activate | definition, scope, outcomes, adjacent_contexts, processes, status | charter (escape) |
| `processes:pc-sd-retire-zxnc3c` | S&D x Retire | definition, scope, outcomes, adjacent_contexts, status; `version` REMOVED (CE-L0-006) | charter (CR-BP-101) |

Rules applied:

- **definition** -- a normative semantic definition (not a description),
  adapted from the record's own `combined_semantic_meaning` /
  `scope_summary`, naming the Domain x Lifecycle intersection and the
  distinct-from clauses.
- **scope.includes** -- derived from `cell_charter.inclusions` (condensed
  to the responsibility level, >=3 entries).
- **scope.excludes** -- derived from `cell_charter.exclusions`, each naming
  the neighbor cell absorbing the exclusion (CE-L0-003 convention).
- **outcomes** -- derived from `cell_charter.expected_outcomes`, each a
  state-change statement, >=3 entries (CE-L0-003b convention).
- **adjacent_contexts** -- the same-domain other-stage PC ids plus the
  cross-domain sibling cells the charter's `adjacent_boundaries` name.
- **processes** (3 records) -- the set of BP records under this cell's
  directory, already carried by `process_groups[]`; promoted to the
  top-level canonical field.
- **status** -- `candidate` per each record's `process_context.status`
  (the schema enum; no lifecycle-state change is made by this tranche).

### 2.2 The bidirectionality closure (CE-L0-004)

Because the 8 cells never carried `adjacent_contexts`, the same-domain
siblings (the conformant 41) could not reciprocally list them. This tranche
adds the reciprocal entries: **22 sibling records** gain 1-3 new
`adjacent_contexts` ids each. Every adjacency established in §2.1 is now
bidirectional: for each of the 8 cells and each of their listed adjacents,
the adjacent PC lists the cell back.

### 2.3 The prohibited-field removal (CE-L0-006)

`processes:pc-sd-retire-zxnc3c` carried `version: 1.0.0`, prohibited on
ProcessContext by the canonical profile (schema `additionalProperties:
false`; the PC has no version dimension). Removed. `CATALOG.yaml` is
regenerated: the record's index `version` normalizes `1.0.0 -> 0.0.0`,
consistent with the other 48 ProcessContext entries.

### 2.4 The gate admission (CR-META-006 reconciliation)

The tranche is named per the umbrella CR §6: `CR-BP-CE-L0`. The
`check_cr_metadata.py` CR-number pattern (CR-BP-16 S16) predated the
completeness-programme naming and did not admit the `CE-L<N>` form; the
pattern is extended additively (`CR-BP-CE-N`, `CR-BP-CE-LN`, with slug) so
the tranche CRs can land under their ratified names. No existing admitted
form changes.

## 3. What is NOT changed

- No Business Process, Process Group, Activity, or Task record is touched.
- No `cell_charter`, `admission`, `change_history`, `audit`,
  `process_context`, or `metadata` block on any record is modified.
- No schema, validator rule (other than the additive CR-number pattern
  above), gate registration, or template changes.
- No record is added or removed; the catalogue remains 3,723 records
  (49 L0 + 49 L1 + 145 L2 + 580 L3 + 2,900 L4).

## 4. Verification

- `python scripts/check_completeness.py` -- **0 blocking** findings
  (was 43), 1,210 advisory (unchanged; the advisory population is the
  CE-L1..L4 tranche target, not this slice).
- `python scripts/check_process_context.py` -- PASS (PC-001..PC-008).
- `python scripts/check_process_specialization.py` -- PASS.
- `python scripts/check_ecf_conformance.py` -- PASS (3,724 entries).
- `python scripts/check_id_system.py --strict` -- CONFORMANT.
- `python scripts/check_cr_metadata.py --strict` -- CONFORMANT (168 files).
- `python scripts/check_cr_readme.py --strict` -- CONFORMANT.
- `python scripts/regenerate_catalog.py --check` -- CATALOG.yaml current.
- `reconciliation/completeness-report.yaml` regenerated (CE-900 baseline
  post-tranche: 0 blocking).

## 5. Out of scope / next steps

1. **CR-BP-CE-L1** -- the 49 ProcessGroup `owner` adopted-field tranche
   (advisory findings, not blocking).
2. **CR-BP-CE-L2..L4** -- the per-level adopted-field tranches (the
   1,210 advisory findings).
3. **CR-BP-CE-RL** -- flip gate [50] to strict once all level tranches
   land.

Per CR-BP-CE-0 §6, the remaining tranches are generated mechanically from
the completeness report once this level-0 tranche is accepted.

**D-004 clean.**
