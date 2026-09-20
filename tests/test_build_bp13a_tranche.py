"""Tests for build_bp13a_tranche (CR-BP-13a).

Offline-only: tests exercise the generator's renderers against
fixture data. The generator is deterministic; we test the rendered
YAML output against expected field shapes (parses, has required
fields, has expected number of composes / relationships).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

# Make the tool importable.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from build_bp13a_tranche import (
    L2_PROCESSES,
    PROCESS_CONTEXTS,
    PROCESS_GROUPS,
    render_l2_process,
    render_process_context,
    render_process_group,
)


def test_render_process_context_parses_yaml() -> None:
    """Every Process Context renderer output is parseable YAML."""
    for c in PROCESS_CONTEXTS:
        text = render_process_context(c)
        doc = yaml.safe_load(text)
        assert doc is not None
        assert doc["id"] == c["id"]
        assert doc["domain"] == c["domain"]
        assert doc["lifecycle_stage"] == c["stage"]


def test_render_process_context_has_cell_charter() -> None:
    """Cell Charter (CR-BP-02 §7) requires 5 fields."""
    for c in PROCESS_CONTEXTS:
        text = render_process_context(c)
        doc = yaml.safe_load(text)
        charter = doc.get("cell_charter", {})
        required = {
            "enterprise_concern",
            "lifecycle_concern",
            "combined_semantic_meaning",
            "expected_outcomes",
            "inclusions",
            "exclusions",
            "adjacent_boundaries",
        }
        assert required.issubset(set(charter.keys())), (
            f"{c['id']} missing Cell Charter fields: "
            f"{required - set(charter.keys())}"
        )


def test_render_process_group_parses_yaml() -> None:
    for g in PROCESS_GROUPS:
        text = render_process_group(g)
        doc = yaml.safe_load(text)
        assert doc is not None
        assert doc["id"] == g["id"]
        assert doc["type"] == "ProcessGroup"
        # Each composes entry should resolve to a known L2.
        for c in doc.get("composes", []):
            assert c["relationship_type"] == "composes"
            assert c["target_id"].startswith("processes:process-")


def test_render_l2_process_parses_yaml() -> None:
    for p in L2_PROCESSES:
        text = render_l2_process(p)
        doc = yaml.safe_load(text)
        assert doc is not None
        assert doc["id"] == p["id"]
        assert doc["type"] == "Process"
        # Identity sub-block required by CR-BP-03 §5.4.
        assert "identity" in doc
        assert doc["identity"]["verb"] == p["verb"]


def test_render_l2_process_name_matches_verb_object() -> None:
    """BP-ARC-ID-001 requires name to start with verb."""
    for p in L2_PROCESSES:
        text = render_l2_process(p)
        doc = yaml.safe_load(text)
        # Name should start with the verb (or the verb's present form).
        verb = doc["identity"]["verb"]
        assert doc["name"].lower().startswith(verb.lower()), (
            f"{p['id']}: name '{doc['name']}' does not start with "
            f"verb '{verb}'"
        )


def test_render_l2_process_uses_real_industry_evidence() -> None:
    """Each L2 entry should reference real industry frameworks."""
    ALLOWED_DOMAINS = {"apqc.org", "tmforum.org", "scor", "itil", "bian"}
    for p in L2_PROCESSES:
        text = render_l2_process(p)
        doc = yaml.safe_load(text)
        ev_links = doc.get("identity", {}).get("evidence_links", [])
        # At least one evidence link should be from an industry framework.
        has_industry = any(
            any(d in link["ref"].lower() for d in ALLOWED_DOMAINS)
            for link in ev_links
            if link.get("type") == "standard"
        )
        assert has_industry, f"{p['id']}: missing industry-framework evidence"


def test_render_process_group_ecf_conformance() -> None:
    """Each Process Group's ECF canonical reference is well-formed."""
    for g in PROCESS_GROUPS:
        text = render_process_group(g)
        doc = yaml.safe_load(text)
        ref = doc["ecfConformance"]["canonicalReferences"][0]
        assert ref["kind"] == "coordinate"
        assert ref["domain"] == "PartyAndRelationship"
        assert ref["stage"] in {"Conceive", "Design", "Build", "Operate", "Improve"}
        assert ref["identifier"].startswith("ecf:partyRelationship.")


def test_render_l2_process_ecf_conformance() -> None:
    for p in L2_PROCESSES:
        text = render_l2_process(p)
        doc = yaml.safe_load(text)
        ref = doc["ecfConformance"]["canonicalReferences"][0]
        assert ref["kind"] == "coordinate"
        assert ref["identifier"].startswith("ecf:partyRelationship.")


def test_render_process_group_composes_count_matches_l2s() -> None:
    """Each Process Group's `composes` array length matches the
    number of L2 entries whose process_group == this group."""
    by_group: dict[str, int] = {}
    for p in L2_PROCESSES:
        by_group[p["process_group"]] = by_group.get(p["process_group"], 0) + 1
    for g in PROCESS_GROUPS:
        text = render_process_group(g)
        doc = yaml.safe_load(text)
        n_composes = len(doc.get("composes", []))
        n_l2s = by_group.get(g["id"], 0)
        assert n_composes == n_l2s, (
            f"{g['id']}: composes={n_composes} but {n_l2s} L2 entries"
        )


def test_render_process_group_dash_clean() -> None:
    """New files must be em-dash clean (CR-BP-13 §dash-sweep)."""
    BAD = ["\u2014", "\u2013", "\u2192"]
    for g in PROCESS_GROUPS:
        text = render_process_group(g)
        for ch in BAD:
            assert ch not in text, (
                f"{g['id']}: contains forbidden char U+{ord(ch):04X}"
            )


def test_render_l2_process_dash_clean() -> None:
    BAD = ["\u2014", "\u2013", "\u2192"]
    for p in L2_PROCESSES:
        text = render_l2_process(p)
        for ch in BAD:
            assert ch not in text, (
                f"{p['id']}: contains forbidden char U+{ord(ch):04X}"
            )


def test_render_process_context_dash_clean() -> None:
    BAD = ["\u2014", "\u2013", "\u2192"]
    for c in PROCESS_CONTEXTS:
        text = render_process_context(c)
        for ch in BAD:
            assert ch not in text, (
                f"{c['id']}: contains forbidden char U+{ord(ch):04X}"
            )


def test_process_group_kind_is_controlled_vocabulary() -> None:
    """PG-007 enforces controlled vocabulary for process_group_kind."""
    from build_bp13a_tranche import PROCESS_GROUPS as groups
    ALLOWED = {"end-to-end", "value-stream", "support", "governance"}
    for g in groups:
        assert g["process_group_kind"] in ALLOWED, (
            f"{g['id']}: process_group_kind '{g['process_group_kind']}' "
            f"not in {ALLOWED}"
        )


def test_process_intent_enum() -> None:
    """process_intent must be one of the 3-value enum."""
    from build_bp13a_tranche import L2_PROCESSES as procs
    ALLOWED = {"operational", "support", "management"}
    for p in procs:
        assert p["process_intent"] in ALLOWED, (
            f"{p['id']}: process_intent '{p['process_intent']}' "
            f"not in {ALLOWED}"
        )


def test_process_type_enum() -> None:
    """process_type must be one of the 5-value Mintzberg vocabulary."""
    from build_bp13a_tranche import L2_PROCESSES as procs
    ALLOWED = {"strategic", "management", "core", "support", "standardization"}
    for p in procs:
        assert p["process_type"] in ALLOWED, (
            f"{p['id']}: process_type '{p['process_type']}' "
            f"not in {ALLOWED}"
        )