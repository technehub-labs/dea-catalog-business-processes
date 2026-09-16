# CR-BP-76 - G&E Retire Escape-Clause Discovery (Regulator-Mandated Governance Unwind)

**Status**: Proposed
**Layer**: L0 (Discovery escape-clause record)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-16
**Carrier**: Discovery-only escape-clause slice landing at the previously unpopulated GovernanceAndExistence x Retire coordinate. ADMIT-CANONICAL recommendation only; admission will be a follow-on slice (CR-BP-7x).
**Depends on**: CR-BP-62 (lifecycle discovery method; DISC-001..008), CR-BP-19 (register v2 per-cell escape condition).
**Lands against**: 17 prior canonical Discovery records + 1 new = 18 records; 24-gate suite CONFORMANT (0 blocking, 0 advisory).

---

## 1. Change Request

Targeted escape-clause evaluation of the GovernanceAndExistence x Retire register cell against its verbatim deferral condition (CR-BP-19, register v2):

> "Retirement of governance is rare and largely an attribute of operating-model retirement; defer until a sector example (e.g. regulator-mandated unwind) requires it."

The escape clause is met. The 2024-2026 regulatory landscape (FCA WDPG UK firm wind-down planning, California Corporations Code 5033-5034, 6610, 8610, 9680, IRS 501(c)(3) federal tax-exempt dissolution obligations, state attorney-general charity oversight, federal banking regulator cease-and-desist orders, court receivership decrees) introduces a regulator- or court-mandated unwind scenario that is a legally mandated, boundary-clear, evidence-authoritative transformation distinct from voluntary governance sunset (Improve coordinate), asset retirement (E&O x Retire), counterparty close-out (P&R x Retire), product retirement (P&V x Retire), workforce wind-down (A&O x Retire), and regulated entity run-off (F&A x Retire).

## 2. Candidates evaluated

| # | Candidate | Verdict | Score |
|---|---|---|---|
| 1 | Effect Regulator-Mandated Governance Unwind | **ADMIT-CANONICAL** | 9/10 |
| 2 | Operate Governance Sunset Procedures | DEFER | 5/10 |
| 3 | Document Governance Wind-Down Plan | RECLASSIFY | 3/10 |
| 4 | File Statutory Governance Dissolution Filings | RECLASSIFY | 3/10 |

Candidate 1 is recommended for admission as `dea:process-effect-regulator-mandated-governance-unwind`. ADMIT-CANONICAL is recommendation-only; admission is a follow-on CR. Candidates 3 and 4 are Activity-shaped; once the parent Process is admitted they will be surfaced as L3 decomposition under it. Candidate 2 (voluntary governance sunset) stays DEFER pending the Improve coordinate charter extension per CR-BP-63.

## 3. Mechanics

- One discovery record at `discovery/v1-alpha/governance-and-existence-retire-escape.yaml`, conforming to `schemas/discovery/lifecycle-discovery.schema.json` and the CR-BP-62 section-16 disposition model.
- Each candidate carries a complete 14-field `evaluation` block (per schema) and the canonical `scoring` block (5 dimensions + total + rationale).
- Evidence.sources flattened to string items per schema (the previous object shape was rejected by DISC-001).
- `evidence.evidence_strength` field added per schema requirement.
- `proposed_identity` reduced to verb / object / scope per schema (no `id` key).
- Count assertion updates: tests/test_check_lifecycle_discovery.py 17 -> 18 (three assertions + docstring).

## 4. Gate posture

- Gate [19] DISC-001..008: CONFORMANT, 18 Discovery records (was 17), 0 findings.
- Full suite: 24 gates, 0 blocking, 0 advisory failures (was 1 advisory).

## 5. Repository changes

| Path | Status | Notes |
|---|---|---|
| `discovery/v1-alpha/governance-and-existence-retire-escape.yaml` | NEW | CR-BP-76 escape-clause record; 4 candidates; ADMIT-CANONICAL recommendation on candidate 1 |
| `tests/test_check_lifecycle_discovery.py` | MOD | Count assertions 17 -> 18 (3 sites) + docstring narrative |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 88 -> 89 |

## 6. What this CR is NOT

- **NOT an admission.** The CR-BP-76 record carries an ADMIT-CANONICAL recommendation for candidate 1 only; canonical admission (PC + PG + BP stack at the G&E x Retire coordinate) is a future CR-BP-7x slice per the CR-BP-62 section-20 governance.
- **NOT a schema, validator-rule, CI, or gate change.** The gate wiring from the pilot and CR-BP-62..74 is reused unchanged.
- **NOT an L3 deposition.** Activity-shaped candidates (3 and 4) remain on the recommendation register; they surface as L3 Activities only after the parent Process is admitted.
- **NOT a discovery on adjacent coordinates.** A&O x Retire (CR-BP-72), E&O x Retire (CR-BP-66), P&R x Retire (CR-BP-67), P&V x Retire (CR-BP-67 adjacent), and F&A x Retire (CR-BP-74) are unchanged and remain the canonical evidence for their own cells.

## 7. Acceptance criteria

1. `python3 scripts/check_lifecycle_discovery.py` runs CONFORMANT: 18 records checked, 0 findings.
2. `pytest tests/test_check_lifecycle_discovery.py` passes (3 count assertions + CLI shape + record loader).
3. Full pytest suite passes; 24-gate suite CONFORMANT (0 blocking, 0 advisory).
4. CR-META 0 new findings.
5. CATALOG index strict mode passes.
6. No validator-rule, schema, CI, or governance-decision change.

## 8. Result

CR-BP-76 lands the G&E x Retire escape-clause discovery record. Discovery records 17 -> 18; the previously failing Lifecycle Discovery advisory gate goes green. ADMIT-CANONICAL on candidate 1 is the recommendation; admission is a follow-on slice (CR-BP-7x) per the CR-BP-62 section-20 governance.