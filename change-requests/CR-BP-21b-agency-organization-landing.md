# CR-BP-21b: AgencyAndOrganization Landing (ECF v2.4.0 — Second Unadmitted Domain)

**Status**: Accepted
**Admission authority**: yes
**Layer**: Process Catalog
**Owner**: Emmanuel A. Otchere
**Date**: 2026-09-07
**Depends on**: CR-BP-19 (register v2); CR-BP-20 (alignment); CR-BP-21a (StrategyAndDirection landing, prior); CR-DEA-BC-07 (workforce capabilities re-stated substrate-neutral, BC PR #48)
**Related**: dea-metaframework/framework/domain-grounding.md §3.3; ADR-ECF-002 §5 (Substrate Independence Stress Test); CR-ECF-007

## 1. What this CR is

Second landing tranche under the CR-BP-21 series. Lands
AgencyAndOrganization against the rediscovered register v2 cells
(Conceive / Design / Build / Operate / Improve). The Activate / Retire
cells remain deferred register-wide per CR-BP-19.

**Substrate Independence** is the load-bearing property of this
landing. v2.4.0 (CR-ECF-007, ADR-ECF-002 §5) reframed this domain from
the v2.3.0 "People & Organization" to "Agency & Organization" because
the substrate-independent test requires that human, artificial, and
hybrid agents all map to the same process identities without
reclassification. The BC catalog's `capability-workforce-management`
already re-stated substrate-neutrally under CR-DEA-BC-07 (PR #48);
this CR follows the same pattern for the process catalog.

## 2. The 5 process contexts

- `dea:pc-ao-conceive` — Agent Capacity & Organization Conception
- `dea:pc-ao-design` — Organization & Agent Topology Design
- `dea:pc-ao-build` — Agent Acquisition & Onboarding
- `dea:pc-ao-operate` — Agent Operations & Performance
- `dea:pc-ao-improve` — Agent Development & Organization Improvement

The Activate / Retire cells (per register v2) remain deferred.

## 3. The 1 Process Group (L1)

- `dea:group-organization-and-agent-conception` — Process Group for
  AgencyAndOrganization × Conceive. Composes the 3 L2s of the
  Conceive cell (Frame agent capacity strategy, Frame organization
  model, Conceive workforce and agent mix).

  Naming note: the L1 group covers the full Conceive cell
  (Agent Capacity Strategy + Organization Model + Workforce/Agent Mix).
  The id is `dea:group-organization-and-agent-conception` to align with
  the BC catalog's `capability-workforce-management` (which lands under
  `agency-organization` per CR-DEA-BC-07). The id surfaces "organization
  and agent" rather than "workforce and agent" because the canonical
  v2.4.0 identifier is Agency & Organization, not Workforce & People
  (the substrate-neutral renaming grounded in ADR-ECF-002 §5).

## 4. The 5 L2 Business Processes

One L2 per ratified cell. **All substrate-neutral** (no "human",
"talent", "AI model", "ML" qualifiers — the process identity is the
same for biological, artificial, and hybrid agents). Per CR-BP-19,
all land as `lifecycle_status: candidate`.

| L2 ID | Cell | process_intent | process_type | process_specialization |
|---|---|---|---|---|
| dea:process-frame-organization-and-agent-strategy | AO/Conceive | develop | management | workforce |
| dea:process-design-organization-structure | AO/Design | develop | management | workforce |
| dea:process-acquire-and-onboard-agents | AO/Build | develop | core | workforce |
| dea:process-operate-agent-performance | AO/Operate | operate | management | workforce |
| dea:process-develop-agents-and-organization | AO/Improve | develop | management | workforce |

The 3-L2 Conceive cell lands 1 L2 (organization+agent strategy frame;
remaining 2 in CR-BP-21b.1). The 4-L2 Design cell lands 1 L2
(organization structure; remaining 3 in CR-BP-21b.1). The 5-L2
Operate cell lands 1 L2 (agent performance operation; remaining 4 in
CR-BP-21b.1). The 4-L2 Improve cell lands 1 L2 (agents and
organization; remaining 3 in CR-BP-21b.1).

## 5. Substrate-neutral naming convention

Per ADR-ECF-002 §5 (Substrate Independence Stress Test) and the
work done in CR-DEA-BC-07 for the BC catalog, this landing adopts
the following substrate-neutral vocabulary:

- "Agent" instead of "Human" / "Employee" / "Talent" / "Personnel" /
  "AI model" / "Bot"
- "Acquire and onboard" instead of "Recruit" / "Hire" / "Train"
  (covers recruitment, model deployment, API integration, etc.)
- "Operate agent performance" instead of "Manage performance" /
  "Monitor utilisation" (substrate-neutral)
- "Develop agents and organization" instead of "Learning &
  development" / "Model fine-tuning"
- "Workforce" as the **process_specialization** (carries the legacy
  v2.3.0 vocabulary for BC alignment while the substrate-neutral
  language governs process names and outcome statements)

## 6. Provenance + classification (per the landed-population pattern)

- `lifecycle_status: candidate` for all 5 L2s and the 1 L1 group.
- `process_intent` / `process_type` from canonical vocabularies
  (CR-BP-14 §10).
- `process_specialization: workforce` for cross-catalog alignment
  with BC `capability-workforce-management`.
- `metadata.change_history` carries the CR-BP-21b entry on every
  entry with phase-7 marker, `cr: CR-BP-21b`, the date, and the
  rationale (grounds the change in domain-grounding.md §3.3 +
  ADR-ECF-002 §5).
- `metadata.cross_context_overlap: []` (no cross-cell overlap;
  MECE for the AO cells is verified in the register v2).

## 7. Cross-repo alignment

- `dea-catalog-business-capabilities`: `capability-workforce-management`
  is affiliated with `agency-organization` per CR-DEA-BC-07
  (PR #48, merged 2026-09-07). The BC catalog re-stated the
  capability substrate-neutrally. This process landing follows the
  same convention.
- `dea-metaframework/framework/domain-grounding.md` §3.3 is the
  authoritative source for the AO domain's MECE partition and
  substrate-independence note.

## 8. What this CR does NOT do

- The remaining 3 unadmitted v2.4.0 domains (ProductAndValue,
  EnablementAndOperations, FinanceAndAccounting) — each gets its
  own CR-BP-21c..e landing tranche.
- The remaining L2s of the AO/Conceive cell (Frame organization
  model; Conceive workforce and agent mix), AO/Design cell (Role
  catalogue; Competency framework; Agent topology), AO/Operate
  cell (4 additional L2s), and AO/Improve cell (3 additional L2s) —
  follow-up CR-BP-21b.1 when more L2 material is ready.
- AO/Activate and AO/Retire cells — register v2 keeps these
  deferred.
- Updating the `dea:process-manage-customer-relationship` (the one
  PartyAndRelationship L2) — out of scope here. PR cells are
  already landed; no rename required.

## 9. Verification

- All 15 conformance gates pass (CONFORMANT).
- pytest 149 pass / 1 pre-existing failure.
- check_process_identity 0 outcome_mismatch findings.
- check_ecf_conformance: 39 entries (34 prior + 5 new).
- Admission gate `--strict-provenance`: exit 0; the 6 new entries
  (5 L2s + 1 L1 group) all carry the CR-BP-21b reference.
- Fresh-clone reproduction (with `git remote set-url origin ...git`
  normalization per `.github/workflows/ci.yml`):
  `python scripts/regenerate_catalog.py --check` OK.
