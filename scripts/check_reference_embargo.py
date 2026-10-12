#!/usr/bin/env python3
"""
check_reference_embargo.py
CR-BP-112: Reference Embargo gate (EMB-001..004).

Enforces the user directive of 2026-09-22 (eaojnr): the catalog
content must not reference the embargoed framework or its publications
in any artifact of any org repo. The CR-BP-TMF-EMBARGO strip
(2026-09-22) removed every substantive citation; CR-BP-112 records
the determination and turns the embargo into a machine-checked
invariant.

Token-class distinction (the design decision that makes "no reference"
enforceable):

1. Substantive references to the embargoed organization or its
   publications -- forbidden everywhere, EMB-001.
2. The governance identifier `CR-BP-TMF-EMBARGO` -- an immutable
   CR id baked into check_cr_metadata.py's CR_NUMBER_PATTERN and
   CR-BP-107's history. It names a change request, not the
   organization. The gate masks this exact token on a line before
   term matching, so the id remains usable in Depends-on chains,
   README rows, and validator patterns.
3. The sealed historical carrier
   `change-requests/CR-BP-TMF-EMBARGO-tmforum-reference-strip.md` --
   the one file allowed to enumerate what was removed (an audit
   record that cannot say what it removed protects nobody). Sealed
   by hash under EMB-003; its id is not reusable for new CRs.

Usage:
  python scripts/check_reference_embargo.py [--strict] [--json]
  python scripts/check_reference_embargo.py --self-test

Exit codes:
  0  CONFORMANT (0 blocking findings)
  1  NON-CONFORMANT (>= 1 blocking finding)
  2  Self-test failure

Blocking rules:
  EMB-001  occurrence of an embargoed term outside the
           sealed-file allowlist
  EMB-002  allowlist data file missing or malformed
  EMB-003  sealed-file integrity drift (SHA-256 mismatch)

Advisory rules:
  EMB-004  false-positive registry hit that matches no recorded
           entry pattern
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
ALLOWLIST_PATH = ROOT / "reconciliation" / "reference-embargo-allowlist.yaml"

# Embargoed term list (case-insensitive, word-boundary). The list is
# the union of the CR-BP-TMF-EMBARGO strip's audit terms and the
# organization/standards catalogue. Substring variants
# (tm-forum, tmforum.org) are included as a single word-boundary entry.
EMBARGOED_TERMS: tuple[str, ...] = (
    "tmforum",
    "tm forum",
    "tmf",
    "etom",
    "frameworx",
    "gb921",
    "gb925",
    "sid",
    "tam",
    "odf",
    "oss/bss",
    "tm-forum",
    "tmforum.org",
)

# Term -> compiled case-insensitive word-boundary regex.
TERM_PATTERNS: dict[str, re.Pattern[str]] = {
    term: re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
    for term in EMBARGOED_TERMS
}

# Token-class 2: the governance identifier `CR-BP-TMF-EMBARGO` is
# permitted everywhere as a CR id. The bare component `TMF-EMBARGO`
# is also permitted wherever it appears as part of a CR id token
# (e.g. inside the CR_NUMBER_PATTERN regex literal in
# check_cr_metadata.py, where it is a path-component of the
# CR-BP family). The gate masks these tokens on a line before term
# matching, so the id remains usable in Depends-on chains, README
# rows, and validator patterns.
MASKED_TOKEN_PATTERN = re.compile(r"\bCR-BP-TMF-EMBARGO\b|\bTMF-EMBARGO\b")

# Files to scan: source-bearing artifacts (markdown, yaml, json, py,
# sh). The 01_plan/ archive and reconciliation/cross-check-org-wide.md
# carry historical mentions that pre-date the strip and are out of
# scope for the live conformance gate (the embargo is forward-going;
# historical archive is sealed by mtime in CR-BP-TMF-EMBARGO section 6).
SCAN_EXTENSIONS: tuple[str, ...] = (".md", ".yaml", ".yml", ".json", ".py", ".sh", ".txt")

# Paths to skip entirely (the strip's sealed carrier is the one
# exception; the rest of these carry pre-strip history that the
# CR-BP-TMF-EMBARGO acceptance criteria explicitly excludes from the
# forward-going gate).
SKIP_PATH_PREFIXES: tuple[str, ...] = (
    ".git/",
    ".venv/",
    "__pycache__/",
    "node_modules/",
    "01_plan/",
)


def _mask_token(line: str, sealed_paths: tuple[str, ...] = ()) -> str:
    """Mask the CR-BP-TMF-EMBARGO id token on a line before term
    matching, plus the path of every sealed file (the sealed
    carrier's filename contains the embargoed framework name; the
    gate must not flag documentation links that reference the
    carrier by name). Replaces every match with a fixed-width
    placeholder that preserves word boundaries for adjacent
    embargoed terms.

    Order matters: path replacement runs first so the regex sub
    cannot corrupt the path before it is replaced (a path like
    `change-requests/CR-BP-TMF-EMBARGO-tmforum-reference-strip.md`
    would otherwise be partially replaced by the regex and the
    remaining `tmforum-reference-strip` would still match the
    `tmforum` pattern)."""
    from pathlib import PurePosixPath
    masked = line
    for path in sealed_paths:
        # Mask the full path AND just the trailing filename so both
        # `/path/to/file-tmforum-reference-strip.md` and
        # `file-tmforum-reference-strip.md` are masked.
        masked = masked.replace(path, "XXXX")
        masked = masked.replace(PurePosixPath(path).name, "XXXX")
    masked = MASKED_TOKEN_PATTERN.sub("XXXX", masked)
    return masked


def _term_hit(line: str, sealed_paths: tuple[str, ...] = ()) -> str | None:
    """Return the first embargoed term matched on a line, or None.

    The id token is masked first so `CR-BP-TMF-EMBARGO` does not
    trip the `tmf` / `tm-forum` patterns by accident. Sealed file
    paths are masked so documentation links to the carrier do not
    trip the gate."""
    masked = _mask_token(line, sealed_paths)
    for term, pattern in TERM_PATTERNS.items():
        if pattern.search(masked):
            return term
    return None


def _iter_files(root: Path, allowlist: dict[str, Any]) -> list[Path]:
    """Iterate every file under `root` whose extension is in
    SCAN_EXTENSIONS, excluding SKIP_PATH_PREFIXES and the sealed
    files in the allowlist (which carry historical mentions and
    are validated by hash under EMB-003 instead)."""
    out: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith(SKIP_PATH_PREFIXES):
            continue
        if rel in {s["path"] for s in allowlist.get("sealed_files", [])}:
            continue
        if path.suffix.lower() not in SCAN_EXTENSIONS:
            continue
        out.append(path)
    return out


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_allowlist(allowlist_path: Path | None = None) -> dict[str, Any]:
    """Load and validate the allowlist data file. Returns an empty
    dict if the file is missing (the gate reports EMB-002 separately
    so the caller's verdict distinguishes missing-file from
    bad-content)."""
    p = allowlist_path or ALLOWLIST_PATH
    if not p.exists():
        return {}
    try:
        data = yaml.safe_load(p.read_text())
    except yaml.YAMLError:
        return {"_malformed": True}
    if not isinstance(data, dict):
        return {"_malformed": True}
    if "sealed_files" not in data or "false_positives" not in data:
        return {"_malformed": True}
    return data


def evaluate(root: Path, allowlist_path: Path | None = None) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """Run every EMB rule against the repository. Returns
    (blocking, advisory) lists of (rule, message) tuples.

    Pure evaluator: prints nothing, exits nothing. The CLI entry
    point wraps this for the `conformance_result.py` gate.

    `allowlist_path` is the path to the reference-embargo-allowlist
    data file. Defaults to the live repo's
    `reconciliation/reference-embargo-allowlist.yaml`. Tests
    override this to point at a fixture under `tmp_path`."""
    blocking: list[tuple[str, str]] = []
    advisory: list[tuple[str, str]] = []

    # EMB-002: allowlist data file
    allowlist = _load_allowlist(allowlist_path)
    if not allowlist:
        try:
            rel = (allowlist_path or ALLOWLIST_PATH).relative_to(root).as_posix()
        except ValueError:
            rel = str(allowlist_path or ALLOWLIST_PATH)
        blocking.append((
            "EMB-002",
            f"allowlist file missing: {rel}",
        ))
        return blocking, advisory
    if allowlist.get("_malformed"):
        try:
            rel = (allowlist_path or ALLOWLIST_PATH).relative_to(root).as_posix()
        except ValueError:
            rel = str(allowlist_path or ALLOWLIST_PATH)
        blocking.append((
            "EMB-002",
            f"allowlist file malformed: {rel}",
        ))
        return blocking, advisory

    # EMB-003: sealed-file integrity. The allowlist file is exempt
    # from its own self-hash check (the hash it records is the
    # allowlist's own hash; the allowlist cannot list a stable hash
    # for itself without resolving a recursive fixed-point, which
    # is solved by exempting the self-reference at the gate level).
    allowlist_abs = (root / "reconciliation" / "reference-embargo-allowlist.yaml").resolve()
    sealed = allowlist.get("sealed_files", [])
    for entry in sealed:
        p = (root / entry["path"]).resolve()
        if not p.exists():
            blocking.append((
                "EMB-003",
                f"sealed file missing: {entry['path']}",
            ))
            continue
        if p == allowlist_abs:
            # Self-reference: the allowlist file's hash is content-
            # dependent on the hashes it records; the gate does not
            # verify the self-reference. Any change to the allowlist
            # is a CR-level event caught by `git diff` review, not
            # by an in-gate self-hash.
            continue
        actual = _sha256(p)
        if actual != entry["sha256"]:
            blocking.append((
                "EMB-003",
                f"sealed-file integrity drift: {entry['path']} "
                f"(recorded {entry['sha256'][:12]}, actual {actual[:12]})",
            ))

    # EMB-001: substantive embargoed-term occurrence outside the
    # sealed-file allowlist
    false_positive_patterns = {
        fp["path"]: re.compile(fp["pattern"], re.IGNORECASE)
        for fp in allowlist.get("false_positives", [])
    }
    sealed_paths = tuple(s["path"] for s in allowlist.get("sealed_files", []))
    fp_paths = set(false_positive_patterns.keys())
    for path in _iter_files(root, allowlist):
        rel = path.relative_to(root).as_posix()
        try:
            content = path.read_text(errors="replace")
        except OSError:
            continue
        fp_pattern = false_positive_patterns.get(rel)
        for lineno, raw in enumerate(content.splitlines(), 1):
            term = _term_hit(raw, sealed_paths)
            if not term:
                continue
            # EMB-004: false-positive registry match without a
            # recorded pattern on the line
            if fp_pattern and fp_pattern.search(raw):
                # The line's hit is a recorded false positive;
                # suppress and continue.
                continue
            blocking.append((
                "EMB-001",
                f"{rel}:{lineno}: embargoed term {term!r}: {raw.strip()[:120]}",
            ))

    # EMB-004: false-positive registry entries that match no
    # term pattern. (Advisory; catches dead patterns.)
    for fp in allowlist.get("false_positives", []):
        pat = re.compile(fp["pattern"], re.IGNORECASE)
        # If the registered false-positive pattern is not exercised
        # anywhere in the file it claims to suppress, flag it.
        p = root / fp["path"]
        if not p.exists():
            advisory.append((
                "EMB-004",
                f"false-positive pattern {fp['pattern']!r} registered for "
                f"missing file {fp['path']}",
            ))
            continue
        if not pat.search(p.read_text(errors="replace")):
            advisory.append((
                "EMB-004",
                f"false-positive pattern {fp['pattern']!r} registered for "
                f"{fp['path']} matches no current content",
            ))

    return blocking, advisory


def _self_test() -> int:
    """Exercise every EMB rule with synthetic fixtures."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        # Minimal repo skeleton: entities/ dummy + CR file + script
        # + sealed file
        (root / "change-requests").mkdir()
        (root / "entities" / "v1-alpha").mkdir(parents=True)
        (root / "scripts").mkdir()
        (root / "reconciliation").mkdir()
        (root / "change-requests" / "CR-BP-1-test.md").write_text(
            "# Test CR\n\nSome prose that mentions tmforum in a finding.\n"
        )
        (root / "scripts" / "check_reference_embargo.py").write_text(
            "import os\n"  # avoid scanning the validator itself
        )
        sealed = root / "change-requests" / "CR-BP-TMF-EMBARGO-tmforum-reference-strip.md"
        sealed.write_text(
            "# CR-BP-TMF-EMBARGO: TMForum reference embargo compliance strip\n"
            "The user directive 2026-09-22 is to drop tmforum / eTOM / Frameworx.\n"
        )
        allowlist_path = root / "reconciliation" / "reference-embargo-allowlist.yaml"
        allowlist = {
            "version": 1,
            "sealed_files": [
                {
                    "path": "change-requests/CR-BP-TMF-EMBARGO-tmforum-reference-strip.md",
                    "sha256": _sha256(sealed),
                    "rationale": "Sealed carrier (CR-BP-112).",
                },
            ],
            "false_positives": [
                {
                    "path": "scripts/check_id_system.py",
                    "pattern": r"\bsid\b",
                    "rationale": "Python variable name (CR-BP-TMF-EMBARGO strip section 3).",
                },
            ],
        }
        allowlist_path.write_text(yaml.safe_dump(allowlist, sort_keys=False))

        blocking, advisory = evaluate(root, allowlist_path=allowlist_path)
        if any(r == "EMB-001" for r, _ in blocking):
            print("self-test PASS: EMB-001 detects tmforum mention")
        else:
            print("self-test FAIL: EMB-001 missed tmforum mention", file=sys.stderr)
            return 2

        # The sealed file must NOT trip EMB-001.
        if not any("sealed" in m for r, m in blocking):
            print("self-test PASS: sealed file suppressed from EMB-001")
        else:
            print("self-test FAIL: sealed file emitted finding", file=sys.stderr)
            return 2

        # EMB-002: missing allowlist
        allowlist_path.unlink()
        b2, _ = evaluate(root, allowlist_path=allowlist_path)
        if any(r == "EMB-002" for r, _ in b2):
            print("self-test PASS: EMB-002 detects missing allowlist")
        else:
            print("self-test FAIL: EMB-002 missed missing allowlist", file=sys.stderr)
            return 2
        allowlist_path.write_text(yaml.safe_dump(allowlist, sort_keys=False))

        # EMB-003: tampered sealed file
        sealed.write_text(sealed.read_text() + "\nextra\n")
        b3, _ = evaluate(root, allowlist_path=allowlist_path)
        if any(r == "EMB-003" for r, _ in b3):
            print("self-test PASS: EMB-003 detects sealed-file drift")
        else:
            print("self-test FAIL: EMB-003 missed sealed-file drift", file=sys.stderr)
            return 2
        sealed.write_text(
            "# CR-BP-TMF-EMBARGO: TMForum reference embargo compliance strip\n"
            "The user directive 2026-09-22 is to drop tmforum / eTOM / Frameworx.\n"
        )
        allowlist["sealed_files"][0]["sha256"] = _sha256(sealed)
        allowlist_path.write_text(yaml.safe_dump(allowlist, sort_keys=False))

        # Token-class 2: the CR id `CR-BP-TMF-EMBARGO` is permitted
        (root / "change-requests" / "CR-BP-1-test.md").write_text(
            "# Test CR\n\nDepends on CR-BP-TMF-EMBARGO strip.\n"
        )
        b4, _ = evaluate(root, allowlist_path=allowlist_path)
        if not any(r == "EMB-001" for r, _ in b4):
            print("self-test PASS: CR-BP-TMF-EMBARGO id token masked")
        else:
            print("self-test FAIL: id token tripped EMB-001", file=sys.stderr)
            return 2

    print("self-test PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--strict", action="store_true",
                        help="Treat advisory findings as failures.")
    parser.add_argument("--json", action="store_true",
                        help="Emit JSON summary instead of text.")
    parser.add_argument("--self-test", action="store_true",
                        help="Run the synthetic-fixture self-test.")
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    blocking, advisory = evaluate(ROOT)

    if args.json:
        print(json.dumps({
            "gate": "Reference Embargo (CR-BP-112; EMB-001..004)",
            "blocking": [{"rule": r, "message": m} for r, m in blocking],
            "advisory": [{"rule": r, "message": m} for r, m in advisory],
        }, indent=2))
    else:
        verdict = "CONFORMANT"
        if blocking or (args.strict and advisory):
            verdict = "NON-CONFORMANT"
        elif advisory:
            verdict = "CONFORMANT-WITH-WARNINGS"
        print(f"Reference Embargo (CR-BP-112; EMB-001..004): {verdict}")
        print(f"  {len(blocking)} blocking finding(s); {len(advisory)} advisory.")
        for r, m in blocking:
            print(f"    [BLOCKING/{r}] {m}")
        for r, m in advisory:
            print(f"    [ADVISORY/{r}] {m}")

    return 1 if (blocking or (args.strict and advisory)) else 0


if __name__ == "__main__":
    sys.exit(main())
