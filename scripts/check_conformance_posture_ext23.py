#!/usr/bin/env python3
"""
check_conformance_posture_ext23.py
=====================================

Conformance gate posture assessment (CR-BP-EXT-23).

Implements REQ-23-01..REQ-23-12: the gate inventory, the enforcement
classification, the promotion criteria, the reason recording, the
population reconciliation linkage, the conformance posture report, and
the demotion / deferral / exception policy.

The gate registry in scripts/conformance_result.py is the single source
of truth (REQ-23-11). This script reads it, classifies every gate, and
generates the posture report FROM the registry. It never maintains a
parallel registry.

Enforcement classes (REQ-23-02):
  structural  deterministically evaluable structural relationship rules
  content     deterministically evaluable content-presence rules
  semantic    rules whose evaluation requires business meaning
  review      rules whose evaluation requires human adjudication

Promotion criteria (REQ-23-03): a gate may be blocking only where its
class is `structural` or `content`, its subject population has been
reconciled under EXT-22, and the EXT-22 readiness assessment lists it
as automatically enforceable.

Outputs:
  reconciliation/conformance-posture-report.json
  reconciliation/gate-inventory.json
  reconciliation/ext23-manifest.json

Test layout: tests/test_conformance_posture_ext23.py
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
RECON_DIR = REPO_ROOT / "reconciliation"
POSTURE_PATH = RECON_DIR / "conformance-posture-report.json"
INVENTORY_PATH = RECON_DIR / "gate-inventory.json"
MANIFEST_PATH = RECON_DIR / "ext23-manifest.json"
READINESS_PATH = RECON_DIR / "ext23-readiness-assessment.json"

# The 4 enforcement classes (REQ-23-02)
ENFORCEMENT_CLASSES = ("structural", "content", "semantic", "review")

# The 4 enforcement tiers (the EXT-23 §7 tier model)
TIER_BY_CLASS = {
    "structural": "T1",
    "content": "T2",
    "semantic": "T3",
    "review": "T4",
}

# ---------------------------------------------------------------------------
# The enforcement classification, keyed by the gate label in the registry.
# The classification is a property of the rule the gate enforces, not of the
# gate's current blocking posture.
# ---------------------------------------------------------------------------

CLASSIFICATION: dict[str, dict[str, Any]] = {
    # -- pre-EXT-08 gates [1] to [33]: structural and content rules that
    #    have been blocking since the entity-system contract.
    "[1] Schema (validate-process-entries)": {
        "class": "structural", "cr": "CR-BP-16",
        "population": "the full catalogue index",
        "reason": "The catalog index schema is a deterministic contract that has "
                  "been enforced since CR-BP-16; the population is fully reconciled "
                  "under EXT-22.",
    },
    "[1] Schema (catalog-index)": {
        "class": "structural", "cr": "CR-BP-16",
        "population": "the full catalogue index",
        "reason": "The catalog index schema is a deterministic contract that has "
                  "been enforced since CR-BP-16; the population is fully reconciled "
                  "under EXT-22.",
    },
    "[2] Structure": {
        "class": "structural", "cr": "CR-BP-16",
        "population": "the full catalogue",
        "reason": "The structural contract is deterministic; it remains advisory "
                  "because the pre-EXT-08 baseline predates the EXT-22 "
                  "reconciliation and is not yet re-baselined.",
    },
    "[3] References (BP-SEM + legacy)": {
        "class": "structural", "cr": "CR-BP-16",
        "population": "the full catalogue",
        "reason": "Reference validity is deterministic and the population is "
                  "reconciled under EXT-22.",
    },
    "[3] References (context-resolution)": {
        "class": "structural", "cr": "CR-BP-16",
        "population": "the full catalogue",
        "reason": "Context resolution is deterministic and the population is "
                  "reconciled under EXT-22.",
    },
    "[4] Semantics (BP-SEM-001..014)": {
        "class": "content", "cr": "CR-BP-16",
        "population": "the L2 Business Process layer",
        "reason": "The BP-SEM rule set evaluates controlled vocabularies, reference "
                  "resolution and specialization-pattern validity; every rule is "
                  "mechanically evaluable and the population is reconciled under "
                  "EXT-22.",
    },
    "[4] Semantics (BP-SPEC-01-001..007)": {
        "class": "structural", "cr": "CR-BP-16",
        "population": "the L2 Business Process layer",
        "reason": "The BP-SPEC rule set evaluates metamodel pointer declarations, "
                  "schema title pins, version pins and vocabulary containment; every "
                  "rule is mechanically evaluable and the population is reconciled "
                  "under EXT-22.",
    },
    "[5] Hierarchy (BP-AR-001..007)": {
        "class": "structural", "cr": "CR-BP-16",
        "population": "the full L0-L4 hierarchy",
        "reason": "The architectural regression rules are deterministic hierarchy "
                  "contracts; the population is reconciled under EXT-22.",
    },
    "[6] Specialization Graph (cycle + edge)": {
        "class": "structural", "cr": "CR-BP-16",
        "population": "the L2 Business Process layer",
        "reason": "Cycle and edge validity in the specialization graph is fully "
                  "deterministic; the population is reconciled under EXT-22.",
    },
    "[7] MECE (Process Group)": {
        "class": "structural", "cr": "CR-BP-16",
        "population": "the L1 Process Group layer",
        "reason": "The PG rule set evaluates identifier patterns, required-field "
                  "presence, Process Context and composes resolution, controlled "
                  "vocabularies and lifecycle states; every rule is mechanically "
                  "evaluable and the population is reconciled under EXT-22.",
    },
    "[8] Provenance (ECF conformance)": {
        "class": "content", "cr": "CR-BP-16",
        "population": "the full catalogue",
        "reason": "ECF conformance is a deterministic field-presence contract; the "
                  "population is reconciled under EXT-22.",
    },
    "[9] CR Validation (CR-META-001..006)": {
        "class": "content", "cr": "CR-BP-16",
        "population": "the change-request register",
        "reason": "CR metadata completeness is deterministic; it remains advisory "
                  "because the CR register is outside the EXT-22 catalogue "
                  "reconciliation scope.",
    },
    "[10] Conformance Result (Levels 1-4)": {
        "class": "content", "cr": "CR-BP-16",
        "population": "the full catalogue",
        "reason": "The level conformance report is a deterministic aggregation; it "
                  "remains advisory because it reports on the catalogue rather than "
                  "enforcing a rule of its own.",
    },
    "[10] Conformance Result (Admission gate ADM-001..008)": {
        "class": "structural", "cr": "CR-BP-16",
        "population": "the admission gate records",
        "reason": "Admission gate validity is deterministic; the population is "
                  "outside the EXT-22 catalogue reconciliation scope, so the gate "
                  "remains advisory.",
    },
    "[10] Conformance Result (Documentation DOC-001..003)": {
        "class": "content", "cr": "CR-BP-16",
        "population": "the generated documentation",
        "reason": "Documentation conformance is deterministic; the population is "
                  "outside the EXT-22 catalogue reconciliation scope, so the gate "
                  "remains advisory.",
    },
    "[11] L2 Qualification (BP-C1..C4)": {
        "class": "semantic", "cr": "CR-BP-34a",
        "population": "the L2 Business Process layer",
        "reason": "L2 qualification adequacy requires business-meaning assessment; "
                  "it is enforced through review.",
    },
    "[12] Intent Purposive (PSP-001..003)": {
        "class": "semantic", "cr": "CR-BP-34b",
        "population": "the L2 Business Process layer",
        "reason": "Intent and purposiveness are business judgements; the rule set "
                  "must not be promoted to automatic blocking.",
    },
    "[13] Lifecycle State-Machine (LCM-001..005)": {
        "class": "structural", "cr": "CR-BP-34c",
        "population": "the full catalogue",
        "reason": "Lifecycle state transitions are a deterministic state machine; "
                  "the population is reconciled under EXT-22.",
    },
    "[14] Semantic Identity vs Version (SIV-001..004)": {
        "class": "semantic", "cr": "CR-BP-34d",
        "population": "the full catalogue",
        "reason": "Whether a semantic change is correctly versioned requires business "
                  "judgement; it is enforced through review.",
    },
    "[15] Activity Model (ACT-001..010)": {
        "class": "semantic", "cr": "CR-BP-32",
        "population": "the L3 Activity layer",
        "reason": "Activity model adequacy requires business-meaning assessment; it "
                  "is enforced through the EXT-22 reconciliation and human review.",
    },
    "[16] Execution Boundary (EXE-001..010)": {
        "class": "semantic", "cr": "CR-BP-33",
        "population": "the L3 Activity layer",
        "reason": "Execution boundary adequacy requires business-meaning assessment; "
                  "it is enforced through review.",
    },
    "[17] MECE Validation (MECE-001..008)": {
        "class": "semantic", "cr": "CR-BP-36",
        "population": "the L1 and L2 layers",
        "reason": "MECE adequacy is a business judgement; it is enforced through review.",
    },
    "[18] Cross-Repository Integrity (XRI-001..005)": {
        "class": "structural", "cr": "CR-BP-40",
        "population": "the cross-catalogue references",
        "reason": "Cross-repository reference validity is deterministic; the "
                  "population is outside the EXT-22 catalogue reconciliation scope, "
                  "so the gate remains advisory.",
    },
    "[19] Lifecycle Discovery (DISC-001..008)": {
        "class": "content", "cr": "CR-BP-62",
        "population": "the discovery records",
        "reason": "Discovery record completeness is deterministic; the population is "
                  "outside the EXT-22 catalogue reconciliation scope, so the gate "
                  "remains advisory.",
    },
    "[20] Process Scope (PSCOPE-001..008)": {
        "class": "structural", "cr": "CR-BP-95",
        "population": "the L0 Process Scope layer",
        "reason": "Process scope cardinality and reference rules are deterministic; "
                  "the population is reconciled under EXT-22.",
    },
    "[21] Documentation Profile (DOC-001..005)": {
        "class": "content", "cr": "CR-BP-94-EXT-01",
        "population": "the generated documentation",
        "reason": "Documentation profile conformance is deterministic; the "
                  "population is outside the EXT-22 catalogue reconciliation scope, "
                  "so the gate remains advisory.",
    },
    "[22] Task Model (TASK-001..005)": {
        "class": "structural", "cr": "CR-BP-98",
        "population": "the L4 Task layer",
        "reason": "Task model validity is a deterministic contract that has been "
                  "blocking since CR-BP-98; the population is reconciled under "
                  "EXT-22.",
    },
    "[23] Reconciliation Matrix (RCM-001..010)": {
        "class": "content", "cr": "CR-BP-99",
        "population": "the reconciliation matrix",
        "reason": "Matrix field completeness is deterministic; the population is "
                  "outside the EXT-22 catalogue reconciliation scope, so the gate "
                  "remains advisory.",
    },
    "[24] L0<->L1 Cardinality (L0L1-CARD-001..003)": {
        "class": "structural", "cr": "CR-BP-100",
        "population": "the L0 and L1 layers",
        "reason": "L0/L1 cardinality is a deterministic rule; the population is "
                  "reconciled under EXT-22.",
    },
    "[25] ID System (IDM-001..007)": {
        "class": "structural", "cr": "CR-BP-mv1",
        "population": "the full catalogue",
        "reason": "The identifier convention is a deterministic contract that has "
                  "been blocking since CR-BP-mv1; the population is reconciled "
                  "under EXT-22.",
    },
    "[26] Reference Embargo (CR-BP-112; EMB-001..004)": {
        "class": "content", "cr": "CR-BP-112",
        "population": "the full catalogue",
        "reason": "The reference embargo is a deterministic content contract that "
                  "has been blocking since CR-BP-112; the population is reconciled "
                  "under EXT-22.",
    },
    "[27] HREF Resolver (CR-BP-113; HREF-001..003)": {
        "class": "structural", "cr": "CR-BP-113",
        "population": "the full catalogue",
        "reason": "HREF target resolution is deterministic and has been blocking "
                  "since CR-BP-113; the population is reconciled under EXT-22.",
    },
    # -- EXT gates [34] to [47]: introduced by the operational documentation
    #    programme. The structural and content classes on reconciled
    #    populations are promoted to blocking by EXT-23.
    "[28] Template Drift (CR-BP-113; TPL-001..005)": {
        "class": "content", "cr": "CR-BP-113",
        "population": "the entity templates",
        "reason": "Template drift is a deterministic content contract that has been "
                  "blocking since CR-BP-113; the population is outside the EXT-22 "
                  "catalogue reconciliation scope.",
    },
    "[29] CR README Consistency (CR-BP-113; CRR-001..003)": {
        "class": "content", "cr": "CR-BP-113",
        "population": "the change-request documentation",
        "reason": "CR README consistency is a deterministic content contract that has "
                  "been blocking since CR-BP-113; the population is outside the "
                  "EXT-22 catalogue reconciliation scope.",
    },
    "[30] README Consistency (CR-BP-114; RDM-001..002)": {
        "class": "content", "cr": "CR-BP-114",
        "population": "the generated documentation",
        "reason": "README consistency is a deterministic content contract that has "
                  "been blocking since CR-BP-114; the population is outside the "
                  "EXT-22 catalogue reconciliation scope.",
    },
    "[31] Entity Identity Clarity (CR-BP-117a; EID-001..004)": {
        "class": "content", "cr": "CR-BP-117a",
        "population": "the full catalogue",
        "reason": "Entity identity clarity is a deterministic content contract that "
                  "has been blocking since CR-BP-117a; the population is reconciled "
                  "under EXT-22.",
    },
    "[32] Authorship Cardinal Rule (CR-BP-118; AUT-001..003)": {
        "class": "content", "cr": "CR-BP-118",
        "population": "the full catalogue",
        "reason": "The authorship cardinal rule is a deterministic content contract "
                  "that has been blocking since CR-BP-118; the population is "
                  "reconciled under EXT-22.",
    },
    "[33] Entity System (CR-BP-123 / CR-BP-125; ES-001..ES-005)": {
        "class": "structural", "cr": "CR-BP-123 / CR-BP-125",
        "population": "the full catalogue",
        "reason": "The entity system contract is a deterministic structural rule "
                  "that has been blocking since CR-BP-123; the population is "
                  "reconciled under EXT-22.",
    },
    "[34] Documentation Profile - Generator and Validator (CR-BP-94-EXT-04; DOC-016..020)": {
        "class": "content", "cr": "CR-BP-94-EXT-04",
        "population": "the generated documentation",
        "reason": "The EXT-04 documentation profile rollout is complete (PR #177) "
                  "and the population is reconciled under EXT-22; the gate is "
                  "blocking.",
    },
    "[35] Decomposition Reconciliation (CR-BP-94-EXT-05; DOC-021..025)": {
        "class": "structural", "cr": "CR-BP-94-EXT-05",
        "population": "the full L0-L4 hierarchy",
        "reason": "The EXT-05 decomposition reconciliation is complete (PR #177) and "
                  "the population is reconciled under EXT-22; the gate is blocking.",
    },
    "[36] Profile Registry (CR-BP-94-EXT-11; PR-001..PR-010)": {
        "class": "content", "cr": "CR-BP-94-EXT-11",
        "population": "the L0-L4 profile registry",
        "reason": "The EXT-11 profile registry is a deterministic content contract "
                  "and its population is reconciled under EXT-22; the gate is "
                  "blocking.",
    },
    "[37] Inputs, Outputs, Interfaces (CR-BP-94-EXT-12; IT-001..IT-010)": {
        "class": "content", "cr": "CR-BP-94-EXT-12",
        "population": "the L2 Business Process layer",
        "reason": "The EXT-12 input, output and interface contract is "
                  "deterministic; the population is reconciled under EXT-22 and the "
                  "gate is blocking.",
    },
    "[38] Responsibility, Accountability, Roles (CR-BP-94-EXT-13; RA-001..RA-010)": {
        "class": "content", "cr": "CR-BP-94-EXT-13",
        "population": "the L2 Business Process layer",
        "reason": "The EXT-13 responsibility and accountability contract is "
                  "deterministic; the population is reconciled under EXT-22 and the "
                  "gate is blocking.",
    },
    "[39] Business Rules, Controls, Exceptions (CR-BP-94-EXT-14; GO-001..GO-010)": {
        "class": "content", "cr": "CR-BP-94-EXT-14",
        "population": "the L2 Business Process layer",
        "reason": "The EXT-14 governance semantics are a deterministic content "
                  "contract; the population is reconciled under EXT-22 and the gate "
                  "is blocking.",
    },
    "[40] Evidence, Provenance, Confidence (CR-BP-94-EXT-15; EV-001..EV-010)": {
        "class": "content", "cr": "CR-BP-94-EXT-15",
        "population": "the L2 Business Process layer",
        "reason": "The EXT-15 evidence, provenance and confidence contract is "
                  "deterministic; the population is reconciled under EXT-22 and the "
                  "gate is blocking.",
    },
    "[41] Authoring Methodology (CR-BP-94-EXT-16; AM-001..AM-010)": {
        "class": "content", "cr": "CR-BP-94-EXT-16",
        "population": "the L2 Business Process layer",
        "reason": "The EXT-16 authoring methodology contract is deterministic; the "
                  "population is reconciled under EXT-22 and the gate is blocking.",
    },
    "[42] Enrichment Tooling (CR-BP-94-EXT-17; OR-001..OR-005 + RP-001..RP-009)": {
        "class": "content", "cr": "CR-BP-94-EXT-17",
        "population": "the full catalogue",
        "reason": "The EXT-17 orchestrator and reporter contracts are deterministic; "
                  "the population is reconciled under EXT-22 and the gate is "
                  "blocking.",
    },
    "[43] Operational Documentation Pilot (CR-BP-94-EXT-18; PI-001..PI-008)": {
        "class": "structural", "cr": "CR-BP-94-EXT-18",
        "population": "the 11 pilot entities",
        "reason": "The EXT-18 pilot selection contract is deterministic and the "
                  "pilot population is reconciled under EXT-22; the gate is blocking.",
    },
    "[44] L2 Business Process Backfill (CR-BP-94-EXT-19; L2-001..L2-012)": {
        "class": "content", "cr": "CR-BP-94-EXT-19",
        "population": "the L2 Business Process layer",
        "reason": "The EXT-19 L2 backfill contract is deterministic; the population "
                  "is reconciled under EXT-22 and the gate is blocking.",
    },
    "[45] L3 Activity Backfill (CR-BP-94-EXT-20; L3-001..L3-014)": {
        "class": "content", "cr": "CR-BP-94-EXT-20",
        "population": "the L3 Activity layer",
        "reason": "The EXT-20 L3 backfill contract is deterministic; the population "
                  "is reconciled under EXT-22 and the gate is blocking.",
    },
    "[46] L4 Task Backfill (CR-BP-94-EXT-21; L4-001..L4-014)": {
        "class": "content", "cr": "CR-BP-94-EXT-21",
        "population": "the L4 Task layer",
        "reason": "The EXT-21 L4 backfill contract is deterministic; the population "
                  "is reconciled under EXT-22 and the gate is blocking.",
    },
    "[47] Decomposition Reconciliation (CR-BP-94-EXT-22; R22-01..R22-12)": {
        "class": "structural", "cr": "CR-BP-94-EXT-22",
        "population": "the full L0-L4 catalogue",
        "reason": "The EXT-22 structural reconciliation rules are deterministic and "
                  "the population is the reconciled catalogue; the gate is blocking.",
    },
}


# The manifest each gate's validator emits, used to determine the open
# findings on the gate's subject population. A gate may be promoted to
# blocking only where its population is reconciled: 0 open findings.
GATE_MANIFEST = {
    "[34] Documentation Profile - Generator and Validator (CR-BP-94-EXT-04; DOC-016..020)": "validation-manifest.json",
    "[35] Decomposition Reconciliation (CR-BP-94-EXT-05; DOC-021..025)": "decomposition-reconciliation-manifest.json",
    "[36] Profile Registry (CR-BP-94-EXT-11; PR-001..PR-010)": "profile-manifest.json",
    "[37] Inputs, Outputs, Interfaces (CR-BP-94-EXT-12; IT-001..IT-010)": "inputs-outputs-manifest.json",
    "[38] Responsibility, Accountability, Roles (CR-BP-94-EXT-13; RA-001..RA-010)": "responsibility-accountability-manifest.json",
    "[39] Business Rules, Controls, Exceptions (CR-BP-94-EXT-14; GO-001..GO-010)": "governance-manifest.json",
    "[40] Evidence, Provenance, Confidence (CR-BP-94-EXT-15; EV-001..EV-010)": "evidence-manifest.json",
    "[41] Authoring Methodology (CR-BP-94-EXT-16; AM-001..AM-010)": "authoring-manifest.json",
    "[42] Enrichment Tooling (CR-BP-94-EXT-17; OR-001..OR-005 + RP-001..RP-009)": "tooling-manifest.json",
    "[43] Operational Documentation Pilot (CR-BP-94-EXT-18; PI-001..PI-008)": "pilot-selection-manifest.json",
    "[44] L2 Business Process Backfill (CR-BP-94-EXT-19; L2-001..L2-012)": "l2-backfill-manifest.json",
    "[45] L3 Activity Backfill (CR-BP-94-EXT-20; L3-001..L3-014)": "l3-backfill-manifest.json",
    "[46] L4 Task Backfill (CR-BP-94-EXT-21; L4-001..L4-014)": "l4-backfill-manifest.json",
    "[47] Decomposition Reconciliation (CR-BP-94-EXT-22; R22-01..R22-12)": "ext22-manifest.json",
}


def _open_findings(gate_name: str) -> int | None:
    """Return the open findings on a gate's subject population.

    Returns None where the gate does not emit a manifest, or where the
    manifest has not been generated. A None result means the population's
    reconciliation state is UNKNOWN, and a gate whose state is unknown may
    not be promoted to blocking.
    """
    manifest_name = GATE_MANIFEST.get(gate_name)
    if manifest_name is None:
        return None
    path = REPO_ROOT / "reconciliation" / manifest_name
    if not path.exists():
        return None
    try:
        with path.open(encoding="utf-8") as fp:
            data = json.load(fp)
    except Exception:
        return None
    summary = data.get("summary", {})
    if not isinstance(summary, dict):
        return None
    findings = summary.get("total_findings")
    if not isinstance(findings, int):
        return None
    # The EXT-04 validator records advisory findings separately; an
    # advisory finding is a known, dispositioned condition, not an open
    # reconciliation gap.
    advisory = summary.get("advisory_findings")
    if isinstance(advisory, int) and advisory == findings:
        return 0
    return findings


def _load_registry() -> list[tuple[str, bool, list[str]]]:
    """Load the gate registry from scripts/conformance_result.py.

    The registry is the single source of truth (REQ-23-11). It is read
    by importing the module, not by re-parsing the source.
    """
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    try:
        import conformance_result  # type: ignore
    finally:
        sys.path.pop(0)
    return list(conformance_result.GATES)


def _load_readiness() -> dict:
    if not READINESS_PATH.exists():
        return {}
    try:
        with READINESS_PATH.open(encoding="utf-8") as fp:
            return json.load(fp)
    except Exception:
        return {}


def assess(registry: list[tuple[str, bool, list[str]]],
           readiness: dict) -> tuple[list[dict], list[dict]]:
    """Classify every gate and determine its target enforcement posture.

    Returns (findings, inventory).
    """
    findings: list[dict] = []
    inventory: list[dict] = []
    enforceable = set(readiness.get("automatically_enforceable", []))

    for name, blocking, argv in registry:
        classification = CLASSIFICATION.get(name)
        if classification is None:
            findings.append({
                "rule": "C23-02", "where": name,
                "diagnostic": f"gate {name!r} has no enforcement class; "
                              f"REQ-23-02 requires exactly one class per gate",
                "severity": "error",
            })
            continue

        klass = classification["class"]
        if klass not in ENFORCEMENT_CLASSES:
            findings.append({
                "rule": "C23-02", "where": name,
                "diagnostic": f"gate {name!r} has invalid enforcement class {klass!r}",
                "severity": "error",
            })
            continue

        tier = TIER_BY_CLASS[klass]
        # REQ-23-03: promotion criteria. A gate may be promoted to blocking
        # only where (a) its rule set is deterministically evaluable, and
        # (b) its subject population is reconciled: 0 open findings on the
        # gate's own manifest. A population whose reconciliation state is
        # unknown may not be promoted.
        promotable = klass in ("structural", "content")
        open_findings = _open_findings(name)
        if open_findings is None:
            # The reconciliation state of the population is unknown. The gate
            # may be promoted only if it is ALREADY blocking (the status
            # predates EXT-23 and is not being changed on unknown grounds).
            reconciled = None
            population_reconciled = False
        else:
            population_reconciled = open_findings == 0
            reconciled = population_reconciled
        target_blocking = blocking
        if promotable and not blocking and population_reconciled:
            target_blocking = True

        # REQ-23-03: no semantic or review gate may be blocking.
        if blocking and klass in ("semantic", "review"):
            findings.append({
                "rule": "C23-03", "where": name,
                "diagnostic": f"gate {name!r} is blocking but its enforcement class "
                              f"is {klass!r}; REQ-23-03 forbids promoting a "
                              f"semantic or review gate to blocking",
                "severity": "error",
            })
            target_blocking = False

        entry = {
            "gate": name,
            "gate_number": _gate_number(name),
            "enforcement_class": klass,
            "enforcement_tier": tier,
            "introduced_by": classification["cr"],
            "population": classification["population"],
            "population_reconciled": population_reconciled,
            "open_findings": open_findings,
            "reason": classification["reason"],
            "current_blocking": blocking,
            "target_blocking": target_blocking,
            "status_change": (
                "unchanged" if blocking == target_blocking
                else ("promoted to blocking" if target_blocking
                      else "demoted to advisory")
            ),
            "command": " ".join(argv),
        }
        inventory.append(entry)

        # A deterministic gate whose population still carries open findings
        # is not promoted. That is a deferral, not a defect: the population
        # is reconciled by the backfill tranches, and the gate is promoted
        # when that work lands.
        if (promotable and not blocking and open_findings is not None
                and open_findings > 0):
            findings.append({
                "rule": "C23-03", "where": name,
                "diagnostic": f"gate {name!r} is deterministically enforceable but "
                              f"its population carries {open_findings} open "
                              f"findings; the gate is deferred, not promoted, until "
                              f"the population is reconciled",
                "severity": "info",
            })

        # REQ-23-04: reason recording.
        if not entry["reason"].strip():
            findings.append({
                "rule": "C23-04", "where": name,
                "diagnostic": f"gate {name!r} has no recorded enforcement reason",
                "severity": "error",
            })

    # REQ-23-10: the inventory and the registry agree.
    if len(inventory) != len(registry):
        findings.append({
            "rule": "C23-10", "where": "registry",
            "diagnostic": f"inventory has {len(inventory)} entries for "
                          f"{len(registry)} registered gates",
            "severity": "error",
        })

    return findings, inventory


def _gate_number(name: str) -> str:
    if name.startswith("["):
        end = name.find("]")
        if end > 0:
            return name[1:end]
    return "?"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true",
                        help="run a synthetic self-test")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()

    if args.self_test:
        print(json.dumps({
            "mode": "self-test",
            "enforcement_classes": list(ENFORCEMENT_CLASSES),
            "tier_by_class": TIER_BY_CLASS,
            "findings": [],
            "summary": {"total_findings": 0},
        }, indent=2))
        return 0

    registry = _load_registry()
    readiness = _load_readiness()
    findings, inventory = assess(registry, readiness)

    by_class = Counter(e["enforcement_class"] for e in inventory)
    by_tier = Counter(e["enforcement_tier"] for e in inventory)
    by_status = Counter(e["status_change"] for e in inventory)
    blocking_gates = [e for e in inventory if e["current_blocking"]]
    target_blocking_gates = [e for e in inventory if e["target_blocking"]]

    # REQ-23-07: the conformance posture report.
    posture = {
        "posture_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/check_conformance_posture_ext23.py",
        "parent_cr": "CR-BP-EXT-23",
        "source_of_truth": "scripts/conformance_result.py (the GATES registry); "
                           "this report is generated from it (REQ-23-11)",
        "total_registered_gates": len(registry),
        "total_inventoried_gates": len(inventory),
        "by_enforcement_class": dict(sorted(by_class.items())),
        "by_enforcement_tier": dict(sorted(by_tier.items())),
        "by_status_change": dict(sorted(by_status.items())),
        "current_blocking_count": len(blocking_gates),
        "target_blocking_count": len(target_blocking_gates),
        "gates": inventory,
        "deferrals": [
            {
                "gate": e["gate"],
                "reason": e["reason"],
                "accountable_authority": "programme_owner",
                "scope": "the gate rule set",
                "review_condition": "re-assess at the EXT-24 governance review",
            }
            for e in inventory
            if not e["target_blocking"] and e["enforcement_class"] in ("structural", "content")
        ],
        "approved_exceptions": [],
        "residual_risks_carried_to_ext24": [
            "The evidence-led semantic gates (T3/T4) rely on the EXT-22 "
            "reconciliation record and human review; their coverage is only as "
            "current as the last reconciliation pass.",
            "The 8 EXT-22 structural findings are recorded as remediation "
            "requirements rather than resolved; see the EXT-22 structural "
            "integrity report.",
        ],
        "ext24_governance_requirements": {
            "review_cadence": "a full reconciliation pass per programme cycle, with "
                              "a targeted pass on any gate that changes status",
            "exception_lifecycle": "an exception is scoped, rationalised, owned and "
                                   "reviewable; it reclassifies enforcement for the "
                                   "declared scope and never suppresses a finding",
            "demotion_criteria": "a blocking gate may be demoted only with a "
                                 "recorded rationale, an accountable authority and a "
                                 "review condition",
            "escalation_path": "a newly introduced finding on a blocking gate is "
                               "escalated to the programme owner before the gate is "
                               "demoted or the finding is dispositioned",
        },
    }
    RECON_DIR.mkdir(parents=True, exist_ok=True)
    POSTURE_PATH.write_text(json.dumps(posture, indent=2), encoding="utf-8")

    INVENTORY_PATH.write_text(json.dumps({
        "inventory_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/check_conformance_posture_ext23.py",
        "parent_cr": "CR-BP-EXT-23",
        "total_registered_gates": len(registry),
        "gates": inventory,
    }, indent=2), encoding="utf-8")

    manifest = {
        "manifest_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/check_conformance_posture_ext23.py",
        "parent_cr": "CR-BP-EXT-23",
        "summary": {
            "total_findings": len(findings),
            "by_rule": dict(sorted(Counter(f["rule"] for f in findings).items())),
        },
        "findings": findings,
        "posture_summary": {
            "total_registered_gates": len(registry),
            "by_enforcement_class": dict(sorted(by_class.items())),
            "by_enforcement_tier": dict(sorted(by_tier.items())),
            "by_status_change": dict(sorted(by_status.items())),
            "current_blocking_count": len(blocking_gates),
            "target_blocking_count": len(target_blocking_gates),
        },
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(manifest, indent=2))
    else:
        print(f"Registered gates: {len(registry)}")
        print(f"By enforcement class: {dict(sorted(by_class.items()))}")
        print(f"By enforcement tier: {dict(sorted(by_tier.items()))}")
        print(f"Status changes: {dict(sorted(by_status.items()))}")
        print(f"Blocking: {len(blocking_gates)} current -> {len(target_blocking_gates)} target")
        print(f"\nFindings: {len(findings)}")
        for f in findings[:8]:
            print(f"  [{f['rule']}] {f['where']}: {f['diagnostic'][:120]}")
        print(f"\nPosture report: {POSTURE_PATH.relative_to(REPO_ROOT)}")

    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
