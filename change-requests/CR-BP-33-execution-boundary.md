# CR-BP-33: Execution Boundary Validators (EXE-001..010)

**Status**: Proposed
**Layer**: L3
**Owner**: Emmanuel A. Otchere
**Date**: 2026-09-12
**Carrier**: Sixth execution slice of the BP-32/33/34 tranche plan; first slice of Phase 4 (CR-BP-33 — Execution Boundary). See `01_plan/CR-BP-32-33-34-foundation/POSITIONING.md` §7.
**Depends on**: CR-BP-03, CR-BP-14, CR-BP-16, CR-BP-32 (Activity Model; PR #74 MERGED)
**Lands against**: 126 canonical BP records (type=Process) + 35 PG + 35 PC + 0 Activity + 0 Workflow + 0 Task records; conformance level L4; 0 records with Workflow references

---

## 1. Change Request

Codify the Execution Boundary rules from CR-BP-33 §15 as a standalone, machine-testable validator that emits **no findings on the existing 196 canonical records** and provides a regression guard against any future record that leaks execution semantics into the structural process model.

The ten rules (derived from CR-BP-33 §15):

| # | Rule | Machine-checkable |
|---|---|---|
| **EXE-001** | **Structural decomposition shall not encode execution sequence.** | For any record: `composes[]` entries MUST NOT carry `execution_order`, `sequence_index`, `step_index`, `temporal_sequence`, `before`, `after`, `precedes`, `follows`, `triggers`, `next_step`. |
| **EXE-002** | **`dea:composes` shall not be interpreted as execution ordering.** | Type-level complement to EXE-001: entries with `relationship_type=dea:composes` MUST NOT carry the ordering fields listed in EXE-001. |
| **EXE-003** | **Workflow remains distinct from Business Process.** | A record with `type=Workflow` MUST NOT carry BP classification fields (`process_intent`, `process_type`, `process_specialization`, `process_audience`). |
| **EXE-004** | **A Business Process may have multiple execution Workflows.** | Singleton workflow fields (`workflow`, `workflow_ref`, `execution_workflow`) are rejected; use `workflow_references[]` list. |
| **EXE-005** | **Different Workflow implementations shall not automatically create different Business Processes.** | For any BP with ≥ 2 `workflow_references[]`: `process_intent` and `process_type` MUST remain singular (not lists). |
| **EXE-006** | **Execution actors shall reference existing Actor semantics.** | `executed_by` / `performed_by` values MUST be `dea:actor-*` ids (or `{actor_reference: dea:actor-*}` dicts), NOT inline strings. |
| **EXE-007** | **Execution systems shall reference existing System semantics.** | `execution_system` / `system_ref` / `executing_system` values MUST be `dea:system-*` ids (or `{system_reference: dea:system-*}` dicts). |
| **EXE-008** | **Execution logic shall not redefine process identity.** | A `type=Workflow` record MUST NOT carry `identity.verb` / `identity.object` (those live on the parent BP). |
| **EXE-009** | **Implementation detail shall remain outside the Business Process decomposition model.** | For any record: MUST NOT carry `api_sequence`, `database_procedure`, `application_control_flow`, `infrastructure_operation`, `script`, `code_ref`, `technical_runbook`. |
| **EXE-010** | **Every catalogued Workflow reference shall identify its relationship to the associated Business Process.** | Each `workflow_references[]` entry MUST declare `relationship_kind` from the controlled vocabulary: `reference`, `operational`, `scenario`, `implementation`. |

## 2. Why this CR is paper-trail-only (forward-looking)

CR-BP-33 §15 declares the ten Execution Boundary rules. The existing CR-BP-16 gate does not address execution semantics (no execution-bearing fields existed prior to this slice). There is no validator today that:

1. Catches execution-ordering annotations on `composes[]` entries (the "A composes B, B composes C ⇒ A→B→C executes in that order" inference).
2. Catches `dea:composes` reinterpretation as before/after/precedence/branching/parallelism semantics.
3. Catches a Workflow record that drifts into BP classification (which would violate CR-BP-33 §14 "no new normative execution ontology").
4. Catches a singleton workflow field (which would prevent multiple execution realizations per CR-BP-33 §11).
5. Catches a BP with multiple Workflow realizations that silently splits its identity axes (which would imply multiple BPs).
6. Catches an inline actor string (which bypasses Actor record semantics per CR-BP-33 §9).
7. Catches an inline system string (which bypasses System record semantics).
8. Catches a Workflow record that re-defines the BP's identity (which would imply the Workflow is a separate process).
9. Catches implementation-detail leakage (`api_sequence`, `script`, `code_ref`) below the L4 boundary.
10. Catches a Workflow reference that lacks the `relationship_kind` discriminator from CR-BP-33 §13.

**Coverage on the live 196 records** (run 2026-09-12):

| Rule | Pass | Fail |
|---|---|---|
| EXE-001..010 (all 161 records loaded; 35 PG / 35 PC / 126 BP + legacy scope) | 161 | 0 |

**Coverage on a hypothetical Workflow / opted-in BP fixture**: all ten rules are exercised by the `--self-test` entry point (18 cases) and by `tests/test_check_execution_boundary.py` (32 cases).

## 3. Repository changes

| Path | Status | Notes |
|---|---|---|
| `scripts/check_execution_boundary.py` | NEW | Validates EXE-001..010. Mirrors `check_lifecycle_state.py` / `check_semantic_identity_version.py` / `check_activity_model.py` CLI shape. |
| `tests/test_check_execution_boundary.py` | NEW | 32 tests; covers each rule individually + CLI + live catalog + type-agnostic checks. |
| `metamodel-pointer.yaml` | MODIFIED | References `dea:Workflow` / `dea:Task` additively from the dea-metamodel registry (`lifecycle: proposed`, `catalog_repo: null`). No new entries created; cross-repo reference only. |
| `scripts/conformance_result.py` | MODIFIED | Adds gate `[16] Execution Boundary (EXE-001..010)` (advisory, non-blocking). |
| `CATALOG.yaml` | MODIFIED | Regenerator bumps `open_change_requests` 45 → 46. |
| `change-requests/README.md` | MODIFIED | Adds CR-BP-33 row. |
| `change-requests/CR-BP-33-execution-boundary.md` | NEW | Slice carrier CR (this PR). |

## 4. Why the validator never fires on existing records

The validator's discovery loop loads **every record** under `entities/v1-alpha/` (unlike LCM/SIV which filter on `type=Process`, or ACT which filters on `type=Activity`). However:

- **Tier 1 (universal)**: checks for execution-leakage fields (`api_sequence`, `script`, ordering annotations on `composes[]`, etc.). None of the 161 records carry such fields.
- **Tier 2 (opt-in)**: checks Workflow-references specifically. None of the 161 records carry `workflow_references[]`.

The validator therefore emits `0 findings` on the live catalog by construction. It is a **forward-looking regression guard**: the first record to declare `workflow_references[]` (or to attempt execution leakage) will be evaluated against all ten rules.

This is the same posture as CR-BP-32 (ACT; gate [15]) and CR-BP-34c/d (LCM/SIV; gates [13]/[14]).

## 5. Tranche plan status

| Phase | Slice | Status |
|---|---|---|
| 1 | CR-BP-32/33/34 foundation carrier | Merged (PR #69, `f40a45c`) |
| 2 | CR-BP-34a L2 Qualification | Merged (PR #70, gate [11]) |
| 2 | CR-BP-34b Intent Purposive | Merged (PR #71, gate [12]) |
| 2 | CR-BP-34c Lifecycle State-Machine | Merged (PR #72, gate [13]) |
| 2 | CR-BP-34d Semantic Identity vs Version | Merged (PR #73, gate [14]) |
| 3 | CR-BP-32 Activity Model | Merged (PR #74, gate [15]) |
| **4** | **CR-BP-33 Execution Boundary (EXE-001..010)** | **This slice; gate [16]** |
| 5 | CR-BP-35..38 (architecture / MECE / cross-repo / ECF retrospective) | Documentation |

## 6. What this CR is NOT

- **NOT a Workflow instantiation.** No `dea:workflow-*` records are created; the catalog references the metamodel types as opt-in targets only.
- **NOT a Task instantiation.** `dea:Task` exists in the metamodel registry but no catalog records carry Task references yet. Task adoption is a future opt-in.
- **NOT an execution-semantics ontology.** CR-BP-33 §14 explicitly forbids "Process Flow", "Execution Process", "Process Instance", "Execution Process Group", "Workflow Process", "Process Sequence" — none are introduced here.
- **NOT a retroactive execution model.** Existing BPs stay at L4 conformance with no execution references (CR-BP-33 "Result (post-landing)" §3).
- **NOT a metamodel CR.** `dea:Workflow` / `dea:Task` already exist in `dea-metamodel/metamodel/registry/entities.yaml` with `lifecycle: proposed` and `catalog_repo: null`. This CR references them; it does not modify them.
- **NOT a BPMN / workflow-execution CR.** BPMN, execution engines, and runtime semantics are outside the catalog's scope (CR-BP-33 §13).

## 7. Acceptance criteria

1. `scripts/check_execution_boundary.py` runs on the live catalog with 0 findings.
2. `scripts/check_execution_boundary.py --self-test` passes (18 cases).
3. `tests/test_check_execution_boundary.py` passes (32 tests).
4. `scripts/conformance_result.py` runs with gate [16] added; final verdict remains CONFORMANT.
5. `metamodel-pointer.yaml` references `dea:Workflow` / `dea:Task` additively; no existing entries mutated.
6. No schema, no validator, and no canonical record mutation outside the additive changes listed in §3.

## 8. Result

CR-BP-33 establishes the L4 Execution Boundary as a forward-looking authorial affordance for the catalog. The 10-rule validator (EXE-001..010) gates any future record that references Workflow / Actor / System / Execution-Model semantics without restructuring the 161 existing records. Execution realizations remain opt-in; BPMN and workflow-engine integration are outside scope.
