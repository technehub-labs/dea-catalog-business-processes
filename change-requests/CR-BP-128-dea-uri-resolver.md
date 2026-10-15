# CR-BP-128: dea:// URI Resolver CLI Tool (T9.3)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance) - implementation
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-15
**Depends on**: CR-BP-126 (Stage 7); CR-BP-127 (dea:// URI scheme spec)
**Companion**: the dea:// URI scheme spec (`docs/entity-system/specs/07-dea-uri-scheme.md`)

## 1. Purpose

This is the T9.3 follow-on to the Entity System institutionalisation. CR-BP-127 documented the `dea://` URI scheme specification; this CR implements the resolution algorithm (§8 of the spec) as a CLI tool. The tool resolves a `dea://` URI to a file path on disk, supports legacy `dea:` ids via the migration id map, and works across the in-thread repo + the 11 sibling repos.

After this slice: any `dea://` URI can be resolved to a local file path via a single CLI command. The tool is the reference implementation of the resolution algorithm documented in CR-BP-127 §8.

## 2. The 2 deliverables

### 2.1 The resolver CLI

`scripts/dea_uri_resolver.py` (~250 lines) - the reference implementation. Features:
- URI parsing: handles both canonical ids (e.g. `processes:process-foo-bar-f3n8wb`) and legacy ids (e.g. `dea:process-foo-bar`).
- Scope resolution: looks up the scope in the cross-catalog resolution registry; falls back to the in-thread repo for `dea-catalog-business-processes`.
- Legacy id resolution: looks up the legacy id in the migration id map; resolves to the canonical id; then to the file path.
- File path computation: derives the slug from the id (descriptor only, matching the live tree's directory naming convention); the file is at `entities/v1-alpha/{slug}/{namespace}-{rest}.yaml`.
- CLI modes:
  - Default: print the file path
  - `--exists`: exit 0 if the file exists locally, 1 otherwise
  - `--fetch`: print the file contents
  - `--list`: list all known scopes
  - `--resolve`: print the path AND the canonical URI form

### 2.2 The 20-test suite

`tests/test_dea_uri_resolver.py` - 20 tests:
- 5 URI parsing tests (canonical, legacy, malformed, long-descriptor)
- 4 id rest splitting tests (PC, short BP, long BP, uppercase hash rejection)
- 3 registry + migration map tests
- 5 resolution tests (canonical, non-existent, legacy, unknown scope, malformed)
- 3 CLI tests (--list, resolve, unknown scope)
- 1 integration test (PC record resolution; skipped if no PC records)

## 3. Repository changes

| Path | Status | Notes |
|---|---|---|
| `scripts/dea_uri_resolver.py` | NEW | The CLI tool (~250 lines) |
| `tests/test_dea_uri_resolver.py` | NEW | 20 tests; 20/20 pass |
| `change-requests/CR-BP-128-dea-uri-resolver.md` | NEW | This file (the carrier CR) |
| `change-requests/README.md` | MOD | New row at top of table |
| `CHANGELOG.md` | MOD | [Unreleased] entry |
| `CATALOG.yaml` | MOD | Regenerator bump |

## 4. Acceptance criteria

- AC-01 The resolver is at `scripts/dea_uri_resolver.py` (~250 lines).
- AC-02 The 20-test suite passes.
- AC-03 The resolver handles canonical ids, legacy ids, malformed URIs, unknown scopes, and non-existent files.
- AC-04 The resolver CLI supports `--list`, `--exists`, `--fetch`, `--resolve`, and the default path-printing mode.
- AC-05 The slug computation matches the live tree's directory naming convention (descriptor only, no hash).
- AC-06 The legacy `dea:` id resolution uses the migration id map at `reconciliation/migration-id-map.yaml`.
- AC-07 D-004 (no en/em-dash, no U+2E3B) is clean across all new/modified files.
- AC-08 118a/118b/118c/123/124/125/126/127 authorship + entity-system gates remain CONFORMANT.

## 5. Test posture (live, 2026-10-15)

```
$ python3 -m pytest tests/test_dea_uri_resolver.py -v
========================================== 20 passed, 1 skipped in 1.2s ==========================================

$ python3 scripts/dea_uri_resolver.py --list
Known scopes:
  dea-catalog-business-capabilities: technehub-labs/dea-catalog-business-capabilities
  dea-catalog-business-objects: technehub-labs/dea-catalog-business-objects
  dea-catalog-business-processes: <in-thread>
  dea-catalog-organizational-units: technehub-labs/dea-catalog-organizational-units
  ...

$ python3 scripts/dea_uri_resolver.py dea://dea-catalog-business-processes/processes:pc-fa-retire-64q5p9
/home/hermes/dea-catalog-processes/entities/v1-alpha/fa-retire/processes-pc-fa-retire-64q5p9.yaml
```

## 6. What this CR is NOT

- **NOT the IANA submission.** The submission is a T9.2 follow-on (user sign-off + actual submission).
- **NOT the URI scheme promotion to Permanent.** Permanent status is a 2027-Q3 follow-on.
- **NOT a remote-fetcher.** The resolver is local-only; a remote-fetcher (git clone + checkout) is a T9.5 follow-on.
- **NOT a web resolver.** A web-based resolver (a Flask/Quart app that accepts a `dea://` URI via HTTP) is a T9.6 follow-on.
- **NOT a metadata change.** No entity, schema, or id changes.

## 7. Out-of-scope follow-ons

- **T9.2** (IANA submission): submit the IANA registration template to the IANA URI Schemes registry.
- **T9.4** (Permanent status): submit the I-D to IETF for review; achieve Permanent status.
- **T9.5** (Remote-fetcher): extend the resolver to fetch the file from the remote repository when the local clone is absent.
- **T9.6** (Web resolver): a Flask/Quart app that exposes the resolver over HTTP.

## 8. Cross-references

- **CR-BP-126** §8: the resolution algorithm.
- **CR-BP-127** §8: the dea:// URI scheme spec's resolution algorithm.
- **CR-BP-mv1**: the migration id map (3640 lines).
- **CR-BP-124** §2.3: the cross-catalog resolution registry schema.
- **DEA-ID-000**: the foundation paper.
- **CR-012**: the org-wide governance CR.
- **RFC 3986** (URI generic syntax).
- **RFC 7595** (URI scheme registration).
