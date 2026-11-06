# CR-BP-232: Human Readability Gate (HUM-001..007) + Provided-Layer Naming Principles

**Status**: Accepted (landed via PR #228; status backfilled post-merge per the immutability rule)
**Layer**: Cross-cutting (catalog documentation layer)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-05
**Depends on**: CR-BP-230 (the five plain-language attributes the gate validates), CR-BP-231 (the profile v3 layout whose Part I sections this gate polices), CR-BP-CE-RL (the posture-flip precedent this gate's wave-closure blocking flip follows), CR-BP-118/118c (the authorship + prose-authorship regime all provided prose lands under)

> **Scope.** Owner directive 2026-11-05 (the nomenclature assessment §7): validation must distinguish three independently assessable quality dimensions — semantic quality, human comprehension, operational clarity — rather than collapsing them into one documentation-completeness score. Semantic quality stays owned by the existing gates (BP-SEM, ECF, BP-SPEC, architectural regression). This CR adds the other two as gate **[51] Human Readability (HUM-001..007)**, a new advisory validator `scripts/check_human_readability.py` over the CR-BP-230 provided fields, plus the naming-principles normative section in the documentation architecture. Posture: **advisory now** (the provided layer is 100% unbackfilled — 18,615 = 3,723 × 5 presence findings at the baseline run); flips **blocking at wave closure** (CR-BP-236), mirroring the CR-BP-CE-RL flip: with all waves landed the blocking profile is 0, so strict mode fails only on NEWLY introduced provided-layer defects.

**Lands against**: `scripts/check_human_readability.py` (new; HUM-001..007; self-test; writes `reconciliation/human-readability-report.yaml` + the posture-engine JSON manifest `human-readability-report.json`); `scripts/conformance_result.py` (gate [51] appended, advisory); `scripts/check_conformance_posture_ext23.py` (CLASSIFICATION + GATE_MANIFEST rows for gates [48]–[51]: [48]/[49]/[50] were landed by CR-BP-EXT-23 / CR-BP-94-EXT-24 / CR-BP-CE-0 without classification rows — the pre-existing C23-02 rot this CR repairs — and [51] is classified `content`/T2 with the manifest feeding REQ-23-03: the posture engine computes the wave-closure promotion itself, `promoted to blocking: 1` at the baseline run); regenerated posture artefacts (`reconciliation/gate-inventory.json`, `conformance-posture-report.json`) + the other reconciliation manifests regenerated in the same tranche; `docs/process-documentation-architecture.md` (§6.2b naming principles); this CR + CHANGELOG + register row. **0 entity-record changes. 0 id changes. 0 existing-gate logic changes.**

## 1. The rule set

| Rule | Dimension | Contract |
|---|---|---|
| HUM-001 | Human comprehension | `plain_language_name` present, 8..200 chars |
| HUM-002 | Human comprehension | `plain_language_description` present, ≥ 40 chars |
| HUM-003 | Human comprehension | `business_purpose` present, ≥ 30 chars |
| HUM-004 | Human comprehension | `practical_context` present, ≥ 30 chars |
| HUM-005 | Human comprehension | Metamodel-jargon denylist over authored prose ("bounded unit of work", "verb-object", "decomposition", canonical-id tokens, level codes, `{{` tokens, ...) — the human layer speaks business, not metamodel |
| HUM-006 | Operational clarity | `worked_example` carries a valid `agent_type` ∈ {human, non-human, mixed} and a narrative ≥ 40 chars |
| HUM-007 | MECE (CR-BP-230 S1) | `plain_language_description` MUST NOT restate the formal `definition` verbatim (normalised containment) |

HUM-001..004 and the presence half of HUM-006 are **population gates**: they drain to 0 as the CR-BP-233..236 waves land. HUM-005, the agent-type half of HUM-006, and HUM-007 are **permanent quality gates** over the provided layer from the first authored record onward.

## 2. What does NOT change

- No existing gate's logic, posture, or rule ids. The three-dimension separation is additive: BP-SEM/ECF remain the sole owners of semantic quality.
- No README, no record, no schema content changes in this CR.
- The gate report (`reconciliation/human-readability-report.yaml`) is a new artefact; no existing reconciliation artefact is touched.

## 3. Verification / Acceptance Criteria

1. Self-test PASS: 6 cases (good record clean; bare record fires HUM-001..004 + HUM-006; jargon fires HUM-005; verbatim restatement fires HUM-007; invalid agent type fires HUM-006; L0 id-pattern level resolution).
2. Baseline corpus run: **18,615 advisory findings, all presence-class** (3,723 × {HUM-001, HUM-002, HUM-003, HUM-004, HUM-006}); HUM-005/007 = 0 (no authored prose yet); report committed.
3. Gate [51] appears in `conformance_result.py` as advisory and does not flip the pipeline verdict (CONFORMANT-WITH-WARNINGS at worst).
4. `check_cr_metadata.py --strict` green on this CR file.
