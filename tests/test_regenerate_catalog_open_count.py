"""Tests for scripts/regenerate_catalog.py open_change_requests count fix.

Locks behaviour for the CR-BP-115 duplicated-condition fix:
the dead branch that counted all non-Merged CRs as open is replaced
by explicit CLOSED_STATUSES / OPEN_STATUSES classification.

Authoritative reference: CR-BP-115 (2026-10-13, eaojnr).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from regenerate_catalog import (  # noqa: E402
    CLOSED_STATUSES,
    count_open_change_requests,
    OPEN_STATUSES,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


def test_closed_statuses_include_accepted():
    assert "Accepted" in CLOSED_STATUSES


def test_closed_statuses_include_merged():
    assert "Merged" in CLOSED_STATUSES


def test_closed_statuses_include_rejected():
    assert "Rejected" in CLOSED_STATUSES


def test_closed_statuses_include_superseded():
    assert "Superseded" in CLOSED_STATUSES


def test_open_statuses_include_proposed():
    assert "Proposed" in OPEN_STATUSES


def test_open_statuses_include_draft():
    assert "Draft" in OPEN_STATUSES


# ---------------------------------------------------------------------------
# Fixture-based counting
# ---------------------------------------------------------------------------


def _make_cr(tmp_path: Path, name: str, status_line: str | None) -> Path:
    """Create a minimal CR file with an optional Status metadata line."""
    cr_dir = tmp_path / "change-requests"
    cr_dir.mkdir(exist_ok=True)
    content = f"# {name}\n"
    if status_line is not None:
        content += f"**Status**: {status_line}\n"
    content += "\nBody text.\n"
    p = cr_dir / f"{name}.md"
    p.write_text(content)
    return tmp_path


class TestCountOpenChangeRequests:
    def test_proposed_counts_open(self, tmp_path):
        _make_cr(tmp_path, "CR-BP-01-a", "Proposed")
        assert count_open_change_requests(tmp_path) == 1

    def test_draft_counts_open(self, tmp_path):
        _make_cr(tmp_path, "CR-BP-01-a", "Draft")
        assert count_open_change_requests(tmp_path) == 1

    def test_merged_counts_closed(self, tmp_path):
        _make_cr(tmp_path, "CR-BP-01-a", "Merged")
        assert count_open_change_requests(tmp_path) == 0

    def test_accepted_counts_closed(self, tmp_path):
        _make_cr(tmp_path, "CR-BP-01-a", "Accepted")
        assert count_open_change_requests(tmp_path) == 0

    def test_rejected_counts_closed(self, tmp_path):
        _make_cr(tmp_path, "CR-BP-01-a", "Rejected")
        assert count_open_change_requests(tmp_path) == 0

    def test_superseded_counts_closed(self, tmp_path):
        _make_cr(tmp_path, "CR-BP-01-a", "Superseded")
        assert count_open_change_requests(tmp_path) == 0

    def test_proposed_with_qualifier_counts_open(self, tmp_path):
        _make_cr(tmp_path, "CR-BP-01-a", "Proposed (this PR)")
        assert count_open_change_requests(tmp_path) == 1

    def test_accepted_with_qualifier_counts_closed(self, tmp_path):
        _make_cr(tmp_path, "CR-BP-01-a", "Accepted (paperwork-only)")
        assert count_open_change_requests(tmp_path) == 0

    def test_no_status_counts_open_with_warning(self, tmp_path):
        _make_cr(tmp_path, "CR-BP-01-a", None)
        warnings: list[str] = []
        assert count_open_change_requests(tmp_path, warnings) == 1
        assert len(warnings) == 1
        assert "no Status line" in warnings[0]

    def test_unrecognized_status_counts_open_with_warning(self, tmp_path):
        _make_cr(tmp_path, "CR-BP-01-a", "InReview")
        warnings: list[str] = []
        assert count_open_change_requests(tmp_path, warnings) == 1
        assert len(warnings) == 1
        assert "unrecognized Status" in warnings[0]

    def test_mixed_statuses(self, tmp_path):
        _make_cr(tmp_path, "CR-BP-01-a", "Proposed")
        _make_cr(tmp_path, "CR-BP-02-b", "Accepted")
        _make_cr(tmp_path, "CR-BP-03-c", "Draft")
        _make_cr(tmp_path, "CR-BP-04-d", "Merged")
        _make_cr(tmp_path, "CR-BP-05-e", "Rejected")
        assert count_open_change_requests(tmp_path) == 2

    def test_body_text_status_not_matched(self, tmp_path):
        """Body text containing 'Status**: Merged' must not close the CR."""
        cr_dir = tmp_path / "change-requests"
        cr_dir.mkdir(exist_ok=True)
        (cr_dir / "CR-BP-01-a.md").write_text(
            "# CR-BP-01\n"
            "**Status**: Proposed\n"
            "\n"
            "The old code checked if \"Status**: Merged\" in head.\n"
            "This body text should not affect the count.\n"
        )
        assert count_open_change_requests(tmp_path) == 1


# ---------------------------------------------------------------------------
# Live repo
# ---------------------------------------------------------------------------


def test_live_count_is_reasonable():
    """Live repo: open count is significantly less than total CR count."""
    from pathlib import Path
    total = len(list(Path(ROOT / "change-requests").glob("CR-*.md")))
    warnings: list[str] = []
    open_count = count_open_change_requests(ROOT, warnings)
    # Sanity: open < total (some are closed), open > 0
    assert 0 < open_count < total
    # The fix should drop the count significantly from the buggy 128.
    assert open_count < 100, (
        f"open_change_requests={open_count} still too high; "
        f"expected < 100 after fix"
    )
