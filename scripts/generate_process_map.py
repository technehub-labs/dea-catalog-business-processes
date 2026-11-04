#!/usr/bin/env python3
"""generate_process_map.py — CR-BP-30a: the L0 ⊃ L1 ⊃ L2 ECF process map.

Renders the catalog as a static, deterministic HTML poster on the ECF 7x7
matrix (decision D1 = A: ECF grid overlay). Cells are the 49 Process
Contexts; each cell stacks its Process Groups as ribbons; each ribbon
lists its L2 Business Processes as sub-rows. Adapted from the Business
Capabilities catalog's generate_capability_map.py pattern (CR-BP-30 §4.3)
for the process substrate: entities/v1-alpha containment tree, PC
records at cell roots, group `process_context` back-links, group
`composes` edges to L2.

Deterministic: sorted iteration everywhere; no timestamps in output
(the version label is caller-supplied). PNG rasterization is optional
(--png) via weasyprint + pdftoppm per CR-BP-30 §2 artifact #2; the CI
publish workflow installs both.

Usage:
  python3 scripts/generate_process_map.py --label v0.5.0 \
      --out out/v0.5.0/process-map.html [--png out/v0.5.0/process-map-a3.png] [--dpi 300]
"""

from __future__ import annotations

import argparse
import html
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTITIES = ROOT / "entities" / "v1-alpha"

DOMAINS = [
    ("PartyAndRelationship", "Party & Relationship", "pr"),
    ("GovernanceAndExistence", "Governance & Existence", "ge"),
    ("ProductAndValue", "Product & Value", "pv"),
    ("AgencyAndOrganization", "Agency & Organization", "ao"),
    ("StrategyAndDirection", "Strategy & Direction", "sd"),
    ("FinanceAndAccounting", "Finance & Accounting", "fa"),
    ("EnablementAndOperations", "Enablement & Operations", "eo"),
]
STAGES = ["Conceive", "Design", "Build", "Activate", "Operate", "Improve", "Retire"]


def _load_records():
    pcs, groups, processes = {}, {}, {}
    for p in sorted(ENTITIES.rglob("*.yaml")):
        parts = p.parts
        if any(s in parts for s in ("research", "candidates", "retired")):
            continue
        d = yaml.safe_load(p.read_text()) or {}
        rid = d.get("id")
        if not isinstance(rid, str):
            continue
        if rid.startswith("processes:pc-"):
            pcs[rid] = d
        elif d.get("type") == "ProcessGroup":
            groups[rid] = d
        elif d.get("type") == "Process":
            processes[rid] = d
    return pcs, groups, processes


def _cell_index(pcs, groups, processes):
    """cell (domain, stage) -> {pc, [ (group, [process records]) ]}."""
    group_children = {}
    for gid, g in groups.items():
        kids = []
        for e in g.get("composes") or []:
            tid = e.get("target_id")
            if tid in processes:
                kids.append(processes[tid])
        group_children[gid] = sorted(kids, key=lambda r: r["id"])

    cell = {}
    for pc_id, pc in sorted(pcs.items()):
        key = (pc.get("domain"), pc.get("lifecycle_stage"))
        ribbons = []
        for gid, g in sorted(groups.items()):
            pc_ref = g.get("process_context")
            pc_ref_id = pc_ref.get("id") if isinstance(pc_ref, dict) else pc_ref
            if pc_ref_id == pc_id:
                ribbons.append((g, group_children.get(gid, [])))
        cell[key] = {"pc": pc, "ribbons": ribbons}
    return cell


def render_html(label: str, ecf_ref: str = "ECF v2.5.0") -> str:
    pcs, groups, processes = _load_records()
    cell = _cell_index(pcs, groups, processes)
    total = len(pcs) + len(groups) + len(processes) + 2900  # + L4 tasks
    n_l4 = sum(1 for _ in ENTITIES.rglob("processes-task-*.yaml"))
    total = len(pcs) + len(groups) + len(processes) + n_l4

    out = ["""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>OpenDEAM Business Process Catalog</title>
<style>
:root { --cell-bg: #f7f8fa; --ribbon: #e8eef7; --ink: #1a2332; --muted: #5b6b7f; --line: #d3dae3; --accent: #2456a6; }
* { box-sizing: border-box; }
body { margin: 0; padding: 24px 28px; font: 13px/1.45 -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; color: var(--ink); background: #fff; }
h1 { font-size: 15px; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); margin: 0 0 2px; }
h2 { font-size: 26px; margin: 0 0 4px; }
.meta { color: var(--muted); font-size: 12px; margin-bottom: 18px; }
.grid { display: grid; grid-template-columns: 150px repeat(7, 1fr); gap: 6px; }
.corner { }
.axis { background: var(--accent); color: #fff; font-weight: 600; font-size: 11.5px; padding: 7px 8px; border-radius: 3px; text-align: center; }
.domain { background: var(--accent); color: #fff; font-weight: 600; font-size: 12px; padding: 8px; border-radius: 3px; display: flex; align-items: center; }
.cellbox { background: var(--cell-bg); border: 1px solid var(--line); border-radius: 3px; padding: 7px 8px; min-height: 64px; }
.pcname { font-weight: 700; font-size: 12px; margin-bottom: 6px; }
.ribbon { background: var(--ribbon); border-left: 3px solid var(--accent); border-radius: 2px; padding: 4px 6px; margin-bottom: 4px; }
.ribbon .gname { font-weight: 600; font-size: 11px; }
.ribbon ul { margin: 2px 0 0; padding-left: 14px; }
.ribbon li { font-size: 10.5px; color: var(--ink); }
.legend { margin-top: 18px; color: var(--muted); font-size: 11.5px; }
.attrib { margin-top: 6px; color: var(--muted); font-size: 10.5px; }
</style>
</head>
<body>
<h1>OpenDEAM</h1>
<h2>Business Process Catalog — ECF 7×7 Process Matrix</h2>
<div class="meta">"""]
    out.append(html.escape(f"{label} · {total} canonical records "
                           f"({len(pcs)} L0 · {len(groups)} L1 · {len(processes)} L2 · {n_l4} L4) · {ecf_ref}"))
    out.append('</div>\n<div class="grid">\n<div class="corner"></div>')
    for _full, disp, _c in DOMAINS:
        parts = disp.replace(" & ", "<br>").split("<br>")
        out.append(f'<div class="axis">{html.escape(disp)}</div>' if False else
                   '<div class="axis">' + "<br>".join(html.escape(x) for x in parts) + "</div>")
    for full, disp, code in DOMAINS:
        out.append(f'<div class="domain">{html.escape(disp)}</div>')
        for stage in STAGES:
            entry = cell.get((full, stage))
            out.append('<div class="cellbox">')
            if entry:
                out.append(f'<div class="pcname">{html.escape(entry["pc"].get("name", ""))}</div>')
                for g, kids in entry["ribbons"]:
                    out.append('<div class="ribbon">')
                    out.append(f'<div class="gname">{html.escape(g.get("name", ""))}</div>')
                    if kids:
                        out.append("<ul>")
                        for k in kids:
                            out.append(f"<li>{html.escape(k.get('name', ''))}</li>")
                        out.append("</ul>")
                    out.append("</div>")
            else:
                out.append('<div style="color:var(--muted);font-size:10.5px">—</div>')
            out.append("</div>")
    out.append(f"""</div>
<div class="legend"><b>Legend</b> — cell: L0 Process Context (domain × lifecycle stage); blue-edged ribbon: L1 Process Group; bullets: L2 Business Processes. L3 Activities and L4 Tasks decompose inside each record's directory (see the record READMEs). Status/lifecycle detail lives in the catalog XLSX and the per-record README pages.</div>
<div class="attrib">TechNeHub Labs · OpenDEAM federation · generated by scripts/generate_process_map.py (CR-BP-30a; decision D1=A) · deterministic render</div>
</body>
</html>
""")
    return "\n".join(out)


def render_png(html_path: Path, png_path: Path, dpi: int) -> None:
    """HTML -> PDF (weasyprint) -> PNG (pdftoppm), per CR-BP-30 §2 artifact 2."""
    pdf_path = html_path.with_suffix(".pdf")
    try:
        import weasyprint  # noqa: F401
    except ImportError:
        print("WARN: weasyprint not installed; skipping PNG (CI installs it)")
        return
    weasyprint.HTML(str(html_path)).write_pdf(str(pdf_path))
    subprocess.run(["pdftoppm", "-png", "-r", str(dpi),
                    "-singlefile", str(pdf_path), str(png_path.with_suffix(""))],
                   check=True)
    pdf_path.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    ap.add_argument("--label", required=True, help="version label, e.g. v0.5.0")
    ap.add_argument("--out", required=True, help="output HTML path")
    ap.add_argument("--png", default=None, help="output A3 PNG path (optional)")
    ap.add_argument("--dpi", type=int, default=300)
    args = ap.parse_args(argv)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    html_text = render_html(args.label)
    out.write_text(html_text)
    print(f"process-map: wrote {out} ({len(html_text)} bytes)")
    if args.png:
        render_png(out, Path(args.png), args.dpi)
        if Path(args.png).exists():
            print(f"process-map: wrote {args.png}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
