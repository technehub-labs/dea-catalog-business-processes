# CR-BP-03C — Sample Business Process Contribution (walk-the-flow)

**Status:** Proposed (2026-09-03)
**Layer:** L1
**Owner:** TechNeHub Labs
**Type:** Sample Entry / Worked Example / End-to-End Validation
**Priority:** High
**Repository:** `technehub-labs/dea-catalog-processes`
**Depends on:** CR-BP-03, CR-BP-03A, CR-BP-02
**Supersedes:** none
**Working folder:** `/home/hermes/dea-work/process/00_inbox/CR-BP-03C-...`

---

## 1. Intent

Land the **first** Business Process entry in the catalog,
walking the full CR-BP-03 / CR-BP-03A / CR-BP-02 flow
end-to-end. This CR:

1. validates the contribution mechanism with a real worked
   example;
2. validates the 4-axis classification with real axes;
3. validates the process-identity contract with a real
   identity;
4. validates the metamodel-aligned relationship-instance
   shape (composes + realizes);
5. validates the cell charter with a real Process Context
   cell (PartyAndRelationship × Operate);
6. provides the **canonical example** that future
   contributors can pattern-match against.

This is **not** a comprehensive landscape; it is **one** BP
chosen to exercise every part of the machinery.

---

## 2. Sample Business Process

**`dea:process-manage-customer-relationship`** — *Manage Customer Relationship*

A Business Process that operates the day-to-day management
of an active customer relationship across its lifecycle
(acquisition → onboarding → active use → renewal /
win-back). The principal organizational locus is the
**Middle Line** (sales / account management leadership);
the work coordinates customer-facing resources, monitors
the customer's value exchange with the enterprise, and
allocates attention and effort across the customer
portfolio.

### 2.1 The 4-axis classification

| Axis | Value | Why |
|---|---|---|
| `process_intent` | `management` | Coordinates, monitors, plans, controls (CR-BP-SPEC-BP-01 §3). Not operational (no direct value-delivery work) and not support (not an internal enabler). |
| `process_type` | `management` | Mintzberg Middle Line (CR-BP-03 §2.1; `classifications/process-types.yaml`). Plan, monitor, and control allocation of resources to achieve strategic goals. |
| `process_specialization` | `[]` | This BP is the **root** of the customer-relationship specialization; it has no parent processes. Future specializations (e.g. `dea:bp:manage-enterprise-customer`, `dea:bp:manage-retail-customer`) will declare this id in their `process_specialization` list. |
| `process_audience` | `party-relationship` | The ECF Domain `PartyAndRelationship` is the principal audience. The BP's outcomes serve customers and the demand they bring. |

### 2.2 The Process Identity contract

| Field | Value |
|---|---|
| `identity.verb` | `manage` |
| `identity.object` | `customer relationship` |
| `identity.scope` | `(all customer segments)` |
| `identity.outcome_statement` | An active customer relationship is sustained across its lifecycle (acquisition → onboarding → active use → renewal or win-back) through allocation of attention, escalation handling, and renewal coordination. |
| `identity.evidence_links` | `[https://www.apqc.org/resource-library/resource-collections/56391]` (APQC Process Classification Framework — Customer Relationship Management process class) |

### 2.3 The relationships (canonical; metamodel-aligned)

```yaml
relationships:
  # Structural: this BP is the root; no composes relationship.
  # Capability realization: realizes the Business Capability
  # `Customer Relationship Management`.
  - source_id: dea:process-customer-relationship-management
    target_id: dea:entity-capability:customer-relationship-management
    relationship_type: realizes
    status: active
    direction: "outgoing"
    rationale: |
      The Business Process realizes the Business Capability
      `Customer Relationship Management`. The capability is the
      abstract "what the enterprise can do"; the process is
      the structured "how it does it".
    asserted_by: "DEa team"
    asserted_at: "2026-09-03"
    provenance:
      type: manual
      asserted_by: "DEa team"
      asserted_at: "2026-09-03"
      evidence: "https://www.apqc.org/resource-library/resource-collections/56391"
```

### 2.4 The Process Context

The BP operates in the **PartyAndRelationship × Operate**
context: an active customer relationship is in the
"operate" lifecycle stage, and the audience is the
"customer and demand" domain. A Cell Charter entry
(`dea:pc-pr-op`) is provided alongside the BP entry.

The Cell Charter entry's `processes` array references the
BP via `dea:process-manage-customer-relationship`.

---

## 3. The L0/L1/L2 (conceptual) hierarchy

Per CR-BP-03 §9, the L0/L1/L2 hierarchy is a conceptual
model — not separate top-level directories. For this sample:

| Level | Construct | Sample |
|---|---|---|
| **Context** | `dea:pc-pr-op` (Cell Charter) | `PartyAndRelationship × Operate` |
| **Scope (L0)** | The bounded enterprise context | Customer-facing operations |
| **Group (L1)** | A loose grouping of related BPs | Customer lifecycle management group |
| **Business Process (L2)** | `dea:process-manage-customer-relationship` | Manage Customer Relationship (this entry) |

The **scope** and **group** are recorded in the entry's
metadata (for documentation purposes); they are **not**
separate catalog entities and **not** claimed as OpenDEA
metamodel entities (per CR-BP-03 §3: classification ≠
ontology).

---

## 4. Files added

```
change-requests/CR-BP-03C-sample-process-contribution.md  [NEW] (this file)
entities/v1-alpha/dea_bp_manage-customer-relationship.yaml  [NEW] (canonical entry)
contexts/v1-alpha/dea-pc-pr-op.yaml                        [NEW] (cell charter)
contributions/processes/dea_bp_manage-customer-relationship.yaml  [NEW] (contribution record)
docs/examples/manage-customer-relationship.md              [NEW] (worked example)
```

The CR's canonical fingerprint:

```
md5:  d6a3c1f8...  (refined during implementation)
```

---

## 5. Validators exercised

| Validator | Expected outcome on the sample |
|---|---|
| `check_process_identity.py` | PASS (BP-ARC-ID-001..005) |
| `check_process_specialization.py` | PASS (BP-SPEC-01-001..007) |
| `check_process_context.py` | PASS (PC-001..PC-008) — the new `dea:pc-pr-op` cell is well-formed |
| `check_legacy_migration.py` | PASS (BP-MIG-001..005) — the entry uses canonical form; no migration recommendation |
| `check_ecf_conformance.py` | PASS — `process_audience: party-relationship` is one of the allowed values |
| `validate_consumer.py` against `dea-architecture-framework@v0.6.0` | PASS — pointer drift = 0 |
| Process Contribution Report workflow | Generates a reclassification report showing the entry is well-formed and a candidate for promotion to the next stage |

---

## 6. Honest scoping notes

- **One BP, one cell**. This is not a comprehensive
  landscape; it is one chosen BP that exercises every part
  of the machinery. Future CRs (CR-BP-06, CR-BP-07, ...)
  will add more BPs.
- **The capability reference is forward-looking**. The
  Business Capability `dea:entity-capability:customer-relationship-management`
  will live in `dea-catalog-business-capabilities`. Until
  that catalog lands the capability entry, the BP's
  `realizes` relationship references a forward-looking
  capability id. The relationship's `provenance` notes
  this.
- **L0/L1 are metadata, not entities**. The Scope and
  Group are recorded in the entry's `metadata` field as
  documentation. They are NOT promoted to catalog entries
  (per CR-BP-03 §3).
- **The example is intentional and exemplary**. Future
  contributors should treat this entry as the **canonical
  pattern** for new BPs.

---

## 7. Change programme impact

| Previous CR | This CR |
|---|---|
| CR-BP-03 (4-axis classification) | First entry to use all 4 axes |
| CR-BP-03A (migration validator) | First entry to demonstrate "PASS on canonical form" |
| CR-BP-02 (Process Context register) | First cell charter entry |
| CR-BP-03 (contribution mechanism) | First contribution to flow through |

---

## 8. Acceptance criteria

- [ ] Canonical entry lands at
      `entities/v1-alpha/dea_bp_manage-customer-relationship.yaml`.
- [ ] Cell charter lands at
      `contexts/v1-alpha/dea-pc-pr-op.yaml`.
- [ ] Contribution record lands at
      `contributions/processes/dea_bp_manage-customer-relationship.yaml`.
- [ ] Worked example lands at
      `docs/examples/manage-customer-relationship.md`.
- [ ] All 7 validators pass on the new entries.
- [ ] The Process Contribution Report workflow generates a
      reclassification report on the contribution.
- [ ] `docs/examples/` is created (new directory) with
      its own README explaining the example.
- [ ] CHANGELOG entry added.
- [ ] README updated with a "Sample entry" pointer.

---

## 9. Review & Voting Before Committing 

Processes are adopted through a submission and CR-gate (CR-programme convention, is gated with a pause for processing, and voting) before merging into the main catalog. 
