#!/usr/bin/env python3
"""check_prose_authorship.py: enforce CR-BP-118c cardinal prose rule.

The 118a/118b authorship gate (``check_authorship.py``) covers the
**METADATA** fields whose values are literal identity strings
(``**Owner**: Emmanuel A. Otchere``, ``audit.author: Emmanuel A. Otchere``,
``authors[].name: ...``). The 118c prose gate covers the
**CONTENT** fields whose values are sentence-form prose
(``name``, ``definition``, ``description``, ``summary`` on entity
YAML records).

The cardinal rule (CR-BP-118) prohibits authoring-tool references
(``Coder``, ``Agent``, ``Hermes``, ``Claude``, ``GPT``, ``Cline``,
``OpenAI``, ``MiniMax``, ``MiniMax-M3``) in any published artifact.
The 118c rule extends that prohibition to prose content fields.
A single exception: the keyword ``Agent`` is allowlisted in content
fields because the dea-catalog-processes domain vocabulary uses
``Agent`` extensively as a workforce/role noun (e.g. "Agent
Operations", "Agent Acquisition and Onboarding", "AgentProfile",
"multi-agent", "agentive capability") that predates the cardinal
rule and has nothing to do with the Coder/Agent authoring tools.
See CR-BP-118c for the doctrinal rationale.

Two rules, both data-driven from
``reconciliation/prose-fields.yaml``:

- PROSE-001 (blocking): every registered content field's value
  contains zero tokens from the denylist. The allowlist is
  word-boundary exempted.

- PROSE-002 (advisory): every registered content field's value is
  non-empty when the field is present. Catches records that
  carried the field with an empty value.

Run: python3 scripts/check_prose_authorship.py [--strict] [--json]
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "reconciliation" / "prose-fields.yaml"


# --------------------------------------------------------------------------- #
# Registry loader
# --------------------------------------------------------------------------- #

def _load_registry(path: Path = REGISTRY_PATH) -> dict:
    """Parse the prose-fields YAML registry.

    Tolerant YAML loader: the registry is hand-maintained and may
    use YAML 1.2 features not in stdlib's safe_load. We use a small
    custom parser keyed on the small subset the registry uses
    (top-level ``fields:``, ``allowlist:``, ``denylist:`` blocks of
    dash-prefixed entries). This avoids a pyyaml dependency for the
    gate itself.
    """
    text = path.read_text(encoding="utf-8")
    out: dict = {"fields": [], "allowlist": [], "denylist": []}
    section = None
    for raw in text.splitlines():
        stripped = raw.lstrip()
        if not stripped or stripped.startswith("#"):
            continue
        if raw.startswith("fields:"):
            section = "fields"
            continue
        if raw.startswith("allowlist:"):
            section = "allowlist"
            continue
        if raw.startswith("denylist:"):
            section = "denylist"
            continue
        if section is None:
            continue
        if not stripped.startswith("- "):
            # sub-key of last fields entry
            if section == "fields" and ":" in raw:
                m = re.match(r"^\s+([a-z_]+):\s*(.*)$", raw)
                if m and out["fields"]:
                    val = m.group(2)
                    # Strip inline comments and quotes
                    val = val.split("#", 1)[0].rstrip()
                    val = val.strip().strip('"').strip("'")
                    out["fields"][-1][m.group(1)] = val
            continue
        # new entry
        first = stripped[2:].rstrip()
        # Strip inline comments
        first = first.split("#", 1)[0].rstrip()
        if section in ("allowlist", "denylist"):
            out[section].append(first.strip().strip('"').strip("'"))
        elif section == "fields":
            m = re.match(r"^([a-z_]+):\s*(.*)$", first)
            if m:
                key, val = m.group(1), m.group(2).strip().strip('"').strip("'")
                out["fields"].append({key: val})
            else:
                out["fields"].append({"path": first})
    return out


# --------------------------------------------------------------------------- #
# YAML value extractor
# --------------------------------------------------------------------------- #

_CONTENT_FIELD_NAMES = ("name", "definition", "description", "summary")


def _extract_field_values(path: Path, field: str) -> list[tuple[int, str]]:
    """Walk a file, return [(line_no, value)] for each <field>: occurrence.

    Handles four YAML forms:
      1. inline single-line:     ``name: Some value``
      2. inline quoted:          ``name: "Some value"``
      3. multi-line block:       ``name: |\\n  line1\\n  line2``
      4. multi-line folded:      ``name: >\\n  line1\\n  line2``

    Multi-line forms are collected until the line's indent returns to
    or below the field declaration's indent.
    """
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    out: list[tuple[int, str]] = []
    field_re = re.compile(rf"^(\s*){re.escape(field)}\s*:\s*(.*)$")
    for i, line in enumerate(lines):
        m = field_re.match(line)
        if not m:
            continue
        base_indent = len(m.group(1))
        first = m.group(2).rstrip()
        # Determine the multi-line block scalar header
        if first in ("|", ">", "|-", "|-", ">+", ">-") or first.lstrip() in (
            "|", ">", "|-", ">+", ">-"
        ):
            block_lines: list[str] = []
            j = i + 1
            block_indent = None
            while j < len(lines):
                cont = lines[j]
                if cont.strip() == "":
                    block_lines.append("")
                    j += 1
                    continue
                # Detect first content line to anchor block indent
                if block_indent is None:
                    stripped_l = cont.lstrip()
                    if not stripped_l:
                        block_lines.append("")
                        j += 1
                        continue
                    block_indent = len(cont) - len(stripped_l)
                if len(cont) - len(cont.lstrip()) > base_indent:
                    block_lines.append(cont[block_indent:].rstrip() if block_indent else cont.strip())
                    j += 1
                else:
                    break
            value = " ".join(b for b in block_lines if b).strip()
            out.append((i + 1, value))
            continue
        # Inline single-line or quoted form
        value = first.strip()
        if value.startswith('"') and value.endswith('"') and len(value) >= 2:
            value = value[1:-1]
        elif value.startswith("'") and value.endswith("'") and len(value) >= 2:
            value = value[1:-1]
        out.append((i + 1, value))
    return out


# --------------------------------------------------------------------------- #
# Evaluator
# --------------------------------------------------------------------------- #

def _matches_allowlist(token: str, value: str) -> bool:
    """True iff the token appears in value as a whole word (word-boundary)."""
    return bool(re.search(rf"(?<![A-Za-z0-9_]){re.escape(token)}(?![A-Za-z0-9_])", value))


def evaluate(repo_root: Path = REPO_ROOT, registry_path: Path = REGISTRY_PATH) -> list[dict]:
    """Run PROSE-001 + PROSE-002 across the registered content fields.

    Returns a list of finding dicts, each with:
      rule, file, line, field, value, matched (token or '(empty)').
    """
    reg = _load_registry(registry_path)
    findings: list[dict] = []
    denylist = reg.get("denylist", [])
    allowlist = reg.get("allowlist", [])
    for fdef in reg.get("fields", []):
        path_glob = fdef.get("file_glob", "")
        field = fdef.get("path", "")
        if not field or not path_glob:
            continue
        # Walk files matching the glob; bind to the literal path prefix
        # to avoid scanning vendored content (e.g. .metaframework/).
        literal_prefix = path_glob.split("*", 1)[0]
        if literal_prefix.endswith("/"):
            literal_prefix = literal_prefix[:-1]
        if literal_prefix:
            base = repo_root / literal_prefix
        else:
            base = repo_root
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if not fnmatch.fnmatch(str(path.relative_to(repo_root)), path_glob):
                continue
            for line_no, value in _extract_field_values(path, field):
                # PROSE-001: denylist. Allowlist is the word-boundary
                # exemption: if a denylist token matches as a whole word
                # AND the same token (or one of its allowlist variants)
                # is in the allowlist, the hit is suppressed.
                for token in denylist:
                    if not _matches_allowlist(token, value):
                        continue
                    # Allowlist exemption: if the value also contains the
                    # allowlisted token as a whole word, suppress the
                    # denylist hit. The denylist and allowlist are
                    # cross-checked: a token in BOTH is treated as
                    # domain-vocabulary and exempt.
                    if any(_matches_allowlist(allowed, value) for allowed in allowlist):
                        continue
                    findings.append({
                        "rule": "PROSE-001",
                        "file": str(path.relative_to(repo_root)),
                        "line": line_no,
                        "field": field,
                        "value": value[:200],
                        "matched": token,
                    })
                # PROSE-002: empty value when field is present
                if not value:
                    findings.append({
                        "rule": "PROSE-002",
                        "file": str(path.relative_to(repo_root)),
                        "line": line_no,
                        "field": field,
                        "value": "",
                        "matched": "(empty)",
                    })
    return findings


def _verdict(findings: list[dict]) -> str:
    if any(f["rule"] == "PROSE-001" for f in findings):
        return "NON-CONFORMANT"
    if findings:
        return "CONFORMANT-WITH-WARNINGS"
    return "CONFORMANT"


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--strict", action="store_true",
                        help="Exit 1 on any PROSE-001 finding (default: PROSE-001 only).")
    parser.add_argument("--json", action="store_true",
                        help="Emit findings as JSON on stdout.")
    parser.add_argument("--self-test", action="store_true",
                        help="Run the in-script self-test; ignore other flags.")
    parser.add_argument("--catalog-root", default=str(REPO_ROOT),
                        help="Repo root (default: REPO_ROOT).")
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    findings = evaluate(Path(args.catalog_root))
    verdict = _verdict(findings)
    if args.json:
        print(json.dumps({"verdict": verdict, "findings": findings}, indent=2))
    else:
        print(f"PROSE Authorship Gate: {verdict}")
        if findings:
            for f in findings:
                print(f"  [{f['rule']}] {f['file']}:{f['line']} {f['field']}: matched='{f['matched']}' value={f['value'][:80]!r}")

    if args.strict and any(f["rule"] == "PROSE-001" for f in findings):
        return 1
    return 0


def _self_test() -> int:
    """Hand-rolled fixtures; covers the 5 paths in the gate's contract."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        # Registry fixture
        reg = tmpdir / "prose-fields.yaml"
        reg.write_text(
            "fields:\n"
            "  - path: name\n"
            "    file_glob: '*.yaml'\n"
            "  - path: definition\n"
            "    file_glob: '*.yaml'\n"
            "allowlist:\n"
            "  - Agent\n"
            "denylist:\n"
            "  - Coder\n"
            "  - MiniMax\n",
            encoding="utf-8",
        )
        # Fixture 1: clean record (Agent allowed)
        f1 = tmpdir / "f1.yaml"
        f1.write_text(
            "id: foo\nname: Agent Operations\ndefinition: |\n"
            "  The cohesive grouping of work within Agent Operations that\n"
            "  identifies the demand signal.\n",
            encoding="utf-8",
        )
        # Fixture 2: Coder in name (denied)
        f2 = tmpdir / "f2.yaml"
        f2.write_text(
            "id: bar\nname: Built by Coder (eaojnr)\ndefinition: |\n  Does stuff.\n",
            encoding="utf-8",
        )
        # Fixture 3: MiniMax in definition (denied)
        f3 = tmpdir / "f3.yaml"
        f3.write_text(
            "id: baz\nname: A clean record\ndefinition: |\n  Generated by MiniMax-M3 on 2026-10-13.\n",
            encoding="utf-8",
        )
        # Fixture 4: empty value (PROSE-002)
        f4 = tmpdir / "f4.yaml"
        f4.write_text(
            "id: qux\nname: ''\ndefinition: |\n  Has a definition.\n",
            encoding="utf-8",
        )
        # Fixture 5: Agent word-boundary
        f5 = tmpdir / "f5.yaml"
        f5.write_text(
            "id: agentive\nname: agentive capability\ndefinition: A capability.\n",
            encoding="utf-8",
        )

        findings = evaluate(tmpdir, reg)
        # 2 PROSE-001 (Coder + MiniMax), 1 PROSE-002 (empty), 0 from Agent/agentive
        prose_001 = [f for f in findings if f["rule"] == "PROSE-001"]
        prose_002 = [f for f in findings if f["rule"] == "PROSE-002"]
        assert len(prose_001) == 2, f"expected 2 PROSE-001, got {len(prose_001)}: {prose_001}"
        assert len(prose_002) == 1, f"expected 1 PROSE-002, got {len(prose_002)}: {prose_002}"
        # The 'Coder' must match the actual fixture, not 'agentive'
        matched_kinds = {f["matched"] for f in prose_001}
        assert "Coder" in matched_kinds and "MiniMax" in matched_kinds, matched_kinds
        # Agent/agentive must NOT trigger
        for f in prose_001:
            assert f["matched"] not in ("Agent", "agentive"), f
        # Strict mode would exit 1 with 2 PROSE-001 findings; verify
        # the strict-mode flag by re-running the verdict logic
        from check_prose_authorship import _verdict
        v = _verdict(findings)
        assert v == "NON-CONFORMANT", v
    print("self-test PASS (5 cases)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
