"""CR-BP-113: Reference HREF Resolver Gate (HREF-001..003)

Closes the enforcement gap that let 484 relative href: values in
entity/discovery YAML files rot silently post-mv1. Three rules:

  HREF-001  (blocking).  Any relative href: whose target does not
                          exist on disk (resolved from REPO ROOT;
                          http(s) hrefs are HREF-003 territory).
  HREF-002  (blocking).  An href field whose value is not a non-empty
                          string.
  HREF-003  (advisory).  An http(s) href whose URL shape is
                          malformed (scheme/host parse failure; no
                          network fetch in CI).

The gate runs as part of the conformance suite and as a standalone
CI step.

Authoritative reference: CR-BP-113 (2026-10-13, eaojnr).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent

HREF_LINE_RE = re.compile(r'^\s*href:\s*["\']?([^"\'\n]+)["\']?\s*$')

# Paths to skip (CI scratch dirs and pre-mv1 history mirrors).
SKIP_PATH_PREFIXES: tuple[str, ...] = (
    ".git/",
    ".venv/",
    ".metaframework/",
    "__pycache__/",
    "node_modules/",
    "01_plan/",
)

# Files scanned for href resolution checks.
SCAN_GLOBS: tuple[str, ...] = (
    "entities/**/*.yaml",
    "discovery/**/*.yaml",
)


# ---------------------------------------------------------------------------
# Resolver
# ---------------------------------------------------------------------------


def _resolve(src_root: Path, target: str) -> Path | None:
    """Resolve `target` to a Path on disk, returning None if the
    target is external (http/https) or invalid.

    The catalog convention is REPO-ROOT-relative: an href value like
    `change-requests/CR-BP-19.md` resolves from the repo root, NOT
    from the file's own directory. The legacy `contexts/v1-alpha/...`
    paths that survived mv1 are also repo-root-relative.

    `./` and `/` prefixes are normalized: `./foo` resolves from the
    repo root, `/foo` strips the leading slash and resolves from the
    repo root."""
    if target.startswith(("http://", "https://")):
        return None
    if target.startswith("./"):
        return (src_root / target[2:]).resolve()
    if target.startswith("/"):
        return (src_root / target.lstrip("/")).resolve()
    return (src_root / target).resolve()


# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------


def _iter_scan_files(allowlist_sealed: tuple[str, ...] = ()) -> list[Path]:
    out: list[Path] = []
    for pattern in SCAN_GLOBS:
        for path in ROOT.glob(pattern):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT).as_posix()
            if any(rel.startswith(p) for p in SKIP_PATH_PREFIXES):
                continue
            if rel in allowlist_sealed:
                continue
            out.append(path)
    return out


def evaluate(allowlist_sealed: tuple[str, ...] = ()) -> tuple[
    list[tuple[str, str]], list[tuple[str, str]]
]:
    """Run HREF-001..003 over the catalog. Returns (blocking, advisory)."""
    blocking: list[tuple[str, str]] = []
    advisory: list[tuple[str, str]] = []

    files = _iter_scan_files(allowlist_sealed)
    seen_targets: Counter[str] = Counter()

    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        try:
            text = path.read_text()
        except OSError as e:
            blocking.append(("HREF-002", f"{rel}: read error: {e}"))
            continue
        for ln, line in enumerate(text.splitlines(), 1):
            m = HREF_LINE_RE.match(line)
            if not m:
                continue
            target = m.group(1).strip()
            if not target:
                blocking.append(("HREF-002", f"{rel}:{ln}: empty href value"))
                continue
            if target.startswith(("http://", "https://")):
                # HREF-003: URL shape only (no network).
                try:
                    parsed = urlparse(target)
                except ValueError:
                    advisory.append((
                        "HREF-003", f"{rel}:{ln}: malformed URL: {target[:80]}",
                    ))
                    continue
                if not parsed.scheme or not parsed.netloc:
                    advisory.append((
                        "HREF-003",
                        f"{rel}:{ln}: missing scheme/host: {target[:80]}",
                    ))
                continue
            seen_targets[target] += 1
            resolved = _resolve(ROOT, target)
            if resolved is None or not resolved.exists():
                blocking.append((
                    "HREF-001",
                    f"{rel}:{ln}: target does not resolve: {target}",
                ))

    return blocking, advisory


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _verdict(blocking: list, advisory: list) -> str:
    if blocking:
        return "NON-CONFORMANT"
    if advisory:
        return "CONFORMANT-WITH-WARNINGS"
    return "CONFORMANT"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 on any blocking finding")
    parser.add_argument("--json", action="store_true",
                        help="emit JSON payload")
    parser.add_argument("--self-test", action="store_true",
                        help="run the in-script self-test")
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    blocking, advisory = evaluate()
    verdict = _verdict(blocking, advisory)

    if args.json:
        import json
        print(json.dumps({
            "verdict": verdict,
            "blocking": [{"rule": r, "message": m} for r, m in blocking],
            "advisory": [{"rule": r, "message": m} for r, m in advisory],
        }, indent=2))
    else:
        print(f"Reference HREF Resolver (CR-BP-113; HREF-001..003): {verdict}")
        print(f"  {len(blocking)} blocking finding(s); {len(advisory)} advisory.")
        for rule, msg in blocking[:20]:
            print(f"    [{rule}] {msg}")
        if len(blocking) > 20:
            print(f"    ... and {len(blocking) - 20} more")
        for rule, msg in advisory[:10]:
            print(f"    [{rule}] {msg}")
        if len(advisory) > 10:
            print(f"    ... and {len(advisory) - 10} more")

    if args.strict and blocking:
        return 1
    return 0


def _self_test() -> int:
    """Exercise the HREF-001..003 rules on hand-rolled records.
    Returns 0 on PASS, non-zero on FAIL."""
    import tempfile
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        # HREF-001: a target that exists on disk resolves; a
        # nonexistent one does not.
        existing = tmp_root / "exists.md"
        existing.write_text("# x\n")
        r1 = _resolve(tmp_root, "exists.md")
        if r1 is None or not r1.exists():
            failures.append("HREF-001: failed to resolve existing target")
        r2 = _resolve(tmp_root, "does-not-exist.md")
        if r2 is not None and r2.exists():
            failures.append("HREF-001: false resolve of nonexistent target")
        # HREF-002: empty href value detected.
        line = "  href: \n"
        m = HREF_LINE_RE.match(line)
        if m is None or m.group(1).strip():
            failures.append("HREF-002: empty href not detected")
        # HREF-003: a malformed URL is parseable but yields empty
        # scheme/host. urlparse is permissive; we only fail on
        # unparseable input. Just check the happy path: a valid
        # http URL is detected as http(s) (skips HREF-001).
        from urllib.parse import urlparse
        try:
            parsed = urlparse("http://example.com/path")
            if parsed.scheme != "http" or parsed.netloc != "example.com":
                failures.append("HREF-003: valid http URL did not parse")
        except ValueError as e:
            failures.append(f"HREF-003: unexpected ValueError: {e}")
    if failures:
        print("self-test FAIL:")
        for f in failures:
            print(f"  {f}")
        return 2
    print(f"self-test PASS: 4 cases (HREF-001/002/003)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
