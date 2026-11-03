# CR-BP-222: Narrative Legacy-Id Sweep (mv1 Completion, Prose Layer)

**Status**: Accepted (landed via PR #221; status backfilled post-merge per the immutability rule)
**Layer**: Process Catalog (Cross-cutting id-system hygiene)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-02
**Depends on**: CR-BP-mv1 (2026-09-20 org-wide id migration; this CR finishes its prose layer), CR-BP-113 (href/structured-layer completion), CR-BP-135 (composes token migration; the immediately preceding mechanical sweep precedent)

> **Scope.** Mechanical narrative-field sweep completing the CR-BP-mv1 id migration in the one artifact class every prior slice left behind: legacy `dea:*` id tokens embedded in current-state prose. A full-repo census (2026-11-02) finds **5,416 legacy tokens across 2,977 canonical entity files**. Of these, **5,407 resolve mechanically** via `reconciliation/migration-id-map.yaml`; 2 are registered `known_residuals` (documented, disposition pending their own slices); 4 are per-case items dispositioned in §3. The sweep rewrites current-state narrative fields only; `metadata.change_history` prose (2,906 tokens) is deliberately preserved as historical audit trail, per the house rule that landed history is immutable (§2). A new permanent gate rule (**IDM-009**) makes post-sweep recurrence a CI failure. Zero semantic changes: every rewrite replaces a legacy id token with the canonical id of the *same record*; no definition, boundary, or evidence meaning is altered.

**Lands against**: 2,394 entity YAML files (narrative-field token rewrites, mechanical); `reconciliation/migration-id-map.yaml` (unchanged — no new residuals needed); 1 new one-shot repair script (`scripts/repair_narrative_ids.py`); 1 validator extension (`scripts/check_id_system.py` IDM-009, wired into both full-scan and PR-scoped IDM-008 modes); 1 new test module; CATALOG.yaml regenerated (last_modified bumps only). **0 id changes. 0 definition/evidence-content changes beyond token substitution. 0 entity count moves.**

---

## 1. Background and Authority

Three completed slices migrated the catalog's identifiers: CR-BP-mv1 migrated the id system org-wide (`dea:*` → `processes:*`) and enforced it at the structured-data layer (IDM-006 bans legacy ids in machine-readable reference fields); CR-BP-113 repaired 272 broken relative hrefs; CR-BP-135 migrated the last legacy type token (`dea:composes` → `composes`). Each slice stopped where its enforcement stopped. Narrative prose was never swept and never gated:

1. **The census.** As of 2026-11-02, canonical entity files carry **5,416 legacy `dea:{pc,group,process,activity,task,scope}-*` tokens** in prose. By field: `metadata.change_history.change` 2,906; `definition` 2,241; `description` 117; `inputs[].description` 108; `evidence[].reference` 35; `identity.evidence_links[].ref` 3; `scope.excludes` 2; `composes[].rationale` 1; plus the 2 registered residuals (`metadata.supersedes`, `metadata.scope.id`). A reader of any affected definition — or of any README generated from it — is taught a retired identifier that resolves to nothing.
2. **The enforcement gap.** IDM-006 checks only structured reference fields (`id`, `belongs_to_*`, `source_id`, `target_id`, `ref`, …) and only against exact-string matches; narrative fields are unchecked by design (its docstring: "historical prose … may cite legacy ids verbatim"). The design intent is right for *change_history* but was never narrowed: current-state narrative (`definition`, `description`, `trigger`, `outcome`, …) teaches the pre-mv1 world to every consumer, and nothing prevents new records from re-introducing legacy tokens in prose.
3. **The README amplifier.** Every generated README (CR-BP-114 regeneration) embeds these fields verbatim — the legacy tokens propagate from 2,977 YAML files into 2,900+ rendered README pages (companion CR-BP-221's regen inherits this CR's sweep).

This CR closes the prose layer with the same discipline as its predecessors: one-shot data-driven repair (§4), permanent gate (§5), and documented residuals (§3).

## 2. Sweep Policy (what rewrites, what is preserved)

| Field class | Tokens | Disposition |
|---|---|---|
| `definition`, `description`, `trigger`, `outcome`, `scope.*`, `inputs[].description`, `outputs[].description`, `cell_charter.*`, `composes[].rationale` | ~2,505 | **Rewrite** via `id_map` (current-state narrative; the record teaches the canonical id) |
| `evidence[].reference`, `identity.evidence_links[].ref` | 38 | **Rewrite** via `id_map` (machine-resolvable citations; same treatment as CR-BP-113 hrefs) |
| `metadata.change_history[].change` | 2,906 | **Preserve** — historical attestation prose describing actions taken when the legacy ids were current; rewriting history would falsify the audit trail (house rule: landed history is immutable) |
| `known_residuals` entries | 2 | **Preserve** — already registered with per-record dispositions (ge-conceive supersedes lineage; pr-operate scope label) |

Rewrites are token-for-token substitutions using `reconciliation/migration-id-map.yaml` only. The repair script never invents a mapping: an unmappable token is left in place and reported, never guessed.

## 3. Per-Case Dispositions (the unmapped census)

The census's unmapped set is small, and most of it needs no repair action at all:

| Token | Site (parsed) | Disposition |
|---|---|---|
| `dea:pc-fa-re` (source string truncated mid-token: `…within the dea:pc-fa-re'`) | `processes-process-fa-retire-wkbrsa.yaml`, `inputs[].description` | **Repair** via explicit exception to the full canonical id `processes:pc-fa-retire-64q5p9` (the same record's non-truncated sibling token `dea:pc-fa-retire` in `description` maps normally) |
| `dea:process-conduct-` (truncated across folded-scalar lines) | `processes-group-fa-conceive-9xzf3b.yaml`, `metadata.change_history` | **Preserve** — historical attestation prose (CR-BP-21e.1 entry); exempt by §2 policy |
| `dea:process-frame-financial-policy-thesis` (well-formed legacy id, absent from id_map) | `processes-group-fa-conceive-9xzf3b.yaml`, `metadata.change_history` | **Preserve** — historical attestation prose (CR-BP-58 entry describing the never-instantiated target); the passage *is* the historical record of that disposition |
| `dea:group-regulated-` (truncated across folded-scalar lines) | `processes-group-sd-retire-7fksad.yaml`, `metadata.change_history` | **Preserve** — historical attestation prose |
| `dea:group-strategy-and-governance-conception`, `dea:scope-customer-facing-operations` | `metadata.supersedes` / `metadata.scope.id` (+ change_history echoes) | **Preserve** — already registered in `migration-id-map.yaml` `known_residuals` with per-record dispositions; IDM-009 exempts registered values |

The gate's truncation-aware regex (`[a-z0-9-]*`) ensures source-string truncations like `dea:pc-fa-re` are caught, not skipped, so this table stays closed: any future truncation trips IDM-009 instead of passing silently.

## 4. Repair Script

`scripts/repair_narrative_ids.py` (one-shot, `--dry-run`, idempotent), driven by data, not hand-editing:

1. Load `id_map` from `reconciliation/migration-id-map.yaml` + the §3 exception table (hardcoded, small, commented).
2. For each canonical entity file (state directories `research/`, `candidates/`, `retired/` excluded), parse YAML; walk **string values**, skipping the `metadata.change_history` subtree; apply regex token substitution for every `dea:{pc,group,process,activity,task,scope}-[a-z0-9-]+` match found in `id_map` or the exception table.
3. Rewrite files with PyYAML dump settings matching the tree's existing serialization (block style, preserve key order) so diffs are token-substitution-only.
4. Report per-file and per-token counts; exit non-zero if any token is unmapped and unexcepted (never silently).

## 5. Gate: IDM-009 (narrative id currency)

Extend `scripts/check_id_system.py` with **IDM-009**: no legacy `dea:{pc,group,process,activity,task,scope}-*` token may appear in any string value of a canonical entity record **except** inside `metadata.change_history` subtrees and except values registered in `known_residuals` (or matching their `legacy_value` strings). Blocking under the same `--strict` posture as IDM-006. This makes the CR-BP-135 pattern (sweep + gate) the standing discipline: future tranches generated with legacy tokens fail CI at authorship time, not at audit time.

NOT-list: IDM-009 does not check `change_history` (immutable audit trail); does not check state directories (`research/`, `candidates/`, `retired/` — non-canonical by CR-CATALOG-STRUCT-01 §5); does not check non-entity files (docs carry their own CR-BP-113-completed layer); does not ban the string `dea:` generally (namespaces like `dea:maps-to` classification bindings are current vocabulary).

## 6. Verification / Acceptance Criteria

1. `repair_narrative_ids.py --dry-run` reports exactly **2,508 rewrites across 2,394 files** (2,507 via `id_map` + 1 §3 exception) and **2 preserved residuals**; the real run is idempotent (second run reports 0 rewrites, 0 files touched).
2. Post-sweep parsed census returns **0** legacy tokens outside `metadata.change_history` subtrees and `known_residuals` values (verified 2026-11-02).
3. `check_id_system.py --strict` green, including IDM-009: fires on a legacy token in `definition`, on truncated tokens; exempts `change_history` subtrees and registered residuals (8 tests in `tests/test_check_id_system_narrative.py`; existing 15 id-system tests unchanged and green).
4. Full gate suite green; CATALOG.yaml regenerated (last_modified bumps only; no count moves).
5. Generated READMEs re-rendered (companion CR-BP-221 regen) carrying only canonical ids in prose.
