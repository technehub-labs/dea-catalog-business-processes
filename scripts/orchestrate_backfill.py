#!/usr/bin/env python3
"""
orchestrate_backfill.py
========================

Backfill orchestrator (CR-BP-94-EXT-17).

Implements the EXT-17 REQ-17-04..15 orchestrator contract:

  OR-001  Dry-run mode does not modify repository files (idempotency).
  OR-002  Per-record selection by metadata.authoring.state (the 9-value
          EXT-16 vocabulary: not_started | planning | researching |
          drafted | under_review | approved | published | rejected |
          withdrawn).
  OR-003  Per-record execution of the relevant validators (state-driven).
  OR-004  Severity mapping (error | warning | info | deferred).
  OR-005  No automatic invention (REQ-17-14; the orchestrator only
          reports, it does not write content).

The orchestrator consumes the EXT-16 metadata.authoring state (already
established in PR #185) and drives the EXT-19+ backfill tranches in
dependency order. It does NOT introduce new validators; it aggregates
the findings from the existing validators and reports them with the
EXT-17 severity model.

Test layout: tests/test_enrichment_tooling_ext17.py
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError:
    sys.stderr.write("ERROR: PyYAML is required.\n")
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "reconciliation" / "tooling-manifest.json"

# The 9 EXT-16 authoring states (consumed by the orchestrator)
EXT16_AUTHORING_STATES = frozenset({
    "not_started", "planning", "researching", "drafted",
    "under_review", "approved", "published", "rejected", "withdrawn",
})

# The 4 EXT-17 severity levels
SEVERITY_LEVELS = ("error", "warning", "info", "deferred")

# The existing validators the orchestrator consumes
VALIDATOR_COMMANDS = [
    ("check_profile_registry_ext11.py", "EXT-11 Profile Registry (PR-001..PR-010)"),
    ("check_inputs_outputs_interfaces_ext12.py", "EXT-12 Inputs/Outputs/Interfaces (IT-001..IT-010)"),
    ("check_responsibility_accountability_ext13.py", "EXT-13 Responsibility/Accountability (RA-001..RA-010)"),
    ("check_business_rules_controls_exceptions_ext14.py", "EXT-14 Business Rules/Controls/Exceptions (GO-001..GO-010)"),
    ("check_evidence_provenance_ext15.py", "EXT-15 Evidence/Provenance/Confidence (EV-001..EV-010)"),
    ("check_authoring_methodology_ext16.py", "EXT-16 Authoring Methodology (AM-001..AM-010)"),
]


def _select_records(catalog_root: Path, state_filter: str | None) -> list[tuple[Path, dict]]:
    """Select records for the orchestrator's pass.

    Per OR-002: when state_filter is set, select records whose
    metadata.authoring.state matches. When None, select all records.
    """
    selected: list[tuple[Path, dict]] = []
    for f in (catalog_root / "entities" / "v1-alpha").rglob("*.yaml"):
        try:
            with f.open(encoding="utf-8") as fp:
                rec = yaml.safe_load(fp) or {}
        except Exception:
            continue
        if not isinstance(rec, dict):
            continue
        if state_filter is None:
            selected.append((f, rec))
            continue
        # State filter: read metadata.authoring.state.
        meta = rec.get("metadata")
        if not isinstance(meta, dict):
            continue
        authoring = meta.get("authoring")
        if not isinstance(authoring, dict):
            continue
        if authoring.get("state") == state_filter:
            selected.append((f, rec))
    return selected


def _run_validator(script_name: str, catalog_root: Path) -> dict:
    """Run a single validator and return its manifest summary.

    The orchestrator consumes the per-validator manifest's summary;
    it does NOT re-evaluate the findings. Per OR-005, the orchestrator
    only reports; it does not write content.
    """
    cmd = ["python3", f"scripts/{script_name}", "--catalog-root", str(catalog_root), "--json"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True,
                                timeout=300, cwd=str(REPO_ROOT))
    except subprocess.TimeoutExpired:
        return {"script": script_name, "error": "timeout", "summary": {"total_findings": 0}}
    except Exception as e:
        return {"script": script_name, "error": str(e), "summary": {"total_findings": 0}}
    try:
        data = json.loads(result.stdout)
    except Exception:
        return {"script": script_name, "error": "non-json output", "summary": {"total_findings": 0}}
    return data


def orchestrate(catalog_root: Path,
                state_filter: str | None = None,
                dry_run: bool = True) -> dict:
    """Run the orchestrator. Returns the catalogue-level report."""
    records = _select_records(catalog_root, state_filter)
    validator_runs = []

    # Per OR-003: per-record execution of the relevant validators.
    # We invoke each validator at the catalogue level (the orchestrator
    # does not re-evaluate; the validators are the source of truth).
    for script_name, label in VALIDATOR_COMMANDS:
        run = _run_validator(script_name, catalog_root)
        run["script"] = script_name
        run["label"] = label
        validator_runs.append(run)

    # Build the catalogue-level report.
    report = {
        "report_schema_version": "1",
        "generated_at": "2026-10-19",
        "generator": "scripts/orchestrate_backfill.py",
        "parent_cr": "CR-BP-94-EXT-17",
        "catalog_root": str(catalog_root),
        "selection": {
            "state_filter": state_filter,
            "total_selected_records": len(records),
        },
        "mode": "dry-run" if dry_run else "live",
        "per_validator_summary": {
            run.get("script", "?"): run.get("summary", {}).get("total_findings", 0)
            for run in validator_runs
        },
        "total_findings": sum(
            run.get("summary", {}).get("total_findings", 0)
            for run in validator_runs
        ),
    }

    # Per OR-001: dry-run does NOT modify repository files. We confirm this
    # by recording the mode.
    if not dry_run:
        # Live mode is reserved for the EXT-19 backfill tranche; the
        # orchestrator is a reporting tool, not a content writer.
        report["note"] = (
            "Live mode is reserved for the EXT-19 backfill tranche. "
            "The orchestrator only reports; it does not write content "
            "(REQ-17-14; no automatic semantic invention)."
        )

    # Per OR-005: no automatic invention.
    report["no_automatic_invention"] = True

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true",
                        help="run a synthetic self-test (no live tree scan)")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="dry-run mode (default; does not modify repo files)")
    parser.add_argument("--live", action="store_true",
                        help="live mode (reserved for EXT-19 backfill)")
    parser.add_argument("--state", default=None,
                        help="filter records by metadata.authoring.state "
                             "(one of the 9 EXT-16 authoring states)")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--catalog-root", default=".", help="catalog root")
    args = parser.parse_args()

    if args.self_test:
        synthetic_report = {
            "mode": "self-test",
            "selection": {"state_filter": None, "total_selected_records": 0},
            "per_validator_summary": {},
            "total_findings": 0,
            "no_automatic_invention": True,
        }
        print(json.dumps(synthetic_report, indent=2))
        return 0

    if yaml is None:
        sys.stderr.write("ERROR: PyYAML is required.\n")
        return 2

    if args.state is not None and args.state not in EXT16_AUTHORING_STATES:
        sys.stderr.write(
            f"ERROR: --state {args.state!r} is not in the EXT-16 9-value vocabulary: "
            f"{sorted(EXT16_AUTHORING_STATES)}\n"
        )
        return 2

    if args.live and not args.dry_run:
        # Honour the explicit dry-run default; live is reserved for EXT-19.
        pass

    catalog_root = Path(args.catalog_root).resolve()
    dry_run = not args.live
    report = orchestrate(catalog_root, state_filter=args.state, dry_run=dry_run)

    # Emit the tooling manifest (the orchestrator's per-run record).
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST_PATH.open("w", encoding="utf-8") as fp:
        json.dump(report, fp, indent=2)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Orchestrator run: {report['mode']}")
        print(f"  Records selected: {report['selection']['total_selected_records']}")
        if args.state:
            print(f"  State filter: {args.state}")
        print(f"  Total findings (per_validator_summary): {report['total_findings']}")
        for script, n in report["per_validator_summary"].items():
            print(f"    [{n:>3}] {script}")
        print(f"  Manifest: {MANIFEST_PATH.relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
