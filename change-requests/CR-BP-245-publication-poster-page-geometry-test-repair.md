# CR-BP-245 — Publication Poster Page-Geometry Test Constant Repair

**Status**: Proposed  
**Layer**: Cross-cutting  
**Owner**: Emmanuel A. Otchere  
**Type**: Test-constant repair and validation  
**Depends on**: CR-BP-239  
**Baseline**: `1ea72000` (PR #256 merge; CR-BP-243 implementation)

## 1. Purpose

Repair the failing `tests/test_publication_renderers.py::test_pdf_and_png_are_from_a_single_a1_page_when_dependencies_exist` assertion that is the remaining cause of the red `validate` job after CR-BP-243 restored aggregate conformance to zero blocking findings.

## 2. Evidence and Diagnosis

- Validation runs #46020116524 (PR #256) and #46093215456 (post-merge main) fail only at the step "Build strict CR-BP-239 publication model and Slice B assets" with:
  `AssertionError: assert 1542.0500000000002 < 1.5` at `tests/test_publication_renderers.py:174`.
- The poster stylesheet has specified `@page { size: A1 landscape; margin: 8mm; }` at `scripts/render_publication_assets.py:137` since the file was introduced (commit `5978c669`, CR-BP-239 Slice B). A1 landscape in PDF points is 2383.94 × 1683.78 pts; the observed width 841.89 + 1542.05 = 2383.94 pts matches the CSS exactly.
- The test constants added in commit `5ddae8f4` assert `841.89` × `594.95` pts while commenting them "A1 landscape width/height" — but 841.89 × 594.95 pts are the **A4 landscape** dimensions. The test therefore encodes A4 geometry against an A1 poster stylesheet.
- The failure is independent of entity content: the test builds a synthetic publication model (`_model(tmp_path)`), not repository READMEs or records, so CR-BP-243's README regeneration cannot be implicated. The step was simply never reached in earlier red runs because the job failed earlier on RDM-001.
- Diagnosis: the renderer honours its long-standing A1 CSS; the test's geometry constants are wrong (mm-value/pt confusion: 841 × 594 are A1 dimensions in **mm**, not pts).

## 3. Scope

1. Correct the expected page-geometry constants in `tests/test_publication_renderers.py` to the A1 landscape point values the stylesheet specifies (2383.94 × 1683.78 pts, tolerance unchanged), keeping the "single A1 page" semantics of the test name.
2. Run `python -m pytest -q tests/test_publication_model.py tests/test_publication_renderers.py` in an environment with poppler (`pdftoppm`) and weasyprint, as CI installs them.
3. Confirm the "Build strict CR-BP-239 publication model and Slice B assets" CI step passes.

## 4. Explicit Non-Goals

- No change to `scripts/render_publication_assets.py` or the `@page` CSS: the A1 poster is the long-standing CR-BP-239 Slice B design; shrinking the poster to A4 would be a publication-model change requiring an explicit CR-BP-239 owner decision, not a test repair.
- No weasyprint/poppler version pinning or CI dependency changes.
- No weakening of the test (the Pages: 1 and stable-content assertions remain).
- No claim of CR-BP-239 Slice B closure or release readiness.

## 5. Acceptance Criteria

- [ ] The page-geometry constants match the A1 landscape point geometry of the committed stylesheet.
- [ ] `tests/test_publication_renderers.py` passes locally with poppler + weasyprint present.
- [ ] The CI step "Build strict CR-BP-239 publication model and Slice B assets" passes on the implementation PR.
- [ ] The change request register includes CR-BP-245.

## 6. Validation Boundary

This CR repairs a test-constant defect only. Publication-model semantics, asset content, and Slice B readiness remain governed by CR-BP-239 and its downstream validation.

## 7. Evidence

- Post-CR-BP-243 main run #46093215456: https://github.com/technehub-labs/dea-catalog-business-processes/actions/runs/46093215456
- PR #256 run #46020116524: https://github.com/technehub-labs/dea-catalog-business-processes/actions/runs/46020116524
- Stylesheet: `scripts/render_publication_assets.py:137` (`@page { size: A1 landscape; }`, since `5978c669`)
- Test constants: `tests/test_publication_renderers.py:174-175` (since `5ddae8f4`)
