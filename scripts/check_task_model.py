#!/usr/bin/env python3
"""
check_task_model.py
===================

L4 Task structural validator (CR-BP-98; TASK-001..005).

Codifies the L4 Task structural invariants from CR-BP-93 §7 and the
L4 normative info-requirement matrix in CR-BP-93 §9. The validator
fires on any record where `type: Task`. Today the catalog has zero
Task records; the validator is a regression guard that prepares the
catalog for the first opt-in L4 contribution (CR-BP-99 reconciliation
or a dedicated L4 tranche).

Rules:

  TASK-001 — Task id format. The id must match `dea:task-*`
             (CR-BP-04 §4 id family). The discriminator `type: Task`
             alone is not sufficient.

  TASK-002 — Definition + responsibility + boundary (CR-BP-93 §9:
             `Definition`, `Boundary` are `Required` at L4;
             `Responsibility` is `Required` at L4).

  TASK-003 — Trigger + outcome (CR-BP-93 §9: `Trigger` is `Required`
             at L4; `Outcomes` is `Completion state` at L4, which
             requires a `definition`-like state marker).

  TASK-004 — belongs_to_activity must resolve. The parent L3 Activity
             must exist in the catalog. (CR-BP-93 §7: L4 is composed
             by exactly one parent L3 Activity.)

  TASK-005 — Disallowed at L4. The Task MUST NOT carry execution-
             ordering / workflow / orchestration semantics (CR-BP-93
             §7 Disallowed: `sequencing`, `branching`, `conditions`,
             `dependencies`, `participants`, `events`,
             `orchestration`, `state transitions`, `automation`).
             These belong to Workflow Definition (CR-BP-98 §13).
             Forbidden fields:
               sequencing, branching, conditions, dependencies,
               participants, events, orchestration, automation,
               workflow_definition, workflow_instance, executed_by,
               executed_at, execution_order, sequence_index,
               step_index, temporal_sequence, before, after,
               precedes, follows, triggers_workflow, next_step.

All TASK-001..005 are MANDATORY (NOT advisory). The schema dispatch
in `scripts/conformance_result.py` wires this gate as `BLOCKING`.

Self-test
---------
The validator runs a built-in self-test that constructs a valid L4
record and verifies that none of the five rules fire on it.

CLI
---
The script supports the conventional flags:
  --self-test : run the in-process self-test, exit 0 / 1
  --json      : emit a JSON payload, exit 0 / 1
  (no flag)   : run against the live catalog, exit 0 / 1

Live catalog
------------
Zero Task records exist today; the validator returns 0 findings and
verdict = CONFORMANT. The script's exit code is 0.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parent.parent
ENTITIES = ROOT / "entities" / "v1-alpha"

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

ID_PATTERN = r"^dea:task-[a-z0-9-]+$"
ACTIVITY_ID_PATTERN = r"^dea:activity-[a-z0-9-]+$"

# Disallowed-at-L4 fields per CR-BP-93 §7 (Execution lives downstream).
DISALLOWED_L4_FIELDS = frozenset({
    # Sequencing / orchestration (CR-BP-93 §7 Disallowed; CR-BP-92 §10)
    "sequencing", "branching", "conditions", "dependencies",
    "participants", "events", "orchestration", "automation",
    "state_transitions",
    # Workflow references (CR-BP-33 §15; CR-BP-93 §8 decomposition-vs-execution)
    "workflow_definition", "workflow_instance", "executed_by",
    "executed_at", "execution_order", "sequence_index",
    "step_index", "temporal_sequence", "before", "after",
    "precedes", "follows", "triggers_workflow", "next_step",
})

RULE_IDS = ("TASK-001", "TASK-002", "TASK-003", "TASK-004", "TASK-005")

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

import re
_ID_RE = re.compile(ID_PATTERN)
_ACTIVITY_ID_RE = re.compile(ACTIVITY_ID_PATTERN)


def _iter_task_records(entities_dir: Path = ENTITIES):
    """Yield (path, record) tuples for every `type: Task` record."""
    if not entities_dir.exists():
        return
    for path in sorted(entities_dir.glob("**/*.yaml")):
        # Skip state-directory files (research/, candidates/, retired/)
        if any(p in path.parts for p in ("research", "candidates", "retired")):
            continue
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        if data.get("type") == "Task":
            yield path, data


def _activity_exists(activity_id: str, entities_dir: Path = ENTITIES) -> bool:
    """Resolve the activity id against the canonical catalog."""
    if not _ACTIVITY_ID_RE.match(activity_id):
        return False
    # A canonical Activity record at entities/v1-alpha/<id>/<id>.yaml
    expected_dir = entities_dir / activity_id
    expected_file = expected_dir / f"{activity_id}.yaml"
    if not expected_file.exists():
        return False
    try:
        with open(expected_file) as f:
            data = yaml.safe_load(f)
    except Exception:
        return False
    return isinstance(data, dict) and data.get("type") == "Activity"


# -----------------------------------------------------------------------------
# Findings
# -----------------------------------------------------------------------------

@dataclass
class Finding:
    rule: str
    record_id: str
    severity: str
    message: str
    path: str

    def to_dict(self) -> dict:
        return {
            "rule": self.rule,
            "record_id": self.record_id,
            "severity": self.severity,
            "message": self.message,
            "path": self.path,
        }


# -----------------------------------------------------------------------------
# Per-rule checks
# -----------------------------------------------------------------------------


def _check_id_format(record: dict, path: str) -> list[Finding]:
    findings: list[Finding] = []
    rid = record.get("id", "")
    if not _ID_RE.match(rid):
        findings.append(Finding(
            rule="TASK-001",
            record_id=rid or "<missing>",
            severity="error",
            message=f"Task id {rid!r} does not match {ID_PATTERN!r}",
            path=path,
        ))
    return findings


def _check_definition_responsibility_boundary(record: dict, path: str) -> list[Finding]:
    """TASK-002 — Definition + Responsibility + Boundary (Required at L4)."""
    findings: list[Finding] = []
    rid = record.get("id", "<missing>")

    definition = record.get("definition")
    if not (isinstance(definition, str) and len(definition.strip()) > 0):
        findings.append(Finding(
            rule="TASK-002",
            record_id=rid,
            severity="error",
            message="Task `definition` must be a non-empty string (CR-BP-93 §9 Required at L4)",
            path=path,
        ))

    responsibility = record.get("responsibility")
    if not (isinstance(responsibility, str) and len(responsibility.strip()) > 0):
        findings.append(Finding(
            rule="TASK-002",
            record_id=rid,
            severity="error",
            message="Task `responsibility` must be a non-empty string (CR-BP-93 §9 Required at L4)",
            path=path,
        ))

    boundary = record.get("boundary")
    if not (isinstance(boundary, dict) and (
        (isinstance(boundary.get("inclusions"), list) and boundary["inclusions"])
        or (isinstance(boundary.get("exclusions"), list) and boundary["exclusions"])
    )):
        findings.append(Finding(
            rule="TASK-002",
            record_id=rid,
            severity="error",
            message="Task `boundary` must carry `inclusions[]` and/or `exclusions[]` (CR-BP-93 §9 Required at L4)",
            path=path,
        ))

    return findings


def _check_trigger_outcome(record: dict, path: str) -> list[Finding]:
    """TASK-003 — Trigger + Outcome (Required at L4)."""
    findings: list[Finding] = []
    rid = record.get("id", "<missing>")

    trigger = record.get("trigger")
    if not (isinstance(trigger, str) and len(trigger.strip()) > 0):
        findings.append(Finding(
            rule="TASK-003",
            record_id=rid,
            severity="error",
            message="Task `trigger` must be a non-empty string (CR-BP-93 §9 Required at L4)",
            path=path,
        ))

    outcome = record.get("outcome")
    if not (isinstance(outcome, str) and len(outcome.strip()) > 0):
        findings.append(Finding(
            rule="TASK-003",
            record_id=rid,
            severity="error",
            message="Task `outcome` must be a non-empty string (CR-BP-93 §9 Completion state at L4)",
            path=path,
        ))

    return findings


def _check_activity_resolution(record: dict, path: str, entities_dir: Path = ENTITIES) -> list[Finding]:
    """TASK-004 — belongs_to_activity must resolve to a canonical L3 Activity."""
    findings: list[Finding] = []
    rid = record.get("id", "<missing>")
    activity_id = record.get("belongs_to_activity", "")
    if not _ACTIVITY_ID_RE.match(str(activity_id)):
        findings.append(Finding(
            rule="TASK-004",
            record_id=rid,
            severity="error",
            message=f"Task `belongs_to_activity` {activity_id!r} does not match {ACTIVITY_ID_PATTERN!r}",
            path=path,
        ))
        return findings
    if not _activity_exists(str(activity_id), entities_dir=entities_dir):
        findings.append(Finding(
            rule="TASK-004",
            record_id=rid,
            severity="error",
            message=(
                f"Task `belongs_to_activity` {activity_id!r} does not resolve to a "
                f"canonical Activity record (CR-BP-93 §7: L4 has exactly one parent L3 Activity)"
            ),
            path=path,
        ))
    return findings


def _check_no_disallowed_fields(record: dict, path: str) -> list[Finding]:
    """TASK-005 — Disallowed at L4 (workflow / orchestration / execution)."""
    findings: list[Finding] = []
    rid = record.get("id", "<missing>")
    extras = sorted(set(record.keys()) & DISALLOWED_L4_FIELDS)
    for f in extras:
        findings.append(Finding(
            rule="TASK-005",
            record_id=rid,
            severity="error",
            message=(
                f"Task carries disallowed field `{f}`. Workflow / execution semantics "
                f"live downstream of L4 (CR-BP-93 §7 Disallowed; CR-BP-98 §13)."
            ),
            path=path,
        ))
    return findings


# -----------------------------------------------------------------------------
# Aggregate evaluate()
# -----------------------------------------------------------------------------


def evaluate(records: list[tuple[Path, dict]], entities_dir: Path = ENTITIES) -> list[Finding]:
    findings: list[Finding] = []
    for path, record in records:
        findings.extend(_check_id_format(record, str(path)))
        findings.extend(_check_definition_responsibility_boundary(record, str(path)))
        findings.extend(_check_trigger_outcome(record, str(path)))
        findings.extend(_check_activity_resolution(record, str(path), entities_dir=entities_dir))
        findings.extend(_check_no_disallowed_fields(record, str(path)))
    return findings


def verdict(findings: list[Finding]) -> str:
    """Return `CONFORMANT` (no findings) or `NON-CONFORMANT`."""
    return "CONFORMANT" if not findings else "NON-CONFORMANT"


# -----------------------------------------------------------------------------
# Self-test fixture
# -----------------------------------------------------------------------------


def _self_test_record() -> dict:
    """A self-test Task that should pass TASK-001..005."""
    return {
        "id": "dea:task-self-test",
        "type": "Task",
        "name": "Self Test Submission",
        "definition": "A bounded self-test fixture Task used by check_task_model.py.",
        "belongs_to_activity": "dea:activity-self-test",
        "trigger": "Self-test invocation",
        "outcome": "Self-test exit code 0",
        "responsibility": "Self-test framework",
        "boundary": {
            "inclusions": ["Validate the L4 Task validator's 5 rules"],
            "exclusions": ["Production L4 records"],
        },
        "evidence": [
            {
                "source": "CR-BP-98",
                "claim": "Task is bounded, actionable, single-responsibility",
                "strength": "E5",
            },
        ],
        "version": "1.0.0",
        "lifecycle_status": "candidate",
        "status": "candidate",
        "ecfConformance": {
            "framework": "EnterpriseConceptFramework",
            "contractVersion": "1.0.0",
            "profile": "dea:ecf@1.0.0",
            "status": "conformant",
            "affiliation": "inherits-catalog",
            "canonicalReferences": [
                {
                    "kind": "coordinate",
                    "domain": "PartyAndRelationship",
                    "stage": "Improve",
                    "identifier": "ecf:partyRelationship.improve",
                }
            ],
        },
        "metadata": {
            "established_by": "CR-BP-98",
            "established_at": "2026-09-18",
        },
    }


def _self_test() -> int:
    """In-process self-test; exit 0 on pass, 1 on fail."""
    import tempfile

    record = _self_test_record()
    activity_id = record["belongs_to_activity"]

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        activity_dir = tmp_path / activity_id
        activity_dir.mkdir()
        activity_yaml = activity_dir / f"{activity_id}.yaml"
        activity_yaml.write_text(yaml.safe_dump({
            "id": activity_id,
            "type": "Activity",
            "name": "Self Test Activity",
            "definition": "Self-test fixture Activity for check_task_model.py.",
            "version": "1.0.0",
            "lifecycle_status": "candidate",
            "status": "candidate",
        }))
        findings = evaluate([(Path("<self-test>"), record)], entities_dir=tmp_path)
    if findings:
        print("self-test FAIL:", file=sys.stderr)
        for f in findings:
            print(f"  X {f.rule} {f.record_id}: {f.message}", file=sys.stderr)
        return 1
    print("self-test PASS (TASK-001 id format; TASK-002 definition/responsibility/boundary; "
          "TASK-003 trigger/outcome; TASK-004 belongs_to_activity; TASK-005 no disallowed fields)")
    return 0


# -----------------------------------------------------------------------------
# Live catalog
# -----------------------------------------------------------------------------


def _live_findings() -> list[Finding]:
    records = list(_iter_task_records())
    return evaluate(records)


def _cli_live() -> int:
    findings = _live_findings()
    n = len(list(_iter_task_records()))
    print(f"Task validation (CR-BP-98 TASK-001..005): {verdict(findings)}")
    print(f"  Records checked:  {n}")
    print(f"  Findings:         {len(findings)}")
    for rule in RULE_IDS:
        n_rule = sum(1 for f in findings if f.rule == rule)
        if n_rule:
            print(f"    {rule}: {n_rule}")
    if findings:
        print("Findings:")
        for f in findings:
            print(f"  [{f.rule}] {f.record_id}: {f.message}")
    return 0 if verdict(findings) == "CONFORMANT" else 1


def _cli_json() -> int:
    records = list(_iter_task_records())
    findings = evaluate(records)
    payload = {
        "verdict": verdict(findings),
        "records_checked": len(records),
        "findings": [f.to_dict() for f in findings],
        "rules": [{"id": rid, "severity": "error", "description": _RULE_DESCRIPTION[rid]} for rid in RULE_IDS],
    }
    print(json.dumps(payload, indent=2))
    return 0 if verdict(findings) == "CONFORMANT" else 1


_RULE_DESCRIPTION = {
    "TASK-001": "Task id format `dea:task-*` (CR-BP-04 §4 id family)",
    "TASK-002": "Definition + Responsibility + Boundary are Required at L4 (CR-BP-93 §9)",
    "TASK-003": "Trigger + Outcome (Completion state) are Required at L4 (CR-BP-93 §9)",
    "TASK-004": "belongs_to_activity must resolve to a canonical L3 Activity (CR-BP-93 §7)",
    "TASK-005": "Task MUST NOT carry workflow / execution / orchestration semantics (CR-BP-93 §7)",
}


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="L4 Task structural validator (CR-BP-98)")
    parser.add_argument("--self-test", action="store_true", help="run in-process self-test")
    parser.add_argument("--json", action="store_true", help="emit JSON payload")
    args = parser.parse_args()
    if args.self_test:
        return _self_test()
    if args.json:
        return _cli_json()
    return _cli_live()


if __name__ == "__main__":
    sys.exit(main())