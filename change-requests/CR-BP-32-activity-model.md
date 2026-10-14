# CR-BP-32: Activity Model Validators (ACT-001..010)

**Status**: Proposed
**Layer**: L3 (Business Process / Activity decomposition)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-09-12
**Carrier**: Fifth execution slice of the BP-32/33/34 tranche plan; first slice of Phase 3 (CR-BP-32 — Activity Model). See `01_plan/CR-BP-32-33-34-foundation/POSITIONING.md` §7.
**Depends on**: CR-BP-03, CR-BP-04 (id-family contract), CR-BP-14 (BP-SEM-001..014), CR-BP-16 (conformance gate), CR-BP-34a (BP-C4 Resource Dedication)
**Lands against**: 126 canonical BP records; conformance level L4; 0 Activity records (Activity is a forward-looking affordance per §17 "Result (post-landing)")

---

## 1. Change Request

Codify the Activity Model rules from CR-BP-32 §15 as a standalone, machine-testable validator that emits **no findings on the existing 126 canonical records** and provides a regression guard against any future Activity contribution that violates an Activity-Model rule.

The ten rules (derived from CR-BP-32 §15):

| # | Rule | Machine-checkable |
|---|---|---|
| **ACT-001** | **Every Activity belongs to a Business Process.** | `type=Activity` ⇒ `belongs_to_business_process` (top-level or `metadata.belongs_to_business_process`) is set AND matches the `dea:process-*` id family. |
| **ACT-002** | **Activity is not represented as a Business Process.** | `type=Activity` ⇒ no auxiliary promotion field (`kind`, `process_kind`, `promoted_to`) carries a `BusinessProcess` / `Process` / `L2Process` value. |
| **ACT-003** | **Every Activity has a cohesion rationale.** | `type=Activity` ⇒ `cohesion_rationale` (top-level or `metadata.cohesion_rationale`) is a non-empty string of length ≥ 20 characters. |
| **ACT-004** | **Activity has composed Task OR boundary marker.** | `type=Activity` ⇒ either `composes[]` has ≥ 1 entry targeting a `dea:task-*` id (or with `target_kind: Task`), OR `decomposition_boundary` is asserted (`l4-reached` / `l4` / `atomic` / `no-further-decomposition`). |
| **ACT-005** | **Composition uses `dea:composes`.** | Every entry in `composes[]` uses `relationship_type: dea:composes`. Forbidden: `parent_activity`, `child_activities`, `decomposes`, `contains_activity` (CR-BP-32 §7). |
| **ACT-006** | **No execution-ordering fields.** | `type=Activity` ⇒ MUST NOT carry `execution_order`, `temporal_sequence`, `start_time`, `end_time`, `duration`, `sequence_index`, `step_index` (top-level or `metadata.*`). Composition is structural only (CR-BP-32 §7). |
| **ACT-007** | **Activity is not a synonym for Business Function.** | `type=Activity` ⇒ id MUST NOT match `dea:function-*` (the Business Function id family; CR-BP-04 §4). |
| **ACT-008** | **No implementation-detail marker fields.** | `type=Activity` ⇒ MUST NOT carry `script_ref`, `api_call_ref`, `system_operation`, `procedure_ref`, `work_instruction_ref`, `technical_step_ref` (top-level or `metadata.*`). L4 is the catalog decomposition boundary (CR-BP-32 §12). |
| **ACT-009** | **No execution-model fields.** | `type=Activity` ⇒ MUST NOT carry `workflow`, `bpmn`, `execution_model`, `workflow_definition`, `bpmn_process`. Activity does NOT introduce execution semantics (CR-BP-32 §11; that is CR-BP-33). |
| **ACT-010** | **Activity traceability to parent BP.** | `type=Activity` ⇒ the parent BP (when present on disk) declares the Activity in `metadata.activity_references[]` or in a `composes[]` entry whose `target_id` matches the Activity id. Forward + reverse bidirectional traceability. |

## 2. Why this CR is paper-trail-only (forward-looking)

CR-BP-32 §15 declares the ten Activity Model rules. The existing CR-BP-16 gate does not address Activity (no Activity record type existed prior to this slice). There is no validator today that:

1. Catches an Activity that lacks a parent Business Process reference.
2. Catches silent promotion of an Activity to Business Process (via auxiliary `kind` / `process_kind` fields).
3. Catches an Activity that lacks a cohesion rationale (or has a 5-character label instead of a real rationale).
4. Catches an Activity that declares composition without terminating the decomposition at L4 (Task) — a categorical boundary violation of CR-BP-32 §12.
5. Catches forbidden composition relationships (`parent_activity`, `decomposes`, etc.) — drifting from the canonical `dea:composes` discipline.
6. Catches execution-ordering leakage into a structural-composition record.
7. Catches Activity-as-Business-Function confusion (id-family drift).
8. Catches implementation-detail leakage below the L4 boundary (CR-BP-32 §12).
9. Catches execution-model leakage (CR-BP-32 §11 reserves execution semantics for CR-BP-33).
10. Catches forward-reference-without-reverse-reference: an Activity names its parent BP but the parent BP does not list the Activity.

**Coverage on the live 126 records** (run 2026-09-12):

| Rule | Pass | Fail |
|---|---|---|
| ACT-001..010 (BP records) | 126 | 0 |

(BP records are filtered out by the type discriminator. The validator never inspects `type: Process` records. See §6 below.)

**Coverage on a hypothetical Activity fixture**: all ten rules are exercised by the `--self-test` entry point (20 cases) and by `tests/test_check_activity_model.py` (34 cases).

## 3. Repository changes

| Path | Status | Notes |
|---|---|---|
| `scripts/check_activity_model.py` | NEW | Validates ACT-001..010. Mirrors `check_lifecycle_state.py` (CR-BP-34c) and `check_semantic_identity_version.py` (CR-BP-34d) CLI shape: `--self-test`, `--strict`, `--json`. |
| `tests/test_check_activity_model.py` | NEW | 34 tests; covers each rule individually + CLI + live catalog + BP-record-never-inspected contract. |
| `schemas/entities/activity.schema.json` | NEW | Activity record type schema. Mirrors `process-group.schema.json` / `process-context.schema.json` shape. `additionalProperties: false` locks the contract. |
| `metamodel-pointer.yaml` | MODIFIED | Registers `dea:Activity` as an `lifecycle: proposed` specialization under `dea:Process`. Additive; mirrors how `dea:BusinessProcess` is declared. |
| `scripts/conformance_result.py` | MODIFIED | Adds gate `[15] Activity Model (ACT-001..010)` (advisory, non-blocking). |
| `CATALOG.yaml` | MODIFIED | Regenerator bumps `open_change_requests` 44 → 45. |
| `change-requests/README.md` | MODIFIED | Adds CR-BP-32 row. |

## 4. Why the validator never fires on existing records

The validator's discovery loop filters on `type: Activity`. The 126 canonical BP records carry `type: Process`. The 35 Process Group records carry `type: ProcessGroup`. The 35 Process Context records carry `type: ProcessContext`. None carry `type: Activity`.

The validator therefore emits `0 findings` on the live catalog by construction. It is a **forward-looking regression guard**: the first Activity contribution will be evaluated against all ten rules.

This is the same posture as CR-BP-34c (LCM; 0 findings on live catalog; gate [13]) and CR-BP-34d (SIV; 0 findings on live catalog; gate [14]). The validator establishes the contract before the data exists.

## 5. Tranche plan status

| Phase | Slice | Status |
|---|---|---|
| 1 | CR-BP-32/33/34 foundation carrier (L3/L4/Profile) | Merged (PR #69, `f40a45c`) |
| 2 | CR-BP-34a L2 Qualification (BP-C1..C4) | Merged (PR #70, gate [11]) |
| 2 | CR-BP-34b Intent Purposive (PSP-001..003) | Merged (PR #71, gate [12]) |
| 2 | CR-BP-34c Lifecycle State-Machine (LCM-001..005) | Merged (PR #72, gate [13]) |
| 2 | CR-BP-34d Semantic Identity vs Version (SIV-001..004) | Merged (PR #73, gate [14]) |
| **3** | **CR-BP-32 Activity Model (ACT-001..010)** | **This slice; gate [15]** |
| 4 | CR-BP-33 Execution Boundary (EXE-001..010 + Workflow refs) | Next per user direction |
| 5 | CR-BP-35..38 (architecture / MECE / cross-repo / ECF retrospective) | Documentation |

## 6. What this CR is NOT

- **NOT a retroactive decomposition of the 126 BPs into Activities.** Existing BPs without Activity decomposition are valid and remain at L4 conformance (CR-BP-32 §17 "Result (post-landing)").
- **NOT a new metamodel CR.** `dea:Activity` is a CATALOG-OWNED record type (mirrors `dea:ProcessGroup`). It is registered in `metamodel-pointer.yaml` as `lifecycle: proposed` per the existing `dea:BusinessProcess` pattern. A separate metamodel CR would be needed if `dea:Activity` were to be promoted to OpenDEAM Core (deferred).
- **NOT an execution-semantics CR.** Activity does NOT introduce Workflow, BPMN, or execution-modeling semantics. Those belong to CR-BP-33.
- **NOT a MECE claim.** The validator checks structural conformance of individual Activity records; collective exhaustiveness across the L3 layer is deferred to CR-BP-36 (MECE programme).
- **NOT a replacement for any CR-BP-16 gate.** Activity is gate [15], advisory, layered on top of the existing 14-gate suite.

## 7. Acceptance criteria

1. `scripts/check_activity_model.py` runs on the live catalog with 0 findings.
2. `scripts/check_activity_model.py --self-test` passes (20 cases).
3. `tests/test_check_activity_model.py` passes (34 tests).
4. `scripts/conformance_result.py` runs with gate [15] added; final verdict remains CONFORMANT.
5. `schemas/entities/activity.schema.json` is registered and discoverable by the regenerator's per-entity subtree scan.
6. `metamodel-pointer.yaml` registers `dea:Activity` additively; no existing entries mutated.
7. No schema, no validator, and no canonical record mutation outside the additive changes listed in §3.

## 8. Result

CR-BP-32 establishes the L3 Activity layer as a forward-looking authorial affordance for the catalog. The 10-rule validator (ACT-001..010) gates future Activity contributions without restructuring the 126 existing Business Process records. Execution semantics remain the territory of CR-BP-33; metamodel promotion of `dea:Activity` (if ever pursued) is a separate CR.
