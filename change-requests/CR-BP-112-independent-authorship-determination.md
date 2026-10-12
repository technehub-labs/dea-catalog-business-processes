# CR-BP-112: Independent-Authorship Determination, NOTICE/LICENSE Correction, and Reference Embargo Gate

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance)
**Owner**: Coder (for eaojnr)
**Date**: 2026-10-12
**Depends on**: CR-BP-TMF-EMBARGO (2026-09-22 strip; this CR records the determination that strip implied and makes it enforceable)
**Trigger**: User directive 2026-10-12, eaojnr: the catalog content is independently authored; ensure no reference remains, and put the attribution posture on a recorded, auditable basis.
**Carrier**: Single-PR governance slice, four moves: (a) records the formal independent-authorship determination that grounds NOTICE's "Third-party attributions: None" declaration; (b) fills the LICENSE Apache-2.0 appendix copyright placeholder (Copyright [yyyy] [name of copyright owner] -> Copyright 2026 TechNeHub Labs); (c) sweeps the residual embargoed-term mentions that post-date the CR-BP-TMF-EMBARGO strip (CHANGELOG.md, change-requests/README.md, CR-BP-105, CR-BP-106, CR-BP-107); (d) adds a permanent blocking conformance gate (scripts/check_reference_embargo.py, EMB-001..004) so references cannot re-enter silently.
**Lands against**: 2 root files (NOTICE, LICENSE); 3 change-request documents rephrased (CR-BP-105, -106, -107) + this carrier; 1 generated governance file (change-requests/README.md row for this CR); CHANGELOG.md [Unreleased] entry; 1 new validator script + 1 new allowlist data file + 1 new test module; conformance_result.py GATES list 26 -> 27; ci.yml +1 blocking step; CATALOG.yaml regenerated (open_change_requests 125 -> 126). 0 entity-record changes. 0 id changes. 0 catalog count assertions move other than open_change_requests.

---

## 1. Background and Authority

Two gaps follow from CR-BP-TMF-EMBARGO:

- **The determination was never recorded.** The strip removed every substantive citation, but the reason that removal is sufficient -- that the catalog is an independent original work, not a derivative of the embargoed framework -- exists only implicitly. NOTICE declares "Third-party attributions: None" with no recorded basis, and LICENSE still ships the stock Apache-2.0 appendix placeholder. An external reviewer reading the history sees an "embargo compliance" scrub and an unexplained "None" -- the worst of both postures.
- **The strip was one-shot and has already leaked.** A full-repo audit for the embargo pattern today returns substantive hits in five post-strip artifacts, all of them compliance-attestation prose that repeats the embargoed name while asserting its absence: CHANGELOG.md (5 occurrences: the embargo entry title/body plus three later CR summaries), change-requests/README.md (rows for CR-BP-TMF-EMBARGO, -105, -106, -107), CR-BP-105 acceptance line 93, CR-BP-106 lines 27/118/134, CR-BP-107 line 19. Nothing enforces the directive; every new CR re-risks the leak by hand.

This CR closes both: the determination is recorded (section 2), the residuals are swept (section 4), and the embargo becomes a machine-checked invariant instead of a memory (section 3).

## 2. Independent-Authorship Determination (recorded)

Scope and finding, recorded under the owner's 2026-10-12 directive:

- **Scope.** All content under entities/, discovery/, classifications/, templates/, and the process definitions, decompositions, names, and structural elements of the catalog: 3,723 entity records, 29 discovery records, and their research registers.
- **Finding.** The catalog is an independent original work. Process identities, decompositions, and prose were authored under this repo's CR governance chain (CR-BP-01 through CR-BP-111). No publication of the embargoed framework was used as source material for any definition, decomposition, name, classification value, or structural element. The mentions removed by CR-BP-TMF-EMBARGO were evidence-cite-level references in research and admission prose (citations to an external framework as evidence, the same treatment given ISO 55000, APQC PCF, ITIL 4, COBIT 2019, and financial/regulatory sources), not derivation; citation is not incorporation, and those cites have already been dropped under the drop-do-not-substitute policy.
- **Effect.** NOTICE's "Third-party attributions: None" declaration is grounded in this determination. External standards and regulations remain cited as evidence only; no third-party content is incorporated.
- **Authority.** The determination is the owner's attestation, recorded here as the audit record. This CR is the instrument a downstream consumer or reviewer is pointed to; NOTICE points here (section 5).

## 3. Reference Embargo Gate (new validator)

New `scripts/check_reference_embargo.py` (rule codes EMB-001..004), following the house validator contract (`--strict` / `--json` / `--self-test`, exit 0/1/2):

- **EMB-001 (blocking).** Any occurrence of an embargoed term outside the sealed-file allowlist. Term list (case-insensitive, word-boundary): tmforum, tm forum, tmf, etom, frameworx, gb921, gb925, sid, tam, odf, oss/bss, tm-forum, tmforum.org.
- **EMB-002 (blocking).** Allowlist data file `reconciliation/reference-embargo-allowlist.yaml` missing or malformed.
- **EMB-003 (blocking).** Sealed-file integrity drift: the SHA-256 recorded in the allowlist for each sealed historical file no longer matches the file on disk (catches silent edits to the historical record).
- **EMB-004 (advisory).** A hit suppressed by the false-positive registry that matches no recorded entry pattern (registry hygiene).

**Token-class distinction** (the design decision that makes "no reference" enforceable):

1. Substantive references to the embargoed organization or its publications -- forbidden everywhere, EMB-001.
2. The governance identifier `CR-BP-TMF-EMBARGO` -- an immutable CR id baked into `check_cr_metadata.py`'s `CR_NUMBER_PATTERN` and CR-BP-107's history. It names a change request, not the organization. The gate masks this exact token on a line before term matching, so the id remains usable in Depends-on chains, README rows, and validator patterns.
3. The sealed historical carrier `change-requests/CR-BP-TMF-EMBARGO-tmforum-reference-strip.md` -- the one file allowed to enumerate what was removed (an audit record that cannot say what it removed protects nobody). Sealed by hash under EMB-003; its id is not reusable for new CRs.

Allowlist data (sealed files + hashes, suppressed false positives) lives in `reconciliation/reference-embargo-allowlist.yaml`, seeded with the 7 known sid code-identifier false positives documented in the strip CR section 3. Allowlist changes require a CR. The gate is wired into `conformance_result.py` GATES (blocking) and `.github/workflows/ci.yml`, and carries `tests/test_check_reference_embargo.py` (per-rule pass/fail fixtures + `--self-test` subprocess test, house style).

## 4. Residual Sweep (rephrase, drop-do-not-substitute)

All rephrasing replaces the embargoed name with "the embargoed framework" or "embargoed-framework references"; no substitute source is introduced (policy unchanged from the strip):

- **CHANGELOG.md**: embargo entry retitled `### CR-BP-TMF-EMBARGO: reference embargo compliance strip` with the term enumeration replaced by "the embargoed term list (see carrier CR and gate allowlist)"; the three later CR summaries' "Zero TMForum references introduced" attestations rephrased to "Zero embargoed-framework references introduced".
- **change-requests/README.md**: rows for CR-BP-TMF-EMBARGO / -105 / -106 / -107 rephrased identically; link targets and CR ids unchanged.
- **CR-BP-105 line 93, CR-BP-106 lines 27/118/134**: attestation lines rephrased; regulator evidence anchors untouched.
- **CR-BP-107 line 19**: prose around the id rephrased; the id token itself stands (masked class 2).

Historical CR bodies outside these attestation lines are not rewritten beyond what the strip already did; the sealed carrier is not touched at all.

## 5. NOTICE and LICENSE Corrections

- **NOTICE** -- "Third-party attributions" section becomes: `None. Basis: independent-authorship determination CR-BP-112 (2026-10-12). External standards and regulations are cited as evidence only; no third-party content is incorporated.`
- **LICENSE** -- Apache-2.0 appendix line: `Copyright [yyyy] [name of copyright owner]` -> `Copyright 2026 TechNeHub Labs` (matches NOTICE's existing copyright line).

## 6. Conformance + Test Posture

- `python3 scripts/check_reference_embargo.py --strict` -> CONFORMANT, 0 findings; `--self-test` PASS.
- `python3 scripts/check_cr_metadata.py --strict` -> CONFORMANT (this carrier carries Status/Layer/Owner; id and filename match `CR_NUMBER_PATTERN`).
- `python3 scripts/conformance_result.py` -> 27 gates CONFORMANT (gate count 26 -> 27), 0 blocking.
- Targeted pytest: `tests/test_check_reference_embargo.py` + `tests/test_check_cr_metadata.py` 0 failures. (Full-suite CI wiring is a separate slice; noted in section 8.)
- Full-repo audit for the section 3 term list returns 0 hits outside the sealed carrier, the masked id token, and the recorded false-positive registry.

## 7. CATALOG.yaml Posture

`open_change_requests 125 -> 126` (this carrier lands as Proposed). No entity counts move; no paths change. Regenerated via `scripts/regenerate_catalog.py` in the same PR, per the house `fix(catalog)` commit pattern.

## 8. NOT-List (Out of Scope)

- **No renaming or deletion of the sealed carrier.** Renaming breaks CR-META-006 filename to id matching and destroys the audit record of what was removed. The name stays; its content is hash-sealed.
- **No substitution.** Drop-do-not-substitute continues; no replacement framework cite is added anywhere.
- **No entity-record edits.** The determination (section 2) attests to existing content; no record's definition, evidence, or id changes.
- **No cross-repo work.** The org-wide sweep in the strip CR's cross-repo note remains per-repo; this CR covers dea-catalog-processes only and exports the gate pattern for reuse.
- **No CI test-suite wiring.** Running pytest `tests/` in CI is a separate governance slice; this CR adds only its own targeted tests, per house style.

## 9. Acceptance Criteria

1. `python3 scripts/check_reference_embargo.py --strict` reports CONFORMANT (0 findings) and `--self-test` PASS.
2. Full-repo sweep for the section 3 term list returns zero substantive hits outside the sealed carrier, the masked `CR-BP-TMF-EMBARGO` id token, and the recorded false positives.
3. NOTICE carries the determination basis line; LICENSE appendix contains `Copyright 2026 TechNeHub Labs` and no `[yyyy]` placeholder.
4. The section 4 files are rephrased with zero embargoed-term occurrences at the listed lines; link targets and CR ids unchanged.
5. `conformance_result.py` reports 27 gates CONFORMANT; `ci.yml` runs the new gate as blocking.
6. CATALOG.yaml regenerated: `open_change_requests 125 -> 126`; all other counts unchanged.
7. CHANGELOG.md carries a `## [Unreleased]` entry for this slice.

## 10. Result

The attribution posture is closed end-to-end: the "None" declaration in NOTICE rests on a recorded determination rather than an unexplained scrub; the LICENSE is properly filled; the residuals that re-entered after the strip are removed; and the embargo stops depending on human memory -- it is a hash-sealed, data-driven, blocking gate. An external reviewer finds a documented basis instead of a deletion event.
