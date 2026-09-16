#!/usr/bin/env python3
"""New Process Admission Gate (CR-BP-16 S15; ADM-001..008).

CR-BP-16 S15 mandates the 14-step admission gate for new Business
Processes:

  Candidate -> Evidence -> Identity -> Context -> Group Fit ->
  Boundary -> Intent -> Classification -> Specialization ->
  Sibling Analysis -> MECE -> Schema -> Provenance -> Governance
  -> CANONICAL

A new admission candidate is a YAML file under
entities/v1-alpha/dea:process-<new>/ that does NOT yet have an
entry in the disposition register's LOCKED set. The gate runs
eight blocking checks (ADM-001..008):

  ADM-001  Evidence coverage. Required: change_history[*].cr
           pointing at an admission CR (CR-BP-NN(.X)?).
  ADM-002  Identity shape. Required fields: name, type=Process,
           version. id matches dea:process-[a-z0-9-]+.
  ADM-003  Context resolution. context[].ref MUST resolve to a
           canonical Process Context under contexts/v1-alpha/.
  ADM-004  Group fit. If process_group_id is present, MUST
           resolve to a canonical Process Group.
  ADM-005  Boundary completeness. Required: triggers (list) and
           outcomes (list), each non-empty.
  ADM-006  Intent + Classification in approved vocabularies.
  ADM-007  Specialization validity. If specializations[] present,
           every parent must resolve to a canonical Process.
  ADM-008  Provenance. change_history non-empty with at least one
           entry with date + cr + change fields.

Usage::

    python3 scripts/check_admission_gate.py
        [--strict]                # all ADM-001..008 findings are blocking
        [--strict-provenance]     # only ADM-001 + ADM-008 are blocking
                                  # (advisory for the rest). Used in CI
                                  # to enforce §17 Step 8 (provenance)
                                  # without flipping the §15 boundary
                                  # recommendation to a hard rule.
        [--json] [--self-test]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

import yaml

ID_PATTERN = re.compile(r"^dea:process-[a-z0-9-]+$")
PC_PATTERN = re.compile(r"^dea:pc-[a-z0-9-]+$")
PG_PATTERN = re.compile(r"^dea:pg-[a-z0-9-]+$")
APPROVED_INTENTS = {
    "govern", "manage", "operate", "deliver", "support", "develop",
    "transform",
}


def _catalog_pc_ids(root: Path) -> set[str]:
    ids: set[str] = set()
    for d in (root / "contexts" / "v1-alpha").rglob("*.yaml"):
        data = _try_load(d)
        if isinstance(data, dict):
            rid = data.get("id")
            if isinstance(rid, str):
                ids.add(rid)
    return ids


def _catalog_pg_ids(root: Path) -> set[str]:
    ids: set[str] = set()
    for d in (root / "entities" / "v1-alpha").rglob("*.yaml"):
        # Only ProcessGroup records (top-level file under dea:pg-*)
        rel = d.relative_to(root)
        parts = rel.parts
        if len(parts) >= 3 and parts[1].startswith("dea:pg-"):
            data = _try_load(d)
            if isinstance(data, dict):
                rid = data.get("id")
                if isinstance(rid, str):
                    ids.add(rid)
    return ids


def _catalog_process_ids(root: Path) -> set[str]:
    ids: set[str] = set()
    for d in (root / "entities" / "v1-alpha").rglob("*.yaml"):
        data = _try_load(d)
        if isinstance(data, dict):
            rid = data.get("id")
            if isinstance(rid, str) and rid.startswith("dea:process-"):
                ids.add(rid)
    return ids


def _try_load(path: Path) -> dict | None:
    try:
        return yaml.safe_load(path.read_text())
    except (yaml.YAMLError, OSError):
        return None


def _disposition_locked_ids(root: Path) -> set[str]:
    """Return the set of record_ids with register_status=LOCKED entries."""
    path = root / "reconciliation" / "dispositions" / "register.yaml"
    if not path.exists():
        return set()
    data = _try_load(path)
    if not isinstance(data, dict):
        return set()
    locked = set()
    for entry in data.get("dispositions", []) or []:
        if isinstance(entry, dict) and entry.get("lock_status") == "LOCKED":
            locked.add(entry.get("record_id"))
    return {r for r in locked if r}


def check_admission(path: Path, root: Path,
                    pc_ids: set[str], pg_ids: set[str],
                    process_ids: set[str]) -> list[tuple[str, str]]:
    """Return [(rule_code, finding), ...] for a candidate Process."""
    findings: list[tuple[str, str]] = []
    data = _try_load(path)
    if not isinstance(data, dict):
        return [("ADM-PARSE", f"YAML parse error in {path.relative_to(root)}")]

    rec_id = data.get("id")
    if not isinstance(rec_id, str) or not ID_PATTERN.match(rec_id):
        findings.append((
            "ADM-002",
            f"{path.relative_to(root)}: id {rec_id!r} does not match "
            "`dea:process-[a-z0-9-]+`",
        ))

    # ADM-002: identity shape
    name = data.get("name")
    typ = data.get("type")
    version = data.get("version")
    if not name or not isinstance(name, str):
        findings.append(("ADM-002", f"{rec_id}: missing or non-string name"))
    if typ != "Process":
        findings.append((
            "ADM-002",
            f"{rec_id}: type={typ!r} (must be 'Process')",
        ))
    if not version or not isinstance(version, str):
        findings.append(("ADM-002", f"{rec_id}: missing version"))

    # ADM-003: context resolution
    context_refs = [c.get("ref") for c in data.get("context", []) or []
                    if isinstance(c, dict)]
    for ref in context_refs:
        if not isinstance(ref, str) or not PC_PATTERN.match(ref):
            findings.append((
                "ADM-003",
                f"{rec_id}: context ref {ref!r} is not a valid "
                "`dea:pc-[a-z0-9-]+` id",
            ))
            continue
        if ref not in pc_ids:
            findings.append((
                "ADM-003",
                f"{rec_id}: context ref {ref!r} does not resolve to a "
                f"canonical Process Context",
            ))

    # ADM-004: group fit
    pg = data.get("process_group_id")
    if pg is not None:
        if not isinstance(pg, str) or not PG_PATTERN.match(pg):
            findings.append((
                "ADM-004",
                f"{rec_id}: process_group_id {pg!r} is not a valid "
                "`dea:pg-[a-z0-9-]+` id",
            ))
        elif pg not in pg_ids:
            findings.append((
                "ADM-004",
                f"{rec_id}: process_group_id {pg!r} does not resolve to a "
                f"canonical Process Group",
            ))

    # ADM-005: boundary completeness
    triggers = data.get("triggers") or []
    outcomes = data.get("outcomes") or []
    if not (isinstance(triggers, list) and triggers):
        findings.append((
            "ADM-005",
            f"{rec_id}: triggers missing or empty (boundary)",
        ))
    if not (isinstance(outcomes, list) and outcomes):
        findings.append((
            "ADM-005",
            f"{rec_id}: outcomes missing or empty (boundary)",
        ))

    # ADM-006: intent + classification in approved vocabularies
    intent = data.get("process_intent")
    if intent not in APPROVED_INTENTS:
        findings.append((
            "ADM-006",
            f"{rec_id}: process_intent={intent!r} not in approved "
            f"vocabulary {sorted(APPROVED_INTENTS)}",
        ))

    # ADM-007: specialization validity
    for parent in data.get("process_specialization", []) or []:
        if parent not in process_ids:
            findings.append((
                "ADM-007",
                f"{rec_id}: specialization parent {parent!r} does not "
                f"resolve to a canonical Process",
            ))

    # ADM-008: provenance. Process records carry their provenance
    # under `metadata.change_history` (canonical schema; see
    # CR-BP-15-IMP Phase 2). Top-level `change_history` is also
    # accepted as a legacy location so the gate stays robust
    # against ad-hoc record shapes.
    change_history = (
        data.get("change_history")
        or data.get("metadata", {}).get("change_history")
        or []
    )
    if not isinstance(change_history, list) or not change_history:
        findings.append((
            "ADM-008",
            f"{rec_id}: metadata.change_history missing or empty (provenance)",
        ))
    else:
        # Every change_history entry must have date + cr + change.
        for j, entry in enumerate(change_history):
            if not isinstance(entry, dict):
                findings.append((
                    "ADM-008",
                    f"{rec_id}: change_history[{j}] is not a mapping",
                ))
                continue
            if not entry.get("date"):
                findings.append((
                    "ADM-008",
                    f"{rec_id}: change_history[{j}] missing date",
                ))
            if not entry.get("cr"):
                findings.append((
                    "ADM-008",
                    f"{rec_id}: change_history[{j}] missing cr",
                ))
            if not entry.get("change"):
                findings.append((
                    "ADM-008",
                    f"{rec_id}: change_history[{j}] missing change",
                ))
        # ADM-001: at least one entry must reference an admission CR.
        # We treat CR-BP-13[a-z] (a/b/c/d admission tranches) and
        # CR-BP-03C (sample-process-contribution walk-the-flow) as
        # admission authorities. CR-BP-03C predates the formal
        # CR-BP-13 admission programme but is functionally equivalent
        # (it admitted the first canonical sample process, see
        # change-requests/CR-BP-03C-sample-process-contribution.md).
        # CR-BP-19/20/21a..e (StrategyAndDirection landing) are the
        # rediscovery / alignment / landing tranches under the v2.4.0
        # admission programme, and are accepted as admission
        # authorities for new L1/L2 entries landed under them.
        # CR-BP-64.. are the discovery-driven admission tranches under
        # the CR-BP-62/63 lifecycle discovery programme: each admission
        # tranche registers its own CR number here as it lands.
        # CR-BP-70: escape-clause discovery for P&R x Activate (KYC);
        # CR-BP-71: P&R Activate admission tranche landed under it.
        # CR-BP-72: escape-clause discovery for A&O x Retire (mass-layoff
        # regulated wind-down); CR-BP-73: A&O Retire admission tranche
        # landed under it.
        # CR-BP-74: escape-clause discovery for F&A x Retire (regulated
        # run-off / mutual insurer); CR-BP-75: F&A Retire admission
        # tranche landed under it.
        # CR-BP-76: escape-clause discovery for G&E x Retire
        # (regulator-mandated governance unwind); CR-BP-78: G&E
        # Retire admission tranche landed under it.
        _ADMISSION_CR_RE = re.compile(
            r"^(?:CR-BP-13[a-z]?|CR-BP-19|CR-BP-20|CR-BP-21[a-z]?|CR-BP-03C|CR-BP-64|CR-BP-65|CR-BP-66|CR-BP-67|CR-BP-71|CR-BP-73|CR-BP-75|CR-BP-78)(?:\.\d+)*$"
        )
        has_admission = any(
            isinstance(e, dict) and _ADMISSION_CR_RE.match(
                (e.get("cr") or "")
            )
            for e in change_history
        )
        if not has_admission:
            findings.append((
                "ADM-001",
                f"{rec_id}: no admission CR (CR-BP-13..) in change_history",
            ))

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--catalog-root", default=".")
    parser.add_argument("--strict", action="store_true",
                        help="Treat all ADM-001..008 findings as errors")
    parser.add_argument("--strict-provenance", action="store_true",
                        help="Treat only ADM-001 + ADM-008 findings as "
                             "errors (provenance/evidence coverage). "
                             "Used by CI for CR-BP-16 §17 Step 8 "
                             "(blocking).")
    parser.add_argument("--json", action="store_true",
                        help="Emit JSON output")
    parser.add_argument("--self-test", action="store_true",
                        help="Run self-test and exit")
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    root = Path(args.catalog_root).resolve()
    pc_ids = _catalog_pc_ids(root)
    pg_ids = _catalog_pg_ids(root)
    process_ids = _catalog_process_ids(root)
    locked = _disposition_locked_ids(root)

    # Walk all Process records. Candidates (not in LOCKED) are checked
    # against ADM-001..008. LOCKED records are also checked, with
    # findings reported but not gating.
    candidates: list[tuple[Path, bool]] = []
    for d in sorted((root / "entities" / "v1-alpha").rglob("dea:process-*")):
        if not d.is_dir():
            continue
        files = list(d.glob("dea:process-*.yaml"))
        if not files:
            continue
        candidates.append((files[0], False))

    findings: list[dict[str, str]] = []
    for path, _ in candidates:
        for code, msg in check_admission(path, root, pc_ids, pg_ids, process_ids):
            findings.append({
                "rule": code,
                "path": str(path.relative_to(root)),
                "message": msg,
            })

    # Decide which findings are blocking. --strict blocks everything;
    # --strict-provenance blocks only ADM-001 + ADM-008 (the
    # provenance/evidence rules that §17 Step 8 enforces).
    if args.strict:
        blocking = list(findings)
    elif args.strict_provenance:
        blocking = [f for f in findings if f["rule"] in ("ADM-001", "ADM-008")]
    else:
        blocking = []

    verdict = (
        "NON-CONFORMANT" if blocking else
        "CONFORMANT-WITH-WARNINGS" if findings else
        "CONFORMANT"
    )
    if args.json:
        print(json.dumps({
            "verdict": verdict,
            "findings": findings,
            "blocking_findings": blocking,
            "blocking_rules": (
                "all" if args.strict else
                "ADM-001+ADM-008" if args.strict_provenance else
                "none"
            ),
            "candidate_count": len(candidates),
            "locked_count": len(locked),
        }, indent=2))
    else:
        print(f"Admission Gate (CR-BP-16 S15; ADM-001..008): {verdict}")
        if findings:
            blocking_msg = (
                f" ({len(blocking)} blocking)" if blocking else ""
            )
            print(f"  {len(findings)} findings{blocking_msg} across "
                  f"{len(candidates)} Process records")
            # Per-rule breakdown is never truncated so that specific
            # ADM codes remain greppable even when the first-10 window
            # is saturated by one rule class.
            from collections import Counter
            code_counts = Counter(f["rule"] for f in findings)
            for code in sorted(code_counts):
                print(f"    {code}: {code_counts[code]} finding(s)")
            for f in findings[:10]:
                marker = "[BLOCKING] " if f in blocking else ""
                print(f"    {marker}[{f['rule']}] {f['path']}: {f['message']}")
            if len(findings) > 10:
                print(f"    ... and {len(findings) - 10} more")
        else:
            print(f"  {len(candidates)} Process records, all admission-gate compliant")
    return 1 if blocking else 0


def _self_test() -> int:
    """Exercise each rule via fixtures."""
    import tempfile

    failed: list[str] = []
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        entities = root / "entities" / "v1-alpha"
        contexts = root / "contexts" / "v1-alpha"
        (entities / "dea:process-candidate-bad").mkdir(parents=True)
        (entities / "dea:process-candidate-bad" / "dea:process-candidate-bad.yaml").write_text(yaml.safe_dump({
            "id": "dea:process-candidate-bad",
            "name": None,  # missing
            "type": "Process",
            "version": "1.0.0",
            "process_intent": "harmonise",  # ADM-006
            "process_type": "core",
            "context": [{"ref": "dea:pc-unknown"}],  # ADM-003
            "process_group_id": "dea:pg-bogus",  # ADM-004
            "triggers": [],  # ADM-005
            "outcomes": [],  # ADM-005
            "process_specialization": ["dea:process-bogus-parent"],  # ADM-007
            "change_history": [{"date": "2026-09-06", "cr": None, "change": None}],  # ADM-008
        }, sort_keys=False))
        (contexts).mkdir(parents=True, exist_ok=True)
        (contexts / "dea-pc-pr-op.yaml").write_text(yaml.safe_dump({
            "id": "dea:pc-pr-op", "name": "Customer Demand Operate",
            "type": "ProcessContext",
        }))
        # Disposition register must exist for the gate to read LOCKED
        # set; absent is fine.
        findings = []
        pc_ids = _catalog_pc_ids(root)
        pg_ids = _catalog_pg_ids(root)
        process_ids = _catalog_process_ids(root)
        bad_file = next((entities / "dea:process-candidate-bad").glob("dea:process-*.yaml"))
        for code, msg in check_admission(bad_file, root, pc_ids, pg_ids, process_ids):
            findings.append(code)
        seen = set(findings)
        # ADM-002 missing name, ADM-003 unknown pc, ADM-004 unknown pg,
        # ADM-005 triggers empty, ADM-005 outcomes empty, ADM-006 bad
        # intent, ADM-007 unknown parent, ADM-008 bad provenance,
        # ADM-001 no admission CR.
        expected = {"ADM-002", "ADM-003", "ADM-004", "ADM-005",
                    "ADM-006", "ADM-007", "ADM-008", "ADM-001"}
        for code in expected:
            if code not in seen:
                failed.append(f"expected {code} to fire on bad fixture")

        # Good fixture: every field present and valid.
        (entities / "dea:process-candidate-good").mkdir(parents=True)
        (entities / "dea:process-candidate-good" / "dea:process-candidate-good.yaml").write_text(yaml.safe_dump({
            "id": "dea:process-candidate-good",
            "name": "Candidate Good",
            "type": "Process",
            "version": "1.0.0",
            "process_intent": "manage",
            "process_type": "core",
            "context": [{"ref": "dea:pc-pr-op"}],
            "triggers": ["trigger"],
            "outcomes": ["outcome"],
            "change_history": [
                {"date": "2026-09-06", "cr": "CR-BP-13a",
                 "change": "Initial admission under CR-BP-13a."},
            ],
        }, sort_keys=False))
        good_file = next((entities / "dea:process-candidate-good").glob("dea:process-*.yaml"))
        good_findings = []
        for code, msg in check_admission(good_file, root, pc_ids, pg_ids, process_ids):
            good_findings.append(code)
        if good_findings:
            failed.append(f"good fixture fired: {good_findings}")

        # CR-BP-16 §17 Step 8 path regression: provenance stored
        # under metadata.change_history MUST be read.
        (entities / "dea:process-meta-path-good").mkdir(parents=True)
        (entities / "dea:process-meta-path-good" /
         "dea:process-meta-path-good.yaml").write_text(yaml.safe_dump({
            "id": "dea:process-meta-path-good",
            "name": "Meta Path Good",
            "type": "Process",
            "version": "1.0.0",
            "process_intent": "manage",
            "process_type": "core",
            "context": [{"ref": "dea:pc-pr-op"}],
            "metadata": {
                "change_history": [
                    {"date": "2026-09-03", "cr": "CR-BP-03C",
                     "change": "Sample-process-contribution admission."},
                ],
            },
        }, sort_keys=False))
        meta_file = next((entities / "dea:process-meta-path-good").glob(
            "dea:process-*.yaml"))
        meta_findings = []
        for code, msg in check_admission(meta_file, root, pc_ids,
                                        pg_ids, process_ids):
            meta_findings.append(code)
        if "ADM-008" in meta_findings or "ADM-001" in meta_findings:
            failed.append(
                "metadata.change_history path not read: "
                f"got findings {meta_findings}"
            )

        # CR-BP-03C admission CR acceptance (legacy sample CR).
        (entities / "dea:process-bp-15-only").mkdir(parents=True)
        (entities / "dea:process-bp-15-only" /
         "dea:process-bp-15-only.yaml").write_text(yaml.safe_dump({
            "id": "dea:process-bp-15-only",
            "name": "Migration Only",
            "type": "Process",
            "version": "1.0.0",
            "process_intent": "manage",
            "process_type": "core",
            "context": [{"ref": "dea:pc-pr-op"}],
            "metadata": {
                "change_history": [
                    {"date": "2026-09-06", "cr": "CR-BP-15-IMP",
                     "change": "Phase 5 migration only."},
                ],
            },
        }, sort_keys=False))
        mig_file = next((entities / "dea:process-bp-15-only").glob(
            "dea:process-*.yaml"))
        mig_findings = []
        for code, msg in check_admission(mig_file, root, pc_ids,
                                        pg_ids, process_ids):
            mig_findings.append(code)
        if "ADM-001" not in mig_findings:
            failed.append(
                "expected ADM-001 (no admission CR) on CR-BP-15-IMP-only "
                f"fixture; got {mig_findings}"
            )

    if failed:
        print("self-test FAIL:", failed)
        return 1
    print("self-test PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())