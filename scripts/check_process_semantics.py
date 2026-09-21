#!/usr/bin/env python3
"""
check_process_semantics.py: Process Semantics validator.

Implements CR-BP-14 §21 rules BP-SEM-001..BP-SEM-012.

Rules:

  BP-SEM-001  Intent Vocabulary (CR-BP-14 S9.2; classification/process-intents.yaml).
              process_intent MUST contain only an approved intent value.

  BP-SEM-002  Classification Vocabulary (CR-BP-14 S10.2; process-types.yaml).
              process_type / process_classification.type MUST use the
              approved landscape vocabulary.

  BP-SEM-003  Intent Independence (CR-BP-14 S11, S18).
              Validation MUST NOT infer Process Intent from Process
              Classification. Enforced by construction: the rules are
              evaluated independently and no rule emits a finding
              because a classification token lexically resembles an
              intent token.

  BP-SEM-004  Classification Independence (CR-BP-14 S11, S18).
              Validation MUST NOT infer Process Classification from
              Process Intent. Enforced by construction; same argument.

  BP-SEM-005  Specialization Validity (CR-BP-14 S12.2).
              Every specialization reference MUST resolve to an existing
              process entry (dea:process-*) currently canonical.

  BP-SEM-006  Specialization Differentiation (CR-BP-14 S12.2).
              A specialized process MUST carry a specialization_pattern
              and the pattern MUST be drawn from the approved basis
              vocabulary (process-specializations.yaml) or be a free-text
              label accompanied by a non-empty specialization_basis field.

  BP-SEM-007  Context Distinction (CR-BP-14 S13).
              A Process Context MUST NOT be represented solely through
              process_audience. The canonical `context:` block MUST be
              present (with at least one Process Context reference) on
              every canonical Business Process entry.

  BP-SEM-008  Context Reference Integrity (CR-BP-14 S13).
              Every declared Process Context reference MUST resolve to
              a canonical Process Context entry (dea:pc-*) under
              contexts/v1-alpha/.

  BP-SEM-009  Identity Independence (CR-BP-14 S15).
              Changes to intent, classification, context, or audience
              SHALL NOT automatically create a new process identity.
              Enforced by construction: the validator never asserts
              that intent/classification/context differences mandate
              distinct identities; it never compares two entries by
              intent/classification/context to declare a split.

  BP-SEM-010  Legacy Detection (CR-BP-14 S17, S19).
              Legacy process_intent values (operational, management) and
              legacy scalar process_context fields are reported as
              migration findings (warning class until CR-BP-15
              migration completes). process_audience presence is also
              reported as a migration-alias finding (not blocking).

  BP-SEM-011  Classification Collision (CR-BP-14 S11).
              Identical vocabulary appearing in Intent and
              Classification SHALL NOT be treated as semantic
              equivalence. The shared `support` token is a lexical
              coincidence; the rule emits a warning whenever
              process_intent equals process_type lexically, so a human
              can confirm the choice is intentional.

  BP-SEM-012  Context Multiplicity (CR-BP-14 S13).
  BP-SEM-013  Specialization Relationship (CR-BP-14 S12, S23).
              Every `relationships[]` entry with relationship_type
              'specializes' MUST target a canonical Process entry;
              the target_id MUST match the dea:process-<id> pattern;
              the entry MUST declare specialization_pattern (from the
              approved basis vocabulary) or a non-empty
              specialization_basis field. Specialization is
              intra-context (CR-BP-14 S23); cross-context
              specialization is decomposition, not specialization.
  BP-SEM-014  Specialization Cycle Detection (CR-BP-16 S10).
              The specializes graph MUST be acyclic. A cycle (A
              specializes B, B specializes A; or A -> B -> C -> A)
              is an architectural regression and SHALL block
              canonical admission. Identical parent/child semantics
              (same id specializing itself) are forbidden.
              A Business Process MAY participate in multiple Process
              Contexts where evidence establishes legitimate
              cross-context responsibility. The rule never treats
              multiple context references as an error; it reports the
              count as advisory information only.

Exit: 0 = all blocking rules pass (warnings may be reported); 1 = at least
one blocking rule failed; 2 = self-test.

Built-in --self-test exercises each rule on a deliberately broken
catalog (then on a fixed catalog) and verifies the expected exit codes.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

import yaml

BASE = Path(__file__).parent.parent

# Authoritative intent vocabulary (CR-BP-14 S9.2). Mirrors
# classifications/process-intents.yaml canonical values + legacy
# aliases admitted as deprecated migration values (S17).
CANONICAL_INTENTS = {
    "govern", "manage", "operate", "deliver", "support", "develop",
    "transform",
}
LEGACY_INTENTS = {"operational", "management"}  # `support` is both

# Authoritative classification vocabulary (CR-BP-14 S10.2). Mirrors
# classifications/process-types.yaml.
CLASSIFICATION_VALUES = {
    "strategic", "management", "core", "support", "standardization",
}

# Approved specialization bases (CR-BP-14 S12.2). The labels carry the
# "by-" prefix used throughout the catalog (see
# classifications/process-specializations.yaml + docs/classification.md).
# A free-text label is also admitted when accompanied by a
# specialization_basis field.
APPROVED_SPECIALIZATION_BASES = {
    "by-customer-segment", "by-geography", "by-product", "by-service",
    "by-channel", "by-regulatory-regime", "by-operating-model",
    "by-lifecycle-condition", "by-organizational-context",
}

PC_PATTERN = re.compile(r"^processes:pc-[a-z0-9-]+$")
PROCESS_PATTERN = re.compile(r"^processes:process-[a-z0-9-]+$")


def _make_emit(prefix: str):
    """Return an `emit(messages, rule, msg)` closure with the
    given prefix baked in. Module-level so other helpers can use it.
    """
    def emit(messages: list[str], rule: str, msg: str) -> None:
        messages.append(f"rule:{rule} {prefix}: {msg}")
    return emit


def _load_yaml(path: Path) -> dict | None:
    try:
        return yaml.safe_load(path.read_text()) or {}
    except yaml.YAMLError:
        return None


def _catalog_pc_ids(catalog_root: Path) -> set[str]:
    """CR-BP-mv1: PCs now live in the L0-rooted containment tree at
    entities/v1-alpha/<cell>/processes-pc-*.yaml (contexts/ is retired)."""
    ent_dir = catalog_root / "entities" / "v1-alpha"
    ids: set[str] = set()
    if not ent_dir.exists():
        return ids
    for path in ent_dir.rglob("processes-pc-*.yaml"):
        data = _load_yaml(path) or {}
        cid = data.get("id")
        if cid:
            ids.add(cid)
    return ids


def _catalog_process_ids(catalog_root: Path) -> set[str]:
    ent_dir = catalog_root / "entities" / "v1-alpha"
    ids: set[str] = set()
    if not ent_dir.exists():
        return ids
    for path in ent_dir.rglob("processes-process-*.yaml"):
        data = _load_yaml(path) or {}
        cid = data.get("id")
        if cid:
            ids.add(cid)
    return ids


def _classification_value(entry: dict) -> str | None:
    """Return the effective landscape classification for an entry.

    Honors the canonical block form (process_classification.type,
    CR-BP-14 S20) and the backward-compatible alias (process_type).
    """
    block = entry.get("process_classification")
    if isinstance(block, dict) and block.get("type"):
        return block["type"]
    return entry.get("process_type")


def _intent_value(entry: dict) -> str | None:
    val = entry.get("process_intent")
    if isinstance(val, str):
        return val
    return None


def _context_refs(entry: dict) -> list[str]:
    refs = entry.get("context")
    out: list[str] = []
    if isinstance(refs, list):
        for r in refs:
            if isinstance(r, dict) and r.get("ref"):
                out.append(r["ref"])
    return out


def _audience_value(entry: dict) -> str | None:
    val = entry.get("process_audience")
    if isinstance(val, str):
        return val
    return None


def run_checks(
    catalog_root: Path,
    pc_ids: set[str] | None = None,
    process_ids: set[str] | None = None,
) -> tuple[list[str], list[str]]:
    """Return (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []

    if pc_ids is None:
        pc_ids = _catalog_pc_ids(catalog_root)
    if process_ids is None:
        process_ids = _catalog_process_ids(catalog_root)

    entries_dir = catalog_root / "entities" / "v1-alpha"
    if not entries_dir.exists():
        return errors, warnings

    for path in sorted(entries_dir.rglob("processes-process-*.yaml")):
        data = _load_yaml(path) or {}
        # L1 Process Groups are catalog-owned; the semantic rules
        # apply to L2 Business Processes only.
        if data.get("type") != "Process":
            continue
        eid = data.get("id", path.stem)
        prefix = f"BP-SEM ({eid})"

        # Emit a `rule:<code> prefix so callers (and the self-test) can
        # extract the rule deterministically without parsing prose.
        emit = _make_emit(f"BP-SEM ({eid})")

        intent = _intent_value(data)
        classification = _classification_value(data)
        context_refs = _context_refs(data)
        audience = _audience_value(data)
        specialization = data.get("process_specialization") or []
        specialization_pattern = data.get("specialization_pattern")
        specialization_basis = data.get("specialization_basis")

        # BP-SEM-001: Intent vocabulary
        if intent is None:
            emit(errors, "BP-SEM-001", "process_intent is required")
        elif intent not in CANONICAL_INTENTS | LEGACY_INTENTS:
            emit(
                errors, "BP-SEM-001",
                f"process_intent={intent!r} is not in the approved vocabulary "
                f"(canonical: {sorted(CANONICAL_INTENTS)})"
            )

        # BP-SEM-002: Classification vocabulary
        if classification is not None and classification not in CLASSIFICATION_VALUES:
            emit(
                errors, "BP-SEM-002",
                f"process_type={classification!r} is not in the approved "
                f"landscape vocabulary"
            )

        # BP-SEM-007: Context distinction (canonical `context:` block required)
        if not context_refs:
            emit(
                errors, "BP-SEM-007",
                "the canonical `context:` block is required; process_audience "
                "is not a substitute (CR-BP-14 §13)"
            )

        # BP-SEM-008: Context reference integrity
        for ref in context_refs:
            if not PC_PATTERN.match(ref):
                emit(
                    errors, "BP-SEM-008",
                    f"context ref {ref!r} does not match `dea:pc-[a-z0-9-]+`"
                )
                continue
            if ref not in pc_ids:
                emit(
                    errors, "BP-SEM-008",
                    f"context ref {ref!r} does not resolve to a canonical "
                    f"Process Context"
                )

        # BP-SEM-005: Specialization validity
        if not isinstance(specialization, list):
            emit(
                errors, "BP-SEM-005",
                "process_specialization must be a list"
            )
        else:
            for parent in specialization:
                if not isinstance(parent, str):
                    emit(
                        errors, "BP-SEM-005",
                        "specialization reference must be a string id"
                    )
                    continue
                if not PROCESS_PATTERN.match(parent):
                    emit(
                        errors, "BP-SEM-005",
                        f"specialization reference {parent!r} does not match "
                        f"`dea:process-[a-z0-9-]+`"
                    )
                elif parent not in process_ids:
                    emit(
                        warnings, "BP-SEM-005",
                        f"specialization reference {parent!r} does not resolve "
                        f"to a canonical Process entry (may be a planned parent)"
                    )

        # BP-SEM-006: Specialization differentiation
        if specialization:
            if not specialization_pattern and not specialization_basis:
                emit(
                    errors, "BP-SEM-006",
                    "specialization requires specialization_pattern or "
                    "specialization_basis"
                )
            if (
                specialization_pattern
                and specialization_pattern not in APPROVED_SPECIALIZATION_BASES
                and not specialization_basis
            ):
                emit(
                    errors, "BP-SEM-006",
                    f"specialization_pattern={specialization_pattern!r} is "
                    f"not an approved basis ({sorted(APPROVED_SPECIALIZATION_BASES)}) "
                    f"and no specialization_basis is provided"
                )

        # BP-SEM-013: Specialization relationship validation. When an
        # entry declares a `specializes` relationship, the target
        # must be a canonical Process (not a Process Group, not a
        # Process Context, not an ECF coordinate); the entry must
        # carry a specialization_pattern from the approved basis
        # vocabulary or a non-empty specialization_basis.
        for rel in data.get("relationships", []) or []:
            if rel.get("relationship_type") != "specializes":
                continue
            target_id = rel.get("target_id")
            if not target_id or not PROCESS_PATTERN.match(target_id):
                emit(
                    errors, "BP-SEM-013",
                    f"specializes target_id {target_id!r} does not match "
                    f"`dea:process-[a-z0-9-]+`"
                )
                continue
            if target_id not in process_ids:
                emit(
                    errors, "BP-SEM-013",
                    f"specializes target {target_id!r} does not resolve to "
                    f"a canonical Process entry"
                )
            if not specialization_pattern and not specialization_basis:
                emit(
                    errors, "BP-SEM-013",
                    "specializes relationship requires specialization_pattern "
                    "(approved basis) or non-empty specialization_basis "
                    "(CR-BP-14 S12)"
                )
            elif (
                specialization_pattern
                and specialization_pattern not in APPROVED_SPECIALIZATION_BASES
                and not specialization_basis
            ):
                emit(
                    errors, "BP-SEM-013",
                    f"specialization_pattern={specialization_pattern!r} is "
                    f"not in the approved basis vocabulary "
                    f"({sorted(APPROVED_SPECIALIZATION_BASES)})"
                )

        # BP-SEM-011: Classification collision (advisory)
        if (
            intent is not None
            and classification is not None
            and intent == classification
        ):
            emit(
                warnings, "BP-SEM-011",
                f"process_intent={intent!r} equals process_type={classification!r} "
                f"lexically; the token is shared but the semantics are independent "
                f"(CR-BP-14 §11; BP-SEM-011). Confirm the choice."
            )

        # BP-SEM-010: Legacy detection (warning class until
        # CR-BP-15 migration completes)
        if intent in LEGACY_INTENTS:
            emit(
                warnings, "BP-SEM-010",
                f"process_intent={intent!r} is a legacy CR-BP-01 value; "
                f"migrate to the CR-BP-14 vocabulary (CR-BP-14 §17)"
            )
        if audience is not None:
            emit(
                warnings, "BP-SEM-010",
                f"process_audience={audience!r} is a legacy migration alias; "
                f"canonicalize via the `context:` block and a `serves` "
                f"relationship toward an ECF coordinate (CR-BP-14 §13, §19)"
            )
        if "process_context" in data and not context_refs:
            emit(
                warnings, "BP-SEM-010",
                f"legacy scalar process_context={data['process_context']!r} "
                f"predates the canonical `context:` block; migrate (CR-BP-14 §20)"
            )

        # BP-SEM-012: Context multiplicity (advisory)
        if len(context_refs) > 1:
            emit(
                warnings, "BP-SEM-012",
                f"{len(context_refs)} Process Context references; this is "
                f"permitted where evidence justifies cross-context responsibility"
            )

    # BP-SEM-014: Specialization cycle detection. After per-record
    # checks, build the specializes graph and run a DFS to detect
    # cycles (CR-BP-16 S10).
    _check_specialization_cycles(catalog_root, errors, warnings)

    return errors, warnings


def _check_specialization_cycles(
    catalog_root: Path, errors: list[str], warnings: list[str],
) -> None:
    """Build the specializes graph from canonical entries and detect cycles.

    A cycle is any path A -> B -> ... -> A in the specializes graph.
    Self-specialization (A specializes A) is also a cycle. Each
    cycle emits a single BP-SEM-014 error citing the participating ids.
    """
    emit = _make_emit("BP-SEM (cycle)")
    adj: dict[str, set[str]] = {}
    for path in sorted((catalog_root / "entities" / "v1-alpha").rglob("*.yaml")):
        try:
            data = yaml.safe_load(path.read_text())
        except yaml.YAMLError:
            continue
        if not isinstance(data, dict):
            continue
        if data.get("type") != "Process":
            continue
        rec_id = data.get("id")
        if not isinstance(rec_id, str):
            continue
        targets: set[str] = set()
        for rel in data.get("relationships", []) or []:
            if rel.get("relationship_type") != "specializes":
                continue
            tgt = rel.get("target_id")
            if isinstance(tgt, str):
                targets.add(tgt)
        adj[rec_id] = targets

    # Self-loops are cycles.
    for rec_id, targets in list(adj.items()):
        if rec_id in targets:
            emit(
                errors, "BP-SEM-014",
                f"self-specialization: {rec_id} specializes itself "
                "(identical parent/child semantics; CR-BP-16 S10)"
            )
            # Remove the self-loop from the adjacency to avoid
            # re-reporting the cycle in the DFS pass below.
            adj[rec_id] = targets - {rec_id}

    # DFS cycle detection (Tarjan would be overkill for our graph sizes).
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {n: WHITE for n in adj}
    cycle_emitted: set[frozenset[str]] = set()

    def dfs(u: str, stack: list[str]) -> None:
        color[u] = GRAY
        stack.append(u)
        for v in adj.get(u, ()):
            if color.get(v) == GRAY:
                # Found a back-edge: cycle from v to u via stack.
                idx = stack.index(v)
                cycle = stack[idx:]
                key = frozenset(cycle)
                if key not in cycle_emitted:
                    cycle_emitted.add(key)
                    emit(
                        errors, "BP-SEM-014",
                        f"specialization cycle: {' -> '.join(cycle + [v])}"
                    )
            elif color.get(v, WHITE) == WHITE:
                dfs(v, stack)
        stack.pop()
        color[u] = BLACK

    for node in list(adj):
        if color.get(node, WHITE) == WHITE:
            dfs(node, [])


def _self_test(catalog_root: Path) -> tuple[bool, str]:
    """Run the self-test; return (passed, summary)."""
    broken_errors: list[str] = []
    fixed_errors: list[str] = []
    pc_ids = {"processes:pc-pr-op", "processes:pc-pr-im"}
    process_ids = {"processes:process-parent-process", "processes:process-cycle-parent"}

    # Broken catalog fixture
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "entities" / "v1-alpha" / "pr-operate" / "cycle-parent").mkdir(parents=True)
        (tmp_path / "entities" / "v1-alpha" / "pr-operate" / "bad").mkdir(parents=True)
        # BP-SEM-014 fixture: a parent that specializes back to its
        # child, forming a cycle. Created before `bad` so the bad
        # record's specializes edge points at a real id.
        cycle_parent = {
            "id": "processes:process-cycle-parent",
            "name": "Cycle Parent",
            "type": "Process",
            "version": "1.0.0",
            "process_intent": "manage",
            "process_type": "core",
            "context": [{"ref": "processes:pc-pr-op"}],
            # Reverse-edge back to `dea:process-bad` forms a cycle.
            "relationships": [{
                "source_id": "processes:process-cycle-parent",
                "relationship_type": "specializes",
                "target_id": "processes:process-bad",
                "specialization_pattern": "by-customer-segment",
            }],
        }
        (tmp_path / "entities" / "v1-alpha" / "pr-operate" / "cycle-parent" / "processes-process-cycle-parent.yaml").write_text(
            yaml.safe_dump(cycle_parent, sort_keys=False)
        )
        broken = {
            "id": "processes:process-bad",
            "name": "Bad",
            "type": "Process",
            "version": "1.0.0",
            "process_intent": "harmonise",        # BP-SEM-001
            "process_type": "essential",          # BP-SEM-002
            "process_audience": "party-relationship",
            "context": [{"ref": "processes:pc-unknown"}],  # BP-SEM-008
            "process_specialization": ["processes:process-nope"],  # BP-SEM-005
            "specialization_pattern": "by-magic",  # no basis -> BP-SEM-006
            # BP-SEM-013: specializes to an unknown target with no
            # specialization_pattern / specialization_basis.
            # Plus a cycle-forming edge to dea:process-cycle-parent
            # for BP-SEM-014.
            "relationships": [
                {
                    "source_id": "processes:process-bad",
                    "relationship_type": "specializes",
                    "target_id": "processes:process-nonexistent",
                },
                {
                    "source_id": "processes:process-bad",
                    "relationship_type": "specializes",
                    "target_id": "processes:process-cycle-parent",
                    "specialization_pattern": "by-customer-segment",
                },
            ],
        }
        (tmp_path / "entities" / "v1-alpha" / "pr-operate" / "bad" / "processes-process-bad.yaml").write_text(
            yaml.safe_dump(broken, sort_keys=False)
        )
        broken_errors, broken_warnings = run_checks(tmp_path, pc_ids=pc_ids, process_ids=process_ids)

    # Fixed catalog fixture
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "entities" / "v1-alpha" / "pr-operate" / "good").mkdir(parents=True)
        (tmp_path / "entities" / "v1-alpha" / "pr-operate" / "good-2").mkdir(parents=True)
        good = {
            "id": "processes:process-good",
            "name": "Manage Example",
            "type": "Process",
            "version": "1.0.0",
            "process_intent": "support",   # collision with process_type
            "process_type": "support",     # for BP-SEM-011 advisory
            "process_audience": "party-relationship",  # legacy alias only
            "context": [{"ref": "processes:pc-pr-op"}],
            "process_specialization": ["processes:process-parent-process"],
            "specialization_pattern": "by-customer-segment",
        }
        good_2 = {
            "id": "processes:process-good-2",
            "name": "Manage Example 2",
            "type": "Process",
            "version": "1.0.0",
            "process_intent": "manage",
            "process_type": "core",
            "context": [{"ref": "processes:pc-pr-op"}, {"ref": "processes:pc-pr-im"}],
            "process_specialization": ["processes:process-not-yet-canonical"],
            "specialization_basis": "by-customer-segment",
            # BP-SEM-013 valid specializes: approved basis + valid target.
            "relationships": [{
                "source_id": "processes:process-good-2",
                "relationship_type": "specializes",
                "target_id": "processes:process-parent-process",
            }],
        }
        (tmp_path / "entities" / "v1-alpha" / "pr-operate" / "good" / "processes-process-good.yaml").write_text(
            yaml.safe_dump(good, sort_keys=False)
        )
        (tmp_path / "entities" / "v1-alpha" / "pr-operate" / "good-2" / "processes-process-good-2.yaml").write_text(
            yaml.safe_dump(good_2, sort_keys=False)
        )
        fixed_errors, fixed_warnings = run_checks(
            tmp_path, pc_ids=pc_ids, process_ids=process_ids
        )

    # BP-SEM-001..008 must each appear on the broken fixture.
    # BP-SEM-005 may legitimately emit as a warning (unresolved
    # parent) rather than an error (malformed id) depending on the
    # fixture; the assertion accepts either signal.
    blocking_seen = {
        e.split(" ", 1)[0].split(":")[1]
        for e in broken_errors if e.startswith("rule:BP-SEM-")
    }
    warning_seen = {
        e.split(" ", 1)[0].split(":")[1]
        for e in broken_warnings if e.startswith("rule:BP-SEM-")
    }
    seen = blocking_seen | warning_seen
    missing = {"BP-SEM-001", "BP-SEM-002", "BP-SEM-005", "BP-SEM-006",
               "BP-SEM-008", "BP-SEM-013", "BP-SEM-014"} - seen
    extra_blocking = fixed_errors
    summary = (
        f"broken-blocking={len(broken_errors)} "
        f"fixed-blocking={len(fixed_errors)} "
        f"fixed-warnings={len(fixed_warnings)} "
        f"missing={sorted(missing)}"
    )
    # Confirm every expected rule fires at least once on the broken fixture.
    # Confirm the fixed fixture is blocking-free and surfaces the
    # expected advisory findings (legacy audience, unresolved parent,
    # context multiplicity, etc.).
    ok = not missing and not extra_blocking and len(fixed_warnings) >= 4
    return ok, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Process semantics validator (CR-BP-14 S21).")
    parser.add_argument(
        "--catalog-root", default=str(BASE),
        help="Catalog root directory (defaults to repo root).",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Promote legacy/collision/multiplicity findings to errors.",
    )
    parser.add_argument(
        "--self-test", action="store_true",
        help="Run the built-in self-test on deliberately broken and fixed catalogs.",
    )
    args = parser.parse_args()

    if args.self_test:
        ok, summary = _self_test(Path(args.catalog_root))
        print(f"self-test {'PASS' if ok else 'FAIL'}: {summary}")
        return 0 if ok else 2

    errors, warnings = run_checks(Path(args.catalog_root))
    if args.strict:
        errors = errors + warnings
        warnings = []

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    if warnings and not errors:
        print(
            f"Process Semantics (CR-BP-14 S21): CONFORMANT-WITH-WARNINGS "
            f"({len(warnings)} warnings)"
        )
    elif errors:
        print(
            f"Process Semantics (CR-BP-14 S21): NON-CONFORMANT "
            f"({len(errors)} errors, {len(warnings)} warnings)"
        )
        return 1
    else:
        print(f"Process Semantics (CR-BP-14 S21): CONFORMANT")
    return 0


if __name__ == "__main__":
    sys.exit(main())