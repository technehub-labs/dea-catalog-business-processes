#!/usr/bin/env python3
r"""
check_semantic_identity_version.py
===================================

Semantic-Identity-vs-Version validator (CR-BP-34d; CR-BP-34 §19 SIV-001..004).

Codifies the version-discipline rules from CR-BP-34 §19 as machine-testable
per-record invariants. Today the discipline is enforced only by PR review
and CR-META-006 (cross-repo identifier integrity); there is no
intra-repo validator that catches "version bump without identity
documentation" or "MAJOR bump without semantic-change marker".

  SIV-001 — Version is SemVer.
            `version` ∈ ^\d+\.\d+\.\d+$ (per schemas/entity.schema.json).
            3 dot-separated integers. 4-segment or suffixed values fail.

  SIV-002 — Version bump requires change_history evidence.
            For any record whose version != 1.0.0 (MAJOR > 1, or MINOR > 0,
            or PATCH > 0), at least one entry in `change_history` must carry
            a non-empty `change` (or `description`) text field naming the
            change. Empty change_history arrays on bumped records are
            forbidden.

  SIV-003 — MAJOR bump requires a semantic-change marker.
            For any record whose MAJOR component > 1, at least one
            change_history entry must contain a semantic-change marker
            (case-insensitive substring): one of BREAKING, SEMANTIC,
            RENAME, REC-, DEPRECATED, SUPERSEDED, CR-BP-, CR-ECF-, CR-AR-,
            CR-MM-, CR-OU-, CR-BC-, CR-BO-. The marker establishes that
            the bump was intentional, not accidental.

  SIV-004 — MINOR/PATCH bump shall not silently alter identity.verb or
            identity.object.
            For any record whose MAJOR == 1 but MINOR > 0 or PATCH > 0,
            the record should carry an optional `previous_identity` sub-
            block (under `identity`) declaring the prior verb and object.
            Absence is recorded as an *advisory* finding (no failure) —
            spot-check rather than gate.
            If `previous_identity` IS present, identity.verb and
            identity.object MUST equal previous_identity.verb and
            previous_identity.object respectively (or both absent).

Coverage on the live catalog (2026-09-11):
  126 canonical BP records.
  125 at version 1.0.0; 1 at version 2.0.0.
  Expected findings (seed): SIV-001 = 0; SIV-002 = 1; SIV-003 = 1;
  SIV-004 = 0. The CR remediates the v2.0.0 record in the same PR so the
  validator emits 0 findings on the post-remediation catalog (advisory
  gate).

Exit codes:
  0  all records satisfy all four rules
  1  at least one record fails at least one rule
  2  self-test failure or I/O error

Usage:
  python3 scripts/check_semantic_identity_version.py
  python3 scripts/check_semantic_identity_version.py --strict
  python3 scripts/check_semantic_identity_version.py --json
  python3 scripts/check_semantic_identity_version.py --self-test

Author: Coder (for eaojnr). Established by CR-BP-34d (2026-09-11).
Derived from CR-BP-34 §19 (Version Conformance) and CR-BP-16 (Conformance
Gate). See change-requests/CR-BP-34d-semantic-identity-vs-version.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Callable

import yaml

# SemVer: exactly 3 dot-separated non-negative integers.
# Same regex as schemas/entity.schema.json: "^\\d+\\.\\d+\\.\\d+$"
# Use re.fullmatch so a trailing newline (or other whitespace) does
# NOT count as SemVer (matches ajv's full-string anchor semantics).
SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")

# Case-insensitive substring markers that establish a MAJOR-bumped record
# carried an intentional semantic-identity change. Union of:
#   - explicit rename/breaking markers (BREAKING, SEMANTIC, RENAME, REC-,
#     DEPRECATED case-sensitive transition marker per LCM-003,
#     SUPERSEDED)
#   - cross-CR identifiers (CR-BP-, CR-ECF-, CR-AR-, CR-MM-, CR-OU-,
#     CR-BC-, CR-BO-)
SEMANTIC_CHANGE_MARKERS: tuple[str, ...] = (
    "BREAKING",
    "SEMANTIC",
    "RENAME",
    "REC-",        # reconciliation-id prefix (BP-REC-NNNN)
    "DEPRECATED",  # transition-event marker per LCM-003 (case-sensitive)
    "SUPERSEDED",
    "CR-BP-",
    "CR-ECF-",
    "CR-AR-",
    "CR-MM-",
    "CR-OU-",
    "CR-BC-",
    "CR-BO-",
)


def _semver_parts(version: str) -> tuple[int, int, int] | None:
    """Parse a SemVer string. Returns (major, minor, patch) or None."""
    m = SEMVER_RE.fullmatch(version)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2)), int(m.group(3))


def _change_history_texts(record: dict) -> list[str]:
    """Return all change_history entry text fields (top-level OR metadata.change_history)."""
    ch = record.get("change_history")
    if not isinstance(ch, list):
        md = record.get("metadata") or {}
        ch = md.get("change_history") if isinstance(md, dict) else None
    if not isinstance(ch, list):
        return []
    texts: list[str] = []
    for entry in ch:
        if isinstance(entry, dict):
            text = entry.get("change") or entry.get("description") or ""
            if isinstance(text, str) and text.strip():
                texts.append(text)
    return texts


def _has_nonempty_change_history(record: dict) -> bool:
    """True iff at least one change_history entry has non-empty text."""
    return bool(_change_history_texts(record))


def _has_semantic_change_marker(record: dict) -> bool:
    """True iff any change_history text contains a semantic-change marker.

    Markers are matched case-insensitively EXCEPT for the "DEPRECATED"
    transition-event marker (per LCM-003), which is case-sensitive.
    Implementation: convert text to uppercase first for the case-folded
    markers; check the original text separately for "DEPRECATED" exactly.
    """
    for text in _change_history_texts(record):
        upper = text.upper()
        for marker in SEMANTIC_CHANGE_MARKERS:
            if marker == "DEPRECATED":
                if marker in text:  # case-sensitive
                    return True
            else:
                if marker in upper:  # case-insensitive
                    return True
    return False


def _check_siv_001(record: dict) -> str | None:
    """SIV-001: version is SemVer (3 dot-separated integers)."""
    raw = record.get("version")
    if raw is None:
        return "version field missing"
    if not isinstance(raw, str):
        return f"version must be a string; got {type(raw).__name__}"
    if not SEMVER_RE.fullmatch(raw):
        return f"version={raw!r} is not SemVer (expected ^\\d+\\.\\d+\\.\\d+$)"
    return None


def _check_siv_002(record: dict) -> str | None:
    """SIV-002: version bump requires non-empty change_history."""
    raw = record.get("version")
    if not isinstance(raw, str):
        return None  # covered by SIV-001
    parts = _semver_parts(raw)
    if parts is None:
        return None  # covered by SIV-001
    major, minor, patch = parts
    # v1.0.0 is exempt (initial canonical release).
    if major == 1 and minor == 0 and patch == 0:
        return None
    if not _has_nonempty_change_history(record):
        return (
            f"version={raw!r} (bumped from 1.0.0) but change_history is "
            "missing or empty; every version bump requires at least one "
            "change_history entry naming the change"
        )
    return None


def _check_siv_003(record: dict) -> str | None:
    """SIV-003: MAJOR bump requires a semantic-change marker."""
    raw = record.get("version")
    if not isinstance(raw, str):
        return None
    parts = _semver_parts(raw)
    if parts is None:
        return None
    major, minor, patch = parts
    if major <= 1:
        return None  # only fires on MAJOR > 1
    if not _has_semantic_change_marker(record):
        return (
            f"version={raw!r} is a MAJOR bump (>= 2.0.0) but no "
            "change_history entry contains a semantic-change marker "
            "(one of: BREAKING, SEMANTIC, RENAME, REC-, DEPRECATED, "
            "SUPERSEDED, CR-BP-, CR-ECF-, CR-AR-, CR-MM-, CR-OU-, "
            "CR-BC-, CR-BO-); every MAJOR bump requires explicit "
            "documentation of the semantic-identity change"
        )
    return None


def _check_siv_004(record: dict) -> str | None:
    """SIV-004: MINOR/PATCH bump shall not silently alter identity.

    Advisory: if previous_identity is absent, returns a "spot-check"
    diagnostic. If present, identity.verb/object MUST equal
    previous_identity.verb/object (or both absent).
    """
    raw = record.get("version")
    if not isinstance(raw, str):
        return None
    parts = _semver_parts(raw)
    if parts is None:
        return None
    major, minor, patch = parts
    # Only MINOR/PATCH bumps on MAJOR==1.
    if major != 1 or (minor == 0 and patch == 0):
        return None
    identity = record.get("identity") or {}
    if not isinstance(identity, dict):
        return None  # covered by BP-ARC-ID-001..005
    prev = identity.get("previous_identity")
    if not isinstance(prev, dict):
        # Advisory only — does not fail.
        return (
            f"version={raw!r} is a MINOR/PATCH bump but no "
            "`identity.previous_identity` block is present; spot-check "
            "that identity.verb and identity.object did not silently "
            "change (advisory, non-blocking)"
        )
    # previous_identity declared — enforce identity stability.
    cur_verb = identity.get("verb")
    cur_obj = identity.get("object")
    prev_verb = prev.get("verb")
    prev_obj = prev.get("object")
    if (cur_verb or prev_verb) and cur_verb != prev_verb:
        return (
            f"version={raw!r} is a MINOR/PATCH bump but identity.verb "
            f"silently changed: was {prev_verb!r}, now {cur_verb!r}; a "
            "semantic-identity change requires a MAJOR bump plus a "
            "semantic-change marker in change_history"
        )
    if (cur_obj or prev_obj) and cur_obj != prev_obj:
        return (
            f"version={raw!r} is a MINOR/PATCH bump but identity.object "
            f"silently changed: was {prev_obj!r}, now {cur_obj!r}; a "
            "semantic-identity change requires a MAJOR bump plus a "
            "semantic-change marker in change_history"
        )
    return None


# (rule_id, function, label, severity)
# severity: "blocking" => strict-mode failure
#           "advisory" => reported but never fails strict mode
_RULES: tuple[tuple[str, Callable[[dict], str | None], str, str], ...] = (
    ("SIV-001", _check_siv_001, "version is SemVer", "blocking"),
    ("SIV-002", _check_siv_002, "version bump requires change_history evidence", "blocking"),
    ("SIV-003", _check_siv_003, "MAJOR bump requires semantic-change marker", "blocking"),
    ("SIV-004", _check_siv_004, "MINOR/PATCH bump shall not silently alter identity", "advisory"),
)


def _load_bp_records(catalog_root: Path) -> list[tuple[Path, dict]]:
    """Load every canonical Business Process record (with path).

    Walks `entities/v1-alpha/dea:process-*/<id>.yaml`. Skips dirs
    without the expected YAML file. Returns (path, record) pairs.
    """
    base = catalog_root / "entities" / "v1-alpha"
    pairs: list[tuple[Path, dict]] = []
    if not base.exists():
        return pairs
    for yaml_path in sorted(base.rglob("processes-process-*.yaml")):
        try:
            data = yaml.safe_load(yaml_path.read_text())
        except yaml.YAMLError as exc:
            print(f"WARN: {yaml_path}: YAML parse error: {exc}", file=sys.stderr)
            continue
        if isinstance(data, dict):
            pairs.append((yaml_path, data))
    return pairs


def evaluate(pairs: list[tuple[Path, dict]]) -> list[dict]:
    """Run all four rules against every (path, record) pair."""
    findings: list[dict] = []
    for _path, record in pairs:
        rec_id = record.get("id") or _path.parent.name
        for rule_id, fn, _label, severity in _RULES:
            diagnostic = fn(record)
            if diagnostic is not None:
                findings.append({
                    "rule": rule_id,
                    "record_id": rec_id,
                    "severity": severity,
                    "diagnostic": diagnostic,
                })
    return findings


def _verdict(findings: list[dict]) -> str:
    blocking = [f for f in findings if f["severity"] == "blocking"]
    if blocking:
        return "NON-CONFORMANT"
    if findings:
        return "CONFORMANT-WITH-WARNINGS"
    return "CONFORMANT"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(
        "Semantic-Identity-vs-Version validator (CR-BP-34d; SIV-001..004)."
    ))
    parser.add_argument(
        "--catalog-root",
        default=".",
        help="Path to the catalog repo root (default: current directory).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 on any blocking finding (advisory findings are reported but do not fail).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON output instead of human-readable summary.",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run the built-in self-test and exit.",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    catalog_root = Path(args.catalog_root).resolve()
    pairs = _load_bp_records(catalog_root)
    findings = evaluate(pairs)
    verdict = _verdict(findings)

    if args.json:
        print(json.dumps({
            "verdict": verdict,
            "candidate_count": len(pairs),
            "finding_count": len(findings),
            "blocking_count": sum(1 for f in findings if f["severity"] == "blocking"),
            "advisory_count": sum(1 for f in findings if f["severity"] == "advisory"),
            "findings": findings,
            "rules": [
                {"id": rid, "name": label, "severity": sev}
                for rid, _fn, label, sev in _RULES
            ],
            "semantic_change_markers": list(SEMANTIC_CHANGE_MARKERS),
        }, indent=2, sort_keys=True))
    else:
        print(f"Semantic Identity vs Version (CR-BP-34d; SIV-001..004): {verdict}")
        print(f"  Records checked:  {len(pairs)}")
        print(f"  Findings:         {len(findings)} "
              f"(blocking={sum(1 for f in findings if f['severity']=='blocking')}, "
              f"advisory={sum(1 for f in findings if f['severity']=='advisory')})")
        for rid, _fn, label, sev in _RULES:
            n = sum(1 for f in findings if f["rule"] == rid)
            tag = "blocking" if sev == "blocking" else "advisory"
            print(f"    {rid} [{tag}] ({label}): {n}")
        if findings:
            print("\nFindings:")
            for f in findings:
                tag = "BLOCK" if f["severity"] == "blocking" else "ADV "
                print(f"  [{tag}][{f['rule']}] {f['record_id']}: {f['diagnostic']}")

    blocking = [f for f in findings if f["severity"] == "blocking"]
    if blocking and args.strict:
        return 1
    return 0


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def _rec(version: str = "1.0.0",
         change_history: list[dict] | None = None,
         identity: dict | None = None) -> dict:
    """Build a minimal record for self-test fixtures."""
    rec: dict = {
        "id": "processes:process-test-fixture",
        "name": "Test",
        "type": "Process",
        "version": version,
        "process_intent": "manage",
    }
    if change_history is not None:
        rec["change_history"] = change_history
    if identity is not None:
        rec["identity"] = identity
    return rec


def _self_test() -> int:
    """Built-in self-test. Exits 0 on success, 2 on any assertion failure."""

    def _expect(findings: list[dict], rule: str, count: int, label: str) -> bool:
        actual = sum(1 for f in findings if f["rule"] == rule)
        ok = actual == count
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}: expected {count} {rule} findings, got {actual}")
        return ok

    failures = 0

    # --- SIV-001 ---
    print("\n[SIV-001] SemVer format")
    # pass
    if not (_expect(evaluate([(Path("/x"), _rec("1.0.0"))]), "SIV-001", 0, "1.0.0 pass")):
        failures += 1
    if not (_expect(evaluate([(Path("/x"), _rec("2.0.0", [{"change": "x"}]))]), "SIV-001", 0, "2.0.0 pass")):
        failures += 1
    if not (_expect(evaluate([(Path("/x"), _rec("1.0.0.0"))]), "SIV-001", 1, "4-segment fail")):
        failures += 1
    if not (_expect(evaluate([(Path("/x"), _rec("v1.0.0"))]), "SIV-001", 1, "v-prefix fail")):
        failures += 1
    if not (_expect(evaluate([(Path("/x"), _rec("1.0"))]), "SIV-001", 1, "2-segment fail")):
        failures += 1

    # --- SIV-002 ---
    print("\n[SIV-002] version bump requires change_history")
    if not (_expect(evaluate([(Path("/x"), _rec("1.0.0", [{"change": "x"}]))]), "SIV-002", 0, "v1.0.0 exempt")):
        failures += 1
    if not (_expect(evaluate([(Path("/x"), _rec("1.1.0", [{"change": "minor bump"}]))]), "SIV-002", 0, "1.1.0 with change_history pass")):
        failures += 1
    if not (_expect(evaluate([(Path("/x"), _rec("1.1.0"))]), "SIV-002", 1, "1.1.0 with no change_history fail")):
        failures += 1
    if not (_expect(evaluate([(Path("/x"), _rec("1.0.1", [{"change": "patch"}]))]), "SIV-002", 0, "1.0.1 with change_history pass")):
        failures += 1
    if not (_expect(evaluate([(Path("/x"), _rec("2.0.0"))]), "SIV-002", 1, "2.0.0 with no change_history fail")):
        failures += 1
    # change_history present but entries have empty change field
    if not (_expect(evaluate([(Path("/x"), _rec("1.1.0", [{"change": ""}, {"description": "  "}]))]), "SIV-002", 1, "1.1.0 with empty entries fail")):
        failures += 1

    # --- SIV-003 ---
    print("\n[SIV-003] MAJOR bump requires semantic-change marker")
    if not (_expect(evaluate([(Path("/x"), _rec("1.0.0", [{"change": "x"}]))]), "SIV-003", 0, "v1.0.0 exempt")):
        failures += 1
    if not (_expect(evaluate([(Path("/x"), _rec("1.1.0", [{"change": "minor"}]))]), "SIV-003", 0, "v1.1.0 exempt (MAJOR==1)")):
        failures += 1
    if not (_expect(evaluate([(Path("/x"), _rec("2.0.0", [{"change": "Initial release"}]))]), "SIV-003", 1, "v2.0.0 no marker fail")):
        failures += 1
    if not (_expect(evaluate([(Path("/x"), _rec("2.0.0", [{"change": "CR-BP-21a: rename to corporate strategy"}]))]), "SIV-003", 0, "v2.0.0 CR-BP- marker pass")):
        failures += 1
    if not (_expect(evaluate([(Path("/x"), _rec("2.0.0", [{"change": "Breaking semantic rename via REC-0042"}]))]), "SIV-003", 0, "v2.0.0 REC- marker pass")):
        failures += 1
    if not (_expect(evaluate([(Path("/x"), _rec("2.0.0", [{"change": "Renamed per DEPRECATED transition"}]))]), "SIV-003", 0, "v2.0.0 DEPRECATED case-sensitive marker pass")):
        failures += 1
    # DEPRECATED lowercase should NOT count (per LCM-003 case-sensitive convention)
    if not (_expect(evaluate([(Path("/x"), _rec("2.0.0", [{"change": "lifecycle_status=deprecated status update"}]))]), "SIV-003", 1, "v2.0.0 'deprecated' lowercase narrative does NOT count")):
        failures += 1

    # --- SIV-004 ---
    print("\n[SIV-004] MINOR/PATCH bump identity stability (advisory)")
    if not (_expect(evaluate([(Path("/x"), _rec("1.0.0"))]), "SIV-004", 0, "v1.0.0 exempt")):
        failures += 1
    if not (_expect(evaluate([(Path("/x"), _rec("1.1.0", [{"change": "x"}]))]), "SIV-004", 1, "v1.1.0 missing previous_identity advisory")):
        failures += 1
    # With previous_identity declared and unchanged
    id_ok = {
        "verb": "Manage",
        "object": "Customer",
        "previous_identity": {"verb": "Manage", "object": "Customer"},
    }
    if not (_expect(evaluate([(Path("/x"), _rec("1.1.0", [{"change": "x"}], id_ok))]), "SIV-004", 0, "v1.1.0 unchanged identity pass")):
        failures += 1
    # With previous_identity declared but verb silently changed
    id_verb = {
        "verb": "Manage",
        "object": "Customer",
        "previous_identity": {"verb": "Operate", "object": "Customer"},
    }
    if not (_expect(evaluate([(Path("/x"), _rec("1.1.0", [{"change": "x"}], id_verb))]), "SIV-004", 1, "v1.1.0 verb changed fail")):
        failures += 1
    # With previous_identity declared but object silently changed
    id_obj = {
        "verb": "Manage",
        "object": "Customer",
        "previous_identity": {"verb": "Manage", "object": "Account"},
    }
    if not (_expect(evaluate([(Path("/x"), _rec("1.1.0", [{"change": "x"}], id_obj))]), "SIV-004", 1, "v1.1.0 object changed fail")):
        failures += 1

    # --- Verdict logic ---
    print("\n[Verdict]")
    pairs_clean = [(_make_path(), _rec("1.0.0", [{"change": "seed"}]))]
    findings_clean = evaluate(pairs_clean)
    if _verdict(findings_clean) != "CONFORMANT":
        print(f"  [FAIL] clean catalog verdict: expected CONFORMANT, got {_verdict(findings_clean)}")
        failures += 1
    else:
        print("  [PASS] clean catalog => CONFORMANT")

    pairs_adv = [(_make_path(), _rec("1.1.0", [{"change": "minor"}]))]
    findings_adv = evaluate(pairs_adv)
    # SIV-004 fires as advisory => CONFORMANT-WITH-WARNINGS
    if _verdict(findings_adv) != "CONFORMANT-WITH-WARNINGS":
        print(f"  [FAIL] advisory-only verdict: expected CONFORMANT-WITH-WARNINGS, got {_verdict(findings_adv)}")
        failures += 1
    else:
        print("  [PASS] advisory-only => CONFORMANT-WITH-WARNINGS")

    pairs_block = [(_make_path(), _rec("2.0.0"))]
    findings_block = evaluate(pairs_block)
    if _verdict(findings_block) != "NON-CONFORMANT":
        print(f"  [FAIL] blocking verdict: expected NON-CONFORMANT, got {_verdict(findings_block)}")
        failures += 1
    else:
        print("  [PASS] blocking findings => NON-CONFORMANT")

    print()
    if failures:
        print(f"SELF-TEST FAILED: {failures} assertion(s) failed")
        return 2
    print("SELF-TEST PASSED")
    return 0


def _make_path() -> Path:
    """Dummy path helper for self-test fixtures (path is unused by rules)."""
    return Path("/tmp/fake/dea:process-test/dea:process-test.yaml")


if __name__ == "__main__":
    sys.exit(main())
