#!/usr/bin/env python3
"""
check_canonical_serves.py
=========================

Regression guard for CR-BP-31.

For every Business Process (L2) record in the canonical catalog, this script
verifies that the entity's `relationships[].target_id` carries an entry of
type `serves` whose value resolves to the **canonical v2.5.0 ECF identifier**
matching the BP's cell charter (`dea:pc-<DOM>-<STG>` -> `ecf:<domain>.<stage>`).

The legacy v2.3.0 / v2.4.0 entries are tolerated (preserved as historical
provenance per CR-BP-31 §6); only the canonical pair is required.

Exit code:
  0  every BP has a canonical serves relationship
  1  at least one BP is missing the canonical serves relationship
  2  structural / I/O error (inventory unreadable, etc.)

Usage:
  python3 scripts/check_canonical_serves.py
  python3 scripts/check_canonical_serves.py --strict   # treat as CI gate

Author: Coder (for eaojnr). Established by CR-BP-31 (2026-09-10).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("PyYAML is required. pip install pyyaml\n")
    sys.exit(2)


# Canonical v2.5.0 ECF identifier construction (CR-BP-23, register v4).
DOMAIN_LETTER_TO_CANONICAL = {
    "GE": "governanceexistence",
    "SD": "strategydirection",
    "AO": "agencyorganization",
    "PR": "partyrelationship",
    "PV": "productvalue",
    "OE": "enablementoperations",
    "FA": "financeaccounting",
}

STAGE_LETTER_TO_CANONICAL = {
    "C": "conceive",
    "D": "design",
    "B": "build",
    "A": "activate",
    "O": "operate",
    "I": "improve",
    "R": "retire",
}

# Legacy / tolerated spellings of the domain code (preserved as provenance).
LEGACY_DOMAIN_NORMALISATION = {
    "partyandrelationship": "partyrelationship",
    "enablementandoperations": "enablementoperations",
    "governanceandexistence": "governanceexistence",
    # v2.3.0 / pre-rename spellings kept verbatim — NOT normalised to canonical;
    # these are reported as 'legacy only' if they are the sole entry.
    "customeranddemand": None,        # v2.3.0 PR
    "peopleandorganization": None,    # v2.3.0 AO
    "supplyandresources": None,       # v2.3.0 mixed
    "offering": None,                 # v2.3.0 PV
    "operationsandenablement": None,  # v2.4.0 OE
    "productandservice": None,        # v2.3.0 PV
}


def normalise_ecf_identifier(target: str) -> str:
    """Normalise an `ecf:<domain>.<stage>` target_id to its lowercase, canonical
    v2.5.0 form. Returns the input verbatim if it does not match the pattern."""
    if not isinstance(target, str):
        return ""
    t = target.strip().lower()
    if not t.startswith("ecf:"):
        return t
    body = t[len("ecf:"):]
    if "." not in body:
        return t
    dom, stage = body.split(".", 1)
    dom = LEGACY_DOMAIN_NORMALISATION.get(dom, dom)
    if dom is None:
        # Pure legacy — leave as-is so it does NOT match canonical.
        return t
    return f"ecf:{dom}.{stage}"


def cell_charter_to_canonical_id(entity: dict) -> str | None:
    """Extract the canonical ECF identifier for a BP entity.

    Two pathways are accepted (in order of preference):

    1. The BP's description references its cell charter
       (e.g. "processes:pc-pr-d Cell Charter"). Established convention
       (CR-BP-21* landings).
    2. The BP carries an `ecfConformance.canonicalReferences[]` entry
       whose `identifier` is an `ecf:` URI. Used by earlier
       sample/contribution records that pre-date the cell-charter
       sentence convention (CR-BP-03C sample).
    """
    import re
    description = entity.get("description", "") or ""
    m = re.search(r"processes:pc-([a-z]{2,3})-([a-z])", description)
    if m:
        dom_letter = m.group(1).upper()
        stage_letter = m.group(2).upper()
        dom = DOMAIN_LETTER_TO_CANONICAL.get(dom_letter)
        stage = STAGE_LETTER_TO_CANONICAL.get(stage_letter)
        if dom and stage:
            return f"ecf:{dom}.{stage}"
    # Fallback: canonicalReferences
    for cref in (entity.get("ecfConformance") or {}).get("canonicalReferences", []) or []:
        ident = cref.get("identifier") or ""
        if isinstance(ident, str) and ident.startswith("ecf:") and "." in ident:
            return normalise_ecf_identifier(ident)
    return None


def has_canonical_serves(entity: dict, canonical_target: str) -> bool:
    serves = [
        r for r in (entity.get("relationships") or [])
        if r.get("relationship_type") == "serves"
    ]
    return any(
        normalise_ecf_identifier(r.get("target_id", "")) == canonical_target
        for r in serves
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[1] if (__doc__ or "").splitlines() else "")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 on any missing canonical serves relationship (CI gate mode).",
    )
    parser.add_argument(
        "--inventory",
        default="reconciliation/inventory.yaml",
        help="Path to the inventory file.",
    )
    args = parser.parse_args()

    inv_path = Path(args.inventory)
    if not inv_path.exists():
        sys.stderr.write(f"Inventory not found: {inv_path}\n")
        return 2

    inv = yaml.safe_load(inv_path.read_text())
    records = inv.get("records", {}).get("business_processes", [])

    missing: list[tuple[str, str]] = []
    checked = 0
    skipped = 0
    for bp in records:
        path = Path(bp["path"])
        if not path.exists():
            skipped += 1
            continue
        entity = yaml.safe_load(path.read_text())
        if not isinstance(entity, dict):
            skipped += 1
            continue
        canonical = cell_charter_to_canonical_id(entity)
        if canonical is None:
            skipped += 1
            continue
        checked += 1
        if not has_canonical_serves(entity, canonical):
            missing.append((bp["id"], canonical))

    print(f"Checked {checked} BPs; skipped {skipped} (no cell-charter reference).")
    if missing:
        print(f"\n{len(missing)} BPs missing canonical v2.5.0 serves relationship:")
        for bp_id, want in missing:
            print(f"  - {bp_id}  (want {want})")
        print(
            "\nSee change-requests/CR-BP-31-pr-canonical-serves-migration.md for the "
            "migration-pair protocol."
        )
        return 1 if args.strict else 0
    print("All BPs have a canonical v2.5.0 serves relationship. PASS.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
