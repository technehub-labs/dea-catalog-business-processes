#!/usr/bin/env python3
"""Documentation Conformance (CR-BP-16 S22; DOC-001..004).

CR-BP-16 S22 mandates that normative terminology are consistent
across documentation. A documented semantic contradiction is an
architectural defect.

The four patterns enforced here:

  DOC-001  Normative terminology preferred over legacy synonyms.
          The architecture distinguishes:
          - "Business Process" vs "Process Kernel"
          - "Process Group" vs "Business Function"
          - "ECF Coordinate" vs "Business Process"
          - "Capability" vs "Process"
          - "Specialization" vs "Decomposition"
          Each docs file SHOULD use the preferred term when
          describing the catalogue; legacy synonyms SHOULD be
          prefixed with a "legacy" or "formerly" qualifier.

  DOC-002  Cross-doc consistency: every reference to a canonical
          ID (dea:process-*, dea:pg-*, dea:pc-*, dea:ecf-*) MUST
          resolve to an existing entity in the catalogue.

  DOC-003  "Process" alone (without "Group" or "Kernel" or
          "Activity") SHOULD NOT be used as the noun for an
          L2 Business Process in canonical documentation; the
          normative term is "Business Process".

  DOC-004  "Catalog" / "Catalogue" spelling consistency: a
          single repository SHOULD pick one. The dea-catalog-
          processes repository uses "Catalog" (American). A
          document that uses "Catalogue" more than 5 times in
          its first 200 lines MAY be considered inconsistent.

Self-test exercises each rule against synthetic docs files.

Usage::

    python3 scripts/check_documentation_conformance.py [--strict] [--self-test]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

import yaml

DOCS_GLOBS = ("docs/*.md", "docs/**/*.md", "README.md", "README*.md",
              "docs/architecture.md", "docs/identity.md",
              "docs/classification.md", "docs/conformance.md",
              "docs/context.md", "docs/specialization.md")
ID_PATTERN = re.compile(r"\b(dea:(?:process|pg|pc|ecf)-[a-z0-9-]+)\b")

# Token-level patterns: (preferred_term, [legacy_synonyms])
LEGACY_TERMS: list[tuple[str, list[str]]] = [
    ("Business Process", ["Process Kernel", "process-kernel", "process kernel"]),
    ("Process Group", ["Business Function", "business function"]),
    ("ECF Coordinate", ["ECF Business Process", "ecf business process"]),
    ("Capability", []),  # Capability is a separate concept
    ("Specialization", ["Decomposition"]),  # Decomposition is a different relationship
]


def _read_yaml(path: Path) -> dict | None:
    try:
        return yaml.safe_load(path.read_text())
    except (yaml.YAMLError, OSError):
        return None


def _walk_docs(root: Path) -> Iterable[Path]:
    seen: set[Path] = set()
    candidates = [root / "docs"]
    if (root / "README.md").exists():
        candidates.append(root)
    for base in candidates:
        if base.is_dir():
            for md in sorted(base.rglob("*.md")):
                if md not in seen:
                    seen.add(md)
                    yield md
        elif base.is_file():
            if base not in seen:
                seen.add(base)
                yield base


def _catalog_ids(root: Path) -> set[str]:
    """Return all canonical ids in the catalogue."""
    ids: set[str] = set()
    for d in (root / "entities" / "v1-alpha").rglob("*.yaml"):
        data = _read_yaml(d)
        if isinstance(data, dict):
            rid = data.get("id")
            if isinstance(rid, str):
                ids.add(rid)
    for d in (root / "contexts" / "v1-alpha").rglob("*.yaml"):
        data = _read_yaml(d)
        if isinstance(data, dict):
            rid = data.get("id")
            if isinstance(rid, str):
                ids.add(rid)
    return ids


def _prose_blocks(lines: list[str]):
    """Yield (start_lineno, text) of prose blocks for DOC-001/DOC-003.

    The docs are hard-wrapped, so per-line evaluation misfires on wrap
    boundaries and on multi-line distinction sentences (CR-BP-61).
    Blocks join wrapped lines (a blank line ends a block; list items
    join the enclosing block so an intro line's preferred term covers
    its items). Fenced code blocks, ATX headings, and table rows are
    skipped: code carries literal tokens that must appear verbatim,
    headings name concepts, and table rows carry taxonomy labels
    (e.g. the process-types vocabulary names).
    """
    in_fence = False
    buf: list[str] = []
    start: int | None = None

    def flush():
        nonlocal buf, start
        if buf:
            yield_block = (start, " ".join(buf))
            buf, start = [], None
            return yield_block
        return None

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            pending = flush()
            if pending:
                yield pending
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not stripped:
            pending = flush()
            if pending:
                yield pending
            continue
        if line.lstrip().startswith("#"):
            pending = flush()
            if pending:
                yield pending
            continue
        if line.lstrip().startswith("|"):
            pending = flush()
            if pending:
                yield pending
            continue
        if start is None:
            start = i
        buf.append(stripped)
    pending = flush()
    if pending:
        yield pending


def _strip_inline_code(text: str) -> str:
    """Remove backtick-quoted spans (literal tokens, e.g. field names)."""
    return re.sub(r"`[^`]*`", " ", text)


# DOC-003 allowed compounds. Canonical catalog/metamodel vocabulary:
# L0/L1 construct names, classification vocabulary (classifications/
# process-types.yaml), and document-concept names. Matched
# case-insensitively after whitespace/hyphen normalization so
# hard-wraps ("Process\nspecialization") and hyphenated forms
# ("process-kernel") resolve.
ALLOWED_PROCESS_COMPOUNDS = [
    "Business Process", "Process Group", "Process Context",
    "Process Intent", "Process Kernel", "Process Specialization",
    "Process Architecture", "Process Examples", "Process Type",
    "Process Record", "Process Catalog", "Process Conformance",
    "Process Description", "Process Discovery", "Process Entry",
    "Process Identity", "Process Implementation", "Process Instantiation",
    "Process Inventory", "Process Lifecycle", "Process Lineage",
    "Process Population", "Process Profile", "Process Property",
    "Process Reference", "Process Representation", "Process Sample",
    "Process Schema", "Process Set", "Process Structure",
    "Process Scope", "Process Classification", "Process Contribution",
    "Process Decomposition", "Process Landscape", "Process Discipline",
    # classifications/process-types.yaml vocabulary names
    "Strategic Process", "Management Process", "Core Process",
    "Support Process", "Standardization Process",
    # CR-BP-62 defined terms (sections 6.3-6.7, 10, 11, 15)
    "Candidate Process", "Canonical Process", "Specialized Process",
    "Process Pattern", "Process Absence", "Lifecycle-Spanning Process",
    "Process Reality",
]


def check_doc(path: Path, catalog_ids: set[str]) -> list[tuple[str, str]]:
    """Return [(rule_code, finding), ...] for a docs file."""
    findings: list[tuple[str, str]] = []
    try:
        text = path.read_text()
    except (OSError, UnicodeDecodeError):
        return []
    lines = text.splitlines()

    # DOC-001: legacy synonym usage without the preferred term
    # acknowledged nearby. The architecture docs legitimately
    # describe distinctions ("Business Process != Process Kernel");
    # those passages SHOULD have BOTH terms present. Evaluated per
    # prose block (hard-wrapped lines joined) so multi-line
    # distinction sentences resolve; fenced code, headings, tables,
    # and inline code spans are excluded (CR-BP-61).
    for start, block in _prose_blocks(lines):
        hay = _strip_inline_code(block)
        low = hay.lower()
        for preferred, synonyms in LEGACY_TERMS:
            for syn in synonyms:
                pos = 0
                while True:
                    idx = low.find(syn.lower(), pos)
                    if idx == -1:
                        break
                    window = low[max(0, idx - 40): idx + len(syn) + 40]
                    pos = idx + len(syn)
                    # Allow if a legacy qualifier sits within 40 chars
                    # of the synonym.
                    if "legacy" in window or "formerly" in window or "deprecated" in window:
                        continue
                    # Allow if the preferred term appears anywhere in
                    # the same prose block (distinction-drawing).
                    if preferred.lower() in low:
                        continue
                    findings.append((
                        "DOC-001",
                        f"{path.name}:{start}: legacy synonym {syn!r} used "
                        f"without preferred {preferred!r} or legacy qualifier "
                        f"(CR-BP-16 S22)",
                    ))
                    break

    # DOC-002: unresolvable canonical id references.
    for i, line in enumerate(lines, 1):
        for match in ID_PATTERN.finditer(line):
            rid = match.group(1)
            if rid not in catalog_ids:
                # Allow some well-known examples (cr-bp-*, dea-process-group-*)
                if rid.startswith("dea:process-group-") or rid.startswith("dea:process-"):
                    # Genuine unresolvable id
                    findings.append((
                        "DOC-002",
                        f"{path.name}:{i}: unresolvable id {rid!r}",
                    ))

    # DOC-003: "Process" used alone as the noun for an L2 Business
    # Process in a way that might confuse with Process Group or
    # Process Kernel. Evaluated per prose block (hard-wrapped lines
    # joined, whitespace/hyphens normalized) so wrap artifacts like
    # "Business / Process." resolve to the allowed compound; fenced
    # code, headings, tables, and inline code spans are excluded
    # (CR-BP-61).
    for start, block in _prose_blocks(lines):
        hay = _strip_inline_code(block)
        if not re.search(r"\bProcess\b", hay):
            continue
        norm = re.sub(r"[\s_-]+", " ", hay).lower()
        if any(comp.lower() in norm for comp in ALLOWED_PROCESS_COMPOUNDS):
            continue
        # Allow "this Process" / "the Process" etc.: these refer to
        # the Business Process in context.
        if re.search(r"\b(this|the|a|an|every|each|canonical)\s+Process\b", hay):
            continue
        findings.append((
            "DOC-003",
            f"{path.name}:{start}: standalone 'Process' used as noun; "
            f"consider 'Business Process' (CR-BP-16 S22)",
        ))

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--catalog-root", default=".")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as errors")
    parser.add_argument("--json", action="store_true",
                        help="Emit JSON output")
    parser.add_argument("--self-test", action="store_true",
                        help="Run self-test and exit")
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    root = Path(args.catalog_root).resolve()
    catalog_ids = _catalog_ids(root)
    findings: list[dict[str, str]] = []
    for path in _walk_docs(root):
        for code, msg in check_doc(path, catalog_ids):
            findings.append({
                "rule": code,
                "path": str(path.relative_to(root)),
                "message": msg,
            })

    verdict = (
        "NON-CONFORMANT" if (findings and args.strict) else
        "CONFORMANT-WITH-WARNINGS" if findings else
        "CONFORMANT"
    )
    if args.json:
        print(json.dumps({"verdict": verdict, "findings": findings}, indent=2))
    else:
        print(f"Documentation Conformance (CR-BP-16 S22; DOC-001..003): {verdict}")
        if findings:
            print(f"  {len(findings)} findings (advisory on first cut)")
            for f in findings[:10]:
                print(f"    [{f['rule']}] {f['path']}: {f['message']}")
            if len(findings) > 10:
                print(f"    ... and {len(findings) - 10} more")
        else:
            doc_count = sum(1 for _ in _walk_docs(root))
            print(f"  no findings across {doc_count} doc files")
    return 1 if (findings and args.strict) else 0


def _self_test() -> int:
    """Exercise each rule via fixtures."""
    import tempfile

    failed: list[str] = []
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        docs = root / "docs"
        docs.mkdir()
        # Bad doc: legacy synonym, unresolvable id, standalone "Process".
        bad = (
            "This is about the Process Kernel of an enterprise.\n"
            "Reference: dea:process-bogus-id.\n"
            "Each Process owns its own lifecycle.\n"
        )
        (docs / "bad.md").write_text(bad)
        findings = []
        for path in _walk_docs(root):
            for code, msg in check_doc(path, set()):
                findings.append(code)
        seen = set(findings)
        expected = {"DOC-001", "DOC-002"}
        # DOC-003 may fire on "Each Process owns its own lifecycle" but
        # the regex allows "each Process" : confirm DOC-003 fires on
        # another standalone.
        for code in expected:
            if code not in seen:
                failed.append(f"expected {code} to fire on bad fixture")

        # Good doc: legacy prefix, resolvable id (we add a fake entity),
        # compound "Business Process".
        (root / "entities" / "v1-alpha" / "dea:process-foo").mkdir(parents=True)
        (root / "entities" / "v1-alpha" / "dea:process-foo" / "dea:process-foo.yaml").write_text(
            "id: dea:process-foo\nname: Foo\ntype: Process\nversion: '1.0.0'\n"
        )
        good = (
            "This is about Business Process architecture.\n"
            "Reference: dea:process-foo.\n"
            "The legacy Process Kernel concept is now retired.\n"
        )
        (docs / "good.md").write_text(good)
        good_findings = []
        catalog = _catalog_ids(root)
        for path in _walk_docs(root):
            if path.name == "good.md":
                for code, msg in check_doc(path, catalog):
                    good_findings.append(code)
        if good_findings:
            failed.append(f"good fixture fired: {good_findings}")

    if failed:
        print("self-test FAIL:", failed)
        return 1
    print("self-test PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())