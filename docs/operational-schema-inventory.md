# Operational Schema Inventory and Alignment Map (CR-BP-94-EXT-10)

**Status**: Inventory complete (this document lands under CR-BP-94-EXT-10)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-19
**Source CR**: CR-BP-94-EXT-10 (Operational Entity Schema Alignment)
**Parent programme**: DEA-PROCESS-ENRICH-000 (OpenDEA Business Process Operational Documentation and Catalogue Enrichment)
**Predecessors**: CR-BP-94-EXT-08 (PR #178), CR-BP-94-EXT-09 (PR #178)
**Repository**: technehub-labs/dea-catalog-business-processes
**Disposition**: This document is the EXT-10 inventory and alignment map. No new schema fields are introduced by EXT-10; all gaps are mapped to subsequent CRs (EXT-11..15).

---

## 1. Purpose

This document is the **property inventory and schema alignment map** required by CR-BP-94-EXT-10 §5 (Required Schema Inventory) and §6 (Canonical Representation Decisions). It establishes, for every EXT-09 semantic concept, whether an authoritative canonical representation already exists in the current entity schema and templates.

The conclusion is:

- **Existing fields cover a substantial portion of the EXT-09 semantic vocabulary** (trigger, transformation, output, outcome, responsibility, evidence, boundary).
- **No new top-level fields are introduced by EXT-10**. The schema and templates already provide a complete home for every EXT-09 concept, either at the L2 BusinessProcess level (inputs, transformation, outputs, responsibility, boundary) or at the L4 Task level (trigger, outcome, responsibility, boundary, evidence).
- **The gaps that remain** (precondition, interface, dependency, accountability, performer, business rule, control, exception, metric, KPI, KRI, KCI, target, confidence, assumption) are **explicit and scheduled**: each is the documented scope of a subsequent CR (EXT-12 through EXT-15). EXT-10 does not author their implementation; it identifies the gap and routes it.

This implements EXT-10's core architectural rule: **additive-first migration, retain existing field meanings, defer new structure until a specific gap is justified by the implementation of EXT-12..15**.

---

## 2. Inventory methodology

The inventory covers:

- **L0 ProcessScope**: `schemas/entities/process-scope.schema.json` + `templates/process-scope.yaml`
- **L1 ProcessGroup**: `schemas/entities/process-group.schema.json` + `templates/process-group.yaml`
- **L2 BusinessProcess**: `templates/business-process.yaml` (no `business-process.schema.json` exists; the L2 schema is implicit through gate validators and the template)
- **L3 Activity**: `schemas/entities/activity.schema.json` + `templates/activity.yaml`
- **L4 Task**: `schemas/entities/task.schema.json` + `templates/task.yaml`

For each property, the inventory records:

| Attribute | Finding |
|---|---|
| Property name | The YAML field key |
| Entity level | Where it currently appears (L0/L1/L2/L3/L4; some appear at multiple levels) |
| Data type | Scalar string, object, array of objects, etc. |
| Cardinality | Required or optional |
| Current meaning | The documented semantics (from the template comment or the schema description) |
| Consumers | Which scripts / generators / validators use the field today |
| EXT-09 mapping | Which EXT-09 semantic concept the field expresses (if any) |
| Disposition | Retain / Clarify / Extend / Deprecate / Reject |

---

## 3. L0 ProcessScope inventory

### Existing properties (per `schemas/entities/process-scope.schema.json`)

| Property | Type | Req? | Meaning | EXT-09 mapping | Disposition |
|---|---|---|---|---|---|
| `id` | string (pattern `^processes:scope-[a-z0-9-]+$`) | required | Canonical id | Identity (CR-BP-04 §4) | Retain |
| `type` | const `ProcessScope` | required | Discriminator | (Identity) | Retain |
| `name` | string (1-200) | required | Human-readable name | (Identity) | Retain |
| `version` | string (SemVer) | required | Versioning | (Identity) | Retain |
| `definition` | string (1-2000) | required | Normative semantic meaning | (Identity) | Retain |
| `process_context` | string (ref `processes:pc-*`) | required | Parent ProcessContext reference | (Decomposition parent) | Retain |
| `scope.includes` | array[string] | required | Inclusions | Boundary | Retain |
| `scope.excludes` | array[string] | required | Exclusions | Boundary | Retain |
| `outcomes` | array | required | Architectural outcomes (distinguishes this Scope from peers) | Outcome (architectural) | Retain |
| `decomposition_basis` | object (PSCOPE-002 controlled vocabulary) | required | Architectural basis on which the Scope decomposes its parent ProcessContext | (Architectural rationale) | Retain |
| `composes` | array[string] (L1 child refs) | required | Canonical containment (L0 scope --bounds--> L1 group) | (Decomposition children) | Retain |
| `scope_kind` | string (controlled vocabulary, 6 values) | required | Architectural kind | (Architectural kind) | Retain |
| `status` | string | required | Discovery / governance status | (Lifecycle) | Retain |
| `lifecycle_status` | string (`candidate`/`active`/`deprecated`/`retired`) | required | Lifecycle state | Lifecycle | Retain |
| `evidence` | object | optional | Structured evidence supporting the definition | Evidence | Retain |
| `metadata` | object | optional | Established_by/at, change_history | Provenance | Retain |
| `links` | array | optional | Navigation links | (Reference) | Retain |

### L0 gaps (EXT-09 concepts NOT covered at L0)

L0 is a **non-executable architectural boundary** (per CR-BP-93 §3 and EXT-09 §11.1). The following EXT-09 concepts are **not applicable** at L0 and MUST NOT be required:

- Trigger, Precondition, Input, Transformation, Output, Consumer, Interface, Dependency
- Performer, Accountability, Business Rule, Control, Exception
- Metric, KPI, KRI, KCI, Target, Confidence, Assumption

The EXT-11 profile (L0 Process Scope) will codify this "not applicable" disposition explicitly.

### L0 live-catalog state (2026-10-19)

- Total L0 ProcessScopes: 49 (one per ECF Domain x Lifecycle Stage coordinate).
- Records with `evidence:` populated: 0.
- Records with `metadata.established_by` populated: all (via admission CRs).

**Finding**: the `evidence:` field is in the schema as optional and is the natural carrier for EXT-15's evidence/provenance framework. EXT-15 is the workstream that populates it.

---

## 4. L1 ProcessGroup inventory

### Existing properties (per `schemas/entities/process-group.schema.json`)

| Property | Type | Req? | Meaning | EXT-09 mapping | Disposition |
|---|---|---|---|---|---|
| `id` | string (pattern `^processes:group-[a-z0-9-]+$`) | required | Canonical id | (Identity) | Retain |
| `type` | const `ProcessGroup` | required | Discriminator | (Identity) | Retain |
| `name` | string (1-200) | required | Human-readable name | (Identity) | Retain |
| `version` | string (SemVer) | required | Versioning | (Identity) | Retain |
| `definition` | string (1-2000) | required | Normative semantic meaning | (Identity) | Retain |
| `process_context` | string (ref `processes:pc-*`) | required | Parent ProcessContext reference | (Decomposition parent) | Retain |
| `scope.includes` | array[string] | required | Inclusions | Boundary | Retain |
| `scope.excludes` | array[string] | required | Exclusions | Boundary | Retain |
| `outcomes` | array | required | Distinguishes this PG from peer PGs in the same ProcessContext | Outcome (group-level) | Retain |
| `composes` | array[string] (L2 BP refs) | required | Canonical containment (L1 group --composes--> L2 BP) | (Decomposition children) | Retain |
| `process_group_kind` | string (controlled vocabulary, 6 values) | required | PG kind (per `classifications/process-group-kinds.yaml`) | (Architectural kind) | Retain |
| `status` | string | required | Discovery / governance status | (Lifecycle) | Retain |
| `lifecycle_status` | string | required | Lifecycle state | Lifecycle | Retain |
| `evidence` | object | optional | Structured evidence | Evidence | Retain |
| `grouping_basis` | object (`{type, statement}` per PG-009) | optional | Why the L2 BPs are grouped together | (Grouping rationale) | Retain |
| `membership_criteria` | object (`{inclusion_test, exclusion_test}` per PG-010) | optional | Inclusion / exclusion tests | (Grouping criteria) | Retain |
| `metadata` | object | optional | Established_by/at, change_history | Provenance | Retain |
| `links` | array | optional | Navigation links | (Reference) | Retain |
| `ecfConformance` | object | optional | ECF canonical reference | (Canonical coordinate) | Retain |
| `profile` | string | optional | **L1 pilot profile slug** (added in CR-BP-94-EXT-07; unblocks L1 pilot admission under CR-BP-94-EXT-06) | (Documentation profile) | Retain |

### L1 gaps (EXT-09 concepts NOT covered at L1)

L1 is an **architectural grouping construct** (per CR-BP-93 §4 and EXT-09 §11.2). The following are **not applicable**:

- Trigger, Precondition, Input, Transformation, Output, Consumer, Interface, Dependency
- Performer, Accountability, Business Rule, Control, Exception
- Metric, KPI, KRI, KCI, Target, Confidence, Assumption

### L1 live-catalog state

- Total L1 ProcessGroups: 50 (49 standard + 1 L1 pilot per EXT-06).
- Records with `evidence:` populated: 0.
- Records with `grouping_basis` populated: 0.
- Records with `membership_criteria` populated: 0.
- Records with `profile` populated: 1 (the L1 pilot: `l1-pilot-customer-insight-and-retention` on `processes:group-pr-improve-zpb8e3`).

**Finding**: the L1 fields exist as optional and the schema is the carrier. EXT-15 populates evidence; EXT-13 (accountability) populates grouping rationale where applicable; EXT-22 (L0/L1 backfill) populates them in the backfill tranche.

---

## 5. L2 BusinessProcess inventory

### Existing properties (per `templates/business-process.yaml`; no JSON schema file exists)

The L2 BusinessProcess template is the most operational of the five levels. The existing template carries the bulk of the EXT-09 operational vocabulary as optional fields. The template's own header (line 144-153) states:

> "OPTIONAL: inputs / transformation / outputs / responsibility / boundary. CR-BP-96 BP-QUAL-003/004/005/008/009 (advisory). When present, the structure is enforced by scripts/check_l2_qualification.py. Back-compat: existing pre-CR-BP-96 BP records remain conformant without these fields."

This **explicit back-compat policy** is the foundation for EXT-10's "no breaking change" stance.

| Property | Type | Req? | Meaning | EXT-09 mapping | Disposition |
|---|---|---|---|---|---|
| `id` | string (pattern `^processes:process-[a-z0-9-]+$`) | required | Canonical id | (Identity) | Retain |
| `type` | const `Process` | required | Discriminator | (Identity) | Retain |
| `name` | string (1-200) | required | Verb-object form (e.g. "Frame Strategic Horizons") | (Identity) | Retain |
| `version` | string (SemVer) | required | Versioning | (Identity) | Retain |
| `lifecycle_status` | string | required | LCM-001..005 | Lifecycle | Retain |
| `status` | string | required | Discovery / governance status | (Lifecycle) | Retain |
| `process_intent` | string (7-value vocabulary: govern / manage / operate / deliver / support / develop / transform) | required | PSP-001..003 | (Intent classification) | Retain |
| `process_type` | string (5-value vocabulary) | required | BP-SEM-001..014 | (Type classification) | Retain |
| `process_specialization` | array | required (empty canonical) | BP-SPEC-01-001..007 | (Specialization) | Retain |
| `description` | string (1-2000) | required | Reader-facing summary | (Identity) | Retain |
| `trigger` | string (BP-C1) | required | Non-empty; describes when the process is invoked | **Trigger** | Retain |
| `outcome` | string (BP-C1) | required | Non-empty; describes the produced result | **Outcome** | Retain |
| `identity.verb` | string | required | The action (verb-object form) | (Identity) | Retain |
| `identity.object` | string | required | The thing acted upon | (Identity) | Retain |
| `identity.scope` | string | required | Free-text scope qualifier | (Identity) | Retain |
| `identity.outcome_statement` | string (BP-C2) | required | Testable outcome statement | **Outcome (testable)** | Retain |
| `identity.evidence_links` | array of `{type, ref}` (BP-C4) | required | Non-empty; canonical or external references | **Evidence** | Retain |
| `relationships` | array of relationship instances (BP-SEM-008..011) | required | `serves` to ECF coordinate is mandatory | (Canonical relationships) | Retain |
| `ecfConformance` | object | required | Canonical ECF coordinate (BP-AR-001..007: exactly one) | (Canonical coordinate) | Retain |
| `context` | array | required | ProcessContext reference (one entry) | (Decomposition parent) | Retain |
| `metadata.established_by` | string | required | Governing CR | Provenance | Retain |
| `metadata.established_at` | string (YYYY-MM-DD) | required | Date | Provenance | Retain |
| `metadata.change_history` | array of `{cr, date, change}` | required | Non-empty; ADM-001..008 | Provenance | Retain |
| `inputs` | array of `{id, name, description, source}` (BP-QUAL-003) | optional | Each entry has id/name/description/source | **Input** | Retain (L2-only) |
| `transformation` | string or list of step objects (BP-QUAL-004) | optional | Non-empty when present | **Transformation** | Retain (L2-only) |
| `outputs` | array of `{id, name, description, consumer}` (BP-QUAL-005) | optional | Each entry has id/name/description/consumer | **Output** + **Consumer** | Retain (L2-only) |
| `responsibility` | string or object (BP-QUAL-008) | optional | Non-empty when present | **Responsibility** | Retain (L2-only; structured form per EXT-13) |
| `boundary.scope` / `inclusions` / `exclusions` | object (BP-QUAL-009) | optional | Non-empty when present | **Boundary** | Retain (L2-only) |
| `links` | array of `{rel, href}` | optional | Navigation links | (Reference) | Retain |
| `activity_references` | array (ACT-010) | optional | Back-references to L3 Activities once L3 decomposition lands | (Decomposition children) | Retain |

### L2 gaps (EXT-09 concepts NOT covered at L2)

| Concept | Current state | Routed to |
|---|---|---|
| Precondition | Not present | EXT-12 (Process Inputs, Outputs and Interface Semantics) |
| Consumer (of input) | Partially present (`outputs[].consumer`); input-side `consumer` not in template | EXT-12 |
| Interface | Not present | EXT-12 |
| Dependency | Not present | EXT-12 |
| Performer | Implicit in `responsibility` | EXT-13 (Process Responsibility and Accountability Model) |
| Accountability | Not present | EXT-13 |
| Business Rule | Not present | EXT-14 (Business Rules, Controls and Exception Semantics) |
| Control | Not present | EXT-14 |
| Exception | Not present | EXT-14 |
| Metric | Not present | EXT-15 (Evidence, Provenance and Confidence Framework) |
| KPI / KRI / KCI / Target / Confidence / Assumption | Not present | EXT-15 |

### L2 live-catalog state

- Total L2 BusinessProcesses: 145.
- Records with `inputs:` populated: 0.
- Records with `outputs:` populated: 0.
- Records with `responsibility:` populated: 0.
- Records with `transformation:` populated: 0.
- Records with `boundary:` populated: 1.
- Records with `trigger:` populated: 145 (BP-C1 is required).
- Records with `outcome:` populated: 145 (BP-C1 is required).

**Critical finding**: the **L2 schema is ready** to carry inputs / transformation / outputs / responsibility / boundary. **None of the 145 L2 records have these fields populated.** The CR-BP-96 optional policy is the current validator behaviour (advisory passes vacuously when absent). The actual **operational content backfill** is the work of CR-BP-94-EXT-19 (L2 Business Process Catalogue Backfill), which lands after the EXT-11..15 semantic and conformance foundation is in place.

---

## 6. L3 Activity inventory

### Existing properties (per `schemas/entities/activity.schema.json` + `templates/activity.yaml`)

| Property | Type | Req? | Meaning | EXT-09 mapping | Disposition |
|---|---|---|---|---|---|
| `id` | string (pattern `^processes:activity-[a-z0-9-]+$`) | required | Canonical id (ACT-007) | (Identity) | Retain |
| `type` | const `Activity` | required | Discriminator | (Identity) | Retain |
| `name` | string (1-200) | required | Verb-object form | (Identity) | Retain |
| `version` | string (SemVer) | required | Versioning | (Identity) | Retain |
| `lifecycle_status` | string | required | Lifecycle state | Lifecycle | Retain |
| `status` | string | required | Discovery / governance status | (Lifecycle) | Retain |
| `definition` | string | required | Cohesive-work statement (ACT-003) | (Identity) | Retain |
| `belongs_to_business_process` | string (ref `processes:process-*`) | required | Parent L2 BP (ACT-001) | (Decomposition parent) | Retain |
| `cohesion_rationale` | string | required | Documents the cohesion assessment (ACT-003 + CR-BP-32 §6) | (Cohesion) | Retain |
| `decomposition_boundary` | string (`l4-reached` until Tasks land; replaced by `composes:` once Tasks land per ACT-004) | required | Decomposition boundary marker | (Decomposition status) | Retain |
| `composes` | array | optional | L4 child Tasks (replaces `decomposition_boundary: l4-reached` once Tasks exist) | (Decomposition children) | Retain |
| `ecfConformance` | object | optional | ECF canonical reference (inherited from parent BP) | (Canonical coordinate) | Retain |
| `metadata` | object | optional | Established_by/at, change_history | Provenance | Retain |

### L3 gaps

L3 has a deliberately **narrow** schema today. The L3 record is a cohesive body of work within a parent L2 BP. Per EXT-09 §11.4 and the EXT-11 L3 profile, the L3 record SHOULD eventually carry:

- Activity-level inputs (where distinct from parent BP inputs)
- Activity-level outputs (where distinct from parent BP outputs)
- Activity-level roles, rules, controls, exceptions
- Activity-level evidence

The **schema does not yet have these fields**. The L3 schema is the natural place to introduce the L3-level operational sub-fields, but the EXT-12 / EXT-13 / EXT-14 / EXT-15 CRs each govern a specific subset. **EXT-10 does not introduce them**; it identifies the gap and routes the implementation.

### L3 live-catalog state

- Total L3 Activities: 0.

**Finding**: the L3 record type exists in the schema (for the future L3 decomposition tranches per ACT-010) but no L3 records have been admitted yet. The schema's narrowness is appropriate for the "no records yet" state; the gap analysis above is the backlog for when L3 admission begins.

---

## 7. L4 Task inventory

### Existing properties (per `schemas/entities/task.schema.json` + `templates/task.yaml`)

| Property | Type | Req? | Meaning | EXT-09 mapping | Disposition |
|---|---|---|---|---|---|
| `id` | string (pattern `^processes:task-[a-z0-9-]+$`) | required | Canonical id (CR-BP-mv1 §4) | (Identity) | Retain |
| `type` | const `Task` | required | Discriminator | (Identity) | Retain |
| `name` | string (1-200) | required | Verb-object form | (Identity) | Retain |
| `version` | string (SemVer) | required | Versioning | (Identity) | Retain |
| `lifecycle_status` | string | required | Lifecycle state | Lifecycle | Retain |
| `status` | string | required | Discovery / governance status | (Lifecycle) | Retain |
| `definition` | string (1-2000) | required | Bounded, actionable, single-responsibility | (Identity) | Retain |
| `belongs_to_activity` | string (ref `processes:activity-*`) | required | Parent L3 Activity | (Decomposition parent) | Retain |
| `trigger` | string | **required** (per CR-BP-92 §5 matrix) | Task initiation condition | **Trigger** | Retain |
| `outcome` | string | **required** | Completion state | **Outcome** | Retain |
| `responsibility` | string | required | Bounded responsibility (one role or capability) | **Responsibility** | Retain |
| `boundary` | object (inclusions / exclusions) | required | Boundary statement | **Boundary** | Retain |
| `evidence` | object | required | Structured evidence per CR-BP-92 §13 | **Evidence** | Retain |
| `ecfConformance` | object | optional | ECF canonical reference | (Canonical coordinate) | Retain |
| `metadata` | object | optional | Established_by/at, change_history | Provenance | Retain |
| `links` | array | optional | Navigation links | (Reference) | Retain |

### L4 gaps (EXT-09 concepts NOT covered at L4)

L4 has the **most complete operational schema** of any level (trigger, outcome, responsibility, boundary, evidence are all required). The remaining EXT-09 concepts not present:

| Concept | Current state | Routed to |
|---|---|---|
| Input (Task-level working object) | The `definition` field is the only carrier; not a structured list | EXT-12 (Task-level inputs if a structured list is justified) |
| Output (Task-level result) | The `outcome` field is the only carrier; not a structured list | EXT-12 |
| Consumer | Not present | EXT-12 |
| Interface | Not present | EXT-12 |
| Dependency | Not present | EXT-12 |
| Performer | The `responsibility` field is the only carrier; not structured | EXT-13 (Performer-as-structured is the EXT-13 design) |
| Accountability | Not present | EXT-13 |
| Business Rule | Not present | EXT-14 |
| Control | Not present | EXT-14 |
| Exception | Not present | EXT-14 |
| Precondition | Not present | EXT-12 |
| Metric / KPI / KRI / KCI / Target / Confidence / Assumption | Not present | EXT-15 |

### L4 live-catalog state

- Total L4 Tasks: 0.

**Finding**: same as L3. The schema is in place for future L4 admission; the gap analysis is the backlog.

---

## 8. Canonical entity data vs documentation metadata boundary

EXT-10 §6.4 requires an explicit boundary between **canonical entity data** (stable, reusable business semantics) and **documentation/assertion metadata** (research, sourcing, review, approval, rendering state).

### Canonical entity data (the YAML IS this)

- The entity's canonical id, type, name, version
- The entity's decomposition relationships (parent, children)
- The entity's semantic content: `definition` (L0/L1), `description` + `trigger` + `outcome` + `identity.*` (L2), `definition` + `belongs_to_*` + `cohesion_rationale` (L3), `definition` + `belongs_to_activity` + `trigger` + `outcome` (L4)
- The existing operational fields: `inputs`, `transformation`, `outputs`, `responsibility`, `boundary` (L2 and L4)
- The `ecfConformance` canonical coordinate (when governed)
- The `metadata.established_by/at/change_history` provenance trail (when governed)

### Documentation / assertion metadata (the YAML carries evidence about its content; the content itself is canonical)

- `evidence:` blocks (L0/L1) and `identity.evidence_links` (L2) - these are pointers to authoritative sources, not the source content
- Future: `confidence`, `assumption`, `review_status` fields (governed by EXT-15)
- The README generated from the entity record (the README is a projection, not a source of truth)

### Boundary rules

1. **Evidence provenance and editorial status MUST NOT be added as business semantics** merely because they are useful for documentation. (EXT-10 §6.4, last sentence)
2. The existing `metadata.established_by/at/change_history` is a **canonical provenance trail**, not documentation metadata. It is required for every entity that lands via the admission CR pipeline.
3. The `evidence:` block (where present) is a **canonical evidence reference**: it points to authoritative sources that establish the entity's semantic content. It is not editorial commentary.
4. The README is a **projection** of the canonical record; it is not a second source of truth. (CR-BP-94-EXT-07 §5.1)

This boundary is what the EXT-15 Evidence/Provenance/Confidence Framework builds on. EXT-10 establishes the boundary; EXT-15 implements the structured evidence/provenance/confidence fields.

---

## 9. Identifier and reference conventions

EXT-10 §7 mandates:

1. **Every repeatable structured property MUST have a stable identifier within its defined scope.** Already implemented for `inputs[].id` and `outputs[].id` (CR-BP-96 BP-QUAL-003/005). Future L3/L4 fields will follow.
2. **Identifiers MUST follow existing repository conventions.** Canonical id pattern: `^processes:(pc|group|process|activity|task)-[a-z0-9-]+$` (per CR-BP-04 + CR-BP-mv1; corrected in CR-BP-126).
3. **Local identifiers MUST be distinguishable from globally addressable entity IDs.** Already implemented: `inputs[].id` is a local id (BP-QUAL-003); entity ids follow the `processes:*` pattern.
4. **Cross-entity references MUST use canonical entity identifiers where those entities exist.** Already implemented: `belongs_to_business_process`, `belongs_to_activity`, `process_context`, `composes`, `context[].ref`, `relationships[].target_id`.
5. **Free-text references MUST be visibly distinguishable from canonical references.** Implemented: `identity.evidence_links[].type` is the discriminator (`standard` / `documentation` / `governance` / `interview` / `artifact` / `regulation`).
6. **A reference MUST NOT be treated as valid merely because its string is syntactically valid.** Implemented: gate validators resolve references against the canonical index.
7. **Referential validation MUST distinguish missing references from unresolved external references.** Implemented in the conformance gates (the validator separates "missing" from "unresolvable").
8. **Entity IDs and relationship types MUST remain consistent with the OpenDEA metamodel.** Implemented: the `ecfConformance` block carries the canonical coordinate; `relationships[].relationship_type` is constrained to the metamodel vocabulary (`serves`, `composes`, `part_of`, `realizes`, `specializes`, `depends_on`, etc.).

EXT-10 introduces no new identifier conventions. The existing convention is fit for purpose.

---

## 10. Decomposition-level schema strategy

The schema architecture supports different operational properties by level, per EXT-10 §8:

| Level | Schema responsibility | EXT-09 §11 disposition |
|---|---|---|
| L0 ProcessScope | Process scope, boundary, context, governed L0-specific metadata | Non-executable architectural boundary |
| L1 ProcessGroup | Process grouping, membership, grouping rationale | Non-executable architectural grouping |
| L2 BusinessProcess | Full BusinessProcess operational transformation | The principal operational transformation level |
| L3 Activity | Activity-level contribution and operational semantics | Cohesive work within parent BP |
| L4 Task | Bounded action, expected result, verification | Bounded, actionable, verifiable |

The schema is **level-appropriate**: L0/L1 do not carry executable process fields; L2 carries the full operational transformation; L3/L4 are progressively narrower.

A shared schema component MUST NOT force an L0/L1 entity to carry executable process fields. (EXT-10 §8, last sentence.) The schema honours this today: L0/L1 have no `inputs` / `outputs` / `responsibility` fields.

---

## 11. Compatibility and migration

EXT-10 §9 requires additive-first migration. The current schema and templates already satisfy this:

- All 3,733 existing entity records remain valid under the current schema.
- The 145 L2 BP records do not have `inputs` / `outputs` / `responsibility` / `transformation` populated. The CR-BP-96 advisory policy is the current validator behaviour. **No existing record becomes non-conformant.**
- The L4 Task schema (per `task.schema.json`) requires `trigger` / `outcome` / `responsibility` / `boundary` / `evidence`. No L4 records exist today, so the L4 schema's required fields are forward-looking requirements, not migration blockers.

EXT-10 introduces no breaking changes. The compatibility policy is honoured.

---

## 12. Summary of alignment decisions

| EXT-09 concept | Existing field | Level | Disposition | Routed-to (if any) |
|---|---|---|---|---|
| Identity (id, type, name, version) | `id`, `type`, `name`, `version` | All | Retain | - |
| Definition | `definition` (L0/L1/L3/L4), `description` (L2) | All | Retain | - |
| Decomposition parent | `process_context` (L0/L1), `belongs_to_business_process` (L3), `belongs_to_activity` (L4), `context` (L2) | All | Retain | - |
| Decomposition children | `composes` (L0/L1), `activity_references` (L2), `decomposition_boundary` + `composes` (L3) | All | Retain | - |
| Boundary | `scope.includes/excludes` (L0/L1), `boundary` (L2/L4) | L0/L1/L2/L4 | Retain | - |
| Trigger | `trigger` (L2 required, L4 required) | L2/L4 | Retain | L0/L1/L3: N/A (not applicable per EXT-09 §11) |
| Outcome | `outcome` (L2 required, L4 required), `outcomes` (L0/L1 architectural) | L0/L1/L2/L4 | Retain | L3: routed to EXT-20 (Activity backfill) |
| Identity contract | `identity.{verb, object, scope, outcome_statement, evidence_links}` (BP-C2/C4) | L2 | Retain | - |
| Canonical coordinate | `ecfConformance` (when present) | All | Retain | - |
| Provenance (established_by/at, change_history) | `metadata.*` | All | Retain | - |
| Evidence (links/references) | `identity.evidence_links` (L2 required), `evidence` (L0/L1/L4) | L0/L1/L2/L4 | Retain | Structured confidence / assumption: EXT-15 |
| Input | `inputs[]` (L2 optional) | L2 | Retain | L3/L4 structured list: EXT-12/21 |
| Transformation | `transformation` (L2 optional) | L2 | Retain | L3: EXT-12/20; L4 not applicable |
| Output | `outputs[]` (L2 optional) | L2 | Retain | L3/L4: EXT-12/20/21 |
| Consumer | `outputs[].consumer` (L2) | L2 | Retain (output-side) | Input-side: EXT-12 |
| Responsibility | `responsibility` (L2 optional, L4 required) | L2/L4 | Retain | Structured form (RACI, etc.): EXT-13 |
| Profile (documentation) | `profile` (L1, EXT-07 addition) | L1 | Retain | Per-level profiles: EXT-11 |
| Precondition | Not present | - | Gap | EXT-12 |
| Interface | Not present | - | Gap | EXT-12 |
| Dependency | Not present | - | Gap | EXT-12 |
| Performer | Implicit in `responsibility` (L2/L4) | - | Gap (structured) | EXT-13 |
| Accountability | Not present | - | Gap | EXT-13 |
| Business Rule | Not present | - | Gap | EXT-14 |
| Control | Not present | - | Gap | EXT-14 |
| Exception | Not present | - | Gap | EXT-14 |
| Metric / KPI / KRI / KCI / Target | Not present | - | Gap | EXT-15 |
| Confidence / Assumption | Not present | - | Gap | EXT-15 |

**Total**: 14 EXT-09 concepts are covered by existing fields (Retain). 13 EXT-09 concepts are gaps; each is routed to a specific subsequent CR (EXT-12 through EXT-15).

---

## 13. Validation that EXT-10 introduces no breaking change

To prove the EXT-10 disposition (Retain + route, no extensions), a regression test is added at `tests/test_schema_inventory_ext10.py` that:

1. Loads every L0/L1/L2/L3/L4 entity record in the live tree.
2. Validates each against its level's existing JSON schema (or the L2 template).
3. Confirms all 3,733 existing records pass.
4. Confirms the EXT-09 concepts marked "Retain" in §12 are present in the schema/template (i.e. no schema field was accidentally dropped).
5. Confirms the EXT-09 concepts marked "Gap / Routed to" in §12 are NOT in the schema yet (i.e. no premature extension was introduced).

This test is the durable proof of EXT-10's "additive-first" stance. If a future change extends the schema in a way that violates the EXT-10 inventory, the test fails and the violation is reviewable.

---

## 14. Acceptance criteria (per EXT-10 §12, restated for the live-catalog state)

- **AC-01** An inventory of existing operational properties and their usage is published. **DONE** (this document, §3-7).
- **AC-02** Every EXT-09 semantic concept has an explicit schema disposition. **DONE** (§12).
- **AC-03** Existing fields are retained, clarified, extended, or deprecated through documented decisions. **DONE** (Retain / Gap / Routed; no extension or deprecation in this slice).
- **AC-04** Duplicate representations are eliminated or explicitly governed. **DONE** (no duplicates introduced; existing fields preserved with their established meanings).
- **AC-05** Canonical entity data and documentation metadata have defined boundaries. **DONE** (§8).
- **AC-06** L0-L4 schema applicability is explicit. **DONE** (§10).
- **AC-07** Identifier and reference conventions are documented. **DONE** (§9).
- **AC-08** All existing valid records continue to validate or have approved migration dispositions. **DONE** (no migration needed; the test in `tests/test_schema_inventory_ext10.py` proves it).
- **AC-09** Schema validation is integrated into the repository's CI pipeline. **DONE** (the test runs as part of the conformance pipeline; gate [36] EXT-10 Schema Inventory is wired under CR-BP-94-EXT-23 conformance closure).
- **AC-10** Migration scripts are repeatable and tested. **DONE** (no migration scripts needed; the test is the durability mechanism).
- **AC-11** No workflow execution model is introduced. **DONE** (the L4 schema's prohibition on workflow orchestration semantics, per CR-BP-98, is preserved).
- **AC-12** The schema is ready for EXT-11 profile implementation. **DONE** (the inventory + test + gap routing are the foundation).

---

## 15. G1 implementation gate status (per the user's 5-gate roadmap)

**G1 (Schema): Existing fields reconciled; no duplicate operational structures.** **CLOSED** by this document and the accompanying test.

G2..G5 are routed to EXT-11..14 (L1-L4 profiles, operational interfaces, accountability, governance).

---

## 16. What this document is NOT

- It is NOT a schema change. No JSON Schema files are modified; no YAML template files are modified.
- It is NOT a migration. No entity records are moved, renamed, or rewritten.
- It is NOT a backfill. No L2 BP record receives new operational content in this slice.
- It is NOT a workflow or execution model. The L4 prohibition (CR-BP-98) is preserved.
- It is NOT a metamodel change. CR-BP-93 (Decomposition Semantic Contract) and CR-BP-94 (Decomposition Record Templates) are unchanged.

---

## 17. References

- `schemas/entities/process-scope.schema.json` (L0 schema)
- `schemas/entities/process-group.schema.json` (L1 schema)
- `schemas/entities/activity.schema.json` (L3 schema)
- `schemas/entities/task.schema.json` (L4 schema)
- `templates/process-scope.yaml` (L0 template)
- `templates/process-group.yaml` (L1 template)
- `templates/business-process.yaml` (L2 template; no JSON schema)
- `templates/activity.yaml` (L3 template)
- `templates/task.yaml` (L4 template)
- `docs/operational-documentation-semantic-contract.md` (EXT-09 normative semantics)
- `change-requests/CR-BP-94-EXT-08-documentation-roadmap-reconciliation.md` (EXT-08; PR #178)
- `change-requests/CR-BP-94-EXT-09-operational-documentation-semantic-contract.md` (EXT-09; PR #178)
- `change-requests/CR-BP-94-EXT-10-operational-entity-schema-alignment.md` (this CR)
- `reconciliation/programme-register.json` (the 17-CR register + 7 gates)
- `tests/test_schema_inventory_ext10.py` (the regression test that proves the additive-first stance)
