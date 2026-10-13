"""test_check_authorship.py: tests for the CR-BP-118 authorship gate.

Coverage:
- Registry loads with the expected fields, allowlist, denylist.
- Allowlist contains the canonical name + the org.
- Denylist contains every agent/tool name from CR-BP-118 R1.
- AUT-001 substring match catches forbidden values embedded in prose.
- AUT-002 fires when the field's parent block is present but the field
  itself is empty.
- AUT-003 fires for typos that pass AUT-001 but are not in the allowlist.
- Live tree contains zero AUT-001 blocking findings after the sweep
  (the CR's main acceptance criterion).
- The --json output envelope is stable.
- The --strict flag exits non-zero on advisory findings.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_authorship.py"
REGISTRY = ROOT / "reconciliation" / "authorship-fields.yaml"


def _load_module():
    spec = importlib.util.spec_from_file_location("check_authorship_test", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


MOD = _load_module()


def _run(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT, capture_output=True, text=True, **kwargs,
    )


def test_registry_exists():
    assert REGISTRY.exists(), f"missing authorship registry at {REGISTRY}"


def test_registry_loads_expected_fields():
    fields, _, _ = MOD._load_registry()
    paths = {f["path"] for f in fields}
    assert "**Owner**" in paths
    assert "**Author**" in paths
    assert "audit.author" in paths
    assert "authors[].name" in paths


def test_allowlist_contains_canonical_name_and_org():
    _, allowlist, _ = MOD._load_registry()
    assert "Emmanuel A. Otchere" in allowlist
    assert "TechNeHub Labs" in allowlist


@pytest.mark.parametrize("name", [
    "Coder", "Agent", "Hermes", "Claude", "GPT", "Cline",
    "OpenAI", "MiniMax", "MiniMax-M3",
])
def test_denylist_contains_agent_tool_names(name):
    _, _, denylist = MOD._load_registry()
    assert name in denylist


def _run_check(path: str, value: str, kind: str = "metadata"):
    _, allowlist, denylist = MOD._load_registry()
    findings: list[dict] = []
    summary = {"AUT-001": 0, "AUT-002": 0, "AUT-003": 0}
    fake_field = {"path": path, "file_glob": "x.md", "kind": kind}
    MOD._check_value("x.md", 1, path, value, allowlist, denylist, findings, summary, fake_field)
    return findings


def test_aut001_substring_match_catches_forbidden_embedded_in_prose():
    """A field value like 'Emmanuel A. Otchere (Coder for eaojnr)' must trip AUT-001
    because 'Coder' is a substring of the value."""
    findings = _run_check("**Owner**", "Emmanuel A. Otchere (Coder for eaojnr)")
    assert len(findings) == 1
    assert findings[0]["rule"] == "AUT-001"
    assert findings[0]["deny_hit"] == "Coder"


def test_aut002_fires_on_empty_value():
    findings = _run_check("audit.author", "")
    assert len(findings) == 1
    assert findings[0]["rule"] == "AUT-002"


def test_aut003_fires_on_canonical_typo():
    """'Emmanuel Otchere' (missing middle initial) is not in the allowlist
    and trips AUT-003 advisory."""
    findings = _run_check("**Owner**", "Emmanuel Otchere")
    assert len(findings) == 1
    assert findings[0]["rule"] == "AUT-003"
    assert findings[0]["value"] == "Emmanuel Otchere"


def test_clean_value_passes_all_rules():
    findings = _run_check("**Owner**", "Emmanuel A. Otchere")
    assert findings == []


def test_self_test_exits_zero():
    r = _run(["--self-test"])
    assert r.returncode == 0, f"self-test failed: {r.stdout}\n{r.stderr}"


def test_live_tree_has_zero_aut001_blocking_findings():
    """The main CR-BP-118a acceptance criterion: after the sweep, no
    AUT-001 (deny-list substring) finding in the live tree."""
    r = _run(["--json"])
    assert r.returncode == 0, f"gate non-conformant: {r.stdout}\n{r.stderr}"
    envelope = json.loads(r.stdout)
    assert envelope["gate"] == "AUT-001..003"
    assert envelope["summary"]["AUT-001"] == 0, (
        f"AUT-001 blocking findings remain after sweep: "
        f"{envelope['blocking'][:5]}"
    )


def test_json_output_envelope_schema_stable():
    r = _run(["--json"])
    envelope = json.loads(r.stdout)
    assert set(envelope.keys()) >= {
        "gate", "cr", "summary", "blocking", "advisory", "verdict",
    }
    assert set(envelope["summary"].keys()) == {"AUT-001", "AUT-002", "AUT-003"}


def test_strict_exits_zero_on_clean_tree():
    """The CR-BP-118a acceptance: --strict exit 0 after the sweep.
    AUT-003 advisory findings would fail --strict; the sweep should
    leave none."""
    r = _run(["--strict"])
    assert r.returncode == 0, f"--strict non-conformant: {r.stdout}\n{r.stderr}"
