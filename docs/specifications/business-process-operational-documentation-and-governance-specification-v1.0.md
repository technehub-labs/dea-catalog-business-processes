# Business Process Operational Documentation and Governance Specification v1.0

**Specification ID**: BP-DS-Spec-v1.0
**Version**: 1.0.0
**Status**: Proposed for adoption (consolidation of CR-BP-94-EXT-08 through CR-BP-94-EXT-24)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-20
**Repository**: technehub-labs/dea-catalog-business-processes
**Source programme**: DEA-PROCESS-ENRICH-000 (the 17-CR operational documentation and enrichment programme)
**Source baseline**: `reconciliation/closure/catalogue-baseline.json` (revision 9275f77d)

---

## 0. Purpose

This specification is the **single coherent architectural and operational reference** for the Business Process catalogue. It consolidates the 17 Change Requests of the DEA-PROCESS-ENRICH-000 programme into five integrated parts so that contributors, reviewers, owners and automation can reason about the catalogue without re-interpreting 17 separate documents.

The specification is **normative** for the parts marked `[NORMATIVE]`. Where a part is marked `[REFERENCE]`, the part points to the authoritative artefact and is not itself authoritative.

Every normative rule carries its source CR identifier (e.g. `CR-BP-94-EXT-11 REQ-22-04`). The full per-requirement traceability is in `reconciliation/conformance/requirement-traceability-matrix.json`.

---

## 1. Normative model [NORMATIVE]

The normative model defines the canonical decomposition, the entity semantics, the relationships and the decomposition profiles.

### 1.1 The L0-L4 decomposition

The catalogue decomposes business work into five levels:

| Level | Entity | Primary purpose | Non-executability |
|---|---|---|---|
| **L0** | Process Context | Establishes the overall scope and boundaries of a process domain or process landscape. | Non-executable. A Process Context is a scope, not a process. |
| **L1** | Process Group | Organises related Business Processes into meaningful groups. | Non-executable. A Process Group is a grouping, not a process. |
| **L2** | Business Process | Represents a complete business transformation or coherent business result-producing process. | Executable in a business-process sense. Not a workflow. |
| **L3** | Activity | Represents a cohesive body of work contributing to a Business Process. | Functional decomposition, not a workflow step. |
| **L4** | Task | Represents a bounded, independently understandable unit of work contributing to an Activity. | Non-orchestrating. A Task is a unit of work, not a workflow step. |

**Source**: `CR-BP-94-EXT-11 REQ-11-01..12`, `CR-BP-94-EXT-09 REQ-09-01..15`.

### 1.2 The decomposition is functional, not sequential

The hierarchy represents **progressively decomposed business responsibility and work**. It does not inherently represent execution order, workflow steps, branching logic, runtime orchestration, state transitions, scheduling, queue management or retry behaviour. (`CR-BP-94-EXT-09 REQ-09-12`, `CR-BP-94-EXT-12 REQ-12-01..12`.)

### 1.3 Canonical entity types

The catalogue recognises five canonical entity types, one per decomposition level. Each entity is a canonical YAML file with the schema defined in `schemas/entities/`:

- `process-context.schema.json` (L0)
- `process-group.schema.json` (L1)
- `process-scope.schema.json` (L1 process scope variant; **the L0 cell-charter variant uses the process-context schema and carries no `type` field**)
- `process.yaml` / `process-scope.schema.json` (L2)
- `activity.schema.json` (L3)
- `task.schema.json` (L4)

The L0 Process Context records use the **cell-charter schema**: they carry no `type` field, and their level is resolved from the canonical identifier prefix (`processes:pc-...`) per the EXT-05 convention. (`CR-BP-94-EXT-10 REQ-10-01..12`, `CR-BP-94-EXT-22 R22-08`.)

### 1.4 Parent-child relationships

The permitted parent-child relationships are:

| Parent | Permitted child |
|---|---|
| L0 Process Context | L1 Process Group |
| L1 Process Group | L2 Business Process |
| L2 Business Process | L3 Activity |
| L3 Activity | L4 Task |

Cross-cutting associations (a Task that supports multiple Activities, an Activity that references multiple Processes) are represented separately from decomposition parentage. They do not violate the model.

The framework detects:

- Invalid parent-child level combinations
- Missing parent references
- Multiple conflicting immediate parents where prohibited by the model
- Invalid child membership
- Orphaned entities
- Broken hierarchy paths
- Duplicate hierarchy relationships

**Source**: `CR-BP-94-EXT-22 R22-02`, `CR-BP-EXT-23 REQ-23-09`, `CR-BP-94-EXT-09 REQ-09-05`.

### 1.5 The 5-phase L4 Task pattern (canonical)

Every L3 Activity has exactly **5 L4 Tasks** in the canonical CR-BP-102 5-phase pattern:

1. **Intake** (the request or trigger enters the Activity)
2. **Processing** (the work is performed)
3. **Verification** (the work is checked)
4. **Confirmation** (the result is confirmed)
5. **Record** (the result is recorded)

These are 5 phase-differentiated siblings with distinct responsibility values, **not** duplicates. The pattern is uniform across all 580 L3 Activities (2,900 L4 Tasks total). (`CR-BP-94-EXT-22 R22-11`, `CR-BP-94-EXT-21 L4-005`.)

### 1.6 Decomposition profiles (required / conditional / optional / not_applicable / inherited)

Every operational attribute has a profile classification per decomposition level:

- **required** - the attribute must be populated
- **conditional** - the attribute is required under documented conditions
- **optional** - the attribute may be populated
- **not_applicable** - the attribute does not apply at this level (L0/L1 are non-executable; L4 is non-orchestrating)
- **inherited** - the attribute is inherited from a parent (L3 inherits certain operational attributes from its L2; L4 from its L3)

The framework must **not** require every operational property to be populated at every level. In particular:

- An L1 Process Group must not be treated as an executable Business Process.
- An L3 Activity must not automatically be required to have all the operational attributes of an L2 Business Process.
- An L4 Task must not be required to define workflow orchestration or execution sequence.

**Source**: `CR-BP-94-EXT-11 REQ-11-04..10`, `CR-BP-EXT-23 REQ-23-05`.

### 1.7 The 5-level entity-kind / state vocabulary

| State | Meaning |
|---|---|
| `proposed` | the entity has been proposed but not yet approved |
| `under_review` | the entity is being reviewed by a domain reviewer |
| `approved` | the entity has been approved for inclusion |
| `active` | the entity is the current operational source of truth |
| `superseded` | the entity has been replaced by a successor |
| `deprecated` | the entity is no longer valid (preserved for traceability) |
| `retired` | the entity has been removed (only the history remains) |

The lifecycle distinguishes **entity approval** from **the operational status of the real-world process**. A process entity may be approved as a catalogue representation while the underlying business process is under redesign. These are separate facts. (`CR-BP-94-EXT-24 REQ-24-13`.)

---

## 2. Operational data model [NORMATIVE]

The operational data model defines the canonical schema, the evidence model, the controlled vocabularies and the completeness model.

### 2.1 The 5 canonical schemas

Every entity conforms to one of the 5 entity schemas (`schemas/entities/*.schema.json`). The schemas are the **authoritative definitions** of permitted fields, field types, required properties, identifier formats and reference formats. Validation tooling does not independently redefine entity semantics through validation scripts.

The schemas carry a version (currently 1.0.0). Schema changes follow the EXT-24 metamodel + schema evolution governance: change rationale, affected entity types, compatibility assessment, migration strategy, validation changes, regression tests, documentation updates, approval, deprecation plan. (`CR-BP-94-EXT-10 REQ-10-01..12`, `CR-BP-94-EXT-24 REQ-24-31`.)

### 2.2 Identifier rules (IDM)

Canonical identifiers conform to:

- **Pattern (IDM-001)**: `^[a-z]+:[a-z]+(-[a-z]+){1,4}-[a-z2-9]{6}$`
- **Strict BASE32 (IDM-004)**: `abcdefghjkmnpqrstuvwxyz23456789`
- **Filename + cell segment + depth** consistency (IDM-005)

The cell-charter L0 Process Context uses the `pc-...` id segment; L1 Process Groups use `group-...`; L2 Business Processes use `process-...`; L3 Activities use `activity-...`; L4 Tasks use `task-...`. (`CR-BP-94-EXT-10 REQ-10-08..10`.)

### 2.3 The evidence and provenance model

A material operational assertion carries:

- **Source reference** - a stable reference to the source material
- **Source classification** - the type of source (regulation, internal policy, external standard, etc.)
- **Confidence classification** - high / medium / low
- **Verification status** - not_reviewed / under_review / verified / rejected / superseded / disputed
- **Review requirements** - what level of approval is needed

The framework distinguishes **confidence** from **verification status**. A claim marked `high confidence` must not automatically be treated as `verified`. Likewise, the existence of a source reference must not automatically establish that the source supports the associated assertion. The latter requires substantive review.

AI-assisted research is permitted but must be disclosed: every AI-assisted assertion carries an `ai_assisted` flag, a confidence classification and a review requirement.

**Source**: `CR-BP-94-EXT-15 REQ-15-01..12`, `CR-BP-EXT-23 REQ-23-13..14`.

### 2.4 The 6-value completeness / information-state vocabulary

The framework distinguishes the state of information from its value:

- `automated` - machine-verified by an active conformance rule
- `human_review` - the assertion requires business authority review
- `evidence_assessment` - the assertion requires examination of source material
- `deferred` - the assertion is formally deferred with approved disposition
- `not_enforceable` - the requirement cannot be automatically enforced
- `not_applicable` - the requirement does not apply to this entity

An empty value must not automatically be interpreted as any of these states. The framework flags ambiguous empty or missing information where the applicable profile requires explicit disposition.

**Source**: `CR-BP-EXT-23 REQ-23-02`, `CR-BP-EXT-23 REQ-23-06`.

### 2.5 Controlled vocabularies

The catalogue uses four controlled vocabularies (`classifications/`):

- `process-group-kinds.yaml`
- `process-intents.yaml`
- `process-specializations.yaml`
- `process-types.yaml`

New values are not introduced informally through individual entity files. Vocabulary changes follow the EXT-24 profile and vocabulary governance procedure: identify affected entities, assess migration, version, approve, migrate. A vocabulary value must not be removed while existing canonical entities still depend on it unless an approved migration or compatibility mechanism exists.

**Source**: `CR-BP-94-EXT-10 REQ-10-11..12`, `CR-BP-94-EXT-24 REQ-24-32`.

### 2.6 Responsibilities and accountability (RACI)

The framework distinguishes:

- **Responsibility** - the role performing the work
- **Accountability** - the role answerable for the outcome (single point of accountability per Activity / Task)
- **Consulted** - the role whose input is sought
- **Informed** - the role kept informed of progress or outcome
- **Decision authority** - the role with authority to make the decision
- **Process Owner** - the role answerable for the meaning, scope and operational accuracy of a Business Process
- **Performer** - the role or agent that actually executes the work (may be human, AI agent, or automation system)

AI agents may be performers but are **never automatically accountable**. An AI agent's ability to execute a Task does not automatically make it accountable for the Business Process.

**Source**: `CR-BP-94-EXT-13 REQ-13-01..12`, `CR-BP-94-EXT-24 REQ-24-43..46`.

---

## 3. Engineering specification [NORMATIVE]

The engineering specification defines authoring, generation, validation, CI integration, reconciliation and reporting.

### 3.1 Authoring methodology

Every entity is authored according to a controlled methodology:

1. **Discovery** - identify the gap and the proposed entity (formal Discovery exercises where required)
2. **Classification** - assign the entity type, level and applicable profile
3. **Parent assignment** - identify the parent entity and verify the parent-child relationship is permitted
4. **Scope and purpose** - define what the entity represents and what it does not
5. **Operational documentation** - populate the required attributes per the profile
6. **Evidence and provenance** - source, confidence, verification status, AI-assisted research disclosure
7. **Relationship validation** - verify all parent-child and cross-cutting references resolve
8. **Review and approval** - obtain the required business, architectural and governance approvals
9. **Canonical publication** - commit the canonical YAML to the entity directory
10. **Documentation generation** - regenerate the README from the canonical entity data
11. **Conformance validation** - run the conformance framework to verify the entity is structurally valid

New entities must not be added as unstructured documentation outside the canonical entity architecture. A change must not be implemented as an informal data correction when it materially changes the architecture or semantics.

**Source**: `CR-BP-94-EXT-16 REQ-16-01..12`, `CR-BP-94-EXT-24 REQ-24-14..15, REQ-24-41`.

### 3.2 Documentation generation pipeline

Documentation is **generated** from the canonical entity data using the approved documentation architecture:

- **Schema-driven generation**: the README template (`templates/*.md`) is filled from the entity YAML
- **Single source of truth**: the YAML is authoritative; the README is generated and must not become an independent source of conflicting operational truth
- **Conformance check**: every README must conform to the EXT-04 documentation profile validator (DOC-016..020)
- **Refresh on policy change**: when the documentation profile changes, all entity READMEs are regenerated

The framework identifies whether documentation is:

- generated and current
- generated but outdated
- manually maintained where generation is required
- missing
- inconsistent with the canonical entity representation

**Source**: `CR-BP-94-EXT-04 DOC-016..020`, `CR-BP-EXT-23 REQ-23-15`.

### 3.3 The conformance framework (EXT-23)

Conformance is governed by the formal conformance framework landed in CR-BP-EXT-23:

- **Versioned conformance rule catalogue** (`reconciliation/conformance/conformance-rule-catalogue.json`): every rule carries all 16 required attributes per REQ-23-01
- **Requirement-to-rule traceability matrix** (`reconciliation/conformance/requirement-traceability-matrix.json`): every requirement from EXT-08..EXT-23 is mapped to one or more rules, or explicitly classified with the 6-value vocabulary
- **Controlled vocabularies**: 9 conformance dimensions (structural / schema / profile / semantic / evidence / documentation / cross-catalogue / reconciliation / governance), 8 validation layers (L1..L8), 5 rule classifications (C1 deterministic / C2 rule-assisted / C3 evidence-dependent / C4 human-judgement / C5 governance-controlled), 4 severities (error / warning / info / deferred), 6 outcomes (passed / passed_with_warnings / failed / blocked / not_assessed / passed_with_approved_exceptions)
- **Progressive enforcement**: 5 stages (discovery_and_reporting -> warning_only -> blocking_for_new_defects -> historical_remediation -> full_enforcement); current stage: `blocking_for_new_defects`
- **Exception lifecycle**: 5 categories (technical / semantic / evidence / governance / migration) and 8 states (proposed / under_review / approved / rejected / active / expired / revoked / closed); only an approved active exception may affect enforcement
- **Validation report** (`reconciliation/conformance/conformance-report.json`) and **catalogue-level dashboard** (`reconciliation/conformance/conformance-dashboard.json`)

The 5 important design decisions preserved per the user's CR §20:

1. **No single conformance score** - the dashboard exposes the 9 dimensions separately; `aggregate_score` is `null`
2. **No false semantic automation** - C2-C5 rules cannot be `automated_blocking`; human_review and evidence_assessment are explicit statuses
3. **No permanent grandfathering** - historical baseline defects are accounted for but do not block; newly introduced defects block immediately
4. **No parallel source of truth** - the catalogue consumes the registry; the matrix consumes the catalogue; the report consumes both
5. **No ungoverned exceptions** - every exception has owner, scope, approval, review date

**Source**: `CR-BP-EXT-23 REQ-23-01..32`, `CR-BP-94-EXT-22 REQ-22-17`.

### 3.4 Conformance posture (the 52 gates)

The conformance registry in `scripts/conformance_result.py` is the single source of truth for 52 conformance gates. The conformance posture:

- **29 blocking gates** (the default blocking set)
- **23 advisory gates** (deferred / pre-validation)
- **9 promoted EXT gates** ([36] Profile Registry, [37] Inputs/Outputs/Interfaces, [38] Responsibility/Accountability, [39] Business Rules/Controls/Exceptions, [40] Evidence/Provenance, [41] Authoring Methodology, [43] Operational Documentation Pilot, plus the EXT-04 [34] Documentation Profile and EXT-05 [35] Decomposition Reconciliation foundations), all PASS

The 4 pre-existing blocking failures ([1] validate-process-entries, [26] Reference Embargo, [30] README Consistency, [33] Entity System) are owned by their originating CRs, predating the EXT-08..EXT-24 programme, and are explicitly recorded in the residual gap register (REQ-24-04).

The 4 EXT-23 deferred gates ([44] L2 backfill, [45] L3 backfill, [46] L4 backfill, [47] decomposition reconciliation) carry advisory findings pending the L2/L3/L4 content backfills (REQ-19..24 deferred work).

### 3.5 CI integration

The conformance framework is integrated with the existing CI pipeline (`.github/workflows/ci.yml`):

- **Pull request validation**: every relevant pull request executes the applicable conformance checks; PRs may be blocked by 29 blocking gates
- **Full catalogue validation**: a full catalogue validation is available independently of pull request validation
- **Change-impact validation**: a change to an L2 Process triggers review of its L3 Activities and L1 membership; a change to a controlled vocabulary triggers review of every entity using that vocabulary
- **Backwards compatibility**: historical baseline defects do not block acceptance; newly introduced defects block acceptance immediately

The protocol uses an `--auto` flag with `gh pr merge --squash --delete-branch` for the merge step; the same flag is used to retry a merge that has been blocked by an unrelated failure.

**Source**: `CR-BP-EXT-23 REQ-23-23..24, REQ-23-28`.

### 3.6 Reconciliation (EXT-22)

The L2-L4 Reconciliation Matrix (`reconciliation/reconciliation-matrix.json`) is the principal reconciliation artefact:

- **2,901 records** with all 26 of the Section 7.2 required fields
- **Generated view** over the canonical entity data (no new canonical entity fields)
- **8 structural findings** recorded with disposition: 1 L2 without L3 decomposition + 1 L2 without L1 membership (the same deprecated process-ge-conceive-e6jx6s) + 6 L1-to-L2 L0 context mismatches
- **16 granularity review prompts** (16 L1 Process Groups with exactly 1 L2 member); review prompts, not defects per principle 5.4 (no fixed entity-count requirement)

Reconciliation must distinguish **top-down decomposition integrity** (the parent is adequately represented by its children) from **bottom-up semantic integrity** (every child has a defensible relationship to its parent). Both directions are necessary.

**Source**: `CR-BP-94-EXT-22 REQ-22-01..22, R22-01..12`.

### 3.7 Reporting and dashboards

The reporting regime distinguishes:

- **Validation report** (per-run): machine-readable result + human-readable summary; includes run id, framework / schema / profile / rule versions, scope, rules executed, results by severity and dimension, findings, outcome, remediation guidance, and the **interpretation limit**: passing validation is not proof that documented business practice matches actual organisational practice
- **Catalogue-level dashboard**: the 9 dimension measures reported separately; `aggregate_score` is `null`; the framework does not average dimensions into a single number
- **Trend analysis**: historical reports are retained for trends showing defects introduced / resolved / recurring / ageing, review completion, overdue review levels, evidence freshness, exception frequency, documentation drift

**Source**: `CR-BP-EXT-23 REQ-23-25..26`, `CR-BP-94-EXT-24 REQ-24-36..37`.

---

## 4. Governance specification [NORMATIVE]

The governance specification establishes ownership, lifecycle, approvals, exceptions, review cycles and continuous improvement.

### 4.1 The 9 governance roles

The 9 roles and their mapping to actual repository governance conventions:

| ID | Role | Mapped to |
|---|---|---|
| GOV-001 | Catalogue Steward | programme owner |
| GOV-002 | Business Process Owner | the accountable business authority for each L2 BP |
| GOV-003 | Process Domain Reviewer | cell-scoped domain reviewers (F&A, P&R, P&V, S&D, R&C) |
| GOV-004 | Entity Maintainer | cell-charter maintainers |
| GOV-005 | Metamodel Steward | dea-metaframework steward |
| GOV-006 | Data and Evidence Reviewer | EXT-15 evidence framework owner |
| GOV-007 | Conformance Maintainer | EXT-23 conformance framework owner |
| GOV-008 | Repository Maintainer | the repo maintainer; CI via .github/workflows/ci.yml |
| GOV-009 | Governance Authority | programme authority |

A single individual may fulfil multiple roles where appropriate.

**Source**: `CR-BP-94-EXT-24 REQ-24-09`.

### 4.2 Ownership assignment

Every L2 Business Process has an identifiable ownership disposition in the ownership register (`reconciliation/closure/ownership-register.json`):

- **146 L2 BPs**; every BP has an explicit disposition
- Where the actual owner is known, the canonical entity references that owner using the appropriate existing model
- Where ownership cannot be established, the entity is explicitly marked `awaiting_owner_confirmation` and the Process Domain Reviewer (GOV-003) is responsible for assigning the named owner
- L3 Activities and L4 Tasks may have distinct responsible parties, performers or authorities where justified
- Ownership is not automatically inherited from the parent entity

**Source**: `CR-BP-94-EXT-24 REQ-24-10`.

### 4.3 Entity lifecycle

The lifecycle vocabulary is the 7-state model in Section 1.7. Lifecycle transitions follow the EXT-24 §9.2 procedures:

- **New entity governance**: proposal -> classification -> parent assignment -> scope/purpose -> operational documentation -> evidence/provenance -> relationship validation -> review/approval -> canonical publication -> documentation generation -> conformance validation
- **Entity modification governance**: material changes are traceable; the change identifies the reason and the relevant authority
- **Deprecation and supersession**: entities that are no longer valid are not silently deleted where doing so would destroy traceability; the lifecycle mechanism supports deprecation, supersession, replacement references, historical traceability, relationship migration, documentation updates
- **Parent-child lifecycle coordination**: changes to a parent entity trigger impact assessment of affected children (L2 boundary change -> L3 review; L3 boundary change -> L4 review; L1 change -> L2 membership review; L0 change -> L1 + L2 scope review)

**Source**: `CR-BP-94-EXT-24 REQ-24-14..17`.

### 4.4 Approvals and exception lifecycle

Material governance decisions follow the exception lifecycle:

- **Categories** (REQ-24-21 §10.1): `technical`, `semantic`, `evidence`, `governance`, `migration`
- **States**: `proposed` -> `under_review` -> `approved` / `rejected` -> `active` -> `expired` / `revoked` / `closed`
- **Only an approved active exception may affect enforcement**
- **Constraints**: owner, scope, rationale, approving authority, approval date, expiry / review date
- An exception must not alter the underlying rule and must not propagate to child entities (an exception on an L2 Process does not automatically exempt its L3 Activities or L4 Tasks)

**Source**: `CR-BP-94-EXT-24 REQ-24-21`.

### 4.5 Review cycles

The default review intervals:

| Entity or artefact | Suggested review interval |
|---|---|
| L0 Process Context | annually and on material scope changes |
| L1 Process Group | annually and on membership changes |
| L2 Business Process | at least annually, or more frequently for high-impact processes |
| L3 Activity | every 12-24 months or when its parent changes materially |
| L4 Task | every 12-24 months or when its Activity, systems or operational method changes |
| Evidence references | according to source volatility and evidence classification |
| Schemas and profiles | on approved model changes and scheduled governance review |
| Validation rules | on requirement changes and periodic rule effectiveness review |
| Exceptions and deferrals | at their approved review or expiry date |

These intervals are policy defaults, not automatic claims that an entity remains accurate until its next review.

Review frequency is influenced by: business criticality, regulatory significance, operational risk, rate of organisational change, system dependency, evidence volatility, degree of automation, AI involvement, previous non-conformance, historical frequency of material changes.

**Source**: `CR-BP-94-EXT-24 REQ-24-18..19`.

### 4.6 Event-triggered governance

Periodic reviews alone are insufficient. Events that initiate impact assessment or review include:

- **Organisational**: restructuring, ownership changes, mergers / acquisitions, outsourcing / insourcing
- **Business**: new products or services, customer journey changes, new capabilities or functions, operating model changes, process introductions / retirements
- **Technology**: IS introduction / replacement / retirement, IS function changes, major integrations, automation introduction, AI agent introduction, agent responsibilities changes
- **Governance**: new policies, regulatory changes, risk assessments, audit findings, material incidents
- **Architecture**: metamodel changes, vocabulary changes, relationship model changes, catalogue boundary changes
- **Evidence**: new authoritative documentation, contradictory operational evidence, expired evidence, process owner confirmation, undocumented practice discovery

The event-to-entity impact mapping identifies affected entities using canonical references (not textual similarity). A material change to decomposition triggers repetition of the relevant EXT-22 reconciliation requirements.

**Source**: `CR-BP-94-EXT-24 REQ-24-23..25`.

### 4.7 Cross-catalogue governance

The Business Process catalogue maintains its relationships with relevant OpenDEA catalogues via canonical identifiers and approved relationship types:

- Business Capabilities
- Business Functions
- Information Systems
- Information Systems Functions
- Metrics
- Organisational entities
- Policies
- Risks
- Controls
- Agent profiles
- Agent skills
- Value Streams

The Business Process catalogue must not create local copies of external entity semantics merely to avoid maintaining references. Cross-catalogue ownership boundaries: Business Process purpose and transformation belong to the process model; Business Capability definition belongs to the capability catalogue; Information System identity belongs to the Information Systems catalogue; Metric definition belongs to the Metric catalogue; Risk definition belongs to the Risk catalogue; Control definition belongs to the applicable control model.

Cross-catalogue references use canonical identifiers and approved relationship types; a change to a referenced entity triggers an impact assessment of dependent processes.

**Source**: `CR-BP-94-EXT-24 REQ-24-26..29`.

### 4.8 Metamodel and schema evolution

Metamodel alignment is monitored continuously. Changes that trigger impact assessment include:

- Entity definitions
- Attribute semantics
- Relationship types
- Relationship cardinality
- Identifier rules
- Entity lifecycle
- Decomposition
- Evidence representation
- Responsibility and accountability
- Metrics and measurement

Schema changes follow controlled change management: change rationale, affected entity types, compatibility assessment, migration strategy, validation changes, regression tests, documentation updates, approval, deprecation plan. Schema changes must not silently reinterpret historical entity data.

**Source**: `CR-BP-94-EXT-24 REQ-24-30..34`.

### 4.9 AI and automation governance

AI-assisted catalogue maintenance is permitted but governed:

- **AI may support**: entity discovery, documentation drafting, evidence classification, potential duplicate detection, parent-child contribution analysis, decomposition gap detection, cross-catalogue reference discovery, semantic consistency review, documentation generation, conformance issue explanation
- **AI must not independently**: approve Business Process semantics, confirm actual operational practice, assign organisational accountability, authorise entity deprecation, approve exceptions, change metamodel semantics, declare a catalogue fully reconciled
- **AI-assisted recommendations must remain distinguishable from verified catalogue information** (the `ai_assisted` flag on every AI-assisted assertion)
- **Human approval remains mandatory** for decisions requiring business authority

Where automation materially changes how work is performed, the affected process entities are reviewed. The introduction of automation must not automatically result in a new Task or Activity; the decision is based on whether the underlying business responsibility or functional composition has changed.

**Source**: `CR-BP-94-EXT-24 REQ-24-43..46`.

### 4.10 Continuous improvement

The continuous improvement cycle:

1. **Monitor** - observe conformance, evidence freshness, entity lifecycle, cross-catalogue changes
2. **Detect** - identify changes, defects, outdated assertions, broken references, emerging requirements
3. **Assess** - determine business impact, affected entities, evidence requirements, governance implications
4. **Decide** - approve corrections, changes, exceptions, deferrals, architectural improvements
5. **Implement** - update canonical entities, documentation, relationships, schemas, tooling
6. **Validate** - run EXT-23 conformance checks + any required EXT-22 reconciliation
7. **Approve** - obtain the required business, architectural, governance approvals
8. **Publish** - release approved catalogue changes and associated documentation
9. **Review** - monitor the outcome and update the improvement backlog

The improvement backlog classifies items by category (defect correction / completeness improvement / semantic improvement / structural improvement / metamodel alignment / automation improvement / governance improvement / integration improvement / innovation) and prioritises by business impact, risk reduction, regulatory significance, catalogue quality, operational value, architectural alignment, dependency impact, implementation effort and urgency.

This is a governance lifecycle, not an instruction to model every process as a workflow.

**Source**: `CR-BP-94-EXT-24 REQ-24-39..42, REQ-24-18`.

---

## 5. Implementation and acceptance baseline [NORMATIVE]

The implementation and acceptance baseline records the CR traceability, ADR decisions, test coverage, migration status and operational readiness.

### 5.1 CR-to-rule traceability

**246 requirements** are traced from EXT-08 through EXT-23 in the requirement-to-rule traceability matrix (`reconciliation/conformance/requirement-traceability-matrix.json`):

- **212 automated** (mapped to one or more active conformance rules)
- **33 human_review** (the semantic and governance-approval requirements; scripts detect but cannot certify)
- **1 evidence_assessment** (REQ-23-14)

Every requirement has an explicit status from the 6-value vocabulary; no requirement is silently absent. The matrix exposes any requirement that has been specified but never operationalised.

### 5.2 Conformance rule catalogue

**52 conformance rules** (`reconciliation/conformance/conformance-rule-catalogue.json`):

- Each rule carries all 16 REQ-23-01 required attributes: rule_id, rule_name, description, requirement_traceability, adr_traceability, applicable_entity_types, applicable_levels, validation_dimension, validation_layer, validation_method, severity, rule_version, expected_result, remediation_guidance, exception_eligible, test_coverage, rule_lifecycle_status (plus disclosure_class)
- Distribution: 21 structural / 4 schema / 8 profile / 7 semantic / 3 evidence / 6 documentation / 1 cross-catalogue / 3 reconciliation / 5 governance
- Classification: 45 C1 deterministic / 7 C2 rule-assisted
- All 8 validation layers represented

### 5.3 ADR register (programme-wide)

The 13 ADRs established across the programme (CR §17 references + EXT-23 + EXT-24):

- **ADR-BP-CONF-001..006** (EXT-23): Conformance Rule Architecture; Validation Outcome and Severity Model; Exception and Waiver Governance; Progressive Enforcement Strategy; Validation Report and Metrics Architecture; Semantic Validation and Human Review Boundary
- **ADR-BP-GOV-001..009** (EXT-24): Catalogue Governance Operating Model; Process Entity Lifecycle; Ownership and Review Accountability; Evidence Refresh and Verification Policy; Cross-Catalogue Dependency Governance; Metamodel and Schema Evolution Governance; Continuous Conformance Monitoring; AI-Assisted Catalogue Maintenance; Programme Closure and Catalogue Baseline

### 5.4 Test coverage

The 66+ automated tests across the programme (the meta-frameworks + the 52 conformance rules + the 9 governance artefacts):

- **EXT-22 tests** (18 tests + 1,343 subtests): L0/L1/L2/L3/L4 hierarchy validation, the 12 deterministic rules, the reconciliation matrix integrity, the structural integrity report
- **EXT-23 v2 tests** (22 tests + 22 subtests): the conformance framework's own self-check (the rule catalogue, the traceability matrix, the controlled vocabularies, the exception model, the deferral model, the progressive enforcement policy, the report, the dashboard)
- **EXT-24 tests** (22 tests + 22 subtests): the closure self-check (the closure matrix, the catalogue baseline, the governance artefacts)
- **Per-rule test files**: 52 named test files in `tests/test_*.py` exercising the 52 conformance rules

### 5.5 Migration status (deferred work)

The 7 deferred-work items recorded in the deferred-work register (`reconciliation/closure/deferred-work-register.json`):

- **DFR-001**: L2 content backfill (REQ-19; 146 L2 BPs; 733 evidence gaps; target 2027-03-31)
- **DFR-002**: L3 content backfill (REQ-20; 580 L3 Activities; 4,061 evidence gaps; target 2027-06-30)
- **DFR-003**: L4 content backfill (REQ-21; 2,900 L4 Tasks; 5,800 evidence + authoring gaps; target 2027-09-30)
- **DFR-004**: EXT-22 structural findings (8; the deprecated process-ge-conceive-e6jx6s + 6 L1-to-L2 compositions; target 2026-12-31)
- **DFR-005**: EXT-22 granularity reviews (16 L1 Process Groups with exactly 1 L2 member; target 2027-03-31)
- **DFR-006**: pre-existing blocking failures (4: [1] [26] [30] [33]; target 2026-11-30)
- **DFR-007**: AI-assisted maintenance policy (REQ-24-43..46; target 2026-12-31)

### 5.6 Operational readiness

The catalogue baseline at the post-EXT-24 merge commit:

- **3,724 canonical records** (49 L0 + 49 L1 + 146 L2 + 580 L3 + 2,900 L4)
- **All 9 promoted EXT gates PASS**
- **0 approved exceptions** at programme closure
- **0 EXT-23 framework findings**
- **0 EXT-22 structural findings** beyond the 8 recorded
- **0 EXT-24 closure findings**
- **3,725 lifecycle records** with state + approved_by + review dates

The conformance framework is **operational** after programme closure (EXT-23 REQ-23-35): pull request validation, entity change validation, full catalogue validation, scheduled validation, cross-catalogue reference validation, evidence freshness checks, exception expiry checks, documentation drift checks, reconciliation status checks.

### 5.7 Acceptance criteria for v1.0

The Specification v1.0 is accepted when:

1. **AC-1**: All 17 CRs of the DEA-PROCESS-ENRICH-000 programme are sealed (programme closure)
2. **AC-2**: The rule catalogue carries 52 conformance rules with all 16 required attributes (REQ-23-01)
3. **AC-3**: The traceability matrix maps all 246 requirements from EXT-08..EXT-23 to conformance rules with explicit status (REQ-23-02)
4. **AC-4**: The catalogue baseline records 3,724 canonical records at the post-EXT-24 revision with integrity notes (REQ-24-06..08)
5. **AC-5**: The 9 governance roles are mapped to actual repository governance conventions (REQ-24-09)
6. **AC-6**: The L2 BP ownership register covers all 146 L2 BPs with explicit dispositions (REQ-24-10)
7. **AC-7**: The lifecycle register covers 3,725 records with the 7-state controlled vocabulary (REQ-24-13)
8. **AC-8**: The exception register, the deferred-work register and the improvement backlog carry the 5 / 7 / 10 required fields per record (REQ-24-21..22, REQ-24-39..40)
9. **AC-9**: All 9 promoted EXT gates PASS the conformance run
10. **AC-10**: The 8 operational governance artefacts (§17 of EXT-24) are version-controlled under `reconciliation/closure/`
11. **AC-11**: The 66+ automated tests pass (22 + 22 + 22 minimum)
12. **AC-12**: D-004 is clean across all 60+ files of the EXT-08..EXT-24 programme
13. **AC-13**: The 4 pre-existing blocking failures are owned by their originating CRs, not by EXT-24
14. **AC-14**: The interpretation limit (passing validation is not proof of business effectiveness) is preserved in the conformance report
15. **AC-15**: The improvement backlog IMP-010 (Specification v1.0 itself) carries target_review_date 2027-03-31

---

## 6. Document control

| Field | Value |
|---|---|
| Specification ID | BP-DS-Spec-v1.0 |
| Version | 1.0.0 |
| Status | Proposed for adoption |
| Owner | Emmanuel A. Otchere |
| Source CRs | CR-BP-94-EXT-08..24 (17 CRs) |
| Programme | DEA-PROCESS-ENRICH-000 |
| Repository | technehub-labs/dea-catalog-business-processes |
| Source baseline | `reconciliation/closure/catalogue-baseline.json` (revision 9275f77d) |
| Date | 2026-10-20 |

### Companion artefacts

- `reconciliation/conformance/conformance-rule-catalogue.json` - the 52 conformance rules
- `reconciliation/conformance/requirement-traceability-matrix.json` - the 246 traced requirements
- `reconciliation/conformance/conformance-report.json` - the validation report
- `reconciliation/conformance/conformance-dashboard.json` - the catalogue-level dashboard
- `reconciliation/closure/programme-closure-matrix.json` - the 17-CR closure matrix
- `reconciliation/closure/catalogue-baseline.json` - the authoritative baseline
- `reconciliation/closure/residual-gap-register.json` - the 12 residual gaps
- `reconciliation/closure/governance-roles.json` - the 9 governance roles
- `reconciliation/closure/ownership-register.json` - the 146 L2 BP dispositions
- `reconciliation/closure/lifecycle-register.json` - the 3,725 lifecycle records
- `reconciliation/closure/exception-register.json` - the 0 approved exceptions
- `reconciliation/closure/deferred-work-register.json` - the 7 deferred items
- `reconciliation/closure/improvement-backlog.json` - the 10 improvement items
- `reconciliation/reconciliation-matrix.json` - the 2,901-record L2-L4 reconciliation
- `governance/closure-report.md` - the human-readable programme closure report

### Versioning

This specification follows semantic versioning. A change to a normative rule requires:

- Change rationale
- Impact assessment
- Compatibility assessment
- Regression tests
- Approval where required

Historical validation reports retain the version information needed to interpret their results.

### The 5 important design decisions (CR §20)

1. **No single conformance score** - the dashboard exposes the 9 dimensions separately; `aggregate_score` is `null`
2. **No false semantic automation** - C2-C5 rules cannot be `automated_blocking`
3. **No permanent grandfathering** - historical baseline defects do not block; newly introduced defects block immediately
4. **No parallel source of truth** - the catalogue consumes the registry; the matrix consumes the catalogue; the report consumes both
5. **No ungoverned exceptions** - every exception has owner, scope, approval, review date

### The 8 operational governance artefacts (CR §17)

| Artefact | Status |
|---|---|
| Programme Closure Report | landed (`governance/closure-report.md`) |
| Catalogue Baseline Record | landed (`reconciliation/closure/catalogue-baseline.json`) |
| Requirement Traceability Matrix | landed (`reconciliation/conformance/requirement-traceability-matrix.json`) |
| Entity Ownership Register | landed (`reconciliation/closure/ownership-register.json`) |
| Entity Lifecycle Register | landed (`reconciliation/closure/lifecycle-register.json`) |
| Reconciliation Matrix | landed (`reconciliation/reconciliation-matrix.json`) |
| Conformance Rule Catalogue | landed (`reconciliation/conformance/conformance-rule-catalogue.json`) |
| Conformance Reports | landed (`reconciliation/conformance/conformance-report.json`) |
| Exception Register | landed (`reconciliation/closure/exception-register.json`) |
| Deferred Work Register | landed (`reconciliation/closure/deferred-work-register.json`) |
| Improvement Backlog | landed (`reconciliation/closure/improvement-backlog.json`) |

### What this specification does NOT do

This specification does not:

- Replace the established metamodel or the L0-L4 semantics
- Reopen completed enrichment work without an identified reason
- Make every entity subject to identical review frequencies
- Require all evidence to be publicly stored in the repository
- Assume that all process information can be fully automated
- Replace enterprise process ownership or operational governance
- Automatically certify the effectiveness of documented processes
- Automatically approve changes to process semantics
- Introduce new relationship types without appropriate metamodel governance

Where new substantive requirements are discovered, they are managed through separate CRs or approved changes to the relevant architectural artefacts.

---

## 7. Glossary

| Term | Definition |
|---|---|
| ADMIT-CANONICAL | The Discovery decision that a candidate is suitable for inclusion in the canonical catalogue |
| AI agent | An automated or agentic system that can perform Tasks; may be a Performer but is never automatically Accountable |
| Business Process | An L2 entity representing a complete business transformation |
| Canonical data | The authoritative YAML representation of an entity |
| Cell-charter | The L0 Process Context variant using the process-context schema and no `type` field; level resolved from id prefix |
| Conformance framework | The EXT-23 rule catalogue + traceability matrix + report + dashboard + governance regime |
| Cross-cutting association | A reference that is not decomposition parentage (e.g., a Task supporting multiple Activities) |
| Decomposition profile | The required / conditional / optional / not_applicable / inherited classification per decomposition level |
| Discovery | The formal process for evaluating candidate entities for canonical admission |
| Disposition vocabulary | The 6-value state of information vocabulary (automated / human_review / evidence_assessment / deferred / not_enforceable / not_applicable) |
| ECF | Enterprise Conceptual Framework - the OpenDEA cross-cutting framework |
| Evidence | A reference + classification + confidence + verification status on a material assertion |
| Exception | An approved deviation from a conformance rule, scoped, owned, approved, reviewable, revocable, time-bound |
| Gate | A registered conformance check in `scripts/conformance_result.py` |
| Improvement backlog | The controlled list of future catalogue improvements (REQ-24-39) |
| Lifecycle | The 7-state entity lifecycle (proposed / under_review / approved / active / superseded / deprecated / retired) |
| Process Owner | The role answerable for the meaning, scope and operational accuracy of a Business Process |
| RACI | Responsibility / Accountability / Consulted / Informed |
| Review cycle | The periodic review interval for an entity or class of entities |
| Rule classification | The 5-value C1-C5 classification (deterministic / rule-assisted / evidence-dependent / human-judgement / governance-controlled) |
| Validation layer | The 8-layer validation framework (L1 repository integrity ... L8 governance) |
| Validation rule | A version-controlled conformance check bound to a registered gate |
| Validation severity | The 4-value severity model (error / warning / info / deferred) |

---

**End of Specification v1.0**