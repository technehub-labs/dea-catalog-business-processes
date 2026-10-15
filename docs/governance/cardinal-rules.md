# Cardinal Rules (CR-BP-118 / CR-BP-125)

Pinned governance rules that the conformance gate cannot silently relax.

## R1. Authorship-field cardinal rule (per CR-BP-118 / EGV-008)

Every authorship-bearing field in every artifact of every `technehub-labs/*`
repository must carry the value `Emmanuel A. Otchere` (or, for org-level
CITATION.cff entries, `TechNeHub Labs`). The string `Coder`, `Agent`,
`Hermes`, `Claude`, `GPT`, `Cline`, `OpenAI`, `MiniMax`, `MiniMax-M3`, or
any other agent/tool name is forbidden in any authorship-bearing field of
any published artifact.

**Authorship-bearing fields** (the registry at
`reconciliation/authorship-fields.yaml` is the canonical list):

- `**Owner**` in CR doc headers (`change-requests/CR-*.md`)
- `**Author**` in CR doc headers
- `audit.author` in entity record YAML (`entities/v1-alpha/**/processes-*.yaml`)
- `authors[].name`, `authors[].given-names`, `authors[].family-names` in
  `CITATION.cff`
- `name`, `definition`, `description`, `summary` content fields
  (per CR-BP-118c; the `Agent` allowlist covers the dea-catalog-processes
  domain vocabulary; word-boundary matching ensures the allowlist is precise)

The agent's role in producing the work is recorded in
`change-requests/CR-BP-NNN.md` per the CR governance chain. It is not a
named role in the published artifact.

## R2. Named-role file cardinal rule (per CR-BP-118)

Any file or field whose purpose is to name a person playing a named role
(commissioning authority, decision-maker, accountable owner, signatory,
copyright holder, etc.) -- including `NOTICE`, `LICENSE`, copyright
headers, `AUTHORS`, named-role fields in schemas, named-role fields in
contribution templates, `contributions/processes/*` contribution records
-- must carry `Emmanuel A. Otchere` (or, for the org, `TechNeHub Labs`).

The role of a tool or AI agent in producing the work is recorded in the
CR chain; it is not a named role in the published artifact.

## R3. Entity System cardinal rule (per CR-BP-121/122/123/124/125 / EGV-001..012)

Every governed entity in `dea-catalog-processes` (per the authority model
in `docs/governance/entity-system.md` §4) must conform to the General
Entity System per the 5 spec docs in `docs/entity-system/specs/`:

- **Identity Standard IS-001..IS-006**: the `processes:` namespace is
  canonical; the `dea:` family is grandfathered per EGV-012; cross-
  catalog references carry `identity_scope`.
- **Entity Contract Standard EC-001..EC-004**: the common envelope
  (id / type / name / definition / lifecycle / provenance) + 5 type-
  specific profiles.
- **Relationship Standard RS-001..RS-005**: 3 stored types
  (`composes` / `realizes` / `specializes`) + 1 forbidden
  (`part-of`); source / target type constraints; cross-catalog
  references.
- **Lifecycle Standard LS-001..LS-007**: 5-state machine
  (`proposed` / `admitted` / `deprecated` / `retired` / `superseded`);
  transition table; identity continuity; version-separation per
  EGV-007.
- **Conformance Standard CS-001..CS-011**: 5-rule umbrella gate
  (ES-001..ES-005); data-driven from
  `reconciliation/entity-system-registry.yaml`; exception mechanism
  (CS-008/CS-009) consults `reconciliation/normalization.yaml`;
  blocking in Stage 6 (per CS-010).

The exception mechanism (per `docs/governance/exception-process.md`) is
the only escape hatch under EGV-011. No bulk renames (per EGV-012): the
35 `dea:` legacy tails are grandfathered.

The entity-system gate at `scripts/check_entity_system.py` is the
enforcement mechanism. The gate is wired into `scripts/conformance_result.py`
at position [33] and into `.github/workflows/ci.yml` (the `Run Entity
System gate` step). The gate is **blocking** in Stage 6+ (per CR-BP-125).

## How the rules are enforced

`scripts/check_authorship.py` (gate [32] in the rollup, blocking) enforces
R1 mechanically. `scripts/check_prose_authorship.py` (gate between [32]
and [33], blocking under `--strict`) enforces R1 on the prose content
fields. `scripts/check_entity_system.py` (gate [33] in the rollup,
blocking in Stage 6+) enforces R3 mechanically.

## How to extend

Adding a new authorship-bearing field (a new `package.json author`
field, a new schema, a new contribution template) is a CR-level change:

1. Edit `reconciliation/authorship-fields.yaml` to add the new field's
   path, file glob, and kind.
2. Add a test to `tests/test_check_authorship.py` for the new field.
3. Land the change via PR; CI will block any merged authorship field
   that violates the rule.

Adding a new entity-type profile (e.g. a new specialization in
the metamodel) is a CR-level change:

1. Edit `reconciliation/entity-system-registry.yaml` to add the
   type's profile.
2. Add a per-type schema at `schemas/entities/<type>.schema.json`.
3. Add the type to the per-type gate list.
4. Add tests to `tests/test_check_entity_system.py`.
5. Land the change via PR; CI will enforce the new type's profile.

## History

- **CR-BP-118 (2026-10-13)**: rules R1 + R2 introduced; sweep across
  `dea-catalog-processes` brings 119 metadata hits into compliance; gate
  wired at position [32].
- **CR-BP-118b (deferred)**: extend the rule + sweep to the rest of the
  `technehub-labs/*` org.
- **CR-BP-118c (2026-10-13)**: prose-content migration; `Agent` allowlist
  for the dea-catalog-processes domain vocabulary; gate wired after [32].
- **CR-BP-121 (2026-10-13)**: rule R3 (entity-system) introduced as
  Stage 1 of the General Entity System institutionalisation.
- **CR-BP-122 (2026-10-13)**: Stage 2 (5 normative spec docs).
- **CR-BP-123 (2026-10-13)**: Stage 3-4 (5-rule umbrella gate, advisory
  in Stage 3-4 and Stage 5).
- **CR-BP-124 (2026-10-13)**: Stage 5 (disposition register + cross-
  catalog resolution; 35 `dea:` legacy tails grandfathered).
- **CR-BP-125 (2026-10-13)**: Stage 6 (institutionalisation; R3 rule
  codified; gate promoted to blocking; exception process documented).
