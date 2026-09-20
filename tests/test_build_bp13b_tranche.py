"""Tests for build_bp13b_tranche (CR-BP-13b).

Offline-only: tests exercise the generator's data declarations
(L2_PROCESSES, PROCESS_GROUPS, PROCESS_CONTEXTS) and verify the
renderers produce valid output. The renderers themselves are
covered by build_bp13a_tranche tests (they are shared).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from build_bp13b_tranche import (  # noqa: E402
    L2_PROCESSES,
    PROCESS_CONTEXTS,
    PROCESS_GROUPS,
)
from build_bp13a_tranche import (  # noqa: E402
    render_l2_process,
    render_process_context,
    render_process_group,
)


def test_process_context_count_matches_domain() -> None:
    """5 lifecycle stages = 5 Process Context cells."""
    assert len(PROCESS_CONTEXTS) == 5
    ids = {c["id"] for c in PROCESS_CONTEXTS}
    assert ids == {
        "processes:pc-ge-c",
        "processes:pc-ge-d",
        "processes:pc-ge-b",
        "processes:pc-ge-op",
        "processes:pc-ge-im",
    }


def test_process_group_count_matches_domain() -> None:
    assert len(PROCESS_GROUPS) == 5


def test_l2_process_count_matches_register() -> None:
    """Register has 9 L1 candidates -> 9 L2 entries."""
    assert len(L2_PROCESSES) == 9


def test_process_groups_cover_all_coordinates() -> None:
    """Every Process Group's process_context matches a known cell."""
    cell_ids = {c["id"] for c in PROCESS_CONTEXTS}
    for g in PROCESS_GROUPS:
        assert g["context"] in cell_ids, (
            f"{g['id']} process_context {g['context']} not in cells"
        )


def test_l2_processes_all_compose_into_known_group() -> None:
    """Every L2's process_group must reference a known Process Group."""
    group_ids = {g["id"] for g in PROCESS_GROUPS}
    for p in L2_PROCESSES:
        assert p["process_group"] in group_ids, (
            f"{p['id']} process_group {p['process_group']} not in groups"
        )


def test_l2_processes_all_reference_known_context() -> None:
    cell_ids = {c["id"] for c in PROCESS_CONTEXTS}
    for p in L2_PROCESSES:
        assert p["process_context"] in cell_ids, (
            f"{p['id']} process_context {p['process_context']} not in cells"
        )


def test_l2_process_names_are_verb_first() -> None:
    """BP-ARC-ID-001: name must start with identity.verb."""
    for p in L2_PROCESSES:
        verb = p["verb"].lower()
        assert p["name"].lower().startswith(verb), (
            f"{p['id']}: name '{p['name']}' does not start with "
            f"verb '{verb}'"
        )


def test_l2_processes_use_real_industry_evidence() -> None:
    ALLOWED_DOMAINS = {
        "iso.org", "opengroup.org", "isaca.org",
        "coso.org", "scor", "apqc.org",
    }
    for p in L2_PROCESSES:
        has_industry = any(
            any(d in link["ref"].lower() for d in ALLOWED_DOMAINS)
            for link in p.get("evidence_links", [])
            if link.get("type") == "standard"
        )
        assert has_industry, (
            f"{p['id']}: missing industry-framework evidence"
        )


def test_render_all_process_contexts_parses() -> None:
    for c in PROCESS_CONTEXTS:
        text = render_process_context(c)
        doc = yaml.safe_load(text)
        assert doc["id"] == c["id"]
        # Cell Charter present.
        charter = doc["cell_charter"]
        for field in ("enterprise_concern", "lifecycle_concern",
                      "combined_semantic_meaning", "expected_outcomes",
                      "inclusions", "exclusions", "adjacent_boundaries"):
            assert field in charter


def test_render_all_process_groups_parses() -> None:
    for g in PROCESS_GROUPS:
        text = render_process_group(g)
        doc = yaml.safe_load(text)
        assert doc["id"] == g["id"]
        # ECF conformance well-formed.
        ref = doc["ecfConformance"]["canonicalReferences"][0]
        assert ref["kind"] == "coordinate"
        assert ref["domain"] == "GovernanceAndExistence"
        assert ref["identifier"].startswith("ecf:governanceExistence.")


def test_render_all_l2_processes_parses() -> None:
    for p in L2_PROCESSES:
        text = render_l2_process(p)
        doc = yaml.safe_load(text)
        assert doc["id"] == p["id"]
        assert doc["identity"]["verb"] == p["verb"]


def test_all_renderers_dash_clean() -> None:
    """No em-dash, en-dash, or right-arrow in any new file."""
    BAD = ["\u2014", "\u2013", "\u2192"]
    for c in PROCESS_CONTEXTS:
        assert not any(b in render_process_context(c) for b in BAD)
    for g in PROCESS_GROUPS:
        assert not any(b in render_process_group(g) for b in BAD)
    for p in L2_PROCESSES:
        assert not any(b in render_l2_process(p) for b in BAD)


def test_process_group_kind_is_controlled_vocabulary() -> None:
    """The shared renderer hardcodes 'end-to-end' (PG-007 enum)."""
    for g in PROCESS_GROUPS:
        text = render_process_group(g)
        doc = yaml.safe_load(text)
        assert doc["process_group_kind"] == "end-to-end"


def test_process_type_enum() -> None:
    ALLOWED = {"strategic", "management", "core", "support", "standardization"}
    for p in L2_PROCESSES:
        assert p["process_type"] in ALLOWED, (
            f"{p['id']}: process_type '{p['process_type']}' "
            f"not in {ALLOWED}"
        )
