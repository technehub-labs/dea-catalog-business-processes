# CR-BP-66: E&O Retire Admission Tranche (Decommission)

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Proposed
**Layer**: L2 (Retire admission)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-14
**Carrier**: Third governed admission from the CR-BP-63 discovery exercise: lands the Decommission recommendation (9/10) at its primary cell (EnablementAndOperations x Retire) as a full PC + PG + BP stack, and reverses the register cell from backlog-deferred to ratified-accepted/landed (register v7, superseding v6 from the merged CR-BP-65).
**Depends on**: CR-BP-62 (discovery method); CR-BP-63 (discovery records); CR-BP-64 (first admission tranche; ADM-001 authority registration pattern); CR-BP-02 (PC profile); CR-BP-12 (PG profile)
**Lands against**: 128 canonical BP records (127 active + 1 deprecated), 37 canonical PG records, 37 canonical PC records, 501 canonical Activity records; 24 conformance gates CONFORMANT; CR-BP-63 merged (PR #104); CR-BP-64 merged (PR #105); CR-BP-65 merged (PR #106; this branch was cut from origin/main and rebased onto post-#106 main)

---

## 1. Change Request

Admit the CR-BP-63 discovery outcome at EnablementAndOperations x Retire:

**Decommission** (score 9/10): the withdrawal and retirement of operational assets. Evidence base: ISO 55000 asset management normative end-of-life activities; APQC asset disposition and eTOM resource retirement as stable industry-neutral identities; data center, facility and fleet decommissioning practice with safety and data-sanitization evidence.

Notably, this admission meets the register v2 cell's own escape condition verbatim: the v2 deferral said "defer until a regulated decommission (e.g. nuclear-grade) requires a standalone group." The discovery evaluation established decommissioning as exactly that -- a governed end-of-life discipline with its own trigger, transformation and outcome (BP-LIFE-002/003/004/009), distinct from capability lifecycle management.

## 2. Naming and Lineage

The register v2 l2 candidates for this cell were asset-flavored ("Decommission production line", "Dispose of assets", ...). The CR-BP-63 evaluation established the stronger candidate (Decommission) on evidence and ECF-independence grounds. At admission the record name is refined to satisfy BP-ARC-ID-001 (name = verb + object): **Decommission Enterprise Asset** (verb Decommission; object Enterprise Asset). The discovery candidate name and the proposed id (`dea:process-decommission`) are unchanged; the deposition carries the naming_note.

## 3. Repository Changes

| Path | Status | Notes |
|---|---|---|
| `contexts/v1-alpha/dea-pc-oe-retire.yaml` | NEW | PC: Operations and Asset Decommissioning (full cell charter) |
| `entities/v1-alpha/dea:group-operations-and-asset-decommissioning/` | NEW | PG + README; `process_group_kind: functional`; composes the new BP |
| `entities/v1-alpha/dea:process-decommission/` | NEW | BP + README + research/l2-admission-deposition.yaml |
| `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml` | MOD | Register v7 (supersedes v6 from CR-BP-65): E&O/Retire flipped with admission note recording the met escape condition; ratification block 39 accepted / 10 deferred |
| `scripts/check_admission_gate.py` | MOD | ADM-001 admission-authority vocabulary: CR-BP-66 registered |
| `reconciliation/dispositions/register.yaml` | MOD | RETAIN entry for the new BP |
| `reconciliation/tranches/plan.yaml` | MOD | oe-ret.66 tranche appended (68 tranches, 129 records) |
| `tests/` (9 files) | MOD | Count assertions: BP 129 -> 130; PG 38 -> 39; PC 38 -> 39; EXE 668 -> 670 (BP + PG enter the ledger); report 706 -> 709 (PC + PG + BP enter the report); tranches 68 -> 69 |
| `scripts/check_activity_model.py`, `scripts/check_mece.py` | MOD | Docstring count text only |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated; 709 records, all L4 |
| `change-requests/CR-BP-66-eo-retire-admission.md` | NEW | This document |
| `change-requests/README.md` | MOD | CR-BP-66 row |
| `CATALOG.yaml` | MOD | Regenerator: 669 entities; `open_change_requests` 77 -> 78 |

## 4. Coverage on the Live Catalog

- PC gate PASS (39 PCs); PG gate PASS (39 PGs); MECE 0 findings across 39 register-landed coordinates; register audit agrees with catalog reality.
- Process Identity gate (CI-enforced): PASS (BP-ARC-ID-001..005).
- L2 qualification / intent / lifecycle-state / SIV: 0 findings across the 130-BP universe; ECF conformance PASS (669 entries; `ecf:enablementAndOperations.retire` validates against the canonical 49-space (the canonical domain token keeps "And": enablementAndOperations, per dea-metamodel DOMAIN_ID)).
- Discovery gate [19]: unaffected (14 records, 0 findings).

## 5. Tranche Plan Status

| Slice | Status |
|---|---|
| CR-BP-62 (discovery method + DISC gate) | Merged (PR #103) |
| CR-BP-63 (Activate/Retire discovery exercise) | Merged (PR #104) |
| CR-BP-64 (P&V pair admission) | Merged (PR #105) |
| CR-BP-65 (G&E Activate admission) | Merged (PR #106) |
| CR-BP-66 (E&O Retire admission) | This slice |
| P&R Retire admission (Close Enterprise Relationship) | Next |
| L3 decomposition of the admitted BPs | Follow-on L3 tranche slices |

## 6. What This CR Is NOT

- **NOT a blanket Activate/Retire reversal.** Ten cells remain backlog-deferred with documented CR-BP-63 outcomes; only the evidence-backed E&O/Retire cell flips in this slice.
- **NOT a new discovery.** The evaluation is CR-BP-63's; this slice enacts it.
- **NOT an L3 decomposition.** The new BP carries no Activity records yet (follow-on slice).
- **NOT a specialization.** `process_specialization: []`; specialization work remains unauthorized per program governance.
- **NOT a register re-derivation.** The bump is a targeted disposition reversal; the v4 rederivation basis stands.

## 7. Acceptance Criteria

1. PC gate PASS with 38 PCs; PG gate PASS with 38 PGs; the new composes target resolves.
2. MECE 0 findings across 38 register-landed coordinates; register audit agrees with catalog reality.
3. Register v7 ratification block consistent: 39 ratified-accepted / 10 backlog-deferred; the E&O/Retire admission note cites the CR-BP-63 record and the met escape condition.
4. Count assertions updated (BP 130 / PG 39 / PC 39 / EXE 670 / report 709 / tranches 69); full pytest suite passes.
5. `scripts/conformance_result.py` remains CONFORMANT (24 gates).
6. `python3 scripts/check_cr_metadata.py` reports 0 new findings.
7. Process Identity gate passes on the admitted BP (BP-ARC-ID-001 name = verb + object).

## 8. Result

CR-BP-66 admits the fourth discovery-recommended canonical Business Process and the second at a Retire coordinate, meeting the register's own v2 escape condition with ISO 55000-grade evidence. The catalog covers 39 of 49 ECF coordinates with canonical stacks; 11 Activate/Retire cells hold documented discovery outcomes.
