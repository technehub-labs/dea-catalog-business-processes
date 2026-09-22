"""Generate CR-BP-13a tranche files (PartyAndRelationship).

Produces 4 Process Context cells + 4 Process Group records + 8 L2
Process entries + 4 context README files + 4 process README files +
the CR doc.

This is a one-shot generator for a specific tranche. It is NOT a
general-purpose framework; the per-entity narrative prose is curated
per coordinate.

Usage:
    python tools/build_bp13a_tranche.py
    python tools/build_bp13a_tranche.py --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
CRATED_AT = "2026-09-05"
CR = "CR-BP-13a"

# Stage name mapping (short code -> canonical Lifecycle Stage).
STAGE_NAMES = {
    "c": "Conceive",
    "d": "Design",
    "b": "Build",
    "op": "Operate",
    "im": "Improve",
}

# ECF identifier per Process Context id. Maps `<domain>-<stage>`
# suffix to ECF identifier string.
ECF_IDENTIFIERS = {
    # PartyAndRelationship (CR-BP-13a)
    "dea:pc-pr-c": "ecf:partyRelationship.conceive",
    "dea:pc-pr-d": "ecf:partyRelationship.design",
    "dea:pc-pr-b": "ecf:partyRelationship.build",
    "dea:pc-pr-op": "ecf:partyRelationship.operate",
    "dea:pc-pr-im": "ecf:partyRelationship.improve",
    # GovernanceAndExistence (CR-BP-13b)
    "dea:pc-ge-c": "ecf:governanceExistence.conceive",
    "dea:pc-ge-d": "ecf:governanceExistence.design",
    "dea:pc-ge-b": "ecf:governanceExistence.build",
    "dea:pc-ge-op": "ecf:governanceExistence.operate",
    "dea:pc-ge-im": "ecf:governanceExistence.improve",
}

# Domain name lookup by Process Context id (mid-segment).
DOMAIN_NAMES = {
    "pr": "PartyAndRelationship",
    "ge": "GovernanceAndExistence",
    "sd": "StrategyAndDirection",
    "ag": "AgencyAndOrganization",
    "pv": "ProductAndValue",
    "oe": "EnablementAndOperations",
    "fa": "FinanceAndAccounting",
}


# ---------------------------------------------------------------------------
# Process Context cells (Conceive, Design, Build, Improve for PartyAndRelationship)
# ---------------------------------------------------------------------------

PROCESS_CONTEXTS = [
    {
        "id": "dea:pc-pr-c",
        "domain": "PartyAndRelationship",
        "stage": "Conceive",
        "name": "Customer Strategy Conception",
        "definition": (
            "The bounded enterprise context for **conceiving** customer "
            "and demand strategy in the **customer and demand** domain. "
            "This context addresses the front-end work of framing customer "
            "strategy, market segmentation, and demand thesis: deciding "
            "which customer segments the enterprise will serve, what "
            "value exchange to offer, and which demand thesis to commit to."
        ),
        "includes": [
            "Customer strategy framing",
            "Market segmentation",
            "Demand thesis development",
            "Customer portfolio thesis",
        ],
        "excludes": [
            "Customer experience design (Design stage; adjacent context)",
            "Channel build (Build stage; adjacent context)",
            "Active relationship operation (Operate stage; adjacent context)",
        ],
        "outcomes": [
            "Customer strategy is framed with a defensible segment thesis.",
            "Market segmentation aligns with enterprise value proposition.",
            "Demand thesis is testable and bounded.",
        ],
        "adjacent": [
            ("dea:pc-pr-d", "Design"),
            ("dea:pc-pr-b", "Build"),
            ("dea:pc-pr-op", "Operate"),
            ("dea:pc-pr-ac", "Activate"),
        ],
        "l2_processes": [
            "dea:process-customer-strategy-conception",
            "dea:process-market-and-demand-conception",
        ],
        "enterprise_concern": (
            "Customer and demand: the enterprise's exchange with its "
            "customer base."
        ),
        "lifecycle_concern": (
            "Conceive: framing the customer and demand thesis."
        ),
        "combined_semantic_meaning": (
            "The front-end work of deciding which customer segments to "
            "serve, what value to offer, and which demand thesis to "
            "commit to."
        ),
        "expected_outcomes": [
            "Customer strategy is framed with a defensible segment thesis.",
            "Market segmentation aligns with enterprise value proposition.",
            "Demand thesis is testable and bounded.",
        ],
        "inclusions": [
            "Customer strategy framing",
            "Market segmentation",
            "Demand thesis development",
        ],
        "exclusions": [
            "Customer experience design (Design stage)",
            "Channel build (Build stage)",
            "Active relationship operation (Operate stage)",
        ],
        "adjacent_boundaries": [
            "dea:pc-pr-d (Design): translates strategy into experience, journey, and demand designs.",
            "dea:pc-pr-b (Build): builds the channels and acquisition engines.",
            "dea:pc-pr-op (Operate): runs the active customer relationships framed here.",
            "dea:pc-pr-ac (Activate): transition from strategy to first active customer.",
        ],
    },
    {
        "id": "dea:pc-pr-d",
        "domain": "PartyAndRelationship",
        "stage": "Design",
        "name": "Customer Experience Design",
        "definition": (
            "The bounded enterprise context for **designing** customer "
            "experience, journey, and demand models in the **customer "
            "and demand** domain. This context addresses the work of "
            "translating customer strategy into a designed experience, "
            "an articulated customer journey, and a model of how demand "
            "is shaped by the enterprise's offerings."
        ),
        "includes": [
            "Customer experience design",
            "Customer journey design",
            "Demand model design",
            "CX pattern selection",
        ],
        "excludes": [
            "Customer strategy framing (Conceive stage)",
            "Channel implementation (Build stage)",
            "Live customer operation (Operate stage)",
        ],
        "outcomes": [
            "Customer experience is designed and testable.",
            "Customer journey is articulated end-to-end.",
            "Demand model grounds Build and Operate contexts.",
        ],
        "adjacent": [
            ("dea:pc-pr-c", "Conceive"),
            ("dea:pc-pr-b", "Build"),
            ("dea:pc-pr-op", "Operate"),
            ("dea:pc-pr-ac", "Activate"),
        ],
        "l2_processes": [
            "dea:process-customer-experience-design",
            "dea:process-demand-design",
            "dea:process-customer-journey-design",
        ],
        "enterprise_concern": (
            "Customer and demand: the enterprise's exchange with its "
            "customer base."
        ),
        "lifecycle_concern": (
            "Design: articulating how customer value will be realised."
        ),
        "combined_semantic_meaning": (
            "Translating customer strategy into a designed experience, "
            "an articulated journey, and a demand model."
        ),
        "expected_outcomes": [
            "Customer experience is designed and testable.",
            "Customer journey is articulated end-to-end.",
            "Demand model grounds Build and Operate contexts.",
        ],
        "inclusions": [
            "Customer experience design",
            "Customer journey design",
            "Demand model design",
        ],
        "exclusions": [
            "Customer strategy framing (Conceive stage)",
            "Channel implementation (Build stage)",
            "Live customer operation (Operate stage)",
        ],
        "adjacent_boundaries": [
            "dea:pc-pr-c (Conceive): the prior lifecycle stage; strategy flows into design.",
            "dea:pc-pr-b (Build): designs flow into channel and acquisition build.",
            "dea:pc-pr-op (Operate): designed experience is realised in operation.",
            "dea:pc-pr-ac (Activate): designs activate at first-customer onboarding.",
        ],
    },
    {
        "id": "dea:pc-pr-b",
        "domain": "PartyAndRelationship",
        "stage": "Build",
        "name": "Customer Channel and Acquisition Build",
        "definition": (
            "The bounded enterprise context for **building** customer "
            "channels, acquisition engines, and demand-generation "
            "infrastructure in the **customer and demand** domain. This "
            "context addresses the work of standing up the operational "
            "assets that will acquire customers and generate demand: "
            "channel infrastructure, marketing automation, and "
            "demand-generation engines."
        ),
        "includes": [
            "Channel infrastructure build",
            "Acquisition engine build",
            "Marketing automation build",
            "Demand-generation engine build",
        ],
        "excludes": [
            "Customer strategy framing (Conceive stage)",
            "Customer experience design (Design stage)",
            "Live customer operation (Operate stage)",
        ],
        "outcomes": [
            "Channel infrastructure is operational.",
            "Acquisition engine produces qualified leads.",
            "Demand-generation engine produces sustained demand.",
        ],
        "adjacent": [
            ("dea:pc-pr-c", "Conceive"),
            ("dea:pc-pr-d", "Design"),
            ("dea:pc-pr-op", "Operate"),
            ("dea:pc-pr-ac", "Activate"),
        ],
        "l2_processes": [
            "dea:process-customer-channel-and-acquisition-build",
            "dea:process-demand-generation-build",
        ],
        "enterprise_concern": (
            "Customer and demand: the enterprise's exchange with its "
            "customer base."
        ),
        "lifecycle_concern": (
            "Build: standing up the operational assets that acquire "
            "customers and generate demand."
        ),
        "combined_semantic_meaning": (
            "Standing up the channels, acquisition engines, and "
            "demand-generation infrastructure that will carry customer "
            "value into the Operate stage."
        ),
        "expected_outcomes": [
            "Channel infrastructure is operational.",
            "Acquisition engine produces qualified leads.",
            "Demand-generation engine produces sustained demand.",
        ],
        "inclusions": [
            "Channel infrastructure build",
            "Acquisition engine build",
            "Marketing automation build",
        ],
        "exclusions": [
            "Customer strategy framing (Conceive stage)",
            "Customer experience design (Design stage)",
            "Live customer operation (Operate stage)",
        ],
        "adjacent_boundaries": [
            "dea:pc-pr-c (Conceive): strategy is the build's input.",
            "dea:pc-pr-d (Design): experience/journey/demand designs guide the build.",
            "dea:pc-pr-op (Operate): built channels and engines operate on active customers.",
            "dea:pc-pr-ac (Activate): built assets activate at first-customer onboarding.",
        ],
    },
    {
        "id": "dea:pc-pr-im",
        "domain": "PartyAndRelationship",
        "stage": "Improve",
        "name": "Customer Insight and Retention",
        "definition": (
            "The bounded enterprise context for **improving** customer "
            "experience, retention, and lifetime value in the **customer "
            "and demand** domain. This context addresses the work of "
            "monitoring customer insight (satisfaction, churn risk, "
            "win-back opportunities) and operating retention programs "
            "that close the loop between insight and design/build/operate."
        ),
        "includes": [
            "Customer satisfaction monitoring",
            "Churn analysis and prediction",
            "Win-back program operation",
            "Customer feedback loops",
        ],
        "excludes": [
            "Active customer relationship operation (Operate stage)",
            "Customer strategy framing (Conceive stage)",
            "Customer experience design (Design stage)",
        ],
        "outcomes": [
            "Customer insight informs Conceive/Design/Build cycles.",
            "Retention programs reduce churn.",
            "Win-back programs re-engage lapsed customers.",
        ],
        "adjacent": [
            ("dea:pc-pr-c", "Conceive"),
            ("dea:pc-pr-d", "Design"),
            ("dea:pc-pr-b", "Build"),
            ("dea:pc-pr-op", "Operate"),
        ],
        "l2_processes": [
            "dea:process-customer-insight-and-retention",
        ],
        "enterprise_concern": (
            "Customer and demand: the enterprise's exchange with its "
            "customer base."
        ),
        "lifecycle_concern": (
            "Improve: closing the loop between insight and "
            "conceive/design/build/operate cycles."
        ),
        "combined_semantic_meaning": (
            "Monitoring customer insight (satisfaction, churn, win-back) "
            "and operating retention programs that translate insight into "
            "action across the customer value stream."
        ),
        "expected_outcomes": [
            "Customer insight feeds Conceive/Design/Build/Operate.",
            "Retention programs reduce churn.",
            "Win-back programs re-engage lapsed customers.",
        ],
        "inclusions": [
            "Customer satisfaction monitoring",
            "Churn analysis and prediction",
            "Win-back program operation",
        ],
        "exclusions": [
            "Active customer relationship operation (Operate stage)",
            "Customer strategy framing (Conceive stage)",
            "Customer experience design (Design stage)",
        ],
        "adjacent_boundaries": [
            "dea:pc-pr-c (Conceive): insights shape strategy framing.",
            "dea:pc-pr-d (Design): insights sharpen experience design.",
            "dea:pc-pr-b (Build): insights reveal channel gaps.",
            "dea:pc-pr-op (Operate): insights refine day-to-day relationship operation.",
        ],
    },
]


def render_process_context(c: dict) -> str:
    """Render a Process Context cell as YAML."""
    lines = [
        f"# Process Context Cell Charter: {c['domain']} x {c['stage']}.",
        "#",
        f"# Lands as part of {CR} (PartyAndRelationship admission tranche).",
        "# This is the N-th Process Context cell in the catalog; the first",
        f"# was dea:pc-pr-op (PartyAndRelationship x Operate; CR-BP-03C).",
        "#",
        "# Each cell carries the full Cell Charter (CR-BP-02 §7):",
        "#   enterprise_concern, lifecycle_concern, combined_semantic_meaning,",
        "#   inclusions / exclusions, adjacent_boundaries.",
        "",
        f"id: {c['id']}",
        f"domain: {c['domain']}",
        f"lifecycle_stage: {c['stage']}",
        f"name: {c['name']}",
        "",
        "# Normative definition (PC-006).",
        "definition: |",
    ]
    for line in c["definition"].splitlines():
        lines.append(f"  {line}")
    lines += [
        "",
        "# Scope (PC-005).",
        "scope:",
        "  includes:",
    ]
    for item in c["includes"]:
        lines.append(f"    - {item}")
    lines += ["  excludes:"]
    for item in c["excludes"]:
        lines.append(f"    - {item}")
    lines += [
        "",
        "# Intended outcomes.",
        "outcomes:",
    ]
    for o in c["outcomes"]:
        lines.append(f"  - {o}")
    lines += [
        "",
        "# Adjacent contexts (CR-BP-02 §11).",
        "adjacent_contexts:",
    ]
    for adj_id, adj_stage in c["adjacent"]:
        lines.append(f"  - {adj_id}")
    lines += [
        "",
        "# Business Processes belonging to this context (PC-008).",
        "processes:",
    ]
    for p in c["l2_processes"]:
        lines.append(f"  - {p}")
    lines += [
        "",
        "# Cell Charter (CR-BP-02 §7; PC-006).",
        "cell_charter:",
        f'  enterprise_concern: "{c["enterprise_concern"]}"',
        f'  lifecycle_concern: "{c["lifecycle_concern"]}"',
        "  combined_semantic_meaning: |",
    ]
    for line in c["combined_semantic_meaning"].splitlines():
        lines.append(f"    {line}")
    lines += ["  expected_outcomes:"]
    for o in c["expected_outcomes"]:
        lines.append(f"    - {o}")
    lines += ["  inclusions:"]
    for item in c["inclusions"]:
        lines.append(f"    - {item}")
    lines += ["  exclusions:"]
    for item in c["exclusions"]:
        lines.append(f"    - {item}")
    lines += ["  adjacent_boundaries:"]
    for ab in c["adjacent_boundaries"]:
        lines.append(f'    - "{ab}"')
    lines += [
        "",
        "# Lifecycle status (CR-BP-02 §17).",
        f"lifecycle_status: candidate",
        f"status: candidate",
        "",
        "# Provenance.",
        f"established_by: {CR}",
        f"established_at: '{CRATED_AT}'",
        "",
        "# Change history.",
        "change_history:",
        f"  - cr: {CR}",
        f"    date: '{CRATED_AT}'",
        "    change: |",
        f"      Initial Process Context record; promoted from the CR-BP-11",
        f"      49-coordinate register (ratified by CR-BP-13) as part of the",
        f"      CustomerAndDomain admission tranche ({CR}).",
        "",
        "links:",
        "  - rel: change-request",
        "    href: change-requests/CR-BP-13a-customer-and-demand-admission.md",
        "  - rel: research-register",
        "    href: entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Process Groups
# ---------------------------------------------------------------------------

PROCESS_GROUPS = [
    {
        "id": "dea:group-customer-strategy-conception",
        "name": "Customer Strategy Conception",
        "context": "dea:pc-pr-c",
        "definition": (
            "The bounded Process Group that organizes the Business "
            "Process responsibilities of conceiving customer strategy in "
            "the PartyAndRelationship x Conceive context. This group "
            "captures the front-end work of framing which customer "
            "segments the enterprise will serve, what value exchange to "
            "offer, and which demand thesis to commit to. The group is "
            "the canonical Process Group for the customer-strategy "
            "value stream; functional refinements specialize the L2 "
            "processes beneath it, not the group itself."
        ),
        "includes": [
            "Customer strategy framing",
            "Market segmentation",
            "Demand thesis development",
            "Customer portfolio thesis",
        ],
        "excludes": [
            "Customer experience design (Design stage; adjacent context)",
            "Channel build (Build stage; adjacent context)",
            "Active customer relationship operation (Operate stage)",
        ],
        "outcomes": [
            "Customer strategy is framed with a defensible segment thesis.",
            "Market segmentation aligns with enterprise value proposition.",
            "Demand thesis is testable and bounded.",
        ],
        "composes": [
            "dea:process-customer-strategy-conception",
            "dea:process-market-and-demand-conception",
        ],
        "process_group_kind": "value-stream",
        "coordinate": "ecf:partyRelationship.conceive",
    },
    {
        "id": "dea:group-customer-experience-design",
        "name": "Customer Experience Design",
        "context": "dea:pc-pr-d",
        "definition": (
            "The bounded Process Group that organizes the Business "
            "Process responsibilities of designing customer experience, "
            "journey, and demand models in the PartyAndRelationship x "
            "Design context. This group captures the work of translating "
            "customer strategy into a designed experience, an articulated "
            "customer journey, and a model of how demand is shaped by "
            "the enterprise's offerings. The group is the canonical "
            "Process Group for the customer-experience value stream."
        ),
        "includes": [
            "Customer experience design",
            "Customer journey design",
            "Demand model design",
            "CX pattern selection",
        ],
        "excludes": [
            "Customer strategy framing (Conceive stage)",
            "Channel implementation (Build stage)",
            "Live customer operation (Operate stage)",
        ],
        "outcomes": [
            "Customer experience is designed and testable.",
            "Customer journey is articulated end-to-end.",
            "Demand model grounds Build and Operate contexts.",
        ],
        "composes": [
            "dea:process-customer-experience-design",
            "dea:process-demand-design",
            "dea:process-customer-journey-design",
        ],
        "process_group_kind": "value-stream",
        "coordinate": "ecf:partyRelationship.design",
    },
    {
        "id": "dea:group-customer-channel-and-acquisition-build",
        "name": "Customer Channel and Acquisition Build",
        "context": "dea:pc-pr-b",
        "definition": (
            "The bounded Process Group that organizes the Business "
            "Process responsibilities of building customer channels, "
            "acquisition engines, and demand-generation infrastructure "
            "in the PartyAndRelationship x Build context. This group "
            "captures the work of standing up the operational assets "
            "that will acquire customers and generate demand: channel "
            "infrastructure, marketing automation, and demand-generation "
            "engines. The group is the canonical Process Group for the "
            "customer-acquisition value stream."
        ),
        "includes": [
            "Channel infrastructure build",
            "Acquisition engine build",
            "Marketing automation build",
            "Demand-generation engine build",
        ],
        "excludes": [
            "Customer strategy framing (Conceive stage)",
            "Customer experience design (Design stage)",
            "Live customer operation (Operate stage)",
        ],
        "outcomes": [
            "Channel infrastructure is operational.",
            "Acquisition engine produces qualified leads.",
            "Demand-generation engine produces sustained demand.",
        ],
        "composes": [
            "dea:process-customer-channel-and-acquisition-build",
            "dea:process-demand-generation-build",
        ],
        "process_group_kind": "value-stream",
        "coordinate": "ecf:partyRelationship.build",
    },
    {
        "id": "dea:group-customer-insight-and-retention",
        "name": "Customer Insight and Retention",
        "context": "dea:pc-pr-im",
        "definition": (
            "The bounded Process Group that organizes the Business "
            "Process responsibilities of monitoring customer insight "
            "and operating retention programs in the PartyAndRelationship x "
            "Improve context. This group captures the work of closing "
            "the loop between customer insight (satisfaction, churn "
            "risk, win-back opportunities) and the Conceive/Design/"
            "Build/Operate cycles that follow from it. The group is the "
            "canonical Process Group for the customer-improvement value "
            "stream."
        ),
        "includes": [
            "Customer satisfaction monitoring",
            "Churn analysis and prediction",
            "Win-back program operation",
            "Customer feedback loops",
        ],
        "excludes": [
            "Active customer relationship operation (Operate stage)",
            "Customer strategy framing (Conceive stage)",
            "Customer experience design (Design stage)",
        ],
        "outcomes": [
            "Customer insight informs Conceive/Design/Build cycles.",
            "Retention programs reduce churn.",
            "Win-back programs re-engage lapsed customers.",
        ],
        "composes": [
            "dea:process-customer-insight-and-retention",
        ],
        "process_group_kind": "value-stream",
        "coordinate": "ecf:partyRelationship.improve",
    },
]


def render_process_group(g: dict) -> str:
    """Render a Process Group record as YAML."""
    lines = [
        f"# Canonical Process Group entry: {g['id']}.",
        "#",
        f"# Lands as part of {CR} (PartyAndRelationship admission tranche).",
        "# One of four new Process Group records that, together with the",
        "# existing dea:group-customer-lifecycle-management (Operate;",
        "# CR-BP-12), populates the PartyAndRelationship value stream across",
        "# the 5 accepted lifecycle stages (Conceive / Design / Build /",
        "# Operate / Improve).",
        "#",
        "# Design (CR-BP-12 §4):",
        "#   - Catalog-owned record, NOT a metamodel entity.",
        "#   - ID family: dea:group-* (CR-BP-04 §4).",
        "#   - Canonical containment: L1 group --composes--> L2 process.",
        "#   - The L2 entities carry the inverse `part_of` for navigation.",
        "#   - MECE within Process Context (PG-006) is enforced.",
        "",
        f"id: {g['id']}",
        "type: ProcessGroup",
        "version: 1.0.0",
        "",
        f"name: {g['name']}",
        "",
        "# Normative definition (PG-006 / MECE).",
        "definition: |",
    ]
    for line in g["definition"].splitlines():
        lines.append(f"  {line}")
    lines += [
        "",
        "# Process Context reference (PG-003 enforces resolution).",
        f"process_context: {g['context']}",
        "",
        "# Scope (MECE boundary; PG-006 depends on excludes).",
        "scope:",
        "  includes:",
    ]
    for item in g["includes"]:
        lines.append(f"    - {item}")
    lines += ["  excludes:"]
    for item in g["excludes"]:
        lines.append(f"    - {item}")
    lines += [
        "",
        "# Intended enterprise outcomes.",
        "outcomes:",
    ]
    for o in g["outcomes"]:
        lines.append(f"  - {o}")
    lines += [
        "",
        "# Canonical containment (PG-004 / PG-005 / PG-006 enforce).",
        f"# This Process Group composes {len(g['composes'])} L2 Business",
        "# Process specialization(s) that landed as part of the same",
        f"# {CR} tranche.",
        "composes:",
    ]
    for i, target in enumerate(g["composes"], 1):
        lines += [
            f"  - source_id: {g['id']}",
            f"    target_id: {target}",
            "    relationship_type: composes",
            "    direction: source-to-target",
            "    status: active",
            "    asserted_by: dea-team",
            "    rationale: |",
            "      The L2 process is a principal responsibility of the",
            f"      {g['name']} value stream within PartyAndRelationship.",
            f"      This composition is canonical per CR-BP-13a.",
            f"    evidence: docs/examples/{g['id'].replace(':', '-')}.md",
            "    provenance:",
            "      type: architecture-review",
            f"      reference: {CR}",
            "      asserted_by: dea-team",
            f"      asserted_at: '{CRATED_AT}'",
        ]
    lines += [
        "",
        "# Process Group kind (PG-007 enforces controlled vocabulary).",
        "process_group_kind: end-to-end",
        "",
        "# Discovery / governance status (mirrors CR-BP-11 register values).",
        "# 'accepted' per CR-BP-13 (research ratification). The ratified-accepted",
        "# register value is mapped to canonical `accepted` here per the schema's",
        "# controlled vocabulary (CR-CATALOG-STRUCT-01 §5).",
        "status: accepted",
        "",
        "# Catalog entry lifecycle (PG-008 enforces).",
        "# `candidate` because full admission is gated by end-to-end MECE",
        "# validation in a follow-up admission tranche (CR-BP-13a.1).",
        "lifecycle_status: candidate",
        "",
        "# ECF Conformance Gate (CR-ECF-CG-001..004).",
        "ecfConformance:",
        "  framework: EnterpriseConceptFramework",
        "  contractVersion: '1.0.0'",
        "  profile: dea:ecf@1.0.0",
        "  status: conformant",
        "  affiliation: inherits-catalog",
        "  canonicalReferences:",
        "    - kind: coordinate",
        f"      domain: {DOMAIN_NAMES[g['context'].split('-')[1]]}",
        f"      stage: {STAGE_NAMES[g['context'].split('-')[-1]]}",
        f"      identifier: {ECF_IDENTIFIERS[g['context']]}",
        "",
        "# Evidence (CR-BP-11 register strength scale E0..E5).",
        "evidence:",
        f"  - source: {CR} (49-coordinate discovery register, ratified)",
        "    claim: |",
        "      This Process Group's coordinate was ratified as accepted",
        "      in CR-BP-13; the register records the L1 candidates and",
        "      L2 process names that compose this group.",
        "    strength: E4",
        "    reference: entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml",
        "",
        "# Metadata (PG-006 cross-context overlap exception path lives here).",
        "metadata:",
        f"  established_by: {CR}",
        f"  established_at: '{CRATED_AT}'",
        "  cross_context_overlap: []",
        "  change_history:",
        f"    - cr: {CR}",
        f"      date: '{CRATED_AT}'",
        "      change: |",
        f"        Initial Process Group record; promoted from the CR-BP-11",
        "        49-coordinate register (ratified by CR-BP-13) as part of",
        f"        the {CR} admission tranche.",
        "",
        "links:",
        "  - rel: change-request",
        f"    href: change-requests/{CR.lower()}-customer-and-demand-admission.md",
        "  - rel: research-register",
        "    href: entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# L2 Process entries
# ---------------------------------------------------------------------------

L2_PROCESSES = [
    # Conceive
    {
        "id": "dea:process-customer-strategy-conception",
        "name": "Develop Customer Strategy",
        "process_context": "dea:pc-pr-c",
        "process_group": "dea:group-customer-strategy-conception",
        "process_intent": "management",
        "process_type": "management",
        "verb": "Develop",
        "object": "Customer Strategy",
        "trigger": (
            "A new customer strategy framing is needed because the "
            "enterprise is entering a new segment, the existing strategy "
            "has drifted, or the demand thesis needs to be re-tested."
        ),
        "outcome": (
            "A customer strategy document with bounded segment thesis, "
            "value exchange, and demand thesis is committed."
        ),
        "outcome_statement": (
            "A customer strategy document with bounded segment thesis, "
            "value exchange, and demand thesis is committed and ready to "
            "drive Design work."
        ),
        "evidence_links": [
            {
                "type": "standard",
                "ref": "https://www.apqc.org/resource-library/resource-collections/56391",
            },
            {
                "type": "documentation",
                "ref": "docs/examples/develop-customer-strategy.md",
            },
        ],
        "realizes_capabilities": [],
    },
    {
        "id": "dea:process-market-and-demand-conception",
        "name": "Develop Market Intelligence",
        "process_context": "dea:pc-pr-c",
        "process_group": "dea:group-customer-strategy-conception",
        "process_intent": "management",
        "process_type": "management",
        "verb": "Develop",
        "object": "Market Intelligence",
        "trigger": (
            "A new market entry, an existing segment's drift, or a "
            "demand-side hypothesis needs to be tested before strategy "
            "commitment."
        ),
        "outcome": (
            "A market and demand thesis with testable hypotheses and "
            "initial segment targets is committed."
        ),
        "outcome_statement": (
            "A market and demand thesis with testable hypotheses, "
            "initial segment targets, and a test plan is committed and "
            "ready to be incorporated into customer strategy."
        ),
        "evidence_links": [
            {
                "type": "standard",
                "ref": "https://www.apqc.org/resource-library/resource-collections/56391",
            },
            {
                "type": "documentation",
                "ref": "docs/examples/develop-market-intelligence.md",
            },
        ],
        "realizes_capabilities": [],
    },
    # Design
    {
        "id": "dea:process-customer-experience-design",
        "name": "Design Customer Experience",
        "process_context": "dea:pc-pr-d",
        "process_group": "dea:group-customer-experience-design",
        "process_intent": "management",
        "process_type": "standardization",
        "verb": "Design",
        "object": "Customer Experience",
        "trigger": (
            "Customer strategy has committed a segment thesis and "
            "value exchange; the experience must now be designed to "
            "realise that exchange."
        ),
        "outcome": (
            "A customer experience design with articulated touchpoints, "
            "interactions, and quality criteria is committed."
        ),
        "outcome_statement": (
            "A customer experience design with articulated touchpoints, "
            "interaction patterns, and quality criteria is committed and "
            "ready to guide channel and journey implementation."
        ),
        "evidence_links": [
            {
                "type": "standard",
                "ref": "https://www.apqc.org/resource-library/resource-collections/56391",
            },
            {
                "type": "documentation",
                "ref": "docs/examples/design-customer-experience.md",
            },
        ],
        "realizes_capabilities": [],
    },
    {
        "id": "dea:process-demand-design",
        "name": "Design Demand Model",
        "process_context": "dea:pc-pr-d",
        "process_group": "dea:group-customer-experience-design",
        "process_intent": "management",
        "process_type": "management",
        "verb": "Design",
        "object": "Demand Model",
        "trigger": (
            "Customer experience has been designed; the demand model "
            "(how customer need becomes enterprise supply) must now be "
            "articulated."
        ),
        "outcome": (
            "A demand model with articulated supply paths, capacity "
            "assumptions, and demand-shaping levers is committed."
        ),
        "outcome_statement": (
            "A demand model with articulated supply paths, capacity "
            "assumptions, and demand-shaping levers is committed and "
            "ready to drive channel and acquisition build."
        ),
        "evidence_links": [
            {
                "type": "standard",
                "ref": "https://www.apqc.org/resource-library/resource-collections/56391",
            },
            {
                "type": "documentation",
                "ref": "docs/examples/design-demand-model.md",
            },
        ],
        "realizes_capabilities": [],
    },
    {
        "id": "dea:process-customer-journey-design",
        "name": "Design Customer Journey",
        "process_context": "dea:pc-pr-d",
        "process_group": "dea:group-customer-experience-design",
        "process_intent": "support",
        "process_type": "core",
        "verb": "Design",
        "object": "Customer Journey",
        "trigger": (
            "Customer experience has been designed; the journey (the "
            "end-to-end path the customer takes through the experience) "
            "must be articulated."
        ),
        "outcome": (
            "A customer journey design with articulated stages, "
            "moments-of-truth, and handoff points is committed."
        ),
        "outcome_statement": (
            "A customer journey design with articulated stages, "
            "moments-of-truth, and handoff points is committed and ready "
            "to align Operate and Improve contexts."
        ),
        "evidence_links": [
            {
                "type": "standard",
                "ref": "https://www.apqc.org/resource-library/resource-collections/56391",
            },
            {
                "type": "documentation",
                "ref": "docs/examples/design-customer-journey.md",
            },
        ],
        "realizes_capabilities": [],
    },
    # Build
    {
        "id": "dea:process-customer-channel-and-acquisition-build",
        "name": "Build Customer Acquisition Channels",
        "process_context": "dea:pc-pr-b",
        "process_group": "dea:group-customer-channel-and-acquisition-build",
        "process_intent": "operational",
        "process_type": "core",
        "verb": "Build",
        "object": "Customer Acquisition Channels",
        "trigger": (
            "Customer experience and journey designs are committed; the "
            "channel and acquisition infrastructure must be built to "
            "carry them."
        ),
        "outcome": (
            "Channel infrastructure and acquisition engines are "
            "operational and ready to acquire first customers."
        ),
        "outcome_statement": (
            "Channel infrastructure and acquisition engines are "
            "operational, integrated with the designed experience, and "
            "ready to acquire first customers in the Activate context."
        ),
        "evidence_links": [
            {
                "type": "standard",
                "ref": "https://www.apqc.org/resource-library/resource-collections/56391",
            },
            {
                "type": "documentation",
                "ref": "docs/examples/build-customer-acquisition-channels.md",
            },
        ],
        "realizes_capabilities": [],
    },
    {
        "id": "dea:process-demand-generation-build",
        "name": "Build Demand Generation Programs",
        "process_context": "dea:pc-pr-b",
        "process_group": "dea:group-customer-channel-and-acquisition-build",
        "process_intent": "operational",
        "process_type": "core",
        "verb": "Build",
        "object": "Demand Generation Programs",
        "trigger": (
            "Customer demand model is committed; the demand-generation "
            "engine (the asset that produces sustained demand) must be "
            "built."
        ),
        "outcome": (
            "A demand-generation engine is operational, integrated with "
            "the channels, and producing initial demand."
        ),
        "outcome_statement": (
            "A demand-generation engine is operational, integrated with "
            "the channels, and producing initial demand consistent with "
            "the customer demand model."
        ),
        "evidence_links": [
            {
                "type": "standard",
                "ref": "https://www.apqc.org/resource-library/resource-collections/56391",
            },
            {
                "type": "documentation",
                "ref": "docs/examples/build-demand-generation-programs.md",
            },
        ],
        "realizes_capabilities": [],
    },
    # Improve
    {
        "id": "dea:process-customer-insight-and-retention",
        "name": "Operate Customer Retention Programs",
        "process_context": "dea:pc-pr-im",
        "process_group": "dea:group-customer-insight-and-retention",
        "process_intent": "management",
        "process_type": "core",
        "verb": "Operate",
        "object": "Customer Retention Programs",
        "trigger": (
            "Active customer relationships are in operation; customer "
            "insight (satisfaction, churn risk, win-back opportunities) "
            "must be monitored and acted on continuously."
        ),
        "outcome": (
            "Customer insight (NPS, churn risk, win-back lists) is "
            "produced continuously and feeds Conceive/Design/Build/"
            "Operate cycles."
        ),
        "outcome_statement": (
            "Customer insight is produced continuously, retention "
            "programs run on the insight, and the insight is fed back "
            "into Conceive/Design/Build/Operate cycles."
        ),
        "evidence_links": [
            {
                "type": "standard",
                "ref": "https://www.apqc.org/resource-library/resource-collections/56391",
            },
            {
                "type": "documentation",
                "ref": "docs/examples/operate-customer-retention-programs.md",
            },
        ],
        "realizes_capabilities": [],
    },
]


def render_l2_process(p: dict) -> str:
    """Render an L2 Process entry as YAML."""
    lines = [
        f"# Canonical Business Process entry: `{p['id']}`.",
        "#",
        f"# Lands as part of {CR} (PartyAndRelationship admission tranche).",
        f"# This L2 process composes into `{p['process_group']}`.",
        "#",
        "# Shape (CR-BP-03 / CR-BP-03A / CR-BP-SPEC-BP-01):",
        "#   - 4-axis classification (intent / type / specialization / audience)",
        "#   - Process Identity contract (verb + object + outcome + evidence)",
        "#   - Canonical relationships (array-of-relationship-instances)",
        "#   - Process Context reference (Cell Charter cell)",
        "#   - ECF Conformance Gate (inherits-catalog with doesNotRedefine)",
        "",
        f"id: {p['id']}",
        f"name: {p['name']}",
        "type: Process",
        "version: 1.0.0",
        "lifecycle_status: candidate",
        "status: candidate",
        "",
        "# Classification (CR-BP-03 §2.1)",
        f"process_intent: {p['process_intent']}",
        "process_audience: party-relationship",
        "",
        "# Classification: 5-value Mintzberg vocabulary (CR-BP-03 §2.1).",
        f"process_type: {p['process_type']}",
        "",
        "# Classification: inheritance / pattern-based refinement (CR-BP-03 §2.1).",
        "# No parent specialization at admission time; future specializations",
        f"# may declare this id in their process_specialization list.",
        "process_specialization: []",
        "",
        "description: |",
        f"  Operate the {p['name']} L2 process within the",
        f"  {p['process_context']} Cell Charter. See trigger and outcome for",
        "  the bounded work this process owns; see identity.outcome_statement",
        "  for the testable outcome the process produces.",
        "",
        "# Trigger (BP-ARC-ID-002): what initiates the process.",
        "trigger: |",
    ]
    for line in p["trigger"].splitlines():
        lines.append(f"  {line}")
    lines += [
        "",
        "# Outcome (BP-ARC-ID-003): what the process produces.",
        "outcome: |",
    ]
    for line in p["outcome"].splitlines():
        lines.append(f"  {line}")
    lines += [
        "",
        "# Process Context (CR-BP-02).",
        f"process_context: {p['process_context']}",
        "",
        "# Process Identity (CR-BP-03 §5.4).",
        "identity:",
        f"  verb: {p['verb']}",
        f"  object: {p['object']}",
        "  scope: (all customer segments)",
        "  outcome_statement: |",
    ]
    for line in p["outcome_statement"].splitlines():
        lines.append(f"    {line}")
    lines += ["  evidence_links:"]
    for ev in p["evidence_links"]:
        lines += [
            f"    - type: {ev['type']}",
            f"      ref: {ev['ref']}",
        ]
    lines += [
        "",
        "# Canonical relationships (CR-BP-03 §6; CR-BP-03A §3.1).",
        "# The L1 Process Group's `composes` array is the canonical",
        "# containment direction (PG-004). The inverse `part-of` is",
        "# generated at query time (CR-BP-12 §8); it is NOT a",
        "# first-class relationship-type in the metamodel's allowed",
        "# set, so this L2 entry does not declare it here. Only",
        "# realizes and other metamodel-allowed types appear.",
        "relationships: []",
        "",
        "# ECF Conformance Gate (CR-ECF-CG-001..004).",
        "ecfConformance:",
        "  framework: EnterpriseConceptFramework",
        "  contractVersion: '1.0.0'",
        "  profile: dea:ecf@1.0.0",
        "  status: conformant",
        "  affiliation: inherits-catalog",
        "  canonicalReferences:",
        "    - kind: coordinate",
        f"      domain: {DOMAIN_NAMES[p['process_context'].split('-')[1]]}",
        f"      stage: {STAGE_NAMES[p['process_context'].split('-')[-1]]}",
        f"      identifier: {ECF_IDENTIFIERS[p['process_context']]}",
        "",
        "# Change history.",
        "metadata:",
        f"  established_by: {CR}",
        f"  established_at: '{CRATED_AT}'",
        "  change_history:",
        f"    - cr: {CR}",
        f"      date: '{CRATED_AT}'",
        "      change: |",
        f"        Initial L2 Process entry; lands as part of the {CR}",
        "        PartyAndRelationship admission tranche.",
        "",
        "links:",
        "  - rel: change-request",
        f"    href: change-requests/{CR.lower()}-customer-and-demand-admission.md",
        "  - rel: process-context",
        f"    href: contexts/v1-alpha/{p['process_context'].replace(':', '-')}.yaml",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Manifests and driver
# ---------------------------------------------------------------------------

def write_file(path: Path, content: str, dry_run: bool) -> None:
    if dry_run:
        print(f"  would write: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  wrote: {path}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="build-bp13a-tranche")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    print("=== Process Context cells ===")
    for c in PROCESS_CONTEXTS:
        path = REPO_ROOT / f"contexts/v1-alpha/{c['id'].replace(':', '-')}.yaml"
        write_file(path, render_process_context(c), args.dry_run)

    print("\n=== Process Group records ===")
    for g in PROCESS_GROUPS:
        path = REPO_ROOT / (
            f"entities/v1-alpha/{g['id']}/{g['id']}.yaml"
        )
        write_file(path, render_process_group(g), args.dry_run)
        # Stub research/, candidates/, retired/ folders with .gitkeep.
        for sub in ("research", "candidates", "retired"):
            stub = REPO_ROOT / f"entities/v1-alpha/{g['id']}/{sub}/.gitkeep"
            if not args.dry_run:
                stub.parent.mkdir(parents=True, exist_ok=True)
                stub.touch()
        # Process Group README.
        readme = REPO_ROOT / f"entities/v1-alpha/{g['id']}/README.md"
        write_file(
            readme,
            (
                f"# Canonical Process Group: `{g['id']}`\n\n"
                f"This directory hosts the canonical Process Group record\n"
                f"for `{g['id']}`. The Process Group is a catalog-owned\n"
                f"record (not an OpenDEA metamodel entity) that organises\n"
                f"the L2 Business Process entries composing into it within\n"
                f"the {g['context']} Process Context.\n\n"
                f"## Composition\n\n"
                f"This Process Group composes the following L2 Business\n"
                f"Process specialization(s):\n\n"
            ),
            args.dry_run,
        )
        # Append the composes list.
        if not args.dry_run:
            with readme.open("a", encoding="utf-8") as f:
                for c in g["composes"]:
                    f.write(f"- `{c}`\n")
                f.write(
                    "\n## Change history\n\n"
                    f"See the canonical YAML's `metadata.change_history` "
                    f"for the per-CR history.\n\n"
                    "## Governing CR\n\n"
                    f"- **{CR}** (this tranche): admission of the "
                    f"Process Group into the PartyAndRelationship value "
                    "stream.\n"
                )
        # Research README placeholder (CR-CATALOG-STRUCT-01 §5 requires
        # research/README.md even when the research folder is otherwise
        # empty).
        research_readme = (
            REPO_ROOT / f"entities/v1-alpha/{g['id']}/research/README.md"
        )
        write_file(
            research_readme,
            (
                f"# Research register: `{g['id']}`\n\n"
                "This directory holds research artifacts specific to\n"
                f"this Process Group. No L1-specific research has been\n"
                "moved into this subtree yet; the coordinate's research\n"
                f"lives in the CR-BP-11 49-coordinate register (ratified\n"
                "by CR-BP-13; record under\n"
                "`dea:group-customer-lifecycle-management/research/`).\n"
                "Group-specific evidence will accumulate here as it\n"
                "is produced.\n\n"
                "## Provenance\n\n"
                f"Established by {CR} on {CRATED_AT}.\n\n"
                "## Governing CR\n\n"
                f"- **{CR}**: admission of the Process Group into\n"
                "  the PartyAndRelationship value stream.\n"
            ),
            args.dry_run,
        )

    print("\n=== L2 Process entries ===")
    for p_obj in L2_PROCESSES:
        path = REPO_ROOT / (
            f"entities/v1-alpha/{p_obj['id']}/{p_obj['id']}.yaml"
        )
        write_file(path, render_l2_process(p_obj), args.dry_run)
        # Stub folders.
        for sub in ("research", "candidates", "retired"):
            stub = REPO_ROOT / f"entities/v1-alpha/{p_obj['id']}/{sub}/.gitkeep"
            if not args.dry_run:
                stub.parent.mkdir(parents=True, exist_ok=True)
                stub.touch()
        # Process README.
        readme = REPO_ROOT / f"entities/v1-alpha/{p_obj['id']}/README.md"
        write_file(
            readme,
            (
                f"# Canonical Business Process: `{p_obj['id']}`\n\n"
                f"This directory hosts the canonical L2 Business Process\n"
                f"entry for `{p_obj['id']}`. The process composes into\n"
                f"the `{p_obj['process_group']}` Process Group within\n"
                f"the {p_obj['process_context']} Process Context.\n\n"
                "## Governing CR\n\n"
                f"- **{CR}**: initial admission as part of the\n"
                f"  PartyAndRelationship admission tranche.\n"
            ),
            args.dry_run,
        )
        # Research README placeholder.
        research_readme = (
            REPO_ROOT / f"entities/v1-alpha/{p_obj['id']}/research/README.md"
        )
        write_file(
            research_readme,
            (
                f"# Research register: `{p_obj['id']}`\n\n"
                "This directory holds research artifacts specific to\n"
                "this L2 Business Process. No L2-specific research has\n"
                "been moved into this subtree yet; the coordinate's\n"
                "research lives in the CR-BP-11 49-coordinate register\n"
                "(ratified by CR-BP-13; record under\n"
                "`dea:group-customer-lifecycle-management/research/`).\n"
                "Process-specific evidence will accumulate here as it\n"
                "is produced.\n\n"
                "## Provenance\n\n"
                f"Established by {CR} on {CRATED_AT}.\n\n"
                "## Governing CR\n\n"
                f"- **{CR}**: initial admission as part of the\n"
                "  PartyAndRelationship admission tranche.\n"
            ),
            args.dry_run,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())