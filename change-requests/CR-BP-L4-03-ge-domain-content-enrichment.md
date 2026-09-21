# CR-BP-L4-03: GovernanceAndExistence L4 Task Content Enrichment

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree. Its 340 enriched Task records were absorbed into the
> migration tree at merge time (enriched content spliced onto migrated
> structure; legacy ids rewritten via the id map).

**Status**: Proposed
**Layer**: L4
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-20
**Carrier**: Second L4 content-enrichment slice (CR-BP-L4-01 reserved the population surface; CR-BP-L4-02 landed PartyAndRelationship; CR-BP-L4-03..14 reserved the remaining per-domain enrichment slices). Replaces the templated definition / trigger / outcome / responsibility / boundary / evidence content of every GovernanceAndExistence L4 Task with cell-specific, sector-grounded prose describing the bounded work performed by each phase custodian.
**Depends on**: CR-BP-98 (Task schema + TASK-001..005 validator), CR-BP-102 (L4 Task decomposition pipeline; landed 2026-09-19, PR #146; produced 2,800 templated Tasks across 49 cells), CR-BP-L4-02 (P&R enrichment; landed 2026-09-20, PR #147; established the per-domain generator + test pattern)
**Lands against**: 340 L4 Task records (68 GovernanceAndExistence Activities x 5 phases) across 7 cells (Activate 20 / Build 60 / Conceive 40 / Design 60 / Improve 60 / Operate 80 / Retire 20); 29 conformance gates CONFORMANT; no record-count delta (in-place enrichment)

---

## 1. Change Request

Land cell-specific content for every GovernanceAndExistence L4 Task. CR-BP-102 deposited 2,800 Tasks via a templated verb-object decomposition (Intake / Verify / Transform / Confirmation / Audit Record) carrying prose drawn from the parent Activity's cohesion rationale. CR-BP-L4-02 replaced that templated content for PartyAndRelationship (220 Tasks, PR #147). CR-BP-L4-03 replaces it for GovernanceAndExistence (340 Tasks) with sector-grounded bounded-work prose per (stage, phase) cell pair, plus evidence[] drawn from the cell's governing-sector library.

**Per-cell surface:**

| Coordinate (domain / stage) | Activities | Tasks | Governing sector sources |
|---|---|---|---|
| GovernanceAndExistence / Activate | 4 | 20 | Delaware DGCL §§101-108; UK Companies Act 2006 Part 2; Model Business Corporation Act §2.03; EU Directive 2017/1132 |
| GovernanceAndExistence / Build | 12 | 60 | OECD Principles of Corporate Governance (G20/OECD 2023); King IV Report (IoDSA 2016); UK Corporate Governance Code 2018; IIA Three Lines Model |
| GovernanceAndExistence / Conceive | 8 | 40 | ISO 31000:2018; COSO ERM 2017; Basel Committee BCBS 328; FSB Principles for Sound Risk Governance |
| GovernanceAndExistence / Design | 12 | 60 | OECD Principles G20/OECD 2023 Chapter VI; King IV outcomes-based governance; COSO Internal Control 2013; UK CA 2006 §172 |
| GovernanceAndExistence / Improve | 12 | 60 | IIA IPPF / Global Internal Audit Standards 2024; ISO 19011:2018; COSO monitoring component |
| GovernanceAndExistence / Operate | 16 | 80 | UK CA 2006 Part 10 + Part 15; Sarbanes-Oxley §§301-302; SEC Rule 14a-21; IIA attribute standards 1100-1322 |
| GovernanceAndExistence / Retire | 4 | 20 | Delaware DGCL §§275-283; UK Insolvency Act 1986 Part IV; UNCITRAL Model Law on Enterprise Group Insolvency; UK CA 2006 §388 |
| **Total** | **68** | **340** |  |

The 7 cells form the complete GovernanceAndExistence domain (340 Tasks; second-thinnest domain after P&R at 220). Remaining domains follow as CR-BP-L4-04..08 in ascending Task-count order: ProductAndValue (360), AgencyAndOrganization (400), StrategyAndDirection (435), FinanceAndAccounting (440), EnablementAndOperations (605).

## 2. Enrichment mechanics

1. **Generator script** (`scripts/enrich_l4_governance_and_existence.py`) mirrors the CR-BP-L4-02 pattern: walks every `entities/v1-alpha/dea:task-*/` directory, filters by `ecfConformance.canonicalReferences[0].domain == GovernanceAndExistence`, derives the phase from the task-id suffix (`-intake` / `-verify` / `-transform` / `-confirm` / `-record`), and looks up the (stage, phase) bounded-work prose in the in-script `BOUNDED_WORK` table.
2. **Bounded-work prose** is keyed on (stage, phase): 35 distinct entries covering every (stage, phase) pair present in G&E. Each entry names the action taken by the named custodian, the artefact produced, and the custody transfer. G&E-specific artefacts: constitutive instruments, committee charters, policy artifacts, risk registers, assurance evidence packs, dissolution filings.
3. **Trigger / outcome / responsibility** are phase-specific, derived from the phase's predecessor and successor in the 5-phase pattern (intake -> verify -> transform -> confirm -> record). Custody transfers name the governance custodian and the registrar of companies (Retire) where statutory filing applies.
4. **Boundary inclusions / exclusions** are phase-specific. Exclusions name what is NOT this phase's work (e.g. phase 5 excludes re-execution of prior phases; phase 4 excludes notification outside the notify-list).
5. **Evidence[]** carries 3 entries per Task: two from the cell's `STAGE_EVIDENCE` library (the governing-sector sources for that stage) plus one citing the parent Activity's cohesion rationale (CR-BP-32 §6) and this enrichment CR. Strengths E1 (regulatory statute / international standard), E2 (industry framework), E3 (parent-rationale + CR provenance).
6. **BP-AR-004 capability-process avoidance** is asserted by test (defensive: no G&E Activity ends in `Capability`; the assertion guards against future re-runs).
7. **Idempotence** is asserted by test (running the generator twice produces byte-identical output on all 340 G&E Task yaml files).
8. **Scope filter** (`--scope SUFFIX`) restricts generation to a subset for spot-checks; confirmed by test.
9. **Dry-run mode** (`--dry-run`) reports per-stage counts without touching the filesystem.

## 3. Gate posture

- Gate [22] L4 Task validation (CR-BP-98 TASK-001..005): **CONFORMANT, 2800 records, 0 findings**.
- Gate [15] L3 Activity model (CR-BP-32 ACT-001..010 + CR-BP-97 ACT-011..015): **CONFORMANT, 560 Activity records, 0 findings** (no Activity mutation in this slice).
- Gate [23] Architectural regression (CR-BP-16 S21; BP-AR-001..007): **CONFORMANT, no architectural regressions detected** (BP-AR-004 capability-process avoidance verified).
- Gate [23] Reconciliation matrix (CR-BP-99 RCM-001..010): **CONFORMANT, 22 rows, 0 findings** (no row mutation in this slice; matrix_version unchanged).
- Full suite: **29 gates, 0 blocking, 0 advisory failures**.

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `scripts/enrich_l4_governance_and_existence.py` | NEW | Deterministic generator mirroring the CR-BP-L4-02 pattern; G&E bounded-work table keyed on (stage, phase); per-stage evidence library; idempotent on re-run; `--dry-run` and `--scope` flags |
| `tests/test_enrich_l4_governance_and_existence.py` | NEW | 11 tests: bounded-work table coverage (35 pairs), BP-AR-004 avoidance (defensive), evidence grounding (3 entries per Task with E1/E2/E3 strength), field population, per-stage count assertion (Activate 20 / Build 60 / Conceive 40 / Design 60 / Improve 60 / Operate 80 / Retire 20), live-run validator conformance (2800 records, 0 findings), idempotence, scope filter |
| `entities/v1-alpha/dea:task-*/dea:task-*.yaml` (G&E subset, 340 files) | MOD | In-place enrichment of `definition` / `trigger` / `outcome` / `responsibility` / `boundary.{inclusions, exclusions}` / `evidence[]` on every G&E Task. All other fields preserved verbatim |
| `change-requests/CR-BP-L4-03-ge-domain-content-enrichment.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-L4-03 row added |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 118 -> 119 |

## 5. What this CR is NOT

- **NOT a re-opening of CR-BP-98, CR-BP-102, or CR-BP-L4-02.** The Task schema, the L4 decomposition pipeline, and the per-domain enrichment pattern are unchanged; this slice consumes the established pattern with a G&E-specific table.
- **NOT a schema, validator-rule, gate wire, or CI change.** No `_RULES` family extended; no gate added to `scripts/conformance_result.py` GATES list. The CR-META validator extension (L4 layer + CR-BP-LL-NN pattern) landed in CR-BP-L4-02 and is reused unchanged.
- **NOT an Activity (L3) record change.** No Activity yaml is touched; the parent Activity's `composes[]` back-reference to its 5 Task ids is preserved.
- **NOT a coverage-completion slice for the documentation profile.** DOC-NN closure is downstream scope (EXT-04); this slice touches Task prose only.
- **NOT an L4 attestation.** Tasks remain at `lifecycle_status: candidate` / `status: candidate`; the candidate -> active transition is reserved for CR-BP-L4-15 after all 13 enrichment slices merge.

## 6. Acceptance criteria

1. `python3 scripts/enrich_l4_governance_and_existence.py --dry-run` reports `tasks_written: 340, tasks_skipped: 0` across the 7 expected per-stage counts.
2. `python3 scripts/enrich_l4_governance_and_existence.py` runs against the live catalog without error; 340 G&E Task files are updated.
3. `python3 scripts/check_task_model.py` reports `Records checked: 2800, Findings: 0, CONFORMANT`.
4. `python3 scripts/check_activity_model.py` reports `Activity records: 560, Findings: 0, CONFORMANT` (L3 validator unaffected).
5. `python3 scripts/check_architectural_regression.py` reports `CONFORMANT, no architectural regressions detected` (BP-AR-004 holds).
6. `python3 scripts/check_reconciliation_matrix.py` reports 22 rows, 0 findings, matrix_version 5 unchanged.
7. `python3 -m pytest tests/test_enrich_l4_governance_and_existence.py -v` passes all 11 tests.
8. Full pytest suite passes; `scripts/conformance_result.py` remains CONFORMANT (29 gates, 0 blocking, 0 advisory failures).
9. `python3 scripts/check_cr_metadata.py` reports 0 new findings on this CR (L4 layer + CR-BP-L4-NN pattern admitted by CR-BP-L4-02's validator extension).
10. Em-dash / en-dash audit: 0 violations in new prose.
11. CI: 3/3 green (`conformance`, `validate-process-entries`, `allocation / validate`).
12. Idempotence: re-running the generator produces byte-identical content on all 340 G&E Task files (asserted by test).

## 7. Result

CR-BP-L4-03 is the second content-enrichment slice in the CR-BP-L4-02..14 pipeline. It replaces the templated prose of all 340 GovernanceAndExistence L4 Tasks (68 Activities x 5 phases across 7 cells: Activate 20 / Build 60 / Conceive 40 / Design 60 / Improve 60 / Operate 80 / Retire 20) with cell-specific bounded-work prose citing the action taken by each phase custodian, the artefact produced, and the custody transfer to the next phase. Evidence[] is grounded in each cell's governing-sector library (Delaware DGCL / UK CA 2006 / EU Directive 2017/1132 for Activate; OECD Principles / King IV / IIA Three Lines for Build; ISO 31000 / COSO ERM / BCBS 328 for Conceive; OECD Chapter VI / COSO Internal Control / CA 2006 §172 for Design; IIA IPPF / ISO 19011 / COSO monitoring for Improve; UK CA 2006 Part 10+15 / SOX §§301-302 / IIA attribute standards for Operate; DGCL §§275-283 / UK Insolvency Act 1986 / CA 2006 §388 for Retire). The 29-gate suite remains CONFORMANT (0 blocking, 0 advisory). Five remaining domains follow as CR-BP-L4-04..08 (each its own PR); CR-BP-L4-15 lands the candidate -> active attestation after all 13 enrichment slices merge.

### Counts (post-merge)

| Metric | Before (PR #147) | After (this slice) |
|---|---|---|
| L0 Process Contexts | 49 | 49 (unchanged) |
| L1 Process Groups | 49 | 49 (unchanged) |
| L2 Business Processes | 140 | 140 (unchanged) |
| L3 Activity records | 560 | 560 (unchanged) |
| L4 Task records (total) | 2,800 | 2,800 (unchanged in count) |
| L4 Task records enriched | 220 (P&R) | **560** (P&R + G&E) |
| L4 Task records templated | 2,580 | **2,240** (remaining 5 domains) |
| Entities (catalog index) | 3,549 | 3,549 (in-place mutation; no id delta) |
| ECF entries | 3,550 | 3,550 (no new entries) |
| Matrix rows | 22 | 22 (no row mutation) |
| Matrix rows closed | 16 | 16 (unchanged) |
| `open_change_requests` | 118 | **119** (+1) |