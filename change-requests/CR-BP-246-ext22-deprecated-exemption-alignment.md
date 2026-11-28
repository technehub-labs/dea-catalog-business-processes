# CR-BP-246: EXT-22 R22-04/R22-06 Deprecated-Record Exemption Alignment

**Status**: Proposed
**Layer**: Process Catalog (Cross-Cutting Documentation)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-28
**Parent programme**: CR-BP-94-EXT-22 (Process Decomposition Reconciliation and Structural Integrity)
**Repository**: technehub-labs/dea-catalog-business-processes
**Change type**: Validator alignment + disposition record (no entity data change)
**Priority**: High
**Depends on**: CR-BP-91 (deprecated-BP L3 exclusion), CR-BP-36 (MECE-008), CR-BP-21a (GE/SD split), CR-BP-243 (baseline refresh precedent, PR #261)

---

## 1. Summary

Align `scripts/check_reconciliation_ext22.py` rules R22-04 and R22-06 with the
already-established deprecated-record exemption (CR-BP-91 + MECE-008 in
CR-BP-36), and record the exemption explicitly in the emitted artefacts as
`deprecated_exclusions` instead of emitting errors.

## 2. Evidence (verified against main @ 8547b00c, 2026-11-28)

The only records tripping R22-04 / R22-06 are one and the same record:

- `processes:process-ge-conceive-e6jx6s` ("Develop Governance Strategy"),
  `entities/v1-alpha/ge-conceive/Governance-Conception/Develop-Governance-Strategy/processes-process-ge-conceive-e6jx6s.yaml`
  - `lifecycle_status: deprecated`, `status: deprecated`
  - `metadata.supersedes` on the active sibling
    `processes:process-sd-conceive-ahwvp5` ("Develop Corporate Strategy",
    StrategyAndDirection × Conceive, CR-BP-21a) points back to this record and
    carries 4 L3 activities (`activity_references`)
  - `metadata.change_history` records CR-BP-21a (2026-09-07, "now DEPRECATED")
    and CR-BP-91 (2026-09-18, "L3 decomposition explicitly DELIBERATELY EXCLUDED")
  - migration map: `dea:process-develop-governance-strategy` →
    `processes:process-ge-conceive-e6jx6s` (`reconciliation/migration-id-map.yaml`)

Grounds for exemption (convergent, per CR-BP-91 §2):

1. CR-BP-21a retired this entry in favour of `processes:process-sd-conceive-ahwvp5`
   under the CR-BP-20 Option A split (GE authorises but does not direct).
2. MECE-008 (`scripts/check_mece.py`) already exempts
   `lifecycle_status=deprecated` BPs from the composed-by-PG gate with the same
   deactivation rationale; R22-06 is the same gate under EXT-22.
3. The active sibling already covers L3 decomposition; adding L3/L1 membership
   to the parked duplicate would re-activate it and pollute L2-L3 traceability.

Legacy-ID verification (no name-based inference): the only `dea:` identifiers
remaining in canonical entity files are historical provenance pointers
(`supersedes: dea:group-strategy-and-governance-conception` on the GE-conceive
group; `metadata.scope.id: dea:scope-customer-facing-operations` on
`processes-process-pr-operate-bbe384`), both present in
`reconciliation/migration-id-map.yaml`, plus one preserved research artefact
(`dea:research-l2-admission-...`, classified outside the canonical population
per CR-BP-238). `check_id_system.py` = CONFORMANT (3,723 records, 0 findings);
`check_legacy_migration.py` = PASS.

## 3. Change

- `scripts/check_reconciliation_ext22.py`: R22-04 and R22-06 skip records with
  `lifecycle_status == "deprecated"` when emitting error findings; each skip is
  appended to a new `deprecated_exclusions` list carrying
  `{rule, record_id, basis}` and surfaced in `ext22-manifest.json`,
  `structural-integrity-report.json`, and `l0-l1-reconciliation-report.json`.
  The factual structural lists (`l2_without_l3_decomposition`,
  `l2_without_l1_membership`) are unchanged, so the reports remain truthful.
- `tests/test_reconciliation_ext22.py`: R22-04/R22-06 now assert 0 error
  findings with the exclusion recorded; R22-07 updated to 0 (the six
  L0-context mismatches were remediated on main after 2026-10-19; baseline
  refreshed in PR #261).
- Regenerated EXT-22 artefacts: `total_findings` 2 → 0,
  `deprecated_exclusions` = 2 entries (R22-04, R22-06 on
  `processes:process-ge-conceive-e6jx6s`).

## 4. Disposition

**RETIRE-as-deprecated (no reactivation).** The record stays deprecated with
its successor pointer; no L3 decomposition and no L1 composition are added.
This is a disposition record, not new content: gate [47] (EXT-22) moves from
advisory-failing to passing because the two remaining findings are now
recorded, evidence-backed exclusions.

## 5. Gate posture

- `check_reconciliation_ext22.py` on main: rc=0, 0 findings, 2 exclusions.
- `check_decomposition_reconciliation.py`: 0 advisory findings (3,729 records).
- `check_id_system.py`: CONFORMANT; `check_legacy_migration.py`: PASS.
- CI on main @ 8547b00c: validate / validate-allocation /
  ecf-conformance-consumer all success (baseline for this PR).
