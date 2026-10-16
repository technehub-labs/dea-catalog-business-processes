# Re-landscape: Contribution-Driven

**CR-BP-03 §9.**

This document captures the **contribution-driven re-landscape
mechanism**. A new process is not added directly to
`entities/vn/` (where n is a realease number); instead, the contributor
submits a **Process Contribution** to `contributions/processes/`, and the
**CI contribution report workflow** generates a reclassification recommendation.

## Why contribution-driven?

- **Human-in-the-loop**: a process that is poorly named or
  described should be reviewed by a human before it lands in the
  catalog.
- **Evidence-based**: the contribution template captures the
  current classification, the evidence, and the contributor's
  reasoning; the report is generated against that evidence.
- **CI-piped**: the report runs in CI; it's deterministic,
  reproducible, and reviewable as a PR artifact.
- **Auditability**: each contribution + report is a
  first-class catalog artifact, preserved in the contribution
  space.

## The contribution flow

```text
contribution submitted
   │  (PR to contributions/processes/<id>.yaml)
   ▼
CI report generated
   │  (artifact: contributions/processes/<id>.report.md)
   │  (PR comment)
   ▼
Reviewer reviews
   │
   ├── accept  → land in entities/v1-alpha/<id>.yaml
   │
   ├── re-classify → contributor updates proposed_entry
   │                and re-runs CI
   │
   └── reject → PR closed; contribution archived
```

## Process Contribution Template

A Process Contribution is a YAML file at
`contributions/processes/<id>.yaml` conforming to
[`schemas/contribution.schema.json`](../schemas/contribution.schema.json).
The template is at
[`contributions/processes/PROCESS-CONTRIBUTION-TEMPLATE.yaml`](../contributions/processes/PROCESS-CONTRIBUTION-TEMPLATE.yaml).

The contribution captures:

- `contributor`: the contributor's GitHub handle.
- `contribution_date`: the date of contribution.
- `proposed_entry`: the proposed L2 Business Process entry
  (must conform to `schemas/entity.schema.json` +
  `schemas/identity.schema.json`).
- `evidence`: supporting evidence (documentation, governance,
  interview, artifact, standard, regulation).
- `reviewer`: the assigned catalog maintainer.
- `status`: `pending` (initial) → `accepted` /
  `re-landscaped` / `rejected`.
- `report`: filled by the CI workflow (not by the contributor).

### The `relationships` field (CR-BP-03 §6; CR-BP-03A §3.1)

The `proposed_entry.relationships` field is an **array of
relationship instances** (NOT a structured object), conforming
to the metamodel's `relationship-instance.json`. Each entry is a
typed relationship with CR-002 provenance, CR-6 lifecycle, and
effective_from/to temporal validity:

```yaml
relationships:
  - source_id: dea:bp:example-process
    target_id: dea:bp:parent-process
    relationship_type: composes
    status: active
    rationale: "Example process composes the parent process."
    provenance:
      type: manual
      asserted_by: <github-handle>
      asserted_at: <YYYY-MM-DD>
  - source_id: dea:bp:example-process
    target_id: dea:capability:example-capability
    relationship_type: realizes
    status: active
    rationale: "Example process realizes the example capability."
    provenance:
      type: manual
      asserted_by: <github-handle>
      asserted_at: <YYYY-MM-DD>
```

The catalog primarily uses `composes` (structural composition)
and `realizes` (capability realization). Other types
(`specializes`, `aggregates`, `depends-on`, etc.) are admitted
when the contributor can defend the choice.

### The legacy fields (CR-BP-03A)

The legacy `parent_process` / `child_processes` / `capabilities_delivered`
fields are **not part of the contribution schema**. The migration
validator (`scripts/check_legacy_migration.py`; BP-MIG-001..005)
surfaces any entry that declares them with a migration
recommendation. See [`docs/architecture.md`](architecture.md) §6
for the migration discipline.

## CI Contribution Report Workflow

The workflow at
`.github/workflows/process-contribution-report.yml` runs on PRs
that touch `contributions/processes/`:

1. **Detects** new / modified contributions.
2. **Validates** the contribution against the contribution
   schema.
3. **Runs the identity checker**
   (`scripts/check_process_identity.py`) on the proposed_entry.
4. **Cross-checks** the proposed classification
   (`process_type` + `process_intent`) against the
   `outcome_statement` and `evidence_links`.
5. **Emits a report** at
   `contributions/processes/<id>.report.md` containing:
   - Current state (extracted from the contribution);
   - Suggested state (CI-recommended reclassification, if any);
   - Confidence score;
   - Rationale (which signals triggered the recommendation);
   - Evidence summary;
   - Reviewer next-steps.
6. **Posts the report** as a PR comment.
7. The PR is **not auto-merged**; the reviewer (catalog
   maintainer) decides.

## Re-landscape suggestions

The contribution report can emit a **re-landscape suggestion**
with a confidence score when:

- The `process_type` is inconsistent with the `outcome_statement`
  (e.g. `core` but the outcome talks about direction-setting).
- The `process_intent` is inconsistent with the `outcome_statement`.
- The name does not match the `identity.verb` + `identity.object`.
- The trigger or outcome is missing.
- The evidence_links are missing or insufficient.

The suggestion is **not** an automatic rewrite; it requires
human review (the `reviewer` field). The catalog does not
auto-reclassify.

## Re-landscape lifecycle

| State | Description |
|---|---|
| `pending` | Contribution submitted; awaiting CI report. |
| `reported` | CI report generated; awaiting reviewer. |
| `accepted` | Reviewer accepts the contribution as-is; entry lands in `entities/v1-alpha/`. |
| `re-landscaped` | Reviewer requests re-landscape; contributor updates the proposed_entry and re-runs CI. |
| `rejected` | Reviewer rejects the contribution; PR closed; the contribution is archived. |

## Worked example: re-landscape suggestion

A contributor submits a Process Contribution for a new process:

```yaml
proposed_entry:
  id: dea:bp-set-strategic-direction
  name: Set Strategic Direction
  process_intent: management
  process_type: core              # WRONG: should be 'strategic'
  process_audience: governance-existence
  description: |
    Set the strategic direction and goals for the enterprise.
  identity:
    verb: Set
    object: Strategic Direction
    outcome_statement: |
      The strategic direction and goals of the enterprise are
      established; the portfolio is governed accordingly.
    evidence_links:
      - type: governance
        ref: governance/strategic-direction.md
```

The CI contribution report detects that `process_type: core` is
inconsistent with the `outcome_statement` (which talks about
"strategic direction" and "portfolio governance": keywords
associated with `strategic`). The report emits:

```markdown
# Contribution Report: dea:bp-set-strategic-direction

## Recommendation
**re-classify** (confidence: 0.85)

## Current state
- process_type: core
- process_intent: management
- name: Set Strategic Direction
- outcome_statement: "The strategic direction and goals of the
  enterprise are established; the portfolio is governed
  accordingly."

## Suggested state
- process_type: strategic
- process_intent: management

## Rationale
- outcome_statement contains keywords ["strategic", "direction",
  "goals", "portfolio", "governance"], all of which are
  associated with process_type: strategic.
- name contains "Strategic", consistent with process_type:
  strategic.
- The Operating Core (process_type: core) produces value; the
  Strategic Apex (process_type: strategic) sets direction. The
  outcome_statement is direction-setting, not value-producing.

## Evidence summary
- governance/strategic-direction.md is the authoritative
  reference; the outcome_statement aligns with this document.

## Reviewer next-steps
- Update process_type from `core` to `strategic` in the
  proposed_entry.
- Re-push; the CI report will re-run.
```

The contributor updates the contribution, re-pushes, and the CI
report re-runs. Once the report recommends `accept`, the
reviewer approves and the entry lands.

## See also

- [`docs/identity.md`](identity.md): the identity contract
- [`docs/semantic-contract.md`](semantic-contract.md): the CR-BP-14
  semantic constitution (dimensions, separations)
- [`contributions/processes/PROCESS-CONTRIBUTION-TEMPLATE.yaml`](../contributions/processes/PROCESS-CONTRIBUTION-TEMPLATE.yaml)
- [`schemas/contribution.schema.json`](../schemas/contribution.schema.json)
- [`scripts/check_process_identity.py`](../scripts/check_process_identity.py)
- [`scripts/check_process_semantics.py`](../scripts/check_process_semantics.py):
  the CR-BP-14 §21 validator; future contributions must satisfy
  BP-SEM-001..012 before admission is considered final
- [`change-requests/CR-BP-03-business-process-architecture.md`](../change-requests/CR-BP-03-business-process-architecture.md) §9
- [`change-requests/CR-BP-14-process-semantic-reconciliation.md`](../change-requests/CR-BP-14-process-semantic-reconciliation.md) §24
