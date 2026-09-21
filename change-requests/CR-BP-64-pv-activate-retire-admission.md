# CR-BP-64: P&V Activate/Retire Admission Tranche (Transition to Service / Transition Out of Service)

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Proposed
**Layer**: L2 (first Activate/Retire canonical admissions)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-14
**Carrier**: First governed admission from the CR-BP-63 discovery exercise: lands the two 10/10 ADMIT-CANONICAL recommendations at their primary cells (ProductAndValue Activate + Retire) as full PC + PG + BP stacks, and reverses the two register cells from backlog-deferred to ratified-accepted/landed (register v5).
**Depends on**: CR-BP-62 (discovery method); CR-BP-63 (discovery records); CR-BP-02 (PC profile); CR-BP-12 (PG profile); CR-BP-19 (register v2); CR-BP-28 (register v4)
**Lands against**: 126 canonical BP records (125 active + 1 deprecated), 35 canonical PG records, 35 canonical PC records, 501 canonical Activity records; 24 conformance gates CONFORMANT; CR-BP-62 merged (PR #103); CR-BP-63 in flight (PR #104)

---

## 1. Change Request

Admit the two strongest CR-BP-63 discovery outcomes as canonical catalog records:

1. **Transition to Service** at ProductAndValue x Activate (score 10/10; ITIL 4 transition practices, COBIT 2019 BAI07, IT4IT Requirement to Deploy).
2. **Transition Out of Service** at ProductAndValue x Retire (score 10/10; ITIL service retirement, eTOM lifecycle management, industry EOL practice).

Each admission lands the full stack: a new Process Context (the first PCs at Activate/Retire coordinates), a new L1 Process Group (the L1 home the admission requires), the L2 Business Process record with the full identity contract, and an admission deposition citing the discovery record. The L1 register flips the two cells to ratified-accepted/landed (register v5) with the CR-BP-63 evidence cited per cell.

The remaining three CR-BP-63 recommendations (Bring into Force at G&E/Activate; Decommission at E&O/Retire; Close Enterprise Relationship at P&R/Retire) land as their own tranche slices.

## 2. Why This Slice Is Substantive

This is the first population of any Activate/Retire coordinate since the register's v2 uniform deferral (CR-BP-19). The slice is corrective in posture: it changes live state (2 PC + 2 PG + 2 BP records, register v5) rather than guarding future contributions. The discovery-first sequence (CR-BP-62 method -> CR-BP-63 evidence -> CR-BP-64 admission) is exactly the governed path CR-BP-62 section 20 prescribes: discovery recommends, governed admission decides.

Register lineage reconciliation: the v2 register cells named l2 candidates "Launch proposition / Activate service" (Activate) and "Retire proposition / Decommission service" (Retire). The CR-BP-63 evaluation superseded those candidate names on ECF-independence grounds (BP-LIFE-009): "Transition to Service" / "Transition Out of Service" name the transformations directly, independent of the stage label. The register cells keep their historical candidate lists; the admission note records the supersession. At admission the record names are refined to satisfy BP-ARC-ID-001 (name = verb + object): "Transition Proposition to Service" / "Transition Proposition Out of Service"; the discovery candidate names and the proposed ids are unchanged, and both depositions carry a naming_note recording the refinement.

## 3. Repository Changes

| Path | Status | Notes |
|---|---|---|
| `contexts/v1-alpha/dea-pc-pv-activate.yaml` | NEW | PC: Proposition Launch and Service Transition |
| `contexts/v1-alpha/dea-pc-pv-retire.yaml` | NEW | PC: Proposition Retirement and Service Withdrawal |
| `entities/v1-alpha/dea:group-service-transition-activation/` | NEW | PG + README; composes the new BP (PG-004/005) |
| `entities/v1-alpha/dea:group-service-transition-retirement/` | NEW | PG + README; composes the new BP |
| `entities/v1-alpha/dea:process-transition-to-service/` | NEW | BP + README + research/l2-admission-deposition.yaml |
| `entities/v1-alpha/dea:process-transition-out-of-service/` | NEW | BP + README + research/l2-admission-deposition.yaml |
| `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml` | MOD | Register v5: two cells flipped (ratified-accepted / landed) with per-cell admission notes; ratification block updated (37 accepted / 12 deferred) |
| `scripts/check_admission_gate.py` | MOD | ADM-001 admission-authority vocabulary: CR-BP-64 registered as the discovery-driven admission authority (each future admission tranche registers its own CR number as it lands) |
| `reconciliation/dispositions/register.yaml` | MOD | RETAIN entries for the two new BPs (locked-register coverage) |
| `reconciliation/tranches/plan.yaml` | MOD | pv-act.64 + pv-ret.64 tranches appended (67 tranches, 128 records) |
| `tests/` (9 files) | MOD | Count assertions: BP 126 -> 128; PG 35 -> 37; PC 35 -> 37; EXE 662 -> 666; report 697 -> 703; tranche count 65 -> 67 |
| `scripts/check_activity_model.py`, `scripts/check_mece.py` | MOD | Docstring count text only |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated (new record hashes) |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated; 703 records, all L4 |
| `change-requests/CR-BP-64-pv-activate-retire-admission.md` | NEW | This document |
| `change-requests/README.md` | MOD | CR-BP-64 row |
| `CATALOG.yaml` | MOD | Regenerator: 666 entities; `open_change_requests` 75 -> 76 |

## 4. Coverage on the Live Catalog

- PC gate: PASS (PC-001..008) with 37 PCs including the first Activate/Retire contexts.
- PG gate: PASS (PG-001..008) with 37 PGs; both new composes targets resolve.
- MECE: register-landed coordinates now 37; each has PC + PG; 0 findings.
- Register audit: audit_status agrees with catalog reality.
- L2 qualification (BP-C1..C4), intent (PSP-001..003), lifecycle state (LCM), semantic identity (SIV): 0 findings across the 128-BP universe.
- ECF conformance: PASS, 666 entries (new coordinates `ecf:productValue.activate` / `ecf:productValue.retire` validate against the canonical stage vocabulary, which always included Activate/Retire).
- Discovery gate [19]: unaffected (14 records, 0 findings).

## 5. Tranche Plan Status

| Slice | Status |
|---|---|
| CR-BP-62 (discovery method + DISC gate) | Merged (PR #103) |
| CR-BP-63 (Activate/Retire discovery exercise) | In flight (PR #104) |
| CR-BP-64 (P&V pair admission) | This slice |
| G&E Activate admission (Bring into Force) | Next |
| E&O Retire admission (Decommission) | Next |
| P&R Retire admission (Close Enterprise Relationship) | Next |
| L3 decomposition of the new BPs | Follow-on L3 tranche slice |

## 6. What This CR Is NOT

- **NOT a blanket Activate/Retire reversal.** Twelve cells remain backlog-deferred with their CR-BP-63 documented outcomes; only the two evidence-backed P&V cells flip.
- **NOT a discovery-method change.** The method and gate are CR-BP-62's; this slice applies them.
- **NOT an L3 decomposition.** The two new BPs carry no Activity records yet; L3 decomposition follows the established pattern as a follow-on slice (ACT-010 fires only when Activity records exist).
- **NOT a specialization.** `process_specialization: []` on both BPs; specialization work remains unauthorized per program governance.
- **NOT a Process Group kind invention.** Both PGs use `cross-cutting` from the existing PG-kind vocabulary.

## 7. Acceptance Criteria

1. PC gate PASS with 37 PCs; PG gate PASS with 37 PGs; both new composes targets resolve.
2. MECE 0 findings across 37 register-landed coordinates; register audit agrees with catalog reality.
3. Register v5 ratification block consistent: 37 ratified-accepted / 12 backlog-deferred; per-cell admission notes cite the CR-BP-63 records.
4. Count assertions updated: BP 128 / PG 37 / PC 37 / EXE 666 / report 703; full pytest suite passes.
5. `scripts/conformance_result.py` remains CONFORMANT (24 gates).
6. `python3 scripts/check_cr_metadata.py` reports 0 new findings.
7. L2 qualification, intent, lifecycle-state and SIV gates report 0 findings across the 128-BP universe.

## 8. Result

CR-BP-64 admits the first two canonical Business Processes at Activate/Retire coordinates, completing the first full discovery-to-admission cycle under CR-BP-62: method (62), evidence (63), governed admission (64). The catalog now covers 37 of 49 ECF coordinates with canonical stacks; the remaining 12 Activate/Retire cells hold documented discovery outcomes rather than an untested blanket deferral.
