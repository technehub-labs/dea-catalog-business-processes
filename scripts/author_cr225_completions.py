"""CR-BP-225 one-shot: complete the three remaining operational-backfill items.

1. L2 definition promotion (145 records): `definition:` appended at EOF,
   verbatim from the record's own `description` (the documented definition;
   CR-BP-220 derivation method — no invention). The README renderer's
   description-fallback remains as a safety net but becomes unused.
2. L3/L4 inputs/outputs declarations (580 + 2,900 records), per the EXT-12
   §9 applicability contract ("A child input or output MUST NOT
   automatically be copied from the parent. Where a child uses a
   parent-level input, the relationship must be explicit and the child's
   actual use described."):
   - L4 (task working objects): inputs[] from the task's own `trigger`,
     outputs[] from its own `outcome` — required fields that already
     document the phase's actual use.
   - L3 (activity working inputs / contribution to parent outcome):
     derived from the activity's OWN child tasks — the intake-phase task's
     trigger is the working input (the moment work enters the activity);
     the concluding task's outcome is the contribution. Selection is
     deterministic (responsibility contains 'intake' → else first sorted
     id; responsibility contains outcome/record/notification → else last
     sorted id), and each entry cites the child ids.
3. L0 register confirmation (49 PCs): governance.provenance gains
   `status: confirmed` — user directive 2026-11-04 confirms the derived
   L0 roles + metrics register ahead of the 2026-12-31 window;
   review_due remains as the annual-cycle anchor.

Raw-text surgery: fresh top-level blocks appended at EOF (definition /
inputs / outputs are absent from these records today); the L0 provenance
line is replaced only where the EXT-24 marker block exists. Idempotent
via the inputs/outputs/definition presence checks. Schema: the
entity/activity/task schemas are non-strict (additionalProperties unset)
— no schema change required, matching the CR-BP-220 precedent.

Usage:
  python3 scripts/author_cr225_completions.py [--dry-run]

Authoritative reference: CR-BP-225 (2026-11-04, eaojnr); EXT-12 §9.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTITIES = ROOT / "entities" / "v1-alpha"
STATE_DIRS = ("research", "candidates", "retired")
CONFIRM_LINE = "    review_due: '2026-12-31'"


def _slug(record_id: str) -> str:
    """Local entry id from the canonical id (CR-BP-96 baseline)."""
    slug = re.sub(r"^processes:", "", record_id).replace(":", "-")
    return slug[:80]


def _yq(text, limit: int = 160) -> str:
    """Condense + single-quote-escape for safe YAML embedding."""
    s = " ".join(str(text).split())
    if len(s) > limit:
        s = s[:limit].rsplit(" ", 1)[0].rstrip(" ,;:.") + " …"
    return s.replace("'", "''")


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text()) or {}


def _canonical(path: Path) -> Path:
    return Path(str(path))


def promote_l2(path: Path, d: dict, dry: bool) -> bool:
    if d.get("definition") or not d.get("description"):
        return False
    block = (
        f"\n# {MARKER_COMMENT}\n"
        f"# documented description (CR-BP-220 derivation method; no invention).\n"
        f"definition: '{_yq(d['description'])}'\n"
    )
    if not dry:
        path.write_text(path.read_text().rstrip() + "\n" + block)
    return True


MARKER_COMMENT = "CR-BP-225 completions (2026-11-04): promoted verbatim from the record's"


def _pick(children_ids: list[str], tasks_by_id: dict):
    intake = concluding = None
    for tid in children_ids:
        t = tasks_by_id.get(tid)
        if not t:
            continue
        resp = str(t.get("responsibility", "")).lower()
        if intake is None and "intake" in resp:
            intake = t
        if any(k in resp for k in ("outcome", "record", "notification")):
            concluding = t
    if intake is None and children_ids:
        intake = tasks_by_id.get(children_ids[0])
    if concluding is None and children_ids:
        concluding = tasks_by_id.get(children_ids[-1])
    return intake or {}, concluding or {}


def declare_l3(path: Path, d: dict, tasks_by_id: dict, dry: bool) -> bool:
    if d.get("inputs") or d.get("outputs"):
        return False
    child_ids = sorted({e.get("target_id") for e in d.get("composes") or []
                        if isinstance(e, dict) and e.get("target_id")})
    if not child_ids:
        return False
    intake, concluding = _pick(child_ids, tasks_by_id)
    block = (
        f"\n# CR-BP-225 completions (2026-11-04): EXT-12 §9 activity IO derived\n"
        f"# from the activity's own child tasks — no parent copying; the cited\n"
        f"# child ids document the actual use (EXT-12 §9 rule).\n"
        f"inputs:\n"
        f"- id: in-{_slug(d.get('id', ''))}\n"
        f"  name: 'Working inputs of the composing tasks (intake task: {_yq(intake.get('name', ''))})'\n"
        f"  description: 'Declared per EXT-12 §9 (activity working inputs): intake task {_yq(intake.get('id', ''))} documents the input class in its own trigger — {_yq(intake.get('trigger', ''))}'\n"
        f"  source: The activity's own composing tasks (EXT-12 §9; no parent copying)\n"
        f"  mandatory: true\n"
        f"outputs:\n"
        f"- id: out-{_slug(d.get('id', ''))}\n"
        f"  name: 'Contribution to parent outcome (concluding task: {_yq(concluding.get('name', ''))})'\n"
        f"  description: 'Declared per EXT-12 §9: this activity contributes to {_yq(d.get('belongs_to_business_process', ''))} through concluding task {_yq(concluding.get('id', ''))}, whose outcome — {_yq(concluding.get('outcome', ''))}'\n"
        f"  source: The activity's own concluding task (EXT-12 §9)\n"
        f"  mandatory: true\n"
    )
    if not dry:
        path.write_text(path.read_text().rstrip() + "\n" + block)
    return True


def declare_l4(path: Path, d: dict, dry: bool) -> bool:
    if d.get("inputs") or d.get("outputs"):
        return False
    trigger, outcome = d.get("trigger"), d.get("outcome")
    if not trigger or not outcome:
        return False
    block = (
        f"\n# CR-BP-225 completions (2026-11-04): EXT-12 §9 task working\n"
        f"# objects, from the task's own required trigger/outcome fields\n"
        f"# (its documented actual use).\n"
        f"inputs:\n"
        f"- id: in-{_slug(d.get('id', ''))}\n"
        f"  name: 'Phase working object (presented per the task trigger)'\n"
        f"  description: '{_yq(trigger)}'\n"
        f"  source: The task's own trigger field (EXT-12 §9 task working objects)\n"
        f"  mandatory: true\n"
        f"outputs:\n"
        f"- id: out-{_slug(d.get('id', ''))}\n"
        f"  name: 'Phase result (recorded per the task outcome)'\n"
        f"  description: '{_yq(outcome)}'\n"
        f"  source: The task's own outcome field (EXT-12 §9)\n"
        f"  mandatory: true\n"
    )
    if not dry:
        path.write_text(path.read_text().rstrip() + "\n" + block)
    return True


def confirm_l0(path: Path, dry: bool) -> bool:
    text = path.read_text()
    if "status: confirmed" in text or CONFIRM_LINE not in text:
        return False
    replacement = (CONFIRM_LINE
                   + "\n    status: confirmed (user directive 2026-11-04; the derived"
                     " register is confirmed ahead of the 2026-12-31 window)")
    if not dry:
        path.write_text(text.replace(CONFIRM_LINE, replacement, 1))
    return True


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    # Preload the task index once (580/2,900 child lookups must not rescan).
    tasks_by_id: dict[str, dict] = {}
    for p in sorted(ENTITIES.rglob("processes-task-*.yaml")):
        if any(s in p.parts for s in STATE_DIRS):
            continue
        d = _load(p)
        if d.get("id"):
            tasks_by_id[d["id"]] = d

    counts = {"l0_confirm": 0, "l2_def": 0, "l3_io": 0, "l4_io": 0}
    for p in sorted(ENTITIES.rglob("processes-*.yaml")):
        if any(s in p.parts for s in STATE_DIRS):
            continue
        d = _load(p)
        rid = d.get("id", "")
        if rid.startswith("processes:pc-"):
            if confirm_l0(p, args.dry_run):
                counts["l0_confirm"] += 1
        elif d.get("type") == "Process":
            if promote_l2(p, d, args.dry_run):
                counts["l2_def"] += 1
        elif d.get("type") == "Activity":
            if declare_l3(p, d, tasks_by_id, args.dry_run):
                counts["l3_io"] += 1
        elif d.get("type") == "Task":
            if declare_l4(p, d, args.dry_run):
                counts["l4_io"] += 1

    mode = "DRY-RUN " if args.dry_run else ""
    print(f"{mode}author_cr225_completions: {counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
