# CR-BP-71 - P&R Activate admission tranche (Regulated Onboarding, KYC)

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
**Date**: 2026-09-15

## 1. Change Request

Governed admission of the CR-BP-70 escape-clause recommendation at the
PartyAndRelationship x Activate coordinate. Lands the canonical PC + PG + BP
stack:
- `dea:pc-pr-act` (Process Context)
- `dea:group-regulated-onboarding` (Process Group)
- `dea:process-onboard-regulated-party-relationship` (Business Process)

The register cell flips from backlog-deferred to ratified-accepted / landed
in register v9. The register v2 cell's verbatim escape condition ("defer until
a regulated onboarding (e.g. KYC for financial services) requires a distinct
group") is activated by the CR-BP-70 discovery evidence (FATF R.10, FinCEN
CDD 31 CFR 1010.230 + CIP, EU AMLD4/AMLD5/AMLD6, Basel BCBS ML/FT guidelines,
Wolfsberg Group guidance).

## 2. Mechanics

- PC + PG + BP landed together (CR-BP-62 method, CR-BP-70 evidence, CR-BP-71
  admission slice).
- BP name: "Onboard Regulated Party Relationship" satisfies BP-ARC-ID-001
  (verb + object form, no refinement needed; id preserved unchanged from
  the CR-BP-70 discovery recommendation).
- PG kind: cross-cutting (per CR-BP-66 precedent for KYC/AML group classification).
- BP process_type: standardization (control-oriented regulated onboarding);
  process_intent: manage (governance-style intent per the standardized
  onboarding discipline).
- Admission deposition at
  `entities/v1-alpha/dea:process-onboard-regulated-party-relationship/research/l2-admission-deposition.yaml`
  cites the discovery record, score, evidence, and ADM-001 authority.
- ADM-001 admission-authority regex extended to include CR-BP-71
  (`scripts/check_admission_gate.py`).
- Disposition register: RETAIN entry appended.
- Tranche plan: pr-act.71 entry appended; total_tranches 70 -> 71;
  total_records 131 -> 132.

## 3. Gate posture

- ECF conformance: 692 -> 694 entries conform (PC + BP enter the EXE ledger;
  PG does not).
- Process Context (PC-001..008): PASS, 0 findings.
- Process Group (PG-001..008): PASS, 0 findings.
- Process Identity (BP-ARC-ID-001..005): 0 errors, 0 suggestions on
  `dea:process-onboard-regulated-party-relationship` (verified in-process).
- Activity Model (ACT-001..010): CONFORMANT, 0 findings; BP count 131 -> 132.
- Execution Boundary (EXE-001..010): CONFORMANT, 0 findings; 692 -> 694 records.
- Conformance report: 732 -> 735 records (PC + PG + BP all enter the report).
- Dispositions: DISP-OK (0 errors, 113 warnings; warnings unchanged from
  baseline; all are pre-existing advisory cross-check notices).
- Lifecycle Discovery (DISC-001..008): CONFORMANT, 15 records, 0 findings
  (CR-BP-70 escape record still present).
- Cross-Repository Integrity (XRI-001..005): CONFORMANT.
- pytest 383/0; 24-gate suite CONFORMANT (0 blocking, 0 advisory); CR-META
  0 new findings.

## 4. Repository changes

| Path | Status | Purpose |
|---|---|---|
| `contexts/v1-alpha/dea-pc-pr-act.yaml` | NEW | Process Context record |
| `entities/v1-alpha/dea:group-regulated-onboarding/dea:group-regulated-onboarding.yaml` | NEW | Process Group record |
| `entities/v1-alpha/dea:process-onboard-regulated-party-relationship/dea:process-onboard-regulated-party-relationship.yaml` | NEW | Business Process record |
| `entities/v1-alpha/dea:process-onboard-regulated-party-relationship/README.md` | NEW | Entity-dir README (catalog-index requirement) |
| `entities/v1-alpha/dea:process-onboard-regulated-party-relationship/research/README.md` | NEW | Research README |
| `entities/v1-alpha/dea:process-onboard-regulated-party-relationship/research/l2-admission-deposition.yaml` | NEW | L2 admission deposition |
| `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml` | MOD | Cell flipped; version 8 -> 9; counts 40/9 -> 41/8; v8_to_v9_note added |
| `scripts/check_admission_gate.py` | MOD | ADM-001 regex extended to include CR-BP-71 |
| `reconciliation/dispositions/register.yaml` | MOD | RETAIN entry appended (132 dispositions) |
| `reconciliation/tranches/plan.yaml` | MOD | pr-act.71 tranche + records_per_tranche + review_checkpoints entries; totals 70/131 -> 71/132 |
| `tests/test_dispositions.py` | MOD | Count assertion 70 -> 71; docstring updated |
| `tests/test_check_activity_model.py` | MOD | BP count 131 -> 132; docstring updated |
| `tests/test_check_execution_boundary.py` | MOD | Records checked 692 -> 694; docstring updated |
| `tests/test_architectural_regression.py` | MOD | Conformance report 732 -> 735 |
| `change-requests/README.md` | MOD | Index row |
| `reconciliation/baseline/v1.yaml` | MOD | Rebuilt (SHA256s of new PC/PG/BP files) |
| `reconciliation/inventory.yaml` | MOD | Rebuilt |
| `reconciliation/conformance_report.yaml` | MOD | Rebuilt |
| `CATALOG.yaml` | MOD | Regenerated (`open_change_requests` 81 -> 82) |

## 5. What this CR does NOT do

- Does not introduce L3 Activities for `dea:process-onboard-regulated-party-relationship`;
  L3 decomposition is a separate slice.
- Does not flip any other register cell; the 8 remaining Activate/Retire
  backlog-deferred cells retain their dispositions.
- Does not exercise specialization; decomposition-only per governance
  directive (specialization out of scope until L0-L4 stabilizes universally).
- Does not stack on open PRs; branch cut from origin/main post-#111.
- Does not authorize the CR-BP-63 baseline discovery record's
  Commence Relationship (DEFER 5/10) or Activate Customer Journeys
  (RECLASSIFY 2/10) candidates; only the escape-clause candidate is
  enacted.

## 6. Acceptance criteria

- [x] PC + PG + BP validate against their respective schemas (Draft-07, 0
      errors per record).
- [x] PC validation: PASS, 0 findings.
- [x] PG validation: PASS, 0 findings.
- [x] ECF conformance: 694 entries conform.
- [x] BP-ARC-ID-001..005: 0 errors, 0 suggestions on the new BP.
- [x] ACT-001..010, EXE-001..010, MECE-001..008, DISC-001..008: CONFORMANT,
      0 findings.
- [x] ADM-001: gate passes; CR-BP-71 is in the admission-authority regex.
- [x] Dispositions: DISP-OK.
- [x] Register v9: ratified_accepted 41 / backlog_deferred 8; cell disposition
      flipped to ratified-accepted/landed with verbatim escape-clause
      citation.
- [x] Tranche plan: 71 tranches, 132 records; pr-act.71 entry in rpt +
      review.
- [x] Count assertions: architectural_regression 735; activity_model 132 BP;
      execution_boundary 694; dispositions 71.
- [x] Full pytest 383/0; 24-gate suite CONFORMANT; CR-META 0 new.
- [x] CATALOG.yaml regenerated and current.

## 7. Tranche plan status

| Phase | Slice | Status | Gate |
|---|---|---|---|
| 5 | CR-BP-32/33/34 foundation carrier | MERGED (PR #69) | - |
| 5 | CR-BP-34a/b/c/d | MERGED (PRs #70-#73) | [11]-[14] |
| 5 | CR-BP-32 Activity Model | MERGED (PR #74) | [15] |
| 5 | CR-BP-33 Execution Boundary | MERGED (PR #75) | [16] |
| 5 | CR-BP-36 MECE Validation | MERGED (PR #76) | [17] |
| 5 | CR-BP-35 Process Catalog Architecture | MERGED (PR #77) | - |
| 5 | CR-BP-37 Cross-Repository Integrity | MERGED (PR #78) | - |
| 5 | CR-BP-38 ECF Matrix Population retrospective | MERGED (PR #79) | - |
| 5 | CR-BP-62 lifecycle discovery method | MERGED (PR #103) | [19] |
| 5 | CR-BP-63 Activate/Retire discovery | MERGED (PR #104) | - |
| 5 | CR-BP-64 P&V Activate/Retire admission | MERGED (PR #105) | - |
| 5 | CR-BP-65 G&E Activate admission | MERGED (PR #106) | - |
| 5 | CR-BP-66 E&O Retire admission | MERGED (PR #107) | - |
| 5 | CR-BP-67 P&R Retire admission | MERGED (PR #108) | - |
| 5 | CR-BP-68 PC processes-list hygiene | MERGED (PR #109) | - |
| 5 | CR-BP-69 admitted-BP L3 decomposition | MERGED (PR #110) | - |
| 5 | CR-BP-70 P&R Activate escape-clause discovery | MERGED (PR #111) | - |
| **5** | **CR-BP-71 P&R Activate admission** | **This PR** | - |

## 8. Result

Landed as PR #112. The PartyAndRelationship x Activate coordinate is now
populated with a full L0 -> L2 stack backed by authoritative regulatory
evidence; the register v2 escape clause is activated verbatim. Catalog
posture: 132 BP / 521 Activities / 41 of 49 coordinates at full L0-L3 (the
8 remaining Activate/Retire cells remain backlog-deferred with documented
CR-BP-63 outcomes). The escape-clause workstream is complete for the
strongest of the 9 backlog-deferred cells (sequence item 1); the next
candidate per the recommended ordering is A&O x Retire (mass-layoff
regulated wind-down).
