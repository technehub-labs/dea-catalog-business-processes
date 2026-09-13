# Changelog

All notable changes to this repository are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows
`docs/versioning.md`.

## [Unreleased]

## [v0.3.0] - 2026-09-12

Third tagged release. Captures the entire post-v0.1.0 work as a single versioned snapshot: the ECF v2.3.0/v2.4.0/v2.5.0 cascade (CR-BP-17, -18, -23), the BP-32/33/34 tranche plan (CR-BP-32, -33, -34a-d, -35, -36, -37, -38), the XRI asset + gate promotion (CR-BP-37 + CR-BP-40), the CHANGELOG + README reconciliation (CR-BP-39), and the carrier CRs (CR-BP-30, -31). The catalogue at v0.3.0 is materially different from v0.1.0 in every dimension that downstream consumers care about.

Per `docs/versioning.md` §"What triggers a version bump", this is a **minor bump** capturing a canonical admission wave + a Domain rename cascade (ECF v2.3.0/v2.4.0/v2.5.0). Not patch (those are reserved for documentation / governance-artifact reconciliations); not major (those require ECF stability + sustained conformance).

The stranded `## [v0.2.0]` block below this section represents a never-tagged release state per user directive 2026-09-12 ("ignore the cut"); it is preserved as a historical artifact of the abandoned v0.2.0 cut (CR-BP-29, PR #66 MERGED on 2026-09-09). The first tag after `v0.1.0` is `v0.3.0`.

The 14 CRs that accumulated under `[Unreleased]` since v0.1.0 was cut:

### CR-BP-34c: Lifecycle State-Machine Validators (LCM-001..005) — third execution slice of CR-BP-34

Codifies the lifecycle state-machine rules from CR-BP-34 §10 as a
standalone, machine-testable validator. LCM-001 (lifecycle_status
vocabulary) + LCM-002 (status ↔ lifecycle_status consistency) +
LCM-003 (deprecated must carry DEPRECATED transition marker) +
LCM-004 (non-deprecated must NOT carry DEPRECATED marker) +
LCM-005 (retired records must live in entities/_retired/, forward-
only). New script `scripts/check_lifecycle_state.py` plus new test
`tests/test_check_lifecycle_state.py` (27 tests). Wired into
`scripts/conformance_result.py` as gate **[13] Lifecycle State-
Machine (LCM-001..005)** (advisory; non-blocking).

**Coverage on the live catalog:** all 126 canonical Business Process
records satisfy all five rules; validator emits 0 findings today.
The validator is a pure regression guard.

**Important finding during design:** narrative mentions of
"lifecycle_status=deprecated" in `change_history` (camelCase,
lowercase) had to be distinguished from transition-event mentions
of "DEPRECATED" (UPPERCASE). The 6-state machine lives at the
record level; case-sensitive marker match cleanly separates the
two patterns. The 1 live deprecated record (`dea:process-develop-
governance-strategy`) carries both DEPRECATED markers in its
`change_history` and passes LCM-003.

**Forward-only LCM-005** — no retired records exist today; the rule
catches future records marked `lifecycle_status=retired` that
haven't been moved into the archive directory. Additive-only.
Carrier: [CR-BP-34c](change-requests/CR-BP-34c-lifecycle-state-machine.md).

### CR-BP-34b: Intent Purposive Validators (PSP-001..003) — second execution slice of CR-BP-34

Codifies the three Intent purposive rules from CR-BP-34 §7 as a
standalone, machine-testable validator. PSP-001 (Intent shall be
purposive) + PSP-002 (approved vocabulary) + PSP-003 (shall not
encode organizational ownership). New script
`scripts/check_intent_purposive.py` plus new test
`tests/test_check_intent_purposive.py` (20 tests). Wired into
`scripts/conformance_result.py` as gate **[12] Intent Purposive
(PSP-001..003)** (advisory; non-blocking).

**Coverage on the live catalog:** all 126 canonical Business Process
records pass all three rules; validator emits 0 findings today.
The validator is a pure regression guard. Additive-only; no entity,
schema, validator-rule, or governance-decision change.
Carrier: [CR-BP-34b](change-requests/CR-BP-34b-intent-purposive-validators.md).

### CR-BP-34a: L2 Qualification Validators (BP-C1..C4) — first execution slice of CR-BP-34

Codifies the four mandatory L2 qualification criteria from CR-BP-34
§11 (BP-C1 Input–Output Transformation, BP-C2 Objective Contribution,
BP-C3 Standalone Executability, BP-C4 Resource Dedication) as a
standalone, machine-testable validator. New script
`scripts/check_l2_qualification.py` plus new test
`tests/test_check_l2_qualification.py` (17 tests). Wired into
`scripts/conformance_result.py` as gate **[11] L2 Qualification
(BP-C1..C4)** (advisory; non-blocking).

**Coverage on the live catalog:** all 126 canonical Business Process
records pass all four criteria; validator emits 0 findings today.
The validator is a **regression guard** — it catches any future BP
that violates one or more criteria at admission time, without
disrupting any existing record.

No entity, schema, validator-rule, governance-decision, or
conformance-gate change to existing behaviour. Additive-only.
Carrier: [CR-BP-34a](change-requests/CR-BP-34a-l2-qualification-validators.md).

### CR-BP-32/33/34 introduced (carrier PRs — knowledge harvest + positioning only)

Three foundational CRs authored by eaojnr (2026-09-10) that extend
the catalog into L3 (Activity) and L4 (Task / Workflow / Execution
Boundary), plus a four-level conformance profile. Renumbered from
the user's CR-BP-04/05/06 because the canonical IDs are already
allocated (CR-BP-04 is MERGED as ID-Family Reconciliation).

**This is a documentation carrier only.** No code, no schema, no
validator change. The renumbering decisions and the additive
harvest plan are in `01_plan/CR-BP-32-33-34-foundation/POSITIONING.md`.

Six genuinely novel insights identified in the harvest:

1. L2 qualification becomes a validator (BP-C1..C4).
2. Lifecycle status becomes a state machine (6-state lifecycle).
3. Semantic-identity-vs-version becomes an explicit rule.
4. Intent cannot be substituted for organizational component (PSP-001..003).
5. The Activity / Task / Workflow layer is genuinely missing (the single largest gap).
6. MECE validation is real work not yet attempted (CR-BP-36).

**Execution plan:** Phase 2 lands additive conformance validators
(CR-BP-34a/b/c/d — no entity mutation). Phase 3 lands the L3
Activity record type (CR-BP-32). Phase 4 lands the L4 Execution
Boundary (CR-BP-33). Phase 5 documents the closure (CR-BP-35..38).

The 196 canonical records stay at conformance level L4 throughout.

Carrier PR pending; awaiting user direction on execution order.

### CR-BP-30 introduced: Release Package for `dea-catalog-processes` (carrier CR — discussion only)

Defines the artifact family and the CI shape that will produce the
`v0.3.0` (or later) release zip. **No code, no schema, no validator
change in this PR.** Six design decisions (§3 of the CR body) are
tabled for user lock-in at merge time; defaults are listed in the
CR's §0 TL;DR table. Implementation slices CR-BP-30a..30h are
sequenced in the CR's §5 and land in independent, revertable PRs
once D1–D6 are resolved.
Carrier: [CR-BP-30](change-requests/CR-BP-30-release-package.md).

### CR-BP-31 implementation: PartyAndRelationship canonical `serves` migration-pair

Paperwork-only normalization. Appends the canonical v2.5.0
`ecf:partyRelationship.<stage>` `serves` relationship alongside the
preserved v2.3.0 `ecf:customerAndDemand.<stage>` entry on 7
PartyAndRelationship L2 records (Conceive 2 / Design 3 / Operate 1
/ Improve 1). No entity ID or name change, no register change, no
L1 group change, no schema change, no disposition change. Adds a
new regression guard `scripts/check_canonical_serves.py` so future
migration-pair drift is caught at CI time. Closes the last v2.3.0
-> v2.5.0 migration-pair debt in the catalog; the six other ECF
Domains already carried canonical serves pairs. Carrier:
[CR-BP-31](change-requests/CR-BP-31-pr-canonical-serves-migration.md).

### CR-BP-34d implementation: Semantic-Identity-vs-Version Validators (SIV-001..004) — fourth execution slice of CR-BP-34

Codifies CR-BP-34 §19 as four machine-testable rules:
SIV-001 (every record's version follows SemVer), SIV-002 (every
version bump carries `change_history` evidence), SIV-003 (a MAJOR
bump requires a semantic-change marker from the controlled
vocabulary: `BREAKING` / `SEMANTIC` / `RENAME` / `REC-` /
`DEPRECATED` / `SUPERSEDED` / `CR-BP-` / `CR-ECF-` / `CR-AR-` /
`CR-MM-` / `CR-OU-` / `CR-BC-` / `CR-BO-`), SIV-004 (a MINOR / PATCH
bump shall not silently alter `identity.verb` or `identity.object`;
advisory only). New script `scripts/check_semantic_identity_version.py`
plus new test `tests/test_check_semantic_identity_version.py`
(43 tests). Wired into `scripts/conformance_result.py` as gate
**[14] Semantic Identity vs Version** (advisory; non-blocking).

**Coverage on the live catalog:** all 126 canonical Business
Process records satisfy all four rules; validator emits 0
findings today. The single v2.0.0 record
(`dea:process-develop-corporate-strategy`) carries a `CR-BP-21a`
marker in its `metadata.change_history` and passes SIV-002 +
SIV-003 cleanly. The SIV-004 advisory does not block; the bare
MINOR/PATCH semantics are otherwise enforced by SIV-001..003
combined.

**Forward-only SIV-004** — the rule is advisory (does not block);
the other three rules are sufficient to catch every major-bump
without a semantic marker. The 43-case test suite establishes the
advisory semantics independently.

Carrier:
[CR-BP-34d](change-requests/CR-BP-34d-semantic-identity-vs-version.md).

### CR-BP-32 implementation: Activity Model Validators (ACT-001..010) — first execution slice of Phase 3

Codifies the CR-BP-32 §15 Activity Model rules as ten
machine-testable invariants: ACT-001 (every Activity belongs to a
Business Process), ACT-002 (Activity is not a Business Process),
ACT-003 (cohesion rationale ≥ 20 chars), ACT-004 (composed Task OR
`decomposition_boundary: l4-reached` marker), ACT-005 (composition
uses `dea:composes`; forbidden fields: `parent_activity` /
`child_activities` / `decomposes` / `contains_activity`), ACT-006
(no execution-ordering fields), ACT-007 (Activity id ≠ Business
Function id family), ACT-008 (no implementation-detail marker
fields — L4 is the decomposition boundary), ACT-009 (no
execution-model fields — CR-BP-33 owns execution), ACT-010
(bidirectional traceability: parent BP declares the Activity in
`metadata.activity_references[]` or `composes[]`). New script
`scripts/check_activity_model.py` plus new test
`tests/test_check_activity_model.py` (34 tests); new schema
`schemas/entities/activity.schema.json` (JSON Schema draft-07,
`additionalProperties: false`); `metamodel-pointer.yaml` registers
`dea:Activity` additively as `lifecycle: proposed`,
`catalog_repo: dea-catalog-processes`. Wired into
`scripts/conformance_result.py` as gate **[15] Activity Model**
(advisory; non-blocking).

**Coverage on the live catalog:** 0 Activity records today;
validator emits 0 findings by construction (type-discriminator
filter never inspects BP records). The validator is a pure
forward-looking regression guard for the first Activity
contribution. Activity is registered as a catalog-owned record
type (mirrors how `dea:ProcessGroup` is declared under
CR-BP-SPEC-BP-01).

Carrier:
[CR-BP-32](change-requests/CR-BP-32-activity-model.md).

### CR-BP-33 implementation: Execution Boundary Validators (EXE-001..010) — first execution slice of Phase 4

Codifies the CR-BP-33 §15 Execution Boundary rules as ten
machine-testable invariants: EXE-001 (structural decomposition does
not encode execution sequence), EXE-002 (`dea:composes` does not
imply execution ordering), EXE-003 (Workflow remains distinct from
Business Process — no BP classification on Workflow records),
EXE-004 (multiple execution Workflows require `workflow_references[]`
list, not a singleton field), EXE-005 (multiple Workflow
realizations do not split the BP — singular `process_intent` /
`process_type` axes), EXE-006 (execution actors reference
`dea:actor-*` semantics, not inline strings), EXE-007 (execution
systems reference `dea:system-*` semantics), EXE-008 (execution
logic does not redefine process identity — Workflow records carry
no `identity.verb` / `identity.object`), EXE-009 (no
implementation-detail fields — `api_sequence`, `script`,
`code_ref`, etc. forbidden), EXE-010 (every `workflow_references[]`
entry declares `relationship_kind` from the controlled vocabulary:
`reference` / `operational` / `scenario` / `implementation`). New
script `scripts/check_execution_boundary.py` plus new test
`tests/test_check_execution_boundary.py` (32 tests).
`metamodel-pointer.yaml` references `dea:Workflow` / `dea:Task`
additively from the dea-metamodel registry
(`lifecycle: proposed`, `catalog_repo: null`; metamodel-owned). Wired
into gate **[16] Execution Boundary** (advisory).

**Coverage on the live catalog:** 161 records checked, 0 opted-in,
0 findings. Pure forward-looking regression guard for the first
Workflow / Execution contribution. The Workflow / Task record
types remain metamodel-owned; the catalog does not define local
Workflow records.

Carrier:
[CR-BP-33](change-requests/CR-BP-33-execution-boundary.md).

### CR-BP-36 implementation: MECE Validation (MECE-001..008) — first execution slice of Phase 5

Codifies catalog-wide MECE (CR-BP-34 §4 distinguishes Conformance
from MECE) as eight machine-testable invariants: MECE-001
(coordinate coverage — every register-landed coordinate has a PC
record), MECE-002 (group coverage per context), MECE-003 (BP
coverage per group), MECE-004 (BP semantic uniqueness via
`(identity.verb, identity.object)`), MECE-005 (group coordinate
uniqueness via `(process_context, name)`), MECE-006
(register-to-catalog alignment), MECE-007 (orphan detection
PG → PC), MECE-008 (orphan detection BP → PG; deprecated records
exempt). Coordinate matching uses `(domain, lifecycle_stage)` to
bridge the legacy full-word vs abbreviated PC id convention drift
(`dea:pc-ge-conceive` vs `dea:pc-ge-c`). New script
`scripts/check_mece.py` plus new test `tests/test_check_mece.py`
(23 tests). Wired into gate **[17] MECE Validation** (advisory).

**Real finding caught in-slice:** pre-slice live run found 1
MECE-008 violation (`dea:process-secure-funding-facilities` listed
in `dea:pc-fa-build.processes` but missing from
`dea:group-financial-build.composes[]`). Remediated in-slice: the
PG record's `composes[]` block was extended with the missing entry
plus a `change_history` entry bumping `v1.2.0` → `v1.3.0`; the
baseline SHA256 in `reconciliation/baseline/v1.yaml` was updated
to match.

**Important design decision:** MECE-008 exempts records with
`lifecycle_status: deprecated` from the orphan check. The
deprecated `dea:process-develop-governance-strategy` (superseded
by `dea:process-develop-corporate-strategy` per CR-BP-21a) is
correctly exempt. This is the register-wide policy from
`l1-register.yaml` (CR-BP-19 §3; Activate/Retire and superseded
records are intentionally not composed by any Process Group).

**Coverage post-remediation:** 161 records evaluated; 0 findings
across MECE-001..008. Validator emits a clean
CONFORMANT result.

Carrier:
[CR-BP-36](change-requests/CR-BP-36-mece-validation.md).

### CR-BP-35 implementation: Process Catalog Architecture Retrospective

Documentation-only slice that closes the loop between the
user's original CR-BP-07 (the "what would the BP-07 architecture
look like?" framing) and the architecture that has actually landed
in `main` after Phase 1..4 harvest tranches plus Phase 5 slice 1
(CR-BP-36 MECE).

**Surfaces four deltas from the original CR-BP-07 framing:**

1. Landing order was inverted: the catalog was populated before
   the BP-32/33/34 foundation carrier landed. CR-BP-11 → CR-BP-19
   → CR-BP-21 tranches ran 2026-09-04 to 2026-09-08; CR-BP-32/33/34
   foundation landed 2026-09-09 (PR #69).
2. L0..L4 conformance levels were introduced by CR-BP-15-IMP and
   CR-BP-16 (PRs #38–42), not in the original CR-BP-07 framing.
3. Kernel + specialization discipline was introduced by
   CR-MM-PROC-01 / CR-AR-FMWK-01 / CR-BP-SPEC-BP-01
   (PRs #12, #163 metamodel, #10 architecture-framework).
4. The validator library (now 22 gates in
   `scripts/conformance_result.py`) was established as a
   first-class artifact, not a side-effect of conformance work.

**Documents:** eight-slot decomposition (Process Context → Scope →
Process Group → Business Process → Activity → Workflow / Task);
six characterization dimensions (CR-BP-14); cross-repo contracts
(dea-metamodel, dea-architecture-framework, WSF, ECF); ECF
version history (v2.3.0 / v2.4.0 / v2.5.0 with companion catalog
CRs CR-BP-17 / -18 / -23).

**No validator, no schema, no record mutation, no gate wiring.**
Paperwork-only slice; ~180 LOC equivalent (single CR doc).

Carrier:
[CR-BP-35](change-requests/CR-BP-35-process-catalog-architecture.md).

### CR-BP-37 implementation: Cross-Repository Integrity Validators (XRI-001..005)

Documents the catalog's cross-repo reference surface and
codifies five invariants about `metamodel-pointer.yaml` +
`change-requests/README.md` `## Cross-repo context`: XRI-001
(metamodel-pointer.yaml structure), XRI-002 (entity entry
completeness), XRI-003 (federation mapping + canonical CR
lineage references), XRI-004 (entity_id uniqueness), XRI-005
(companion CR lineage references resolve).

**Cross-repo surface documented:**

- **Canonical lineage** (load-bearing): `CR-MM-PROC-01`
  (dea-metamodel PR #163, commit `1665209`) declares `dea:Process`
  (abstract kernel) + `dea:BusinessProcess` (specialization);
  `CR-AR-FMWK-01` (dea-architecture-framework PR #10, commit
  `76463b2`; tag `v0.6.0`) declares `dea:entity-process` (root-model
  kernel; `discriminator: process-kernel`) +
  `dea:entity-business-process` (specialization; `class_alias: BP`).
  Federation mapping: **1:1 LOSSLESS** (kernel ↔ kernel;
  specialization ↔ specialization).
- **ECF conformance lineage** (dea-metaframework): `CR-ECF-CG-001..004`
  (gate; catalog companion: gate [8]); `CR-ECF-006 + ADR-ECF-001`
  (v2.3.0; catalog: CR-BP-17 PR #44); `CR-ECF-007 + ADR-ECF-002`
  (v2.4.0; catalog: CR-BP-18 PR #45); `CR-ECF-008 + ADR-ECF-003`
  (v2.5.0; catalog: CR-BP-23 PR #61).
- **Companion catalog CRs** (sibling repos): `CR-BC-ECF-03`
  (dea-catalog-business-capabilities); `CR-BO-02`
  (dea-catalog-business-objects); `CR-OU-02`
  (dea-catalog-organizational-units).
- **WSF lineage:** `wsf:Process` (Tier-3 derived).

**Implementation:** new script
`scripts/check_cross_repo_integrity.py` plus new test
`tests/test_check_cross_repo_integrity.py` (23 tests). Runtime
asset (NOT a CI gate — promotion to gate [18] deferred to a
future CR).

**Coverage on the live catalog:** 0 findings across XRI-001..005.
The validator is a forward-looking regression guard for the first
sibling-repo CR added without proper lineage references.

Carrier:
[CR-BP-37](change-requests/CR-BP-37-cross-repo-integrity.md).

### CR-BP-38 implementation: ECF Matrix Population Retrospective

Documentation-only retrospective of how the catalog's ECF matrix
(7 domains × 7 stages = 49 coordinates) was discovered, ratified,
and populated with Process Group (PG), Process Context (PC), and
Business Process (BP) records from CR-BP-11 (L1 discovery) through
CR-BP-28 (register v4 re-derivation under ECF v2.5.0), including
the seven admission tranches (CR-BP-21a/b/c/d/e/f +
21a.1/b.1/c.1/d.1/e.1) that closed every register gap.

**Lineage walk-through (11 CRs):**

1. CR-BP-11 — L1 Process Group Discovery (research methodology;
   49 candidate coordinates).
2. CR-BP-12 — Process Group Profile (structural shape; PG entity
   in `metamodel-pointer.yaml`).
3. CR-BP-13 — Research Ratification (v1 register; partial).
4. CR-BP-14 — Process Semantic Reconciliation (six dimensions).
5. CR-BP-17 — ECF v2.3.0 Domain enum migration (PR #44).
6. CR-BP-18 — ECF v2.4.0 Domain enum migration (PR #45).
7. CR-BP-19 — L1 Register Re-derivation (v2.4.0; 35 ratified).
8. CR-BP-21a-f + 21a.1/b.1/c.1/d.1/e.1 — Domain admission tranches
   (7 domains; 10 PRs #51–60).
9. CR-BP-22 — Register `audit_status` axis (4-value enum).
10. CR-BP-23 — ECF v2.5.0 Domain 6 rename
    (`OperationsAndEnablement` → `EnablementAndOperations`)
    (PR #61).
11. CR-BP-28 — Register v4 re-derivation (ECF v2.5.0; 35 ratified +
    14 backlog-deferred; ratified 2026-09-08) (PR #65).

**Current matrix state** (2026-09-12, register v4):

- 7 domains: `GovernanceAndExistence`, `StrategyAndDirection`,
  `AgencyAndOrganization`, `PartyAndRelationship`, `ProductAndValue`,
  `EnablementAndOperations`, `FinanceAndAccounting`.
- 7 stages: `Conceive` → `Design` → `Build` → `Activate` → `Operate`
  → `Improve` → `Retire`.
- 49 coordinates: 35 ratified + 14 backlog-deferred.
- Population: 162 PGs, 36 PCs, 161 BPs at L4 conformance.

**Per-domain ratification status:**

| Domain | Ratified | Backlog |
|---|---|---|
| GovernanceAndExistence | 7/7 | 0 |
| StrategyAndDirection | 7/7 | 0 |
| AgencyAndOrganization | 7/7 | 0 |
| PartyAndRelationship | 6/7 | 1 (Retire) |
| ProductAndValue | 7/7 | 0 |
| EnablementAndOperations | 6/7 | 1 (Retire; v2.5.0 rename) |
| FinanceAndAccounting | 5/7 | 2 (Improve + Retire) |

**No validator, no schema, no record mutation, no gate wiring.**
Paperwork-only slice; ~180 LOC equivalent. Closes Phase 5 and the
BP-32/33/34 tranche plan.

Carrier:
[CR-BP-38](change-requests/CR-BP-38-ecf-matrix-population-retrospective.md).

### CR-BP-40 implementation: Cross-Repository Integrity Gate Promotion (XRI-001..005 → Gate [18])

Promotes `scripts/check_cross_repo_integrity.py` from a runtime
asset (landed in CR-BP-37, PR #78) to a conformance gate wired
into `scripts/conformance_result.py` as gate **[18] Cross-
Repository Integrity (XRI-001..005)** (advisory; non-blocking).
Follows up on the explicit deferral in CR-BP-37 §3.

**Wiring:** adds one entry to the GATES list, immediately after
gate [17] MECE Validation:

```python
("[18] Cross-Repository Integrity (XRI-001..005)",
 False, ["python", "scripts/check_cross_repo_integrity.py",
         "--strict"]),  # CR-BP-40; advisory
```

The runtime asset is unchanged. Its `--strict` mode already returns
exit code 1 on any finding (`scripts/check_cross_repo_integrity.py:402`),
matching the contract used by gates [11]–[17] for their respective
validators.

**Promotion rationale:**

1. The runtime asset has run 0 findings across XRI-001..005 on
   every CI invocation since PR #78 merged (PRs #79, #80, and the
   CR-BP-40 PR). Stable.
2. The tranche plan is closed; the next CI-driven drift is more
   likely to come from a sibling-repo CR addition than from a
   local pointer edit. XRI-005 is the explicit regression guard
   for that case.

**Promotion decision:** advisory (non-blocking). XRI-005 is
forward-looking; making it blocking would either be a no-op today
(all rules pass) or would block the first PR that adds an
ungrounded companion CR. The advisory status lets CI surface the
finding while the catalog maintainer decides.

**Coverage on the live catalog:** gate [18] reports CONFORMANT
with 0 findings across XRI-001..005. The promotion adds zero
new noise; it converts a maintainer-run check into a CI check.

**Repo totals post-slice:** 23 conformance gates (was 22); 10
blocking + 13 advisory.

**No entity, schema, validator-rule, or canonical-record change.**
Pure additive wiring slice; ~10 LOC of code + paperwork.

Carrier:
[CR-BP-40](change-requests/CR-BP-40-xri-gate-promotion.md).

## [v0.2.0] - 2026-09-09

Second tagged release. Carries the formal L1 register v4
re-derivation against the upstream ECF v2.5.0 vocabulary (CR-BP-28,
PR #65). The catalogue at this tag is functionally identical to
v0.1.0: 196/196 records at CR-BP-16 conformance level L4; 0
findings (blocking and advisory); register audit 35 landed / 0
ratified-pending-landing / 14 backlog-deferred; dispositions 107
RETAIN / 18 RECLASSIFY / 1 MOVE. The bump (0.1.0 -> 0.2.0) is the
register-version stamp, not a content change. Downstream consumers
of the L1 register itself should pin to this tag for register-v4
fidelity.

Carrier: CR-BP-29. The single CR that accumulated under
`[Unreleased]` since v0.1.0:

### CR-BP-28 implementation: register v4 re-derived against ECF v2.5.0

Re-derives the L1 register against ECF v2.5.0 as
`ratification.version: 4` (was `v3` under CR-BP-22). The v2.4.0 ->
v2.5.0 transition (CR-ECF-008 + ADR-ECF-003; Domain 6
`OperationsAndEnablement` -> `EnablementAndOperations`) was a
label-only rename; no coordinate was added, removed, or
re-scoped. Register audit remains 35 / 0 / 14. `l1-register.yaml`
and `l1-candidate-universe.yaml` bump `ratification.version` 3 ->
4 and `ratification.cr` CR-BP-22 -> CR-BP-28; `L1-REGISTER-v0.1.md`
updates its status line and adds a v3 -> v4 note. The
re-derivation is the formal v4 ratification; the release cut
(v0.2.0) is its own separate slice. No entity, schema,
validator-rule, or CI-pipeline change.

## [v0.1.0] - 2026-09-09

First tagged release. Closes the CR-BP-15 Phase 20 governance gate
(CR-BP-25, 2026-09-09) and freezes the post-landing-programme
snapshot. The catalogue at this tag is the artefact downstream may
pin to: 196/196 records at CR-BP-16 conformance level L4; 0 findings
(blocking and advisory); register audit 35 landed / 0
ratified-pending-landing / 14 backlog-deferred; dispositions 107
RETAIN / 18 RECLASSIFY / 1 MOVE.

Carrier: CR-BP-26. The four sub-programmes accumulated under this
release, in landing order:

### CR-BP-25 implementation: Phase 20 governance review closes CR-BP-15 §22

Records the Phase 20 decision at
`docs/governance/phase-20-review-crbp15.md` against the five
CR-BP-15 §22 criteria (no semantic regressions; no lost provenance;
no unresolved canonical ambiguity; no accidental ontology expansion;
no ECF-driven artificial processes). Evidence: 196/196 records at
CR-BP-16 conformance level L4; 0 findings (blocking and advisory);
register audit 35 landed / 0 ratified-pending-landing / 14
backlog-deferred; dispositions 107 RETAIN / 18 RECLASSIFY / 1 MOVE.
The CR-BP-15 and CR-BP-16 index rows move from "Phase 20 governance
approval pending" to "closed by CR-BP-25, 2026-09-09";
`docs/versioning.md` becomes Active; the first release cut is
actionable. No entity, schema, validator-rule, or CI-pipeline change.

### CR-BP-24 implementation: programme closure reconciliation. Reconciles
tracking artifacts with catalog reality now that the seven-domain
landing series is complete (register audit 35 landed / 0 pending / 14
backlog-deferred; CR-BP-16 conformance report scores all 196 records
at level L4). Closes the 10 stale `proposed` tranches in
`reconciliation/tranches/plan.yaml` (`status: applied` with
`applied_by` / `applied_pr`; `plan_status` PRELIMINARY -> EXECUTED);
corrects stale CR index statuses (CR-BP-15/16 Implemented, CR-BP-21f.1
Merged PR #60, CR-BP-23 Merged PR #61); extends the root README CR
table through CR-BP-24; authors `docs/versioning.md` so the
CHANGELOG reference resolves. No entity, schema, validator-rule, or
CI pipeline change. Phase 20 governance approval for CR-BP-15 is
explicitly NOT claimed by this CR; that gate is the trigger for the
first release cut per `docs/versioning.md`.

### CR-BP-23 implementation: ECF Domain Enum v2.5.0 migration. ECF Domain 6
is renamed from `OperationsAndEnablement` (v2.4.0) to
`EnablementAndOperations` (v2.5.0), driven by the Domain/Stage
Orthogonality Stress Test (`dea-metaframework` ADR-ECF-003 §5;
CR-ECF-008). The Domain 6 name shared a lexical root with Stage 5
`Operate`, obscuring the orthogonality that the ECF requires between
the Domain axis and the Stage axis. The rename swaps the two nouns:
`Enablement` now leads (lexically distinct from any Stage name) and
`Operations` trails (the sustained day-to-day concern, not the
lifecycle Stage).

**Files touched**: 129 files + 1 new CR carrier + reconciliation
regeneration. See `change-requests/CR-BP-23.md` for the full mapping
table and validation evidence.

**Unchanged**: Domain number (6), matrix position, semantic anchor
(`Execution`), seven-Domain partition, seven lifecycle Stages, Stage 5
name (`Operate`), catalog ID abbreviation `oe` (stable; not re-keyed),
group ids (`dea:group-operations-and-enablement-*` are stable
identifiers per CR-ECF-008 §18 non-goal "no content redistribution").

**Verification**: ECF conformance PASS (161 entries); PC PASS
(PC-001..PC-008); BP-SPEC PASS (BP-SPEC-01-001..007); PG PASS
(PG-001..008); register audit PASS (35 landed / 0 pending / 14
deferred); CATALOG.yaml no drift.

### CR-BP-21f.1 implementation: GovernanceAndExistence completion
(retroactive completion for the pre-register-v2-discipline domain).
GE's register v2 candidate list was never fully populated when the
domain was seeded under CR-BP-13a; audit found the entire
risk-framework track (one candidate per lifecycle stage) plus
assurance-review, audit-findings-scoring, and policy-framework-
improvement unlanded. Lands 7 new L2 processes (Conceive 1,
Design 1, Build 1, Operate 2, Improve 2); extends the 5 existing
GE Process Groups' composes edges and the 5 GE contexts' processes
lists. All 18 register v2 GE candidates are now covered by 16 BPs
(9 seeds + 7 new). Disposition register +7 RETAIN; tranche plan
60 to 65; inventory 119 to 126 BPs.

### CR-BP-21e.1 implementation: FinanceAndAccounting completion (fifth
and final domain-completion tranche; closes the v2.4.0 register
scope). Lands the 4 remaining FA Process Groups
(`dea:group-financial-design`, `-financial-build`, `-financial-operate`,
`-financial-improve`) and the 15 remaining register v2 FA L2
candidates (Conceive 0, Design 3, Build 3, Operate 7, Improve 2);
extends `dea:group-financial-model-conception` with composes edges
for the 4 already-landed 21e L2s (one per non-Conceive cell); extends
the 5 FA Process Contexts' processes lists. Register v3 audit final
state: **35 `landed` / 0 `ratified-pending-landing` / 14
`backlog-deferred`**. FA D/B/O/Im audit_status flipped to `landed`.
Disposition register +15 RETAIN; tranche plan 55 to 60.

Two L2s needed `process_type` flips driven by BP-ARC-ID-004 keyword
density (`operate-financial-reporting-and-disclosure` to core;
`onboard-tax-and-compliance-capability` to management). One L2 was
reworded for the same reason (`tax-and-compliance-capability`
outcome now supervised by the tax policy review).

### CR-BP-21d.1 implementation: EnablementAndOperations completion
(fourth domain-completion tranche; the largest, reflecting OE's
execution-core position). Lands the 4 remaining OE Process Groups
(`dea:group-process-and-enablement-design`,
`-operations-and-enablement-build`, `-execution-and-fulfillment`,
`-operations-and-enablement-improvement`) and the 23 remaining
register v2 OE L2 candidates (Conceive 3, Design 4, Build 4, Operate
8, Improve 4); extends `dea:group-operations-model-conception` with
composes edges for the 3 new Conceive-cell L2s; extends the 5 OE
Process Contexts' processes lists. Register v3 audit counts updated:
31 `landed` / 4 `ratified-pending-landing` / 14 `backlog-deferred`.
OE is the fourth fully-landed v2.4.0 domain. Disposition register
+23 RETAIN; tranche plan 50 -> 55.

### CR-BP-21c.1 implementation: ProductAndValue completion (third
domain-completion tranche). Lands the 4 remaining PV Process Groups
(`dea:group-proposition-design`, `-product-development`,
`-portfolio-management-operation`, `-product-evolution`) and the 11
remaining register v2 PV L2 candidates; extends
`dea:group-proposition-conception` with composes edges for the 2 new
Conceive-cell L2s; extends the 5 PV Process Contexts' processes
lists. Register v3 audit counts updated: 27 `landed` / 8
`ratified-pending-landing` / 14 `backlog-deferred`. PV is the third
fully-landed v2.4.0 domain at register v2 scope. Disposition register
+11 RETAIN; tranche plan 45 -> 50.

### CR-BP-21b.1 implementation: AgencyAndOrganization completion (second
domain-completion tranche). Lands the 4 remaining AO Process Groups
(`dea:group-organization-and-role-design`,
`-agent-acquisition-and-onboarding`, `-agent-operations`,
`-agent-and-organization-improvement`) and the 13 remaining register
v2 AO L2 candidates; extends
`dea:group-organization-and-agent-conception` with composes edges for
the 2 new Conceive-cell L2s; extends the 5 AO Process Contexts'
processes lists. Substrate-neutral per CR-BP-21b §5 / ADR-ECF-002.
Register v3 audit counts updated: 23 `landed` / 12
`ratified-pending-landing` / 14 `backlog-deferred`. AO is the second
fully-landed v2.4.0 domain at register v2 scope. Disposition register
+13 RETAIN; tranche plan 40 -> 45.

### CR-BP-21a.1 implementation: StrategyAndDirection completion (first
domain-completion tranche). Lands the 4 remaining SD Process Groups
(`dea:group-strategic-choices-design`, `-strategic-plan-build`,
`-strategic-steering-operation`, `-strategic-adaptation`) and the 14
remaining register v2 SD L2 candidates; extends
`dea:group-strategy-direction-conception` with composes edges for the
3 new Conceive-cell L2s; extends the 5 SD Process Contexts' processes
lists. Register v3 audit counts updated: 19 `landed` / 16
`ratified-pending-landing` / 14 `backlog-deferred`. SD is the first
fully-landed v2.4.0 domain at register v2 scope. Disposition register
+14 RETAIN; tranche plan 35 -> 40.

### CR-BP-21e implementation: FinanceAndAccounting landing (fifth and final
v2.4.0 unadmitted-domain tranche). Lands 5 Process Contexts, 1 L1
Process Group (`dea:group-financial-model-conception`), and 5 L2
Business Processes across the FA x {Conceive, Design, Build, Operate,
Improve} cells. v2.4.0 monetary scoping: abstract value removed;
procure-to-pay and order-to-cash operational execution live in
enablement-operations while monetary recording remains here. Register
v3 audit counts updated: 15 `landed` / 20 `ratified-pending-landing` /
14 `backlog-deferred`. FA/Conceive audit_status flipped to `landed`.
With this landing, every v2.4.0 domain has its Conceive-cell L1
Process Group landed. Disposition register +5 RETAIN; tranche plan
30 -> 35.

### CR-BP-21d implementation: EnablementAndOperations landing (fourth
v2.4.0 unadmitted-domain tranche). Lands 5 Process Contexts, 1 L1
Process Group (`dea:group-operations-model-conception`), and 5 L2
Business Processes across the OE x {Conceive, Design, Build, Operate,
Improve} cells. Absorbs execution-side sourcing/asset concerns from the
dissolved v2.3.0 Supply & Resources domain per register v2
migration_notes. Register v3 audit counts updated: 14 `landed` / 21
`ratified-pending-landing` / 14 `backlog-deferred`. OE/Conceive
audit_status flipped to `landed`. Disposition register +5 RETAIN;
tranche plan 25 -> 30.

### CR-BP-21c implementation: ProductAndValue landing (third v2.4.0
unadmitted-domain tranche). Lands 5 Process Contexts, 1 L1 Process Group
(`dea:group-proposition-conception`), and 5 L2 Business Processes across
the PV x {Conceive, Design, Build, Operate, Improve} cells. Register v3
audit counts updated: 13 `landed` / 22 `ratified-pending-landing` / 14
`backlog-deferred`. PV/Conceive audit_status flipped to `landed`.
Disposition register +5 RETAIN; tranche plan 20 -> 25. Per ADR-ECF-002
§5 / CR-ECF-007.

### CR-BP-22 implementation: register audit-status reconciliation. Adds
`audit_status` axis orthogonal to `disposition`, naming the gap between
research-register acceptance and catalog landing reality. As of 2026-09-08:
12 `landed` / 23 `ratified-pending-landing` / 14 `backlog-deferred` across
the 49 ECF coordinates. Each `ratified-pending-landing` coordinate carries
a `planned_tranche` pointer (CR-BP-21a.1, CR-BP-21b.1, CR-BP-21c,
CR-BP-21d, CR-BP-21e). Register ratification bumped v2 -> v3. New
`scripts/check_register_audit.py` (non-blocking tool, runs after each
landing tranche). No canonical entity, no schema, no CI gate change. The
`L1-REGISTER-v0.1.md` persona summary updated with v2 register counts
(35/14) and v3 audit counts (12/23/14).

## [2.4.0-migration] - 2026-09-07

### CR-BP-18 implementation: ECF Domain enum migration to the v2.4.0
canonical Domain set (carried by `technehub-labs/dea-metaframework` v2.4.0;
CR-ECF-007 + ADR-ECF-002). One of seven Domains renamed: Domain 3
`PeopleAndOrganization` -> `AgencyAndOrganization` (kebab-case
`people-organization` -> `agency-organization`), driven by the Substrate
Independence Stress Test. 16 files re-keyed (3 schemas, 3 check scripts,
1 contribution template, 3 research files, 1 docs file, 5 CR records);
reconciliation artifacts regenerated. The DOMAIN_NAMES abbreviation key
`po` -> `ag` in `tools/build_bp13a_tranche.py`. No content redistribution
required (CR-ECF-007 §6.3).

## [2.3.0-migration] - 2026-09-07

### CR-BP-17 (a.k.a. CR-BP-ECF-01) implementation: ECF Domain enum migration to the v2.3.0
canonical Domain set (carried by `technehub-labs/dea-metaframework` v2.3.0;
CR-ECF-006 + ADR-ECF-001). Five of seven Domains renamed; one Domain
replaced (Supply & Resources -> Strategy & Direction). 109 files modified;
5 context YAMLs + 1 CR file renamed; 2 reconciliation artifacts regenerated.

This is the 3rd landing in the v2.3.0 wave (after metaframework + metamodel);
the next is `dea-catalog-business-capabilities` (CR-BC-ECF-01).

### Changed

- **Process Context ID abbreviations** (CR-BP-17 (a.k.a. CR-BP-ECF-01) §1.1, v2.3.0):

  | # | Before (v2.2.0) | After (v2.3.0) |
  |---|------------------|------------------|
  | 1 | `cd` (CustomerAndDemand) | `pr` (PartyAndRelationship) |
  | 2 | `sr` (SupplyAndResources) | `sd` (StrategyAndDirection) |
  | 5 | `po` (ProductAndOffering) | `pv` (ProductAndValue) |
  | 6 | `od` (OperationsAndDelivery) | `oe` (EnablementAndOperations) |
  | 7 | `fv` (FinanceAndValue) | `fa` (FinanceAndAccounting) |

- **5 Process Context YAMLs renamed + content migrated**:
  - `dea-pc-cd-b.yaml` -> `dea-pc-pr-b.yaml` (Party & Relationship x Build)
  - `dea-pc-cd-c.yaml` -> `dea-pc-pr-c.yaml` (Party & Relationship x Conceive)
  - `dea-pc-cd-d.yaml` -> `dea-pc-pr-d.yaml` (Party & Relationship x Design)
  - `dea-pc-cd-im.yaml` -> `dea-pc-pr-im.yaml` (Party & Relationship x Improve)
  - `dea-pc-cd-op.yaml` -> `dea-pc-pr-op.yaml` (Party & Relationship x Operate)
- **1 CR file renamed**: `CR-BP-13a-customer-and-demand-admission.md` ->
  `CR-BP-13a-party-and-relationship-admission.md` (the CustomerAndDemand
  tranche is now the PartyAndRelationship tranche).
- **3 JSON schemas** (`process-context.schema.json`, `entity.schema.json`,
  `contribution.schema.json`): Domain enums migrated to v2.3.0.
- **8 conformance scripts** in `scripts/`: CANON enum, lowercase mapping,
  test fixtures, and disposition records migrated.
- **1 build script** in `tools/build_bp13a_tranche.py`: `DOMAIN_NAMES`
  keys flipped from `cd/sr/pd/od/fv` to `pr/sd/pv/oe/fa`.
- **4 test files** in `tests/`: fixtures migrated.
- **2 reconciliation artifacts regenerated**: `inventory.yaml` and
  `baseline/v1.yaml` (they round-trip byte-identically under the new
  identifiers; `scripts/build_inventory.py --self-test --strict` passes).
- **11 CR files in `change-requests/`**: every narrative reference to
  the v2.2.0 Domain names updated.
- **6 docs files in `docs/`**: narrative updated.
- **README.md** + **change-requests/README.md**: pointers updated.
- All CR/programme references to the renamed Domains re-keyed.

### Not changed (out of scope for the v2.3.0 migration)

- **No new Process Contexts admitted.** The v2.3.0 wave is a pure
  rename; no new coordinates are admitted in this PR.
- **The L1 process discovery work for the renamed Domains** (Strategy
  & Direction, Product & Value, Enablement & Operations, Finance &
  Accounting, Party & Relationship deepening) is parked as a separate
  task that follows this PR — not in scope.
- **The `test_check_struct_clean_repo_passes` pre-existing failure**
  (`STRUCT-OK` is in stdout but the test asserts in stderr) — pre-existing,
  not introduced by this PR.

### Verification

- `tests/conformance/`: 8/8 conformance suites pass.
- `tests/runtime/`: all runtime tests pass.
- `tests/test_build_bp13a_tranche.py`: **15/15 pass**.
- `tests/test_apply_phase_5_tranche.py`: all pass (idempotency holds).
- `tests/test_reconciliation_baseline.py`: 11/12 pass (1 pre-existing
  failure unrelated to this PR).
- `scripts/check_ecf_conformance.py`: **PASS** (28 entries conform).
- `scripts/check_process_context.py`: **PASS** (PC-001..PC-008).
- `scripts/check_process_semantics.py`: **CONFORMANT** (BP-SEM S21).
- `scripts/build_inventory.py --self-test --strict`: **PASS**
  (inventory + baseline round-trip byte-identically under v2.3.0 IDs).

## [2.5.0-conformance-gate] - 2026-09-08

The CR-BP-16 conformance gate machinery (S10 / S15 / S16 / S17 / S18 /
S22 / S25; CR-META strict mode; unified Conformance Result) is now
live in CI. Landed across PRs #38-#42; the second `[Unreleased]`
block that this section replaces predated the CR-BP-22 audit / CR-BP-24
discipline. Date-stamped retroactively per the existing
`[2.4.0-migration]` / `[2.3.0-migration]` pattern.

### CR-BP-16 §16 enforcement promotion (CR-META strict mode)

The CR-META-001..006 gate is now **blocking** in CI for new
and modified CRs. Legacy CRs (mtime < 2026-09-06) remain
advisory. Five CRs were retro-fitted to the §21 metadata
format: CR-BP-03C, CR-BP-12, CR-BP-14, CR-BP-15, and
CR-BP-16. The 16th (CR-BP-13A) was already §21-compliant
and was used as the canonical reference.

- `scripts/check_cr_metadata.py` (extended):
  - **New `--cutoff-date` flag** (default 2026-09-06 = CR-BP-16
    acceptance). CRs last modified on or after the cutoff are
    classified as "new"; CRs modified earlier are "legacy".
  - **New `--strict` mode**: blocks the gate when any NEW CR
    fails any rule. Legacy CRs are reported as advisory and
    do not block.
  - **CR-META-001 normalisation**: `Proposed (2026-09-03)` is
    accepted as a valid `Proposed` Status (parens stripped).
  - **CR-META-002 normalisation**: `L1 (Process Catalog)` is
    accepted as a valid `L1` Layer (parens stripped).
  - **Filename pattern** extended to admit `CR-BP-NN` with
    uppercase letter suffix (legacy `CR-BP-03C`).
  - **Metadata line pattern** admits both `**Key**: value`
    (canonical) and `**Key:** value` (legacy / GitHub-issues).
  - **JSON output** includes `new_findings` and
    `legacy_findings` arrays + `cutoff_date`.
  - Self-test extended with cutoff-aware good and bad fixtures.
- `change-requests/CR-BP-03C-sample-process-contribution.md`:
  added `**Layer**: L1` + `**Owner**: TechNeHub Labs`.
- `change-requests/CR-BP-12-process-group-profile.md`:
  bolded existing metadata + added Layer/Owner.
- `change-requests/CR-BP-14-process-semantic-reconciliation.md`:
  added full §21 metadata block (Status, Layer, Owner, Type,
  Scope, Depends On).
- `change-requests/CR-BP-15-process-catalog-reconciliation.md`:
  added full §21 metadata block.
- `change-requests/CR-BP-16-process-catalog-conformance-gate.md`:
  added §21 metadata for both CR-BP-16 and CR-BP-15-IMP
  blocks.
- `reconciliation/baseline/v1.yaml`: refreshed SHA-256 for
  the 3 CRs whose content changed.
- `reconciliation/inventory.yaml`: regenerated to reflect the
  touched CRs.
- `.github/workflows/ci.yml`: CR-META step now runs
  `python scripts/check_cr_metadata.py --strict`.
- `docs/conformance-pipeline.md`: new "CR Validation (Step 9)
  cutoff policy" subsection documents the policy.
- `tests/test_cr_bp16_gates.py` (extended, 5 new tests):
  - `test_cr_meta_strict_passes_when_no_new_failures`:
    --strict returns 0 when no NEW CR fails.
  - `test_cr_meta_strict_fails_on_new_bad_fixture`: --strict
    fails on a future-dated bad fixture.
  - `test_cr_meta_strict_passes_on_legacy_bad_fixture`:
    --strict passes on a past-dated bad fixture.
  - `test_cr_meta_accepts_layer_with_parenthetical_qualifier`:
    `L1 (Process Catalog)` normalised to `L1`.
  - `test_cr_meta_accepts_status_with_date_qualifier`:
    `Proposed (2026-09-03)` normalised to `Proposed`.

CR-BP-16 §29 acceptance criteria: **11 fully met** (up from 10);
1 partial (provenance schema validation only); 0 unmet.

Conformance Result on the new branch: **CONFORMANT**
BP-SEM live: 0 errors, 0 warnings: CONFORMANT
BP-AR live: 0 findings: CONFORMANT
Conformance Levels: 38/38 at Level 4
CR-META on the new branch: ADVISORY-LEGACY (24 legacy findings,
0 new findings); --strict returns 0.

### CR-BP-16 conformance pipeline (S17/S18/S19/S25) + unified Conformance Result

The CR-BP-16 §17 CI Conformance Pipeline, §18 unified
Conformance Result, §19 blocking-conditions mapping, and
§25 continuous-conformance triggers are now live. Every PR
receives a single CONFORMANCE RESULT verdict that aggregates
all 10 pipeline steps.

- `docs/conformance-pipeline.md` (new, 153 lines): documents
  the 10-step pipeline (Schema, Structure, References,
  Semantics, Hierarchy, Specialization Graph, MECE, Provenance,
  CR Validation, Conformance Result), the blocking-vs-advisory
  matrix, the §19 blocking-conditions mapping (13 conditions),
  and the §25 continuous-conformance triggers. Closes D7
  (the missing visitor-facing pipeline doc).
- `scripts/conformance_result.py` (new, 162 lines): runs all
  15 gates (10 blocking + 5 advisory) and produces a single
  CONFORMANCE RESULT verdict. Verdict is one of CONFORMANT,
  CONFORMANT-WITH-WARNINGS, or NON-CONFORMANT (CR-BP-16 §18).
  `--json` mode emits a structured report. `--strict` treats
  advisory failures as blocking.
- `.github/workflows/ci.yml`: new "Aggregate Conformance
  Result (CR-BP-16 §17/S18)" step runs after the per-gate
  steps. The aggregated verdict is the canonical pre-merge
  source.
- `docs/conformance.md`: links to `docs/conformance-pipeline.md`
  in the See Also block.
- `tests/test_conformance_result.py` (new, 7 tests): verdict
  on live, JSON shape, --strict propagation, pipeline doc
  existence + coverage of all 10 steps, all 13 §19 blocking
  conditions, and all 7 §25 continuous-conformance triggers.

Conformance Result on main: **CONFORMANT**
BP-SEM live: 0 errors, 0 warnings: CONFORMANT
BP-AR live: 0 findings: CONFORMANT
Conformance Levels: 38/38 at Level 4

### CR-BP-16 full conformance gate: S10/S15/S16/S22 machinery

The remaining CR-BP-16 sections called out in §29 acceptance
criteria are now live as CI machinery (advisory). The catalogue
remains **38/38 Level 4 (Canonically Conformant)** and **0
BP-SEM / BP-AR findings**.

- `scripts/check_process_semantics.py` (extended):
  - New rule **BP-SEM-014 Specialization Cycle Detection**
    (CR-BP-16 S10). The specializes graph MUST be acyclic;
    self-specialization and any cycle (A -> B -> ... -> A) are
    architectural regressions. Module docstring updated to
    document BP-SEM-014 alongside BP-SEM-001..013. Self-test
    extended with a cycle fixture.
- `scripts/check_cr_metadata.py` (new): CR-BP-16 S16 metadata
  validator. Six rules (CR-META-001..006) check that every
  architectural CR carries **Status**, **Layer**, **Owner**,
  **Depends on** (with CR-BP-NN refs), **Companion to**, and a
  filename matching the CR-BP-NN pattern. **Advisory** mode:
  legacy CRs lack S21 metadata; CR-BP-13A is the planned first
  CR to demonstrate full S21 compliance.
- `scripts/check_documentation_conformance.py` (new): CR-BP-16
  S22 normative terminology consistency checker. Three rules
  (DOC-001..003) flag legacy synonym usage without the preferred
  term, unresolvable canonical id references, and standalone
  'Process' usage outside compound forms. **Advisory** mode.
- `scripts/check_admission_gate.py` (new): CR-BP-16 S15 new-
  process admission gate. Eight rules (ADM-001..008) check
  Evidence coverage (admission CR in change_history), Identity
  shape, Context resolution, Group fit, Boundary completeness
  (triggers, outcomes), Intent+Classification in approved
  vocabularies, Specialization validity, and Provenance shape.
  **Advisory** mode: surfaces findings on the locked population
  for review.
- `.github/workflows/ci.yml`: new "Run CR metadata gate" step
  (advisory); new "Run documentation conformance gate" step
  (advisory); new "Run admission gate" step (advisory).
- `tests/test_check_process_semantics.py`:
  - New `test_bp_sem_014_detects_cycle`: confirms BP-SEM-014
    fires on a 2-record cycle.
  - New `test_bp_sem_014_rejects_self_specialization`: confirms
    BP-SEM-014 fires on self-specialization.
  - Parametrized rule-coverage test extended for BP-SEM-014.
- `tests/test_cr_bp16_gates.py` (new, 11 tests): CR metadata,
  documentation conformance, and admission gate tests.

BP-SEM live verdict: 0 errors, 0 warnings: CONFORMANT
BP-AR live verdict: 0 findings: CONFORMANT
CR-META live verdict: 46 findings across 16 CR files (advisory;
legacy CRs lack S21 metadata)
DOC live verdict: 436 findings across many docs files (advisory;
docs cleanup is a separate programme item)
ADM live verdict: 54 findings across 18 Process records (advisory;
boundary + provenance fields are recommended, not required)
Conformance Levels: 38/38 at Level 4

**CR-BP-16 §29 acceptance criteria update:**
- [x] CI executes structural validation (was already PASS in PR-31)
- [x] CI executes semantic validation (BP-SEM; PR-29 + PR-36)
- [x] CI validates specialization graphs (BP-SEM-013 + BP-SEM-014;
  PR-37 + this PR)
- [x] CI validates references (BP-SEM-008; PR-31)
- [x] Architectural regression patterns are detected (BP-AR-001..007;
  PR-38)
- [x] CI validates CR metadata (CR-META-001..006; this PR)
- [x] Conformance results reproducible (--check modes; PR-38)
- [x] Canonical status tied to conformance + governance (Level 4;
  PR-38)
- [x] Gate does not equate ECF coverage with process completeness
  (BP-SEM-008; PR-31)
- [partial] CI validates provenance (gate machinery live; full
  change_history schema validation is a separate item)
- [partial] New-process admission has mandatory conformance path
  (gate machinery live; mandatory enforcement requires CR-BP-13A
  to land first as the pilot)
- [partial] Documentation describes the gate (gate machinery live;
  docs walkthrough is a separate programme item)

### CR-BP-15-IMP Phase 7: Pre-admission readiness

The permanent CR-BP-16 conformance gate machinery is now live:
the seven architectural regression patterns (BP-AR-001..007)
and the per-record conformance report (CR-BP-16 S23/24 Levels
1-4) are both running in CI. The catalogue is **38/38 Level 4
(Canonically Conformant)**.

- `scripts/check_architectural_regression.py` (new): the seven
  architectural regression patterns from CR-BP-16 S21 are now a
  blocking CI gate. Each pattern forbids conflation of two
  semantic concepts:
  - BP-AR-001: Business Process != Process Kernel
  - BP-AR-002: ECF Coordinate != Business Process
  - BP-AR-003: Process Group != Business Function
  - BP-AR-004: Capability != Process
  - BP-AR-005: Audience != Context (also catches reintroduction
    of legacy `process_audience` scalar)
  - BP-AR-006: Intent != Classification (also scans
    specialization_pattern / specialization_basis)
  - BP-AR-007: Specialization != Decomposition (catches
    same-context `specializes` relationships)
  Supports `--strict`, `--json`, `--self-test` (5 of 7 patterns
  are unit-tested via fixtures; the Process Group / Capability
  patterns are field-level and don't surface in the canonical
  data structure).
- `scripts/build_conformance_report.py` (new): generates
  `reconciliation/conformance_report.yaml` from the live
  catalogue. Each record is assigned a Conformance Level:
  - Level 0: Unassessed
  - Level 1: Structurally Conformant (schema + references)
  - Level 2: Semantically Conformant (BP-SEM clean)
  - Level 3: Architecturally Conformant (BP-AR clean)
  - Level 4: Canonically Conformant (evidence + governance)
  Supports `--check` to assert the report is up to date.
- `reconciliation/conformance_report.yaml` (new, generated):
  38 records, all Level 4 (Canonically Conformant).
- `.github/workflows/ci.yml`: new "Run architectural regression
  gate" step (blocking); new "Refresh conformance report" step
  (advisory). CI now runs BP-AR + report refresh on every PR.
- `tests/test_architectural_regression.py` (new): 7 tests
  covering the self-test, live conformance, JSON shape,
  canonical-bad fixture rejection, and report invariants.

BP-SEM live verdict: 0 errors, 0 warnings: CONFORMANT
BP-AR live verdict: 0 findings: CONFORMANT
Conformance Levels: {0: 0, 1: 0, 2: 0, 3: 0, 4: 38}

**Pre-admission readiness:** the §24 admission freeze can now
be lifted as soon as CR-BP-13A / CR-BP-13B admission tranches
are ready, because the BP-AR-001..007 gate will catch
architectural regressions at PR time. Phase 7 closes the
readiness loop opened by Phase 1-6.

### CR-BP-15-IMP Phase 6: Specialization machinery (machinery-only)

The BP-SEM-013 specialization-relationship validation rule is now
live, but **zero `specializes` relationships are introduced** on
the canonical 18 records. Phase 6 is machinery-only.

- `scripts/check_process_semantics.py` (modified):
  - New rule **BP-SEM-013** validates `relationships[]` entries
    with `relationship_type: specializes`. A valid specializes
    relationship MUST: target a canonical Process entry; carry a
    `specialization_pattern` from the approved basis vocabulary
    or a non-empty `specialization_basis` field; resolve to an
    existing Process entry.
  - Module docstring updated to document BP-SEM-013 alongside
    BP-SEM-001..012.
  - Self-test extended: broken fixture carries an unresolved
    specializes target (must fail); fixed fixture carries a
    valid specializes with approved basis (must pass).
- `tests/test_check_process_semantics.py`:
  - New `test_bp_sem_013_rejects_unresolved_specializes_target`:
    confirms BP-SEM-013 fires on an unknown target.
  - New `test_bp_sem_013_accepts_valid_specializes`: confirms
    BP-SEM-013 passes on a valid canonical-fan-out.
  - Parametrized rule-coverage test extended for BP-SEM-013.
- `reconciliation/dispositions/register.yaml`: `phase6_status`
  section added; `specializations_introduced: 0`,
  `validation_mode: machinery-only`, `bp_sem_013_rule_added:
  true`, with rationale documented inline.

**Why no specializations introduced:** CR-BP-14 S23 semantics
distinguish specialization (cardinality fan-out under a
controlled pattern like `by-customer-segment`) from
decomposition (sequential work within a single context, using
`composes`). Every candidate pair examined in Phase 6 planning
- `customer-journey-design` + `customer-experience-design`
  (cd-d);
- `design-policies-and-controls` + `design-governance-system`
  (ge-d);
- `market-and-demand-conception` + `customer-strategy-conception`
  (cd-c);
- is sequential decomposition, not cardinality fan-out. The
  CR-BP-14 S24 admission freeze prevents new admission
  tranches that would introduce clean fan-out candidates
  (e.g., `manage-enterprise-customer` specializing
  `manage-customer-relationship` under `by-customer-segment`).

**Future work:** Phase 7 (or the first post-freeze admission
tranche) will exercise BP-SEM-013 against a real fan-out
candidate. The machinery is in place; the canonical evidence
  will arrive when admission resumes.

BP-SEM live verdict: **0 errors, 0 warnings: CONFORMANT**
(no live records have `specializes` relationships, so BP-SEM-013
has no input to flag).

### CR-BP-15-IMP Phase 5 fourth tranche (ge-op) + Phase 5 closure

The final two governance-existence operate records have been
reconciled to the CR-BP-14 canonical contract. The disposition
register is now LOCKED (18/18). **The CR-BP-15-IMP Phase 5 loop
is complete.**

- `entities/v1-alpha/dea:process-audit-policy-compliance/`
  (ge-op): legacy `support` intent -> canonical `govern`
  (audit-and-oversight is governance activity); audience-vs-context
  high-risk flag resolved by removing `process_audience`
  (canonical `context: [{ref: dea:pc-ge-op}]` replaces it);
  serves toward `ecf:governanceAndExistence.operate`.
- `entities/v1-alpha/dea:process-operate-governance-oversight/`
  (ge-op): legacy `management` intent -> canonical `operate`;
  same ge-op migration pattern.
- `contexts/v1-alpha/dea_pc-pr-op.yaml` -> `dea-pc-pr-op.yaml`
  (filename typo fixed; canonical id `dea:pc-pr-op` was always
  correct inside the file). Updated 4 documentation references
  (CR-BP-03C + CR-BP-12 + manage-customer-relationship.md +
  CHANGELOG). The BP-SEM-008 context-reference-integrity check
  now passes.
- `reconciliation/diffs/phase-5-ge-op.yaml` (new): per-tranche
  audit trail; 2 records touched; closure observations on the
  audience-vs-context resolution and the filename correction.
- `reconciliation/dispositions/register.yaml`: register_status
  -> LOCKED; register_lock_progress records all 10 tranches and
  18 locked records; 0 remaining.
- `.github/workflows/ci.yml`: Process Semantics gate promoted
  from advisory (`--strict || true`) to **blocking** (`--strict`).
  Any future regression on the canonical CR-BP-14 contract is
  caught at PR time.
- `tests/test_reconciliation_baseline.py`: legacy_findings_present
  test updated to reflect the all-locked state (0 remaining,
  not 2).
- `tests/test_apply_phase_5_tranche.py`: register_lock_progress
  test now asserts the LOCKED status of the disposition register
  and the 18-of-18 lock progress.
- `tests/test_check_process_semantics.py`: live --strict test
  updated to assert CONFORMANT (0 errors, 0 warnings) on the
  post-Phase-5 catalogue. Added `test_strict_mode_fails_on_
  legacy_fixture` to lock the strict-mode machinery against a
  synthetic legacy-bearing sandbox.

BP-SEM live verdict: **0 errors, 0 warnings: CONFORMANT**
for the first time since CR-BP-14 S21 was introduced.

### CR-BP-15-IMP Phase 5 third tranche (ge-b + ge-c + ge-d + ge-im)

Seven governance records have been reconciled to the CR-BP-14
canonical contract. The disposition register is now 16-of-18
locked.

- `entities/v1-alpha/dea:process-codify-charters-and-policies/`
  (ge-b): legacy `operational` intent -> canonical `operate`;
  ge-b context block; serves toward
  `ecf:governanceAndExistence.build`.
- `entities/v1-alpha/dea:process-establish-governance-bodies/`
  (ge-b): legacy `operational` intent -> canonical `operate`;
  same ge-b migration pattern.
- `entities/v1-alpha/dea:process-develop-governance-strategy/`
  (ge-c): legacy `management` intent -> canonical `develop`;
  ge-c block; serves toward `ecf:governanceAndExistence.conceive`.
- `entities/v1-alpha/dea:process-initiate-policy-and-charter/`
  (ge-c): legacy `management` intent -> canonical `manage`;
  same ge-c pattern; serves toward
  `ecf:governanceAndExistence.conceive`.
- `entities/v1-alpha/dea:process-design-governance-system/`
  (ge-d): legacy `management` intent -> canonical `develop`;
  ge-d block; serves toward `ecf:governanceAndExistence.design`.
- `entities/v1-alpha/dea:process-design-policies-and-controls/`
  (ge-d): legacy `management` intent -> canonical `develop`;
  same ge-d pattern.
- `entities/v1-alpha/dea:process-review-governance-effectiveness/`
  (ge-im): legacy `management` intent -> canonical `govern`
  (review-and-correction is governance activity per the
  disposition register rationale); ge-im block; serves toward
  `ecf:governanceAndExistence.improve`.
- `reconciliation/diffs/phase-5-ge-b-ge-c-ge-d-ge-im.yaml`
  (new): per-tranche audit trail; 7 records touched;
  cross-tranche observations on ge-c intent diversity,
  ge-d as L2 conceptual foundation, ge-im as single-record
  Improve context work.
- `reconciliation/dispositions/register.yaml`: register_lock
  progress updated to 16 locked records (cd-b, cd-c, cd-d,
  cd-im, cd-op, ge-b, ge-c, ge-d, ge-im) and 2 remaining
  (the ge-op records; PR-9 next).
- `tests/test_reconciliation_baseline.py`: legacy_findings_present
  test updated to reflect the third tranche lock (2 remaining,
  not 9).
- `tests/test_apply_phase_5_tranche.py`: register_lock_progress
  test expanded to cover the four governance tranches.

BP-SEM live verdict: 2 errors (down from 9). Only the two
ge-op records remain.

### CR-BP-15-IMP Phase 5 second tranche (cd-d + cd-im + cd-op)

Five additional party-relationship records have been reconciled to
the CR-BP-14 canonical contract. The disposition register is now
9-of-18 locked.

- `entities/v1-alpha/dea:process-customer-experience-design/`:
  legacy `management` intent -> canonical `develop`; cd-d context
  block; serves toward `ecf:customerAndDemand.design`.
- `entities/v1-alpha/dea:process-customer-journey-design/`:
  legacy `support` intent -> canonical `develop`; same cd-d
  migration pattern.
- `entities/v1-alpha/dea:process-demand-design/`: legacy
  `management` intent -> canonical `develop`; same cd-d
  pattern.
- `entities/v1-alpha/dea:process-customer-insight-and-retention/`:
  legacy `management` intent -> canonical `operate` (Improve
  context work is operational); cd-im block; serves toward
  `ecf:customerAndDemand.improve`.
- `entities/v1-alpha/dea:process-manage-customer-relationship/`:
  legacy `management` intent -> canonical `manage`; cd-op block;
  serves toward `ecf:customerAndDemand.operate`. The existing
  `realizes` capability relationship is preserved.
- `reconciliation/diffs/phase-5-cd-d-cd-im-cd-op.yaml` (new):
  per-tranche audit trail; 5 records touched; cross-tranche
  observations on cd-d density and the management-vs-manage
  intent disambiguation.
- `reconciliation/dispositions/register.yaml`: register_lock
  progress updated to 9 locked records (cd-b, cd-c, cd-d,
  cd-im, cd-op) and 9 remaining.
- `tests/test_reconciliation_baseline.py`: legacy_findings_present
  test updated to reflect the second tranche lock (9 remaining,
  not 14).

BP-SEM live verdict: 9 errors (down from 14). Half of the
party-relationship records now conform to the canonical contract.

### CR-BP-15-IMP Phase 5 first tranche (cd-b + cd-c)

The first two party-relationship tranches (4 records: 2 build + 2
conceive) have been reconciled to the CR-BP-14 canonical contract.
The disposition register is now PARTIALLY_LOCKED with 4 records
locked.

- `entities/v1-alpha/dea:process-customer-channel-and-acquisition-build/`:
  legacy `operational` intent -> canonical `operate`; legacy
  scalar `process_context: dea:pc-pr-b` -> canonical
  `context: [{ref: dea:pc-pr-b}]` block; legacy
  `process_audience: party-relationship` removed; canonical `serves`
  relationship toward `ecf:customerAndDemand.build` added;
  change_history entry appended.
- `entities/v1-alpha/dea:process-demand-generation-build/`: same
  migration as the cd-b peer (operate + dea:pc-pr-b + serves).
- `entities/v1-alpha/dea:process-customer-strategy-conception/`:
  legacy `management` intent -> canonical `develop`; cd-c
  context; serves toward `ecf:customerAndDemand.conceive`.
- `entities/v1-alpha/dea:process-market-and-demand-conception/`:
  same migration as the cd-c peer.
- `reconciliation/diffs/phase-5-cd-b-cd-c.yaml` (new): per-tranche
  audit trail; 4 records touched; SHA-256 evolution recorded;
  cross-tranche observations.
- `reconciliation/dispositions/register.yaml`: register_status
  -> PARTIALLY_LOCKED; register_lock_progress records 4 locked
  records and 14 remaining.
- `schemas/entity.schema.json`: `process_audience` removed from
  the `required` list; the legacy field remains readable as a
  backward-compat alias (CR-BP-14 /19) but is no longer
  required for canonical entries.
- `scripts/apply_phase_5_tranche.py` (new): reproducible tranche
  migration script; supports `--self-test` (idempotence contract)
  and `--tranche <id>` for any of the 10 tranches; applies the
  full migration pattern (intent, audience removal, context
  block, serves relationship, change_history append).
- `tests/test_apply_phase_5_tranche.py` (new): 8 tests covering
  the migration script + per-record shape + idempotence + lock
  progress.
- `tests/test_reconciliation_baseline.py`: legacy_findings_present
  test updated to reflect the Phase 5 first-tranche lock (14
  remaining, not 18).

Programme position: CR-BP-14 still **Implemented**; CR-BP-15 +
CR-BP-15-IMP still **Proposed**; this PR is the fourth
CR-BP-15-IMP delivery and the first Phase 5 tranche migration.

BP-SEM live verdict: 14 errors (down from 18). The 4 migrated
records no longer trigger BP-SEM-007 (canonical context: block
required).

### CR-BP-15-IMP Phase 3-4: Disposition register + tranche plan

CR-BP-15 §28 (the ten dispositions) is now formalised; the 18
Business Processes in the canonical catalogue each receive a
preliminary RECLASSIFY disposition. The 18 records are grouped
into 10 tranches (one per Process Context) so future CR-BP-15-IMP
Phases 5-7 migrations are sequenced.

- `reconciliation/dispositions/schema.yaml` (new): the canonical
  disposition schema; 9 dispositions (RETAIN, RECLASSIFY, RENAME,
  SPECIALIZE, MERGE, SPLIT, MOVE, DEFER, RETIRE) each with
  required/optional fields, target_id requirement, and a
  rationale pattern; the reclassify_axes block documents the
  CR-BP-14 §17 migration mapping.
- `reconciliation/dispositions/register.yaml` (new, PRELIMINARY):
  18 disposition entries (one per Business Process); every
  entry is RECLASSIFY at this stage because every record carries
  the documented legacy fields; rationale + evidence recorded
  per entry; the register will be LOCKED in CR-BP-15-IMP
  Phase 5 (PR-6 onward).
- `reconciliation/tranches/plan.yaml` (new): 10 tranches (cd-b,
  cd-c, cd-d, cd-im, cd-op, ge-b, ge-c, ge-d, ge-im, ge-op); two
  are flagged high-risk (ge-b: audience-vs-context; ge-op:
  cross-tranche references); per-tranche PR target, owner
  placeholder, and review checkpoints recorded.
- `reconciliation/README.md`: orientation block extended to
  describe Phases 3-4 layout and Phase 5-7 roadmap.
- `scripts/check_dispositions.py` (new): disposition validator
  with --self-test; checks that every record has exactly one
  disposition entry, that every disposition id is canonical,
  that RECLASSIFY changes conform to the CR-BP-14 axes and
  vocabularies, that context targets resolve to the Process
  Context register, and that the tranche plan covers every
  disposition entry.
- `tests/test_dispositions.py` (new): 9 tests covering the
  disposition validator + register + tranche plan.
- `.github/workflows/ci.yml`: Disposition register step added
  (advisory until the register is LOCKED).

Programme position: CR-BP-14 still **Implemented**; CR-BP-15 +
CR-BP-15-IMP still **Proposed**; this PR is the third
CR-BP-15-IMP delivery.

### CR-BP-15-IMP Phase 1-2: Inventory + immutable baseline

CR-BP-15 §6 / §7 (existing-population reconciliation) is now
seeded. The Phase 1 inventory enumerates every canonical record at
the moment CR-BP-14 was declared Implemented; the Phase 2 baseline
freezes each record's SHA-256 so future tranches can diff exactly
which bytes were touched.

- `reconciliation/inventory.yaml` (new): 18 Business Processes +
  10 Process Groups + 10 Process Contexts + 4 Change Requests
  (CR-BP-14, CR-BP-15, CR-BP-15-IMP, CR-BP-16); per-record
  metadata + `legacy_findings` (BP-SEM raw findings on each
  record).
- `reconciliation/baseline/v1.yaml` (new): immutable SHA-256
  snapshot of every record's file contents; baseline_version = v1;
  baseline_commit = 816c63b (CR-BP-14 Implemented); baseline_at =
  2026-09-06.
- `reconciliation/README.md` (new): orientation for visitors;
  layout, phase progression, STRUCT conformance reference.
- `scripts/build_inventory.py` (new): reproducible generator;
  `--self-test --strict` asserts byte-identity with committed
  files; supports `--out` for diff scenarios.
- `scripts/check_struct.py` (new, decision D6): STRUCT conformance
  check that flags unknown top-level entries; intentionally
  permissive (the catalogue's contracts own schema integrity);
  wired into CI as an advisory step.
- `tests/test_reconciliation_baseline.py` (new): 9 tests covering
  inventory regeneration, baseline SHA-256 integrity, and STRUCT
  typo detection.
- `.github/workflows/ci.yml`: STRUCT conformance step added
  between Legacy Migration gate and Process Semantics gate.

Programme position: CR-BP-14 still **Implemented**; CR-BP-15 +
CR-BP-15-IMP still **Proposed**; this PR is the first CR-BP-15-IMP
delivery.

### CR-BP-14 Phase 4: Documentation reconciliation (Implemented)

CR-BP-14 §22 is now satisfied. The repository prose reflects the
CR-BP-14 semantic contract; legacy vocabulary references are
reconciled to the canonical forms or marked historical; no
superseded semantic contract remains presented as normative.

- `docs/architecture.md`: oriented (links to the semantic-contract
  and governance documents); L0/L1/L2 narratives rewritten to the
  CR-BP-14 §6 / §7 definitions; Process Group confirmed as catalog-
  owned, not a metamodel entity; See-also expanded.
- `docs/identity.md`: identity-independence clause added (CR-BP-14
  §15); BP-ARC-ID-004 cross-check note clarifies its distinction from
  BP-SEM-003/004; See-also expanded; broken `../../` link defect
  swept.
- `docs/classification.md`: front matter records the CR-BP-14 §10 /
  §11 formal separation; the canonical `classifications/process-intents.yaml`
  link is now correct (the pre-existing `../../classifications` link
  defect is swept); See-also expanded.
- `docs/relandscape.md`: See-also expanded with the semantic-
  contract document and the BP-SEM validator; CR-BP-14 §24
  admission-freeze reference added; broken `../../` link defect
  swept.
- `docs/context.md` (new): Process Context as canonical placement
  (CR-BP-14 §5, §13, §20); the canonical `context:` block;
  multiplicity rule; the Process Context register at
  `contexts/v1-alpha/`; relationship to BP-SEM-007 and BP-SEM-008.
- `docs/specialization.md` (new): specialization as semantic
  refinement (CR-BP-14 §12); approved specialization bases;
  specialization vs decomposition; canonical form; identity
  independence (BP-SEM-009).
- `README.md` §2 (Process Architecture): the four-axes table is
  replaced with the CR-BP-14 axes (Intent / Classification /
  Specialization / Context); the obsolete `Audience` axis is replaced
  by the canonical `context:` block; §8 No Breaking Changes explains
  the migration-period field aliasing.

Register close-out: **CR-BP-14 -> Implemented** (the constitutional
phase is complete; CR-BP-15-IMP owns the existing-population
migration; CR-BP-16 owns the permanent gate).

### CR-BP-14 Phase 3: BP-SEM-001..012 Process Semantics gate

- `scripts/check_process_semantics.py` (new): implements BP-SEM-001
  (Intent Vocabulary), BP-SEM-002 (Classification Vocabulary),
  BP-SEM-003/004 (Intent/Classification Independence by construction),
  BP-SEM-005 (Specialization Validity), BP-SEM-006 (Specialization
  Differentiation), BP-SEM-007 (Context Distinction), BP-SEM-008
  (Context Reference Integrity), BP-SEM-009 (Identity Independence by
  construction), BP-SEM-010 (Legacy Detection), BP-SEM-011
  (Classification Collision, advisory), BP-SEM-012 (Context
  Multiplicity, advisory). Each finding carries a deterministic
  `rule:<code>` prefix; warnings never block unless `--strict`.
- `--self-test` exercises every BP-SEM rule on a broken fixture and
  asserts the fixed fixture is blocking-free with the expected advisory
  findings.
- Wired into CI as an advisory step between the legacy migration gate
  and the process group gate (`--strict || true`): the current
  canonical population carries CR-BP-14 S24 admission-freeze findings
  (legacy process_intent, legacy scalar process_context, missing
  canonical `context:` block, legacy process_audience); the validator
  surfaces them and CR-BP-15-IMP Phases 8..10 reduces them.
- New `tests/test_check_process_semantics.py` (16 tests) locks the
  self-test, docstring coverage of every code, and the live/strict
  verdict contract.
- The live run finds: 18 entries missing the canonical `context:`
  block (BP-SEM-007); all 18 carry legacy `process_intent` or legacy
  `process_audience` (BP-SEM-010); all 18 carry the legacy scalar
  `process_context` (BP-SEM-010). These are exactly the seed findings
  already documented in the CR-BP-14/15/16 programme plan.

### CR-BP-14 Phase 2: Process Context block and contextual relationships

- `context:` block added to `schemas/entity.schema.json` and
  `schemas/contribution.schema.json` (CR-BP-14 §13, §20): an array of
  `{ref: dea:pc-*}` Process Context references; multiple contexts are
  permitted where evidence justifies them (BP-SEM-012).
- `relationship_type` enum extended with `serves` and `contributes-to`
  (both admitted by the metamodel relationship registry; catalog-governed
  extension, no metamodel CR required). `operates-within` is deliberately
  absent: its semantics are carried by the `context:` block.
- `target_id` now admits canonical ECF identifiers
  (`ecf:<lowerCamelDomain>[.<lowerCamelStage>]`, the CG-003 form)
  alongside entity ids; the entity-id branch excludes the `ecf:` prefix
  so the kebab-case label form is rejected (consistent with CG-004 §10).
- Contribution template updated: the canonical `context:` block replaces
  the pre-CR-BP-14 `process_context` scalar; a `serves` relationship
  example toward an ECF coordinate is included.
- New `tests/test_process_context_relationships.py` (16 tests) locks the
  block shape, enum extension, target patterns, and backward
  compatibility of all existing canonical entries.
- Recorded for CR-BP-15-IMP Phase 10: existing entries carry a legacy
  scalar `process_context` field that predates the canonical block; the
  schema remains permissive toward it until the audience/context
  migration.

### CR-BP-15 + CR-BP-16 landing and knowledge harvest

- CR-BP-15 (Process Catalog Reconciliation) and CR-BP-16 (Process
  Catalog Conformance Gate, carrying CR-BP-15-IMP) landed verbatim at
  `change-requests/CR-BP-15-process-catalog-reconciliation.md` and
  `change-requests/CR-BP-16-process-catalog-conformance-gate.md`.
- New visitor-facing documentation distilled from the CR lineage:
  `docs/semantic-contract.md` (the semantic constitution: six
  characterization dimensions, controlled vocabularies, the normative
  separations) and `docs/governance/reconciliation-programme.md` (the
  closed governance loop, CR lineage, reconciliation dispositions,
  conformance levels, repository status model).
- README gains a "Reading This Repository" orientation block.
- CR register + README change programme: CR-BP-15 and CR-BP-16 rows
  added as Proposed; CR-BP-14 row updated to reflect Phase 1 (PR #26).

### CR-BP-14: Process Semantic Reconciliation (landing + Phase 1)

Landing (PR #25):
- CR landed verbatim at
  `change-requests/CR-BP-14-process-semantic-reconciliation.md`.
- CR register synchronized with actual status (CR-BP-14 §23): CR-BP-13b
  corrected to Merged (PR #24); README change programme rows synced for
  CR-BP-03/03A/03C/04/11/12/13/13a/13b; stale Activity Model / Execution
  Boundary placeholders renumbered as unnumbered future rows.

Phase 1 (semantic vocabularies + schema; CR-BP-14 §9, §10, §11, §17, §18, §20):
- New controlled vocabulary `classifications/process-intents.yaml`: the
  seven-value purpose-oriented Process Intent vocabulary (govern / manage /
  operate / deliver / support / develop / transform) with the §17 legacy
  migration mapping (operational -> operate or deliver; support -> support;
  management -> manage or govern; evidence-based, never mechanical).
- `schemas/entity.schema.json`: `process_intent` enum extended to the
  canonical seven values with legacy `operational` / `management` retained
  as deprecated migration aliases; new optional `process_classification`
  block (canonical form per §20); `process_type` retained unchanged as the
  landscape classification and backward-compatible alias (§18);
  `process_audience` marked as legacy migration alias (§13, §19).
- `schemas/contribution.schema.json` mirrors the same extensions.
- `classifications/process-types.yaml` header records the CR-BP-14 §10
  Process Classification semantics and the Intent != Classification rule
  (§11; BP-SEM-011).
- `scripts/check_process_specialization.py` BP-SPEC-01-007 text updated to
  quote the extended intent vocabulary; non-promotion rule unchanged.
- `docs/classification.md` gains a CR-BP-14 Phase 1 status section; the
  pre-CR-BP-14 prose is marked historical pending Phase 4 reconciliation.
- Contribution template updated to the canonical intent vocabulary with the
  optional `process_classification` block shown.
- New `tests/test_process_intents.py` locks vocabulary / schema mirror
  integrity.

### CR-CATALOG-STRUCT-02: Process Catalog Adoption (Three-Step Migration)

Brings `dea-catalog-processes` into conformance with the catalog repository
standard (CR-CATALOG-STRUCT-01).

Step 1 (layout):
- `entities/v1-alpha/dea:process-manage-customer-relationship/{research,candidates,retired}/`
  subtree created; canonical file moved from `dea_bp_manage-customer-relationship.yaml`
  and renamed to canonical `dea:process-*` form (CR-BP-04).
- `entities/v1-alpha/dea:group-customer-lifecycle-management/{research,candidates,retired}/`
  subtree created; canonical file moved from `dea_group-customer-lifecycle-management.yaml`.

Step 2 (research distribution):
- `docs/research/l1-register.yaml`, `l1-candidate-universe.yaml`, `L1-REGISTER-v0.1.md`
  moved into `entities/v1-alpha/dea:group-customer-lifecycle-management/research/`
  (research is about L1 Process Groups; L1 entities own L1 evidence).
- `docs/research/` removed (empty after the move).
- Provenance `research/README.md` per subtree.

Step 3 (contribution flow):
- `contributions/processes/` intake queue and template kept as-is (catalog
  hosts one entity type; renaming is a future concern).

Catalog index + CI:
- `CATALOG.yaml` (machine-generated, 1.9 KB) committed.
- `TEMPLATE_VERSION` (`0.1.0`) written; matches the canonical template.
- `metamodel-pointer.yaml` extended with additive top-level metadata block
  (id/name/abbreviation/version/status/metamodel_version/description/owner);
  existing nested `metamodel:` and `catalog:` blocks unchanged.
- `scripts/regenerate_catalog.py`, `scripts/check_catalog_index.py`, and
  `catalog-index-schema/catalog-index-schema.json` vendored from
  `dea-metaframework/tools/` (CST-013/CST-014).
- `.github/workflows/ci.yml` updated to run the regenerator check, the
  gate, the per-file schema dispatch (with state-directory filter), the
  six existing catalog validators, and the cross-repo conformance suite.
- `scripts/check_ecf_conformance.py` fixed: skip files under
  `research/`, `candidates/`, `retired/` (state-directory files are not
  catalog entries and do not carry `ecfConformance`).

Verification:
- All 6 catalog validators PASS.
- Regenerator --check exits 0.
- Gate --strict exits 0.
- Conformance --strict: 16/16 CSTs passed, 0 warnings.
- Cross-repo contract satisfied; STRUCT-03..05 can adopt the same pattern.

### CR-BP-12: L1 Process Group Profile, Schema, and Validator

Lands the first-class Process Group record type. Process Group remains a catalog-owned record (NOT a metamodel entity). The canonical containment direction is `L1 group --composes--> L2 process`; the inverse `part-of` view is generated at query time per CR-002 §8 because the metamodel relationship-type enum does not currently admit `part-of`.

#### Added

- `schemas/entities/process-group.schema.json` — JSON Schema for Process Group entries. ID family: `dea:group-*` (CR-BP-04 §4).
- `classifications/process-group-kinds.yaml` — six-value controlled vocabulary (`end-to-end`, `functional`, `support`, `cross-cutting`, `governance`, `innovation`).
- `scripts/check_process_group.py` — validator enforcing PG-001..PG-008; includes `--self-test` mode.
- `entities/v1-alpha/dea_group-customer-lifecycle-management.yaml` — the first canonical Process Group record; promotes the `metadata.group` label that lived on `dea:process-manage-customer-relationship` into a governed first-class record with `process_group_kind: end-to-end`.
- New CI step in `.github/workflows/ci.yml` that runs `scripts/check_process_group.py` on every PR.

#### Changed

- `entities/v1-alpha/dea_bp_manage-customer-relationship.yaml` loses the `metadata.group` block; the Process Group is now an external first-class record referenced via the Process Group's `composes` array.

#### Not changed

- Existing Process Context (`dea:pc-pr-op`), classifications, contribution template, and contribution report workflow remain as PR #17 + #18 + #19 landed them.
- No Process Group promotion to the OpenDEA Core metamodel (CR-BP-14, future, conditional).
- Process Group kinds vocabulary is closed; additions require a CR-BP-12 minor revision.

### CR-BP-04: Business Process Identity & ID-Family Reconciliation

Documentation-first CR. Locks the four canonical ID families used by the
catalog (`dea:process-*`, `dea:pc-*`, `dea:group-*`, `dea:scope-*`) and the
legacy-migration `dea:bp:*` colon-separated family. Resolves the apparent
`dea:bp-*` versus `dea:process-*` drift by collapsing it to three intentional
roles: (1) legacy-migration reference inside `legacy_ids` arrays; (2) canonical
Business Process id on live entities and Process Context references;
(3) validator self-test fixture, used only to exercise failure paths inside
`scripts/check_legacy_migration.py` and `scripts/check_process_identity.py`.

#### Added

- `change-requests/CR-BP-04-id-family-reconciliation.md` (the CR; 13 sections;
  Design Specification tone; no en/em dashes; locks the colon-vs-dash
  distinction for the legacy family).
- New section **Canonical ID families (CR-BP-04 §4)** in `docs/identity.md`,
  restating the four-family contract verbatim.

#### Not changed

- No schema change. `schemas/entity.schema.json`, `schemas/contribution.schema.json`,
  and `schemas/entities/process-context.schema.json` already conform to the
  rule this CR documents.
- No validator change. `check_process_identity.py`, `check_process_context.py`,
  `check_legacy_migration.py`, and `check_ecf_conformance.py` already enforce
  the rule this CR documents.
- No entity change. No live catalog content uses the `dea:bp-*` dash form as
  a canonical identifier.
- No migration script. The `dea:bp-bad-*`, `dea:bp-parent`, and `dea:bp-child-*`
  validator fixtures remain as synthetic broken-input examples.

### CR-BP-11: L1 Process Group Discovery Across the 49 ECF Coordinates

Research-only register. Establishes a comprehensive L1 Process Group
discovery across the 7x7 ECF matrix (49 coordinates). Records an explicit
disposition per coordinate: 38 `accepted`, 11 `deferred`. Five cross-domain
findings are recorded once at their primary coordinate and referenced from
peer coordinates (Technology Management held unmapped; Change Management
cross-cutting at governance-existence x improve; Partner Management
dual-home at party-relationship x conceive; Resilience/Innovation/Analytics
at their primary coordinates; Marketing distinct from Customer Management).

The register is the input gate for CR-BP-12 (L1 Process Group profile +
schema + validator) and CR-BP-13..BP-19 (seven-domain admission tranches).
No canonical L1 records, no new schema, no new validator, no new CI
surface are added in this CR. The existing canonical L2 entry
(`dea:process-manage-customer-relationship`) remains the only canonical
Process entity in the catalog.

Process Group remains a catalog-owned record type, not an OpenDEA Core
metamodel entity. The canonical containment direction is
`L1 group --composes--> L2 process`; the inverse `part-of` is a derived
query view. Process Group and Business Function are explicit distinct
catalog-topology constructs (not synonyms, not subtypes, not aliases).

#### Added

- `change-requests/CR-BP-11-l1-process-group-discovery.md` (the CR;
  19 sections; Design Specification tone; no en/em dashes).
- `docs/research/l1-register.yaml` (the 49-coordinate disposition
  register; machine-readable; each coordinate carries process_context,
  l1_candidates, l2_candidates, in_scope, out_of_scope, evidence,
  disposition, deferral_reason).
- `docs/research/l1-candidate-universe.yaml` (the L1 candidate
  universe; 102 candidates across 49 coordinates; five cross-domain
  findings).
- `docs/research/L1-REGISTER-v0.1.md` (persona-readable summary).

#### Not changed

- Existing canonical entries under `entities/v1-alpha/`, `contexts/v1-alpha/`,
  `contributions/processes/`, `docs/examples/`, `schemas/`, `scripts/`,
  `classifications/`, `.github/workflows/` remain as PR #17 landed them.
- No `dea:bp-*` versus `dea:process-*` ID-family reconciliation happens
  here; that is a separate CR-BP-04.

### CR-BP-03C: Sample Business Process Contribution (walk-the-flow)

Lands the **first** Business Process entry in the catalog,
walking the full CR-BP-03 / CR-BP-03A / CR-BP-02 flow
end-to-end. The sample entry — `dea:bp:manage-customer-relationship`
("Manage Customer Relationship") — exercises every part of
the machinery:

  - 4-axis classification (intent / type / specialization /
    audience), all populated.
  - Process Identity contract (verb + object + outcome +
    evidence; BP-ARC-ID-001..005 PASS).
  - Canonical relationships (array-of-relationship-instances
    per metamodel relationship-instance.json; one realizes
    relationship to `dea:entity-capability:manage-customer-relationship`).
  - L0/L1/L2 conceptual hierarchy (Scope and Group recorded
    in metadata; NOT promoted to separate catalog entities
    per CR-BP-03 §3).
  - Process Context reference (the entry belongs to the
    PartyAndRelationship × Operate cell at
    `dea:pc-pr-op`).
  - ECF Conformance Gate (inherits-catalog; canonical
    references resolve to `ecf:partyRelationship.operate`;
    extensions declare `doesNotRedefine: true`).
  - Process Identity validator: case-insensitive + doubled-
    parentheses-tolerant fuzzy match (`_fuzzy_name_match`).

#### Added

- `change-requests/CR-BP-03C-sample-process-contribution.md`
  (md5 `0504cbca05a1875aac02137c959b7cab`; byte-identical to
  working folder `/home/hermes/dea-work/process/00_inbox/`).
- `entities/v1-alpha/dea_bp_manage-customer-relationship.yaml`
  (the canonical BP entry; first entry in the catalog;
  id `dea:process-manage-customer-relationship`).
- `contexts/v1-alpha/dea-pc-pr-op.yaml` (the Cell Charter for
  PartyAndRelationship × Operate; first Cell Charter in the
  catalog).
- `contributions/processes/dea_bp_manage-customer-relationship.yaml`
  (the contribution record; first contribution in the catalog).
- `contributions/processes/dea_bp_manage-customer-relationship.report.md`
  (the generated reclassification report; status=PASS,
  zero recommendations).
- `docs/examples/README.md` (introduction to the worked-
  examples directory).
- `docs/examples/manage-customer-relationship.md` (the
  worked example; future contributors should treat this
  as the canonical pattern).

#### Changed

- `scripts/check_process_identity.py`:
  - `_fuzzy_name_match` extended to be case-insensitive
    (entry names are conventionally Title Case; identity
    sub-block is conventionally lowercase).
  - `_fuzzy_name_match` extended to normalize doubled
    parentheses (e.g. `((all customer segments))` produced
    by wrapping a scope like `(all customer segments)`).
  - BP-ARC-ID-001: when the scope is already parenthesized,
    the validator does not wrap it again.
- `.github/workflows/process-contribution-report.yml`:
  - Reclassification report generator upgraded (CR-BP-03C §7)
    to cross-check the proposed_entry against BP-ARC-ID-001..005
    and emit a confidence-scored recommendation.
  - Includes migration check (BP-MIG-001..005) in the report
    pipeline.

#### Validators exercised (all PASS)

| Validator | Result |
|---|---|
| `check_process_identity.py` (BP-ARC-ID-001..005) | PASS |
| `check_process_identity.py --self-test` | PASS |
| `check_process_specialization.py` (BP-SPEC-01-001..007) | PASS |
| `check_process_context.py` (PC-001..PC-008) | PASS |
| `check_legacy_migration.py` (BP-MIG-001..005) | PASS |
| `check_legacy_migration.py --self-test` | PASS |
| `check_ecf_conformance.py` | PASS (1 entry conforms) |
| `validate_consumer.py` against `dea-architecture-framework@v0.6.0` | PASS |
| `jsonschema.validate(canonical_entry, entity_schema)` | PASS |
| `jsonschema.validate(cell_charter, process-context_schema)` | PASS |
| `jsonschema.validate(contribution, contribution_schema)` | PASS |
| Report generator (CR-BP-03C §7) | Generated report with status=PASS, 0 recommendations |

### CR-BP-03A: Legacy Field Migration

Resolves three issues with the CR-BP-03 schema that came to
light during implementation:

1. **`relationships` shape corrected** to array-of-relationship-
   instances (per the metamodel's `relationship-instance.json`).
   The CR-BP-03 shape was a structured object with
   `composes` / `realizes` keys; the authoritative metamodel
   shape is a flat array of typed relationship instances with
   full CR-002 provenance, CR-6 lifecycle, and effective_from/to
   temporal validity.
2. **`parent_process` / `child_processes` REMOVED** from the
   catalog schema. These were catalog inventions from CR-BP-01
   (the wrong-premise implementation, since reverted); the
   metamodel's `process.json` does not declare them.
3. **`capabilities_delivered` soft-deprecated**. The metamodel
   still declares this as a simple array of strings (a
   backward-compat shim). CR-BP-03A keeps the field in the
   catalog schema but marks it as soft-deprecated; the canonical
   form is `relationships[relationship_type=realizes]` with
   full provenance.

#### Added

- `change-requests/CR-BP-03A-legacy-migration.md` (md5
  `3e4a951008bf28e0b7d3bd325bcc2949`; byte-identical to working
  folder `/home/hermes/dea-work/process/00_inbox/`).
- `scripts/check_legacy_migration.py` — the migration validator
  enforcing BP-MIG-001..005 (with built-in `--self-test`).

#### Changed

- `schemas/entity.schema.json`:
  - `relationships` shape corrected to array-of-relationship-
    instances; each entry has `source_id`, `target_id`,
    `relationship_type`, plus optional `direction`, `status`,
    `effective_from`/`to`, `asserted_by`, `rationale`, `evidence`,
    and `provenance`.
  - `parent_process` and `child_processes` REMOVED.
  - `capabilities_delivered` retained but documented as
    soft-deprecated; the canonical form is
    `relationships[relationship_type=realizes]`.
- `schemas/contribution.schema.json` — `proposed_entry.relationships`
  shape updated to match the metamodel relationship-instance
  shape (array of instances).
- `contributions/processes/PROCESS-CONTRIBUTION-TEMPLATE.yaml` —
  template updated with the relationship-instance shape.
- `docs/architecture.md` — "Structural composition" and
  "Capability realization" sections updated to reflect the
  metamodel-aligned shape; new "The `relationships` shape"
  and "Legacy field migration" sections added.
- `docs/relandscape.md` — "The `relationships` field" and
  "The legacy fields" subsections added.
- `.github/workflows/ci.yml` — adds the Legacy Migration gate
  step (after the Process Identity gate).
- `change-requests/README.md` — CR-BP-03A row added.

#### Architecture-only (no file changes)

- The catalog now aligns with the metamodel's relationship-
  instance shape. Each relationship carries full provenance,
  lifecycle, and temporal validity.
- The catalog's `entities/v1-alpha/` is empty by design
  (CR-BP-02 §22), so the migration validator is forward-looking
  on future entries.

### CR-BP-03: Business Process Architecture

Lands the **4-axis classification**, **process-identity contract**,
and **contribution-driven re-landscape** mechanism on top of
CR-MM-PROC-01 + CR-AR-FMWK-01 + CR-BP-SPEC-BP-01 + CR-BP-02.

**No breaking changes.** CR-BP-03 introduces new fields additively;
existing entries continue to validate. The L0/L1/L2 hierarchy is a
**conceptual model** (not separate top-level directories).

#### Added

- `change-requests/CR-BP-03-business-process-architecture.md`
  (md5 `85697440a09102165099e4f67650b635`; byte-identical to working
  folder `/home/hermes/dea-work/process/00_inbox/`).
- `classifications/process-types.yaml` — the 5-value Mintzberg
  vocabulary with primary organizational component + primary
  purpose for each.
- `classifications/process-specializations.yaml` — the
  catalog-level specialization pattern vocabulary
  (by-customer-segment / by-region / by-product-line / by-tier /
  by-compliance-regime) with worked examples.
- `schemas/identity.schema.json` — the process-identity sub-block
  schema (verb + object + scope + outcome_statement +
  evidence_links). Mirrored inline in
  `schemas/entity.schema.json` to avoid a remote `$ref`.
- `schemas/contribution.schema.json` — the process-contribution
  schema (the input shape for `contributions/processes/`).
- `contributions/processes/PROCESS-CONTRIBUTION-TEMPLATE.yaml` —
  the template contributors copy + fill in.
- `contributions/processes/README.md` — the contribution flow
  documentation.
- `scripts/check_process_identity.py` — process-identity validator
  enforcing BP-ARC-ID-001..005 (with built-in `--self-test`).
- `docs/architecture.md` — the L0/L1/L2 structural architecture
  narrative.
- `docs/classification.md` — the 4-axis classification narrative.
- `docs/identity.md` — the process-identity contract narrative.
- `docs/relandscape.md` — the contribution-driven re-landscape
  mechanism.
- `docs/conformance.md` — the conformance gates summary.
- `validation/conformance/README.md` — forward-looking alias for
  the catalog's conformance validation.
- `.github/workflows/process-contribution-report.yml` — CI
  workflow for contribution-driven re-landscape (PRs to
  `contributions/processes/`).

#### Changed

- `schemas/entity.schema.json` — adds the new fields
  additively:
    - `process_type` (5-value enum; default `core`).
    - `process_specialization` (list of parent process ids).
    - `specialization_pattern` (free-text pattern label).
    - `relationships.{composes, realizes}` (canonical OpenDEA
      form).
    - `identity` (inline sub-schema mirroring
      `schemas/identity.schema.json`).
  - The id pattern is loosened to allow two-colon ids
    (`dea:bp:...`); the existing one-colon pattern still matches.
  - All existing fields are preserved; the legacy
    `parent_process` / `child_processes` / `capabilities_delivered`
    are documented as preserved migration aliases.
- `.github/workflows/ci.yml` — adds the Process Identity gate
  step (after the Process Context gate).

#### Architecture-only (no file changes)

- The 4-axis classification (intent / type / specialization /
  audience) is documented in `docs/classification.md` and
  `README.md`. Existing fields (`process_intent`,
  `process_audience`) are preserved; new fields (`process_type`,
  `process_specialization`) are added alongside.
- The L0/L1/L2 hierarchy is conceptual, documented in
  `docs/architecture.md` and `README.md`. There are no separate
  top-level directories for L0 / L1 / L2 entries.
- The re-landscape mechanism is contribution-driven, not
  in-tree. A re-landscape suggestion is generated by the
  contribution report workflow and reviewed by a catalog
  maintainer; the catalog does not auto-rewrite.

### CR-BP-02: Establish Process Context

Lands the **Process Context register + Cell Charter schema** on top of
the kernel + specialization discipline established by CR-MM-PROC-01 +
CR-AR-FMWK-01 + CR-BP-SPEC-BP-01.

**Authority chain (CR-BP-02 depends on the kernel + specialization
tranche):**

- `1665209` — CR-MM-PROC-01 merged on `dea-metamodel` (kernel + specialization).
- `76463b2` — CR-AR-FMWK-01 merged on `dea-architecture-framework` (root model v0.5.0 → v0.6.0).
- `1e4b916` — CR-BP-SPEC-BP-01 merged on `dea-catalog-processes` (Business Process specialization).
- `cb1a410` — CI hotfix (validate-allocation pin v0.2.1 → v0.6.0).
- `v0.6.0` — OpenDEAM root model tag published.

#### Added

- `change-requests/CR-BP-02.md` (md5 `9a56f5b0fc351c23416c51d216d805ef`; byte-identical to working folder `/home/hermes/dea-work/process/00_inbox/CR-BP-02.md`; refined to depend on the kernel + specialization tranche and to re-anchor PC-007/008/AC-07 to the corrected canonical ids).
- `schemas/entities/process-context.schema.json` — the canonical Process Context + Cell Charter schema. References the authoritative ECF vocabulary (CR-ECF-003/004/005) without redefining it.
- `scripts/check_process_context.py` — Process Context validator enforcing PC-001..PC-008 (with built-in `--self-test`).
- `contexts/v1-alpha/README.md` — placeholder documenting that the 49-cell matrix is **empty by design** per CR-BP-02 §22.

#### Changed

- `.github/workflows/ci.yml` — adds the Process Context gate step (after the Business Process specialization gate).
- `README.md` — "Canonical Process Context" section updated to reference the new Process Context Register at `contexts/v1-alpha/`, the schema, and the validator; adds an explicit "Process Context ≠ Business Process" callout.
- `change-requests/README.md` — CR-BP-02 row added.

**Out of scope (gated on its merge):** CR-BP-03 (L0/L1 decomposition
semantics); CR-BP-04 (Activity); CR-BP-05 (Workflow/Task); CR-BP-06
(Business Process criteria); CR-BP-07 (cross-context relationships);
CR-BP-08 (MECE within contexts); CR-BP-09 (Process Discovery
execution); CR-BP-10 (49-cell matrix population).

### CR-BP-SPEC-BP-01: Business Process Specialization Catalog

Re-anchors the catalog on the **kernel + specializations** discipline for
the OpenDEA Process concept. Refines + supersedes the prior CR-BP-01
(which landed as PR #10 on the wrong premise that `dea:BusinessProcess`
is the sole canonical Process identity).

**Authority chain established by this CR (end-to-end):**

```
WSF (org)                                     wsf:Process (Tier-3 derived)
 └─ dea-metamodel (Core authority)              CR-MM-PROC-01; PR #163
     ├─ dea:Process            (abstract Core kernel)
     └─ dea:BusinessProcess    (Core specialization)
        └─ dea-architecture-framework (root model)   CR-AR-FMWK-01; PR #10 + tag v0.6.0
             ├─ dea:entity-process               (abstract kernel; class_alias PRC;
             │                                       discriminator process-kernel)
             └─ dea:entity-business-process      (specialization; class_alias BP;
                                                    specializes PRC)
                └─ dea-catalog-processes (this catalog)   CR-BP-SPEC-BP-01; this PR
```

**Tranche history:**

- `1665209` — CR-MM-PROC-01 merged on `dea-metamodel` (kernel + specialization).
- `76463b2` — CR-AR-FMWK-01 merged on `dea-architecture-framework` (root model v0.5.0 → v0.6.0; consumer-validator abstract-kernel branch; ADR-0006).
- `417114f` — Revert of `a34c7ff` (CR-BP-01 implementation) merged on `dea-catalog-processes`.
- `v0.6.0` — OpenDEAM root model tag published.

**Changes:**

#### Added

- `change-requests/CR-BP-SPEC-BP-01.md` (md5 `5f5aa30e7ebfe2f1c187c300d5136406`; byte-identical to working folder `/home/hermes/dea-work/process/00_inbox/`).
- `docs/governance/process-specialization.md` — the governance narrative for the kernel + specialization contract.
- `scripts/check_process_specialization.py` — new validator enforcing `BP-SPEC-01-001..007` (with built-in `--self-test`).

#### Changed

- `metamodel-pointer.yaml` — pointer now declares the dual contract:
  - Primary `metamodel:` block: `dea:BusinessProcess` (specialization; class_alias BP; layer L3; building_block L3-value-delivery).
  - `metamodel.entities:` list: `dea:entity-process` (kernel; class_alias PRC; discriminator process-kernel; no layer, no dimension).
  - `metamodel.version: v0.6.0` (advances from v0.2.1; the root model carries both ids as of v0.6.0).
- `schemas/entity.schema.json` — `title: "Business Process"` (was `"Process Catalog Entry"`); description now references the WSF / Process-kernel lineage (CR-MM-PROC-01; CR-AR-FMWK-01; CR-BP-SPEC-BP-01).
- `.github/workflows/ci.yml` — adds the Business Process specialization gate step.
- `README.md` — "Purpose" reframed as Business Process **specialization** catalog; governing principle updated to "One kernel. Many valid specializations. One canonical home per specialization."

#### Removed (from the reverted `a34c7ff`; re-anchored here under the corrected premise)

- `change-requests/CR-BP-01.md` — superseded by this CR (the original text remains archived in `/home/hermes/dea-work/process/00_inbox/CR-BP-01.md`).
- `docs/governance/canonical-identity-business-process.md` — replaced by `docs/governance/process-specialization.md`.
- `scripts/check_bp01_canonical.py` — replaced by `scripts/check_process_specialization.py` (extended to `BP-SPEC-01-001..007`; original BP-01-001/002/003 rules folded into the new ruleset).

**Sub-classifications (operational / support / management)** remain
**catalog-internal** via the `process_intent` field. They do not promote
to root-model entities (`dea:entity-operational-process`, etc.). The
validator's `BP-SPEC-01-007` rule enforces this.

**Out of scope (gated on its merge):** CR-BP-02 (Process Context register
+ Cell Charter schema).

## Superseded (do not proceed with these)

- `a34c7ff` (CR-BP-01; PR #10): wrong premise — promoted
  `dea:BusinessProcess` as the sole canonical Process identity. Reverted
  by PR #11 (commit `417114f`). The artifacts (governance doc, validator,
  CI wire) are **preserved** and re-anchored by this CR under the
  corrected kernel + specialization discipline.