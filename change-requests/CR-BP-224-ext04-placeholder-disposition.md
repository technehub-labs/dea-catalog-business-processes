# CR-BP-224: EXT-04 Placeholder Disposition (Derive, Re-Point, Retire)

**Status**: Accepted (this PR)
**Layer**: Cross-cutting (catalog documentation layer)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-04
**Depends on**: CR-BP-94-EXT-04 (landed via PR #177 as the generation/validation pipeline — its scope never was the content backfill the placeholders promised), CR-BP-220 (the derived-backfill method: mechanical composition from documented record fields, no invention, every item source-cited), CR-BP-GS-1 (GOV-002/GOV-003 owner and charter-vocabulary provenance the derivations cite), CR-BP-221 (the generator this CR extends)

> **Scope.** Closes the EXT-04 placeholder question with a full disposition: **zero `_(pending; backfill at EXT-04)_` promises remain in the 3,723-record README corpus** (was 14,937 slots at the 2026-11-02 review). Three moves: (a) **derive** — the generator now renders Roles & Responsibilities and Business Rules and Controls from each record's own fields (owner/actors/stakeholders/responsibility/boundary/scope/cohesion, every line source-cited, zero invention), fixes two renderer field gaps that manufactured false pendings (L1 groups' `composes` children and L0 PCs' `scope` were never read), renders L4 tasks as leaves-by-design with their parent link, and falls L2 definitions back to the record's documented `description`; (b) **re-point** — the only genuinely deferred content (the L0 metrics register; L0 role assignment) renders an explicit standing pointer to the CR-BP-94-EXT-24 closure window (due 2026-12-31) instead of promising a slice that closed in October; (c) **retire** — the generator's placeholder vocabulary and completeness note no longer mention EXT-04 as a backfill. Zero entity-record YAML changes (READMEs are views; definitions render via fallback, not rewrite).

**Lands against**: `scripts/generate_readmes.py` (two renderer gap fixes + two derivation helpers + standing-pointer vocabulary + boilerplate); 3,723 regenerated READMEs; `tests/test_generate_readmes.py` (+5 tests, 1 updated). **0 entity-record changes. 0 gate changes. 0 id changes. 0 count moves.**

---

## 1. Background and Authority

The 2026-11-02 README quality review found 14,937 placeholder slots all promising "backfill at EXT-04" — but EXT-04 had landed on 2026-10-18 (PR #177) as the generation/validation pipeline, a different scope entirely. The promise pointed at a closed slice: no tranche was ever coming, and nothing tracked the deferral. Investigation of the actual slots found most were **not content gaps at all but renderer gaps**:

| Slot class | Count | Diagnosis | Disposition |
|---|---|---|---|
| L1 Hierarchical Decomposition | 49 | Renderer never read the groups' `composes` blocks (150 group→process edges exist) | **Derive** — composes children render |
| L4 Hierarchical Decomposition | 2,900 | Tasks are leaves; renderer had no leaf concept and never read `belongs_to_activity` | **Derive** — leaf-by-design statement + parent link |
| L2 Intent and Definition | 145 | mv1-era records document the definition in `description`; renderer had no fallback | **Derive** — definition falls back to `description` |
| Operational Details, L1 (×2) | 98 | Renderer read `governance.roles` only; groups carry `owner` (GOV-002) and `scope` | **Derive** — owner + composes count; governing scope |
| Operational Details, L2 (×2) | 290 | Same, plus `actors`/`stakeholders` (GOV-003) never read | **Derive** — owner + actors + stakeholders; process scope |
| Operational Details, L3 (×2) | 1,160 | Activities carry `belongs_to_business_process` + `cohesion_rationale`; renderer read neither | **Derive** — owner inheritance (EXT-13) + cohesion control rationale |
| Operational Details, L4 (×2) | 5,800 | Tasks carry `responsibility` (phase custodian) + `boundary` (inclusions/exclusions); renderer read neither | **Derive** — phase responsibility + boundary rules |
| L0 Inputs/Outputs/Interfaces | 49 | Renderer read `process_scope`; PCs carry `scope` (field-name mismatch) | **Derive** — scope fix |
| L0 Business Rules | 49 | No derivable rules field on PCs beyond charter/regulatory base | **Re-point** — standing pointer (EXT-24) |
| L0 Roles | 49 | PCs carry no owner (GS-1 assigned owners at L1/L2, not L0) | **Re-point** — standing pointer (EXT-24) |
| L0 Metrics (KPI/KRI/KCI) | 196 | Metric design requires invention — not mechanically derivable | **Re-point** — standing pointer (EXT-24) |
| Technical Metadata note | 49 | Boilerplate repeated the stale EXT-04 promise | **Retire** — new completeness note |

## 2. The Derivation Rules (no invention; every line cites its source field)

- **Roles, L1**: `owner.value` (GOV-002-confirmed) + composes-children count. **L2**: owner + `actors` + `stakeholders` verbatim. **L3**: owner inheritance from `belongs_to_business_process` (EXT-13 accountability model) + cohesion accountability (`cohesion_rationale`, CR-BP-32 §6). **L4**: the task's own `responsibility` field (phase custodian, CR-BP-102) + parent activity link.
- **Rules, L4**: `boundary.inclusions` / `boundary.exclusions` verbatim. **L1**: `scope.includes` / `scope.excludes`. **L2**: `process_scope.includes` / `process_scope.excludes`. **L3**: controls-inherited-from-parent-BP statement + cohesion control rationale.
- Long values truncate at word boundaries with an ellipsis (CR-BP-221 `_truncate_cell`), never mid-word.
- A level with no derivable data renders the **standing pointer**, never a false promise: `_(standing item: tracked in the documentation improvement backlog; closure under CR-BP-94-EXT-24, due 2026-12-31)_`.

## 3. What Does NOT Change

- **No entity-record YAML changes**: definitions render via fallback (the record's `description` is its documented definition — rendering it is a view, not a rewrite). A future slice may promote the 145 composed definitions into the records' `definition` fields per the CR-BP-220 method; that is a content tranche, deliberately out of scope here.
- No section added/removed/reordered in any profile; numbering per CR-BP-221 is untouched.
- No gate or CI change; DOC-016..020 semantics unchanged (DOC-019's 49 standing advisories are the L0 metrics deferral, now honest).
- The deprecated-record exclusion (MECE-008, CR-BP-36) now renders explicitly instead of as a false pending.

## 4. Verification / Acceptance Criteria

1. Catalog-wide census: **0** `backfill at EXT-04` / `(Pending EXT-04)` occurrences across 3,723 READMEs (was 14,937 placeholder slots); standing pointers present where deferral is real.
2. The review-trigger README (`process-ao-activate-jqxtqn`) renders a populated Definition; L1 groups render composes children + owner + governing scope; L4 tasks render leaf + responsibility + boundary.
3. `generate_readmes.py --check` green on 3,723; RDM-001..003 CONFORMANT; IDM-009 CONFORMANT; DOC-002/DOC-004 = 0.
4. Tests: +5 new (L1 composes render, L4 leaf+responsibility, deprecated MECE-008 statement, L2 definition fallback, no-EXT-04-promise invariant), 1 updated (metrics placeholder → standing pointer); full README test files green.
5. Freshness gate green post-commit (regen + amend discipline).
