# CR-BP-21c: ProductAndValue Landing (ECF v2.4.0 — Third Unadmitted Domain)

**Status**: Accepted
**Admission authority**: yes
**Layer**: Process Catalog
**Owner**: Emmanuel A. Otchere
**Date**: 2026-09-08
**Depends on**: CR-BP-19 (register v2); CR-BP-20 (alignment); CR-BP-21a (StrategyAndDirection landing, prior); CR-BP-21b (AgencyAndOrganization landing, prior)
**Related**: dea-metaframework/framework/domain-grounding.md §3.5; CR-BP-21d..e (remaining 2 unadmitted domains, planned)

## 1. What this CR is

Third landing tranche of the CR-BP-21 series. Lands
ProductAndValue against the rediscovered register v2 cells
(Conceive / Design / Build / Operate / Improve). The Activate / Retire
cells remain deferred register-wide per CR-BP-19.

v2.4.0 (CR-ECF-006) reframed this domain from the v2.3.0 "Product &
Offering" to "Product & Value" because "Offering" overlapped with
"Product" without distinguishing the value proposition. The domain
manages the complete lifecycle of whatever the enterprise creates,
shapes, packages, and makes available for exchange with external
parties: products, services, solutions, experiences, platforms, and
intellectual property.

## 2. The 5 process contexts

- `dea:pc-pv-conceive` — Proposition & Portfolio Conception
- `dea:pc-pv-design` — Proposition & Packaging Design
- `dea:pc-pv-build` — Product Development & Market Readiness Build
- `dea:pc-pv-operate` — Portfolio Management & Proposition Lifecycle Operation
- `dea:pc-pv-improve` — Product Evolution & Portfolio Rationalization

The Activate / Retire cells (per register v2) remain deferred.

## 3. The 1 Process Group (L1)

- `dea:group-proposition-conception` — Process Group for
  ProductAndValue x Conceive. Composes the 3 L2s of the
  Conceive cell (Frame value proposition thesis, Frame portfolio
  direction, Frame innovation thesis).

  Naming note: the L1 group covers the full Conceive cell
  (Proposition Conception + Portfolio Direction Conception).
  The id is `dea:group-proposition-conception` to capture the
  principal L1 candidate; the group scope covers both L1 candidates
  as a single bounded Process Group per CR-BP-12 §4 (group id is
  domain-scoped, not cell-component-scoped).

## 4. The 5 L2 Business Processes

One L2 per ratified cell. Per CR-BP-19,
all land as `lifecycle_status: candidate`.

| L2 ID | Cell | process_intent | process_type |
|---|---|---|---|
| dea:process-frame-value-proposition-thesis | PV/Conceive | develop | management |
| dea:process-design-product-and-service-propositions | PV/Design | develop | management |
| dea:process-develop-product-variants | PV/Build | develop | core |
| dea:process-operate-product-catalogue | PV/Operate | operate | core |
| dea:process-conduct-proposition-performance-review | PV/Improve | develop | management |

The 3-L2 Conceive cell (value proposition thesis, portfolio direction,
innovation thesis) lands 1 L2 (value proposition thesis; remaining 2 in
CR-BP-21c.1). The 3-L2 Design cell (propositions, packaging,
innovation experiment) lands 1 L2 (propositions; remaining 2 in
CR-BP-21c.1). The 4-L2 Build cell (product variants, service
capability, innovation prototype, market readiness) lands 1 L2
(product variants; remaining 3 in CR-BP-21c.1). The 3-L2 Operate cell
(catalogue, portfolio performance, proposition lifecycle) lands 1 L2
(catalogue; remaining 2 in CR-BP-21c.1). The 3-L2 Improve cell
(proposition performance review, product evolution, portfolio
rationalization) lands 1 L2 (performance review; remaining 2 in
CR-BP-21c.1).

## 5. Provenance + classification (per the landed-population pattern)

- `lifecycle_status: candidate` for all 5 L2s and the 1 L1 group.
- `process_intent` / `process_type` from canonical vocabularies
  (CR-BP-14 §10).
- `metadata.change_history` carries the CR-BP-21c entry on every
  entry with phase-7 marker, `cr: CR-BP-21c`, the date, and the
  rationale (grounds the change in domain-grounding.md §3.5).
- `metadata.cross_context_overlap: []` (no cross-cell overlap;
  MECE for the PV cells is verified in the register v2).

## 6. Cross-repo alignment

- `dea-metaframework/framework/domain-grounding.md` §3.5 is the
  authoritative source for the PV domain's MECE partition and
  the "value-bearing proposition" semantic definition.
- The BC catalog's `capability-offering-management` is the
  capability-side counterpart; the process catalog uses
  "proposition" (not "offering") per the v2.4.0 rename rationale.

## 7. What this CR does NOT do

- The remaining 2 unadmitted v2.4.0 domains
  (EnablementAndOperations, FinanceAndAccounting) — each gets its
  own CR-BP-21d..e landing tranche.
- The remaining L2s of the PV cells — follow-up CR-BP-21c.1 when
  more L2 material is ready.
- PV/Activate and PV/Retire cells — register v2 keeps these
  deferred.
- Cross-repo BC capability-offering-management re-affiliation or
  rename — out of scope here.

## 8. Verification

- All 15 conformance gates pass (CONFORMANT).
- pytest 149 pass / 1 pre-existing failure.
- check_process_identity 0 outcome_mismatch findings.
- check_ecf_conformance: 44 entries (39 prior + 5 new).
- Admission gate `--strict-provenance`: exit 0; the 6 new entries
  (5 L2s + 1 L1 group) all carry the CR-BP-21c reference.
- Fresh-clone reproduction (with `git remote set-url origin ...git`
  normalization per `.github/workflows/ci.yml`):
  `python scripts/regenerate_catalog.py --check` OK.
