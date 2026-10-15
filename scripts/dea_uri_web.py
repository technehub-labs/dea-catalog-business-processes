#!/usr/bin/env python3
"""dea_uri_web.py

HTTP server that exposes the dea:// URI resolver (from
scripts/dea_uri_resolver.py) over HTTP. Uses the stdlib
http.server (no Flask/Quart dependency).

Usage:
  python3 scripts/dea_uri_web.py [--port PORT] [--host HOST]

Default: localhost:8080

Endpoints:
  GET /health
      Returns 200 OK with the version.
  GET /list
      Returns a JSON list of known scopes.
  GET /resolve?uri=<dea-uri>
      Returns JSON with the resolution result:
        {"resolved": true, "path": "...", "scope": "...", ...}
      or {"resolved": false, "error": "..."}.
  GET /fetch?uri=<dea-uri>
      Returns the file contents (200) or an error (4xx).
  GET /exists?uri=<dea-uri>
      Returns 200 if the file exists locally, 404 otherwise.

This is T9.6 (web resolver HTTP API). The server is single-
threaded (sufficient for a documentation tool / development
server). For production deployment, run behind a reverse proxy
like nginx or use a WSGI/ASGI server.
"""
from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Make the resolver importable
sys.path.insert(0, str(__file__).rsplit("/", 2)[0])
import dea_uri_resolver as resolver  # type: ignore


VERSION = "0.1.0"


class ResolverHandler(BaseHTTPRequestHandler):
    """HTTP handler for the dea:// URI web resolver."""

    def log_message(self, format, *args):
        """Quiet logging to stderr."""
        sys.stderr.write(f"[dea_uri_web] {self.address_string()} - {format % args}\n")

    def _send_json(self, status: int, payload: dict) -> None:
        # Convert PosixPath to str for JSON serialization
        def _normalize(obj):
            if isinstance(obj, dict):
                return {k: _normalize(v) for k, v in obj.items()}
            if isinstance(obj, (list, tuple)):
                return [_normalize(v) for v in obj]
            if isinstance(obj, Path):
                return str(obj)
            return obj
        body = json.dumps(_normalize(payload), indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")  # CORS for browser use
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, status: int, text: str, content_type: str = "text/plain") -> None:
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _get_uri_param(self) -> str | None:
        """Extract the `uri` query parameter from the request."""
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        uris = params.get("uri", [])
        if not uris:
            return None
        return uris[0]

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"

        if path == "/health":
            self._send_json(200, {"status": "ok", "version": VERSION})
            return

        if path == "/list":
            registries = resolver._load_registry()
            scopes = sorted(set(list(registries.keys()) + list(resolver.DEFAULT_SCOPE_PATHS.keys())))
            payload = {
                "scopes": [
                    {"scope": scope, "repository": registries.get(scope, {}).get("repository", "<in-thread>")}
                    for scope in scopes
                ],
            }
            self._send_json(200, payload)
            return

        if path == "/resolve":
            uri = self._get_uri_param()
            if not uri:
                self._send_json(400, {"resolved": False, "error": "missing 'uri' parameter"})
                return
            result = resolver.resolve(uri, remote=False)
            self._send_json(200 if result["resolved"] else 400, result)
            return

        if path == "/fetch":
            uri = self._get_uri_param()
            if not uri:
                self._send_text(400, "missing 'uri' parameter\n")
                return
            result = resolver.resolve(uri, remote=False)
            if not result["resolved"]:
                self._send_json(400, result)
                return
            path_obj = result["path"]
            if not path_obj.exists():
                self._send_text(404, f"file does not exist: {path_obj}\n")
                return
            try:
                content = path_obj.read_text(encoding="utf-8", errors="ignore")
            except Exception as e:
                self._send_text(500, f"read error: {e}\n")
                return
            content_type = "application/x-yaml" if path_obj.suffix in (".yaml", ".yml") else "text/plain"
            self._send_text(200, content, content_type)
            return

        if path == "/exists":
            uri = self._get_uri_param()
            if not uri:
                self._send_text(400, "missing 'uri' parameter\n")
                return
            result = resolver.resolve(uri, remote=False)
            if not result["resolved"]:
                self._send_text(404, f"unresolvable: {result.get('error', 'unknown')}\n")
                return
            if result["path"].exists():
                self._send_text(200, "exists\n")
            else:
                self._send_text(404, f"file does not exist: {result['path']}\n")
            return

        # Default: 404
        self._send_json(404, {"error": "not found", "path": path})


def main(argv: list) -> int:
    parser = argparse.ArgumentParser(
        description="HTTP server exposing the dea:// URI resolver.",
    )
    parser.add_argument("--port", type=int, default=8080,
                        help="Port to listen on (default 8080)")
    parser.add_argument("--host", default="127.0.0.1",
                        help="Host to bind to (default 127.0.0.1)")
    args = parser.parse_args(argv)

    server = ThreadingHTTPServer((args.host, args.port), ResolverHandler)
    print(f"[dea_uri_web] listening on http://{args.host}:{args.port}", file=sys.stderr)
    print(f"[dea_uri_web] version {VERSION}", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("[dea_uri_web] shutting down", file=sys.stderr)
        server.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
