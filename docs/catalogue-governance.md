# Catalogue Operational Governance Model

**Status**: Active (CR-BP-94-EXT-24 execution, 2026-11-04 — delivered ahead of the 2026-12-31 window by user directive)
**Applies to**: `dea-catalog-business-processes` (all 3,723 canonical records, L0–L4)

This document is the operating model that CR-BP-94-EXT-24 requires: the
transition from project-based enrichment to continuous catalogue
stewardship. It consolidates the governance machinery that already
operates in this repository and names the cadences that keep it alive.

## 1. Closure summary (the authoritative baseline)

The EXT-08..23 programme closed with the machinery in
`reconciliation/closure/`:

| Register | Contents |
|---|---|
| `catalogue-baseline.json` | the accepted baseline snapshot |
| `programme-closure-matrix.json` | EXT-08..23 deliverable-by-deliverable closure |
| `governance-roles.json` | the 9 governance roles mapped to house conventions |
| `ownership-register.json` | ownership dispositions (GOV-002 role-based) |
| `lifecycle-register.json` | per-record lifecycle state |
| `residual-gap-register.json` | 12 governed residual gaps |
| `improvement-backlog.json` | 12 prioritised improvement items |
| `deferred-work-register.json` | deferred work with dispositions |
| `exception-register.json` | approved exceptions |
| `ext24-manifest.json` | the closure gate result (0 findings, passed) |
| `ext24-l0-register-execution.json` | the L0 register execution this document accompanies |

Enforced continuously by gate [49] (Programme Closure, CG-001..080) and
gate [50] (Completeness Profiles, CE-000..900) in the conformance rollup.

## 2. The 2026-11-04 execution (ahead of schedule)

The two standing items CR-BP-224 had re-pointed to this window are
delivered early:

1. **L0 role assignment** — all 49 Process Contexts carry
   `governance.roles` with the domain Process Owner (GOV-002 role-based,
   extracted from the domain's own L1 owner blocks) and
   `governance.provenance` with `review_due: 2026-12-31`.
2. **L0 metrics register** — all 49 Process Contexts carry `metrics`
   (KPI/KRI/KCI per CR-BP-120 shape; 147 entries). KPIs ground in each
   cell's own first outcome; KRIs in its own first exclusion; targets
   are directional stage standards — no invented numbers. Owner
   confirmation of the derived register is the window's remaining act,
   already scheduled by the review_due dates.

Consequence: zero `standing item` pointers remain in any of the 3,723
generated READMEs; DOC-019 advisories are 0. The generator's
derivations (CR-BP-224 method, extended here to L0 charter rules and L2
inherited-control context) render every operational section from record
fields.

## 3. Recurring governance cadences

| Cycle | Cadence | Owner | Mechanism |
|---|---|---|---|
| Owner review of the L0 register | by 2026-12-31, then annual | Domain Process Owners (GOV-002) | `governance.provenance.review_due` on each PC; changes land as CRs |
| Evidence freshness review | semi-annual | Domain Process Owners + reviewers (EXT-16 roles) | `evidence[].verified` flags per EXT-15; stale evidence re-verified or flagged |
| Conformance monitoring | every push (CI) | Catalogue maintainer | the 50-gate rollup (`conformance_result.py`); blocking gates fail CI |
| Completeness profiles | every push (CI) | Catalogue maintainer | gate [50] CE-000..900, 0-findings posture preserved |
| KRI review | quarterly | Domain Process Owners | the `metrics.risk` entries per PC |
| KCI review | semi-annual | Domain Process Owners + compliance function | the `metrics.compliance` entries per PC |
| Residual-gap triage | per-quarter or on trigger | Catalogue governance (EXT-24 §8.1 roles) | `residual-gap-register.json` + `improvement-backlog.json` re-prioritisation via CR |
| Dependency / register reconciliation | weekly (org CI, CR-014) + per release | Catalogue maintainer | dea-governance portfolio register R1–R4 |

## 4. Event-triggered reviews (change-impact management)

An out-of-cycle review of affected records is mandatory when any of:

- an organisational change invalidates a process responsibility
  (owner blocks, `actors`/`stakeholders`) — GOV-002/GOV-003 re-derivation;
- a business process changes in operation (definition, scope, boundary);
- a related catalogue (capabilities, information-assets, …) changes ids
  or structure touching cross-catalogue references (IDM-003/IDM-008
  catch the mechanical drift; semantic review via CR);
- the OpenDEA metamodel or ECF contract evolves (metamodel-pointer /
  `dependencies.yaml` pins move; reconciliation CR required);
- schema, profile or vocabulary changes land (EXT-10/11 artefacts;
  affected records re-profiled);
- evidence becomes stale or superseded (EXT-15 registers);
- new automation/AI agents alter how activities/tasks execute
  (EXT-16 §REQ-16-09 boundaries apply to any documentation of the change).

## 5. Exception and deferral management

Exceptions and deferrals live in their registers with dispositions and
are never silently dropped: `exception-register.json`,
`deferred-work-register.json`. New exceptions enter via CR with an
explicit disposition and review date. The two EMB-003-sealed files (the
embargo carrier and the CR-BP-112 determination) are permanent
governance artefacts: their open `open_change_requests` count is
by-design and not a defect.

## 6. Change control

All catalogue change flows through the CR governance chain (house
landing conventions): implement + regenerate `CATALOG.yaml` in the same
PR + CHANGELOG `[Unreleased]` entry + register row, PR review, and the
commit→regen→amend discipline before merge. READMEs are generated
artifacts — never hand-edited (RDM-001..003).
