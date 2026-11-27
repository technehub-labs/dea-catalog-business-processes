# CR-BP-241 — Generated README Reconciliation and Conformance-Test Integration

**Status**: Proposed  
**Layer**: Cross-cutting  
**Owner**: Emmanuel A. Otchere  
**Type**: Generated documentation reconciliation and CI regression coverage  
**Depends on**: CR-BP-114; CR-BP-240; CR-BP-251  
**Companion to**: CR-BP-239  
**Baseline**: `4710a9478b039e02aa186af69839ca6c6de79c`

## 1. Purpose

Reconcile the two generated Process Group READMEs made stale by the canonical L1–L2 composition corrections in CR-BP-240, and ensure that the CR-BP-251 conformance-aggregator regression tests execute in the repository's main validation workflow.

The YAML Process Group records remain authoritative. README files are generated projections and must remain byte-identical to the output of `scripts/generate_readmes.py` under CR-BP-114. This CR does not restore removed composition assertions or modify canonical process semantics.

## 2. Investigation Evidence

Post-merge validation run #649 at the CR-BP-251 merge state reported two blocking RDM-001/RDM-002 findings:

- `entities/v1-alpha/fa-conceive/Financial-Model-Conception/README.md`
- `entities/v1-alpha/fa-improve/Financial-Improve/README.md`

The current authoritative Process Group YAML records show:

- Finance Model Conception: one active `composes` assertion, following removal of five out-of-context assertions by CR-BP-240.
- Financial Improve: three active `composes` assertions, following removal of the Audit Policy Compliance assertion by CR-BP-240.
- Both records include a CR-BP-240 entry in `metadata.change_history`.

The committed READMEs still represent the pre-CR-BP-240 composition counts and omit the CR-BP-240 change-history entry. The stale artefacts therefore reflect an omitted regeneration after the source-record change; the evidence does not indicate a generator defect.

The CR-BP-251 regression tests exist, but the main workflow's pytest invocations do not execute `tests/test_conformance_result.py`.

## 3. Scope

1. Regenerate and commit only the two affected Process Group READMEs from their current YAML records using the canonical generator.
2. Preserve all provided human-readable content and all unaffected generated content.
3. Integrate the CR-BP-251 regression test module into `.github/workflows/ci.yml`.
4. Align the live conformance test expectations with the established aggregate contract: zero blocking failures may produce either `CONFORMANT` or `CONFORMANT-WITH-WARNINGS` when advisory findings remain.
5. Retain the existing strict invocation and failed-gate diagnostic assertions.

## 4. Explicit Non-Goals

- No changes to canonical entity YAML, composition relationships, L0 context, ECF coordinates, identity, lifecycle, or process semantics.
- No blanket README regeneration.
- No weakening, demotion, or suppression of any conformance gate.
- No disposition of the four separate advisory backfill/decomposition findings.
- No changes to CR-BP-239 publication model, renderer, release integration, or publication automation.
- No declaration that CR-BP-240 or CR-BP-239 Slice B is closed.

## 5. Acceptance Criteria

- [ ] The two named README files are byte-identical to canonical generator output.
- [ ] The Finance Model Conception README reports one composed L2 process and includes the CR-BP-240 history entry.
- [ ] The Financial Improve README reports three composed L2 processes and includes the CR-BP-240 history entry.
- [ ] `python scripts/generate_readmes.py --check` passes.
- [ ] `python scripts/check_readme_consistency.py --strict` passes with no blocking RDM findings.
- [ ] `tests/test_conformance_result.py` executes in the main `validate-process-entries` workflow and passes.
- [ ] Its live-run tests accept the documented warning-bearing state only when there are zero blocking failures.
- [ ] The aggregate conformance result has zero blocking failures; advisory findings remain visible and unchanged unless separately dispositioned.
- [ ] The strict CR-BP-239 build and Slice B asset validation execute only after the aggregate gate passes.

## 6. Validation Boundary

This CR repairs generated documentation consistency and closes a CI regression-coverage gap. It does not itself establish Slice B publication readiness. That requires a successful post-merge main validation run, strict publication-model build, complete asset validation, and subsequent artifact inspection under CR-BP-239.
