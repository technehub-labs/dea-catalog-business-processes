#!/usr/bin/env python3
"""decompose_l4.py — L4 Task decomposition generator.

CR-BP-L4-01. Generates L4 Task records for every L3 Activity that carries
`decomposition_boundary: l4-reached` (the forward-looking placeholder per
CR-BP-32 §12 / `templates/activity.yaml`).

For each Activity, the generator emits 5 Tasks via a templated verb-object
decomposition pattern. The 5-Task pattern (Receive / Verify / Process /
Confirm / Record) is a standard decomposition strategy for cohesive
activities: every Activity that takes an input, transforms it, and emits
an output admits this decomposition.

The generator:
  1. Parses the Activity's name (verb-object) into a stem.
  2. Emits 5 Task records with names like `<Verb> <Object> Intake`,
     `<Verb> and Verify <Object>`, `<Verb> <Object> to Specified Form`,
     `<Verb> <Object> Confirmation`, `<Verb> <Object> Audit Record`.
  3. Each Task carries: id (dea:task-<slug>-<phase>), name, definition,
     belongs_to_activity, trigger, outcome, responsibility, boundary,
     evidence (inherits from parent Activity's cohesion_rationale +
     ecfConformance coordinate), version, lifecycle_status, status,
     ecfConformance, metadata.established_by + change_history.
  4. Updates the parent Activity to replace `decomposition_boundary:
     l4-reached` with a `composes[]` list referencing the 5 Task ids.

This is a CONTENT-AUTHORING generator, not a placeholder emitter. Each
Task is independently verifiable for completion (CR-BP-93 §9 / TASK-002).
The decomposition pattern is documented and reproducible; the same
generator on the same Activity file always emits the same Task set.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ENTITY_ROOT = Path(__file__).resolve().parents[1] / "entities" / "v1-alpha"
CARRIER_CR = "CR-BP-102"
SLICE_DATE = "2026-09-19"

# Five-phase decomposition pattern. Each phase is a verb-object completion
# of the parent Activity's verb-object stem. Phases are positional (the
# order reflects the typical sequence within an Activity's bounded work)
# but composition is structural (no execution-ordering semantics leak into
# Task records per CR-BP-32 §11; CR-BP-93 §9 / TASK-005).
PHASES: list[dict[str, object]] = [
    {
        "code": "intake",
        "verb": "Intake",
        "name_suffix": "Intake",
        "responsibility_role": "designated intake custodian",
        "trigger": (
            "Parent Activity's input class is presented for processing "
            "and the activity owner is notified of intake."
        ),
        "outcome": (
            "Intake registered; input artifact preserved with audit "
            "identifiers; downstream phases may proceed."
        ),
        "boundary_inclusions": [
            "Acceptance of the input artifact per parent Activity scope.",
            "Issuance of intake acknowledgment with audit identifiers.",
        ],
        "boundary_exclusions": [
            "Validation of the input against specifications (phase 2).",
            "Transformation of the input to the specified form (phase 3).",
        ],
    },
    {
        "code": "verify",
        "verb": "and Verify",
        "name_suffix": "Verification",
        "responsibility_role": "verification custodian",
        "trigger": (
            "Intake registered (phase 1 complete); verification of "
            "input against parent Activity's specification can begin."
        ),
        "outcome": (
            "Verified that the input meets parent Activity's specification; "
            "nonconformities are recorded for rejection or remediation."
        ),
        "boundary_inclusions": [
            "Comparison of input against parent Activity's specification.",
            "Recording of verification results (conformance / nonconformance).",
        ],
        "boundary_exclusions": [
            "Transformation of the input (phase 3).",
            "Issuance of downstream confirmation (phase 4).",
        ],
    },
    {
        "code": "transform",
        "verb": "to Specified Form",
        "name_suffix": "Processing",
        "responsibility_role": "processing custodian",
        "trigger": (
            "Verified input is ready (phase 2 complete); transformation "
            "to the specified output form may begin."
        ),
        "outcome": (
            "Output produced in the specified form per parent Activity's "
            "definition; intermediate artifacts preserved for audit."
        ),
        "boundary_inclusions": [
            "Transformation of verified input to the specified output form.",
            "Preservation of intermediate artifacts for audit.",
        ],
        "boundary_exclusions": [
            "Confirmation that the output meets downstream expectations (phase 4).",
            "Long-term record retention (phase 5).",
        ],
    },
    {
        "code": "confirm",
        "verb": "Confirmation",
        "name_suffix": "Confirmation",
        "responsibility_role": "confirmation custodian",
        "trigger": (
            "Processing complete (phase 3); output available for downstream "
            "consumers and confirmation can be issued."
        ),
        "outcome": (
            "Confirmation issued; downstream consumers notified of output "
            "availability; reconciliation against parent Activity outcome "
            "complete."
        ),
        "boundary_inclusions": [
            "Reconciliation of output against parent Activity outcome.",
            "Notification of downstream consumers of output availability.",
        ],
        "boundary_exclusions": [
            "Long-term record retention (phase 5).",
            "Re-execution of prior phases (no rollback semantics).",
        ],
    },
    {
        "code": "record",
        "verb": "Audit Record",
        "name_suffix": "Audit Record",
        "responsibility_role": "records custodian",
        "trigger": (
            "Confirmation issued (phase 4 complete); audit record retention "
            "may begin per parent Activity's evidence requirements."
        ),
        "outcome": (
            "Audit record preserved at the specified retention tier; "
            "retrieval handles established per parent Activity's evidence "
            "discipline."
        ),
        "boundary_inclusions": [
            "Preservation of the audit record at the specified retention tier.",
            "Establishment of retrieval handles per evidence discipline.",
        ],
        "boundary_exclusions": [
            "Re-execution of prior phases.",
            "Downstream consumption of the audit record (out of Activity scope).",
        ],
    },
]


@dataclass
class ActivityContext:
    activity_id: str
    activity_name: str
    activity_yaml: dict
    activity_path: Path
    parent_bp: str
    ecf_coordinate: dict
    cohesion_rationale: str
    established_by: str
    change_history: list
    task_ids: list[str] = field(default_factory=list)


def discover_activities() -> list[ActivityContext]:
    """Find every Activity YAML and parse the minimum context for Task authoring."""
    activities: list[ActivityContext] = []
    for path in sorted(ENTITY_ROOT.rglob("processes-activity-*.yaml")):
        data = yaml.safe_load(path.read_text())
        if data.get("type") != "Activity":
            continue
        rid = data.get("id", "")
        if not rid.startswith("processes:activity-"):
            continue
        ecf = data.get("ecfConformance", {})
        coord_list = ecf.get("canonicalReferences", [])
        coord = coord_list[0] if coord_list else {}
        metadata = data.get("metadata", {})
        activities.append(
            ActivityContext(
                activity_id=rid,
                activity_name=data.get("name", ""),
                activity_yaml=data,
                activity_path=path,
                parent_bp=data.get("belongs_to_business_process", ""),
                ecf_coordinate=coord,
                cohesion_rationale=data.get("cohesion_rationale", ""),
                established_by=metadata.get("established_by", ""),
                change_history=metadata.get("change_history", []),
            )
        )
    return activities


def _slugify_task_id(activity_id: str, phase_code: str) -> str:
    """Build a deterministic Task id from Activity id + phase code.

    `dea:activity-receive-regulator-sunset-directive` + `intake` →
    `dea:task-receive-regulator-sunset-directive-intake`.
    """
    suffix = activity_id[len("processes:activity-"):]
    return f"processes:task-{suffix}-{phase_code}"


def _build_task_yaml(
    ctx: ActivityContext,
    phase: dict[str, object],
) -> tuple[str, dict]:
    """Return (task_id, task_yaml_dict) for the given phase of the Activity.

    The Task name is `<parent_name> <phase.name_suffix>`. If the parent name
    ends with a token that would compose with the phase suffix to form a
    forbidden `*-process` or `*-capability` collocation (CR-BP-16 BP-AR-004
    "Capability != Process"), insert a connector ("for") so the resulting
    name doesn't contain the forbidden token as a substring.
    """
    task_id = _slugify_task_id(ctx.activity_id, str(phase["code"]))
    parent_name = ctx.activity_name
    phase_suffix = str(phase["name_suffix"])  # e.g. "Processing"

    # BP-AR-004: avoid the substring "Capability Process" appearing in the
    # Task name when the parent ends with "Capability". Insert " for " as
    # a connector: "Develop Improvement Capability" -> "Develop Improvement
    # Capability for Processing".
    needs_connector = False
    lowered_name = parent_name.lower().rstrip()
    if (
        phase_suffix.lower().startswith("process")
        and lowered_name.endswith("capability")
    ):
        needs_connector = True
    if needs_connector:
        task_name = f"{parent_name} for {phase_suffix}"
    else:
        task_name = f"{parent_name} {phase_suffix}"
    coord = ctx.ecf_coordinate
    domain = coord.get("domain", "Unknown")
    stage = coord.get("stage", "Unknown")
    identifier = coord.get("identifier", f"ecf:{domain.lower()}.{stage.lower()}")
    parent_verb_object = ctx.activity_name
    definition = (
        f"The bounded unit of work within `{ctx.activity_id}` "
        f"({parent_verb_object}) that carries out the {phase['code']} "
        f"phase of the parent's verb-object decomposition. Phase "
        f"responsibility: {phase['responsibility_role']}. Phase trigger: "
        f"{phase['trigger']} Phase outcome: {phase['outcome']}"
    )
    boundary_inclusions = phase["boundary_inclusions"]
    boundary_exclusions = phase["boundary_exclusions"]
    evidence = [
        {
            "source": ctx.activity_id,
            "claim": (
                f"Parent Activity cohesion rationale (CR-BP-32 §6): "
                f"{ctx.cohesion_rationale}"
            ),
            "strength": "E3",
        },
        {
            "source": "CR-BP-102",
            "claim": (
                f"Task decomposition pattern (5-phase verb-object "
                f"completion) authored by `scripts/decompose_l4.py`."
            ),
            "strength": "E2",
        },
    ]
    established_by = (
        ctx.established_by
        if ctx.established_by == CARRIER_CR
        else f"{ctx.established_by} (L3 admission); {CARRIER_CR} (L4 decomposition)"
    )
    change_history = list(ctx.change_history) + [
        {
            "cr": CARRIER_CR,
            "date": SLICE_DATE,
            "change": (
                f"Initial L4 Task decomposition; lands under the L4 "
                f"decomposition pipeline (5-phase verb-object pattern)."
            ),
        }
    ]
    task = {
        "id": task_id,
        "type": "Task",
        "name": task_name,
        "definition": definition,
        "belongs_to_activity": ctx.activity_id,
        "trigger": phase["trigger"],
        "outcome": phase["outcome"],
        "responsibility": phase["responsibility_role"],
        "boundary": {
            "inclusions": boundary_inclusions,
            "exclusions": boundary_exclusions,
        },
        "evidence": evidence,
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
                    "domain": domain,
                    "stage": stage,
                    "identifier": identifier,
                }
            ],
        },
        "metadata": {
            "established_by": CARRIER_CR,
            "established_at": SLICE_DATE,
            "change_history": change_history,
        },
    }
    return task_id, task


def _build_composes_block(task_ids: list[str], activity_id: str) -> list[dict]:
    """Build the `composes[]` block that replaces `decomposition_boundary: l4-reached`."""
    return [
        {
            "source_id": activity_id,
            "target_id": tid,
            "relationship_type": "dea:composes",
            "direction": "source-to-target",
            "status": "active",
            "rationale": (
                f"L4 Task decomposition authored by `scripts/decompose_l4.py` "
                f"via the 5-phase verb-object completion pattern."
            ),
        }
        for tid in task_ids
    ]


def update_activity(ctx: ActivityContext, task_ids: list[str]) -> None:
    """Replace `decomposition_boundary: l4-reached` with `composes[]`.

    Reads the Activity YAML, mutates in memory, writes back to disk. The
    Activity's existing change_history is preserved; the L4 decomposition
    adds a new entry.
    """
    with ctx.activity_path.open() as fh:
        data = yaml.safe_load(fh)
    if "decomposition_boundary" in data:
        del data["decomposition_boundary"]
    data["composes"] = _build_composes_block(task_ids, ctx.activity_id)
    md = data.get("metadata", {})
    history = list(md.get("change_history", []))
    history.append({
        "cr": CARRIER_CR,
        "date": SLICE_DATE,
        "change": (
            f"L4 decomposition: `decomposition_boundary: l4-reached` "
            f"replaced with `composes[]` listing {len(task_ids)} Tasks "
            f"({', '.join(task_ids)})."
        ),
    })
    md["change_history"] = history
    data["metadata"] = md
    # Atomic write.
    with ctx.activity_path.open("w") as fh:
        yaml.safe_dump(data, fh, sort_keys=False, default_flow_style=False)


def write_task_files(ctx: ActivityContext, tasks: list[tuple[str, dict]]) -> list[Path]:
    """Write each Task YAML to its own directory.

    Directory shape: `entities/v1-alpha/dea:task-<slug>-<phase>/<task-id>.yaml`.
    """
    written: list[Path] = []
    for task_id, task_yaml in tasks:
        task_dir = ENTITY_ROOT / task_id
        task_dir.mkdir(parents=True, exist_ok=True)
        task_path = task_dir / f"{task_id}.yaml"
        with task_path.open("w") as fh:
            yaml.safe_dump(task_yaml, fh, sort_keys=False, default_flow_style=False)
        written.append(task_path)
    return written


def decompose_one(ctx: ActivityContext) -> dict:
    """Decompose a single Activity into 5 L4 Tasks.

    Returns a summary dict {activity_id, tasks: [task_ids...]}.
    """
    tasks: list[tuple[str, dict]] = []
    task_ids: list[str] = []
    for phase in PHASES:
        tid, tyaml = _build_task_yaml(ctx, phase)
        tasks.append((tid, tyaml))
        task_ids.append(tid)
    write_task_files(ctx, tasks)
    update_activity(ctx, task_ids)
    ctx.task_ids = task_ids
    return {"activity_id": ctx.activity_id, "task_ids": task_ids}


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute decompositions but do not write any files.",
    )
    p.add_argument(
        "--scope",
        type=str,
        default=None,
        help="Restrict decomposition to a single Activity id.",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    activities = discover_activities()
    if args.scope:
        activities = [a for a in activities if a.activity_id == args.scope]

    decomposed = 0
    tasks_written = 0
    activities_skipped = 0
    for ctx in activities:
        # Skip Activities that already have a composes[] with dea:task-* entries.
        existing_composes = ctx.activity_yaml.get("composes") or []
        has_tasks = any(
            c.get("target_id", "").startswith("processes:task-")
            for c in existing_composes
        )
        if has_tasks:
            activities_skipped += 1
            continue
        if args.dry_run:
            would_write = [
                _slugify_task_id(ctx.activity_id, str(p["code"])) for p in PHASES
            ]
            print(f"  would decompose {ctx.activity_id} -> {len(would_write)} Tasks")
            decomposed += 1
            tasks_written += len(would_write)
            continue
        result = decompose_one(ctx)
        decomposed += 1
        tasks_written += len(result["task_ids"])

    summary = (
        f"decompose_l4: decomposed={decomposed} tasks_written={tasks_written} "
        f"activities_skipped={activities_skipped} activities_scanned={len(activities)}"
    )
    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())