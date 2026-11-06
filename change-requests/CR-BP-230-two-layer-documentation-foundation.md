# CR-BP-230: Two-Layer Documentation Foundation (Plain-Language Attributes)

**Status**: Accepted (landed via PR #228; status backfilled post-merge per the immutability rule)
**Layer**: Cross-cutting (catalog documentation layer)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-05
**Depends on**: CR-BP-94-EXT-07 (the consolidated README profile this programme layers onto), CR-BP-224 (the derive/re-point/retire placeholder disposition whose standing-pointer pattern this programme reuses), CR-BP-221 (the profile-integrity precedent: layout changes land at the generator source, then regenerate the corpus)

> **Scope.** Owner directive 2026-11-05 (the "nomenclature" assessment): every entity must be *semantically precise enough for architectural and computational use, and sufficiently intelligible for a human being to recognise, understand and relate to it in the context of everyday business operations*. The catalog's 3,723 generated READMEs serve architects and machines but give a business reader no plain-language entry point. This CR is the **foundation tranche** of the two-layer documentation programme: it introduces the five plain-language record attributes (schema-level enablement only) that the documentation CR (CR-BP-231), the validation CR (CR-BP-232) and the four remediation waves (CR-BP-233..236, L2 → L3 → L4 → L1/L0) consume. The architecture: provided content lives **in the YAML records** and flows through the generator (the CR-BP-94-EXT-18..21 backfill precedent) — it is never hand-authored into READMEs, which would break the RDM-001 byte-identity gate. One README, two tagged parts: **Part I — Human-Readable Interpretation (provided)**, then **Part II — Canonical Record (CI generated)**.

**Lands against**: `schemas/entity.schema.json`, `schemas/entities/activity.schema.json`, `schemas/entities/task.schema.json`, `schemas/entities/process-group.schema.json`, `schemas/entities/process-context.schema.json` (five optional plain-language properties added to each); this CR + CHANGELOG + register row. **0 entity-record changes. 0 id changes. 0 gate changes. 0 README regeneration (CR-BP-231 carries the corpus regen).**

## 1. The two-layer principle

Every process entity documents two audiences simultaneously:

| Layer | Audience | Content | Source |
|---|---|---|---|
| Part I — Human-Readable Interpretation | Business and operational stakeholders | Plain-language name, everyday description, business purpose, practical context, worked example | `plain_language_*` record fields (provided, authored in CR-BP-233..236) + derived identity card |
| Part II — Canonical Record | Architects, analysts, engineers, machines | Formal definition, intent and scope, triggers, IO, boundaries, relationships, decomposition, governance | Existing generated profile (CR-BP-94-EXT-07 v2, unchanged) |

The layers describe the **same entity**. Part I must not introduce meanings that contradict or extend Part II (enforced by the CR-BP-232 gates); it is an interpretation, not a second definition. The MECE rule: Part I prose MUST NOT restate the formal definition verbatim, and the identity card is a narrative statement, not a duplicate of the Part II identity table.

## 2. The plain-language attribute set (normative)

Five new **optional** record fields, identical across all five entity schemas:

| Attribute | Type | Constraint | Purpose |
|---|---|---|---|
| `plain_language_name` | string 1..200 | MUST remain semantically equivalent to the canonical `name`; a familiar rendering, not an informal synonym that introduces ambiguity | The business-facing name (e.g. "Preserve the Supervisor Notification Record") |
| `plain_language_description` | string 1..2000 | Everyday explanation; no metamodel jargon (HUM denylist, CR-BP-232) | "In a nutshell" + "what this means in everyday work" |
| `business_purpose` | string 1..1000 | Why the entity exists; the business significance | "Why it matters" |
| `practical_context` | string 1..1000 | When and where the work is encountered in operations | "When you'd encounter it" |
| `worked_example` | object | `agent_type` ∈ {`human`, `non-human`, `mixed`} + `narrative` 1..2000 | An office-relatable worked example of the task being done by an agent of type human or non-human; at L4, `agent_type` defaults from the record's `responsibility` field (author-refinable) |

Field shapes follow the existing string conventions (`minLength`/`maxLength` per the `trigger`/`outcome`/`responsibility` pattern). The L3/L4 schemas are `additionalProperties: false`, so this schema edit is the enabler for every wave; the L2 and L1 schemas are likewise closed at top level and gain the same block. The L0 `process-context.schema.json` gains the same optional block for programme symmetry (L0 records may carry a plain-language cell charter summary; population is Wave D's discretion).

Per the Authorship Cardinal Rule (CR-BP-118, PROSE-001/002): all provided prose authored in CR-BP-233..236 is authored under Emmanuel A. Otchere's ownership; agent agency is recorded in the CR narrative layers only, never in authorship-bearing fields.

## 3. Naming principles (adopted; normative from CR-BP-232)

Canonical names and canonical IDs **do not change** in this programme. The seven naming principles of the assessment govern `plain_language_name` authoring (Wave A–D) and any future naming CR:

1. Use familiar business vocabulary wherever possible.
2. Prefer natural English constructions over mechanically concatenated semantic terms.
3. Use consistent verb-object naming for executable process elements.
4. Avoid unnecessary hyphenation and compound terminology.
5. Avoid abbreviations unless genuinely established business language.
6. Ensure the name communicates the action or business subject without requiring the reader to inspect the identifier.
7. Preserve the formal semantic meaning even when a more familiar expression is used.

## 4. What does NOT change

- **No canonical `name` changes; no id changes** — `plain_language_name` carries the human-facing rendering; the qgmj5u-style ID family and 3,723 change histories are untouched.
- **No metamodel changes** — the dea-metamodel introduction of the plain-language attributes (CR-MET-019-scale fan-out: schemas, TTL, pydantic, registry, sqlite, typescript) is **enabled** by this CR and lands as a companion follow-up; the catalog-side schemas are the operational truth for record validation until then.
- **No README regeneration in this CR** — zero records carry the new fields yet; the corpus regen happens in CR-BP-231 when the generator renders Part I.
- **No gate changes** — CR-BP-232 introduces the HUM gates; existing gates are untouched.
- The v2 generated profile (7/8 sections, numbering, RDM-001/003 byte-identity) is preserved intact inside Part II.

## 5. Verification / Acceptance Criteria

1. All five schemas gain the five optional properties with the §2 constraints; `additionalProperties: false` is preserved on L1/L3/L4.
2. Schema validation suite green on the full 3,723-record corpus (zero records carry the new fields yet — pure enablement): CI schema-dispatch step unchanged and passing.
3. CR-BP-231 (documentation profile v3) consumes these fields; CR-BP-232 (HUM gates) validates their quality; CR-BP-233..236 author them. None of those CRs need further schema edits.
4. `check_cr_metadata.py --strict` green on this CR file.
