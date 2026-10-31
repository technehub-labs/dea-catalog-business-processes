#!/usr/bin/env python3
"""Generate the remaining CR-BP-21a artifacts: 4 process contexts, 1 L1
group, 4 L2 processes, and the L2 migration (process-develop-governance-strategy
-> process-develop-corporate-strategy, with a deprecation README at the
old path).

One-shot — kept under scripts/ for reproducibility per the team's
process-tooling convention (see scripts/apply_phase_5_tranche.py for
the prior pattern).

Run: python scripts/apply_phase_7a_tranche.py
"""
from __future__ import annotations
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
CTX = ROOT / "contexts/v1-alpha"
ENT = ROOT / "entities/v1-alpha"
CHANGE_DATE = "2026-09-07"


# ----- Process Contexts (4) -----

CONTEXTS = [
    {
        "filename": "dea-pc-sd-design",
        "id": "dea:pc-sd-design",
        "domain": "StrategyAndDirection",
        "stage": "Design",
        "name": "Strategic Choices Design",
        "definition": (
            "The bounded enterprise context for **designing** the strategic choices, "
            "alternatives, objectives, and scenarios of the enterprise in the **Strategy & "
            "Direction** domain. This context addresses the analytical work of producing "
            "designs for strategic options, evaluating alternatives, defining objectives "
            "and targets, and framing scenarios. v2.4.0: design mechanics that translate "
            "conceived strategic intent into candidate options and choices."
        ),
        "includes": [
            "Strategic option design",
            "Strategic alternative evaluation",
            "Objectives and targets design",
            "Strategic scenario design",
        ],
        "excludes": [
            "Strategic intent conception (Conceive stage; adjacent context)",
            "Strategic plan and roadmap build (Build stage; adjacent context)",
            "Operational planning (enablement-operations x design)",
            "Financial plan design (finance-accounting x design)",
        ],
        "outcomes": [
            "Strategic options are designed with bounded trade-offs.",
            "Strategic alternatives are evaluated against stated criteria.",
            "Objectives and targets are designed and committed.",
            "Strategic scenarios are framed for resilience assessment.",
        ],
        "adjacent": [
            "dea:pc-sd-conceive", "dea:pc-sd-build", "dea:pc-sd-operate", "dea:pc-sd-improve",
        ],
        "processes": ["dea:process-design-strategic-options"],
        "l1_candidates": ["Strategic Choices Design", "Objectives and Targets Design"],
        "grounding_phrase": "design of strategic choices, alternatives, objectives, scenarios",
        "enterprise_concern": "the design of strategic choices and trade-offs.",
        "lifecycle_concern": "designing options, evaluating alternatives, defining objectives and scenarios.",
        "combined_meaning": "The analytical work of producing designs for strategic options, alternatives, objectives, and scenarios from the conceived intent.",
    },
    {
        "filename": "dea-pc-sd-build",
        "id": "dea:pc-sd-build",
        "domain": "StrategyAndDirection",
        "stage": "Build",
        "name": "Strategic Plan Build",
        "definition": (
            "The bounded enterprise context for **building** the strategic plan, "
            "roadmap, and initiative portfolio of the enterprise in the **Strategy & "
            "Direction** domain. This context addresses the constructive work of "
            "translating designed strategic choices into a plan, building a roadmap, "
            "translating choices into initiatives, and setting resource allocation "
            "priorities. v2.4.0: the plan artefact construction; capability build "
            "remains in the receiving domain."
        ),
        "includes": [
            "Strategic plan build",
            "Strategic roadmap build",
            "Strategic choice-to-initiative translation",
            "Resource allocation priority setting",
        ],
        "excludes": [
            "Strategic option design (Design stage; adjacent context)",
            "Budget construction (finance-accounting x build)",
            "Capability build (owning domains)",
        ],
        "outcomes": [
            "Strategic plan is built and versioned.",
            "Strategic roadmap is built and committed.",
            "Strategic choices are translated into an initiative portfolio.",
            "Resource allocation priorities are set within the authorised frame.",
        ],
        "adjacent": [
            "dea:pc-sd-design", "dea:pc-sd-operate", "dea:pc-sd-improve", "dea:pc-sd-conceive",
        ],
        "processes": ["dea:process-build-strategic-plan"],
        "l1_candidates": ["Strategic Plan Build", "Strategic Roadmap Build"],
        "grounding_phrase": "construction of the strategic plan, roadmap, and initiative portfolio",
        "enterprise_concern": "the construction of the strategic plan and roadmap.",
        "lifecycle_concern": "translating strategic choices into a plan, roadmap, and initiative portfolio.",
        "combined_meaning": "The constructive work of translating designed strategic choices into a versioned plan, roadmap, and initiative portfolio.",
    },
    {
        "filename": "dea-pc-sd-operate",
        "id": "dea:pc-sd-operate",
        "domain": "StrategyAndDirection",
        "stage": "Operate",
        "name": "Strategic Steering Operation",
        "definition": (
            "The bounded enterprise context for **operating** the strategic steering, "
            "environmental sensing, and strategic review cycle of the enterprise in the "
            "**Strategy & Direction** domain. This context addresses the steady-state "
            "work of monitoring strategic performance, sensing environmental signals, "
            "steering the initiative portfolio, and operating the strategic review cycle. "
            "v2.4.0: monitoring and steering the strategy as a stable subject; "
            "operational performance management lives in Enablement & Operations."
        ),
        "includes": [
            "Strategic performance monitoring",
            "Environmental sensing",
            "Initiative portfolio steering",
            "Strategic review cycle operation",
        ],
        "excludes": [
            "Operational performance management (enablement-operations x operate)",
            "Initiative execution (enablement-operations x operate)",
            "Strategic adaptation (Improve stage; adjacent context)",
        ],
        "outcomes": [
            "Strategic performance is monitored against the plan.",
            "Environmental signals are sensed and contextualised.",
            "Initiative portfolio is steered in line with strategic intent.",
            "Strategic review cycle is operated on a defined cadence.",
        ],
        "adjacent": [
            "dea:pc-sd-conceive", "dea:pc-sd-design", "dea:pc-sd-build", "dea:pc-sd-improve",
        ],
        "processes": ["dea:process-monitor-strategic-performance"],
        "l1_candidates": ["Strategic Steering Operation", "Environmental Sensing Operation"],
        "grounding_phrase": "monitoring, environmental sensing, and steering of strategic performance",
        "enterprise_concern": "the steady-state steering of strategic performance.",
        "lifecycle_concern": "monitoring strategic performance and operating the review cycle.",
        "combined_meaning": "The steady-state work of monitoring strategic performance, sensing environmental signals, and steering the initiative portfolio in line with the plan.",
    },
    {
        "filename": "dea-pc-sd-improve",
        "id": "dea:pc-sd-improve",
        "domain": "StrategyAndDirection",
        "stage": "Improve",
        "name": "Strategic Adaptation",
        "definition": (
            "The bounded enterprise context for **adapting** the strategic direction, "
            "objectives, and effectiveness of the enterprise in the **Strategy & "
            "Direction** domain. This context addresses the learning and adaptation "
            "work of refreshing objectives, adapting strategic direction, and reviewing "
            "strategy effectiveness. v2.4.0: adaptation and refresh as a stable subject; "
            "capability improvement remains in the owning domain."
        ),
        "includes": [
            "Strategic direction adaptation",
            "Objectives and targets refresh",
            "Strategy effectiveness review",
        ],
        "excludes": [
            "Strategic performance monitoring (Operate stage; adjacent context)",
            "Capability improvement (owning domains)",
        ],
        "outcomes": [
            "Strategic direction is adapted to changing context.",
            "Objectives and targets are refreshed as needed.",
            "Strategy effectiveness is reviewed and learned from.",
        ],
        "adjacent": [
            "dea:pc-sd-conceive", "dea:pc-sd-design", "dea:pc-sd-build", "dea:pc-sd-operate",
        ],
        "processes": ["dea:process-adapt-strategic-direction"],
        "l1_candidates": ["Strategic Adaptation"],
        "grounding_phrase": "adaptation, objectives refresh, and effectiveness review",
        "enterprise_concern": "the adaptation and refresh of strategic direction.",
        "lifecycle_concern": "adapting strategic direction and refreshing objectives and targets.",
        "combined_meaning": "The learning and adaptation work of refreshing objectives, adapting strategic direction, and reviewing strategy effectiveness.",
    },
]


def render_list(items, indent="    - "):
    return "\n".join(f"{indent}{i}" for i in items)


def render_adjacent_boundaries(stage, adjacent):
    lines = []
    for a in adjacent:
        short = a.replace("dea:", "")
        lines.append(f'    - "dea:{short} (adjacent context): strategy flows between {stage} and the adjacent cell."')
    return "\n".join(lines)


CONTEXT_TEMPLATE = """# Process Context Cell Charter: {domain} x {stage}.
#
# Lands as part of CR-BP-21a (StrategyAndDirection landing, first
# unadmitted-domain tranche under ECF v2.4.0 register v2 / CR-BP-19).
# Carries the full Cell Charter (CR-BP-02 §7).
#
# v2.4.0 grounding: dea-metaframework/framework/domain-grounding.md §3.2
# (Strategy & Direction: {grounding_phrase}).

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
  enterprise_concern: "Strategy & Direction: {enterprise_concern}"
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
established_by: CR-BP-21a
established_at: '{CHANGE_DATE}'

# Change history.
change_history:
  - cr: CR-BP-21a
    date: '{CHANGE_DATE}'
    change: |
      Initial Process Context record; promoted from the CR-BP-19
      register v2 (ratified against ECF v2.4.0) as part of the
      StrategyAndDirection landing tranche.

links:
  - rel: change-request
    href: change-requests/CR-BP-21a-strategy-direction-landing.md
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


# ----- L1 Process Group: dea:group-strategy-direction-conception -----

group_dir = ENT / "dea:group-strategy-direction-conception"
group_dir.mkdir(parents=True, exist_ok=True)
(group_dir / "candidates").mkdir(exist_ok=True)
(group_dir / "retired").mkdir(exist_ok=True)
(group_dir / "research").mkdir(exist_ok=True)

# README
(group_dir / "README.md").write_text(
    """# Canonical Process Group: `dea:group-strategy-direction-conception`

This directory hosts the canonical Process Group record
for `dea:group-strategy-direction-conception`. The Process Group is a
catalog-owned record (not an OpenDEA metamodel entity) that organises
the Business Process responsibilities of conceiving strategic direction
in the **StrategyAndDirection × Conceive** context (per ECF v2.4.0,
dea-metaframework/framework/domain-grounding.md §3.2).

Lands as part of CR-BP-21a (StrategyAndDirection landing). Composes the
L2 Business Processes assigned to the Conceive cell of
StrategyAndDirection:

- `dea:process-develop-corporate-strategy` (migrated from
  `dea:process-develop-governance-strategy` in governance-existence x
  conceive, per CR-BP-20 Option A split)
- (Future) L2s for enterprise purpose and ambition, strategic intent
  conception, and strategic horizons framing (CR-BP-21a.1).
"""
)

# YAML
(group_dir / "dea:group-strategy-direction-conception.yaml").write_text(
    f"""id: dea:group-strategy-direction-conception
type: ProcessGroup
version: 1.0.0

name: Strategy and Direction Conception

# Normative definition (PG-006 / MECE).
definition: |
  The bounded Process Group that organises the Business Process
  responsibilities of conceiving the enterprise's strategic direction
  in the StrategyAndDirection × Conceive context. This group covers the
  front-end work of framing the enterprise's purpose, ambition, strategic
  intent, strategic horizons, and corporate strategy. v2.4.0 grounding:
  Strategy & Direction directs the enterprise's deliberate choice of
  trajectory within the authorised frame (governance-existence x conceive
  authorises; strategy-direction x conceive directs).

# Process Context reference (PG-003 enforces resolution).
process_context: dea:pc-sd-conceive

# Scope (MECE boundary; PG-006 depends on excludes).
scope:
  includes:
    - Purpose and ambition conception
    - Strategic intent conception
    - Strategic horizons framing
    - Corporate strategy development
  excludes:
    - Constitutional mandate and authority (governance-existence x conceive)
    - Charter and policy conception (governance-existence x conceive)
    - Strategic option design (Design stage; adjacent context)
    - Strategic plan and roadmap build (Build stage; adjacent context)
    - Initiative execution (enablement-operations)

# Intended enterprise outcomes.
outcomes:
  - Enterprise purpose and ambition are framed and articulated.
  - Strategic intent is committed with a defined trajectory.
  - Strategic horizons are framed and bounded.
  - Corporate strategy is developed within the authorised frame.

# Canonical containment (PG-004 / PG-005 / PG-006 enforce).
# CR-BP-21a tranche composes 1 L2 (the corporate-strategy migration
# target); the remaining 3 register v2 candidates land in CR-BP-21a.1.
composes:
  - source_id: dea:group-strategy-direction-conception
    target_id: dea:process-develop-corporate-strategy
    relationship_type: composes
    direction: source-to-target
    status: active
    asserted_by: dea-team
    rationale: |
      The L2 process develops corporate strategy, which is the v2.4.0
      principal responsibility of the StrategyAndDirection x Conceive
      cell. It migrated from governance-existence x conceive under
      the user-approved Option A split (CR-BP-20) and lands in this
      group under CR-BP-21a.
    evidence: docs/examples/develop-corporate-strategy.md
    provenance:
      type: architecture-review
      reference: CR-BP-21a
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
      domain: StrategyAndDirection
      stage: Conceive
      identifier: ecf:strategyDirection.conceive

# Evidence (CR-BP-11 register strength scale E0..E5).
evidence:
  - source: CR-BP-19 (register v2, ratified against ECF v2.4.0)
    claim: |
      This Process Group's coordinate is ratified-accepted in register
      v2. CR-BP-21a lands the corresponding L1 group; remaining 3
      register v2 L2 candidates land in CR-BP-21a.1.
    strength: E4
    reference: entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml

# Metadata (PG-006 cross-context overlap exception path lives here).
metadata:
  established_by: CR-BP-21a
  established_at: '{CHANGE_DATE}'
  cross_context_overlap: []
  change_history:
    - cr: CR-BP-21a
      date: '{CHANGE_DATE}'
      change: |
        Initial Process Group record; promoted from the CR-BP-19 register
        v2 (ratified against ECF v2.4.0) as part of the StrategyAndDirection
        landing tranche. Composes the migrated L2
        dea:process-develop-corporate-strategy (formerly
        dea:process-develop-governance-strategy; CR-BP-20 Option A split).

links:
  - rel: change-request
    href: change-requests/CR-BP-21a-strategy-direction-landing.md
  - rel: predecessor
    href: change-requests/CR-BP-19-l1-register-rederivation-ecf-v240.md
  - rel: predecessor
    href: change-requests/CR-BP-20-l1-l2-alignment-ecf-v240.md
  - rel: research-register
    href: entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml
"""
)
print(f"wrote {group_dir}/dea:group-strategy-direction-conception.yaml")


# ----- 4 new L2 processes (the migration target dea:process-develop-corporate-strategy
#       is a separate dedicated handler below; this is for the other 4). -----

L2_TEMPLATES = {
    "dea:process-design-strategic-options": {
        "name": "Design Strategic Options",
        "intent": "develop",
        "ptype": "management",
        "context": "dea:pc-sd-design",
        "verb": "Design",
        "object": "Strategic Options",
        "scope": "(all enterprise segments)",
        "trigger": "A new set of strategic options is needed because the conceived strategic intent requires bounded trade-off designs to evaluate.",
        "description": "Operate the Design Strategic Options L2 process within the dea:pc-sd-design Cell Charter. See trigger and outcome for the bounded work this process owns; see identity.outcome_statement for the testable outcome the process produces.",
        "outcome": "A set of strategic option designs with bounded trade-offs and evaluation criteria is committed.",
        "outcome_statement": "A set of strategic option designs with bounded trade-offs and evaluation criteria is committed and ready for evaluation and translation.",
        "evidence_links": [
            {"type": "standard", "ref": "https://www.apqc.org/resource-overview/resource-library/apqc-process-classification-framework-pcf"},
        ],
    },
    "dea:process-build-strategic-plan": {
        "name": "Build Strategic Plan",
        "intent": "develop",
        "ptype": "management",
        "context": "dea:pc-sd-build",
        "verb": "Build",
        "object": "Strategic Plan",
        "scope": "(all enterprise segments)",
        "trigger": "A strategic plan build is required because the designed choices and alternatives have been evaluated and a chosen path needs to be articulated as a versioned plan and roadmap.",
        "description": "Operate the Build Strategic Plan L2 process within the dea:pc-sd-build Cell Charter. See trigger and outcome for the bounded work this process owns; see identity.outcome_statement for the testable outcome the process produces.",
        "outcome": "A versioned strategic plan with roadmap and initiative portfolio is built and committed.",
        "outcome_statement": "A versioned strategic plan with roadmap and initiative portfolio is built and committed, with resource allocation priorities set within the authorised frame.",
        "evidence_links": [
            {"type": "standard", "ref": "https://www.apqc.org/resource-overview/resource-library/apqc-process-classification-framework-pcf"},
        ],
    },
    "dea:process-monitor-strategic-performance": {
        "name": "Monitor Strategic Performance",
        "intent": "operate",
        "ptype": "core",
        "context": "dea:pc-sd-operate",
        "verb": "Operate",
        "object": "Strategic Performance Monitoring",
        "scope": "(all enterprise segments)",
        "trigger": "A strategic review cycle is open because the plan is in execution and strategic performance requires ongoing monitoring and steering.",
        "description": "Operate the Monitor Strategic Performance L2 process within the dea:pc-sd-operate Cell Charter. See trigger and outcome for the bounded work this process owns; see identity.outcome_statement for the testable outcome the process produces.",
        "outcome": "Strategic performance is monitored against the plan, environmental signals are sensed, and the initiative portfolio is steered in line with strategic intent.",
        "outcome_statement": "Strategic performance is monitored against the plan, environmental signals are sensed, and the initiative portfolio is steered in line with strategic intent, with the strategic review cycle operated on a defined cadence.",
        "evidence_links": [
            {"type": "standard", "ref": "https://www.apqc.org/resource-overview/resource-library/apqc-process-classification-framework-pcf"},
        ],
    },
    "dea:process-adapt-strategic-direction": {
        "name": "Adapt Strategic Direction",
        "intent": "develop",
        "ptype": "management",
        "context": "dea:pc-sd-improve",
        "verb": "Develop",
        "object": "Strategic Adaptation",
        "scope": "(all enterprise segments)",
        "trigger": "Strategic adaptation is required because environmental signals, performance monitoring, or effectiveness review indicate that the strategic direction needs to be refreshed or adapted.",
        "description": "Operate the Adapt Strategic Direction L2 process within the dea:pc-sd-improve Cell Charter. See trigger and outcome for the bounded work this process owns; see identity.outcome_statement for the testable outcome the process produces.",
        "outcome": "Strategic direction is adapted, objectives and targets are refreshed, and strategy effectiveness is reviewed.",
        "outcome_statement": "Strategic direction is adapted, objectives and targets are refreshed, and strategy effectiveness is reviewed and learned from, ready to drive the next planning cycle.",
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
  established_by: CR-BP-21a
  established_at: '{CHANGE_DATE}'
  change_history:
  - cr: CR-BP-21a
    date: '{CHANGE_DATE}'
    change: |
      Initial L2 Process entry; lands as part of the CR-BP-21a
      StrategyAndDirection landing tranche under ECF v2.4.0
      register v2 (CR-BP-19). One of the 5 L2 landings
      targeting the 5 ratified cells of the StrategyAndDirection
      domain.
links:
- rel: change-request
  href: change-requests/CR-BP-21a-strategy-direction-landing.md
- rel: process-context
  href: contexts/v1-alpha/{context_file}.yaml
context:
- ref: {context_id}
"""


def render_evidence(links):
    return "\n".join(f'  - type: {l["type"]}\n    ref: {l["ref"]}' for l in links)


ECF_DOMAIN_MAP = {
    "StrategyAndDirection": "strategyAndDirection",
}


for eid, t in L2_TEMPLATES.items():
    pdir = ENT / eid
    pdir.mkdir(parents=True, exist_ok=True)
    (pdir / "candidates").mkdir(exist_ok=True)
    (pdir / "retired").mkdir(exist_ok=True)
    (pdir / "research").mkdir(exist_ok=True)
    context_id = t["context"]
    context_file = context_id.replace("dea:", "").replace(":", "-")
    domain = "StrategyAndDirection"
    stage = context_id.split("-")[-1]
    stage_title = stage.capitalize()  # Operate, Improve, Design, Build
    ecf_domain = ECF_DOMAIN_MAP[domain]
    ecf_stage = stage  # identifier uses lowercase
    (pdir / "README.md").write_text(
        f"""# Canonical L2 Business Process: `{eid}`

This directory hosts the canonical L2 Business Process record
for `{eid}`. Lands as part of CR-BP-21a (StrategyAndDirection
landing). Process Context: `{context_id}`.
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


# ----- L2 migration: dea:process-develop-governance-strategy ->
#       dea:process-develop-corporate-strategy (new path; old path gets
#       deprecation README + deprecation status in its own change_history). -----

new_l2 = ENT / "dea:process-develop-corporate-strategy"
new_l2.mkdir(parents=True, exist_ok=True)
(new_l2 / "candidates").mkdir(exist_ok=True)
(new_l2 / "retired").mkdir(exist_ok=True)
(new_l2 / "research").mkdir(exist_ok=True)

(new_l2 / "README.md").write_text(
    """# Canonical L2 Business Process: `dea:process-develop-corporate-strategy`

This directory hosts the canonical L2 Business Process record
for `dea:process-develop-corporate-strategy`. Process Context:
`dea:pc-sd-conceive`.

This L2 migrated from `dea:process-develop-governance-strategy`
(governance-existence x conceive) under the user-approved Option A
split in CR-BP-20 (2026-09-07). The migration grounds the placement
in dea-metaframework/framework/domain-grounding.md §3.1 ("Governance
authorizes but does not direct; Strategy & Direction directs within
the authorized frame") and §3.2 (Strategy & Direction owns purpose,
ambition, strategic intent, corporate strategy conception).

The previous L2 entry remains at
`dea:process-develop-governance-strategy/` with `lifecycle_status:
deprecated` and a redirect README for any external link.
"""
)

(new_l2 / "dea:process-develop-corporate-strategy.yaml").write_text(
    f"""id: dea:process-develop-corporate-strategy
name: Develop Corporate Strategy
type: Process
version: 2.0.0
lifecycle_status: candidate
status: candidate
process_intent: develop
process_type: management
process_specialization: []
description: 'Operate the Develop Corporate Strategy L2 process within the
  dea:pc-sd-conceive Cell Charter. See trigger and outcome for
  the bounded work this process owns; see identity.outcome_statement
  for the testable outcome the process produces.

  '
trigger: 'A new corporate strategy is needed because the enterprise is establishing
  a new strategic trajectory, reframing an existing one, or responding to environmental
  signals that require board-level strategic realignment.

  '
outcome: 'A corporate strategy with bounded ambition, strategic intent, and
  choice of trajectory is committed.

  '
identity:
  verb: Develop
  object: Corporate Strategy
  scope: (all enterprise segments)
  outcome_statement: 'A corporate strategy with bounded ambition, strategic intent,
    and choice of trajectory is committed and ready to drive Design work.

    '
  evidence_links:
  - type: standard
    ref: https://www.iso.org/standard/27036.html
  - type: documentation
    ref: docs/examples/develop-corporate-strategy.md
relationships:
- source_id: dea:process-develop-corporate-strategy
  relationship_type: serves
  target_id: ecf:strategyDirection.conceive
ecfConformance:
  framework: EnterpriseConceptFramework
  contractVersion: 1.0.0
  profile: dea:ecf@1.0.0
  status: conformant
  affiliation: inherits-catalog
  canonicalReferences:
  - kind: coordinate
    domain: StrategyAndDirection
    stage: Conceive
    identifier: ecf:strategyDirection.conceive
metadata:
  established_by: CR-BP-21a
  established_at: '{CHANGE_DATE}'
  supersedes: dea:process-develop-governance-strategy (v1.0.0; CR-BP-13a)
  change_history:
  - cr: CR-BP-13a
    date: '2026-09-05'
    change: |
      Original L2 entry (id: dea:process-develop-governance-strategy) lands
      as part of the CR-BP-13a admission tranche. Affiliated with
      governance-existence x conceive.
  - cr: CR-BP-15-IMP
    phase: phase-5
    date: '2026-09-06'
    change: |
      Phase 5 tranche migration (under original id):
      legacy intent migrated to canonical vocabulary;
      legacy scalar `process_context` migrated to canonical
      `context:` block; legacy `process_audience` removed;
      canonical `serves` relationship toward the ECF coordinate added.
  - cr: CR-BP-20
    date: '2026-09-07'
    change: |
      CR-BP-20 Option A GE/SD split (user-approved 2026-09-07):
      Develop corporate strategy is excluded from GovernanceAndExistence
      per v2.4.0. Original L2 entry marked 'planned' on its compose edge
      with scheduled_to pointing at the new SD-Conceive group.
  - cr: CR-BP-21a
    date: '{CHANGE_DATE}'
    change: |
      L2 migration executed under CR-BP-21a. New id
      dea:process-develop-corporate-strategy; new context
      dea:pc-sd-conceive; new serves relationship
      ecf:strategyDirection.conceive; new Process Group
      dea:group-strategy-direction-conception. Version bumped to 2.0.0.
      The original L2 entry remains at
      dea:process-develop-governance-strategy/ with
      lifecycle_status=deprecated and a redirect README for any
      external link.

links:
- rel: change-request
  href: change-requests/CR-BP-21a-strategy-direction-landing.md
- rel: predecessor
  href: change-requests/CR-BP-19-l1-register-rederivation-ecf-v240.md
- rel: predecessor
  href: change-requests/CR-BP-20-l1-l2-alignment-ecf-v240.md
- rel: process-context
  href: contexts/v1-alpha/dea-pc-sd-conceive.yaml
- rel: process-group
  href: entities/v1-alpha/dea:group-strategy-direction-conception/dea:group-strategy-direction-conception.yaml
context:
- ref: dea:pc-sd-conceive
"""
)
print(f"wrote {new_l2}/dea:process-develop-corporate-strategy.yaml")


# ----- Deprecate old L2 path: dea:process-develop-governance-strategy -----
old_l2 = ENT / "dea:process-develop-governance-strategy"
if old_l2.exists():
    # Append a deprecation entry to change_history; set lifecycle_status.
    yaml_path = old_l2 / "dea:process-develop-governance-strategy.yaml"
    if yaml_path.exists():
        text = yaml_path.read_text()
        text = text.replace("lifecycle_status: candidate", "lifecycle_status: deprecated")
        text = text.replace("status: candidate", "status: deprecated")
        # Insert a CR-BP-21a change_history entry just before "links:"
        dep_entry = f"""  - cr: CR-BP-21a
    date: '{CHANGE_DATE}'
    change: |
      L2 migration executed. This entry is now DEPRECATED; the active
      process lives at dea:process-develop-corporate-strategy in
      StrategyAndDirection x Conceive (CR-BP-21a). The migration follows
      the user-approved Option A split in CR-BP-20 grounded in
      domain-grounding.md §3.1: GE authorises but does not direct;
      Strategy & Direction directs within the authorised frame.
      External links should update to the new id. A redirect README
      is in place.
"""
        text = text.replace("links:\n- rel: change-request", dep_entry + "links:\n- rel: change-request")
        # Append a migration-link entry in `links`
        text = text.replace(
            "href: change-requests/cr-bp-13a-customer-and-demand-admission.md",
            "href: change-requests/cr-bp-13a-customer-and-demand-admission.md\n- rel: migration-target\n  href: entities/v1-alpha/dea:process-develop-corporate-strategy/dea:process-develop-corporate-strategy.yaml",
        )
        yaml_path.write_text(text)
        print(f"deprecated {yaml_path}")
    # Redirect README
    (old_l2 / "README.md").write_text(
        f"""# DEPRECATED — use `dea:process-develop-corporate-strategy`

This L2 entry has been **deprecated** under CR-BP-21a. The active
process lives at:

- `entities/v1-alpha/dea:process-develop-corporate-strategy/dea:process-develop-corporate-strategy.yaml`

The migration follows the user-approved Option A split in CR-BP-20
(2026-09-07), grounded in
`dea-metaframework/framework/domain-grounding.md §3.1` ("Governance
authorizes but does not direct; Strategy & Direction directs within
the authorized frame") and §3.2 (Strategy & Direction owns purpose,
ambition, strategic intent, corporate strategy conception).

External links should update to the new id. The deprecated entry
remains in the tree so any historical reference resolves and so the
change_history trail is auditable.
"""
    )
    print(f"wrote {old_l2}/README.md (redirect)")


# ----- Also clean up the compose edge on dea:group-governance-conception -----
gov_group = ENT / "dea:group-governance-conception" / "dea:group-governance-conception.yaml"
if gov_group.exists():
    text = gov_group.read_text()
    # The CR-BP-20 entry for the develop-governance-strategy edge had
    # status: planned; under CR-BP-21a that L2 has migrated, so the
    # compose edge should be removed (or moved to status: deprecated).
    # We remove the composes entry for develop-governance-strategy
    # and add a CR-BP-21a change_history entry.
    # Use a simple approach: find the planned entry block and remove it.
    import re
    pattern = re.compile(
        r"  - source_id: dea:group-governance-conception\n"
        r"    target_id: dea:process-develop-governance-strategy\n"
        r"    relationship_type: composes\n"
        r"    direction: source-to-target\n"
        r"    status: planned\n"
        r"    scheduled_to: dea:group-strategy-direction-conception\n"
        r"    scheduled_by: CR-BP-21a\n"
        r"    asserted_by: dea-team\n"
        r"    rationale: \|[^\n]*\n(?:      [^\n]*\n)*"
        r"    evidence: docs/examples/develop-governance-strategy.md\n"
        r"    provenance:\n"
        r"      type: architecture-review\n"
        r"      reference: CR-BP-20\n"
        r"      asserted_by: dea-team\n"
        r"      asserted_at: '2026-09-07'\n"
    )
    text = pattern.sub("", text)
    # Update change_history
    dep_entry = (
        f"    - cr: CR-BP-21a\n"
        f"      date: '{CHANGE_DATE}'\n"
        f"      change: |\n"
        f"        L2 migration executed: the planned-migration edge for\n"
        f"        dea:process-develop-governance-strategy is removed; the\n"
        f"        process now lives at dea:process-develop-corporate-strategy\n"
        f"        in StrategyAndDirection x Conceive under\n"
        f"        dea:group-strategy-direction-conception. The\n"
        f"        dea:process-develop-governance-strategy entry is\n"
        f"        deprecated; the redirect README is in place. Scope of\n"
        f"        this group (governance mandate / policy / charter\n"
        f"        conception) is unchanged.\n"
    )
    # Insert just after the existing CR-BP-20 entry in change_history
    # The existing entry ends with 'until\n        CR-BP-21a lands.' followed by a blank line then 'links:'.
    marker = "        until\n        CR-BP-21a lands.\n"
    if marker in text:
        text = text.replace(marker, marker + "\n" + dep_entry)
    gov_group.write_text(text)
    print(f"cleaned {gov_group}")


print("\nDone. Next: regenerate CATALOG.yaml and run conformance gates.")
