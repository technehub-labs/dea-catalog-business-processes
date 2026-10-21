#!/usr/bin/env python3
"""OpenDEA Entity Map Generator -- L0 x L1 overview (49-cell ECF matrix)
==========================================================================
Renders a single-page CSS-Grid HTML poster from the live catalogue YAML in
dea-catalog-business-processes, plus an optional PDF/PNG rasterisation.

PROVENANCE
    Ported from the capability-map renderer
    (dea-catalog-business-capabilities, scripts/generate_capability_map.py,
    CR-DEA-BC-06). The grid renderer, CSS, evidence dots, and rasterisation
    are adapted from that proven implementation. The BC version is MIT-licensed
    org tooling; this is the same rendering approach applied to the process
    catalogue.

WHY A PORT RATHER THAN A REUSE
    The BC generator positions every entity by reading `ecf.primary.{domain,
    stage}` off each record. The PROCESS catalogue does not carry that field:
    its `ecfConformance` block is a conformance DECLARATION (framework,
    contractVersion, profile, status, affiliation, canonicalReferences), not
    a position on the ECF axes. Verified across all 3,723 canonical records:
    zero carry `ecf.primary`.

    So this port derives each record's cell from the parent link the records
    actually carry -- `process_context` on L1 groups, `context[].ref` on L2
    processes -- resolved against the L0 cell register's own `domain` and
    `lifecycle_stage` fields. That is the same evidence the decomposition
    reconciliation gate ([47]) uses, so the map and the gate agree by
    construction rather than by coincidence.

    The alternative (writing `ecf.primary` onto thousands of records to make
    the BC generator run unmodified) would write a field no canonical schema
    defines, which the evidence-before-assertion control forbids.

LAYOUT
    Top-left title block, then a 7 x 7 grid: 7 ECF domains (rows) by 7
    lifecycle stages (columns). Each cell shows the L0 cell name, the L1
    Process Group, and counts of its L2/L3/L4 members.

Usage
-----
    # Overview poster only (HTML)
    python3 scripts/generate_entity_map.py -o out/entity-map-l0-l1.html

    # With the PNG raster (requires weasyprint)
    python3 scripts/generate_entity_map.py -o out/entity-map-l0-l1.html \\
        --png out/entity-map-l0-l1.png --pdf out/entity-map-l0-l1.pdf

    # Check the walk without writing anything
    python3 scripts/generate_entity_map.py --dry-run
"""
from __future__ import annotations

import argparse
import html
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ENTITIES = REPO_ROOT / "entities" / "v1-alpha"

# Level ordering used for the density badge and the drill-down ordering.
LEVEL_OF_TYPE = {
    "ProcessContext": "L0",
    "ProcessGroup": "L1",
    "ProcessScope": "L1",
    "Process": "L2",
    "Activity": "L3",
    "Task": "L4",
}


# --------------------------------------------------------------------------- #
# Record discovery
# --------------------------------------------------------------------------- #

def iter_records(entities_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    """Yield every canonical record under entities_dir.

    research/, documentation/, discovery/, reports/ and templates/ are NOT
    canonical records: they hold candidate universes, admission depositions,
    and documentation indexes that mirror a parent entity's identity. They
    are skipped here for the same reason the entity-system gate skips them
    (see reconciliation/entity-system-registry.yaml, IMP-001).
    """
    skip_dirs = {"research", "documentation", "discovery", "reports", "templates"}
    out: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(entities_dir.rglob("*.yaml")):
        if any(part in skip_dirs for part in path.parts):
            continue
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:  # a malformed record must not kill the render
            print(f"  warn: {path}: {exc}", file=sys.stderr)
            continue
        if isinstance(doc, dict) and doc.get("id"):
            out.append((path, doc))
    return out


def level_of(doc: dict[str, Any]) -> str:
    """Resolve a record's level.

    L0 Process Context records use the cell-charter schema and carry NO
    `type` field; their level is identified by the canonical id prefix
    (`:pc-`). This is the EXT-05 convention the decomposition walk uses.
    """
    declared = LEVEL_OF_TYPE.get(str(doc.get("type") or ""))
    if declared:
        return declared
    if ":pc-" in str(doc.get("id", "")):
        return "L0"
    return "?"


def parent_context_id(doc: dict[str, Any]) -> str | None:
    """The L0 cell this record belongs to, or None.

    L1 groups carry a scalar `process_context`. L2 processes carry a
    `context` list of {ref: ...}. L3/L4 do not carry a parent context
    directly; they are resolved through their L2/L3 parent (see build_cells).
    """
    pc = doc.get("process_context")
    if isinstance(pc, str) and pc:
        return pc
    ctx = doc.get("context")
    if isinstance(ctx, list):
        for item in ctx:
            if isinstance(item, dict) and isinstance(item.get("ref"), str):
                if ":pc-" in item["ref"]:
                    return item["ref"]
            elif isinstance(item, str) and ":pc-" in item:
                return item
    return None


# --------------------------------------------------------------------------- #
# Cell assembly
# --------------------------------------------------------------------------- #

def build_cells(records: list[tuple[Path, dict[str, Any]]]) -> tuple[dict, dict]:
    """Assemble the 7 x 7 matrix.

    Returns (cells, audit) where cells maps (domain, stage) to a dict with
    the L0 cell, its L1 groups, and the member counts per level; audit
    records every placement decision so the render can report its own
    provenance and an unplaced record is never silently dropped.
    """
    by_id = {doc["id"]: (path, doc) for path, doc in records}

    l0 = {rid: (p, d) for rid, (p, d) in by_id.items() if level_of(d) == "L0"}
    l1 = {rid: (p, d) for rid, (p, d) in by_id.items() if level_of(d) == "L1"}
    l2 = {rid: (p, d) for rid, (p, d) in by_id.items() if level_of(d) == "L2"}
    l3 = {rid: (p, d) for rid, (p, d) in by_id.items() if level_of(d) == "L3"}
    l4 = {rid: (p, d) for rid, (p, d) in by_id.items() if level_of(d) == "L4"}

    # Which L3 belongs to which L2, and which L4 to which L3.
    l3_to_l2: dict[str, str] = {}
    for rid, (_p, d) in l3.items():
        parent = d.get("belongs_to_business_process")
        if isinstance(parent, str):
            l3_to_l2[rid] = parent

    l4_to_l3: dict[str, str] = {}
    for rid, (_p, d) in l4.items():
        parent = d.get("belongs_to_activity")
        if isinstance(parent, str):
            l4_to_l3[rid] = parent

    cells: dict[tuple[str, str], dict[str, Any]] = {}
    audit = {"unplaced_l1": [], "unplaced_l2": [], "unplaced_l3": [],
             "unplaced_l4": [], "orphan_l3": [], "orphan_l4": []}

    for rid, (_p, doc) in l0.items():
        key = (str(doc.get("domain", "")), str(doc.get("lifecycle_stage", "")))
        cells.setdefault(key, {
            "cell_id": rid,
            "name": doc.get("name", rid),
            "groups": [],
            "counts": {"L2": 0, "L3": 0, "L4": 0},
        })

    # L1 groups -> cell
    group_cell: dict[str, tuple[str, str]] = {}
    for rid, (_p, doc) in l1.items():
        pc = parent_context_id(doc)
        if pc and pc in l0:
            key = (str(l0[pc][1].get("domain", "")), str(l0[pc][1].get("lifecycle_stage", "")))
            cells[key]["groups"].append({"id": rid, "name": doc.get("name", rid)})
            group_cell[rid] = key
        else:
            audit["unplaced_l1"].append(rid)

    # L2 -> cell via its own context
    l2_cell: dict[str, tuple[str, str]] = {}
    for rid, (_p, doc) in l2.items():
        pc = parent_context_id(doc)
        if pc and pc in l0:
            key = (str(l0[pc][1].get("domain", "")), str(l0[pc][1].get("lifecycle_stage", "")))
            l2_cell[rid] = key
            cells[key]["counts"]["L2"] += 1
        else:
            audit["unplaced_l2"].append(rid)

    # L3 -> cell by walking up to its L2
    l3_cell: dict[str, tuple[str, str]] = {}
    for rid in l3:
        parent = l3_to_l2.get(rid)
        key = l2_cell.get(parent) if parent else None
        if key:
            l3_cell[rid] = key
            cells[key]["counts"]["L3"] += 1
        else:
            audit["unplaced_l3"].append(rid)
            if parent and parent not in l2_cell:
                audit["orphan_l3"].append((rid, parent))

    # L4 -> cell by walking up to its L3
    for rid in l4:
        parent = l4_to_l3.get(rid)
        key = l3_cell.get(parent) if parent else None
        if key:
            cells[key]["counts"]["L4"] += 1
        else:
            audit["unplaced_l4"].append(rid)
            if parent and parent not in l3_cell:
                audit["orphan_l4"].append((rid, parent))

    for key in cells:
        cells[key]["groups"].sort(key=lambda g: str(g["name"]))

    return cells, audit


def axis_order(cells: dict) -> tuple[list[str], list[str]]:
    """Domains as rows, stages as columns, in canonical order."""
    domains = sorted({d for d, _ in cells})
    stages = sorted({s for _, s in cells})

    def domain_key(name: str) -> tuple[int, str]:
        # Keep the ECF lifecycle reading order for stages; domains alphabetised.
        return (0, name)

    stage_order = ["conceive", "design", "build", "activate", "operate", "improve", "retire"]
    stages.sort(key=lambda s: (stage_order.index(s.lower()) if s.lower() in stage_order else 99, s))
    domains.sort(key=domain_key)
    return domains, stages


# --------------------------------------------------------------------------- #
# Render
# --------------------------------------------------------------------------- #

def esc(s: Any) -> str:
    return html.escape(str(s), quote=True)


# The map TYPE and the level span are part of the artefact's identity and must
# appear in every title: the H1, the <title> element, the PDF document title,
# and the file name. A poster that renders L0-L2 must never be captioned as an
# L0-L1 overview, or a reader cannot tell two different artefacts apart.
MAP_TYPE = "OpenDEA Business Process Entity Map"

SUPPORTED_DEPTHS = ("L1", "L2")


def map_title(depth: str) -> str:
    """The canonical title for a map at the given depth.

    L1 -> "OpenDEA Business Process Entity Map - L0 - L1 overview"
    L2 -> "OpenDEA Business Process Entity Map - L0 - L2 overview"
    """
    if depth not in SUPPORTED_DEPTHS:
        raise ValueError(f"unsupported depth {depth!r}; expected one of {SUPPORTED_DEPTHS}")
    return f"{MAP_TYPE} - L0 - {depth} overview"


def map_slug(depth: str) -> str:
    """File-name stem matching the title: entity-map-l0-l2-overview."""
    depth_num = depth.lower()
    return f"entity-map-l0-{depth_num}-overview"


DOMAIN_SEPARATORS = ("And", "and")


def row_label(domain: str) -> str:
    """Render a domain name for the row head, once-escaped.

    Splitting camel-case domain names on "And" keeps the seven rows readable
    at poster width. The replacement is done BEFORE escaping, so the
    ampersand is escaped exactly once and renders as a single "&".
    """
    for sep in DOMAIN_SEPARATORS:
        if sep in domain:
            return domain.replace(sep, " & ")
    return domain


def cell_html(domain: str, stage: str, cell: dict | None, depth: str = "L1",
              tree: dict | None = None) -> str:
    """Render one L0 cell.

    At depth L1 the cell shows the Process Group name and the L2/L3/L4 counts.
    At depth L2 it additionally names every Business Process in the cell, so
    the poster carries the L0 -> L1 -> L2 chain on one sheet.
    """
    if not cell:
        return (f'<div class="cell empty"><div class="cell-head">'
                f'{esc(domain)} &times; {esc(stage)}</div>'
                f'<div class="cell-body"><span class="none">no cell</span></div></div>')

    counts = dict(cell["counts"])
    l2_ids = tree["l2_by_cell"].get((domain, stage), []) if (tree and depth == "L2") else []
    n2 = len(l2_ids) if depth == "L2" else counts["L2"]

    # Density is judged on what the poster actually shows, not on the
    # invisible L3/L4 tail: at L1 that is the member count, at L2 the number
    # of named Business Processes.
    shown = n2 if depth == "L2" else counts["L2"] + counts["L3"] + counts["L4"]
    density = " dense" if shown >= 8 else (" mid" if shown >= 4 else "")

    group_rows = []
    for g in cell["groups"]:
        group_rows.append(
            f'<div class="l1-row"><span class="l1-tag">L1</span>'
            f'<span class="l1-name">{esc(g["name"])}</span></div>'
        )
    if not group_rows:
        group_rows.append('<div class="l1-row none"><span class="l1-tag">L1</span>'
                          '<span class="none">no group</span></div>')

    bp_rows = []
    if depth == "L2":
        for rid in l2_ids:
            rec = tree["records"].get(rid, {})
            bp_rows.append(
                f'<div class="l2-row"><span class="l2-tag">L2</span>'
                f'<span class="l2-name">{esc(rec.get("name", rid))}</span></div>'
            )
        if not bp_rows:
            bp_rows.append('<div class="l2-row none"><span class="l2-tag">L2</span>'
                           '<span class="none">no business process</span></div>')

    counts_html = (
        f'<div class="counts">'
        f'<span class="c c2" title="L2 Business Processes">{n2}</span>'
        f'<span class="c c3" title="L3 Activities">{counts["L3"]}</span>'
        f'<span class="c c4" title="L4 Tasks">{counts["L4"]}</span>'
        f'</div>'
    )

    return (
        f'<div class="cell{density}">'
        f'<div class="cell-head">{esc(cell["name"])}</div>'
        f'<div class="cell-axis">{esc(domain)} &times; {esc(stage)}</div>'
        f'<div class="cell-body">{"".join(group_rows)}{"".join(bp_rows)}{counts_html}</div>'
        f'</div>'
    )


def css(n_domains: int, n_stages: int) -> str:
    return f"""
  :root {{
    --bg: #ffffff; --ink: #14181d; --mid: #4a5560; --line: #c9d1d9;
    --wash: #f6f8fa; --accent: #1b4f72; --hot: #8b0000;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; background: var(--bg); color: var(--ink);
    font: 11px/1.35 -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }}
  .sheet {{ width: 100%; max-width: 1680px; margin: 0 auto; padding: 10px 14px 12px; }}
  /* Print: one poster per sheet. The @page size is set by the caller. */
  @media print {{ body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }} }}
  header {{ border-bottom: 2px solid var(--accent); padding-bottom: 5px; margin-bottom: 6px; }}
  h1 {{ margin: 0; font-size: 16px; letter-spacing: -0.2px; color: var(--accent); }}
  .sub {{ margin-top: 3px; color: var(--mid); font-size: 11px; }}
  .legend {{ margin-top: 4px; display: flex; gap: 10px; align-items: center; font-size: 9px; color: var(--mid); }}
  .legend b {{ color: var(--ink); }}
  .key {{ display: inline-flex; align-items: center; gap: 4px; }}
  .swatch {{ width: 10px; height: 10px; border: 1px solid var(--line); display: inline-block; }}
  .sw-dense {{ background: #ffe6e6; border-color: var(--hot); }}
  .sw-mid {{ background: #fdf3e0; }}
  .sw-empty {{ background: repeating-linear-gradient(45deg, #f6f8fa, #f6f8fa 4px, #eef1f4 4px, #eef1f4 8px); }}

  .grid {{ display: grid; gap: 3px;
           grid-template-columns: 124px repeat({n_stages}, minmax(0, 1fr)); }}
  .corner {{ }}
  .colhead {{ font-weight: 700; font-size: 11px; color: var(--accent);
              text-align: center; padding: 4px 0; text-transform: uppercase;
              letter-spacing: 0.5px; }}
  .rowhead {{ font-weight: 700; font-size: 11px; color: var(--accent);
              display: flex; align-items: center; padding-right: 6px;
              text-transform: uppercase; letter-spacing: 0.3px; }}

  .cell {{ border: 2px solid var(--accent); border-radius: 3px; overflow: hidden;
           display: flex; flex-direction: column; min-height: 70px; background: #fff; }}
  .cell.dense {{ border-color: var(--hot); background: #fffdfd; }}
  .cell.mid {{ background: #fffefb; }}
  .cell.empty {{ border: 1px dashed var(--line); background: var(--wash); min-height: 44px; }}
  .cell-head {{ font-weight: 700; font-size: 10px; line-height: 1.15; padding: 2px 5px 1px;
                background: var(--accent); color: #fff; }}
  .cell.dense .cell-head {{ background: var(--hot); }}
  .cell.empty .cell-head {{ background: var(--wash); color: var(--mid); font-weight: 600; }}
  .cell-axis {{ font-size: 8px; line-height: 1.15; color: var(--mid); padding: 0 5px 2px;
                background: var(--accent); }}
  .cell.dense .cell-axis {{ background: var(--hot); color: #f0d0d0; }}
  .cell.empty .cell-axis {{ display: none; }}
  .cell-body {{ padding: 3px 5px 4px; flex: 1; overflow: hidden; }}
  .l1-row {{ display: flex; gap: 3px; align-items: baseline; margin-bottom: 1px; }}
  .l1-tag {{ font-size: 8px; font-weight: 700; color: #fff; background: var(--mid);
             border-radius: 2px; padding: 0 3px; }}
  .l1-name {{ font-size: 9px; font-weight: 600; line-height: 1.2; }}
  .none {{ color: var(--mid); font-style: italic; font-size: 10px; }}
  .counts {{ margin-top: 3px; display: flex; gap: 3px; }}
  .c {{ font-size: 8px; font-weight: 700; padding: 0 3px; border-radius: 2px;
        border: 1px solid var(--line); }}
  .c2 {{ background: #eef4fa; }}
  .c3 {{ background: #f2f0fa; }}
  .c4 {{ background: #faf4ee; }}
  .l2-row {{ display: flex; gap: 3px; align-items: baseline; margin-bottom: 1px; }}
  .l2-tag {{ font-size: 7px; font-weight: 700; color: var(--accent); border: 1px solid var(--accent);
             border-radius: 2px; padding: 0 2px; flex: none; }}
  .l2-name {{ font-size: 8px; line-height: 1.25; }}
  footer {{ margin-top: 6px; padding-top: 4px; border-top: 1px solid var(--line);
            color: var(--mid); font-size: 8px; }}
"""


def render(cells: dict, domains: list[str], stages: list[str], meta: dict,
          depth: str = "L1", tree: dict | None = None) -> str:
    # Build the grid row-major so the DOM order reads correctly.
    grid = ['<div class="corner"></div>']
    for s in stages:
        grid.append(f'<div class="colhead">{esc(s)}</div>')
    for d in domains:
        grid.append(f'<div class="rowhead">{esc(row_label(d))}</div>')
        for s in stages:
            grid.append(cell_html(d, s, cells.get((d, s)), depth=depth, tree=tree))

    audit = meta.get("audit", {})
    unplaced = {k: v for k, v in audit.items() if v}

    audit_rows = "".join(
        f"<tr><td>{esc(k)}</td><td>{len(v)}</td>"
        f"<td class='mono'>{esc(', '.join(str(x) for x in v[:6]))}"
        f"{' ...' if len(v) > 6 else ''}</td></tr>"
        for k, v in sorted(unplaced.items())
    )
    audit_block = (
        f"<h2>Placement audit</h2><table class='audit'>"
        f"<tr><th>bucket</th><th>count</th><th>records</th></tr>{audit_rows}</table>"
        if audit_rows else
        "<h2>Placement audit</h2><p class='none'>Every canonical record placed "
        "into exactly one cell. No unplaced records.</p>"
    )

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{esc(meta["title"])}</title>
<style>{css(len(domains), len(stages))}</style>
<style>
  h2 {{ font-size: 11px; margin: 7px 0 3px; color: var(--accent); }}
  table.audit {{ border-collapse: collapse; font-size: 10px; }}
  table.audit th, table.audit td {{ border: 1px solid var(--line); padding: 2px 6px; text-align: left; }}
  .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 9px; color: var(--mid); }}
</style>
</head><body>
<div class="sheet">
  <header>
    <h1>{esc(meta["title"])}</h1>
    <div class="sub">{esc(meta['repo'])} &middot; {esc(meta['revision'])} &middot; generated {esc(meta['generated_at'])}</div>
    <div class="legend">
      <span class="key"><span class="swatch sw-dense"></span><b>&ge;8</b> {esc(meta["density_unit"])}</span>
      <span class="key"><span class="swatch sw-mid"></span><b>4-7</b> {esc(meta["density_unit"])}</span>
      <span class="key"><span class="swatch sw-empty"></span>no cell</span>
      <span class="key"><span class="c c2">{meta['totals']['L2']}</span>L2 Processes</span>
      <span class="key"><span class="c c3">{meta['totals']['L3']}</span>L3 Activities</span>
      <span class="key"><span class="c c4">{meta['totals']['L4']}</span>L4 Tasks</span>
      <span class="key"><b>{meta['totals']['L0']}</b> L0 cells &middot; <b>{meta['totals']['L1']}</b> L1 groups</span>
    </div>
  </header>
  <div class="grid">{"".join(grid)}</div>
  {audit_block}
  <footer>
    Cell position is derived from the parent link each record carries
    (<code>process_context</code> on L1 groups, <code>context[].ref</code> on L2
    processes, <code>belongs_to_business_process</code> on L3,
    <code>belongs_to_activity</code> on L4) resolved against the L0 cell
    register's own <code>domain</code> and <code>lifecycle_stage</code>. This is
    the same evidence the decomposition reconciliation gate ([47]) uses, so the
    map and the gate agree by construction. Research, documentation, discovery,
    report and template artefacts are excluded: they are not canonical records.
    This map renders the <b>L0 - {esc(meta['depth'])}</b> chain; L3 and L4 counts are shown
    per cell for reference and their members are carried by the per-cell drill-down pages.
    Printed at {esc(paper_for(meta["depth"]))}, one poster per sheet.<br>
    Renderer ported from the capability-map generator (CR-DEA-BC-06).
  </footer>
</div>
</body></html>
"""


# --------------------------------------------------------------------------- #
# Rasterisation
# --------------------------------------------------------------------------- #

# --------------------------------------------------------------------------- #
# Drill-down: one page per cell, L2 -> L3 -> L4
# --------------------------------------------------------------------------- #

def drilldown_html(cell_key: tuple[str, str], cell: dict, tree: dict, meta: dict) -> str:
    """Render one cell's L2 processes with their L3 activities and L4 tasks.

    A single page cannot legibly carry 2,900 Tasks, so the overview carries
    the counts and the drill-down carries the members. This is the (c) half of
    the design: overview for shape, drill-down for detail.
    """
    domain, stage = cell_key
    out = [f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{esc(meta["title"])} - {esc(cell["name"])}</title>
<style>{css(7, 7)}
.cellbody {{ padding: 8px 10px; }}
.bp {{ border: 1px solid var(--line); border-left: 3px solid var(--accent);
       border-radius: 3px; padding: 6px 8px; margin-bottom: 6px; background: #fff; }}
.bp-head {{ display: flex; align-items: baseline; gap: 6px; }}
.bp-name {{ font-weight: 700; font-size: 12px; }}
.bp-meta {{ font-size: 9px; color: var(--mid); }}
.ax {{ margin: 5px 0 3px; padding-left: 8px; border-left: 2px dotted var(--line); }}
.act {{ font-size: 10px; margin-bottom: 1px; }}
.act .t {{ color: var(--mid); font-size: 9px; }}
.tk {{ color: #8a8f98; font-size: 9px; }}
a {{ color: var(--accent); }}
</style></head><body>
<div class="sheet">
<header>
  <h1>{esc(cell["name"])}</h1>
  <div class="sub-title">{esc(meta["title"])}</div>
  <div class="sub">{esc(domain)} &times; {esc(stage)} &middot; {esc(cell['cell_id'])} &middot; {esc(meta['repo'])} @ {esc(meta['revision'])}</div>
</header>
<div class="cellbody">"""]

    l2_ids = tree["l2_by_cell"].get(cell_key, [])
    if not l2_ids:
        out.append('<p class="none">No L2 Business Processes in this cell.</p>')
    for rid in l2_ids:
        rec = tree["records"].get(rid, {})
        out.append(
            f'<div class="bp"><div class="bp-head"><span class="bp-name">{esc(rec.get("name", rid))}</span>'
            f'<span class="bp-meta">{esc(rid)}</span></div>'
            f'<div class="bp-meta">intent: {esc(rec.get("process_intent","-"))} &middot; '
            f'type: {esc(rec.get("process_type","-"))}</div>'
        )
        acts = tree["l3_by_l2"].get(rid, [])
        if acts:
            out.append('<div class="ax">')
            for arid in acts:
                arec = tree["records"].get(arid, {})
                tasks = tree["l4_by_l3"].get(arid, [])
                out.append(
                    f'<div class="act"><b>{esc(arec.get("name", arid))}</b> '
                    f'<span class="t">&middot; {len(tasks)} L4 tasks</span></div>'
                )
                for trid in tasks:
                    trec = tree["records"].get(trid, {})
                    out.append(f'<div class="tk">&nbsp;&nbsp;&middot; {esc(trec.get("name", trid))}</div>')
            out.append('</div>')
        out.append('</div>')

    out.append(f"""
</div>
<footer>Derived from the same parent links as the overview: process_context (L1),
context[].ref (L2), belongs_to_business_process (L3), belongs_to_activity (L4).</footer>
</div></body></html>""")
    return "".join(out)


def build_tree(records: list[tuple[Path, dict[str, Any]]]) -> dict:
    """Index records by id and by their parent chain, for drill-down rendering."""
    by_id = {doc["id"]: doc for _p, doc in records}
    l0 = {rid: d for rid, d in by_id.items() if level_of(d) == "L0"}
    l1 = {rid: d for rid, d in by_id.items() if level_of(d) == "L1"}
    l2 = {rid: d for rid, d in by_id.items() if level_of(d) == "L2"}
    l3 = {rid: d for rid, d in by_id.items() if level_of(d) == "L3"}
    l4 = {rid: d for rid, d in by_id.items() if level_of(d) == "L4"}

    l2_by_cell: dict[tuple[str, str], list[str]] = defaultdict(list)
    for rid, doc in sorted(l2.items()):
        pc = parent_context_id(doc)
        if pc and pc in l0:
            key = (str(l0[pc].get("domain", "")), str(l0[pc].get("lifecycle_stage", "")))
            l2_by_cell[key].append(rid)

    l3_by_l2: dict[str, list[str]] = defaultdict(list)
    for rid, doc in sorted(l3.items()):
        parent = doc.get("belongs_to_business_process")
        if isinstance(parent, str):
            l3_by_l2[parent].append(rid)

    l4_by_l3: dict[str, list[str]] = defaultdict(list)
    for rid, doc in sorted(l4.items()):
        parent = doc.get("belongs_to_activity")
        if isinstance(parent, str):
            l4_by_l3[parent].append(rid)

    return {"records": by_id, "l2_by_cell": dict(l2_by_cell),
            "l3_by_l2": dict(l3_by_l2), "l4_by_l3": dict(l4_by_l3)}


# ONE poster per sheet, always, at a legible scale.
#
# The depth decides the paper. An L0-L1 poster fits A3 landscape. An L0-L2
# poster additionally names 145 Business Processes (median 3 per cell, max 9)
# and its grid is ~1137px against ~1062px of A3 content height. Compressing
# that into A3 means ~6px body type, which is not legible. So L2 prints at A2
# landscape (594 x 420 mm, the standard ISO poster size) rather than
# pretending to be an A3 sheet.
#
# This is stated in the artefact and reported by --dry-run so the paper size
# is never a silent surprise.
PAPER_FOR_DEPTH = {"L1": "A3 landscape", "L2": "A2 landscape"}


def paper_for(depth: str) -> str:
    return PAPER_FOR_DEPTH.get(depth, "A3 landscape")


def _sp_paper_css(depth: str = "L1") -> "io.BytesIO | None":
    """Return the @page override as a file-like object weasyprint accepts."""
    import io as _io
    css = f"@page {{ size: {paper_for(depth)}; margin: 8mm; }}\n"
    return _io.BytesIO(css.encode("utf-8"))


def rasterise(html_path: Path, png_out: Path | None, pdf_out: Path | None,
              depth: str = "L1") -> None:
    try:
        from weasyprint import HTML as WP_HTML
    except ImportError:
        print("  warn: weasyprint not installed; skipping rasterisation "
              "(the HTML poster is the deliverable)", file=sys.stderr)
        return
    if pdf_out:
        pdf_out.parent.mkdir(parents=True, exist_ok=True)
        # One poster per A3 landscape sheet. The 7x7 grid at ~1100px of
        # content height paginates across two default sheets otherwise, and a
        # two-sheet "single page map" is not a map anyone can read.
        page_css = _sp_paper_css(depth)
        WP_HTML(filename=str(html_path)).write_pdf(str(pdf_out),
                                                  stylesheets=[page_css] if page_css else None)
        print(f"  wrote {pdf_out}")
    if png_out:
        png_out.parent.mkdir(parents=True, exist_ok=True)
        import subprocess as _sp
        tmp = png_out.with_suffix(".pdf")
        # The temp PDF MUST carry the same @page override as the real one,
        # otherwise the raster path paginates differently from the PDF path
        # and the two deliverables disagree about how many sheets the poster is.
        page_css = _sp_paper_css(depth)
        WP_HTML(filename=str(html_path)).write_pdf(str(tmp),
                                                  stylesheets=[page_css] if page_css else None)
        # pdftoppm names multi-page output <base>-1.png, <base>-2.png ... A
        # poster that paginates must be reported as such rather than silently
        # producing no file at the requested path.
        prefix = png_out.with_suffix("")
        for stale in prefix.parent.glob(prefix.name + "-*.png"):
            stale.unlink()
        proc = _sp.run(["pdftoppm", "-png", "-r", "110", str(tmp), str(prefix)],
                       capture_output=True, text=True)
        tmp.unlink(missing_ok=True)
        if proc.returncode != 0:
            print(f"  warn: pdftoppm failed ({proc.stderr.strip()[:90]}); PNG skipped",
                  file=sys.stderr)
            return
        pages = sorted(prefix.parent.glob(prefix.name + "-*.png"))
        if not pages:
            print(f"  warn: pdftoppm produced no page images; PNG skipped", file=sys.stderr)
            return
        if len(pages) == 1:
            pages[0].rename(png_out)
            print(f"  wrote {png_out}")
            return
        # Multiple pages: the poster does not fit one sheet. Keep every page
        # with a numbered suffix and say so, instead of pretending it is one
        # image.
        print(f"  wrote {len(pages)} page images (the poster does NOT fit one "
              f"sheet at this paper size):")
        for i, page in enumerate(pages, 1):
            target = png_out.with_name(f"{png_out.stem}-{i}{png_out.suffix}")
            page.rename(target)
            print(f"    {target}")


# --------------------------------------------------------------------------- #

def main(argv: list[str] | None = None) -> int:
    doc = __doc__ or ""
    ap = argparse.ArgumentParser(description=doc.split("\n")[1] if "\n" in doc else "entity map generator")
    ap.add_argument("--entities", default=str(DEFAULT_ENTITIES),
                    help="path to the entities root (default: entities/v1-alpha)")
    ap.add_argument("-o", "--out", default=None,
                    help="output HTML path (default: out/<title slug>.html, so the "
                         "file name always matches the map's title and depth)")
    ap.add_argument("--png", default=None, help="also write a rasterised PNG")
    ap.add_argument("--pdf", default=None, help="also write a PDF")
    ap.add_argument("--depth", default="L2", choices=list(SUPPORTED_DEPTHS),
                    help="deepest level the poster renders: L1 shows the Process Group "
                         "name and counts; L2 also names every Business Process")
    ap.add_argument("--drilldown-dir", default=None,
                    help="also write one drill-down page per L0 cell into this directory")
    ap.add_argument("--dry-run", action="store_true",
                    help="report the walk and the placement audit; write nothing")
    args = ap.parse_args(argv)

    entities_dir = Path(args.entities)
    if not entities_dir.is_dir():
        print(f"ERROR: no entity catalog at {entities_dir}", file=sys.stderr)
        return 2

    print(f"OpenDEA entity map generator\n  entities: {entities_dir}")
    records = iter_records(entities_dir)
    print(f"  loaded {len(records)} canonical records")

    cells, audit = build_cells(records)
    domains, stages = axis_order(cells)
    print(f"  grid: {len(domains)} domains x {len(stages)} stages = {len(domains)*len(stages)} cells "
          f"({len(cells)} occupied)")

    totals = {"L0": 0, "L1": 0, "L2": 0, "L3": 0, "L4": 0}
    for _p, d in records:
        lv = level_of(d)
        if lv in totals:
            totals[lv] += 1
    print(f"  levels: " + "  ".join(f"{k}={v}" for k, v in totals.items()))

    unplaced = {k: len(v) for k, v in audit.items() if v}
    if unplaced:
        print("  PLACEMENT AUDIT (not silently dropped):")
        for k, v in sorted(unplaced.items()):
            print(f"    {k}: {v}")
            for item in audit[k][:5]:
                print(f"        {item}")
    else:
        print("  placement audit: every canonical record placed exactly once")

    if args.dry_run:
        print("\n--dry-run: nothing written")
        return 0

    import datetime
    try:
        revision = __import__("subprocess").run(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True).stdout.strip() or "unknown"
    except Exception:
        revision = "unknown"

    title = map_title(args.depth)
    tree = build_tree(records)

    meta = {
        "title": title,
        "depth": args.depth,
        "density_unit": "processes" if args.depth == "L2" else "members",
        "paper": paper_for(args.depth),
        "repo": "technehub-labs/dea-catalog-business-processes",
        "revision": revision,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "totals": totals,
        "audit": audit,
    }

    out = Path(args.out) if args.out else (REPO_ROOT / "out" / f"{map_slug(args.depth)}.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(cells, domains, stages, meta, depth=args.depth, tree=tree),
                   encoding="utf-8")
    print(f"\n  title: {title}")
    print(f"  paper: {paper_for(args.depth)}")
    print(f"  wrote {out} ({out.stat().st_size:,} bytes)")

    if args.drilldown_dir:
        dd_dir = Path(args.drilldown_dir)
        dd_dir.mkdir(parents=True, exist_ok=True)
        tree = build_tree(records)
        n = 0
        for key, cell in sorted(cells.items()):
            slug = f"{key[0]}-{key[1]}".lower()
            page = dd_dir / f"{slug}.html"
            page.write_text(drilldown_html(key, cell, tree, meta), encoding="utf-8")
            n += 1
        print(f"  wrote {n} drill-down pages to {dd_dir}")

    if args.png or args.pdf:
        rasterise(out, Path(args.png) if args.png else None,
                   Path(args.pdf) if args.pdf else None, depth=args.depth)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())