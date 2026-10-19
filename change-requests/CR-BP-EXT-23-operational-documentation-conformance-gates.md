# CR-BP-EXT-23: Operational Documentation Conformance Gates

**Status**: Normative (proposed for adoption under CR-BP-EXT-23)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-19
**Source CR**: CR-BP-EXT-23 (Operational Documentation Conformance Gates)
**Programme**: Operational Documentation Framework Extension (DEA-PROCESS-ENRICH-000)
**Repository**: technehub-labs/dea-catalog-business-processes
**Change type**: Catalogue governance, conformance enforcement, CI integration
**Target scope**: L0 Process Scope, L1 Process Group, L2 Business Process, L3 Activity, L4 Task
**Priority**: Critical
**Depends on**: EXT-08 through EXT-22, particularly EXT-17, EXT-19, EXT-20, EXT-21, EXT-22
**Enables**: EXT-24 (Catalogue closure and continuous governance)
**Implementation approach**: Readiness assessment, gate classification, tiered enforcement, CI integration

---

## 1. Executive summary

This Change Request establishes the conformance gate framework that enforces the operational documentation standards established by EXT-08 through EXT-22.

The preceding CRs establish:

- The semantic model (EXT-09, EXT-10, EXT-11)
- The operational semantics (EXT-12, EXT-13, EXT-14)
- The evidence, provenance and authoring framework (EXT-15, EXT-16)
- The enrichment and validation tooling (EXT-17)
- The controlled pilot and its GO decision (EXT-18)
- The level-wise backfills (EXT-19, EXT-20, EXT-21)
- The catalogue-wide structural reconciliation and the EXT-23 readiness assessment (EXT-22)

EXT-23 converts those standards into enforced gates.

The central distinction is one the EXT-22 CR already drew: a catalogue can pass structural validation while still having poor functional decomposition. EXT-23 therefore enforces **deterministic structural rules automatically**, while **semantic adequacy remains evidence-led and subject to human review**. A gate that encodes an unresolved semantic rule as an automatic blocking check would convert an open question into a false assurance.

---

## 2. Problem statement

The repository currently runs 46 conformance gates through `scripts/conformance_result.py`. Their blocking status is inconsistent with the maturity of the underlying standards:

- The pre-EXT-08 gates [1] to [33] are blocking, reflecting the original entity-system contract.
- The EXT-04 and EXT-05 gates [34] and [35] are blocking, having passed their rollout gates.
- The gates introduced by EXT-11 through EXT-22 ([36] to [47]) are advisory, because the corresponding backfill work has not been completed.

This is the correct posture for advisory gates. It is not the correct end state. A gate that remains advisory after its subject has been reconciled is not enforcing anything.

EXT-23 closes that gap by:

1. Classifying every gate by enforcement class (deterministic structural, deterministic content, evidence-led semantic, human-review).
2. Promoting gates to blocking only where the EXT-22 readiness assessment confirms the rule is deterministic and the subject population has been reconciled.
3. Recording, for each gate, the reason it is or is not blocking.
4. Integrating the classification into CI as an explicit, auditable tier.
5. Establishing the enforcement policy for each tier, including the conditions under which a gate may be demoted or deferred.

---

## 3. Objectives

1. Produce a complete gate inventory with an enforcement classification per gate.
2. Promote the deterministic structural gates to blocking.
3. Retain the evidence-led semantic gates as advisory, with an explicit review requirement.
4. Record the reason for every gate's enforcement status.
5. Integrate the tiered enforcement into CI.
6. Establish the demotion, deferral and exception policy.
7. Publish the conformance posture report.
8. Establish the baseline for EXT-24 continuous governance.

---

## 4. Scope

### 4.1 In scope

- The 47 conformance gates registered in `scripts/conformance_result.py`.
- The gate inventory and enforcement classification.
- The CI integration of the tiered enforcement.
- The conformance posture report.
- The demotion, deferral and exception policy.

### 4.2 Out of scope

EXT-23 does not:

- Introduce a new validation rule that is not already expressed in a landed CR.
- Automatically enforce an unresolved semantic rule.
- Modify the canonical entity representation.
- Create, merge, delete or reassign entities.
- Change the metamodel.
- Introduce a second governance model parallel to the EXT-15/EXT-16 framework.
- Replace the EXT-22 reconciliation matrix with a gate.

---

## 5. Governing principles

### 5.1 Enforcement follows evidence, not ambition

A gate becomes blocking only when:

1. The rule it enforces is deterministic and mechanically evaluable.
2. The population it applies to has been reconciled under EXT-22.
3. Its findings on that population are understood and dispositioned.
4. Its enforcement does not convert an open question into a false assurance.

A requirement expressed in prose is not, by itself, grounds for an automatic blocking check.

### 5.2 Semantic adequacy remains human-reviewed

Rules that depend on business meaning, functional contribution, coverage adequacy, duplicate resolution, granularity judgement or boundary interpretation cannot be enforced automatically. They are enforced through the EXT-22 reconciliation record, the disposition vocabulary and human review.

### 5.3 One source of truth for the gate registry

The gate registry is the `GATES` list in `scripts/conformance_result.py`. The enforcement classification is stored alongside it, not in a parallel document. A gate's blocking status is read from the registry, never duplicated.

### 5.4 No gate may be silently demoted

A gate may be demoted or deferred only through an approved decision recorded in the conformance posture report, with a rationale and an accountable authority.

### 5.5 The enforcement tier is a first-class artefact

The tiered enforcement must be readable, diffable and reviewable in the repository, and must be exercised by the test suite.

---

## 6. Requirements

### REQ-23-01: Gate inventory

Produce a complete inventory of the registered conformance gates. For each gate, record:

- Gate number
- Gate name
- The CR that introduced it
- The rule set it enforces
- Its enforcement class
- Its blocking status
- The reason for that status
- The population it applies to
- The reconciliation status of that population

### REQ-23-02: Enforcement classification

Every gate shall be assigned exactly one enforcement class:

- **structural**: deterministically evaluable structural relationship rules
- **content**: deterministically evaluable content-presence rules
- **semantic**: rules whose evaluation requires business meaning
- **review**: rules whose evaluation requires human adjudication

### REQ-23-03: Promotion criteria

A gate may be promoted to blocking only where its enforcement class is `structural` or `content`, its subject population has been reconciled under EXT-22, and the EXT-22 readiness assessment lists it as automatically enforceable.

A gate whose enforcement class is `semantic` or `review` shall not be promoted to blocking.

### REQ-23-04: Reason recording

Every gate shall carry a recorded reason for its enforcement status. The reason shall state the basis, not merely restate the status.

### REQ-23-05: Population reconciliation linkage

Every gate shall record the reconciliation status of its subject population, referencing the EXT-22 readiness assessment.

### REQ-23-06: CI integration

The tiered enforcement shall be integrated into the existing CI pipeline. The pipeline shall report the enforcement tier of every gate alongside its result, so that a reviewer can see not only whether a gate passed but under which standard it was evaluated.

### REQ-23-07: Conformance posture report

Publish a conformance posture report covering:

- Total registered gates
- Gates by enforcement class
- Gates by blocking status
- The gate inventory with reasons
- The reconciled population coverage per gate
- The gates deferred, with rationale
- The approved exceptions
- The residual risks carried into EXT-24

### REQ-23-08: Demotion and deferral policy

A gate may be demoted or deferred only where:

- The rationale is recorded.
- The accountable authority is recorded.
- The scope of the deferral is explicit (gate, population or rule).
- The deferral has an expiry or review condition.

No demotion shall be performed by editing the registry without a corresponding posture report entry.

### REQ-23-09: Exception policy

An approved exception shall record the gate, the scope, the rationale, the accountable authority and the review condition. An exception shall not suppress a finding; it shall reclassify its enforcement for the declared scope only.

### REQ-23-10: Test coverage

The test suite shall assert that:

- Every registered gate has an enforcement class.
- Every registered gate has a recorded reason.
- Every registered gate has a reconciliation linkage.
- No `semantic` or `review` gate is blocking.
- Every blocking gate appears in the automatically-enforceable set of the EXT-22 readiness assessment.
- The gate count and the inventory count agree.

### REQ-23-11: Registry consistency

The gate registry shall be the single source of truth. The enforcement classification, reason and linkage shall be stored in the registry alongside the gate definition, and the posture report shall be generated from the registry.

### REQ-23-12: EXT-24 readiness

The conformance posture report shall identify the governance model required for continuous operation: the review cadence, the exception lifecycle, the demotion criteria and the escalation path for a newly introduced finding.

---

## 7. The enforcement tier model

| Tier | Enforcement class | Blocking | Basis |
|---|---|---|---|
| T1 | structural | yes | Mechanically evaluable structural rule on a reconciled population |
| T2 | content | yes | Mechanically evaluable content-presence rule on a reconciled population |
| T3 | semantic | no | Requires business meaning; enforced through the EXT-22 reconciliation record and human review |
| T4 | review | no | Requires human adjudication; enforced through the EXT-22 reconciliation record and human review |

A T3 or T4 gate that returns a finding is not a failure of the build. It is an input to the review queue.

---

## 8. Quality gates

- Gate 23-A: Inventory completeness (every registered gate inventoried)
- Gate 23-B: Classification completeness (every gate has exactly one class)
- Gate 23-C: Promotion integrity (no semantic or review gate is blocking)
- Gate 23-D: Reason completeness (every gate has a recorded reason)
- Gate 23-E: Population linkage (every gate records its reconciliation status)
- Gate 23-F: Registry consistency (posture report generated from the registry)
- Gate 23-G: Test coverage (the REQ-23-10 assertions pass)

---

## 9. Acceptance criteria

AC-23-01: A complete gate inventory exists for every registered gate.

AC-23-02: Every gate carries exactly one enforcement class.

AC-23-03: Every blocking gate is classified `structural` or `content`.

AC-23-04: Every gate carries a recorded reason for its enforcement status.

AC-23-05: Every gate records the reconciliation status of its subject population.

AC-23-06: The CI pipeline reports the enforcement tier of every gate.

AC-23-07: A conformance posture report is published.

AC-23-08: Every deferred gate has a rationale, an accountable authority and a review condition.

AC-23-09: Every approved exception is scoped, rationalised and reviewable.

AC-23-10: The test suite asserts the REQ-23-10 invariants.

AC-23-11: The posture report is generated from the registry, not maintained separately.

AC-23-12: The EXT-24 governance requirements are identified.

---

## 10. Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Semantic rules are promoted to blocking automatically | False assurance | REQ-23-03 forbids it; the test suite asserts it |
| A gate is demoted silently | Unexplained loss of enforcement | REQ-23-08 requires a posture report entry |
| The posture report drifts from the registry | Two sources of truth | REQ-23-11 makes the report generated |
| Blocking promotion is applied to an unreconciled population | False failures | REQ-23-03 requires EXT-22 reconciliation first |
| Gate count and inventory diverge | Silent coverage loss | REQ-23-10 asserts they agree |
| The enforcement model is invented rather than reused | A parallel governance model | The tiers map onto the EXT-22 readiness assessment classes |

---

## 11. Expected deliverables

1. The gate inventory with enforcement class, reason and linkage.
2. The registry-integrated enforcement classification.
3. The tiered CI integration.
4. The conformance posture report.
5. The demotion, deferral and exception policy.
6. The test suite assertions.
7. The EXT-24 governance identification.

---

## 12. Definition of done

EXT-23 is complete when every registered gate carries an enforcement class, a recorded reason and a population linkage; the deterministic structural and content gates on reconciled populations are blocking; the evidence-led semantic gates remain advisory with an explicit review requirement; the posture report is generated from the registry; and the governance model for continuous operation is identified for EXT-24.

---

## 13. References

- `change-requests/CR-BP-94-EXT-22-process-decomposition-reconciliation-and-structural-integrity.md` (EXT-22)
- `change-requests/CR-BP-94-EXT-21-l4-task-operational-documentation-backfill.md` (EXT-21)
- `change-requests/CR-BP-94-EXT-20-l3-activity-operational-documentation-backfill.md` (EXT-20)
- `change-requests/CR-BP-94-EXT-19-l2-business-process-operational-documentation-backfill.md` (EXT-19)
- `change-requests/CR-BP-94-EXT-18-operational-documentation-pilot.md` (EXT-18 + GO decision)
- `change-requests/CR-BP-94-EXT-17-enrichment-tooling-and-backfill-orchestration.md` (EXT-17)
- `docs/operational-documentation-programme/CR-BP-94-EXT-22-to-23-detailed-design.md` (the EXT-22/23 detailed design)
- `scripts/conformance_result.py` (the gate registry)
- `reconciliation/ext23-readiness-assessment.json` (the EXT-22 readiness assessment)
- `reconciliation/reconciliation-matrix.json` (the EXT-22 reconciliation matrix)
- `reconciliation/programme-register.json` (the 17-CR register)
