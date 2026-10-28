# CR-BP-GS-1: Governance Sweep (GOV-002 Owner Ratification + GOV-003 Role-Based Derivation)

**Status**: Proposed
**Layer**: Process Catalog (Governance)
**Owner**: Emmanuel A. Otchere
**Depends on**: CR-BP-CE-0, CR-BP-CE-L1, CR-BP-CE-L2, CR-BP-CE-RL
**Companion to**: CR-BP-94-EXT-24

> **Scope.** The GOV-002/GOV-003 governance sweep closing the completeness
> programme's final open items (the CE-RL carve-out population): the 194
> proposed `owner` candidates are CONFIRMED under the GOV-002 domain-level
> ratification, and the 290 CE-L2-006 `actors`/`stakeholders` findings are
> populated under the GOV-003 role-based derivation policy. Post-sweep the
> gate [50] profile reports **0 blocking, 0 advisory** across all 3,723
> records: the catalogue is 100% complete on its ratified profiles.

---

## 1. The ratifications (normative)

Both decisions were ratified by the GOV-002/GOV-003 role-holder
(2026-10-27) as **role-based** policies:

### 1.1 GOV-002: domain-level Process Owner roles (194 owners CONFIRMED)

One Process Owner role per domain covers all L1 ProcessGroups and L2
Business Processes of that domain:

| Domain | Owner role |
|---|---|
| AgencyAndOrganization | Agency & Organization Process Owner |
| EnablementAndOperations | Enablement & Operations Process Owner |
| FinanceAndAccounting | Finance & Accounting Process Owner |
| GovernanceAndExistence | Governance & Existence Process Owner |
| PartyAndRelationship | Party & Relationship Process Owner |
| ProductAndValue | Product & Value Process Owner |
| StrategyAndDirection | Strategy & Direction Process Owner |

Each of the 194 owner blocks flips `status: proposed -> confirmed` with
`value: <domain owner role>` and `provenance.type: manual` (the GOV-002
decision record is the reference).

### 1.2 GOV-003: charter-derived actor/stakeholder roles (145 BPs)

The actor/stakeholder lists are **derived from each record's own parent
cell charter vocabulary** — only roles the charter actually names (its
inclusions / expected_outcomes / adjacent_boundaries) are assigned:

- keyword mapping (charter term -> role): regulator -> industry
  regulator; supervisor -> supervising authority; board -> governing
  board; audit -> audit function; risk -> risk function; legal -> legal
  function; compliance -> compliance function; finance -> finance
  function; workforce -> workforce management; customer -> customer
  relationship management; supplier -> supplier and partner management;
  operations -> operations function; product -> product management;
  strategy -> strategy function; human resources -> HR function.
- **Fallback**: where the charter's vocabulary is purely architectural
  (e.g. `pc-ao-design`: organization structure, role catalogue,
  competency framework), the minimal charter-honest role is the domain's
  design authority (e.g. organization design authority).
- Both `actors` and `stakeholders` carry the derived role list: the
  charter derivation does not reliably distinguish performers from
  oversight parties; **per-record refinement remains the GOV-003
  standing review item** (the EXT-23 human_review classification).

Each landing records its provenance in `metadata.change_history`
(CR-BP-GS-1, 2026-10-27).

## 2. What this slice lands

1. 49 ProcessGroup owner confirmations (proposed -> confirmed).
2. 145 Business Process owner confirmations + actors/stakeholders
   derivation (with metadata.change_history entries).
3. This CR document; CHANGELOG; the change-requests README registration;
   CATALOG.yaml post-commit regeneration; the completeness report
   (CE-900: 0/0).
4. The one-shot migration `scripts/governance_sweep.py`, retained as the
   governance record.

## 3. What is NOT changed

- No ProcessContext, Activity, or Task record is touched.
- No schema change (actors/stakeholders were already declared as
  string arrays; the owner block schema landed in CE-L1/L2).
- No gate or severity change (gate [50] remains blocking; it now guards
  a fully-clean profile).

## 4. Verification

- `python scripts/check_completeness.py --strict` — **0 blocking, 0
  advisory** across 3,723 records (the CE-L2-006 population is closed).
- All 49 PG owner blocks: status confirmed.
- All 145 BP owner blocks: status confirmed; actors/stakeholders
  non-empty; every record carries the CR-BP-GS-1 change_history entry.

## 5. Standing review items (post-sweep)

1. **GOV-003 per-record actor refinement** — the derived lists are
   charter-honest but coarse (performers vs oversight not
   distinguished); refine opportunistically.
2. The EXT-24 ownership register's `awaiting_owner_confirmation`
   dispositions should be reconciled to the confirmed roles in a
   follow-up closure update.

**D-004 clean.**
