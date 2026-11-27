# CR-BP-242 — CATALOG Open Change Request Count Reconciliation

**Status**: Proposed  
**Layer**: Cross-cutting  
**Owner**: Emmanuel A. Otchere  
**Type**: Generated catalog-index reconciliation  
**Depends on**: CR-BP-241; CR-CATALOG-STRUCT-06a  
**Baseline**: `d3be5782700d81af0f0fec96cb399b435b9131f7`

## 1. Purpose

Reconcile the committed `CATALOG.yaml` generated index with the canonical output of `scripts/regenerate_catalog.py` after CR-BP-241 introduced an additional open change request.

## 2. Investigation Evidence

The post-merge validation run for CR-BP-241 (run #45938343121) failed at the first catalog-index regeneration check. The exact regenerator diff was limited to:

- committed `catalog.counts.open_change_requests: 7`
- generated `catalog.counts.open_change_requests: 8`

The regenerator's `count_open_change_requests()` scans `change-requests/CR-*.md`, reads the **Status** metadata in the first 30 lines, and counts `Proposed` and `Draft` records as open. CR-BP-241 is Proposed and therefore correctly increases the generated count by one.

No entity inventory, lifecycle state, repository metadata, or other CATALOG field was implicated by the reported diff.

## 3. Scope

1. Update only the generated `CATALOG.yaml` open change request count to the exact regenerator result, including this CR's own Proposed status.
2. Add this CR to the change request register.
3. Retain the existing regeneration check as the enforcement mechanism.

## 4. Explicit Non-Goals

- No changes to canonical entity records, entity counts, identities, lifecycle, or semantics.
- No changes to the catalog regenerator, schema, or CI gate.
- No change to the status or disposition of any existing change request.
- No publication readiness or CR-BP-239 Slice B closure claim.

## 5. Acceptance Criteria

- [ ] The generated `CATALOG.yaml` reports the exact open CR count.
- [ ] `python scripts/regenerate_catalog.py --check --schema catalog-index-schema/catalog-index-schema.json` passes.
- [ ] The full validation workflow proceeds beyond the CATALOG regeneration gate.
- [ ] The change request register includes CR-BP-242.

## 6. Validation Boundary

This CR repairs a generated index discrepancy. It does not establish overall catalog conformance or publication readiness; those remain subject to the downstream gates and strict CR-BP-239 Slice B validation.
