# CR-BP-122: Entity System Stage 2 (Specifications)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance) - pinned rule
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-13
**Depends on**: CR-BP-121 (Stage 1; the 4 doc outputs); DEA-ID-000 (foundation paper, `dea-governance`); CR-012 (org-wide governance CR, `dea-governance`)
**Companion**: CR-BP-123 (Stage 3-4 Reference Implementation); CR-BP-124 (Stage 5 Catalog Adoption); CR-BP-125 (Stage 6 Institutionalisation)

## 1. Purpose

This is the Stage 2 slice of the General Entity System institutionalisation in `dea-catalog-business-processes`. Stage 1 (CR-BP-121) produced the 4 doc outputs (Charter, Existing Decisions and Gap Register, Normative Design Proposal, Implementation Plan); this slice codifies the 9 N-classification decisions + the 7 U-classification open questions into 5 normative spec docs.

The 5 specs (in `docs/entity-system/specs/`):

1. **Identity Standard** (`01-identity-standard.md`) - codifies the 6 normative rules for entity identity (IS-001..IS-006); the `processes:` namespace discipline; the legacy `dea:` grandfathering per IS-004; the cross-catalog reference resolution (deferred to T8) per IS-006.
2. **Entity Contract Standard** (`02-entity-contract-standard.md`) - codifies the 4 normative rules for the entity contract (EC-001..EC-004); the common envelope + 5 type-specific profiles; the extension rules; the metamodel reconciliation.
3. **Relationship Standard** (`03-relationship-standard.md`) - codifies the 5 normative rules for entity relationships (RS-001..RS-005); the 4 canonical relationship types (`composes`, `realizes`, `specializes`, `part-of` derived); the source / target type constraints; the cardinality rules; the cross-catalog reference resolution.
4. **Lifecycle Standard** (`04-lifecycle-standard.md`) - codifies the 7 normative rules for entity lifecycle (LS-001..LS-007); the 5-state machine (`proposed` / `admitted` / `deprecated` / `retired` / `superseded`); the transition table; the identity continuity; the version-separation discipline per EGV-007.
5. **Conformance Standard** (`05-conformance-standard.md`) - codifies the 11 normative rules for the conformance discipline (CS-001..CS-011); the 5-rule umbrella gate (ES-001..ES-005); the rollup integration; the CI enforcement; the exception mechanism (the EGV-011 escape hatch); the advisory-then-blocking staging.

This slice is **design-only**: 0 entity changes, 0 schema changes, 0 bulk renames. Stage 3-4 (CR-BP-123) implements the umbrella gate; Stage 5 (CR-BP-124) files the disposition register; Stage 6 (CR-BP-125) institutionalises the standard.

## 2. Scope

### 2.1 In scope (this PR)

- The 5 spec docs in `docs/entity-system/specs/`.
- The carrier CR (this file).
- `change-requests/README.md` row (new entry).
- `CHANGELOG.md` entry.
- `CATALOG.yaml` regeneration.

### 2.2 Out of scope (this PR)

- The umbrella gate `scripts/check_entity_system.py` (Stage 3-4, CR-BP-123).
- The disposition register (Stage 5, CR-BP-124).
- The institutionalisation (Stage 6, CR-BP-125).
- The cross-repo cascade (T7 of the umbrella programme).
- The legacy id reconciliation (T8 of the umbrella programme).

## 3. Resolutions from the Gap Register

The Stage 1 Gap Register identified 9 N-classification decisions (needing framing) and 7 U-classification open questions. This Stage 2 slice resolves them in the 5 specs:

### 3.1 N-classification decisions (Stage 2 codification)

| N-id | Decision | Spec location | Resolution |
|---|---|---|---|
| G-01 | Identity Standard | `01-identity-standard.md` | IS-001 (canonical format), IS-002 (namespace ownership), IS-003 (identity continuity), IS-004 (legacy id handling), IS-005 (split/merge/supersession) |
| G-02 | Entity Contract Standard | `02-entity-contract-standard.md` | EC-001 (common envelope), EC-002 (type-specific profiles), EC-003 (extension rules), EC-004 (metamodel reconciliation) |
| G-03 | Relationship Standard | `03-relationship-standard.md` | RS-001 (typed-relationship vocabulary), RS-002 (source / target type constraints), RS-003 (cardinality), RS-005 (no competing definitions) |
| G-04 | Lifecycle Standard | `04-lifecycle-standard.md` | LS-001 (states), LS-002 (transitions), LS-003 (identity continuity), LS-004 (terminal states), LS-005 (provenance per transition), LS-006 (version-separation), LS-007 (revision vs identity) |
| G-05 | Conformance Standard | `05-conformance-standard.md` | CS-001..CS-005 (the 5-rule umbrella gate), CS-006 (rollup position), CS-007 (CI enforcement), CS-011 (data-driven registry) |
| G-06 | Cross-catalog reference standard | `01-identity-standard.md` IS-006 + `03-relationship-standard.md` RS-004 | `identity_scope` declaration; the URI form is deferred to T8 (per the U-01 disposition) |
| G-07 | Legacy ID reconciliation | `01-identity-standard.md` IS-004 | `reconciliation/migration-id-map.yaml`; the 35 `dea:` legacy tails are grandfathered |

### 3.2 U-classification open questions (Stage 2 dispositions)

| U-id | Question | Spec location | Disposition |
|---|---|---|---|
| U-01 | Cross-catalog URI form | `01-identity-standard.md` IS-006 + `03-relationship-standard.md` RS-004 | **Deferred to T8** (Legacy ID reconciliation); today's references use target id + scope; URL-based URIs are a future enhancement |
| U-02 | Lifecycle state machine | `04-lifecycle-standard.md` LS-001..LS-005 | **Resolved**: 5 states (`proposed` / `admitted` / `deprecated` / `retired` / `superseded`); transition table LS-002 |
| U-03 | `provenance` vs `change_history` | `02-entity-contract-standard.md` EC-001 (envelope) + `04-lifecycle-standard.md` LS-005 | **Resolved**: `provenance` is the parent block; `change_history[]` is the per-transition list within `provenance` |
| U-04 | Advisory vs blocking for the umbrella gate | `05-conformance-standard.md` CS-010 | **Resolved**: advisory in Stage 3-4 + Stage 5; blocking in Stage 6 (per the user's DP-7) |
| U-05 | Interaction with the conformance rollup | `05-conformance-standard.md` CS-006 | **Resolved**: single rollup row; the umbrella semantics are inside the gate; one CI step |
| U-06 | Exception mechanism | `05-conformance-standard.md` CS-008..CS-009 | **Resolved**: review-retained verdict in `reconciliation/normalization.yaml` (per the CR-BP-25 precedent) |
| U-07 | OpenDEAM authority chain alignment | `docs/entity-system/00-charter.md` §3 (authority model) + `docs/entity-system/01-existing-decisions-and-gap-register.md` §7 (U-07) | **Resolved**: the 12 EGV-001..012 are ratified under the new `dea-governance` repo's authority track (per CR-012); the alignment with CR-001..008 (OpenDEA 1.0.0) is a Stage 5 / T7 cross-reference (the architecture framework's ADRs are the architectural authority; the governance repo is the identity/lifecycle/conformance authority) |

## 4. The 5 specs at a glance

### 4.1 Identity Standard (IS-001..IS-006)

- IS-001 (canonical format): the `processes:<token>-<descriptor>-<base32hash>` format is the canonical identity.
- IS-002 (namespace ownership): the `processes:` namespace is owned by this catalog; cross-namespace references carry `identity_scope`.
- IS-003 (identity continuity): mutable attribute changes don't change identity; the hash-suffix is stable.
- IS-004 (legacy id handling): the 35 `dea:` legacy tails are grandfathered per EGV-012.
- IS-005 (split/merge/supersession): explicit transitions; no silent reassignment.
- IS-006 (cross-catalog references): `identity_scope` declaration; URI form deferred to T8.

### 4.2 Entity Contract Standard (EC-001..EC-004)

- EC-001 (common envelope): the 9 envelope fields (id, type, name, definition, description, relationships, classifications, provenance, lifecycle).
- EC-002 (type-specific profiles): the 5 entity types (Process, ProcessContext, ProcessGroup, Activity, Task) + the 6th (ProcessScope, dormant-by-design).
- EC-003 (extension rules): a new type is added by authoring a per-type schema + metamodel registration + per-type gate + carrier CR.
- EC-004 (metamodel reconciliation): the catalog's profiles extend the metamodel's entity-type definitions; no redefinition.

### 4.3 Relationship Standard (RS-001..RS-005)

- RS-001 (typed-relationship vocabulary): the 3 stored types (`composes`, `realizes`, `specializes`); the derived inverse (`part-of`) is view-time only.
- RS-002 (source / target type constraints): per-type constraints declared in the spec.
- RS-003 (cardinality): per-type cardinality rules.
- RS-004 (cross-catalog references): `identity_scope` declaration; URI form deferred.
- RS-005 (no competing definitions): a new type requires an amendment to this spec.

### 4.4 Lifecycle Standard (LS-001..LS-007)

- LS-001 (states): the 5 governed states.
- LS-002 (transitions): the per-state transition table.
- LS-003 (identity continuity): transitions don't change id (with the `superseded` exception for successor introduction).
- LS-004 (terminal states): `superseded` and `retired` are terminal.
- LS-005 (provenance per transition): every transition adds a `change_history[]` entry.
- LS-006 (version-separation): the 4 distinct concepts (entity identity / entity revision / schema version / catalog release).
- LS-007 (revision vs identity): an in-place update is a revision; a state change is a transition.

### 4.5 Conformance Standard (CS-001..CS-011)

- CS-001 (ES-001 Identity): present, format-valid, scope-bound, unique id.
- CS-002 (ES-002 Entity Contract): common envelope + type-specific profiles.
- CS-003 (ES-003 Relationship): canonical types, source / target constraints, cardinality, cross-catalog.
- CS-004 (ES-004 Lifecycle): governed state, transition table, identity continuity, terminal states, provenance per transition.
- CS-005 (ES-005 Conformance Umbrella): the per-type gates are CONFORMANT.
- CS-006 (rollup position): single rollup row; the next free number when CR-BP-123 lands.
- CS-007 (CI enforcement): `--strict` in CI; non-conformant PRs cannot merge.
- CS-008 (exception mechanism): the review-retained verdict in `reconciliation/normalization.yaml`.
- CS-009 (exception lifecycle): granted / active / expired / renewed / retired.
- CS-010 (advisory-then-blocking staging): advisory in Stage 3-4 + Stage 5; blocking in Stage 6.
- CS-011 (data-driven registry): `reconciliation/entity-system-registry.yaml` is the gate's configuration source.

## 5. Repository changes

| Path | Status | Notes |
|---|---|---|
| `docs/entity-system/specs/01-identity-standard.md` | NEW | ~10K; IS-001..IS-006 |
| `docs/entity-system/specs/02-entity-contract-standard.md` | NEW | ~11K; EC-001..EC-004 |
| `docs/entity-system/specs/03-relationship-standard.md` | NEW | ~11K; RS-001..RS-005 + 4 RT-001..RT-004 type definitions |
| `docs/entity-system/specs/04-lifecycle-standard.md` | NEW | ~12K; LS-001..LS-007 + 5-state machine + transition table |
| `docs/entity-system/specs/05-conformance-standard.md` | NEW | ~10K; CS-001..CS-011 + exception mechanism |
| `change-requests/CR-BP-122-entity-system-specifications.md` | NEW | This file (the carrier CR) |
| `change-requests/README.md` | MOD | New row at top of table |
| `CHANGELOG.md` | MOD | [Unreleased] entry |
| `CATALOG.yaml` | MOD | Regenerator bump |

## 6. Acceptance criteria

- AC-01 The 5 spec docs are filed under `docs/entity-system/specs/`.
- AC-02 Each spec is normative: every rule is machine-verifiable or has an explicit "informational" annotation.
- AC-03 The 9 N-classification decisions in the Gap Register each have a normative rule in the corresponding spec.
- AC-04 The 7 U-classification open questions each have a disposition (codified, deferred, or out-of-scope) in the carrier CR.
- AC-05 The exception mechanism is codified as a normative spec (CS-008, CS-009).
- AC-06 The identity-scope declaration for cross-catalog references is documented (IS-006 + RS-004).
- AC-07 The lifecycle state machine is documented with per-transition rules and a worked example (LS-001..LS-005 + the §4 worked example).
- AC-08 The version-separation discipline is documented (LS-006, LS-007).
- AC-09 D-004 (no en/em-dash, no U+2E3B) is clean across all new/modified files.
- AC-10 118a/118b/118c authorship gates remain CONFORMANT (no overlap with this slice).
- AC-11 No entity, schema, or id changes (the slice is design-only).

## 7. Test posture (live, 2026-10-13)

```
$ python3 scripts/check_authorship.py --strict
Authorship Cardinal Rule (CR-BP-118; AUT-001..003): CONFORMANT
  AUT-001 hits: 0
  AUT-002 hits: 0
  AUT-003 hits: 0

$ python3 scripts/check_prose_authorship.py --strict
PROSE Authorship Gate: CONFORMANT
$ echo $?
0

$ python3 scripts/regenerate_catalog.py --schema ... --check
OK: /home/hermes/dea-catalog-processes/CATALOG.yaml is current
```

The 118a/118b/118c authorship gates remain CONFORMANT (no overlap with this slice).

## 8. What this CR is NOT

- **NOT the umbrella gate.** The 5-rule gate ships as CR-BP-123 (Stage 3-4).
- **NOT the disposition register.** Ships as CR-BP-124 (Stage 5).
- **NOT the institutionalisation.** Ships as CR-BP-125 (Stage 6).
- **NOT a sweep.** No entity, schema, or id changes (the slice is design-only).
- **NOT a bulk rename.** Per EGV-012, no existing records are renumbered.
- **NOT a metamodel change.** Out of scope (different repo).
- **NOT a cross-catalog URI resolution.** U-01 is deferred to T8.

## 9. Out-of-scope follow-ons

- **CR-BP-123** (Stage 3-4 Reference Implementation): the umbrella gate + tests + workflow + rollup integration.
- **CR-BP-124** (Stage 5 Catalog Adoption): the disposition register + migration id map + cross-catalog resolution.
- **CR-BP-125** (Stage 6 Institutionalisation): the doctrine doc + cardinal-rules update + CONTRIBUTING + envelope template + exception process.
- **T7 of umbrella programme** (Cross-repo cascade): 11 sibling repos get per-repo entity-system CR docs.
- **T8 of umbrella programme** (Legacy ID reconciliation): per-repo disposition registers + cross-catalog URI form (U-01 resolution).

## 10. Cross-references

- **CR-BP-121** (Stage 1): the 4 doc outputs (Charter, Gap Register, Normative Design Proposal, Implementation Plan).
- **DEA-ID-000**: `dea-governance/docs/design/entity-system-foundation.md` (the foundation paper).
- **CR-012**: `dea-governance/change-requests/CR-012-org-wide-entity-governance.md` (the org-wide governance CR; 12 EGV-001..012).
- **The 118a/118b/118c authorship cardinal rule**: `change-requests/CR-BP-118-authorship-cardinal-rule.md` + the 11-repo cascade.
- **The dea-metamodel cross-reference**: `dea-metamodel` is the source-of-truth for entity-type definitions (per EGV-001).
