#!/usr/bin/env python3
"""build_release_notes.py + decisions log — CR-BP-30d (decision D4 = A).

Two artifacts in one builder:
  1. RELEASE-NOTES.md — the human-readable narrative of the tagged
     release: the CHANGELOG section for the version, the register
     posture, and the conformance gate summary.
  2. decisions.md — the curated decisions log (per-disposition table
     from reconciliation/dispositions/register.yaml + per-CR one-line
     index), with the verbatim dispositions/ folder copied alongside by
     the workflow (this script emits decisions.md only).

Deterministic: no timestamps beyond the caller-supplied release date.

Usage:
  python3 scripts/build_release_notes.py --version v0.5.0 \
      --date 2026-11-04 --out out/v0.5.0/RELEASE-NOTES.md \
      [--decisions out/v0.5.0/decisions.md]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def _changelog_section(version: str) -> str:
    """Return the CHANGELOG body for `version` (or [Unreleased] when the
    version section does not exist yet — pre-tag preview)."""
    text = (ROOT / "CHANGELOG.md").read_text()
    sections = re.split(r"^## ", text, flags=re.M)
    for s in sections:
        if s.startswith(f"[{version}]") or (s.startswith("[Unreleased]") and version.startswith("v")):
            return s.split("\n", 1)[1].strip()
    return "(no CHANGELOG section found)"


def _register_stats():
    reg = ROOT / "change-requests" / "README.md"
    rows = [l for l in reg.read_text().splitlines() if l.startswith("| [CR-")]
    return len(rows)


def _gate_summary():
    report = ROOT / "reconciliation" / "conformance_report.yaml"
    if not report.exists():
        return "conformance report not present at build time"
    try:
        d = yaml.safe_load(report.read_text()) or {}
        s = d.get("summary") or {}
        return (f"gates: {s.get('gate_count', 'n/a')} — "
                f"blocking: {s.get('blocking', 'n/a')}, "
                f"advisory: {s.get('advisory', 'n/a')}")
    except Exception:
        return "conformance report unreadable at build time"


def build_release_notes(version: str, date: str) -> str:
    out = [f"# Release Notes — {version}", "",
           f"**Date**: {date}", "",
           "## What landed", "",
           _changelog_section(version), "",
           "## Catalog posture", "",
           f"- Change-request register rows: {_register_stats()}",
           f"- Conformance: {_gate_summary()}",
           "- Artifacts: process-map.html + process-map-a3.png (CR-BP-30a, D1=A), "
           "catalog.xlsx 6 sheets (CR-BP-30b, D2), bpmn-library.bpmn (CR-BP-30c, "
           "D3=A), decisions.md + dispositions/ (CR-BP-30d, D4=A), "
           "dependencies.yaml (CR-BP-30e, D5), full YAML substrate "
           "(self-contained zip principle), MANIFEST.md with per-file sha256 "
           "(provenance principle).", "",
           "## Provenance", "",
           "Every artifact carries its generating script + commit SHA in "
           "MANIFEST.md; the zip is self-auditable per CR-BP-30 §2 "
           "(provenance principle). Versioning per CR-BP-116 Path B "
           "(docs/versioning.md; docs/release-cut-procedure.md)."]
    return "\n".join(out) + "\n"


def build_decisions() -> str:
    reg = ROOT / "reconciliation" / "dispositions" / "register.yaml"
    lines = ["# Decisions Log", "",
             "Curated decisions surface (CR-BP-30d; decision D4=A). The raw",
             "register ships verbatim in `dispositions/` beside this file.", ""]
    if reg.exists():
        d = yaml.safe_load(reg.read_text()) or {}
        entries = d.get("dispositions") or []
        lines += ["| Record | Disposition | Rationale | CR |",
                  "| :--- | :--- | :--- | :--- |"]
        for e in sorted(entries, key=lambda x: str(x.get("record_id", x.get("id", ""))) if isinstance(x, dict) else ""):
            if isinstance(e, dict):
                lines.append(f"| {e.get('record_id', e.get('id', ''))} "
                             f"| {e.get('disposition', e.get('decision', ''))} "
                             f"| {str(e.get('rationale', ''))[:120]} "
                             f"| {e.get('cr', '')} |")
        if not entries:
            lines.append("(the dispositions register carries no entries)")
    else:
        lines.append("(no dispositions register at build time)")
    lines += ["", "## Change-request index", "",
              "The authoritative CR register is `change-requests/README.md`",
              "(linked verbatim in the zip's substrate); its row count and",
              "posture summary are in RELEASE-NOTES.md."]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    ap.add_argument("--version", required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--decisions", default=None)
    args = ap.parse_args(argv)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    notes = build_release_notes(args.version, args.date)
    out.write_text(notes)
    print(f"release-notes: wrote {out} ({len(notes)} bytes)")
    if args.decisions:
        dp = Path(args.decisions)
        dp.parent.mkdir(parents=True, exist_ok=True)
        decisions = build_decisions()
        dp.write_text(decisions)
        print(f"decisions-log: wrote {dp} ({len(decisions)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
