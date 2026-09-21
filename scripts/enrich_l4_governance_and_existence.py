#!/usr/bin/env python3
"""
enrich_l4_governance_and_existence.py
CR-BP-L4-03: GovernanceAndExistence per-domain L4 Task content enrichment.

Replaces the templated definition / trigger / outcome / responsibility /
boundary.inclusions / boundary.exclusions / evidence[] content of every
GovernanceAndExistence L4 Task record with cell-specific, sector-grounded
prose describing the bounded work performed by each phase custodian.

Scope: 340 Tasks (68 Activities x 5 phases) across 7 cells
(Activate 20 / Build 60 / Conceive 40 / Design 60 / Improve 60 / Operate 80 /
Retire 20). Idempotent on rerun.

Mirrors the CR-BP-L4-02 pattern (P&R enrichment); per-domain table swap
with the same 5-phase bounded-work shape.

Usage:
  python scripts/enrich_l4_governance_and_existence.py [--dry-run] [--scope SUFFIX]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTITIES = ROOT / "entities" / "v1-alpha"

DOMAIN = "GovernanceAndExistence"

PHASE_ROLE = {
    "intake": "designated intake custodian",
    "verify": "verification custodian",
    "transform": "processing custodian",
    "confirm": "confirmation custodian",
    "record": "records custodian",
}

# Per-(stage, phase) bounded-work prose. GovernanceAndExistence covers the
# entity's legal constitution, governance apparatus, policy and risk
# frameworks, assurance machinery, and statutory wind-down.
BOUNDED_WORK = {
    ("Activate", "intake"):
        "accept custody of the legal-commencement input pack (constitutive "
        "instrument, commencement-order reference, obligations-and-rights "
        "schedule) and persist a registered intake manifest binding the "
        "commencement event to the activation case file.",
    ("Activate", "verify"):
        "verify the commencement conditions against the constitutive "
        "instrument and the governing statute (incorporation formalities, "
        "regulatory authorization prerequisites), and emit a verification "
        "certificate naming the conditions verified and any unmet "
        "prerequisites flagged for remediation.",
    ("Activate", "transform"):
        "effect the commencement: register the instrument with the "
        "competent authority, establish the enforcement baseline (the "
        "obligations-and-rights schedule as in force at commencement), and "
        "produce the activated-instrument record conforming to the "
        "legal-commencement schema.",
    ("Activate", "confirm"):
        "reconcile the activated-instrument record against the "
        "constitutive instrument and the governing statute, issue the "
        "commencement confirmation to the governance custodian and the "
        "obligated parties, and log the confirmation against the case file.",
    ("Activate", "record"):
        "retain the commencement case file (intake manifest, verification "
        "certificate, activated-instrument record, confirmation "
        "acknowledgement, and any condition-remediation trail) under the "
        "statutory-records retention schedule with cryptographic integrity "
        "protection.",

    ("Build", "intake"):
        "accept custody of the governance-apparatus input pack (charter "
        "drafts, policy drafts, body-constitution proposals, monitoring-"
        "tooling specifications) and persist a registered intake manifest "
        "binding the build package to the apparatus case file.",
    ("Build", "verify"):
        "verify the build package against the governance-framework "
        "contract (OECD / King IV structural requirements), the "
        "committee-charter completeness rules, and the monitoring-tooling "
        "specification, and emit a verification report naming any "
        "structural deviations and their remediation.",
    ("Build", "transform"):
        "execute the build: codify the charters and policies, constitute "
        "the bodies, establish the operating cycles and reporting lines, "
        "establish the risk registers, deploy the monitoring tooling, and "
        "produce the build-ready apparatus inventory conforming to the "
        "governance-apparatus schema.",
    ("Build", "confirm"):
        "reconcile the build-ready apparatus inventory against the "
        "governance-framework contract and the committee-charter "
        "completeness rules, issue the apparatus-completion confirmation "
        "to the governance custodian, and log the confirmation.",
    ("Build", "record"):
        "retain the apparatus build package (intake manifest, verification "
        "report, build-ready apparatus inventory, apparatus-completion "
        "confirmation, and any structural-deviation remediations) under "
        "the governance-records retention schedule with cryptographic "
        "integrity protection.",

    ("Conceive", "intake"):
        "accept custody of the policy-conception input pack (risk-appetite "
        "drafts, policy-scope proposals, authority-and-decision-rights "
        "proposals) and persist a registered intake manifest binding the "
        "inputs to the conception case file.",
    ("Conceive", "verify"):
        "verify the input pack against the risk-framework methodology "
        "(ISO 31000 / COSO ERM) and the policy-scope bounding rules, and "
        "emit a verification report naming any methodology deviations and "
        "their remediation.",
    ("Conceive", "transform"):
        "execute the conception: articulate the risk appetite, bound the "
        "policy scope, frame the governance posture for risk, propose the "
        "authority and decision rights, define the tolerance bands, and "
        "produce the conception-ready framework package conforming to the "
        "risk-and-policy conception schema.",
    ("Conceive", "confirm"):
        "reconcile the conception-ready framework package against the "
        "risk-framework methodology and the policy-scope bounding rules, "
        "issue the conception-completion confirmation to the governance "
        "custodian, and log the confirmation.",
    ("Conceive", "record"):
        "retain the conception package (intake manifest, verification "
        "report, conception-ready framework package, conception-completion "
        "confirmation, and any methodology-deviation remediations) under "
        "the risk-framework records retention schedule with cryptographic "
        "integrity protection.",

    ("Design", "intake"):
        "accept custody of the governance-design input pack (conception "
        "framework reference, body-architecture proposals, delegation "
        "models, compliance-regime requirements) and persist a registered "
        "intake manifest binding the inputs to the design case file.",
    ("Design", "verify"):
        "verify the input pack against the governance-architecture "
        "standards (OECD Principles, King IV outcomes) and the "
        "delegation-of-authority contract, and emit a verification report "
        "naming any architecture deviations and their remediation.",
    ("Design", "transform"):
        "execute the design: articulate the governance bodies, design the "
        "authority delegations and decision rights, design the policy "
        "artifacts and control objectives, design the risk taxonomy and "
        "assessment scales, design the compliance regime and governance "
        "integration, and produce the design-ready governance artefact "
        "conforming to the governance-design schema.",
    ("Design", "confirm"):
        "reconcile the design-ready governance artefact against the "
        "governance-architecture standards and the delegation-of-authority "
        "contract, issue the design-completion confirmation to the "
        "governance custodian, and log the confirmation.",
    ("Design", "record"):
        "retain the design package (intake manifest, verification report, "
        "design-ready governance artefact, design-completion confirmation, "
        "and any architecture-deviation remediations) under the "
        "governance-design records retention schedule with cryptographic "
        "integrity protection.",

    ("Improve", "intake"):
        "accept custody of the improvement-case input pack (finding "
        "register, effectiveness-review scope, policy-gap inventory) and "
        "persist a registered intake manifest binding the inputs to the "
        "improvement case file.",
    ("Improve", "verify"):
        "verify the input pack against the internal-audit methodology "
        "(IIA IPPF) and the finding-classification contract, and emit a "
        "verification report naming any methodology deviations and their "
        "remediation.",
    ("Improve", "transform"):
        "execute the improvement: measure governance performance, measure "
        "policy gaps, score finding severity, assess finding recurrence, "
        "capture lessons learned, formulate effectiveness recommendations, "
        "and produce the improvement-ready outcomes pack conforming to the "
        "assurance-improvement schema.",
    ("Improve", "confirm"):
        "reconcile the improvement-ready outcomes pack against the "
        "internal-audit methodology and the finding-classification "
        "contract, issue the improvement-completion confirmation to the "
        "governance custodian and the audit committee, and log the "
        "confirmation.",
    ("Improve", "record"):
        "retain the improvement package (intake manifest, verification "
        "report, improvement-ready outcomes pack, improvement-completion "
        "confirmation, and any methodology-deviation remediations) under "
        "the assurance-records retention schedule with cryptographic "
        "integrity protection.",

    ("Operate", "intake"):
        "accept custody of the governance-operating input pack (board and "
        "committee cycle schedule, assurance-evidence queue, risk-review "
        "calendar, compliance-audit plan) and persist a registered intake "
        "manifest binding the inputs to the operating case file.",
    ("Operate", "verify"):
        "verify the input pack against the board-cycle contract "
        "(statutory meeting-frequency requirements), the assurance-"
        "evidence standards (IIA), and the risk-review methodology (ISO "
        "31000), and emit a verification report naming any contract "
        "deviations and their remediation.",
    ("Operate", "transform"):
        "execute the operating rhythm: run the board and committee cycles, "
        "maintain the governance machinery, maintain the risk registers, "
        "surface risk exposures, execute the risk reviews and compliance "
        "audits, assemble the assurance evidence, facilitate governance "
        "decisions, and produce the operating-ready outcomes pack "
        "conforming to the governance-operating schema.",
    ("Operate", "confirm"):
        "reconcile the operating-ready outcomes pack against the "
        "board-cycle contract and the assurance-evidence standards, issue "
        "the operating-completion confirmation to the governance custodian "
        "and the board secretary, and log the confirmation.",
    ("Operate", "record"):
        "retain the operating package (intake manifest, verification "
        "report, operating-ready outcomes pack, operating-completion "
        "confirmation, and any contract-deviation remediations) under the "
        "governance-operating records retention schedule with "
        "cryptographic integrity protection.",

    ("Retire", "intake"):
        "accept custody of the wind-down input pack (regulator or court "
        "order reference, retained-records inventory, dissolution-filing "
        "drafts) and persist a registered intake manifest binding the "
        "inputs to the wind-down case file.",
    ("Retire", "verify"):
        "verify the input pack against the dissolution statute (DGCL "
        "§§275-283 / UK Insolvency Act 1986 Part IV), the wind-down quorum "
        "requirements, and the retained-records custodianship contract, "
        "and emit a verification report naming any statutory deviations "
        "and their remediation.",
    ("Retire", "transform"):
        "execute the wind-down: assess the regulator or court order scope, "
        "assign the retained-records custodianship, reduce the governance "
        "apparatus to the wind-down quorum, submit the statutory "
        "dissolution filings, and produce the wind-down-ready record pack "
        "conforming to the dissolution schema.",
    ("Retire", "confirm"):
        "reconcile the wind-down-ready record pack against the dissolution "
        "statute and the retained-records custodianship contract, issue "
        "the wind-down completion confirmation to the governance custodian "
        "and the registrar of companies, and log the confirmation.",
    ("Retire", "record"):
        "retain the wind-down package (intake manifest, verification "
        "report, wind-down-ready record pack, wind-down completion "
        "confirmation, and any statutory-deviation remediations) under "
        "the dissolved-entity records retention schedule with "
        "cryptographic integrity protection for the full statutory "
        "retention horizon.",
}

STAGE_GOVERNING = {
    "Activate": "Delaware DGCL §§101-108 (formation + commencement); UK Companies Act 2006 "
                "Part 2; Model Business Corporation Act §2.03; EU Directive 2017/1132 "
                "(company law harmonization).",
    "Build":     "OECD Principles of Corporate Governance (G20/OECD 2023); King IV Report "
                "(IoDSA 2016); UK Corporate Governance Code 2018; IIA Three Lines Model.",
    "Conceive":  "ISO 31000:2018 (risk management guidelines); COSO ERM 2017; Basel "
                "Committee risk-governance guidance (BCBS 328); FSB Principles for Sound "
                "Risk Governance.",
    "Design":    "OECD Principles G20/OECD 2023 Chapter VI (board responsibilities); "
                "King IV outcomes-based governance; COSO Internal Control 2013; "
                "UK Companies Act 2006 §172 (stakeholder duty).",
    "Improve":   "IIA International Professional Practices Framework (IPPF 2017 incl. "
                "2024 Global Internal Audit Standards); ISO 19011:2018 (audit programme "
                "guidelines); COSO monitoring component.",
    "Operate":   "UK Companies Act 2006 Part 10 (directors) + Part 15 (accounts); "
                "Sarbanes-Oxley §§301-302 (audit committee + certification); "
                "SEC Rule 14a-21 (say-on-pay); IIA attribute standards 1100-1322.",
    "Retire":    "Delaware DGCL §§275-283 (dissolution and winding up); UK Insolvency "
                "Act 1986 Part IV; UNCITRAL Model Law on Enterprise Group Insolvency; "
                "statutory records retention post-dissolution (e.g. UK CA 2006 §388, "
                "10-year accounting records).",
}

STAGE_EVIDENCE = {
    "Activate": [
        {"source": "Delaware DGCL §§101-108 (Formation and Commencement)",
         "strength": "E1",
         "claim_role": "statutory formation and commencement provisions binding the activate-phase verification step to incorporation formalities."},
        {"source": "UK Companies Act 2006 Part 2",
         "strength": "E1",
         "claim_role": "UK formation statute grounding the activate-phase commencement-condition checks and the constitutive-instrument registration."},
        {"source": "EU Directive 2017/1132 (Company Law)",
         "strength": "E2",
         "claim_role": "EU company-law harmonization directive grounding the cross-border constitutive-instrument recognition in the activate-phase."},
    ],
    "Build": [
        {"source": "OECD Principles of Corporate Governance (G20/OECD 2023)",
         "strength": "E1",
         "claim_role": "international governance benchmark binding the build-phase structural verification (charter completeness, body constitution) to a recognised framework."},
        {"source": "King IV Report (IoDSA 2016)",
         "strength": "E2",
         "claim_role": "outcomes-based governance report grounding the build-phase committee-charter completeness rules and operating-cycle design."},
        {"source": "IIA Three Lines Model",
         "strength": "E2",
         "claim_role": "assurance-architecture model grounding the build-phase monitoring-tooling specification and reporting-line establishment."},
    ],
    "Conceive": [
        {"source": "ISO 31000:2018 (Risk Management Guidelines)",
         "strength": "E1",
         "claim_role": "international risk-management standard binding the conceive-phase risk-framework methodology verification and the tolerance-band definition."},
        {"source": "COSO ERM 2017",
         "strength": "E2",
         "claim_role": "enterprise risk-management framework grounding the conceive-phase risk-appetite articulation and governance-posture framing."},
        {"source": "Basel Committee BCBS 328 (Risk Governance)",
         "strength": "E1",
         "claim_role": "banking-sector risk-governance standard grounding the conceive-phase authority-and-decision-rights proposal."},
    ],
    "Design": [
        {"source": "OECD Principles G20/OECD 2023 Chapter VI",
         "strength": "E1",
         "claim_role": "board-responsibilities chapter binding the design-phase body articulation and delegation-of-authority design."},
        {"source": "COSO Internal Control 2013",
         "strength": "E2",
         "claim_role": "internal-control framework grounding the design-phase control-objective definition and compliance-regime design."},
        {"source": "UK Companies Act 2006 §172",
         "strength": "E1",
         "claim_role": "stakeholder-duty provision grounding the design-phase decision-rights specification and governance-integration design."},
    ],
    "Improve": [
        {"source": "IIA IPPF / Global Internal Audit Standards 2024",
         "strength": "E1",
         "claim_role": "internal-audit professional framework binding the improve-phase finding classification and effectiveness-review methodology."},
        {"source": "ISO 19011:2018 (Audit Programme Guidelines)",
         "strength": "E2",
         "claim_role": "audit-programme standard grounding the improve-phase measurement methodology and finding-severity scoring."},
        {"source": "COSO Monitoring Component",
         "strength": "E2",
         "claim_role": "monitoring framework grounding the improve-phase governance-performance measurement and policy-gap measurement."},
    ],
    "Operate": [
        {"source": "UK Companies Act 2006 Part 10 + Part 15",
         "strength": "E1",
         "claim_role": "directors and accounts provisions binding the operate-phase board-cycle contract and statutory meeting-frequency requirements."},
        {"source": "Sarbanes-Oxley §§301-302",
         "strength": "E1",
         "claim_role": "audit-committee and certification provisions binding the operate-phase compliance-audit execution and assurance-evidence standards."},
        {"source": "IIA Attribute Standards 1100-1322",
         "strength": "E2",
         "claim_role": "internal-audit attribute standards grounding the operate-phase assurance-evidence assembly and audit-quality maintenance."},
    ],
    "Retire": [
        {"source": "Delaware DGCL §§275-283 (Dissolution)",
         "strength": "E1",
         "claim_role": "statutory dissolution and winding-up provisions binding the retire-phase verification and the statutory dissolution filings."},
        {"source": "UK Insolvency Act 1986 Part IV",
         "strength": "E1",
         "claim_role": "UK winding-up statute grounding the retire-phase wind-down quorum requirements and registrar filings."},
        {"source": "UK CA 2006 §388 (10-year records retention)",
         "strength": "E2",
         "claim_role": "statutory records-retention provision binding the retire-phase retained-records custodianship and the record-phase retention horizon."},
    ],
}


def _evidence_for(stage: str, parent_activity_id: str, task_phase: str) -> list[dict]:
    stage_sources = STAGE_EVIDENCE[stage]
    out = []
    for s in stage_sources[:2]:
        out.append({
            "source": s["source"],
            "claim": f"{s['claim_role']} Bounded-work evidence for the {task_phase}-phase custodian of `{parent_activity_id}` (CR-BP-L4-03 enrichment).",
            "strength": s["strength"],
        })
    out.append({
        "source": parent_activity_id,
        "claim": "Parent Activity cohesion rationale (CR-BP-32 §6) and the "
                 "CR-BP-L4-03 cell-specific bounded-work prose for this "
                 "GovernanceAndExistence L4 Task.",
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
    phase_words = ["Audit Record", "Confirmation", "Processing", "Verification", "Intake"]
    for pw in phase_words:
        if task_name.endswith(" " + pw):
            return task_name[: -len(pw) - 1]
    return task_name


def _stage_from_task(task: dict) -> str:
    coord = task.get("ecfConformance", {}).get("canonicalReferences", [{}])[0]
    return coord.get("stage", "")


def _enrich_task(task: dict, stage: str, phase: str) -> dict:
    parent_activity = task["belongs_to_activity"]
    human_name = _human_name(task["name"])
    bounded = BOUNDED_WORK[(stage, phase)]

    new_def = (
        f"The bounded unit of work within `{parent_activity}` ({human_name}) "
        f"that {bounded}"
    )

    triggers = {
        "intake":    f"Custody of the {stage}-stage input pack for {human_name} ready for intake; predecessor phase has produced the case file context and intake contract applies.",
        "verify":    f"Intake manifest registered for {human_name}; verification gate may execute the contract and quality-criteria checks against the input pack.",
        "transform": f"Verification certificate issued for {human_name}; transform gate may execute the bounded work and emit the conformant artefact under the {stage} schema.",
        "confirm":   f"Bounded-work artefact produced for {human_name}; confirm gate may reconcile against the governing contract and issue the completion confirmation to the governance custodian.",
        "record":    f"Completion confirmation issued for {human_name}; record gate may retain the case file under the records retention schedule with cryptographic integrity protection.",
    }
    new_trigger = triggers[phase]

    outcomes = {
        "intake":    f"Intake manifest registered and bound to the {human_name} case file; registered intake custodian passes custody to the verification custodian.",
        "verify":    f"Verification certificate issued for {human_name} naming verification methods applied and any deviations remediated; verification custodian passes custody to the processing custodian.",
        "transform": f"Bounded-work artefact produced for {human_name} conforming to the {stage} schema; processing custodian passes custody to the confirmation custodian.",
        "confirm":   f"Completion confirmation issued for {human_name} and acknowledged by the governance custodian and any governing-party notify-list; confirmation custodian passes custody to the records custodian.",
        "record":    f"Case file retained for {human_name} under the records retention schedule with cryptographic integrity protection; statutory retention horizon applied where the governing statute requires.",
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
            f"Retention of the {human_name} case file under the records retention schedule with cryptographic integrity protection.",
            f"Application of the statutory retention horizon for {human_name} records where the governing statute requires.",
        ],
    }
    new_inclusions = inclusions[phase]

    exclusions = {
        "intake": [
            "Re-execution of prior intake phases on rejected or withdrawn cases (no rollback semantics).",
            "Long-term retention of the case file (phase 5).",
        ],
        "verify": [
            "Long-term retention of the case file (phase 5).",
            "Re-execution of prior phases on rejected or withdrawn cases.",
        ],
        "transform": [
            "Long-term retention of the case file (phase 5).",
            "Notification of governing parties outside the notify-list (phase 4).",
        ],
        "confirm": [
            "Long-term retention of the case file (phase 5).",
            "Re-execution of prior phases on confirmation rejection.",
        ],
        "record": [
            "Re-execution of prior phases (no rollback semantics).",
            "Re-classification of records already past the statutory retention horizon (cryptographic destruction is irreversible).",
        ],
    }
    new_exclusions = exclusions[phase]

    new_evidence = _evidence_for(stage, parent_activity, phase)

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