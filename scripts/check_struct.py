#!/usr/bin/env python3
"""
check_struct.py: STRUCT conformance check for top-level directory
shape (CR-BP-15-IMP Phase 1, decision D6).

Walks the repository root and asserts that every top-level entry is
either a known directory / file or an explicitly enumerated "extra".
Unknown top-level entries are reported so the reconciliation gate
never silently lets a typo (e.g. `reconcilliation/`) shadow a real
directory.

This check is intentionally permissive: the catalogue's contracts
(schema, validators, regenerator) own structural integrity; STRUCT only
guards against accidental mis-spellings of recognised directories.

Authoritative reference: CR-BP-15-IMP /2.3 (decision D6).

Usage:
  python scripts/check_struct.py [--self-test] [--strict]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Top-level entries the catalogue always recognises. Additions must be
# deliberate; consult CR-BP-15-IMP /2.3 (decision D6) before adding.
KNOWN_TOP_LEVEL: frozenset[str] = frozenset({
    # Catalogue code / data
    "catalog-index-schema",
    "change-requests",
    "classifications",
    "contexts",
    "contributions",
    # Lifecycle process-discovery records (CR-BP-62 S17; populated by CR-BP-63)
    "discovery",
    "docs",
    "entities",
    "schemas",
    "scripts",
    "tests",
    "tools",
    "utils",
    "validation",
    # Reconciliation / governance scaffolding (CR-BP-15-IMP)
    "reconciliation",
    "reports",
    # Repo plumbing
    ".github",
    "CHANGELOG.md",
    "NOTICE",
    "CATALOG.yaml",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "TEMPLATE_VERSION",
    "docs.governance.md",
    "metamodel-pointer.yaml",
    # PR plan workspace (dev only; PR body files live here
    # between `git add -A -- ':!01_plan'` and the merge).
    "01_plan",
})


def _extras(root: Path) -> list[str]:
    out: list[str] = []
    for entry in sorted(root.iterdir()):
        if entry.name in KNOWN_TOP_LEVEL:
            continue
        # Accept conventional hidden / tooling entries (git, gitignore,
        # pytest cache, etc.). Listed explicitly to avoid surprises when
        # new tooling appears.
        if entry.name in {".git", ".gitignore", ".gitattributes",
                          ".editorconfig", ".pytest_cache", ".venv",
                          "__pycache__", ".vscode"}:
            continue
        if entry.name.startswith(".") and not entry.name.startswith(".github"):
            out.append(entry.name + "  (hidden; review before commit)")
            continue
        out.append(entry.name)
    return out


def check_struct(root: Path) -> list[str]:
    return _extras(root)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--self-test", action="store_true",
                   help="Run against a tmp dir; assert no extras are reported.")
    p.add_argument("--strict", action="store_true",
                   help="Treat any extras as errors (default: warnings only).")
    p.add_argument("--root", type=Path, default=None,
                   help="Repository root to scan (default: the script's REPO_ROOT).")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args(argv)

    if args.self_test:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            for known in KNOWN_TOP_LEVEL:
                if known.startswith("."):
                    (tmp_path / known).mkdir(parents=True, exist_ok=True)
                elif "." in known:
                    # recognised file (e.g. README.md, CATALOG.yaml)
                    (tmp_path / known).write_text("")
                else:
                    (tmp_path / known).mkdir(parents=True, exist_ok=True)
            extras = _extras(tmp_path)
            if extras:
                print(f"self-test FAIL: extras reported on clean tmp dir: {extras}",
                      file=sys.stderr)
                return 2
            # Now add an unrecognised dir; expect one extra
            (tmp_path / "reconcilliation").mkdir()
            extras = _extras(tmp_path)
            if "reconcilliation" not in extras:
                print("self-test FAIL: did not detect 'reconcilliation' as an extra",
                      file=sys.stderr)
                return 2
            if not args.quiet:
                print("self-test PASS: STRUCT check detects unrecognised top-level entries")
            return 0

    extras = check_struct(args.root.resolve() if args.root else REPO_ROOT)
    if extras:
        for e in extras:
            print(f"STRUCT-WARN: unrecognised top-level entry: {e}",
                  file=sys.stderr)
        if args.strict:
            print("STRUCT-FAIL: --strict; exiting 1", file=sys.stderr)
            return 1
        print(f"STRUCT-OK: {len(extras)} unrecognised top-level entries (warnings only)",
                  file=sys.stderr)
        return 0
    if not args.quiet:
        print("STRUCT-OK: no unrecognised top-level entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
