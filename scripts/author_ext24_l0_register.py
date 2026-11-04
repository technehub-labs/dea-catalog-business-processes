"""CR-BP-94-EXT-24 execution (2026-11-04, ahead of the 2026-12-31 window):
author the L0 governance + metrics register on all 49 ProcessContext records.

This is the delivery of the two standing items that CR-BP-224 re-pointed to
EXT-24 ("closure under CR-BP-94-EXT-24"): (a) L0 role assignment and
(b) the L0 metrics register (KPI/KRI/KCI). Both are DERIVED, not invented:

- roles: the domain Process Owner role, extracted from the domain's own
  L1 ProcessGroup records (GOV-002-confirmed by CR-BP-GS-1 with manual
  provenance). L0 inherits the domain-level owner because the GOV-002
  decision assigns one owner role per domain covering the domain's
  contexts.
- metrics KPI: lifecycle-stage effectiveness standard, grounded in the
  cell's own first `outcomes` entry (the cell's strongest performance
  statement, cited in the name).
- metrics KRI: adjacent-context leakage risk, grounded in the cell's own
  first `scope.excludes` entry (cited in the name).
- metrics KCI: charter/regulatory evidence currency, grounded in the
  cell's domain x stage identity.

Targets are directional stage standards (no invented numbers); every
entry carries `review_due: 2026-12-31` provenance — owner confirmation
at the EXT-24 review is the next governance act, already scheduled via
the GOV-002 review_due mechanics.

Raw-text surgery: two fresh top-level blocks (`governance:`, `metrics:`)
are APPENDED to each PC file at EOF. PCs carry neither block today
(verified across all 49), so no key duplication is possible and the
diff is additions-only. Idempotent: a file already carrying the
execution marker is skipped.

Schema: schemas/entities/process-context.schema.json is extended in the
same PR to accept the two blocks (additionalProperties: false).

Usage:
  python3 scripts/author_ext24_l0_register.py [--dry-run]

Authoritative reference: CR-BP-94-EXT-24 (Accepted, landed) executed
ahead of its 2026-12-31 window by user directive 2026-11-04.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTITIES = ROOT / "entities" / "v1-alpha"

MARKER = "CR-BP-94-EXT-24 L0 register execution (2026-11-04)"

STAGE_STANDARDS = {
    "Conceive": ("Mandate and framing ratified before the Build gate",
                 "per conception cycle"),
    "Design": ("Design ratified; boundaries testable before the Build gate",
               "per design cycle"),
    "Build": ("Capability operational at the Activate gate", "per build cycle"),
    "Activate": ("Authorization evidence complete; live state recorded",
                 "per activation"),
    "Operate": ("Continuous operation within charter scope",
                "continuous; quarterly review"),
    "Improve": ("Improvement cycle executed; findings dispositioned",
                "per improvement cycle"),
    "Retire": ("Orderly wind-down; records preserved per retention policy",
               "per retirement"),
}

DOMAIN_NAMES = {
    "PartyAndRelationship": ("pr", "Party & Relationship"),
    "GovernanceAndExistence": ("ge", "Governance & Existence"),
    "ProductAndValue": ("pv", "Product & Value"),
    "AgencyAndOrganization": ("ao", "Agency & Organization"),
    "StrategyAndDirection": ("sd", "Strategy & Direction"),
    "FinanceAndAccounting": ("fa", "Finance & Accounting"),
    "EnablementAndOperations": ("eo", "Enablement & Operations"),
}


def _yq(text: str) -> str:
    """Single-quote-escape a string for safe YAML embedding."""
    return str(text).replace("'", "''")


def _condense(text: str, limit: int = 90) -> str:
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:.") + " …"


def _domain_owner(domain_enum: str, code: str) -> str:
    """Extract the GOV-002-confirmed owner from the domain's L1 groups."""
    owners = set()
    for p in ENTITIES.rglob("processes-group-*.yaml"):
        parts = p.parts
        if any(s in parts for s in ("research", "candidates", "retired")):
            continue
        d = yaml.safe_load(p.read_text()) or {}
        pc = d.get("process_context")
        pc_id = pc.get("id") if isinstance(pc, dict) else pc
        if isinstance(pc_id, str) and f"pc-{code}-" in pc_id:
            owner = d.get("owner")
            if isinstance(owner, dict) and owner.get("value"):
                owners.add(str(owner["value"]))
    if not owners:
        raise SystemExit(f"ERROR: no GOV-002 owner found for domain {domain_enum}")
    return sorted(owners)[0]


def author_file(path: Path, dry_run: bool) -> bool:
    text = path.read_text()
    if MARKER in text:
        return False
    d = yaml.safe_load(text) or {}
    domain_enum = d["domain"]
    stage = d["lifecycle_stage"]
    code, domain_full = DOMAIN_NAMES[domain_enum]
    owner = _domain_owner(domain_enum, code)

    outcomes = d.get("outcomes") or []
    excludes = (d.get("scope") or {}).get("excludes") or []
    kpi_ground = _condense(outcomes[0]) if outcomes else "charter outcomes"
    kri_ground = _condense(excludes[0]) if excludes else "adjacent contexts"
    kpi_target, kpi_freq = STAGE_STANDARDS[stage]
    owner_escaped = _yq(owner)
    stage_escaped = _yq(stage)
    kpi_ground_escaped = _yq(kpi_ground)
    kpi_target_escaped = _yq(kpi_target)
    kpi_freq_escaped = _yq(kpi_freq)
    kri_ground_escaped = _yq(kri_ground)

    block = f"""

# {MARKER}: L0 governance + metrics register (derived; see
# scripts/author_ext24_l0_register.py and
# reconciliation/closure/ext24-l0-register-execution.json).
governance:
  roles:
  - '{owner_escaped} (GOV-002 role-based; domain-level owner for the {domain_full} contexts)'
  provenance:
    source: change-requests/CR-BP-GS-1-governance-sweep.md
    execution: CR-BP-94-EXT-24 (2026-11-04; ahead of the 2026-12-31 window)
    review_due: '2026-12-31'
metrics:
  performance:
  - name: '{stage_escaped} effectiveness — {kpi_ground_escaped}'
    target: '{kpi_target_escaped}'
    frequency: '{kpi_freq_escaped}'
  risk:
  - name: 'Adjacent-context leakage — {code}-{stage} exclusions: {kri_ground_escaped}'
    target: 'none observed at governance review'
    frequency: 'quarterly'
  compliance:
  - name: 'Charter and regulatory evidence currency — {domain_full} x {stage}'
    target: 'evidence refreshed per governance cadence; owner confirmation due 2026-12-31'
    frequency: 'semi-annual'
"""
    if not dry_run:
        # Normalize the tail: some PCs end with a whitespace-only line;
        # strip ALL trailing whitespace so the appended blocks start at
        # column 0 immediately after a clean newline.
        path.write_text(text.rstrip() + "\n" + block)
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    pcs = sorted(
        p for p in ENTITIES.rglob("processes-pc-*.yaml")
        if p.parent.name != "v1-alpha" or True  # PCs live at cell roots
    )
    pcs = [p for p in pcs if not any(s in p.parts for s in ("research", "candidates", "retired"))]
    authored = 0
    for p in pcs:
        if author_file(p, args.dry_run):
            authored += 1
    mode = "DRY-RUN " if args.dry_run else ""
    print(f"{mode}author_ext24_l0_register: pcs={len(pcs)} authored={authored}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
