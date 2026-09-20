# CR-BP-20: L1→L2 Alignment to ECF v2.4.0 Register v2

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Accepted
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-07
**Depends on**: CR-BP-19 (register v2); CR-BP-13a/b (admission tranches); CR-BP-18 (v2.4.0 enum carrier)
**Related**: CR-BP-21 (StrategyAndDirection landing, planned); dea-metaframework framework/domain-grounding.md

## 1. What this CR is

The alignment phase of the L0→L2 rediscovery / alignment / landing workstream
(CR-BP-19 was rediscovery; this is alignment; CR-BP-21+ is landing). Aligns
the 28 landed entities and 10 Process Contexts to register v2 and the v2.4.0
grounding records, with the user-approved Option A GE/SD split executed.

## 2. Scope and non-scope

### In scope (surgical changes)

1. **Group rename + re-scope** — `dea:group-strategy-and-governance-conception`
   is renamed `dea:group-governance-conception`, scope narrowed to charter /
   mandate / policy / board-mandate conception only (per Option A split).
2. **L2 split mapping** — `dea:process-develop-governance-strategy` is
   retained as `lifecycle_status: candidate` (the receiving cell does not
   yet exist; full migration to StrategyAndDirection × Conceive is parked for
   CR-BP-21a, the StrategyAndDirection landing tranche). The change_history
   carries the migration intent explicitly.
3. **Three BP-ARC-ID-003 outcome mismatches** —
   `dea:process-customer-channel-and-acquisition-build`,
   `dea:process-customer-experience-design`,
   `dea:process-market-and-demand-conception`. Each had a minor wording
   drift between `outcome` and `identity.outcome_statement`. Aligning.
4. **Provenance pass** — CR-META `--strict-provenance` reads
   `metadata.change_history` (PR #42); verifying the renamed group and the
   3 alignment-fixed processes all carry the new change_history entry.

### Out of scope (deferred to landing tranches)

- **L2 migration to StrategyAndDirection×Conceive**: cannot land until
  `dea:pc-sd-conceive` and the SD-Conceive group exist. Planned for
  CR-BP-21a.
- **Process-Context id format**: register v2's `process_context` field
  carries full-slug ids (`pc-pr-build`, `pc-ge-operate`, etc.); the
  existing context files use short codes (`pc-pr-b`, `pc-ge-op`).
  `check_process_context.py` accepts both — no gate failure. Renaming the
  10 existing context files would touch every L2 reference and yield zero
  compliance benefit; deferred.
- **L1 Process Group landings for unadmitted domains** (StrategyAndDirection,
  AgencyAndOrganization, ProductAndValue, EnablementAndOperations,
  FinanceAndAccounting): the 5 unadmitted v2.4.0 domains. Planned tranches
  CR-BP-21a..e.
- **BP-AR / DOC-001 advisory findings**: pre-existing, not introduced by
  this CR.

## 3. Changes

### 3.1 Group rename (`dea:group-strategy-and-governance-conception` → `dea:group-governance-conception`)

- File `entities/v1-alpha/dea:group-strategy-and-governance-conception/dea:group-strategy-and-governance-conception.yaml`
  is renamed to `dea:group-governance-conception/dea:group-governance-conception.yaml`
  (and the README.md sibling).
- `id:`, `name:`, `definition:`, `scope.includes:` updated to remove
  "strategy" framing per Option A. Scope remains governance-mandate /
  policy / charter conception only.
- `change_history` gains an entry pointing at CR-BP-20 with rationale
  "v2.4.0 Option A split: Develop corporate strategy migrated to
  StrategyAndDirection × Conceive (CR-BP-21a, planned)."
- `composes:` is left pointing at the existing two L2s
  (`dea:process-develop-governance-strategy`,
  `dea:process-initiate-policy-and-charter`); the former is the
  future-migration candidate, the latter remains the group's stable
  principal.

### 3.2 L2 split mapping (`dea:process-develop-governance-strategy`)

- Identity, scope, intent, type unchanged.
- `change_history` gains an entry: "Scheduled migration to
  StrategyAndDirection × Conceive cell `dea:pc-sd-conceive` once that
  cell and its Process Group land (CR-BP-21a). Until then this process
  remains affiliated with GovernanceAndExistence × Conceive; v2.4.0
  excludes strategic choices from Governance & Existence
  (domain-grounding.md §3.1 boundary: 'governance authorizes but does
  not direct; Strategy & Direction directs within the authorized
  frame')."

### 3.3 Outcome alignments (3 processes)

For each of the 3 processes, `outcome:` is brought to agreement with
`identity.outcome_statement:` by adopting the longer form (the longer
form is authoritative per CR-BP-14 S21 — identity.outcome_statement is
the canonical outcome).

- `dea:process-customer-channel-and-acquisition-build`: outcome
  extended to "Channel infrastructure and acquisition engines are
  operational, integrated with the designed experience, and ready to
  acquire first customers."
- `dea:process-customer-experience-design`: outcome extended to
  "A customer experience design with articulated touchpoints,
  interaction patterns, and quality criteria is committed and ready to
  be built."
- `dea:process-market-and-demand-conception`: outcome extended to "A
  market and demand thesis with testable hypotheses, initial segment
  targets, and a test plan is committed and ready to be designed."

### 3.4 CATALOG.yaml

Regenerated (git-date `last_modified` for the touched subtrees).
ID rename from `dea:group-strategy-and-governance-conception` to
`dea:group-governance-conception` reflected.

## 4. Verification

- All 15 conformance gates pass (conformant).
- pytest 148 pass / 1 pre-existing failure (`test_check_struct_clean_repo_passes`,
  unrelated, pre-dates this CR).
- BP-ARC-ID-003 outcome mismatch count: 3 → 0.
- CR-META `--strict-provenance`: 0 new findings; CR-BP-20's
  `change_history` populates the new entries for the renamed group and
  the 3 alignment-fixed processes.
- Admission gate: pass (no new entities; the L1 group rename does not
  require re-admission — it's a re-scope under an existing admission).
- Fresh-clone reproduction: clone `feature/cr-bp-20-alignment-v240`
  into `/tmp`, run `scripts/regenerate_catalog.py --check`, exit 0.