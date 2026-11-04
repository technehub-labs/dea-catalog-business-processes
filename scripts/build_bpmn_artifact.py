#!/usr/bin/env python3
"""build_bpmn_artifact.py — CR-BP-30c: the BPMN 2.0 seed library.

Decision D3 = A: a single `bpmn-library.bpmn` file, one `<bpmn:process>`
per canonical L2 Business Process, each carrying a single Task named
after the process with the record's coordinates (ECF cell, Process
Context, Process Group, canonical ids) as `<bpmn:documentation>`.
Consumes natively in bpmn.io / Camunda / Signavio with zero install.

Deterministic: processes emitted sorted by id; no timestamps. XML via
the stdlib ElementTree (lxml not required — the CR's lxml suggestion
predated the zero-dependency choice; noted in CR-BP-30-IMP).

Usage:
  python3 scripts/build_bpmn_artifact.py --out out/v0.5.0/bpmn-library.bpmn
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTITIES = ROOT / "entities" / "v1-alpha"
STATE_DIRS = ("research", "candidates", "retired")

BPMN_NS = "http://www.omg.org/spec/BPMN/20100524/MODEL"
ET.register_namespace("bpmn", BPMN_NS)


def _load_processes():
    procs = []
    for p in sorted(ENTITIES.rglob("processes-process-*.yaml")):
        if any(s in p.parts for s in STATE_DIRS):
            continue
        d = yaml.safe_load(p.read_text()) or {}
        if not d.get("id"):
            continue
        pc = d.get("process_context")
        pc_id = pc.get("id") if isinstance(pc, dict) else (pc or "")
        procs.append({
            "id": d["id"],
            "name": d.get("name", ""),
            "version": d.get("version", "1.0.0"),
            "status": d.get("status", ""),
            "lifecycle_status": d.get("lifecycle_status", ""),
            "domain": d.get("domain", ""),
            "stage": d.get("lifecycle_stage", ""),
            "pc": pc_id,
            "trigger": d.get("trigger", ""),
            "outcome": d.get("outcome", ""),
        })
    return sorted(procs, key=lambda r: r["id"])


def build(out_path: Path, label: str = "catalog") -> int:
    procs = _load_processes()
    defs = ET.Element(f"{{{BPMN_NS}}}definitions", {
        "id": f"OpenDEA-ProcessCatalog-{label}",
        "targetNamespace": "https://technehub-labs.github.io/opendea/processes",
    })
    for r in procs:
        proc = ET.SubElement(defs, f"{{{BPMN_NS}}}process", {
            "id": "_bp_" + r["id"].replace(":", "_").replace("processes-", ""),
            "name": r["name"],
        })
        doc = ET.SubElement(proc, f"{{{BPMN_NS}}}documentation")
        doc.text = (
            f"Canonical id: {r['id']} · version {r['version']} · "
            f"status {r['status']}/{r['lifecycle_status']} · "
            f"ECF cell: {r['domain']} x {r['stage']} · "
            f"Process Context: {r['pc']} · "
            f"Trigger: {r['trigger']} · Outcome: {r['outcome']} · "
            "Seed element from the OpenDEA Business Process Catalog "
            "(CR-BP-30c; decision D3=A). Clone-and-extend: replace this "
            "task with the process's real flow; L3 activities under this "
            "BP are the candidate flow steps."
        )
        ET.SubElement(proc, f"{{{BPMN_NS}}}task", {"id": "_seed_", "name": r["name"]})

    out_path.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(defs).write(out_path, encoding="utf-8", xml_declaration=True)
    print(f"bpmn-library: wrote {out_path} ({len(procs)} processes)")
    return len(procs)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    ap.add_argument("--out", required=True)
    ap.add_argument("--label", default="catalog")
    args = ap.parse_args(argv)
    build(Path(args.out), args.label)
    return 0


if __name__ == "__main__":
    sys.exit(main())
