#!/usr/bin/env python3
"""generate_readmes.py — EXT-02 README generator.

CR-BP-94-EXT-02. Generates README.md for every canonical record under
entities/v1-alpha/ that does not already have one. Each generated
README follows the documentation profile required by the record's
(type, level) combination as registered in scripts/check_documentation_profile.py
PROFILE_REGISTRY.

Sections (per EXPECTED_HEADINGS in check_documentation_profile.py):
  1. Entity Identity
  2. Formal Definition
  3. Canonical Semantic Dimensions
  4. Decomposition
  5. Behavior
  6. Inputs, Outputs, Interfaces
  7. Roles, Responsibilities
  8. Business Rules, Controls
  9. Outcomes (conditional; absent at L0/L1 per PROFILE_REGISTRY)
  10. Evidence
  11. Documentation Completeness
  12. Revision History

Content is drawn from each record's YAML fields. Sections that have no
data in the source record are populated with a deterministic placeholder
that the validator accepts (DOC-002 only checks section presence, not
section content). Placeholders are flagged as DOC-004 informational so
authors know what to fill in.

Usage:
  python3 scripts/generate_readmes.py [--dry-run] [--scope path]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Iterable

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
ENTITIES_ROOT = REPO_ROOT / "entities" / "v1-alpha"
CONTEXTS_ROOT = REPO_ROOT / "contexts" / "v1-alpha"


# Required section ids per (type, level) profile. Mirrors
# PROFILE_REGISTRY in scripts/check_documentation_profile.py.
PROFILE_SECTIONS: dict[tuple[str, str], list[str]] = {
    ("ProcessContext", "L0"): [
        "entity-identity", "formal-definition", "semantic-dimensions",
        "decomposition", "behavior", "interfaces", "roles",
        "rules-controls", "evidence", "completeness", "revision-history",
    ],
    ("ProcessGroup", "L1"): [
        "entity-identity", "formal-definition", "semantic-dimensions",
        "decomposition", "behavior", "interfaces", "roles",
        "rules-controls", "evidence", "completeness", "revision-history",
    ],
    ("Process", "L2"): [
        "entity-identity", "formal-definition", "semantic-dimensions",
        "decomposition", "behavior", "interfaces", "roles",
        "rules-controls", "outcomes", "evidence", "completeness",
        "revision-history",
    ],
    ("Activity", "L3"): [
        "entity-identity", "formal-definition", "semantic-dimensions",
        "decomposition", "behavior", "interfaces", "roles",
        "rules-controls", "outcomes", "evidence", "completeness",
        "revision-history",
    ],
    ("Task", "L4"): [
        "entity-identity", "formal-definition", "semantic-dimensions",
        "decomposition", "behavior", "interfaces", "roles",
        "rules-controls", "outcomes", "evidence", "completeness",
        "revision-history",
    ],
}


# Section id -> markdown heading (matches EXPECTED_HEADINGS regex).
SECTION_HEADINGS: dict[str, str] = {
    "entity-identity": "## 1. Entity Identity",
    "formal-definition": "## 2. Formal Definition",
    "semantic-dimensions": "## 3. Canonical Semantic Dimensions",
    "decomposition": "## 4. Decomposition",
    "behavior": "## 5. Behavior",
    "interfaces": "## 6. Inputs, Outputs, Interfaces",
    "roles": "## 7. Roles, Responsibilities",
    "rules-controls": "## 8. Business Rules, Controls",
    "outcomes": "## 9. Outcomes",
    "evidence": "## 10. Evidence",
    "completeness": "## 11. Documentation Completeness",
    "revision-history": "## 12. Revision History",
}


def resolve_level(record: dict) -> str | None:
    """Resolve the L0..L4 level from a record's type + structural cues.

    L0 ProcessContext is the only record type that doesn't carry an
    explicit `type` discriminator; it's identified by the id pattern
    `dea:pc-*` (CR-BP-02 §3 convention).
    """
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
    # L0 fallback: id-pattern discrimination.
    rid = record.get("id") or ""
    if isinstance(rid, str) and rid.startswith("dea:pc-"):
        return "L0"
    return None


def resolve_record_paths() -> list[Path]:
    """Walk entities/v1-alpha/ and contexts/v1-alpha/ for canonical records.

    Two storage shapes:
      1. L2 BP / L1 PG / L3 Activity / L4 Task live in a directory
         of the form `entities/v1-alpha/<record-id>/<record-id>.yaml`
         with README.md as a sibling.
      2. L0 ProcessContext lives as a flat YAML file at
         `contexts/v1-alpha/<record-id>.yaml` (no surrounding
         directory). README.md is placed in a sibling directory of
         the same name to keep DOC-001 path conventions consistent.

    Skips documentation/, examples/, research/ subdirectories
    (those are not canonical records).
    """
    paths: list[Path] = []
    # Entities: directory-per-record shape (L1/L2/L3/L4).
    if ENTITIES_ROOT.exists():
        for child in sorted(ENTITIES_ROOT.iterdir()):
            if not child.is_dir():
                continue
            yamls = [
                p for p in child.glob("*.yaml")
                if not any(part in p.parts for part in ("documentation", "examples", "research"))
            ]
            if yamls:
                paths.append(yamls[0])
    # Contexts: flat-file shape (L0 ProcessContext only).
    if CONTEXTS_ROOT.exists():
        for yaml_file in sorted(CONTEXTS_ROOT.glob("dea-pc-*.yaml")):
            paths.append(yaml_file)
    return paths


def load_record(path: Path) -> dict | None:
    try:
        with path.open() as fh:
            data = yaml.safe_load(fh)
    except (yaml.YAMLError, OSError):
        return None
    if not isinstance(data, dict) or not data.get("id"):
        return None
    return data


def resolve_readme_path(record_yaml_path: Path, record_id: str) -> Path:
    """Return the canonical README.md path for a record.

    Two shapes, per resolve_record_paths():
      1. L1/L2/L3/L4 directory-per-record: sibling of the YAML.
      2. L0 ProcessContext flat-file: synthesise a sibling directory
         named after the YAML stem (e.g. dea-pc-sd-retire/) and place
         README.md inside it. Keeps DOC-001's
         `entities/v1-alpha/<entity-id>/README.md` convention.
    """
    parent = record_yaml_path.parent
    # Flat-file L0: parent is `contexts/v1-alpha`.
    if parent.name == "v1-alpha" and record_yaml_path.name.startswith("dea-pc-"):
        return parent / record_yaml_path.stem / "README.md"
    # Directory-per-record: README is a sibling of the YAML.
    return parent / "README.md"


def render_section(
    section_id: str,
    record: dict,
    level: str,
) -> str:
    """Render one section's content deterministically from record fields."""
    rid = record.get("id", "unknown")
    rtype = record.get("type", "Record")
    name = record.get("name", "(unnamed)")
    version = record.get("version", "1.0.0")

    if section_id == "entity-identity":
        lines = [
            f"- **Canonical id**: `{rid}`",
            f"- **Name**: {name}",
            f"- **Type**: {rtype}",
            f"- **Level**: {level}",
            f"- **Version**: {version}",
            f"- **Lifecycle status**: {record.get('lifecycle_status', 'candidate')}",
        ]
        if record.get("belongs_to_business_process"):
            lines.append(
                f"- **Belongs to Business Process**: "
                f"`{record['belongs_to_business_process']}`"
            )
        return "\n".join(lines)

    if section_id == "formal-definition":
        definition = (
            record.get("definition")
            or record.get("description")
            or record.get("process_intent")
            or "(definition pending; backfill at EXT-04)"
        )
        return f"{definition}"

    if section_id == "semantic-dimensions":
        # ProcessGroup-specific: kind. Process-specific: identity.{verb,object}.
        dims: list[str] = []
        identity = record.get("identity") or {}
        if isinstance(identity, dict):
            for k in ("verb", "object", "scope"):
                if identity.get(k):
                    dims.append(f"- **{k.title()}**: {identity[k]}")
        kind = record.get("kind")
        if kind:
            dims.append(f"- **Kind**: {kind}")
        ecf = record.get("ecfConformance") or {}
        canonical_refs = ecf.get("canonicalReferences") or []
        for ref in canonical_refs:
            if isinstance(ref, dict):
                coord = " x ".join(
                    str(ref.get(k)) for k in ("domain", "stage") if ref.get(k)
                )
                if coord:
                    dims.append(f"- **ECF coordinate**: {coord}")
                    break
        return "\n".join(dims) if dims else "(ontological + teleological dimensions to be filled at EXT-04)"

    if section_id == "decomposition":
        # For BP: part_of + activity_references. For Activity: cohesion_rationale. For PC: ecf cell.
        parts: list[str] = []
        part_of = record.get("part_of")
        if part_of:
            if isinstance(part_of, list):
                parts.append("- **Part of (L1 Process Group)**:")
                for p in part_of:
                    parts.append(f"  - `{p}`")
            else:
                parts.append(f"- **Part of (L1 Process Group)**: `{part_of}`")
        act_refs = (record.get("metadata") or {}).get("activity_references") or []
        if act_refs:
            parts.append("- **Composes (L3 Activities)**:")
            for a in act_refs:
                parts.append(f"  - `{a}`")
        # PC-specific: ECF cell + adjacent cells
        if rtype == "ProcessContext":
            ctx = record.get("cell") or {}
            if ctx:
                parts.append(
                    f"- **ECF cell**: "
                    f"{ctx.get('domain', '?')} x {ctx.get('stage', '?')}"
                )
        cohesion = record.get("cohesion_rationale")
        if cohesion:
            parts.append(f"- **Cohesion rationale**: {cohesion}")
        return "\n".join(parts) if parts else "(decomposition relationships pending)"

    if section_id == "behavior":
        # Trigger / outcome for BP. decomposition_boundary marker.
        lines: list[str] = []
        if record.get("trigger"):
            lines.append(f"- **Trigger**: {record['trigger']}")
        if record.get("outcome"):
            lines.append(f"- **Outcome**: {record['outcome']}")
        if record.get("decomposition_boundary"):
            lines.append(
                f"- **Decomposition boundary**: `{record['decomposition_boundary']}`"
            )
        # PC cell charter
        charter = record.get("cell_charter")
        if charter:
            lines.append(f"- **Cell charter**: {charter}")
        # Activity resource dedication
        resource = record.get("resource_dedication")
        if resource:
            lines.append(f"- **Resource dedication**: {resource}")
        return "\n".join(lines) if lines else "(behavior description to be authored at EXT-04)"

    if section_id == "interfaces":
        # For BP: process_scope.includes / excludes. For others: cross-references.
        scope = record.get("process_scope") or {}
        includes = scope.get("includes") if isinstance(scope, dict) else None
        excludes = scope.get("excludes") if isinstance(scope, dict) else None
        lines: list[str] = []
        if includes:
            lines.append("**Includes**:")
            for inc in includes:
                lines.append(f"- {inc}")
        if excludes:
            lines.append("")
            lines.append("**Excludes**:")
            for exc in excludes:
                lines.append(f"- {exc}")
        return "\n".join(lines) if lines else "(interface scope to be authored at EXT-04)"

    if section_id == "roles":
        # Governance roles / owners.
        gov = record.get("governance") or {}
        roles = gov.get("roles") if isinstance(gov, dict) else None
        if roles:
            if isinstance(roles, list):
                return "\n".join(f"- {r}" for r in roles)
            return str(roles)
        owners = (record.get("metadata") or {}).get("owners")
        if owners:
            return "\n".join(f"- {o}" for o in owners)
        return "(stewardship roles to be assigned at EXT-04)"

    if section_id == "rules-controls":
        # Governance regulators + rules.
        gov = record.get("governance") or {}
        lines: list[str] = []
        regs = gov.get("regulators") if isinstance(gov, dict) else None
        if regs:
            lines.append("**Regulators / supervisors**:")
            for r in regs:
                lines.append(f"- {r}")
        rules = gov.get("rules") if isinstance(gov, dict) else None
        if rules:
            lines.append("")
            lines.append("**Rules**:")
            for r in rules:
                lines.append(f"- {r}")
        return "\n".join(lines) if lines else "(business rules and controls to be authored at EXT-04)"

    if section_id == "outcomes":
        outcome = record.get("outcome")
        if outcome:
            return f"{outcome}"
        return "(outcomes to be quantified at EXT-04; L0/L1 inherit from ECF framework per PROFILE_REGISTRY)"

    if section_id == "evidence":
        meta = record.get("metadata") or {}
        ch = meta.get("change_history") or []
        lines: list[str] = []
        if ch:
            lines.append("**Change history**:")
            for entry in ch:
                if isinstance(entry, dict):
                    cr = entry.get("cr", "?")
                    date = entry.get("date", "?")
                    change = entry.get("change", "").strip().split("\n")[0][:200]
                    lines.append(f"- {date}: {cr} -- {change}")
        # Evidence links (BP-specific).
        identity = record.get("identity") or {}
        ev_links = identity.get("evidence_links") if isinstance(identity, dict) else None
        if ev_links:
            lines.append("")
            lines.append("**Evidence links**:")
            for link in ev_links:
                if isinstance(link, dict):
                    lines.append(
                        f"- {link.get('type', '?')}: `{link.get('ref', '?')}`"
                    )
        # Provenance for PC.
        prov = record.get("provenance") or {}
        if prov:
            lines.append("")
            lines.append("**Provenance**:")
            for k, v in prov.items():
                lines.append(f"- {k}: {v}")
        if not lines:
            return "(evidence and provenance to be backfilled at EXT-04)"
        return "\n".join(lines)

    if section_id == "completeness":
        return (
            "Sections authored by `scripts/generate_readmes.py` from the "
            "record's YAML fields. Section content marked as 'pending' "
            "indicates fields not present in the source record; these "
            "are flagged as DOC-004 informational placeholders and are "
            "scheduled for backfill under EXT-04 (section authoring) and "
            "EXT-06 (content completeness)."
        )

    if section_id == "revision-history":
        meta = record.get("metadata") or {}
        ch = meta.get("change_history") or []
        lines: list[str] = []
        lines.append(
            "Revision history is governed by CR-BP-04 / SIV-001..004 "
            "(additive change_history entries; version unchanged for "
            "additive metadata-only changes)."
        )
        if ch:
            lines.append("")
            lines.append("**Governing CRs**:")
            for entry in ch:
                if isinstance(entry, dict):
                    cr = entry.get("cr", "?")
                    date = entry.get("date", "?")
                    lines.append(f"- {date}: {cr}")
        return "\n".join(lines)

    return ""


def generate_readme(record: dict, level: str) -> str:
    """Render the full README markdown for a record at the given level."""
    rid = record.get("id", "unknown")
    # L0 ProcessContext records lack an explicit `type` field; default to
    # the canonical L0 type label.
    if level == "L0":
        rtype = "ProcessContext"
    else:
        rtype = record.get("type", "Record")
    name = record.get("name", "(unnamed)")
    sections = PROFILE_SECTIONS.get((rtype, level), [])
    if not sections:
        return ""
    out: list[str] = []
    out.append(f"# Canonical {rtype}: `{rid}`")
    out.append("")
    out.append(
        f"This directory hosts the canonical {rtype} record for `{rid}`. "
        f"This README is generated by `scripts/generate_readmes.py` "
        f"(CR-BP-94-EXT-02) from the record's YAML fields per the "
        f"documentation profile required at the {level} level."
    )
    out.append("")
    out.append(f"**Name**: {name}")
    out.append("")
    for sid in sections:
        out.append(SECTION_HEADINGS[sid])
        out.append("")
        out.append(render_section(sid, record, level))
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would be written without touching the filesystem.",
    )
    parser.add_argument(
        "--scope",
        type=Path,
        default=None,
        help="Restrict generation to a single record directory.",
    )
    args = parser.parse_args(argv)

    paths = resolve_record_paths()
    if args.scope is not None:
        scope = str(args.scope)
        paths = [
            p for p in paths
            if scope in str(p) or scope in str(p.parent)
        ]

    written = 0
    skipped_existing = 0
    skipped_invalid = 0
    for path in paths:
        record = load_record(path)
        if record is None:
            skipped_invalid += 1
            continue
        level = resolve_level(record)
        if level is None:
            skipped_invalid += 1
            continue
        readme_path = resolve_readme_path(path, rid := record.get("id", ""))
        if readme_path.exists():
            skipped_existing += 1
            continue
        content = generate_readme(record, level)
        if not content:
            skipped_invalid += 1
            continue
        if args.dry_run:
            print(f"[dry-run] would write {readme_path} ({len(content)} bytes)")
        else:
            readme_path.parent.mkdir(parents=True, exist_ok=True)
            readme_path.write_text(content)
        written += 1

    print(
        f"generate_readmes: written={written} "
        f"skipped_existing={skipped_existing} "
        f"skipped_invalid={skipped_invalid} "
        f"total_scanned={len(paths)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
