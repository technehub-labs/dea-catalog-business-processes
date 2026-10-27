#!/usr/bin/env python3
"""CR-BP-CE-L2 migration: land the adopted fields on all 145 L2 Process records.

Per CR-BP-CE-0 §3 (L2 profile) and §5 (provenance policy):

- `process_classification` is DERIVABLE: the legacy `process_type` field
  carries the same controlled vocabulary (the schema declares it the
  backward-compatible alias). The canonical block lands with
  `status: active`, `type: migration`.
- `owner` is KNOWLEDGE-DEPENDENT: lands as a `status: proposed` candidate
  carrying the EXT-24 ownership-register disposition
  (`awaiting_owner_confirmation`, GOV-002 confirms, review due 2026-12-31).
  No owner name is invented.

`actors` and `stakeholders` are deliberately NOT populated: no
evidence-bound source exists in the record tree (L3 Activities carry no
responsibility fields; the ownership register carries no actor data).
Inventing values would violate §5; they remain advisory findings awaiting
the human governance sweep. One-shot migration; not a gate.
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
        "reference": "change-requests/CR-BP-CE-L2-process-adopted-fields.md",
    },
    "review_due": "2026-12-31",
    "decision_right": "Business Process Owner (GOV-002) confirms",
}


def main():
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 100000

    register = json.loads(
        (ROOT / "reconciliation" / "closure" / "ownership-register.json")
        .read_text(encoding="utf-8")
    )
    by_bp = {d["bp_id"]: d for d in register["dispositions"]}

    procs = sorted(
        glob.glob(str(ROOT / "entities" / "**" / "processes-process-*.yaml"), recursive=True)
    )
    # exclude L3/L4 files that share the processes- prefix pattern? L3 are
    # processes-activity-*, L4 processes-task-*, so this glob is L2-only.
    assert len(procs) == 145, f"expected 145 L2 Process records, found {len(procs)}"

    landed_class = landed_owner = 0
    for p in procs:
        data = yaml.load(Path(p).read_text(encoding="utf-8"))
        rid = data["id"]
        assert rid in by_bp, f"{rid} missing from the ownership register"

        new = {}
        inserted = False
        for k, v in data.items():
            new[k] = v
            if k == "process_type" and not inserted:
                # canonical classification block lands right after its
                # legacy alias
                if not data.get("process_classification"):
                    new["process_classification"] = {
                        "type": data["process_type"],
                        "provenance": {
                            "type": "migration",
                            "asserted_by": "dea-completeness-programme",
                            "asserted_at": "2026-10-27",
                            "reference": "change-requests/CR-BP-CE-L2-process-adopted-fields.md",
                        },
                        "status": "active",
                    }
                    landed_class += 1
                if not data.get("owner"):
                    new["owner"] = OWNER_BLOCK
                    landed_owner += 1
                inserted = True
        assert inserted, f"{rid}: no process_type anchor"
        with Path(p).open("w", encoding="utf-8") as fh:
            yaml.dump(new, fh)

    print(f"classification landed: {landed_class}; owner landed: {landed_owner}")


if __name__ == "__main__":
    main()
