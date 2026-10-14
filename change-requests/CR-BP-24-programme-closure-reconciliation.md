# CR-BP-24: Programme Closure Reconciliation (tracking artifacts vs catalog reality)

**Status**: Accepted
**Layer**: Process Catalog (governance / tracking)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-09-08
**Depends on**: CR-BP-15 (catalog reconciliation); CR-BP-16 (conformance gate, carrying CR-BP-15-IMP); CR-BP-21e.1 (FinanceAndAccounting completion, PR #59); CR-BP-21f.1 (GovernanceAndExistence completion, PR #60); CR-BP-23 (ECF v2.5.0 migration, PR #61)
**Related**: CR-BP-22 (register audit-status reconciliation; same reconciliation pattern applied to the register axis)

## 1. What this CR is

The CR-BP-21 landing series (13a/13b, 21a..21e, 21a.1..21f.1) is complete: the register audit reads **35 landed / 0 ratified-pending-landing / 14 backlog-deferred** across the 49 ECF coordinates, and the CR-BP-16 conformance report scores all **196 catalog records at level L4**. The CR-BP-15-IMP programme machinery (inventory, baseline, dispositions, tranche execution, conformance pipeline) is landed and enforced in CI (PRs #31..#42).

The **tracking artifacts**, however, still describe the programme as in flight. This CR reconciles the four drifted surfaces with catalog reality, in the same pattern as CR-BP-22 (which reconciled the register axis). No entity, schema, or validator behaviour changes; this CR touches documentation and reconciliation metadata only.

## 2. The four drifts (as of 2026-09-08)

### 2.1 Tranche plan statuses

`reconciliation/tranches/plan.yaml` (`plan_status: PRELIMINARY`, dated 2026-09-06) still marks 10 tranches as `status: proposed` even though every one of them has landed:

| Tranche | Cell | Landed by | PR |
|---|---|---|---|
| fa-c.1 | FinanceAndAccounting.Conceive | CR-BP-21e.1 (no-op; covered by 21e) | #59 |
| fa-d.1 | FinanceAndAccounting.Design | CR-BP-21e.1 | #59 |
| fa-b.1 | FinanceAndAccounting.Build | CR-BP-21e.1 | #59 |
| fa-op.1 | FinanceAndAccounting.Operate | CR-BP-21e.1 | #59 |
| fa-im.1 | FinanceAndAccounting.Improve | CR-BP-21e.1 | #59 |
| ge-c.1 | GovernanceAndExistence.Conceive | CR-BP-21f.1 | #60 |
| ge-d.1 | GovernanceAndExistence.Design | CR-BP-21f.1 | #60 |
| ge-b.1 | GovernanceAndExistence.Build | CR-BP-21f.1 | #60 |
| ge-op.1 | GovernanceAndExistence.Operate | CR-BP-21f.1 | #60 |
| ge-im.1 | GovernanceAndExistence.Improve | CR-BP-21f.1 | #60 |

The remaining 55 tranches carry no `status` key; their landed state is proven by entity existence and the register audit, but the plan as a whole never records that execution finished.

### 2.2 CR index statuses

`change-requests/README.md` and the root `README.md` "Current Change Programme" table still show:

- **CR-BP-15: Proposed** — in reality the 20-phase programme (CR-BP-15-IMP) is implemented across PRs #31..#38 plus the Phase 5/6/7 tranche PRs; what remains open is only Phase 20 (Governance Approval), which is a human decision gate per CR-BP-16 §22.
- **CR-BP-16: Proposed** — in reality the conformance gate is live in CI (PRs #38..#42: S10/S15/S16/S22, S17/S18/S19/S25 unified Conformance Result, §17 Step 8 provenance blocking).
- **CR-BP-21f.1: Proposed (this PR)** — merged as PR #60.
- **CR-BP-23: Proposed (this PR)** — merged as PR #61.

### 2.3 Root README index coverage

The root `README.md` table stops at CR-BP-16. CR-BP-17 through CR-BP-23 (all merged, PRs #44..#61) have no rows there; only `change-requests/README.md` indexes them. The front-door document is one enum wave and one migration behind.

### 2.4 Broken versioning reference

`CHANGELOG.md` line 5 states versioning follows `docs/versioning.md`. That file does not exist. The repository carries no tags and no documented version policy.

## 3. What this CR changes

| # | Surface | Change |
|---|---|---|
| 1 | `reconciliation/tranches/plan.yaml` | The 10 stale tranches get `status: applied` with `applied_by` / `applied_pr` evidence; `plan_status: PRELIMINARY` becomes `EXECUTED` with a closure note naming the closing PRs (#59, #60). The 55 unmarked tranches are left as-is (their landed state is attested by the register audit; this CR does not rewrite history). |
| 2 | `change-requests/README.md` | CR-BP-15 and CR-BP-16 rows become **Implemented** with their PR chains and an explicit "Phase 20 governance approval pending" note on CR-BP-15. CR-BP-21f.1 becomes **Merged** (PR #60). CR-BP-23 becomes **Merged** (PR #61). New row for CR-BP-24. |
| 3 | `README.md` | Current Change Programme table gains rows for CR-BP-17 through CR-BP-24, consistent with `change-requests/README.md`; CR-BP-15/16 statuses corrected as above. |
| 4 | `docs/versioning.md` | New minimal versioning policy so the CHANGELOG reference resolves: Keep a Changelog 1.1.0 format; SemVer once the first tag is cut; the catalog is pre-1.0 and untagged by deliberate decision until Phase 20 governance approval closes CR-BP-15; version bumps are release-cut events, not per-CR events. |
| 5 | `CHANGELOG.md` | `[Unreleased]` entry for CR-BP-24. The `docs/versioning.md` reference becomes true by deliverable 4. |

Non-goals (explicit):

- No Phase 20 governance approval is claimed by this CR. CR-BP-15 remains open on exactly that gate; the index rows say so.
- No entity, schema, validator-rule, or CI-pipeline change.
- No release tag is cut. Tagging is a release-cut decision after Phase 20, not a bookkeeping action.
- The 14 backlog-deferred Activate/Retire cells remain deferred (CR-BP-11 §316; unchanged).

## 4. Conformance with existing gates

- `check_dispositions.py` validates tranche-record cross-consistency only; it constrains no `status` vocabulary. The new `applied` status and `plan_status: EXECUTED` pass unmodified gates.
- `check_cr_metadata.py` (CR-META-001..006, strict mode): this CR carries Status / Layer / Owner / Depends on; CR number CR-BP-24 is unique and matches the filename.
- `check_register_audit.py`: unaffected; still 35 / 0 / 14.
- CATALOG.yaml is regenerated (open_change_requests increments by 1 for this CR).

## 5. Acceptance criteria

1. `plan.yaml` shows zero `proposed` tranches; the 10 listed tranches carry `status: applied` with `applied_by` and `applied_pr`.
2. `plan_status` is `EXECUTED` with a closure note.
3. Both CR indexes agree with `gh pr list --state merged`: CR-BP-15/16 Implemented (Phase 20 pending on 15), CR-BP-21f.1 Merged (PR #60), CR-BP-23 Merged (PR #61), CR-BP-24 present.
4. Root README table covers CR-BP-01 through CR-BP-24 with no gaps.
5. `docs/versioning.md` exists and the CHANGELOG reference resolves.
6. Full local validator suite passes; CI on the PR is green.
