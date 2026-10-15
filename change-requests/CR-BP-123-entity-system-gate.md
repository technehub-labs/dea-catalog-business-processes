# CR-BP-123: Entity System Stage 3-4 (Reference Implementation + Umbrella Gate)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance) - pinned rule
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-13
**Depends on**: CR-BP-121 (Stage 1); CR-BP-122 (Stage 2 Specifications)
**Companion**: CR-BP-124 (Stage 5 Catalog Adoption); CR-BP-125 (Stage 6 Institutionalisation)

## 1. Purpose

This is the Stage 3-4 slice of the General Entity System institutionalisation in `dea-catalog-business-processes`. Stages 1+2 (CR-BP-121, CR-BP-122) produced the 4 doc outputs + 5 normative spec docs. This slice implements the 5-rule umbrella gate per the Conformance Standard (CR-BP-122 §5).

The umbrella gate has 5 rules, one per concern:

- **ES-001 (Identity)**: present, format-valid, scope-bound, unique id (per IS-001..IS-006 in the Identity Standard).
- **ES-002 (Entity Contract)**: common envelope + 5 type-specific profiles (per EC-001..EC-004 in the Entity Contract Standard).
- **ES-003 (Relationship)**: canonical types, source / target type constraints, cardinality, cross-catalog `identity_scope` (per RS-001..RS-005 in the Relationship Standard).
- **ES-004 (Lifecycle)**: governed state, transition table, identity continuity, terminal states, provenance per transition (per LS-001..LS-007 in the Lifecycle Standard).
- **ES-005 (Conformance Umbrella)**: per-type gate delegation (advisory in Stage 3-4; per-type gate verdicts are delegated to the per-type gates in the conformance rollup).

The gate is **advisory** under default mode and **blocking** under `--strict` (per CS-010 in the Conformance Standard). The staging is: advisory in Stage 3-4 (this PR) + Stage 5 (CR-BP-124); blocking in Stage 6 (CR-BP-125).

## 2. The 5 rules

### 2.1 ES-001 Identity

Validates the `id` field on every record. The canonical pattern is `^[a-z]+:[a-z]+(-[a-z]+){1,4}-[a-z2-9]{6}$` (the corrected IDM-001 pattern; covers all 5 type families: process- / pc- / group- / activity- / task- with 1-4 segments before the hash). The legacy `dea:` family is grandfathered per IS-004 + EGV-012.

**Note**: the existing IDM-001 pattern in `scripts/check_id_system.py` is `^[a-z]+:[a-z]+-[a-z]{2,3}-[a-z]+(-[a-z]+)*-[a-z2-9]{6}$` (requires the domain code to be 2-3 chars). This is too strict for BP records with long descriptors (e.g. `process-manage-customer-relationship` is 6 chars and doesn't match). The entity-system gate's pattern is the corrected form; the IDM-001 pattern fix is a follow-on in T7 / T8 of the umbrella programme.

### 2.2 ES-002 Entity Contract

Validates the common envelope + 5 type-specific profiles. The profile resolution:
- By `type` field (Process, ProcessGroup, Activity, Task, ProcessScope)
- For ProcessContext records: by `process_context` or `domain` field presence (covers both the new shape with `process_context` + `cell_charter` blocks and the legacy shape with top-level `domain` + `lifecycle_stage`)

The profiles declare the type-specific required fields + the lifecycle state machine fields. ProcessContext records use a slim profile (id + name); the other 5 types use the full envelope (id + type + name + definition + lifecycle + provenance).

### 2.3 ES-003 Relationship

Validates the `relationships[]` block on every record. The 3 stored types (`composes`, `realizes`, `specializes`) + the 1 forbidden type (`part-of`, derived inverse, view-time only). Source / target type constraints per relationship type. Cross-catalog references (e.g. `realizes` pointing at `dea-catalog-business-capabilities`) carry an `identity_scope` declaration.

### 2.4 ES-004 Lifecycle

Validates the lifecycle state machine + provenance per transition. Only applies to types with a `lifecycle_state_field` in their profile (Process, ProcessGroup, Activity, Task, ProcessScope). ProcessContext is exempt (lifecycle_status is the admission status, not a state-machine value). The 5 governed states: `proposed`, `admitted`, `deprecated`, `retired`, `superseded`. The `change_history[]` entries require `cr`, `date`, `change` keys.

### 2.5 ES-005 Conformance Umbrella

A global check (per gate invocation, not per record) that the per-type gate SCRIPT EXISTS for each registered type. The full per-type gate validation is delegated to the per-type gates in the conformance rollup; the entity-system gate is the umbrella, not the per-type validator.

## 3. The data-driven registry

The gate is data-driven from `reconciliation/entity-system-registry.yaml` (per CS-011 in the Conformance Standard). The registry declares:

- The envelope (file globs, type field, 6 type-specific profiles)
- The identity validation (id field, canonical prefix, canonical pattern, legacy prefix + pattern, legacy migration map)
- The relationship types (3 stored + 1 forbidden) + source/target type constraints + cross-catalog field
- The lifecycle state machine (5 valid states + 2 terminal states + transition table + provenance required keys)
- The per-type gate delegation (6 type-to-script mappings)
- The exception mechanism (registry path, verdict key, cr key, expiry key, reviewer key, excepted rules key)

Changing the gate's behavior is a YAML edit, not a code change.

## 4. The exception mechanism (the EGV-011 escape hatch)

The exception mechanism is the **review-retained verdict** in `reconciliation/normalization.yaml`. An exception is granted by:

1. The carrier CR explicitly requests the exception, citing the EGV-011 reason.
2. The user (eaojnr) approves the exception.
3. The exception is recorded with: `verdict: review-retained`; `cr` (the carrier CR); `reviewed_by`; `expiry` (ISO-8601); `excepted_rules: [...]` (the rules to exempt).
4. The entity-system gate consults the registry; a record carrying an exception is not blocking for the excepted rules.

A `excepted_rules: ['*']` exempts the record from all rules.

## 5. Repository changes

| Path | Status | Notes |
|---|---|---|
| `scripts/check_entity_system.py` | NEW | ~700 lines; 5 rules (ES-001..ES-005); --self-test (5 cases) + --strict + --json CLI; data-driven from the registry |
| `reconciliation/entity-system-registry.yaml` | NEW | The single source of truth for the gate's configuration; 6 type-specific profiles; corrected IDM-001 canonical pattern |
| `tests/test_check_entity_system.py` | NEW | 32 tests; CLI x4, registry x4, ES-001 x5, ES-002 x5, ES-003 x4, ES-004 x4, ES-005 x2, exception mechanism x2, live catalog x2 |
| `scripts/conformance_result.py` | MOD | New gate at [33] in the rollup; advisory (per CS-010) |
| `.github/workflows/ci.yml` | MOD | New "Run Entity System gate" step after the 118c prose step; both under --strict |
| `change-requests/CR-BP-123-entity-system-gate.md` | NEW | This file (the carrier CR) |
| `change-requests/README.md` | MOD | New row at top of table |
| `CHANGELOG.md` | MOD | [Unreleased] entry |
| `CATALOG.yaml` | MOD | Regenerator bump |

## 6. Acceptance criteria

- AC-01 The gate is data-driven from `reconciliation/entity-system-registry.yaml`; changing the gate's behavior is a YAML edit, not a code change.
- AC-02 The 5 rules (ES-001..ES-005) are individually testable; the live-catalog test asserts the gate runs without error on the current main.
- AC-03 The exception mechanism is consulted: a record carrying a review-retained verdict in `reconciliation/normalization.yaml` is not blocking for the excepted rules.
- AC-04 The gate runs under `--strict` in CI; non-conformant PRs cannot merge (advisory in Stage 3-4; the gate is added to the rollup at [33] as `blocking: False`).
- AC-05 The gate position in the rollup is documented in `scripts/conformance_result.py` and in this carrier CR.
- AC-06 D-004 (no en/em-dash, no U+2E3B) is clean across all new/modified files.
- AC-07 The 32-test suite passes on the current main.
- AC-08 The 118a/118b/118c authorship gates remain CONFORMANT (no overlap with this slice).
- AC-09 The walker skips config files (entity-system-registry.yaml, conformance_report.yaml, migration-id-map.yaml, the exceptions path) and tooling directories (.git, .github, scripts, tests, node_modules, __pycache__).
- AC-10 ProcessContext records (both new shape and legacy shape) are detected by the slim profile; ES-002 / ES-004 are exempt for them per the type-specific profile.

## 7. Test posture (live, 2026-10-13)

```
$ python3 -m pytest tests/test_check_entity_system.py -q
................................                          [100%]
32 passed in 70s

$ python3 scripts/check_entity_system.py --self-test
self-test PASS (5 cases)

$ python3 scripts/check_entity_system.py --strict
Entity System Gate (CR-BP-123): NON-CONFORMANT
[ES-002] ... (live tree findings; advisory)
...
```

The live tree has ~8700+ findings (mostly ES-002 / ES-003 issues on records that don't have the full envelope or that have non-canonical relationship types). These are real shape issues that the disposition register (CR-BP-124, Stage 5) will document and resolve.

## 8. What this CR is NOT

- **NOT blocking.** The gate is advisory in Stage 3-4; the disposition register (Stage 5) files the per-record disposition for every finding. The gate becomes blocking in Stage 6 (CR-BP-125) when the catalog is conformant under the disposition register.
- **NOT the disposition register.** Ships as CR-BP-124 (Stage 5).
- **NOT the institutionalisation.** Ships as CR-BP-125 (Stage 6).
- **NOT a sweep.** No entity, schema, or id changes.
- **NOT a bulk rename.** Per EGV-012, no existing records are renumbered.
- **NOT a metamodel change.** Out of scope (different repo).
- **NOT a cross-catalog URI resolution.** U-01 is deferred to T8.

## 9. Out-of-scope follow-ons

- **CR-BP-124** (Stage 5): the disposition register + migration id map + cross-catalog resolution.
- **CR-BP-125** (Stage 6): the doctrine doc + cardinal-rules update + CONTRIBUTING + envelope template + exception process. Promotes the gate from advisory to blocking.
- **T7 of umbrella programme** (Cross-repo cascade): 11 sibling repos get per-repo entity-system CR docs. The 118b cascade pattern.
- **T8 of umbrella programme** (Legacy ID reconciliation): per-repo disposition registers + cross-catalog URI form (U-01 resolution) + the IDM-001 pattern fix.
- **IDM-001 pattern fix**: the existing `scripts/check_id_system.py` has the old (broken) pattern. The entity-system gate's corrected pattern is documented in this CR; the IDM-001 fix is a follow-on.

## 10. Cross-references

- **CR-BP-121** (Stage 1): the 4 doc outputs (Charter, Gap Register, Normative Design Proposal, Implementation Plan).
- **CR-BP-122** (Stage 2): the 5 normative spec docs in `docs/entity-system/specs/`.
- **DEA-ID-000**: `dea-governance/docs/design/entity-system-foundation.md` (the foundation paper).
- **CR-012**: `dea-governance/change-requests/CR-012-org-wide-entity-governance.md` (the org-wide governance CR; 12 EGV-001..012).
- **CR-BP-118a/b/c**: the authorship cardinal rule (cross-references for EGV-008).
- **CR-BP-mv1**: IDM-001..007; the IDM-001 pattern fix is a follow-on.
- **The 118b cascade pattern**: data-driven gate + per-repo registry + per-repo workflow.
