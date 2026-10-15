# CR-BP-129: dea:// URI Remote Resolver (T9.5)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance) - implementation
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-15
**Depends on**: CR-BP-128 (T9.3 dea:// URI resolver CLI)
**Companion**: the resolver at `scripts/dea_uri_resolver.py`

## 1. Purpose

This is the T9.5 follow-on to the Entity System institutionalisation. CR-BP-128 (T9.3) shipped the local-only resolver; this CR adds the `--remote` flag that fetches the catalog repository from GitHub when the local clone is absent.

After this slice: any `dea://` URI can be resolved regardless of whether the catalog repository is locally cloned. The resolver is now a cross-repo tool, not just a local-tree tool.

## 2. The 2 deliverables

### 2.1 The remote-fetcher

`scripts/dea_uri_resolver.py` (MOD) - new `_fetch_remote_repo` function and `--remote` CLI flag:
- The `_fetch_remote_repo(scope, registries, depth=1)` function clones the catalog repository from GitHub (shallow clone by default; pass `depth` for full history).
- The `--remote` CLI flag triggers the fetch when the local clone is absent.
- The fetch uses `git clone --depth 1` for speed; full history is not needed for resolution.
- The cloned repo is placed at `$SIBLING_ROOT/{repo}` (default: `/home/hermes/Projects/dea-sibling-check/{repo}`).
- After fetch, the URI is resolved against the freshly-cloned repo.

### 2.2 The 23-test suite (3 new tests)

`tests/test_dea_uri_resolver.py` (MOD) - 3 new tests:
- `test_remote_fetch_known_scope`: a known scope (e.g. `dea-metamodel`) is fetched on `--remote` (skips if network unavailable).
- `test_remote_fetch_unknown_scope`: a scope with no registry entry fails to fetch.
- `test_cli_remote_flag_accepted`: the `--remote` flag is accepted by the CLI parser.

Total: 23 tests (20 from CR-BP-128 + 3 new).

## 3. Repository changes

| Path | Status | Notes |
|---|---|---|
| `scripts/dea_uri_resolver.py` | MOD | Added `_fetch_remote_repo`; `--remote` flag |
| `tests/test_dea_uri_resolver.py` | MOD | 3 new tests (total 23) |
| `change-requests/CR-BP-129-dea-uri-remote-resolver.md` | NEW | This file (the carrier CR) |
| `change-requests/README.md` | MOD | New row at top of table |
| `CHANGELOG.md` | MOD | [Unreleased] entry |
| `CATALOG.yaml` | MOD | Regenerator bump |

## 4. Acceptance criteria

- AC-01 The `--remote` flag is accepted by the CLI parser.
- AC-02 The `_fetch_remote_repo` function clones the catalog repository from GitHub.
- AC-03 A scope with no local clone + `--remote` flag is fetched and resolved.
- AC-04 A scope with no registry entry + `--remote` flag returns an error.
- AC-05 The 23-test suite passes.
- AC-06 D-004 (no en/em-dash, no U+2E3B) is clean across all new/modified files.
- AC-07 118a/118b/118c/123/124/125/126/127/128 authorship + entity-system gates remain CONFORMANT.

## 5. Test posture (live, 2026-10-15)

```
$ python3 -m pytest tests/test_dea_uri_resolver.py -v
========================================== 23 passed, 1 skipped in 1.2s ==========================================
```

(The skipped test is the PC integration test that requires a specific PC record shape.)

## 6. What this CR is NOT

- **NOT a web resolver.** A web-based resolver (Flask/Quart HTTP API) is a T9.6 follow-on.
- **NOT a sync tool.** The remote-fetch is a one-shot clone; ongoing sync (fetch + pull) is a T9.7 follow-on.
- **NOT a remote-update tool.** The resolver does not push changes to the remote; that is the contribution flow.
- **NOT a metadata change.** No entity, schema, or id changes.

## 7. Out-of-scope follow-ons

- **T9.2** (IANA submission): submit the IANA registration template to the IANA URI Schemes registry.
- **T9.4** (Permanent status): submit the I-D to IETF for review; achieve Permanent status.
- **T9.6** (Web resolver): a Flask/Quart app that exposes the resolver over HTTP.
- **T9.7** (Sync tool): `dea_uri_sync.py` - a tool that fetches and updates local clones against the remote.

## 8. Cross-references

- **CR-BP-128** (T9.3): the local-only resolver.
- **CR-BP-127** (T9.1): the dea:// URI scheme spec.
- **CR-BP-126** (Stage 7): the U-01 Cross-Catalog URI Standard.
- **DEA-ID-000**: the foundation paper.
- **CR-012**: the org-wide governance CR.
