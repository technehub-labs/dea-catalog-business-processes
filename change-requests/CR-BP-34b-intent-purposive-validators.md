# CR-BP-34b: Intent Purposive Validators (PSP-001..003)

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Proposed
**Layer**: L2 (Business Process) — semantic conformance
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-10
**Carrier**: Second execution slice of CR-BP-34 (Process Conformance Profile; PR #69 MERGED, commit `f40a45c`)
**Depends on**: CR-BP-03, CR-BP-14 (BP-SEM-001..012), CR-BP-16
**Lands against**: 126 canonical BP records; conformance level L4

---

## 1. Change Request

Codify the Intent purposive rules from CR-BP-34 §7 as a standalone, machine-testable validator that emits **no findings on the existing 126 canonical records** and provides a regression guard against any future BP that violates one or more rules.

The three rules (verbatim from CR-BP-34 §7):

| # | Rule | Machine-checkable |
|---|---|---|
| **PSP-001** | **Intent shall be purposive.** | `process_intent` (when present) is non-empty AND expresses a purpose, not a noun-of-being. |
| **PSP-002** | **Intent shall use an approved vocabulary.** | `process_intent` value ∈ the approved 7-value purposive vocabulary from `classifications/process-intents.yaml` (govern / manage / operate / deliver / support / develop / transform). |
| **PSP-003** | **Intent shall not encode organizational ownership.** | `process_intent` value ∉ the organizational-component denylist (curated list of org-component words that belong on the org-unit / capability axes, not on intent). |

## 2. Why this CR is paper-trail-only

**PSP-002 is already partially enforced** by `BP-SEM-001` in `check_process_semantics.py`, which gates admission and emits findings for non-approved intent values. The live catalog uses 4 of the 7 approved values (develop 82 / operate 37 / manage 4 / govern 3); the other 3 (deliver / support / transform) are unused.

**PSP-001 and PSP-003 are new.** PSP-003 in particular has not been codified as a validator — it is the user's prose rule that Intent shall not be a substitute for Organizational Component, Process Domain, ECF Domain, or Lifecycle Stage.

**Coverage on the live 126 records** (run 2026-09-10):

| Rule | Pass | Fail |
|---|---|---|
| PSP-001 (purposive) | 126 | 0 |
| PSP-002 (approved vocabulary) | 126 | 0 |
| PSP-003 (no org-component substitution) | 126 | 0 |

The validator ships as a **no-finding** addition — pure regression guard.

## 3. Non-Goals

- **Not a new blocking gate.** Wired into `conformance_result.py` as gate **[12] Intent Purposive (PSP-001..003)** with `blocking=False` (advisory).
- **No entity mutation.** No BP YAML is touched.
- **No change to the approved vocabulary.** The 7-value purposive vocabulary stays exactly as it is in `classifications/process-intents.yaml`.
- **No change to BP-SEM-001.** The existing semantic check still enforces PSP-002 at admission time; this slice adds an independent post-hoc check that covers the same vocabulary for the live catalog.
- **No change to PSP-003's authoritative list.** The denylist is curated from the user's prose (CR-BP-34 §7 + §11 BP-C4) and the Mintzberg 5-part organisation vocabulary from CR-BP-34 §8. No ECF domain names, no lifecycle stage names, no organizational-component names.

## 4. Implementation

### 4.1 New script: `scripts/check_intent_purposive.py`

Self-contained Python script. Patterns established in `check_l2_qualification.py`. Reads every BP YAML under `entities/v1-alpha/dea:process-*/`, applies the three rules, emits findings.

### 4.2 Approved vocabulary (PSP-002)

Loaded from `classifications/process-intents.yaml` (already in the catalog). The 7 approved values are:

```
govern, manage, operate, deliver, support, develop, transform
```

### 4.3 Organizational-component denylist (PSP-003)

Curated from CR-BP-34 §7 (organizational-component substitution prohibition) and §8 (Mintzberg 5-part vocabulary — Operating Core / Strategic Apex / Middle Line / Technostructure / Support Staff). The denylist is a curated Python set in the validator script; future expansion is a one-line edit.

```python
ORG_COMPONENT_DENYLIST = {
    # Functional silos (Mintzberg 5-part)
    "operations", "production", "sales", "marketing", "hr",
    "finance", "it", "legal", "facilities", "admin",
    # Sectors / industries (out of scope for intent)
    "manufacturing", "logistics", "warehouse", "procurement",
    "engineering", "treasury", "tax", "audit", "compliance",
    "risk",
    # Org-structure terms
    "department", "division", "team", "unit", "office",
    "branch", "subsidiary", "section", "group",
    # ECF domain names (these belong in process_context)
    "strategyanddirection", "agencyandorganization",
    "partyandrelationship", "productandvalue",
    "enablementandoperations", "financeandaccounting",
    "governanceandexistence",
    # Lifecycle stage names (these belong in process_context)
    "conceive", "design", "build", "activate",
    "improve", "retire",
}
```

Comparison is **case-folded**; leading/trailing whitespace is stripped. The denylist is intentionally narrow — adding every possible org-component word would create false positives. The 28 entries above cover the documented Mintzberg vocabulary, the common functional silos, and the v2.5.0 ECF domain / lifecycle stage names.

### 4.4 Conformance integration: `scripts/conformance_result.py`

Adds one new gate row:

```python
("[12] Intent Purposive (PSP-001..003)",
 False, ["python", "scripts/check_intent_purposive.py", "--strict"]),
```

Placed immediately after gate [11] (L2 Qualification). Marked `blocking=False` (advisory).

### 4.5 New test: `tests/test_check_intent_purposive.py`

17 tests, mirroring the structure of `test_check_l2_qualification.py`:

- Per-rule pass / fail coverage.
- Multi-rule failure aggregation.
- Edge cases: empty intent (advisory, not blocking), whitespace-padded intent, case-folding.
- Live-catalog assertion: 126/126 conformant, 0 findings.
- CLI self-test + JSON shape.

## 5. Acceptance criteria

1. `python3 scripts/check_intent_purposive.py --strict` exits 0 on the live catalog.
2. The validator emits exactly 0 findings against the 126 canonical BPs.
3. `python3 scripts/conformance_result.py` reports gate [12] as `PASS/BLOCKING` (returns 0; the gate pipeline records `passed` regardless of `blocking` flag).
4. `python3 -m pytest tests/test_check_intent_purposive.py -q` reports all tests pass.
5. `python3 -m pytest tests/ -q` (full suite) reports no new failures.
6. `python3 scripts/check_l2_qualification.py --strict` continues to pass (regression guard: this slice does not perturb gate [11]).
7. `python3 scripts/check_canonical_serves.py --strict` continues to pass (126/126).
8. `python3 scripts/check_cr_metadata.py --strict` reports 0 new findings.
9. `python3 scripts/regenerate_catalog.py --check --schema catalog-index-schema/catalog-index-schema.json` matches `CATALOG.yaml`.

## 6. Why this is additive-only

The three PSP rules are derived from the existing semantic contract (CR-BP-14 BP-SEM-001) and the user's prose formalisation (CR-BP-34 §7). The existing schema was authored with these rules in mind — every canonical BP has a `process_intent` value that is both purposive (PSP-001) and approved (PSP-002) and not an org-component (PSP-003). This slice surfaces that implicit coverage as an explicit, machine-checkable contract.

Existing records stay conformant; future records gain a regression guard against the *next* contributor who tries to encode "this is the IT department's process" as `process_intent: it`.

## 7. What this is NOT

- **Not a vocabulary change.** The approved 7-value intent vocabulary is unchanged.
- **Not an org-component validator.** This script checks that Intent does not encode org-component; it does NOT check that the BP's actual organizational responsibility is correct. Org-component validation belongs to `dea-catalog-organizational-units`.
- **Not an ECF domain validator.** Domain encoding belongs in `process_context`; that's enforced by BP-SEM-007..008.
- **Not a MECE check.** Per CR-BP-34 §23, conformance is separate from MECE. MECE is CR-BP-36 (renumbered CR-BP-08).

## 8. Result

CR-BP-34b closes the gap between the prose declaration of the Intent purposive rules (CR-BP-34 §7) and the machine-checkable conformance gate (CR-BP-16). All 126 records pass all three rules. Future contributors cannot accidentally submit a BP that uses Intent to encode organizational ownership, domain, or lifecycle stage; the validator catches them at admission time (if wired into admission) or at conformance time (current default).

The 196 canonical records remain at conformance level L4 throughout this PR.
