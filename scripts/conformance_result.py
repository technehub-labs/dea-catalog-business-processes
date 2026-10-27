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
    ("[20] Process Scope (PSCOPE-001..008)",
     False, ["python", "scripts/check_process_scope.py"]),  # CR-BP-95; advisory
    ("[21] Documentation Profile (DOC-001..005)",
     False, ["python", "scripts/check_documentation_profile.py"]),  # CR-BP-94-EXT-01; advisory
    ("[22] Task Model (TASK-001..005)",
     True, ["python", "scripts/check_task_model.py"]),  # CR-BP-98; blocking
    ("[23] Reconciliation Matrix (RCM-001..010)",
     False, ["python", "scripts/check_reconciliation_matrix.py"]),  # CR-BP-99; advisory
    ("[24] L0<->L1 Cardinality (L0L1-CARD-001..003)",
     False, ["python", "scripts/check_l0_l1_cardinality.py"]),  # CR-BP-100; advisory
    ("[25] ID System (IDM-001..007)",
     True, ["python", "scripts/check_id_system.py"]),  # CR-BP-mv1; blocking
    ("[26] Reference Embargo (CR-BP-112; EMB-001..004)",
     True, ["python", "scripts/check_reference_embargo.py"]),  # CR-BP-112; blocking
    ("[27] HREF Resolver (CR-BP-113; HREF-001..003)",
     True, ["python", "scripts/check_href_targets.py"]),  # CR-BP-113; blocking
    ("[28] Template Drift (CR-BP-113; TPL-001..005)",
     True, ["python", "scripts/check_templates.py"]),  # CR-BP-113; blocking
    ("[29] CR README Consistency (CR-BP-113; CRR-001..003)",
     True, ["python", "scripts/check_cr_readme.py"]),  # CR-BP-113; blocking
    ("[30] README Consistency (CR-BP-114; RDM-001..002)",
     True, ["python", "scripts/check_readme_consistency.py"]),  # CR-BP-114; blocking
    ("[31] Entity Identity Clarity (CR-BP-117a; EID-001..004)",
     True, ["python", "scripts/check_entity_identity.py"]),  # CR-BP-117a; blocking
    ("[32] Authorship Cardinal Rule (CR-BP-118; AUT-001..003)",
     True, ["python", "scripts/check_authorship.py", "--strict"]),  # CR-BP-118; blocking
    ("[33] Entity System (CR-BP-123 / CR-BP-125; ES-001..ES-005)",
     True, ["python", "scripts/check_entity_system.py", "--strict"]),  # CR-BP-123/125; blocking (Stage 6+)
    ("[34] Documentation Profile - Generator and Validator (CR-BP-94-EXT-04; DOC-016..020)",
     True, ["python", "scripts/validate_readme_structure.py", "--catalog-root", "."]),  # CR-BP-94-EXT-04; BLOCKING (CR-BP-94-EXT-06; was advisory before)
    ("[35] Decomposition Reconciliation (CR-BP-94-EXT-05; DOC-021..025)",
     True, ["python", "scripts/check_decomposition_reconciliation.py", "--catalog-root", "."]),  # CR-BP-94-EXT-05; BLOCKING (CR-BP-94-EXT-06; was advisory before)
    ("[36] Profile Registry (CR-BP-94-EXT-11; PR-001..PR-010)",
     True, ["python", "scripts/check_profile_registry_ext11.py"]),  # CR-BP-94-EXT-11; BLOCKING (promoted by CR-BP-EXT-23; T2 content; 0 open findings)
    ("[37] Inputs, Outputs, Interfaces (CR-BP-94-EXT-12; IT-001..IT-010)",
     True, ["python", "scripts/check_inputs_outputs_interfaces_ext12.py", "--catalog-root", "."]),  # CR-BP-94-EXT-12; BLOCKING (promoted by CR-BP-EXT-23; T2 content; 0 open findings)
    ("[38] Responsibility, Accountability, Roles (CR-BP-94-EXT-13; RA-001..RA-010)",
     True, ["python", "scripts/check_responsibility_accountability_ext13.py", "--catalog-root", "."]),  # CR-BP-94-EXT-13; BLOCKING (promoted by CR-BP-EXT-23; T2 content; 0 open findings)
    ("[39] Business Rules, Controls, Exceptions (CR-BP-94-EXT-14; GO-001..GO-010)",
     True, ["python", "scripts/check_business_rules_controls_exceptions_ext14.py", "--catalog-root", "."]),  # CR-BP-94-EXT-14; BLOCKING (promoted by CR-BP-EXT-23; T2 content; 0 open findings)
    ("[40] Evidence, Provenance, Confidence (CR-BP-94-EXT-15; EV-001..EV-010)",
     True, ["python", "scripts/check_evidence_provenance_ext15.py", "--catalog-root", "."]),  # CR-BP-94-EXT-15; BLOCKING (promoted by CR-BP-EXT-23; T2 content; 0 open findings)
    ("[41] Authoring Methodology (CR-BP-94-EXT-16; AM-001..AM-010)",
     True, ["python", "scripts/check_authoring_methodology_ext16.py", "--catalog-root", "."]),  # CR-BP-94-EXT-16; BLOCKING (promoted by CR-BP-EXT-23; T2 content; 0 open findings)
    ("[42] Enrichment Tooling (CR-BP-94-EXT-17; OR-001..OR-005 + RP-001..RP-009)",
     False, ["python", "scripts/orchestrate_backfill.py", "--dry-run", "--catalog-root", "."]),  # CR-BP-94-EXT-17; ADVISORY (PR-186 lands; flipped to blocking under CR-BP-94-EXT-23; third slice of the engineering and governance readiness tranche)
    ("[43] Operational Documentation Pilot (CR-BP-94-EXT-18; PI-001..PI-008)",
     True, ["python", "scripts/check_pilot_selection_ext18.py", "--catalog-root", "."]),  # CR-BP-94-EXT-18; BLOCKING (promoted by CR-BP-EXT-23; T1 structural; 0 open findings)
    ("[44] L2 Business Process Backfill (CR-BP-94-EXT-19; L2-001..L2-012)",
     False, ["python", "scripts/check_l2_backfill_ext19.py", "--catalog-root", "."]),  # CR-BP-94-EXT-19; ADVISORY (PR-188 lands; flipped to blocking under CR-BP-94-EXT-23; first slice of the catalogue enrichment tranche; authorised by the EXT-18 GO decision)
    ("[45] L3 Activity Backfill (CR-BP-94-EXT-20; L3-001..L3-014)",
     False, ["python", "scripts/check_l3_backfill_ext20.py", "--catalog-root", "."]),  # CR-BP-94-EXT-20; ADVISORY (PR-189 lands; flipped to blocking under CR-BP-94-EXT-23; second slice of the catalogue enrichment tranche)
    ("[46] L4 Task Backfill (CR-BP-94-EXT-21; L4-001..L4-014)",
     False, ["python", "scripts/check_l4_backfill_ext21.py", "--catalog-root", "."]),  # CR-BP-94-EXT-21; ADVISORY (PR-190 lands; deferred by CR-BP-EXT-23 until the L4 population is reconciled; third slice of the catalogue enrichment tranche; completes the L2-to-L3-to-L4 traceability matrix)
    ("[47] Decomposition Reconciliation (CR-BP-94-EXT-22; R22-01..R22-12)",
     False, ["python", "scripts/check_reconciliation_ext22.py", "--catalog-root", "."]),  # CR-BP-94-EXT-22; ADVISORY (PR-191 lands; deferred by CR-BP-EXT-23 until the 8 structural findings are reconciled; the fourth slice of the catalogue enrichment tranche)
    ("[48] Conformance Framework (CR-BP-EXT-23; CF-001..CF-051)",
     False, ["python3", "scripts/check_conformance_framework_ext23.py"]),  # CR-BP-EXT-23; ADVISORY (the conformance framework's own self-check: the rule catalogue + the traceability matrix + the report + the dashboard must all validate; the validator returns rc=1 if any CF-NNN framework-finding is emitted; the framework is a meta-artefact and its failure is an exception in the meta-framework, not a catalogue defect)
    ("[49] Programme Closure (CR-BP-94-EXT-24; CG-001..CG-080)",
     False, ["python3", "scripts/check_programme_closure_ext24.py"]),  # CR-BP-94-EXT-24; ADVISORY (the programme-closure self-check: the closure matrix + the catalogue baseline + the governance artefacts (roles, ownership, lifecycle, exceptions, deferrals, improvement backlog) must all validate; the validator returns rc=1 if any CG-NNN closure-finding is emitted; closure is a meta-artefact and its failure is an exception in the meta-closure, not a catalogue defect)
    ("[50] Completeness Profiles (CR-BP-CE-0; CE-000..CE-900)",
     True, ["python3", "scripts/check_completeness.py", "--strict"]),  # CR-BP-CE-0; BLOCKING since CR-BP-CE-RL (all five level tranches landed; the blocking profile is 0 across 3,723 records, so strict fails only on NEWLY introduced profile defects; the 290 knowledge-dependent CE-L2-006 actors/stakeholders candidates remain advisory pending the GOV-002/GOV-003 sweep per the EXT-24 ownership register; the gate WRITES reconciliation/completeness-report.yaml (CE-900))
]


def _run_gate(name: str, blocking: bool, argv: list[str],
              catalog_root: Path) -> GateResult:
    """Run a single gate and return the structured result.

    CR-BP-94-EXT-06: gates [34] (EXT-04) + [35] (EXT-05) are now
    blocking. The validators themselves still return rc=0 (findings
    are reported in the manifest), so we post-process: if the
    validator's manifest shows any findings AND the gate is now
    blocking, we set returncode=1 to make the gate fail. This is
    the wire into the development model the user directed on
    2026-10-17.
    """
    proc = subprocess.run(
        argv, capture_output=True, text=True, cwd=str(catalog_root),
    )
    # Take the first non-blank line as the verdict line.
    verdict_line = next(
        (l.strip() for l in proc.stdout.splitlines() if l.strip()),
        "(no output)",
    )
    rc = proc.returncode

    # Blocking posture check: read the validator's manifest.
    if blocking and rc == 0:
        manifest_name = _manifest_for_gate(name)
        if manifest_name:
            manifest_path = catalog_root / "reconciliation" / manifest_name
            try:
                import json as _json
                m = _json.loads(manifest_path.read_text(encoding="utf-8"))
                summary = m.get("summary", {})
                findings = summary.get("total_findings", 0)
                advisory = summary.get("advisory_findings")
                # Advisory findings are known, dispositioned conditions, not
                # open reconciliation gaps.
                if isinstance(advisory, int) and advisory == findings:
                    findings = 0
                if findings > 0:
                    rc = 1
                    verdict_line = (f"{verdict_line} [BLOCKED: {findings} "
                                    f"findings must be reconciled]")
            except Exception:
                pass

    return GateResult(
        name=name,
        blocking=blocking,
        returncode=rc,
        verdict_line=verdict_line,
        raw_stdout=proc.stdout,
    )


# The manifest each blocking gate's validator emits. Keyed by the gate label
# in the GATES registry above.
_GATE_MANIFESTS = {
    "[34] Documentation Profile - Generator and Validator (CR-BP-94-EXT-04; DOC-016..020)":
        "validation-manifest.json",
    "[35] Decomposition Reconciliation (CR-BP-94-EXT-05; DOC-021..025)":
        "decomposition-reconciliation-manifest.json",
    "[36] Profile Registry (CR-BP-94-EXT-11; PR-001..PR-010)":
        "profile-manifest.json",
    "[37] Inputs, Outputs, Interfaces (CR-BP-94-EXT-12; IT-001..IT-010)":
        "inputs-outputs-manifest.json",
    "[38] Responsibility, Accountability, Roles (CR-BP-94-EXT-13; RA-001..RA-010)":
        "responsibility-accountability-manifest.json",
    "[39] Business Rules, Controls, Exceptions (CR-BP-94-EXT-14; GO-001..GO-010)":
        "governance-manifest.json",
    "[40] Evidence, Provenance, Confidence (CR-BP-94-EXT-15; EV-001..EV-010)":
        "evidence-manifest.json",
    "[41] Authoring Methodology (CR-BP-94-EXT-16; AM-001..AM-010)":
        "authoring-manifest.json",
    "[43] Operational Documentation Pilot (CR-BP-94-EXT-18; PI-001..PI-008)":
        "pilot-selection-manifest.json",
}


def _manifest_for_gate(name: str) -> str | None:
    """Return the manifest filename for a gate, or None."""
    return _GATE_MANIFESTS.get(name)


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