#!/usr/bin/env python3
"""Render the CR-BP-239 poster and offline HTML from a publication model.

This module deliberately does not read canonical YAML. Entity facts, ECF
coordinates, hierarchy assertions, findings and provenance come only from the
versioned publication-model JSON produced by build_publication_model.py.
"""
from __future__ import annotations

import argparse
import base64
import collections
import gzip
import hashlib
import html
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODEL = ROOT / "out" / "process-catalogue.json"
SCHEMA = ROOT / "schemas" / "publication-model.schema.json"
REPO = "technehub-labs/dea-catalog-business-processes"


def _esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _canonical_digest(model: dict[str, Any]) -> str:
    payload = {key: value for key, value in model.items() if key != "model_digest"}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                     ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def validate_model(model: dict[str, Any], schema_path: Path = SCHEMA) -> None:
    """Reject invalid schema, stale digest, duplicate IDs or coordinates."""
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(Draft7Validator(schema).iter_errors(model),
                    key=lambda err: list(err.path))
    if errors:
        summary = "; ".join(
            f"{'/'.join(map(str, err.path))}: {err.message}" for err in errors[:8]
        )
        raise ValueError(f"publication model does not match its schema: {summary}")
    if _canonical_digest(model) != model.get("model_digest"):
        raise ValueError("publication model digest does not match its contents")
    entity_ids = [entity.get("id") for entity in model["entities"]]
    if len(entity_ids) != len(set(entity_ids)):
        raise ValueError("publication model contains duplicate entity identities")
    coordinates = [(cell["domain"], cell["stage"]) for cell in model["coordinates"]]
    if len(coordinates) != 49 or len(set(coordinates)) != 49:
        raise ValueError("publication model must contain 49 unique ECF coordinates")


def load_model(path: Path, schema_path: Path = SCHEMA) -> dict[str, Any]:
    model = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(model, dict):
        raise ValueError("publication model root must be an object")
    validate_model(model, schema_path)
    return model


def _entity_maps(model: dict[str, Any]) -> tuple[dict[str, dict], dict[str, list[dict]]]:
    entities = {entity["id"]: entity for entity in model["entities"]}
    by_coordinate: dict[str, list[dict]] = collections.defaultdict(list)
    for entity in model["entities"]:
        coord = entity.get("ecf_coordinate")
        if isinstance(coord, dict):
            by_coordinate[coord["identifier"]].append(entity)
    return entities, by_coordinate


def _finding_counts(model: dict[str, Any]) -> tuple[collections.Counter, collections.Counter]:
    severity = collections.Counter(item.get("severity", "unspecified")
                                   for item in model.get("findings", []))
    codes = collections.Counter(item.get("code", "unspecified")
                                for item in model.get("findings", []))
    return severity, codes


def _axis_label(domain: str) -> str:
    return domain.replace("And", " & ")


def render_poster_html(model: dict[str, Any]) -> str:
    """Create the one-page L0-L2 A1 poster source from the model."""
    validate_model(model)
    entities, _ = _entity_maps(model)
    provenance = model["provenance"]
    totals = model["inventory"]["by_level"]
    severity, code_counts = _finding_counts(model)
    issue_count = sum(severity.values())
    cells_by_coordinate: dict[tuple[str, str], str] = {}
    for coordinate in model["coordinates"]:
        context_ids = coordinate["process_context_ids"]
        group_ids = coordinate["process_group_ids"]
        bp_ids = coordinate["business_process_ids"]
        context_names = [entities[rid].get("record", {}).get("name", rid)
                         for rid in context_ids if rid in entities]
        group_names = [entities[rid].get("record", {}).get("name", rid)
                       for rid in group_ids if rid in entities]
        bp_names = [entities[rid].get("record", {}).get("name", rid)
                    for rid in bp_ids if rid in entities]
        marker = f"<p class='empty'>No L0 context resolves to this coordinate.</p>" if not context_ids else ""
        groups = "".join(f"<li><b>L1</b> {_esc(name)}</li>" for name in group_names)
        processes = "".join(f"<li><b>L2</b> {_esc(name)}</li>" for name in bp_names)
        cell_findings = [f for f in model.get("findings", [])
                         if f.get("source_id") in set(context_ids + group_ids + bp_ids)
                         or f.get("target_id") in set(context_ids + group_ids + bp_ids)]
        flagged = " <span class='flag' title='Model findings affect relationships in this cell'>!</span>" if cell_findings else ""
        cells_by_coordinate[(coordinate["domain"], coordinate["stage"])] = (
            f"<article class='cell{' flagged' if cell_findings else ''}'>"
            f"<h3>{_esc(', '.join(context_names) or 'Unresolved L0 context')}{flagged}</h3>"
            f"<p class='axis'>{_esc(_axis_label(coordinate['domain']))} · {_esc(coordinate['stage'])}</p>"
            f"{marker}<ul class='groups'>{groups or '<li class=empty>No resolved L1 group</li>'}</ul>"
            f"<ul class='processes'>{processes or '<li class=empty>No L2 process asserts this L0 context</li>'}</ul>"
            f"<p class='counts'>L0 {coordinate['counts']['L0']} · L1 {coordinate['counts']['L1']} · "
            f"L2 {coordinate['counts']['L2']} · L3 {coordinate['counts']['L3']} · L4 {coordinate['counts']['L4']}</p>"
            f"</article>"
        )
    severity_text = ", ".join(f"{_esc(k)}: {v}" for k, v in sorted(severity.items())) or "none"
    finding_text = ", ".join(f"{_esc(k)}: {v}" for k, v in sorted(code_counts.items())) or "none"
    diag = (
        f"<aside class='diagnostic'><b>Diagnostic model · not release-ready</b> · "
        f"{issue_count} finding(s) ({severity_text})<br><span>Findings by code: {finding_text}. "
        "L2 entries are placed by their own context assertion. L1 composition claims are shown separately; "
        "see the embedded offline catalogue for each unresolved relationship.</span></aside>"
    ) if issue_count else "<aside class='ready'>No publication-model findings.</aside>"
    style = """
@page { size: A1 landscape; margin: 8mm; }
* { box-sizing:border-box; }
body { margin:0; color:#17212b; font:8.5pt/1.15 Arial,Helvetica,sans-serif; }
header { border-bottom:1.2mm solid #17486b; padding:0 0 3mm; margin-bottom:2mm; }
h1 { margin:0; color:#17486b; font-size:22pt; }
.meta { margin-top:1.2mm; color:#43515d; font-size:7pt; }
.legend { margin-top:1.2mm; font-size:7pt; }
.diagnostic,.ready { margin:1.5mm 0; padding:1.5mm 2mm; border:0.4mm solid #9b2c2c; background:#fff3f0; color:#672121; font-size:7pt; }
.ready { border-color:#28734b; background:#effaf2; color:#1e5c3a; }
.grid { display:grid; grid-template-columns:25mm repeat(7,minmax(0,1fr)); gap:1mm; }
.corner { }
.colhead,.rowhead { display:flex; align-items:center; justify-content:center; color:#17486b; font-weight:bold; font-size:8pt; text-align:center; padding:1mm; }
.rowhead { justify-content:flex-start; font-size:8pt; }
.cell { min-height:65mm; border:.4mm solid #557185; border-radius:1mm; padding:1.1mm; overflow:hidden; }
.cell.flagged { border-color:#ad4940; background:#fffafa; }
h3 { font-size:7.4pt; margin:0; padding:1mm; color:#fff; background:#17486b; }
.flag { display:inline-block; color:#fff; background:#a22b22; border-radius:50%; width:4mm; text-align:center; }
.axis { margin:.7mm 0 1mm; color:#43515d; font-size:6pt; }
ul { list-style:none; padding:0; margin:.5mm 0; }
li { margin:.45mm 0; overflow-wrap:anywhere; }
li b { display:inline-block; font-size:5.8pt; color:#17486b; }
.groups { padding-bottom:.6mm; border-bottom:.25mm solid #d5dde3; font-weight:bold; }
.processes { font-size:7.2pt; }
.counts { border-top:.25mm solid #d5dde3; padding-top:.6mm; margin:.7mm 0 0; color:#43515d; font-size:5.5pt; }
.empty { color:#777; font-style:italic; font-size:6pt; }
footer { border-top:.3mm solid #bdc8d0; margin-top:1.5mm; padding-top:1mm; color:#43515d; font-size:6pt; }
"""
    grid = ["<div class='corner'></div>"]
    for coordinate in model["coordinates"][:7]:
        grid.append(f"<div class='colhead'>{_esc(coordinate['stage'])}</div>")
    for index, domain in enumerate(dict.fromkeys(c["domain"] for c in model["coordinates"])):
        grid.append(f"<div class='rowhead'>{_esc(_axis_label(domain))}</div>")
        for coordinate in model["coordinates"][index * 7:(index + 1) * 7]:
            grid.append(cells_by_coordinate[(coordinate["domain"], coordinate["stage"])])
    axis = " · ".join(f"{level} {totals.get(level, 0)}" for level in ("L0", "L1", "L2", "L3", "L4"))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>OpenDEA Process Catalogue Poster · L0-L2</title><style>{style}</style></head><body>
<header><h1>OpenDEA Business Process Catalogue · ECF L0-L2 Map</h1>
<p class="meta">{_esc(REPO)} · catalogue {_esc(model['catalogue']['version'])} · source {_esc(provenance['canonical_entity_snapshot_commit'])} · ECF {_esc(provenance['ecf_contract']['tag'])} · model {_esc(model['model_digest'])}</p>
<p class="legend">A1 landscape · Levels shown: L0 Process Context, L1 Process Group and every L2 Business Process · Inventory: {_esc(axis)} · exclamation mark indicates an affected cell</p></header>
{diag}<main class="grid">{''.join(grid)}</main>
<footer>Provenance build commit: {_esc(provenance.get('build_commit') or 'not supplied')}. Population and names are read from the canonical publication model. L1 composition assertions and L2 context assertions remain distinct; the diagnostic banner summarizes unresolved findings. No wall-clock generation time is included.</footer>
</body></html>"""


def _script_json(model: dict[str, Any]) -> str:
    # Escape script delimiters, then use deterministic gzip to keep the offline
    # edition compact without relying on a remote compression or runtime asset.
    encoded = json.dumps(model, ensure_ascii=False, separators=(",", ":")) \
        .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026").encode("utf-8")
    return base64.b64encode(gzip.compress(encoded, mtime=0)).decode("ascii")


def render_catalogue_html(model: dict[str, Any]) -> str:
    """Build a self-contained HTML browser with no remote assets."""
    validate_model(model)
    data = _script_json(model)
    style = r"""
:root{color-scheme:light;--ink:#17212b;--muted:#586875;--line:#cad4dc;--blue:#17486b;--wash:#f3f7fa;--red:#8f2525}
*{box-sizing:border-box}body{margin:0;color:var(--ink);font:15px/1.45 system-ui,-apple-system,"Segoe UI",Arial,sans-serif}header{padding:1.25rem 2rem;background:var(--blue);color:#fff}h1{margin:0;font-size:1.7rem}header p{margin:.35rem 0 0;color:#e2edf4}.warning{padding:.8rem 2rem;background:#fff0ed;border-bottom:1px solid #d8aaa4;color:#632323}.controls{display:grid;grid-template-columns:minmax(15rem,2fr) repeat(5,minmax(10rem,1fr));gap:.65rem;padding:1rem 2rem;background:var(--wash);border-bottom:1px solid var(--line)}label{display:grid;gap:.25rem;font-size:.8rem;font-weight:650;color:var(--muted)}input,select,button{font:inherit;padding:.5rem;border:1px solid #98aab7;border-radius:.3rem;background:white;color:var(--ink)}main{display:grid;grid-template-columns:minmax(18rem,1.1fr) minmax(30rem,2fr);gap:1rem;padding:1rem 2rem}.matrix-wrap,.results-wrap,.detail{border:1px solid var(--line);border-radius:.4rem;padding:.8rem;min-width:0}.matrix{display:grid;grid-template-columns:9rem repeat(7,minmax(5rem,1fr));gap:.25rem;overflow:auto}.matrix .axis{font-weight:bold;color:var(--blue);font-size:.75rem}.matrix button{min-height:4rem;text-align:left;font-size:.72rem;padding:.35rem}.matrix button:hover,.matrix button:focus{outline:3px solid #81b5d5}.results{max-height:40rem;overflow:auto}.entity{display:block;width:100%;margin:.25rem 0;text-align:left;font-size:.85rem}.entity small{display:block;color:var(--muted)}.detail{margin-top:1rem}.field{padding:.65rem 0;border-bottom:1px solid #e2e7eb}.field h3{margin:0 0 .3rem;font-size:.95rem;color:var(--blue)}.field p,.field pre{margin:.2rem 0;white-space:pre-wrap;overflow-wrap:anywhere}.field pre{font: .77rem/1.4 ui-monospace,SFMono-Regular,monospace;background:var(--wash);padding:.5rem;max-height:20rem;overflow:auto}.links{display:flex;flex-wrap:wrap;gap:.35rem}.links button{font-size:.75rem}.finding{padding:.55rem;border-left:3px solid var(--red);background:#fff7f5;margin:.4rem 0}.muted{color:var(--muted)}footer{padding:1rem 2rem;color:var(--muted);border-top:1px solid var(--line)}@media(max-width:1100px){.controls{grid-template-columns:repeat(2,minmax(0,1fr))}main{grid-template-columns:1fr;padding:1rem}.matrix-wrap{overflow:auto}}@media print{header{background:white;color:var(--ink);border-bottom:2px solid var(--blue)}header p{color:var(--muted)}.controls,.results-wrap{display:none}main{display:block;padding:.4rem}.matrix{overflow:visible;grid-template-columns:7rem repeat(7,1fr)}.matrix button{min-height:2.5rem;font-size:6pt}.detail{break-before:page}footer{font-size:8pt}}
"""
    script = r"""
(async()=>{
if(!('DecompressionStream' in window)){document.getElementById('warning').hidden=false;document.getElementById('warning').textContent='This browser cannot open the compressed offline catalogue. Use a recent browser with gzip DecompressionStream support.';return}
const packed=Uint8Array.from(atob(document.getElementById('publication-model').textContent.trim()),c=>c.charCodeAt(0));
const stream=new Blob([packed]).stream().pipeThrough(new DecompressionStream('gzip'));
const M=JSON.parse(await new Response(stream).text()), E=new Map(M.entities.map(x=>[x.id,x]));
const rel=M.relationships||[], findings=M.findings||[], byId=id=>E.get(id), $=id=>document.getElementById(id);
const fields=[['Formal definition','definition'],['Plain-language description','plain_language_description'],['Description','description'],['Business purpose','business_purpose'],['Practical context','practical_context'],['Worked example','worked_example'],['Trigger','trigger'],['Outcome','outcome'],['Scope','scope'],['Inputs','inputs'],['Outputs','outputs'],['Responsibility','responsibility'],['Accountability','accountability'],['Owner','owner'],['Actors','actors'],['Stakeholders','stakeholders'],['Business rules','business_rules'],['Controls','controls'],['Exceptions','exceptions'],['Measures','metrics'],['Evidence','evidence']];
function pretty(v){return typeof v==='string'?v:JSON.stringify(v,null,2)}
function textField(title,v){if(v===undefined||v===null)return '';return `<section class="field"><h3>${esc(title)}</h3><pre>${esc(pretty(v))}</pre></section>`}
function sourceField(title,r,key){if(!Object.prototype.hasOwnProperty.call(r,key))return `<section class="field"><h3>${esc(title)}</h3><p class="muted">Not declared in the source record.</p></section>`;const v=r[key];if(v===null||v===''||(Array.isArray(v)&&v.length===0)||(typeof v==='object'&&!Array.isArray(v)&&Object.keys(v).length===0))return `<section class="field"><h3>${esc(title)}</h3><p class="muted">Declared but empty.</p></section>`;return textField(title,v)}
function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function coord(e){return e.ecf_coordinate||{domain:'',stage:''}}
function parentLinks(e){return rel.filter(r=>r.resolution==='resolved'&&((r.relationship_type==='composes'&&r.target_id===e.id)||(r.relationship_type==='in_process_context'&&r.source_id===e.id)||(['belongs_to_business_process','belongs_to_activity'].includes(r.relationship_type)&&r.source_id===e.id)))}
function childLinks(e){return rel.filter(r=>r.resolution==='resolved'&&((r.relationship_type==='composes'&&r.source_id===e.id)||(['belongs_to_business_process','belongs_to_activity','in_process_context'].includes(r.relationship_type)&&r.target_id===e.id)))}
function relatedButton(id,label){const x=byId(id);return x?`<button type="button" data-open="${esc(id)}">${esc(label||x.record.name||id)}</button>`:`<span class="muted">${esc(id)}</span>`}
function showEntity(id){const e=byId(id);if(!e)return;const r=e.record||{}, c=coord(e), unresolved=rel.filter(x=>(x.source_id===id||x.target_id===id)&&x.resolution==='unresolved'), localFindings=findings.filter(x=>x.source_id===id||x.target_id===id);
let out=`<h2>${esc(r.name||id)}</h2><p class="muted">${esc(id)} · ${esc(e.level)} · ${esc(c.domain||'No resolved domain')} / ${esc(c.stage||'No resolved stage')} · lifecycle ${esc(e.lifecycle_state||'unregistered')}</p>`;
out+=`<section class="field"><h3>Canonical navigation</h3><div class="links">${parentLinks(e).map(x=>{const id=x.relationship_type==='composes'?x.source_id:x.target_id;return relatedButton(id,byId(id)?.record?.name||id)}).join('')||'<span class="muted">No resolved parent assertion</span>'}</div></section>`;
out+=`<section class="field"><h3>Resolved children</h3><div class="links">${childLinks(e).map(x=>{const id=x.relationship_type==='composes'?x.target_id:x.source_id;return relatedButton(id,byId(id)?.record?.name||id)}).join('')||'<span class="muted">No resolved child assertions</span>'}</div></section>`;
for(const [label,key] of fields)out+=sourceField(label,r,key);
out+=`<section class="field"><h3>All canonical source fields</h3><pre>${esc(JSON.stringify(r,null,2))}</pre></section>`;
out+=textField('Source path',e.source_path)+textField('Field provenance',e.field_provenance)+textField('Governance and lifecycle',e.governance);
if(unresolved.length||localFindings.length)out+=`<section class="field"><h3>Unresolved model diagnostics</h3>${localFindings.map(f=>`<div class="finding"><b>${esc(f.code)}</b> · ${esc(f.message)}<br><span class="muted">target ${esc(f.target_id||'—')}</span></div>`).join('')||'<p>No related findings.</p>'}</section>`;
$('detail').innerHTML=out; $('detail').focus();}
function searchText(e){return JSON.stringify(e).toLowerCase()}
function filtered(){const q=$('q').value.trim().toLowerCase(),domain=$('domain').value,stage=$('stage').value,level=$('level').value,intent=$('intent').value,state=$('state').value,classification=$('classification').value,specialization=$('specialization').value;
return M.entities.filter(e=>{const c=coord(e),r=e.record||{},sp=Array.isArray(r.process_specialization)?r.process_specialization:[];return(!q||searchText(e).includes(q))&&(!domain||c.domain===domain)&&(!stage||c.stage===stage)&&(!level||e.level===level)&&(!intent||r.process_intent===intent)&&(!state||e.lifecycle_state===state)&&(!classification||r.process_classification?.type===classification)&&(!specialization||sp.some(x=>(typeof x==='string'?x:x?.type)===specialization))})}
function fillSelect(id,vals,label){const s=$(id);s.innerHTML=`<option value="">All ${label}</option>`+vals.map(x=>`<option>${esc(x)}</option>`).join('')}
let resultLimit=300;
function render(){const entities=filtered();$('summary').textContent=`${entities.length.toLocaleString()} of ${M.entities.length.toLocaleString()} entities · ${M.findings.length} model findings`;
$('results').innerHTML=entities.slice(0,resultLimit).map(e=>`<button class="entity" type="button" data-open="${esc(e.id)}">${esc(e.record.name||e.id)}<small>${esc(e.level)} · ${esc(e.id)} · ${esc(coord(e).domain)} / ${esc(coord(e).stage)}</small></button>`).join('')+(entities.length>resultLimit?'<button id="more" type="button">Show more results</button>':'');
document.querySelectorAll('#results [data-open]').forEach(b=>b.addEventListener('click',()=>showEntity(b.dataset.open)));if($('more'))$('more').addEventListener('click',()=>{resultLimit+=300;render()})}
function matrix(){const grid=$('matrix'),cells=M.coordinates;grid.innerHTML='<span></span>'+cells.slice(0,7).map(c=>`<span class="axis">${esc(c.stage)}</span>`).join('');
for(let i=0;i<7;i++){const row=cells.slice(i*7,(i+1)*7),name=row[0].domain;grid.insertAdjacentHTML('beforeend',`<span class="axis">${esc(name.replace(/And/g,' & '))}</span>`);for(const c of row){const pc=c.process_context_ids.length,grp=c.process_group_ids.length,bp=c.business_process_ids.length;const affected=findings.filter(f=>[...c.process_context_ids,...c.process_group_ids,...c.business_process_ids].includes(f.source_id)||[...c.process_context_ids,...c.process_group_ids,...c.business_process_ids].includes(f.target_id)).length;
grid.insertAdjacentHTML('beforeend',`<button type="button" data-cell="${esc(c.identifier)}"><b>${pc} L0 · ${grp} L1 · ${bp} L2</b><br>${affected?`⚠ ${affected} finding(s)`:esc(c.label)}</button>`)}}
grid.querySelectorAll('[data-cell]').forEach(b=>b.addEventListener('click',()=>{$('domain').value=cells.find(c=>c.identifier===b.dataset.cell).domain;$('stage').value=cells.find(c=>c.identifier===b.dataset.cell).stage;render();$('results').scrollIntoView({block:'nearest'})}))}
const dom=[...new Set(M.coordinates.map(c=>c.domain))],stg=[...new Set(M.coordinates.map(c=>c.stage))],levels=[...new Set(M.entities.map(e=>e.level))].sort(),intents=[...new Set(M.entities.map(e=>e.record.process_intent).filter(Boolean))].sort(),states=[...new Set(M.entities.map(e=>e.lifecycle_state).filter(Boolean))].sort(),classifications=[...new Set(M.entities.map(e=>e.record.process_classification?.type).filter(Boolean))].sort(),specializations=[...new Set(M.entities.flatMap(e=>(Array.isArray(e.record.process_specialization)?e.record.process_specialization:[]).map(x=>typeof x==='string'?x:x?.type).filter(Boolean)))].sort();
fillSelect('domain',dom,'domains');fillSelect('stage',stg,'stages');fillSelect('level',levels,'levels');fillSelect('intent',intents,'intents');fillSelect('state',states,'lifecycle states');fillSelect('classification',classifications,'classifications');fillSelect('specialization',specializations,'specializations');
for(const id of ['q','domain','stage','level','intent','state','classification','specialization'])$(id).addEventListener('input',()=>{resultLimit=300;render()});for(const id of ['domain','stage','level','intent','state','classification','specialization'])$(id).addEventListener('change',()=>{resultLimit=300;render()});
const coverageKeys=['definition','plain_language_description','description','business_purpose','practical_context','worked_example','inputs','outputs'];
$('coverage').innerHTML=coverageKeys.map(k=>{let declared=0,empty=0,absent=0;for(const e of M.entities){const r=e.record||{};if(!Object.prototype.hasOwnProperty.call(r,k))absent++;else if(r[k]===null||r[k]===''||(Array.isArray(r[k])&&r[k].length===0)||(typeof r[k]==='object'&&!Array.isArray(r[k])&&Object.keys(r[k]).length===0))empty++;else declared++}return `<li><b>${esc(k)}</b>: ${declared} populated · ${empty} declared empty · ${absent} not declared</li>`}).join('');
matrix();render();if(M.findings.length){$('warning').hidden=false;$('warning').textContent=`Diagnostic model · not release-ready. ${M.findings.length} unresolved finding(s): `+Object.entries(M.findings.reduce((a,f)=>(a[f.code]=(a[f.code]||0)+1,a),{})).map(([k,v])=>`${k} (${v})`).join(', ')+'. Findings remain visible in entity details.'}
})();
"""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OpenDEA Offline Process Catalogue</title><style>{style}</style></head><body>
<header><h1>OpenDEA Business Process Catalogue</h1><p>Offline edition · {_esc(model['catalogue']['version'])} · source {_esc(model['provenance']['canonical_entity_snapshot_commit'])} · model {_esc(model['model_digest'])}</p></header>
<div id="warning" class="warning" role="alert" hidden></div>
<section class="controls" aria-label="Catalogue filters"><label>Search name, ID and canonical fields<input id="q" type="search" autocomplete="off"></label><label>ECF domain<select id="domain"></select></label><label>Lifecycle stage<select id="stage"></select></label><label>Level<select id="level"></select></label><label>Intent<select id="intent"></select></label><label>Specialization<select id="specialization"></select></label><label>Classification<select id="classification"></select></label><label>Lifecycle state<select id="state"></select></label></section>
<main><section class="matrix-wrap"><h2>ECF matrix</h2><p class="muted">Select a cell to filter. L2 context placement and L1 composition assertions remain distinct.</p><div id="matrix" class="matrix" aria-label="ECF domain and lifecycle matrix"></div><section class="detail"><h2>Field coverage</h2><p class="muted">Counts distinguish populated source fields, fields declared empty, and fields not declared.</p><ul id="coverage"></ul></section><section class="detail"><h2>Model findings</h2>{''.join(f'<div class="finding"><b>{_esc(f.get("severity", "unspecified"))} · {_esc(f.get("code"))}</b> · {_esc(f.get("message"))}<br><span class="muted">source {_esc(f.get("source_id") or "—")} · target {_esc(f.get("target_id") or "—")} · {_esc(f.get("source_path") or "")}</span></div>' for f in model.get('findings', [])) or '<p>No findings.</p>'}</section></section>
<section class="results-wrap"><h2>Entities</h2><p id="summary" class="muted" aria-live="polite"></p><div id="results" class="results"></div><section id="detail" class="detail" tabindex="-1" aria-live="polite"><h2>Entity details</h2><p>Select a result to inspect source fields, hierarchy, inputs, outputs and provenance.</p></section></section></main>
<footer>All data, scripts and styles are embedded in this file. It does not request network resources. Entity content and relationships are rendered from the validated publication model; absent source fields remain absent.</footer>
<script type="application/octet-stream" id="publication-model">{data}</script><script>{script}</script></body></html>"""


def render_assets(model: dict[str, Any], output_dir: Path, *, poster_pdf: bool = False,
                  poster_png: bool = False) -> dict[str, Path]:
    """Write offline HTML, poster HTML, and optionally PDF plus its PNG raster."""
    validate_model(model)
    output_dir.mkdir(parents=True, exist_ok=True)
    html_path = output_dir / "process-catalogue.html"
    poster_path = output_dir / "process-catalogue-poster.html"
    html_path.write_text(render_catalogue_html(model), encoding="utf-8", newline="\n")
    poster_path.write_text(render_poster_html(model), encoding="utf-8", newline="\n")
    outputs = {"html": html_path, "poster_html": poster_path}
    if poster_pdf or poster_png:
        try:
            from weasyprint import HTML as WeasyHTML
        except ImportError as exc:
            raise RuntimeError("PDF/PNG output requires WeasyPrint") from exc
        pdf_path = output_dir / "process-catalogue-poster.pdf"
        document = WeasyHTML(string=poster_path.read_text(encoding="utf-8"),
                             base_url=str(output_dir)).render()
        if len(document.pages) != 1:
            raise RuntimeError(f"A1 poster PDF must contain exactly one page (got {len(document.pages)})")
        identifier = bytes.fromhex(model["model_digest"].removeprefix("sha256:"))
        document.write_pdf(str(pdf_path), pdf_identifier=identifier)
        outputs["poster_pdf"] = pdf_path
        if poster_png:
            png_path = output_dir / "process-catalogue-poster.png"
            subprocess.run(["pdftoppm", "-f", "1", "-singlefile", "-png", "-r", "110",
                            str(pdf_path), str(png_path.with_suffix(""))], check=True,
                           capture_output=True, text=True)
            if not png_path.is_file():
                raise RuntimeError("PNG rasterization did not create the expected file")
            outputs["poster_png"] = png_path
    return outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL,
                        help="validated publication-model JSON (default: out/process-catalogue.json)")
    parser.add_argument("--schema", type=Path, default=SCHEMA)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "out")
    parser.add_argument("--pdf", action="store_true", help="also create and validate the one-page A1 PDF")
    parser.add_argument("--png", action="store_true", help="rasterize the same PDF as a PNG")
    parser.add_argument("--allow-findings", action="store_true",
                        help="render a diagnostic model with visible unresolved findings")
    args = parser.parse_args(argv)
    try:
        model = load_model(args.model, args.schema)
        if any(item.get("severity") == "error" for item in model["findings"]) and not args.allow_findings:
            raise ValueError("model has error-level findings; pass --allow-findings to render a clearly marked diagnostic edition")
        outputs = render_assets(model, args.output_dir, poster_pdf=args.pdf, poster_png=args.png)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    for kind, path in outputs.items():
        print(f"{kind}: {path} ({path.stat().st_size:,} bytes)")
    print(f"model: {model['model_digest']} · findings={len(model['findings'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
