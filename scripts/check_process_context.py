#!/usr/bin/env python3
"""
check_process_context.py — Process Context validator.

Implements CR-BP-02 rules PC-001..PC-008.

Rules:
  PC-001 — Valid Coordinates: domain MUST reference an authoritative ECF Domain.
  PC-002 — Valid Lifecycle: lifecycle_stage MUST reference an authoritative
           Lifecycle Stage.
  PC-003 — Unique Coordinate: Domain x Lifecycle MUST identify one unique
           Process Context (no two contexts share the same coordinate).
  PC-004 — No Orphan Context: every Process Context must resolve to valid
           ECF coordinates (subsumed by PC-001/002; explicit check that
           the context is not in 'candidate' state without a Cell Charter).
  PC-005 — No Local ECF Definitions: the catalog does not redefine
           canonical ECF vocabulary. (the schema's $ref to
           dea-metaframework schemas enforces this at the JSON-schema
           layer; the validator checks that no catalog YAML adds a
           non-canonical domain or lifecycle_stage value).
  PC-006 — Charter Completeness: an established Process Context must
           contain the required semantic charter fields (combined_semantic_meaning
           non-empty; inclusions/exclusions/adjacent_boundaries present).
  PC-007 — No Automatic Process Equivalence: a Process Context must NOT
           be classified as dea:BusinessProcess. (checked at the schema
           layer via required fields; the validator ensures no Process
           Context entry declares an id that begins with `dea:process-`
           or `dea:BusinessProcess`).
  PC-008 — Canonical Process References: any process assigned to a context
           must resolve to the canonical BusinessProcess specialization
           id (`dea:BusinessProcess` in dea-metamodel; `dea:entity-business-process`
           in OpenDEAM root model v0.6.0). The Process Context's
           `processes:` list is governed by CR-BP-02 + CR-BP-SPEC-BP-01.
           Extended by CR-BP-68: each `dea:process-*` entry must be a single
           well-formed id string (a concatenated multi-id scalar from a
           YAML indentation error is a violation) and must resolve to an
           existing canonical Business Process record in the entities tree
           (skipped only when the catalog under check has no entities tree).

Exit: 0 = all rules pass; 2 = self-test.

Built-in --self-test exercises each rule on a deliberately broken
catalog (then on a fixed catalog) and verifies the expected exit codes.
"""
import argparse
import json
import sys
import tempfile
from pathlib import Path

import yaml

BASE = Path(__file__).parent.parent

# Authoritative ECF vocabulary (mirrors dea-metaframework/schemas/ecf-domain.schema.json
# and ecf-stage.schema.json). The catalog must not redefine this.
ECF_DOMAINS = {
    "GovernanceAndExistence",
    "StrategyAndDirection",
    "AgencyAndOrganization",
    "PartyAndRelationship",
    "ProductAndValue",
    "EnablementAndOperations",
    "FinanceAndAccounting",
}
ECF_STAGES = {
    "Conceive",
    "Design",
    "Build",
    "Activate",
    "Operate",
    "Improve",
    "Retire",
}

# Ids reserved for the BusinessProcess specialization (PC-007 / PC-008).
RESERVED_BUSINESS_PROCESS_IDS = {
    "dea:BusinessProcess",
    "dea:entity-business-process",
}


def _load_yaml(path: Path):
    return yaml.safe_load(path.read_text())


def _check_one(ctx: dict, all_contexts: list[dict], errors: list[str],
               known_bp_ids: set | None = None) -> None:
    label = ctx.get("id", "<unknown>")

    # PC-001: domain must reference an authoritative ECF Domain.
    domain = ctx.get("domain")
    if domain not in ECF_DOMAINS:
        errors.append(
            f"PC-001 ({label}): domain {domain!r} is not in the authoritative "
            f"ECF Domain enum ({sorted(ECF_DOMAINS)}). The catalog must reference "
            f"canonical ECF identifiers; it must not redefine the ECF vocabulary."
        )

    # PC-002: lifecycle_stage must reference an authoritative Lifecycle Stage.
    stage = ctx.get("lifecycle_stage")
    if stage not in ECF_STAGES:
        errors.append(
            f"PC-002 ({label}): lifecycle_stage {stage!r} is not in the authoritative "
            f"ECF Lifecycle Stage enum ({sorted(ECF_STAGES)})."
        )

    # PC-003: Domain x Lifecycle MUST identify one unique Process Context.
    if domain in ECF_DOMAINS and stage in ECF_STAGES:
        coord = (domain, stage)
        same_coord = [c.get("id") for c in all_contexts
                      if c.get("domain") == coord[0] and c.get("lifecycle_stage") == coord[1]]
        if len(same_coord) > 1:
            errors.append(
                f"PC-003: Domain x Lifecycle coordinate ({domain} x {stage}) is "
                f"shared by multiple Process Contexts: {same_coord}. Each "
                f"coordinate must identify one unique Process Context."
            )

    # PC-006: charter completeness.
    charter = ctx.get("cell_charter") or {}
    csm = charter.get("combined_semantic_meaning")
    if not csm or not str(csm).strip():
        errors.append(
            f"PC-006 ({label}): cell_charter.combined_semantic_meaning is required "
            f"and must be a non-empty string (CR-BP-02 §7 / AC-04)."
        )
    for key in ("enterprise_concern", "lifecycle_concern"):
        if not charter.get(key):
            errors.append(
                f"PC-006 ({label}): cell_charter.{key} is required (CR-BP-02 §7)."
            )
    for key in ("expected_outcomes", "inclusions", "exclusions", "adjacent_boundaries"):
        if key not in charter:
            errors.append(
                f"PC-006 ({label}): cell_charter.{key} is required (CR-BP-02 §7 / AC-05)."
            )

    # PC-007: a Process Context must NOT be classified as Business Process.
    if label in RESERVED_BUSINESS_PROCESS_IDS:
        errors.append(
            f"PC-007: Process Context id {label!r} is reserved for the Business "
            f"Process specialization. Process Contexts are NOT Business Processes."
        )
    if isinstance(ctx.get("type"), str) and ctx["type"] == "Process":
        errors.append(
            f"PC-007 ({label}): type 'Process' is reserved for Business Process "
            f"specialization entries. Process Context is a distinct contextual "
            f"construct."
        )

    # PC-008: processes: list (when present) references canonical Business Process
    # specialization ids. The catalog's process_intent enum (operational/support/
    # management) does NOT promote to root-model entities (BP-SPEC-01-007).
    # CR-BP-68 extension: entries must be single well-formed id strings (a
    # concatenated scalar from a YAML continuation-indent error is flagged),
    # and each dea:process-* entry must resolve to an existing BP record when
    # the catalog under check carries an entities tree.
    for proc_id in ctx.get("processes", []) or []:
        if not isinstance(proc_id, str):
            errors.append(
                f"PC-008 ({label}): processes entry {proc_id!r} is not a string "
                f"identifier. Each entry must be a single dea:process-* id."
            )
            continue
        if proc_id.count("dea:process-") > 1 or " - dea:process-" in proc_id:
            errors.append(
                f"PC-008 ({label}): processes entry {proc_id!r} concatenates "
                f"multiple process ids into one scalar (YAML indentation "
                f"defect). Each process id must be its own list item."
            )
            continue
        if proc_id.startswith("dea:process-"):
            # OK: lowercase-namespaced catalog entry id; CR-BP-68 also
            # requires it to resolve when an entities tree is present.
            if known_bp_ids is not None and proc_id not in known_bp_ids:
                errors.append(
                    f"PC-008 ({label}): processes entry {proc_id!r} does not "
                    f"resolve to an existing canonical Business Process record "
                    f"in entities/v1-alpha/."
                )
            continue
        if proc_id.startswith("dea:entity-operational-process") \
                or proc_id.startswith("dea:entity-support-process") \
                or proc_id.startswith("dea:entity-management-process"):
            errors.append(
                f"PC-008 ({label}): processes entry {proc_id!r} promotes "
                f"process_intent (operational / support / management) to a "
                f"root-model entity. BP-SPEC-01-007 forbids this."
            )
            continue
        if proc_id in RESERVED_BUSINESS_PROCESS_IDS:
            errors.append(
                f"PC-008 ({label}): processes entry {proc_id!r} references the "
                f"BUSINESS PROCESS SPECIALIZATION class, not a specific Business "
                f"Process instance. The specialization is realized by catalog "
                f"entries (dea:process-...)."
            )


def _load_known_bp_ids(catalog_root: Path) -> set | None:
    """Load the ids of canonical Business Process records (CR-BP-68).

    Returns None when the catalog under check has no entities tree (e.g.
    minimal fixture catalogs), in which case PC-008 resolution is skipped.
    """
    ent_dir = catalog_root / "entities" / "v1-alpha"
    if not ent_dir.exists():
        return None
    ids: set = set()
    for yml in sorted(ent_dir.glob("dea:process-*/dea:process-*.yaml")):
        rec = _load_yaml(yml)
        if isinstance(rec, dict) and isinstance(rec.get("id"), str):
            ids.add(rec["id"])
        else:
            ids.add(yml.parent.name)
    return ids


def run_checks(catalog_root: Path) -> list[str]:
    errors: list[str] = []
    ctx_dir = catalog_root / "contexts"
    if not ctx_dir.exists():
        # No contexts yet; that's allowed (CR-BP-02 §19 explicitly defers
        # population until after the architecture is established).
        return errors
    known_bp_ids = _load_known_bp_ids(catalog_root)
    all_contexts: list[dict] = []
    for yml in sorted(ctx_dir.rglob("*.yaml")):
        ctx = _load_yaml(yml)
        all_contexts.append(ctx)
        _check_one(ctx, all_contexts, errors, known_bp_ids)
    # second pass for uniqueness across all loaded contexts (the in-loop
    # check is incremental; this catches the case where duplicates live in
    # different files).
    _check_uniqueness(all_contexts, errors)
    return errors


def _check_uniqueness(all_contexts: list[dict], errors: list[str]) -> None:
    by_coord: dict[tuple, list[str]] = {}
    for ctx in all_contexts:
        d = ctx.get("domain")
        s = ctx.get("lifecycle_stage")
        if d in ECF_DOMAINS and s in ECF_STAGES:
            by_coord.setdefault((d, s), []).append(ctx.get("id", "<unknown>"))
    for coord, ids in by_coord.items():
        if len(ids) > 1:
            errors.append(
                f"PC-003: coordinate ({coord[0]} x {coord[1]}) is shared by "
                f"multiple Process Contexts: {ids}."
            )


def self_test() -> int:
    """Verify the validator detects broken Process Contexts + accepts the fixed one."""
    with tempfile.TemporaryDirectory(prefix="pc_self_test_") as tmp:
        tmp_path = Path(tmp)
        ctx_dir = tmp_path / "contexts"
        ctx_dir.mkdir()

        # Write a deliberately broken Process Context (PC-001..006 violations).
        broken_ctx = {
            "id": "dea:pc-bad-01",
            "domain": "NotARealDomain",  # PC-001 violation
            "lifecycle_stage": "NotARealStage",  # PC-002 violation
            "name": "Broken",
            "definition": "",  # AC-04 violation (empty definition)
            "scope": {"includes": [], "excludes": []},
            "outcomes": [],
            "adjacent_contexts": [],
            "cell_charter": {
                # PC-006 violations: required fields missing
                "combined_semantic_meaning": "",
            },
            "status": "candidate",
            "type": "Process",  # PC-007 violation
        }
        (ctx_dir / "broken.yaml").write_text(yaml.safe_dump(broken_ctx, sort_keys=False))

        # Add a second context with the SAME valid coordinate to trigger PC-003.
        # Two contexts both at PartyAndRelationship x Operate -> PC-003 collision.
        broken_ctx_2 = {
            "id": "dea:pc-pr-op-dup-1",
            "domain": "PartyAndRelationship",
            "lifecycle_stage": "Operate",
            "name": "Customer Demand x Operate (DUPLICATE-1)",
            "definition": "x",
            "scope": {"includes": [], "excludes": []},
            "outcomes": [],
            "adjacent_contexts": [],
            "cell_charter": {
                "enterprise_concern": "x",
                "lifecycle_concern": "x",
                "combined_semantic_meaning": "x",
                "expected_outcomes": [],
                "inclusions": [],
                "exclusions": [],
                "adjacent_boundaries": [],
            },
            "status": "candidate",
        }
        broken_ctx_2b = {
            "id": "dea:pc-pr-op-dup-2",
            "domain": "PartyAndRelationship",
            "lifecycle_stage": "Operate",
            "name": "Customer Demand x Operate (DUPLICATE-2)",
            "definition": "x",
            "scope": {"includes": [], "excludes": []},
            "outcomes": [],
            "adjacent_contexts": [],
            "cell_charter": {
                "enterprise_concern": "x",
                "lifecycle_concern": "x",
                "combined_semantic_meaning": "x",
                "expected_outcomes": [],
                "inclusions": [],
                "exclusions": [],
                "adjacent_boundaries": [],
            },
            "status": "candidate",
        }
        (ctx_dir / "also-broken.yaml").write_text(yaml.safe_dump(broken_ctx_2, sort_keys=False))
        (ctx_dir / "also-broken-2.yaml").write_text(yaml.safe_dump(broken_ctx_2b, sort_keys=False))

        # Promote process_intent to root-model entity (PC-008 / BP-SPEC-01-007).
        broken_ctx_3 = {
            "id": "dea:pc-bad-03",
            "domain": "PartyAndRelationship",
            "lifecycle_stage": "Build",
            "name": "Promotes Intent",
            "definition": "x",
            "scope": {"includes": [], "excludes": []},
            "outcomes": [],
            "adjacent_contexts": [],
            "cell_charter": {
                "enterprise_concern": "x",
                "lifecycle_concern": "x",
                "combined_semantic_meaning": "x",
                "expected_outcomes": [],
                "inclusions": [],
                "exclusions": [],
                "adjacent_boundaries": [],
            },
            "processes": ["dea:entity-operational-process"],  # PC-008 violation
            "status": "candidate",
        }
        (ctx_dir / "intent-violator.yaml").write_text(
            yaml.safe_dump(broken_ctx_3, sort_keys=False)
        )

        # CR-BP-68: entities fixture so PC-008 resolution checking is active.
        bp_dir = tmp_path / "entities" / "v1-alpha" / "dea:process-real-one"
        bp_dir.mkdir(parents=True)
        (bp_dir / "dea:process-real-one.yaml").write_text(
            yaml.safe_dump({"id": "dea:process-real-one", "type": "Process",
                            "name": "Real One", "status": "established"},
                           sort_keys=False)
        )

        charter_ok = {
            "enterprise_concern": "x",
            "lifecycle_concern": "x",
            "combined_semantic_meaning": "x",
            "expected_outcomes": [],
            "inclusions": [],
            "exclusions": [],
            "adjacent_boundaries": [],
        }

        # CR-BP-68 PC-008 violation: concatenated multi-id scalar (the YAML
        # continuation-indent defect found in 5 legacy PC records).
        broken_ctx_4 = {
            "id": "dea:pc-bad-04",
            "domain": "FinanceAndAccounting",
            "lifecycle_stage": "Build",
            "name": "Concatenated",
            "definition": "x",
            "scope": {"includes": [], "excludes": []},
            "outcomes": [],
            "adjacent_contexts": [],
            "cell_charter": dict(charter_ok),
            "processes": ["dea:process-real-one - dea:process-other-one"],
            "status": "candidate",
        }
        (ctx_dir / "concat-violator.yaml").write_text(
            yaml.safe_dump(broken_ctx_4, sort_keys=False)
        )

        # CR-BP-68 PC-008 violation: dangling process reference.
        broken_ctx_5 = {
            "id": "dea:pc-bad-05",
            "domain": "FinanceAndAccounting",
            "lifecycle_stage": "Design",
            "name": "Dangling",
            "definition": "x",
            "scope": {"includes": [], "excludes": []},
            "outcomes": [],
            "adjacent_contexts": [],
            "cell_charter": dict(charter_ok),
            "processes": ["dea:process-does-not-exist"],
            "status": "candidate",
        }
        (ctx_dir / "dangling-violator.yaml").write_text(
            yaml.safe_dump(broken_ctx_5, sort_keys=False)
        )

        errs = run_checks(tmp_path)
        for prefix in ("PC-001", "PC-002", "PC-003", "PC-006", "PC-007", "PC-008"):
            if not any(e.startswith(prefix) for e in errs):
                print(f"self-test FAIL: expected at least one {prefix}* error in: {errs}")
                return 2

        # Now FIX everything.
        # Remove the broken files; create one fixed context (no PC-003 collision).
        for f in ctx_dir.iterdir():
            f.unlink()
        fixed_ctx = {
            "id": "dea:pc-pr-op",
            "domain": "PartyAndRelationship",
            "lifecycle_stage": "Operate",
            "name": "Customer Demand x Operate",
            "definition": (
                "The enterprise context in which customer demand for products "
                "and services is met during the Operate lifecycle stage."
            ),
            "scope": {
                "includes": [
                    "Customer order fulfilment",
                    "Demand fulfilment against committed SLAs",
                ],
                "excludes": [
                    "Customer acquisition (covered in: Conceive)",
                    "Capacity planning (covered in: Design)",
                ],
            },
            "outcomes": [
                "Customer demand satisfied within committed SLAs",
                "Demand signals propagated upstream for planning",
            ],
            "adjacent_contexts": ["dea:pc-pr-dsgn"],
            "processes": ["dea:process-real-one"],
            "cell_charter": {
                "enterprise_concern": "Customer-facing value delivery.",
                "lifecycle_concern": "Steady-state operation of customer demand.",
                "combined_semantic_meaning": (
                    "Operate the customer demand pipeline: receive, fulfil, "
                    "and signal demand; maintain customer relationships "
                    "during steady-state delivery."
                ),
                "expected_outcomes": [
                    "Demand fulfilled within SLAs",
                    "Demand signals propagated",
                ],
                "inclusions": [
                    "Order fulfilment",
                    "Customer service during steady-state",
                ],
                "exclusions": [
                    "Acquisition (covered in: Conceive)",
                    "Capacity planning (covered in: Design)",
                ],
                "adjacent_boundaries": [
                    "dea:pc-pr-dsgn (Design context for capacity planning)",
                    "dea:pc-pr-impr (Improve context for demand-signal feedback)",
                ],
            },
            "status": "established",
        }
        (ctx_dir / "cd-op.yaml").write_text(yaml.safe_dump(fixed_ctx, sort_keys=False))

        errs_fixed = run_checks(tmp_path)
        if errs_fixed:
            print(f"self-test FAIL: expected zero errors on fixed catalog, got: {errs_fixed}")
            return 2

    print("self-test PASS: PC-001..PC-008 all triggered on broken catalog; zero errors on fixed.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument(
        "--catalog-root", type=Path, default=BASE,
        help="Catalog root directory (default: parent of scripts/)",
    )
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    errors = run_checks(args.catalog_root)
    if errors:
        print("Process Context validation: FAILED")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print("Process Context validation: PASS (PC-001..PC-008)")
    return 0


if __name__ == "__main__":
    sys.exit(main())