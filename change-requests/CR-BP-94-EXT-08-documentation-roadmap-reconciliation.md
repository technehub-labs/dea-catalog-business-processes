# CR-BP-94-EXT-08: Documentation Extension Roadmap Reconciliation and Deferred-Work Disposition

Status: Proposed
Layer: Process Catalog
Owner: Emmanuel A. Otchere
Date: 2026-10-19
Parent: CR-BP-94 (Decomposition Record Templates)
Related CRs: CR-BP-94-EXT-01, CR-BP-94-EXT-01a, CR-BP-94-EXT-02, CR-BP-94-EXT-04, CR-BP-94-EXT-05, CR-BP-94-EXT-06, CR-BP-94-EXT-07
Sub-pipeline position: First reconciliation slice following EXT-07 and the existing EXT-04 proposal
Target repository: technehub-labs/dea-catalog-business-processes
Proposed path: change-requests/CR-BP-94-EXT-08-documentation-roadmap-reconciliation.md

---

1. Executive Summary

This Change Request reconciles the CR-BP-94 documentation extension programme into one authoritative, dependency-aware implementation roadmap.

The documentation extension series has evolved through several architectural and implementation proposals. The current repository contains multiple generations of documentation profiles, README generators, validation requirements, and backfill references. These are not yet expressed as one consistent and unambiguous delivery sequence.

A material inconsistency exists in the generated entity READMEs:

Operational Details fields are described as pending backfill at EXT-04.

However, EXT-04 is already defined as the Generation and Validation Pipeline. Its stated responsibility is to validate documentation and publish findings. EXT-06 is identified as the pilot and catalogue rollout that reconciles documentation content.

Consequently, the README placeholder creates an incorrect implementation instruction. It directs contributors towards a pipeline-validation CR for work that requires semantic research, authoring, evidence, review, and controlled publication.

This CR establishes the authoritative disposition:

1. EXT-04 is the documentation validation and pipeline workstream. It is not the operational-content backfill workstream.
2. EXT-05 is the decomposition documentation reconciliation workstream.
3. EXT-06 is the pilot, content enrichment, and catalogue rollout workstream.
4. EXT-07 is the consolidated README template and generator workstream.
5. EXT-08 reconciles the programme, its terminology, dependencies, and deferred-work references.
6. EXT-09 establishes the operational documentation semantic contract.
7. Subsequent CRs establish the data model, documentation profiles, evidence methodology, authoring process, automation, pilot, backfill, and conformance closure.

No operational content is to be fabricated merely to remove a placeholder. A record can be incomplete, not applicable, awaiting evidence, or genuinely unknown. These states must remain distinguishable.

2. Problem Statement

2.1 Conflicting extension references

The current extension programme contains the following relevant CRs:

CR	Existing responsibility	Reconciliation required
EXT-01	Documentation architecture	Retain as foundational architecture
EXT-01a	L0/L1 documentation profiles	Retain as cardinal-entity profile extension
EXT-02	README generation pipeline	Treat as historical generator design superseded by EXT-07
EXT-03	Documentation manifest and coverage model	Its implementation status and dependency relationship require explicit reconciliation
EXT-04	Generation and validation pipeline	Retain as validation and pipeline work, not content backfill
EXT-05	Decomposition reconciliation	Retain as parent-child documentation reconciliation
EXT-06	Pilot and catalogue rollout	Make this the controlled operational-content authoring and backfill delivery workstream
EXT-07	README template consolidation and Generator V2	Retain as the current consolidated README structure and generation baseline

The programme must not silently redefine existing CR identifiers or assign an existing identifier to a different scope.

2.2 Incorrect operational backfill instruction

A generated L2 README currently contains statements equivalent to:

## Operational Details
**Inputs / Outputs**: _(pending; backfill at EXT-04)_
**Roles and Responsibilities**: _(pending; backfill at EXT-04)_
**Business Rules and Controls**: _(pending; backfill at EXT-04)_

This is problematic for four reasons:

1. EXT-04 does not own business-content research or approval.
2. The existing YAML model already permits some operational properties.
3. The documentation profile identifies these sections as curated semantic content.
4. A placeholder does not communicate whether the information is unknown, unresearched, not applicable, inherited, or awaiting approval.

The placeholder therefore conflates a missing model value with a missing documentation activity and a missing evidence or approval state.

2.3 Existing model structures must be respected

The current Business Process template already contains optional operational fields, including:

* inputs
* transformation
* outputs
* responsibility
* boundary

The existing L2 documentation profile also identifies inputs, outputs, interfaces, roles, responsibilities, accountability, business rules, and controls as semantic documentation concerns.

EXT-08 must not introduce competing structures or redefine these fields. Their semantics, relationships, cardinality, and authoritative location will be resolved under EXT-09 and subsequent approved CRs.

3. Objectives

This CR SHALL:

1. Establish an authoritative register of the EXT documentation workstream.
2. Resolve conflicting references to EXT-04 and EXT-06.
3. Distinguish documentation generation, structural validation, semantic validation, decomposition reconciliation, and content backfill.
4. Define the dependency order for all remaining documentation work.
5. Establish the disposition of existing placeholders.
6. Identify the repository artefacts requiring correction.
7. Prevent duplicate schemas, fields, validators, and documentation sources of truth.
8. Establish explicit exit criteria before operational-content backfill begins.
9. Ensure the extension programme remains compatible with the current L0-L4 decomposition model and the canonical entity storage layout.

4. Scope

4.1 Included

* Reconciliation of EXT-01 through EXT-07.
* Correction of inaccurate placeholder instructions.
* Definition of the remaining extension roadmap.
* Identification of missing or unverified CR artefacts.
* Reconciliation of EXT-03 dependencies and implementation status.
* Definition of workstream ownership and dependency gates.
* Alignment with the existing generator, profiles, validator, and conformance pipeline.
* Backfill sequencing and readiness requirements.

4.2 Excluded

* Introducing new operational entity concepts.
* Defining the detailed operational semantic model.
* Changing the canonical Process metamodel.
* Adding operational fields to entity schemas.
* Performing catalogue-wide operational-content backfill.
* Rewriting existing READMEs manually.
* Changing L0 metrics semantics.
* Changing the decomposition hierarchy.
* Making advisory documentation findings blocking.

These are governed by subsequent CRs.

5. Normative Programme Decisions

5.1 Canonical source of truth

The canonical entity YAML remains the authoritative source for structured entity facts.

The README is a human-readable documentation projection of the canonical record, supplemented by curated semantic content where the canonical record or an approved documentation asset does not yet express the necessary explanation.

A README MUST NOT become an independent competing source of truth for structured operational properties.

A documentation manifest, where adopted, MUST identify the source and status of curated content and MUST NOT silently override canonical entity values.

5.2 Responsibilities of the existing extension CRs

The following responsibility assignments are authoritative for this programme:

Workstream	Responsibility
EXT-01 / EXT-01a	Documentation architecture and five-level profile coverage
EXT-02	Historical README generator design
EXT-03	Documentation manifest and coverage model; implementation status to be reconciled
EXT-04	Documentation generation/validation pipeline and structural findings
EXT-05	Parent-child documentation and decomposition reconciliation
EXT-06	Pilot, semantic authoring, operational-content backfill, and catalogue rollout
EXT-07	Consolidated README template and Generator V2
EXT-08	Programme reconciliation and roadmap governance
EXT-09	Operational documentation semantic contract

The scope of EXT-04 is not expanded to include manual or AI-assisted business-content research.

5.3 EXT-04 and EXT-06 distinction

EXT-04 SHALL validate the presence and structure of documentation artefacts and publish findings.

EXT-06 SHALL coordinate the content-enrichment process that resolves findings requiring substantive business or operational knowledge.

The distinction is:

Canonical entity YAML
        |
        v
README Generator
        |
        v
Generated README
        |
        v
EXT-04: Structural validation
        |
        v
EXT-05: Decomposition reconciliation
        |
        v
EXT-06: Semantic research and content backfill
        |
        v
Human review and approval
        |
        v
Canonical source update / approved documentation update
        |
        v
README regeneration and conformance validation

This diagram represents programme responsibilities, not an execution sequence that overrides the detailed dependencies of existing CRs.

5.4 Placeholder disposition

The phrase pending; backfill at EXT-04 MUST NOT be used to direct operational-content authoring.

For L1-L4 operational details, the placeholder MUST be replaced through the approved documentation profile and generator design with a status that identifies the actual disposition.

For L0 metrics and cell-charter fields, existing EXT-07 and EXT-04 provisions remain subject to their own reconciliation. This CR does not move L0 metrics into the L2-L4 operational model.

A placeholder MUST never be interpreted as evidence that the field is semantically required for every entity level.

5.5 No automatic semantic inference

The following rules are mandatory:

* An input MUST NOT be inferred merely from a trigger.
* An output MUST NOT be inferred merely from an outcome.
* A resource MUST NOT be classified as an input without semantic justification.
* A role MUST NOT be inferred from a process name or ECF coordinate.
* A control MUST NOT be inferred from a regulatory domain alone.
* A metric MUST NOT be treated as an approved target without governance evidence.
* A system interaction MUST NOT be invented from a process description.
* A parent entity’s content MUST NOT be copied into a child entity without an explicit inheritance relationship and applicability assessment.

6. Authoritative Extension Roadmap

The following roadmap is the programme baseline. Proposed future CRs are not represented as already existing or approved repository artefacts.

Sequence	CR	Title	Primary output
1	EXT-08	Documentation Roadmap Reconciliation	Authoritative programme baseline
2	EXT-09	Operational Documentation Semantic Contract	Normative semantic definitions
3	EXT-10	Operational Entity Schema Alignment	Approved canonical YAML/schema representation
4	EXT-11	Decomposition-Level Documentation Profiles	L0-L4 applicability and requirements
5	EXT-12	Process Inputs, Outputs and Interface Semantics	Interface and transformation semantics
6	EXT-13	Responsibility and Accountability Semantics	Role and accountability model
7	EXT-14	Business Rules, Controls and Exception Semantics	Rule, control and exception model
8	EXT-15	Evidence, Provenance and Confidence Framework	Evidence and assertion lifecycle
9	EXT-16	Operational Authoring and Research Methodology	Repeatable content research method
10	EXT-17	Enrichment Tooling and Backfill Orchestration	Controlled authoring and review tooling
11	EXT-18	Operational Documentation Pilot	Validated representative pilot
12	EXT-19	L2 Business Process Catalogue Backfill	L2 operational enrichment
13	EXT-20	L3 Activity Catalogue Backfill	L3 operational enrichment
14	EXT-21	L4 Task Catalogue Backfill	L4 operational enrichment, when canonical L4 records exist
15	EXT-22	L0/L1 Context and Process Group Documentation Reconciliation	Cardinal-entity documentation
16	EXT-23	Operational Documentation Conformance Gates	Approved conformance enforcement
17	EXT-24	Catalogue Closure and Continuous Governance	Closure evidence and ongoing governance

The EXT-10 through EXT-24 identifiers are proposed programme allocations. Before creating each CR, the repository CR register MUST be checked for collisions and existing commitments.

EXT-03 remains a separate reconciliation item. Its original reserved scope MUST be preserved and its actual implementation status recorded before EXT-04 dependencies are declared complete.

7. Dependency and Readiness Gates

Gate G1: Programme architecture reconciled

Requires:

* EXT-08 approved.
* EXT-01 and EXT-01a retained as the profile architecture baseline.
* EXT-07 identified as the current README structure and generator design.
* EXT-04 and EXT-06 responsibilities unambiguously separated.
* EXT-03 status and dependency implications documented.

Gate G2: Semantic model approved

Requires:

* EXT-09 approved.
* EXT-10 schema alignment approved.
* EXT-11 profile requirements approved.
* No unresolved duplicate operational properties.
* No unapproved changes to canonical metamodel semantics.

Gate G3: Authoring and evidence ready

Requires:

* EXT-12 through EXT-16 approved.
* Evidence and provenance requirements implemented.
* Research and review responsibilities established.
* Level-specific applicability rules documented.

Gate G4: Tooling ready

Requires:

* EXT-17 approved and implemented.
* Existing generator remains deterministic.
* Content changes can be traced to their source and approval.
* Backfill operations are repeatable and auditable.

Gate G5: Pilot approved

Requires:

* EXT-18 completed.
* Pilot records pass semantic review.
* Generator output and structural validation are conformant.
* No unsupported assumptions remain.
* Pilot methodology is repeatable.

Gate G6: Catalogue backfill complete

Requires:

* EXT-19 through EXT-22 completed or explicitly dispositioned.
* Every in-scope record has a documented completeness state.
* Not-applicable and inherited dispositions are justified.
* No placeholder is falsely represented as completed content.

Gate G7: Governance closure

Requires:

* EXT-23 conformance requirements approved and implemented.
* EXT-24 closure evidence published.
* Ownership and review cadence established.

8. Repository Changes

The following repository artefacts are in scope.

Path	Change
docs/process-documentation-architecture.md	Reconcile extension roadmap and references
docs/decomposition-template-guide.md	Correct backfill guidance and clarify operational-content authoring
change-requests/README.md	Add EXT-08 and update programme register
change-requests/CR-BP-94-EXT-08-documentation-roadmap-reconciliation.md	Add this CR
reconciliation/	Add or update a machine-readable extension roadmap/disposition register
scripts/	No generator or validator implementation change required by this CR
templates/	No operational schema extension required by this CR

The reconciliation register SHOULD contain:

* CR identifier.
* Current title.
* Existing repository path.
* Original scope.
* Current disposition.
* Dependencies.
* Superseded artefacts.
* Open decisions.
* Completion evidence.
* Next action.

It MUST distinguish proposed, implemented, merged, superseded, deferred, and closed states according to the repository’s established governance vocabulary.

9. Migration and Compatibility

1. Existing entity YAML records MUST remain valid.
2. Existing README files MUST remain readable.
3. No existing CR identifier may be repurposed.
4. No entity identifier or content-derived hash may be changed solely to correct documentation wording.
5. Generator output changes MUST be deterministic.
6. Historical CR references MUST remain traceable.
7. Any change to generated README wording MUST be reflected in generator tests.
8. Existing advisory findings MUST not be silently deleted or suppressed.

10. Test and Validation Requirements

The implementation of this CR MUST verify:

* All existing CR identifiers remain unique.
* EXT-01 through EXT-07 have one documented disposition each.
* EXT-03 is not treated as completed without implementation evidence.
* EXT-04 does not claim ownership of semantic content backfill.
* EXT-06 explicitly owns content-enrichment and rollout activities.
* No README operational placeholder directs contributors to EXT-04 for content authoring.
* L0 metrics placeholders remain distinct from L1-L4 operational-content placeholders.
* The documentation architecture and decomposition template guide do not contradict the CR register.
* CR metadata checks pass.
* Existing catalogue conformance gates remain conformant.

11. Acceptance Criteria

* AC-01: The extension programme has one authoritative reconciled roadmap.
* AC-02: EXT-01, EXT-01a, EXT-02, EXT-03, EXT-04, EXT-05, EXT-06 and EXT-07 each have an explicit disposition.
* AC-03: EXT-04 is explicitly limited to its generation/validation responsibilities.
* AC-04: EXT-06 explicitly owns the semantic content backfill and catalogue rollout.
* AC-05: The distinction between L0 metrics and L1-L4 operational details is documented.
* AC-06: The phrase pending; backfill at EXT-04 is no longer used as an operational-content implementation instruction.
* AC-07: No duplicate operational data structures are introduced.
* AC-08: EXT-03 implementation status and dependency implications are recorded.
* AC-09: The extension roadmap register is machine-readable or otherwise auditable.
* AC-10: CR metadata validation passes.
* AC-11: Existing entity records, IDs, and decomposition relationships remain unchanged.
* AC-12: The programme is ready to proceed to EXT-09.

12. Risks and Mitigations

Risk	Mitigation
Existing CRs contradict the new roadmap	Preserve historical scope and record explicit dispositions
EXT-03 is assumed complete without evidence	Require implementation verification
EXT-04 absorbs business research responsibilities	Maintain strict validation versus authoring separation
Operational fields are duplicated	Require EXT-09 semantic review before schema changes
README placeholders are removed without content	Replace with explicit completeness dispositions
Backfill becomes uncontrolled mass editing	Require pilot and evidence-based approval
L0 metrics are mixed with process-level metrics	Retain separate level-specific treatment

13. Rollback

This CR is principally a governance and documentation reconciliation.

If implementation introduces regressions:

1. Revert only the affected documentation and roadmap changes.
2. Preserve existing generator and validator behaviour.
3. Restore the prior CR register and documentation architecture if necessary.
4. Do not remove historical CR records or alter entity records.
5. Re-run CR metadata and conformance validation.

14. Completion Definition

EXT-08 is complete when the extension programme has a reconciled, auditable roadmap and the repository no longer directs operational-content backfill to the wrong CR.

EXT-08 does not itself backfill any Business Process, Activity, Task, Process Group, or Process Context.

Its output is the approved governance baseline for EXT-09 and the subsequent operational documentation workstream.