#!/usr/bin/env python3
"""Conformance Result Aggregator (CR-BP-16 S18).

CR-BP-16 S18 mandates that every change receive a single
CONFORMANCE RESULT verdict, one of:

  CONFORMANT                 All mandatory gates pass.
  CONFORMANT-WITH-WARNINGS   All blocking gates pass, advisory findings
                             remain.
  NON-CONFORMANT             At least one mandatory gate fails.

This script runs every blocking + advisory gate in the pipeline
and produces a unified verdict. It is the canonical pre-merge
verdict source: the `Conformance Result` CI step in
`.github/workflows/ci.yml` calls this script and writes the
verdict to `reconciliation/conformance_result.yaml`.

Usage::

    python scripts/conformance_result.py [--strict] [--catalog-root .]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parent


class GateResult(NamedTuple):
    name: str
    blocking: bool
    returncode: int
    verdict_line: str
    raw_stdout: str

    @property
    def passed(self) -> bool:
        return self.returncode == 0


# Pipeline order matches docs/conformance-pipeline.md.
# Each entry: (gate label, blocking?, script invocation)
GATES: list[tuple[str, bool, list[str]]] = [
    ("[1] Schema (validate-process-entries)",
     True, ["python", "scripts/regenerate_catalog.py", "--check",
            "--schema", "catalog-index-schema/catalog-index-schema.json"]),
    ("[1] Schema (catalog-index)",
     True, ["python", "scripts/check_catalog_index.py", "--strict",
            "--schema", "catalog-index-schema/catalog-index-schema.json"]),
    ("[2] Structure",
     False, ["python", "scripts/check_struct.py"]),  # advisory
    ("[3] References (BP-SEM + legacy)",
     True, ["python", "scripts/check_legacy_migration.py"]),
    ("[3] References (context-resolution)",
     True, ["python", "scripts/check_process_context.py"]),
    ("[4] Semantics (BP-SEM-001..014)",
     True, ["python", "scripts/check_process_semantics.py", "--strict"]),
    ("[4] Semantics (BP-SPEC-01-001..007)",
     True, ["python", "scripts/check_process_specialization.py"]),
    ("[5] Hierarchy (BP-AR-001..007)",
     True, ["python", "scripts/check_architectural_regression.py", "--strict"]),
    ("[6] Specialization Graph (cycle + edge)",
     True, ["python", "scripts/check_process_specialization.py"]),
    ("[7] MECE (Process Group)",
     True, ["python", "scripts/check_process_group.py"]),
    ("[8] Provenance (ECF conformance)",
     True, ["python", "scripts/check_ecf_conformance.py"]),
    ("[9] CR Validation (CR-META-001..006)",
     False, ["python", "scripts/check_cr_metadata.py"]),  # advisory for now
    ("[10] Conformance Result (Levels 1-4)",
     False, ["python", "scripts/build_conformance_report.py"]),  # advisory
    ("[10] Conformance Result (Admission gate ADM-001..008)",
     False, ["python", "scripts/check_admission_gate.py"]),  # advisory
    ("[10] Conformance Result (Documentation DOC-001..003)",
     False, ["python", "scripts/check_documentation_conformance.py"]),  # advisory
    ("[11] L2 Qualification (BP-C1..C4)",
     False, ["python", "scripts/check_l2_qualification.py", "--strict"]),  # CR-BP-34a; advisory
    ("[12] Intent Purposive (PSP-001..003)",
     False, ["python", "scripts/check_intent_purposive.py", "--strict"]),  # CR-BP-34b; advisory
    ("[13] Lifecycle State-Machine (LCM-001..005)",
     False, ["python", "scripts/check_lifecycle_state.py", "--strict"]),  # CR-BP-34c; advisory
    ("[14] Semantic Identity vs Version (SIV-001..004)",
     False, ["python", "scripts/check_semantic_identity_version.py", "--strict"]),  # CR-BP-34d; advisory
    ("[15] Activity Model (ACT-001..010)",
     False, ["python", "scripts/check_activity_model.py", "--strict"]),  # CR-BP-32; advisory
    ("[16] Execution Boundary (EXE-001..010)",
     False, ["python", "scripts/check_execution_boundary.py", "--strict"]),  # CR-BP-33; advisory
    ("[17] MECE Validation (MECE-001..008)",
     False, ["python", "scripts/check_mece.py", "--strict"]),  # CR-BP-36; advisory
    ("[18] Cross-Repository Integrity (XRI-001..005)",
     False, ["python", "scripts/check_cross_repo_integrity.py", "--strict"]),  # CR-BP-40; advisory (promoted from runtime asset per CR-BP-37 §3)
    ("[19] Lifecycle Discovery (DISC-001..008)",
     False, ["python", "scripts/check_lifecycle_discovery.py", "--strict"]),  # CR-BP-62; advisory
]


def _run_gate(name: str, blocking: bool, argv: list[str],
              catalog_root: Path) -> GateResult:
    """Run a single gate and return the structured result."""
    proc = subprocess.run(
        argv, capture_output=True, text=True, cwd=str(catalog_root),
    )
    # Take the first non-blank line as the verdict line.
    verdict_line = next(
        (l.strip() for l in proc.stdout.splitlines() if l.strip()),
        "(no output)",
    )
    return GateResult(
        name=name,
        blocking=blocking,
        returncode=proc.returncode,
        verdict_line=verdict_line,
        raw_stdout=proc.stdout,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--catalog-root", default=".")
    parser.add_argument("--strict", action="store_true",
                        help="Treat any non-zero gate returncode as failure.")
    parser.add_argument("--json", action="store_true",
                        help="Emit JSON output.")
    args = parser.parse_args(argv)

    root = Path(args.catalog_root).resolve()
    results: list[GateResult] = []
    for name, blocking, argv2 in GATES:
        results.append(_run_gate(name, blocking, argv2, root))

    blocking_failures = [r for r in results if r.blocking and not r.passed]
    advisory_failures = [r for r in results if (not r.blocking) and not r.passed]
    any_failure = blocking_failures or (args.strict and advisory_failures)

    if any_failure:
        verdict = "NON-CONFORMANT"
    elif advisory_failures:
        verdict = "CONFORMANT-WITH-WARNINGS"
    else:
        verdict = "CONFORMANT"

    summary = {
        "verdict": verdict,
        "blocking_failures": [
            {"gate": r.name, "exit": r.returncode, "verdict": r.verdict_line}
            for r in blocking_failures
        ],
        "advisory_failures": [
            {"gate": r.name, "exit": r.returncode, "verdict": r.verdict_line}
            for r in advisory_failures
        ],
        "gates": [
            {
                "name": r.name,
                "blocking": r.blocking,
                "returncode": r.returncode,
                "verdict_line": r.verdict_line,
            }
            for r in results
        ],
    }
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(f"Conformance Result (CR-BP-16 §18): {verdict}")
        print(f"  {len(results)} gates evaluated; "
              f"{len(blocking_failures)} blocking failures, "
              f"{len(advisory_failures)} advisory failures.")
        for r in results:
            tag = "FAIL" if not r.passed else "PASS"
            kind = "BLOCKING" if r.blocking else "ADVISORY"
            print(f"    [{tag}/{kind}] {r.name}: {r.verdict_line[:80]}")
    return 1 if any_failure else 0


if __name__ == "__main__":
    sys.exit(main())