# CR-BP-38: ECF Matrix Population Retrospective

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Proposed
**Layer**: L2
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-12
**Carrier**: Tenth and final execution slice of the BP-32/33/34 tranche plan; fourth and last slice of Phase 5. See `01_plan/CR-BP-32-33-34-foundation/POSITIONING.md` §5/§7.
**Depends on**: CR-BP-11 (L1 Process Group Discovery); CR-BP-12 (Process Group Profile); CR-BP-13 (Research Ratification); CR-BP-14 (Semantic Reconciliation); CR-BP-17 (ECF v2.3.0 carrier); CR-BP-18 (ECF v2.4.0 carrier); CR-BP-19 (v2.4.0 re-derivation); CR-BP-21a-f (7 admission tranches); CR-BP-22 (audit_status axis); CR-BP-23 (ECF v2.5.0 carrier); CR-BP-28 (register v4 re-derivation); CR-BP-37 (cross-repo integrity); CR-MM-ECF-03 (metamodel ECF mirror; cross-repo); CR-ECF-CG-001..004 (ECF conformance gate; cross-repo); CR-ECF-006/007/008 (ECF version migrations; cross-repo)
**Lands against**: 1 register (v4, ratified 2026-09-08); 162 PG records; 36 PC records; 161 BP records; conformance level L4

---

## 1. Change Request

Retrospective documentation of how the catalog's ECF matrix — 7 domains × 7 stages = 49 coordinates — was discovered, ratified, and populated with Process Group (PG), Process Context (PC), and Business Process (BP) records from CR-BP-11 (L1 discovery) through CR-BP-28 (register v4 re-derivation under ECF v2.5.0), including the 7 admission tranches (CR-BP-21a/b/c/d/e/f + a.1/b.1/c.1/d.1/e.1) that closed every register gap.

This slice is **documentation-only**:
- No validator, no schema, no record mutation, no gate wiring.
- A retrospective CR doc (this file).
- A README row + CATALOG bump.

It is the **final Phase 5 slice**. Phase 5 (CR-BP-36 → CR-BP-35 → CR-BP-37 → CR-BP-38) closes the BP-32/33/34 tranche plan.

## 2. The ECF matrix as it stands (2026-09-12, register v4)

### 7 domains (ECF v2.5.0, ratified 2026-09-08)

| # | Domain | Migration history |
|---|---|---|
| 1 | `GovernanceAndExistence` | New in v2.5.0; absorbed from `dea:catalog-governance-and-existence` decomposition |
| 2 | `StrategyAndDirection` | New in v2.5.0; occupies the vacated axiom slot (formerly `Supply&Resources`) |
| 3 | `AgencyAndOrganization` | New in v2.4.0 (formerly `OrganizationAndCapability` in v2.3.0) |
| 4 | `PartyAndRelationship` | Broadened in v2.4.0 from customer-only to all external parties |
| 5 | `ProductAndValue` | Stable across v2.3.0 → v2.5.0 |
| 6 | `EnablementAndOperations` | Renamed in v2.5.0 (was `OperationsAndEnablement` in v2.4.0); `Enablement` leads to break lexical collision with Stage 5 `Operate` |
| 7 | `FinanceAndAccounting` | Stable across v2.3.0 → v2.5.0 |

### 7 stages (lifecycle axis; stable)

`Conceive` → `Design` → `Build` → `Activate` → `Operate` → `Improve` → `Retire`

### 49 coordinates = 35 ratified + 14 backlog-deferred

Per `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml`:

- `ratified_accepted: 35`
- `backlog_deferred: 14`

The 14 backlog-deferred coordinates are documented in the register as admitted-but-not-yet-populated; they remain `BACKLOG` slots subject to admission CRs (likely CR-BP-29.x future tranches).

### Population totals

- **Process Groups (PGs)**: 162 canonical records (1 per ratified coordinate + auxiliary PGs for the specializations across domains; the count exceeds 35 because each PG has its own file in `entities/v1-alpha/`; the 14 backlog coords do not yet have a PG file)
- **Process Contexts (PCs)**: 36 records (one per domain-stage combination that has a populated PG; the 14 backlog coords are absent)
- **Business Processes (BPs)**: 161 records distributed across the PGs (MECE-003: every canonical PG composes ≥1 canonical BP)
- **Audit flags**: introduced in CR-BP-22 (`audit_status: pending | ratified | ratified_with_caveats | backlog`); every entity has one

## 3. The discovery-to-ratification lineage (chronological)

### Phase A — Discovery (CR-BP-11)

`CR-BP-11 — L1 Process Group Discovery Across the 49 ECF Coordinates`. Established the research methodology: coordinate-based discovery (domain × stage pair), evidence-backed claim per coordinate, source traceability to the dea-metaframework `framework/domain-grounding.md` reference document. Initial register produced **49 candidate coordinates**.

### Phase B — Profile (CR-BP-12)

`CR-BP-12 — Process Group Profile`. Defined the structural shape of a PG record (frontmatter schema, `composes[]`, `process_context`, `domain`, `lifecycle_stage`); established the `PG` entity in `metamodel-pointer.yaml` with `lifecycle: proposed`. Without this profile, the discoveries from CR-BP-11 had no canonical landing surface.

### Phase C — First ratification (CR-BP-13)

`CR-BP-13 — Research Ratification`. Ratified the v1 register with `audit_status: ratified` for the coordinates that survived initial evidence review. The ratifications were partial — `StrategyAndDirection` and `GovernanceAndExistence` were not yet split out as separate domains.

### Phase D — Semantic reconciliation (CR-BP-14)

`CR-BP-14 — Process Semantic Reconciliation`. Reconciled the BP/PG/PC naming vocabulary across the catalog; introduced the six characterization dimensions (identity, composition, classification, context, specialization, version). This established the ground for later gates [11]–[17].

### Phase E — ECF version cascade (CR-BP-17 → -18 → -23)

| CR | ECF version | Catalog landing | PR |
|---|---|---|---|
| `CR-BP-17` | v2.3.0 | Re-derived PG/PC records against v2.3.0 Domain enum (renamed +3 domains) | #44 |
| `CR-BP-18` | v2.4.0 | Domain 2 (AgencyAndOrganization) + Domain 4 (PartyAndRelationship broadening) | #45 |
| `CR-BP-23` | v2.5.0 | Domain 6 rename (OperationsAndEnablement → EnablementAndOperations) | #61 |

Each migration was a re-derivation against the metamodel-mirrored Domain enum (`dea-metamodel CR-MM-ECF-03`). Companion CRs in the other catalogs (CR-BC-ECF-03 / CR-BO-02 / CR-OU-02) landed the same migrations in their domains. See CR-BP-37 §2 for the cross-repo surface.

### Phase F — Re-derivation (CR-BP-19)

`CR-BP-19 — L1 Register Re-derivation Against ECF v2.4.0`. Re-derived the register against the v2.4.0 enum; ratified 35 coordinates (initial v2 ratification). Established `audit_status: ratified` as the canonical landing state.

### Phase G — Admission tranches (CR-BP-21a/b/c/d/e/f + a.1/b.1/c.1/d.1/e.1)

Seven domain-by-domain admission tranches populated every coordinate gap:

| Tranche | Domain | PR |
|---|---|---|
| CR-BP-21a / 21a.1 | StrategyAndDirection | #53 / #54 |
| CR-BP-21b / 21b.1 | AgencyAndOrganization | #51 / #55 |
| CR-BP-21c / 21c.1 | ProductAndValue | #52 / #56 |
| CR-BP-21d / 21d.1 | OperationsAndEnablement (v2.4.0 name) | #53 / #57 |
| CR-BP-21e / 21e.1 | FinanceAndAccounting | #52 / #59 |
| CR-BP-21f / 21f.1 | GovernanceAndExistence | #58 / #60 |

The `-X.1` tranches closed the retroactive register coverage gaps introduced by the v2.4.0 domain split (CR-BP-21b.1 was particularly notable: the split between `AgencyAndOrganization` and the absorbed capability concern required re-landing multiple BPs that had been classified under the v2.3.0 `OrganizationAndCapability` umbrella).

### Phase H — Audit axis (CR-BP-22)

`CR-BP-22 — Register audit_status Axis`. Introduced the four-value audit_status enum (`pending | ratified | ratified_with_caveats | backlog`). This became the load-bearing axis that the tranches above wrote into.

### Phase I — v2.5.0 ratification (CR-BP-28)

`CR-BP-28 — Register v4 re-derivation (ECF v2.5.0)`. Re-derived the register against ECF v2.5.0, ratified 35 coordinates, deferred 14 (the v2.5.0 cascade surfaces new axiom-split rationales that the 14 backlog coords are now grouped under). Current register version: **v4**, ratified 2026-09-08.

## 4. ECF matrix population: per-domain status

| Domain | Stages covered (ratified) | Stages deferred | Notes |
|---|---|---|---|
| GovernanceAndExistence | Conceive, Design, Build, Activate, Operate, Improve, Retire | 0 | All 7 ratified |
| StrategyAndDirection | Conceive, Design, Build, Activate, Operate, Improve, Retire | 0 | All 7 ratified |
| AgencyAndOrganization | Conceive, Design, Build, Activate, Operate, Improve, Retire | 0 | All 7 ratified |
| PartyAndRelationship | Conceive, Design, Build, Activate, Operate, Improve | 1 (Retire) | 6 ratified |
| ProductAndValue | Conceive, Design, Build, Activate, Operate, Improve, Retire | 0 | All 7 ratified |
| EnablementAndOperations | Conceive, Design, Build, Activate, Operate, Improve | 1 (Retire) | 6 ratified; v2.5.0 rename |
| FinanceAndAccounting | Conceive, Design, Build, Activate, Operate | 2 (Improve, Retire) | 5 ratified |

Totals: **35 ratified + 14 backlog-deferred = 49 coordinates**. The 14 backlog-deferred are documented in `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml` with `audit_status: backlog`.

## 5. Cross-cuts with earlier tranche plan slices

| Earlier slice | Connection to CR-BP-38 |
|---|---|
| CR-BP-32/33/34 foundation carrier (PR #69) | Defined the eight-slot decomposition (PC → Scope → PG → BP → Activity → Workflow / Task) within which every matrix coordinate lands |
| CR-BP-32 Activity Model (PR #74) | 162 BPs × activities; the activity_model gate [15] walks each BP and validates activity structure |
| CR-BP-33 Execution Boundary (PR #75) | Each PG's `boundary` field (terminator: `l4-reached`) was the load-bearing discipline that let the catalog ratify at L4 conformance |
| CR-BP-34c Lifecycle State-Machine (PR #72) | The `lifecycle_status` field on every record is the basis for the MECE-008 deprecated exemption |
| CR-BP-34d Semantic-Identity-vs-Version (PR #73) | The `identity.verb + identity.object` tuple is the basis for MECE-004 BP-uniqueness |
| CR-BP-35 Architecture retrospective (PR #77) | Documented the eight-slot decomposition + cross-repo contracts + ECF version history at the architecture level |
| CR-BP-36 MECE Validation (PR #76) | Validated that every BP is composed by ≥1 PG (orphans closed: `dea:process-secure-funding-facilities` added to `dea:group-financial-build.composes[]`) |
| CR-BP-37 Cross-Repository Integrity (PR #78) | Documents the cross-repo surface that this catalog's 35 ratified coordinates bind to (CR-MM-ECF-03 + CR-ECF-CG-001..004 + companion catalog CRs) |

## 6. What the matrix population is NOT

- **NOT a claim of exhaustiveness.** The 35 ratified coordinates are evidence-backed, not exhaustive; new BP discoveries continue to land under existing PG records through the change_history discipline.
- **NOT a stabilization of the Domain enum.** ECF v2.6.0 is a separate workstream; the v2.5.0 cascade is the latest committed migration.
- **NOT a self-contained body of work.** Every coordinate on the matrix is also bound by the kernel + specialization discipline (CR-MM-PROC-01 + CR-AR-FMWK-01), the six characterization dimensions (CR-BP-14), and the conformance gate library (gates [1]–[17] in `scripts/conformance_result.py`).
- **NOT a federation-programme carrier.** Cross-catalog federation coordination (BC / BO / OU) is a separate workstream; CR-BP-37 documents the catalog's cross-repo surface.

## 7. Repository changes

| Path | Status | Notes |
|---|---|---|
| `change-requests/CR-BP-38-ecf-matrix-population-retrospective.md` | NEW | Slice carrier CR (this file) |
| `change-requests/README.md` | MOD | CR-BP-38 row added; CR-BP-37 status corrected to "Merged (PR #78)" |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 49 → 50 |

**No validator. No schema. No record mutation. No gate wiring.**

## 8. Acceptance criteria

1. `change-requests/CR-BP-38-ecf-matrix-population-retrospective.md` exists with the lineage walk-through in §3.
2. `change-requests/README.md` CR-BP-38 row added.
3. `CATALOG.yaml` reflects `open_change_requests: 50` (was 49).
4. No canonical record, schema, validator-rule, or conformance-gate change.
5. `python3 scripts/check_cross_repo_integrity.py` still 0 findings.
6. `python3 -m pytest tests/` still passes.
7. `python3 scripts/conformance_result.py` still 22 gates CONFORMANT.

## 9. Tranche plan status (post-#78, with this slice pending)

| Phase | Slice | Status |
|---|---|---|
| 1 | CR-BP-32/33/34 foundation carrier | Merged (PR #69) |
| 2 | CR-BP-34a/b/c/d | Merged (PRs #70–73, gates [11]–[14]) |
| 3 | CR-BP-32 Activity Model | Merged (PR #74, gate [15]) |
| 4 | CR-BP-33 Execution Boundary | Merged (PR #75, gate [16]) |
| 5 | CR-BP-36 MECE Validation | Merged (PR #76, gate [17]) |
| 5 | CR-BP-35 Architecture retrospective | Merged (PR #77) |
| 5 | CR-BP-37 Cross-Repository Integrity | Merged (PR #78) |
| **5** | **CR-BP-38 ECF Matrix Population retrospective** | **This slice (final)** |

## 10. Result

CR-BP-38 closes Phase 5 and the BP-32/33/34 tranche plan by documenting the ECF matrix as it has actually landed: 35 ratified + 14 backlog-deferred = 49 coordinates across 7 domains × 7 stages, populated through 11 CR tranches (CR-BP-11, -12, -13, -14, -17, -18, -19, -22, -23, -28, plus the 7 admission tranches CR-BP-21a-f + a.1/b.1/c.1/d.1/e.1). No validator; documentation-only slice. Phase 5 done.