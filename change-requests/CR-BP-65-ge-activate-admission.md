# CR-BP-65: G&E Activate Admission Tranche (Bring into Force)

**Status**: Proposed
**Layer**: L2 (Activate admission)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-14
**Carrier**: Second governed admission from the CR-BP-63 discovery exercise: lands the Bring into Force recommendation (9/10) at its primary cell (GovernanceAndExistence x Activate) as a full PC + PG + BP stack, and reverses the register cell from backlog-deferred to ratified-accepted/landed (register v6).
**Depends on**: CR-BP-62 (discovery method); CR-BP-63 (discovery records); CR-BP-64 (first admission tranche; ADM-001 authority registration pattern); CR-BP-02 (PC profile); CR-BP-12 (PG profile)
**Lands against**: 128 canonical BP records (127 active + 1 deprecated), 37 canonical PG records, 37 canonical PC records, 501 canonical Activity records; 24 conformance gates CONFORMANT; CR-BP-63 merged (PR #104); CR-BP-64 merged (PR #105)

---

## 1. Change Request

Admit the CR-BP-63 discovery outcome at GovernanceAndExistence x Activate:

**Bring into Force** (score 9/10): the commencement of adopted governance instruments. Evidence base: entry-into-force semantics are universal in legal-regulatory systems (adoption vs commencement are distinct, governed events in every jurisdiction's statute and regulation practice), corporate governance practice (board resolutions and charters take effect upon adoption-plus-commencement conditions), and standard-setter practice (effective-date mechanics for new standards).

This admission overturns the register v2 per-cell deferral note ("governance activation is an attribute of governance operate") with evidence: adoption and commencement are distinct events with distinct triggers, transformations and outcomes (BP-LIFE-002/003/004), and the transformation's identity ("entry into force") is wholly independent of the ECF stage label (BP-LIFE-009).

## 2. Naming and Lineage

The register v2 l2 candidates for this cell were "Onboard governance bodies / Activate policy regime". The CR-BP-63 evaluation established the stronger candidate (Bring into Force) on evidence and ECF-independence grounds. At admission the record name is refined to satisfy BP-ARC-ID-001 (name = verb + object): **Bring Policy Instrument into Force** (verb Bring; object Policy Instrument into Force). The discovery candidate name and the proposed id (`dea:process-bring-into-force`) are unchanged; the deposition carries the naming_note.

## 3. Repository Changes

| Path | Status | Notes |
|---|---|---|
| `contexts/v1-alpha/dea-pc-ge-activate.yaml` | NEW | PC: Governance Instrument Commencement (full cell charter) |
| `entities/v1-alpha/dea:group-governance-instrument-commencement/` | NEW | PG + README; `process_group_kind: governance`; composes the new BP |
| `entities/v1-alpha/dea:process-bring-into-force/` | NEW | BP + README + research/l2-admission-deposition.yaml |
| `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml` | MOD | Register v6: G&E/Activate flipped with admission note; ratification block 38 accepted / 11 deferred |
| `scripts/check_admission_gate.py` | MOD | ADM-001 admission-authority vocabulary: CR-BP-65 registered |
| `reconciliation/dispositions/register.yaml` | MOD | RETAIN entry for the new BP |
| `reconciliation/tranches/plan.yaml` | MOD | ge-act.65 tranche appended (68 tranches, 129 records) |
| `tests/` (9 files) | MOD | Count assertions: BP 128 -> 129; PG 37 -> 38; PC 37 -> 38; EXE 666 -> 668; report 703 -> 706 (PC + PG + BP all enter the report); tranches 67 -> 68 |
| `scripts/check_activity_model.py`, `scripts/check_mece.py` | MOD | Docstring count text only |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated; 706 records, all L4 |
| `change-requests/CR-BP-65-ge-activate-admission.md` | NEW | This document |
| `change-requests/README.md` | MOD | CR-BP-65 row |
| `CATALOG.yaml` | MOD | Regenerator: 667 entities; `open_change_requests` 76 -> 77 |

## 4. Coverage on the Live Catalog

- PC gate PASS (38 PCs); PG gate PASS (38 PGs); MECE 0 findings across 38 register-landed coordinates; register audit agrees with catalog reality.
- Process Identity gate (CI-enforced): PASS (BP-ARC-ID-001..005).
- L2 qualification / intent / lifecycle-state / SIV: 0 findings across the 129-BP universe; ECF conformance PASS (667 entries; `ecf:governanceExistence.activate` validates against the canonical stage vocabulary).
- Discovery gate [19]: unaffected (14 records, 0 findings).

## 5. Tranche Plan Status

| Slice | Status |
|---|---|
| CR-BP-62 (discovery method + DISC gate) | Merged (PR #103) |
| CR-BP-63 (Activate/Retire discovery exercise) | Merged (PR #104) |
| CR-BP-64 (P&V pair admission) | Merged (PR #105) |
| CR-BP-65 (G&E Activate admission) | This slice |
| E&O Retire admission (Decommission) | Next |
| P&R Retire admission (Close Enterprise Relationship) | Next |
| L3 decomposition of the admitted BPs | Follow-on L3 tranche slices |

## 6. What This CR Is NOT

- **NOT a blanket Activate/Retire reversal.** Eleven cells remain backlog-deferred with documented CR-BP-63 outcomes; only the evidence-backed G&E/Activate cell flips.
- **NOT a new discovery.** The evaluation is CR-BP-63's; this slice enacts it.
- **NOT an L3 decomposition.** The new BP carries no Activity records yet (follow-on slice).
- **NOT a specialization.** `process_specialization: []`; specialization work remains unauthorized per program governance.
- **NOT a register re-derivation.** v6 is a targeted disposition reversal; the v4 rederivation basis stands.

## 7. Acceptance Criteria

1. PC gate PASS with 38 PCs; PG gate PASS with 38 PGs; the new composes target resolves.
2. MECE 0 findings across 38 register-landed coordinates; register audit agrees with catalog reality.
3. Register v6 ratification block consistent: 38 ratified-accepted / 11 backlog-deferred; the G&E/Activate admission note cites the CR-BP-63 record.
4. Count assertions updated (BP 129 / PG 38 / PC 38 / EXE 668 / report 706 / tranches 68); full pytest suite passes.
5. `scripts/conformance_result.py` remains CONFORMANT (24 gates).
6. `python3 scripts/check_cr_metadata.py` reports 0 new findings.
7. Process Identity gate passes on the admitted BP (BP-ARC-ID-001 name = verb + object).

## 8. Result

CR-BP-65 admits the third discovery-recommended canonical Business Process and the first in the GovernanceAndExistence domain, on the strongest ECF-independence evidence in the exercise: entry into force is a universal, framework-independent enterprise transformation. The catalog now covers 38 of 49 ECF coordinates with canonical stacks; 11 Activate/Retire cells hold documented discovery outcomes.
