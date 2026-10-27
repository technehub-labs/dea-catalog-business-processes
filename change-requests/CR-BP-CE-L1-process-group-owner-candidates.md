# CR-BP-CE-L1: Process Group Owner Candidates Tranche (the 49 L1 records)

**Status**: Proposed
**Layer**: Process Catalog (Adopted-Field Population)
**Owner**: Emmanuel A. Otchere
**Depends on**: CR-BP-CE-0, CR-BP-CE-L0
**Companion to**: CR-BP-94-EXT-24

> **Scope.** This is the second level tranche of the completeness programme
> ratified under CR-BP-CE-0 §6 (item 3: "CR-BP-CE-L1 -- the 49 ProcessGroup
> records"). It lands the L1 adopted field -- `owner` -- on all 49
> ProcessGroup records as **status: proposed candidates** per the §5
> provenance policy. Post-tranche the gate [50] CE-L1 profile reports
> **0 findings** (49 CE-L1-005 resolved); the programme total drops from
> 1,210 to 1,161 advisory findings.

---

## 1. Background

The CR-BP-CE-0 §3 L1 profile declares `owner` an **adopted** field:
"knowledge-dependent -> admitted as `status: proposed` candidate during
tranche (see §5)". The pre-tranche baseline found all 49 ProcessGroup
records without the field (49 CE-L1-005 advisory findings).

The EXT-24 closure (CR-BP-94-EXT-24, REQ-24-10) landed the L2 BP ownership
register (`reconciliation/closure/ownership-register.json`): every L2
Business Process has an explicit ownership disposition, and **where the
actual owner is not yet known, the disposition is `awaiting_owner_confirmation`
with a Process Domain Reviewer (GOV-003) responsible for assigning it**,
review due 2026-12-31. This tranche carries that same governed disposition
to the L1 level: no owner name is invented.

## 2. What this tranche lands (normative)

### 2.1 The additive schema extension

`schemas/entities/process-group.schema.json` gains an OPTIONAL `owner`
property (`additionalProperties: false` at the schema root is unchanged; the
property is declared, not opened). Shape:

```yaml
owner:
  value: awaiting_owner_confirmation   # the EXT-24 register disposition
  status: proposed                      # CR-BP-CE-0 §5 candidate lifecycle
  provenance:
    type: inference
    asserted_by: dea-completeness-programme
    asserted_at: '2026-10-27'
    reference: change-requests/CR-BP-CE-L1-process-group-owner-candidates.md
  review_due: '2026-12-31'
  decision_right: >-
    Process Domain Reviewer (GOV-003) confirms; Business Process Owner
    (GOV-002) holds the accountability once confirmed
```

Back-compat: the field is OPTIONAL; the pre-tranche records were and remain
schema-conformant. `status` admits `proposed` -> `confirmed`; the transition
to `confirmed` is GOV-003's decision right and is NOT performed by this
tranche.

### 2.2 The 49 record updates

Every ProcessGroup record gains the `owner` block above (identical governed
disposition; per-record confirmation remains the reviewer's act). No other
field on any record is touched. The one-shot migration is
`scripts/remediate_ce_l1.py`, retained as the governance record.

### 2.3 Provenance policy compliance (§5)

- Knowledge-dependent field lands as `status: proposed` -- the report's
  "candidate -- awaiting ratification" marker clears only on GOV-003
  confirmation.
- The generated value satisfies no `identity.evidence_links`; evidence stays
  human/evidence-bound (no evidence block is touched).

## 3. What is NOT changed

- No ProcessContext, Business Process, Activity, or Task record is touched.
- No `cell_charter`, `admission`, `change_history`, `audit`, `metadata`,
  `evidence`, `ecfConformance`, `composes`, or identity block on any
  ProcessGroup is modified; the `owner` key is the only addition.
- No validator rule, gate registration, or template changes beyond the
  additive schema property.
- No record is added or removed; the catalogue remains 3,723 records.

## 4. Verification

- All 49 ProcessGroup records validate against the extended
  `process-group.schema.json` (Draft7, the CI dispatch).
- `python scripts/check_completeness.py` -- CE-L1 findings **0** (was 49);
  0 blocking; total advisory 1,210 -> **1,161**.
- `python scripts/check_process_group.py` -- PASS.
- `reconciliation/completeness-report.yaml` regenerated (CE-900
  post-tranche counters).

## 5. Out of scope / next steps

1. **GOV-003 confirmation sweep** -- the Process Domain Reviewer confirms
   or amends each candidate (the `status: proposed -> confirmed` transition);
   the ownership register's review window closes 2026-12-31.
2. **CR-BP-CE-L2** -- the 145 Process adopted-field tranche
   (`process_classification`, `context`, `trigger`, `outcome`, `identity`,
   `owner`, `actors`, `stakeholders`).
3. **CR-BP-CE-RL** -- flip gate [50] to strict once all level tranches land.

**D-004 clean.**
