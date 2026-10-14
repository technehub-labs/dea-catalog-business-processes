# CR-BP-32/33/34 Foundation — Positioning & Knowledge Harvest

**Date**: 2026-09-10
**Author**: Emmanuel A. Otchere
**Source**: User-attached document `/home/hermes/.hermes/profiles/coder/cache/documents/doc_cf6fc6bb9e80_CR-BP-04_06.md` (1578 lines)
**Companion files**: `CR-BP-32-activity-model.md`, `CR-BP-33-execution-boundary.md`, `CR-BP-34-process-conformance-profile.md`

---

## 1. Why this document exists

The user attached a 3-CR package that defines a coherent and rigorous extension of the catalog into **L3 (Activity)** and **L4 (Task / Workflow / Execution Boundary)**, plus a four-level conformance profile. The package was authored in the assumption that these CRs would land **before** catalog population. The actual landing order in `main` is the inverse: the catalog is already populated (196 canonical records; 126 L2 BPs / 35 L1 Groups / 35 Process Contexts; conformance level L4), under the looser CR-BP-12 + CR-BP-14 + CR-BP-15 + CR-BP-16 regime.

This document is the **knowledge harvest** the user requested: a faithful mapping of the new package against the actual repo state, identification of the harvestable insights, explicit acknowledgement of the historical inversion, and a phased execution plan that keeps every step additive.

---

## 2. Renumbering decisions

The user's package uses CR-BP-04 / CR-BP-05 / CR-BP-06. These IDs collide with the canonical sequence:

| User ID | Title | Conflict | Renumbered to |
|---|---|---|---|
| CR-BP-04 | Activity Model | **CR-BP-04 is MERGED** (PR #19; "Business Process Identity & ID-Family Reconciliation"; commit `2c0e62f`) | **CR-BP-32** |
| CR-BP-05 | Execution Boundary | CR-BP-05 unused, but the user's CR-BP-06 §27 sequence references "CR-BP-05" as a dependency of CR-BP-06. To preserve the sequencing integrity, renumber to **CR-BP-33** rather than claim CR-BP-05 | **CR-BP-33** |
| CR-BP-06 | Process Conformance Profile | CR-BP-06 unused | **CR-BP-34** |

Renumbering rationale is recorded verbatim in the carrier header of each CR document.

---

## 3. Mapping the user's conformance levels to the existing CR-BP-16 gate

The CR-BP-34 conformance profile defines 6 levels (A–F). Here is the **honest map** against the actual CR-BP-16 + CR-BP-14 + CR-BP-12 enforcement surface:

### A — Identity (covered)

`check_process_identity.py` (BP-ARC-ID-001..005), `check_process_specialization.py` (BP-SPEC-01-001..007), and the schema (`schemas/identity.schema.json`) cover canonical id, version, type, authority, and reference integrity. **No new validators needed.**

### B — Architectural (mostly covered)

`check_process_context.py` (PC-001..008), `check_process_group.py` (PG-001..008), `check_struct.py` (STRUCT), and `check_legacy_migration.py` (BP-MIG-001..005) cover Process Context, Scope, Group, and Business Process. **Activity and Task are not yet record types** (they live in `dea-metamodel` as `dea:Workflow` / `dea:Task` with `catalog_repo: null`; `dea:Activity` is not even in the metamodel registry). CON-005 (Activity belongs to BP) and CON-006 (uses `dea:composes`) are **new** and land with CR-BP-32.

### C — Semantic (covered)

`check_process_semantics.py` (BP-SEM-001..012) implements the CR-BP-14 semantic contract: intent, specialization, classification, outcome, capability realization. **PSP-001..003 strengthen the Intent axis** — they forbid organizational-domain substitutions of Intent (e.g. using "finance" as a process intent when "operate" is the canonical value). Landable as additive rules.

### D — Decomposition (partially covered; blocked on CR-BP-32)

`BP-SEM-007..009` enforce some L2 qualification criteria. **BP-C1..C4** (Input–Output Transformation, Objective Contribution, Standalone Executability, Resource Dedication) are the four formal L2 criteria from CR-BP-34 §11 — declared in prose today, not enforced as validators. **Landable as `scripts/check_l2_qualification.py` with 4 rules.** Activity cohesion (ACT-001..010) is blocked on CR-BP-32 (no Activity record type).

### E — Execution (not covered; blocked on CR-BP-33)

EXE-001..010 cannot land — there are no execution references in any of the 196 records. **Blocked on CR-BP-33**, which introduces `dea:Workflow` / `dea:Task` as referenced types. Once CR-BP-33 lands, EXE-001..010 become additive rules on `check_process_semantics.py`.

### F — Ecosystem (mostly covered)

`check_ecf_conformance.py` covers the ECF axis. `check_cr_metadata.py` (CR-META-001..006) covers cross-repo identifier integrity. **Metamodel reference integrity is partial** — `metamodel-pointer.yaml` references some metamodel entities but does not exhaustively cover all the ones CR-BP-34 §18 expects (Business Function, Actor, Workflow, Task, System, Service, Business Object, ECF Domain, Lifecycle Stage). Strengthen as a follow-on.

---

## 4. Harvestable insights (the genuine value-add from the user's package)

The user's package is **not** redundant with the existing catalog. It carries six genuinely novel insights that strengthen rather than duplicate the current state:

### 4.1 L2 qualification becomes a validator, not prose

CR-BP-34 §11 names the four L2 criteria (BP-C1..C4). Today they are described in `docs/semantic-contract.md` but not enforced. A contributor can submit a Business Process that fails any of the four criteria and the admission gate does not catch it. **Landable as `scripts/check_l2_qualification.py`** with 4 rules. BP-C3 (Standalone Executability) and BP-C4 (Resource Dedication) are the most novel — they would close a real governance gap.

### 4.2 Lifecycle status as a state machine

CR-BP-34 §20 names a six-state lifecycle (Draft / Proposed / Validated / Published / Deprecated / Retired) with transition rules. Today the catalog uses `status` and `lifecycle_status` as free-text fields. The transition discipline (Draft → Proposed → Validated → Published) is partially enforced by `check_admission_gate.py` but not as a complete state machine. **Landable as `scripts/check_lifecycle_state_machine.py`** — closes a real governance gap.

### 4.3 Semantic-identity-vs-version discipline

CR-BP-34 §19 says "a version change shall not silently create a new semantic identity; a semantic identity change shall require an explicit governed change." Today the catalog enforces this via PR review (CR-META-006) but not via a validator. **Strengthen with explicit semantic-identity-vs-version rules in `check_process_identity.py`.**

### 4.4 Intent cannot be substituted for organizational component

CR-BP-34 §7 (PSP-001..003) forbids using Intent as a substitute for organizational component, process domain, ECF Domain, or Lifecycle Stage. Today this is enforced by the 7-value purpose-oriented vocabulary (govern / manage / operate / deliver / support / develop / transform) but not as an explicit "no cross-axis substitution" rule. **Landable as `scripts/check_intent_purposive.py`** with 3 rules.

### 4.5 The Activity / Task / Workflow layer is genuinely missing

CR-BP-32 + CR-BP-33 introduce three record types that do not exist today: `dea:Activity` (not in the metamodel at all), `dea:Workflow` (in the metamodel, `lifecycle: proposed`, `catalog_repo: null`), and `dea:Task` (same). The current 196 records have **no internal decomposition** below the Business Process. This is the single largest gap in the catalog. Land CR-BP-32 + CR-BP-33 as the natural extension of the L3 catalog into the adjacent metamodel layer.

### 4.6 The CR-BP-16 conformance gate is "type L" not "rule-set L"

CR-BP-34 §4 distinguishes "Conformance" (is this artifact valid?) from "MECE" (is the catalog collectively exhaustive and mutually exclusive?). CR-BP-16 implements Conformance but explicitly defers MECE to a future programme. **CR-BP-36 (renumbered CR-BP-08) would be the carrier for the MECE programme.** This is real work that has not been done.

---

## 5. Net additive harvest

Six insights, each landable as a separate carrier PR. Estimated sizes:

| PR | Title | Scope | LOC + tests |
|---|---|---|---|
| **CR-BP-34a** | L2 qualification validators (BP-C1..C4) | One new script + 4 rules | ~250 LOC |
| **CR-BP-34b** | Intent purposive validators (PSP-001..003) | One new script + 3 rules | ~150 LOC |
| **CR-BP-34c** | Lifecycle state-machine validator | One new script + state transitions for 6 states | ~300 LOC |
| **CR-BP-34d** | Semantic-identity-vs-version validators | Strengthen existing | ~150 LOC |
| **CR-BP-32** | Activity Model (record type + ACT-001..010) | New schema, new record type, 10 new rules, `dea:Activity` in `metamodel-pointer.yaml` | ~600 LOC |
| **CR-BP-33** | Execution Boundary (Workflow refs + EXE-001..010) | New validator rules, `dea:Workflow` / `dea:Task` references | ~400 LOC |
| **CR-BP-35** | Process Catalog Architecture (user's CR-BP-07) | Documentation retrospective | ~50 LOC |
| **CR-BP-36** | MECE Validation (user's CR-BP-08) | Real work; ~600 LOC + tests | ~600 LOC |
| **CR-BP-37** | Cross-Repository Integrity (user's CR-BP-09) | Documentation + contracts | ~200 LOC |
| **CR-BP-38** | ECF Matrix Population retrospective (user's CR-BP-10) | Documentation retrospective | ~50 LOC |

**Total additive harvest**: ~2750 LOC + tests across 10 PRs. Each PR is independently mergeable, independently revertable, and leaves the 196 canonical records at L4 conformance throughout.

---

## 6. Historical-context disclaimer

The user's package was authored with the assumption that CR-BP-04..06 would land **before** CR-BP-07 (Catalog Architecture) and the population. The actual landing order is the inverse. This is not a defect in either plan — it reflects the iterative discovery pattern of the federation: the catalog was populated under a looser regime, the population surfaced real-world complexity, and the user's payload represents the **mature, post-hoc formalization** of what those CRs *should have* said if we had known what we know now.

Each carrier CR document carries a "Result (post-landing)" section that explicitly acknowledges this inversion and reframes the rule set as **retroactive conformance additions** to the existing CR-BP-16 gate, rather than as a restructuring of the catalog. This is the right framing: it preserves the user's intent (objective, machine-testable validation of L2/L3/L4) without invalidating the 196 records already shipped.

---

## 7. Recommended execution order

| Phase | PR(s) | Title | Why this order |
|---|---|---|---|
| **1** | (this branch) | Land CR-BP-32/33/34 in `01_plan/` + this positioning doc | Knowledge harvest first; surfaces the harvestable insights and the renumbering decisions before any code lands |
| **2** | CR-BP-34a, CR-BP-34b, CR-BP-34c, CR-BP-34d | Additive conformance validators (4 PRs) | These are **independent** of CR-BP-32/33 and can land first; they close real governance gaps; no entity mutation |
| **3** | CR-BP-32 | L3 Activity (record type + ACT-001..010) | Introduces `dea:Activity` and the internal-decomposition affordance; opt-in for new BPs |
| **4** | CR-BP-33 | L4 Execution Boundary (Workflow refs + EXE-001..010) | Introduces execution semantics; opt-in; requires CR-BP-32's Activity decomposition to be useful |
| **5** | CR-BP-35..38 | Documentation + MECE follow-ons | Closes the loop per user's §27 sequence; CR-BP-36 (MECE) is the real work item |

Each phase is independently mergeable, independently revertable, and preserves L4 conformance on the 196 records.

---

## 8. What this is NOT

- **Not a restructure of the 196 records.** Existing BPs are not retroactively decomposed into Activities or Workflows.
- **Not a new metamodel CR.** The metamodel already has the entity types we need (`dea:Workflow`, `dea:Task`) or they belong in the metamodel as new proposals (`dea:Activity`). This package stays inside the catalog's scope.
- **Not a regression on the existing CR-BP-16 gate.** CR-BP-34's rules are **additive** — they layer on top of the existing 15-gate suite, they do not replace it.
- **Not a MECE claim.** MECE validation is explicitly deferred to CR-BP-36.

---

## 9. Acceptance criteria for this carrier PR

1. The three CR documents are saved at `01_plan/CR-BP-32-33-34-foundation/` with renumbered IDs and post-landing Result sections.
2. This positioning document is the knowledge-harvest record.
3. No code, no schema, no validator change in this PR.
4. The user has reviewed the renumbering decisions and the additive harvest plan.

After acceptance, the natural next step is **Phase 2 (CR-BP-34a — L2 qualification validators)** — the smallest, most-independent, highest-value harvest item.
