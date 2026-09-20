#!/usr/bin/env python3
"""check_register_audit.py: Validate the CR-BP-22 audit_status axis in the
research register against the canonical catalog.

The register (research/l1-register.yaml) and the catalog (entities/v1-alpha/)
are two views on the same set of L1 Process Group facts. CR-BP-22 introduces
an `audit_status` axis that must agree with the catalog at every coordinate.

Audit logic:
  disposition=ratified-accepted AND landed_count>=1 -> audit_status=landed
  disposition=ratified-accepted AND landed_count=0  -> audit_status=ratified-pending-landing
  disposition=backlog-deferred                       -> audit_status=backlog-deferred

Landed means: at least one canonical `dea:group-<...>` record in
entities/v1-alpha/ whose `process_context` resolves to the coordinate's
`dea:pc-<...>` id.

Run: python scripts/check_register_audit.py
Exit: 0 = all coordinates pass; 1 = at least one coordinate disagrees.

Authoritative reference: CR-BP-22.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTITIES_DIR = REPO_ROOT / "entities/v1-alpha"
REGISTER_PATH = ENTITIES_DIR / "pr-operate/pr-operate-7ab3ma/research/l1-register.yaml"
UNIVERSE_PATH = ENTITIES_DIR / "pr-operate/pr-operate-7ab3ma/research/l1-candidate-universe.yaml"

DOMAIN_ABBR = {
    "ge": "GovernanceAndExistence",
    "sd": "StrategyAndDirection",
    "ao": "AgencyAndOrganization",
    "pr": "PartyAndRelationship",
    "pv": "ProductAndValue",
    "oe": "EnablementAndOperations",
    "fa": "FinanceAndAccounting",
}


def _parse_stage(s: str) -> str:
    if s in ("c", "conceive"):
        return "Conceive"
    if s in ("d", "design"):
        return "Design"
    if s in ("b", "build"):
        return "Build"
    if s in ("a", "activate"):
        return "Activate"
    if s in ("o", "op", "operate"):
        return "Operate"
    if s in ("im", "i", "improve"):
        return "Improve"
    if s in ("r", "retire"):
        return "Retire"
    return s


def _collect_landed() -> dict[tuple[str, str], list[str]]:
    """Walk entities/v1-alpha/*/dea:group-*.yaml and group by (domain, stage)."""
    landed: dict[tuple[str, str], list[str]] = {}
    for entry in sorted(ENTITIES_DIR.iterdir()):
        if not entry.name.startswith("processes:group-"):
            continue
        fpath = entry / f"{entry.name}.yaml"
        if not fpath.exists():
            continue
        with fpath.open() as f:
            doc = yaml.safe_load(f)
        pc = doc.get("process_context", "")
        m = re.match(r"processes:pc-([a-z]+)-(.+)", pc)
        if not m:
            continue
        dom = DOMAIN_ABBR.get(m.group(1), "?")
        st = _parse_stage(m.group(2))
        landed.setdefault((dom, st), []).append(entry.name)
    return landed


def _expected_audit(disposition: str, landed_count: int) -> str:
    if disposition == "ratified-accepted":
        return "landed" if landed_count >= 1 else "ratified-pending-landing"
    if disposition == "backlog-deferred":
        return "backlog-deferred"
    return disposition


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 if audit_status is missing on any coordinate")
    parser.add_argument("--self-test", action="store_true",
                        help="exercise the audit on a synthetic register")
    parser.add_argument("--no-recursion", action="store_true",
                        help=argparse.SUPPRESS)  # internal guard against self-test recursion
    args = parser.parse_args(list(argv) if argv else None)

    if args.self_test and not args.no_recursion:
        return _self_test()

    if not REGISTER_PATH.exists():
        print(f"register not found: {REGISTER_PATH}", file=sys.stderr)
        return 1

    with REGISTER_PATH.open() as f:
        reg = yaml.safe_load(f)

    landed = _collect_landed()

    failures: list[str] = []
    counts = {"landed": 0, "ratified-pending-landing": 0, "backlog-deferred": 0}
    missing: list[str] = []

    for dom, stages in reg["register"].items():
        for st, payload in stages.items():
            disposition = payload.get("disposition", "?")
            landed_count = len(landed.get((dom, st), []))
            expected = _expected_audit(disposition, landed_count)
            actual = payload.get("audit_status")
            counts[expected] += 1
            if actual is None:
                missing.append(f"({dom}, {st})")
                if args.strict:
                    failures.append(f"{dom} x {st}: missing audit_status")
            elif actual != expected:
                failures.append(
                    f"{dom} x {st}: disposition={disposition} landed={landed_count} "
                    f"expected audit_status={expected} got {actual}"
                )

    print("CR-BP-22 audit reconciliation:")
    print(f"  landed:                   {counts['landed']}")
    print(f"  ratified-pending-landing: {counts['ratified-pending-landing']}")
    print(f"  backlog-deferred:         {counts['backlog-deferred']}")
    print(f"  total:                    {sum(counts.values())}")
    print()

    if missing:
        print(f"Coordinates missing audit_status: {len(missing)}")
    if failures:
        print(f"\nFAILURES ({len(failures)}):")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("OK: audit_status agrees with catalog reality.")
    return 0


def _self_test() -> int:
    """Exercise the audit on a fixed-pair register + catalog (one disagreement)."""
    import tempfile
    import textwrap

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        ent = td / "entities"
        ent_a = ent / "processes:group-foo"
        ent_a.mkdir(parents=True)
        (ent_a / "processes:group-foo.yaml").write_text(textwrap.dedent("""
            id: dea:group-foo
            process_context: dea:pc-ge-build
        """))

        # patch module globals for the test
        global ENTITIES_DIR, REGISTER_PATH
        ENTITIES_DIR = ent
        REGISTER_PATH = ent / "l1-register.yaml"
        (ent / "l1-register.yaml").write_text(textwrap.dedent("""
            register:
              GovernanceAndExistence:
                Build:
                  process_context: dea:pc-ge-build
                  disposition: ratified-accepted
                  audit_status: landed
                Conceive:
                  process_context: dea:pc-ge-conceive
                  disposition: ratified-accepted
                  audit_status: ratified-pending-landing
                Activate:
                  process_context: dea:pc-ge-activate
                  disposition: backlog-deferred
                  audit_status: backlog-deferred
        """))

        rc = main(["--no-recursion"])
        if rc != 0:
            print("self-test: expected rc=0 got rc=" + str(rc))
            return 2
        print("self-test: PASS")
        return 0


if __name__ == "__main__":
    sys.exit(main())