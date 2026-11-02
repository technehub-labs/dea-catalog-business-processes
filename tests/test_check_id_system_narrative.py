"""Test suite for CR-BP-222: narrative id currency (IDM-009) and the
one-shot narrative sweep script (scripts/repair_narrative_ids.py).

IDM-009 forbids legacy `dea:*` id tokens in current-state narrative
fields of canonical entity records. `change_history` subtrees are exempt
(historical attestation prose; landed history is immutable), as are
values registered in reconciliation/migration-id-map.yaml
known_residuals. The `*` quantifier in the rule regex catches
source-string truncations (`dea:pc-fa-re`).
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load(name: str):
    script = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, script)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


idmod = _load("check_id_system")
repmod = _load("repair_narrative_ids")

P = Path("entities/v1-alpha/x/processes-process-test-abc123.yaml")


# ---------------------------------------------------------------------------
# IDM-009: rule behavior
# ---------------------------------------------------------------------------

def test_idm009_fires_on_legacy_token_in_definition():
    rec = {"definition": "work within the dea:activity-administer-benefits boundary"}
    assert idmod._check_idm009(rec, P)


def test_idm009_catches_truncated_token():
    rec = {"inputs": [{"description": "within the dea:pc-fa-re"}]}
    findings = idmod._check_idm009(rec, P)
    assert findings and "dea:pc-fa-re" in findings[0]


def test_idm009_exempts_change_history_subtree():
    rec = {"metadata": {"change_history": [
        {"cr": "CR-BP-21e", "change": "added edge to dea:activity-administer-benefits"},
        {"cr": "CR-BP-58", "change": "removed dea:process-conduct- dangling edge"},
    ]}}
    assert idmod._check_idm009(rec, P) == []


def test_idm009_exempts_registered_residuals():
    rec = {"metadata": {
        "supersedes": "dea:group-strategy-and-governance-conception (v1.0.0; CR-BP-13a)",
        "scope": {"id": "dea:scope-customer-facing-operations"},
    }}
    assert idmod._check_idm009(rec, P) == []


def test_idm009_clean_record_passes():
    rec = {"definition": "work within the processes:activity-fa-operate-rnszvv boundary",
           "description": "canonical ids only"}
    assert idmod._check_idm009(rec, P) == []


def test_idm009_current_namespace_untouched():
    rec = {"description": "the processes:* id family replaced dea:* scheme refs"}
    assert idmod._check_idm009(rec, P) == []


# ---------------------------------------------------------------------------
# repair_narrative_ids.py: change_history skip state machine
# ---------------------------------------------------------------------------

def test_skip_skips_change_history_including_sequence_entries():
    text = (
        "definition: canonical text\n"
        "metadata:\n"
        "  change_history:\n"
        "  - cr: CR-BP-21e\n"
        "    change: 'edge to dea:activity-administer-benefits\n"
        "\n"
        "      continued dea:process-conduct- edge'\n"
        "  - cr: CR-BP-58\n"
        "    change: 'removed dea:process-frame-financial-policy-thesis'\n"
        "  other_key: value\n"
        "description: after dea:activity-administer-benefits\n"
    )
    eligible = {i for i, _ in repmod._iter_submittable_lines(text)}
    assert 0 in eligible          # definition
    assert 2 not in eligible      # change_history key
    assert all(i not in eligible for i in range(3, 9))   # subtree incl. `- ` entries + continuation
    assert 9 in eligible          # `other_key` sibling ends the subtree
    assert 10 in eligible         # after the subtree


def test_repair_substitutes_only_mapped_tokens():
    id_map = {"dea:activity-administer-benefits": "processes:activity-ao-operate-8sc5gr"}
    residuals = {"dea:scope-customer-facing-operations"}
    text = (
        "definition: within dea:activity-administer-benefits and dea:process-unknown-x\n"
        "scope:\n"
        "  id: dea:scope-customer-facing-operations\n"
    )
    # exercise the substitution closure via a minimal replica of repair_file
    import re
    eligible = {i for i, _ in repmod._iter_submittable_lines(text)}
    lines = text.splitlines(keepends=True)
    rewrites = 0
    preserved = 0
    for i, line in enumerate(lines):
        if i not in eligible or not repmod.LEGACY_TOKEN_RE.search(line):
            continue
        def _sub(m):
            nonlocal rewrites, preserved
            tok = m.group(0)
            if tok in residuals:
                preserved += 1
                return tok
            new = id_map.get(tok)
            if new is None:
                return tok
            rewrites += 1
            return new
        lines[i] = repmod.LEGACY_TOKEN_RE.sub(_sub, line)
    out = "".join(lines)
    assert "processes:activity-ao-operate-8sc5gr" in out
    assert "dea:process-unknown-x" in out        # unmapped: left, reported
    assert "dea:scope-customer-facing-operations" in out  # residual: preserved
    assert rewrites == 1 and preserved == 1
