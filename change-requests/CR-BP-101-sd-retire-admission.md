# CR-BP-101: StrategyAndDirection x Retire Admission Tranche

**Status**: Proposed
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-19
**Carrier**: SD/Retire admission tranche that closes the 7x7 = 49-cell matrix. Acts on the CR-BP-80 escape-clause DEFER for SD/Retire (eaojnr 2026-09-19 directive: "let's act on that deferred CR now").
**Doctrine** (eaojnr 2026-09-19): the L0 layer is the Process Context matrix; the matrix must be 7x7 = 49 cells. The SD/Retire cell was deferred at v2 and re-evaluated under CR-BP-80's escape-clause exercise; this slice lands the substantive BP candidate "Sunset Regulated Strategic Plan" (escape score 8) per CR-BP-80's evidence.
**Depends on**: CR-BP-02 (Process Context), CR-BP-12 (Process Group), CR-BP-28 (L0 register v2; SD/Retire deferral), CR-BP-38 (L0 matrix ratification), CR-BP-62 (lifecycle process-discovery method), CR-BP-63 (Activate/Retire baseline discovery), CR-BP-80 (SD/Retire escape-clause discovery), CR-BP-86 (SD/Activate admission tranche).
**Lands against**: 48 PCs / 48 PGs / 139 BPs / 553 Activities / 28 conformance gates CONFORMANT; v0.4.0+10 commits on main.

---

## 1. Change Request

Land the **SD/Retire admission tranche** as PC + PG + BP records that complete the 7x7 = 49-cell ECF matrix. The CR-BP-80 escape-clause discovery yielded the substantive BP candidate "Sunset Regulated Strategic Plan" (regulator-directed sunset of a regulated strategic plan; banking FDICIA Section 131, SRB rejection, Bank of England PRA SS9/17; utilities state PUC retraction; healthcare NHS England directive). This slice acts on that deferred CR.

| Artifact | Status | Notes |
|---|---|---|
| `contexts/v1-alpha/dea-pc-sd-retire.yaml` | NEW | Process Context record for SD/Retire; closes the 49th cell. |
| `entities/v1-alpha/dea:group-regulated-strategic-plan-sunset/dea:group-regulated-strategic-plan-sunset.yaml` | NEW | L1 Process Group record (kind: functional). |
| `entities/v1-alpha/dea:process-sunset-regulated-strategic-plan/dea:process-sunset-regulated-strategic-plan.yaml` | NEW | L2 Business Process record (verb: Sunset; object: Regulated Strategic Plan; scope: enterprise). |
| `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml` | MOD | v17 note appended; SD/Retire flips ratified-accepted/landed; register counts update 47→48 ratified + 1→0 backlog-deferred + 1 follow-on. |
| `change-requests/CR-BP-101-sd-retire-admission.md` | NEW | Slice carrier CR (this document). |
| `change-requests/README.md` | MOD | CR-BP-101 row added. |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 112 → 113. |

## 2. Deposition mechanics

1. **Schema-first.** PC, PG, BP records follow the established admission pattern (CR-BP-86 SD/Activate). The PC carries the cell charter + ECF coordinate + boundaries; the PG carries the bounded process group + MECE scope; the BP carries the canonical business process with trigger/outcome/identity.
2. **No Activity decomposition this slice.** Activity decomposition follows the CR-BP-86 / CR-BP-87 precedent (BP-only admission at SD/Activate; Activity decomposition as a follow-on slice). The BP carries `activity_references:` as null/empty; the future L3 tranche will populate it.
3. **Escape-clause evidence.** CR-BP-80 evaluated the SD/Retire coordinate under the regulator-directed sunset landscape (FDICIA Section 131, SRB rejection, PRA SS9/17, state PUC retraction, NHS England directive) at score 8 (process_reality 2, semantic_stability 2, cross_domain_applicability 1, boundary_clarity 2, evidence_strength 1). The 2024-2026 supervisor-acknowledged sunset regime supersedes the v2 escape condition "Activate and Retire are lifecycle transition stages, not stable Process Group operating scopes."
4. **Register update.** l1-register.yaml advances from v16 → v17: SD/Retire flips ratified-accepted/landed; backlog-deferred count 1 → 0; ratified-accepted count 47 → 48.
5. **L0↔L1 cardinality invariant.** With this slice, the live catalog carries 49 PCs and 49 PGs in 1:1 cardinality. CR-BP-100 (PR #141) introduces the cardinality gate; CR-BP-100a (PR #143) refreshes its live-catalog test counts from 48 to 49 to validate this end-to-end against the post-CR-BP-101 state. PR #143 supersedes PR #141.
6. **Gate posture.** All28 gates remain CONFORMANT (0 blocking, 0 advisory). ECF conformance: 743 entries (was 741; +2 for the new PG and BP records :  PC records don't carry the `ecfConformance` block per the established pattern).

## 3. Cell evidence summary (CR-BP-80 escape-clause)

| Sector | Regulator | Mechanism |
|---|---|---|
| Banking | Federal Deposit Insurance Corporation (FDIC) | FDICIA Section 131 prompt-corrective-action; recovery-plan replacement |
| Banking | Single Resolution Board (SRB) | Bank recovery-plan rejection directive |
| Banking | Bank of England Prudential Regulation Authority (PRA) | SS9/17 recovery and resolution planning; withdrawal under PRA direction |
| Utilities | US state Public Utility Commissions (PUC) | Integrated resource plan and strategic-plan retraction |
| Healthcare | NHS England / Department of Health | Trust 5-year strategy directive |

Identity survival under ECF-label removal (BP-LIFE-009): the "Sunset Regulated Strategic Plan" identity holds whether the cell is named SD/Retire or not :  the verb (sunset), object (regulated strategic plan), and outcome (regulator-acknowledged-and-sunset) are stable.

## 4. Gate posture

- Gate [3] Process Context (PC-001..PC-008): **CONFORMANT, PASS** (49 records).
- Gate [7] MECE (Process Group, PG-001..010): **CONFORMANT, PASS** (49 records).
- Gate [8] Provenance (ECF conformance): **CONFORMANT, 743 entries**.
- Gate [4] Semantics (BP-SEM-001..014): **CONFORMANT**.
- Full suite: **28 gates, 0 blocking, 0 advisory failures**.
- `open_change_requests`: 112 → 113.

## 5. What this CR is NOT

- **NOT an Activity decomposition tranche.** The BP carries `activity_references:` as null; Activity decomposition follows the CR-BP-86 / CR-BP-87 precedent (BP-only admission; Activity decomposition as a follow-on slice). Activity universe discovery is downstream of this admission.
- **NOT a re-opening of CR-BP-20 (PG kind vocabulary).** The new PG uses the existing `functional` kind per CR-BP-12 §6 (controlled vocabulary). No new vocabulary entry.
- **NOT a tightening of the L0↔L1 cardinality invariant to blocking.** Gate [24] (CR-BP-100; PR #141) is advisory; promotion to blocking is a future slice.
- **NOT a re-derivation of the v2 escape condition.** CR-BP-38 ratified all 49 cells; CR-BP-80 documented the SD/Retire escape as the substantive BP admission candidate; this slice acts on that documented outcome.
- **NOT a count assertion change.** The 49-cell matrix is the canonical assertion; this slice completes it. The count itself doesn't change (was 7x7=49; now 49/49 admitted).

## 6. Acceptance criteria

1. `contexts/v1-alpha/dea-pc-sd-retire.yaml` exists and validates against the Process Context schema (`PC-001..PC-008`).
2. `entities/v1-alpha/dea:group-regulated-strategic-plan-sunset/dea:group-regulated-strategic-plan-sunset.yaml` exists and validates against the Process Group schema (`PG-001..010`).
3. `entities/v1-alpha/dea:process-sunset-regulated-strategic-plan/dea:process-sunset-regulated-strategic-plan.yaml` exists and validates against `schemas/entity.schema.json` (BP) and the cross-record checks (`BP-SEM-001..014`, `BP-AR-001..007`).
4. The SD/Retire PG carries `process_context: dea:pc-sd-retire` (resolves to a known PC); the BP carries `context: [ref: dea:pc-sd-retire]` (resolves to a known PC).
5. ECF conformance: 743 entries conformant.
6. Full conformance suite: 28 gates, 0 blocking, 0 advisory failures.
7. `l1-register.yaml` advances to v17 with SD/Retire flipped ratified-accepted/landed.
8. CR-META gate reports 0 new findings on CR-BP-101.
9. Em-dash / en-dash audit: 0 violations in new prose (the GitHub language rule excludes fenced code blocks and inline code spans).

## 7. Result

CR-BP-101 lands the SD/Retire admission tranche as 3 canonical records (PC + PG + BP) that complete the 7x7 = 49-cell ECF matrix. The CR-BP-80 escape-clause DEFER for SD/Retire is acted on: the "Sunset Regulated Strategic Plan" BP candidate (score 8; FDICIA Section 131, SRB rejection, PRA SS9/17, PUC retraction, NHS England directive) is admitted as `dea:process-sunset-regulated-strategic-plan`. The 28-gate suite remains CONFORMANT (0 blocking, 0 advisory); `open_change_requests` 112 → 113. CR-BP-100a (PR #143) supersedes CR-BP-100 (PR #141) and refreshes the cardinality gate's test assertions to validate the 49-of-49 cell state with every PC paired 1:1 with exactly one PG. The documentation pipeline (EXT-02..06) is now fully unblocked: every L0 has its L1 pair, every L1 has its L0 pair, the matrix is complete.

### Counts (post-merge)

- Process Context records: 48 → **49**
- Process Group records: 48 → **49**
- BP records: 139 → **140**
- Activity records: 553 (unchanged)
- L4 Task records: 0 (unchanged)
- Entities (catalog index): 740 → **742**
- Conformance report total: 789 → **792**
- `open_change_requests`: 112 → **113**