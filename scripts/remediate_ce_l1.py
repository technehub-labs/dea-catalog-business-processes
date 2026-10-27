#!/usr/bin/env python3
"""CR-BP-CE-L1 migration: land the adopted `owner` field on all 49 ProcessGroups.

Per CR-BP-CE-0 §3 (L1 profile: `owner` adopted) and §5 (provenance policy:
knowledge-dependent fields land as status: proposed candidates), this adds an
`owner` block to every ProcessGroup record, carrying the EXT-24 ownership
register's disposition (`awaiting_owner_confirmation`, GOV-003 confirms,
review due 2026-12-31) rather than an invented owner name. One-shot
migration script for the CE-L1 tranche; not a gate.
"""
import glob
import json
from pathlib import Path

from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parent.parent

OWNER_BLOCK = {
    "value": "awaiting_owner_confirmation",
    "status": "proposed",
    "provenance": {
        "type": "inference",
        "asserted_by": "dea-completeness-programme",
        "asserted_at": "2026-10-27",
        "reference": "change-requests/CR-BP-CE-L1-process-group-owner-candidates.md",
    },
    "review_due": "2026-12-31",
    "decision_right": "Process Domain Reviewer (GOV-003) confirms; Business Process Owner (GOV-002) holds the accountability once confirmed",
}


def main():
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 100000

    register = json.loads(
        (ROOT / "reconciliation" / "closure" / "ownership-register.json").read_text(
            encoding="utf-8"
        )
    )
    bp_owner_by_group = {}
    for d in register["dispositions"]:
        bp_owner_by_group[d["bp_id"]] = d

    groups = sorted(glob.glob(str(ROOT / "entities" / "**" / "processes-group-*.yaml"), recursive=True))
    assert len(groups) == 49, f"expected 49 ProcessGroups, found {len(groups)}"
    for p in groups:
        data = yaml.load(Path(p).read_text(encoding="utf-8"))
        if data.get("owner"):
            print(f"skip (already owned): {data['id']}")
            continue
        new = {}
        inserted = False
        for k, v in data.items():
            new[k] = v
            # place owner after status (canonical governance fields cluster)
            if k == "status" and not inserted:
                new["owner"] = OWNER_BLOCK
                inserted = True
        if not inserted:
            new["owner"] = OWNER_BLOCK
        with Path(p).open("w", encoding="utf-8") as fh:
            yaml.dump(new, fh)
        print(f"owner landed: {data['id']}")
    print("done")


if __name__ == "__main__":
    main()
