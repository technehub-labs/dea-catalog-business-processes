#!/usr/bin/env python3
"""
enrich_l4_party_and_relationship.py
CR-BP-L4-02: PartyAndRelationship per-domain L4 Task content enrichment.

Replaces the templated definition / trigger / outcome / responsibility /
boundary.inclusions / boundary.exclusions / evidence[] content of every
PartyAndRelationship L4 Task record with cell-specific, sector-grounded
prose describing the bounded work performed by each phase custodian.

Scope: 220 Tasks (44 Activities x 5 phases) across 7 cells
(Activate 20 / Build 40 / Conceive 40 / Design 60 / Improve 20 / Operate 20 /
Retire 20). Idempotent on rerun: the enrichment is a deterministic
re-write of the affected fields; running twice produces the same on-disk
content.

Usage:
  python scripts/enrich_l4_party_and_relationship.py [--dry-run] [--scope SUFFIX]

The companion test file tests/test_enrich_l4_party_and_relationship.py
exercises the bounded-work table, the BP-AR-004 capability edge case
(not present in P&R but asserted for defense), the evidence grounding,
and the live-run validator conformance.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTITIES = ROOT / "entities" / "v1-alpha"

DOMAIN = "PartyAndRelationship"

# Per-phase custodian label.
PHASE_ROLE = {
    "intake": "designated intake custodian",
    "verify": "verification custodian",
    "transform": "processing custodian",
    "confirm": "confirmation custodian",
    "record": "records custodian",
}

# Per-(stage, phase) bounded-work prose: the bounded unit of work performed
# by the named custodian. Each entry is a complete sentence describing
# the action taken, the artifact produced, and the custody transfer.
BOUNDED_WORK = {
    ("Activate", "intake"):
        "accept custody of the incoming party record, identity-document package, "
        "and onboarding-request packet, and persist a registered intake manifest "
        "binding the request to the activation case file.",
    ("Activate", "verify"):
        "execute the multi-factor identity, sanctions/PEP, and adverse-media "
        "verification checks against the registered intake manifest, reconcile the "
        "verification results, and emit a verification certificate naming the "
        "verification methods applied.",
    ("Activate", "transform"):
        "execute the verified-record transformation: resolve the canonical party "
        "identifier, compute the risk classification, derive the due-diligence tier, "
        "and produce the activated-party record conforming to the master-data model.",
    ("Activate", "confirm"):
        "reconcile the activated-party record against the onboarding-decision "
        "criteria and the verification certificate, issue the onboarding "
        "confirmation to the relationship custodian and the activated party, and "
        "log the confirmation against the case file.",
    ("Activate", "record"):
        "retain the onboarding case file (intake manifest, verification "
        "certificate, activated-party record, confirmation acknowledgement, and any "
        "adverse-decision rationale) under the party-records retention schedule "
        "with cryptographic integrity protection.",

    ("Build", "intake"):
        "accept custody of the acquisition-engine design brief (channel mix, "
        "demand-program specification, asset library manifest), confirm the "
        "build-package scope with the channel and demand-program owners, and "
        "persist a registered intake manifest.",
    ("Build", "verify"):
        "verify the build-package against the channel-integration contract, the "
        "consent-capture contract, and the data-quality rules governing PII "
        "handling, and emit a verification report naming any contract violations "
        "and their remediation.",
    ("Build", "transform"):
        "execute the build: provision the channel-integration surface, instantiate "
        "the demand-program assets, calibrate the attribution model, and produce "
        "the build-ready asset inventory conforming to the channel-portfolio "
        "schema.",
    ("Build", "confirm"):
        "reconcile the build-ready asset inventory against the channel-integration "
        "contract and the consent-capture contract, issue the build-completion "
        "confirmation to the channel and demand-program custodians, and log the "
        "confirmation.",
    ("Build", "record"):
        "retain the build package (intake manifest, verification report, "
        "build-ready asset inventory, build-completion confirmation, and any "
        "contract-violation remediations) under the acquisition-engine records "
        "retention schedule with cryptographic integrity protection.",

    ("Conceive", "intake"):
        "accept custody of the segment-thesis input pack (market-research "
        "artefacts, JTBD evidence, demand-thesis drafts) and persist a registered "
        "intake manifest binding the inputs to the conceive case file.",
    ("Conceive", "verify"):
        "verify the input pack against the segment-thesis methodology and the "
        "JTBD-evidence quality criteria, and emit a verification report naming any "
        "methodology deviations and their remediation.",
    ("Conceive", "transform"):
        "execute the conception: frame the segment thesis, articulate the value "
        "exchange, formulate the demand thesis and demand hypotheses, and produce "
        "the conceive-ready thesis package conforming to the segment-strategy "
        "artefact schema.",
    ("Conceive", "confirm"):
        "reconcile the conceive-ready thesis package against the "
        "segment-strategy artefact schema and the JTBD-evidence quality criteria, "
        "issue the conceive-completion confirmation to the strategy custodian, and "
        "log the confirmation.",
    ("Conceive", "record"):
        "retain the conceive package (intake manifest, verification report, "
        "conceive-ready thesis package, conceive-completion confirmation, and any "
        "methodology-deviation remediations) under the segment-strategy records "
        "retention schedule with cryptographic integrity protection.",

    ("Design", "intake"):
        "accept custody of the journey-design input pack (segment thesis "
        "reference, interaction-pattern library, experience-quality criteria) and "
        "persist a registered intake manifest binding the inputs to the design "
        "case file.",
    ("Design", "verify"):
        "verify the input pack against the experience-quality criteria and the "
        "touchpoint-taxonomy contract, and emit a verification report naming any "
        "quality-criteria deviations and their remediation.",
    ("Design", "transform"):
        "execute the design: map the journey stages, identify the moments of "
        "truth, design the touchpoints and interaction patterns, model the "
        "capacity assumptions, and produce the design-ready journey artefact "
        "conforming to the journey-design schema.",
    ("Design", "confirm"):
        "reconcile the design-ready journey artefact against the "
        "experience-quality criteria and the touchpoint-taxonomy contract, issue "
        "the design-completion confirmation to the experience custodian, and log "
        "the confirmation.",
    ("Design", "record"):
        "retain the design package (intake manifest, verification report, "
        "design-ready journey artefact, design-completion confirmation, and any "
        "quality-criteria remediations) under the journey-design records "
        "retention schedule with cryptographic integrity protection.",

    ("Improve", "intake"):
        "accept custody of the improvement-case input pack (churn-risk register, "
        "VoC feedback stream, retention-action candidates) and persist a "
        "registered intake manifest binding the inputs to the improvement case "
        "file.",
    ("Improve", "verify"):
        "verify the input pack against the churn-risk-model contract and the "
        "VoC-quality criteria, and emit a verification report naming any "
        "model-contract deviations and their remediation.",
    ("Improve", "transform"):
        "execute the improvement: assess the churn risk per affected party, "
        "collect and aggregate the customer feedback, execute the retention "
        "actions, and produce the improvement-ready outcomes pack conforming to "
        "the retention outcomes schema.",
    ("Improve", "confirm"):
        "reconcile the improvement-ready outcomes pack against the "
        "churn-risk-model contract and the retention-outcomes schema, issue the "
        "improvement-completion confirmation to the relationship custodian, and "
        "log the confirmation.",
    ("Improve", "record"):
        "retain the improvement package (intake manifest, verification report, "
        "improvement-ready outcomes pack, improvement-completion confirmation, and "
        "any model-contract remediations) under the customer-improvement records "
        "retention schedule with cryptographic integrity protection.",

    ("Operate", "intake"):
        "accept custody of the relationship-operating input pack "
        "(relationship-review schedule, escalation queue, renewal pipeline) and "
        "persist a registered intake manifest binding the inputs to the operating "
        "case file.",
    ("Operate", "verify"):
        "verify the input pack against the account-review-cadence contract and "
        "the KAM-playbook contract, and emit a verification report naming any "
        "contract deviations and their remediation.",
    ("Operate", "transform"):
        "execute the operating rhythm: conduct the relationship reviews, allocate "
        "relationship attention across the portfolio, handle the relationship "
        "escalations, and coordinate the renewals, producing the operating-ready "
        "outcomes pack conforming to the KAM-operating schema.",
    ("Operate", "confirm"):
        "reconcile the operating-ready outcomes pack against the KAM-playbook "
        "contract and the renewal-execution contract, issue the "
        "operating-completion confirmation to the relationship custodian, and log "
        "the confirmation.",
    ("Operate", "record"):
        "retain the operating package (intake manifest, verification report, "
        "operating-ready outcomes pack, operating-completion confirmation, and "
        "any playbook-contract remediations) under the relationship-operating "
        "records retention schedule with cryptographic integrity protection.",

    ("Retire", "intake"):
        "accept custody of the relationship-closure input pack (close-out plan, "
        "outstanding-obligations inventory, records-and-rights register) and "
        "persist a registered intake manifest binding the inputs to the closure "
        "case file.",
    ("Retire", "verify"):
        "verify the input pack against the records-retention schedule, the "
        "obligation-settlement contract, and the data-storage-limitation rules, "
        "and emit a verification report naming any schedule or contract deviations "
        "and their remediation.",
    ("Retire", "transform"):
        "execute the closure: settle the outstanding obligations, execute the "
        "evidenced closure, resolve the records and rights under the "
        "storage-limitation rules, and produce the closure-ready record pack "
        "conforming to the relationship-closure schema.",
    ("Retire", "confirm"):
        "reconcile the closure-ready record pack against the records-retention "
        "schedule and the obligation-settlement contract, issue the "
        "closure-completion confirmation to the relationship custodian and the "
        "records custodian, and log the confirmation.",
    ("Retire", "record"):
        "retain the closure package (intake manifest, verification report, "
        "closure-ready record pack, closure-completion confirmation, and any "
        "retention-schedule remediations) under the relationship-closure records "
        "retention schedule with cryptographic integrity protection, with "
        "cryptographic destruction attestation for records past the "
        "storage-limitation horizon.",
}

# Per-stage governing-sector summary (printed in carrier CR section 2).
STAGE_GOVERNING = {
    "Activate": "FATF Recommendation 10 / 24 (customer due diligence + beneficial ownership); "
                "FinCEN CDD Rule (31 CFR 1010.230); EU AMLD5/6; UK MLR 2017 Reg 33/35; "
                "PCI DSS 4.0 §3.2-3.5; OFAC SDN screening guidance.",
    "Build":     "CRM/loyalty platform contract (Salesforce Industries / Adobe Experience Platform "
                "reference architectures); channel-attribution standards (MRC attribution standards "
                "2023); data-quality governance (DAMA DMBOK2 §10); consent management under "
                "GDPR Art 6/7, ePrivacy Dir 2002/58/EC Art 5(3) / PECR Reg 6.",
    "Conceive":  "Segment strategy practice (Forrester / Bain segmentation); value-exchange design "
                "(Osterwalder value proposition canvas); demand-thesis / JTBD methodology "
                "(Christensen / Ulwick Jobs-to-be-Done); win-loss analysis (Gartner primary research).",
    "Design":    "Customer journey mapping practice (Richardson / Kaplanis touchpoint taxonomy); "
                "experience-quality measurement (NPS / CES standards via Bain Net Promoter System / "
                "Customer Effort Score); interaction-pattern design (NN/g interaction design foundations).",
    "Improve":   "Retention / churn-risk practice (Gartner subscriber retention benchmark; Bain "
                "loyalty economics); voice-of-customer capture (Press Ganey / Medallia VoC "
                "platforms); win-back (Salesforce / HubSpot win-back workflow).",
    "Operate":   "Key-account / strategic-account management practice (SAMA Strategic Account "
                "Management playbook); relationship-review cadence (Gartner account-review "
                "cadence benchmark); renewal-management (TSIA renewal execution benchmark).",
    "Retire":    "Customer offboarding / contract closure practice (IAOP outsourcing transition "
                "standards); records retention (Sarbanes-Oxley §802 / IRS Reg §1.6001-1 / "
                "GDPR Art 5(1)(e)); obligation settlement (UCC §3-302 holder-in-due-course / "
                "commercial-contract netting).",
}

# Per-stage evidence library: cell -> [evidence entries]
STAGE_EVIDENCE = {
    "Activate": [
        {"source": "FATF Recommendation 10 (Customer Due Diligence)",
         "strength": "E1",
         "claim_role": "governing AML/CDD standard for party-activation verification; binds the identity, sanctions, and adverse-media verification step to a regulator-recognised control."},
        {"source": "FinCEN CDD Rule (31 CFR 1010.230)",
         "strength": "E1",
         "claim_role": "US-specific CDD rule establishing minimum identity-verification procedures that the activate-phase verification step operationalises."},
        {"source": "PCI DSS 4.0 §3.2-3.5",
         "strength": "E2",
         "claim_role": "cardholder-data retention and protection standard informing the activate-phase records custodian retention schedule and cryptographic integrity protection."},
    ],
    "Build": [
        {"source": "DAMA DMBOK2 §10 (Data Quality)",
         "strength": "E2",
         "claim_role": "data-quality governance framework informing the build-phase verification step's PII handling and the transform-phase data-quality rules."},
        {"source": "MRC Attribution Standards 2023",
         "strength": "E2",
         "claim_role": "media-rating-council attribution standard informing the build-phase transform step's attribution-model calibration."},
        {"source": "GDPR Art 6/7 + ePrivacy PECR Reg 6",
         "strength": "E1",
         "claim_role": "lawful-basis and consent-capture regulation governing the build-phase consent-capture contract and the verify-phase contract checks."},
    ],
    "Conceive": [
        {"source": "Osterwalder Value Proposition Canvas",
         "strength": "E3",
         "claim_role": "value-exchange design framework grounding the conceive-phase transform step's articulation of the value exchange and the segment-thesis formulation."},
        {"source": "Christensen Jobs-to-be-Done",
         "strength": "E3",
         "claim_role": "JTBD methodology grounding the conceive-phase demand-thesis and demand-hypotheses formulation."},
        {"source": "Gartner Win-Loss primary research methodology",
         "strength": "E3",
         "claim_role": "win-loss analysis methodology grounding the conceive-phase verification step's JTBD-evidence quality criteria."},
    ],
    "Design": [
        {"source": "Bain Net Promoter System methodology",
         "strength": "E2",
         "claim_role": "experience-quality measurement methodology grounding the design-phase experience-quality criteria and the verify-phase quality-criteria checks."},
        {"source": "Nielsen Norman Group interaction-design foundations",
         "strength": "E3",
         "claim_role": "interaction-design framework grounding the design-phase touchpoint and interaction-pattern design step."},
        {"source": "Richardson touchpoint taxonomy",
         "strength": "E3",
         "claim_role": "touchpoint taxonomy grounding the design-phase touchpoint-taxonomy contract and the verify-phase contract checks."},
    ],
    "Improve": [
        {"source": "Gartner Subscriber Retention Benchmark 2024",
         "strength": "E2",
         "claim_role": "industry benchmark grounding the improve-phase churn-risk-model contract and the transform-phase churn-risk assessment."},
        {"source": "Bain Loyalty Economics (Reichheld)",
         "strength": "E2",
         "claim_role": "loyalty-economics methodology grounding the improve-phase retention-actions execution and the retention-outcomes schema."},
        {"source": "Medallia VoC platform methodology",
         "strength": "E3",
         "claim_role": "voice-of-customer capture methodology grounding the improve-phase VoC-feedback stream collection and the VoC-quality criteria."},
    ],
    "Operate": [
        {"source": "SAMA Strategic Account Management playbook",
         "strength": "E2",
         "claim_role": "strategic-account management playbook grounding the operate-phase KAM-playbook contract and the transform-phase operating-rhythm execution."},
        {"source": "TSIA renewal execution benchmark",
         "strength": "E2",
         "claim_role": "renewal-execution benchmark grounding the operate-phase renewal-execution contract and the confirm-phase reconciliation."},
        {"source": "Gartner account-review cadence benchmark",
         "strength": "E3",
         "claim_role": "account-review cadence benchmark grounding the operate-phase account-review-cadence contract."},
    ],
    "Retire": [
        {"source": "Sarbanes-Oxley §802 records retention",
         "strength": "E1",
         "claim_role": "US records-retention statute binding the retire-phase records custodian retention schedule to a regulator-recognised minimum."},
        {"source": "GDPR Art 5(1)(e) storage limitation",
         "strength": "E1",
         "claim_role": "data-protection storage-limitation principle binding the retire-phase storage-limitation rules and the record-phase cryptographic destruction attestation."},
        {"source": "IAOP outsourcing transition standards",
         "strength": "E3",
         "claim_role": "outsourcing-transition framework grounding the retire-phase close-out plan and the obligation-settlement contract."},
    ],
}


def _evidence_for(stage: str, parent_activity_id: str, task_phase: str) -> list[dict]:
    """Build per-Task evidence[]: stage sources + parent-activity cohesion source + CR-BP-L4-02 source.

    Three entries per Task, per TASK-001..005 evidence[2+] requirement.
    """
    stage_sources = STAGE_EVIDENCE[stage]
    out = []
    # First two entries: stage governing sources
    for s in stage_sources[:2]:
        out.append({
            "source": s["source"],
            "claim": f"{s['claim_role']} Bounded-work evidence for the {task_phase}-phase custodian of `{parent_activity_id}` (CR-BP-L4-02 enrichment).",
            "strength": s["strength"],
        })
    # Third entry: parent-activity cohesion rationale + this enrichment CR
    out.append({
        "source": parent_activity_id,
        "claim": "Parent Activity cohesion rationale (CR-BP-32 §6) and the "
                 "CR-BP-L4-02 cell-specific bounded-work prose for this "
                 "PartyAndRelationship L4 Task.",
        "strength": "E3",
    })
    return out


def _phase_from_task_id(task_id: str) -> str:
    """Extract the phase from the task id.

    CR-BP-mv1 form: `processes:task-<domain>-<stage>-<phase>-<hash>`
    (phase is the second-to-last token, before the hash suffix).
    Legacy form: `dea:task-<slug>-<phase>` (phase is the last token).
    """
    tokens = task_id.split("-")
    if len(tokens) >= 2 and tokens[-2] in PHASE_ROLE:
        return tokens[-2]
    suffix = tokens[-1]
    if suffix in PHASE_ROLE:
        return suffix
    raise ValueError(f"Cannot parse phase from task id: {task_id}")


def _human_name(task_name: str) -> str:
    """Strip the trailing phase word to get the human-facing activity name.

    Task name form: '<Activity Name> <Phase Word>' e.g.
    'Verify Party Identity Intake' -> 'Verify Party Identity'.
    The phase words are: Intake / Verification / Processing / Confirmation / Audit Record.
    """
    phase_words = ["Audit Record", "Confirmation", "Processing", "Verification", "Intake"]
    for pw in phase_words:
        if task_name.endswith(" " + pw):
            return task_name[: -len(pw) - 1]
    # Fallback: return as-is (should not happen on well-formed Task records).
    return task_name


def _stage_from_task(task: dict) -> str:
    coord = task.get("ecfConformance", {}).get("canonicalReferences", [{}])[0]
    return coord.get("stage", "")


def _enrich_task(task: dict, stage: str, phase: str) -> dict:
    """Return a copy of the task with enriched prose fields."""
    parent_activity = task["belongs_to_activity"]
    human_name = _human_name(task["name"])
    bounded = BOUNDED_WORK[(stage, phase)]

    # Build new definition, trigger, outcome, responsibility, boundary, evidence.
    new_def = (
        f"The bounded unit of work within `{parent_activity}` ({human_name}) "
        f"that {bounded}"
    )

    # Trigger: phase-specific, derived from the predecessor phase completion.
    triggers = {
        "intake":    f"Custody of the {stage}-stage input pack for {human_name} ready for intake; predecessor phase has produced the case file context and intake contract applies.",
        "verify":    f"Intake manifest registered for {human_name}; verification gate may execute the contract and quality-criteria checks against the input pack.",
        "transform": f"Verification certificate issued for {human_name}; transform gate may execute the bounded work and emit the conformant artefact under the {stage} schema.",
        "confirm":   f"Bounded-work artefact produced for {human_name}; confirm gate may reconcile against the governing contract and issue the completion confirmation to the relationship custodian.",
        "record":    f"Completion confirmation issued for {human_name}; record gate may retain the closure case file under the records retention schedule with cryptographic integrity protection.",
    }
    new_trigger = triggers[phase]

    outcomes = {
        "intake":    f"Intake manifest registered and bound to the {human_name} case file; registered intake custodian passes custody to the verification custodian.",
        "verify":    f"Verification certificate issued for {human_name} naming verification methods applied and any deviations remediated; verification custodian passes custody to the processing custodian.",
        "transform": f"Bounded-work artefact produced for {human_name} conforming to the {stage} schema; processing custodian passes custody to the confirmation custodian.",
        "confirm":   f"Completion confirmation issued for {human_name} and acknowledged by the relationship custodian and any governing-party notify-list; confirmation custodian passes custody to the records custodian.",
        "record":    f"Closure case file retained for {human_name} under the records retention schedule with cryptographic integrity protection; cryptographic destruction attestation recorded where storage-limitation horizons apply.",
    }
    new_outcome = outcomes[phase]

    new_resp = PHASE_ROLE[phase]

    inclusions = {
        "intake": [
            f"Receipt and registration of the {human_name} input pack against the {stage}-stage intake contract.",
            f"Binding of the input pack to the {human_name} case file with cryptographic chain-of-custody.",
        ],
        "verify": [
            f"Execution of the {human_name} contract checks and quality-criteria verification.",
            f"Reconciliation of the input pack against the {human_name} verification certificate requirements.",
        ],
        "transform": [
            f"Execution of the {human_name} bounded work producing the conformant artefact.",
            f"Application of the {human_name} schema and any derived classifications or computations.",
        ],
        "confirm": [
            f"Reconciliation of the {human_name} artefact against the governing contract and any notify-list requirements.",
            f"Issuance of the {human_name} completion confirmation and acknowledgement logging.",
        ],
        "record": [
            f"Retention of the {human_name} closure case file under the records retention schedule with cryptographic integrity protection.",
            f"Issuance of cryptographic destruction attestation for {human_name} records past the storage-limitation horizon.",
        ],
    }
    new_inclusions = inclusions[phase]

    exclusions = {
        "intake": [
            "Re-execution of prior intake phases on rejected or withdrawn cases (no rollback semantics).",
            "Long-term retention of the closure case file (phase 5).",
        ],
        "verify": [
            "Long-term retention of the closure case file (phase 5).",
            "Re-execution of prior phases on rejected or withdrawn cases.",
        ],
        "transform": [
            "Long-term retention of the closure case file (phase 5).",
            "Notification of governing parties outside the notify-list (phase 4).",
        ],
        "confirm": [
            "Long-term retention of the closure case file (phase 5).",
            "Re-execution of prior phases on confirmation rejection.",
        ],
        "record": [
            "Re-execution of prior phases (no rollback semantics).",
            "Re-classification of records already past the storage-limitation horizon (cryptographic destruction is irreversible).",
        ],
    }
    new_exclusions = exclusions[phase]

    new_evidence = _evidence_for(stage, parent_activity, phase)

    # Compose enriched record (preserve all other fields verbatim).
    out = dict(task)
    out["definition"] = new_def
    out["trigger"] = new_trigger
    out["outcome"] = new_outcome
    out["responsibility"] = new_resp
    out["boundary"] = {
        "inclusions": new_inclusions,
        "exclusions": new_exclusions,
    }
    out["evidence"] = new_evidence
    return out


def _walk_tasks(domain: str, scope: str | None = None):
    """Yield (path, task) tuples for every L4 Task in the given domain.

    Optional --scope SUFFIX restricts to tasks whose file path contains SUFFIX
    (substring match against the activity slug or stage).
    """
    for yaml_path in sorted(ENTITIES.rglob("processes-task-*.yaml")):
        # CR-BP-mv1: rglob yields the record FILES directly (containment tree).
        if not yaml_path.is_file():
            continue
        with yaml_path.open() as f:
            data = yaml.safe_load(f)
        coord = data.get("ecfConformance", {}).get("canonicalReferences", [{}])[0]
        if coord.get("domain") != domain:
            continue
        if scope and scope not in str(yaml_path):
            continue
        yield yaml_path, data


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    p.add_argument("--dry-run", action="store_true",
                   help="report counts without writing files")
    p.add_argument("--scope", default=None,
                   help="restrict to tasks whose path contains SUFFIX")
    args = p.parse_args()

    written = 0
    skipped = 0
    by_stage: dict[str, int] = {}
    for path, task in _walk_tasks(DOMAIN, args.scope):
        stage = _stage_from_task(task)
        phase = _phase_from_task_id(task["id"])
        if (stage, phase) not in BOUNDED_WORK:
            print(f"  SKIP (no bounded-work for {stage}/{phase}): {path.name}",
                  file=sys.stderr)
            skipped += 1
            continue
        enriched = _enrich_task(task, stage, phase)
        if args.dry_run:
            written += 1
            by_stage[stage] = by_stage.get(stage, 0) + 1
            continue
        with path.open("w") as f:
            yaml.safe_dump(enriched, f, sort_keys=False, allow_unicode=True,
                           default_flow_style=False, width=1000)
        written += 1
        by_stage[stage] = by_stage.get(stage, 0) + 1

    print(f"L4 Task content enrichment ({DOMAIN}):")
    print(f"  tasks_written: {written}")
    print(f"  tasks_skipped: {skipped}")
    for s in sorted(by_stage):
        print(f"  stage {s}: {by_stage[s]} tasks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())