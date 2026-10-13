# CR-BP-21e: FinanceAndAccounting Landing (ECF v2.4.0 — Fifth and Final Unadmitted Domain)

**Status**: Accepted
**Admission authority**: yes
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-08
**Depends on**: CR-BP-19 (register v2); CR-BP-20 (alignment); CR-BP-21a (StrategyAndDirection landing); CR-BP-21b (AgencyAndOrganization landing); CR-BP-21c (ProductAndValue landing); CR-BP-21d (EnablementAndOperations landing)
**Related**: dea-metaframework/framework/domain-grounding.md §3.7

## 1. What this CR is

Fifth and final landing tranche of the CR-BP-21 series. Lands
FinanceAndAccounting against the rediscovered register v2 cells
(Conceive / Design / Build / Operate / Improve). The Activate / Retire
cells remain deferred register-wide per CR-BP-19. With this landing,
every v2.4.0 domain has its Conceive-cell L1 Process Group landed;
remaining landing work is L2 completion (CR-BP-21a.1..e.1) and the
deferred Activate/Retire question.

v2.4.0 (CR-ECF-006) renamed this domain from "Finance & Value" to
"Finance & Accounting" and scoped it to monetary consequence: abstract
"value" was removed (it is a cross-cutting outcome owned by no single
domain), planning (Finance) and recording (Accounting) are treated as
inseparable complements, and financial resources absorbed from the
dissolved Supply & Resources domain are scoped here
(domain-grounding.md §3.7).

## 2. The 5 process contexts

- `dea:pc-fa-conceive` — Financial Model & Funding Conception
- `dea:pc-fa-design` — Financial Planning & Accounting Architecture Design
- `dea:pc-fa-build` — Finance Capability & System Build
- `dea:pc-fa-operate` — Accounting, Reporting & Treasury Operation
- `dea:pc-fa-improve` — Finance & Financial Control Improvement

The Activate / Retire cells (per register v2) remain deferred.

## 3. The 1 Process Group (L1)

- `dea:group-financial-model-conception` — Process Group for
  FinanceAndAccounting x Conceive. Composes the 3 L2s of the
  Conceive cell (Frame finance strategy, Frame monetary model, Frame
  funding and capital approach).

  Naming note: the L1 group covers the full Conceive cell (Financial
  Model Conception + Funding Strategy Conception). The id surfaces
  "financial model" as the principal L1 candidate; the group scope
  covers both L1 candidates as a single bounded Process Group per
  CR-BP-12 §4 (group id is domain-scoped, not cell-component-scoped).

## 4. The 5 L2 Business Processes

One L2 per ratified cell. Per CR-BP-19,
all land as `lifecycle_status: candidate`.

| L2 ID | Cell | process_intent | process_type |
|---|---|---|---|
| dea:process-frame-finance-strategy | FA/Conceive | develop | management |
| dea:process-design-financial-plan-structure | FA/Design | develop | management |
| dea:process-secure-funding-facilities | FA/Build | develop | core |
| dea:process-operate-general-ledger | FA/Operate | operate | core |
| dea:process-conduct-cost-optimization-review | FA/Improve | develop | management |

The 3-L2 Conceive cell (finance strategy, monetary model, funding and
capital approach) lands 1 L2 (finance strategy; remaining 2 in
CR-BP-21e.1). The 4-L2 Design cell (chart of accounts, cost allocation
model, plan structure, financial controls) lands 1 L2 (plan structure;
remaining 3 in CR-BP-21e.1). The 3-L2 Build cell (finance function,
ERP finance module, funding facilities) lands 1 L2 (funding
facilities; remaining 2 in CR-BP-21e.1). The 8-L2 Operate cell
(general ledger, payables, receivables, treasury, tax, close, FP&A,
reporting) lands 1 L2 (general ledger; remaining 7 in CR-BP-21e.1).
The 3-L2 Improve cell (cost optimization, reporting improvement,
control strengthening) lands 1 L2 (cost optimization review;
remaining 2 in CR-BP-21e.1).

## 5. Boundary discipline (v2.4.0 monetary scoping)

- Financial Stewardship is folded into Accounting and Reporting per
  the monetary-measurement scoping (register v2 migration_note).
- Procure-to-pay and order-to-cash operational *execution* live in
  enablement-operations x operate; the monetary *recording* of those
  cycles remains here (domain-grounding.md §3.7 boundary rule).
- Strategic investment choices live in strategy-direction; investment
  strategy governance lives in governance-existence. This domain owns
  the monetary model, not the investment decision.
- "Value Strategy Conception", "Value Architecture Design", and
  "Value Performance" were removed from the register per v2.4.0
  (abstract value is out of scope).

## 6. Provenance + classification (per the landed-population pattern)

- `lifecycle_status: candidate` for all 5 L2s and the 1 L1 group.
- `process_intent` / `process_type` from canonical vocabularies
  (CR-BP-14 §10). `process_type` aligned to outcome keyword density
  (BP-ARC-ID-004): Build/Operate L2s land as `core` (secure/operate
  verbs dominate); Conceive/Design/Improve land as `management`.
- `metadata.change_history` carries the CR-BP-21e entry on every
  entry with phase-7 marker, `cr: CR-BP-21e`, the date, and the
  rationale (grounds the change in domain-grounding.md §3.7).
- `metadata.cross_context_overlap: []` (no cross-cell overlap;
  MECE for the FA cells is verified in the register v2).

## 7. What this CR does NOT do

- The remaining L2s of the FA cells — follow-up CR-BP-21e.1 when
  more L2 material is ready.
- FA/Activate and FA/Retire cells — register v2 keeps these
  deferred.
- L2-completion tranches for the other four landed domains
  (CR-BP-21a.1..d.1) — separate follow-ups.
- Cross-repo BC capability-financial-management re-affiliation —
  out of scope here.

## 8. Verification

- All 15 conformance gates pass (CONFORMANT).
- pytest 148 pass / 1 pre-existing failure.
- check_process_identity 0 blocking findings.
- Admission gate `--strict-provenance`: exit 0; the 6 new entries
  (5 L2s + 1 L1 group) all carry the CR-BP-21e reference.
- Fresh-clone reproduction (with `git remote set-url origin ...git`
  normalization per `.github/workflows/ci.yml`):
  `python scripts/regenerate_catalog.py --check` OK.
