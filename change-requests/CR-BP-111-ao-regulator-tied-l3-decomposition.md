# CR-BP-111: A&O Regulator-Tied L3/L4 Decomposition Tranche (5 BPs x 4 Activities x 5 Tasks = 100 new records)

**Status**: Proposed (this PR)
**Layer**: L3 (Activity decomposition)
**Owner**: Coder (for eaojnr)
**Date**: 2026-10-12
**Carrier**: Single-PR L3/L4 decomposition tranche for the 5 ADMIT-CANONICAL A&O regulator-tied Business Processes admitted by CR-BP-106. Lands 20 new Activity records (4 per BP) and 100 new L4 Task records (5 per Activity) under the established 5-phase verb-object completion pattern. 5 generator scripts + 1 admission-gate allowlist extension + 6 test-file count-assertion updates + 1 CATALOG.yaml regen.

**Lands against**: 5 BP records patched (metadata.activity_references added; change_history CR-BP-111 entry added); 20 new Activity records at 5 cells; 100 new L4 Task records at 20 cells; 5 research/l3-candidate-universe.yaml files; CATALOG.yaml regen (3602 -> 3722 canonical, 329 -> 334 research files); 6 test files with count-assertion bumps; 1 validator script (admission gate allowlist).

## 1. Goal

CR-BP-106 admitted 5 new regulator-tied BPs at AgencyAndOrganization x {Conceive, Design, Build, Operate, Improve} but deferred the L3/L4 decomposition to "CR-BP-111 (deferred follow-on tranche; 5 BPs x 4 Activities x 5 Tasks = 100 new records)". This CR lands that decomposition.

Each BP is decomposed into 4 cohesive Activities following the established pattern (4 concerns per cell: supervisor-controlled scope, fitness-and-propriety attestation, supervised-training completion, and continuing-supervisor notification) drawn from the BP's own description/outcome text per the L3 deposition procedure. Each Activity is then decomposed into 5 L4 Tasks per the 5-phase verb-object completion pattern (intake -> verify -> transform -> confirm -> record) authored by `scripts/decompose_l4.py`.

## 2. Slice shape

### 2.1 The 5 BPs and their 4 Activities each

| Cell | BP (CR-BP-106 admitted) | 4 Activities (this CR) |
|---|---|---|
| ao-conceive | Conceive Licensed or Regulated Agent Capacity (pnrhem) | Declare Regulator-Licensed Role Mix (cqkwrm); Document Fitness-And-Propriety Attestation Regime (vnkqzf); Map Supervised-Training Completion Requirements (fmxtqr); Capture Continuing-Supervisor Notification Path (pzmwkl) |
| ao-design | Design Regulated Role Architecture (2fkvhx) | Catalogue Regulator-Tied Role Entries (jbf2v9); Align Competency Framework To Continuing-Supervision (wnqz3k); Define Fitness-And-Propriety Assessment Regime (x9k4m7); Define Continuing-Supervisor Notification Path (v8r5n2) |
| ao-build | Build Regulated Agent Pool (9my4jr) | Verify Candidates Against Regulator Licence Registry (q7m3k9); Attest Fitness-And-Propriety For Pool (w2n8p4); Screen Candidates Against Sanctions / AML / FCRA / ADA (f5k1m3); Stage Regulated Personnel Record (r6h2t8) |
| ao-operate | Operate Regulated Performance Oversight (ba8scr) | Audit Conduct-Rule Compliance (z4n9m2); Annual Fitness-And-Propriety Re-Attestation (j8k5p7); Track Hours-Of-Work And Rest-Rule Compliance (q3w6r1); Track Continuing-Competence Completion (b5v2k9) |
| ao-improve | Improve Regulated Workforce Capability (qqxe4d) | Run Regulator-Mandated Recurrent Training (x7m4n2); Run Fit-And-Proper Re-Assessment Cycle (k9w5p8); Execute Regulator-Mandated Remediation (f2r6t4); Notify Continuing Supervisor Of Improvement (v3h8k1) |

### 2.2 Each Activity is decomposed into 5 L4 Tasks per the 5-phase pattern

`scripts/decompose_l4.py --scope <activity-id>` writes 5 Tasks per Activity: `<slug>-intake`, `<slug>-verify`, `<slug>-transform`, `<slug>-confirm`, `<slug>-record`. Each Task is a bounded unit of work within the parent Activity, with a `belongs_to_activity` reference and a `rationale` for the phase. Total: 20 Activities x 5 Tasks = **100 new L4 Task records**.

### 2.3 Generator scripts (committed for reproducibility)

- `scripts/gen_cr_bp_111_activities.py` — generates 20 Activity records from the in-script `CELLS` dict. Idempotent on re-run; existing Activity records are overwritten with identical content.
- `scripts/decompose_l4.py` (existing) — generates the 100 Task records. Used with `--scope <activity-id>` to limit to one Activity at a time.
- `scripts/reorg_cr_bp_111_tasks.py` — one-time reorganization of the 100 Tasks from the script's flat `entities/v1-alpha/<task_id>/` layout to the post-mv1 nested `entities/v1-alpha/<cell>/<pg-hash>/<bp-hash>/<act-hash>/<task-hash>/` layout. The `decompose_l4.py` script's path scheme is pre-mv1; the reorganization is a workaround for that pre-existing script bug (not fixed in this slice per the surgical-change discipline; out-of-scope for the L3 tranche).
- `scripts/patch_cr_bp_111_bp_refs.py` — patches the 5 BPs to add `metadata.activity_references` and a CR-BP-111 `change_history` entry.
- `scripts/gen_cr_bp_111_research.py` — generates the 5 `research/l3-candidate-universe.yaml` files (one per BP) describing the 4-Activity decomposition.

### 2.4 Validator patch

- `scripts/check_admission_gate.py` — extended `_ADMISSION_CR_RE` regex to admit `CR-BP-111`. The L3-deposition skill's "extend the allowlist in the same commit" rule is now extended to admission tranches (CR-BP-106 was the first tranche to ship without the allowlist extension; that gap was retro-fixed in the CR-BP-107 follow-on).

### 2.5 Test count-assertion updates (6 files)

- `tests/test_check_activity_model.py`: 560 -> 580 Activity records
- `tests/test_check_execution_boundary.py`: 3598 -> 3718 records
- `tests/test_architectural_regression.py`: 3599 -> 3719 total records; L3=23, L4=3696
- `tests/test_decompose_l4.py`: 2800 -> 2900 Task files
- `tests/test_check_task_model.py`: 2800 -> 2900 records
- `tests/test_enrich_l4_party_and_relationship.py` and `tests/test_enrich_l4_governance_and_existence.py`: 2800 -> 2900 records (conformance regression assertions)

## 3. Posture

- `scripts/check_activity_model.py`: **CONFORMANT** (0 findings; 580 Activities, 145 BPs).
- `scripts/check_admission_gate.py --strict-provenance`: **CONFORMANT-WITH-WARNINGS, 0 BLOCKING** (the 245 ADM-005 advisory findings are pre-existing on main; CR-BP-111 adds 0 blocking findings).
- `scripts/check_cr_metadata.py --strict`: CONFORMANT (124 CR files; CR-BP-111 itself is metadata-clean).
- `scripts/regenerate_catalog.py`: regenerated successfully; `canonical: 3722, entities: 3723, research_files: 334, open_change_requests: 124` (was 3602, 3603, 329, 122 pre-CR-BP-111; +120 entities = 20 Activities + 100 Tasks, +5 research files, +2 open CRs = CR-BP-111 + this branch).
- All 100 Task files re-registered under the post-mv1 nested layout by `scripts/reorg_cr_bp_111_tasks.py`.

## 4. Open follow-on

- `decompose_l4.py` writes tasks to the pre-mv1 flat layout (`entities/v1-alpha/<task_id>/`); the post-mv1 layout is nested under the parent Activity. The workaround `scripts/reorg_cr_bp_111_tasks.py` is a one-shot tool, not a permanent fix. A future `CR-BP-decompose_l4-fix` slice should extend `decompose_l4.py` to write directly to the post-mv1 nested layout, removing the need for the reorganization step.
- 245 ADM-005 advisory findings (missing triggers/outcomes on every BP) are pre-existing on main and out of scope for this L3 tranche; they will be addressed in a future Process-Catalog-layer repair slice.
- 5 BP records still have empty `metadata.activity_references[]` from CR-BP-106 (before this patch); now populated with 4 Activity ids each.
