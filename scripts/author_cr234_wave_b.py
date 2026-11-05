#!/usr/bin/env python3
"""CR-BP-234 Wave B one-shot: apply the authored plain-language fields
to all 580 L3 Activity records.

The five CR-BP-230 fields (plain_language_name, plain_language_description,
business_purpose, practical_context, worked_example{agent_type, narrative})
are authored content grounded in each record's own documented fields (the
CR-BP-220/225 discipline: no invention; the record's own actors may be
referenced). This driver:

  1. loads the per-batch authored mappings (*/tmp/wave-b/<batch>.json*
     at authoring time; committed to `reconciliation/authoring/cr234-wave-b/`
     for the audit trail),
  2. mechanically re-validates every string against the CR-BP-232 HUM
     contracts (min lengths; the jargon denylist; MECE normalised
     containment against the record's own definition/description),
  3. appends the five fields at EOF with the CR-BP-225 comment-banner
     convention (raw-text surgery; fresh top-level blocks — these fields
     are absent from the records today),
  4. writes the execution manifest `reconciliation/closure/cr233-wave-a.json`.

Idempotent via the plain_language_name presence check (second run: 0
writes). Schema: CR-BP-230 already enabled the fields on all five schemas.

Usage:
  python3 scripts/author_cr234_wave_b.py [--dry-run]

Authoritative reference: CR-BP-234 (2026-11-05, eaojnr); CR-BP-230 S2.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTITIES = ROOT / "entities" / "v1-alpha"
AUTHORING_DIR = ROOT / "reconciliation" / "authoring" / "cr234-wave-b"
MANIFEST = ROOT / "reconciliation" / "closure" / "cr234-wave-b.json"

JARGON_DENYLIST: tuple[str, ...] = (
    "bounded unit of work", "verb-object", "verb object", "decomposition",
    "ecfconformance", "ecf", "lifecycle_status", "belongs_to",
    "belongs to activity", "processes:", "dea:", "cr-bp-", "mece",
    "yaml", "schema", "canonical id", "canonical identifier",
    "l0 ", "l1 ", "l2 ", "l3 ", "l4 ", "phase working object",
    "cell charter", "governance.provenance", "{{", "pending",
)

MIN = {"plain_language_name": 8, "plain_language_description": 40,
       "business_purpose": 30, "practical_context": 30}
AGENT_TYPES = {"human", "non-human", "mixed"}


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", text.lower())).strip()


def _l2_records() -> dict[str, Path]:
    """All 145 canonical L2 record paths keyed by id."""
    out: dict[str, Path] = {}
    for f in sorted(ENTITIES.rglob("processes-*.yaml")):
        pos = f.as_posix()
        if "/documentation/" in pos or "/examples/" in pos or "/research/" in pos:
            continue
        try:
            d = yaml.safe_load(f.read_text())
        except yaml.YAMLError:
            continue
        if isinstance(d, dict) and d.get("type") == "Activity" and d.get("id"):
            out[d["id"]] = f
    return out


def _validate(record: dict, authored: dict) -> list[str]:
    """Mechanical re-validation of one record's authored fields."""
    problems: list[str] = []
    for field, minimum in MIN.items():
        v = authored.get(field)
        if not isinstance(v, str) or len(v.strip()) < minimum:
            problems.append(f"{field}: missing or short (<{minimum})")
            continue
        low = v.lower()
        for token in JARGON_DENYLIST:
            # Word-boundary match for single-word tokens ("pending" must
            # not flag "depending"/"spending"); substring for phrases.
            if " " in token:
                hit = token in low
            else:
                hit = re.search(rf"\b{re.escape(token)}\b", low) is not None
            if hit:
                problems.append(f"{field}: denylist token {token!r}")
    we = authored.get("worked_example")
    if not isinstance(we, dict) or we.get("agent_type") not in AGENT_TYPES:
        problems.append("worked_example.agent_type: invalid")
    elif not isinstance(we.get("narrative"), str) or len(we["narrative"].strip()) < 40:
        problems.append("worked_example.narrative: missing or short")
    # MECE: the provided description must not restate the formal
    # definition/description as a normalised contiguous span.
    desc = authored.get("plain_language_description", "")
    for source_field in ("definition",):
        src = record.get(source_field)
        if isinstance(src, str) and src.strip():
            if _norm(src) and _norm(src) in _norm(desc):
                problems.append(
                    f"plain_language_description: restates {source_field} (MECE)")
    return problems


def _yaml_str(value: str) -> str:
    """Single-quote YAML scalar (CR-BP-225 _yq convention, no truncation)."""
    return "'" + value.strip().replace("'", "''") + "'"


def _banner() -> str:
    return (
        "# CR-BP-234 Wave B (2026-11-05): plain-language fields authored from the\n"
        "# activity's own + its child tasks' + its parent process's documented\n"
        "# content (CR-BP-230 S2; no invention; MECE against the formal definition).\n"
        "# Rendered in README Part I by the CR-BP-231 profile v3 generator."
    )


def _block(authored: dict) -> str:
    we = authored["worked_example"]
    lines = [_banner(), ""]
    lines.append(f"plain_language_name: {_yaml_str(authored['plain_language_name'])}")
    lines.append(
        f"plain_language_description: {_yaml_str(authored['plain_language_description'])}")
    lines.append(f"business_purpose: {_yaml_str(authored['business_purpose'])}")
    lines.append(f"practical_context: {_yaml_str(authored['practical_context'])}")
    lines.append("worked_example:")
    lines.append(f"  agent_type: {we['agent_type']}")
    lines.append(f"  narrative: {_yaml_str(we['narrative'])}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    records = _l2_records()
    authored: dict[str, dict] = {}
    for path in sorted(AUTHORING_DIR.glob("*.json")):
        authored.update(json.loads(path.read_text()))

    missing = sorted(set(records) - set(authored))
    extra = sorted(set(authored) - set(records))
    if missing:
        print(f"ERROR: {len(missing)} L2 records without authored content "
              f"(first 5: {missing[:5]})")
        return 2
    if extra:
        print(f"ERROR: {len(extra)} authored ids are not L2 records: {extra[:5]}")
        return 2

    written = 0
    rejected: dict[str, list[str]] = {}
    manifest_rows: list[dict] = []
    for rid, path in sorted(records.items()):
        record = yaml.safe_load(path.read_text())
        if record.get("plain_language_name"):
            continue  # idempotent
        problems = _validate(record, authored[rid])
        if problems:
            rejected[rid] = problems
            continue
        block = _block(authored[rid])
        if not args.dry_run:
            with path.open("a") as fh:
                fh.write("\n\n" + block + "\n")
        we = authored[rid]["worked_example"]
        manifest_rows.append({
            "id": rid,
            "file": str(path.relative_to(ROOT)),
            "agent_type": we["agent_type"],
            "name_chars": len(authored[rid]["plain_language_name"]),
            "description_chars": len(authored[rid]["plain_language_description"]),
        })
        written += 1

    if rejected:
        print(f"ERROR: {len(rejected)} records failed mechanical validation:")
        for rid, probs in list(rejected.items())[:10]:
            print(f"  {rid}: {probs}")
        return 3

    if not args.dry_run:
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        agent_types: dict[str, int] = {}
        for row in manifest_rows:
            agent_types[row["agent_type"]] = agent_types.get(row["agent_type"], 0) + 1
        MANIFEST.write_text(json.dumps({
            "cr": "CR-BP-233",
            "wave": "A (L2 Business Process plain-language authoring)",
            "records_authored": written,
            "agent_type_distribution": agent_types,
            "author_of_record": "Emmanuel A. Otchere",
            "records": manifest_rows,
        }, indent=2) + "\n")

    print(f"author_cr234_wave_b: written={written} "
          f"rejected={len(rejected)} total_l3={len(records)}"
          f"{' [dry-run]' if args.dry_run else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
