# CR-BP-130: dea:// URI Web Resolver HTTP API (T9.6)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance) - implementation
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-15
**Depends on**: CR-BP-128 (T9.3 dea:// URI resolver CLI); CR-BP-129 (T9.5 remote resolver)
**Companion**: the web resolver at `scripts/dea_uri_web.py`; the CLI resolver at `scripts/dea_uri_resolver.py`

## 1. Purpose

This is the T9.6 follow-on to the Entity System institutionalisation. CR-BP-128 (T9.3) shipped the CLI resolver; CR-BP-129 (T9.5) added remote-fetch; this CR exposes the resolver over HTTP. The web resolver is a documentation-friendly way to resolve `dea://` URIs without a CLI.

After this slice: any HTTP client (curl, browser, static-site generator, doc tool) can resolve a `dea://` URI to a file path or fetch the file contents.

## 2. The 2 deliverables

### 2.1 The web resolver

`scripts/dea_uri_web.py` (~180 lines) - the HTTP server. Features:
- Uses stdlib `http.server` (no Flask/Quart dependency).
- 5 endpoints:
  - `GET /health` - returns `{status, version}` JSON.
  - `GET /list` - returns a JSON list of known scopes.
  - `GET /resolve?uri=<dea-uri>` - returns the resolution result as JSON.
  - `GET /fetch?uri=<dea-uri>` - returns the file contents (text/yaml).
  - `GET /exists?uri=<dea-uri>` - returns 200 if the file exists, 404 otherwise.
- CORS enabled (`Access-Control-Allow-Origin: *`) for browser-based usage.
- Threading server (handles concurrent requests).
- Defaults: `127.0.0.1:8080` (use `--port` and `--host` to override).
- For production: run behind nginx or a WSGI/ASGI server.

### 2.2 The 12-test suite

`tests/test_dea_uri_web.py` - 12 tests:
- 3 health + list tests (health endpoint, list endpoint, CORS header)
- 4 resolve endpoint tests (canonical URI, missing param, malformed URI, unknown scope)
- 2 fetch endpoint tests (YAML content, missing param)
- 2 exists endpoint tests (real file returns 200, missing file returns 404)
- 1 default 404 test

## 3. Repository changes

| Path | Status | Notes |
|---|---|---|
| `scripts/dea_uri_web.py` | NEW | The HTTP server (~180 lines) |
| `tests/test_dea_uri_web.py` | NEW | 12 tests; 12/12 pass |
| `change-requests/CR-BP-130-dea-uri-web-resolver.md` | NEW | This file (the carrier CR) |
| `change-requests/README.md` | MOD | New row at top of table |
| `CHANGELOG.md` | MOD | [Unreleased] entry |
| `CATALOG.yaml` | MOD | Regenerator bump |

## 4. Acceptance criteria

- AC-01 The web resolver is at `scripts/dea_uri_web.py` (~180 lines).
- AC-02 The 12-test suite passes.
- AC-03 The 5 endpoints (`/health`, `/list`, `/resolve`, `/fetch`, `/exists`) work correctly.
- AC-04 CORS headers are present for browser-based usage.
- AC-05 The server uses stdlib `http.server` (no new dependencies).
- AC-06 The threading server handles concurrent requests.
- AC-07 D-004 (no en/em-dash, no U+2E3B) is clean across all new/modified files.
- AC-08 118a/118b/118c/123/124/125/126/127/128/129 authorship + entity-system gates remain CONFORMANT.

## 5. Test posture (live, 2026-10-15)

```
$ python3 -m pytest tests/test_dea_uri_web.py -v
========================================== 12 passed in 1.5s ==========================================
```

## 6. What this CR is NOT

- **NOT a production-grade server.** The web resolver is a single-threaded dev tool; for production, use nginx + a WSGI/ASGI server.
- **NOT a sync tool.** The web resolver doesn't fetch remote repositories; that's the CLI's `--remote` flag.
- **NOT a metadata change.** No entity, schema, or id changes.

## 7. Out-of-scope follow-ons

- **T9.2** (IANA submission): submit the IANA registration template to the IANA URI Schemes registry.
- **T9.4** (Permanent status): submit the I-D to IETF for review; achieve Permanent status.
- **T9.7** (Sync tool): `dea_uri_sync.py` - a tool that fetches and updates local clones against the remote.
- **T9.8** (Production server): wrap the web resolver in a WSGI/ASGI server (gunicorn / uvicorn) for production deployment.

## 8. Cross-references

- **CR-BP-128** (T9.3): the CLI resolver.
- **CR-BP-129** (T9.5): the remote resolver.
- **CR-BP-127** (T9.1): the dea:// URI scheme spec.
- **CR-BP-126** (Stage 7): the U-01 Cross-Catalog URI Standard.
- **DEA-ID-000**: the foundation paper.
- **CR-012**: the org-wide governance CR.
