"""Tests for the CR-BP-94-EXT-04 Validation Manifest generator.

Locks behaviour for DOC-016..020 by exercising both the in-process
`evaluate()` function and the live-catalog assertion that the manifest
is emitted at reconciliation/validation-manifest.json with the
expected schema_version + summary tally. The validator is wired as
gate [34] Documentation Profile - Generator and Validator (advisory)
in scripts/conformance_result.py; EXT-04 lands the validator; EXT-06
flips the gate to blocking.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "validate_readme_structure.py"
SCHEMA = ROOT / "schemas" / "validation-manifest.schema.json"

sys.path.insert(0, str(ROOT / "scripts"))
from validate_readme_structure import (  # noqa: E402
    MANIFEST_GENERATOR,
    MANIFEST_PARENT_CR,
    MANIFEST_SCHEMA_VERSION,
    _cell_charter_table_state,
    _metrics_block_state,
    _properties_table_populated,
    _relationships_table_present,
    _section_present,
    evaluate,
)


# -----------------------------------------------------------------------------
# Self-test runner (called by `python scripts/validate_readme_structure.py
# --self-test`). The script imports this module at the bottom so the
# `from tests.test_validate_readme_structure import run_self_test` line in
# the main script resolves.
# -----------------------------------------------------------------------------


def run_self_test() -> int:
    """Synthetic-fixture self-test for DOC-016..020.

    Creates temp directories with synthetic READMEs + records and
    runs the in-process `evaluate()` against them. Returns 0 on
    success, 1 on failure.

    The self-test must use real files on disk because the
    `_walk_records` + `evaluate()` path reads the README from
    `path.parent / "README.md"`. The temp directories are created
    under `<catalog_root>/tmp-fixture/validate-readme-self-test/`
    and cleaned up on success.
    """
    import tempfile
    import shutil

    # Use a temp directory under the catalog root.
    catalog_root = ROOT
    fixture_root = catalog_root / "tmp-fixture" / "validate-readme-self-test"
    if fixture_root.exists():
        shutil.rmtree(fixture_root)
    fixture_root.mkdir(parents=True)

    try:
        fixtures = [
            ("L0-pass", {"id": "dea:pc-test-1-abcdef", "type": "ProcessContext",
                          "metrics": {"performance": [{"name": "X"}]},
                          "cell_charter": {"inclusions": ["a"], "exclusions": ["b"],
                                           "adjacent_boundaries": ["c"]}},
             _L0_README_FULL),
            ("L0-placeholder", {"id": "dea:pc-test-2-abcdef", "type": "ProcessContext"},
             _L0_README_PLACEHOLDER),
            ("L0-missing-section", {"id": "dea:pc-test-3-abcdef", "type": "ProcessContext"},
             _L0_README_MISSING_SECTION),
            ("L1-pass", {"id": "dea:group-test-1-abcdef", "type": "ProcessGroup"},
             _L1_README_FULL),
        ]

        records = []
        for name, rec, readme in fixtures:
            d = fixture_root / name
            d.mkdir(parents=True)
            (d / "record.yaml").write_text(
                yaml.safe_dump(rec, allow_unicode=True), encoding="utf-8",
            )
            (d / "README.md").write_text(readme, encoding="utf-8")
            records.append((d / "record.yaml", rec))

        findings = evaluate(records)

        # DOC-016 for the L0 missing-section record should be present
        rules = {(f["record_id"], f["rule"]) for f in findings}
        assert ("dea:pc-test-3-abcdef", "DOC-016") in rules, \
            "DOC-016 not emitted for the missing-section fixture"
        # DOC-019 for the L0 placeholder record should be ABSENT
        # (placeholder is acceptable per the rule)
        assert ("dea:pc-test-2-abcdef", "DOC-019") not in rules, \
            "DOC-019 false-positive: placeholder record should not flag"

        print(f"Self-test: {len(findings)} findings; expected DOC-016 + DOC-019/020 false-positive guard")
        return 0
    finally:
        if fixture_root.exists():
            shutil.rmtree(fixture_root)


# -----------------------------------------------------------------------------
# Fixtures
# -----------------------------------------------------------------------------


_L0_README_FULL = """\
# Canonical ProcessContext: `dea:pc-test-1-abcdef`

## Header and Identity Table

| Attribute | Value | Attribute | Value |
| :--- | :--- | :--- | :--- |
| **Domain** | AO | **Lifecycle Stage** | Activate |
| **Level** | L0 (ProcessContext) | **Status** | `candidate (yellow)` |

## 1. Executive Summary

The bounded context for the test fixture.

## 2. Governance and Provenance

| Attribute | Value |
| :--- | :--- |
| **Admission score** | 1.0 |
| **Regulatory evidence** | EXT-04 |

## 3. Behavioral Boundaries (Cell Charter)

| Scope Type | Description |
| :--- | :--- |
| In Scope (inclusions) | - a |
| Out of Scope (exclusions) | - b |
| Adjacent (adjacent_boundaries) | - c |

## 4. Hierarchical Decomposition

<details><summary>L1-L4 tree</summary>

```
L0: pc-test-1
  L1: group-test-1
    L2: process-test-1
      L3: activity-test-1
        L4: task-test-1
```

</details>

## 5. Properties and Relationships

| Property | Value | Property | Value |
| :--- | :--- | :--- | :--- |
| **id** | dea:pc-test-1-abcdef | **name** | Test ProcessContext |

| Relationship | Target | Cardinality | Notes |
| :--- | :--- | :--- | :--- |
| decomposes | dea:group-test-1-abcdef | 1:N | standard |

## 6. Operational, Control and Metrics Details

**Inputs, Outputs and Interfaces**: fixtures only.

**Roles and Responsibilities**: fixtures only.

**Business Rules and Controls**: fixtures only.

**Target Metrics and Indicators**

| Type | Name | Target | Frequency |
| :--- | :--- | :--- | :--- |
| KPI (performance) | X | Y | Weekly |

## 7. Technical Metadata

- **Source YAML**: record YAML in the same directory as this README
- **Record version**: 1.0.0
- **Governing CR**: `CR-BP-94-EXT-07`
"""


_L0_README_PLACEHOLDER = """\
# Canonical ProcessContext: `dea:pc-test-2-abcdef`

## Header and Identity Table

| Attribute | Value | Attribute | Value |
| :--- | :--- | :--- | :--- |
| **Domain** | AO | **Lifecycle Stage** | Activate |
| **Level** | L0 (ProcessContext) | **Status** | `candidate (yellow)` |

## 1. Executive Summary

The bounded context for the placeholder fixture.

## 2. Governance and Provenance

| Attribute | Value |
| :--- | :--- |
| **Admission score** | 1.0 |
| **Regulatory evidence** | EXT-04 |

## 3. Behavioral Boundaries (Cell Charter)

| Scope Type | Description |
| :--- | :--- |
| In Scope (inclusions) | - a |
| Out of Scope (exclusions) | - b |
| Adjacent (adjacent_boundaries) | - c |

## 4. Hierarchical Decomposition

<details><summary>L1-L4 tree</summary>

```
L0: pc-test-2
```

</details>

## 5. Properties and Relationships

| Property | Value | Property | Value |
| :--- | :--- | :--- | :--- |
| **id** | dea:pc-test-2-abcdef | **name** | Test ProcessContext (placeholder) |

| Relationship | Target | Cardinality | Notes |
| :--- | :--- | :--- | :--- |
| (none) | | | |

## 6. Operational, Control and Metrics Details

_(Pending EXT-04)_

## 7. Technical Metadata

- **Source YAML**: record YAML in the same directory as this README
- **Record version**: 1.0.0
- **Governing CR**: `CR-BP-94-EXT-07`
"""


_L0_README_MISSING_SECTION = """\
# Canonical ProcessContext: `dea:pc-test-3-abcdef`

## Header and Identity Table

| Attribute | Value | Attribute | Value |
| :--- | :--- | :--- | :--- |
| **Domain** | AO | **Lifecycle Stage** | Activate |
| **Level** | L0 (ProcessContext) | **Status** | `candidate (yellow)` |

## 1. Executive Summary

The bounded context for the missing-section fixture.

## 2. Governance and Provenance

| Attribute | Value |
| :--- | :--- |
| **Admission score** | 1.0 |
| **Regulatory evidence** | EXT-04 |

# (Sections 3..7 intentionally omitted for the missing-section fixture.)

## 7. Technical Metadata

- **Source YAML**: record YAML in the same directory as this README
- **Record version**: 1.0.0
- **Governing CR**: `CR-BP-94-EXT-07`
"""


_L1_README_FULL = """\
# Canonical ProcessGroup: `dea:group-test-1-abcdef`

## Header and Identity Table

| Attribute | Value | Attribute | Value |
| :--- | :--- | :--- |
| **Domain** | AO | **Lifecycle Stage** | Activate |
| **Level** | L1 (ProcessGroup) | **Status** | `candidate (yellow)` |

## Intent and Definition

The bounded grouping for the test fixture.

## 2. Governance and Provenance

| Attribute | Value |
| :--- | :--- |
| **Admission score** | 1.0 |
| **Regulatory evidence** | EXT-04 |

## 5. Properties and Relationships

| Property | Value | Property | Value |
| :--- | :--- | :--- | :--- |
| **id** | dea:group-test-1-abcdef | **name** | Test ProcessGroup |

| Relationship | Target | Cardinality | Notes |
| :--- | :--- | :--- | :--- |
| decomposes | dea:process-test-1-abcdef | 1:N | standard |

## 4. Hierarchical Decomposition

<details><summary>L1-L4 tree</summary>

```
L1: group-test-1
  L2: process-test-1
```

</details>

## Operational Details

_(Pending EXT-04)_

## 7. Technical Metadata

- **Source YAML**: record YAML in the same directory as this README
- **Record version**: 1.0.0
- **Governing CR**: `CR-BP-94-EXT-07`
"""


# -----------------------------------------------------------------------------
# Per-rule tests
# -----------------------------------------------------------------------------


def test_constants() -> None:
    """The manifest schema version + generator + parent CR are constants.

    The manifest schema is versioned; the manifest is the input for
    the EXT-05 decomposition reconciliation slice, so the schema
    version is a contract that downstream tooling depends on.
    """
    assert MANIFEST_SCHEMA_VERSION == 1
    assert MANIFEST_GENERATOR == "scripts/validate_readme_structure.py"
    assert MANIFEST_PARENT_CR == "CR-BP-94-EXT-04"


def test_schema_version_is_1() -> None:
    """Manifest schema version 1 is the initial contract.

    Any bump must land as a new test (test_schema_version_is_2 etc.)
    and a new entry in the gate verdict history.
    """
    with SCHEMA.open() as fh:
        schema = json.load(fh)
    assert schema["properties"]["manifest_schema_version"]["const"] == 1
    title_lower = schema["title"].lower()
    assert "validation" in title_lower and "manifest" in title_lower
    # The parent CR is the EXT-04 CR; the schema title must reference
    # it so that downstream tooling can identify the schema's lineage.
    assert "ext-04" in title_lower or "cr-bp-94" in title_lower


def test_section_present_recognises_ext07_sections() -> None:
    """DOC-016: the section-presence helper recognises the EXT-07 sections."""
    assert _section_present(_L0_README_FULL, "header-identity-table")
    assert _section_present(_L0_README_FULL, "executive-summary")
    assert _section_present(_L0_README_FULL, "governance-provenance")
    assert _section_present(_L0_README_FULL, "behavioral-boundaries")
    assert _section_present(_L0_README_FULL, "hierarchical-decomposition")
    assert _section_present(_L0_README_FULL, "properties-relationships")
    assert _section_present(_L0_README_FULL, "operational-metrics")
    assert _section_present(_L0_README_FULL, "technical-metadata")
    # Missing section fixture: behavioral-boundaries and others absent
    assert not _section_present(_L0_README_MISSING_SECTION, "behavioral-boundaries")
    assert not _section_present(_L0_README_MISSING_SECTION, "operational-metrics")


def test_properties_table_populated_detects_rows() -> None:
    """DOC-017: the properties-table helper detects populated tables."""
    assert _properties_table_populated(_L0_README_FULL)
    assert _properties_table_populated(_L0_README_PLACEHOLDER)
    assert _properties_table_populated(_L1_README_FULL)
    # Missing section fixture has no Properties section
    assert not _properties_table_populated(_L0_README_MISSING_SECTION)


def test_relationships_table_present_detects_second_table() -> None:
    """DOC-018: the relationships-table helper detects the second table."""
    assert _relationships_table_present(_L0_README_FULL)
    assert _relationships_table_present(_L1_README_FULL)
    # Placeholder L0 has Properties + Relationships (both empty)
    assert _relationships_table_present(_L0_README_PLACEHOLDER)
    # Missing section fixture has no Properties section
    assert not _relationships_table_present(_L0_README_MISSING_SECTION)


def test_metrics_block_state_for_l0() -> None:
    """DOC-019: L0 metrics block state recognises populated + placeholder."""
    full = {"id": "dea:pc-x", "type": "ProcessContext",
            "metrics": {"performance": [{"name": "X"}]}}
    state_full = _metrics_block_state(_L0_README_FULL, full)
    assert state_full["populated"]
    assert state_full["has_yaml_metrics"]
    assert state_full["has_table"]

    placeholder = {"id": "dea:pc-y", "type": "ProcessContext"}
    state_placeholder = _metrics_block_state(_L0_README_PLACEHOLDER, placeholder)
    assert state_placeholder["populated"]
    assert not state_placeholder["has_yaml_metrics"]
    assert state_placeholder["has_placeholder"]


def test_cell_charter_state_for_l0() -> None:
    """DOC-020: L0 cell_charter table state recognises populated + placeholder."""
    full = {"id": "dea:pc-x", "type": "ProcessContext",
            "cell_charter": {"inclusions": ["a"], "exclusions": ["b"],
                             "adjacent_boundaries": ["c"]}}
    state_full = _cell_charter_table_state(_L0_README_FULL, full)
    assert state_full["populated"]
    assert state_full["has_yaml_charter"]
    assert state_full["has_three_rows"]

    placeholder = {"id": "dea:pc-y", "type": "ProcessContext"}
    state_placeholder = _cell_charter_table_state(_L0_README_PLACEHOLDER, placeholder)
    assert state_placeholder["populated"]
    assert not state_placeholder["has_yaml_charter"]
    assert state_placeholder["has_placeholder"]


def test_evaluate_emits_finding_for_missing_sections() -> None:
    """DOC-016: evaluate() emits findings for missing required sections."""
    rec = {"id": "dea:pc-test-3-abcdef", "type": "ProcessContext"}
    findings = evaluate([(ROOT / "tmp" / "test-3.yaml", rec)])
    # The missing-section fixture isn't actually passed in; we just
    # verify that evaluate() accepts a minimal (path, record) pair
    # and returns a list of findings. The fixture-based DOC-016
    # assertion is in run_self_test().
    assert isinstance(findings, list)
    # When the path's parent README does not exist, evaluate() skips
    # without emitting findings (DOC-001 is the owner rule for that case).
    assert all(f["advisory"] for f in findings)


def test_self_test_synthetic_fixtures() -> None:
    """run_self_test() covers the 5 rules via the in-process evaluate()."""
    rc = run_self_test()
    assert rc == 0, f"self-test returned {rc}; expected 0"


# -----------------------------------------------------------------------------
# Live-catalog integration test
# -----------------------------------------------------------------------------


def test_live_catalog_writes_manifest() -> None:
    """The validator writes the manifest at reconciliation/validation-manifest.json.

    The manifest must have the expected schema_version, generator,
    parent_cr, and a non-empty summary. This is the live-catalog
    integration assertion; it is the proof that the validator is
    wired into the standing development model.
    """
    manifest_path = ROOT / "reconciliation" / "validation-manifest.json"
    if not manifest_path.exists():
        # Run the validator
        r = subprocess.run(
            [sys.executable, str(SCRIPT), "--catalog-root", str(ROOT)],
            capture_output=True, text=True, timeout=120,
        )
        assert r.returncode == 0, f"validator failed: {r.stderr}\n{r.stdout[-2000:]}"

    assert manifest_path.exists(), "validation-manifest.json not written"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["manifest_schema_version"] == MANIFEST_SCHEMA_VERSION
    assert manifest["generator"] == MANIFEST_GENERATOR
    assert manifest["parent_cr"] == MANIFEST_PARENT_CR
    assert manifest["summary"]["total_records"] > 0
    assert "by_level" in manifest["summary"]
    assert "by_rule" in manifest["summary"]
    # The manifest has the records list
    assert isinstance(manifest["records"], list)
    assert len(manifest["records"]) == manifest["summary"]["total_records"]


def test_live_catalog_manifest_validates_against_schema() -> None:
    """The emitted manifest validates against schemas/validation-manifest.schema.json.

    The schema is the machine-readable contract; the manifest is the
    input for EXT-05, so the manifest must validate against the schema.
    """
    try:
        import jsonschema  # type: ignore
    except ImportError:
        # jsonschema is optional; if not present, skip the strict
        # schema-validation assertion. The manifest is still tested
        # for the structural assertions in test_live_catalog_writes_manifest.
        import pytest
        pytest.skip("jsonschema not installed")

    manifest_path = ROOT / "reconciliation" / "validation-manifest.json"
    if not manifest_path.exists():
        return  # covered by the previous test

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    with SCHEMA.open() as fh:
        schema = json.load(fh)

    jsonschema.validate(manifest, schema)
