# Decomposition Template Guide

**Source of truth:** CR-BP-94 (Decomposition Record Templates); recon-programme slice CR-BP-92 §9 + §15.
**Authoritative contract:** [`docs/decomposition-semantic-contract.md`](decomposition-semantic-contract.md) (CR-BP-93).
**Where templates live:** `templates/process-scope.yaml`, `templates/process-group.yaml`, `templates/business-process.yaml`, `templates/activity.yaml`, `templates/task.yaml`.

## Purpose

This guide is the **human-oriented authoring companion** to the five decomposition record templates. Each template encodes both:

1. **machine-oriented schema structure**: the YAML skeleton the catalog's validators and JSON-Schema files enforce; and
2. **human-oriented authoring guidance**: inline comments at every required-field site, plus this guide's prose.

The goal (per CR-BP-92 §15) is to **make it difficult to create a superficially complete element whose semantic definition is inadequate**. Templates must force the author to write substantive prose at every required-field site, not just fill in boilerplate.

## How to use these templates

1. **Pick the layer** you are authoring (L0, L1, L2, L3, L4).
2. **Copy the matching template** to the canonical path:
   - L0: `entities/v1-alpha/dea:scope-<kebab-name>/dea:scope-<kebab-name>.yaml`
   - L1: `entities/v1-alpha/dea:group-<kebab-name>/dea:group-<kebab-name>.yaml`
   - L2: `entities/v1-alpha/dea:process-<kebab-name>/dea:process-<kebab-name>.yaml`
   - L3: `entities/v1-alpha/dea:activity-<kebab-name>/dea:activity-<kebab-name>.yaml`
   - L4: `entities/v1-alpha/dea:task-<kebab-name>/dea:task-<kebab-name>.yaml`
3. **Replace every `<...>` placeholder** with the actual value.
4. **Run the relevant gate(s)** before committing:
   - L0: `python scripts/check_process_scope.py`
   - L1: `python scripts/check_process_group.py`
   - L2: `python scripts/check_l2_qualification.py --strict && python scripts/check_process_semantics.py --strict`
   - L3: `python scripts/check_activity_model.py --strict && python scripts/check_execution_boundary.py --strict`
   - L4: no gate today (CR-BP-98 will establish); CI conformance_result still applies
5. **Run the full conformance pipeline**: `python scripts/conformance_result.py`

## Layer-by-layer authoring guidance

### L0 Process Scope

L0 is a **non-executable architectural boundary**. It has no inputs, outputs, transformation, outcome, or trigger. The `definition` field is the L0 layer's prose contract; PSCOPE-006 (MECE) depends on it being non-overlapping with peer Process Scopes in the same Process Context. The `decomposition_basis.statement` field (1-1000 chars) forces the author to write substantive prose about the architectural basis on which the Scope decomposes its parent Process Context.

**Common authoring mistakes (CR-BP-93 §3 disallowed):**
- Treating L0 as a Business Process or Activity. L0 does NOT perform work.
- Auto-deriving an L0 from an ECF coordinate. ECF coordinates do NOT automatically constitute Process Scopes (CR-BP-93 §3).
- Including inputs, outputs, or a trigger on an L0 record. These are disallowed.

### L1 Process Group

L1 is the canonical entity that organizes related Business Processes within an L0 Process Scope. L1 has a controlled-vocabulary `process_group_kind` (PG-007) and: under CR-BP-95: an OPTIONAL `grouping_basis` block (PG-009) and OPTIONAL `membership_criteria` block (PG-010). New L1 records are strongly encouraged to populate the OPTIONAL fields; existing 48 records remain conformant without them (back-compat).

**Common authoring mistakes (CR-BP-93 §4 disallowed):**
- Treating L1 as a Business Function, organizational unit, or Capability.
- Using L1 as a proxy for organizational ownership.
- Missing `scope.includes` or `scope.excludes` (PG-002 requires both).

### L2 Business Process

L2 is the centerpiece: an independently meaningful, bounded enterprise transformation. The `identity:` block encodes the BP-C1..C4 + BP-SEM-001..014 contract:

- `identity.verb` + `identity.object`: the verb-object form (e.g. "Frame Strategic Horizons").
- `identity.scope`: the qualifier.
- `identity.outcome_statement`: the testable outcome (BP-C2).
- `identity.evidence_links`: at least one (BP-C4).

The `trigger` and `outcome` top-level fields together encode the input/output transformation (BP-C1).

**Common authoring mistakes (CR-BP-93 §5 disallowed):**
- Naming a BP with a gerund or system-function form ("Performing", "Generating", "Processing"). Use the verb-object pattern: `Frame Strategic Horizons`, `Address Performance Exceptions`, `Bring Policy Instrument into Force`.
- Treating a BP as an Activity, Task, or workflow step. The L2 layer is the independently meaningful transformation.
- Missing `ecfConformance.canonicalReferences` (BP-AR-001..007 requires exactly one canonical coordinate per record).

### L3 Activity

L3 is a cohesive body of work within an L2 Business Process. Every Activity must:

1. Belong to exactly one parent BP (`belongs_to_business_process`: ACT-001).
2. Have a substantive `definition` (ACT-003) and `cohesion_rationale` (ACT-003 + CR-BP-32 §6).
3. Carry `decomposition_boundary: l4-reached` until L4 Task records exist (ACT-004 + CR-BP-32 §12). Once Tasks land, REPLACE the marker with `composes:` entries.
4. Inherit the parent BP's `ecfConformance.canonicalReferences` coordinate.

**Common authoring mistakes (CR-BP-93 §6 disallowed):**
- Naming an Activity with a system-function, organizational-role, or workflow-step form ("Generate Report", "Email Customer", "Wait for Approval"). Use the cohesive-work verb-object pattern.
- Treating an Activity as an independently qualified Business Process. ACT-002 enforces: every Activity must FAIL the L2 qualification criteria (Standalone Executability; Resource Dedication).
- Adding execution-ordering fields to an Activity (ACT-006). Sequencing lives in Workflow Definition.

### L4 Task

L4 is the lowest semantic decomposition level (CR-BP-32 §12; CR-BP-93 §7). Tasks are bounded, actionable, single-responsibility, and independently verifiable for completion. **No L4 schema or gate exists today**; CR-BP-98 (Task Boundary and Workflow Realization) will establish them. The `templates/task.yaml` template is the first normative description of the L4 record shape.

**What L4 does NOT carry (CR-BP-93 §7 disallowed):**

- Sequencing (Task A -> Task B -> Task C): that lives in Workflow Definition.
- Branching / conditions / dependencies / orchestration.
- Workflow Instance semantics or execution events.

**Common authoring mistakes (CR-BP-93 §7 disallowed):**
- Treating a Task as a workflow step, software operation, work instruction, or implementation detail.
- Adding sequence / ordering fields to a Task.
- Treating a Task as a Workflow Instance or Execution event.

## Cross-cutting authoring rules

### Em-dash / en-dash rule

The repository's GitHub language rule (memory directive) forbids U+2013 (en-dash) and U+2014 (em-dash) in any artifact shipped to GitHub. When authoring prose in templates, use:

- Parenthetical: `X: Y` -> colon: `X: Y`.
- Tight compound: `X-Y` -> hyphen.
- Multi-dash sentence -> split into short clear sentences.

This applies to template files, README.md, change-requests, docs/, and any other file.

### CR-META gate

Every `change-requests/CR-*.md` file is scanned by `scripts/check_cr_metadata.py` (CR-META-001..006). The required header fields are:

- `**Status**`: column-0 `**Field**: value` (no leading markdown bullet).
- `**Layer**`: one of `L0, L1, L2, L3, Process Catalog, Metamodel, Cross-cutting`. Qualifiers in parentheses only (e.g. `L3 (Activity Admitted-Activate-BP Decomposition Tranche)`).
- `**Owner**`: free text.
- `**Date**`: `YYYY-MM-DD`.

### Reconnaissance-only slices

A Reconnaissance slice (e.g. CR-BP-92) is a Process Catalog-layer CR with prose-only changes. Reconnaissance CRs do not mutate schemas, validators, tests, templates, or canonical records. The Recon's purpose is to establish the architectural basis and implementation pipeline for downstream slices.

### Backwards-compatibility rule for new template fields

When a downstream slice (e.g. CR-BP-95 for PG-009/010) adds a new OPTIONAL field to a schema, the existing canonical records remain conformant without that field. Backfill of OPTIONAL fields across the existing record population is the work of a separate reconciliation slice (CR-BP-99 or a dedicated enrichment tranche), NOT of the schema-extension slice.

## Validation flow

After authoring a record:

```bash
# Per-layer gate (where applicable)
python scripts/check_process_scope.py
python scripts/check_process_group.py
python scripts/check_l2_qualification.py --strict
python scripts/check_activity_model.py --strict
python scripts/check_execution_boundary.py --strict

# Full pipeline
python scripts/conformance_result.py

# Targeted pytest
python -m pytest tests/test_check_<gate>.py -q

# Dash audit (en-dash / em-dash sweep)
python -c "
import re
for f in ['<your-new-file>']:
    with open(f, encoding='utf-8') as fp:
        text = fp.read()
    bad = sum(1 for c in text if c in '\u2013\u2014')
    print(f'{f}: {bad} em/en-dash characters')
"
```

If any gate emits findings, fix them before committing. If `conformance_result.py` reports `NON-CONFORMANT`, the change is blocked at PR time by the conformance CI step.

## See also

* [`docs/decomposition-semantic-contract.md`](decomposition-semantic-contract.md): the normative decomposition-half contract (CR-BP-93).
* [`docs/semantic-contract.md`](semantic-contract.md): the characterization-half contract (CR-BP-14).
* [`docs/architecture.md`](architecture.md): the reader-facing decomposition overview.
* [`docs/identity.md`](identity.md): the process-identity contract.
* [`docs/classification.md`](classification.md): the Intent / Classification reconciliation.
* [`change-requests/CR-BP-92-recon-decomposition-and-execution-boundary-hardening.md`](../change-requests/CR-BP-92-recon-decomposition-and-execution-boundary-hardening.md): the recon programme that establishes this template family.
* [`change-requests/CR-BP-93-decomposition-semantic-contract.md`](../change-requests/CR-BP-93-decomposition-semantic-contract.md): the carrier CR for the decomposition contract.
* [`change-requests/CR-BP-94-decomposition-record-templates.md`](../change-requests/CR-BP-94-decomposition-record-templates.md): the carrier CR for this template family.
* [`change-requests/CR-BP-95-l0-l1-conformance-gate.md`](../change-requests/CR-BP-95-l0-l1-conformance-gate.md): the L0/L1 conformance gate.
