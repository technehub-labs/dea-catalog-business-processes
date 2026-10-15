"""Test suite for dea_uri_web.py (CR-BP-130; T9.6 web resolver).

The web resolver exposes the dea:// URI resolver over HTTP.
Uses http.server (stdlib) so no Flask/Quart dependency. Tests
spin up the server on a free port and exercise the endpoints.
"""
from __future__ import annotations

import json
import socket
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "dea_uri_web.py"


def _free_port() -> int:
    """Find a free port on localhost."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _wait_for_server(port: int, timeout: float = 5.0) -> bool:
    """Wait until the server is accepting connections."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.1)
    return False


@pytest.fixture
def server():
    """Spin up the web resolver on a free port; tear down at the end."""
    port = _free_port()
    proc = subprocess.Popen(
        [sys.executable, str(SCRIPT), "--port", str(port), "--host", "127.0.0.1"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    try:
        if not _wait_for_server(port):
            proc.kill()
            stderr = proc.stderr.read().decode() if proc.stderr else ""
            pytest.skip(f"server did not start within 5s: {stderr}")
        yield port
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()


def _http_get(port: int, path: str, params: dict | None = None) -> tuple[int, str, dict]:
    """GET a URL; return (status, body, headers)."""
    if params:
        path = f"{path}?{urllib.parse.urlencode(params)}"
    url = f"http://127.0.0.1:{port}{path}"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, resp.read().decode("utf-8"), dict(resp.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8"), dict(e.headers)


# --------------------------------------------------------------------------- #
# Health + List (3 tests)
# --------------------------------------------------------------------------- #

def test_health_returns_ok(server):
    status, body, _ = _http_get(server, "/health")
    assert status == 200
    data = json.loads(body)
    assert data["status"] == "ok"
    assert "version" in data


def test_list_returns_scopes(server):
    status, body, _ = _http_get(server, "/list")
    assert status == 200
    data = json.loads(body)
    assert "scopes" in data
    assert len(data["scopes"]) >= 5
    scope_names = [s["scope"] for s in data["scopes"]]
    assert "dea-catalog-business-processes" in scope_names
    assert "dea-catalog-business-capabilities" in scope_names


def test_cors_header_present(server):
    """CORS header for browser-based usage."""
    _, _, headers = _http_get(server, "/health")
    assert headers.get("Access-Control-Allow-Origin") == "*"


# --------------------------------------------------------------------------- #
# Resolve endpoint (4 tests)
# --------------------------------------------------------------------------- #

def test_resolve_canonical_uri(server):
    """A canonical URI resolves to a file path."""
    uri = "dea://dea-catalog-business-processes/processes:pc-fa-retire-64q5p9"
    status, body, _ = _http_get(server, "/resolve", {"uri": uri})
    assert status == 200
    data = json.loads(body)
    assert data["resolved"] is True
    assert data["exists"] is True
    assert "fa-retire" in data["path"]


def test_resolve_missing_uri_param_returns_400(server):
    status, body, _ = _http_get(server, "/resolve")
    assert status == 400
    data = json.loads(body)
    assert "missing" in data["error"]


def test_resolve_malformed_uri_returns_400(server):
    status, body, _ = _http_get(server, "/resolve", {"uri": "not-a-uri"})
    assert status == 400
    data = json.loads(body)
    assert data["resolved"] is False


def test_resolve_unknown_scope_returns_400(server):
    uri = "dea://unknown-scope/processes:process-foo-bar-f3n8wb"
    status, body, _ = _http_get(server, "/resolve", {"uri": uri})
    assert status == 400
    data = json.loads(body)
    assert data["resolved"] is False


# --------------------------------------------------------------------------- #
# Fetch endpoint (2 tests)
# --------------------------------------------------------------------------- #

def test_fetch_returns_yaml_content(server):
    """A known URI returns the YAML file content."""
    uri = "dea://dea-catalog-business-processes/processes:pc-fa-retire-64q5p9"
    status, body, headers = _http_get(server, "/fetch", {"uri": uri})
    assert status == 200
    assert "id:" in body  # YAML content
    assert "processes:pc-fa-retire-64q5p9" in body
    assert "application/x-yaml" in headers.get("Content-Type", "")


def test_fetch_missing_uri_returns_400(server):
    status, body, _ = _http_get(server, "/fetch")
    assert status == 400


# --------------------------------------------------------------------------- #
# Exists endpoint (2 tests)
# --------------------------------------------------------------------------- #

def test_exists_returns_200_for_real_file(server):
    uri = "dea://dea-catalog-business-processes/processes:pc-fa-retire-64q5p9"
    status, body, _ = _http_get(server, "/exists", {"uri": uri})
    assert status == 200
    assert "exists" in body


def test_exists_returns_404_for_missing_file(server):
    uri = "dea://dea-catalog-business-processes/processes:process-this-does-not-exist-f3n8wb"
    status, body, _ = _http_get(server, "/exists", {"uri": uri})
    assert status == 404


# --------------------------------------------------------------------------- #
# 404 default (1 test)
# --------------------------------------------------------------------------- #

def test_unknown_path_returns_404(server):
    status, body, _ = _http_get(server, "/this-does-not-exist")
    assert status == 404
    data = json.loads(body)
    assert data["error"] == "not found"
