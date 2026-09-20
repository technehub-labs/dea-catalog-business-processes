# CR-BP-19: L1 Register Re-derivation Against ECF v2.4.0 (Rediscovery)

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
**Date**: 2026-09-07
**Depends on**: CR-BP-13 (register v1); CR-BP-17 (v2.3.0 migration carrier); CR-BP-18 (v2.4.0 migration carrier); dea-metaframework CR-ECF-006 + CR-ECF-007
**Related**: dea-metaframework framework/domain-grounding.md; ADR-ECF-001; ADR-ECF-002; CR-BP-20 (alignment, planned)

## 1. What this CR is

A full re-derivation of the L1 Process Group register
(`entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml`)
against the ECF v2.4.0 canonical domain semantics — the "rediscovery" phase of
the L0→L2 rediscovery / alignment / landing workstream.

The v2.3.0 (CR-BP-17) and v2.4.0 (CR-BP-18) migrations renamed the domain keys
in the register, but the register *content* was carried over unchanged. The
ECF renames were semantic re-scopings, not pure renames (see §2), so register
v1 content is misaligned with v2.4.0 meaning in 5 of 7 domains.

This CR lands **register v2**: all 49 coordinates re-derived against
`dea-metaframework/framework/domain-grounding.md` (the v2.4.0 grounding
records), with explicit migration notes where content moves between cells.

## 2. Why re-derive (the semantic shifts)

| Domain (v2.4.0) | Semantic shift vs register v1 content |
|---|---|
| StrategyAndDirection | **Full replacement.** Former Supply & Resources dissolved: physical/virtual resources → Enablement & Operations (as enablers); supplier relationships → Party & Relationship; financial resources → Finance & Accounting (grounding §3.2 evidence). The vacated axiom slot ("persists" as deliberate steering) now holds purpose, ambition, strategic choices, objectives, planning, adaptation. All 6 previously-ratified cells held dissolved-domain content. |
| PartyAndRelationship | **Broadened.** Customer-only → all external parties (customer, supplier, partner, regulator, community). One party, one bond, multiple facets (grounding §3.4). |
| FinanceAndAccounting | **Narrowed to monetary reality.** "Value" in the abstract explicitly excluded (grounding §3.7). "Value Strategy Conception" / "Value Architecture Design" / "Value Performance" candidates removed. |
| AgencyAndOrganization | **Substrate-independence.** Human "workforce" reframed as agent capacity covering human + artificial + hybrid agents (grounding §3.3; ADR-ECF-002). |
| ProductAndValue | **Renamed concerns.** "Offering" dropped as vague; Proposition/Portfolio/Evolution naming per grounding §3.5. Service delivery execution and partner programmes moved out (to OE and PR respectively). |
| EnablementAndOperations | **Absorbs enablement.** Takes physical + technology assets as enablers of execution from dissolved Supply & Resources (grounding §3.6). Technology/IT coverage asserted here. |
| GovernanceAndExistence | **Boundary clarified.** Strategic choices excluded — "Governance authorizes but does not direct; Strategy & Direction directs within the authorized frame" (grounding §3.1). Corporate strategy conception moves out. |

## 3. The split decision (user-approved Option A)

GE-Conceive in v1 held "Strategy and Governance Conception" with L2 candidate
"Develop corporate strategy". Per grounding §3.1/§3.2, strategic choices belong
to Strategy & Direction.

**Decision (user, 2026-09-07): Option A — split.**
- "Develop corporate strategy" migrates to `strategy-direction x conceive`.
- GE-Conceive keeps charter / mandate / policy direction / risk-framework
  conception ("Governance Mandate Conception", "Policy and Charter Conception").
- The landed entity `dea:group-strategy-and-governance-conception` (and its
  member L2s) is renamed/re-scoped in the follow-on alignment CR (CR-BP-20).

## 4. Content migration map (v1 → v2)

| v1 cell (content) | v2 home |
|---|---|
| strategy-direction x conceive/design/build (sourcing, supply-base, asset strategy/blueprint/acquisition) | enablement-operations x conceive/design/build (execution-side); supplier relationship conception → party-relationship x conceive |
| strategy-direction x operate (Sourcing and Procurement Operation; Asset and Facility Operation) | enablement-operations x operate (procurement execution, facility, asset maintenance); Supplier Management Operation → party-relationship x operate |
| strategy-direction x improve (supplier review/consolidation; asset utilization) | supplier side → party-relationship x improve; asset side → enablement-operations x improve |
| strategy-direction x retire (supply and asset retirement) | enablement-operations x retire (deferred) |
| governance-existence x conceive (Develop corporate strategy) | strategy-direction x conceive (Option A split) |
| party-relationship x operate (Demand Fulfillment) | enablement-operations x operate (fulfillment is execution) |
| product-value x operate (service delivery management; partner and alliance programme) | enablement-operations x operate; party-relationship x operate |
| finance-accounting x operate (Procure-to-Pay / Order-to-Cash *execution*) | enablement-operations x operate; the monetary recording of those cycles remains in finance-accounting |

## 5. Disposition normalization

v1 ratified 38 cells and deferred 11 — inconsistently: 3 Activate cells
(strategy-direction, product-value, enablement-operations) were
ratified-accepted while the other 11 Activate/Retire cells were deferred under
a rationale that applies to all of them.

v2 applies the deferred rationale uniformly: **35 ratified-accepted
(7 domains × Conceive/Design/Build/Operate/Improve), 14 backlog-deferred
(all Activate/Retire cells)**. The 3 previously-ratified Activate cells change
disposition with an explicit note in each cell's `deferral_reason`.

## 6. Structural hygiene fixes (register v1 bugs)

- Duplicate `deferral_reason` keys on 11 cells (YAML last-write-wins; the
  register-wide rationale was silently overwritten by the per-cell note).
  v2: single `deferral_reason` carrying both.
- Malformed `in_scope` lists on 4 cells mixing strings and lists with embedded
  "Out of scope:" text. v2: `in_scope` is a string; `out_of_scope` is a list.
- Duplicate `out_of_scope` keys on 3 cells. v2: single key.
- Stray non-ASCII tokens in two evidence lists ("Service退役", "Workforce退出").
  v2: removed.
- Process-context id prefixes updated to v2.4.0 domain codes: `pc-sd-*` (was
  `pc-sr-*`), `pc-ao-*` (was `pc-po-*`), `pc-pv-*` (was `pc-po2-*`),
  `pc-oe-*` (was `pc-od-*`), `pc-fa-*` (was `pc-fv-*`). `pc-ge-*` and
  `pc-pr-*` unchanged.

## 7. What this CR does NOT do

- No canonical entity changes. Landed-population alignment (group renames,
  GE/SD split execution, the 3 BP-ARC-ID-003 outcome mismatches) is CR-BP-20.
- No new L1/L2 landings. Per-domain landing tranches follow after CR-BP-20.
- No tooling changes. The register is a research artifact; no gate consumes it.

## 8. Verification

- `python3 -c` YAML parse: 49 cells, 35 ratified / 14 deferred, matching the
  `ratification` block; all cells carry the full field set; every deferred
  cell carries `deferral_reason`.
- Full pytest suite: no regressions (register tests use fixtures).
- `check_process_semantics.py`, `check_ecf_conformance.py`,
  `check_admission_gate.py --strict-provenance`, `conformance_result.py`: pass.
- `CATALOG.yaml` regenerated (git-date-based `last_modified` for the
  register's host entity subtree).
