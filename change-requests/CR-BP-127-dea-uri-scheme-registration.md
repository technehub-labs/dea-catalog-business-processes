# CR-BP-127: `dea://` URI Scheme Registration (T9 follow-on)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance) - pinned rule
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-15
**Depends on**: CR-BP-121..126 (Stages 1-7 of the entity system)
**Resolves**: CR-BP-121 Gap Register U-01; CR-BP-126 §9 (URI scheme registration)

## 1. Purpose

This is the T9 follow-on to the General Entity System institutionalisation. CR-BP-126 (Stage 7) defined the canonical URI form `dea://{scope}/{id}` and the resolvable form (GitHub URL); this CR drafts the full URI scheme specification + the IANA registration template (per RFC 7595 §7.4) and proposes the registration path (Provisional first, then Permanent).

After this slice: the `dea://` URI scheme has a complete specification ready for IANA submission. The IANA registration is a 30-day follow-on (T9.2) once the user signs off on the specification.

## 2. The 1 deliverable

### 2.1 The `dea://` URI scheme specification

`docs/entity-system/specs/07-dea-uri-scheme.md` (~10K) - the full URI scheme specification. Covers:
- The scheme name (`dea`, ASCII, lowercase).
- The status (Provisional; pending Permanent).
- The applicability (OpenDEAM entity catalog references).
- The authority, contacts, and change control (TechNeHub Labs; emmanuel@otchere.com).
- The scheme syntax (per the corrected IDM-001 pattern; BASE32 hash; no query/fragment).
- The scheme semantics (canonical identifier; not directly resolvable; resolved via the cross-catalog resolution registry).
- The encoding and character set (ASCII only at this time).
- The resolution algorithm (deterministic; cross-catalog registry lookup + git fetch + id verification).
- The security considerations (URI spoofing, repository impersonation, DoS).
- The privacy considerations (no personal data in the URI; the entity may contain personal data).
- The interoperability considerations (HTTP/HTTPS conversion; git integration; cross-scheme references).
- The examples (RFC 7595 §7.4 example format).
- The IANA registration template (RFC 7595 §7.4 format).
- The registration procedure (Provisional first, then Permanent via mailing list review).
- The timeline (2026-10-15 spec drafted; 2026-11-01 IANA submission; 2027 Permanent status).

## 3. The IANA submission timeline

| Date | Event |
|---|---|
| 2026-10-15 (this PR) | Scheme specification drafted, IANA template prepared |
| 2026-11-01 (planned) | IANA submission for Provisional registration |
| 2026-12-01 (planned) | Provisional status confirmed by IANA |
| 2027-Q1 (planned) | I-D submitted to IETF for review |
| 2027-Q3 (planned) | Permanent status achieved |

The IANA submission is a follow-on slice (T9.2) that requires user sign-off. This CR is the SPEC + the template; the actual submission is a separate decision.

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `docs/entity-system/specs/07-dea-uri-scheme.md` | NEW | The full URI scheme specification (~10K) |
| `change-requests/CR-BP-127-dea-uri-scheme-registration.md` | NEW | This file (the carrier CR) |
| `change-requests/README.md` | MOD | New row at top of table |
| `CHANGELOG.md` | MOD | [Unreleased] entry |
| `CATALOG.yaml` | MOD | Regenerator bump |

## 5. Acceptance criteria

- AC-01 The `dea://` URI scheme specification is filed at `docs/entity-system/specs/07-dea-uri-scheme.md`.
- AC-02 The IANA registration template (RFC 7595 §7.4 format) is in the spec.
- AC-03 The scheme syntax is consistent with the corrected IDM-001 pattern (per CR-BP-126).
- AC-04 The scheme semantics are consistent with the U-01 standard (per CR-BP-126 §2-3).
- AC-05 The security and privacy considerations are addressed (per RFC 7595 §3.7).
- AC-06 D-004 (no en/em-dash, no U+2E3B) is clean across all new/modified files.
- AC-07 118a/118b/118c/123/124/125/126 authorship + entity-system gates remain CONFORMANT.
- AC-08 The IANA submission template is ready to be sent to the IANA URI Schemes registry.

## 6. Test posture (live, 2026-10-15)

This is a SPEC-only slice. There are no test changes. The 32 entity-system tests + 15 IDM-001 tests + 118a/118b/118c authorship gates remain green.

## 7. What this CR is NOT

- **NOT the IANA submission.** The submission is a T9.2 follow-on (user sign-off + actual submission).
- **NOT the cross-catalog resolver tool.** The tool is a T9.3 follow-on (a CLI that resolves a `dea://` URI to the file path on disk).
- **NOT the URI scheme promotion to Permanent.** Permanent status is a 2027-Q3 follow-on (after mailing list review).
- **NOT a metadata change.** No entity, schema, or id changes.
- **NOT a metamodel change.** Out of scope (different repo).

## 8. Out-of-scope follow-ons

- **T9.2** (IANA submission): submit the IANA registration template to the IANA URI Schemes registry.
- **T9.3** (Resolver tool): implement `scripts/dea_uri_resolver.py` - a CLI that resolves a `dea://` URI to the file path on disk.
- **T9.4** (Permanent status): submit the I-D to IETF for review; achieve Permanent status.

## 9. Cross-references

- **CR-BP-121..126**: the 7 stages of the General Entity System institutionalisation.
- **CR-BP-126** §2.1: the U-01 Cross-Catalog URI Standard.
- **DEA-ID-000**: the foundation paper.
- **CR-012**: the org-wide governance CR.
- **RFC 3986** (URI generic syntax).
- **RFC 7595** (URI scheme registration).
- **RFC 2119** (key words for RFCs).
- **`reconciliation/cross-catalog-resolution.yaml`**: the resolution registry.
