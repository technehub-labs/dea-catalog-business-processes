# CR-BP-28: Register v4 — Re-derivation against ECF v2.5.0

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Accepted
**Layer**: Process Catalog (research register)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-09
**Depends on**: CR-BP-22 (register v3, audit_status axis); CR-BP-23 (ECF v2.5.0 migration, PR #61); CR-BP-25 (Phase 20 governance closure, 2026-09-09); CR-BP-26 (first release cut v0.1.0)
**Related**: `dea-metaframework` v2.5.0 (CR-ECF-008 + ADR-ECF-003); `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml` (the register)

## 1. What this CR is

A v0.x evolution admission wave. The register v3 (CR-BP-22, 2026-09-08)
was re-derived against ECF v2.4.0. ECF v2.5.0 renamed Domain 6
`OperationsAndEnablement` -> `EnablementAndOperations` (carried by
CR-BP-23 in PR #61). This CR re-derives the register against the
v2.5.0 source-of-truth and stamps register `version: 4`.

The re-derivation is a **no-op for the disposition axis**: every
coordinate that was `ratified-accepted` against v2.4.0 is still
`ratified-accepted` against v2.5.0, and every `backlog-deferred`
cell is still `backlog-deferred`. The Domain rename is a label swap
on the same row; no Domain was added, removed, or re-scoped. The
audit axis (CR-BP-22) remains 35 / 0 / 14.

This is the first 0.x evolution admission on the catalogue. It is
intentionally a bookkeeping-grade slice: durable, minimal, no new
entity, no schema, no validator change. It produces register `v4`
and a `v0.2.0` candidate (the next release cut after v0.1.0).

## 2. Why this is the right next slice

The user asked for an "evolution admission" on `dea-catalog-processes`.
The honest read of the catalogue state:

- Register audit: 35 / 0 / 14. No coordinate is unlanded.
- Tranche plan: EXECUTED (65 / 65).
- Conformance: 196/196 at L4, 0 findings.
- Phase 20 governance: CLOSED (CR-BP-25).

There is no L1 gap to fill, no L2 backlog to drain, no new ECF
coordinate to admit. The 0.x evolution space is constrained to:
(a) re-deriving the register against a new ECF source version
[this CR]; (b) admitting a sector specialization tranche; (c)
introducing the L3 Activity Model; (d) re-litigating the Activate
deferral. Of these, (a) is the lowest-risk, smallest, and most
reversible, and it produces durable structure (a new register
version + a v0.2.0 release candidate).

## 3. The re-derivation (no-op evidence)

| Domain (v2.5.0) | Stage | Disposition v3 | Disposition v4 | audit v3 | audit v4 |
|---|---|---|---|---|---|
| GovernanceAndExistence | Conceive / Design / Build / Operate / Improve | ratified-accepted | ratified-accepted | landed (5/5) | landed (5/5) |
| GovernanceAndExistence | Activate / Retire | backlog-deferred | backlog-deferred | backlog-deferred (2/2) | backlog-deferred (2/2) |
| StrategyAndDirection | Conceive / Design / Build / Operate / Improve | ratified-accepted | ratified-accepted | landed (5/5) | landed (5/5) |
| StrategyAndDirection | Activate / Retire | backlog-deferred | backlog-deferred | backlog-deferred (2/2) | backlog-deferred (2/2) |
| AgencyAndOrganization | Conceive / Design / Build / Operate / Improve | ratified-accepted | ratified-accepted | landed (5/5) | landed (5/5) |
| AgencyAndOrganization | Activate / Retire | backlog-deferred | backlog-deferred | backlog-deferred (2/2) | backlog-deferred (2/2) |
| PartyAndRelationship | Conceive / Design / Build / Operate / Improve | ratified-accepted | ratified-accepted | landed (5/5) | landed (5/5) |
| PartyAndRelationship | Activate / Retire | backlog-deferred | backlog-deferred | backlog-deferred (2/2) | backlog-deferred (2/2) |
| ProductAndValue | Conceive / Design / Build / Operate / Improve | ratified-accepted | ratified-accepted | landed (5/5) | landed (5/5) |
| ProductAndValue | Activate / Retire | backlog-deferred | backlog-deferred | backlog-deferred (2/2) | backlog-deferred (2/2) |
| **EnablementAndOperations** | Conceive / Design / Build / Operate / Improve | ratified-accepted | ratified-accepted | landed (5/5) | landed (5/5) |
| **EnablementAndOperations** | Activate / Retire | backlog-deferred | backlog-deferred | backlog-deferred (2/2) | backlog-deferred (2/2) |
| FinanceAndAccounting | Conceive / Design / Build / Operate / Improve | ratified-accepted | ratified-accepted | landed (5/5) | landed (5/5) |
| FinanceAndAccounting | Activate / Retire | backlog-deferred | backlog-deferred | backlog-deferred (2/2) | backlog-deferred (2/2) |

**Totals.** 35 ratified-accepted (unchanged), 14 backlog-deferred
(unchanged), 49 total (unchanged). Register audit remains
35 / 0 / 14.

The Domain 6 rename touched the **label** of one Domain row
(`OperationsAndEnablement` -> `EnablementAndOperations`); the
5x5 active coordinate set, the 2 backlog-deferred cells, the
candidate-universe shape, and the disposition register are all
unchanged. This is the expected outcome of a re-derivation
against a label-only change.

## 4. The candidate universe — also re-checked

For thoroughness, this CR also re-reads the candidate universe
(102 L1 candidates, 196 L2 candidates) and confirms:

- every L1 candidate's `domain` field is one of the seven
  v2.5.0 Domain enum values (no stragglers using the v2.4.0
  `operationsAndEnablement` form)
- every L2 candidate's `ecfConformance.canonicalReferences[0].domain`
  is the v2.5.0 PascalCase enum value
- the OE L2 candidates (23, landed by CR-BP-21d.1) were
  re-keyed in-place by CR-BP-23 (PR #61) to the v2.5.0
  Domain identifier

Verification: `scripts/check_ecf_conformance.py` is green
on the current `main` (161/161 entries pass), which is the
machine-readable form of this re-derivation. CR-BP-23 §"Verified"
attests to that explicitly.

## 5. What this CR does (and does not)

**Does:**

- Bump `l1-register.yaml` `ratification.version` 3 -> 4;
  `ratification.cr` CR-BP-22 -> CR-BP-28; `ratification.supersedes`
  -> "version 3 (CR-BP-22, ratified 2026-09-08)".
- Bump `l1-candidate-universe.yaml` `ratification.version` 3 -> 4
  to match.
- Update `L1-REGISTER-v0.1.md` §1 with the v4 ratification
  reference and the v2.5.0 source-of-truth citation.
- Update `CHANGELOG.md` `[Unreleased]` with a CR-BP-28 entry.
- Add a CR-BP-28 row to both CR indexes.

**Does not:**

- Add, remove, or re-classify any coordinate.
- Touch any entity, schema, validator-rule, or CI-pipeline.
- Cut a release tag. The next release cut is a separate slice
  on this repo (analogous to CR-BP-26).

## 6. Acceptance criteria

1. `l1-register.yaml` and `l1-candidate-universe.yaml` both
   show `ratification.version: 4`, `ratification.cr: CR-BP-28`.
2. `scripts/check_register_audit.py` PASSES with 35 / 0 / 14
   (unchanged).
3. `L1-REGISTER-v0.1.md` §1 references the v4 ratification and
   the v2.5.0 source.
4. `CHANGELOG.md` and both CR indexes have CR-BP-28 entries.
5. CI on the PR is green.
