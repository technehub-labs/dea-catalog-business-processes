# CR-BP-114: Record README Regeneration, Drift Gate, and Release-Cut Integration

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-13
**Depends on**: CR-BP-113 (mv1 migration completion; this CR lands on the same hygiene surface)
**Trigger**: User directive 2026-10-13, eaojnr: "In the report, the '/entities/v1-alpha/' still has many readme's embedded deep that are out of synch with the changes. Do a rigorous pass through to update and bring them up to speed, while entrusting that going forward there is a mechanism to keep them consistent with the entities changing. In addition to ensure new cuts or versions reflect this change management process."
**Carrier**: Single-PR remediation, three moves: (a) regenerates all 3,723 record READMEs from the current entity records via `scripts/generate_readmes.py --force` (new flag), replacing four classes of stale content; (b) adds a permanent blocking gate (`scripts/check_readme_consistency.py`, RDM-001..002) making README drift a CI failure; (c) wires the README-consistency verification into the release-cut procedure (`docs/versioning.md` step 3) so every future tag carries READMEs consistent with the records they document.

Lands against: 3,723 record READMEs (regenerated in place); `scripts/generate_readmes.py` (`--force` + `--check` modes; L0 type-label fix); 1 new gate + 1 new test module; `scripts/conformance_result.py` GATES 29 -> 30; `ci.yml` +1 blocking step; `docs/versioning.md` release checklist; CHANGELOG `[Unreleased]` entry; change-requests/README.md row; CATALOG.yaml regenerated (open_change_requests 127 -> 128). 0 id changes. 0 record-content changes (definitions, triggers, outcomes, evidence prose untouched).

## 1. Background and Authority

CR-BP-mv1 migrated the entity records and their structured fields; CR-BP-113 repaired hrefs, templates, schemas, and docs. One surface remained frozen at the pre-mv1 state: the per-record README tree under `entities/v1-alpha/`. The audit (2026-10-13) found 3,879 READMEs in five classes:

| Class | Count | Pre-fix state |
|---|---|---|
| Generator-owned record READMEs (L3/L4) | 3,405 | Frozen pre-mv1 (`dea:*` ids, legacy parent refs). Root cause: `generate_readmes.py` skipped any existing README (`skipped_existing`), so the post-mv1 generator never rewrote them. |
| Tranche-written L1/L2 directory READMEs | 162 | Hand/tool-written at admission with `dea:group-*` / `dea:process-*` ids and `dea:pc-*` context refs. |
| Task dirs carrying research-README content | 100 | Wrong template: the record README held "Research artifacts for ..." text instead of the Task documentation profile. |
| Cell-root READMEs | 49 | Stale copies of the retired `contexts/v1-alpha/README.md` register text ("matrix is empty by design", CR-BP-02 era). |
| Hand-titled L2 READMEs | 6 | Free-form headers from the CR-BP-106 tranche. |

(The remaining 154 research/ READMEs were already post-mv1; `entities/v1-alpha/README.md` is the curated structural template and is correct.)

## 2. Remediation: Full Regeneration

`generate_readmes.py` gains two modes:

- `--force`: overwrite existing READMEs (the previous behaviour was fill-missing-only, which is what allowed the tree to freeze).
- `--check`: recompute every README in memory and diff against disk; exit 3 with a drift list (mirrors `regenerate_catalog.py --check`).

A one-shot `python3 scripts/generate_readmes.py --force` regenerated all 3,723 record READMEs (12.7s). Every record README is now byte-identical to the generator's rendering of the current record: canonical `processes:*` ids, current names, current lifecycle status, revision history from `metadata.change_history`. The deprecated-record signal is preserved: `lifecycle_status: deprecated` renders in section 1 and the retirement rationale renders via the change-history evidence section.

Known residue, out of scope by design: legacy `dea:*` tokens that live inside record *prose* (definition / change text of the records themselves, rendered verbatim into section 2) are record content. Rewriting definition prose is a content migration with semantic-check implications and belongs to its own CR.

## 3. New Gate: scripts/check_readme_consistency.py (RDM-001..002)

House validator contract (`--strict` / `--json` / `--self-test`, exit 0/1/2):

- **RDM-001 (blocking)**: every canonical record's README is byte-identical to the generator output for the current record fields (missing or stale = finding).
- **RDM-002 (advisory)**: orphan READMEs under `entities/` (no owning record; not a research/ artifact; not the v1-alpha structural template).

After this CR, record READMEs are a generated artifact under CI enforcement, the same contract as `CATALOG.yaml`: the entity record is the source of truth, the generator renders, the gate verifies. Hand-editing a generated README fails CI at the next push.

## 4. Release-Cut Integration

`docs/versioning.md` "Cutting the next tag" gains step 3: before the carrier PR merges, run `generate_readmes.py --force` (commit any delta as a separate `chore:` commit), verify `check_readme_consistency.py --strict` exits 0, verify the existing CATALOG `--check` and the full conformance rollup. The org-level release-cut procedure note carries the same step for every dea-catalog-* repo. Every future release tag therefore carries READMEs consistent with the records at the tagged commit.

## 5. Conformance + Test Posture

- `python3 scripts/generate_readmes.py --check` -> exit 0 ("3,723 record README(s) current").
- `python3 scripts/check_readme_consistency.py --strict` -> CONFORMANT (0 blocking, 0 advisory).
- `python3 scripts/check_readme_consistency.py --self-test` -> PASS (4 fixture cases: missing / exact / stale / orphan).
- `tests/test_check_readme_consistency.py`: 8 tests pass.
- `python3 scripts/conformance_result.py`: GATES 29 -> 30, all CONFORMANT.
- `ci.yml`: +1 blocking step after the CR-BP-113 gates.

## 6. NOT-List (Out of Scope)

- No record-content changes. Legacy `dea:*` tokens inside record definition/change prose are preserved verbatim; rewriting them is a content migration requiring its own CR.
- No README template changes beyond the L0 type-label fix (`Type: Record` -> `Type: ProcessContext` for L0 records lacking an explicit `type` field).
- No changes to `entities/v1-alpha/README.md` (curated structural template; verified current) or the 154 research/ READMEs (already post-mv1).
- No cross-repo work. Sibling catalog repos carry their own README surfaces; this CR exports the gate pattern via the org-level release-cut note.

## 7. Acceptance Criteria

- All 3,723 record READMEs byte-identical to generator output (`generate_readmes.py --check` exit 0).
- Zero README under `entities/` references a retired `dea:<level>-*` id in generator-rendered fields (spot-verified; residual legacy tokens exist only inside record prose, §2 residue note).
- RDM-001..002 gate CONFORMANT under `--strict`; wired as gate [30] in `conformance_result.py` and as a blocking `ci.yml` step.
- `docs/versioning.md` release checklist carries the README-consistency verification step.
- CATALOG.yaml regenerated: `open_change_requests` 127 -> 128; all other counts unchanged.

## 8. Result

The embedded README tree is no longer a hand-maintained surface that can freeze at a historical state: it is a generated view over the records, refreshed by one command, enforced in CI, and verified at every release cut. The last pre-mv1 presentation surface is closed.
