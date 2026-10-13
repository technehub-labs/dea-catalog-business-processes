# CR-BP-35: Process Catalog Architecture Retrospective

**Status**: Proposed
**Layer**: Cross-cutting
**Owner**: Emmanuel A. Otchere
**Date**: 2026-09-12
**Carrier**: Eighth execution slice of the BP-32/33/34 tranche plan; second slice of Phase 5. See `01_plan/CR-BP-32-33-34-foundation/POSITIONING.md` §5/§7.
**Depends on**: CR-BP-02, CR-BP-03, CR-BP-12, CR-BP-14, CR-BP-15, CR-BP-16, CR-BP-SPEC-BP-01
**Lands against**: 161 canonical records (126 BP + 35 PG); conformance level L4; architecture documentation already live in `docs/architecture.md`

---

## 1. Change Request

Codify a retrospective on the **Process Catalog Architecture** as it has actually landed in `main`, against the user's original "CR-BP-07 — Process Catalog Architecture" attachment (from `doc_cf6fc6bb9e80_CR-BP-04_06.md`, lines ~1100..1300 in the source). This is the second slice of Phase 5 in the BP-32/33/34 additive harvest plan (`POSITIONING.md` §5/§7).

The user's original CR-BP-07 was authored in the assumption that the CR-BP-32/33/34 foundation would land **before** catalog population. The actual landing order is the inverse: the catalog was populated first (PRs #22..#60) under CR-BP-12 + CR-BP-14 + CR-BP-15 + CR-BP-16, and the BP-32/33/34 foundation landed as a post-hoc carrier (PR #69). This retrospective documents the architecture as it actually stands after the harvest tranches have landed.

This is a **documentation-only** slice. No validator, no schema, no record mutation, no gate wiring.

## 2. Why this slice exists

The architecture narrative is already distributed across multiple documents:

- `docs/architecture.md` — top-level Process Architecture (CR-BP-03 + CR-BP-14 lineage)
- `docs/semantic-contract.md` — the six characterization dimensions (CR-BP-14)
- `docs/context.md` — Process Context (CR-BP-02)
- `docs/classification.md` — process_intent / process_type / process_specialization axes
- `docs/specialization.md` — kernel + specialization discipline (CR-BP-SPEC-BP-01)
- `docs/identity.md` — identity contract (CR-BP-03 §6)
- `docs/conformance.md` — conformance levels L0..L4 (CR-BP-15-IMP / CR-BP-16)
- `docs/conformance-pipeline.md` — the 22-gate pipeline
- `docs/governance/reconciliation-programme.md` — closed governance loop
- `docs/governance/process-specialization.md` — kernel / specialization lineage
- `docs/governance/process-audience-vs-ecf-domain.md` — ECF conformance
- `docs/governance/phase-20-review-crbp15.md` — Phase 20 governance review

This retrospective adds a **single landing document** that ties the architecture narrative together as of 2026-09-12 (post-Phase 5 slice 1). It documents:

1. **What was originally proposed** (user's CR-BP-07 framing)
2. **What actually landed** (the eight-slot architecture documented in `docs/architecture.md`)
3. **What changed between the two** (the four landing-order / framework / vocabulary / validator deltas)
4. **Where the architecture stands now** (161 records, L4 conformance, 22 gates)
5. **What is forward-looking** (CR-BP-32 Activity layer, CR-BP-33 Execution Boundary)

The narrative is captured in this CR doc (the slice's deliverable) and is referenced from `change-requests/README.md` (the standard pointer pattern established by the carrier PR #69).

## 3. The architecture as it has landed (2026-09-12)

### Top-level decomposition

```
ECF Domain x Lifecycle Stage
       |
       v
Process Context            (CR-BP-02; contexts/v1-alpha/; 35 records)
       |
       v
L0 Process Scope           (CR-BP-14 §6; conceptual; documented)
       |
       v
L1 Process Group           (CR-BP-12; entities/v1-alpha/dea:group-*; 35 records)
       |
       v
L2 Business Process        (CR-BP-SPEC-BP-01 / CR-BP-03; entities/v1-alpha/dea:process-*; 126 records)
       |
       v
Activity                   (CR-BP-32; PR #74; gate [15]; future opt-in)
       |
       v
Workflow / Task            (CR-BP-33; PR #75; gate [16]; future opt-in; metamodel references)
```

### Six characterization dimensions (CR-BP-14)

Every Business Process record carries six axes:

| Axis | Field | Vocabulary |
|---|---|---|
| Intent | `process_intent` | 7-value purposive (govern / manage / operate / deliver / support / develop / transform) |
| Type | `process_type` | 5-value Mintzberg (operating / management / support / ...) |
| Specialization | `process_specialization` | inheritance / pattern-based refinement (CR-BP-03) |
| Classification | `process_classification` | ECF Domain (7-value) + Lifecycle Stage (7-value) → Process Context |
| Audience | (legacy alias) | legacy migration alias for `process_context` + `relationship_type=serves` |
| Identity | `identity` | verb + object + outcome + evidence_links (CR-BP-03 §6) |

### Conformance gate stack (CR-BP-15-IMP / CR-BP-16)

22 gates in `scripts/conformance_result.py`:

- **Structural** ([1]–[3]): Schema, Structure, References (BP-SEM + legacy + context-resolution)
- **Semantic** ([4]): BP-SEM-001..014, BP-SPEC-01-001..007
- **Architectural** ([5]): Hierarchy (BP-AR-001..007)
- **Specialization** ([6]): cycle + edge check
- **MECE** ([7]): Process Group intra-context (PG-006)
- **Provenance** ([8]): ECF Conformance Gate
- **Cross-repo integrity** ([9]): CR-META-001..006
- **Levels 1-4** ([10]): Levels report, Admission gate, Documentation
- **Phase 2 validators** ([11]–[14]): L2 Qualification, Intent Purposive, Lifecycle State-Machine, Semantic Identity vs Version
- **Phase 3-5 validators** ([15]–[17]): Activity Model, Execution Boundary, MECE Validation

### Cross-repo contracts

- **dea-metamodel**: `dea:Process` (abstract kernel) + `dea:BusinessProcess` (specialization); CR-MM-PROC-01
- **dea-architecture-framework**: `dea:entity-process` (root-model kernel; discriminator `process-kernel`) + `dea:entity-business-process` (specialization; class_alias BP); CR-AR-FMWK-01; tag v0.6.0
- **WSF** (org): `wsf:Process` (Tier-3 derived; structural activity organization)
- **ECF** (dea-metaframework): 7 Domains (CR-ECF-003, CR-ECF-006, CR-ECF-007, CR-ECF-008) + 7 Stages (CR-ECF-004, CR-ECF-005); current version v2.5.0

The 1:1 LOSSLESS federation mapping between metamodel and root-model ids is documented in `docs/governance/process-specialization.md` and `metamodel-pointer.yaml`.

### ECF version history (catalog-internal)

- **v2.3.0** (CR-ECF-006 + ADR-ECF-001): 5 Domains renamed; 1 Domain replaced (Supply & Resources → Strategy & Direction). Landed in PR #44.
- **v2.4.0** (CR-ECF-007 + ADR-ECF-002): Domain 3 renamed (PeopleAndOrganization → AgencyAndOrganization); substrate-independent per CR-ECF-007. Landed in PR #45.
- **v2.5.0** (CR-ECF-008 + ADR-ECF-003): Domain 6 renamed (OperationsAndEnablement → EnablementAndOperations); Domain/Stage orthogonality stress test. Landed in PR #61.

Each version migration carried companion CRs in the catalog (CR-BP-17, -18, -23) and cross-repo (BC-ECF-03, BO-02, OU-02).

## 4. What changed between the user's original CR-BP-07 and what landed

### Delta 1 — Landing order was inverted

User's CR-BP-07 assumed CR-BP-32/33/34 would land **before** the catalog was populated. Actual landing order: CR-BP-07 was implicit in the early carrier PRs (CR-BP-12, CR-BP-14, CR-BP-15, CR-BP-16); catalog was populated under that regime (PRs #22..#60); then CR-BP-32/33/34 foundation landed as the post-hoc harvest carrier (PR #69). The harvest tranches (PRs #70..#76) then layered the BP-34 conformance profile validators + Activity / Execution / MECE gates on top.

### Delta 2 — Conformance levels L0..L4 (not in original CR-BP-07)

The original CR-BP-07 did not articulate conformance levels. CR-BP-15-IMP (Phases 1..20) and CR-BP-16 introduced the L0..L4 conformance model (CR-BP-16 §11). All 161 records today are at L4. The 22-gate pipeline is the live operationalization of L4.

### Delta 3 — Specialization graph (kernel + specializations)

Original CR-BP-07 did not differentiate between the abstract Process kernel and its specializations. CR-MM-PROC-01 (PR #163 in dea-metamodel) and CR-AR-FMWK-01 (PR #10 + tag v0.6.0 in dea-architecture-framework) introduced the kernel + specialization discipline. CR-BP-SPEC-BP-01 (PR #12 in this catalog) operationalized it locally. The catalog currently specializes only `dea:BusinessProcess`; `dea:Activity` (PR #74) and `dea:Workflow` / `dea:Task` (PR #75) are opt-in target types with `lifecycle: proposed`.

### Delta 4 — Validator library as a first-class artifact

Original CR-BP-07 referenced validation as a future concern. CR-BP-16 §S17/S18/S19/S25 established the unified conformance pipeline (`scripts/conformance_result.py`) with 22 gates. The Phase 2..5 harvest added 7 more gates ([11]–[17]) covering L2 qualification, intent purposive, lifecycle state-machine, semantic identity vs version, activity model, execution boundary, and MECE validation.

## 5. Repository changes (this slice)

| Path | Status | Notes |
|---|---|---|
| `change-requests/CR-BP-35-process-catalog-architecture.md` | NEW | This document — the retrospective slice |
| `change-requests/README.md` | MOD | Adds CR-BP-35 row; CR-BP-36 status corrected to "Merged (PR #76)" |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 47 → 48 |

**No code. No schema. No validator. No record mutation.**

## 6. Tranche plan status

| Phase | Slice | Status |
|---|---|---|
| 1 | CR-BP-32/33/34 foundation carrier | Merged (PR #69) |
| 2 | CR-BP-34a L2 Qualification | Merged (PR #70, gate [11]) |
| 2 | CR-BP-34b Intent Purposive | Merged (PR #71, gate [12]) |
| 2 | CR-BP-34c Lifecycle State-Machine | Merged (PR #72, gate [13]) |
| 2 | CR-BP-34d Semantic Identity vs Version | Merged (PR #73, gate [14]) |
| 3 | CR-BP-32 Activity Model | Merged (PR #74, gate [15]) |
| 4 | CR-BP-33 Execution Boundary | Merged (PR #75, gate [16]) |
| 5 | CR-BP-36 MECE Validation | Merged (PR #76, gate [17]) |
| **5** | **CR-BP-35 Process Catalog Architecture retrospective** | **This slice** |
| 5 | CR-BP-37 Cross-Repository Integrity | Next per user direction |
| 5 | CR-BP-38 ECF Matrix Population retrospective | Next per user direction |

## 7. What this CR is NOT

- **NOT a restructuring of the architecture.** The eight-slot decomposition (Process Context → Scope → Process Group → Business Process → Activity → Workflow / Task) is unchanged.
- **NOT a new conformance gate.** No gate wiring; no validator.
- **NOT a record mutation.** No entity changes; no schema bump.
- **NOT a release cut.** No CHANGELOG / CITATION / tag updates.
- **NOT a CR-BP-07 replacement.** This is a **retrospective** on the user's original CR-BP-07 in light of what actually landed; it does not supersede the original.

## 8. Acceptance criteria

1. `change-requests/CR-BP-35-process-catalog-architecture.md` exists with this full retrospective.
2. `change-requests/README.md` CR-BP-35 row added.
3. `CATALOG.yaml` reflects `open_change_requests: 48` (was 47).
4. No code, no schema, no validator, no canonical record mutation.
5. The retrospective references the live architecture (`docs/architecture.md`, `docs/semantic-contract.md`, etc.) and the live gate roster (22 gates).

## 9. Result

CR-BP-35 documents the Process Catalog Architecture as it has actually landed in `main` after Phase 1..4 of the BP-32/33/34 harvest and Phase 5 slice 1 (MECE Validation). The retrospective surfaces four deltas from the user's original CR-BP-07 (landing-order inversion, L0..L4 conformance levels, kernel + specialization discipline, validator library as first-class artifact) and ties together the 161 records / 22 gates / cross-repo contracts that constitute the live architecture.
