# CR-BP-13b: GovernanceAndExistence Admission Tranche

**Status**: Proposed
**Admission authority**: yes
**Layer**: L1 (Process Catalog)
**Owner**: TechNeHub Labs
**Depends on**: CR-BP-11 (research register; merged), CR-BP-12 (L1
Process Group profile/schema; merged), CR-BP-13 (research ratification;
merged), CR-BP-13a (PartyAndRelationship admission tranche; merged)

## What this CR is

Promotes all 5 accepted GovernanceAndExistence coordinates from the
ratified research register (CR-BP-13) into canonical Process Group
records with their composing L2 Business Process specialization
entries.

**Coverage** (all 5 accepted lifecycle stages):

| Stage | Process Group | L2 Processes |
|---|---|---|
| Conceive | `dea:group-strategy-and-governance-conception` | Develop Governance Strategy; Initiate Policy and Charter |
| Design | `dea:group-governance-system-design` | Design Governance System; Design Policies and Controls |
| Build | `dea:group-governance-body-establishment` | Establish Governance Bodies; Codify Charters and Policies |
| Operate | `dea:group-governance-oversight` | Operate Governance Oversight; Audit Policy Compliance |
| Improve | `dea:group-governance-review-and-learning` | Review Governance Effectiveness |

**Total adds**: 5 Process Context cells + 5 Process Group records + 9 L2 Process specialization entries = **19 new canonical entries**.

## Process Context cells

| ID | Stage |
|---|---|
| `dea:pc-ge-c` | Conceive |
| `dea:pc-ge-d` | Design |
| `dea:pc-ge-b` | Build |
| `dea:pc-ge-op` | Operate |
| `dea:pc-ge-im` | Improve |

Each cell carries the full Cell Charter (CR-BP-02 §7): enterprise
concern, lifecycle concern, combined semantic meaning, inclusions,
exclusions, adjacent boundaries.

## Naming policy (locked)

- **Process Group names** follow the ratified register's first `l1_candidates[]` entry per coordinate (CR-BP-11 §4 verbatim).
- **L2 names** follow BP-ARC-ID-001 (verb-first) using real industry
  vocabulary (ISO 37000:2021, TOGAF, COBIT 2019, COSO Internal
  Control); not made-up.

## Tool

`tools/build_bp13b_tranche.py` (~1100 lines): per-tranche generator
that produces the 19 new entries from a Python declaration. Reuses
the renderer helpers from `tools/build_bp13a_tranche.py` (the
shared renderers are domain-agnostic; the per-tranche script
declares the 5+5+9 entries specific to GovernanceAndExistence).

The generator is NOT vendored into CI; it is a build-time aid for
this tranche only. Re-running is idempotent.

## Verification

- `python tools/build_bp13b_tranche.py` produces 19 new files
  (5 cells + 5 groups + 9 L2 entries) + stub folders + per-entity
  READMEs.
- `python -m pytest tests/`: existing 24 tests pass (CR-BP-13 +
  CR-BP-13a tests are domain-agnostic and continue to apply).
- `python3 scripts/regenerate_catalog.py --check`: CATALOG.yaml
  regenerates cleanly with the new entries.
- `python3 scripts/check_catalog_index.py --strict`: 28 entities
  validate.
- `python3 /home/hermes/dea-work/dea-metaframework/tools/
  conformance_test_catalog_structure.py --strict`: 16/16 CSTs pass.
- All 6 process validators pass:
  - `check_ecf_conformance.py`: PASS (28 entries conform).
  - `check_legacy_migration.py`: PASS.
  - `check_process_context.py`: PASS (PC-001..PC-008).
  - `check_process_group.py`: PASS (PG-001..PG-008; 10 Process Groups).
  - `check_process_identity.py`: PASS (with suggestions).
  - `check_process_specialization.py`: PASS.
- Per-file schema dispatch (CI: validate-process-entries): PASS.
- Dash sweep on new prose: clean.
- Secret scan: 0.
- `git diff --check`: clean.

## Out of scope (intentional)

This CR does NOT:

- Promote the 11 backlog-deferred Activate/Retire coordinates (deferred
  by CR-BP-13 §4).
- Add per-Process Group examples (`docs/examples/*.md`); those follow
  in CR-BP-13b.1.
- Update `dea-catalog-business-capabilities` or other consumer
  catalogs. The new L2 entries are pure additions; no consumer breaks.

## Sequencing

| CR | Status |
|---|---|
| CR-BP-11 | Merged (research register) |
| CR-BP-12 | Merged (L1 Process Group profile) |
| CR-BP-13 | Merged (research ratification; PR #22) |
| CR-BP-13a | Merged (PartyAndRelationship admission; PR #23) |
| **CR-BP-13b (this PR)** | **Proposed** |
| CR-BP-13c..BP-13g (other 5 domains) | future |

After this CR lands, **2 of the 7 ECF domains are fully populated**
(PartyAndRelationship + GovernanceAndExistence). The 5 remaining
domains (StrategyAndDirection, AgencyAndOrganization,
ProductAndValue, EnablementAndOperations, FinanceAndAccounting) follow
in CR-BP-13c..BP-13g.
