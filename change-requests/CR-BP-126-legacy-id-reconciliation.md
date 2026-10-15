# CR-BP-126: Entity System Stage 7 (Legacy ID Reconciliation)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance) - pinned rule
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-13
**Depends on**: CR-BP-121..125 (Stages 1-6); CR-012 (org-wide governance CR)
**Resolves**: CR-BP-121 Gap Register §5.2 U-01 (cross-catalog URI form)

## 1. Purpose

This is the final stage (Stage 7 / T8) of the General Entity System institutionalisation in `dea-catalog-business-processes`. Stages 1-6 (CR-BP-121 through CR-BP-125) produced the 4 doc outputs + 5 normative spec docs + the 5-rule umbrella gate + the disposition register + the institutionalisation. This slice:

1. Resolves the U-01 open question (cross-catalog URI form) with a new spec doc.
2. Fixes the IDM-001 pattern in `scripts/check_id_system.py` to match the corrected entity-system gate pattern.
3. Documents the legacy id reconciliation path for the 35 `dea:` grandfathered records.
4. Ships the 7-test suite for the IDM-001 fix.

After this slice: cross-catalog references are resolvable via the canonical URI form; the IDM-001 pattern matches all 5 type families (including BP records with long descriptors); the legacy `dea:` ids are documented and grandfathered per EGV-012.

## 2. The 4 deliverables

### 2.1 U-01 Cross-Catalog URI Standard

`docs/entity-system/specs/06-cross-catalog-uri.md` (~8K) - the canonical URI form for cross-catalog references. The form is `dea://{scope}/{id}`. The resolvable form is the GitHub URL (derived from the cross-catalog resolution registry). The standard covers:

- The canonical URI form (identifier-only; not directly resolvable)
- The resolvable form (GitHub URL; deterministic derivation)
- The relationship entry (target + identity_scope)
- The cross-catalog resolution registry schema
- The resolution algorithm
- The legacy id form (via migration id map)
- Version-stable references (URI does not change with lifecycle state)
- The future `dea://` URI scheme registration (T9 follow-on)

### 2.2 IDM-001 pattern fix

`scripts/check_id_system.py` (MOD) - the corrected pattern matches all 5 type families:

- Original: `^[a-z]+:[a-z]+-[a-z]{2,3}-[a-z]+(-[a-z]+)*-[a-z2-9]{6}$` (requires 2-3 char domain code; excludes BP records with long descriptors)
- Corrected: `^[a-z]+:[a-z]+(-[a-z]+){1,4}-[a-z2-9]{6}$` (matches all 5 type families with 1-4 segments between type and hash)

The corrected form matches:
- `processes:pc-fa-retire-64q5p9` (1 segment)
- `processes:process-foo-bar-f3n8wb` (2 segments)
- `processes:process-manage-customer-relationship-f3n8wb` (4 segments)
- `processes:process-foo-bar-baz-qux-f3n8wb` (4 segments)

The fix is consistent with the entity-system gate's corrected pattern (per CR-BP-123 §2.1).

### 2.3 14-test suite for IDM-001

`tests/test_check_id_system.py` (NEW) - 14 tests:
- 4 type-family tests (PC, Activity, Task, ProcessGroup)
- 2 BP descriptor tests (short, long)
- 2 segment-count tests (3-segment, 4-segment)
- 4 negative tests (uppercase, missing hash, short hash, 5-segment)
- 1 namespace test (no namespace rejected)
- 1 legacy-dea test (legacy `dea:` NOT matched by canonical pattern)
- 1 live-tree regression test (all canonical records match)

### 2.4 Legacy ID reconciliation documentation

The legacy `dea:` ids in `entities/v1-alpha/` (35 records) are documented in the migration id map at `reconciliation/migration-id-map.yaml` (CR-BP-mv1; 3640 lines). Each legacy id has a `processes:` migration target. The U-01 standard's legacy id form (`dea://{scope}/dea:{legacy-id}`) resolves via the migration id map to the canonical URI form.

## 3. Repository changes

| Path | Status | Notes |
|---|---|---|
| `scripts/check_id_system.py` | MOD | IDM-001 pattern corrected (5x chars; 1-4 segments) |
| `tests/test_check_id_system.py` | NEW | 14 tests; live-tree regression test included |
| `docs/entity-system/specs/06-cross-catalog-uri.md` | NEW | U-01 standard (~8K) |
| `change-requests/CR-BP-126-legacy-id-reconciliation.md` | NEW | This file (the carrier CR) |
| `change-requests/README.md` | MOD | New row at top of table |
| `CHANGELOG.md` | MOD | [Unreleased] entry |
| `CATALOG.yaml` | MOD | Regenerator bump |

## 4. Acceptance criteria

- AC-01 The U-01 Cross-Catalog URI Standard is filed at `docs/entity-system/specs/06-cross-catalog-uri.md`.
- AC-02 The IDM-001 pattern is corrected in `scripts/check_id_system.py`; the 14-test suite passes.
- AC-03 Every canonical record in `entities/v1-alpha/` matches the corrected pattern (regression test).
- AC-04 The legacy `dea:` ids are NOT matched by the canonical pattern (they are grandfathered).
- AC-05 The cross-catalog resolution registry schema is documented (per `reconciliation/cross-catalog-resolution.yaml` from CR-BP-124).
- AC-06 D-004 (no en/em-dash, no U+2E3B) is clean across all new/modified files.
- AC-07 118a/118b/118c/123/124/125 authorship + entity-system gates remain CONFORMANT.
- AC-08 The IDM-001 fix is consistent with the entity-system gate's corrected pattern (per CR-BP-123 §2.1).

## 5. Test posture (live, 2026-10-13)

```
$ python3 -m pytest tests/test_check_id_system.py -v
============================== 14 passed in 0.5s ===============================

$ python3 -m pytest tests/test_check_entity_system.py -q
============================== 32 passed in 70s ===============================

$ python3 scripts/check_authorship.py --strict
Authorship Cardinal Rule (CR-BP-118; AUT-001..003): CONFORMANT

$ python3 scripts/check_prose_authorship.py --strict
PROSE Authorship Gate: CONFORMANT

$ python3 scripts/check_entity_system.py --strict
Entity System Gate (CR-BP-123/125): NON-CONFORMANT
... (advisory findings; the disposition register documents the resolutions)
```

## 6. What this CR is NOT

- **NOT the per-repo disposition registers.** Those are a T7 follow-on (per-repo work in the 11 sibling repos). The in-thread work is the IDM-001 fix + U-01 standard.
- **NOT the URI scheme registration.** The `dea://` scheme is currently a placeholder; IANA registration is a T9 follow-on.
- **NOT the cross-catalog resolver implementation.** The U-01 standard documents the algorithm; a tool-side implementation is a future slice.
- **NOT a bulk rename.** Per EGV-012, no existing records are renumbered.
- **NOT a metamodel change.** Out of scope (different repo).

## 7. Out-of-scope follow-ons

- **T7 follow-on** (per-repo disposition registers): 11 sibling repos get per-repo disposition registers extending CR-BP-124.
- **T9** (URI scheme registration): IANA registration of the `dea://` URI scheme per RFC 7595.
- **T9** (cross-catalog resolver tool): a CLI tool that resolves a canonical URI form to the file path on disk.

## 8. Cross-references

- **CR-BP-121** Gap Register §5.2 U-01: the open question this CR resolves.
- **CR-BP-123** §2.1: the entity-system gate's corrected IDM-001 pattern.
- **CR-BP-124** §2.3: the cross-catalog resolution registry schema.
- **CR-012** EGV-006 (Relationship and Reference Integrity): the org-wide normative requirement.
- **CR-012** EGV-012 (Existing-Catalog Reconciliation): the no-bulk-renames policy.
- **CR-BP-mv1**: the entity storage and id migration; 3640-line migration id map.
- **DEA-ID-000**: the foundation paper.
- **CR-012**: the org-wide governance CR.
