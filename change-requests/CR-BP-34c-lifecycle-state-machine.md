# CR-BP-34c: Lifecycle State-Machine Validator (LCM-001..005)

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Proposed
**Layer**: L2 (Business Process) — lifecycle governance
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-10
**Carrier**: Third execution slice of CR-BP-34 (Process Conformance Profile; PR #69 MERGED, commit `f40a45c`)
**Depends on**: CR-BP-03, CR-BP-14 (BP-SEM-001..014), CR-BP-16, CR-BP-34a (BP-C4 Resource Dedication; PR #70 MERGED)
**Lands against**: 126 canonical BP records; conformance level L4

---

## 1. Change Request

Codify the lifecycle state-machine rules from CR-BP-34 §10 as a standalone, machine-testable validator that emits **no findings on the existing 126 canonical records** and provides a regression guard against any future BP that violates a lifecycle rule.

The five rules (derived from CR-BP-34 §10):

| # | Rule | Machine-checkable |
|---|---|---|
| **LCM-001** | **`lifecycle_status` vocabulary.** Value ∈ approved vocabulary. Approved set = 6-state machine ∪ legacy compatibility (`candidate`, `deprecated`). | `lifecycle_status` ∈ `{draft, proposed, validated, published, deprecated, retired, candidate}`. |
| **LCM-002** | **`status` ↔ `lifecycle_status` consistency.** The legacy `status` field must be consistent with `lifecycle_status`. | `status == lifecycle_status`, OR both are in legacy compatibility set. |
| **LCM-003** | **Deprecation audit trail.** A deprecated record must carry evidence of the deprecation transition in `change_history`. | `lifecycle_status == "deprecated"` ⇒ at least one `change_history` entry contains the marker `"DEPRECATED"` (case-insensitive substring). |
| **LCM-004** | **No zombie deprecation markers.** A non-deprecated record must not carry a deprecation marker. | `lifecycle_status != "deprecated"` ⇒ no `change_history` entry contains `"DEPRECATED"` (case-insensitive substring). |
| **LCM-005** | **Retired records live in archive.** When retired records are introduced (forward), they MUST be moved out of `entities/v1-alpha/` into a sibling archive directory. | `lifecycle_status == "retired"` ⇒ the record's path is under `entities/_retired/` (forward-only; no findings today because no retired records exist). |

## 2. Why this CR is paper-trail-only

CR-BP-34 §10 declares the 6-state lifecycle machine. The existing CR-BP-16 gate (gate [3] Legacy Migration) touches lifecycle only insofar as legacy values are accepted during migration. There is no validator today that:

1. Catches typos in `lifecycle_status` (e.g. `Draft`, `validated-proposed`).
2. Catches drift between the `status` field and the `lifecycle_status` field.
3. Catches silent deprecation (a record marked deprecated without a `change_history` entry explaining the transition).
4. Catches stale deprecation markers (a record's `change_history` says "DEPRECATED" but the lifecycle_status was rolled back to `candidate`).
5. Enforces that retired records are archived (forward-only).

**Coverage on the live 126 records** (run 2026-09-10):

| Rule | Pass | Fail |
|---|---|---|
| LCM-001 (vocabulary) | 126 | 0 |
| LCM-002 (status ↔ lifecycle_status) | 126 | 0 |
| LCM-003 (deprecation audit trail) | 1 (the one deprecated BP) | 0 |
| LCM-004 (no zombie markers) | 125 (all non-deprecated) | 0 |
| LCM-005 (retired records archived) | n/a (no retired records exist) | n/a |

The validator ships as a **no-finding** addition — pure regression guard.

## 3. The 6-state machine (CR-BP-34 §10)

```
       ┌──────────┐
       │  draft   │  Initial proposal; not yet reviewed
       └────┬─────┘
            │ propose
            ▼
       ┌──────────┐
       │ proposed │  Submitted for review
       └────┬─────┘
            │ validate (criteria satisfied)
            ▼
       ┌──────────┐
       │validated │  Review passed; pending publication
       └────┬─────┘
            │ publish (released in catalog)
            ▼
       ┌──────────┐
       │published │  Live in catalog; canonical reference
       └────┬─────┘
            │ deprecate   (superseded or no longer canonical)
            ▼
       ┌──────────┐
       │deprecated│  No longer recommended; remains visible
       └────┬─────┘
            │ retire (removed from catalog)
            ▼
       ┌──────────┐
       │ retired  │  Removed; archive only
       └──────────┘
```

**Allowed transitions** (declared for documentation; transition validation is a separate slice):

- `draft → proposed, retired`
- `proposed → draft, validated, retired`
- `validated → proposed, published, retired`
- `published → validated, deprecated, retired`
- `deprecated → published, retired`
- `retired → (terminal)`

**Note:** transition validation (e.g. "you cannot go from `draft` directly to `published`") requires reading `change_history` for the audit trail, which is heavier work. This slice codifies the **per-record invariants** (LCM-001..005) but defers the **transition-machine validator** to CR-BP-34c.1 if and when needed.

## 4. Migration policy (NOT in this PR)

The live catalog currently uses **two** lifecycle values: `candidate` (125 records) and `deprecated` (1 record). The 6-state machine is the **target vocabulary for new records**. Migration of the 125 `candidate` records to `validated` or `published` is **explicitly out of scope** for this PR. When migration happens, it will be:

1. A separate CR (proposed: `CR-BP-34c.1`).
2. A coordinated batch with CR-BP-12 (L1 Process Group Profile) and CR-BP-13..16 (which currently reference `candidate` in their governance rules).
3. Backed by a per-domain disposition analysis (per the established CR-BP-22 disposition pattern).

For now, the legacy compatibility set `{candidate, deprecated}` is honored by LCM-001.

## 5. Non-Goals

- **Not a vocabulary migration.** The 125 `candidate` records stay as `candidate`. Migration is a future CR.
- **Not a transition-machine validator.** Per-record invariants only; transition validation is CR-BP-34c.1.
- **Not a new blocking gate.** Wired into `conformance_result.py` as gate **[13] Lifecycle State-Machine (LCM-001..005)** with `blocking=False` (advisory).
- **No entity mutation.** No BP YAML is touched.
- **No change to `status` semantics.** The `status` field remains a legacy alias for `lifecycle_status`; LCM-002 codifies the alias relationship.

## 6. Implementation

### 6.1 New script: `scripts/check_lifecycle_state.py`

Self-contained Python script. Patterns established in `check_l2_qualification.py` and `check_intent_purposive.py`. Reads every BP YAML under `entities/v1-alpha/dea:process-*/`, applies the five rules, emits findings.

### 6.2 Approved vocabulary (LCM-001)

```python
APPROVED_LIFECYCLE_STATES = {
    # 6-state machine (CR-BP-34 §10)
    "draft", "proposed", "validated", "published", "deprecated", "retired",
    # Legacy compatibility set (CR-BP-21a..21f historical usage)
    "candidate",
}
```

`deprecated` is in both sets because the live catalog has 1 record using it (the BP that was migrated to a new id under CR-BP-21a). The 6-state machine also has `deprecated` as a first-class state, so the legacy value and the target value happen to coincide.

### 6.3 Conformance integration: `scripts/conformance_result.py`

```python
("[13] Lifecycle State-Machine (LCM-001..005)",
 False, ["python", "scripts/check_lifecycle_state.py", "--strict"]),
```

Placed after gate [12] (Intent Purposive). Marked `blocking=False`.

### 6.4 New test: `tests/test_check_lifecycle_state.py`

~20 tests covering per-rule pass / fail / edge cases + live-catalog assertion + CLI self-test + JSON shape + the `change_history` substring-match behavior.

## 7. Acceptance criteria

1. `python3 scripts/check_lifecycle_state.py --strict` exits 0 on the live catalog.
2. The validator emits exactly 0 findings against the 126 canonical BPs.
3. `python3 scripts/conformance_result.py` reports gate [13] as `PASS/ADVISORY`.
4. `python3 -m pytest tests/test_check_lifecycle_state.py -q` reports all tests pass.
5. `python3 -m pytest tests/ -q` (full suite) reports no new failures.
6. Gates [11] (L2 Qualification) and [12] (Intent Purposive) regression guards remain PASS.
7. `python3 scripts/check_canonical_serves.py --strict` continues to pass (126/126).
8. `python3 scripts/check_cr_metadata.py --strict` reports 0 new findings.
9. `python3 scripts/regenerate_catalog.py --check` matches `CATALOG.yaml`.

## 8. Result

CR-BP-34c closes the gap between the prose declaration of the lifecycle state-machine (CR-BP-34 §10) and the machine-checkable conformance gate (CR-BP-16). All 126 records satisfy all five rules. Future contributors cannot accidentally submit a BP with a typo'd lifecycle value, with drift between `status` and `lifecycle_status`, with a silent deprecation, or with a stale deprecation marker; the validator catches them at conformance time.

The 196 canonical records remain at conformance level L4 throughout this PR.
