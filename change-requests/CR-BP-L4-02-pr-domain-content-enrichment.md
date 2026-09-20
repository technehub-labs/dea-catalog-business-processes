# CR-BP-L4-02: PartyAndRelationship L4 Task Content Enrichment

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Proposed
**Layer**: L4
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-20
**Carrier**: First L4 content-enrichment slice (CR-BP-L4-01 reserved the population surface; CR-BP-L4-02..14 reserved the per-domain enrichment slices). Replaces the templated definition / trigger / outcome / responsibility / boundary / evidence content of every PartyAndRelationship L4 Task with cell-specific, sector-grounded prose describing the bounded work performed by each phase custodian.
**Depends on**: CR-BP-98 (Task schema + TASK-001..005 validator), CR-BP-102 (L4 Task decomposition pipeline; landed 2026-09-19, PR #146; produced 2,800 templated Tasks across 49 cells)
**Lands against**: 220 L4 Task records (44 PartyAndRelationship Activities x 5 phases) across 7 cells (Activate 20 / Build 40 / Conceive 40 / Design 60 / Improve 20 / Operate 20 / Retire 20); 29 conformance gates CONFORMANT; no record-count delta (in-place enrichment)

---

## 1. Change Request

Land cell-specific content for every PartyAndRelationship L4 Task. CR-BP-102 deposited 2,800 Tasks via a templated verb-object decomposition (Intake / Verify / Transform / Confirmation / Audit Record) carrying prose drawn from the parent Activity's cohesion rationale. CR-BP-L4-02 replaces that templated content with sector-grounded bounded-work prose per (stage, phase) cell pair, plus evidence[] drawn from the cell's governing-sector library.

**Per-cell surface:**

| Coordinate (domain / stage) | Cells | Activities | Tasks | Governing sector sources |
|---|---|---|---|---|
| PartyAndRelationship / Activate | 1 | 4 | 20 | FATF Rec 10 / 24 (CDD + beneficial ownership); FinCEN CDD Rule (31 CFR 1010.230); EU AMLD5/6; UK MLR 2017 Reg 33/35; PCI DSS 4.0 §3.2-3.5; OFAC SDN screening |
| PartyAndRelationship / Build | 1 | 8 | 40 | DAMA DMBOK2 §10 (Data Quality); MRC Attribution Standards 2023; GDPR Art 6/7 + ePrivacy PECR Reg 6 |
| PartyAndRelationship / Conceive | 1 | 8 | 40 | Osterwalder Value Proposition Canvas; Christensen Jobs-to-be-Done; Gartner Win-Loss primary research |
| PartyAndRelationship / Design | 1 | 12 | 60 | Bain Net Promoter System methodology; Nielsen Norman Group interaction-design foundations; Richardson touchpoint taxonomy |
| PartyAndRelationship / Improve | 1 | 4 | 20 | Gartner Subscriber Retention Benchmark 2024; Bain Loyalty Economics (Reichheld); Medallia VoC platform methodology |
| PartyAndRelationship / Operate | 1 | 4 | 20 | SAMA Strategic Account Management playbook; TSIA renewal execution benchmark; Gartner account-review cadence benchmark |
| PartyAndRelationship / Retire | 1 | 4 | 20 | Sarbanes-Oxley §802 records retention; GDPR Art 5(1)(e) storage limitation; IAOP outsourcing transition standards |
| **Total** | **7** | **44** | **220** |  |

The 7 cells form the complete PartyAndRelationship domain (P&R is the thinnest domain at 220 Tasks; the next domain (GovernanceAndExistence) is 340, scaling 13 enrichment slices CR-BP-L4-02..14 by total Task count).

## 2. Enrichment mechanics

1. **Generator script** (`scripts/enrich_l4_party_and_relationship.py`) walks every `entities/v1-alpha/dea:task-*/` directory, filters by `ecfConformance.canonicalReferences[0].domain == PartyAndRelationship`, derives the phase from the task-id suffix (`-intake` / `-verify` / `-transform` / `-confirm` / `-record`), and looks up the (stage, phase) bounded-work prose in the in-script `BOUNDED_WORK` table.
2. **Bounded-work prose** is keyed on (stage, phase): 35 distinct entries covering every (stage, phase) pair present in P&R. Each entry names the action taken by the named custodian, the artefact produced, and the custody transfer.
3. **Trigger / outcome / responsibility** are phase-specific, derived from the phase's predecessor and successor in the 5-phase pattern (intake -> verify -> transform -> confirm -> record). Custody transfers are named explicitly.
4. **Boundary inclusions / exclusions** are phase-specific, each entry naming the (stage, phase) work in human-readable terms. Exclusions name what is NOT this phase's work (e.g. phase 5 excludes re-execution of prior phases; phase 4 excludes notification outside the notify-list).
6. **Evidence[]** carries 3 entries per Task: two from the cell's `STAGE_EVIDENCE` library (the governing-sector sources for that stage) plus one citing the parent Activity's cohesion rationale (CR-BP-32 §6) and this enrichment CR. Strengths E1 (regulatory statute), E2 (industry benchmark), E3 (parent-rationale + CR provenance).
7. **BP-AR-004 capability-process avoidance** is asserted by test (defensive: no PartyAndRelationship Activity ends in `Capability`, so the edge case does not trigger; the assertion is defense-in-depth against future re-runs).
8. **Idempotence** is asserted by test (running the generator twice produces byte-identical output on all 220 P&R Task yaml files).
9. **Scope filter** (`--scope SUFFIX`) restricts generation to a subset for spot-checks; confirmed by test.
10. **Dry-run mode** (`--dry-run`) reports per-stage counts without touching the filesystem; useful for sizing future per-domain slices.

## 3. Gate posture

- Gate [29] L4 Task validation (CR-BP-98 TASK-001..005): **CONFORMANT, 2800 records, 0 findings**.
- Gate [15] L3 Activity model (CR-BP-32 ACT-001..010 + CR-BP-97 ACT-011..015): **CONFORMANT, 560 Activity records, 0 findings** (no Activity mutation in this slice).
- Gate [23] Architectural regression (CR-BP-16 S21; BP-AR-001..007): **CONFORMANT, no architectural regressions detected** (BP-AR-004 capability-process avoidance verified across all 2,800 Tasks).
- Gate [22] Reconciliation matrix (CR-BP-99 RCM-001..010): **CONFORMANT, 22 rows, 0 findings** (no row mutation in this slice; matrix_version unchanged).
- Full suite: **29 gates, 0 blocking, 0 advisory failures**.

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `scripts/enrich_l4_party_and_relationship.py` | NEW | 410-line deterministic generator; bounded-work table keyed on (stage, phase); per-stage evidence library; idempotent on re-run; `--dry-run` and `--scope` flags |
| `tests/test_enrich_l4_party_and_relationship.py` | NEW | 11 tests: bounded-work table coverage (35 pairs), BP-AR-004 avoidance (defensive), evidence grounding (3 entries per Task with E1/E2/E3 strength), field population (definition / trigger / outcome / responsibility / boundary), per-stage count assertion (Activate 20 / Build 40 / Conceive 40 / Design 60 / Improve 20 / Operate 20 / Retire 20), live-run validator conformance (2800 records, 0 findings), idempotence (two-run byte equality), scope filter (--scope SUFFIX restricts writes) |
| `entities/v1-alpha/dea:task-*/dea:task-*.yaml` (220 files) | MOD | In-place enrichment of `definition` / `trigger` / `outcome` / `responsibility` / `boundary.{inclusions, exclusions}` / `evidence[]` on every P&R Task. All other fields (id, type, name, belongs_to_activity, version, lifecycle_status, status, ecfConformance, metadata.established_*, metadata.change_history) preserved verbatim |
| `change-requests/CR-BP-L4-02-pr-domain-content-enrichment.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-L4-02 row added |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 117 -> 118 (regen-after-commit pattern per skill procedure §10) |

## 5. What this CR is NOT

- **NOT a re-opening of CR-BP-98 or CR-BP-102.** The Task schema and the L4 decomposition pipeline are unchanged; this slice consumes their outputs and replaces prose only.
- **NOT a schema, validator-rule, gate wire, or CI change.** No `_RULES` family extended; no gate added to `scripts/conformance_result.py` GATES list.
- **NOT an Activity (L3) record change.** No Activity yaml is touched; the parent Activity's `composes[]` back-reference to its 5 Task ids is preserved.
- **NOT a per-cell rather than per-domain slice.** The decomposition CR reserved CR-BP-L4-02..14 as per-domain enrichment slices; CR-BP-L4-02 lands P&R (the thinnest domain) end-to-end across all 7 of its cells in one PR. The remaining 6 domains (GovernanceAndExistence / ProductAndValue / AgencyAndOrganization / StrategyAndDirection / FinanceAndAccounting / EnablementAndOperations) follow as CR-BP-L4-03..08.
- **NOT a coverage-completion slice for the documentation profile.** DOC-NN closure (matrix-011 / matrix-020) is downstream scope (EXT-04 / EXT-NNa); this slice touches Task prose only.
- **NOT an L4 attestation.** Tasks remain at `lifecycle_status: candidate` / `status: candidate`; the candidate -> active transition is reserved for CR-BP-L4-15 after all 13 enrichment slices land.

## 6. Acceptance criteria

1. `python3 scripts/enrich_l4_party_and_relationship.py --dry-run` reports `tasks_written: 220, tasks_skipped: 0` across the 7 expected per-stage counts.
2. `python3 scripts/enrich_l4_party_and_relationship.py` runs against the live catalog without error; 220 P&R Task files are updated.
3. `python3 scripts/check_task_model.py` reports `Records checked: 2800, Findings: 0, CONFORMANT`.
4. `python3 scripts/check_activity_model.py` reports `Activity records: 560, Findings: 0, CONFORMANT` (L3 validator unaffected).
5. `python3 scripts/check_architectural_regression.py` reports `CONFORMANT, no architectural regressions detected` (BP-AR-004 holds).
6. `python3 scripts/check_reconciliation_matrix.py` reports 22 rows, 0 findings, matrix_version 5 unchanged (no row mutation).
7. `python3 -m pytest tests/test_enrich_l4_party_and_relationship.py -v` passes all 11 tests.
8. Full pytest suite passes; `scripts/conformance_result.py` remains CONFORMANT (29 gates, 0 blocking, 0 advisory failures).
9. `python3 scripts/check_cr_metadata.py` reports 0 new findings on this CR (L4 Layer; standard 7-section header shape).
10. Em-dash / en-dash audit: 0 violations in new prose (governing-sector citations, bounded-work prose, trigger / outcome text, evidence claims).
11. CI: 3/3 green (`conformance`, `validate-process-entries`, `allocation / validate`).
12. Idempotence: re-running `python3 scripts/enrich_l4_party_and_relationship.py` produces byte-identical content on all 220 P&R Task files (asserted by test).

## 7. Result

CR-BP-L4-02 is the first content-enrichment slice in the CR-BP-L4-02..14 pipeline reserved by CR-BP-102. It replaces the templated prose of all 220 PartyAndRelationship L4 Tasks (44 Activities x 5 phases across 7 cells: Activate 20 / Build 40 / Conceive 40 / Design 60 / Improve 20 / Operate 20 / Retire 20) with cell-specific bounded-work prose citing the action taken by each phase custodian, the artefact produced, and the custody transfer to the next phase. Evidence[] is grounded in each cell's governing-sector library (FATF Rec 10 / FinCEN CDD for Activate; DAMA DMBOK2 / MRC / GDPR for Build; Osterwalder / Christensen / Gartner for Conceive; Bain NPS / NN/g / Richardson for Design; Gartner retention benchmark / Reichheld / Medallia for Improve; SAMA / TSIA / Gartner cadence for Operate; SOX §802 / GDPR Art 5(1)(e) / IAOP for Retire). The 29-gate suite remains CONFORMANT (0 blocking, 0 advisory). The generator is idempotent (byte-identical on re-run), scoped (`--scope SUFFIX` filters), and dry-run-safe. Six remaining domains follow as CR-BP-L4-03..08 (each its own PR); CR-BP-L4-15 lands the candidate -> active attestation after all 13 enrichment slices merge.

### Counts (post-merge)

| Metric | Before (PR #146) | After (this slice) |
|---|---|---|
| L0 Process Contexts | 49 | 49 (unchanged) |
| L1 Process Groups | 49 | 49 (unchanged) |
| L2 Business Processes | 140 | 140 (unchanged) |
| L3 Activity records | 560 | 560 (unchanged) |
| L4 Task records (total) | 2,800 | 2,800 (unchanged in count) |
| L4 Task records enriched | 0 (templated) | **220** (PartyAndRelationship fully enriched) |
| L4 Task records templated | 2,800 | **2,580** (remaining 6 domains) |
| Entities (catalog index) | 3,549 | 3,549 (in-place mutation; no id delta) |
| ECF entries | 3,550 | 3,550 (no new entries) |
| Matrix rows | 22 | 22 (no row mutation) |
| Matrix rows closed | 16 | 16 (unchanged) |
| `open_change_requests` | 117 | **118** (+1) |