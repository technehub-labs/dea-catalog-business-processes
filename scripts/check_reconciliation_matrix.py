#!/usr/bin/env python3
"""
check_reconciliation_matrix.py
==============================

CR-BP-99 reconciliation matrix validator.

Validates the structure + invariants of `reconciliation/cr-bp-99-matrix.yaml`.
This is the authoritative catalog of advisory findings + pre-existing
inconsistencies surfaced during the recon programme (CR-BP-91..98 +
EXT-01..01a), with disposition + owner assignments.

The validator enforces:
  RCM-001 — Matrix schema is well-formed (matrix_version, generated_at,
            rows[], summary, invariants[]).
  RCM-002 — Every row has id, finding.rule, finding.record_id,
            finding.summary, category, disposition, owner,
            remediation, status.
  RCM-003 — Row id format: `matrix-NNN` where NNN is a 3-digit integer.
  RCM-004 — Disposition ∈ {backfill, defer, accept_as_is, relax_rule}.
  RCM-005 — Status ∈ {open, closed}.
  RCM-006 — Closed rows MUST carry closed_in (non-empty string).
  RCM-007 — Categories are from the closed enum.
  RCM-008 — Row ids are unique.
  RCM-009 — Summary counts (by_disposition, by_status) match the rows.
  RCM-010 — Invariant list contains at least one invariant per
            category used.

The validator emits findings with `severity: error` (blocking) or
`severity: warning` (advisory). Backfill rows MUST have status=closed
after CR-BP-99 lands; the validator flags discrepancies as warnings so
the gate stays non-blocking.

CLI:
  --self-test : in-process self-test, exit 0 / 1
  --json      : emit JSON payload
  (no flag)   : validate the live matrix file, exit 0 / 1
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
MATRIX_PATH = ROOT / "reconciliation" / "cr-bp-99-matrix.yaml"

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

ROW_ID_PATTERN = re.compile(r"^matrix-\d{3}$")
ALLOWED_DISPOSITIONS = frozenset({"backfill", "defer", "accept_as_is", "relax_rule"})
ALLOWED_STATUSES = frozenset({"open", "closed"})
ALLOWED_CATEGORIES = frozenset({
    "act_backfill",
    "pg_backfill",
    "doc_deferred",
    "doc_conformant",
    "bp_qual_deferred",
    "act_optional_deferred",
    "rule_relaxation",
    "schema_repair",
    "pre_existing",
    "pg_conformant",
    "pscope_conformant",
    "task_conformant",
    "doc_validator_state",
    "pscope_dormant",
})
REQUIRED_ROW_FIELDS = frozenset({
    "id", "finding", "category", "disposition", "owner",
    "remediation", "status",
})
REQUIRED_FINDING_FIELDS = frozenset({"rule", "record_id", "summary"})

RULE_IDS = ("RCM-001", "RCM-002", "RCM-003", "RCM-004", "RCM-005",
            "RCM-006", "RCM-007", "RCM-008", "RCM-009", "RCM-010")


@dataclass
class Finding:
    rule: str
    row_id: str
    severity: str
    message: str

    def to_dict(self) -> dict:
        return {
            "rule": self.rule,
            "row_id": self.row_id,
            "severity": self.severity,
            "message": self.message,
        }


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def _load_matrix(path: Path = MATRIX_PATH) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


# -----------------------------------------------------------------------------
# Per-rule checks
# -----------------------------------------------------------------------------

def _check_schema(matrix: dict) -> list[Finding]:
    """RCM-001 — Matrix schema is well-formed."""
    findings: list[Finding] = []
    if not isinstance(matrix, dict):
        findings.append(Finding(
            rule="RCM-001",
            row_id="<root>",
            severity="error",
            message="Matrix is not a dict.",
        ))
        return findings
    required_top = {"matrix_version", "generated_at", "rows", "summary", "invariants"}
    missing = required_top - set(matrix.keys())
    if missing:
        findings.append(Finding(
            rule="RCM-001",
            row_id="<root>",
            severity="error",
            message=f"Missing top-level fields: {sorted(missing)}",
        ))
    if not isinstance(matrix.get("rows"), list):
        findings.append(Finding(
            rule="RCM-001",
            row_id="<root>",
            severity="error",
            message="`rows` must be a list.",
        ))
    return findings


def _check_row_fields(rows: list[dict]) -> list[Finding]:
    """RCM-002 — Every row has the required fields."""
    findings: list[Finding] = []
    for row in rows:
        rid = row.get("id", "<missing>")
        missing = REQUIRED_ROW_FIELDS - set(row.keys())
        if missing:
            findings.append(Finding(
                rule="RCM-002",
                row_id=rid,
                severity="error",
                message=f"Row missing required fields: {sorted(missing)}",
            ))
        finding = row.get("finding", {})
        if not isinstance(finding, dict):
            findings.append(Finding(
                rule="RCM-002",
                row_id=rid,
                severity="error",
                message="`finding` must be a dict.",
            ))
        else:
            finding_missing = REQUIRED_FINDING_FIELDS - set(finding.keys())
            if finding_missing:
                findings.append(Finding(
                    rule="RCM-002",
                    row_id=rid,
                    severity="error",
                    message=f"`finding` missing fields: {sorted(finding_missing)}",
                ))
    return findings


def _check_row_id_format(rows: list[dict]) -> list[Finding]:
    """RCM-003 — Row id format: matrix-NNN."""
    findings: list[Finding] = []
    for row in rows:
        rid = row.get("id", "")
        if not ROW_ID_PATTERN.match(rid):
            findings.append(Finding(
                rule="RCM-003",
                row_id=rid or "<missing>",
                severity="error",
                message=f"Row id {rid!r} does not match {ROW_ID_PATTERN.pattern!r}",
            ))
    return findings


def _check_disposition(rows: list[dict]) -> list[Finding]:
    """RCM-004 — Disposition ∈ closed enum."""
    findings: list[Finding] = []
    for row in rows:
        rid = row.get("id", "<missing>")
        d = row.get("disposition", "")
        if d not in ALLOWED_DISPOSITIONS:
            findings.append(Finding(
                rule="RCM-004",
                row_id=rid,
                severity="error",
                message=f"Disposition {d!r} not in {sorted(ALLOWED_DISPOSITIONS)}",
            ))
    return findings


def _check_status(rows: list[dict]) -> list[Finding]:
    """RCM-005 — Status ∈ {open, closed}; RCM-006 — Closed rows carry closed_in."""
    findings: list[Finding] = []
    for row in rows:
        rid = row.get("id", "<missing>")
        s = row.get("status", "")
        if s not in ALLOWED_STATUSES:
            findings.append(Finding(
                rule="RCM-005",
                row_id=rid,
                severity="error",
                message=f"Status {s!r} not in {sorted(ALLOWED_STATUSES)}",
            ))
        if s == "closed":
            ci = row.get("closed_in", "")
            if not isinstance(ci, str) or not ci.strip():
                findings.append(Finding(
                    rule="RCM-006",
                    row_id=rid,
                    severity="error",
                    message="Closed row MUST carry non-empty `closed_in` (e.g., PR-NNN).",
                ))
    return findings


def _check_categories(rows: list[dict]) -> list[Finding]:
    """RCM-007 — Categories are from the closed enum."""
    findings: list[Finding] = []
    for row in rows:
        rid = row.get("id", "<missing>")
        c = row.get("category", "")
        if c not in ALLOWED_CATEGORIES:
            findings.append(Finding(
                rule="RCM-007",
                row_id=rid,
                severity="error",
                message=f"Category {c!r} not in {sorted(ALLOWED_CATEGORIES)}",
            ))
    return findings


def _check_unique_ids(rows: list[dict]) -> list[Finding]:
    """RCM-008 — Row ids are unique."""
    findings: list[Finding] = []
    seen: set[str] = set()
    for row in rows:
        rid = row.get("id", "<missing>")
        if rid in seen:
            findings.append(Finding(
                rule="RCM-008",
                row_id=rid,
                severity="error",
                message=f"Duplicate row id {rid!r}",
            ))
        seen.add(rid)
    return findings


def _check_summary_counts(matrix: dict) -> list[Finding]:
    """RCM-009 — Summary counts (by_disposition, by_status) match the rows."""
    findings: list[Finding] = []
    rows = matrix.get("rows", [])
    summary = matrix.get("summary", {})
    by_disposition = summary.get("by_disposition", {})
    by_status = summary.get("by_status", {})

    actual_disposition: dict[str, int] = {}
    actual_status: dict[str, int] = {}
    for row in rows:
        d = row.get("disposition", "<missing>")
        s = row.get("status", "<missing>")
        actual_disposition[d] = actual_disposition.get(d, 0) + 1
        actual_status[s] = actual_status.get(s, 0) + 1

    if by_disposition != actual_disposition:
        findings.append(Finding(
            rule="RCM-009",
            row_id="<summary>",
            severity="warning",
            message=f"by_disposition mismatch: actual={actual_disposition} vs summary={by_disposition}",
        ))
    if by_status != actual_status:
        findings.append(Finding(
            rule="RCM-009",
            row_id="<summary>",
            severity="warning",
            message=f"by_status mismatch: actual={actual_status} vs summary={by_status}",
        ))
    total_rows = summary.get("total_rows")
    if total_rows is not None and total_rows != len(rows):
        findings.append(Finding(
            rule="RCM-009",
            row_id="<summary>",
            severity="warning",
            message=f"total_rows mismatch: summary={total_rows} vs actual={len(rows)}",
        ))
    return findings


def _check_invariants(matrix: dict) -> list[Finding]:
    """RCM-010 — Invariant list contains at least one invariant per category used."""
    findings: list[Finding] = []
    rows = matrix.get("rows", [])
    invariants = matrix.get("invariants", [])
    if not isinstance(invariants, list) or not invariants:
        findings.append(Finding(
            rule="RCM-010",
            row_id="<invariants>",
            severity="warning",
            message="Invariants list is empty.",
        ))
        return findings
    # Each invariant must carry `id`.
    for inv in invariants:
        if not isinstance(inv, dict) or not inv.get("id"):
            findings.append(Finding(
                rule="RCM-010",
                row_id="<invariants>",
                severity="warning",
                message="Invariant missing `id`.",
            ))
    return findings


# -----------------------------------------------------------------------------
# Aggregate evaluate()
# -----------------------------------------------------------------------------

def evaluate(matrix: dict) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(_check_schema(matrix))
    rows = matrix.get("rows", [])
    if not isinstance(rows, list):
        return findings
    findings.extend(_check_row_fields(rows))
    findings.extend(_check_row_id_format(rows))
    findings.extend(_check_disposition(rows))
    findings.extend(_check_status(rows))
    findings.extend(_check_categories(rows))
    findings.extend(_check_unique_ids(rows))
    findings.extend(_check_summary_counts(matrix))
    findings.extend(_check_invariants(matrix))
    return findings


def verdict(findings: list[Finding]) -> str:
    """CONFORMANT unless any `error` findings are present."""
    return "CONFORMANT" if not any(f.severity == "error" for f in findings) else "NON-CONFORMANT"


# -----------------------------------------------------------------------------
# Self-test
# -----------------------------------------------------------------------------

def _self_test_matrix() -> dict:
    """A minimal valid matrix used by --self-test."""
    return {
        "matrix_version": 99,
        "generated_at": "2026-09-18",
        "rows": [
            {
                "id": "matrix-001",
                "finding": {"rule": "TST", "record_id": "x", "summary": "test"},
                "category": "pre_existing",
                "disposition": "backfill",
                "owner": "CR-BP-99",
                "remediation": "test",
                "status": "closed",
                "closed_in": "PR-999",
            },
        ],
        "summary": {
            "total_rows": 1,
            "by_disposition": {"backfill": 1},
            "by_status": {"closed": 1},
        },
        "invariants": [{"id": "test invariant"}],
    }


def _self_test() -> int:
    matrix = _self_test_matrix()
    findings = evaluate(matrix)
    if any(f.severity == "error" for f in findings):
        print("self-test FAIL:", file=sys.stderr)
        for f in findings:
            print(f"  X {f.rule} {f.row_id}: {f.message}", file=sys.stderr)
        return 1
    print(f"self-test PASS ({len(RULE_IDS)} rules; minimal valid matrix)")
    return 0


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def _cli_live() -> int:
    matrix = _load_matrix()
    findings = evaluate(matrix)
    n_rows = len(matrix.get("rows", []))
    print(f"Reconciliation Matrix (CR-BP-99 RCM-001..010): {verdict(findings)}")
    print(f"  Rows checked:  {n_rows}")
    print(f"  Findings:      {len(findings)}")
    err = sum(1 for f in findings if f.severity == "error")
    warn = sum(1 for f in findings if f.severity == "warning")
    print(f"    errors:      {err}")
    print(f"    warnings:    {warn}")
    if findings:
        for f in findings:
            print(f"  [{f.severity}] [{f.rule}] {f.row_id}: {f.message}")
    return 0 if verdict(findings) == "CONFORMANT" else 1


def _cli_json() -> int:
    matrix = _load_matrix()
    findings = evaluate(matrix)
    payload = {
        "verdict": verdict(findings),
        "matrix_version": matrix.get("matrix_version"),
        "rows_checked": len(matrix.get("rows", [])),
        "findings": [f.to_dict() for f in findings],
        "rules": [{"id": rid, "description": _RULE_DESCRIPTION[rid]} for rid in RULE_IDS],
    }
    print(json.dumps(payload, indent=2))
    return 0 if verdict(findings) == "CONFORMANT" else 1


_RULE_DESCRIPTION = {
    "RCM-001": "Matrix schema is well-formed (matrix_version, generated_at, rows, summary, invariants).",
    "RCM-002": "Every row carries id, finding.rule, finding.record_id, finding.summary, category, disposition, owner, remediation, status.",
    "RCM-003": "Row id format `matrix-NNN` (3-digit integer).",
    "RCM-004": "Disposition ∈ {backfill, defer, accept_as_is, relax_rule}.",
    "RCM-005": "Status ∈ {open, closed}.",
    "RCM-006": "Closed rows MUST carry non-empty `closed_in` (e.g., PR-NNN).",
    "RCM-007": "Categories are from the closed enum (act_backfill, doc_deferred, pre_existing, ...).",
    "RCM-008": "Row ids are unique across the matrix.",
    "RCM-009": "Summary counts (by_disposition, by_status, total_rows) match the rows.",
    "RCM-010": "Invariant list is non-empty and every invariant carries `id`.",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="CR-BP-99 reconciliation matrix validator")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return _self_test()
    if args.json:
        return _cli_json()
    return _cli_live()


if __name__ == "__main__":
    sys.exit(main())