# CR-BP-CE-RL: Completeness Gate Posture Flip and Programme Closure

**Status**: Proposed
**Layer**: Process Catalog (Governance)
**Owner**: Emmanuel A. Otchere
**Depends on**: CR-BP-CE-0, CR-BP-CE-L0, CR-BP-CE-L1, CR-BP-CE-L2, CR-BP-CE-L4, CR-BP-CE-REC-1
**Companion to**: CR-BP-94-EXT-24

> **Scope.** The final slice of the completeness programme. All five level
> tranches have landed (L0: 43 blocking -> 0, #202; L1: 49 owner
> candidates, #204; L2: 290 adopted fields, #206; L4: 581 vocabulary/scope
> repairs, #208; numbering reconciled, #209/#210). This CR flips gate
> **[50] Completeness Profiles** from advisory to **blocking** in the
> `conformance_result.py` registry, so newly introduced completeness
> defects fail CI, while the deliberately-deferred knowledge-dependent
> findings (CE-L2-006 `actors`/`stakeholders` candidates) remain advisory
> until the GOV-002/GOV-003 sweep closes them.

---

## 1. The posture decision (normative)

### 1.1 The blocking flip

`scripts/conformance_result.py` gate [50] changes:

```python
("[50] Completeness Profiles (CR-BP-CE-0; CE-000..CE-900)",
 True, ["python3", "scripts/check_completeness.py", "--strict"]),
```

- **Before:** `False, ["python3", "scripts/check_completeness.py", "--advisory"]`
- **After:** `True, [..., "--strict"]`

### 1.2 Why the flip is safe now

The gate's `--strict` mode returns rc=1 **only on blocking findings**
(`scripts/check_completeness.py`: `return 1 if (a.strict and blocking)
else 0`). The blocking profile is already at **0 across all 3,723
records** (the L0 tranche's remediation). The 290 remaining advisory
findings are all CE-L2-006 `actors`/`stakeholders` candidates —
knowledge-dependent fields with no evidence-bound source, deferred per
the §5 provenance policy and reaffirmed by CR-BP-CE-L2 §2.3. They do not
fail strict mode and do not block CI.

### 1.3 What the flip protects against

From this slice forward, any change that introduces a **schema-profile
gap** (a required field removed or emptied on a ProcessContext,
ProcessGroup, Process, Activity, or Task record; a prohibited field
added; a Task `responsibility` outside the 5-phase vocabulary) fails
the aggregate conformance verdict and blocks the PR. The completeness
defect class that produced the original 43 blocking + 1,167 advisory
findings can no longer re-enter the catalogue silently.

### 1.4 The CE-L2-006 carve-out (explicit, time-bound)

The 290 CE-L2-006 findings remain advisory by design. They close via the
human governance sweep: GOV-002/GOV-003 assign `actors`/`stakeholders`
and confirm the 194 proposed `owner` candidates (49 PGs + 145 BPs;
review due 2026-12-31 per the EXT-24 ownership register). If the sweep
has not closed them by the register's review date, the deferral is
revisited as a governance exception (the EXT-23 exception lifecycle
applies: scoped, owned, reviewable, revocable, time-bound).

## 2. What this slice lands

1. The registry flip in `scripts/conformance_result.py` (gate [50]:
   advisory -> blocking; `--advisory` -> `--strict`).
2. The test updates: `tests/test_conformance_result.py` expectations
   where they assert the advisory posture of gate [50].
3. This CR document; CHANGELOG; the change-requests README registration;
   CATALOG.yaml post-commit regeneration.

## 3. What is NOT changed

- The gate's rule set, severities, and report artifact
  (`reconciliation/completeness-report.yaml`, CE-900) — the flip is
  invocation-only.
- No canonical record, schema, or other gate is touched.
- The MECE cross-level relationship validator (`§4` of the umbrella,
  the "New MECE validator" note) is **not** landed by this slice; it
  remains a separate follow-on CR as the umbrella text states.

## 4. Verification

- `python scripts/check_completeness.py --strict` — rc=0 (0 blocking;
  290 advisory remain, by design).
- `python scripts/conformance_result.py` — gate [50] now blocking and
  PASSING.
- The aggregate verdict remains CONFORMANT.

## 5. Programme closure state

| Slice | PR | Outcome |
|---|---|---|
| CE-0 umbrella + gate | #201/#209 | baseline + R1-R7 reconciliation |
| CE-L0 | #202 | 43 blocking -> 0 |
| CE-L1 | #204 | 49 owner candidates |
| CE-L2 | #206 | 290 adopted fields |
| CE-L4 | #208 | 581 vocabulary/scope repairs |
| CE-REC-1 | #210 | numbering reconciled |
| **CE-RL (this slice)** | — | **gate [50] blocking; programme closed** |

Open governance items (owner: GOV-002/GOV-003; due 2026-12-31):
- The 290 CE-L2-006 `actors`/`stakeholders` assignments.
- The 194 proposed `owner` candidate confirmations.

**D-004 clean.**
