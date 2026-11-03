# CR-BP-221: README Generator Profile Integrity (Per-Profile Section Numbering, Cell Fidelity, RDM-003)

**Status**: Accepted (landed via PR #221; status backfilled post-merge per the immutability rule)
**Layer**: Cross-cutting (catalog documentation layer)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-02
**Depends on**: CR-BP-94-EXT-07 (consolidated README profiles; the numbering defect lives in its generator), CR-BP-114 (README regeneration + drift gate; RDM-001 is the enforcement surface this CR extends), CR-BP-222 (narrative legacy-id sweep; co-landed in the same PR — its rewrites re-render through this CR's regeneration)

> **Scope.** A user-directed review (2026-11-02, eaojnr) of the README for `processes:process-ao-activate-jqxtqn` found the section numbering incoherent: unnumbered "Header" and "Intent" sections followed by "2. Governance", "5. Properties", "4. Hierarchical Decomposition" (a 5-before-4 inversion), unnumbered "Operational Details", "7. Technical Metadata". A catalog-wide audit found the defect on **100% of the 3,723 generated READMEs** — deterministic, because it is baked into the generator: `scripts/generate_readmes.py` hardcoded the *L0* section numbers on section keys shared with the L1–L4 profiles and left the L1–L4-only keys unnumbered. Three gates were green throughout because they verify *README == generator output* and *required sections present* — not that the numbering is coherent. This CR fixes the numbering at the source, repairs two further generator fidelity defects found in the same review (mid-word cell truncation; L4 Intent/Definition duplication), and adds a blocking gate rule (**RDM-003**) so the defect class cannot regress.

**Lands against**: `scripts/generate_readmes.py` (heading model, truncation, dedup); 3,723 regenerated READMEs (numbering + CR-BP-222's swept prose); `scripts/check_readme_consistency.py` (RDM-003, blocking; self-test extended); `scripts/check_documentation_profile.py` + `scripts/validate_readme_structure.py` (EXPECTED_HEADINGS made number-agnostic; self-test fixture corrected); `tests/test_generate_readmes.py` (4 tests updated, 4 added). **0 entity-record changes (READMEs are generated artifacts; the records were touched only by CR-BP-222). 0 gate-count moves. 0 id changes.**

---

## 1. Background and Authority

1. **The defect is in the generator, not the records.** The heading map (`SECTION_HEADINGS`, pre-CR-BP-221) stored fully-rendered headings with hardcoded numbers: `governance-provenance` → `## 2.`, `properties-relationships` → `## 5.`, `hierarchical-decomposition` → `## 4.`, while `header-identity-table`, `intent-definition`, and `operational-details` carried no number. The L1–L4 profile emits sections in its own order (Properties 4th, Hierarchical 5th) with the L0 numbers attached — producing `U U N2 N5 N4 U N7` on all 3,723 L1–L4 READMEs. The L0 profile rendered `U N1..N7` on all 49 — an off-by-one against its own 8-section design (the unnumbered Header shares slot 1 with "1. Executive Summary"). The audit signature was uniform per level: one defect, one source, catalog-wide reach.
2. **The gates could not see it.** RDM-001 (README byte-identical to generator output) passes because the generator itself is wrong; DOC-016 (required sections present) passes because the headings exist; the documentation-profile fixture README itself carried the incoherent numbering — the self-test blessed the defect.
3. **Two fidelity defects found in the same review.** (a) Properties-table cells hard-slice values at 120 chars, mid-word (`…regulated-entity appro`), misquoting the record the README documents. (b) L4 tasks carry no separate intent field, so the Intent and Definition sections rendered the *same text twice*.

## 2. Changes

| Site | Change |
|---|---|
| `scripts/generate_readmes.py` — heading model | `SECTION_HEADINGS` (hardcoded numbers) → `SECTION_TITLES` (titles only) + `profile_headings()`, which numbers each profile's sections **1..N by position**. L0: 1-Header … 8-Technical. L1–L4: 1-Header, 2-Intent, 3-Governance, 4-Properties, 5-Hierarchical, 6-Operational, 7-Technical. |
| `scripts/generate_readmes.py` — Properties cells | `_truncate_cell()`: word-boundary truncation with `…` ellipsis (replaces the hard `[:120]` slice). |
| `scripts/generate_readmes.py` — Intent/Definition | When the intent fallback resolves to the same text as the definition (the L4 shape), render one combined `**Intent and Definition**:` line instead of duplicating. |
| `scripts/generate_readmes.py` — new `check_numbering()` | Pure function: every H2 numbered, strictly sequential 1..N; returns a diagnostic otherwise. |
| `scripts/check_readme_consistency.py` | **RDM-003 (blocking)**: `check_numbering()` applied to the generator's expected output for every record. Combined with RDM-001 (disk == generator), an incoherent README is impossible without failing CI at both authorship and regression time. Self-test extended (5 cases). |
| `scripts/check_documentation_profile.py` / `scripts/validate_readme_structure.py` | `EXPECTED_HEADINGS` patterns made number-agnostic (`(?:\d+\.\s*)?` optional prefix) — required now that the same section id carries different numbers per profile. The profile validator's fixture README corrected to coherent numbering. |
| 3,723 READMEs | Regenerated (`generate_readmes.py --force`): coherent per-profile numbering, word-boundary cells, de-duplicated L4 intents, and CR-BP-222's canonical-id prose. |
| `tests/test_generate_readmes.py` | Presence tests re-targeted via `SECTION_TITLES`; `test_section_numbering_continuous` rewritten to assert strict 1..N on L0 and L2 output; new tests: RDM-003 fires on the exact pre-CR-BP-221 inversion shape; L4 intent dedup; word-boundary truncation. |

NOT-list: no section is added, removed, or reordered in any profile; the consolidated CR-BP-94-EXT-07 design is unchanged (only its numbering is now derived, not hardcoded); no record YAML changes in this CR; the EXT-04 content backfill question (placeholders) is a separate programme decision, explicitly out of scope.

## 3. Why a Generator-Level Gate (RDM-003) and Not a DOC Rule

The numbering property lives entirely in generator output; `validate_readme_structure.py` is an advisory manifest generator by design (DOC-016..020, all advisory, exit 0). The blocking enforcement surface for READMEs is `check_readme_consistency.py` (RDM-001, blocking, CI-wired). Placing the coherence check there — as **RDM-003 on the expected content** — gives the rule real teeth and evaluates it before a single byte reaches disk. RDM-001 then guarantees the on-disk README inherits the property.

## 4. Verification / Acceptance Criteria

1. Every generated README's H2 sequence is strictly `1..N` per profile; the specific README that triggered the review (`process-ao-activate-jqxtqn`) renders `1. Header → 2. Intent → 3. Governance → 4. Properties → 5. Hierarchical → 6. Operational → 7. Technical`.
2. `check_readme_consistency.py` CONFORMANT with RDM-003 wired (self-test PASS: 5 cases, including the inversion shape).
3. `generate_readmes.py --check` green on 3,723 records (drift gate proves regeneration is complete).
4. `check_documentation_profile.py` and `validate_readme_structure.py` green under the number-agnostic patterns.
5. No Properties-table cell ends mid-word (word-boundary truncation with ellipsis); no L4 README duplicates Intent and Definition text.
6. Full gate suite green; CATALOG.yaml regenerated.
