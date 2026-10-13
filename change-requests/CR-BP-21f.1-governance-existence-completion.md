# CR-BP-21f.1: GovernanceAndExistence Completion (ECF v2.4.0 — Retroactive Register Coverage)

**Status**: Proposed
**Admission authority**: yes
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-08
**Depends on**: CR-BP-19 (register v2), CR-BP-13a (GE seed landing), CR-BP-21e.1 (merged, PR #59)
**Tranche**: `cr-bp-21f.1`

## Summary

CR-BP-21f.1 completes the GovernanceAndExistence (GE) domain's register v2
L2 coverage. GE was landed before the register-v2 completion discipline
existed (seeds landed under CR-BP-13a and the legacy ge-* reclassification
tranches), so its register v2 candidate list was never fully populated.

Audit of register v2 GE candidates against the live catalog found the
entire **risk-framework track** unlanded (one candidate per lifecycle
stage), plus three further uncovered candidates:

| Cell | Register candidates | Landed before | New (this CR) |
|---|---|---|---|
| GE.Conceive | 4 | 3 covered by 2 seeds | 1 — Frame Risk Framework Direction |
| GE.Design | 4 | 3 covered by 2 seeds | 1 — Design Risk Framework |
| GE.Build | 3 | 2 covered by 2 seeds | 1 — Establish Risk and Control Apparatus |
| GE.Operate | 4 | 2 covered by 2 seeds | 2 — Operate Enterprise Risk Oversight, Conduct Assurance Review |
| GE.Improve | 3 | 1 covered by 1 seed | 2 — Score Audit Findings, Improve Policy and Control Framework |

After this CR: all 18 register v2 GE candidates are covered by 16 BPs
(9 seeds + 7 new; three candidates are covered by broader seeds).

## Scope

### New L2 Business Processes (7)

| EID | Cell | Type |
|---|---|---|
| `dea:process-frame-risk-framework-direction` | GE.Conceive | strategic |
| `dea:process-design-risk-framework` | GE.Design | strategic |
| `dea:process-establish-risk-and-control-apparatus` | GE.Build | core |
| `dea:process-operate-enterprise-risk-oversight` | GE.Operate | core |
| `dea:process-conduct-assurance-review` | GE.Operate | standardization |
| `dea:process-score-audit-findings` | GE.Improve | standardization |
| `dea:process-improve-policy-and-control-framework` | GE.Improve | standardization |

### No new L1 Process Groups

GE's five L1 groups already exist (CR-BP-13a). This CR patches them in
place:

- `dea:group-governance-conception` — +1 composes edge
- `dea:group-governance-system-design` — +1 composes edge
- `dea:group-governance-body-establishment` — +1 composes edge
- `dea:group-governance-oversight` — +2 composes edges
- `dea:group-governance-review-and-learning` — +2 composes edges

Each group receives a matching `change_history` entry.

### Context patches (5)

The five GE Process Contexts (`dea-pc-ge-{c,d,b,op,im}.yaml`) have their
`processes:` lists extended with the new L2 IDs.

### Bookkeeping

- Disposition register: +7 RETAIN entries (tranche `cr-bp-21f.1`)
- Tranche plan: 60 → 65 tranches, 119 → 126 records
- Inventory / baseline / conformance report / CATALOG regenerated
- Test counts updated (BPs 119 → 126; conformance records 189 → 196)

## Coverage rationale (candidate-by-candidate)

Register candidates already covered by existing seeds (verified against
seed outcome statements):

- "Conceive enterprise charter" → `dea:process-initiate-policy-and-charter`
- "Frame mandate and authority model" → `dea:process-develop-governance-strategy`
- "Conceive policy direction" → `dea:process-develop-governance-strategy`
  (outcome: "…mandate, strategic posture, and policy direction…")
- "Design governance framework" → `dea:process-design-governance-system`
- "Design policy architecture" + "Design control objectives" →
  `dea:process-design-policies-and-controls` (outcome covers "policy
  artefacts, control objectives, and compliance regime")
- "Establish board and committees" → `dea:process-establish-governance-bodies`
- "Codify policies and standards" → `dea:process-codify-charters-and-policies`
- "Run board and committee cycle" → `dea:process-operate-governance-oversight`
- "Operate policy compliance" → `dea:process-audit-policy-compliance`
- "Conduct governance effectiveness review" →
  `dea:process-review-governance-effectiveness`

Uncovered candidates landed by this CR (the risk-framework track plus
assurance/audit-scoring/policy-improvement) — see the table above.

## Compliance

- BP-ARC-ID-001: all names are `<single-word verb> <object>`; identity
  verbs match `^[A-Z][a-z]+$`
- BP-ARC-ID-004: outcome statements carry own-type keyword density ≥ 0.3
  (substring matching, per `scripts/check_process_identity.py`)
- L2 identity structure: top-level `trigger:` / `outcome:` scalars plus
  `triggers:` / `outcomes:` lists plus `identity:` block
- CST-004: `lifecycle_status: candidate` + `status: candidate` on all
  new records
- ECF namespace: `ecf:governanceExistence.*` (canonical short camelCase)
- ProcessGroup records untouched in shape; only `composes:` and
  `change_history:` extended via surgical text patches

## Verification

- `check_process_group.py`: PASS (PG-001..008)
- `check_process_context.py`: PASS (PC-001..008)
- `check_process_identity.py`: PASS (no new findings on the 7 records)
- `check_ecf_conformance.py`: PASS (161 entries)
- `check_admission_gate.py --strict-provenance`: CONFORMANT
- pytest: green (same pre-existing STRUCT-OK stderr test bug as main)
- Consumer drift detector (dea-metamodel, local): 0 hard failures
