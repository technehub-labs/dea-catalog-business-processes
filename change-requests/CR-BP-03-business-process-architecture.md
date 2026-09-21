# CR-BP-03 — Business Process Architecture

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status:** Proposed (refined 2026-09-03)
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Type:** Architecture / Semantic / Catalog
**Priority:** High
**Repository:** `technehub-labs/dea-catalog-processes`
**Depends On:** CR-MM-PROC-01 (dea-metamodel), CR-AR-FMWK-01
(dea-architecture-framework), CR-BP-SPEC-BP-01 (this repo), CR-BP-02
(this repo)
**Refines:** CR-BP-03 initial draft (2026-09-03) — applies the user's
clarifications:
- process_audience confirmed to the ECF domain;
- L0/L1/L2 layering is conceptual, not separate top-level
  directories; the spec is improved, not restructured;
- delivery is one PR;
- re-landscape is **contribution-driven** (a new process
  contribution is submitted to `contributions/`, a report is
  generated, and the report is piped through CI for reclassification
  recommendations); not an in-tree automatic validator.

---

## 1. Intent

Establish the Business Process architecture within the enterprise
process landscape by:

1. **Improving the process spec** — adding 4 distinct classification
   axes (intent / type / specialization / audience) and a
   process-identity sub-block (verb + object + scope + outcome +
   evidence) to the existing L2 Business Process schema;
2. Establishing `dea:BusinessProcess` as the canonical L2 semantic
   entity (no new OpenDEAM entities added);
3. Using `dea:composes` as the normative structural relationship
   (with `parent_process` / `child_processes` preserved as
   migration aliases);
4. Using `dea:realizes` as the normative capability-realization
   relationship (with `capabilities_delivered` preserved as a
   migration alias);
5. Distinguishing Business Processes from the four other enterprise
   process types (Strategic / Management / Core / Support /
   Standardization; per Mintzberg);
6. **Contribution-driven re-landscaping** — new process contributions
   are submitted to `contributions/processes/`; a contribution
   template captures the current classification; the CI report
   workflow emits a reclassification recommendation when the
   contribution's name + description + outcome + trigger are
   inconsistent with the declared process_type / process_intent;
7. Revamping the README to make the architecture explicit and
   authoritative.

**Additive only.** CR-BP-03 introduces new fields and
sub-blocks. It does not deprecate, rename, or remove existing
fields. Existing catalog entries continue to validate; new entries
should declare the new fields.

**No new top-level directories** for the L0/L1/L2 hierarchy. L0/L1
are conceptual constructs documented in README + docs; L2 is the
canonical path (`entities/v1/`). The spec is improved; the
top-level structure is preserved.

---

## 2. Architectural insight (refined)

### 2.1 The five organizational components (Mintzberg)

| Organizational Component | Process Type | Primary Character |
|---|---|---|
| Strategic Apex | Strategic | Direction, vision, goals, strategic decisions |
| Middle Line | Management | Plan, monitor, control resource allocation to achieve strategic goals |
| Operating Core | Core | Direct value creation; products / services to external customers |
| Support Staff | Support | Internal-to-enterprise services that keep the organization running |
| Technostructure | Standardization | Cross-cutting overlay for compliance, consistency, continuous improvement, quality |

### 2.2 Four distinct process axes

CR-BP-03 introduces a **4-axis classification** that separates four
distinct concerns. Each axis answers a different question; conflating
them is the historical source of much process-catalog confusion.

| Axis | Field | Vocabulary | Question it answers |
|---|---|---|---|
| **Intent** | `process_intent` (existing; preserved) | operational / support / management | **What is the process doing?** Describes the nature of the work. |
| **Type** | `process_type` (new; CR-BP-03) | strategic / management / core / support / standardization | **Where does the process sit in the enterprise process landscape?** The 5-component classification (Mintzberg). |
| **Specialization** | `process_specialization` (new; CR-BP-03) | list of parent process ids | **What is this process a specialization of?** Inheritance / pattern-based refinement (e.g. `Manage Customer` → `Manage Enterprise Customer`, `Manage VIO Customer`, `Manage Retail Customer`, `Manage Shop Customer`). |
| **Audience** | `process_audience` (existing; preserved; confirmed to be the ECF domain) | governance-existence / strategy-direction / agency-organization / party-relationship / product-value / enablement-operations / finance-accounting | **Which ECF domain does the process serve?** |

The four axes are **additive** and **optional individually**; entries
can declare any subset. Defaults: `process_type` defaults to `core`
when the entry is a Business Process; other axes default to
unspecified.

### 2.3 The five categories are a classification, not ontology

CR-BP-03 explicitly prevents this:

```text
dea:BusinessProcess
dea:StrategicProcess
dea:ManagementProcess
dea:TechnostructureProcess
dea:SupportProcess
```

as five competing foundational entities. **None of these are added.**

Instead:

```text
dea:BusinessProcess  (the L2 semantic entity; canonical)
   ↓ classified by
process_type: strategic | management | core | support | standardization
```

The classification is a **catalog-controlled vocabulary** at
`classifications/process-types.yaml`. The semantic entity remains
`dea:BusinessProcess` regardless of `process_type`.

This keeps the catalog extensible without polluting the OpenDEA
metamodel.

---

## 3. Business Process definition (refined)

> A Business Process is a structured set of enterprise activities
> that collectively produces a defined business outcome and realizes
> one or more business capabilities, with primary responsibility for
> direct value delivery residing in the Operating Core.

This definition deliberately preserves the current normative OpenDEA
definition while adding the architectural context required by this
repository. The 4-axis classification is **added alongside** the
canonical definition; it does not redefine it.

---

## 4. Process Architecture (L0/L1/L2 — conceptual only)

CR-BP-03 establishes the following decomposition as a **conceptual
hierarchy**. The L0 / L1 / L2 levels are not separate top-level
directories; they are levels of abstraction documented here and in
`docs/architecture.md` + `README.md`.

```text
ECF Domain × Lifecycle Stage     (ECF coordinate; CR-BP-02)
         │
         ▼
   Process Context               (CR-BP-02; contexts/v1/)
         │   conceptual L0 (Process Scope)
         ▼
   Process Group                 (conceptual L1; documented; not
         │       a separate directory in this CR)
         ▼
   Business Process              (L2; entities/v1/; the canonical
         │       semantic level; dea:BusinessProcess)
         ▼
   Activity                      (CR-BP-04; future)
         │
         ▼
   Workflow / Task               (CR-BP-05; future; authoritative
                                 metamodel)
```

**L0 Process Scope** is the highest process-architecture scope
beneath Process Context. It establishes the bounded area of process
coverage. It is a **catalog topology construct**, not a new
normative metamodel entity.

**L1 Process Group** is a coherent grouping of Business Processes
within a Process Scope. It is a **catalog topology construct**.
Critically: Process Group is **not** equivalent to Business
Function. A Business Function is an OpenDEA semantic concept
concerned with organizational grouping of capabilities and
ownership. Process Group is concerned with organizing processes.

**L2 Business Process** is the canonical semantic level:
`dea:BusinessProcess`. All L2 process definitions must conform to
the authoritative OpenDEA metamodel.

---

## 5. Structural decomposition

The repository shall use the existing normative relationship
`dea:composes` for process decomposition:

```text
L1 Process Group
       │
       ▼
L2 Business Process
       │
       └── dea:composes ──► L2 Business Process
```

**Local `parent_process` / `child_processes` fields are preserved
but marked as migration aliases** in the schema. They may exist
temporarily on legacy entries but shall not remain authoritative.
New entries should declare `relationships.composes:` in canonical
OpenDEA form. A follow-on migration validator (CR-BP-03A) will
surface entries that have only the old fields.

Structural composition means:

- part-of structure;
- containment within the process architecture;
- hierarchical decomposition;
- no implied sequence;
- no implied execution;
- no implied organizational ownership.

---

## 6. Process realization

Decomposition and realization remain orthogonal:

```text
              ┌───────────────┐
              │ Business      │
              │ Capability    │
              └───────▲───────┘
                      │
                   realizes
                      │
              ┌───────┴───────┐
              │ Business      │
              │ Process       │
              └───────┬───────┘
                      │
                   composes
                      │
                      ▼
              Business Process
```

**Local `capabilities_delivered` field is preserved but marked as a
migration alias.** New entries should declare
`relationships.realizes:` in canonical OpenDEA form.

---

## 7. Process specialization model (refined)

CR-BP-03 introduces the following controlled classification
(`classifications/process-types.yaml`):

```yaml
process_types:
  - id: strategic
    name: Strategic Process
    primary_organizational_component: Strategic Apex
    primary_purpose: ...
  - id: management
    name: Management Process
    primary_organizational_component: Middle Line
    primary_purpose: ...
  - id: core
    name: Core Process
    primary_organizational_component: Operating Core
    primary_purpose: ...
  - id: support
    name: Support Process
    primary_organizational_component: Support Staff
    primary_purpose: ...
  - id: standardization
    name: Standardization Process
    primary_organizational_component: Technostructure
    primary_purpose: ...
```

This is a **primary association**, not an exclusivity constraint. A
`support` process can contribute to a `core` process. An employee
belonging to Support Staff can participate in an operational Core
Process. Thus: **Organizational Component identifies the principal
organizational locus; Process Type identifies the principal character
of the work.**

### 7.1 Process specialization (inheritance / pattern refinement)

In addition to `process_type`, CR-BP-03 introduces
`process_specialization` — the **inheritance / pattern-based
refinement** axis:

```yaml
- id: dea:bp-manage-customer
  process_type: management
  # ...

- id: dea:bp-manage-enterprise-customer
  process_type: management
  process_specialization:
    - dea:bp-manage-customer
  specialization_pattern: by-customer-segment
  # ...

- id: dea:bp-manage-vip-customer
  process_type: management
  process_specialization:
    - dea:bp-manage-customer
  specialization_pattern: by-customer-segment
  # ...
```

`process_specialization` is a list of parent process ids (multi-
inheritance is permitted). `specialization_pattern` is an optional
free-text label (e.g. "by-customer-segment", "by-region",
"by-product-line") for analytics.

This is **not** a new metamodel relationship; it is a
**catalog-level annotation** that records the specialization
hierarchy for navigation and governance. The authoritative
`dea:specializes` relationship in the metamodel continues to govern
the kernel + specialization discipline (CR-MM-PROC-01).

---

## 8. Process identity: testing process-ness by description, not name

CR-BP-03 introduces a **process identity sub-block** that tests a
process by name + description + trigger + outcome + evidence, not
by name alone. This addresses a real risk: a process may be
poorly named but correctly described; or correctly named but
mis-classified. The identity contract requires both.

### 8.1 Identity sub-block shape

```yaml
identity:
  verb: Manage           # action verb (imperative; singular)
  object: Customer       # the noun being acted on
  scope: <optional>      # optional scope qualifier
  outcome_statement: |
    Customer relationships are maintained, escalated where
    required, and renewed or terminated per policy.
  evidence_links:
    - type: documentation
      ref: docs/processes/manage-customer.md
    - type: governance
      ref: governance/process-manage-customer.md
```

The verb + object together approximate the process name; the
outcome_statement is the description-of-record. Evidence links
provide the basis for review when the name or description is
challenged.

---

## 9. Re-landscape: contribution-driven (NOT in-tree)

CR-BP-03 introduces a **contribution-driven re-landscape
mechanism**. A new process is **not** added directly to
`entities/v1/`; instead, the contributor submits a
**Process Contribution** to `contributions/processes/`, and the
**CI contribution report workflow** generates a reclassification
recommendation.

### 9.1 Why contribution-driven?

- **Human-in-the-loop**: a process that is poorly named or
  described should be reviewed by a human before it lands in the
  catalog.
- **Evidence-based**: the contribution template captures the
  current classification, the evidence, and the contributor's
  reasoning; the report is generated against that evidence.
- **CI-piped**: the report runs in CI; it's deterministic,
  reproducible, and reviewable as a PR artifact.

### 9.2 Process Contribution Template

Located at `contributions/processes/PROCESS-CONTRIBUTION-TEMPLATE.yaml`:

```yaml
# Process Contribution
# Submit via PR to contributions/processes/; the CI report
# workflow emits a reclassification recommendation.

schema: dea-catalog-processes/contribution/v1
contributor: <github-handle>
contribution_date: <YYYY-MM-DD>

# === Process to add / re-classify ===
proposed_entry:
  id: dea:bp:...                  # proposed canonical id
  name: ...                       # proposed name
  description: ...                # proposed description
  process_intent: ...             # operational | support | management
  process_type: ...               # strategic | management | core | support | standardization
  process_audience: ...           # ecf-domain
  process_specialization:         # optional inheritance
    - dea:bp:...
  specialization_pattern: ...     # optional free-text
  identity:                       # process identity sub-block
    verb: ...
    object: ...
    outcome_statement: ...
    evidence_links: [...]

# === Evidence ===
evidence:
  - type: documentation
    ref: <link>
  - type: governance
    ref: <link>
  - type: interview
    ref: <interviewee + date>
  - type: artifact
    ref: <system / process-mining output>

# === Reviewer assignment ===
reviewer: <github-handle>     # unassigned → catalog maintainers
status: pending               # pending | accepted | rejected | re-landscaped

# === Re-landscape report (filled by CI) ===
report:
  generated_at: <YYYY-MM-DDTHH:MM:SSZ>
  report_path: <path to report artifact>
  recommendation: accept | re-classify | reject
  current_state: {...}        # captured by CI from the contribution
  suggested_state: {...}      # CI-suggested reclassification
  confidence: <0.0-1.0>
  rationale: ...
```

### 9.3 CI Contribution Report Workflow

A new workflow at `.github/workflows/process-contribution-report.yml`
runs on PRs that touch `contributions/processes/`:

1. Detects new / modified contributions.
2. Validates the contribution against the template.
3. Runs the identity checker (`scripts/check_process_identity.py` —
   see §10) on the proposed_entry.
4. Runs the classification checker (cross-checks process_type +
   process_intent against description + outcome_statement).
5. Emits a **report artifact** at `contributions/processes/<id>.report.md`
   containing:
   - Current state (extracted from the contribution);
   - Suggested state (CI-recommended reclassification);
   - Confidence score;
   - Rationale (which signals triggered the recommendation);
   - Evidence summary;
   - Reviewer next-steps.
6. Posts the report as a PR comment.
7. The PR is **not auto-merged**; the reviewer (catalog maintainer)
   decides.

### 9.4 Re-landscape lifecycle

```text
contribution submitted
   │  (PR to contributions/processes/<id>.yaml)
   ▼
CI report generated
   │  (artifact + PR comment)
   ▼
Reviewer reviews
   │
   ├── accept  → land in entities/v1/<id>.yaml
   │
   ├── re-classify → contributor updates proposed_entry
   │                and re-runs CI
   │
   └── reject → PR closed; contribution archived
```

This is consistent with the user's direction: "re-landscaping should
be traced with surface classification triggered based on
contribution of a new process using a process contribution template
that must be submitted into a contribution space, and then a report
is delivered that is piped through the CI."

---

## 10. Structural vs behavioural process modeling

```text
Structural architecture    Behaviour / execution
─────────────────────      ───────────────────
Context                   Business Process
   ↓                           ↓
Scope                       Activity
   ↓                           ↓
Group                       Workflow
   ↓                           ↓
Business Process             Task
```

Workflow and Task already exist in the OpenDEA metamodel and should
not be reinvented by the process catalog.

- **CR-BP-03** → structural process architecture
- **CR-BP-04** → Activity Model
- **CR-BP-05** → Execution Boundary

---

## 11. Schema direction (additive; preserving existing fields)

### 11.1 `entity.schema.json` (L2 Business Process) — updated

```yaml
id: dea:bp:...              # existing
name: ...                   # existing
type: BusinessProcess       # existing
version: ...                # existing
description: ...            # existing
process_intent: ...         # existing; preserved
process_audience: ...       # existing; preserved
parent_process: ...         # existing; preserved; migration alias
child_processes: [...]      # existing; preserved; migration alias
capabilities_delivered: [...]# existing; preserved; migration alias
relationships:              # NEW; canonical OpenDEA form
  composes:
    - dea:bp:...
  realizes:
    - dea:capability:...
process_type: core          # NEW; default "core"
process_specialization:     # NEW; list of parent process ids
  - dea:bp:...
specialization_pattern: ... # NEW; optional free-text
identity:                   # NEW; the process-identity sub-block
  verb: ...
  object: ...
  scope: ...
  outcome_statement: ...
  evidence_links: [...]
```

**All existing fields are preserved.** New fields have defaults so
existing entries continue to validate.

### 11.2 `identity.schema.json` — new

The process-identity sub-block schema. Required when `identity` is
declared. Mirrors §8.1.

---

## 12. Repository changes (additive; one PR)

### 12.1 New top-level structure

```text
dea-catalog-processes/
│
├── README.md                          (rewritten; architectural statement)
├── CHANGELOG.md                       (CR-BP-03 entry)
├── LICENSE
│
├── change-requests/
│   ├── CR-BP-01-process-semantic-baseline.md
│   ├── CR-BP-02-process-context.md
│   └── CR-BP-03-business-process-architecture.md  ← new
│
├── metamodel-pointer.yaml             (unchanged)
│
├── contexts/                          (existing; CR-BP-02)
│   └── v1-alpha/
│
├── entities/                          (existing; canonical L2 path)
│   └── v1-alpha/                      (unchanged in this CR)
│
├── classifications/                   (new; CR-BP-03)
│   ├── process-types.yaml             (5-value vocabulary)
│   └── process-specializations.yaml   (catalog-level specialization
│                                       vocabulary)
│
├── contributions/                     (new; CR-BP-03 §9; the
│   └── processes/                     contribution space)
│       ├── PROCESS-CONTRIBUTION-TEMPLATE.yaml
│       └── README.md
│
├── schemas/                           (existing + new)
│   ├── entity.schema.json             (updated; additive new fields)
│   ├── entities/
│   │   └── process-context.schema.json
│   ├── identity.schema.json           (new; the identity sub-block)
│   └── contribution.schema.json       (new; the contribution template)
│
├── scripts/                           (existing + new)
│   ├── check_process_specialization.py
│   ├── check_process_context.py
│   ├── check_process_identity.py      (new; BP-ARC-ID-001..005)
│   └── check_ecf_conformance.py
│
├── validation/                        (new; forward-looking
│   └── conformance/                   alias; subdirs added in
│       └── README.md                  CR-BP-03A+)
│
└── docs/                              (new; CR-BP-03 narrative)
    ├── architecture.md
    ├── classification.md
    ├── identity.md
    ├── relandscape.md
    └── conformance.md
```

### 12.2 Migration notes

- `entities/v1-alpha/` continues to be the canonical L2 path.
- `scripts/` continues to be the canonical path for validator
  scripts.
- `validation/conformance/` is a forward-looking alias (README only
  in this CR).
- `contexts/v1/` and `processes/v1/` (L0/L1) are **not** created as
  separate top-level directories; the L0/L1 hierarchy is conceptual
  (§4; documented in README + docs/architecture.md).
- All existing fields are preserved; no breaking changes.

---

## 13. Acceptance criteria

### Architecture

- [x] Process Context → L0 → L1 → L2 is explicitly documented
  (`docs/architecture.md`).
- [x] L2 is explicitly `dea:BusinessProcess` (`README.md`).
- [x] L0 and L1 are documented as conceptual constructs (not
  separate top-level directories).
- [x] Process Group is explicitly distinguished from Business
  Function (`README.md`; `docs/architecture.md`).

### Classification

- [x] Core Process is defined as the Operating Core
  classification (`classifications/process-types.yaml`).
- [x] Strategic / Management / Standardization / Support
  associations all documented.
- [x] Classification does not create competing normative entities
  (no new `dea:entity-*-process` in the root model).
- [x] **Four distinct axes (intent / type / specialization /
  audience) operate independently**.

### Semantics

- [x] `dea:composes` is the canonical decomposition relationship
  (`relationships.composes`; old `parent_process` /
  `child_processes` marked as migration aliases).
- [x] `dea:realizes` is the capability realization relationship
  (`relationships.realizes`; old `capabilities_delivered` marked as
  a migration alias).
- [x] Structural decomposition does not imply sequence
  (documented).

### Identity contract

- [x] A process is tested by name + description + trigger +
  outcome + evidence, not by name alone
  (`schemas/identity.schema.json`;
  `scripts/check_process_identity.py`; BP-ARC-ID-001..005).
- [x] **Re-landscape is contribution-driven** (a new process
  contribution is submitted to `contributions/processes/`, a report
  is generated, the report is piped through CI)
  (`contributions/processes/PROCESS-CONTRIBUTION-TEMPLATE.yaml`;
  `schemas/contribution.schema.json`;
  `.github/workflows/process-contribution-report.yml`;
  `docs/relandscape.md`).

### Repository

- [x] Repository structure reflects the L2 path
  (`entities/v1-alpha/`; canonical).
- [x] Classification vocabulary is explicitly represented
  (`classifications/process-types.yaml`).
- [x] Schemas conform to the canonical metamodel
  (`schemas/entity.schema.json`; `schemas/identity.schema.json`;
  `schemas/contribution.schema.json`).
- [x] Validation detects invalid classification
  (`scripts/check_process_identity.py`).
- [x] README completely reflects the architecture (rewritten).
- [x] CR-BP-01, CR-BP-SPEC-BP-01, and CR-BP-02 are referenced as
  preceding architectural decisions.

### Migration

- [x] **No breaking changes**; existing entries continue to
  validate.
- [x] `process_intent`, `process_audience`, `parent_process`,
  `child_processes`, `capabilities_delivered` are all preserved.
- [x] New fields are added with defaults (`process_type` defaults
  to `core`; `process_specialization` is empty; `identity` is
  optional).

---

## 14. What this changes about the Process programme

The 4-axis classification + identity contract + contribution-driven
re-landscape give us a much stronger foundation:

```text
           ENTERPRISE PROCESS LANDSCAPE (process_type)
                          │
   ┌──────────┬───────────┼───────────┬──────────┐
   ▼          ▼           ▼           ▼          ▼
Strategic  Management   Core       Support   Standardization
   │          │           │           │          │
   ▼          ▼           ▼           ▼          ▼
Strategic   Middle     Operating   Support    Techno-
Apex        Line        Core        Staff    structure

   AND within the Business Process catalog (L2):
   ┌──────────────────────────────────────────────┐
   │ ECF Domain × Lifecycle                        │
   │     │                                         │
   │     ▼                                         │
   │ Process Context                               │
   │     │                                         │
   │     ▼                                         │
   │ L0 Process Scope                              │
   │     │                                         │
   │     ▼                                         │
   │ L1 Process Group                              │
   │     │                                         │
   │     ▼                                         │
   │ L2 Business Process  (dea:BusinessProcess)    │
   │     │                                         │
   │     ├─ intent:  operational|support|management│
   │     ├─ type:    core|... (default core)       │
   │     ├─ specialization: [parent ids]          │
   │     ├─ audience: <ecf-domain>                 │
   │     └─ identity: {verb, object, outcome,     │
   │                   evidence_links}             │
   │                                              │
   │     ▼                                         │
   │   [CR-BP-04] Activity                         │
   │     │                                         │
   │     ▼                                         │
   │   [CR-BP-05] Execution Boundary               │
   └──────────────────────────────────────────────┘

   AND the contribution flow:
   ┌──────────────────────────────────────────────┐
   │ contributions/processes/<id>.yaml             │
   │   ↓ CI report (process-contribution-report)  │
   │ contributions/processes/<id>.report.md        │
   │   ↓ human review                             │
   │ entities/v1-alpha/<id>.yaml  (if accepted)   │
   └──────────────────────────────────────────────┘
```

---

## 15. Honest scoping notes

- **No new OpenDEAM entities.** No `dea:entity-strategic-process`,
  `dea:entity-management-process`, `dea:entity-core-process`,
  `dea:entity-support-process`, `dea:entity-standardization-process`.
- **No breaking changes.** All existing fields preserved.
- **No automatic rewrites.** Re-landscape is contribution-driven,
  CI-piped, human-reviewed.
- **L0/L1 are conceptual, not new top-level directories.** The
  hierarchy is documented in README + docs/architecture.md.
- **Migration aliases** (`parent_process`, `child_processes`,
  `capabilities_delivered`) are preserved and documented.

---

## 16. Follow-on CRs

- **CR-BP-03A**: migrate legacy entries from `parent_process` /
  `child_processes` / `capabilities_delivered` to the canonical
  `relationships.{composes, realizes}` form.
- **CR-BP-04**: Activity Model.
- **CR-BP-05**: Execution Boundary.
- **CR-BP-06..10**: see CR-BP-02 §19.
