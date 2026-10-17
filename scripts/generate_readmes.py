#!/usr/bin/env python3
"""generate_readmes.py ; CR-BP-94-EXT-07 README generator (consolidated template).

CR-BP-94-EXT-07. Supersedes CR-BP-94-EXT-02's 13-section template with
the consolidated 8-section L0 + 7-section L1-L4 design (T9.13 + EXT-02 +
CR-BP-120). Generates README.md for every canonical record under
entities/v1-alpha/ that does not already have one. Each generated
README follows the documentation profile required by the record's
(type, level) combination as registered in scripts/check_documentation_profile.py
PROFILE_REGISTRY.

Sections (per the consolidated design; see change-requests/CR-BP-94-EXT-07):

  L0 ProcessContext (8 sections):
    1. Header and Identity Table
    2. Executive Summary / Intent
    3. Governance and Provenance
    4. Behavioral Boundaries (Cell Charter)
    5. Hierarchical Decomposition (Path Scheme; collapsible)
    6. Properties and Relationships
    7. Operational, Control and Metrics Details (L0-only metrics table)
    8. Technical Metadata

  L1-L4 record (7 sections):
    1. Header and Identity Table
    2. Intent and Definition
    3. Governance and Provenance (lighter)
    4. Properties and Relationships
    5. Hierarchical Decomposition
    6. Operational Details (no metrics at L1-L4)
    7. Technical Metadata

Content is drawn from each record's YAML fields. Sections that have no
data in the source record are populated with a deterministic placeholder
that the validator accepts. The new `metrics` block (L0-only; optional
KPI/KRI/KCI) renders as a 3-column table or `(Pending EXT-04)` placeholder
when absent.

Backward compatibility: existing YAML records without a `metrics` block
or without a `cell_charter` block render the appropriate placeholder.
The dry-run flag is preserved.

Usage:
  python3 scripts/generate_readmes.py [--dry-run] [--scope path]
  python3 scripts/generate_readmes.py --force   # CR-BP-114: regeneration
  python3 scripts/generate_readmes.py --check   # CR-BP-114: drift check
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


# Required section ids per (type, level) profile. CR-BP-94-EXT-07
# consolidated design. Mirrors PROFILE_REGISTRY in
# scripts/check_documentation_profile.py.
PROFILE_SECTIONS: dict[tuple[str, str], list[str]] = {
    ("ProcessContext", "L0"): [
        "header-identity-table",
        "executive-summary",
        "governance-provenance",
        "behavioral-boundaries",
        "hierarchical-decomposition",
        "properties-relationships",
        "operational-metrics",
        "technical-metadata",
    ],
    ("ProcessGroup", "L1"): [
        "header-identity-table",
        "intent-definition",
        "governance-provenance",
        "properties-relationships",
        "hierarchical-decomposition",
        "operational-details",
        "technical-metadata",
    ],
    ("Process", "L2"): [
        "header-identity-table",
        "intent-definition",
        "governance-provenance",
        "properties-relationships",
        "hierarchical-decomposition",
        "operational-details",
        "technical-metadata",
    ],
    ("Activity", "L3"): [
        "header-identity-table",
        "intent-definition",
        "governance-provenance",
        "properties-relationships",
        "hierarchical-decomposition",
        "operational-details",
        "technical-metadata",
    ],
    ("Task", "L4"): [
        "header-identity-table",
        "intent-definition",
        "governance-provenance",
        "properties-relationships",
        "hierarchical-decomposition",
        "operational-details",
        "technical-metadata",
    ],
}


# Section id -> markdown heading.
# L0 sections use numeric prefix 1-8 for scanability; L1-L4 use descriptive
# headings without numeric prefix. The validator's EXPECTED_HEADINGS regex
# matches these exact strings (case-insensitive on the heading text).
SECTION_HEADINGS: dict[str, str] = {
    "header-identity-table": "## Header and Identity Table",
    "executive-summary": "## 1. Executive Summary / Intent",
    "intent-definition": "## Intent and Definition",
    "governance-provenance": "## 2. Governance and Provenance",
    "behavioral-boundaries": "## 3. Behavioral Boundaries (Cell Charter)",
    "hierarchical-decomposition": "## 4. Hierarchical Decomposition (Path Scheme)",
    "properties-relationships": "## 5. Properties and Relationships",
    "operational-metrics": "## 6. Operational, Control and Metrics Details",
    "operational-details": "## Operational Details",
    "technical-metadata": "## 7. Technical Metadata",
}


# Status emoji map (CR-BP-120 example; for the Header and Identity Table).
STATUS_EMOJI: dict[str, str] = {
    "candidate": "candidate (yellow)",
    "proposed": "proposed (blue)",
    "ratified": "ratified (green)",
    "ratified-accepted": "ratified-accepted (green)",
    "deprecated": "deprecated (orange)",
    "retired": "retired (red)",
}


# Per-domain regulatory evidence base (CR-BP-120 example).
# Used by the Governance and Provenance section to surface the
# `regulatory_evidence` block. If the record has no such block, falls
# back to the cell's `domain` (if discoverable) and looks up here.
REGULATORY_BY_DOMAIN: dict[str, list[str]] = {
    "ao": [
        "Banking: FCA SMCR (CF1-CF11 controlled functions, Statements of Responsibilities)",
        "Healthcare: US State Healthcare Licensure regimes",
        "Insurance: NAIC Producer Licensing Model Act",
        "Aviation: EASA / FAA crew licensing (type-rated licences)",
        "Professional Services: UK SRA / US State Bar admissions",
    ],
    "eo": [
        "Banking: PRA / FCA operational risk (SYSC)",
        "Aviation: EASA Air Operator Certificate (AOC) requirements",
        "Energy: FERC / Ofgem operations licensing",
        "Telecommunications: FCC / Ofcom spectrum authorisation",
    ],
    "fa": [
        "Banking: PRA / FCA capital and liquidity (CRR, CRD IV, Basel III)",
        "Insurance: NAIC / Solvency II / IFRS 17 statutory accounting",
        "Securities: SEC / FCA reporting (10-K, FINREP, COREP)",
    ],
    "sd": [
        "Technology: ISO 27001 (information security management)",
        "Privacy: GDPR (EU) / CCPA (California) / PIPEDA (Canada)",
        "Healthcare: HIPAA (US) / NHS Data Security and Protection Toolkit",
    ],
    "ce": [
        "Procurement: ISO 20400 (sustainable procurement)",
        "Trade: WTO Government Procurement Agreement (GPA)",
        "Anti-bribery: UK Bribery Act / FCPA",
    ],
    "hr": [
        "Employment: Equality Act 2010 (UK) / Title VII (US) / EU Directives",
        "Health and safety: OSHA (US) / HSE (UK)",
        "Data: GDPR for employee records",
    ],
    "le": [
        "Contract: Common law / UCC (US) / UNIDROIT Principles",
        "Real estate: local land registries + RICS standards",
    ],
    "pc": [
        "Communications: Ofcom (UK) / FCC (US) spectrum and broadcast licensing",
        "Media: local regulator press / broadcasting codes",
    ],
}


def _cell_of_id(record_id: str) -> str | None:
    """Extract the cell slug (`<domain>-<stage>`) from a canonical id.

    `processes:pc-fa-retire-64q5p9` -> `fa-retire`. Returns None for
    malformed ids.
    """
    body = record_id.split(":", 1)
    if len(body) != 2:
        return None
    parts = body[1].split("-")
    if len(parts) < 4:
        return None
    return f"{parts[1]}-{parts[2]}"


def _domain_of_cell(cell: str | None) -> str | None:
    """Extract the domain prefix from a cell slug.

    `fa-retire` -> `fa`. Returns None when no cell.
    """
    if cell is None:
        return None
    parts = cell.split("-", 1)
    if not parts:
        return None
    return parts[0]


def _stage_of_cell(cell: str | None) -> str | None:
    """Extract the stage suffix from a cell slug.

    `fa-retire` -> `retire`. Returns None when no cell.
    """
    if cell is None:
        return None
    parts = cell.split("-", 1)
    if len(parts) < 2:
        return None
    return parts[1]


def resolve_level(record: dict) -> str | None:
    """Resolve the L0..L4 level from a record's type + structural cues.

    L0 ProcessContext is the only record type that doesn't carry an
    explicit `type` discriminator; it's identified by the id pattern
    `processes:pc-*` (CR-BP-02 section 3 convention; CR-BP-mv1 id system).
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
    if isinstance(rid, str) and rid.startswith("processes:pc-"):
        return "L0"
    return None


def resolve_record_paths() -> list[Path]:
    """Walk the CR-BP-mv1 containment tree for canonical records.

    Records live at `entities/v1-alpha/<cell>/.../processes-<...>.yaml`
    with README.md as a sibling. L0 ProcessContext records live at cell
    level in the same tree (the pre-migration `contexts/v1-alpha/` root
    is retired).

    Skips documentation/, examples/, research/ subdirectories
    (those are not canonical records).
    """
    paths: list[Path] = []
    if ENTITIES_ROOT.exists():
        for f in sorted(ENTITIES_ROOT.rglob("processes-*.yaml")):
            pos = f.as_posix()
            if "/documentation/" in pos or "/examples/" in pos or "/research/" in pos:
                continue
            paths.append(f)
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


# -----------------------------------------------------------------------------
# Section renderers (CR-BP-94-EXT-07 consolidated design)
# -----------------------------------------------------------------------------


def _header_identity_table(record: dict, level: str) -> str:
    """Section 1: Header and Identity Table.

    6-row Markdown table with 2 columns of 3 attribute/value rows each.
    Domain, Lifecycle Stage, Level, Status, Version, Schema.
    """
    rid = record.get("id", "unknown")
    if level == "L0":
        rtype = "ProcessContext"
    else:
        rtype = record.get("type", "Record")
    name = record.get("name", "(unnamed)")
    version = record.get("version", "1.0.0")
    status = record.get("lifecycle_status", "candidate")
    status_text = STATUS_EMOJI.get(status, status)

    # Domain + lifecycle: from the cell slug.
    cell = _cell_of_id(rid)
    domain = _domain_of_cell(cell) or "?"
    stage = _stage_of_cell(cell) or "?"

    domain_pretty = domain.upper() if domain != "?" else "?"
    level_pretty = f"{level} ({rtype})"

    lines = [
        "| Attribute | Value | Attribute | Value |",
        "| :--- | :--- | :--- | :--- |",
        f"| **Domain** | {domain_pretty} | **Lifecycle Stage** | {stage.title()} |",
        f"| **Level** | {level_pretty} | **Status** | `{status_text}` |",
        f"| **Version** | {version} | **Schema** | `dea/v1` |",
        f"| **Name** | {name} | **Canonical ID** | `{rid}` |",
    ]
    return "\n".join(lines)


def _executive_summary(record: dict, level: str) -> str:
    """L0-only Section 2: Executive Summary / Intent.

    1 paragraph: what the entity is + why it exists. Pulls from
    `cell_charter.combined_semantic_meaning` or `definition` or
    `description` or `process_intent`. Falls back to the cell charter
    `enterprise_concern` if all else absent.
    """
    charter = record.get("cell_charter") or {}
    if isinstance(charter, dict):
        meaning = charter.get("combined_semantic_meaning")
        if meaning:
            return meaning.strip()
    definition = record.get("definition") or record.get("description") or record.get("process_intent")
    if definition:
        return definition.strip()
    if isinstance(charter, dict):
        concern = charter.get("enterprise_concern")
        if concern:
            return concern.strip()
    return "(executive summary pending; backfill at EXT-04)"


def _intent_definition(record: dict, level: str) -> str:
    """L1-L4 Section 2: Intent and Definition (combined).

    1 paragraph (the Intent, from `process_intent` or `description`) +
    a sub-section for the formal Definition.
    """
    intent = (
        record.get("process_intent")
        or record.get("description")
        or record.get("definition")
        or "(intent pending; backfill at EXT-04)"
    )
    definition = record.get("definition") or "(definition pending; backfill at EXT-04)"

    out = [
        "**Intent**: " + intent.strip(),
        "",
        "**Definition**: " + definition.strip(),
    ]
    return "\n".join(out)


def _governance_provenance(record: dict, level: str) -> str:
    """Section 3: Governance and Provenance.

    For L0: admission score + regulatory evidence base (from the cell's
    domain lookup) + change history table.

    For L1-L4: admission score + change history table (no regulatory
    evidence base; that's L0-only).
    """
    rid = record.get("id", "unknown")
    cell = _cell_of_id(rid)
    domain = _domain_of_cell(cell)
    out: list[str] = []

    # Admission score (L0 + L1)
    admission = record.get("admission") or {}
    if isinstance(admission, dict) and admission:
        score = admission.get("score", "?")
        max_score = admission.get("max", 10)
        decision = admission.get("decision", "")
        rec_by = admission.get("recommended_by", "")
        rec_date = admission.get("date", "")
        out.append(
            f"- **Admission Score**: `{score}/{max_score}`"
            + (f" (`{decision}`)" if decision else "")
        )
        if rec_by:
            rec_line = f"- **Recommended By**: `{rec_by}`"
            if rec_date:
                rec_line += f" ({rec_date})"
            out.append(rec_line)

    # Regulatory evidence base (L0 only; CR-BP-120 example)
    if level == "L0" and domain:
        evidence = REGULATORY_BY_DOMAIN.get(domain, [])
        if evidence:
            out.append("")
            out.append("- **Regulatory Evidence Base**:")
            for line in evidence:
                out.append(f"  - {line}")

    # Change history (both L0 and L1-L4)
    meta = record.get("metadata") or {}
    ch = meta.get("change_history") or []
    if ch:
        out.append("")
        out.append("**Change and Audit History**")
        out.append("")
        out.append("| Date | Change Request | Action / Disposition | Author |")
        out.append("| :--- | :--- | :--- | :--- |")
        for entry in ch:
            if not isinstance(entry, dict):
                continue
            cr = entry.get("cr", "?")
            date = entry.get("date", "?")
            change = entry.get("change", "").strip().split("\n")[0][:200]
            author = entry.get("author", "System")
            out.append(f"| {date} | `{cr}` | {change} | {author} |")

    if not out:
        return "(governance and provenance to be backfilled at EXT-04)"
    return "\n".join(out)


def _behavioral_boundaries(record: dict, level: str) -> str:
    """L0-only Section 4: Behavioral Boundaries (Cell Charter).

    3-row Markdown table: In Scope, Out of Scope, Adjacent Cells.
    Renders the `cell_charter.inclusions`, `exclusions`, and
    `adjacent_boundaries` blocks. Falls back to a placeholder if the
    record has no cell_charter.
    """
    charter = record.get("cell_charter") or {}
    if not isinstance(charter, dict) or not charter:
        return "(Cell charter pending; backfill at EXT-04)"

    inclusions = charter.get("inclusions") or []
    exclusions = charter.get("exclusions") or []
    adjacent = charter.get("adjacent_boundaries") or []

    # Combine: each cell_charter can have a list of {name, description}
    # or plain strings. Render as bulleted lists within the table cells.
    def _render_list(items: list) -> str:
        if not items:
            return "_(none)_"
        if all(isinstance(x, str) for x in items):
            return "<br>".join(f"- {x}" for x in items)
        out = []
        for item in items:
            if isinstance(item, dict):
                name = item.get("name", "")
                desc = item.get("description", "")
                if name and desc:
                    out.append(f"- **{name}**: {desc}")
                elif desc:
                    out.append(f"- {desc}")
                elif name:
                    out.append(f"- {name}")
            else:
                out.append(f"- {item}")
        return "<br>".join(out) if out else "_(none)_"

    in_scope_text = _render_list(inclusions)
    out_scope_text = _render_list(exclusions)

    # Adjacent: may be a list of {cell_id, relationship} or plain strings.
    if adjacent:
        adj_parts: list[str] = []
        for item in adjacent:
            if isinstance(item, dict):
                cid = item.get("cell_id", "")
                rel = item.get("relationship", "")
                if cid and rel:
                    adj_parts.append(f"- `{cid}`: {rel}")
                elif cid:
                    adj_parts.append(f"- `{cid}`")
                elif rel:
                    adj_parts.append(f"- {rel}")
            else:
                adj_parts.append(f"- {item}")
        adjacent_text = "<br>".join(adj_parts) if adj_parts else "_(none)_"
    else:
        adjacent_text = "_(none)_"

    table = [
        "| Scope Type | Description |",
        "| :--- | :--- |",
        f"| In Scope (inclusions) | {in_scope_text} |",
        f"| Out of Scope (exclusions) | {out_scope_text} |",
        f"| Adjacent Cells | {adjacent_text} |",
    ]
    return "\n".join(table)


def _hierarchical_decomposition(record: dict, level: str) -> str:
    """Section 5: Hierarchical Decomposition (Path Scheme).

    L0: full L1-L4 tree inside a `<details>` HTML collapsible block.
    L1-L4: parent + children path summary inside a collapsible.
    """
    rid = record.get("id", "unknown")
    cell = _cell_of_id(rid)
    if cell is None:
        return "(path scheme unavailable: id has no cell segment)"

    if level == "L0":
        # Full L1-L4 tree (CR-BP-117c C-3: kebab-cased dir names, BASE32
        # hash in record filename, sorted at each level of the walk).
        cell_dir = ENTITIES_ROOT / cell
        if not cell_dir.is_dir():
            return f"(path scheme unavailable: {cell_dir} not found)"

        level_label = {
            "pc": "L0 ProcessContext",
            "group": "L1 ProcessGroup",
            "process": "L2 Process",
            "activity": "L3 Activity",
            "task": "L4 Task",
            "scope": "L0 ProcessScope",
        }
        tree_lines = [f"{cell}/"]

        def walk(d: Path, depth: int) -> None:
            for child in sorted(d.iterdir(), key=lambda p: p.name):
                if not child.is_dir() or child.name == "research":
                    continue
                yamls = sorted(child.glob("processes-*.yaml"))
                if not yamls:
                    continue
                token = yamls[0].name.split("-")[1]
                label = level_label.get(token, "L?")
                tree_lines.append(
                    f"{'  ' * depth}{child.name}/  ({label})"
                )
                walk(child, depth + 1)

        walk(cell_dir, 1)
        tree_text = "\n".join(tree_lines)

        return (
            "Directory layout of this cell (dir names are the "
            "kebab-cased record names; the BASE32 hash lives in the "
            "record filename).\n\n"
            "<details>\n"
            "<summary>Expand to view full L1-L4 Directory Tree</summary>\n\n"
            "```text\n"
            f"{tree_text}\n"
            "```\n\n"
            "_(Full L4 task lists for each L3 activity are available in their respective subdirectories.)_\n"
            "</details>"
        )

    # L1-L4: parent + children summary
    part_of = record.get("part_of")
    children_lines: list[str] = []
    if part_of:
        if isinstance(part_of, list):
            for p in part_of:
                children_lines.append(f"- Part of (parent L1): `{p}`")
        else:
            children_lines.append(f"- Part of (parent L1): `{part_of}`")

    act_refs = (record.get("metadata") or {}).get("activity_references") or []
    if act_refs:
        children_lines.append("- Composes (children L3):")
        for a in act_refs:
            children_lines.append(f"  - `{a}`")

    cohesion = record.get("cohesion_rationale")
    if cohesion:
        children_lines.append(f"- **Cohesion rationale**: {cohesion}")

    if not children_lines:
        return "(decomposition relationships pending)"

    body = "\n".join(children_lines)
    return (
        "<details>\n"
        f"<summary>Expand to view decomposition details</summary>\n\n"
        f"{body}\n"
        "</details>"
    )


def _properties_relationships(record: dict, level: str) -> str:
    """Section 6: Properties and Relationships.

    Two tables:
      1. Properties table: every record field (excluding reserved keys)
         as `name | type | required | description`.
      2. Relationships table: the `composes` / `realizes` / `specializes` /
         `part_of` / `depends_on` / etc. relationships with `kind | target
         id | cardinality`.

    The Properties table is a deterministic enumeration of the record's
    YAML keys. Reserved keys (`id`, `type`, `version`, `lifecycle_status`,
    `metadata`) are excluded.
    """
    rid = record.get("id", "unknown")
    out: list[str] = []

    # Properties table
    reserved = {"id", "type", "version", "lifecycle_status", "metadata", "name"}
    property_rows: list[tuple[str, str, str, str]] = []
    for k, v in record.items():
        if k in reserved or k.startswith("_"):
            continue
        if isinstance(v, dict):
            type_str = "object"
        elif isinstance(v, list):
            type_str = f"array[{len(v)}]"
        elif isinstance(v, bool):
            type_str = "boolean"
        elif isinstance(v, int):
            type_str = "integer"
        elif isinstance(v, float):
            type_str = "number"
        elif isinstance(v, str):
            type_str = "string"
        else:
            type_str = type(v).__name__

        # Build a short description from the field value (truncated).
        if isinstance(v, str):
            desc = v.strip().split("\n")[0][:120]
        elif isinstance(v, dict):
            keys = ", ".join(v.keys())
            desc = f"object: {keys}"[:120]
        elif isinstance(v, list):
            desc = f"array of {len(v)} item(s)"
        else:
            desc = str(v)[:120]

        property_rows.append((k, type_str, "no", desc))

    if property_rows:
        out.append("**Properties**")
        out.append("")
        out.append("| Name | Type | Required | Description |")
        out.append("| :--- | :--- | :--- | :--- |")
        for name, t, req, desc in property_rows:
            out.append(f"| `{name}` | {t} | {req} | {desc} |")
        out.append("")

    # Relationships table
    rel_rows: list[tuple[str, str, str]] = []
    for rel_key in ("composes", "realizes", "specializes", "part_of", "depends_on", "enables", "is_part_of"):
        v = record.get(rel_key)
        if v is None:
            continue
        if isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    target = item.get("target") or item.get("id") or "?"
                    card = item.get("cardinality", "1")
                    rel_rows.append((rel_key, target, card))
                else:
                    rel_rows.append((rel_key, str(item), "1"))
        elif isinstance(v, dict):
            target = v.get("target") or v.get("id") or "?"
            card = v.get("cardinality", "1")
            rel_rows.append((rel_key, target, card))
        else:
            rel_rows.append((rel_key, str(v), "1"))

    if rel_rows:
        out.append("**Relationships**")
        out.append("")
        out.append("| Kind | Target ID | Cardinality |")
        out.append("| :--- | :--- | :--- |")
        for kind, target, card in rel_rows:
            out.append(f"| `{kind}` | `{target}` | {card} |")

    if not out:
        return "_(no additional properties or relationships surfaced)_"
    return "\n".join(out)


def _operational_metrics(record: dict, level: str) -> str:
    """L0-only Section 7: Operational, Control and Metrics Details.

    Four sub-blocks:
      1. Inputs / Outputs / Interfaces (from process_scope or governance)
      2. Roles and Responsibilities (from governance.roles or metadata.owners)
      3. Business Rules and Controls (from governance.rules)
      4. Target Metrics (from the new `metrics` block: KPI / KRI / KCI)

    If the record has no `metrics` block, the Target Metrics sub-block
    renders `(Pending EXT-04)` placeholder.
    """
    out: list[str] = []

    # Inputs / Outputs / Interfaces
    scope = record.get("process_scope") or {}
    includes = scope.get("includes") if isinstance(scope, dict) else None
    excludes = scope.get("excludes") if isinstance(scope, dict) else None
    interfaces_lines: list[str] = []
    if includes:
        interfaces_lines.append("**Includes**:")
        for inc in includes:
            interfaces_lines.append(f"- {inc}")
    if excludes:
        interfaces_lines.append("")
        interfaces_lines.append("**Excludes**:")
        for exc in excludes:
            interfaces_lines.append(f"- {exc}")
    if interfaces_lines:
        out.append("**Inputs, Outputs and Interfaces**")
        out.append("")
        out.extend(interfaces_lines)
    else:
        out.append("**Inputs, Outputs and Interfaces**: _(pending; backfill at EXT-04)_")

    out.append("")

    # Roles and Responsibilities
    gov = record.get("governance") or {}
    roles = gov.get("roles") if isinstance(gov, dict) else None
    if roles:
        out.append("**Roles and Responsibilities**")
        out.append("")
        if isinstance(roles, list):
            for r in roles:
                out.append(f"- {r}")
        else:
            out.append(f"- {roles}")
        out.append("")
    else:
        owners = (record.get("metadata") or {}).get("owners")
        if owners:
            out.append("**Roles and Responsibilities (owners)**")
            out.append("")
            for o in owners:
                out.append(f"- {o}")
            out.append("")
        else:
            out.append("**Roles and Responsibilities**: _(pending; backfill at EXT-04)_")
            out.append("")

    # Business Rules and Controls
    rules = gov.get("rules") if isinstance(gov, dict) else None
    regs = gov.get("regulators") if isinstance(gov, dict) else None
    rules_lines: list[str] = []
    if regs:
        rules_lines.append("**Regulators / supervisors**:")
        for r in regs:
            rules_lines.append(f"- {r}")
        rules_lines.append("")
    if rules:
        rules_lines.append("**Rules**:")
        for r in rules:
            rules_lines.append(f"- {r}")
    if rules_lines:
        out.append("**Business Rules and Controls**")
        out.append("")
        out.extend(rules_lines)
        out.append("")
    else:
        out.append("**Business Rules and Controls**: _(pending; backfill at EXT-04)_")
        out.append("")

    # Target Metrics (the new `metrics` block)
    metrics = record.get("metrics")
    out.append("**Target Metrics and Indicators**")
    out.append("")
    if isinstance(metrics, dict) and metrics:
        out.append("Standardised metrics required to measure the health, "
                   "efficiency, and compliance of this ProcessContext. "
                   "Authored under the EXT-04 workstream; completeness "
                   "validated under EXT-06.")
        out.append("")
        out.append("| Category | Metric / Indicator Name | Target / Threshold | Measurement Frequency |")
        out.append("| :--- | :--- | :--- | :--- |")
        for category, label in [
            ("performance", "KPI (Performance)"),
            ("risk", "KRI (Risk)"),
            ("compliance", "KCI (Compliance)"),
        ]:
            entries = metrics.get(category) or []
            for m in entries:
                if isinstance(m, dict):
                    name = m.get("name", "?")
                    target = m.get("target", "?")
                    freq = m.get("frequency", "?")
                    out.append(f"| **{label}** | {name} | {target} | {freq} |")
    else:
        out.append("_(Pending EXT-04)_")

    return "\n".join(out)


def _operational_details(record: dict, level: str) -> str:
    """L1-L4 Section 6: Operational Details (no metrics).

    Three sub-blocks: Inputs/Outputs, Roles, Rules. Mirrors the L0
    `operational-metrics` minus the metrics sub-block.
    """
    out: list[str] = []

    # Inputs / Outputs
    scope = record.get("process_scope") or {}
    includes = scope.get("includes") if isinstance(scope, dict) else None
    excludes = scope.get("excludes") if isinstance(scope, dict) else None
    if includes or excludes:
        if includes:
            out.append("**Includes**:")
            for inc in includes:
                out.append(f"- {inc}")
            out.append("")
        if excludes:
            out.append("**Excludes**:")
            for exc in excludes:
                out.append(f"- {exc}")
            out.append("")
    else:
        out.append("**Inputs / Outputs**: _(pending; backfill at EXT-04)_")
        out.append("")

    # Roles
    gov = record.get("governance") or {}
    roles = gov.get("roles") if isinstance(gov, dict) else None
    owners = (record.get("metadata") or {}).get("owners")
    if roles or owners:
        out.append("**Roles and Responsibilities**")
        out.append("")
        if roles:
            if isinstance(roles, list):
                for r in roles:
                    out.append(f"- {r}")
            else:
                out.append(f"- {roles}")
        if owners:
            for o in owners:
                out.append(f"- (owner) {o}")
        out.append("")
    else:
        out.append("**Roles and Responsibilities**: _(pending; backfill at EXT-04)_")
        out.append("")

    # Rules
    rules = gov.get("rules") if isinstance(gov, dict) else None
    if rules:
        out.append("**Business Rules and Controls**")
        out.append("")
        for r in rules:
            out.append(f"- {r}")
        out.append("")
    else:
        out.append("**Business Rules and Controls**: _(pending; backfill at EXT-04)_")

    return "\n".join(out)


def _technical_metadata(record: dict, level: str) -> str:
    """Section 8 (L0) / Section 7 (L1-L4): Technical Metadata.

    Source YAML link, register version, documentation completeness.
    """
    rid = record.get("id", "unknown")
    version = record.get("version", "1.0.0")
    established = (record.get("metadata") or {}).get("established_by", "?")

    parts: list[str] = []
    parts.append(f"- **Source YAML**: record YAML in the same directory as this README")
    parts.append(f"- **Record version**: {version}")
    parts.append(f"- **Governing CR**: `{established}`")
    parts.append("- **Generator**: `scripts/generate_readmes.py` (CR-BP-94-EXT-07)")
    parts.append("- **Schema**: `dea/v1`")
    parts.append(
        "- **Documentation Completeness**: sections marked `_(pending; backfill at EXT-04)_` "
        "indicate fields not yet present in the source YAML record. The structural "
        "validator (CR-BP-94-EXT-04) surfaces these as DOC-004 advisory findings; "
        "completeness is validated under CR-BP-94-EXT-06."
    )
    return "\n".join(parts)


def render_section(
    section_id: str,
    record: dict,
    level: str,
) -> str:
    """Render one section's content deterministically from record fields.

    CR-BP-94-EXT-07: routes to the consolidated-design renderers.
    """
    if section_id == "header-identity-table":
        return _header_identity_table(record, level)
    if section_id == "executive-summary":
        return _executive_summary(record, level)
    if section_id == "intent-definition":
        return _intent_definition(record, level)
    if section_id == "governance-provenance":
        return _governance_provenance(record, level)
    if section_id == "behavioral-boundaries":
        return _behavioral_boundaries(record, level)
    if section_id == "hierarchical-decomposition":
        return _hierarchical_decomposition(record, level)
    if section_id == "properties-relationships":
        return _properties_relationships(record, level)
    if section_id == "operational-metrics":
        return _operational_metrics(record, level)
    if section_id == "operational-details":
        return _operational_details(record, level)
    if section_id == "technical-metadata":
        return _technical_metadata(record, level)
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
        f"(CR-BP-94-EXT-07) from the record's YAML fields per the "
        f"documentation profile required at the {level} level. The "
        f"profile is one of the consolidated designs from CR-BP-94-EXT-07 "
        f"(supersedes CR-BP-94-EXT-02's 13-section template)."
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
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing READMEs (CR-BP-114: regeneration, not just fill-in).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help=(
            "Drift check (CR-BP-114): recompute every README in memory and "
            "compare against the on-disk content. Exits 3 and lists drifted "
            "paths when any README is missing or stale; exits 0 when the "
            "tree is current. Mirrors regenerate_catalog.py --check."
        ),
    )
    args = parser.parse_args(argv)

    paths = resolve_record_paths()
    if args.scope is not None:
        scope = str(args.scope)
        # CR-BP-mv1: ids contain colons; paths use the hyphen-normalized form.
        scope_path = scope.replace(":", "-")
        paths = [
            p for p in paths
            if scope in str(p) or scope_path in str(p) or scope in str(p.parent)
        ]

    written = 0
    skipped_existing = 0
    skipped_invalid = 0
    drifted: list[tuple[Path, str]] = []
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
        content = generate_readme(record, level)
        if not content:
            skipped_invalid += 1
            continue
        if args.check:
            if not readme_path.exists():
                drifted.append((readme_path, "missing"))
            else:
                try:
                    on_disk = readme_path.read_text()
                except OSError:
                    on_disk = None
                if on_disk != content:
                    drifted.append((readme_path, "stale"))
            continue
        if readme_path.exists() and not args.force:
            skipped_existing += 1
            continue
        if args.dry_run:
            print(f"[dry-run] would write {readme_path} ({len(content)} bytes)")
        else:
            readme_path.parent.mkdir(parents=True, exist_ok=True)
            readme_path.write_text(content)
        written += 1

    if args.check:
        for p, why in drifted[:50]:
            print(f"DRIFT ({why}): {p.relative_to(REPO_ROOT)}")
        if len(drifted) > 50:
            print(f"... and {len(drifted) - 50} more")
        if drifted:
            print(
                f"ERROR: {len(drifted)} README(s) missing or stale; "
                f"run `python scripts/generate_readmes.py --force` to refresh"
            )
            return 3
        print(f"OK: {len(paths)} record README(s) current")
        return 0

    print(
        f"generate_readmes: written={written} "
        f"skipped_existing={skipped_existing} "
        f"skipped_invalid={skipped_invalid} "
        f"total_scanned={len(paths)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
