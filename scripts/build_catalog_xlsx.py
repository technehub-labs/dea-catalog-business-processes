#!/usr/bin/env python3
"""build_catalog_xlsx.py — CR-BP-30b: the structured Excel workbook.

Decision D2 = 6 sheets: 01_records / 02_lineage / 03_dispositions /
04_register_audit / 05_change_requests / 06_contributions. Sheet 1
carries the "versions of processes" column the request asked for
(`version` per record). Deterministic: sorted iteration everywhere;
no timestamps in the output.

Usage:
  python3 scripts/build_catalog_xlsx.py --out out/v0.5.0/catalog.xlsx
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
ENTITIES = ROOT / "entities" / "v1-alpha"
STATE_DIRS = ("research", "candidates", "retired")

HEAD_FONT = Font(bold=True)

DOMAINS = [
    "PartyAndRelationship", "GovernanceAndExistence", "ProductAndValue",
    "AgencyAndOrganization", "StrategyAndDirection", "FinanceAndAccounting",
    "EnablementAndOperations",
]
STAGES = ["Conceive", "Design", "Build", "Activate", "Operate", "Improve", "Retire"]


def _level_of(rid: str, rtype) -> str:
    if rid.startswith("processes:pc-"):
        return "L0 ProcessContext"
    return {"ProcessGroup": "L1 ProcessGroup", "Process": "L2 Process",
            "Activity": "L3 Activity", "Task": "L4 Task"}.get(rtype, rtype or "?")


def _load_all():
    records, lineage = [], []
    for p in sorted(ENTITIES.rglob("*.yaml")):
        if any(s in p.parts for s in STATE_DIRS):
            continue
        d = yaml.safe_load(p.read_text()) or {}
        rid = d.get("id")
        if not isinstance(rid, str):
            continue
        records.append(d)
        for e in d.get("composes") or []:
            if isinstance(e, dict):
                lineage.append((e.get("source_id", ""), e.get("target_id", ""),
                                e.get("relationship_type", "composes"),
                                e.get("status", ""), e.get("asserted_by", "")))
        for key, rt in (("belongs_to_activity", "belongs_to"),
                        ("belongs_to_business_process", "belongs_to")):
            t = d.get(key)
            if isinstance(t, str) and t:
                lineage.append((rid, t, rt, "active", ""))
    return records, sorted(set(lineage))


def _dispositions():
    reg = ROOT / "reconciliation" / "dispositions" / "register.yaml"
    if not reg.exists():
        return []
    d = yaml.safe_load(reg.read_text()) or {}
    entries = d.get("dispositions") or []
    rows = []
    for e in entries:
        if isinstance(e, dict):
            rows.append((e.get("record_id", e.get("id", "")),
                         e.get("disposition", e.get("decision", "")),
                         e.get("rationale", ""), e.get("cr", "")))
    return sorted(rows)


def _register_audit():
    rows = []
    for p in sorted(ENTITIES.glob("*/processes-pc-*.yaml")):
        d = yaml.safe_load(p.read_text()) or {}
        adm = d.get("admission") or {}
        rows.append((d.get("domain", ""), d.get("lifecycle_stage", ""),
                     d.get("id", ""), d.get("name", ""),
                     str(adm.get("score", "")), str(adm.get("max", "")),
                     adm.get("decision", ""), adm.get("date", "")))
    return sorted(rows)


def _change_requests():
    rows = []
    for p in sorted((ROOT / "change-requests").glob("CR-*.md")):
        head = "\n".join(p.read_text().splitlines()[:30])
        title = status = date = layer = ""
        for line in head.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
            elif line.startswith("**Status**"):
                status = line.split(":", 1)[1].strip().strip("*")
            elif line.startswith("**Date**"):
                date = line.split(":", 1)[1].strip()
            elif line.startswith("**Layer**"):
                layer = line.split(":", 1)[1].strip()
        rows.append((p.stem, title, status, date, layer))
    return rows


def _contributions():
    rows = []
    cdir = ROOT / "contributions" / "processes"
    if not cdir.is_dir():
        return rows
    for p in sorted(cdir.rglob("*.yaml")):
        if p.name == "PROCESS-CONTRIBUTION-TEMPLATE.yaml":
            continue
        d = yaml.safe_load(p.read_text()) or {}
        rows.append((str(p.relative_to(cdir)),
                     d.get("id", d.get("name", "")),
                     d.get("status", "submitted"),
                     "yes" if p.with_name(p.stem + ".report.md").exists() else "no"))
    return sorted(rows)


def _sheet(wb, title, headers, rows):
    ws = wb.create_sheet(title)
    ws.append(headers)
    for c in ws[1]:
        c.font = HEAD_FONT
    for r in rows:
        ws.append([str(x) if x is not None else "" for x in r])
    for i, h in enumerate(headers, start=1):
        ws.column_dimensions[get_column_letter(i)].width = min(max(14, len(h) + 4), 60)
    ws.freeze_panes = "A2"
    return ws


def build(out_path: Path) -> None:
    records, lineage = _load_all()
    wb = Workbook()
    wb.remove(wb.active)

    rec_rows = sorted(
        (d.get("id", ""), d.get("name", ""), _level_of(d.get("id", ""), d.get("type")),
         d.get("domain", ""), d.get("lifecycle_stage", ""), d.get("version", ""),
         d.get("status", ""), d.get("lifecycle_status", ""))
        for d in records
    )
    _sheet(wb, "01_records",
           ["id", "name", "level", "domain", "lifecycle_stage", "version",
            "status", "lifecycle_status"], rec_rows)
    _sheet(wb, "02_lineage",
           ["source_id", "target_id", "relationship_type", "status", "asserted_by"],
           lineage)
    _sheet(wb, "03_dispositions", ["record_id", "disposition", "rationale", "cr"],
           _dispositions())
    _sheet(wb, "04_register_audit",
           ["domain", "lifecycle_stage", "pc_id", "pc_name", "admission_score",
            "admission_max", "decision", "date"], _register_audit())
    _sheet(wb, "05_change_requests", ["id", "title", "status", "date", "layer"],
           _change_requests())
    _sheet(wb, "06_contributions", ["file", "record", "status", "report_present"],
           _contributions())

    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)
    # Determinism: openpyxl stamps docProps timestamps at save time (and
    # re-stamps `modified` even when pinned). Rewrite the archive with a
    # canonical core.xml so two builds byte-compare (CR-BP-30g contract).
    import zipfile
    canonical_core = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"'
        ' xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"'
        ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:creator>OpenDEA process catalog (CR-BP-30b)</dc:creator>'
        '<dcterms:created xsi:type="dcterms:W3CDTF">2026-01-01T00:00:00Z</dcterms:created>'
        '<dcterms:modified xsi:type="dcterms:W3CDTF">2026-01-01T00:00:00Z</dcterms:modified>'
        '</cp:coreProperties>')
    entries = [(i, out_path.read_bytes()) for i in [0]][0:0]  # noqa placeholder
    with zipfile.ZipFile(out_path) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        for info, data in items:
            if info.filename == "docProps/core.xml":
                data = canonical_core.encode("utf-8")
            # Pin entry timestamps too: writestr defaults them to now().
            pinned = zipfile.ZipInfo(info.filename, date_time=(1980, 1, 1, 0, 0, 0))
            pinned.compress_type = zipfile.ZIP_DEFLATED
            pinned.external_attr = info.external_attr
            z.writestr(pinned, data)
    print(f"catalog-xlsx: wrote {out_path} "
          f"(records={len(rec_rows)} lineage={len(lineage)})")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    build(Path(args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
