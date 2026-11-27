# CR-BP-243 — Canonical README Regeneration Reconciliation

**Status**: Proposed  
**Layer**: Cross-cutting  
**Owner**: Emmanuel A. Otchere  
**Type**: Generated-artifact repair and validation  
**Depends on**: CR-BP-114; CR-BP-240; CR-BP-241; CR-BP-242  
**Baseline**: `175f8cb70ede4ef4bd53b251dfbdfc57934fdcd9` (PR #253 merge)

## 1. Purpose

Resolve the two blocking README Consistency (CR-BP-114 / RDM-001) findings that remain after CR-BP-241, by producing the affected README files using the canonical generator and verifying exact byte identity. Preserve the canonical YAML records, their semantics, and the blocking consistency gate.

This CR corrects CR-BP-241's implementation evidence and outcome. It does not presume a generator defect or accept manually reconstructed output as generated.

## 2. Evidence and Diagnosis

Post-merge main validation run #45945322556 (commit `175f8cb70ede4ef4bd53b251dfbdfc57934fdcd9`) completed with failure. Aggregate diagnostics explicitly identify exactly two blocking RDM-001 findings:

- `entities/v1-alpha/fa-conceive/Financial-Model-Conception/README.md`
- `entities/v1-alpha/fa-improve/Financial-Improve/README.md`

Both are reported as `stale (content differs from generator output)`. The live evaluator—not a manually inferred comparison—confirms the blocking discrepancy. The authoritative source records have the CR-BP-240 hierarchy changes: Finance Model Conception has one active `composes` assertion; Financial Improve has three active `composes` assertions. The records' source change-history entries are present.

PR #252 manually reconciled the visible composition tables, decomposition sections and change-history rows, but post-merge validation proves those commits did not achieve canonical byte identity. Do not characterize the exact byte differences until generator output is captured and compared.

## 3. Scope

1. Execute the canonical `scripts/generate_readmes.py` from the exact baseline checkout in a repository-capable environment.
2. Generate only the two named README targets using the generator's supported scoped invocation, or generate the full tree only if the scope mechanism cannot isolate these records; if broader generation is unavoidable, commit only the two targets and record the full-tree drift inventory as evidence.
3. Capture the committed-versus-generated exact diff before replacing files. Establish whether differences are formatting, generated section content, relationship projection, metadata, or another source-derived detail.
4. Replace the two README files with actual generator-produced output. No hand-authoring or synthetic reconstruction.
5. Run `python scripts/generate_readmes.py --check` and `python scripts/check_readme_consistency.py --strict`.
6. Run `python -m pytest -q tests/test_generate_readmes.py tests/test_check_readme_consistency.py tests/test_conformance_result.py`.
7. Run main post-merge validation and resume the chain only after aggregate conformance has zero blocking findings.
8. Reconcile the CR register and generated `CATALOG.yaml` open-CR count to include CR-BP-243 as Proposed (10 open CRs at this baseline).
9. Preserve advisory findings, including documentation backfill and EXT-22 reconciliation, without treating them as resolved by this CR.

## 4. Explicit Non-Goals

- No canonical entity YAML, process hierarchy, relationship semantics, identity, lifecycle, ECF coordinates or source history changes.
- No manual README editing to mimic the generator.
- No change to the generator or README consistency gate unless captured byte-diff evidence demonstrates an actual generator defect, in which case a separate narrowly scoped CR is required.
- No suppression, demotion or weakening of RDM-001.
- No advisory backfill disposition.
- No publication-model, release, asset-generation or automation changes under CR-BP-239.

## 5. Acceptance Criteria

- [ ] Exact generator output for each target is captured from the baseline checkout.
- [ ] A committed-versus-generated diff is retained in the PR evidence (or attached CI artifact), explaining the stale bytes.
- [ ] Only the two target README files are changed, unless a separately approved generator defect CR is required.
- [ ] Both targets are byte-identical to canonical generator output.
- [ ] Generator check mode passes.
- [ ] Strict README consistency reports zero blocking findings.
- [ ] Generator, README consistency and conformance-result test modules pass.
- [ ] Post-merge main validation reaches aggregate conformance and reports zero blocking failures.
- [ ] The CR register entry and generated `CATALOG.yaml` open-CR count reconcile for CR-BP-243.
- [ ] Advisory findings remain visible and are not represented as closed.
- [ ] Downstream CR-BP-238/239 stages run only after aggregate conformance passes; their results are reviewed separately.

## 6. Execution and Validation Boundary

The GitHub Actions run #45945322556 supplies the exact failure evidence, but this task requires executing the generator against the repository checkout. If execution cannot be performed in the available environment, the implementation PR must remain uncreated; a CR tracking PR may record the scope and evidence, but cannot claim the README repair or acceptance criteria as complete.

## 7. Evidence

- Main run #45945322556: https://github.com/technehub-labs/dea-catalog-business-processes/actions/runs/45945322556
- PR #252 (CR-BP-241): https://github.com/technehub-labs/dea-catalog-business-processes/pull/252
- PR #253 (CR-BP-242): https://github.com/technehub-labs/dea-catalog-business-processes/pull/253
