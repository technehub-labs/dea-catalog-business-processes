# CR-BP-74 - F&A Retire escape-clause discovery (Regulated Run-Off)

**Status**: Proposed
**Layer**: L2 (discovery only; admission deferred to CR-BP-75)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-15

## 1. Change Request

Escape-clause re-evaluation of the F&A x Retire register cell,
re-opening the verbatim escape condition from the register v2
ratification (CR-BP-19, 2026-09-07):

> defer until a regulated unwind (e.g. mutual insurer run-off)
> requires a standalone group

The 2024-2026 regulatory landscape satisfies the escape clause:

- PRA PS20/24 (UK): Solvent Exit Planning for Insurers, in force
  30 June 2026. Imposes a Solvent Exit Analysis (SEA) and Solvent
  Exit Plan (SEP), and a 28-day run-off plan once a firm is
  supervised as a run-off firm.
- FSB Final Guidance on Insurance Resolution Strategies (2025):
  categorises run-off as solvent, insolvent, payout/transfer, and
  liquidation. Sets resolution-tool selection criteria.
- NAIC Model Regulation Service of Legal Process (Model 901):
  record retention during run-off, service-of-process, claims-
  handling during run-off.
- IFRS 17 Insurance Contracts (effective 2023): current fulfillment
  value with contractual service margin; the General Model, the
  Variable Fee Approach, and the Premium Allocation Approach each
  define how policies in run-off are measured.
- IFRS 5 Non-current Assets Held for Sale and Discontinued
  Operations: classification, measurement, presentation, and
  disclosure for assets and groups of assets being wound down.
- ASC 205-30 Liquidation Basis of Accounting (FASB ASU 2013-07):
  when and how an entity prepares its financial statements on a
  liquidation basis. ASC 944 Financial Services - Insurance.
- APQC PCF 8.8 Perform financial wind-down (entity-level solvent
  exit).
- Insurance Run-off Association (IRO) Best Practice Guidance (2024):
  governance, communications, claims handling, asset management
  during run-off, reserving adequacy, capital adequacy during
  wind-down.
- dea-metaframework/framework/domain-grounding.md section 3.7
  (F&A lifecycle transition stages): notes the register v2 escape
  condition verbatim.

## 2. Outcome (4 candidates evaluated)

| # | Candidate | Score | Disposition |
|---|-----------|-------|-------------|
| 1 | Conclude a Regulated Run-Off | 9/10 | ADMIT-CANONICAL |
| 2 | Operate Financial Wind-Down | 5/10 | DEFER |
| 3 | Dispose of Investments | 3/10 | RECLASSIFY |
| 4 | Recognize Impairment and Exit Liabilities | 3/10 | RECLASSIFY |

Candidate 1 is the L1 Process to admit at F&A x Retire via
CR-BP-75. It satisfies BP-LIFE-009 (verb + object), BP-ARC-ID-001
(process_type: management), DISC-002 (post-IFRS-17 evidence
basis), DISC-003 (authority-anchored trigger), and DISC-005
(audit completeness). Score of 9/10; the one-point reduction is
for the F&A-domain scope question (insurance-led vs broader
financial-stewardship wind-down), deferred to a future CR.

Candidate 2 fails the BP-LIFE-009 semantic-identity test
(Operate is a state verb, not a transformation verb). Defer until
a future CR re-evaluates the cell charter to include a non-
insurance regulated wind-down L1 candidate (banks under PRA BRRD
/ FDIC OLA, pension funds under PBGC termination).

Candidates 3 and 4 are Activity-shaped (bounded to a single
disposal or recognition event under the broader run-off Process).
Reclassify as Activity-level decomposition candidates for
CR-BP-7x+ once candidate 1 is admitted.

## 3. Repository changes

New:
- discovery/v1-alpha/finance-and-accounting-retire-escape.yaml
  (escape-clause re-evaluation per CR-BP-62 method)
- change-requests/CR-BP-74-fa-retire-escape-discovery.md (this file)

Modified:
- tests/test_check_lifecycle_discovery.py count assertions 16->17
  (record_count, docstring, len(_stage_pairs))
- change-requests/README.md (index row inserted)

## 4. Verified

- check_lifecycle_discovery.py CONFORMANT, 17 records, 0 findings
- pytest 383/0 (15/15 in test_check_lifecycle_discovery.py)
- 0 schema errors against schemas/discovery/lifecycle-discovery.schema.json
- 0 em-dash on new lines (memory directive 2026-09-11)
- No admission; ADMIT-CANONICAL is recommendation-only per CR-BP-62
  section 20 (admission requires its own CR; CR-BP-75 will land the
  PC + PG + BP stack)

## 5. NOT-list

- No PC, PG, BP, or activity files created
- No register cell flip (carried to CR-BP-75)
- No ADM-001 regex extension
- No disposition register append
- No tranche plan update
- No PG, BP, or activity count-assertion bump
- No CATALOG.yaml regeneration
- No CR-META changes

## 6. Next step (separate slice)

CR-BP-75: F&A x Retire admission tranche (PC + PG + BP stack,
PC id dea:pc-fa-retire, BP id dea:process-conclude-regulated-run-off).
Branch will be cut from origin/main after #115 merges.
