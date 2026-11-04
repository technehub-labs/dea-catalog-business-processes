#!/usr/bin/env python3
"""check_human_readability.py ; CR-BP-232 Human Readability Gate (HUM-001..007).

CR-BP-230/CR-BP-232 two-layer documentation programme. The three
documentation quality dimensions are independently assessable
(never collapsed into one documentation-completeness score):

  - Semantic quality   -> owned by the existing gates (BP-SEM, ECF,
                          BP-SPEC, architectural regression). NOT here.
  - Human comprehension -> HUM-001..005 + HUM-007 (this gate).
  - Operational clarity -> HUM-006 (this gate).

Rules (evaluated against each canonical record's CR-BP-230
plain-language fields):

  HUM-001  `plain_language_name` present, 8..200 chars.
  HUM-002  `plain_language_description` present, >= 40 chars.
  HUM-003  `business_purpose` present, >= 30 chars.
  HUM-004  `practical_context` present, >= 30 chars.
  HUM-005  Metamodel-jargon denylist: the provided prose fields must
           not carry metamodel/construction vocabulary ("bounded unit
           of work", "verb-object", "decomposition", canonical-id
           tokens, level codes, "pending", ...). The human layer speaks
           business, not metamodel.
  HUM-006  Operational clarity: `worked_example` carries a valid
           `agent_type` (human | non-human | mixed) and a narrative
           of >= 40 chars.
  HUM-007  MECE: `plain_language_description` MUST NOT restate the
           formal `definition` verbatim (normalised containment).

All findings are ADVISORY until the wave closure flip (CR-BP-236,
mirroring the CR-BP-CE-RL posture precedent): `--strict` fails on any
finding. Presence findings vanish as the CR-BP-233..236 waves backfill
the catalog; the denylist/MECE/agent-type rules are permanent quality
gates over the provided layer.

Writes reconciliation/human-readability-report.yaml (the audit
artefact; CE-900 pattern).

Usage::

    python3 scripts/check_human_readability.py [--strict] [--json]
                                               [--self-test]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
ENTITIES_ROOT = REPO_ROOT / "entities" / "v1-alpha"

# Min lengths (chars). Deliberately modest: the gate catches stubs and
# empty slots, not prose style.
MIN_NAME = 8
MIN_DESCRIPTION = 40
MIN_PURPOSE = 30
MIN_CONTEXT = 30
MIN_NARRATIVE = 40

PROSE_FIELDS = (
    "plain_language_name",
    "plain_language_description",
    "business_purpose",
    "practical_context",
)

# CR-BP-232 HUM-005: the human layer speaks business, not metamodel.
# Case-insensitive substring denylist over the provided prose fields.
JARGON_DENYLIST: tuple[str, ...] = (
    "bounded unit of work",
    "verb-object",
    "verb object",
    "decomposition",
    "ecfconformance",
    "ecf",
    "lifecycle_status",
    "belongs_to",
    "belongs to activity",
    "processes:",
    "dea:",
    "cr-bp-",
    "mece",
    "yaml",
    "schema",
    "canonical id",
    "canonical identifier",
    "l0 ", "l1 ", "l2 ", "l3 ", "l4 ",
    "phase working object",
    "cell charter",
    "governance.provenance",
    "{{",
)

AGENT_TYPES = {"human", "non-human", "mixed"}


def _normalize(text: str) -> str:
    """Lowercase, collapse whitespace, strip punctuation for the
    MECE restatement comparison (HUM-007)."""
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", text.lower())).strip()


def _resolve_level(record: dict) -> str | None:
    rtype = record.get("type")
    if rtype == "ProcessContext":
        return "L0"
    if rtype == "ProcessGroup":
        return "L1"
    if rtype == "Process":
        return "L2"
    if rtype == "Activity":
        return "L3"
    if rtype == "Task":
        return "L4"
    rid = record.get("id") or ""
    if isinstance(rid, str) and rid.startswith("processes:pc-"):
        return "L0"
    return None


def resolve_record_paths() -> list[Path]:
    paths: list[Path] = []
    if ENTITIES_ROOT.exists():
        for f in sorted(ENTITIES_ROOT.rglob("processes-*.yaml")):
            pos = f.as_posix()
            if "/documentation/" in pos or "/examples/" in pos or "/research/" in pos:
                continue
            paths.append(f)
    return paths


def check_record(record: dict) -> list[dict]:
    """Return findings for one record. Each finding:
    {"rule", "record_id", "level", "diagnostic"}."""
    findings: list[dict] = []
    rid = record.get("id", "?")
    level = _resolve_level(record) or "?"

    # HUM-001..004: presence + length of the four prose fields.
    minimums = {
        "plain_language_name": MIN_NAME,
        "plain_language_description": MIN_DESCRIPTION,
        "business_purpose": MIN_PURPOSE,
        "practical_context": MIN_CONTEXT,
    }
    for field, minimum in minimums.items():
        rule = {
            "plain_language_name": "HUM-001",
            "plain_language_description": "HUM-002",
            "business_purpose": "HUM-003",
            "practical_context": "HUM-004",
        }[field]
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            findings.append({
                "rule": rule,
                "record_id": rid,
                "level": level,
                "diagnostic": f"`{field}` not authored",
            })
        elif len(value.strip()) < minimum:
            findings.append({
                "rule": rule,
                "record_id": rid,
                "level": level,
                "diagnostic": f"`{field}` too short ({len(value.strip())} < {minimum} chars)",
            })

    # HUM-005: jargon denylist over authored prose only.
    for field in PROSE_FIELDS:
        value = record.get(field)
        if not isinstance(value, str) or not value.strip():
            continue
        lowered = value.lower()
        for token in JARGON_DENYLIST:
            if token in lowered:
                findings.append({
                    "rule": "HUM-005",
                    "record_id": rid,
                    "level": level,
                    "diagnostic": f"`{field}` carries metamodel jargon token {token!r}",
                })

    # HUM-006: worked example operational clarity.
    we = record.get("worked_example")
    if not isinstance(we, dict) or not we:
        findings.append({
            "rule": "HUM-006",
            "record_id": rid,
            "level": level,
            "diagnostic": "`worked_example` not authored",
        })
    else:
        agent_type = we.get("agent_type")
        narrative = we.get("narrative")
        if agent_type not in AGENT_TYPES:
            findings.append({
                "rule": "HUM-006",
                "record_id": rid,
                "level": level,
                "diagnostic": f"`worked_example.agent_type` invalid ({agent_type!r}; "
                              f"expected one of {sorted(AGENT_TYPES)})",
            })
        if not isinstance(narrative, str) or len(narrative.strip()) < MIN_NARRATIVE:
            findings.append({
                "rule": "HUM-006",
                "record_id": rid,
                "level": level,
                "diagnostic": "`worked_example.narrative` missing or too short",
            })

    # HUM-007: MECE — the provided description must not restate the
    # formal definition.
    desc = record.get("plain_language_description")
    definition = record.get("definition") or record.get("description")
    if isinstance(desc, str) and isinstance(definition, str) and desc.strip() and definition.strip():
        d_norm = _normalize(desc)
        f_norm = _normalize(definition)
        if d_norm and f_norm and (d_norm == f_norm or f_norm in d_norm):
            findings.append({
                "rule": "HUM-007",
                "record_id": rid,
                "level": level,
                "diagnostic": "`plain_language_description` restates the formal "
                              "definition verbatim (MECE violation, CR-BP-230 S1)",
            })

    return findings


def evaluate() -> list[dict]:
    findings: list[dict] = []
    for path in resolve_record_paths():
        try:
            record = yaml.safe_load(path.read_text())
        except (yaml.YAMLError, OSError):
            continue
        if not isinstance(record, dict) or not record.get("id"):
            continue
        findings.extend(check_record(record))
    return findings


def _write_report(findings: list[dict]) -> Path:
    by_rule: dict[str, int] = {}
    by_level: dict[str, int] = {}
    for f in findings:
        by_rule[f["rule"]] = by_rule.get(f["rule"], 0) + 1
        by_level[f["level"]] = by_level.get(f["level"], 0) + 1
    records = len(list(resolve_record_paths()))
    # YAML report (human audit artefact).
    out = REPO_ROOT / "reconciliation" / "human-readability-report.yaml"
    doc = {
        "gate": "HUM-001..007 (CR-BP-232)",
        "records_checked": records,
        "findings_total": len(findings),
        "findings_by_rule": by_rule,
        "findings_by_level": by_level,
        "posture": "advisory (blocks under --strict; flips blocking at wave "
                   "closure CR-BP-236, CR-BP-CE-RL precedent)",
        "findings": findings[:2000],
        "truncated": max(0, len(findings) - 2000),
    }
    out.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))
    # JSON manifest in the house `summary.total_findings` shape consumed
    # by the EXT-23 posture engine's _open_findings (REQ-23-03 promotion
    # criteria). Every HUM finding is advisory until the wave-closure
    # flip, so advisory_findings == total_findings by construction.
    import json as _json
    out_json = REPO_ROOT / "reconciliation" / "human-readability-report.json"
    out_json.write_text(_json.dumps({
        "gate": "HUM-001..007 (CR-BP-232)",
        "records_checked": records,
        "summary": {
            "total_findings": len(findings),
            "advisory_findings": len(findings),
        },
        "findings_by_rule": by_rule,
        "findings_by_level": by_level,
    }, indent=2))
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--strict", action="store_true",
                        help="Advisory findings also fail the gate "
                             "(wave-closure posture; CR-BP-236).")
    parser.add_argument("--json", action="store_true", help="JSON output.")
    parser.add_argument("--self-test", action="store_true",
                        help="Run fixture-based self-test and exit.")
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    findings = evaluate()
    _write_report(findings)

    verdict = "CONFORMANT" if not findings else (
        "NON-CONFORMANT" if args.strict else "CONFORMANT-WITH-WARNINGS")
    if args.json:
        print(json.dumps({
            "gate": "HUM-001..007",
            "verdict": verdict,
            "findings_total": len(findings),
            "findings": findings[:200],
        }, indent=2))
    else:
        print(f"Human Readability (CR-BP-232; HUM-001..007): {verdict}")
        by_rule: dict[str, int] = {}
        for f in findings:
            by_rule[f["rule"]] = by_rule.get(f["rule"], 0) + 1
        print(f"  {len(findings)} finding(s) "
              f"(by rule: {dict(sorted(by_rule.items()))})")
        for f in findings[:10]:
            print(f"    [{f['rule']}] {f['record_id']}: {f['diagnostic']}")
        if len(findings) > 10:
            print(f"    ... and {len(findings) - 10} more")

    if args.strict and findings:
        return 1
    return 0


def _self_test() -> int:
    """Fixture-based self-test; returns 0 on PASS."""
    failures: list[str] = []

    good = {
        "id": "processes:task-test-good",
        "type": "Task",
        "name": "Notify the Duty Supervisor",
        "definition": "The bounded unit of work that notifies the duty "
                      "supervisor of the confirmed schedule.",
        "plain_language_name": "Tell the duty supervisor",
        "plain_language_description": (
            "Once the schedule is confirmed, someone tells the duty "
            "supervisor so the shift team knows the plan for the day."),
        "business_purpose": (
            "Keeps the shift team informed so handovers never rely on "
            "word of mouth."),
        "practical_context": (
            "Happens at the end of every scheduling cycle, before the "
            "supervisor signs off the roster."),
        "worked_example": {
            "agent_type": "human",
            "narrative": (
                "A roster clerk opens the confirmed schedule, picks up "
                "the phone and walks the duty supervisor through the "
                "overnight changes."),
        },
    }
    f = check_record(good)
    if f:
        failures.append(f"good fixture fired: {[x['rule'] for x in f]}")

    # Missing fields -> HUM-001..004 + HUM-006.
    bare = {"id": "processes:task-test-bare", "type": "Task"}
    rules = {x["rule"] for x in check_record(bare)}
    for expected in ("HUM-001", "HUM-002", "HUM-003", "HUM-004", "HUM-006"):
        if expected not in rules:
            failures.append(f"bare fixture: expected {expected}")

    # Jargon -> HUM-005.
    jargon = dict(good)
    jargon["id"] = "processes:task-test-jargon"
    jargon["plain_language_description"] = (
        "This task is the bounded unit of work within the verb-object "
        "decomposition of the parent activity.")
    if "HUM-005" not in {x["rule"] for x in check_record(jargon)}:
        failures.append("jargon fixture: HUM-005 did not fire")

    # Verbatim restatement -> HUM-007.
    restating = dict(good)
    restating["id"] = "processes:task-test-restating"
    restating["plain_language_description"] = good["definition"]
    if "HUM-007" not in {x["rule"] for x in check_record(restating)}:
        failures.append("restatement fixture: HUM-007 did not fire")

    # Bad agent_type -> HUM-006.
    bad_agent = dict(good)
    bad_agent["id"] = "processes:task-test-badagent"
    bad_agent["worked_example"] = {"agent_type": "robot", "narrative": "x" * 50}
    if "HUM-006" not in {x["rule"] for x in check_record(bad_agent)}:
        failures.append("bad-agent fixture: HUM-006 did not fire")

    # L0 fallback level resolution.
    if _resolve_level({"id": "processes:pc-fa-retire-64q5p9"}) != "L0":
        failures.append("L0 id-pattern resolution broken")

    if failures:
        print("self-test FAIL:")
        for f_ in failures:
            print(f"  - {f_}")
        return 1
    print("self-test PASS: 6 cases (good record, bare record, jargon, "
          "MECE restatement, bad agent type, L0 resolution)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
