from __future__ import annotations

import importlib.util
import base64
import gzip
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from render_publication_assets import (  # noqa: E402
    main,
    render_catalogue_html,
    render_poster_html,
    validate_model,
)


def _fixture_builder():
    path = Path(__file__).with_name("test_publication_model.py")
    spec = importlib.util.spec_from_file_location("publication_model_fixtures", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _model(tmp_path):
    fixtures = _fixture_builder()
    root, ecf = fixtures._fixture(tmp_path)
    return fixtures.build_model(root, ecf, build_commit="abcdef123456",
                                verify_ecf_commit=False)


def _with_finding(model):
    import hashlib
    import json
    model["findings"] = [{
        "code": "HIERARCHY-L2-CONTEXT-CONFLICT", "severity": "error",
        "message": "Fixture relationship is unresolved.",
        "source_id": "processes:process-governance-conceive-ghi",
    }]
    payload = {key: value for key, value in model.items() if key != "model_digest"}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    model["model_digest"] = "sha256:" + hashlib.sha256(raw).hexdigest()
    return model


def _embedded_model(page):
    payload = re.search(r'id="publication-model">([^<]+)</script>', page).group(1)
    return gzip.decompress(base64.b64decode(payload)).decode("utf-8")


def test_poster_uses_model_order_and_carries_provenance_and_findings(tmp_path):
    model = _with_finding(_model(tmp_path))
    poster = render_poster_html(model)

    assert poster.index("Governance &amp; Existence") < poster.index("Strategy &amp; Direction")
    assert poster.index("Conceive") < poster.index("Design")
    assert poster.count("class='cell") == 49
    assert "Governance Process" in poster
    assert "A1 landscape" in poster
    assert model["model_digest"] in poster
    assert model["provenance"]["canonical_entity_snapshot_commit"] in poster
    assert "Diagnostic model · not release-ready" in poster


def test_html_embeds_all_model_data_and_preserves_source_detail(tmp_path):
    model = _with_finding(_model(tmp_path))
    page = render_catalogue_html(model)

    embedded = _embedded_model(page)
    for text in ("Governance Process", "Formal process definition for the fixture.",
                 "A concise fixture description.", "An example grounded in the fixture source.",
                 "Request", "Decision", "processes:group-governance-conceive-def",
                 model["provenance"]["canonical_entity_snapshot_commit"]):
        assert text in embedded
    for control in ("id=\"domain\"", "id=\"stage\"", "id=\"level\"", "id=\"intent\"",
                    "id=\"specialization\"", "id=\"classification\"", "id=\"state\""):
        assert control in page
    assert "data-open" in page
    assert "process-catalogue.html" not in page
    assert "Not declared in the source record." in page
    assert "Declared but empty." in page
    assert "Fixture relationship is unresolved." in page
    for relation in ("composes", "belongs_to_business_process", "belongs_to_activity",
                     "in_process_context"):
        assert f"relationship_type==='" in page and relation in page


def test_html_is_offline_and_embedded_model_is_safe_from_script_termination(tmp_path):
    model = _with_finding(_model(tmp_path))
    model["entities"][2]["record"]["description"] = "</script><script>alert(1)</script>"
    # Recompute the fixture digest after changing canonical model content.
    import hashlib
    import json
    payload = {key: value for key, value in model.items() if key != "model_digest"}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    model["model_digest"] = "sha256:" + hashlib.sha256(raw).hexdigest()
    validate_model(model)
    page = render_catalogue_html(model)

    assert "</script><script>alert(1)</script>" not in page
    assert "\\u003c/script\\u003e" in _embedded_model(page)
    assert "<link" not in page
    assert "<img" not in page
    assert "src=\"https://" not in page
    assert "cdn." not in page.lower()
    assert "Diagnostic model · not release-ready" in page


def test_rendering_is_byte_deterministic(tmp_path):
    model = _model(tmp_path)
    assert render_catalogue_html(model).encode("utf-8") == render_catalogue_html(model).encode("utf-8")
    assert render_poster_html(model).encode("utf-8") == render_poster_html(model).encode("utf-8")


def test_embedded_browser_script_parses(tmp_path):
    node = shutil.which("node")
    if not node:
        pytest.skip("Node.js is not installed")
    page = render_catalogue_html(_model(tmp_path))
    script = re.search(r"<script>(.*?)</script>", page, re.DOTALL).group(1)
    script_path = tmp_path / "catalogue.js"
    script_path.write_text(script, encoding="utf-8")
    subprocess.run([node, "--check", str(script_path)], check=True,
                   capture_output=True, text=True)


def test_stale_digest_is_rejected(tmp_path):
    model = _model(tmp_path)
    model["entities"][0]["record"]["name"] = "tampered"
    with pytest.raises(ValueError, match="digest"):
        validate_model(model)


def test_cli_requires_opt_in_for_error_level_diagnostic_model(tmp_path, capsys):
    import json
    model = _with_finding(_model(tmp_path))
    model_path = tmp_path / "model.json"
    model_path.write_text(json.dumps(model), encoding="utf-8")
    output_dir = tmp_path / "preview"

    assert main(["--model", str(model_path), "--output-dir", str(output_dir)]) == 2
    assert "error-level findings" in capsys.readouterr().err
    assert main(["--model", str(model_path), "--output-dir", str(output_dir),
                 "--allow-findings"]) == 0
    assert (output_dir / "process-catalogue.html").is_file()


def test_pdf_and_png_are_from_a_single_a1_page_when_dependencies_exist(tmp_path):
    import shutil
    from render_publication_assets import render_assets

    if not shutil.which("pdftoppm"):
        pytest.skip("Poppler tools are not installed")
    pytest.importorskip("weasyprint")
    model = _model(tmp_path)
    first = render_assets(model, tmp_path / "first", poster_pdf=True, poster_png=True)
    second = render_assets(model, tmp_path / "second", poster_pdf=True, poster_png=True)

    # PDF metadata/serialization may vary between identical renders. Verify
    # stable publication content and page geometry instead of byte identity.
    info = subprocess.run(["pdfinfo", str(first["poster_pdf"])], check=True,
                          capture_output=True, text=True).stdout
    assert re.search(r"^Pages:\s+1$", info, re.MULTILINE)
    size = re.search(r"^Page size:\s+([\d.]+) x ([\d.]+) pts", info, re.MULTILINE)
    assert size is not None
    assert abs(float(size.group(1)) - 2383.94) < 1.5  # A1 landscape width (841 mm in points)
    assert abs(float(size.group(2)) - 1683.78) < 1.5  # A1 landscape height (594 mm in points)

    text_a = subprocess.run(["pdftotext", "-layout", str(first["poster_pdf"]), "-"],
                            check=True, capture_output=True, text=True).stdout
    text_b = subprocess.run(["pdftotext", "-layout", str(second["poster_pdf"]), "-"],
                            check=True, capture_output=True, text=True).stdout
    normalize = lambda value: re.sub(r"\\s+", " ", value).strip()
    assert normalize(text_a) == normalize(text_b)

    from PIL import Image, ImageChops
    image_a = Image.open(first["poster_png"]).convert("RGB")
    image_b = Image.open(second["poster_png"]).convert("RGB")
    assert image_a.size == image_b.size
    assert ImageChops.difference(image_a, image_b).getbbox() is None
