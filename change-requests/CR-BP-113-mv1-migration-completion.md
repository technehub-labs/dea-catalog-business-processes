# CR-BP-113: mv1 Migration Completion - Docs, Templates, Schemas, and HREF Repair

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-13
**Depends on**: CR-BP-mv1 (2026-09-20 org-wide id/path migration; this CR finishes what it left behind)
**Trigger**: User directive 2026-10-13, eaojnr: "Finish the mv1 migration in docs, templates, and hrefs - fix the 278 broken links, regenerate change-requests/README.md, update templates to the processes:* id family (or generate templates from the schemas so they can't drift)."
**Carrier**: Single-PR remediation, five moves: (a) repairs 272 broken relative href: targets across 189 entity files, driven by reconciliation/migration-id-map.yaml and an explicit rename table; (b) modernizes all 5 entity templates to the processes:* id family and current layout, plus a drift gate so templates cannot diverge from schemas again; (c) fixes the two schema/validator leftovers (process-scope.schema.json ^dea:scope- pattern; IDM-006 legacy regex missing scope); (d) completes the docs layer (3 contexts/v1-alpha/ live references and 12 dea:* id-family references across 4 files); (e) repairs the corrupted change-requests/README.md table (148 duplicate CR-BP-90 rows) and retargets the stale contributions-queue record. Three new permanent gates (check_href_targets.py, check_templates.py, check_cr_readme.py) make each class of leftover a CI failure instead of a recurring audit finding.

Lands against: 189 entity YAML files (href fields + one change_history entry each); 5 templates; 1 schema (schemas/entities/process-scope.schema.json); 1 validator (scripts/check_id_system.py IDM-006 regex + self-test fixture); 4 docs/README files; change-requests/README.md (dedupe); 1 contribution record; 3 new validators + 3 new test modules + 1 one-shot repair script; conformance_result.py GATES +3; ci.yml +3 blocking steps; CHANGELOG + CATALOG.yaml regenerated. 0 id changes. 0 definition/evidence-content changes. 0 entity count moves.

## 1. Background and Authority

CR-BP-mv1 migrated the id system org-wide (dea:* -> processes:*, contexts/v1-alpha/ retired, one-directory-per-record layout) and was enforced at the data layer: IDM-006 bans legacy dea:* ids in structured reference fields, and the data-quality agent-style sweep confirms every belongs_to_*, composes[].target_id, and context reference resolves. The migration stopped at the data layer. Four artifact classes still teach or point at the pre-mv1 world:

277 of 484 relative href: targets in entity files are broken (194 files) - 57%. Nothing checks href resolution: IDM-006 covers structured id reference fields, not path strings inside evidence_links[].href.

All 5 entity templates teach dea:task-* / dea:group-* / dea:process-* / dea:activity-* / dea:pc-* ids and entities/v1-alpha/dea:<kebab>/ copy-to paths that fail validation against the current schemas. A contributor following a template verbatim produces an invalid record.

The docs layer presents the retired contexts/v1-alpha/ register and dea:* id families as current in 4 files (down from the original 6 survey; docs/identity.md and docs/decomposition-semantic-contract.md were already clean).

Two migration leftovers in the enforcement layer itself: process-scope.schema.json still pins ^dea:scope-[a-z0-9-]+$ (siblings use ^processes:...), and IDM-006's legacy-id regex lists pc|group|process|activity|task but omits scope.

Plus one corruption: change-requests/README.md carried 149 CR-BP-90 rows (1 legitimate + 148 dupes) and was missing rows for CR-BP-102 and CR-BP-113 - the in-repo table was 5 rows short of the on-disk CR file count.

## 2. HREF Repair (272 hrefs, 189 files)

One-shot scripts/repair_mv1_hrefs.py (supports --dry-run, idempotent), driven by data, not hand-editing. Resolution rules:

| Count | Broken pattern | Resolution rule |
|---|---|---|
| 113 | contexts/v1-alpha/pc-<cell>.yaml | Cell extracted from filename; id_map entry (legacy `pc-<cell>` and `dea-pc-<cell>` aliases both seed the path map); resolves to the on-disk PC record via rglob under `entities/v1-alpha/<cell>/` |
| 86 | entities/v1-alpha/dea:<id>/... (kebab-name form) | id_map lookup; `entities/v1-alpha/<cell>/<parent-hash-dir>/processes-<level>-<cell>-<hash>.yaml`; suffix preserved (e.g. `/research/l1-register.yaml` -> `/processes-group-pr-operate-7ab3ma.yaml`) |
| 27 | change-requests/CR-BP-21d.1-enablement-operations-completion.md | Rename: -> CR-BP-21d.1-operations-enablement-completion.md |
| 25 | change-requests/cr-bp-13a-customer-and-demand-admission.md | Rename: -> CR-BP-13a-party-and-relationship-admission.md |
| 11 | change-requests/CR-BP-21d-enablement-operations-landing.md | Rename: -> CR-BP-21d-operations-enablement-landing.md |
| 9 | change-requests/CR-BP-13a-customer-and-demand-admission.md | Rename: -> CR-BP-13a-party-and-relationship-admission.md |
| 1 | docs/research/l1-register.yaml (inside pr-operate-7ab3ma BP record) | -> entities/v1-alpha/pr-operate/pr-operate-7ab3ma/research/l1-register.yaml |

The 4 CR-link typos are not migration artifacts but name transpositions from the tranche generators; the rename table lives in the repair script and is absorbed by the HREF gate thereafter. Each touched entity file gains one metadata.change_history entry. Href strings only - ids, definitions, and evidence prose are untouched.

A separate one-shot folded-scalar fix collapsed 5 process-group records' `href: \n    <value>` (YAML folded scalar) to single-line `href: <value>` form, exposing the pre-mv1 href to the repair script's regex.

## 3. New Gate: scripts/check_href_targets.py (HREF-001..003)

House validator contract (--strict / --json / --self-test, exit 0/1/2):

HREF-001 (blocking). Any relative href: value in entities/**/*.yaml or discovery/**/*.yaml whose target does not exist on disk (resolved from repo root; ./ and / prefixes normalized).

HREF-002 (blocking). An href field whose value is not a non-empty string.

HREF-003 (advisory). An http(s) href whose URL shape is malformed (scheme/host parse failure only - no network fetch in CI).

This closes the enforcement gap that let 57% of hrefs rot silently. tests/test_check_href_targets.py carries per-rule pass/fail fixtures plus a --self-test subprocess test (8 cases).

## 4. Template Modernization + Drift Gate

Update (all 5 entity templates): business-process.yaml, activity.yaml, task.yaml, process-group.yaml, process-scope.yaml - ids and structured references to processes:<level>-<kebab>[-<hash>], process_context: processes:pc-<kebab>, copy-to paths to the one-directory-per-record layout (entities/v1-alpha/<cell>/...), and the evidence-link type comment at templates/business-process.yaml:92 (standard | documentation | evidence | reference) corrected to the schema enum (documentation | governance | interview | artifact | standard | regulation - evidence and reference are not legal values).

Design decision - gate, not generator. The directive offers "generate templates from the schemas so they can't drift". This CR implements the invariant (templates can never diverge) via scripts/check_templates.py (TPL-001..005) rather than a build step: TPL-001 template id fields match the current schema id patterns; TPL-002 structured reference fields (process_context, belongs_to_*, composes[].target_id) match current id families; TPL-003 templates with a corresponding schema (process-group, activity, task, process-scope, process-context, and business-process against entity.schema.json) load cleanly; TPL-004 evidence-link types within the schema enum; TPL-005 copy-to path comments reflect the current layout. Drift becomes a named CI failure at the moment it is introduced, with zero build machinery for 11 static files. A generator is revisited only if templates become numerous or per-domain.

## 5. Schema and Validator Leftovers

schemas/entities/process-scope.schema.json: ^dea:scope-[a-z0-9-]+$ -> ^processes:scope-[a-z0-9-]+$ (2 occurrences + description text). Zero L0 scope records exist, so the flip is unobservable in data and merely aligns the family. Governed by CR-META change note in the schema description.

scripts/check_id_system.py IDM-006 legacy regex ^dea:(pc|group|process|activity|task)- extended to include scope; a dea:scope-customer-facing-operations id surfaced in processes:process-pr-operate-bbe384's metadata.scope block and was added to known_residuals in migration-id-map.yaml as a documented exception (the migration did not migrate documentation-style L0 scope labels because the ProcessScope record type was instantiated separately under CR-BP-95; the residual's repair is out of scope for CR-BP-113).

## 6. Docs Completion (live refs fixed, history preserved)

Rule: ids and paths presented as current are migrated; historical narrative stays, marked legacy. Affected files: docs/context.md, docs/architecture.md, docs/examples/manage-customer-relationship.md, README.md - 3 contexts/v1-alpha/ live references and 12 dea:pc-|dea:group-|dea:process-|dea:activity-|dea:scope-|dea:bp- references. Concretely: canonical id-family tables and path statements flip to processes:* / entities/v1-alpha/; legacy_ids[] explanations and CR/migration history prose keep dea:* inside explicitly-marked legacy contexts (the id-map depends on them being understandable); docs/examples/manage-customer-relationship.md is rewritten as a current-shape worked example (this record now lives at entities/v1-alpha/pr-operate/pr-operate-7ab3ma/pr-operate-bbe384/processes-process-pr-operate-bbe384.yaml).

## 7. change-requests/README.md Repair + check_cr_readme.py (CRR-001..003)

Dedupe: removed 139 duplicate rows in total (in-repo + cross-repo). Then permanent rules: CRR-001 (blocking) every CR link in every markdown table row resolves on disk; CRR-002 (blocking) no duplicate rows in the in-repo table (the cross-repo table legitimately repeats sibling-repo CRs once per narrative anchor and is exempt); CRR-003 (blocking) every CR file on disk has a row in the in-repo table. Added the missing CR-BP-102 and CR-BP-113 rows. The table stays hand-maintained (no generator - the per-row summaries are editorial); the gate makes paste-corruption a CI failure.

## 8. Contributions Queue Retarget

contributions/processes/dea_bp_manage-customer-relationship.yaml: target_path: entities/v1-alpha/dea_bp_manage-customer-relationship.yaml does not exist (pre-mv1). Retargeted to the record's live location entities/v1-alpha/pr-operate/pr-operate-7ab3ma/pr-operate-bbe384/processes-process-pr-operate-bbe384.yaml; target_entry aligned with the post-mv1 id form; the contribution's own `id:` (dea:contrib-bp-manage-customer-relationship) kept as the legacy contribution identifier (the contribution id is a separate dimension from the catalog record id, and migrating it would break contribution-id-stable references in any downstream tooling).

## 9. Conformance + Test Posture

python3 scripts/check_href_targets.py --strict -> CONFORMANT (484/484 relative hrefs resolve); --self-test PASS.

python3 scripts/check_templates.py --strict -> CONFORMANT (5 templates modernized, zero dea:(pc|group|process|activity|task|scope)- occurrences under templates/); --self-test PASS.

python3 scripts/check_cr_readme.py --strict -> CONFORMANT (128 rows in-repo after dedupe + 1 cross-repo after dedupe, 0 duplicates in-repo, all in-repo links resolve); --self-test PASS.

python3 scripts/check_id_system.py --strict -> CONFORMANT (IDM-006 extended to scope; 3,723 records; 1 known_residual in migration-id-map.yaml).

python3 scripts/conformance_result.py -> CONFORMANT; GATES list +3 (29 standalone; previous 26 + HREF + TPL + CRR).

Targeted pytest: the 3 new test modules 27/27 passed. Full-suite CI wiring remains out of scope (§10).

Documentation-conformance and cross-repo-integrity gates re-run clean against the repaired href population.

## 10. CATALOG.yaml Posture

Regenerated in the same PR: open_change_requests +1 (126 -> 127 with CR-BP-112 already on main). The 189 touched entity files take new last_modified dates; canonical/retired/candidate counts, paths, and id slugs are unchanged (href repair touches no indexed field). Per the house fix(catalog) commit pattern.

## 11. NOT-List (Out of Scope)

No business-process.schema.json authoring. Templates/business-process validation uses entity.schema.json for now; a dedicated strict L2 schema is its own governance slice (the L2 schema gap predates this CR).

No README content refresh beyond mv1 references. The stale CR table (ends at CR-BP-41), wrong record counts, and CHANGELOG structural defects are a separate docs-refresh slice; this CR touches only the 3 contexts/v1-alpha references and dea:* id-family statements in the 4 files listed in §6.

No entity content changes. Definitions, triggers, outcomes, evidence prose, ids, and lifecycle states are untouched; href strings and one change_history entry per file are the only entity-file edits.

No docs-prose link-existence gating. HREF-001 scopes YAML href fields in entities/ and discovery/; markdown-link checking in docs/ is deferred.

No cross-repo work. Sibling catalog repos carry their own mv1 completion; this CR exports the gate pattern.

No template generator build step. Chosen against deliberately (§4); revisit trigger documented there.

## 12. Acceptance Criteria

HREF enumerator over entities/ + discovery/ reports 484 relative hrefs, 0 broken; check_href_targets.py --strict CONFORMANT and --self-test PASS.

The §2 rename table and id-map-driven repairs land; each of the 189 touched entity files carries the CR-BP-113 change_history entry and no other field changes.

grep -rE "dea:(pc|group|process|activity|task|scope)-" templates/ returns 0 hits; check_templates.py --strict CONFORMANT; all 5 templates validate against their schemas.

process-scope.schema.json pins ^processes:scope-; IDM-006 regex includes scope; check_id_system.py --strict CONFORMANT.

Zero unmarked contexts/v1-alpha live references remain across the 4 files in §6; docs/examples/manage-customer-relationship.md shows the current id/path shape.

change-requests/README.md has exactly one in-repo row per CR file; no duplicate CR link in the in-repo table; check_cr_readme.py --strict CONFORMANT.

contributions/processes/ record's target_path resolves on disk.

conformance_result.py reports the expanded gate set CONFORMANT; ci.yml wires HREF/TPL/CRR as blocking.

CATALOG.yaml regenerated per §10; CHANGELOG.md carries a ## [Unreleased] entry for this slice.

## 13. Result

The mv1 migration is finished everywhere it left a trace: contributors copy templates that validate; readers see one id system in docs; every relative href resolves; the CR index table is clean and duplicate-proofed; and three new gates hold each surface so the next migration (or paste accident) cannot silently reopen the gap. The repo's enforcement story - strong at the structured-data layer - now extends to the presentation and reference layers.
