#!/usr/bin/env python3
"""CR-BP-CE-L0 remediation: complete the 8 escape-clause ProcessContext records.

Adds the canonical required fields (definition, scope, outcomes,
adjacent_contexts, processes, status) derived from each record's own
authoritative cell_charter, and removes the prohibited `version` field.
One-shot migration script for the CE-L0 tranche; not a gate.
"""
from pathlib import Path
from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parent.parent

# Per-record remediation content. definition adapted from the record's own
# cell_charter.combined_semantic_meaning / process_context.scope_summary;
# scope from charter inclusions/exclusions; outcomes from charter
# expected_outcomes; adjacent_contexts per the CE-L0-004 convention
# (all other same-domain lifecycle-stage PCs + cross-domain siblings named
# in the charter's adjacent_boundaries).
REMEDIATION = {
    "pc-ao-activate-kusw2u": {
        "definition": (
            "The bounded enterprise context for **governing the live-readiness "
            "activation of a licensed or regulated workforce** in the **Agency & "
            "Organization** domain: the controlled mobilization of individuals who "
            "must hold regulator-issued licences or registrations before performing "
            "live work, with regulator-controlled scope preserved, "
            "fitness-and-propriety attestation recorded, supervised-training "
            "completion preserved, and continuing-supervisor notification activated."
        ),
        "scope": {
            "includes": [
                "Regulator-issued licence or registration verification",
                "Fitness-and-propriety attestation under the regulator's continuing supervision",
                "Supervised-training completion and competency assessment recording",
                "Signing authority or controlled-function designation",
                "Continuing-supervisor notification and continuing-oversight relationship activation",
            ],
            "excludes": [
                "Workforce recruitment, hiring, and general onboarding (AgencyAndOrganization x Build)",
                "Steady-state workforce performance and development (AgencyAndOrganization x Operate / Improve)",
                "Workforce offboarding and licence surrender (AgencyAndOrganization x Retire; CR-BP-73 adjacent)",
                "Non-licensed workforce activation (reserved; the cell is scoped to licensed roles only)",
                "Capabilities sourcing absent a regulator-controlled scope (AgencyAndOrganization x Build)",
            ],
        },
        "outcomes": [
            "Regulator-controlled scope preserved on the regulated personnel record.",
            "Fitness-and-propriety attestation recorded for the licensed individual.",
            "Supervised-training completion preserved on the regulated personnel record.",
            "Continuing-supervisor notification issued and the continuing-oversight relationship activated.",
            "Licensed workforce role formally live and ready to perform live work.",
        ],
        "adjacent_contexts": [
            "processes:pc-ao-build-pjk4rz",
            "processes:pc-ao-operate-zfevmp",
            "processes:pc-ao-retire-3kqe9c",
            "processes:pc-eo-activate-xdfscw",
            "processes:pc-pv-activate-f7kne7",
        ],
    },
    "pc-ao-retire-3kqe9c": {
        "definition": (
            "The bounded enterprise context for **governing the regulated wind-down "
            "of workforce populations** in the **Agency & Organization** domain: "
            "statutory advance notice, information and consultation with workers' "
            "representatives, fair-selection criteria, severance and benefits "
            "funding, and transition supports under regulated wind-down obligations, "
            "distinct from steady-state agent operations and from asset decommissioning."
        ),
        "scope": {
            "includes": [
                "Statutory advance notice to affected employees and statutory recipients",
                "Information and consultation with workers' representatives",
                "Fair-selection criteria application and recording",
                "Severance, benefits continuation, and statutory liability funding",
                "Transition supports routed to the affected population",
            ],
            "excludes": [
                "Steady-state offboarding of individual agents (AgencyAndOrganization x Operate)",
                "Non-regulated cohort decommission (AgencyAndOrganization x Operate)",
                "Asset retirement and decommissioning (EnablementAndOperations x Retire; CR-BP-66)",
                "Counterparty and agent relationship closure (PartyAndRelationship x Retire; CR-BP-67)",
                "Knowledge archival absent regulated wind-down triggers (AgencyAndOrganization x Operate)",
            ],
        },
        "outcomes": [
            "Statutory advance notice served to affected employees and statutory recipients.",
            "Information and consultation with workers' representatives documented per the controlling statute.",
            "Fair-selection criteria applied and recorded for the affected population.",
            "Severance, benefits continuation, and statutory liability recorded and funded.",
            "Transition supports routed to the affected population.",
        ],
        "adjacent_contexts": [
            "processes:pc-ao-build-pjk4rz",
            "processes:pc-ao-operate-zfevmp",
            "processes:pc-ao-activate-kusw2u",
            "processes:pc-eo-retire-nw3ynf",
            "processes:pc-pr-retire-2cusde",
        ],
    },
    "pc-eo-activate-xdfscw": {
        "definition": (
            "The bounded enterprise context for **governing the activation of an "
            "operations capability whose live service is gated by formal "
            "regulator-issued authorization or certification** in the "
            "**Enablement & Operations** domain, distinct from capability build "
            "and from steady-state operation."
        ),
        "scope": {
            "includes": [
                "Regulator-issued authorization or certification acquisition and recording",
                "Operations capability readiness-assessment evidence recording",
                "Operations manuals and runbooks activation under continuing oversight",
                "Operational controls activation on the regulated operations record",
                "Continuing-supervisor notification and regulated operations record entry",
            ],
            "excludes": [
                "Operations capability conception and design (EnablementAndOperations x Conceive / Design)",
                "Operations capability build and configuration (EnablementAndOperations x Build)",
                "Steady-state operations performance management (EnablementAndOperations x Operate)",
                "Operations capability decommission and deregistration (EnablementAndOperations x Retire)",
                "Non-regulated operations-capability activation absent a regulator-issued authorization regime",
            ],
        },
        "outcomes": [
            "Regulator's authorization on record for the operations capability.",
            "Operations manuals and runbooks live under the regulator's continuing oversight.",
            "Operational controls live on the regulated operations record.",
            "Continuing-supervisor notification issued and the continuing-oversight relationship active.",
            "Regulated operations record entry preserved for the activated operations capability.",
        ],
        "adjacent_contexts": [
            "processes:pc-eo-build-zwkhxc",
            "processes:pc-eo-operate-ydqb96",
            "processes:pc-eo-retire-nw3ynf",
            "processes:pc-ao-activate-kusw2u",
            "processes:pc-pv-activate-f7kne7",
        ],
    },
    "pc-fa-activate-yrhcfm": {
        "definition": (
            "The bounded enterprise context for **governing the activation of a "
            "billing or revenue-recognition capability whose live invoicing is "
            "gated by formal regulator-acknowledged accounting or rate framework "
            "activation** in the **Finance & Accounting** domain, distinct from "
            "capability build and from steady-state billing."
        ),
        "scope": {
            "includes": [
                "Regulator-acknowledged accounting or rate framework activation",
                "Tariff or pricing approval acquisition and recording",
                "Billing-capability readiness-assessment evidence recording",
                "Operational controls activation on the regulated billing record",
                "Continuing-supervisor notification and regulated billing record entry",
            ],
            "excludes": [
                "Billing-capability conception and design (FinanceAndAccounting x Conceive / Design)",
                "Billing-capability build and configuration (FinanceAndAccounting x Build)",
                "Steady-state billing operations performance management (FinanceAndAccounting x Operate)",
                "Billing-capability decommission and deregistration (FinanceAndAccounting x Retire; CR-BP-75 adjacent)",
                "Non-regulated billing-capability activation absent a regulator-acknowledged framework",
            ],
        },
        "outcomes": [
            "Regulator's acknowledgement on record for the billing or revenue-recognition capability.",
            "Tariff or pricing approval preserved on the regulated billing record.",
            "Operational controls live on the regulated billing record.",
            "Continuing-supervisor notification issued and the continuing-oversight relationship active.",
            "Regulated billing record entry preserved for the activated billing capability.",
        ],
        "adjacent_contexts": [
            "processes:pc-fa-build-pztsp9",
            "processes:pc-fa-operate-afew7e",
            "processes:pc-fa-retire-64q5p9",
            "processes:pc-ao-activate-kusw2u",
            "processes:pc-eo-activate-xdfscw",
        ],
    },
    "pc-fa-retire-64q5p9": {
        "definition": (
            "The bounded enterprise context for **governing the retirement of a "
            "regulated financial entity under statutory run-off obligations** in "
            "the **Finance & Accounting** domain: regulator-acknowledged run-off "
            "authorisation, run-off plan submission, statutory accounting basis "
            "transition, reserving and capital adequacy, policyholder-priority "
            "claims adjudication, and stakeholder communications, distinct from "
            "pre-run-off stewardship and from physical asset decommissioning."
        ),
        "scope": {
            "includes": [
                "Regulator-acknowledged run-off authorisation",
                "Run-off plan submission within the controlling regulator's window",
                "Statutory accounting basis transition to liquidation-basis or fulfillment-measurement",
                "Reserving, capital adequacy, and asset-liability matching throughout the run-off period",
                "Policyholder priority creditor treatment and claim adjudication",
                "Communications to policyholders and stakeholders",
            ],
            "excludes": [
                "Pre-run-off financial stewardship (FinanceAndAccounting x Operate)",
                "Physical asset decommissioning (EnablementAndOperations x Retire; CR-BP-66)",
                "Counterparty and agent relationship closure (PartyAndRelationship x Retire; CR-BP-67)",
                "Product line retirement (ProductAndValue x Retire; CR-BP-67 adjacent)",
                "Non-insurance regulated wind-downs (deferred to a future CR)",
            ],
        },
        "outcomes": [
            "Regulator-acknowledged run-off authorisation documented per the controlling regulator's requirements.",
            "Run-off plan submitted within the controlling regulator's window.",
            "Statutory accounting basis established for insurance liabilities and held assets.",
            "Reserving and capital adequacy maintained throughout the run-off period.",
            "Policyholder claims adjudicated and paid under policyholder-priority creditor treatment.",
        ],
        "adjacent_contexts": [
            "processes:pc-fa-operate-afew7e",
            "processes:pc-fa-activate-yrhcfm",
            "processes:pc-eo-retire-nw3ynf",
            "processes:pc-pr-retire-2cusde",
            "processes:pc-ge-retire-kndw6x",
        ],
    },
    "pc-ge-retire-kndw6x": {
        "definition": (
            "The bounded enterprise context for **governing the wind-down of "
            "governance bodies, policy regimes, mandates, and constitutional "
            "instruments under regulator or court mandate** in the **Governance & "
            "Existence** domain: statutory dissolution filings, retained-records "
            "custodianship, policy sunset, governance-body quorum reduction, and "
            "surrender of authorisation, distinct from voluntary governance sunset "
            "and from adjacent Retire cells."
        ),
        "scope": {
            "includes": [
                "Regulator- or court-issued mandatory dissolution, revocation, or wind-down order execution",
                "Governance-bodies reduction to wind-down quorum under the controlling statute",
                "Policy instrument sunset per the governance constitution",
                "Statutory dissolution filings to the controlling authority",
                "Retained-records custodianship assignment per the service-of-process regime",
                "Surrender of authorisation or cancellation of permission",
            ],
            "excludes": [
                "Voluntary governance sunset absent regulator or court mandate (GovernanceAndExistence x Improve; CR-BP-63)",
                "Asset retirement and decommissioning (EnablementAndOperations x Retire; CR-BP-66)",
                "Counterparty and agent relationship closure (PartyAndRelationship x Retire; CR-BP-67)",
                "Workforce wind-down under statutory mass-layoff thresholds (AgencyAndOrganization x Retire; CR-BP-73)",
                "Regulated entity run-off (FinanceAndAccounting x Retire; CR-BP-75)",
            ],
        },
        "outcomes": [
            "The governance regime is wound down under the controlling regulator or court authority.",
            "Policy instruments are sunset per the governance constitution.",
            "Statutory dissolution filings are submitted to the controlling authority.",
            "Retained-records custodianship is assigned per the service-of-process regime.",
            "The entity is dissolved or the authorisation is cancelled per the regulator or court determination.",
        ],
        "adjacent_contexts": [
            "processes:pc-ge-operate-hb2dac",
            "processes:pc-ge-improve-c78ppp",
            "processes:pc-eo-retire-nw3ynf",
            "processes:pc-ao-retire-3kqe9c",
            "processes:pc-fa-retire-64q5p9",
        ],
    },
    "pc-sd-activate-ghaub8": {
        "definition": (
            "The bounded enterprise context for **governing the activation of a "
            "regulated entity's strategic plan whose live execution is gated by "
            "formal supervisor-acknowledged strategic-plan filing** in the "
            "**Strategy & Direction** domain, distinct from strategy build and from "
            "steady-state strategy execution."
        ),
        "scope": {
            "includes": [
                "Supervisor-acknowledged strategic-plan filing",
                "Supervisor's review completion and acknowledgement on record",
                "Filing receipt preservation and regulated-records entry",
                "Operational monitoring framework launch (KPIs; early-warning indicators)",
                "Communications plan activation under the regulator's continuing supervision",
            ],
            "excludes": [
                "Strategic-plan conception, design, and build (StrategyAndDirection x Conceive / Design / Build)",
                "Steady-state strategy execution and performance review (StrategyAndDirection x Operate / Improve)",
                "Strategic-plan sunset under regulatory mandate (StrategyAndDirection x Retire)",
                "Non-regulated strategic-plan launch absent a supervisor-acknowledged filing regime",
            ],
        },
        "outcomes": [
            "Supervisor's acknowledgement on record for the regulated strategic plan.",
            "Filing receipt preserved on the regulated strategic-plan record.",
            "Operational monitoring framework live on the regulated strategic-plan record.",
            "Communications plan activated under the regulator's continuing supervision.",
            "Regulated strategic-plan record entry preserved for the activated strategic plan.",
        ],
        "adjacent_contexts": [
            "processes:pc-sd-build-gmzrrm",
            "processes:pc-sd-operate-5cs5ee",
            "processes:pc-sd-retire-zxnc3c",
            "processes:pc-ao-activate-kusw2u",
            "processes:pc-eo-activate-xdfscw",
            "processes:pc-fa-activate-yrhcfm",
        ],
    },
    "pc-sd-retire-zxnc3c": {
        "definition": (
            "The bounded enterprise context for **governing the sunset of a "
            "regulated strategic plan under regulatory mandate** in the **Strategy "
            "& Direction** domain: supervisor-acknowledged sunset filings, plan "
            "cessation, monitoring framework decommission, and records "
            "preservation, distinct from strategy improvement and from adjacent "
            "regulated retirements."
        ),
        "scope": {
            "includes": [
                "Supervisor-acknowledged strategic-plan sunset filings",
                "Strategic-plan cessation and monitoring framework decommission",
                "Regulated strategic-plan records preservation",
                "Stakeholder communications for the mandated sunset",
            ],
            "excludes": [
                "Strategic adaptation and improvement cycles (StrategyAndDirection x Improve)",
                "Strategic-plan activation (StrategyAndDirection x Activate)",
                "Regulated entity run-off (FinanceAndAccounting x Retire; CR-BP-75)",
                "Voluntary strategy retirement absent a regulatory mandate",
            ],
        },
        "outcomes": [
            "Supervisor-acknowledged sunset filings documented for the regulated strategic plan.",
            "The strategic plan ceases execution under the regulatory mandate.",
            "The operational monitoring framework is decommissioned.",
            "Regulated strategic-plan records are preserved per the records-retention regime.",
        ],
        "adjacent_contexts": [
            "processes:pc-sd-improve-ft9k5f",
            "processes:pc-sd-activate-ghaub8",
            "processes:pc-fa-retire-64q5p9",
        ],
    },
}

# Reciprocal entries to add to same-domain sibling PCs (CE-L0-004).
# sibling id -> ids to ensure present in its adjacent_contexts
RECIPROCALS = {}
for rid, spec in REMEDIATION.items():
    for adj in spec["adjacent_contexts"]:
        RECIPROCALS.setdefault(adj, set()).add("processes:" + rid)


def main():
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 100000  # avoid line-wrapping reformatting

    # 1. remediate the 8 records
    for rid, spec in REMEDIATION.items():
        matches = list((ROOT / "entities").glob(f"**/*{rid}.yaml"))
        assert len(matches) == 1, f"{rid}: expected 1 file, found {matches}"
        p = matches[0]
        data = yaml.load(p.read_text(encoding="utf-8"))

        # prohibited field
        if "version" in data:
            del data["version"]

        # insert canonical fields after 'name', in canonical order
        insert_at = list(data.keys()).index("name") + 1
        for key in ("definition", "scope", "outcomes", "adjacent_contexts", "processes", "status"):
            if data.get(key) is None and key in data:
                del data[key]  # drop explicit nulls so insertion order is clean
        new = {}
        for k, v in data.items():
            new[k] = v
            if k == "name":
                new["definition"] = spec["definition"]
                new["scope"] = spec["scope"]
                new["outcomes"] = spec["outcomes"]
                new["adjacent_contexts"] = spec["adjacent_contexts"]
                if not data.get("processes"):
                    # derive from process_groups (each group's processes)
                    procs = []
                    for pg in data.get("process_groups") or []:
                        for pr in pg.get("processes") or []:
                            if pr not in procs:
                                procs.append(pr)
                    new["processes"] = procs
                else:
                    new["processes"] = data["processes"]
                new["status"] = (data.get("process_context") or {}).get("status") or "candidate"
        data = new

        with p.open("w", encoding="utf-8") as fh:
            yaml.dump(data, fh)
        print(f"remediated {rid} -> {p.relative_to(ROOT)}")

    # 2. reciprocal entries in sibling PCs
    for ctx_id, to_add in RECIPROCALS.items():
        short = ctx_id.split(":")[1]
        matches = list((ROOT / "entities").glob(f"**/*{short}.yaml"))
        assert len(matches) == 1, f"{ctx_id}: expected 1 file, found {matches}"
        p = matches[0]
        data = yaml.load(p.read_text(encoding="utf-8"))
        adj = data.get("adjacent_contexts")
        changed = False
        if adj is None:
            # insert after outcomes (or after name if absent)
            anchor = "outcomes" if "outcomes" in data else "name"
            data[anchor] = data[anchor]  # touch
            new = {}
            for k, v in data.items():
                new[k] = v
                if k == anchor:
                    new["adjacent_contexts"] = sorted(to_add)
                    changed = True
            data = new
        else:
            existing = list(adj)
            for x in sorted(to_add):
                if x not in existing:
                    existing.append(x)
                    changed = True
            data["adjacent_contexts"] = existing
        if changed:
            with p.open("w", encoding="utf-8") as fh:
                yaml.dump(data, fh)
            print(f"reciprocal {ctx_id} <- {sorted(to_add)}")
        else:
            print(f"reciprocal {ctx_id}: already complete")


if __name__ == "__main__":
    main()
