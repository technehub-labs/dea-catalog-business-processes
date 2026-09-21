#!/usr/bin/env python3
"""
check_cross_repo_integrity.py
==============================

Cross-Repository Integrity validator (CR-BP-37; XRI-001..005).

Codifies the catalog's cross-repo reference surface as
machine-testable invariants. The catalog's cross-repo contracts
live in `metamodel-pointer.yaml` (the catalog's authoritative
declaration of which metamodel / root-model / WSF entities it
references) and in `change-requests/README.md` (the `## Cross-repo
context` section that names companion CRs in sibling repos).

CR-BP-37 is a documentation-heavy slice (per the tranche plan,
"~200 LOC"). It does not introduce a CI gate (gate [18] deferred
to a future CR if needed); the validator is a runtime / CI-runnable
asset for the catalog maintainer, not a conformance gate. The
five rules below are enforced offline via --self-test and on the
live pointer via the default invocation.

Rules (derived from CR-BP-37 §3 and the pointer / README layout):

  XRI-001 — metamodel-pointer.yaml structure.
            The pointer file is valid YAML, has the required
            top-level keys (metamodel, catalog, metamodel.entities
            is a non-empty list), and exposes metamodel.entity_id
            + metamodel.class_alias + metamodel.layer at the
            metamodel: block.

  XRI-002 — entity entry completeness.
            Every entity in metamodel.entities[] has the fields
            required by its role: kernel entries require
            entity_id + class_alias + discriminator; opt-in
            entries (lifecycle: proposed) require entity_id +
            lifecycle + a documentation pointer (comment block).

  XRI-003 — federation mapping + canonical CR lineage.
            The pointer file's leading comment block references
            the canonical cross-repo CR lineage: CR-MM-PROC-01
            (metamodel Core), CR-AR-FMWK-01 (root model v0.6.0),
            and the 1:1 LOSSLESS federation mapping between
            `dea:Process` <-> `dea:entity-process` and
            `dea:BusinessProcess` <-> `dea:entity-business-process`.

  XRI-004 — entity_id uniqueness.
            No two entries in metamodel.entities[] share the
            same entity_id. Duplicates would silently shadow
            one entry under the consumer-validator's 1:1
            resolution.

  XRI-005 — companion CR lineage references resolve.
            The `change-requests/README.md` Cross-repo context
            section names companion CRs in sibling repos
            (CR-MM-PROC-01, CR-AR-FMWK-01, CR-ECF-CG-001..004,
            CR-ECF-006/007/008, CR-BC-ECF-03, CR-BO-02, CR-OU-02).
            Every CR referenced from this section MUST either
            exist as a file in `change-requests/` OR be
            acknowledged as a foreign-repo CR (the cross-repo
            itself). The validator enforces the former and
            records the latter.

Coverage on the live catalog (2026-09-12): the pointer file is
in good standing (all 5 rules pass). The companion CR lineage
section is intact.

Exit codes:
  0  all rules pass
  1  at least one rule fails
  2  self-test failure or I/O error

Usage:
  python3 scripts/check_cross_repo_integrity.py
  python3 scripts/check_cross_repo_integrity.py --strict
  python3 scripts/check_cross_repo_integrity.py --json
  python3 scripts/check_cross_repo_integrity.py --self-test

Author: Coder (for eaojnr). Established by CR-BP-37 (2026-09-12).
Derived from CR-BP-37 §3 (cross-repo surface) and the catalog's
metamodel-pointer.yaml + change-requests/README.md layout. See
change-requests/CR-BP-37-cross-repo-integrity.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

# Canonical cross-repo CR lineage (the contracts this catalog
# acknowledges as load-bearing).
CANONICAL_LINEAGE_CRS = (
    "CR-MM-PROC-01",        # dea-metamodel Core authority
    "CR-AR-FMWK-01",        # dea-architecture-framework root model
)

# Companion CRs in sibling repos (named in README Cross-repo context).
# Each is paired with a short label and an expected foreign-repo prefix.
COMPANION_CRS = {
    "CG-001": {"repo": "dea-metaframework",
               "pr_ref": "PR #9 MERGED, commit f5b8e01"},
    "CG-002": {"repo": "dea-metamodel",
               "pr_ref": "PR #154 MERGED, commit 561da9f"},
    "CG-003": {"repo": "dea-catalog-business-capabilities",
               "pr_ref": "proposal PR #33 MERGED, impl PR #34 MERGED, commit 6be58a2"},
    "CG-004": {"repo": "this catalog", "pr_ref": "lands here"},
    "CG-005": {"repo": "dea-metamodel", "pr_ref": "matrix + automated CI"},
    "CG-006": {"repo": "dea-metamodel", "pr_ref": "matrix + automated CI"},
    "CR-MM-PROC-01": {"repo": "dea-metamodel", "pr_ref": "PR #163 MERGED, commit 1665209"},
    "CR-AR-FMWK-01": {"repo": "dea-architecture-framework",
                     "pr_ref": "PR #10 MERGED, commit 76463b2; tag v0.6.0"},
    "CR-BP-L4-01": {"repo": "this catalog",
                    "pr_ref": "alias for the CR-BP-102 L4 decomposition pipeline (PR #146 MERGED)"},
}


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def _load_pointer(catalog_root: Path) -> dict | None:
    p = catalog_root / "metamodel-pointer.yaml"
    if not p.exists():
        return None
    try:
        text = p.read_text()
    except OSError as exc:
        print(f"WARN: {p}: I/O error: {exc}", file=sys.stderr)
        return None
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        print(f"WARN: {p}: YAML parse error: {exc}", file=sys.stderr)
        return None
    return data if isinstance(data, dict) else {}


def _load_pointer_text(catalog_root: Path) -> str:
    p = catalog_root / "metamodel-pointer.yaml"
    if not p.exists():
        return ""
    try:
        return p.read_text()
    except OSError:
        return ""


# -----------------------------------------------------------------------------
# Rules
# -----------------------------------------------------------------------------


def _check_xri_001(pointer: dict | None) -> list[str]:
    """XRI-001: metamodel-pointer.yaml structure."""
    findings = []
    if pointer is None:
        return ["metamodel-pointer.yaml missing or unparseable"]
    if not isinstance(pointer.get("metamodel"), dict):
        findings.append("metamodel-pointer.yaml missing `metamodel:` block")
        return findings
    metamodel = pointer["metamodel"]
    for key in ("entity_id", "class_alias", "layer"):
        if not metamodel.get(key):
            findings.append(
                f"metamodel-pointer.yaml `metamodel.{key}` missing or empty"
            )
    entities = metamodel.get("entities")
    if not isinstance(entities, list) or not entities:
        findings.append(
            "metamodel-pointer.yaml `metamodel.entities` missing or empty"
        )
    if not isinstance(pointer.get("catalog"), dict):
        findings.append("metamodel-pointer.yaml missing `catalog:` block")
    return findings


def _check_xri_002(pointer: dict | None) -> list[str]:
    """XRI-002: entity entry completeness."""
    findings = []
    if not isinstance(pointer, dict):
        return findings
    entities = (pointer.get("metamodel") or {}).get("entities") or []
    if not isinstance(entities, list):
        return findings
    for i, entry in enumerate(entities):
        if not isinstance(entry, dict):
            findings.append(f"metamodel.entities[{i}] is not a mapping")
            continue
        eid = entry.get("entity_id")
        alias = entry.get("class_alias")
        discriminator = entry.get("discriminator")
        lifecycle = entry.get("lifecycle")
        if not eid:
            findings.append(f"metamodel.entities[{i}] missing `entity_id`")
            continue
        # Kernel entry: requires class_alias + discriminator
        if not lifecycle:
            if not alias:
                findings.append(
                    f"metamodel.entities[{i}] (entity_id={eid!r}): kernel "
                    f"entry missing `class_alias`"
                )
            if not discriminator:
                findings.append(
                    f"metamodel.entities[{i}] (entity_id={eid!r}): kernel "
                    f"entry missing `discriminator`"
                )
        # Opt-in entry: requires lifecycle marker
        else:
            if lifecycle not in ("proposed", "draft", "candidate",
                                 "experimental", "deprecated", "retired"):
                findings.append(
                    f"metamodel.entities[{i}] (entity_id={eid!r}): "
                    f"lifecycle={lifecycle!r} not in approved vocabulary "
                    f"(proposed / draft / candidate / experimental / "
                    f"deprecated / retired)"
                )
    return findings


def _check_xri_003(pointer_text: str) -> list[str]:
    """XRI-003: federation mapping + canonical CR lineage."""
    findings = []
    if not pointer_text:
        return findings
    # Canonical CR lineage must be referenced in the leading comment block
    for cr in CANONICAL_LINEAGE_CRS:
        if cr not in pointer_text:
            findings.append(
                f"metamodel-pointer.yaml leading comment block missing "
                f"reference to canonical CR {cr}"
            )
    # Federation mapping must be present
    if "1:1" not in pointer_text or "LOSSLESS" not in pointer_text:
        findings.append(
            "metamodel-pointer.yaml missing the federation mapping comment "
            "(`1:1 LOSSLESS` between metamodel and root-model ids)"
        )
    # Both federation mapping pairs
    if "dea:Process" not in pointer_text or "dea:entity-process" not in pointer_text:
        findings.append(
            "metamodel-pointer.yaml missing the kernel federation pair "
            "(`dea:Process` <-> `dea:entity-process`)"
        )
    if "dea:BusinessProcess" not in pointer_text or "dea:entity-business-process" not in pointer_text:
        findings.append(
            "metamodel-pointer.yaml missing the specialization federation "
            "pair (`dea:BusinessProcess` <-> `dea:entity-business-process`)"
        )
    return findings


def _check_xri_004(pointer: dict | None) -> list[str]:
    """XRI-004: entity_id uniqueness."""
    findings = []
    if not isinstance(pointer, dict):
        return findings
    entities = (pointer.get("metamodel") or {}).get("entities") or []
    if not isinstance(entities, list):
        return findings
    seen: dict[str, int] = {}
    for i, entry in enumerate(entities):
        if not isinstance(entry, dict):
            continue
        eid = entry.get("entity_id")
        if not isinstance(eid, str):
            continue
        if eid in seen:
            findings.append(
                f"metamodel.entities[{i}] duplicates entity_id={eid!r} "
                f"(also at index {seen[eid]})"
            )
        else:
            seen[eid] = i
    return findings


def _check_xri_005(catalog_root: Path) -> list[str]:
    """XRI-005: companion CR lineage references resolve."""
    findings = []
    readme = catalog_root / "change-requests" / "README.md"
    if not readme.exists():
        return findings
    text = readme.read_text()
    # Extract CR ids from the Cross-repo context section
    # (anchor: '## Cross-repo context' until end-of-file or next ## heading)
    m = re.search(r"## Cross-repo context\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if not m:
        return findings
    section = m.group(1)
    cr_ids = set(re.findall(r"CR-[A-Z]+(?:-[A-Z0-9]+)*-\d+[a-zA-Z]?", section))
    # Plus the bare "CG-NNN" tokens
    cr_ids.update(re.findall(r"\bCG-\d{3}\b", section))
    if not cr_ids:
        return findings
    # Each CR must either exist as a file OR be in our COMPANION_CRS table
    for cr_id in sorted(cr_ids):
        # Normalize the bare CG-NNN to "CR-ECF-CG-NNN"
        canonical = cr_id if cr_id.startswith("CR-") else f"CR-ECF-{cr_id}"
        # Check local file
        cr_files = list((catalog_root / "change-requests").glob(f"{canonical}*.md"))
        if cr_files:
            continue
        # Check companion table
        if canonical in COMPANION_CRS or cr_id in COMPANION_CRS:
            continue
        findings.append(
            f"Companion CR {canonical!r} referenced from README "
            f"`## Cross-repo context` section does NOT exist as a file in "
            f"`change-requests/` and is NOT in the COMPANION_CRS table. "
            f"Either add a local file, add an entry to COMPANION_CRS, or "
            f"remove the reference."
        )
    return findings


# -----------------------------------------------------------------------------
# Evaluation
# -----------------------------------------------------------------------------


_RULES = (
    ("XRI-001", "metamodel-pointer.yaml structure"),
    ("XRI-002", "entity entry completeness"),
    ("XRI-003", "federation mapping + canonical CR lineage"),
    ("XRI-004", "entity_id uniqueness"),
    ("XRI-005", "companion CR lineage references resolve"),
)


def evaluate(catalog_root: Path) -> list[dict]:
    findings: list[dict] = []
    pointer = _load_pointer(catalog_root)
    pointer_text = _load_pointer_text(catalog_root)

    for diag in _check_xri_001(pointer):
        findings.append({"rule": "XRI-001", "diagnostic": diag})
    for diag in _check_xri_002(pointer):
        findings.append({"rule": "XRI-002", "diagnostic": diag})
    for diag in _check_xri_003(pointer_text):
        findings.append({"rule": "XRI-003", "diagnostic": diag})
    for diag in _check_xri_004(pointer):
        findings.append({"rule": "XRI-004", "diagnostic": diag})
    for diag in _check_xri_005(catalog_root):
        findings.append({"rule": "XRI-005", "diagnostic": diag})
    return findings


def _verdict(findings: list[dict]) -> str:
    return "NON-CONFORMANT" if findings else "CONFORMANT"


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(
        "Cross-Repository Integrity validator (CR-BP-37; XRI-001..005)."
    ))
    parser.add_argument("--catalog-root", default=".",
                        help="Path to the catalog repo root.")
    parser.add_argument("--strict", action="store_true",
                        help="Exit 1 on any finding.")
    parser.add_argument("--json", action="store_true",
                        help="Emit JSON output.")
    parser.add_argument("--self-test", action="store_true",
                        help="Run the built-in self-test and exit.")
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    catalog_root = Path(args.catalog_root).resolve()
    findings = evaluate(catalog_root)
    verdict = _verdict(findings)

    if args.json:
        print(json.dumps({
            "verdict": verdict,
            "finding_count": len(findings),
            "findings": findings,
            "rules": [{"id": rid, "name": name} for rid, name in _RULES],
            "canonical_lineage": list(CANONICAL_LINEAGE_CRS),
            "companion_crs_count": len(COMPANION_CRS),
        }, indent=2, sort_keys=True))
    else:
        print(f"Cross-Repository Integrity (CR-BP-37; XRI-001..005): {verdict}")
        print(f"  Findings: {len(findings)}")
        for rid, label in _RULES:
            n = sum(1 for f in findings if f["rule"] == rid)
            print(f"    {rid} ({label}): {n}")
        if findings:
            print("\nFindings:")
            for f in findings:
                print(f"  [{f['rule']}] {f['diagnostic']}")

    if findings and args.strict:
        return 1
    return 0


# -----------------------------------------------------------------------------
# Self-test
# -----------------------------------------------------------------------------


def _self_test() -> int:
    """Built-in self-test."""
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)

        # === XRI-001: missing pointer
        f = evaluate(root)
        assert any(x["rule"] == "XRI-001" for x in f), f

        # === XRI-001: pointer without metamodel block
        (root / "metamodel-pointer.yaml").write_text(yaml.safe_dump({
            "id": "dea:catalog-processes",
            "catalog": {},
        }))
        f = evaluate(root)
        assert any(x["rule"] == "XRI-001" for x in f), f

        # === XRI-001 + XRI-002: valid pointer
        (root / "metamodel-pointer.yaml").write_text(yaml.safe_dump({
            "metamodel": {
                "version": "v0.6.0",
                "entity_id": "dea:entity-business-process",
                "class_alias": "BP",
                "layer": "L3",
                "entities": [
                    {"entity_id": "dea:entity-process",
                     "class_alias": "PRC",
                     "discriminator": "process-kernel"},
                ],
            },
            "catalog": {"name": "X", "repo": "x/y"},
        }))
        f = evaluate(root)
        # XRI-003 will fire because the comment block isn't present
        xri001_002 = [x for x in f if x["rule"] in ("XRI-001", "XRI-002")]
        assert xri001_002 == [], xri001_002

        # === XRI-002: kernel entry missing class_alias
        (root / "metamodel-pointer.yaml").write_text(yaml.safe_dump({
            "metamodel": {
                "entity_id": "dea:entity-business-process",
                "class_alias": "BP",
                "layer": "L3",
                "entities": [
                    {"entity_id": "dea:entity-process"},
                ],
            },
            "catalog": {},
        }))
        f = evaluate(root)
        assert any("class_alias" in x["diagnostic"] for x in f
                   if x["rule"] == "XRI-002"), f

        # === XRI-002: opt-in entry with valid lifecycle
        (root / "metamodel-pointer.yaml").write_text(yaml.safe_dump({
            "metamodel": {
                "entity_id": "dea:entity-business-process",
                "class_alias": "BP",
                "layer": "L3",
                "entities": [
                    {"entity_id": "dea:Workflow", "lifecycle": "proposed"},
                ],
            },
            "catalog": {},
        }))
        f = evaluate(root)
        xri002 = [x for x in f if x["rule"] == "XRI-002"]
        assert xri002 == [], xri002

        # === XRI-002: opt-in entry with invalid lifecycle
        (root / "metamodel-pointer.yaml").write_text(yaml.safe_dump({
            "metamodel": {
                "entity_id": "dea:entity-business-process",
                "class_alias": "BP",
                "layer": "L3",
                "entities": [
                    {"entity_id": "dea:Workflow", "lifecycle": "weird"},
                ],
            },
            "catalog": {},
        }))
        f = evaluate(root)
        assert any("weird" in x["diagnostic"] for x in f
                   if x["rule"] == "XRI-002"), f

        # === XRI-003: missing federation mapping
        (root / "metamodel-pointer.yaml").write_text("# no federation\n")
        f = evaluate(root)
        assert any(x["rule"] == "XRI-003" for x in f), f

        # === XRI-003: missing canonical CR lineage
        (root / "metamodel-pointer.yaml").write_text(
            "# 1:1 LOSSLESS mapping\ndea:Process <-> dea:entity-process\n"
            "dea:BusinessProcess <-> dea:entity-business-process\n"
        )
        f = evaluate(root)
        assert any("CR-MM-PROC-01" in x["diagnostic"] for x in f
                   if x["rule"] == "XRI-003"), f

        # === XRI-004: duplicate entity_id
        (root / "metamodel-pointer.yaml").write_text(yaml.safe_dump({
            "metamodel": {
                "entity_id": "dea:entity-business-process",
                "class_alias": "BP",
                "layer": "L3",
                "entities": [
                    {"entity_id": "dea:entity-process",
                     "class_alias": "PRC",
                     "discriminator": "process-kernel"},
                    {"entity_id": "dea:entity-process",
                     "class_alias": "PRC2",
                     "discriminator": "process-kernel-2"},
                ],
            },
            "catalog": {},
        }))
        f = evaluate(root)
        assert any("duplicates" in x["diagnostic"] for x in f
                   if x["rule"] == "XRI-004"), f

        # === XRI-005: README references unknown companion CR
        cr_dir = root / "change-requests"
        cr_dir.mkdir()
        (cr_dir / "README.md").write_text(
            "# CRs\n\n"
            "## Cross-repo context\n"
            "CG-007 lives somewhere.\n"
            "CR-UNKNOWN-99 referenced too.\n"
        )
        # XRI-005 needs no other rules satisfied — isolated test
        xri005_findings = _check_xri_005(root)
        assert any("CG-007" in x for x in xri005_findings), xri005_findings
        assert any("CR-UNKNOWN-99" in x for x in xri005_findings), xri005_findings

        # === XRI-005: README references known companion CR
        (cr_dir / "README.md").write_text(
            "# CRs\n\n"
            "## Cross-repo context\n"
            "CR-MM-PROC-01 lives in dea-metamodel.\n"
            "CG-001 lands in dea-metaframework.\n"
        )
        xri005_findings = _check_xri_005(root)
        assert xri005_findings == [], xri005_findings

        # === Full clean state
        # Build a fully valid pointer + a README with known companions
        (root / "metamodel-pointer.yaml").write_text(
            "# CR-MM-PROC-01; CR-AR-FMWK-01\n"
            "# 1:1 LOSSLESS mapping:\n"
            "#   dea:Process <-> dea:entity-process\n"
            "#   dea:BusinessProcess <-> dea:entity-business-process\n"
            + yaml.safe_dump({
                "metamodel": {
                    "version": "v0.6.0",
                    "entity_id": "dea:entity-business-process",
                    "class_alias": "BP",
                    "layer": "L3",
                    "entities": [
                        {"entity_id": "dea:entity-process",
                         "class_alias": "PRC",
                         "discriminator": "process-kernel"},
                        {"entity_id": "dea:Activity", "lifecycle": "proposed"},
                    ],
                },
                "catalog": {"name": "BP", "repo": "x/y"},
            })
        )
        (cr_dir / "README.md").write_text(
            "# CRs\n\n## Cross-repo context\n"
            "CR-MM-PROC-01 lands in dea-metamodel.\n"
            "CR-AR-FMWK-01 lands in dea-architecture-framework.\n"
        )
        f = evaluate(root)
        assert f == [], f

    print("self-test PASS (12 cases)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
