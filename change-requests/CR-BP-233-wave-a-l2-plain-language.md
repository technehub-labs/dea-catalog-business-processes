# CR-BP-233: Wave A — L2 Business Process Plain-Language Authoring (145 Records)

**Status**: Accepted (landed via PR #229; status backfilled post-merge per the immutability rule)
**Layer**: Process Catalog (operational documentation completions)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-05
**Depends on**: CR-BP-230 (the five plain-language fields this wave authors), CR-BP-231 (the profile v3 README that renders them), CR-BP-232 (the HUM-001..007 gate whose L2 findings this wave drains to zero), CR-BP-225 (the EOF-appended-block authoring convention and the L2 `definition` this prose must stay MECE against)

> **Scope.** Wave A of the two-layer remediation programme (owner directive 2026-11-05): author the five plain-language fields for **all 145 L2 Business Process records**, grounded in each record's own documented content (name, definition/description, process_intent, trigger, outcome, identity.outcome_statement, owner, actors, stakeholders, inputs, outputs) — the CR-BP-220/225 derivation discipline applied to authored prose: **no invention** (no org names, systems, KPIs, or regulations absent from the record; the record's own actors/stakeholders/consumers may be referenced). Every record gains `plain_language_name`, `plain_language_description`, `business_purpose`, `practical_context`, `worked_example{agent_type, narrative}` appended at EOF with the CR-BP-225 comment-banner convention. Provenance: authored under Emmanuel A. Otchere's ownership per the Authorship Cardinal Rule (CR-BP-118); the authoring agent's agency is recorded here and in the execution manifest only. After authoring: 3,723 READMEs regenerate (Part I renders the provided prose instead of the standing pointer on all 145 L2 records), `CATALOG.yaml` regenerates, and gate [51] HUM-001..004/006 findings for the L2 layer drain to zero (L3/L4/L1/L0 findings remain until their waves).

**Lands against**: 145 L2 record files (EOF-appended comment banner + five fields); `scripts/author_cr233_wave_a.py` (the applying driver, idempotent); `reconciliation/closure/cr233-wave-a.json` (execution manifest: per-record field sizes + agent_type distribution); 3,723 regenerated READMEs; regenerated `CATALOG.yaml` + `reconciliation/human-readability-report.{yaml,json}`; this CR + CHANGELOG + register row. **0 id changes. 0 gate changes. 0 schema changes. 0 L3/L4/L1/L0 record changes.**

## 1. The authoring method

| Concern | Contract |
|---|---|
| Grounding | Every authored string traces to the record's own fields; worked examples cast the record's own actors |
| MECE (HUM-007) | `plain_language_description` is fresh prose; it never restates the formal `definition`/`description` as a contiguous span |
| Jargon (HUM-005) | The denylist is enforced mechanically at apply time (the CR-BP-232 list); any hit blocks the record |
| Semantic containment | `plain_language_name` is a rendering of the canonical name — familiar, never an ambiguous synonym; canonical names/IDs unchanged |
| Agent typing | `agent_type` chosen from the record's own actors (system/platform actors → non-human/mixed; people roles → human) |
| Idempotency | The driver skips records already carrying `plain_language_name` (second run: 0 writes) |

## 2. What does NOT change

- No canonical name, id, status, owner, boundary, or relationship changes — the five fields are additive documentation attributes.
- No gate logic or posture changes; no schema changes (CR-BP-230 already enabled the fields).
- The generated Part II sections are byte-stable for every L2 record (their source fields are untouched; only Part I changes).

## 3. Verification / Acceptance Criteria

1. HUM gate on the L2 layer: **0 findings** across {HUM-001..004, HUM-006, HUM-005, HUM-007} for all 145 L2 records (corpus-wide HUM findings drop from 18,615 to 17,890 = 3,578 remaining unbackfilled records × 5).
2. Schema validation green (3,675 CI-visible records) with the five fields present on all 145 L2 records.
3. RDM-001/002/003 CONFORMANT on the regenerated corpus; each L2 README's Part I renders the authored prose with no standing pointer.
4. All 145 L2 Part I sections carry a `Worked Example` with a valid `agent_type`; the distribution is recorded in the execution manifest.
5. Driver idempotency: second run writes 0.
6. Full gate suite green; freshness procedure (commit → CATALOG regen → amend) honoured.
