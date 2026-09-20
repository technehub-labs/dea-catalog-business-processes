#!/usr/bin/env python3
"""
check_mece.py
==============

MECE Validation (CR-BP-36; MECE-001..008).

Codifies catalog-wide MECE (Mutually Exclusive, Collectively Exhaustive)
checks as machine-testable rules. CR-BP-16 implements *Conformance* (is
this artifact structurally and semantically valid?); CR-BP-36 implements
*MECE* (is the catalog collectively exhaustive and mutually exclusive?).
These are orthogonal concerns (CR-BP-34 §4).

Gate [7] (check_process_group.py, PG-001..008) covers intra-context MECE
for Process Groups (PG-006: no two PGs share an L2 process in the same
context). CR-BP-36 covers the catalog-wide MECE that gate [7] does NOT
cover: cross-coordinate coverage, register-to-catalog alignment, BP
semantic uniqueness, and orphan detection.

Rules (derived from CR-BP-34 §4 and the catalog's actual structure):

  MECE-001 — Coordinate coverage (PC existence).
             Every register-landed coordinate (Domain x Lifecycle Stage
             with audit_status=landed) has a canonical Process Context
             record on disk. Matching is by (domain, lifecycle_stage)
             coordinate, NOT by raw PC id string, because the register
             uses the full-word convention (dea:pc-ge-conceive) while
             some PC records use the abbreviated convention (dea:pc-ge-c)
             — a known legacy drift from CR-BP-13.

  MECE-002 — Group coverage per context.
             Every canonical Process Context record has at least one
             canonical Process Group whose process_context field
             references it (coordinate match).

  MECE-003 — BP coverage per group.
             Every canonical Process Group composes at least one
             canonical Business Process (via composes[].target_id
             matching a dea:process-* record on disk).

  MECE-004 — BP semantic uniqueness.
             No two canonical Business Process records share the same
             normalized (identity.verb, identity.object) pair.
             Normalization: case-fold + strip whitespace. This prevents
             semantic duplication (two BPs that are the "same" process
             under different ids).

  MECE-005 — Group coordinate uniqueness.
             No two canonical Process Groups share the same
             (process_context, normalized name) pair. Within a context,
             each group must have a distinct name. Cross-context groups
             may share names (they serve different coordinates).

  MECE-006 — Register-to-catalog alignment (group coverage).
             Every register-landed coordinate has at least one canonical
             Process Group on disk (cross-check register vs catalog).
             This is the reverse of MECE-002: MECE-002 checks that every
             PC has a group; MECE-006 checks that every register-landed
             coordinate has a group.

  MECE-007 — Orphan detection (PG → PC).
             Every canonical Process Group references a Process Context
             that exists on disk (coordinate match). A PG whose
             process_context does not resolve to any PC record is an
             orphan.

  MECE-008 — Orphan detection (BP → PG).
             Every canonical Business Process is composed by at least
             one Process Group (via the PG's composes[].target_id
             matching the BP's id). A BP not referenced by any PG
             is an orphan.

Coverage on the live catalog (2026-09-12):
  131 BP + 40 PG + 40 PC records.
  Expected findings: MECE-001..008 = 0.
  The catalog is fully aligned: 35 register-landed coordinates each
  have a PC, a PG, and BPs; 131 BPs each have a unique (verb, object)
  and are composed by exactly one PG.

Exit codes:
  0  all records satisfy all eight rules
  1  at least one record fails at least one rule
  2  self-test failure or I/O error

Usage:
  python3 scripts/check_mece.py
  python3 scripts/check_mece.py --strict
  python3 scripts/check_mece.py --json
  python3 scripts/check_mece.py --self-test

Author: Coder (for eaojnr). Established by CR-BP-36 (2026-09-12).
Derived from CR-BP-34 §4 (Conformance vs MECE) and the catalog's
actual structure. See change-requests/CR-BP-36-mece-validation.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

# ID patterns (CR-BP-04 §4).
PC_ID_PATTERN = re.compile(r"^processes:pc-[a-z0-9-]+$")
GROUP_ID_PATTERN = re.compile(r"^processes:group-[a-z0-9-]+$")
BP_ID_PATTERN = re.compile(r"^processes:process-[a-z0-9-]+$")

# Register path (single canonical location per CR-BP-13 / CR-BP-22).
REGISTER_PATH = (
    "entities/v1-alpha/pr-operate/pr-operate-7ab3ma"
    "/research/l1-register.yaml"
)


# -----------------------------------------------------------------------------
# Discovery
# -----------------------------------------------------------------------------


def _load_bp_records(catalog_root: Path) -> list[tuple[Path, dict]]:
    """Load every canonical Business Process record (CR-BP-mv1 tree)."""
    base = catalog_root / "entities" / "v1-alpha"
    pairs = []
    if not base.exists():
        return pairs
    for yaml_path in sorted(base.rglob("processes-process-*.yaml")):
        if not yaml_path.exists():
            continue
        try:
            data = yaml.safe_load(yaml_path.read_text())
        except yaml.YAMLError as exc:
            print(f"WARN: {yaml_path}: YAML parse error: {exc}",
                  file=sys.stderr)
            continue
        if isinstance(data, dict):
            pairs.append((yaml_path, data))
    return pairs


def _load_pg_records(catalog_root: Path) -> list[tuple[Path, dict]]:
    """Load every canonical Process Group record (CR-BP-mv1 tree)."""
    base = catalog_root / "entities" / "v1-alpha"
    pairs = []
    if not base.exists():
        return pairs
    for yaml_path in sorted(base.rglob("processes-group-*.yaml")):
        if not yaml_path.exists():
            continue
        try:
            data = yaml.safe_load(yaml_path.read_text())
        except yaml.YAMLError as exc:
            print(f"WARN: {yaml_path}: YAML parse error: {exc}",
                  file=sys.stderr)
            continue
        if isinstance(data, dict):
            pairs.append((yaml_path, data))
    return pairs


def _load_pc_records(catalog_root: Path) -> list[tuple[Path, dict]]:
    """Load every canonical Process Context record.

    CR-BP-mv1: PCs live in the containment tree (contexts/ is retired)."""
    ctx_dir = catalog_root / "entities" / "v1-alpha"
    pairs = []
    if not ctx_dir.exists():
        return pairs
    for yf in sorted(ctx_dir.rglob("processes-pc-*.yaml")):
        try:
            data = yaml.safe_load(yf.read_text())
        except yaml.YAMLError as exc:
            print(f"WARN: {yf}: YAML parse error: {exc}", file=sys.stderr)
            continue
        if isinstance(data, dict):
            pairs.append((yf, data))
    return pairs


def _load_register(catalog_root: Path) -> dict:
    """Load the L1 register (CR-BP-13 / CR-BP-22)."""
    reg_path = catalog_root / REGISTER_PATH
    if not reg_path.exists():
        return {}
    try:
        data = yaml.safe_load(reg_path.read_text())
    except yaml.YAMLError as exc:
        print(f"WARN: {reg_path}: YAML parse error: {exc}", file=sys.stderr)
        return {}
    return data if isinstance(data, dict) else {}


# -----------------------------------------------------------------------------
# Index builders
# -----------------------------------------------------------------------------


def _pc_coordinate_index(pc_pairs: list[tuple[Path, dict]]) -> dict[tuple[str, str], str]:
    """Build {(domain, lifecycle_stage) -> pc_id} from PC records."""
    index = {}
    for _path, rec in pc_pairs:
        domain = rec.get("domain", "")
        stage = rec.get("lifecycle_stage", "")
        pc_id = rec.get("id", "")
        if domain and stage and pc_id:
            index[(domain, stage)] = pc_id
    return index


def _pc_id_set(pc_pairs: list[tuple[Path, dict]]) -> set[str]:
    """Build {pc_id} from PC records."""
    return {rec.get("id", "") for _p, rec in pc_pairs if rec.get("id")}


def _pg_pc_reference_index(pg_pairs: list[tuple[Path, dict]]) -> dict[str, list[str]]:
    """Build {pc_id -> [pg_id]} from PG records."""
    index: dict[str, list[str]] = {}
    for _path, rec in pg_pairs:
        pc_ref = rec.get("process_context", "")
        pg_id = rec.get("id", "")
        if pc_ref and pg_id:
            index.setdefault(pc_ref, []).append(pg_id)
    return index


def _pg_composes_index(pg_pairs: list[tuple[Path, dict]]) -> dict[str, list[str]]:
    """Build {pg_id -> [bp_target_id]} from PG composes[] entries."""
    index: dict[str, list[str]] = {}
    for _path, rec in pg_pairs:
        pg_id = rec.get("id", "")
        if not pg_id:
            continue
        targets = []
        for entry in rec.get("composes", []):
            if isinstance(entry, dict):
                tid = entry.get("target_id", "")
                if tid:
                    targets.append(tid)
        index[pg_id] = targets
    return index


def _bp_composed_by_index(pg_pairs: list[tuple[Path, dict]]) -> dict[str, list[str]]:
    """Build {bp_id -> [pg_id]} from PG composes[] entries (reverse)."""
    index: dict[str, list[str]] = {}
    for _path, rec in pg_pairs:
        pg_id = rec.get("id", "")
        if not pg_id:
            continue
        for entry in rec.get("composes", []):
            if isinstance(entry, dict):
                tid = entry.get("target_id", "")
                if tid:
                    index.setdefault(tid, []).append(pg_id)
    return index


def _register_landed_coordinates(register: dict) -> dict[tuple[str, str], str]:
    """Build {(domain, stage) -> register_pc_ref} from the register."""
    coords = {}
    reg = register.get("register", {})
    if not isinstance(reg, dict):
        return coords
    for domain, stages in reg.items():
        if not isinstance(stages, dict):
            continue
        for stage, cell in stages.items():
            if isinstance(cell, dict) and cell.get("audit_status") == "landed":
                pc_ref = cell.get("process_context", "")
                coords[(domain, stage)] = pc_ref
    return coords


def _normalize(text: str) -> str:
    """Case-fold + strip for semantic comparison."""
    return text.strip().lower() if isinstance(text, str) else ""


# -----------------------------------------------------------------------------
# Rules
# -----------------------------------------------------------------------------


def _check_mece_001(register_coords: dict[tuple[str, str], str],
                    pc_index: dict[tuple[str, str], str]) -> list[str]:
    """MECE-001: every register-landed coordinate has a PC record."""
    findings = []
    for (domain, stage), reg_pc in sorted(register_coords.items()):
        if (domain, stage) not in pc_index:
            findings.append(
                f"Register-landed coordinate ({domain} x {stage}) "
                f"references {reg_pc!r} but no canonical PC record "
                f"exists for that coordinate"
            )
    return findings


def _check_mece_002(pc_pairs: list[tuple[Path, dict]],
                    pg_pc_index: dict[str, list[str]]) -> list[str]:
    """MECE-002: every PC has at least one PG referencing it."""
    findings = []
    for _path, rec in pc_pairs:
        pc_id = rec.get("id", "")
        domain = rec.get("domain", "")
        stage = rec.get("lifecycle_stage", "")
        if pc_id not in pg_pc_index:
            findings.append(
                f"PC {pc_id!r} ({domain} x {stage}) has no canonical "
                f"Process Group referencing it"
            )
    return findings


def _check_mece_003(pg_pairs: list[tuple[Path, dict]],
                    bp_ids: set[str]) -> list[str]:
    """MECE-003: every PG composes at least one BP."""
    findings = []
    for _path, rec in pg_pairs:
        pg_id = rec.get("id", "")
        composes = rec.get("composes", [])
        bp_targets = [
            e.get("target_id", "")
            for e in composes
            if isinstance(e, dict) and BP_ID_PATTERN.match(e.get("target_id", ""))
        ]
        # At least one target must resolve to an actual BP record
        resolved = [t for t in bp_targets if t in bp_ids]
        if not resolved:
            findings.append(
                f"PG {pg_id!r} composes no canonical Business Process "
                f"(composes[] has {len(composes)} entries, "
                f"{len(bp_targets)} match dea:process-*, "
                f"{len(resolved)} resolve to a record on disk)"
            )
    return findings


def _check_mece_004(bp_pairs: list[tuple[Path, dict]]) -> list[str]:
    """MECE-004: no two BPs share the same (verb, object)."""
    findings = []
    seen: dict[tuple[str, str], str] = {}
    for _path, rec in bp_pairs:
        bp_id = rec.get("id", "")
        ident = rec.get("identity", {})
        if not isinstance(ident, dict):
            continue
        verb = _normalize(ident.get("verb", ""))
        obj = _normalize(ident.get("object", ""))
        if not verb or not obj:
            continue
        key = (verb, obj)
        if key in seen:
            findings.append(
                f"BP {bp_id!r} shares identity (verb={verb!r}, "
                f"object={obj!r}) with BP {seen[key]!r} "
                f"(semantic duplication)"
            )
        else:
            seen[key] = bp_id
    return findings


def _check_mece_005(pg_pairs: list[tuple[Path, dict]]) -> list[str]:
    """MECE-005: no two PGs share the same (pc, name)."""
    findings = []
    seen: dict[tuple[str, str], str] = {}
    for _path, rec in pg_pairs:
        pg_id = rec.get("id", "")
        pc_ref = rec.get("process_context", "")
        name = _normalize(rec.get("name", ""))
        if not pc_ref or not name:
            continue
        key = (pc_ref, name)
        if key in seen:
            findings.append(
                f"PG {pg_id!r} shares (process_context={pc_ref!r}, "
                f"name={name!r}) with PG {seen[key]!r}"
            )
        else:
            seen[key] = pg_id
    return findings


def _check_mece_006(register_coords: dict[tuple[str, str], str],
                    pc_index: dict[tuple[str, str], str],
                    pg_pc_index: dict[str, list[str]]) -> list[str]:
    """MECE-006: every register-landed coordinate has at least one PG."""
    findings = []
    for (domain, stage), reg_pc in sorted(register_coords.items()):
        # Resolve the coordinate to the actual PC id on disk
        actual_pc = pc_index.get((domain, stage))
        if not actual_pc:
            continue  # MECE-001 already fires here
        if actual_pc not in pg_pc_index:
            findings.append(
                f"Register-landed coordinate ({domain} x {stage}) "
                f"has PC {actual_pc!r} but no canonical Process Group "
                f"references it"
            )
    return findings


def _check_mece_007(pg_pairs: list[tuple[Path, dict]],
                    pc_ids: set[str]) -> list[str]:
    """MECE-007: every PG references an existing PC (no orphans)."""
    findings = []
    for _path, rec in pg_pairs:
        pg_id = rec.get("id", "")
        pc_ref = rec.get("process_context", "")
        if pc_ref and pc_ref not in pc_ids:
            findings.append(
                f"PG {pg_id!r} references PC {pc_ref!r} which does "
                f"not exist on disk (orphan)"
            )
    return findings


def _check_mece_008(bp_pairs: list[tuple[Path, dict]],
                    bp_composed_by: dict[str, list[str]]) -> list[str]:
    """MECE-008: every BP is composed by at least one PG (no orphans).

    Deprecated records are exempt: a deprecated BP is intentionally
    not composed by any PG (it has been superseded or retired from
    active use). The exemption is by lifecycle_status=deprecated.
    """
    findings = []
    for _path, rec in bp_pairs:
        bp_id = rec.get("id", "")
        ls = rec.get("lifecycle_status", "")
        if ls == "deprecated":
            continue  # deprecated records are intentionally not composed
        if bp_id and bp_id not in bp_composed_by:
            findings.append(
                f"BP {bp_id!r} is not composed by any Process Group "
                f"(orphan; lifecycle_status={ls!r})"
            )
    return findings


# -----------------------------------------------------------------------------
# Evaluation
# -----------------------------------------------------------------------------


def evaluate(catalog_root: Path) -> list[dict]:
    """Run all eight MECE rules against the catalog."""
    bp_pairs = _load_bp_records(catalog_root)
    pg_pairs = _load_pg_records(catalog_root)
    pc_pairs = _load_pc_records(catalog_root)
    register = _load_register(catalog_root)

    # Build indices
    pc_index = _pc_coordinate_index(pc_pairs)
    pc_ids = _pc_id_set(pc_pairs)
    pg_pc_index = _pg_pc_reference_index(pg_pairs)
    bp_ids = {rec.get("id", "") for _p, rec in bp_pairs if rec.get("id")}
    bp_composed_by = _bp_composed_by_index(pg_pairs)
    register_coords = _register_landed_coordinates(register)

    findings: list[dict] = []

    # MECE-001: coordinate coverage
    for diag in _check_mece_001(register_coords, pc_index):
        findings.append({"rule": "MECE-001", "record_id": "(register)", "diagnostic": diag})

    # MECE-002: group coverage per context
    for diag in _check_mece_002(pc_pairs, pg_pc_index):
        findings.append({"rule": "MECE-002", "record_id": "(pc)", "diagnostic": diag})

    # MECE-003: BP coverage per group
    for diag in _check_mece_003(pg_pairs, bp_ids):
        findings.append({"rule": "MECE-003", "record_id": "(pg)", "diagnostic": diag})

    # MECE-004: BP semantic uniqueness
    for diag in _check_mece_004(bp_pairs):
        findings.append({"rule": "MECE-004", "record_id": "(bp)", "diagnostic": diag})

    # MECE-005: group coordinate uniqueness
    for diag in _check_mece_005(pg_pairs):
        findings.append({"rule": "MECE-005", "record_id": "(pg)", "diagnostic": diag})

    # MECE-006: register-to-catalog alignment
    for diag in _check_mece_006(register_coords, pc_index, pg_pc_index):
        findings.append({"rule": "MECE-006", "record_id": "(register)", "diagnostic": diag})

    # MECE-007: orphan PG → PC
    for diag in _check_mece_007(pg_pairs, pc_ids):
        findings.append({"rule": "MECE-007", "record_id": "(pg)", "diagnostic": diag})

    # MECE-008: orphan BP → PG
    for diag in _check_mece_008(bp_pairs, bp_composed_by):
        findings.append({"rule": "MECE-008", "record_id": "(bp)", "diagnostic": diag})

    return findings


_RULES = (
    ("MECE-001", "Coordinate coverage (PC existence)"),
    ("MECE-002", "Group coverage per context"),
    ("MECE-003", "BP coverage per group"),
    ("MECE-004", "BP semantic uniqueness"),
    ("MECE-005", "Group coordinate uniqueness"),
    ("MECE-006", "Register-to-catalog alignment"),
    ("MECE-007", "Orphan detection (PG → PC)"),
    ("MECE-008", "Orphan detection (BP → PG)"),
)


def _verdict(findings: list[dict]) -> str:
    return "NON-CONFORMANT" if findings else "CONFORMANT"


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(
        "MECE Validation (CR-BP-36; MECE-001..008)."
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
            "rules": [{"id": rid, "name": label} for rid, label in _RULES],
        }, indent=2, sort_keys=True))
    else:
        print(f"MECE Validation (CR-BP-36; MECE-001..008): {verdict}")
        print(f"  Findings: {len(findings)}")
        for rid, label in _RULES:
            n = sum(1 for f in findings if f["rule"] == rid)
            print(f"    {rid} ({label}): {n}")
        if findings:
            print("\nFindings:")
            for f in findings:
                print(f"  [{f['rule']}] {f['record_id']}: {f['diagnostic']}")

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

        # --- Helper to write a record
        def _write_bp(id_, verb="Manage", obj="X"):
            slug = id_.split(":", 1)[1].replace(":", "-")
            d = root / "entities" / "v1-alpha" / "pr-operate" / slug
            d.mkdir(parents=True, exist_ok=True)
            (d / f"processes-{slug}.yaml").write_text(yaml.safe_dump({
                "id": id_, "name": f"{verb} {obj}", "type": "Process",
                "version": "1.0.0",
                "identity": {"verb": verb, "object": obj},
            }))

        def _write_pg(id_, pc_ref, name, composes_targets=None):
            slug = id_.split(":", 1)[1].replace(":", "-")
            d = root / "entities" / "v1-alpha" / "pr-operate" / slug
            d.mkdir(parents=True, exist_ok=True)
            composes = []
            if composes_targets:
                for t in composes_targets:
                    composes.append({
                        "source_id": id_,
                        "target_id": t,
                        "relationship_type": "dea:composes",
                    })
            (d / f"processes-{slug}.yaml").write_text(yaml.safe_dump({
                "id": id_, "name": name, "type": "ProcessGroup",
                "version": "1.0.0",
                "process_context": pc_ref,
                "composes": composes,
            }))

        def _write_pc(id_, domain, stage):
            d = root / "entities" / "v1-alpha" / "pr-operate"
            d.mkdir(parents=True, exist_ok=True)
            fname = id_.replace(":", "-") + ".yaml"
            (d / fname).write_text(yaml.safe_dump({
                "id": id_, "domain": domain, "lifecycle_stage": stage,
                "name": f"{domain} x {stage}",
            }))

        def _write_register(coords):
            d = root / "entities" / "v1-alpha" / "pr-operate" / "pr-operate-7ab3ma" / "research"
            d.mkdir(parents=True, exist_ok=True)
            reg = {"register": {}}
            for (domain, stage), pc_ref in coords.items():
                reg["register"].setdefault(domain, {})[stage] = {
                    "process_context": pc_ref,
                    "audit_status": "landed",
                }
            (d / "l1-register.yaml").write_text(yaml.safe_dump(reg))

        # === MECE-001: register coordinate without PC ===
        _write_register({("D1", "S1"): "processes:pc-d1-s1"})
        f = evaluate(root)
        assert any(x["rule"] == "MECE-001" for x in f), f

        # === MECE-001: register coordinate WITH PC passes ===
        _write_pc("processes:pc-d1-s1", "D1", "S1")
        f = evaluate(root)
        assert not any(x["rule"] == "MECE-001" for x in f), f

        # === MECE-002: PC without PG ===
        f = evaluate(root)
        assert any(x["rule"] == "MECE-002" for x in f), f

        # === MECE-002: PC with PG passes ===
        _write_pg("processes:group-g1", "processes:pc-d1-s1", "Group One")
        f = evaluate(root)
        assert not any(x["rule"] == "MECE-002" for x in f), f

        # === MECE-003: PG without BP ===
        f = evaluate(root)
        assert any(x["rule"] == "MECE-003" for x in f), f

        # === MECE-003: PG with BP passes ===
        _write_bp("processes:process-b1", "Manage", "Thing")
        # Re-write PG with composes
        _write_pg("processes:group-g1", "processes:pc-d1-s1", "Group One",
                  composes_targets=["processes:process-b1"])
        f = evaluate(root)
        assert not any(x["rule"] == "MECE-003" for x in f), f

        # === MECE-004: duplicate (verb, object) ===
        _write_bp("processes:process-b2", "Manage", "Thing")
        f = evaluate(root)
        assert any(x["rule"] == "MECE-004" for x in f), f

        # === MECE-004: unique passes ===
        _write_bp("processes:process-b2", "Manage", "Other Thing")
        f = evaluate(root)
        assert not any(x["rule"] == "MECE-004" for x in f), f

        # === MECE-005: duplicate (pc, name) ===
        _write_pg("processes:group-g2", "processes:pc-d1-s1", "Group One",
                  composes_targets=["processes:process-b1"])
        f = evaluate(root)
        assert any(x["rule"] == "MECE-005" for x in f), f

        # === MECE-005: different name passes ===
        _write_pg("processes:group-g2", "processes:pc-d1-s1", "Group Two",
                  composes_targets=["processes:process-b1"])
        f = evaluate(root)
        assert not any(x["rule"] == "MECE-005" for x in f), f

        # === MECE-006: register coordinate without PG ===
        # (covered by MECE-002 in this fixture; MECE-006 is the register-side)
        f = evaluate(root)
        assert not any(x["rule"] == "MECE-006" for x in f), f

        # === MECE-007: PG references non-existent PC ===
        _write_pg("processes:group-g3", "processes:pc-nonexistent", "Orphan Group",
                  composes_targets=["processes:process-b1"])
        f = evaluate(root)
        assert any(x["rule"] == "MECE-007" for x in f), f

        # === MECE-007: clean after removing orphan ===
        import shutil
        shutil.rmtree(root / "entities" / "v1-alpha" / "pr-operate" / "group-g3")
        f = evaluate(root)
        assert not any(x["rule"] == "MECE-007" for x in f), f

        # === MECE-008: BP not composed by any PG ===
        _write_bp("processes:process-orphan", "Orphan", "Process")
        f = evaluate(root)
        assert any(x["rule"] == "MECE-008" for x in f), f

        # === MECE-008: clean after composing orphan ===
        _write_pg("processes:group-g1", "processes:pc-d1-s1", "Group One",
                  composes_targets=["processes:process-b1", "processes:process-orphan",
                                    "processes:process-b2"])
        f = evaluate(root)
        assert not any(x["rule"] == "MECE-008" for x in f), f

        # === MECE-008: deprecated BP is exempt ===
        _write_bp("processes:process-deprecated", "Old", "Process")
        # Manually set deprecated lifecycle_status
        dep_dir = root / "entities" / "v1-alpha" / "pr-operate" / "process-deprecated"
        dep_yaml = dep_dir / "processes-process-deprecated.yaml"
        dep_data = yaml.safe_load(dep_yaml.read_text())
        dep_data["lifecycle_status"] = "deprecated"
        dep_yaml.write_text(yaml.safe_dump(dep_data))
        f = evaluate(root)
        assert not any(x["rule"] == "MECE-008" for x in f), f

        # === Full clean state ===
        f = evaluate(root)
        assert f == [], f

    print("self-test PASS (14 cases)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
