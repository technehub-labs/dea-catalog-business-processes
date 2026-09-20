#!/usr/bin/env python3
"""
cross_check_org_wide.py
CR-BP-mv1: org-wide cross-check stage for structural-change CRs.

Audits every change-request (CR) and architecture-decision record (ADR)
artifact for coherence with the org-wide id system + repo-name state:

  XC-A  no legacy path forms (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
        outside clearly historical framing
  XC-B  no legacy repo names (`dea-catalog-processes`,
        `dea-catalog-digital-business-service-factory`) outside historical
        framing
  XC-C  every record id referenced in a CR/ADR resolves against the canonical
        id map (current catalog) or the migration id map (old->new)

Scopes:
  - this repo: change-requests/*.md (open + closed; historical artifacts are
    in scope per the structural-change directive: audit historical artifacts,
    not just live + future)
  - sibling repos: docs/adrs/*.md in each checked-out sibling clone found
    under the DEA work root (default: ../dea-work)

Output: reconciliation/cross-check-org-wide.md (report) + stdout summary.

Usage:
  python scripts/cross_check_org_wide.py [--json] [--work-root PATH]

Exit codes:
  0  all artifacts CLEAN or HISTORICAL-ONLY
  1  at least one artifact NEEDS-FRAMING or has UNRESOLVED references
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WORK_ROOT = ROOT.parent / "dea-work"

LEGACY_PATH_PATTERNS = (
    "entities/v1-alpha/dea:",
    "contexts/v1-alpha/",
)
LEGACY_REPO_NAMES = (
    "dea-catalog-processes",
    "dea-catalog-digital-business-service-factory",
)
HISTORICAL_MARKERS = ("pre-migration", "historical", "formerly", "legacy",
                      "superseded", "pre-rename", "pre-mv1", "old form",
                      "old id", "old name", "renamed")

LEGACY_ID_RE = re.compile(r"\bdea:(pc|group|process|activity|task)-[a-z0-9][a-z0-9-]*")
NEW_ID_RE = re.compile(r"\bprocesses:(pc|group|process|activity|task)-[a-z0-9][a-z0-9-]*")


def _load_id_map() -> dict[str, str]:
    p = ROOT / "reconciliation" / "migration-id-map.yaml"
    if not p.exists():
        return {}
    data = yaml.safe_load(p.read_text()) or {}
    return data.get("id_map", {}) or {}


def _current_ids() -> set[str]:
    ids: set[str] = set()
    ent = ROOT / "entities" / "v1-alpha"
    if ent.exists():
        for f in ent.rglob("processes-*.yaml"):
            try:
                rec = yaml.safe_load(f.read_text())
            except yaml.YAMLError:
                continue
            if isinstance(rec, dict) and isinstance(rec.get("id"), str):
                ids.add(rec["id"])
    return ids


def _scan_markdown(path: Path, current_ids: set[str],
                   id_map: dict[str, str]) -> dict:
    """Scan one CR/ADR markdown. Returns per-file audit record."""
    text = path.read_text()
    # A file-level CR-BP-mv1 layout-note banner is an explicit historical
    # framing declaration for the whole artifact: legacy forms it cites are
    # acknowledged historical references, not unflagged drift.
    has_banner = "Layout note (CR-BP-mv1" in text
    findings: list[dict] = []
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        low = line.lower()
        for pat in LEGACY_PATH_PATTERNS:
            if pat in line and not any(m in low for m in HISTORICAL_MARKERS):
                findings.append({"rule": "XC-A", "line": lineno,
                                 "detail": f"legacy path form {pat!r}",
                                 "info": has_banner})
        for name in LEGACY_REPO_NAMES:
            if name in line and not any(m in low for m in HISTORICAL_MARKERS):
                findings.append({"rule": "XC-B", "line": lineno,
                                 "detail": f"legacy repo name {name!r}",
                                 "info": has_banner})
    # id resolution: legacy ids must exist in the migration id map (or be a
    # documented known residual); new ids must resolve against the current
    # catalog. Ids ending with '-' are line-wrap fragments of longer ids in
    # prose, not real references.
    residuals: set[str] = set()
    for r in (yaml.safe_load(
        (ROOT / "reconciliation" / "migration-id-map.yaml").read_text()
    ) or {}).get("known_residuals", []) or []:
        v = r.get("legacy_value")
        if not v:
            continue
        residuals.add(v)
        m = LEGACY_ID_RE.search(v)
        if m:
            residuals.add(m.group(0))
    unresolved_legacy = sorted({
        m.group(0) for m in LEGACY_ID_RE.finditer(text)
        if m.group(0) not in id_map
        and m.group(0) not in residuals
        and not m.group(0).endswith("-")
    })
    unresolved_new = sorted({
        m.group(0) for m in NEW_ID_RE.finditer(text)
        if m.group(0) not in current_ids
    })
    for rid in unresolved_legacy:
        findings.append({"rule": "XC-C", "line": None,
                         "detail": f"legacy id {rid!r} not in migration id map",
                         "info": has_banner})
    for rid in unresolved_new:
        findings.append({"rule": "XC-C", "line": None,
                         "detail": f"new id {rid!r} not in current catalog"})

    blocking = [f for f in findings
                if f["rule"] in ("XC-A", "XC-B") and not f.get("info")]
    unres = [f for f in findings if f["rule"] == "XC-C" and not f.get("info")]
    if blocking or unres:
        status = "NEEDS-FRAMING" if blocking else "UNRESOLVED-REFS"
    elif findings:
        status = "HISTORICAL-ONLY"
    else:
        status = "CLEAN"
    return {"file": str(path), "status": status, "findings": findings}


def _iter_artifacts(work_root: Path) -> list[tuple[str, Path]]:
    artifacts: list[tuple[str, Path]] = []
    cr_dir = ROOT / "change-requests"
    if cr_dir.exists():
        for f in sorted(cr_dir.glob("CR-*.md")):
            artifacts.append((f"CR ({ROOT.name})", f))
    if work_root.exists():
        for repo in sorted(work_root.iterdir()):
            for dirname in ("adr", "adrs", "ADRs"):
                adr_dir = repo / "docs" / dirname
                if adr_dir.is_dir():
                    for f in sorted(adr_dir.glob("*.md")):
                        artifacts.append((f"ADR ({repo.name})", f))
    return artifacts


def _write_report(out: Path, results: list[dict]) -> None:
    lines = [
        "# Org-Wide Cross-Check Report (CR-BP-mv1)",
        "",
        "Scope: every CR in this repo (open + closed) and every ADR in",
        "sibling clones under the DEA work root. Historical artifacts are in",
        "scope per the structural-change cross-check directive.",
        "",
        "| Artifact | Status | Findings |",
        "|---|---|---|",
    ]
    for r in results:
        label = f"{r['kind']}: {Path(r['file']).name}"
        lines.append(f"| {label} | {r['status']} | {len(r['findings'])} |")
    lines += ["", "## Detail", ""]
    for r in results:
        if not r["findings"]:
            continue
        lines.append(f"### {r['kind']}: {Path(r['file']).name}")
        for f in r["findings"]:
            loc = f"line {f['line']}" if f["line"] else "file-wide"
            lines.append(f"- [{f['rule']}] {loc}: {f['detail']}")
        lines.append("")
    out.write_text("\n".join(lines) + "\n")


def main() -> int:
    p = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[1])
    p.add_argument("--json", action="store_true")
    p.add_argument("--work-root", default=str(DEFAULT_WORK_ROOT))
    p.add_argument("--out", default=str(ROOT / "reconciliation" / "cross-check-org-wide.md"))
    args = p.parse_args()

    id_map = _load_id_map()
    current = _current_ids()
    artifacts = _iter_artifacts(Path(args.work_root))

    results = []
    for kind, f in artifacts:
        r = _scan_markdown(f, current, id_map)
        r["kind"] = kind
        results.append(r)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    _write_report(out, results)

    bad = [r for r in results if r["status"] in ("NEEDS-FRAMING", "UNRESOLVED-REFS")]
    if args.json:
        print(json.dumps({
            "artifacts": len(results),
            "clean": sum(1 for r in results if r["status"] == "CLEAN"),
            "historical_only": sum(1 for r in results if r["status"] == "HISTORICAL-ONLY"),
            "needs_framing": sum(1 for r in results if r["status"] == "NEEDS-FRAMING"),
            "unresolved_refs": sum(1 for r in results if r["status"] == "UNRESOLVED-REFS"),
            "report": str(out),
            "bad_files": [r["file"] for r in bad],
        }, indent=2))
    else:
        print(f"Org-wide cross-check: {len(results)} artifacts")
        for status in ("CLEAN", "HISTORICAL-ONLY", "NEEDS-FRAMING", "UNRESOLVED-REFS"):
            n = sum(1 for r in results if r["status"] == status)
            print(f"  {status}: {n}")
        print(f"  Report: {out}")
        for r in bad[:15]:
            print(f"    ! {r['kind']}: {Path(r['file']).name} ({r['status']})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
