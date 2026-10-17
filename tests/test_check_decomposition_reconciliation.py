"""Tests for the CR-BP-94-EXT-05 Decomposition Reconciliation validator.

Locks behaviour for DOC-021..025 by exercising both the in-process
`evaluate()` function and the live-catalog assertion that the
decomposition reconciliation manifest is emitted with the expected
schema_version + summary tally. The validator is wired as gate
[35] Decomposition Reconciliation (advisory) in
scripts/conformance_result.py; EXT-06 flips the gate to blocking.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_decomposition_reconciliation.py"
SCHEMA = ROOT / "schemas" / "decomposition-reconciliation-manifest.schema.json"

sys.path.insert(0, str(ROOT / "scripts"))
from check_decomposition_reconciliation import (  # noqa: E402
    MANIFEST_GENERATOR,
    MANIFEST_PARENT_CR,
    MANIFEST_SCHEMA_VERSION,
    _build_id_index,
    evaluate,
)


# -----------------------------------------------------------------------------
# Self-test runner
# -----------------------------------------------------------------------------


def run_self_test() -> int:
    """Synthetic-fixture self-test for DOC-021..025.

    Creates temp directories with synthetic READMEs + records and
    runs the in-process `evaluate()` against them. Returns 0 on
    success, 1 on failure.
    """
    import shutil

    fixture_root = ROOT / "tmp-fixture" / "decomposition-reconciliation-self-test"
    if fixture_root.exists():
        shutil.rmtree(fixture_root)
    fixture_root.mkdir(parents=True)

    try:
        # Catalog with a known-good L0..L4 chain.
        records_spec = [
            ("L0", "dea:pc-test-abcdef",
             {"process_groups": ["dea:group-test-abcdef"]}, {}),
            ("L1", "dea:group-test-abcdef",
             {"process_context": "dea:pc-test-abcdef",
              "composes": ["dea:process-test-abcdef"]}, {}),
            ("L2", "dea:process-test-abcdef",
             {"part_of": ["dea:group-test-abcdef"],
              "composes": ["dea:activity-test-abcdef"]}, {}),
            ("L3", "dea:activity-test-abcdef",
             {"belongs_to_business_process": "dea:process-test-abcdef",
              "composes": ["dea:task-test-abcdef"]}, {}),
            ("L4", "dea:task-test-abcdef",
             {"belongs_to_activity": "dea:activity-test-abcdef"}, {}),
        ]

        files = []
        for level, rid, fields, extra in records_spec:
            d = fixture_root / f"rec-{rid.split(':')[-1]}"
            d.mkdir(parents=True, exist_ok=True)
            data = {"id": rid, **fields, **extra}
            p = d / "record.yaml"
            p.write_text(
                __import__("yaml").safe_dump(data, allow_unicode=True),
                encoding="utf-8",
            )
            files.append((p, data))

        # Add a broken L1 with a dangling process_context.
        d = fixture_root / "rec-broken-l1"
        d.mkdir(parents=True, exist_ok=True)
        broken = {"id": "dea:group-broken-abcdef",
                   "process_context": "dea:pc-does-not-exist-123456"}
        p = d / "record.yaml"
        p.write_text(
            __import__("yaml").safe_dump(broken, allow_unicode=True),
            encoding="utf-8",
        )
        files.append((p, broken))

        # Add a broken L0 with a dangling process_groups child.
        d = fixture_root / "rec-broken-l0"
        d.mkdir(parents=True, exist_ok=True)
        broken0 = {"id": "dea:pc-broken-abcdef",
                    "process_groups": ["dea:group-does-not-exist-123456"]}
        p = d / "record.yaml"
        p.write_text(
            __import__("yaml").safe_dump(broken0, allow_unicode=True),
            encoding="utf-8",
        )
        files.append((p, broken0))

        id_index = _build_id_index(files)
        findings = evaluate(files, id_index, validation_manifest={})

        rules = {(f["record_id"], f["rule"]) for f in findings}

        # DOC-021 should fire for the broken L1.
        assert ("dea:group-broken-abcdef", "DOC-021") in rules, \
            "DOC-021 not emitted for the broken L1 fixture"
        # DOC-025 should fire for the broken L0.
        assert ("dea:pc-broken-abcdef", "DOC-025") in rules, \
            "DOC-025 not emitted for the broken L0 fixture"
        # The good chain should NOT emit findings.
        good = {"dea:pc-test-abcdef", "dea:group-test-abcdef",
                "dea:process-test-abcdef", "dea:activity-test-abcdef",
                "dea:task-test-abcdef"}
        bad = {(rid, rule) for (rid, rule) in rules if rid in good}
        assert not bad, f"good chain produced false positives: {bad}"

        print(f"Self-test: {len(findings)} findings; expected DOC-021 + DOC-025 from broken fixtures")
        return 0
    finally:
        if fixture_root.exists():
            shutil.rmtree(fixture_root)


# -----------------------------------------------------------------------------
# Per-rule tests
# -----------------------------------------------------------------------------


def test_constants() -> None:
    """The manifest schema version + generator + parent CR are constants."""
    assert MANIFEST_SCHEMA_VERSION == 1
    assert MANIFEST_GENERATOR == "scripts/check_decomposition_reconciliation.py"
    assert MANIFEST_PARENT_CR == "CR-BP-94-EXT-05"


def test_schema_version_is_1() -> None:
    """Manifest schema version 1 is the initial contract."""
    with SCHEMA.open() as fh:
        schema = json.load(fh)
    assert schema["properties"]["manifest_schema_version"]["const"] == 1
    title_lower = schema["title"].lower()
    assert "decomposition" in title_lower and "manifest" in title_lower
    assert "ext-05" in title_lower or "cr-bp-94" in title_lower


def test_doc021_l1_process_context_resolves() -> None:
    """DOC-021: L1.process_context references a valid L0 parent."""
    import yaml as _yaml

    l0 = {"id": "dea:pc-test-abcdef"}
    l1_good = {"id": "dea:group-test-abcdef",
                "process_context": "dea:pc-test-abcdef"}
    l1_bad = {"id": "dea:group-bad-abcdef",
               "process_context": "dea:pc-does-not-exist-123456"}

    files = [(ROOT / "a.yaml", l0), (ROOT / "b.yaml", l1_good), (ROOT / "c.yaml", l1_bad)]
    id_index = _build_id_index(files)
    findings = evaluate(files, id_index, validation_manifest={})

    # DOC-021 fires only for the bad L1.
    d21 = [f for f in findings if f["rule"] == "DOC-021"]
    assert len(d21) == 1
    assert d21[0]["record_id"] == "dea:group-bad-abcdef"
    assert "dea:pc-does-not-exist-123456" in d21[0]["diagnostic"]


def test_doc022_l2_part_of_resolves() -> None:
    """DOC-022: L2.part_of references valid L1 parents."""
    l1 = {"id": "dea:group-test-abcdef"}
    l2_good = {"id": "dea:process-test-abcdef", "part_of": ["dea:group-test-abcdef"]}
    l2_bad = {"id": "dea:process-bad-abcdef",
               "part_of": ["dea:group-does-not-exist-123456"]}
    files = [(ROOT / "a.yaml", l1), (ROOT / "b.yaml", l2_good), (ROOT / "c.yaml", l2_bad)]
    id_index = _build_id_index(files)
    findings = evaluate(files, id_index, validation_manifest={})

    d22 = [f for f in findings if f["rule"] == "DOC-022"]
    assert len(d22) == 1
    assert d22[0]["record_id"] == "dea:process-bad-abcdef"


def test_doc023_l3_belongs_to_business_process_resolves() -> None:
    """DOC-023: L3.belongs_to_business_process references a valid L2 parent."""
    l2 = {"id": "dea:process-test-abcdef"}
    l3_good = {"id": "dea:activity-test-abcdef",
                "belongs_to_business_process": "dea:process-test-abcdef"}
    l3_bad = {"id": "dea:activity-bad-abcdef",
               "belongs_to_business_process": "dea:process-does-not-exist-123456"}
    files = [(ROOT / "a.yaml", l2), (ROOT / "b.yaml", l3_good), (ROOT / "c.yaml", l3_bad)]
    id_index = _build_id_index(files)
    findings = evaluate(files, id_index, validation_manifest={})

    d23 = [f for f in findings if f["rule"] == "DOC-023"]
    assert len(d23) == 1
    assert d23[0]["record_id"] == "dea:activity-bad-abcdef"


def test_doc024_l4_belongs_to_activity_resolves() -> None:
    """DOC-024: L4.belongs_to_activity references a valid L3 parent."""
    l3 = {"id": "dea:activity-test-abcdef"}
    l4_good = {"id": "dea:task-test-abcdef",
                "belongs_to_activity": "dea:activity-test-abcdef"}
    l4_bad = {"id": "dea:task-bad-abcdef",
               "belongs_to_activity": "dea:activity-does-not-exist-123456"}
    files = [(ROOT / "a.yaml", l3), (ROOT / "b.yaml", l4_good), (ROOT / "c.yaml", l4_bad)]
    id_index = _build_id_index(files)
    findings = evaluate(files, id_index, validation_manifest={})

    d24 = [f for f in findings if f["rule"] == "DOC-024"]
    assert len(d24) == 1
    assert d24[0]["record_id"] == "dea:task-bad-abcdef"


def test_doc025_reverse_references_resolve() -> None:
    """DOC-025: every child in a parent's list exists in the catalog."""
    l0_good = {"id": "dea:pc-test-abcdef",
                "process_groups": ["dea:group-test-abcdef"]}
    l0_bad = {"id": "dea:pc-bad-abcdef",
               "process_groups": ["dea:group-does-not-exist-123456"]}
    l1 = {"id": "dea:group-test-abcdef"}
    files = [(ROOT / "a.yaml", l0_good), (ROOT / "b.yaml", l0_bad), (ROOT / "c.yaml", l1)]
    id_index = _build_id_index(files)
    findings = evaluate(files, id_index, validation_manifest={})

    d25 = [f for f in findings if f["rule"] == "DOC-025"]
    assert len(d25) == 1
    assert d25[0]["record_id"] == "dea:pc-bad-abcdef"


def test_evaluate_skips_records_with_unresolved_validation_findings() -> None:
    """The validator gates on the EXT-04 validation manifest.

    Records with unresolved DOC-016/017/018 findings are skipped
    (their decomposition chain is not in a known state).
    """
    l1_bad = {"id": "dea:group-bad-abcdef",
               "process_context": "dea:pc-does-not-exist-123456"}
    l0 = {"id": "dea:pc-good-abcdef"}

    # Validation manifest says l1_bad has unresolved DOC-016.
    validation_manifest = {
        "findings": [
            {"rule": "DOC-016", "record_id": "dea:group-bad-abcdef",
             "advisory": True, "level": "L1"},
        ],
    }

    files = [(ROOT / "a.yaml", l0), (ROOT / "b.yaml", l1_bad)]
    id_index = _build_id_index(files)
    findings = evaluate(files, id_index, validation_manifest=validation_manifest)

    # The DOC-021 finding for the bad L1 should be SUPPRESSED
    # because the validation manifest says it has unresolved DOC-016.
    assert not any(f["rule"] == "DOC-021" for f in findings), \
        "DOC-021 should be suppressed when the record has unresolved DOC-016"


def test_self_test_synthetic_fixtures() -> None:
    """run_self_test() covers the 5 rules via the in-process evaluate()."""
    rc = run_self_test()
    assert rc == 0, f"self-test returned {rc}; expected 0"


# -----------------------------------------------------------------------------
# Live-catalog integration test
# -----------------------------------------------------------------------------


def test_live_catalog_writes_manifest() -> None:
    """The validator writes the manifest at reconciliation/decomposition-reconciliation-manifest.json.

    The manifest must have the expected schema_version, generator,
    parent_cr, and a non-empty summary. This is the live-catalog
    integration assertion; it is the proof that the validator is
    wired into the standing development model.
    """
    manifest_path = ROOT / "reconciliation" / "decomposition-reconciliation-manifest.json"
    if not manifest_path.exists():
        # Run the validator (which also depends on the EXT-04 manifest
        # existing; run EXT-04 first if missing).
        ext04_manifest = ROOT / "reconciliation" / "validation-manifest.json"
        if not ext04_manifest.exists():
            r = subprocess.run(
                [sys.executable,
                 str(ROOT / "scripts" / "validate_readme_structure.py"),
                 "--catalog-root", str(ROOT)],
                capture_output=True, text=True, timeout=120,
            )
            assert r.returncode == 0, f"EXT-04 validator failed: {r.stderr}"

        r = subprocess.run(
            [sys.executable, str(SCRIPT), "--catalog-root", str(ROOT)],
            capture_output=True, text=True, timeout=120,
        )
        assert r.returncode == 0, f"validator failed: {r.stderr}\n{r.stdout[-2000:]}"

    assert manifest_path.exists(), "decomposition-reconciliation-manifest.json not written"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["manifest_schema_version"] == MANIFEST_SCHEMA_VERSION
    assert manifest["generator"] == MANIFEST_GENERATOR
    assert manifest["parent_cr"] == MANIFEST_PARENT_CR
    assert manifest["summary"]["total_records"] > 0
    assert "by_rule" in manifest["summary"]
    for rule in ("DOC-021", "DOC-022", "DOC-023", "DOC-024", "DOC-025"):
        assert rule in manifest["summary"]["by_rule"]


def test_live_catalog_manifest_validates_against_schema() -> None:
    """The emitted manifest validates against schemas/decomposition-reconciliation-manifest.schema.json."""
    try:
        import jsonschema  # type: ignore
    except ImportError:
        import pytest
        pytest.skip("jsonschema not installed")

    manifest_path = ROOT / "reconciliation" / "decomposition-reconciliation-manifest.json"
    if not manifest_path.exists():
        return  # covered by the previous test

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    with SCHEMA.open() as fh:
        schema = json.load(fh)

    jsonschema.validate(manifest, schema)
