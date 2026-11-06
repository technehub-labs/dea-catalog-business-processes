# CR-BP-231: Two-Layer README Profile v3 (Part I Provided / Part II Generated)

**Status**: Accepted (landed via PR #228; status backfilled post-merge per the immutability rule)
**Layer**: Cross-cutting (catalog documentation layer)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-05
**Depends on**: CR-BP-230 (the five plain-language record attributes this profile renders), CR-BP-94-EXT-07 (the consolidated v2 profile whose generated set is preserved intact as Part II), CR-BP-221 (the profile-integrity method: layout changes land at the generator source and regenerate the corpus; RDM-003 numbering coherence)

> **Scope.** Owner directive 2026-11-05 (the nomenclature assessment §6): the first part of every entity README must be accessible to a non-technical reader. Implements the two-layer layout: **Part I — Human-Readable Interpretation (provided)**, four sections rendered from the CR-BP-230 plain-language fields (or a tracked standing pointer until the CR-BP-233..236 waves backfill them), opening with a derived plain-sentence **identity card** (name, canonical ID, element type/level, domain, status, and the parent chain with the parent's business name resolved from the record tree); then **Part II — Canonical Record (CI generated)**, the unchanged CR-BP-94-EXT-07 consolidated set, renumbered 1..N within the whole-README sequence with ` (generated)` heading suffixes. Provided content lives in the YAML records and flows through the generator — RDM-001 byte-identity holds across both layers. The corpus (3,723 READMEs) regenerates in this PR; at this tranche every Part I renders the standing pointer (zero records carry the fields yet), so the layout change is content-neutral.

**Lands against**: `scripts/generate_readmes.py` (PROFILE_SECTIONS v3; SECTION_TITLES + the four provided-section renderers + identity card + name index; boilerplate; Technical Metadata generator/layers lines; PLAIN_LANGUAGE_STANDING_ITEM); `scripts/check_documentation_profile.py` (PROFILE_REGISTRY v3 + EXPECTED_HEADINGS provided patterns); `scripts/validate_readme_structure.py` (fallback registry v3; DOC-017/DOC-018 Properties anchor tolerates the ` (generated)` suffix); `scripts/check_readme_consistency.py` (self-test case 2 computes expected under the same ENTITIES_ROOT patch evaluate() uses); `tests/test_generate_readmes.py` (5 numbering assertions); `tests/test_check_documentation_profile.py` (v1-vocabulary rot repaired to v3; _readme helper and fixture README to the v3 heading set); `docs/process-documentation-architecture.md` (§6.2a two-layer normative section); 3,723 regenerated READMEs; this CR + CHANGELOG + register row. **0 entity-record changes. 0 id changes. 0 gate-registry posture changes.**

## 1. The v3 profiles

| Profile | Sections | Part I | Part II |
|---|---|---|---|
| L0 ProcessContext (`dea:profile-readme-l0-process-context-v3`) | 12 | 1. In a Nutshell (provided) · 2. Why It Matters (provided) · 3. Where You'd Encounter It (provided) · 4. Worked Example (provided) | 5. Header and Identity Table · 6. Executive Summary / Intent · 7. Governance and Provenance · 8. Behavioral Boundaries (Cell Charter) · 9. Hierarchical Decomposition (Path Scheme) · 10. Properties and Relationships · 11. Operational, Control and Metrics Details · 12. Technical Metadata — each ` (generated)` |
| L1–L4 (`-l1-process-group-v3`, `-l2-process-v3`, `-l3-activity-v3`, `-l4-task-v3`) | 11 | same four | 5. Header and Identity Table · 6. Intent and Definition · 7. Governance and Provenance · 8. Properties and Relationships · 9. Hierarchical Decomposition (Path Scheme) · 10. Operational Details · 11. Technical Metadata — each ` (generated)` |

Design constraints honoured:

- **DOC-003 H1 anchor unchanged**: the first H1 stays `# Canonical <Type>: \`<id>\`` (the validator requires the canonical id in the first H1); the human-facing name leads the identity card inside section 1.
- **RDM-003 unchanged**: every H2 numbered, strictly 1..N across the whole README (provided first, generated after) — no unnumbered part banners, so the numbering checker needs no new vocabulary.
- **EXPECTED_HEADINGS prefix-match preserved**: the ` (generated)` suffix is trailing, so the existing number-agnostic title regexes match without `$`-anchor changes; only the DOC-017/DOC-018 end-anchored Properties regexes gain an optional ` (generated)` suffix group.
- **Identity card derivation, no invention**: parent names come verbatim from the record tree (`build_name_index()`; cell → L0 context name under the `cell:<slug>` pseudo-key); domain/stage from the cell slug; status from `lifecycle_status` via the existing emoji map. At L0 the card renders the context itself (no parent clause, no self-referential context bit).
- **Worked-example default at L4**: with no authored example, the standing pointer cites the record's own `responsibility` field — source-cited, nothing inferred.

## 2. Standing pointer (CR-BP-224 pattern)

`_(plain-language narrative to be authored in the two-layer documentation waves, CR-BP-233..236)_` — worded to avoid the retired "pending" vocabulary (the `test_generate_readmes` no-pending invariant caught the first draft; reworded).

## 3. What does NOT change

- The Part II generated set: every v2 renderer is byte-preserving; only titles gain the suffix and numbers shift by +4.
- No entity records, no CATALOG.yaml content, no id, no CR history.
- No gate posture: RDM-001/002/003 mechanics untouched; DOC-016..020 rule bodies untouched (registry + anchors only).
- The `templates/documentation-profile-*.yaml` v1 drafts stay as historical artefacts (the in-process registry remains the operative source, per the CR-BP-94-EXT-07 precedent).

## 4. Verification / Acceptance Criteria

1. `generate_readmes.py --check`: **OK 3,723 current** after `--force` regeneration; RDM-001/002/003 **CONFORMANT, 0 findings**.
2. `validate_readme_structure.py`: **4 advisory findings** — exactly the pre-existing DOC-016 set; DOC-017/018 back to 0 (the `(generated)` suffix initially broke the end-anchored Properties regex on 3,723 + 98 records; fixed at the anchor).
3. `check_documentation_profile.py` self-test + `check_readme_consistency.py` self-test + `tests/test_generate_readmes.py` (24) + `tests/test_check_documentation_profile.py` (33) + `tests/test_validate_readme_structure.py` (11) green. Pre-existing failures (12 on `origin/main`: 11 stale v1-vocabulary assertions repaired here to v3, 1 `test_profile_registry_ext11::test_manifest_emitted` environmental PyYAML shell-out) — the 11 repaired, the 1 remains (environment, out of scope).
4. Pilot (`processes:task-eo-activate-record-qgmj5u`): Part I renders the identity card with resolved parent names (`Activate Continuing-Supervisor Notification`, cell context `Activate Operations Capability`), status `candidate (yellow)`, canonical ID; Part II renumbered 5..11 with ` (generated)` suffixes.
5. Full gate suite green (see the PR-level verification run).
