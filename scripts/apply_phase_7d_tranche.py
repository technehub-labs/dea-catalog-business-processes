#!/usr/bin/env python3
"""Generate CR-BP-21d artifacts (EnablementAndOperations landing):
5 process contexts, 1 L1 group, 5 L2 processes. Mirrors the
CR-BP-21c (ProductAndValue) pattern. Substrate-neutral
per ADR-ECF-002 §5 / CR-ECF-007.

Run: python scripts/apply_phase_7d_tranche.py
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).parent.parent
CTX = ROOT / "contexts/v1-alpha"
ENT = ROOT / "entities/v1-alpha"
CHANGE_DATE = "2026-09-08"


CONTEXTS = [
    {
        "filename": "dea-pc-oe-conceive",
        "id": "dea:pc-oe-conceive",
        "domain": "EnablementAndOperations",
        "stage": "Conceive",
        "name": "Operations Model and Enablement Conception",
        "definition": (
            "The bounded enterprise context for **conceiving** the enterprise's "
            "operations model and enablement approach in the **Operations & "
            "Enablement** domain. This context addresses the front-end work of "
            "framing the operations strategy, the delivery model, the technology "
            "enablement approach, and the physical asset approach. v2.4.0: "
            "absorbs execution-side sourcing and asset conception from the "
            "dissolved Supply & Resources domain; physical and virtual resources "
            "are enablers of execution (domain-grounding.md §3.6)."
        ),
        "includes": [
            "Operations strategy framing",
            "Delivery model conception",
            "Technology enablement approach framing",
            "Physical asset approach framing",
        ],
        "excludes": [
            "Customer strategy (party-relationship x conceive; adjacent domain)",
            "Strategic direction for operations (strategy-direction x conceive; adjacent domain)",
            "Supplier relationship conception (party-relationship x conceive; adjacent domain)",
            "Operations model design (Design stage; adjacent context)",
            "Operations build (Build stage; adjacent context)",
        ],
        "outcomes": [
            "Operations strategy is framed for the enterprise.",
            "Delivery model is conceived with bounded scope.",
            "Technology enablement approach is framed.",
            "Physical asset approach is framed.",
        ],
        "adjacent": [
            "dea:pc-oe-design", "dea:pc-oe-build", "dea:pc-oe-operate", "dea:pc-oe-improve",
        ],
        "processes": ["dea:process-frame-operations-strategy"],
        "l1_candidates": ["Operations Model Conception", "Enablement Conception"],
        "grounding_phrase": "conception of operations model, delivery model, technology enablement, and physical asset approach",
        "enterprise_concern": "the conception of the enterprise's operations model and enablement approach.",
        "lifecycle_concern": "framing operations strategy, delivery model, technology enablement approach, and physical asset approach.",
        "combined_meaning": "The front-end work of framing the operations strategy, the delivery model, the technology enablement approach, and the physical asset approach.",
    },
    {
        "filename": "dea-pc-oe-design",
        "id": "dea:pc-oe-design",
        "domain": "EnablementAndOperations",
        "stage": "Design",
        "name": "Operations and Enablement Design",
        "definition": (
            "The bounded enterprise context for **designing** the operations "
            "model, delivery model, technology platform architecture, facility "
            "and asset blueprint, and logistics and routing of the enterprise in "
            "the **Enablement & Operations** domain. This context addresses the "
            "analytical work of producing designs for the execution engine and "
            "its enabling infrastructure. v2.4.0: absorbs asset and facility "
            "blueprint design from the dissolved Supply & Resources domain "
            "(domain-grounding.md §3.6)."
        ),
        "includes": [
            "Operations model design",
            "Delivery model design",
            "Technology platform architecture design",
            "Facility and asset blueprint design",
            "Logistics and routing design",
        ],
        "excludes": [
            "Operations conception (Conceive stage; adjacent context)",
            "Operations build (Build stage; adjacent context)",
            "Capability design (owning domains; adjacent domains)",
            "Proposition design (product-value x design; adjacent domain)",
        ],
        "outcomes": [
            "Operations model is designed with bounded execution scope.",
            "Delivery model is designed for the proposition portfolio.",
            "Technology platform architecture is designed.",
            "Facility and asset blueprint is designed.",
            "Logistics and routing are designed.",
        ],
        "adjacent": [
            "dea:pc-oe-conceive", "dea:pc-oe-build", "dea:pc-oe-operate", "dea:pc-oe-improve",
        ],
        "processes": ["dea:process-design-operations-model"],
        "l1_candidates": ["Process Design", "Enablement Design"],
        "grounding_phrase": "design of operations model, delivery model, technology platforms, facilities, and logistics",
        "enterprise_concern": "the design of the enterprise's execution engine and enabling infrastructure.",
        "lifecycle_concern": "designing the operations model, delivery model, technology platforms, facilities, and logistics.",
        "combined_meaning": "The analytical work of producing designs for the operations model, delivery model, technology platform architecture, facility and asset blueprint, and logistics and routing.",
    },
    {
        "filename": "dea-pc-oe-build",
        "id": "dea:pc-oe-build",
        "domain": "EnablementAndOperations",
        "stage": "Build",
        "name": "Operations and Enablement Build",
        "definition": (
            "The bounded enterprise context for **building** the production "
            "lines, delivery capability, logistics network, technology assets, "
            "and facilities of the enterprise in the **Enablement & Operations** "
            "domain. This context addresses the constructive work of standing up "
            "the execution engine and provisioning its enabling assets. "
            "v2.4.0: absorbs asset acquisition and facility provisioning from "
            "the dissolved Supply & Resources domain; supplier onboarding lives "
            "in party-relationship x build (domain-grounding.md §3.6)."
        ),
        "includes": [
            "Production line stand-up",
            "Delivery capability build",
            "Logistics network build",
            "Technology asset acquisition and installation",
            "Facility acquisition and provisioning",
        ],
        "excludes": [
            "Operations design (Design stage; adjacent context)",
            "Agent provisioning (agency-organization x build; adjacent domain)",
            "Supplier onboarding (party-relationship x build; adjacent domain)",
            "Product variant development (product-value x build; adjacent domain)",
        ],
        "outcomes": [
            "Production lines are stood up and ready for operation.",
            "Delivery capability is built and ready.",
            "Logistics network is built and connected.",
            "Technology assets are acquired and installed.",
            "Facilities are acquired and provisioned.",
        ],
        "adjacent": [
            "dea:pc-oe-conceive", "dea:pc-oe-design", "dea:pc-oe-operate", "dea:pc-oe-improve",
        ],
        "processes": ["dea:process-build-delivery-capability"],
        "l1_candidates": ["Operations Build", "Enablement Build"],
        "grounding_phrase": "build of production lines, delivery capability, logistics, technology assets, and facilities",
        "enterprise_concern": "the construction of the enterprise's execution engine and enabling assets.",
        "lifecycle_concern": "standing up production lines, building delivery capability and logistics, and provisioning technology assets and facilities.",
        "combined_meaning": "The constructive work of standing up production lines, building delivery capability and the logistics network, and acquiring and provisioning technology assets and facilities.",
    },
    {
        "filename": "dea-pc-oe-operate",
        "id": "dea:pc-oe-operate",
        "domain": "EnablementAndOperations",
        "stage": "Operate",
        "name": "Execution, Technology, and Asset Operation",
        "definition": (
            "The bounded enterprise context for **operating** the production "
            "lines, service delivery, logistics, warehouse and inventory, "
            "quality control, technology platforms, facilities, asset "
            "maintenance, and procurement cycle of the enterprise in the "
            "**Enablement & Operations** domain. This context addresses the "
            "steady-state work of running the execution engine. v2.4.0: absorbs "
            "procurement execution, facility operation, and asset maintenance "
            "from the dissolved Supply & Resources domain; supplier performance "
            "relationships live in party-relationship (domain-grounding.md §3.6)."
        ),
        "includes": [
            "Production line operation",
            "Service delivery operation",
            "Logistics operation",
            "Warehouse and inventory operation",
            "Technology platform operation",
            "Facility and asset maintenance operation",
            "Procurement cycle execution",
        ],
        "excludes": [
            "Operations build (Build stage; adjacent context)",
            "Supplier relationship management (party-relationship x operate; adjacent domain)",
            "Customer relationship operation (party-relationship x operate; adjacent domain)",
            "Product catalogue operation (product-value x operate; adjacent domain)",
            "Agent performance operation (agency-organization x operate; adjacent domain)",
        ],
        "outcomes": [
            "Production lines are run to plan.",
            "Service delivery is operated against committed levels.",
            "Logistics, warehouse, and inventory are operated.",
            "Technology platforms are operated and available.",
            "Facilities and assets are maintained.",
            "Procurement cycle is executed.",
        ],
        "adjacent": [
            "dea:pc-oe-conceive", "dea:pc-oe-design", "dea:pc-oe-build", "dea:pc-oe-improve",
        ],
        "processes": ["dea:process-operate-service-delivery"],
        "l1_candidates": ["Execution and Fulfillment", "Technology Operations", "Physical Asset Operation", "Operational Assurance"],
        "grounding_phrase": "operation of production, delivery, logistics, technology platforms, facilities, and procurement",
        "enterprise_concern": "the steady-state operation of the enterprise's execution engine.",
        "lifecycle_concern": "operating production, service delivery, logistics, technology platforms, facilities, assets, and the procurement cycle.",
        "combined_meaning": "The steady-state work of operating production lines, service delivery, logistics, warehouse and inventory, quality control, technology platforms, facilities, asset maintenance, and the procurement cycle.",
    },
    {
        "filename": "dea-pc-oe-improve",
        "id": "dea:pc-oe-improve",
        "domain": "EnablementAndOperations",
        "stage": "Improve",
        "name": "Operations and Enablement Improvement",
        "definition": (
            "The bounded enterprise context for **improving** the operations "
            "and enablement assets of the enterprise in the **Operations & "
            "Enablement** domain. This context addresses the learning and "
            "adaptation work of conducting operations performance reviews, "
            "logistics optimization, lean programmes, asset utilization "
            "optimization, and technology platform evolution. v2.4.0: absorbs "
            "asset utilization improvement from the dissolved Supply & "
            "Resources domain; supplier consolidation lives in "
            "party-relationship x improve (domain-grounding.md §3.6)."
        ),
        "includes": [
            "Operations performance review",
            "Logistics optimization",
            "Lean and continuous improvement programmes",
            "Asset utilization optimization",
            "Technology platform evolution",
        ],
        "excludes": [
            "Operations performance operation (Operate stage; adjacent context)",
            "Capability improvement (owning domains; adjacent domains)",
            "Strategic adaptation (strategy-direction x improve; adjacent domain)",
            "Supplier consolidation (party-relationship x improve; adjacent domain)",
        ],
        "outcomes": [
            "Operations performance review is conducted and findings committed.",
            "Logistics optimization is delivered.",
            "Lean programme results are realized.",
            "Asset utilization is optimized.",
            "Technology platforms are evolved.",
        ],
        "adjacent": [
            "dea:pc-oe-conceive", "dea:pc-oe-design", "dea:pc-oe-build", "dea:pc-oe-operate",
        ],
        "processes": ["dea:process-conduct-operations-performance-review"],
        "l1_candidates": ["Operations Improvement", "Enablement Improvement"],
        "grounding_phrase": "improvement of operations performance, logistics, asset utilization, and technology platforms",
        "enterprise_concern": "the improvement of the enterprise's execution engine and enabling assets.",
        "lifecycle_concern": "improving operations performance, logistics, asset utilization, and technology platforms.",
        "combined_meaning": "The learning and adaptation work of conducting operations performance reviews, logistics optimization, lean programmes, asset utilization optimization, and technology platform evolution.",
    },
]


def render_list(items, indent="    - "):
    return "\n".join(f"{indent}{i}" for i in items)


def render_adjacent_boundaries(stage, adjacent):
    lines = []
    for a in adjacent:
        short = a.replace("dea:", "")
        lines.append(f'    - "dea:{short} (adjacent context): execution flow between {stage} and the adjacent cell."')
    return "\n".join(lines)


CONTEXT_TEMPLATE = """# Process Context Cell Charter: {domain} x {stage}.
#
# Lands as part of CR-BP-21d (EnablementAndOperations landing, fourth
# unadmitted-domain tranche under ECF v2.4.0 register v2 / CR-BP-19).
# Carries the full Cell Charter (CR-BP-02 §7).
#
# v2.4.0 grounding: dea-metaframework/framework/domain-grounding.md §3.6
# (Enablement & Operations: {grounding_phrase}).
#
# Substrate independence (ADR-ECF-002 §5, CR-ECF-007): this context
# applies to biological, artificial, and hybrid agents without
# reclassification.

id: {id}
domain: {domain}
lifecycle_stage: {stage}
name: {name}

# Normative definition (PC-006).
definition: |
  {definition}

# Scope (PC-005).
scope:
  includes:
{includes_yaml}
  excludes:
{excludes_yaml}

# Intended outcomes.
outcomes:
{outcomes_yaml}

# Adjacent contexts (CR-BP-02 §11).
adjacent_contexts:
{adjacent_yaml}

# Business Processes belonging to this context (PC-008).
processes:
{processes_yaml}

# Cell Charter (CR-BP-02 §7; PC-006).
cell_charter:
  enterprise_concern: "Enablement & Operations: {enterprise_concern}"
  lifecycle_concern: "{stage}: {lifecycle_concern}"
  combined_semantic_meaning: |
    {combined_meaning}
  expected_outcomes:
{outcomes_yaml}
  inclusions:
{includes_yaml}
  exclusions:
{excludes_yaml}
  adjacent_boundaries:
{adjacent_boundaries_yaml}

# Lifecycle status (CR-BP-02 §17).
lifecycle_status: candidate
status: candidate

# Provenance.
established_by: CR-BP-21d
established_at: '{CHANGE_DATE}'

# Change history.
change_history:
  - cr: CR-BP-21d
    date: '{CHANGE_DATE}'
    change: |
      Initial Process Context record; promoted from the CR-BP-19
      register v2 (ratified against ECF v2.4.0) as part of the
      EnablementAndOperations landing tranche. Substrate-neutral
      per ADR-ECF-002 §5 / CR-ECF-007.

links:
  - rel: change-request
    href: change-requests/CR-BP-21d-enablement-operations-landing.md
  - rel: predecessor
    href: change-requests/CR-BP-19-l1-register-rederivation-ecf-v240.md
  - rel: research-register
    href: entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml
"""


for c in CONTEXTS:
    out = CTX / f"{c['filename']}.yaml"
    out.write_text(
        CONTEXT_TEMPLATE.format(
            domain=c["domain"],
            stage=c["stage"],
            id=c["id"],
            name=c["name"],
            definition=c["definition"],
            includes_yaml=render_list(c["includes"]),
            excludes_yaml=render_list(c["excludes"]),
            outcomes_yaml=render_list(c["outcomes"]),
            adjacent_yaml=render_list(c["adjacent"]),
            processes_yaml=render_list(c["processes"]),
            adjacent_boundaries_yaml=render_adjacent_boundaries(c["stage"], c["adjacent"]),
            enterprise_concern=c["enterprise_concern"],
            lifecycle_concern=c["lifecycle_concern"],
            combined_meaning=c["combined_meaning"],
            grounding_phrase=c["grounding_phrase"],
            CHANGE_DATE=CHANGE_DATE,
        )
    )
    print(f"wrote {out}")


# ----- L1 Process Group: dea:group-operations-model-conception -----

group_dir = ENT / "dea:group-operations-model-conception"
group_dir.mkdir(parents=True, exist_ok=True)
(group_dir / "candidates").mkdir(exist_ok=True)
(group_dir / "retired").mkdir(exist_ok=True)
(group_dir / "research").mkdir(exist_ok=True)

(group_dir / "README.md").write_text(
    """# Canonical Process Group: `dea:group-operations-model-conception`

This directory hosts the canonical Process Group record
for `dea:group-operations-model-conception`. The Process Group is a
catalog-owned record (not an OpenDEA metamodel entity) that organises
the Business Process responsibilities of conceiving the enterprise's
operations model and enablement approach in the **EnablementAndOperations
x Conceive** context (per ECF v2.4.0,
dea-metaframework/framework/domain-grounding.md §3.6).

Lands as part of CR-BP-21d (EnablementAndOperations landing).
Substrate-neutral: applies to biological, artificial, and hybrid agents
without reclassification (ADR-ECF-002 §5, CR-ECF-007).

Composes the L2 Business Processes assigned to the Conceive cell of
EnablementAndOperations:

- `dea:process-frame-operations-strategy` (lands under
  CR-BP-21d; remaining 3 Conceive L2s land in CR-BP-21d.1)
"""
)

(group_dir / "dea:group-operations-model-conception.yaml").write_text(
    f"""id: dea:group-operations-model-conception
type: ProcessGroup
version: 1.0.0

name: Operations Model Conception

# Normative definition (PG-006 / MECE).
definition: |
  The bounded Process Group that organises the Business Process
  responsibilities of conceiving the enterprise's operations model and
  enablement approach in the EnablementAndOperations x Conceive
  context. This group covers the front-end work of framing the
  operations strategy, the delivery model, the technology enablement
  approach, and the physical asset approach. v2.4.0 grounding
  (domain-grounding.md §3.6): the domain manages the enterprise's
  execution engine and the means that make execution possible,
  including the physical, virtual, and procedural infrastructure
  absorbed from the dissolved Supply & Resources domain.

# Process Context reference (PG-003 enforces resolution).
process_context: dea:pc-oe-conceive

# Scope (MECE boundary; PG-006 depends on excludes).
scope:
  includes:
    - Operations strategy framing
    - Delivery model conception
    - Technology enablement approach framing
    - Physical asset approach framing
  excludes:
    - Customer strategy (party-relationship x conceive)
    - Strategic direction for operations (strategy-direction x conceive)
    - Supplier relationship conception (party-relationship x conceive)
    - Operations model design (Design stage; adjacent context)
    - Operations build (Build stage; adjacent context)

# Intended enterprise outcomes.
outcomes:
  - Operations strategy is framed for the enterprise.
  - Delivery model is conceived with bounded scope.
  - Technology enablement approach is framed.
  - Physical asset approach is framed.

# Canonical containment (PG-004 / PG-005 / PG-006 enforce).
composes:
  - source_id: dea:group-operations-model-conception
    target_id: dea:process-frame-operations-strategy
    relationship_type: composes
    direction: source-to-target
    status: active
    asserted_by: dea-team
    rationale: |
      The L2 process frames the enterprise's operations strategy,
      which is the v2.4.0 principal responsibility of the
      EnablementAndOperations x Conceive cell. Lands under CR-BP-21d.
    evidence: docs/examples/frame-operations-strategy.md
    provenance:
      type: architecture-review
      reference: CR-BP-21d
      asserted_by: dea-team
      asserted_at: '{CHANGE_DATE}'

# Process Group kind (PG-007 enforces controlled vocabulary).
process_group_kind: end-to-end

# Discovery / governance status (mirrors CR-BP-19 register values).
status: accepted

# Catalog entry lifecycle (PG-008 enforces).
lifecycle_status: candidate

# ECF Conformance Gate (CR-ECF-CG-001..004).
ecfConformance:
  framework: EnterpriseConceptFramework
  contractVersion: '1.0.0'
  profile: dea:ecf@1.0.0
  status: conformant
  affiliation: inherits-catalog
  canonicalReferences:
    - kind: coordinate
      domain: EnablementAndOperations
      stage: Conceive
      identifier: ecf:enablementAndOperations.conceive

# Evidence (CR-BP-11 register strength scale E0..E5).
evidence:
  - source: CR-BP-19 (register v2, ratified against ECF v2.4.0)
    claim: |
      This Process Group's coordinate is ratified-accepted in register
      v2. CR-BP-21d lands the corresponding L1 group; remaining 3
      register v2 L2 candidates for Conceive land in CR-BP-21d.1.
    strength: E4
    reference: entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml

# Metadata (PG-006 cross-context overlap exception path lives here).
metadata:
  established_by: CR-BP-21d
  established_at: '{CHANGE_DATE}'
  cross_context_overlap: []
  change_history:
    - cr: CR-BP-21d
      date: '{CHANGE_DATE}'
      change: |
        Initial Process Group record; promoted from the CR-BP-19 register
        v2 (ratified against ECF v2.4.0) as part of the
        EnablementAndOperations landing tranche. Composes the L2
        dea:process-frame-operations-strategy.

links:
  - rel: change-request
    href: change-requests/CR-BP-21d-enablement-operations-landing.md
  - rel: predecessor
    href: change-requests/CR-BP-19-l1-register-rederivation-ecf-v240.md
  - rel: research-register
    href: entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml
"""
)
print(f"wrote {group_dir}/dea:group-operations-model-conception.yaml")


# ----- 5 L2 processes -----

L2_TEMPLATES = {
    "dea:process-frame-operations-strategy": {
        "name": "Frame Operations Strategy",
        "intent": "develop",
        "ptype": "management",
        "context": "dea:pc-oe-conceive",
        "verb": "Frame",
        "object": "Operations Strategy",
        "scope": "(all enterprise segments)",
        "trigger": "An operations strategy is needed because the enterprise is establishing a new execution engine, reframing an existing one, or responding to delivery model shifts that require a re-conception of the operations model and enablement approach.",
        "description": "Operate the Frame Operations Strategy L2 process within the dea:pc-oe-conceive Cell Charter. See trigger and outcome for the bounded work this process owns; see identity.outcome_statement for the testable outcome the process produces.",
        "outcome": "An operations strategy with bounded delivery model, technology enablement approach, and physical asset approach is committed.",
        "outcome_statement": "An operations strategy with bounded delivery model, technology enablement approach, and physical asset approach is committed and ready to drive Design-stage planning.",
        "evidence_links": [
            {"type": "standard", "ref": "https://www.apqc.org/resource-overview/resource-library/apqc-process-classification-framework-pcf"},
        ],
    },
    "dea:process-design-operations-model": {
        "name": "Design Operations Model",
        "intent": "develop",
        "ptype": "management",
        "context": "dea:pc-oe-design",
        "verb": "Design",
        "object": "Operations Model",
        "scope": "(all enterprise segments)",
        "trigger": "An operations model design is needed because the framed operations strategy requires bounded delivery model design, technology platform architecture, facility and asset blueprint, and logistics and routing design.",
        "description": "Operate the Design Operations Model L2 process within the dea:pc-oe-design Cell Charter. See trigger and outcome for the bounded work this process owns; see identity.outcome_statement for the testable outcome the process produces.",
        "outcome": "An operations model design with bounded delivery model, technology platform architecture, facility blueprint, and logistics routing is committed.",
        "outcome_statement": "An operations model design with bounded delivery model, technology platform architecture, facility blueprint, and logistics routing is committed and ready for Build-stage planning.",
        "evidence_links": [
            {"type": "standard", "ref": "https://www.apqc.org/resource-overview/resource-library/apqc-process-classification-framework-pcf"},
        ],
    },
    "dea:process-build-delivery-capability": {
        "name": "Build Delivery Capability",
        "intent": "develop",
        "ptype": "core",
        "context": "dea:pc-oe-build",
        "verb": "Build",
        "object": "Delivery Capability",
        "scope": "(all enterprise segments)",
        "trigger": "A delivery capability build is needed because the designed operations model requires bounded stand-up of production lines, delivery capability, logistics network, technology assets, and facilities.",
        "description": "Operate the Build Delivery Capability L2 process within the dea:pc-oe-build Cell Charter. See trigger and outcome for the bounded work this process owns; see identity.outcome_statement for the testable outcome the process produces.",
        "outcome": "Delivery capability is built with production lines stood up, logistics network connected, and technology assets and facilities provisioned.",
        "outcome_statement": "Delivery capability is built with production lines stood up, logistics network connected, and technology assets and facilities provisioned, ready for the Operate cell.",
        "evidence_links": [
            {"type": "standard", "ref": "https://www.apqc.org/resource-overview/resource-library/apqc-process-classification-framework-pcf"},
        ],
    },
    "dea:process-operate-service-delivery": {
        "name": "Operate Service Delivery",
        "intent": "operate",
        "ptype": "core",
        "context": "dea:pc-oe-operate",
        "verb": "Operate",
        "object": "Service Delivery",
        "scope": "(all enterprise segments)",
        "trigger": "Service delivery operation is needed because the built execution engine is now in active operation and requires steady-state production, delivery, logistics, technology platform, facility, and procurement operation.",
        "description": "Operate the Operate Service Delivery L2 process within the dea:pc-oe-operate Cell Charter. See trigger and outcome for the bounded work this process owns; see identity.outcome_statement for the testable outcome the process produces.",
        "outcome": "Service delivery is operated with production lines run to plan, logistics and inventory operated, and technology platforms and facilities maintained.",
        "outcome_statement": "Service delivery is operated with production lines run to plan, logistics and inventory operated, technology platforms available, facilities and assets maintained, and the procurement cycle executed.",
        "evidence_links": [
            {"type": "standard", "ref": "https://www.apqc.org/resource-overview/resource-library/apqc-process-classification-framework-pcf"},
        ],
    },
    "dea:process-conduct-operations-performance-review": {
        "name": "Conduct Operations Performance Review",
        "intent": "develop",
        "ptype": "management",
        "context": "dea:pc-oe-improve",
        "verb": "Conduct",
        "object": "Operations Performance Review",
        "scope": "(all enterprise segments)",
        "trigger": "An operations performance review is needed because performance signals, logistics gaps, or asset utilization targets indicate that the execution engine or its enabling assets need to be evolved.",
        "description": "Operate the Conduct Operations Performance Review L2 process within the dea:pc-oe-improve Cell Charter. See trigger and outcome for the bounded work this process owns; see identity.outcome_statement for the testable outcome the process produces.",
        "outcome": "Operations performance review is conducted with findings committed for logistics optimization, asset utilization, and technology platform evolution.",
        "outcome_statement": "Operations performance review is conducted with findings committed for logistics optimization, asset utilization, and technology platform evolution, ready to drive the next planning cycle.",
        "evidence_links": [
            {"type": "standard", "ref": "https://www.apqc.org/resource-overview/resource-library/apqc-process-classification-framework-pcf"},
        ],
    },
}


L2_TEMPLATE = """id: {eid}
name: {name}
type: Process
version: 1.0.0
lifecycle_status: candidate
status: candidate
process_intent: {intent}
process_type: {ptype}
process_specialization: []
description: '{description}
  '
trigger: '{trigger}
  '
outcome: '{outcome}
  '
identity:
  verb: {verb}
  object: {object}
  scope: {scope}
  outcome_statement: '{outcome_statement}
    '
  evidence_links:
{evidence_yaml}
relationships:
- source_id: {eid}
  relationship_type: serves
  target_id: {ecf_id}
ecfConformance:
  framework: EnterpriseConceptFramework
  contractVersion: 1.0.0
  profile: dea:ecf@1.0.0
  status: conformant
  affiliation: inherits-catalog
  canonicalReferences:
  - kind: coordinate
    domain: {domain}
    stage: {stage}
    identifier: ecf:{ecf_domain}.{ecf_stage}
metadata:
  established_by: CR-BP-21d
  established_at: '{CHANGE_DATE}'
  change_history:
  - cr: CR-BP-21d
    date: '{CHANGE_DATE}'
    change: |
      Initial L2 Process entry; lands as part of the CR-BP-21d
      EnablementAndOperations landing tranche under ECF v2.4.0
      register v2 (CR-BP-19). Substrate-neutral per ADR-ECF-002
      §5 / CR-ECF-007: applies to biological, artificial, and
      hybrid agents without reclassification. One of the 5 L2
      landings targeting the 5 ratified cells of the
      EnablementAndOperations domain.
links:
- rel: change-request
  href: change-requests/CR-BP-21d-enablement-operations-landing.md
- rel: process-context
  href: contexts/v1-alpha/{context_file}.yaml
context:
- ref: {context_id}
"""


def render_evidence(links):
    return "\n".join(f'  - type: {l["type"]}\n    ref: {l["ref"]}' for l in links)


ECF_DOMAIN_MAP = {
    "EnablementAndOperations": "enablementAndOperations",
}


for eid, t in L2_TEMPLATES.items():
    pdir = ENT / eid
    pdir.mkdir(parents=True, exist_ok=True)
    (pdir / "candidates").mkdir(exist_ok=True)
    (pdir / "retired").mkdir(exist_ok=True)
    (pdir / "research").mkdir(exist_ok=True)
    context_id = t["context"]
    context_file = context_id.replace("dea:", "").replace(":", "-")
    domain = "EnablementAndOperations"
    stage = context_id.split("-")[-1]
    stage_title = stage.capitalize()
    ecf_domain = ECF_DOMAIN_MAP[domain]
    ecf_stage = stage
    (pdir / "README.md").write_text(
        f"""# Canonical L2 Business Process: `{eid}`

This directory hosts the canonical L2 Business Process record
for `{eid}`. Lands as part of CR-BP-21d (EnablementAndOperations
landing). Process Context: `{context_id}`. Substrate-neutral
(ADR-ECF-002 §5 / CR-ECF-007): applies to biological, artificial,
and hybrid agents without reclassification.
"""
    )
    (pdir / f"{eid}.yaml").write_text(
        L2_TEMPLATE.format(
            eid=eid,
            name=t["name"],
            intent=t["intent"],
            ptype=t["ptype"],
            description=t["description"],
            trigger=t["trigger"],
            outcome=t["outcome"],
            outcome_statement=t["outcome_statement"],
            verb=t["verb"],
            object=t["object"],
            scope=t["scope"],
            evidence_yaml=render_evidence(t["evidence_links"]),
            context=context_id,
            context_id=context_id,
            context_file=context_file,
            domain=domain,
            stage=stage_title,
            ecf_id=f"ecf:{ecf_domain}.{ecf_stage}",
            ecf_domain=ecf_domain,
            ecf_stage=ecf_stage,
            CHANGE_DATE=CHANGE_DATE,
        )
    )
    print(f"wrote {pdir}/{eid}.yaml")


print("\nDone. Next: regenerate CATALOG.yaml, append dispositions + tranche entries, run gates.")
