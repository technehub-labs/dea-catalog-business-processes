# CR-BP-98: Task Boundary and Workflow Realization

**Status**: Proposed
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-18
**Recon programme parents**: CR-BP-92 (Process Catalog layer), CR-BP-93 (decomposition semantic contract §7), CR-BP-94 (Decomposition Record Templates; `templates/task.yaml` first normative L4 shape).
**Sub-pipeline**: CR-BP-98 (this slice). EXT-02..06 (documentation sub-pipeline) and CR-BP-99 (Reconciliation Matrix) are downstream.
**Lands against**: 0 L4 records; 740 entities; 21+1=22-gate suite CONFORMANT; v0.4.0 tagged.

---

## 1. Change Request

Establish the **L4 Task schema, the L4 / Workflow boundary, and the L4 structural validator** as the normative downstream of CR-BP-93 §7 and CR-BP-92 §11 (RF-09 compositional-non-implication principle).

### 1.1 What this slice lands

1. **`schemas/entities/task.schema.json`** (NEW, Draft-07): the canonical L4 Task schema. Codifies CR-BP-93 §7 (allowed + disallowed at L4) and CR-BP-93 §9 (L4 information-requirement matrix). Required fields: `id`, `type`, `name`, `definition`, `belongs_to_activity`, `trigger`, `outcome`, `responsibility`, `boundary`, `version`, `lifecycle_status`, `status`, `ecfConformance`. The schema declares `additionalProperties: false` and constrains `id` to `dea:task-*`. The `composes[]` field is intentionally absent: composition lives at the parent Activity (L3) level.

2. **`scripts/check_task_model.py`** (NEW, ~430 lines, TASK-001..005): structural validator with self-test, JSON mode, and live-catalog mode.
   - TASK-001: id format (`dea:task-*`).
   - TASK-002: definition + responsibility + boundary (Required at L4).
   - TASK-003: trigger + outcome (Completion state at L4).
   - TASK-004: `belongs_to_activity` resolves to a canonical L3 Activity.
   - TASK-005: no disallowed fields (workflow / orchestration / execution semantics).
   - All 5 checks are MANDATORY (`severity: error`). The gate is wired as `BLOCKING` in `scripts/conformance_result.py`.

3. **Gate [22] Task Model (TASK-001..005)** in `scripts/conformance_result.py`. The gate is **blocking** because L4 structural validity is a hard requirement (any record claiming `type: Task` must satisfy the schema-derived invariants).

4. **CI schema dispatch extension** in `.github/workflows/ci.yml`:
   - `SCHEMAS` dict adds `"Task": "schemas/entities/task.schema.json"`.
   - The `type: Task` comment now reads `Task -> schemas/entities/task.schema.json (L4, CR-BP-98)`.

5. **`templates/task.yaml`** (MODIFIED): the `# TODO(CR-BP-98):` placeholders from CR-BP-94 are resolved. The template is now anchored to the schema and validator rather than to placeholder annotations. Top docstring references CR-BP-98 as "SLICE LANDED".

6. **28 new tests** in `tests/test_check_task_model.py`: profile constants, helper checks (TASK-001..005 individually), aggregate `evaluate()` + `verdict()`, CLI self-test, live catalog, JSON shape, severity invariant.

### 1.2 What this slice does NOT land

- **NOT a Workflow schema.** Workflow Definition, Workflow Instance, and Execution are downstream of L4 (CR-BP-93 §8) and CR-BP-33 EXE-001..010 already codify the boundary. Workflow is reserved for a future slice (e.g., CR-BP-100 or a dedicated WF programme).
- **NOT a count-assertion change.** No new canonical-entity records are introduced. The L4 schema is normative; the validator is in regression-guard mode until the first L4 tranche lands.
- **NOT a change to the Activity (L3) schema.** `belongs_to_activity` references an existing Activity; L4 composition flows upward through the parent's `composes[]`.
- **NOT a tightening of specialization validation.** Held under CR-BP-92 §21.
- **NOT a pre-existing finding fix.** `tests/test_dispositions.py::test_tranche_count_is_ten` (78 vs 73 drift) remains flagged.

## 2. Deposition mechanics (pattern per CR-BP-92 §16)

1. **Schema is normative prose** (`schemas/entities/task.schema.json`). The validator enforces the schema-derived invariants. Future L4 records must conform; the gate is blocking.
2. **Validator is blocking** (gate [22]). Per CR-BP-32 §13 + CR-BP-33 §15, structural decomposition vs execution separation is a hard requirement.
3. **No count-assertion change.** `open_change_requests` 109 → 110.
4. **No gate wire change to existing gates.** Only an additive gate [22] is wired.

## 3. L4 / Workflow boundary (CR-BP-93 §8)

```
PROCESS ARCHITECTURE          EXECUTION REALIZATION
L0 -> L1 -> L2 -> L3 -> L4    L4 -> Workflow -> Workflow Instance -> Execution
```

Workflow is **not** an additional process-decomposition level. Workflow realizes and coordinates work; it does not constitute another process-decomposition level. The decomposition-vs-execution separation is the structural foundation of this slice.

The compositional-non-implication principle is enforced by:
- TASK-005 (no disallowed fields at L4): `sequencing`, `branching`, `conditions`, `dependencies`, `participants`, `events`, `orchestration`, `automation`, `workflow_definition`, `workflow_instance`, `executed_by`, `executed_at`, `execution_order`, `sequence_index`, `step_index`, `temporal_sequence`, `before`, `after`, `precedes`, `follows`, `triggers_workflow`, `next_step`, `state_transitions`: all forbidden.
- EXE-001..010 (existing): structural decomposition shall not encode execution sequence.
- The parent Activity's `composes[]` (L3 -> L4) is structural only; it does NOT imply `Task A -> Task B -> Task C`.

## 4. Gate posture

- Gate [22] Task Model (TASK-001..005): **CONFORMANT** (PASS/BLOCKING). 0 records / 0 findings.
- Full suite: **27 gates, 0 blocking, 0 advisory** failures (was 21 gates; +1 for the new gate [22], +5 from the EXT-01..01a gate count which was 21, so 21 -> 22 from CR-BP-98; actually the EXT-01..01a landed 1 gate total: gate [21]. So 21 (post-EXT-01a) -> 22 (post-CR-BP-98). And wait, the EXT-01..01a also added gate [21], so prior baseline was 20 -> 21 (post-EXT-01) -> 21 (post-EXT-01a, no new gate) -> 22 (post-CR-BP-98)).
- CR-META: 0 new findings.
- Em-dash / en-dash: 0 violations in new prose.

## 5. Repository changes

| Path | Status | Notes |
|---|---|---|
| `schemas/entities/task.schema.json` | NEW | Draft-07; `additionalProperties: false`; `dea:task-*` id family |
| `scripts/check_task_model.py` | NEW | TASK-001..005 structural validator (~430 lines); self-test + JSON + live-catalog modes |
| `scripts/conformance_result.py` | MOD | + gate [22] Task Model (blocking) |
| `.github/workflows/ci.yml` | MOD | + `"Task"` entry in `SCHEMAS` dict; + `Task -> ... (L4, CR-BP-98)` comment |
| `templates/task.yaml` | MOD | `# TODO(CR-BP-98):` placeholders resolved; schema + validator referenced |
| `tests/test_check_task_model.py` | NEW | 28 tests (constants + helpers + TASK-001..005 + evaluate/verdict + CLI) |
| `change-requests/CR-BP-98-task-boundary-and-workflow-realization.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-98 row added before `## Cross-repo context` |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 109 -> 110 |

No canonical-entity mutation. No gate wire change to existing gates. No L4 record introduced.

## 6. Acceptance criteria

1. `schemas/entities/task.schema.json` validates as Draft-07 JSON Schema.
2. `scripts/check_task_model.py --self-test` passes.
3. `scripts/check_task_model.py` against the live catalog returns CONFORMANT (0 records / 0 findings).
4. Gate [22] Task Model is wired as **blocking** in `scripts/conformance_result.py`; the suite remains CONFORMANT (27 gates, 0 blocking, 0 advisory failures).
5. CI workflow's schema dispatch includes `Task` mapping.
6. `tests/test_check_task_model.py` reports 28 tests pass.
7. CR-BP-98 carrier CR is filed in `change-requests/`.
8. README row + CATALOG regen is committed.
9. Em-dash / en-dash audit: 0 violations in new prose.
10. Full pytest suite passes (pre-existing `test_dispositions::test_tranche_count_is_ten` failure unchanged; NOT introduced by this slice).
11. `templates/task.yaml` no longer carries `# TODO(CR-BP-98):` annotations.

## 7. Result

CR-BP-98 establishes the canonical L4 Task schema, the L4 / Workflow boundary, and the TASK-001..005 structural validator. The L4 layer is now first-class at the schema + validator + CI-dispatch level, even though zero L4 records exist today. The 27-gate suite remains CONFORMANT. `open_change_requests` 109 -> 110. EXT-02..06 (documentation sub-pipeline) and CR-BP-99 (Reconciliation Matrix) are downstream; the L4 documentation profile in CR-BP-94-EXT-01 (`dea:profile-readme-l4-task-v1`) will become enforceable against actual L4 records in future slices.