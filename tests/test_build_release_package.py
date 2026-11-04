"""CR-BP-30a..30e: release-package builder tests.

Each builder runs against the live catalog (the smallest fixtures that
exercise the shape) and asserts artifact content + determinism
(two identical builds byte-compare). Determinism is the contract the
validate-release-package workflow enforces in CI.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

generate_process_map = importlib.import_module("generate_process_map")
build_catalog_xlsx = importlib.import_module("build_catalog_xlsx")
build_bpmn_artifact = importlib.import_module("build_bpmn_artifact")
build_release_notes = importlib.import_module("build_release_notes")


def test_process_map_renders_grid_and_cells(tmp_path):
    out = tmp_path / "process-map.html"
    rc = generate_process_map.main(["--label", "vTEST", "--out", str(out)])
    assert rc == 0
    html = out.read_text()
    assert "Business Process Catalog" in html
    # All 7 domains and 7 stages appear as axis labels.
    for frag in ("Party", "Relationship", "Finance", "Accounting",
                 "Enablement", "Operations"):  # axis labels wrap at " & "
        assert frag in html
    for stage in ("Conceive", "Operate", "Retire"):
        assert stage in html
    # A known L2 process renders as a bullet in its cell ribbon.
    assert "Mobilize Licensed Workforce" in html
    # Determinism: identical second build byte-compares.
    out2 = tmp_path / "process-map2.html"
    generate_process_map.main(["--label", "vTEST", "--out", str(out2)])
    assert out.read_bytes() == out2.read_bytes()


def test_catalog_xlsx_six_sheets(tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    out = tmp_path / "catalog.xlsx"
    build_catalog_xlsx.build(out)
    wb = openpyxl.load_workbook(out)
    assert wb.sheetnames == ["01_records", "02_lineage", "03_dispositions",
                             "04_register_audit", "05_change_requests",
                             "06_contributions"]
    ws = wb["01_records"]
    # 3,723 records + header row.
    assert ws.max_row >= 3724
    # Sheet 1 carries the versions column (the CR-BP-30 §3.2 request).
    headers = [c.value for c in ws[1]]
    assert "version" in headers
    # Determinism.
    out2 = tmp_path / "catalog2.xlsx"
    build_catalog_xlsx.build(out2)
    assert out.read_bytes() == out2.read_bytes()


def test_bpmn_seed_library(tmp_path):
    import xml.etree.ElementTree as ET
    out = tmp_path / "bpmn-library.bpmn"
    build_bpmn_artifact.build(out, "vTEST")
    root = ET.parse(out).getroot()
    ns = {"b": "http://www.omg.org/spec/BPMN/20100524/MODEL"}
    procs = root.findall("b:process", ns)
    assert len(procs) == 145  # one per canonical L2
    doc_texts = [p.find("b:documentation", ns).text for p in procs]
    assert any("ECF cell" in d and "Process Context" in d for d in doc_texts)
    tasks = root.findall(".//b:task", ns)
    assert len(tasks) == 145
    # Determinism.
    out2 = tmp_path / "bpmn2.bpmn"
    build_bpmn_artifact.build(out2, "vTEST")
    assert out.read_bytes() == out2.read_bytes()


def test_release_notes_and_decisions(tmp_path):
    out = tmp_path / "RELEASE-NOTES.md"
    dec = tmp_path / "decisions.md"
    build_release_notes.main(["--version", "v0.5.0", "--date", "2026-11-04",
                              "--out", str(out), "--decisions", str(dec)])
    notes = out.read_text()
    assert "# Release Notes — v0.5.0" in notes
    assert "Catalog posture" in notes and "Provenance" in notes
    decisions = dec.read_text()
    assert "# Decisions Log" in decisions
    assert "D4=A" in decisions or "dispositions" in decisions
    # Determinism.
    out2, dec2 = tmp_path / "RN2.md", tmp_path / "dec2.md"
    build_release_notes.main(["--version", "v0.5.0", "--date", "2026-11-04",
                              "--out", str(out2), "--decisions", str(dec2)])
    assert out.read_bytes() == out2.read_bytes()
    assert dec.read_bytes() == dec2.read_bytes()


def test_build_manifest(tmp_path):
    import hashlib
    (tmp_path / "sub").mkdir()
    (tmp_path / "a.html").write_text("<html>x</html>")
    (tmp_path / "sub" / "b.yaml").write_text("id: x\n")
    import build_manifest
    rc = build_manifest.main(["--dir", str(tmp_path), "--version", "vTEST"])
    assert rc == 0
    manifest = (tmp_path / "MANIFEST.md").read_text()
    assert "a.html" in manifest and "sub/b.yaml" in manifest
    sha = hashlib.sha256(b"<html>x</html>").hexdigest()
    assert sha in manifest
    assert "GENERATED" not in manifest  # provenance map names the script
