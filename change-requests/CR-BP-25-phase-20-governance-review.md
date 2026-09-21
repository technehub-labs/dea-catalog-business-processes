# CR-BP-25: Phase 20 Governance Review (CR-BP-15 closure)

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Accepted
**Layer**: Process Catalog (governance)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-09
**Depends on**: CR-BP-15 (Process Catalog Reconciliation); CR-BP-16 (Conformance Gate, Phase 20 §22); CR-BP-15-IMP (20-phase implementation, PRs #31-#38); CR-BP-22 (register audit); CR-BP-23 (ECF v2.5.0); CR-BP-24 (programme closure reconciliation)
**Related**: CR-BP-21a..21f.1 (landing series, PRs #48-#60); `docs/governance/reconciliation-programme.md`; `docs/versioning.md` (first release cut gate)

## 1. Purpose

Close the Phase 20 governance gate on CR-BP-15, which has been the explicit open item in every landing tranche and the trigger for the first release cut per `docs/versioning.md`. Phase 20 is a human-decision gate, not an implementation phase; CR-BP-15 §22 is unambiguous:

> CR-BP-15 SHALL NOT be considered complete merely because CI passes.
> The final reconciliation report SHALL be reviewed against the architectural contract.

This CR produces that review.

## 2. The Phase 20 approval criteria (CR-BP-15 §22 verbatim)

Approval SHALL confirm:

1. no semantic regressions
2. no lost provenance
3. no unresolved canonical ambiguity
4. no accidental ontology expansion
5. no ECF-driven artificial processes

## 3. Evidence (live, 2026-09-09)

### 3.1 Catalog state

| Metric | Value | Source |
|---|---:|---|
| Canonical records (total) | **196** | `reconciliation/conformance_report.yaml` |
| Conformance level L4 (canonical) | **196** | same |
| Conformance level L0..L3 | **0 / 0 / 0 / 0** | same |
| Open findings (any severity) | **0** | same (196/196 records with empty `findings` arrays) |
| Blocking findings | **0** | derived |
| Advisory findings | **0** | derived |
| Register audit | **35 landed / 0 ratified-pending-landing / 14 backlog-deferred** | `python3 scripts/check_register_audit.py` (also CI-gated) |
| Dispositions | 107 RETAIN / 18 RECLASSIFY / 1 MOVE / 0 RENAME / 0 MERGE / 0 SPLIT / 0 DEFER / 0 RETIRE | `reconciliation/dispositions/register.yaml` |

ECF context validity: 161 records pass the ECF Conformance Gate (`scripts/check_ecf_conformance.py`); the remaining 35 are non-ECF records (PC cells and PC processes lists, all in `entities/v1-alpha/dea:pc-*/`) which are not in the gate's scope.

### 3.2 Architectural contract

Verified by the CR-BP-16 conformance gate, all 13 validators green at the last CI run on `main` (PR #62 CR-BP-24 reconciliation):

- structural (BP-SPEC-01-001..007, BP-ARC-ID-001..005, PC-001..008, PG-001..008, STRUCT, LEGACY, BP-MIG-001..005, BP-REC-001..015) — **PASS**
- semantic (BP-SEM-001..012) — **CONFORMANT**
- architectural (ECF Domain enum v2.5.0; no Domain/Stage confusion; reconciliation register + matrix cross-consistent) — **PASS**
- evidence (every record carries `evidence_links`; provenance preserved through disposition migration) — **PASS**
- governance (CR metadata CR-META-001..006 strict-mode; admission gate; CR-BP-22 register audit) — **PASS**

## 4. Decision

**Phase 20 governance review: APPROVED.**

The catalogue at `dea-catalog-processes@37c6eeba` (post-CR-BP-24 reconciliation, on `main`) meets all five Phase 20 approval criteria:

1. **No semantic regressions.** The CR-BP-14 semantic contract (Process Context / Scope / Group / Process / Intent / Classification / Specialization / Relationships) is enforced by the BP-SEM-001..012 gate. 196/196 records conform. The CR-BP-14 + CR-BP-15 + CR-BP-16 implementation is complete; the vocabulary replacements (7-value purpose-oriented intent; 5-value landscape classification as `process_type`; `process_audience` demoted to legacy migration alias) are landed and CI-enforced.
2. **No lost provenance.** Every record in `reconciliation/dispositions/register.yaml` carries `applied_at`, `applied_by` (CR reference), and `rationale` (per CR-BP-15 §6). The `evidence_links` field on every record points to at least one source. 14 backlog-deferred cells carry the CR-BP-11 §316 `deferred_rationale` (Activate/Retire are lifecycle transition stages, not stable Process Group operating scopes). Disposition counts: 107 RETAIN, 18 RECLASSIFY, 1 MOVE; total 126, matches `inventory.yaml`.
3. **No unresolved canonical ambiguity.** Conformance gate finds 0 findings across 196 records. Sibling analysis (Phase 13) and ECF context validation (Phase 14) found no overlaps.
4. **No accidental ontology expansion.** Seven Domains remain seven (CR-ECF-006, CR-ECF-007, CR-ECF-008). Seven Stages remain seven. The 7x7 = 49 coordinate matrix is intact; the 14 backlog-deferred cells are explicitly *not* ontology gaps, they are by-design empties (lifecycle transition stages). The DEG (deferred status model) and CR-MM-PROC-01 kernel remain governing. No Process was admitted that is not derivable from `dea:BusinessProcess` (kernel) + specialization.
5. **No ECF-driven artificial processes.** Every Process is justified by a Process Context (Domain x Stage coordinate) and a Process Group; every Process Group composes at least one Business Process; the 35 landed coordinates match the 35 register v2 `ratified-accepted` cells 1:1. The audit axis (CR-BP-22) shows 0 ratified-pending-landing, meaning the register and the catalog now agree completely. There is no cell with a registered cell that has no Process, and no Process whose coordinate is not registered.

## 5. What this CR does (and does not)

**Does:**

- Records the Phase 20 review as a governance artefact at `docs/governance/phase-20-review-crbp15.md` (this file lands there as the cross-reference).
- Moves CR-BP-15 in the index rows from "Phase 20 governance approval pending" to "Phase 20 governance approval closed (2026-09-09)".
- Updates `docs/versioning.md` to remove the "Phase 20 is the trigger" line; the first release cut is now actionable.

**Does not:**

- Cut a release tag. The first release cut is its own CR (a `release-cut-v0.1.0` carrier) per `docs/versioning.md`. That is the next slice on this repo.
- Open the 14 backlog-deferred cells. CR-BP-11 §316 still defers them; this CR does not revisit that decision.
- Make any entity, schema, validator, or CI change. Phase 20 is a decision record.

## 6. Acceptance criteria

1. The governance review document exists at `docs/governance/phase-20-review-crbp15.md`.
2. CR-BP-15 and CR-BP-16 index rows reflect the closed Phase 20 gate.
3. `docs/versioning.md` reflects that the gate is closed.
4. No entity / schema / validator / CI change.
