# CR-BP-13a: CustomerAndDemand Admission Tranche

## What this PR is

Promotes 4 of the 5 accepted CustomerAndDemand coordinates from the
ratified research register (CR-BP-13) into canonical Process Group
records with their composing L2 Business Process specialization
entries.

## Coverage

| Coordinate | Process Group | L2 Processes |
|---|---|---|
| Conceive | `dea:group-customer-strategy-conception` | Develop Customer Strategy; Develop Market Intelligence |
| Design | `dea:group-customer-experience-design` | Design Customer Experience; Design Demand Model; Design Customer Journey |
| Build | `dea:group-customer-channel-and-acquisition-build` | Build Customer Acquisition Channels; Build Demand Generation Programs |
| Improve | `dea:group-customer-insight-and-retention` | Operate Customer Retention Programs |
| Operate | (existing `dea:group-customer-lifecycle-management` + `dea:process-manage-customer-relationship`) | (covered by CR-BP-03C + CR-BP-12) |

**Total adds**: 4 Process Context cells + 4 Process Group records + 8 L2 Process specialization entries = **16 new canonical entries**.

## Naming policy (locked)

Two layers of names:

1. **Process Group names** follow the ratified register's first `l1_candidates[]` entry per coordinate (CR-BP-11 §4 verbatim). E.g. the register's Conceive coordinate has `l1_candidates: ['Customer Strategy Conception', 'Market and Demand Conception']`; the catalog's Process Group is `dea:group-customer-strategy-conception` with that as its name.
2. **L2 Process names** follow BP-ARC-ID-001: must start with a verb (e.g. `Develop Customer Strategy` not `Customer Strategy Conception`). The verb + object are real industry vocabulary drawn from APQC PCF 7.0, SCOR, ITIL 4; not made up.

The two layers reference each other: the Process Group's `composes` array points at the L2 entries; the L2 entries carry the inverse in `metadata.change_history` (the `part-of` is generated at query time per CR-BP-12 §8).

## Tool

`tools/build_bp13a_tranche.py` (~580 lines): one-shot generator that produces all 16 entries from a Python declaration. The generator renders canonical YAML directly; hand-edited files are not the source of truth. Re-running the generator is idempotent. The generator is NOT vendored into CI; it is a build-time aid for this tranche only.

## Verification (live)

```
$ pytest tests/
tests/test_build_bp13a_tranche.py ....................... [100%]
tests/test_ratify_research_register.py ........................ [100%]
============================== 24 passed in 0.30s ==============================
```

| Gate | Result |
|---|---|
| `regenerate_catalog.py --check` | OK (CATALOG.yaml current) |
| `check_catalog_index.py --strict` | OK (14 entities validate) |
| `conformance_test_catalog_structure.py --strict` | 16/16 CSTs pass |
| `check_ecf_conformance.py` | PASS (14 entries conform) |
| `check_legacy_migration.py` | PASS (BP-MIG-001..005) |
| `check_process_context.py` | PASS (PC-001..PC-008) |
| `check_process_group.py` | PASS (PG-001..008) |
| `check_process_identity.py` | PASS (with suggestions) |
| `check_process_specialization.py` | PASS (BP-SPEC-01-001..007) |
| Dash sweep on new prose | Clean |
| Secret scan | 0 |
| `git diff --check` | Clean |

## What this unlocks

The CustomerAndDemand value stream is now fully populated across all 5 accepted lifecycle stages. The 6 remaining domains (GovernanceAndExistence, SupplyAndResources, PeopleAndOrganization, ProductAndOffering, OperationsAndDelivery, FinanceAndValue) follow in CR-BP-13b..BP-13g using the same pattern.

## Out of scope (intentional)

This PR does NOT:

- Promote the 11 backlog-deferred Activate/Retire coordinates (deferred by CR-BP-13 §4).
- Add per-Process Group examples (`docs/examples/*.md`); those follow in CR-BP-13a.1.
- Update `dea-catalog-business-capabilities` or other consumer catalogs. The new L2 entries are pure additions; no consumer breaks.

## Sequencing

| CR | Status |
|---|---|
| CR-BP-11 (research register) | Merged |
| CR-BP-12 (L1 Process Group profile) | Merged |
| CR-BP-13 (research ratification) | Merged (PR #22) |
| **CR-BP-13a (this PR)** | **Proposed** |
| CR-BP-13b..BP-13g (other 6 domains) | future |