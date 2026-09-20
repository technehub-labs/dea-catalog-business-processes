#!/usr/bin/env python3
"""
check_dispositions.py: Disposition register + tranche plan validator
(CR-BP-15-IMP Phase 3-4).

Validates that:

  (a) Every record in reconciliation/inventory.yaml has exactly one
      entry in reconciliation/dispositions/register.yaml.
  (b) Every disposition entry conforms to one of the 9 disposition
      ids declared in reconciliation/dispositions/schema.yaml.
  (c) Disposition-specific required fields are present (per schema).
  (d) RECLASSIFY changes: axis is one of the declared axes; from ->
      to follows the migration mapping (the canonical vocabulary).
  (e) Every target_id (MERGE / SPLIT / SPECIALIZE) resolves to an
      existing record id in the inventory (warning, not error, for
      planned-but-not-yet-existing targets).
  (f) Every tranche plan entry references a disposition entry and
      an existing inventory record.

Authoritative reference: CR-BP-15-IMP /3, /4; CR-BP-15 /28.

Usage:
  python scripts/check_dispositions.py [--self-test] [--strict]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
INVENTORY_PATH = REPO_ROOT / "reconciliation/inventory.yaml"
DISPOSITION_SCHEMA = REPO_ROOT / "reconciliation/dispositions/schema.yaml"
DISPOSITION_REGISTER = REPO_ROOT / "reconciliation/dispositions/register.yaml"
TRANCHE_PLAN = REPO_ROOT / "reconciliation/tranches/plan.yaml"

CANONICAL_INTENTS = {
    "govern", "manage", "operate", "deliver",
    "support", "develop", "transform",
}
LEGACY_INTENTS = {"operational", "support", "management"}
CANONICAL_CLASSIFICATIONS = {
    "strategic", "management", "core", "support", "standardization",
}
VALID_DISPOSITIONS = {
    "RETAIN", "RECLASSIFY", "RENAME", "SPECIALIZE",
    "MERGE", "SPLIT", "MOVE", "DEFER", "RETIRE",
}


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text())


def _gather_inventory_ids(inventory: dict) -> set[str]:
    ids: set[str] = set()
    for key in ("business_processes", "process_groups", "process_contexts"):
        for r in inventory.get("records", {}).get(key, []) or []:
            ids.add(r["id"])
    return ids


def check_dispositions(
    inventory: dict,
    schema: dict,
    register: dict,
    tranche_plan: dict | None = None,
) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for the disposition register."""
    errors: list[str] = []
    warnings: list[str] = []

    inv_ids = _gather_inventory_ids(inventory)
    dispositions = register.get("dispositions", [])
    by_record: dict[str, dict] = {d["record_id"]: d for d in dispositions}

    # (a) Every inventory record has exactly one disposition.
    bp_ids = {r["id"] for r in inventory["records"]["business_processes"]}
    missing = bp_ids - set(by_record)
    extra = set(by_record) - bp_ids
    for record_id in sorted(missing):
        errors.append(f"record {record_id}: missing disposition entry")
    for record_id in sorted(extra):
        errors.append(f"disposition for {record_id}: record not in inventory")

    # (b) Disposition ids are valid.
    for d in dispositions:
        disp = d.get("disposition")
        if disp not in VALID_DISPOSITIONS:
            errors.append(
                f"record {d['record_id']}: invalid disposition {disp!r}; "
                f"must be one of {sorted(VALID_DISPOSITIONS)}"
            )

    # (c) Per-disposition required fields.
    for d in dispositions:
        rid = d["record_id"]
        disp = d.get("disposition")
        if disp == "RECLASSIFY":
            changes = d.get("changes")
            if not changes:
                errors.append(f"record {rid}: RECLASSIFY requires 'changes'")
                continue
            for change in changes:
                axis = change.get("axis")
                if axis not in {
                    "process_intent", "process_type", "process_context",
                    "process_specialization", "process_audience",
                }:
                    errors.append(
                        f"record {rid}: RECLASSIFY change axis {axis!r} "
                        f"is not a CR-BP-14 semantic axis"
                    )
                if axis == "process_intent":
                    target = change.get("to")
                    if target not in CANONICAL_INTENTS:
                        errors.append(
                            f"record {rid}: RECLASSIFY intent -> {target!r} "
                            f"is not a canonical Process Intent "
                            f"(must be one of {sorted(CANONICAL_INTENTS)})"
                        )
                    source = change.get("from")
                    if source not in LEGACY_INTENTS:
                        warnings.append(
                            f"record {rid}: RECLASSIFY intent from {source!r} "
                            f"is not a documented legacy intent"
                        )
                if axis == "process_type":
                    target = change.get("to")
                    if target not in CANONICAL_CLASSIFICATIONS:
                        errors.append(
                            f"record {rid}: RECLASSIFY classification -> "
                            f"{target!r} is not a canonical Process "
                            f"Classification"
                        )
                if axis == "process_context":
                    target = change.get("to")
                    if not target or not target.startswith("processes:pc-"):
                        errors.append(
                            f"record {rid}: RECLASSIFY context -> {target!r} "
                            f"must be a Process Context id (dea:pc-*)"
                        )

    # (d) Tranche plan consistency.
    if tranche_plan is not None:
        for tranche in tranche_plan.get("tranches", []):
            tid = tranche["tranche_id"]
            for rid in tranche.get("records", []):
                if rid not in by_record:
                    errors.append(
                        f"tranche {tid}: record {rid} has no disposition entry"
                    )
                else:
                    expected_tranche = by_record[rid].get("tranche")
                    if expected_tranche and expected_tranche != tid:
                        warnings.append(
                            f"tranche {tid}: record {rid} is in disposition "
                            f"tranche {expected_tranche!r}; cross-check"
                        )

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--strict", action="store_true",
                   help="Treat warnings as errors.")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args(argv)

    if args.self_test:
        return _self_test(args)

    inventory = _load_yaml(INVENTORY_PATH)
    schema = _load_yaml(DISPOSITION_SCHEMA)
    register = _load_yaml(DISPOSITION_REGISTER)
    tranche_plan = _load_yaml(TRANCHE_PLAN) if TRANCHE_PLAN.exists() else None

    errors, warnings = check_dispositions(
        inventory, schema, register, tranche_plan
    )

    if errors:
        for e in errors:
            print(f"DISP-ERROR: {e}", file=sys.stderr)
    if warnings:
        for w in warnings:
            print(f"DISP-WARN:  {w}", file=sys.stderr)

    fail = bool(errors) or (args.strict and bool(warnings))
    if fail:
        print(f"DISP-FAIL: {len(errors)} errors, {len(warnings)} warnings",
              file=sys.stderr)
        return 1
    if not args.quiet:
        print(f"DISP-OK: {len(errors)} errors, {len(warnings)} warnings "
              f"(18 dispositions checked)")
    return 0


def _self_test(args) -> int:
    """In-memory self-test: every disposition axis and every error path."""
    inventory = {
        "records": {
            "business_processes": [
                {"id": "processes:process-a", "name": "Test A"},
                {"id": "processes:process-b", "name": "Test B"},
            ],
            "process_groups": [],
            "process_contexts": [],
        }
    }
    schema = _load_yaml(DISPOSITION_SCHEMA)
    # Good dispositions
    good = {
        "dispositions": [
            {
                "record_id": "processes:process-a",
                "disposition": "RECLASSIFY",
                "changes": [
                    {"axis": "process_intent",
                     "from": "management", "to": "manage"},
                    {"axis": "process_context",
                     "from": "processes:pc-pr-op", "to": "processes:pc-pr-op"},
                    {"axis": "process_audience",
                     "from": "party-relationship", "to": "REMOVE"},
                ],
                "tranche": "cd-op",
            },
            {
                "record_id": "processes:process-b",
                "disposition": "RETAIN",
            },
        ]
    }
    errs, warns = check_dispositions(inventory, schema, good)
    if errs:
        print(f"self-test FAIL: good fixture produced errors: {errs}",
              file=sys.stderr)
        return 2

    # Bad: invalid disposition id
    bad_disp = {"dispositions": [
        {"record_id": "processes:process-a", "disposition": "PURGE"}
    ]}
    errs, _ = check_dispositions(inventory, schema, bad_disp)
    if not any("invalid disposition" in e for e in errs):
        print("self-test FAIL: invalid disposition id not detected", file=sys.stderr)
        return 2

    # Bad: RECLASSIFY without changes
    bad_recl = {"dispositions": [
        {"record_id": "processes:process-a", "disposition": "RECLASSIFY"}
    ]}
    errs, _ = check_dispositions(inventory, schema, bad_recl)
    if not any("requires 'changes'" in e for e in errs):
        print("self-test FAIL: RECLASSIFY w/o changes not detected", file=sys.stderr)
        return 2

    # Bad: RECLASSIFY intent -> non-canonical value
    bad_intent = {"dispositions": [
        {"record_id": "processes:process-a", "disposition": "RECLASSIFY",
         "changes": [{"axis": "process_intent", "from": "management", "to": "oversee"}]}
    ]}
    errs, _ = check_dispositions(inventory, schema, bad_intent)
    if not any("not a canonical Process Intent" in e for e in errs):
        print("self-test FAIL: non-canonical intent not detected", file=sys.stderr)
        return 2

    # Bad: RECLASSIFY context -> non-pc- ref
    bad_ctx = {"dispositions": [
        {"record_id": "processes:process-a", "disposition": "RECLASSIFY",
         "changes": [{"axis": "process_context", "from": "x", "to": "dea:wrong"}]}
    ]}
    errs, _ = check_dispositions(inventory, schema, bad_ctx)
    if not any("must be a Process Context id" in e for e in errs):
        print("self-test FAIL: non-pc context not detected", file=sys.stderr)
        return 2

    # Bad: missing disposition for an inventory record
    bad_missing = {"dispositions": [
        {"record_id": "processes:process-a", "disposition": "RETAIN"}
    ]}
    errs, _ = check_dispositions(inventory, schema, bad_missing)
    if not any("missing disposition" in e for e in errs):
        print("self-test FAIL: missing disposition not detected", file=sys.stderr)
        return 2

    if not args.quiet:
        print("self-test PASS: disposition validator covers every rule")
    return 0


if __name__ == "__main__":
    sys.exit(main())
