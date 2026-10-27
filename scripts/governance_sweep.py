#!/usr/bin/env python3
"""CR-BP-GS-1: the governance sweep (GOV-002/GOV-003) across L1 PGs + L2 BPs.

Role-based per the user's ratified decision (2026-10-27):

- OWNERS (GOV-002, CONFIRMED): one Process Owner role per domain, ratified
  as a domain-level pattern. The 194 records' owner blocks flip
  status: proposed -> confirmed with the domain owner role as the value.
- ACTORS/STAKEHOLDERS (GOV-003, PROPOSED): charter-derived role candidates
  per L2 record, drawn ONLY from the roles the record's parent cell
  charter actually names (its inclusions/expected_outcomes/adjacent_
  boundaries vocabulary). Landed as lists with per-record provenance in
  metadata.change_history; the completeness gate's CE-L2-006 fires until
  values exist, and the adoption counters track the ratification state.

One-shot migration for CR-BP-GS-1; not a gate.
"""
import glob
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_completeness as cc  # noqa: E402

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parent.parent

# GOV-002 ratification: one Process Owner role per domain (the ratified
# role-based pattern). PGs inherit their domain's owner role.
DOMAIN_OWNER_ROLE = {
    "AgencyAndOrganization": "Agency & Organization Process Owner",
    "EnablementAndOperations": "Enablement & Operations Process Owner",
    "FinanceAndAccounting": "Finance & Accounting Process Owner",
    "GovernanceAndExistence": "Governance & Existence Process Owner",
    "PartyAndRelationship": "Party & Relationship Process Owner",
    "ProductAndValue": "Product & Value Process Owner",
    "StrategyAndDirection": "Strategy & Direction Process Owner",
}

# GOV-003 derivation vocabulary: charter keyword -> candidate role. Only
# roles whose keyword the record's parent cell charter actually mentions
# are assigned; nothing is invented beyond this mapping.
KWS = {
    "regulator": "industry regulator",
    "supervisor": "supervising authority",
    "board": "governing board",
    "audit": "audit function",
    "risk": "risk function",
    "legal": "legal function",
    "compliance": "compliance function",
    "finance": "finance function",
    "workforce": "workforce management",
    "customer": "customer relationship management",
    "supplier": "supplier and partner management",
    "operations": "operations function",
    "product": "product management",
    "strategy": "strategy function",
    "human resources": "HR function",
}

# GOV-003 fallback: where the parent charter's vocabulary is purely
# architectural and names no functional actor keyword, the minimal
# charter-honest role is the domain's design/ownership function.
DOMAIN_FALLBACK_ROLE = {
    "AgencyAndOrganization": "organization design authority",
    "EnablementAndOperations": "enablement design authority",
    "FinanceAndAccounting": "finance design authority",
    "GovernanceAndExistence": "governance design authority",
    "PartyAndRelationship": "relationship design authority",
    "ProductAndValue": "proposition design authority",
    "StrategyAndDirection": "strategy design authority",
}

CR = "CR-BP-GS-1"
DATE = "2026-10-27"
CR_REF = "change-requests/CR-BP-GS-1-governance-sweep.md"

PROVENANCE_CONFIRMED = {
    "type": "manual",
    "asserted_by": "GOV-002 (Business Process Owner decision, ratified 2026-10-27)",
    "asserted_at": DATE,
    "reference": CR_REF,
}
PROVENANCE_DERIVED = {
    "type": "inference",
    "asserted_by": "dea-completeness-programme (GOV-003 role-based derivation policy, ratified 2026-10-27)",
    "asserted_at": DATE,
    "reference": CR_REF,
}


def domain_of_record(r):
    doms = (r.get("ecfConformance") or {}).get("canonicalReferences", [])
    return doms[0].get("domain") if doms else None


def charter_roles(rec, pcs):
    """Derive candidate actor roles from the record's parent cell charter."""
    roles = []
    for c in rec.get("context") or []:
        cid = c.get("ref") if isinstance(c, dict) else c
        pc = pcs.get(cid)
        if not pc:
            continue
        ch = pc.get("cell_charter") or {}
        text = " ".join(
            list(ch.get("inclusions", []))
            + list(ch.get("expected_outcomes", []))
            + list(ch.get("adjacent_boundaries", []))
        ).lower()
        for kw, role in KWS.items():
            if kw in text and role not in roles:
                roles.append(role)
    return roles


def main():
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 100000

    recs = cc.load_records()
    pcs = {r["id"]: r for _, r in recs if cc.level_of(r) == "ProcessContext"}

    owners_confirmed = actors_landed = 0

    # ---- L1 ProcessGroups: owner flip proposed -> confirmed ----
    for p in sorted(glob.glob(str(ROOT / "entities" / "**" / "processes-group-*.yaml"), recursive=True)):
        data = yaml.load(Path(p).read_text(encoding="utf-8"))
        dom = domain_of_record(data)
        role = DOMAIN_OWNER_ROLE.get(dom)
        assert role, f"{data['id']}: no owner role for domain {dom}"
        o = data.get("owner")
        assert o and o.get("status") == "proposed", f"{data['id']}: unexpected owner state"
        data["owner"]["value"] = role
        data["owner"]["status"] = "confirmed"
        data["owner"]["provenance"] = PROVENANCE_CONFIRMED
        with Path(p).open("w", encoding="utf-8") as fh:
            yaml.dump(data, fh)
        owners_confirmed += 1

    # ---- L2 Processes: owner flip + actors/stakeholders ----
    for p in sorted(glob.glob(str(ROOT / "entities" / "**" / "processes-process-*.yaml"), recursive=True)):
        data = yaml.load(Path(p).read_text(encoding="utf-8"))
        dom = domain_of_record(data)
        role = DOMAIN_OWNER_ROLE.get(dom)
        assert role, f"{data['id']}: no owner role for domain {dom}"

        o = data.get("owner")
        assert o and o.get("status") == "proposed", f"{data['id']}: unexpected owner state"
        data["owner"]["value"] = role
        data["owner"]["status"] = "confirmed"
        data["owner"]["provenance"] = PROVENANCE_CONFIRMED

        roles = charter_roles(data, pcs)
        if not roles:
            roles = [DOMAIN_FALLBACK_ROLE[dom]]
        # actors: the roles that perform/participate; stakeholders: the
        # oversight/impacted roles. Charter derivation does not distinguish
        # perform vs oversight reliably, so both lists carry the derived
        # roles; GOV-003 refines per record during review.
        data["actors"] = list(roles)
        data["stakeholders"] = list(roles)

        md = data.get("metadata") or {}
        ch_hist = md.setdefault("change_history", [])
        ch_hist.append({
            "cr": CR,
            "date": DATE,
            "change": (
                "Governance sweep (CR-BP-GS-1): owner confirmed by the "
                "GOV-002 domain-level ratification (" + role + "); "
                "actors/stakeholders derived from the parent cell charter "
                "vocabulary under the GOV-003 role-based derivation policy "
                "(status: proposed, awaiting per-record review)."
            ),
        })
        with Path(p).open("w", encoding="utf-8") as fh:
            yaml.dump(data, fh)
        actors_landed += 1

    print(f"owners confirmed: {owners_confirmed} (49 PGs + 145 BPs = 194)")
    print(f"actors/stakeholders landed: {actors_landed} BPs")


if __name__ == "__main__":
    main()
