# CR-BP-131: dea:// URI Sync Tool (T9.7)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance) - implementation
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-15
**Depends on**: CR-BP-129 (T9.5 remote resolver)
**Companion**: the sync tool at `scripts/dea_uri_sync.py`

## 1. Purpose

This is the T9.7 follow-on to the Entity System institutionalisation. CR-BP-129 (T9.5) added a one-shot remote-fetch to the resolver; this CR ships a dedicated sync tool that handles multi-scope workflows (clone + pull + checkout). The sync tool is the operational tool for keeping local clones in sync with the remote across all 11 sibling repos.

After this slice: a single command (`python3 scripts/dea_uri_sync.py --all`) syncs every catalog repository. The tool is the operational complement to the resolution algorithm.

## 2. The 2 deliverables

### 2.1 The sync tool

`scripts/dea_uri_sync.py` (~220 lines) - the sync tool. Features:
- `clone_scope(scope, registries, depth=1)`: clones a scope's repo from GitHub if absent. Shallow clone by default for speed.
- `pull_scope(scope, registries, ref=None)`: pulls the latest changes (and optionally checks out a ref).
- `sync_scope(scope, registries, depth, ref)`: clone if absent, else pull.
- CLI modes:
  - `python3 scripts/dea_uri_sync.py <scope>` - sync a specific scope.
  - `python3 scripts/dea_uri_sync.py --all` - sync all known scopes.
  - `python3 scripts/dea_uri_sync.py --ref <ref>` - checkout a specific ref.
  - `python3 scripts/dea_uri_sync.py --depth <n>` - clone depth.
  - `python3 scripts/dea_uri_sync.py --list` - list scopes with local/remote-only status.
- The in-thread scope (`dea-catalog-business-processes`) is skipped (not synced via the tool).
- Exit code: 0 if all requested scopes sync; 1 if any fail.

### 2.2 The 14-test suite

`tests/test_dea_uri_sync.py` - 14 tests:
- 2 registry tests
- 4 git operation tests (init, missing git, unknown scope, in-thread)
- 2 pull_scope tests
- 2 sync_scope integration tests (uses tmpdir + monkeypatch)
- 4 CLI tests

## 3. Repository changes

| Path | Status | Notes |
|---|---|---|
| `scripts/dea_uri_sync.py` | NEW | The sync tool (~220 lines) |
| `tests/test_dea_uri_sync.py` | NEW | 14 tests; 14/14 pass |
| `change-requests/CR-BP-131-dea-uri-sync.md` | NEW | This file (the carrier CR) |
| `change-requests/README.md` | MOD | New row at top of table |
| `CHANGELOG.md` | MOD | [Unreleased] entry |
| `CATALOG.yaml` | MOD | Regenerator bump |

## 4. Acceptance criteria

- AC-01 The sync tool is at `scripts/dea_uri_sync.py` (~220 lines).
- AC-02 The 14-test suite passes.
- AC-03 The sync tool clones + pulls all known scopes.
- AC-04 The `--ref` flag checks out a specific ref after sync.
- AC-05 The `--list` flag lists scopes with local/remote-only status.
- AC-06 The in-thread scope is skipped.
- AC-07 D-004 (no en/em-dash, no U+2E3B) is clean across all new/modified files.
- AC-08 118a/118b/118c/123/124/125/126/127/128/129/130 authorship + entity-system gates remain CONFORMANT.

## 5. Test posture (live, 2026-10-15)

```
$ python3 -m pytest tests/test_dea_uri_sync.py -v
========================================== 14 passed in 5.2s ==========================================
```

## 6. What this CR is NOT

- **NOT a CI tool.** The sync tool is an operator tool; CI is a different concern.
- **NOT a contribution tool.** The sync tool doesn't push changes to the remote; that's the contribution flow.
- **NOT a remote-fetcher.** The remote-fetcher is a one-shot clone in the resolver; the sync tool is a multi-scope operation.
- **NOT a metadata change.** No entity, schema, or id changes.

## 7. Out-of-scope follow-ons

- **T9.2** (IANA submission): submit the IANA registration template to the IANA URI Schemes registry.
- **T9.4** (Permanent status): submit the I-D to IETF for review; achieve Permanent status.
- **T9.8** (Production server): wrap the web resolver in a WSGI/ASGI server for production deployment.
- **T9.9** (Sync daemon): a long-running daemon that auto-syncs on a schedule.

## 8. Cross-references

- **CR-BP-128** (T9.3): the CLI resolver.
- **CR-BP-129** (T9.5): the remote resolver (one-shot clone).
- **CR-BP-127** (T9.1): the dea:// URI scheme spec.
- **CR-BP-130** (T9.6): the web resolver HTTP API.
- **CR-BP-126** (Stage 7): the U-01 Cross-Catalog URI Standard.
- **DEA-ID-000**: the foundation paper.
- **CR-012**: the org-wide governance CR.
