# CR-BP-94-EXT-01: Process Documentation Architecture

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Proposed
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-18
**Parent**: CR-BP-94 (Decomposition Record Templates, PR #134)
**Source**: `change-requests/inbox/CR-BP-94-EXT-01.md` (user-authored attachment)
**Recon programme parents**: CR-BP-92 (Process Catalog layer), CR-BP-93 (decomposition semantic contract).
**Sub-pipeline**: CR-BP-94-EXT-01 (this slice) + EXT-02..06.
**Lands against**: 139 canonical BP records; 553 Activity records; 20 conformance gates CONFORMANT; v0.4.0 tagged; v0.4.0+7 commits on main.

---

## 1. Change Request

Establish the **Canonical Process Documentation Architecture** for the DEA Process Catalog. The architecture is profile-driven, model-aligned, and lifecycle-aware. It lands in phased implementation slices:

| Sub-CR | Title | Scope | Status |
|---|---|---|---|
| **CR-BP-94-EXT-01 (this slice)** | Documentation Architecture | Architecture doc + 3 profile templates + DOC-001..005 + pilot scaffold | Proposed (PR pending) |
| CR-BP-94-EXT-02 | README Profile & Template Standard | Markdown templates with section identifiers + profile-specific extensions + versioning | Reserved |
| CR-BP-94-EXT-03 | Documentation Manifest & Coverage Model | Machine-readable manifest schema + coverage scoring + lifecycle rules | Reserved |
| CR-BP-94-EXT-04 | Generation & Validation Pipeline | Profile-aware generator + structural validator + CI integration | Reserved |
| CR-BP-94-EXT-05 | Decomposition Reconciliation | Parent-child traceability + catalog-wide coverage report | Reserved |
| CR-BP-94-EXT-06 | Pilot & Catalog Rollout | Pilot completion + catalog-wide rollout | Reserved |

### 1.1 What this slice (EXT-01) lands

1. **Architecture specification** at `docs/process-documentation-architecture.md` (~520 lines, 14 sections). Establishes:
   - Three-layer model (Entity / Documentation / Validation).
   - REQ-01 (Canonical Documentation Contract): required metadata, semantic sections, conditional sections, inherited content rules, evidence requirements.
   - REQ-02 (Decomposition-Aware Documentation Profiles): profile registry design.
   - REQ-03 (Canonical README Template): section identifier + ordering standard.
   - **Critical design decision**: do not conflate entity type with decomposition level.
   - Documentation lifecycle states (not-started → published → superseded).
   - Six-dimension coverage model stub.
   - Lifecycle-specific obligations (REQ-09).
   - Extension CR roadmap.

2. **Three documentation profile templates** under `templates/`:
   - `documentation-profile-l2.yaml` (L2 Business Process)
   - `documentation-profile-l3-activity.yaml` (L3 Activity)
   - `documentation-profile-l4-task.yaml` (L4 Task)

   Each profile is a machine-readable contract that specifies required sections, conditional sections, evidence requirements, and lifecycle obligations for the corresponding `(type, level)` classification.

3. **Structural validator** at `scripts/check_documentation_profile.py` (~390 lines, DOC-001..005):
   - DOC-001: README exists at the prescribed location.
   - DOC-002: README has the section identifiers mandated by the resolved profile.
   - DOC-003: README entity id matches the YAML `id` field.
   - DOC-004: Generated sections contain no unresolved `{{placeholder}}` tokens at `validated` lifecycle state.
   - DOC-005: README references the governing CR.

4. **Gate wire** as gate [21] Documentation Profile (advisory) in `scripts/conformance_result.py`. The gate emits advisory findings; it does NOT block merge until a sufficient population of README assets has been authored (EXT-06).

5. **Pilot scaffold** at `entities/v1-alpha/dea:process-customer-insight-and-retention/documentation/manifest.yaml`. The pilot demonstrates the L2 profile machinery against a real BP record. The manifest carries the ECF conformance block per CR-BP-31 (inherits the parent BP's ECF alignment).

6. **29 new tests** in `tests/test_check_documentation_profile.py` covering the validator, the profile registry, the helpers, the CLI shape, and the advisory-tagging invariant.

### 1.2 What this slice does NOT land

- **NOT a generator.** The README generator lands in EXT-04.
- **NOT a manifest schema.** The full machine-readable manifest schema lands in EXT-03.
- **NOT a catalog-wide rollout.** The pilot is structural validation only; catalog-wide coverage is EXT-06.
- **NOT a re-opening of CR-BP-93.** The decomposition semantic contract is the source of truth for level mapping.
- **NOT a count-assertion change.** The new manifest record is a documentation asset of an existing entity; no new entity-level records are introduced.
- **NOT a tightening of specialization validation.** Held under CR-BP-92 §21.

## 2. Deposition mechanics (pattern per CR-BP-92 §16)

1. **Documentation architecture is normative prose** (`docs/process-documentation-architecture.md`), not a script. The architecture establishes the contract; subsequent slices implement it.
2. **Profile templates are machine-readable** (YAML). The validator's `PROFILE_REGISTRY` is an in-process copy of the registered profiles; EXT-03 will codify the registry as a runtime-mutable schema.
3. **Validator is advisory** (gate [21]). Per CR-BP-95 / CR-BP-96 / CR-BP-97 back-compat pattern, the gate surfaces findings for transparency but does not block merge.
4. **Pilot manifest carries the ECF conformance block** per CR-BP-31. The manifest inherits the parent BP's alignment; the conformance gate (gate [8]) validates the manifest alongside all other entity records.
5. **No schema, gate wire, or canonical-entity mutation.** The new `documentation/` directory is per-entity; the existing `entities/v1-alpha/dea:process-customer-insight-and-retention/dea:process-customer-insight-and-retention.yaml` is untouched.
6. **Reconciliation artifacts.** `baseline/v1.yaml` and `conformance_report.yaml` regenerate with the new manifest record (788 → 789 records).

## 3. Gate posture

- Gate [21] Documentation Profile (DOC-001..005): **CONFORMANT** (PASS/ADVISORY).
- 1,956 advisory findings surfaced for transparency: 596 DOC-001 (no README), 1,343 DOC-002 (sections missing), 2 DOC-003 (id mismatch), 15 DOC-005 (CR ref missing), 0 DOC-004.
- Full suite: **21 gates, 0 blocking, 0 advisory** (0 advisory failures in the conformance summary; gate [21] is wired as advisory and reports its own state).
- CR-META: **0 new findings** (CR-BP-94-EXT-01 contributes 0 new findings).

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `docs/process-documentation-architecture.md` | NEW | Architecture specification (~520 lines, 14 sections) |
| `templates/documentation-profile-l2.yaml` | NEW | L2 Business Process documentation profile |
| `templates/documentation-profile-l3-activity.yaml` | NEW | L3 Activity documentation profile |
| `templates/documentation-profile-l4-task.yaml` | NEW | L4 Task documentation profile |
| `scripts/check_documentation_profile.py` | NEW | DOC-001..005 structural validator (~390 lines) |
| `scripts/conformance_result.py` | MOD | + gate [21] Documentation Profile (advisory) |
| `entities/v1-alpha/dea:process-customer-insight-and-retention/documentation/manifest.yaml` | NEW | Pilot scaffold; carries ECF conformance block per CR-BP-31 |
| `tests/test_check_documentation_profile.py` | NEW | 29 tests (profile registry + helpers + DOC-001..005 + CLI shape + advisory tagging) |
| `change-requests/CR-BP-94-EXT-01-documentation-architecture.md` | NEW | Slice carrier CR (this document) |
| `change-requests/inbox/CR-BP-94-EXT-01.md` | NEW | User-authored attachment (saved) |
| `change-requests/README.md` | MOD | CR-BP-94-EXT-01 row added before `## Cross-repo context` |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 107 → 108 |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated (no entity-level changes; +1 manifest record) |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated (788 → 789 records; +1 documentation manifest) |

No canonical-entity mutation. No schema change to the entity model. No gate wire change to existing gates.

## 5. Acceptance criteria

1. `docs/process-documentation-architecture.md` is published and references CR-BP-92/93/94/95/96/97 as upstream dependencies.
2. Three documentation profile templates exist under `templates/`: `documentation-profile-l2.yaml`, `documentation-profile-l3-activity.yaml`, `documentation-profile-l4-task.yaml`.
3. `scripts/check_documentation_profile.py` implements DOC-001..005; self-test passes; live catalog emits advisory findings (advisory, non-blocking).
4. Gate [21] Documentation Profile is wired as **advisory** in `scripts/conformance_result.py`; the suite remains CONFORMANT (0 blocking, 0 advisory failures).
5. `entities/v1-alpha/dea:process-customer-insight-and-retention/documentation/manifest.yaml` exists as the pilot scaffold; the ECF conformance block is present and validates against gate [8].
6. `tests/test_check_documentation_profile.py` reports 29 tests pass.
7. CR-BP-94-EXT-01 carrier CR is filed in `change-requests/`.
8. README row + CATALOG regen is committed.
9. Em-dash / en-dash audit: 0 violations in new prose.
10. Full pytest suite passes (pre-existing `test_dispositions::test_tranche_count_is_ten` failure unchanged; NOT introduced by this slice).

## 6. Result

CR-BP-94-EXT-01 establishes the canonical Process Documentation Architecture and lands the first slice (architecture + 3 profile templates + DOC-001..005 validator + pilot scaffold + 29 tests). The 21-gate suite remains CONFORMANT (0 blocking, 0 advisory failures). The 1,956 advisory DOC-001..005 findings are surfaced for transparency; remediation (populating READMEs per the profile machinery) is the work of EXT-02..06. `open_change_requests` 107 → 108. EXT-02..06 are reserved as the follow-on sub-pipeline.
