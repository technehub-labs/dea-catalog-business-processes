# Business Rules, Controls and Exception Semantics (CR-BP-94-EXT-14)

**Status**: Normative (proposed for adoption under CR-BP-94-EXT-14)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-19
**Source CR**: CR-BP-94-EXT-14 (Business Rules, Controls and Exception Semantics)
**Parent programme**: DEA-PROCESS-ENRICH-000 (charter at `docs/operational-documentation-programme/DEA-PROCESS-ENRICH-000-programme-charter.md`)
**Predecessors**: CR-BP-94-EXT-10 (PR #179, merged), CR-BP-94-EXT-11 (PR #180, merged), CR-BP-94-EXT-12 (PR #181, merged), CR-BP-94-EXT-13 (PR #182, merged)
**Tranche gate**: G5_governance (closes by this slice; the **final** tranche gate of the semantic-model tranche)
**Repository**: technehub-labs/dea-catalog-business-processes
**Path**: `change-requests/CR-BP-94-EXT-14-business-rules-controls-and-exception-semantics.md`

---

## 1. Purpose

This document is the **EXT-14 schema extension and semantic contract** for business rules, controls, exceptions, and deviations at L2/L3/L4. It implements the EXT-10 inventory's routed-gap table (EXT-14 owns: business_rule, control, exception) and the EXT-14 CR's design.

It introduces the new optional L2 top-level fields `business_rules[]`, `controls[]`, `exceptions[]`, and `deviations[]` (the EXT-14 routed-gap closures). The CR-BP-94 trigger, outcome, identity, inputs, transformation, outputs, responsibility, boundary, and the EXT-12/EXT-13 fields are **preserved**; the EXT-14 work is additive.

EXT-14 is the **final tranche gate** (G5) of the 5-gate semantic-model tranche. The other four (G1_schema, G2_profiles, G3_interfaces, G4_accountability) were closed by EXT-10/11/12/13.

---

## 2. Conceptual model

EXT-14 distinguishes five concepts that are routinely conflated:

| Concept | Definition | Cardinality |
|---|---|---|
| **Business rule** | The assertion of how the work is governed. The rule defines the constraint. | 1..n per process |
| **Control** | The mechanism that enforces a rule (preventive, detective, corrective) or directs behaviour (directive). | 1..n per rule |
| **Exception** | The predefined handling for a known deviation: detection, classification, response, escalation, resolution. | 0..n per rule |
| **Deviation** | The instance of a rule being broken (tracked over time). | 0..n over time |
| **Rule maturity** | The lifecycle state of a rule: proposed / documented / approved / in_force / monitored / retired. | 1 per rule |

A **rule** is a statement of what must be true. A **control** is a mechanism that ensures the rule is followed (or detects when it is not). An **exception** is the predefined handling when a rule is broken. A **deviation** is the tracked instance of the rule being broken.

---

## 3. The governance relationship

A business process and its rules form a **governance relationship**: the process is the work, the rules are the constraints under which the work is done, the controls are the mechanisms that ensure the constraints are met, the exceptions are the predefined responses when they are not, and the deviations are the tracked instances of the rules being broken.

```
Business Process
  | (governed by)
  v
Business Rule(s)
  | (enforced by)
  v
Control(s)
  | (with predefined response to)
  v
Exception(s)
  | (track instances of)
  v
Deviation(s)
```

A business process MAY exist without rules (the work is informal). When rules are present, controls SHOULD be present for each rule that materially affects outcomes.

---

## 4. Business rules (new L2 top-level field)

EXT-14 introduces the new optional L2 top-level field `business_rules[]` (array of structured entries). Per EXT-14 §4:

```yaml
business_rules:
  - id: <rule-id>
    name: <rule name>
    description: |
      <The rule statement.>
    source: regulatory | contractual | governance | operational | sector
    source_ref: <uri to the rule's authoritative source>
    maturity: proposed | documented | approved | in_force | monitored | retired
    rationale: |
      <Why this rule exists.>
    owner: <role or organisational unit>
```

### 4.1 Rule source (controlled vocabulary)

| Value | Description |
|---|---|
| `regulatory` | Established by a regulator or law |
| `contractual` | Established by a contract with a counterparty |
| `governance` | Established by enterprise governance (board, policy) |
| `operational` | Established by the operating model |
| `sector` | Established by a sector standard (e.g. ISO, NIST) |

### 4.2 Rule maturity (controlled vocabulary)

| Value | Description |
|---|---|
| `proposed` | The rule is proposed but not yet documented |
| `documented` | The rule is documented but not yet approved |
| `approved` | The rule is approved but not yet in force |
| `in_force` | The rule is in force; controls may exist |
| `monitored` | The rule is in force and is being monitored |
| `retired` | The rule is no longer in force; historical record preserved |

A rule in `in_force` or `monitored` state SHOULD have at least one control that enforces it.

### 4.3 Rule vs policy

A **rule** is a specific assertion. A **policy** is a higher-level governance document. A policy may contain many rules. The catalog captures rules, not policies (the policy is the external reference). The `source_ref` field points to the policy or external authority.

---

## 5. Controls (new L2 top-level field)

EXT-14 introduces the new optional L2 top-level field `controls[]` (array of structured entries). Per EXT-14 §5:

```yaml
controls:
  - id: <control-id>
    name: <control name>
    description: |
      <What this control does.>
    type: preventive | detective | corrective | directive
    enforces: <rule-id or rule statement>
    automation: manual | semi_automated | automated
    frequency: continuous | daily | weekly | monthly | quarterly | annual | on_event
    evidence:
      - <evidence artifact 1>
    owner: <role or organisational unit>
```

### 5.1 Control type (controlled vocabulary; per ISO 27000 / COSO)

| Value | Description |
|---|---|
| `preventive` | Prevents the violation before it occurs (e.g. input validation, segregation of duties) |
| `detective` | Detects the violation after it occurs (e.g. reconciliation, monitoring) |
| `corrective` | Corrects the violation after detection (e.g. reversal, restitution) |
| `directive` | Directs or compels behaviour (e.g. policy, training, reminders) |

A control of type `detective` or `corrective` SHOULD have an associated `exceptions[]` entry that defines the predefined response.

### 5.2 Control automation (controlled vocabulary)

| Value | Description |
|---|---|
| `manual` | Performed by a human |
| `semi_automated` | Partially automated, partially manual |
| `automated` | Fully automated (system-mediated) |

### 5.3 Control frequency (controlled vocabulary)

| Value | Description |
|---|---|
| `continuous` | Continuous (real-time) |
| `daily` / `weekly` / `monthly` / `quarterly` / `annual` | Scheduled |
| `on_event` | Triggered by an event |
| `on_request` | Triggered by a request |

### 5.4 Control evidence

The `evidence[]` field captures the artifacts produced by the control (e.g. the reconciliation report, the audit log, the daily review). Evidence is the input to deviation detection. A control that produces no evidence cannot be monitored.

### 5.5 Control vs rule

A **control** enforces a **rule**. One rule may be enforced by multiple controls (preventive + detective + corrective). The catalog MAY express the same rule's multiple controls as multiple entries in `controls[]`, each with the same `enforces` reference.

---

## 6. Exceptions (new L2 top-level field)

EXT-14 introduces the new optional L2 top-level field `exceptions[]` (array of structured entries). Per EXT-14 §6:

```yaml
exceptions:
  - id: <exception-id>
    name: <exception name>
    description: |
      <What the exception covers.>
    classification: recoverable | non_recoverable | business | technical
    detection: continuous | daily | weekly | monthly | quarterly | annual | on_event | on_request
    response: |
      <The response procedure.>
    escalation: |
      <The escalation path.>
    resolution: |
      <The resolution procedure.>
    owner: <role or organisational unit>
```

### 6.1 Exception classification (controlled vocabulary)

| Value | Description |
|---|---|
| `recoverable` | The deviation can be recovered (the process can be brought back to the rule) |
| `non_recoverable` | The deviation cannot be recovered (the rule has been broken irreversibly) |
| `business` | The exception is a business-level deviation (e.g. policy override, customer accommodation) |
| `technical` | The exception is a technical deviation (e.g. system unavailability, data quality issue) |

The classification informs the response: a `recoverable` exception should be recovered; a `non_recoverable` exception should be remediated (the consequences addressed even if the breach itself cannot be undone).

### 6.2 Exception lifecycle

The five-stage exception handling model:

1. **Detection**: the deviation is identified
2. **Classification**: the exception is categorised (recoverable / non-recoverable / business / technical)
3. **Response**: the immediate response is applied (per the response procedure)
4. **Escalation**: the deviation is escalated to the appropriate role
5. **Resolution**: the deviation is resolved (recovered, remediated, or accepted)

The exception record is created at detection and updated at each stage.

### 6.3 Exception vs deviation

A **deviation** is the instance: a specific rule was broken on a specific date by a specific actor. An **exception** is the predefined handling for a class of deviations. The catalog captures exceptions (the handling), not individual deviations (the instances); the deviations are tracked in `deviations[]` or in an external deviation-tracking system.

---

## 7. Deviations (new L2 top-level field)

EXT-14 introduces the new optional L2 top-level field `deviations[]` (array of structured entries). Per EXT-14 §7:

```yaml
deviations:
  - id: <deviation-id>
    rule_ref: <rule-id>
    description: |
      <The deviation.>
    status: detected | authorised | unauthorised | remediated | escalated | closed
    severity: high | medium | low
    detected_at: <YYYY-MM-DD or ISO-8601>
    remediated_at: <YYYY-MM-DD or ISO-8601>
    remediation: |
      <The remediation.>
```

### 7.1 Deviation status (controlled vocabulary)

| Value | Description |
|---|---|
| `detected` | The deviation has been detected but not yet classified |
| `authorised` | The deviation has been explicitly authorised (e.g. exception approved) |
| `unauthorised` | The deviation is not authorised (the rule was broken without approval) |
| `remediated` | The consequences have been addressed |
| `escalated` | The deviation has been escalated to a higher authority |
| `closed` | The deviation record is closed (remediated or accepted) |

### 7.2 Deviation severity (controlled vocabulary)

| Value | Description |
|---|---|
| `high` | Material impact (regulatory, financial, reputational) |
| `medium` | Moderate impact (operational, process integrity) |
| `low` | Minor impact (cosmetic, low-risk) |

### 7.3 Deviation tracking

The `deviations[]` field is optional. The catalog MAY track deviations in an external deviation-tracking system (e.g. an issue tracker, a GRC platform). The `deviations[]` field is a lightweight local record; for high-volume deviation tracking, an external system is preferred.

---

## 8. L2-L4 applicability

| Concern | L2 BusinessProcess | L3 Activity | L4 Task |
|---|---|---|---|
| Business rules | Process-level rules | Activity-specific rules | Task-specific rules |
| Controls | Process-level controls | Activity-level controls | Task-level controls |
| Exceptions | Process-level exceptions | Activity-level exceptions | Task-level exceptions |
| Deviations | Process-level deviations (summary) | Activity-level (when material) | Task-level (when material) |

L0 and L1 are non-executable (per EXT-11); these concepts are **not applicable** at L0/L1. The validator (GO-010) confirms: L0/L1 records MUST NOT carry business_rules/controls/exceptions/deviations.

A child's rules/controls/exceptions/deviations MUST NOT be auto-copied from the parent. The child MAY inherit the parent's rules via a reference (`source_ref` to the parent) and MAY declare activity/task-specific rules.

---

## 9. Compatibility and migration

EXT-14 is **additive**:

- Existing records that do not declare `business_rules[]` / `controls[]` / `exceptions[]` / `deviations[]` continue to validate.
- The new fields are optional. Records without them remain conformant.
- The validator (GO-001..GO-010) enforces the structural and vocabulary requirements when the fields are populated.

The EXT-10 regression test (`tests/test_schema_inventory_ext10.py`) is updated to remove the L2 entries from the gap list (the **business_rule**, **control**, and **exception** gaps are now legitimately in the L2 template per EXT-14). The L0/L1 entries remain (L0/L1 are non-executable; the rules/controls/exceptions fields remain absent from the L0/L1 schemas).

The 145 existing L2 records have **0** of the new fields populated (per the EXT-10 inventory; the CR-BP-96 advisory policy passes vacuously). The EXT-19 L2 backfill tranche is the work that populates them.

---

## 10. Validator and manifest

EXT-14 lands:

- `scripts/check_business_rules_controls_exceptions_ext14.py` (the validator; GO-001..GO-010 rules)
- `reconciliation/governance-manifest.json` (per-record manifest)
- `gate [39] Business Rules/Controls/Exceptions` wired ADVISORY in `scripts/conformance_result.py`
- `tests/test_business_rules_controls_exceptions_ext14.py` (unit + integration)

The validator enforces:

- **GO-001**: `business_rules` (when present) has the EXT-14 attributes (id, name, description, source, source_ref, maturity, rationale, owner)
- **GO-002**: `business_rules[].source` is in the rule-source vocabulary
- **GO-003**: `business_rules[].maturity` is in the rule-maturity vocabulary
- **GO-004**: `controls` (when present) has the EXT-14 attributes (id, name, description, type, enforces, automation, frequency, evidence, owner)
- **GO-005**: `controls[].type` is in the control-type vocabulary (4 values: preventive / detective / corrective / directive)
- **GO-006**: `controls[].automation` is in the automation vocabulary
- **GO-007**: `controls[].frequency` is in the frequency vocabulary
- **GO-008**: `exceptions` (when present) has the EXT-14 attributes (id, name, description, classification, detection, response, escalation, resolution, owner)
- **GO-009**: `exceptions[].classification` is in the classification vocabulary
- **GO-010**: L0/L1 do NOT carry business_rules/controls/exceptions/deviations (non-executable per EXT-11 + EXT-14 §8)

---

## 11. Closing the semantic-model tranche

EXT-14 closes **tranche gate G5_governance**, the **final** tranche gate of the 5-gate semantic-model tranche. The other four (G1_schema, G2_profiles, G3_interfaces, G4_accountability) were closed by EXT-10, EXT-11, EXT-12, and EXT-13 respectively.

The semantic-model tranche establishes the **structural and operational vocabulary** for describing Business Processes. The next tranche (Initiative C: documentation engineering, EXT-15..17) extends the documentation machinery: evidence/provenance/confidence (EXT-15), the contributor / authority / source-author model (EXT-16), and the cross-cutting documentation profile (EXT-17).

The full DEPENDENCY CHAIN for the semantic-model tranche:

```
G1_schema (EXT-10, MERGED)        - the schema inventory
   |
   v
G2_profiles (EXT-11, MERGED)      - L0-L4 documentation profiles
   |
   v
G3_interfaces (EXT-12, MERGED)    - inputs/outputs/interfaces/dependencies
   |
   v
G4_accountability (EXT-13, MERGED) - responsibility/accountability/roles/RACI
   |
   v
G5_governance (EXT-14, this PR)   - business_rules/controls/exceptions/deviations
   |
   v
EXT-15 (Evidence/Provenance/Confidence) - the next tranche
```

**G5 (Governance) closes by this PR. The 5-gate semantic-model tranche is then COMPLETE.**

---

## 12. References

- `templates/business-process.yaml` (the L2 template; EXT-14 extensions documented inline)
- `change-requests/CR-BP-94-EXT-14-business-rules-controls-and-exception-semantics.md` (the EXT-14 CR)
- `docs/operational-documentation-semantic-contract.md` (EXT-09; the upstream semantic contract)
- `docs/operational-schema-inventory.md` (EXT-10; the schema inventory + routed-gap table)
- `docs/inputs-outputs-interface-semantics.md` (EXT-12; the upstream semantic doc)
- `docs/responsibility-accountability-model.md` (EXT-13; the upstream semantic doc)
- `templates/documentation-profile-ext11-v3.yaml` (EXT-11; the v3 profile that consumes the EXT-14 fields)
- `reconciliation/programme-register.json` (the 17-CR register)
- `reconciliation/profile-manifest.json` (EXT-11 manifest)
- `reconciliation/inputs-outputs-manifest.json` (EXT-12 manifest)
- `reconciliation/responsibility-accountability-manifest.json` (EXT-13 manifest)
