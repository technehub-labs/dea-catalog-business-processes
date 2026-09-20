# CR-BP-17: ECF Domain Enum v2.3.0 Migration (CR-BP-17 (a.k.a. CR-BP-ECF-01))

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Accepted
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Depends on**: CR-BP-16; CR-ECF-006; CR-MM-ECF-01
**Companion to**: CR-BP-13a (the PartyAndRelationship admission tranche; same v2.3.0 scope)
**Related**: CR-DEA-BC-04 (Business Capability Catalog ECF Overlay v0.2 - will need re-derivation); CR-ECF-001..006 (the ECF core wave, all merged); CR-MM-ECF-01 (metamodel v2.3.0 migration, merged); CR-BC-17 (the BC repo's parallel v2.3.0 carrier; will be filed alongside this one)
**Decision Type**: Architectural (domain enum migration)
**Implementation**: Pure rename; no new canonical entities; no new Process Contexts admitted.

> Note: this CR is filed under the `CR-BP-17` number to satisfy
> `scripts/check_cr_metadata.py` CR-META-006 (filename pattern
> `CR-BP-\d+...`). The conventional ECF-migration carrier name is
> `CR-BP-17 (a.k.a. CR-BP-ECF-01)`; both names refer to the same artefact.

---

## 1. Change Request

This CR is the **carrier** for the v2.3.0 Domain enum migration
in `technehub-labs/dea-catalog-processes`. Five of the seven canonical
ECF Domains were renamed in the metaframework (CR-ECF-006 + ADR-ECF-001);
this repo is the first of the **catalog** tier that holds those
identifiers in canonical form (alongside the metamodel profile).

### 1.1 Scope

This CR migrates **every** reference to the v2.2.0 Domain identifiers in
this repo to the v2.3.0 set:

| Before (v2.2.0) | After (v2.3.0) |
|------------------|------------------|
| `CustomerAndDemand` | `PartyAndRelationship` |
| `SupplyAndResources` | `StrategyAndDirection` |
| `ProductAndOffering` | `ProductAndValue` |
| `OperationsAndDelivery` | `EnablementAndOperations` |
| `FinanceAndValue` | `FinanceAndAccounting` |
| `GovernanceAndExistence` | `GovernanceAndExistence` (unchanged) |
| `AgencyAndOrganization` | `AgencyAndOrganization` (unchanged) |

Plus the kebab-case restatement used in `process_audience` and
`domain` values:

| Before (v2.2.0) | After (v2.3.0) |
|------------------|------------------|
| `customer-demand` | `party-relationship` |
| `supply-resources` | `strategy-direction` |
| `product-offering` | `product-value` |
| `operations-delivery` | `enablement-operations` |
| `finance-value` | `finance-accounting` |

Plus the **Process Context ID abbreviations** (the `dea:pc-<domain>-<stage>`
middle segment):

| Before (v2.2.0) | After (v2.3.0) |
|------------------|------------------|
| `cd` (CustomerAndDemand) | `pr` (PartyAndRelationship) |
| `sr` (SupplyAndResources) | `sd` (StrategyAndDirection) |
| `po` (ProductAndOffering) | `pv` (ProductAndValue) |
| `od` (OperationsAndDelivery) | `oe` (EnablementAndOperations) |
| `fv` (FinanceAndValue) | `fa` (FinanceAndAccounting) |

The Process Context ID rename affects **5 context YAMLs** (the admitted
CustomerAndDemand cells: Conceive, Design, Build, Operate, Improve) and
**every reference to those IDs** (CR-BP-13a tranche content, scripts,
tests, dispositions).

### 1.2 What this CR does NOT do

- It does NOT admit new Process Contexts. The v2.3.0 wave is a pure
  rename; no new coordinates are admitted in this PR.
- It does NOT regenerate the L1 candidate universe. The L1 process
  discovery work for the renamed Domains (Strategy&Direction,
  Product&Value, Operations&Enablement, Finance&Accounting,
  Party&Relationship) is a separate task that follows this PR — parked
  per eaojnr's direction but ready to dispatch.
- It does NOT retire CR-BP-13a or CR-BP-13b. The Domain-renamed versions
  of those CRs are still valid (the underlying work is unchanged; only
  the names shifted).

## 2. Files changed

109 files modified + 5 context YAML filenames renamed + 1 CR file renamed
+ 2 reconciliation files regenerated. Highlights:

- **3 JSON schemas**:
  - `schemas/entities/process-context.schema.json` (`domain` PascalCase enum)
  - `schemas/entity.schema.json` (`process_audience` kebab-case enum)
  - `schemas/contribution.schema.json` (process_audience kebab-case enum)
- **10 Process Context YAMLs** in `contexts/v1-alpha/`:
  - 5 CustomerAndDemand cells renamed to PartyAndRelationship (id, filename)
  - 5 GovernanceAndExistence cells (id, content already using GovernanceAndExistence)
- **4 L1 Process Group directories** + their L2 process records (the
  CustomerAndDemand cohorts from CR-BP-13a) — entity directory names
  unchanged because they carry the L1 process name (`dea:group-customer-channel-and-acquisition-build`)
  which is descriptive of the L1 work, not the Domain; only the `domain`
  field inside the YAML and any domain references in the research/README
  files were updated.
- **8 conformance scripts** in `scripts/` + **1 build script** in `tools/`:
  - `scripts/check_ecf_conformance.py` (CANON_DOMAINS + lowercase mapping)
  - `scripts/check_process_context.py` (PC-001..PC-008 fixtures + CANON enum)
  - `scripts/check_process_semantics.py` (BP-SEM fixtures)
  - `scripts/check_architectural_regression.py` (BP-AR-005 fixture)
  - `scripts/check_dispositions.py` (`from: party-relationship, to: REMOVE`)
  - `scripts/check_process_identity.py` (test fixtures)
  - `scripts/check_process_group.py` (test fixtures)
  - `scripts/check_legacy_migration.py` (legacy test fixtures — domain
    value is incidental; updated for consistency)
  - `scripts/apply_phase_5_tranche.py` (the migration tool itself)
  - `tools/build_bp13a_tranche.py` (DOMAIN_NAMES key flipped from `cd` to `pr`,
    and the other 4 abbreviations to their new v2.3.0 keys: `sd`, `pv`,
    `oe`, `fa`; `po` for AgencyAndOrganization is unchanged)
- **4 test files** in `tests/` (test fixtures updated)
- **2 reconciliation artifacts** regenerated:
  - `reconciliation/inventory.yaml`
  - `reconciliation/baseline/v1.yaml`
- **11 CR files** in `change-requests/` (all references migrated to the
  v2.3.0 names) + **1 CR file renamed**:
  - `CR-BP-13a-customer-and-demand-admission.md` →
    `CR-BP-13a-party-and-relationship-admission.md`
- **6 docs files** in `docs/` (narrative updates)
- **CHANGELOG.md** + **README.md** + **change-requests/README.md** updated

## 3. Verification

- `tests/conformance/`: all 8 tests pass (PC-001..PC-008, BP-SEM-001..BP-SEM-012,
  BP-AR-001..BP-AR-006, ECF-CG-001..ECF-CG-007, BP-MIG-001..BP-MIG-005).
- `tests/runtime/`: all runtime ontology tests pass.
- `tests/test_build_bp13a_tranche.py`: **15/15 pass** (the regenerator
  produces content with the new domain identifiers).
- `tests/test_apply_phase_5_tranche.py`: **all pass** (idempotency holds
  under the renamed IDs).
- `tests/test_reconciliation_baseline.py`: **11/12 pass** (1 pre-existing
  unrelated failure in `test_check_struct_clean_repo_passes` — the script
  writes `STRUCT-OK` to stdout but the test asserts it in stderr;
  predates this PR; not in scope).
- `scripts/check_ecf_conformance.py`: **PASS** (28 entries conform).
- `scripts/check_process_context.py`: **PASS** (PC-001..PC-008).
- `scripts/check_process_semantics.py`: **CONFORMANT** (BP-SEM S21).
- `scripts/build_inventory.py --self-test --strict`: **PASS** (inventory
  + baseline round-trip byte-identically under the new identifiers).

## 4. Pause-for-merge

This PR is opened and **paused for explicit user Merge** per the
CR-programme convention. After merge, the next downstream migration
is `dea-catalog-business-capabilities` (CR-BC-ECF-01; the ECF overlay
re-derivation is the heavier of the two).

The L1 process discovery task for the v2.3.0 Domains is also parked and
ready to dispatch once this PR lands.
