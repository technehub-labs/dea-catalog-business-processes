#!/usr/bin/env python3
"""check_readme_consistency.py - README Drift Gate (CR-BP-114; RDM-001..002).

Rules
-----
RDM-001 (blocking). Every canonical record under entities/v1-alpha/
    must carry a README.md whose content is byte-identical to the
    output of scripts/generate_readmes.py for the current record
    fields. Missing or stale READMEs are findings.

RDM-002 (advisory). A README.md under entities/ that belongs to no
    canonical record and is not a research/ artifact or the
    v1-alpha structural template is an orphan (hygiene signal).

The gate makes record READMEs a generated artifact under CI
enforcement, the same contract as CATALOG.yaml --check
(regenerate_catalog.py). After CR-BP-114, READMEs are never edited
by hand: the entity record is the source of truth, the generator
renders, this gate verifies.

CLI: --strict (advisory findings fail), --json, --self-test.
Exit 0 conformant / 1 non-conformant / 2 usage error / 3 drift (from
the generator's own --check surface, surfaced as RDM-001 findings).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import generate_readmes as gr  # noqa: E402

ENTITIES_ROOT = REPO_ROOT / "entities"


def evaluate(root: Path | None = None) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """Return (blocking, advisory) findings as (rule, message) pairs.

    `root` overrides the entities root (used by --self-test with a
    fixture tree); the generator's ENTITIES_ROOT is patched to match
    for the duration of the call.
    """
    blocking: list[tuple[str, str]] = []
    advisory: list[tuple[str, str]] = []

    orig_entities_root = gr.ENTITIES_ROOT
    entities_root = root or orig_entities_root
    if root is not None:
        gr.ENTITIES_ROOT = root
    try:
        # RDM-001: recompute every record README and diff against disk.
        record_readmes: set[Path] = set()
        for path in gr.resolve_record_paths():
            record = gr.load_record(path)
            if record is None:
                continue
            level = gr.resolve_level(record)
            if level is None:
                continue
            readme_path = gr.resolve_readme_path(path, record.get("id", ""))
            expected = gr.generate_readme(record, level)
            if not expected:
                continue
            record_readmes.add(readme_path.resolve())
            rel = readme_path.relative_to(gr.REPO_ROOT)
            if not readme_path.exists():
                blocking.append(("RDM-001", f"{rel}: missing (run generate_readmes.py --force)"))
                continue
            try:
                on_disk = readme_path.read_text()
            except OSError as exc:
                blocking.append(("RDM-001", f"{rel}: unreadable ({exc})"))
                continue
            if on_disk != expected:
                blocking.append(("RDM-001", f"{rel}: stale (content differs from generator output)"))

        # RDM-002: orphan READMEs (not record-owned, not research/, not the template).
        template = (entities_root / "README.md").resolve()
        for p in sorted(entities_root.rglob("README.md")):
            rp = p.resolve()
            if rp in record_readmes or rp == template:
                continue
            if "/research/" in p.as_posix():
                continue
            try:
                rel = p.relative_to(gr.REPO_ROOT)
            except ValueError:
                rel = p
            advisory.append(("RDM-002", f"{rel}: orphan README (no owning record)"))
    finally:
        gr.ENTITIES_ROOT = orig_entities_root

    return blocking, advisory


def _verdict(blocking: list, advisory: list) -> str:
    if blocking:
        return "NON-CONFORMANT"
    if advisory:
        return "CONFORMANT-WITH-WARNINGS"
    return "CONFORMANT"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("--strict", action="store_true",
                        help="Advisory findings also fail the gate.")
    parser.add_argument("--json", action="store_true", help="JSON output.")
    parser.add_argument("--self-test", action="store_true",
                        help="Run fixture-based self-test and exit.")
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    blocking, advisory = evaluate()
    verdict = _verdict(blocking, advisory)

    if args.json:
        print(json.dumps({
            "gate": "RDM-001..002",
            "verdict": verdict,
            "blocking": [{"rule": r, "message": m} for r, m in blocking],
            "advisory": [{"rule": r, "message": m} for r, m in advisory],
        }, indent=2))
    else:
        print(f"README Consistency (CR-BP-114; RDM-001..002): {verdict}")
        print(f"  {len(blocking)} blocking finding(s); {len(advisory)} advisory.")
        for r, m in blocking[:25]:
            print(f"    [BLOCKING] [{r}] {m}")
        for r, m in advisory[:10]:
            print(f"    [{r}] {m}")
        if len(blocking) > 25:
            print(f"    ... and {len(blocking) - 25} more blocking")
        if len(advisory) > 10:
            print(f"    ... and {len(advisory) - 10} more advisory")

    if blocking:
        return 1
    if advisory and args.strict:
        return 1
    return 0


def _self_test() -> int:
    """Fixture test on a synthetic record tree under the system temp dir."""
    import tempfile
    failures = []

    with tempfile.TemporaryDirectory() as td:
        cell = Path(td) / "entities" / "v1-alpha" / "ao-build"
        rec_dir = cell / "ao-build-m6fmyx"
        rec_dir.mkdir(parents=True)
        rec_yaml = rec_dir / "processes-group-ao-build-m6fmyx.yaml"
        rec_yaml.write_text(
            "id: processes:group-ao-build-m6fmyx\n"
            "type: ProcessGroup\n"
            "name: Build Agent Pool\n"
            "version: 1.0.0\n"
            "lifecycle_status: candidate\n"
        )

        # Monkeypatch roots so the generator sees the fixture tree.
        orig_repo = gr.REPO_ROOT
        gr.REPO_ROOT = Path(td)
        fixture_entities = Path(td) / "entities" / "v1-alpha"
        try:
            # Case 1: README missing -> RDM-001 blocking.
            blocking, _ = evaluate(fixture_entities)
            if not any(r == "RDM-001" and "missing" in m for r, m in blocking):
                failures.append("case1: missing README did not fire RDM-001")

            # Case 2: write exact generator output -> no finding.
            record = gr.load_record(rec_yaml)
            expected = gr.generate_readme(record, "L1")
            (rec_dir / "README.md").write_text(expected)
            blocking, _ = evaluate(fixture_entities)
            if any(r == "RDM-001" for r, _ in blocking):
                failures.append("case2: exact generator output fired RDM-001")

            # Case 3: drift (one byte) -> RDM-001 stale.
            (rec_dir / "README.md").write_text(expected + "\n# drift\n")
            blocking, _ = evaluate(fixture_entities)
            if not any(r == "RDM-001" and "stale" in m for r, m in blocking):
                failures.append("case3: drifted README did not fire RDM-001")

            # Case 4: orphan README -> RDM-002 advisory.
            orphan = cell / "orphan-dir"
            orphan.mkdir()
            (orphan / "README.md").write_text("# orphan\n")
            blocking, advisory = evaluate(fixture_entities)
            if not any(r == "RDM-002" for r, _ in advisory):
                failures.append("case4: orphan README did not fire RDM-002")
            if any("orphan" in m for r, m in blocking):
                failures.append("case4: orphan must be advisory, not blocking")
        finally:
            gr.REPO_ROOT = orig_repo

    if failures:
        print("self-test FAIL:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("self-test PASS: 4 cases (RDM-001 missing/exact/stale, RDM-002 orphan)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
