# CR-BP-67: P&R Retire Admission Tranche (Close Enterprise Relationship)

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
**Carrier**: Fourth and final governed admission from the CR-BP-63 discovery exercise: lands the Close Enterprise Relationship recommendation (9/10) at its primary cell (PartyAndRelationship x Retire) as a full PC + PG + BP stack, and reverses the register cell from backlog-deferred to ratified-accepted/landed (register v8). Completes the discovery programme's recommended admissions.
**Depends on**: CR-BP-62 (discovery method); CR-BP-63 (discovery records); CR-BP-64 (first admission tranche; ADM-001 authority registration pattern); CR-BP-02 (PC profile); CR-BP-12 (PG profile)
**Lands against**: 130 canonical BP records (129 active + 1 deprecated), 39 canonical PG records, 39 canonical PC records, 501 canonical Activity records; 24 conformance gates CONFORMANT; CR-BP-63 merged (PR #104); CR-BP-64 merged (PR #105); CR-BP-65 merged (PR #106); CR-BP-66 merged (PR #107)

---

## 1. Change Request

Admit the CR-BP-63 discovery outcome at PartyAndRelationship x Retire:

**Close Enterprise Relationship** (score 9/10): the close-out of enterprise relationships across customer, supplier and partner roles. Evidence base: contract close-out practice (termination settlement, obligation discharge, close-out certification as a stable industry-neutral discipline); eTOM service retirement and party offboarding identities; regulated offboarding obligations (GDPR-driven erasure) that make close-out a governed, evidenced activity.

As with CR-BP-66, this admission meets the register v2 cell's own escape condition verbatim: the v2 deferral said "defer until a regulated offboarding (e.g. GDPR-driven erasure) requires a distinct group." The discovery evaluation established close-out as exactly that governed discipline (BP-LIFE-002/003/004/009).

## 2. Naming and Lineage

The register v2 l1 candidate "Relationship Termination" is adopted directly as the Process Group name -- the discovery evaluation confirmed it. The BP name satisfies BP-ARC-ID-001 without refinement: **Close Enterprise Relationship** = verb Close + object Enterprise Relationship, identical to the discovery candidate name. The register v2 l2 candidates (offboarding / contract termination / supplier exit) are party-role flavors of the admitted canonical process; the admission note records the supersession.

**DISC-007 lifecycle extension.** The exact-name admission surfaced a gap in the discovery gate: its duplicate-name check fired on the enacted recommendation itself. This slice extends the discovery schema with an optional per-candidate `admission` block (recording the admitting CR and the canonical BP id) and extends DISC-007: enacted recommendations skip the duplicate-name face and are instead verified to resolve (`admitted_as` must point at a canonical BP record). The admission blocks are recorded on all five enacted candidates across the CR-BP-64..67 admissions, making the recommendation-to-admission lifecycle explicit and machine-verified. Prior admissions escaped the duplicate-name face only by name refinement (CR-BP-64..66); this extension removes that accidental dependence.

## 3. Repository Changes

| Path | Status | Notes |
|---|---|---|
| `contexts/v1-alpha/dea-pc-pr-retire.yaml` | NEW | PC: Enterprise Relationship Close-Out (full cell charter) |
| `entities/v1-alpha/dea:group-relationship-termination/` | NEW | PG + README; `process_group_kind: cross-cutting` (spans customer/supplier/partner roles); composes the new BP |
| `entities/v1-alpha/dea:process-close-enterprise-relationship/` | NEW | BP + README + research/l2-admission-deposition.yaml |
| `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml` | MOD | Register v8: P&R/Retire flipped with admission note recording the met escape condition; ratification block 40 accepted / 9 deferred |
| `schemas/discovery/lifecycle-discovery.schema.json` | MOD | Optional per-candidate `admission` block (status/admitted_by/admitted_as/admitted_at): records that a recommendation has been enacted |
| `scripts/check_lifecycle_discovery.py` | MOD | DISC-007 lifecycle extension: an ADMIT-CANONICAL candidate with `admission.status: admitted` skips the duplicate-name face and instead requires `admitted_as` to resolve to a canonical BP record; checker plumbing carries a (names, ids) index; self-test gains admitted/admitted-dangling cases (21 cases) |
| `discovery/v1-alpha/{product-and-value-activate,product-and-value-retire,governance-and-existence-activate,enablement-and-operations-retire,party-and-relationship-retire}.yaml` | MOD | Admission blocks recorded on the five enacted candidates (CR-BP-64/65/66/67) |
| `scripts/check_admission_gate.py` | MOD | ADM-001 admission-authority vocabulary: CR-BP-67 registered |
| `reconciliation/dispositions/register.yaml` | MOD | RETAIN entry for the new BP |
| `reconciliation/tranches/plan.yaml` | MOD | pr-ret.67 tranche appended (70 tranches, 131 records) |
| `tests/` (9 files) | MOD | Count assertions: BP 130 -> 131; PG 39 -> 40; PC 39 -> 40; EXE 670 -> 672 (BP + PG enter the ledger); report 709 -> 712 (PC + PG + BP enter the report); tranches 69 -> 70 |
| `scripts/check_activity_model.py`, `scripts/check_mece.py` | MOD | Docstring count text only |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated; 712 records, all L4 |
| `change-requests/CR-BP-67-pr-retire-admission.md` | NEW | This document |
| `change-requests/README.md` | MOD | CR-BP-67 row |
| `CATALOG.yaml` | MOD | Regenerator: 670 entities; `open_change_requests` 78 -> 79 |

## 4. Coverage on the Live Catalog

- PC gate PASS (40 PCs); PG gate PASS (40 PGs); MECE 0 findings across 40 register-landed coordinates; register audit agrees with catalog reality.
- Process Identity gate (CI-enforced): PASS (BP-ARC-ID-001..005); the record name satisfies the name = verb + object contract without refinement.
- L2 qualification / intent / lifecycle-state / SIV: 0 findings across the 131-BP universe; ECF conformance PASS (670 entries; `ecf:partyRelationship.retire` against the canonical 49-space).
- Drift detector (dea-metamodel, canonical 49-space): 0 hard failures.
- Discovery gate [19]: unaffected (14 records, 0 findings).

## 5. Tranche Plan Status

| Slice | Status |
|---|---|
| CR-BP-62 (discovery method + DISC gate) | Merged (PR #103) |
| CR-BP-63 (Activate/Retire discovery exercise) | Merged (PR #104) |
| CR-BP-64 (P&V pair admission) | Merged (PR #105) |
| CR-BP-65 (G&E Activate admission) | Merged (PR #106) |
| CR-BP-66 (E&O Retire admission) | Merged (PR #107) |
| CR-BP-67 (P&R Retire admission) | This slice -- completes the recommended admissions |
| L3 decomposition of the five admitted BPs | Follow-on L3 tranche slices |

## 6. What This CR Is NOT

- **NOT a blanket Activate/Retire reversal.** Nine cells remain backlog-deferred with documented CR-BP-63 outcomes (RECORD-PATTERN / DEFER / process-empty); only the evidence-backed P&R/Retire cell flips.
- **NOT a new discovery.** The evaluation is CR-BP-63's; this slice enacts it.
- **NOT an L3 decomposition.** The new BP carries no Activity records yet (follow-on slice).
- **NOT a specialization.** `process_specialization: []`; specialization work remains unauthorized per program governance.
- **NOT a register re-derivation.** v8 is a targeted disposition reversal; the v4 rederivation basis stands.

## 7. Acceptance Criteria

1. PC gate PASS with 40 PCs; PG gate PASS with 40 PGs; the new composes target resolves.
2. MECE 0 findings across 40 register-landed coordinates; register audit agrees with catalog reality.
3. Register v8 ratification block consistent: 40 ratified-accepted / 9 backlog-deferred; the P&R/Retire admission note cites the CR-BP-63 record and the met escape condition.
4. Count assertions updated (BP 131 / PG 40 / PC 40 / EXE 672 / report 712 / tranches 70); full pytest suite passes.
5. `scripts/conformance_result.py` remains CONFORMANT (24 gates).
6. `python3 scripts/check_cr_metadata.py` reports 0 new findings.
7. Process Identity gate passes on the admitted BP.

## 8. Result

CR-BP-67 completes the discovery programme's recommended admissions: all five ADMIT-CANONICAL candidates from CR-BP-63 are now canonical Business Processes with full PC + PG stacks, and the register stands at v8 with 40 ratified-accepted coordinates and 9 backlog-deferred cells holding documented discovery outcomes. The catalog covers 40 of 49 ECF coordinates with canonical stacks. The full method cycle (CR-BP-62 method -> CR-BP-63 evidence -> CR-BP-64..67 governed admissions) is proven end to end, including two register escape conditions met on evidence.
