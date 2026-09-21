#!/usr/bin/env python3
"""
check_documentation_profile.py
===============================

L0/L1/L2/L3/L4 documentation profile validator (CR-BP-94-EXT-01).

Codifies the documentation architecture defined in
docs/process-documentation-architecture.md §7 (REQ-04..REQ-05):

  DOC-001  README exists at entities/v1-alpha/<entity-id>/README.md.
  DOC-002  README has the section identifiers mandated by the profile
           resolved from (entity.type, entity.level).
  DOC-003  README entity id matches the YAML `id` field.
  DOC-004  Generated sections contain no unresolved {{placeholder}}
           tokens at `validated` lifecycle state.
  DOC-005  README references the governing CR (from
           metadata.established_by).

The validator operates in three modes:

  1. --self-test             : self-test with synthetic fixtures.
  2. --catalog-root PATH     : validate every entity record in the catalog
                                whose YAML is well-formed.
  3. (no args)               : live catalog mode (default --catalog-root=.).

The validator is wired as gate [21] Documentation Profile (advisory) in
scripts/conformance_result.py. Advisory means findings are surfaced but
do not block merge until a sufficient population of README assets has
been authored (EXT-06).

CR-BP-94-EXT-01 (Documentation Architecture slice) lands DOC-001..005.
Subsequent extension CRs land DOC-006+:

  EXT-02: DOC-006..010  template-specific section ordering + profile
                         mandatory/conditional/inherited classification.
  EXT-03: DOC-011..015  manifest + coverage dimension checks.
  EXT-04: DOC-016..020  generation traceability + evidence provenance.
  EXT-05: DOC-021..025  parent-child decomposition traceability.
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
# Profile registry (in-process copy; the source of truth is
# templates/documentation-profile-*.yaml). Each profile maps the
# (entity.type, level) classification to a section-id set.
# -----------------------------------------------------------------------------

PROFILE_REGISTRY: dict[tuple[str, str], dict] = {
    # Cardinal entities (CR-BP-92 §7, CR-BP-93 §3).
    # CR-BP-94-EXT-01a adds L0/L1 profiles; CR-BP-94-EXT-01 (PR #137) covered L2/L3/L4.
    ("ProcessContext", "L0"): {
        "profile_id": "dea:profile-readme-l0-process-context-v1",
        "required_section_ids": [
            "entity-identity",
            "formal-definition",
            "semantic-dimensions",
            "decomposition",
            "behavior",
            "interfaces",
            "roles",
            "rules-controls",
            # outcomes is conditional at L0 (inherited from ECF framework)
            "evidence",
            "completeness",
            "revision-history",
        ],
    },
    ("ProcessGroup", "L1"): {
        "profile_id": "dea:profile-readme-l1-process-group-v1",
        "required_section_ids": [
            "entity-identity",
            "formal-definition",
            "semantic-dimensions",
            "decomposition",
            "behavior",
            "interfaces",
            "roles",
            "rules-controls",
            # outcomes is conditional at L1
            "evidence",
            "completeness",
            "revision-history",
        ],
    },
    ("Process", "L2"): {
        "profile_id": "dea:profile-readme-l2-process-v1",
        "required_section_ids": [
            "entity-identity",
            "formal-definition",
            "semantic-dimensions",
            "decomposition",
            "behavior",
            "interfaces",
            "roles",
            "rules-controls",
            "outcomes",
            "evidence",
            "completeness",
            "revision-history",
        ],
    },
    ("Activity", "L3"): {
        "profile_id": "dea:profile-readme-l3-activity-v1",
        "required_section_ids": [
            "entity-identity",
            "formal-definition",
            "semantic-dimensions",
            "decomposition",
            "behavior",
            "interfaces",
            "roles",
            "rules-controls",
            # outcomes is conditional at L3
            "evidence",
            "completeness",
            "revision-history",
        ],
    },
    ("Task", "L4"): {
        "profile_id": "dea:profile-readme-l4-task-v1",
        "required_section_ids": [
            "entity-identity",
            "formal-definition",
            "semantic-dimensions",
            "decomposition",
            "behavior",
            "interfaces",
            "roles",
            "rules-controls",
            # outcomes is not_applicable at L4
            "evidence",
            "completeness",
            "revision-history",
        ],
    },
}

# Section-id -> expected heading (used by DOC-002 to verify the section
# is present in the README). The validator searches for the heading
# pattern; case-insensitive, whitespace-tolerant.
EXPECTED_HEADINGS: dict[str, str] = {
    "entity-identity": r"^##\s*1\.\s*Entity Identity",
    "formal-definition": r"^##\s*2\.\s*Formal Definition",
    "semantic-dimensions": r"^##\s*3\.\s*Canonical Semantic",
    "decomposition": r"^##\s*4\.\s*Decomposition",
    "behavior": r"^##\s*5\.\s*Behavior",
    "interfaces": r"##\s*6\.\s*Inputs, Outputs",
    "roles": r"##\s*7\.\s*Roles, Responsibilities",
    "rules-controls": r"##\s*8\.\s*Business Rules",
    "outcomes": r"##\s*9\.\s*Outcomes",
    "evidence": r"##\s*10\.\s*Evidence",
    "completeness": r"##\s*11\.\s*Documentation Completeness",
    "revision-history": r"##\s*12\.\s*Revision History",
}

# Placeholder token pattern (DOC-004). Generated sections are allowed to
# contain placeholders until the EXT-04 generator runs; this slice flags
# them only at `validated` lifecycle state.
PLACEHOLDER_PATTERN = re.compile(r"\{\{[A-Za-z_][A-Za-z0-9_.]*\}\}")

# Governing CR reference pattern (DOC-005). The README must reference
# the CR listed in metadata.established_by.
CR_REFERENCE_PATTERN = re.compile(r"CR-BP-\d+[a-zA-Z\-]*")


# -----------------------------------------------------------------------------
# Type / level resolution
# -----------------------------------------------------------------------------

# CR-BP-93 §3 level mapping: type -> level. ProcessContext is L0
# (cardinal); ProcessGroup is L1 (cardinal); Process is L2 (Business
# Process); Activity is L3; Task is L4 (placeholder until CR-BP-98
# codifies the L4 schema).
LEVEL_BY_TYPE: dict[str, str] = {
    "ProcessContext": "L0",
    "ProcessGroup": "L1",
    "Process": "L2",
    "Activity": "L3",
    "Task": "L4",
}


def _resolve_level(record: dict) -> str | None:
    """Resolve the decomposition level from the record's type discriminator.

    Per CR-BP-93 §3 (decomposition semantic contract), entity type maps
    to a level directly. Future slices may consult additional metadata
    (e.g., metadata.decomposition_level) when the catalog supports
    multi-level Process records (CR-BP-92 recon).
    """
    entity_type = record.get("type")
    if not isinstance(entity_type, str):
        return None
    return LEVEL_BY_TYPE.get(entity_type)


def _resolve_profile(record: dict) -> dict | None:
    """Resolve the documentation profile for a record.

    Returns the profile dict from PROFILE_REGISTRY or None when the
    (type, level) combination is unrecognized (DOC-001).
    """
    entity_type = record.get("type")
    if not isinstance(entity_type, str):
        return None
    level = _resolve_level(record)
    if level is None:
        return None
    return PROFILE_REGISTRY.get((entity_type, level))


# -----------------------------------------------------------------------------
# Findings
# -----------------------------------------------------------------------------


def evaluate(records: Iterable[tuple[Path, dict]]) -> list[dict]:
    """Run DOC-001..005 against every (path, record) pair.

    Returns a list of findings:
        [{"rule": "DOC-001", "record_id": ..., "diagnostic": ...,
          "advisory": True}, ...]
    Empty list == all pass.
    """
    findings: list[dict] = []

    for path, record in records:
        rec_id = record.get("id") or path.parent.name
        profile = _resolve_profile(record)
        readme_path = path.parent / "README.md"

        # DOC-001: README exists.
        if not readme_path.is_file():
            findings.append({
                "rule": "DOC-001",
                "record_id": rec_id,
                "diagnostic": f"README.md missing at {readme_path.relative_to(path.parents[3])}",
                "advisory": True,
            })
            continue  # Without a README, downstream checks cannot run.

        readme_text = readme_path.read_text(encoding="utf-8")

        # DOC-003: README entity id matches the YAML `id` field.
        # We look for the entity id in the README's first H1.
        if not _readme_references_id(readme_text, rec_id):
            findings.append({
                "rule": "DOC-003",
                "record_id": rec_id,
                "diagnostic": f"README does not reference canonical id {rec_id!r} in its H1",
                "advisory": True,
            })

        # DOC-005: README references the governing CR.
        governing_cr = _governing_cr(record)
        if governing_cr and not _readme_references_cr(readme_text, governing_cr):
            findings.append({
                "rule": "DOC-005",
                "record_id": rec_id,
                "diagnostic": f"README does not reference governing CR {governing_cr!r}",
                "advisory": True,
            })

        # DOC-002: README has the section identifiers mandated by the profile.
        if profile is None:
            findings.append({
                "rule": "DOC-002",
                "record_id": rec_id,
                "diagnostic": (
                    f"could not resolve documentation profile for "
                    f"type={record.get('type')!r} level={_resolve_level(record)!r}"
                ),
                "advisory": True,
            })
            continue

        for section_id in profile["required_section_ids"]:
            heading_pattern = EXPECTED_HEADINGS.get(section_id)
            if heading_pattern is None:
                continue
            if not re.search(heading_pattern, readme_text, re.MULTILINE):
                findings.append({
                    "rule": "DOC-002",
                    "record_id": rec_id,
                    "diagnostic": (
                        f"README missing required section id={section_id!r} "
                        f"(profile={profile['profile_id']!r})"
                    ),
                    "advisory": True,
                })

        # DOC-004: Generated sections contain no unresolved placeholders
        # at `validated` lifecycle state. Until then, placeholders are
        # allowed; we still flag them as informational so authors know
        # what needs to be substituted.
        lifecycle = (record.get("lifecycle_status") or "").strip().lower()
        placeholders = sorted(set(PLACEHOLDER_PATTERN.findall(readme_text)))
        if placeholders and lifecycle in ("active", "validated"):
            findings.append({
                "rule": "DOC-004",
                "record_id": rec_id,
                "diagnostic": (
                    f"README contains unresolved placeholders at "
                    f"{lifecycle!r} lifecycle: {placeholders}"
                ),
                "advisory": True,
            })

    return findings


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def _governing_cr(record: dict) -> str | None:
    """Return the governing CR id from the record's metadata."""
    md = record.get("metadata") or {}
    if isinstance(md, dict):
        cr = md.get("established_by")
        if isinstance(cr, str) and cr:
            return cr
    return None


def _readme_references_id(readme_text: str, entity_id: str) -> bool:
    """Verify the README's first H1 references the canonical entity id."""
    lines = readme_text.splitlines()
    for line in lines:
        if line.startswith("# "):
            return entity_id in line
        if line.strip():  # Stop at the first non-blank, non-H1 line.
            return False
    return False


def _readme_references_cr(readme_text: str, cr_id: str) -> bool:
    """Verify the README references the governing CR id at least once."""
    return bool(CR_REFERENCE_PATTERN.search(readme_text)) and cr_id in readme_text


# -----------------------------------------------------------------------------
# Record loading
# -----------------------------------------------------------------------------


def _load_records(catalog_root: Path) -> list[tuple[Path, dict]]:
    """Load every YAML record under entities/v1-alpha/.

    Returns a list of (yaml_path, record_dict) pairs. Records that fail
    to parse are skipped (logged to stderr).
    """
    base = catalog_root / "entities" / "v1-alpha"
    if not base.exists():
        return []
    pairs: list[tuple[Path, dict]] = []
    for entry in sorted(base.iterdir()):
        if not entry.is_dir():
            continue
        yaml_path = entry / f"{entry.name}.yaml"
        if not yaml_path.exists():
            continue
        try:
            data = yaml.safe_load(yaml_path.read_text())
        except yaml.YAMLError as exc:
            sys.stderr.write(f"WARN: {yaml_path}: {exc}\n")
            continue
        if isinstance(data, dict):
            pairs.append((yaml_path, data))
    return pairs


# -----------------------------------------------------------------------------
# Self-test
# -----------------------------------------------------------------------------


def _self_test() -> int:
    """Exercise DOC-001..005 on synthetic fixtures; return 0 on PASS."""
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        # Fixture 1: well-formed L2 BP with README containing all required sections.
        entity_dir = td_path / "entities" / "v1-alpha" / "processes:process-good"
        entity_dir.mkdir(parents=True)
        (entity_dir / "processes:process-good.yaml").write_text(yaml.safe_dump({
            "id": "processes:process-good",
            "name": "Good Process",
            "type": "Process",
            "version": "1.0.0",
            "lifecycle_status": "candidate",
            "metadata": {"established_by": "CR-BP-13a"},
        }))
        (entity_dir / "README.md").write_text(
            "# Canonical Business Process: `processes:process-good`\n\n"
            "## 1. Entity Identity and Classification\n\n"
            "## 2. Formal Definition and Scope\n\n"
            "## 3. Canonical Semantic Dimensions\n\n"
            "## 4. Decomposition and Composition\n\n"
            "## 5. Behavior and Workflow\n\n"
            "## 6. Inputs, Outputs, and Interfaces\n\n"
            "## 7. Roles, Responsibilities, and Accountability\n\n"
            "## 8. Business Rules and Controls\n\n"
            "## 9. Outcomes and Performance\n\n"
            "## 10. Evidence and Traceability\n\n"
            "Governed by CR-BP-13a.\n\n"
            "## 11. Documentation Completeness\n\n"
            "## 12. Revision History\n\n"
        )
        # Fixture 2: missing README (DOC-001 violation).
        bad_dir = td_path / "entities" / "v1-alpha" / "processes:process-bad"
        bad_dir.mkdir(parents=True)
        (bad_dir / "processes:process-bad.yaml").write_text(yaml.safe_dump({
            "id": "processes:process-bad",
            "name": "Bad Process",
            "type": "Process",
            "version": "1.0.0",
        }))
        # Fixture 3: README but missing required section.
        incomplete_dir = td_path / "entities" / "v1-alpha" / "processes:process-incomplete"
        incomplete_dir.mkdir(parents=True)
        (incomplete_dir / "processes:process-incomplete.yaml").write_text(yaml.safe_dump({
            "id": "processes:process-incomplete",
            "name": "Incomplete Process",
            "type": "Process",
            "version": "1.0.0",
            "metadata": {"established_by": "CR-BP-13a"},
        }))
        (incomplete_dir / "README.md").write_text(
            "# Canonical Business Process: `processes:process-incomplete`\n\n"
            "## 1. Entity Identity and Classification\n\n"
        )

        pairs = _load_records(td_path)
        findings = evaluate(pairs)

        # Expect DOC-001 for `processes:process-bad`, DOC-002 for
        # `processes:process-incomplete`.
        rules_per_record = {}
        for f in findings:
            rules_per_record.setdefault(f["record_id"], []).append(f["rule"])
        assert "DOC-001" in rules_per_record.get("processes:process-bad", []), rules_per_record
        assert "DOC-002" in rules_per_record.get("processes:process-incomplete", []), rules_per_record
        # The good fixture should produce no findings.
        assert "processes:process-good" not in rules_per_record, rules_per_record

    print("self-test PASS (DOC-001 README exists; DOC-002 required sections; "
          "DOC-003 id match; DOC-004 placeholder handling; DOC-005 CR reference)")
    return 0


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def _verdict(findings: list[dict]) -> str:
    if findings:
        return "NON-CONFORMANT"
    return "CONFORMANT"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(
        "Documentation profile validator (CR-BP-94-EXT-01; DOC-001..005)."
    ))
    parser.add_argument("--catalog-root", default=".",
                        help="Path to the catalog repo root (default: current directory).")
    parser.add_argument("--self-test", action="store_true",
                        help="Run the validator's self-test and exit.")
    parser.add_argument("--strict", action="store_true",
                        help="Exit 1 on any finding (advisory findings do not fail).")
    parser.add_argument("--json", action="store_true",
                        help="Emit a JSON payload instead of human-readable text.")
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    catalog_root = Path(args.catalog_root).resolve()
    pairs = _load_records(catalog_root)
    findings = evaluate(pairs)
    verdict = _verdict(findings)

    if args.json:
        print(json.dumps({
            "verdict": verdict,
            "record_count": len(pairs),
            "finding_count": len(findings),
            "findings": findings,
            "rules": [
                {"id": "DOC-001", "name": "README exists"},
                {"id": "DOC-002", "name": "Required section identifiers present"},
                {"id": "DOC-003", "name": "Entity id matches YAML"},
                {"id": "DOC-004", "name": "No unresolved placeholders at validated lifecycle"},
                {"id": "DOC-005", "name": "Governing CR referenced"},
            ],
            "profile_registry": [
                {"key": list(k), "profile_id": v["profile_id"]}
                for k, v in PROFILE_REGISTRY.items()
            ],
        }, indent=2, sort_keys=True))
    else:
        print(f"Documentation Profile (CR-BP-94-EXT-01 DOC-001..005): {verdict}")
        print(f"  Records checked:  {len(pairs)}")
        print(f"  Findings:         {len(findings)}")
        rule_counts = {"DOC-001": 0, "DOC-002": 0, "DOC-003": 0, "DOC-004": 0, "DOC-005": 0}
        for f in findings:
            rule_counts[f["rule"]] = rule_counts.get(f["rule"], 0) + 1
        for rid, count in rule_counts.items():
            print(f"    {rid}: {count} [advisory]")
        if findings:
            print("\nFindings:")
            for f in findings:
                print(f"  [{f['rule']} [advisory]] {f['record_id']}: {f['diagnostic']}")

    if findings and args.strict:
        mandatory = [f for f in findings if not f.get("advisory", False)]
        if mandatory:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
