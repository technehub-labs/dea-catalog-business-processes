# CR-BP-34a: L2 Qualification Validators (BP-C1..C4)

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Proposed
**Layer**: L2 (Business Process) — conformance
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-10
**Carrier**: First execution slice of CR-BP-34 (Process Conformance Profile; renumbered from CR-BP-06; PR #69 MERGED, commit `f40a45c`)
**Depends on**: CR-BP-03 (Business Process Architecture), CR-BP-14 (Process Semantic Reconciliation), CR-BP-16 (Conformance Gate)
**Lands against**: 126 canonical Business Process records; conformance level L4

---

## 1. Change Request

Codify the four L2 qualification criteria from CR-BP-34 §11 as a standalone, machine-testable validator that emits **no findings on the existing 126 canonical records** and provides a regression guard against any future BP that violates one or more criteria.

The four criteria (verbatim from CR-BP-34 §11):

| # | Rule | Machine-checkable field |
|---|---|---|
| **BP-C1** | **Input–Output Transformation** — the process transforms identifiable inputs into outputs or an equivalent defined result. | `trigger` (input) non-empty AND `outcome` (output) non-empty |
| **BP-C2** | **Objective Contribution** — the process makes a recognizable contribution to an enterprise objective or outcome. | `identity.outcome_statement` non-empty |
| **BP-C3** | **Standalone Executability** — the process represents a coherent unit of work that can be independently identified and performed. | `lifecycle_status` present AND `id` matches `dea:process-[a-z0-9-]+` |
| **BP-C4** | **Resource Dedication** — the process requires identifiable resources or responsibility sufficient to constitute a distinct process boundary. | `identity.evidence_links` non-empty AND `metadata.change_history` (or `change_history`) has at least one entry |

## 2. Why this CR is paper-trail-only

CR-BP-34 §11 declares the four criteria in prose. The existing CR-BP-16 conformance gate enforces some of them implicitly (BP-SEM-007..009 touch BP-C1, BP-C3; BP-ARC-ID-002..003 touch BP-C1, BP-C2), but there is no single validator that codifies all four together as the formal L2 qualification test. This CR makes that codification explicit and machine-checkable.

**Coverage analysis on the live 126 records** (run 2026-09-10):

| Criterion | Pass | Fail |
|---|---|---|
| BP-C1 (Input–Output Transformation) | 126 | 0 |
| BP-C2 (Objective Contribution) | 126 | 0 |
| BP-C3 (Standalone Executability) | 126 | 0 |
| BP-C4 (Resource Dedication) | 126 | 0 |

All 126 records pass all four criteria. The validator ships as a **no-finding** addition to the conformance suite — it is a regression guard, not a new gate that would block any existing record.

## 3. Non-Goals

- **Not a new blocking gate.** `scripts/check_l2_qualification.py` is added to `scripts/conformance_result.py` as gate **[11] L2 Qualification (BP-C1..C4)** with `blocking=False` (advisory only). Existing records stay at conformance level L4.
- **No entity mutation.** No BP YAML is touched by this PR.
- **No schema change.** No `schemas/` addition; the four criteria are checked against the existing canonical shape.
- **No disposition-register change.** The 18 disposition records and the 107 RETAIN / 18 RECLASSIFY / 1 MOVE totals are unaffected.
- **No new admission rule.** This is a post-hoc catalog-wide check, not an admission gate; admission remains governed by `check_admission_gate.py` (ADM-001..008).

## 4. Implementation

### 4.1 New script: `scripts/check_l2_qualification.py`

Self-contained Python script. Patterns established in `check_process_semantics.py` and `check_process_identity.py`. Reads every BP YAML under `entities/v1-alpha/dea:process-*/`, applies the four rules, emits findings as `(rule_id, record_id, diagnostic)` tuples. Exit codes:

- `0` — all 126+ records pass all four rules
- `1` — at least one rule failed (advisory under `--strict`; blocking only if the CI is configured for it)
- `2` — self-test failure or I/O error

Supports `--self-test`, `--json`, `--catalog-root` flags consistent with the other checkers.

### 4.2 Conformance integration: `scripts/conformance_result.py`

Adds one new gate row:

```python
("[11] L2 Qualification (BP-C1..C4)",
 False, ["python", "scripts/check_l2_qualification.py", "--strict"]),
```

Placed after gate [10] (Conformance Result Levels 1-4) and before the closing entry. Marked `blocking=False` (advisory) so existing records are unaffected. Position [11] is reserved for future L2/L3/L4 qualification gates; this is the first one.

### 4.3 New test: `tests/test_check_l2_qualification.py`

Mirrors the structure of `tests/test_check_process_semantics.py`:

- Constructs a small temp catalog with BPs that pass / fail each of the four rules.
- Asserts that the validator returns the expected exit code and finding list.
- Includes a "fixed catalog" assertion (every rule passes, exit 0).

### 4.4 README pointer: `change-requests/README.md`

Adds a row to the CR index: `CR-BP-34a` row with status `Merged (this PR)` once merged.

## 5. Acceptance criteria

1. `python3 scripts/check_l2_qualification.py --strict` exits 0 on the live catalog.
2. The validator emits exactly 0 findings against the 126 canonical BPs.
3. `python3 scripts/conformance_result.py` reports the new gate as `PASS/BLOCKING` (since it returns 0 — the gate pipeline records `passed` regardless of the `blocking` flag).
4. `python3 -m pytest tests/test_check_l2_qualification.py -q` reports all tests pass.
5. `python3 -m pytest tests/ -q` (full suite) reports no new failures.
6. `python3 scripts/check_cr_metadata.py --strict` reports 0 new findings.
7. `python3 scripts/regenerate_catalog.py --check --schema catalog-index-schema/catalog-index-schema.json` matches `CATALOG.yaml`.
8. `python3 scripts/check_canonical_serves.py --strict` continues to pass (126/126).

## 6. Why this is additive-only

The four L2 criteria are derived from the existing canonical schema (CR-BP-03 + CR-BP-14). The existing schema was authored with these criteria in mind, even though the criteria were not codified as a standalone validator. This CR surfaces that implicit coverage as an explicit, machine-checkable contract. Existing records stay conformant; future records gain a regression guard.

## 7. What this is NOT

- **Not a BP-C1..C4 enrichment campaign.** No BP YAML is updated to satisfy a new requirement — they all already satisfy them.
- **Not a MECE validation.** CR-BP-34 §23 explicitly separates conformance from MECE. MECE is CR-BP-36 (renumbered CR-BP-08).
- **Not an Activity / Workflow addition.** CR-BP-34a is a L2-only validator. CR-BP-32 (Activity Model) and CR-BP-33 (Execution Boundary) are separate slices.
- **Not an intent / specialization validator.** Those are covered by `check_process_semantics.py` (BP-SEM-001..012) and `check_process_specialization.py` (BP-SPEC-01-001..007).

## 8. Result

CR-BP-34a closes the gap between the prose declaration of the L2 qualification test (CR-BP-34 §11) and the machine-checkable conformance gate (CR-BP-16). All 126 records pass all four criteria. Future contributors cannot accidentally submit a BP that fails any of the four; the validator catches them at admission time (if wired into admission) or at conformance time (current default).

The 196 canonical records remain at conformance level L4 throughout this PR.
