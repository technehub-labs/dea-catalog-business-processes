# CR-BP-63: Activate/Retire Lifecycle Discovery Exercise

**Status**: Proposed
**Layer**: Process Catalog (lifecycle discovery)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-14
**Carrier**: First application of the CR-BP-62 discovery method: the 14 backlog-deferred Activate/Retire ECF contexts are evaluated cell-by-cell with evidence-backed dispositions, replacing the register's uniform deferral rationale with documented per-cell outcomes (CR-BP-62 section 15).
**Depends on**: CR-BP-62 (discovery method, record schema, DISC-001..008 gate); CR-BP-19 (register v2 deferral normalization); CR-BP-28 (register v4 ratification)
**Lands against**: 126 canonical BP records (125 active + 1 deprecated), 35 canonical PG records, 35 canonical PC records, 501 canonical Activity records; 24 conformance gates CONFORMANT; CR-BP-62 merged (PR #103)

---

## 1. Change Request

Execute the CR-BP-62 lifecycle process-discovery method mechanically across the 14 backlog-deferred Activate/Retire contexts (7 domains x 2 stages). Each context receives one machine-readable discovery record at `discovery/v1-alpha/<domain>-<stage>.yaml` carrying the full candidate evaluation: identity, trigger, transformation, outcome, boundary, actors, controls, evidence, the BP-LIFE-001..015 evaluation dimensions, canonicality scoring, and a section-16 disposition.

The exercise answers the question the register's deferral left open: do Activate and Retire contain canonical Business Processes? The method's answer is **yes, in five cells, with named candidates and authoritative evidence** -- and **no, in nine cells, with the absence now documented as an evaluation outcome rather than presumed from stage semantics**.

## 2. Exercise Outcomes

87 candidates evaluated across 14 contexts. Dispositions:

| Disposition | Count | Notes |
|---|---|---|
| ADMIT-CANONICAL (recommended) | 5 | Governed admission pending (CR-BP-62 section 20); no BP records land in this slice |
| RECORD-PATTERN | 38 | Stable cross-domain transformations; canonical home referenced where one is proposed |
| MERGE | 21 | Duplicate or terminal-phase semantics of a stronger candidate |
| RECLASSIFY | 14 | Composition or capability-distinction failures (wrong level or not a process) |
| DEFER | 9 | Boundary or duplication questions unresolved |

The five canonical-admission recommendations:

| Candidate | Primary cell | Score | Evidence base |
|---|---|---|---|
| Transition to Service | ProductAndValue/Activate | 10 | ITIL 4 transition practices; COBIT 2019 BAI07; IT4IT Requirement to Deploy |
| Transition Out of Service | ProductAndValue/Retire | 10 | ITIL service retirement; eTOM lifecycle management; industry EOL policy practice |
| Bring into Force | GovernanceAndExistence/Activate | 9 | Universal entry-into-force / commencement semantics in legal-regulatory systems; board-resolution effectiveness practice |
| Decommission | EnablementAndOperations/Retire | 9 | ISO 55000 asset decommissioning/disposal; APQC PCF asset end-of-life; eTOM resource lifecycle |
| Close Enterprise Relationship | PartyAndRelationship/Retire | 9 | Contract close-out and termination practice; outsourcing exit management |

Nine cells conclude `process_empty: true` with the section-15 checklist fully recorded: all Activate cells except ProductAndValue and GovernanceAndExistence; all Retire cells except ProductAndValue, EnablementAndOperations and PartyAndRelationship.

## 3. Grounding Improvements Over the Register Deferral

The register's uniform rationale ("lifecycle transition stages, not stable Process Group operating scopes") is tested, not presumed:

1. **G&E/Activate overturns the deferral with evidence.** Entry-into-force semantics (adoption vs commencement) are universal across legal-regulatory systems and corporate governance. "Bring into Force" passes the ECF-independence test more strongly than any other candidate in the exercise: the concept predates and is independent of any framework. The register's note ("governance activation is an attribute of governance operate") does not survive contact with commencement-provision evidence.
2. **G&E/Retire confirms the deferral with evidence.** Sunset/rescission mechanisms are real but arrive as outcomes of policy review (Improve); the standalone boundary fails. The cell is now process-empty by documented evaluation, matching the register's sector-example condition.
3. **Duplication discipline.** Accept into Operation, Commence Service and Recover / Reclaim fail BP-LIFE-010 as standalone candidates and merge into the canonical parents. Specialization dispositions were available but deliberately unused: specialization work is unauthorized per program governance (CR-BP-62 section 30); variants were merged instead.
4. **Composition discipline.** Deploy / Cut Over and Mobilize Capability are reclassified out of L2 process space (Activity-level execution; capability restatement respectively).

## 4. Repository Changes

| Path | Status | Notes |
|---|---|---|
| `discovery/v1-alpha/*.yaml` | NEW | 14 discovery records (87 evaluated candidates) |
| `discovery/README.md` | NEW | Directory purpose, record semantics, exercise index |
| `scripts/check_struct.py` | MOD | `discovery` added to KNOWN_TOP_LEVEL (deliberate structural addition; CR-BP-15-IMP D6) |
| `change-requests/CR-BP-63-activate-retire-discovery.md` | NEW | This document |
| `change-requests/README.md` | MOD | CR-BP-63 row; CR-BP-62 status corrected to Merged (PR #103) |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 75 -> 76 |

## 5. What This CR Is NOT

- **NOT a canonical admission.** The five ADMIT-CANONICAL dispositions are discovery recommendations; admission lands through the governed contribution flow as separate CRs.
- **NOT a register mutation.** The L1 register's disposition axis is unchanged; this exercise produces the evidence base a future register revision would cite.
- **NOT a specialization authorization.** No ADMIT-SPECIALIZATION disposition is used; specialization remains unauthorized per program governance.
- **NOT a catalog record change.** Zero entity records touched; counts unchanged (ACT 501 / EXE 662 / report 697).
- **NOT a Process Group population.** No PG records are proposed for Activate/Retire coordinates; the discovery layer evaluates process identity below the group construct, and any future L2 admission would still require an L1 home via the contribution flow.

## 6. Acceptance Criteria

1. 14 discovery records exist, one per Activate/Retire context, all schema-valid (DISC-001).
2. `python3 scripts/check_lifecycle_discovery.py` reports 14 records checked, 0 findings; `--strict` exits 0.
3. The vacuous-to-exercised transition is demonstrated: gate [19] evaluated 0 records before this slice, 14 after.
4. Every ADMIT-CANONICAL disposition carries non-empty evidence.sources (DISC-006) and a proposed canonical ref (DISC-005).
5. Full pytest suite passes; `scripts/conformance_result.py` remains CONFORMANT (24 gates).
6. `python3 scripts/check_cr_metadata.py` reports 0 new findings.
7. No entity record modified.

## 7. Result

CR-BP-63 converts the Activate/Retire question from doctrine into evidence. Five cells carry canonical-admission recommendations with authoritative grounding; nine cells carry documented, checklist-complete absence findings. The discovery gate transitions from regression guard to exercised: 14 records, 0 findings, all eight DISC rules evaluated.
