# CR-BP-94-EXT-01a: L0/L1 Cardinal Entity Documentation Profiles

**Status**: Proposed
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-18
**Parent**: CR-BP-94-EXT-01 (Process Documentation Architecture, PR #137, merged at `35a0a838`)
**Sub-pipeline**: EXT-01a (this slice) + EXT-02..06.
**Lands against**: 740 entities / 741 conformance records / 21 gates CONFORMANT / v0.4.0 tagged.

---

## 1. Change Request

Reopen **CR-BP-94-EXT-01** (PR #137) to add the L0 (ProcessContext) and L1 (ProcessGroup) documentation profiles that the original slice omitted. The omission was flagged by the user as a substantive gap: cardinal entities per CR-BP-92 §7 and CR-BP-93 §3 must have documentation profiles; treating them as deferred creates the wrong precedent that L0/L1 are less important than L2/L3/L4.

### 1.1 What this slice lands

1. **L0 ProcessContext profile** at `templates/documentation-profile-l0-process-context.yaml` (NEW, ~140 lines):
   - Profile ID: `dea:profile-readme-l0-process-context-v1`
   - Required sections: 11 (entity-identity, formal-definition, semantic-dimensions, decomposition, behavior, interfaces, roles, rules-controls, evidence, completeness, revision-history)
   - Conditional sections: outcomes, business-rules, workflow-visualization
   - Not applicable: execution-steps (L0 has no execution semantics)

2. **L1 ProcessGroup profile** at `templates/documentation-profile-l1-process-group.yaml` (NEW, ~140 lines):
   - Profile ID: `dea:profile-readme-l1-process-group-v1`
   - Required sections: 11 (same as L0; outcomes conditional at L1)
   - Conditional sections: outcomes, workflow-visualization
   - Not applicable: execution-steps
   - Acknowledges CR-BP-95 PG-009 (`grouping_basis`) and PG-010 (`membership_criteria`): when those fields are present in the YAML, the corresponding `decomposition` subsections are required; otherwise conditional.

3. **Validator profile registry extension** in `scripts/check_documentation_profile.py`:
   - `PROFILE_REGISTRY` adds 2 entries: (`ProcessContext`, `L0`) and (`ProcessGroup`, `L1`).
   - `LEVEL_BY_TYPE` adds 2 entries: `ProcessContext -> L0` and `ProcessGroup -> L1`.
   - Back-compat invariant: L2/L3/L4 entries unchanged.

4. **4 new tests** in `tests/test_check_documentation_profile.py`:
   - `test_profile_registry_has_five_entries` (was: three)
   - `test_l0_profile_resolves_for_processcontext_record`
   - `test_l1_profile_resolves_for_processgroup_record`
   - `test_l0_profile_required_sections`
   - `test_l1_profile_required_sections`
   - Plus: `test_resolve_level_by_type` updated to cover L0/L1.

5. **Architecture doc update** in `docs/process-documentation-architecture.md`:
   - §12 Extension CR roadmap: EXT-01 status updated to "Merged"; EXT-01a added.
   - §13 Cardinal entities: L0 (ProcessContext) and L1 (ProcessGroup) added with constraints + L1 pilot decision rationale.
   - §14 Acceptance criteria: profile count updated from 3 to 5.

### 1.2 What this slice does NOT land

- **NOT an L1 pilot manifest record.** The L1 pilot on `dea:group-customer-insight-and-retention` was attempted but rejected due to schema constraints:
  - The L1 PG schema (`schemas/entities/process-group.schema.json`) declares `additionalProperties: false` and requires 12 fields including `composes` (non-empty array per PG-002).
  - The `composes` relationship_type is constrained to the literal `'composes'` (per the schema const).
  - The parent record already composes `dea:process-customer-insight-and-retention`; the manifest's `composes` entry would either duplicate (failing PG-006 MECE) or be empty (failing PG-002).
  - EXT-06 (pilot + catalog rollout) lands the L0/L1 pilot using a **sibling-file pattern**: manifest stays minimal + valid; documentation profile content lives in `docs/manifests/<id>-profile.yaml` referenced via `links:`.
- **NOT a CR-BP-31 ECF affiliation schema change.** The L1 manifest inherits the parent record's ECF conformance block (`affiliation: inherits-catalog`).
- **NOT a count-assertion change.** No new canonical-entity records are introduced. The profile machinery now recognizes L0/L1; that's it.
- **NOT a tightening of specialization validation.** Held under CR-BP-92 §21.

## 2. Deposition mechanics (pattern per CR-BP-92 §16)

1. **Profile templates are machine-readable** (YAML). The validator's `PROFILE_REGISTRY` is an in-process copy of the registered profiles; EXT-03 codifies the registry as a runtime-mutable schema.
2. **Validator is advisory** (gate [21]). Per CR-BP-95 / CR-BP-96 / CR-BP-97 back-compat pattern, the gate surfaces findings for transparency but does not block merge.
3. **No schema, gate wire, or canonical-entity mutation.** The existing entity records are untouched.
4. **No count-assertion change.** `open_change_requests` 108 → 109.

## 3. Cardinal-entity doctrine (CR-BP-92 §7 + CR-BP-93 §3)

L0 ProcessContexts and L1 ProcessGroups are **cardinal entities**: catalog-owned types that pre-exist the L2 Business Process. Their documentation is structurally distinct from L2/L3/L4 and cannot be folded into those profiles.

Lifecycle constraints (lifted into the architecture doc §13):
- L0 ProcessContexts: candidate -> active -> reorganized. NOT deprecated or retired.
- L1 ProcessGroups: candidate -> active -> reorganized. NOT deprecated or retired.
- The `reorganized` lifecycle state is the cardinal-entity analogue of `deprecated`/`retired` for ordinary entities; it lands in EXT-04.

## 4. Gate posture

- Gate [21] Documentation Profile (DOC-001..005): **CONFORMANT** (PASS/ADVISORY).
- Live catalog emits **2,306 advisory findings** (was 1,956 in EXT-01; +350 from the L1 PG records now correctly resolved to a profile). DOC-001: 596. DOC-002: 1,693 (was 1,343). DOC-004: 0. DOC-005: 15.
- Full suite: **21 gates, 0 blocking, 0 advisory** failures.
- CR-META: 0 new findings (CR-BP-94-EXT-01a contributes 0 new findings; CR_NUMBER_PATTERN extension in EXT-01 already covers the EXT-01a suffix).

## 5. Repository changes

| Path | Status | Notes |
|---|---|---|
| `templates/documentation-profile-l0-process-context.yaml` | NEW | L0 ProcessContext profile (~140 lines) |
| `templates/documentation-profile-l1-process-group.yaml` | NEW | L1 ProcessGroup profile (~140 lines) |
| `scripts/check_documentation_profile.py` | MOD | + 2 PROFILE_REGISTRY entries; + 2 LEVEL_BY_TYPE entries |
| `tests/test_check_documentation_profile.py` | MOD | + 4 new tests; existing tests updated for the 5-profile registry (29 -> 33 total) |
| `docs/process-documentation-architecture.md` | MOD | §12 EXT roadmap updated; §13 Cardinal entities added; §14 acceptance criteria profile count 3 -> 5 |
| `change-requests/CR-BP-94-EXT-01a-l0-l1-profiles.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-94-EXT-01a row added before `## Cross-repo context` |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 108 -> 109 |

No canonical-entity mutation. No schema change to any entity schema. No gate wire change to existing gates. No new entity-level records.

## 6. Acceptance criteria

1. `templates/documentation-profile-l0-process-context.yaml` exists with profile_id `dea:profile-readme-l0-process-context-v1`.
2. `templates/documentation-profile-l1-process-group.yaml` exists with profile_id `dea:profile-readme-l1-process-group-v1`.
3. `scripts/check_documentation_profile.py` exposes 5 profile registry entries: `(ProcessContext, L0)`, `(ProcessGroup, L1)`, `(Process, L2)`, `(Activity, L3)`, `(Task, L4)`.
4. `_resolve_level()` consults `LEVEL_BY_TYPE` which includes `ProcessContext -> L0` and `ProcessGroup -> L1`.
5. `tests/test_check_documentation_profile.py` reports 33 tests pass (was 29).
6. Live catalog gate [21] emits 2,306 advisory findings (was 1,956).
7. CR-BP-94-EXT-01a carrier CR is filed in `change-requests/`.
8. README row + CATALOG regen is committed.
9. Em-dash / en-dash audit: 0 violations in new prose.
10. Full pytest suite passes (pre-existing `test_dispositions::test_tranche_count_is_ten` failure unchanged; NOT introduced by this slice).
11. `git log -1 --format=%ct` on `CR-BP-94-EXT-01a-l0-l1-profiles.md` resolves to a real last-commit timestamp (CR-META cutoff probe invariant; CR-BP-EXT-01 already established the EXT pattern).
12. The L1 pilot decision (deferred to EXT-06) is documented in `docs/process-documentation-architecture.md` §13 with rationale.

## 7. Result

CR-BP-94-EXT-01a closes the L0/L1 cardinal-entity profile gap that the original CR-BP-94-EXT-01 slice left open. Five profiles now exist (L0/L1/L2/L3/L4) with consistent structure and validator coverage. The 21-gate suite remains CONFORMANT. The 2,306 advisory DOC-001..005 findings are surfaced for transparency; remediation (populating READMEs per the profile machinery) is the work of EXT-02..06. `open_change_requests` 108 → 109.