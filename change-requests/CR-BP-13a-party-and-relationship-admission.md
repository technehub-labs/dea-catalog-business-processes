# CR-BP-13a: PartyAndRelationship Admission Tranche (Conceive / Design / Build / Improve)

**Status**: Proposed
**Admission authority**: yes
**Layer**: L1 (Process Catalog)
**Owner**: TechNeHub Labs
**Depends on**: CR-BP-11 (49-coordinate research register; merged),
CR-BP-12 (L1 Process Group profile/schema; merged), CR-BP-13 (research
ratification; merged)
**Companion to**: CR-BP-13a.1..a.4 (the per-coordinate admission follow-ups;
separate scope)

## What this CR is

Promotes 4 of the 5 accepted PartyAndRelationship coordinates from the
ratified research register (CR-BP-13) into canonical Process Group
records with their composing L2 Business Process specialization entries.

**Coverage**:
- Conceive: 1 Process Group + 2 L2 processes (`Customer Strategy
  Conception`, `Market and Demand Conception`)
- Design: 1 Process Group + 3 L2 processes (`Customer Experience Design`,
  `Demand Design`, `Customer Journey Design`)
- Build: 1 Process Group + 2 L2 processes (`Customer Channel and
  Acquisition Build`, `Demand Generation Build`)
- Improve: 1 Process Group + 1 L2 process (`Customer Insight and
  Retention`)

The 5th coordinate (Operate) was admitted in CR-BP-03C (Process) +
CR-BP-12 (Process Group); the existing `dea:process-manage-customer-
relationship` + `dea:group-customer-lifecycle-management` covers it.

**Total adds**: 4 Process Context cells + 4 Process Group records +
8 L2 Process specialization entries = **16 new canonical entries**.

## Process Context cells

| ID | Stage | L2 count |
|---|---|---|
| `dea:pc-pr-c` | Conceive | 2 |
| `dea:pc-pr-d` | Design | 3 |
| `dea:pc-pr-b` | Build | 2 |
| `dea:pc-pr-im` | Improve | 1 |

Each cell carries the full Cell Charter (CR-BP-02 §7): enterprise
concern, lifecycle concern, combined semantic meaning, inclusions,
exclusions, adjacent boundaries.

## Process Group records (register names verbatim)

The names follow the ratified register's first `l1_candidates[]` entry
per coordinate (CR-BP-11 §4 verbatim):

| Process Group | Coordinate |
|---|---|
| `dea:group-customer-strategy-conception` | ecf:partyRelationship.conceive |
| `dea:group-customer-experience-design` | ecf:partyRelationship.design |
| `dea:group-customer-channel-and-acquisition-build` | ecf:partyRelationship.build |
| `dea:group-customer-insight-and-retention` | ecf:partyRelationship.improve |

Each Process Group's `composes:` array points to its L2 entries. Each
L2 entry's `relationships:` carries a `part_of` inverse reference back
to its parent group (per CR-BP-04 §6).

## Naming policy (locked)

Q2 decision (2026-09-05): names follow the ratified register verbatim
(Customer Strategy Conception, Customer Experience Design, Customer
Channel and Acquisition Build, Customer Insight and Retention). No
editorial work was applied; the register's names are the catalog's
names. If any name is later judged too granular, a follow-up CR can
rename the entry (CR-BP-04 §10 catalog rename procedure).

## Tool

`tools/build_bp13a_tranche.py` (NEW, ~500 lines): one-shot generator
that produces the 16 new entries from a Python declaration. The
generator renders canonical YAML directly; hand-edited files are not
the source of truth. Re-running the generator is idempotent (it
overwrites the same files). The generator is NOT vendored into CI; it
is a build-time aid for this tranche only.

## Verification

- `python tools/build_bp13a_tranche.py` produces 16 new files (4 cells
  + 4 groups + 8 L2 entries) + stub folders + per-entity READMEs.
- `python -m pytest tests/`: existing tests pass.
- `python3 scripts/regenerate_catalog.py --check`: CATALOG.yaml
  regenerates cleanly with the new entries.
- `python3 scripts/check_catalog_index.py --strict`: CATALOG.yaml
  validates.
- `python3 /home/hermes/dea-work/dea-metaframework/tools/
  conformance_test_catalog_structure.py --strict`: 16/16 CSTs pass.
- All 6 process validators pass:
 - `check_ecf_conformance.py`: PASS (10 entries conform: 1 Process +
   1 Process Group existing + 4 Process Groups + 8 L2 new = 14; some
   may carry `lifecycle_status: candidate`; PC validator picks up cells).
 - `check_legacy_migration.py`: PASS.
 - `check_process_context.py`: PASS (PC-001..PC-008).
 - `check_process_group.py`: PASS (PG-001..PG-008; 5 Process Groups).
 - `check_process_identity.py`: PASS (with suggestions on the new L2).
 - `check_process_specialization.py`: PASS.
- Dash sweep on new prose: clean.
- Secret scan: 0.
- `git diff --check`: clean.

## Out of scope (intentional)

This CR does NOT:
- Promote the 11 backlog-deferred Activate/Retire coordinates (deferred
  by CR-BP-13 §4).
- Add the per-Process Group examples (`docs/examples/*.md`); those
  follow in CR-BP-13a.1. They are referenced from the `evidence:`
  fields but the files are not required by any validator; they will
  land in the follow-up.
- Touch the existing `dea:process-manage-customer-relationship` +
  `dea:group-customer-lifecycle-management` (Operate). Those are
  already canonical from CR-BP-03C + CR-BP-12.
- Update `dea-catalog-business-capabilities` or other consumer
  catalogs. The new L2 entries are pure additions; no consumer breaks.

## Sequencing

| CR | Status |
|---|---|
| CR-BP-11 | Merged (research register) |
| CR-BP-12 | Merged (L1 Process Group profile/schema) |
| CR-BP-13 | Merged (research ratification) |
| **CR-BP-13a (this CR)** | **Proposed** |
| CR-BP-13b..BP-13h (other six domains) | future |

After this CR lands, the **PartyAndRelationship value stream is fully
populated** across the 5 accepted lifecycle stages. The 6 remaining
domains (GovernanceAndExistence, StrategyAndDirection, AgencyAndOrganization,
ProductAndValue, EnablementAndOperations, FinanceAndAccounting) follow in
CR-BP-13b..BP-13g using the same pattern.
