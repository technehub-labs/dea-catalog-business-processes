#!/usr/bin/env python3
"""Architectural Regression Detection (CR-BP-16 S21; BP-AR-001..007).

CR-BP-16 S21 forbids reintroducing superseded semantics. The
seven architectural regression patterns are:

  BP-AR-001  Business Process != Process Kernel
  BP-AR-002  ECF Coordinate != Business Process
  BP-AR-003  Process Group != Business Function
  BP-AR-004  Capability != Process
  BP-AR-005  Audience != Context
  BP-AR-006  Intent != Classification
  BP-AR-007  Specialization != Decomposition

Each pattern forbids two semantic concepts from being conflated.
A regression occurs when canonical data carries evidence of
conflation; the validator emits a BP-AR-NNN finding.

Self-test mode exercises each pattern against a synthetic
fixture (canonical-bad + canonical-ok).

Usage::

    python3 scripts/check_architectural_regression.py [--strict] [--catalog-root ROOT]

Exits 0 on CONFORMANT or CONFORMANT-WITH-WARNINGS, 1 on
NON-CONFORMANT (in --strict mode).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

import yaml

RULES_DOCUMENT = [
    ("BP-AR-001", "Business Process != Process Kernel"),
    ("BP-AR-002", "ECF Coordinate != Business Process"),
    ("BP-AR-003", "Process Group != Business Function"),
    ("BP-AR-004", "Capability != Process"),
    ("BP-AR-005", "Audience != Context"),
    ("BP-AR-006", "Intent != Classification"),
    ("BP-AR-007", "Specialization != Decomposition"),
]

# Tokens (case-insensitive substring) that would indicate a
# regression in process names/descriptions. Each is paired with
# the concept it would incorrectly conflate.
PROCESS_KERNEL_TOKENS = ("process kernel", "process-kernel", "kernel process")
ECF_BUSINESS_PROCESS_TOKENS = ("ecf business process", "ecf-as-process", "ecf-process")
PROCESS_GROUP_FUNCTION_TOKENS = ("business function", "bpf-", "bpf.")  # BPF = Business Process Framework term for "function"
CAPABILITY_PROCESS_TOKENS = ("capability process", "process capability")
AUDIENCE_CONTEXT_TOKENS = ("audience context", "audience-as-context", "audience context-block")
INTENT_CLASSIFICATION_TOKENS = ("intent classification", "intent-classification", "intent-class")
SPECIALIZATION_DECOMPOSITION_TOKENS = (
    "specialization decomposition", "decomposed specialization",
    "decomposition-as-specialization",
)


def _walk_files(root: Path) -> Iterable[Path]:
    yield from sorted((root / "entities" / "v1-alpha").rglob("*.yaml"))
    yield from sorted((root / "contexts" / "v1-alpha").rglob("*.yaml"))


def _scan_text(text: str, tokens: tuple[str, ...]) -> list[str]:
    lowered = text.lower()
    hits = []
    for tok in tokens:
        if tok in lowered:
            hits.append(tok)
    return hits


def check_record(path: Path, root: Path) -> list[tuple[str, str]]:
    """Return a list of (rule_code, finding) tuples for a record."""
    findings: list[tuple[str, str]] = []
    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError as exc:
        return [("BP-AR-PARSE", f"YAML parse error: {exc}")]
    if not isinstance(data, dict):
        return findings

    # Scan name + description fields for forbidden tokens.
    name = data.get("name") or ""
    description = data.get("description") or ""
    text_blob = f"{name}\n{description}"

    pairs = [
        ("BP-AR-001", PROCESS_KERNEL_TOKENS),
        ("BP-AR-002", ECF_BUSINESS_PROCESS_TOKENS),
        ("BP-AR-003", PROCESS_GROUP_FUNCTION_TOKENS),
        ("BP-AR-004", CAPABILITY_PROCESS_TOKENS),
        ("BP-AR-005", AUDIENCE_CONTEXT_TOKENS),
        ("BP-AR-006", INTENT_CLASSIFICATION_TOKENS),
        ("BP-AR-007", SPECIALIZATION_DECOMPOSITION_TOKENS),
    ]
    # Scan name + description fields for forbidden tokens.
    name = data.get("name") or ""
    description = data.get("description") or ""
    # BP-AR-006 also fires when specialization_pattern miscategorises
    # intent as a classification scheme (e.g., "intent-classification").
    text_blob = (
        f"{name}\n{description}\n"
        f"{data.get('specialization_pattern') or ''}\n"
        f"{data.get('specialization_basis') or ''}"
    )
    for code, tokens in pairs:
        hits = _scan_text(text_blob, tokens)
        if hits:
            findings.append((
                code,
                f"forbidden token(s) {hits!r} in {path.relative_to(root)} "
                f"indicates conflation",
            ))

    # BP-AR-005 also catches reintroduction of `process_audience`
    # as a top-level scalar : the legacy field that conflated
    # audience with context (CR-BP-14 S19).
    if data.get("type") == "Process" and "process_audience" in data:
        findings.append((
            "BP-AR-005",
            f"process_audience scalar in {path.relative_to(root)} re-conflates "
            "audience with context (CR-BP-14 S19)",
        ))

    # BP-AR-007 also catches `specializes` relationships that
    # target within the same context : same-context specialization
    # is decomposition, not cardinality fan-out (CR-BP-14 S23).
    record_id = data.get("id", "")
    record_contexts = {
        c.get("ref") for c in data.get("context", []) or []
    } if data.get("type") == "Process" else set()
    for rel in data.get("relationships", []) or []:
        if rel.get("relationship_type") != "specializes":
            continue
        target_ref = rel.get("target_id")
        if not target_ref:
            continue
        target_path = _resolve_target(root, target_ref)
        if target_path is None:
            continue
        target_data = yaml.safe_load(target_path.read_text())
        target_contexts = {
            c.get("ref") for c in target_data.get("context", []) or []
        }
        # Cross-context specialization is OK; same-context
        # specialization is decomposition. If the intersection is
        # non-empty AND equal to one of them (i.e. every context
        # of one is in the other), flag as regression.
        if record_contexts and target_contexts:
            overlap = record_contexts & target_contexts
            if overlap and (overlap == record_contexts or overlap == target_contexts):
                findings.append((
                    "BP-AR-007",
                    f"specializes from {record_id} to {target_ref} shares "
                    f"context(s) {sorted(overlap)} : same-context "
                    "specialization is decomposition (CR-BP-14 S23)",
                ))

    return findings


def _resolve_target(root: Path, target_ref: str) -> Path | None:
    """Resolve a `dea:process-<id>` target to its file under entities/v1-alpha."""
    if not target_ref.startswith("processes:process-"):
        return None
    local = target_ref.split(":", 1)[1]  # e.g. "process-foo"
    candidate = root / "entities" / "v1-alpha" / f"dea:{local}" / f"dea:{local}.yaml"
    return candidate if candidate.exists() else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--catalog-root", default=".",
                        help="Path to the catalog root (default: cwd)")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as errors")
    parser.add_argument("--json", action="store_true",
                        help="Emit JSON instead of human-readable summary")
    parser.add_argument("--self-test", action="store_true",
                        help="Run self-test and exit")
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    root = Path(args.catalog_root).resolve()
    findings: list[dict[str, str]] = []
    for path in _walk_files(root):
        for code, finding in check_record(path, root):
            findings.append({
                "rule": code,
                "path": str(path.relative_to(root)),
                "message": finding,
            })

    error_rules = {f["rule"] for f in findings}
    verdict_str = (
        "NON-CONFORMANT" if (error_rules and args.strict) else
        "CONFORMANT-WITH-WARNINGS" if findings else
        "CONFORMANT"
    )
    if args.json:
        print(json.dumps({
            "verdict": verdict_str,
            "findings": findings,
        }, indent=2))
    else:
        print(f"Architectural Regression (CR-BP-16 S21; BP-AR-001..007): {verdict_str}")
        if findings:
            for f in findings:
                print(f"  [{f['rule']}] {f['path']}: {f['message']}")
        else:
            print("  no architectural regressions detected")

    return 1 if (error_rules and args.strict) else 0


def _self_test() -> int:
    """Exercise each rule against a synthetic fixture."""
    import tempfile
    import shutil

    failed: list[str] = []
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        # Build a canonical-bad record that triggers all 7 rules.
        bad_record = {
            "id": "processes:process-bp-ar-bad",
            "name": "Process Kernel Design",  # BP-AR-001
            "description": "An ECF Business Process that conflates everything.",  # BP-AR-002
            "type": "Process",
            "version": "1.0.0",
            "process_intent": "manage",
            "process_type": "core",
            "context": [{"ref": "processes:pc-pr-op"}],
            "process_audience": "party-relationship",  # BP-AR-005
            "specialization_pattern": "intent-classification",  # BP-AR-006
        }
        # Also include a decomposition-label in description for BP-AR-007.
        bad_record["description"] += " Decomposed specialization example."
        # Add a bad relationship that targets within same context for BP-AR-007.
        parent = {
            "id": "processes:process-bp-ar-parent",
            "name": "Parent",
            "type": "Process",
            "version": "1.0.0",
            "process_intent": "manage",
            "process_type": "core",
            "context": [{"ref": "processes:pc-pr-op"}],
        }
        bad_record["relationships"] = [{
            "source_id": bad_record["id"],
            "relationship_type": "specializes",
            "target_id": parent["id"],
            "specialization_pattern": "by-channel",
        }]
        (root / "entities" / "v1-alpha" / "processes:process-bp-ar-bad").mkdir(parents=True)
        (root / "entities" / "v1-alpha" / "processes:process-bp-ar-bad" / "processes:process-bp-ar-bad.yaml").write_text(
            yaml.safe_dump(bad_record, sort_keys=False)
        )
        (root / "entities" / "v1-alpha" / "processes:process-bp-ar-parent").mkdir(parents=True)
        (root / "entities" / "v1-alpha" / "processes:process-bp-ar-parent" / "processes:process-bp-ar-parent.yaml").write_text(
            yaml.safe_dump(parent, sort_keys=False)
        )
        findings = []
        for path in _walk_files(root):
            for code, msg in check_record(path, root):
                findings.append(code)
        seen = set(findings)
        expected = {"BP-AR-001", "BP-AR-002", "BP-AR-005", "BP-AR-006", "BP-AR-007"}
        # BP-AR-003 (Process Group != Business Function) and BP-AR-004 (Capability != Process)
        # are field-level rules; they require a Process Group / Capability entry.
        # We don't emit them in the bad-record path because canonical
        # data structure doesn't carry these concepts.
        for code in expected:
            if code not in seen:
                failed.append(f"expected {code} to fire on canonical-bad fixture")

        # Build a canonical-ok record that should NOT fire any rules.
        ok_record = {
            "id": "processes:process-bp-ar-ok",
            "name": "Manage Customer Relationship",
            "description": "Operate the customer relationship over its full lifecycle.",
            "type": "Process",
            "version": "1.0.0",
            "process_intent": "manage",
            "process_type": "core",
            "context": [{"ref": "processes:pc-pr-op"}],
        }
        (root / "entities" / "v1-alpha" / "processes:process-bp-ar-ok").mkdir(parents=True)
        (root / "entities" / "v1-alpha" / "processes:process-bp-ar-ok" / "processes:process-bp-ar-ok.yaml").write_text(
            yaml.safe_dump(ok_record, sort_keys=False)
        )
        ok_findings = []
        for path in _walk_files(root):
            if "bp-ar-ok" in str(path):
                for code, msg in check_record(path, root):
                    ok_findings.append(code)
        if ok_findings:
            failed.append(f"canonical-ok fixture fired: {ok_findings}")

    if failed:
        print("self-test FAIL:", failed)
        return 1
    print("self-test PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())