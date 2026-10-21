#!/usr/bin/env python3
"""
validate_readme_structure.py
============================

Generator + Validator half of the EXT documentation workstream
(CR-BP-94-EXT-04).

Codifies DOC-016..020, the validator-side rules that complement
DOC-001..015 (CR-BP-94-EXT-01 / EXT-02). The generator half is
CR-BP-94-EXT-07 (PR #177, OPEN); this validator is the input for
EXT-05 (decomposition reconciliation) per the user directive
2026-10-17 ("Ext-05 should be actioned once we have Ext 04. We need
to wire this in to the development model.").

The five rules:

  DOC-016  Generated README has the EXT-07 section identifiers
           (the 8 L0 / 7 L1-L4 section set; profile-resolved).
  DOC-017  Generated README has the Properties table populated with
           at least one row per record (the EXT-07 properties block).
  DOC-018  Generated README has the Relationships table present
           (rows may be empty for L0 with no decomposes / part_of).
  DOC-019  L0 README has the metrics block populated with at least
           one of {performance, risk, compliance} entries, or the
           (Pending EXT-04) placeholder string.
  DOC-020  L0 README has the cell_charter table populated with all
           three of {In Scope, Out of Scope, Adjacent} scope types,
           or the (Pending EXT-04) placeholder string.

The validator emits two artefacts:

  1. reconciliation/validation-manifest.json
     The machine-readable manifest. Schema:
       schemas/validation-manifest.schema.json.
     This is the input for the EXT-05 decomposition reconciliation
     slice and for any downstream tooling that needs per-record
     validation state.

  2. reconciliation/validation-manifest.yaml
     The human-readable manifest. Same data, YAML serialisation.
     Use this for code review + audit.

The validator is wired as gate [34] Documentation Profile - Generator
and Validator (advisory) in scripts/conformance_result.py. Advisory
means findings are surfaced but do not block merge until a sufficient
population of README assets has been authored (EXT-06, CR-BP-94-EXT-06).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError:
    sys.stderr.write("ERROR: PyYAML is required.\n")
    sys.exit(2)


# -----------------------------------------------------------------------------
# Profile section-id set (re-imported from check_documentation_profile so the
# two validators stay in lock-step on the EXT-07 section IDs).
# -----------------------------------------------------------------------------

try:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from check_documentation_profile import (  # type: ignore
        EXPECTED_HEADINGS,
        LEVEL_BY_TYPE,
        PROFILE_REGISTRY,
    )
    _IMPORT_OK = True
except Exception:  # pragma: no cover - defensive
    _IMPORT_OK = False
    # Fallback constants so the module still loads if the import path is
    # temporarily broken; PROFILE_REGISTRY and EXPECTED_HEADINGS are
    # reproduced verbatim from check_documentation_profile.py.
    LEVEL_BY_TYPE = {
        "ProcessContext": "L0",
        "ProcessGroup": "L1",
        "Process": "L2",
        "Activity": "L3",
        "Task": "L4",
    }
    PROFILE_REGISTRY: dict[tuple[str, str], dict] = {
        ("ProcessContext", "L0"): {
            "profile_id": "dea:profile-readme-l0-process-context-v2",
            "required_section_ids": [
                "header-identity-table", "executive-summary",
                "governance-provenance", "behavioral-boundaries",
                "hierarchical-decomposition", "properties-relationships",
                "operational-metrics", "technical-metadata",
            ],
        },
        ("ProcessGroup", "L1"): {
            "profile_id": "dea:profile-readme-l1-process-group-v2",
            "required_section_ids": [
                "header-identity-table", "intent-definition",
                "governance-provenance", "properties-relationships",
                "hierarchical-decomposition", "operational-details",
                "technical-metadata",
            ],
        },
        ("Process", "L2"): {
            "profile_id": "dea:profile-readme-l2-process-v2",
            "required_section_ids": [
                "header-identity-table", "intent-definition",
                "governance-provenance", "properties-relationships",
                "hierarchical-decomposition", "operational-details",
                "technical-metadata",
            ],
        },
        ("Activity", "L3"): {
            "profile_id": "dea:profile-readme-l3-activity-v2",
            "required_section_ids": [
                "header-identity-table", "intent-definition",
                "governance-provenance", "properties-relationships",
                "hierarchical-decomposition", "operational-details",
                "technical-metadata",
            ],
        },
        ("Task", "L4"): {
            "profile_id": "dea:profile-readme-l4-task-v2",
            "required_section_ids": [
                "header-identity-table", "intent-definition",
                "governance-provenance", "properties-relationships",
                "hierarchical-decomposition", "operational-details",
                "technical-metadata",
            ],
        },
    }
    EXPECTED_HEADINGS: dict[str, str] = {
        "header-identity-table": r"^##\s*Header and Identity Table",
        "executive-summary": r"^##\s*1\.\s*Executive Summary",
        "intent-definition": r"^##\s*Intent and Definition",
        "governance-provenance": r"^##\s*2\.\s*Governance and Provenance",
        "behavioral-boundaries": r"^##\s*3\.\s*Behavioral Boundaries",
        "hierarchical-decomposition": r"^##\s*4\.\s*Hierarchical Decomposition",
        "properties-relationships": r"^##\s*5\.\s*Properties and Relationships",
        "operational-metrics": r"^##\s*6\.\s*Operational, Control and Metrics Details",
        "operational-details": r"^##\s*Operational Details",
        "technical-metadata": r"^##\s*7\.\s*Technical Metadata",
    }

    def _resolve_profile(record: dict) -> dict | None:  # noqa: F811
        # Defensive fallback when the cross-module import failed.
        # The canonical definition is at module level (see below);
        # this branch is only hit when the import raised, which is
        # not the case under normal operation.
        level = _resolve_level(record)
        if level is None:
            return None
        entity_type = record.get("type")
        if not isinstance(entity_type, str):
            entity_type = "ProcessContext" if level == "L0" else None
            if entity_type is None:
                return None
        return PROFILE_REGISTRY.get((entity_type, level))


# -----------------------------------------------------------------------------
# Manifest schema version (bump on structural change to the manifest format).
# -----------------------------------------------------------------------------

MANIFEST_SCHEMA_VERSION = 1
MANIFEST_GENERATOR = "scripts/validate_readme_structure.py"
MANIFEST_PARENT_CR = "CR-BP-94-EXT-04"


# EXT-04 last-resort fallback: cell-root YAML (L0 ProcessContext)
# does not always carry an explicit `type` field at the top level;
# the canonical id carries the level marker instead
# (`pc-` for ProcessContext, `group-` for ProcessGroup,
# `process-` for Process, `activity-` for Activity,
# `task-` for Task).
_ID_LEVEL_MARKER: dict[str, str] = {
    "pc": "L0", "group": "L1", "process": "L2",
    "activity": "L3", "task": "L4",
}
_ID_LEVEL_RE = re.compile(r":(pc|group|process|activity|task)-")


def _resolve_level(record: dict) -> str | None:
    """Resolve the decomposition level from the record.

    Resolution order:
      1. The record's `type` field (canonical).
      2. The canonical id marker (`:pc-`, `:group-`, etc.).
      3. None (unclassifiable; surfaces as `?` in the manifest).

    The id-marker fallback is the EXT-04 addition; the canonical
    `type` field is what CR-BP-93 §3 mandates, but the cell-root
    YAML files do not always carry it. The id is the source of truth
    for the level; the `type` field is informative.
    """
    entity_type = record.get("type")
    if isinstance(entity_type, str):
        return LEVEL_BY_TYPE.get(entity_type)
    rid = record.get("id")
    if isinstance(rid, str):
        m = _ID_LEVEL_RE.search(rid)
        if m:
            return _ID_LEVEL_MARKER.get(m.group(1))
    return None


def _resolve_profile(record: dict) -> dict | None:
    """Resolve the documentation profile for a record.

    Returns the profile dict from PROFILE_REGISTRY or None when
    the (type, level) combination is unrecognized.

    The id-marker fallback is the EXT-04 addition; cell-root YAML
    (L0 ProcessContext) does not always carry the `type` field at
    the top level, so the level is resolved from the canonical id
    when `type` is missing. The (ProcessContext, L0) lookup then
    succeeds.
    """
    level = _resolve_level(record)
    if level is None:
        return None
    entity_type = record.get("type")
    if not isinstance(entity_type, str):
        entity_type = "ProcessContext" if level == "L0" else None
        if entity_type is None:
            return None
    return PROFILE_REGISTRY.get((entity_type, level))


# Placeholder pattern that EXT-07 emits when the source YAML field is
# absent. The placeholder strings are stable so downstream tooling can
# rely on them. (The (Pending EXT-04) marker is what the generator
# emits in DOC-019 and DOC-020; (Pending; backfill at EXT-04) is the
# older DOC-004 marker from EXT-01/02 that EXT-07 supersedes for the
# 49 L0 cell-roots + 3,674 L1-L4 records.)
PENDING_EXT04_PATTERNS = (
    "_(Pending EXT-04)_",
    "(Pending EXT-04)",
    "_(pending; backfill at EXT-04)_",
    "_(pending; backfill at EXT-06)_",
)


# Heading detection helpers. We use the same heading patterns as
# check_documentation_profile.py (the EXPECTED_HEADINGS table) so
# both validators see the same sections.
def _section_present(readme_text: str, section_id: str) -> bool:
    """Return True iff the EXT-07 section with the given id is present
    in the README. Uses the EXPECTED_HEADINGS pattern from the existing
    documentation profile validator so the two stay aligned.
    """
    pattern = EXPECTED_HEADINGS.get(section_id)
    if pattern is None:
        return False
    return re.search(pattern, readme_text, flags=re.MULTILINE) is not None


def _properties_table_populated(readme_text: str) -> bool:
    """DOC-017: the Properties table has at least one row.

    The Properties section is headed by "## 5. Properties and
    Relationships" (L0) or "## Properties and Relationships" (L1-L4).
    The Properties table is the first table; the Relationships table
    is the second. We look for the first table after the Properties
    heading and require at least one non-header row.
    """
    # Find the Properties section anchor
    m = re.search(
        r"^##\s*(?:\d+\.\s*)?Properties and Relationships\s*$",
        readme_text, flags=re.MULTILINE,
    )
    if m is None:
        return False
    # Slice from the heading to the next H2
    after = readme_text[m.end():]
    next_h2 = re.search(r"^##\s", after, flags=re.MULTILINE)
    section_text = after if next_h2 is None else after[:next_h2.start()]
    # Find the first Markdown table. Use [^\n]* to keep the header
    # line single-line; with (.*) dotall the regex would greedily
    # span the first table's content + intervening text + the second
    # table's header line.
    table_match = re.search(
        r"(?ms)^\|[^\n]*\|\s*\n\|[\s\-:|]+\|", section_text,
    )
    if table_match is None:
        return False
    # Count the rows after the separator
    table_text = table_match.group(0)
    rows = [ln for ln in table_text.splitlines() if ln.startswith("|")]
    # 1 header + 1 separator + 1+ data row = at least 3 lines
    return len(rows) >= 3


def _relationships_table_present(readme_text: str) -> bool:
    """DOC-018: the Relationships table is present.

    The Relationships table is the second table in the Properties and
    Relationships section. We look for a second table after the
    Properties table; the second table may be the header + separator
    only (no data rows) for L0 records that do not decompose.

    The DOC-018 rule is enforced for L0 + L1 only; L2-L4 (Process,
    Activity, Task) are leaves in the decomposition tree and the
    generator omits the Relationships table because the relationships
    are surfaced in the Properties table (`belongs_to_activity`,
    `belongs_to_process`, etc.). The EXT-04 evaluator skips L2-L4
    records for DOC-018; the EXT-06 evaluator will surface L2-L4
    relationships that are missing from the Properties table under
    a separate rule.
    """
    m = re.search(
        r"^##\s*(?:\d+\.\s*)?Properties and Relationships\s*$",
        readme_text, flags=re.MULTILINE,
    )
    if m is None:
        return False
    after = readme_text[m.end():]
    next_h2 = re.search(r"^##\s", after, flags=re.MULTILINE)
    section_text = after if next_h2 is None else after[:next_h2.start()]
    tables = re.findall(r"(?ms)^\|[^\n]*\|\s*\n\|[\s\-:|]+\|", section_text)
    # The first table is Properties; the second is Relationships.
    return len(tables) >= 2


def _metrics_block_state(readme_text: str, yaml_record: dict) -> dict:
    """DOC-019: L0 records must have a metrics block (or placeholder).

    The metrics block is the "Target Metrics and Indicators" sub-section
    under "## 6. Operational, Control and Metrics Details". For L0,
    the block is considered populated iff either:
      (a) the YAML record has at least one of
          {metrics.performance, metrics.risk, metrics.compliance}, OR
      (b) the README contains one of the placeholder strings, OR
      (c) the README contains a "Target Metrics" table (the EXT-07
          generator emits a 4-column table with headers that include
          "KPI" / "KRI" / "KCI" labels).
    """
    has_yaml_metrics = False
    metrics = yaml_record.get("metrics")
    if isinstance(metrics, dict):
        for key in ("performance", "risk", "compliance"):
            if isinstance(metrics.get(key), list) and len(metrics[key]) > 0:
                has_yaml_metrics = True
                break
    has_placeholder = any(p in readme_text for p in PENDING_EXT04_PATTERNS)
    # The EXT-07 generator emits a "Target Metrics and Indicators"
    # table. The header row carries "KPI" / "KRI" / "KCI" / "Frequency"
    # labels. We look for the section heading + a subsequent table
    # with a header row containing "KPI" or "KRI" or "KCI".
    has_table = False
    sec = re.search(
        r"^\*?\*?Target Metrics(?:\s+and\s+Indicators)?\*?\*?\s*$",
        readme_text, flags=re.MULTILINE,
    )
    if sec is not None:
        after = readme_text[sec.end():]
        next_h2 = re.search(r"^##\s", after, flags=re.MULTILINE)
        sec_text = after if next_h2 is None else after[:next_h2.start()]
        # Look for a table whose header row contains one of the
        # metric-type labels.
        if re.search(
            r"(?ms)^\|.*(?:KPI|KRI|KCI).*\|", sec_text,
        ):
            has_table = True
    return {
        "has_yaml_metrics": has_yaml_metrics,
        "has_placeholder": has_placeholder,
        "has_table": has_table,
        "populated": has_yaml_metrics or has_placeholder or has_table,
    }


def _cell_charter_table_state(readme_text: str, yaml_record: dict) -> dict:
    """DOC-020: L0 records must have the cell_charter table (or placeholder).

    The cell_charter table is the In Scope / Out of Scope / Adjacent
    table under "## 3. Behavioral Boundaries (Cell Charter)". For L0,
    the table is considered populated iff either:
      (a) the YAML record has a non-empty cell_charter.inclusions,
          cell_charter.exclusions, and cell_charter.adjacent_boundaries
          (any of them), OR
      (b) the README contains one of the placeholder strings.
    """
    has_yaml_charter = False
    charter = yaml_record.get("cell_charter")
    if isinstance(charter, dict):
        for key in ("inclusions", "exclusions", "adjacent_boundaries"):
            v = charter.get(key)
            if isinstance(v, list) and len(v) > 0:
                has_yaml_charter = True
                break
    has_placeholder = any(p in readme_text for p in PENDING_EXT04_PATTERNS)
    has_three_rows = False
    m = re.search(
        r"^##\s*(?:\d+\.\s*)?Behavioral Boundaries",
        readme_text, flags=re.MULTILINE,
    )
    if m is not None:
        after = readme_text[m.end():]
        next_h2 = re.search(r"^##\s", after, flags=re.MULTILINE)
        section_text = after if next_h2 is None else after[:next_h2.start()]
        # The EXT-07 generator emits the cell_charter as a single
        # table with three rows: "In Scope (inclusions)", "Out of
        # Scope (exclusions)", and "Adjacent (adjacent_boundaries)".
        # We require all three scope-type labels in the table rows.
        scope_labels = ("In Scope", "Out of Scope", "Adjacent")
        if all(re.search(rf"\|\s*{lbl}\b", section_text)
               for lbl in scope_labels):
            has_three_rows = True
    return {
        "has_yaml_charter": has_yaml_charter,
        "has_placeholder": has_placeholder,
        "has_three_rows": has_three_rows,
        "populated": has_yaml_charter or has_placeholder or has_three_rows,
    }


# -----------------------------------------------------------------------------
# Findings
# -----------------------------------------------------------------------------


def evaluate(records: Iterable[tuple[Path, dict]]) -> list[dict]:
    """Run DOC-016..020 against every (path, record) pair.

    Returns a list of findings:
        [{"rule": "DOC-016", "record_id": ..., "diagnostic": ...,
          "advisory": True, "level": "L0", "profile": "..."}, ...]
    Empty list == all pass.
    """
    findings: list[dict] = []

    for path, record in records:
        rec_id = record.get("id") or path.parent.name
        profile = _resolve_profile(record)
        readme_path = path.parent / "README.md"

        if not readme_path.is_file():
            # No README: nothing to validate here. DOC-001 is the
            # owner rule and is already enforced by gate [21]. We
            # simply skip.
            continue

        readme_text = readme_path.read_text(encoding="utf-8")
        level = _resolve_level(record) or "?"

        if profile is None:
            findings.append({
                "rule": "DOC-016",
                "record_id": rec_id,
                "level": level,
                "profile": None,
                "diagnostic": "no profile resolved for (type, level); "
                               "EXT-07 template not applicable",
                "advisory": True,
            })
            continue

        # DOC-016: every required section-id is present in the README.
        missing = [
            section_id for section_id in profile["required_section_ids"]
            if not _section_present(readme_text, section_id)
        ]
        if missing:
            findings.append({
                "rule": "DOC-016",
                "record_id": rec_id,
                "level": level,
                "profile": profile["profile_id"],
                "diagnostic": f"missing required section(s): {', '.join(missing)}",
                "missing_sections": missing,
                "advisory": True,
            })

        # DOC-017: Properties table populated.
        if not _properties_table_populated(readme_text):
            findings.append({
                "rule": "DOC-017",
                "record_id": rec_id,
                "level": level,
                "profile": profile["profile_id"],
                "diagnostic": "Properties table is missing or has no data rows",
                "advisory": True,
            })

        # DOC-018: Relationships table present (L0/L1 only).
        # L2-L4 (Process, Activity, Task) are leaves; the generator
        # omits the Relationships table because the relationships are
        # surfaced in the Properties table. See
        # _relationships_table_present() for the rationale.
        if level in ("L0", "L1") and not _relationships_table_present(readme_text):
            findings.append({
                "rule": "DOC-018",
                "record_id": rec_id,
                "level": level,
                "profile": profile["profile_id"],
                "diagnostic": "Relationships table is missing",
                "advisory": True,
            })

        # DOC-019: L0 only -- metrics block populated.
        if level == "L0":
            state = _metrics_block_state(readme_text, record)
            if not state["populated"]:
                findings.append({
                    "rule": "DOC-019",
                    "record_id": rec_id,
                    "level": level,
                    "profile": profile["profile_id"],
                    "diagnostic": "L0 record has no metrics block and no "
                                   "(Pending EXT-04) placeholder",
                    "advisory": True,
                })

        # DOC-020: L0 only -- cell_charter table populated.
        if level == "L0":
            state = _cell_charter_table_state(readme_text, record)
            if not state["populated"]:
                findings.append({
                    "rule": "DOC-020",
                    "record_id": rec_id,
                    "level": level,
                    "profile": profile["profile_id"],
                    "diagnostic": "L0 record has no cell_charter table and no "
                                   "(Pending EXT-04) placeholder",
                    "advisory": True,
                })

    return findings


# -----------------------------------------------------------------------------
# Catalog walk + manifest emission
# -----------------------------------------------------------------------------


def _walk_records(catalog_root: Path):
    """Yield (yaml_path, record_dict) for every record under the catalog root."""
    for yaml_path in sorted(catalog_root.rglob("*.yaml")):
        if not yaml_path.is_file():
            continue
        try:
            with yaml_path.open(encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        # Only process records that have an `id` field (i.e., real records;
        # auxiliary files like profiles, registries, etc. are skipped).
        if not isinstance(data.get("id"), str):
            continue
        yield yaml_path, data


def _build_manifest(catalog_root: Path) -> dict:
    """Build the validation manifest for the catalog at catalog_root.

    The manifest has:
      - manifest_schema_version
      - generated_at
      - generator + parent_cr
      - records: list of per-record validation state
      - summary: per-rule tally
    """
    import datetime as _dt

    records_state: list[dict] = []
    findings: list[dict] = []
    rule_tally: dict[str, int] = {
        "DOC-016": 0, "DOC-017": 0, "DOC-018": 0, "DOC-019": 0, "DOC-020": 0,
    }
    level_tally: dict[str, int] = {"L0": 0, "L1": 0, "L2": 0, "L3": 0, "L4": 0, "?": 0}

    for path, record in _walk_records(catalog_root):
        rec_id = record.get("id") or path.parent.name
        level = _resolve_level(record) or "?"
        profile = _resolve_profile(record)
        readme_path = path.parent / "README.md"
        level_tally[level] = level_tally.get(level, 0) + 1

        record_state: dict = {
            "record_id": rec_id,
            "level": level,
            "type": record.get("type"),
            "profile": profile["profile_id"] if profile else None,
            "yaml_path": str(path.relative_to(catalog_root)),
            "readme_path": str(readme_path.relative_to(catalog_root)),
            "readme_exists": readme_path.is_file(),
            "rules": {},
        }

        if readme_path.is_file():
            readme_text = readme_path.read_text(encoding="utf-8")
            record_state["rules"]["DOC-016"] = {
                "pass": _section_present(readme_text, "header-identity-table")
                        and all(
                            _section_present(readme_text, section_id)
                            for section_id in (profile["required_section_ids"]
                                        if profile else [])
                        ),
            }
            record_state["rules"]["DOC-017"] = {
                "pass": _properties_table_populated(readme_text),
            }
            record_state["rules"]["DOC-018"] = {
                "pass": level not in ("L0", "L1")
                        or _relationships_table_present(readme_text),
                "note": "L2-L4 are leaves; Relationships table is optional",
            }
            if level == "L0":
                metrics_state = _metrics_block_state(readme_text, record)
                record_state["rules"]["DOC-019"] = {
                    "pass": metrics_state["populated"],
                    "details": metrics_state,
                }
                charter_state = _cell_charter_table_state(readme_text, record)
                record_state["rules"]["DOC-020"] = {
                    "pass": charter_state["populated"],
                    "details": charter_state,
                }

        records_state.append(record_state)

    # Findings
    findings = evaluate(_walk_records(catalog_root))
    for f in findings:
        rule_tally[f["rule"]] = rule_tally.get(f["rule"], 0) + 1

    summary = {
        "total_records": len(records_state),
        "by_level": level_tally,
        "by_rule": rule_tally,
        "total_findings": len(findings),
        "advisory_findings": len(findings),  # all findings are advisory
    }

    return {
        "manifest_schema_version": MANIFEST_SCHEMA_VERSION,
        "generated_at": _dt.date.today().isoformat(),
        "generator": MANIFEST_GENERATOR,
        "parent_cr": MANIFEST_PARENT_CR,
        "catalog_root": str(catalog_root),
        "summary": summary,
        "findings": findings,
        "records": records_state,
    }


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--catalog-root", default=".",
        help="Path to the catalog root (default: current directory).",
    )
    parser.add_argument(
        "--manifest-dir", default=None,
        help="Directory to write the manifest artefacts. "
             "Default: <catalog-root>/reconciliation/.",
    )
    parser.add_argument(
        "--self-test", action="store_true",
        help="Run self-test with synthetic fixtures and exit.",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Emit JSON summary to stdout (in addition to writing the manifest).",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    catalog_root = Path(args.catalog_root).resolve()
    if not catalog_root.is_dir():
        sys.stderr.write(f"ERROR: catalog root {catalog_root} is not a directory.\n")
        return 2

    manifest = _build_manifest(catalog_root)

    manifest_dir = Path(args.manifest_dir).resolve() if args.manifest_dir \
        else catalog_root / "reconciliation"
    manifest_dir.mkdir(parents=True, exist_ok=True)

    json_path = manifest_dir / "validation-manifest.json"
    yaml_path = manifest_dir / "validation-manifest.yaml"

    json_path.write_text(json.dumps(manifest, indent=2, sort_keys=False), encoding="utf-8")

    # YAML emission: skip the records list (verbose per-record state) so
    # the human-readable YAML is a summary document. The full per-record
    # state is in the JSON.
    yaml_emit = {
        k: v for k, v in manifest.items() if k != "records"
    }
    yaml_path.write_text(
        yaml.safe_dump(yaml_emit, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )

    if args.json:
        # Emit just the summary, not the full per-record list
        print(json.dumps({k: v for k, v in manifest.items() if k != "records"}, indent=2))
    else:
        s = manifest["summary"]
        print(f"Validation Manifest (CR-BP-94-EXT-04): {s['total_records']} records, "
              f"{s['total_findings']} advisory findings")
        print(f"  By level: {s['by_level']}")
        print(f"  By rule:  {s['by_rule']}")
        print(f"  Manifest: {json_path}")
        print(f"  YAML:     {yaml_path}")
    return 0


def _self_test() -> int:
    """Self-test: synthetic fixtures covering the 5 rules.

    Runs the in-process `evaluate()` against minimal synthetic records
    and verifies the DOC-016..020 findings are emitted correctly.
    """
    from tests.test_validate_readme_structure import run_self_test
    return run_self_test()


if __name__ == "__main__":
    sys.exit(main())
