# CR-BP-CE-L4: Custodian Vocabulary Normalization + the CE-L0-003 Repair

**Status**: Proposed
**Layer**: Process Catalog (Adopted-Field Population)
**Owner**: Emmanuel A. Otchere
**Depends on**: CR-BP-CE-0, CR-BP-CE-L0, CR-BP-CE-L1, CR-BP-CE-L2
**Companion to**: CR-BP-93, CR-BP-102

> **Scope.** The Activity/Task-level tranche of the completeness programme
> (CR-BP-CE-0 §6). The L3 Activity profile was already clean (no findings);
> the L4 findings were a single systematic defect: the Task `responsibility`
> value on the intake-phase records carried a stray modifier outside the
> 5-phase custodian vocabulary. Post-tranche the gate [50] reports
> **581 fewer advisory findings** (871 -> **290**); the only remaining
> programme findings are the deliberately-deferred CE-L2-006
> `actors`/`stakeholders` candidates (the CR-BP-CE-RL input).

---

## 1. Background

CR-BP-CE-0 §3 (L4 profile) fixes `responsibility` to the 5-phase custodian
vocabulary only: `intake custodian` / `records custodian` / `processing
custodian` / `confirmation custodian` / `verification custodian` (per
CR-BP-102's decomposition template and CR-BP-93 §9). The baseline found
**580 CE-L4-002 findings**: every intake-phase Task record (one per L3
Activity, 580 Activities) carried the value
`designated intake custodian` -- the stray modifier `designated ` placing
it outside the controlled vocabulary. The other four phases were clean.

Root cause: three generator sources emit the stray modifier:
`scripts/decompose_l4.py` (the CR-BP-102 pipeline),
`scripts/enrich_l4_governance_and_existence.py`, and
`scripts/enrich_l4_party_and_relationship.py` (the EXT-06 enrichment
tooling). All three are fixed in this slice so the defect cannot recur.

One further CE-L0-003 advisory finding existed: the
`pc-sd-improve-ft9k5f` ProcessContext carried only 2 `scope.excludes`
entries (the profile requires >= 3).

## 2. What this tranche lands (normative)

### 2.1 The custodian vocabulary normalization (580 CE-L4-002 -> 0)

- 580 Task records: `responsibility: designated intake custodian` ->
  `responsibility: intake custodian` (a pure text-level normalization;
  no other field on any Task record is touched).
- The three generator sources are corrected to emit the controlled
  vocabulary value.

### 2.2 The CE-L0-003 repair (1 -> 0)

`pc-sd-improve-ft9k5f` gains a third `scope.excludes` entry derived from
the cell's own semantics (the regulated strategic-plan sunset belongs to
the Retire cell, an adjacency the cell's own `adjacent_contexts` already
declares): "Regulated strategic-plan sunset under regulatory mandate
(StrategyAndDirection x Retire; adjacent context)".

### 2.3 The CE-L2-006 deferral is reaffirmed

The 290 `actors`/`stakeholders` findings remain the explicit
CR-BP-CE-RL input (no evidence-bound source; per §5 and D-004 they are
populated only by the human governance sweep).

## 3. What is NOT changed

- No ProcessContext, ProcessGroup, Business Process, or Activity record
  is touched (the one PC scope.excludes addition excepted).
- On the 580 Task records: only the `responsibility` value; `trigger`,
  `outcome`, `definition`, `evidence`, `ecfConformance`, `metadata` and all
  other fields are untouched.
- No schema, gate, or template changes.

## 4. Verification

- `python scripts/check_completeness.py` -- 0 blocking; advisory
  871 -> **290** (580 CE-L4-002 + 1 CE-L0-003 resolved; the 290 remaining
  are the deferred CE-L2-006).
- `python scripts/check_task_model.py` -- the five TASK rules hold.

## 5. Next steps

1. **CR-BP-CE-RL** -- the gate posture flip: with all level tranches landed
   and only the governance-sweep-dependent CE-L2-006 findings remaining,
   flip gate [50] to blocking (with the CE-L2-006 exception carve-out) or
   hold advisory until the actors/stakeholders sweep closes.

**D-004 clean.**
