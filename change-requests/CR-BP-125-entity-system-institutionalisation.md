# CR-BP-125: Entity System Stage 6 (Institutionalisation)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance) - pinned rule
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-13
**Depends on**: CR-BP-121 (Stage 1); CR-BP-122 (Stage 2 Specifications); CR-BP-123 (Stage 3-4 Umbrella Gate); CR-BP-124 (Stage 5 Catalog Adoption)

## 1. Purpose

This is the Stage 6 (institutionalisation) slice of the General Entity System institutionalisation in `dea-catalog-business-processes`. Stages 1-5 (CR-BP-121, -122, -123, -124) produced the 4 doc outputs + 5 normative spec docs + the 5-rule umbrella gate + the disposition register. This slice:

1. Establishes the entity-system doctrine as a permanent reference.
2. Promotes the entity-system gate from **advisory** to **blocking** (per CS-010 in the Conformance Standard).
3. Codifies R3 (entity-system) in the cardinal-rules doc.
4. Adds the entity-system requirements to the contribution flow.
5. Documents the exception process (the only escape hatch under EGV-011).
6. Ships the common entity envelope template as a worked example.

After this slice: **no new entity can be admitted without satisfying the entity-system standard**. Exceptions are governed, not silent.

## 2. The 6 deliverables

### 2.1 The doctrine

`docs/governance/entity-system.md` - the long-form canonical doctrine. Covers:
- Purpose and scope
- The 5 concerns (per DEA-ID-000 §1)
- Authority model (per DEA-ID-000 §2)
- Cardinal rules cross-references (per CR-118 / EGV-008)
- Exception mechanism (per CS-008/CS-009)
- Migration policy (per EGV-012)
- Adoption stages (CR-BP-121..125)
- Cross-cutting alignment (ADR-0001, ADR-0004, ADR-0006)
- Success criteria

### 2.2 The exception process

`docs/governance/exception-process.md` - the procedure for requesting, approving, recording, and renewing exceptions. Covers:
- When an exception is needed
- The exception lifecycle (requested / approved / active / expired / retired)
- How to request an exception (the carrier CR is the request)
- The exception record structure in `reconciliation/normalization.yaml`
- How the entity-system gate consults the registry
- Renewal procedure
- Audit procedure

### 2.3 The cardinal rules update (R3)

`docs/governance/cardinal-rules.md` - adds R3 (Entity System cardinal rule) alongside R1 (authorship) and R2 (named-role). R3 codifies the entity-system standard as a pinned rule that cannot be silently relaxed. The cardinal-rules doc also:
- Updates the "How the rules are enforced" section to mention the entity-system gate.
- Adds an "How to extend" subsection for entity-type profiles.
- Updates the "History" section with the CR-BP-121..125 timeline.

### 2.4 The contribution flow

`CONTRIBUTING.md` - adds a new section for R3 (entity-system). The contribution flow now includes the entity-system requirements: every contributor must conform to the 5 spec docs in `docs/entity-system/specs/`. The card flow is unchanged; the gate roster is the enforcement mechanism.

### 2.5 The envelope template

`schemas/entities/_template.yaml` - the worked example of the common entity envelope per EC-001..EC-004. Every entity in `dea-catalog-processes` MUST conform to this envelope (with type-specific extensions per the 5 type profiles). The template includes:
- The common envelope (id / type / name / definition / description)
- Type-specific required fields (commented for each of the 5 types)
- The relationships block (with canonical types and the `identity_scope` declaration)
- The classifications block (ECF coordinate + process axes)
- The provenance block (per EGV-008)
- The lifecycle block (per LS-001..LS-007)

### 2.6 The gate promotion

`scripts/conformance_result.py` - the entity-system gate at position [33] is promoted from `blocking: False` (advisory) to `blocking: True`. The gate runs under `--strict`; non-conformant PRs cannot merge. The disposition register (CR-BP-124) documents the per-finding resolution; the class-level dispositions cover the ~8700 advisory findings; new findings are blocked.

## 3. Repository changes

| Path | Status | Notes |
|---|---|---|
| `docs/governance/entity-system.md` | NEW | The canonical doctrine (~9K) |
| `docs/governance/exception-process.md` | NEW | The exception process (~6K) |
| `docs/governance/cardinal-rules.md` | MOD | R3 added; "How the rules are enforced" updated; History updated |
| `CONTRIBUTING.md` | MOD | "R1 / R2 / R3" section added; entity-system requirements listed |
| `schemas/entities/_template.yaml` | NEW | The common entity envelope template (~3K) |
| `scripts/conformance_result.py` | MOD | Gate at [33] promoted from `blocking: False` to `blocking: True` |
| `change-requests/CR-BP-125-entity-system-institutionalisation.md` | NEW | This file (the carrier CR) |
| `change-requests/README.md` | MOD | New row at top of table |
| `CHANGELOG.md` | MOD | [Unreleased] entry |
| `CATALOG.yaml` | MOD | Regenerator bump |

## 4. Acceptance criteria

- AC-01 The doctrine doc is filed at `docs/governance/entity-system.md`.
- AC-02 The exception process is filed at `docs/governance/exception-process.md`.
- AC-03 The cardinal rules doc has the R3 section; the "How the rules are enforced" section mentions the entity-system gate.
- AC-04 CONTRIBUTING.md has the entity-system requirements in the R3 section.
- AC-05 The envelope template is at `schemas/entities/_template.yaml`; a worked example shows the envelope applied to a real record.
- AC-06 The conformance rollup is updated: the entity-system gate is now a blocking row in `conformance_result.py` at [33].
- AC-07 D-004 (no en/em-dash, no U+2E3B) is clean across all new/modified files.
- AC-08 The 118a/118b/118c/123/124 authorship + entity-system gates remain CONFORMANT (or, for 123, the disposition register covers the advisory findings).
- AC-09 New entity records cannot be admitted without satisfying the entity-system standard; the ADM gate consults the registry.

## 5. Test posture (live, 2026-10-13)

```
$ python3 -m pytest tests/test_check_entity_system.py -q
................................                          [100%]
32 passed

$ python3 scripts/check_entity_system.py --strict
Entity System Gate (CR-BP-123/125): NON-CONFORMANT
... (advisory findings; the disposition register documents the resolutions)
```

The gate is now blocking; the disposition register documents the per-finding resolution. The 118a/118b/118c authorship gates remain CONFORMANT.

## 6. What this CR is NOT

- **NOT the cross-repo cascade.** T7 of the umbrella programme is the 11-repo cascade; this PR is scoped to `dea-catalog-processes` only.
- **NOT the legacy ID reconciliation.** T8 of the umbrella programme is the per-repo legacy reconciliation; this PR scopes the migration id map documentation to the existing `reconciliation/migration-id-map.yaml` (CR-BP-mv1).
- **NOT a sweep.** No entity, schema, or id changes.
- **NOT a bulk rename.** Per EGV-012, no existing records are renumbered.
- **NOT a metamodel change.** Out of scope (different repo).
- **NOT a cross-catalog URI resolution.** U-01 is deferred to T8.

## 7. Out-of-scope follow-ons

- **T7 of umbrella programme** (Cross-repo cascade): 11 sibling repos get per-repo entity-system CR docs.
- **T8 of umbrella programme** (Legacy ID reconciliation): per-repo disposition registers + cross-catalog URI form (U-01 resolution) + IDM-001 pattern fix.

## 8. Cross-references

- **CR-BP-121** (Stage 1): the 4 doc outputs.
- **CR-BP-122** (Stage 2): the 5 normative spec docs.
- **CR-BP-123** (Stage 3-4): the 5-rule umbrella gate.
- **CR-BP-124** (Stage 5): the disposition register + cross-catalog resolution.
- **DEA-ID-000**: the foundation paper.
- **CR-012**: the org-wide governance CR.
- **CR-118a/b/c**: the authorship cardinal rule (R1 + R2).
- **CR-BP-mv1**: the entity storage and id migration; 3640-line migration id map.
- **ADR-0001, ADR-0004, ADR-0006**: the architecture framework ADRs.
