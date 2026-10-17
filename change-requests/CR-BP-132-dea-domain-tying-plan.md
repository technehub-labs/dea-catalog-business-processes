# CR-BP-132: dea:// Domain Tying Plan (T9.10; precursor to T9.2, T9.4, T9.8, T9.9)

**Status**: Proposed (this PR; user-approved 2026-10-15)
**Layer**: Cross-cutting (catalog governance) - pinned rule
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-15
**Depends on**: CR-BP-127 (dea:// URI scheme spec); CR-BP-126 (U-01 Cross-Catalog URI Standard)
**Companion**: T9.2 IANA Submission; T9.4 IETF I-D Submission; T9.8 Production Server; T9.9 Sync Daemon
**Resolves**: the dea:// URI scheme's authority + access control model (per user directive 2026-10-15)

## 1. Purpose

This is the precursor to the dea:// URI scheme's authority and access control model. Per the user directive 2026-10-15, the URI references may be **privately tied to** `technehub-labs.github.io` or `technehub.com` domain. This CR captures the plan as a dependency to:

- **T9.2** IANA Submission (the scheme registration lists the authority domain).
- **T9.4** IETF I-D Submission (the I-D declares the controlling organization and domain).
- **T9.8** Production Server (the production server serves the chosen domain).
- **T9.9** Sync Daemon (the daemon authenticates against the chosen domain).
- The cross-catalog resolution registry (every catalog's `url_template` references the chosen domain).
- The dea:// URI scheme spec at `docs/entity-system/specs/07-dea-uri-scheme.md` (the IANA template in §13 lists the authority domain).

The plan is approved by the user on 2026-10-15 with a note: the plan may be replayed and revised later; the intent is to align with the release assets when the time comes.

## 2. The 7 sections

### 2.1 Domain selection

Two options are on the table:

| Option | Pros | Cons |
|---|---|---|
| `technehub-labs.github.io` | free; auto-HTTPS; tied to the org; already exists; matches the GitHub Pages site (per memory #183) | no custom DNS; can be deprecated; GitHub-controlled |
| `technehub.com` | custom domain; full DNS authority; brand control | cost + maintenance; separate from GitHub |

**Default recommendation**: `technehub-labs.github.io`. Reasons: matches the existing GitHub Pages site, no new infrastructure, and aligns with how `technehub-labs` is already structured. The alternative is both: `technehub.com` is the canonical + `technehub-labs.github.io` is the mirror.

### 2.2 Authority model

Per CR-BP-127 §4 (already drafted), the scheme owner is **TechNeHub Labs** (Emmanuel A. Otchere, on behalf of TechNeHub Labs). The IANA submission lists the authority domain. The chosen domain hosts the scheme's authoritative records, including the `.well-known/dea` discovery endpoint (per RFC 8615).

### 2.3 Resolvable form

The current resolvable form is the **GitHub URL** (e.g., `https://github.com/technehub-labs/dea-catalog-processes/blob/main/entities/...`). The proposed change: replace the GitHub URL form with the **chosen domain's URL form** (e.g., `https://technehub-labs.github.io/dea-catalog-processes/entities/...`).

This is a per-catalog change in the cross-catalog resolution registry: each catalog gains a `url_template` field that references the chosen domain.

### 2.4 Access control (the "private" interpretation)

The phrase "privately tied to a domain" is ambiguous. Two interpretations are on the table:

- **Interpretation A** (brand/authority): the dea:// scheme is owned by TechNeHub Labs; the resolvable URL is on the chosen domain. The resolution itself is **public** (anyone can resolve).
- **Interpretation B** (access control): the resolvable URL is **private** (token-gated); only authenticated callers can fetch.

**Default recommendation**: Interpretation A (brand/authority, public resolution). Reasons:
- The current entity records are public (no access control in the live tree).
- The entity-system standard's gate (per CR-BP-123) is blocking for new admissions, but the resolution is public.
- The "private" aspect is the **authority** (only TechNeHub Labs registers new entities via the contribution flow), not the **access** (anyone can read public entities).

For sensitive entities: the entity-system gate's review-retained verdict (per EGV-011 + CR-BP-125) carries an `access: private` marker; the resolver checks the marker and gates the fetch. This is a follow-on, not part of T9.10.

### 2.5 IANA registration impact

The IANA template (CR-BP-127 §13) currently lists "TechNeHub Labs + emmanuel@otchere.com". The template MUST also list the **authority domain** (e.g., "Authority: technehub-labs.github.io" or "technehub.com"). The "Change controller" field (per RFC 7595 §7.4) lists the domain. The mailing list for change control is tied to the domain.

This means: T9.2 (IANA submission) is **blocked until this plan is approved and implemented**. Same for T9.4 (IETF I-D).

### 2.6 Per-repo domain configuration

The cross-catalog resolution registry (`reconciliation/cross-catalog-resolution.yaml`) gains a `domain` field per catalog. Each catalog's `url_template` references the domain. The `dea://` resolver uses the domain in the resolvable form.

Per-catalog mapping (with `technehub-labs.github.io` as the chosen domain):

| Catalog | Domain-prefixed URL |
|---|---|
| `dea-catalog-processes` | `technehub-labs.github.io/dea-catalog-processes` |
| `dea-catalog-business-capabilities` | `technehub-labs.github.io/dea-catalog-business-capabilities` |
| `dea-catalog-business-objects` | `technehub-labs.github.io/dea-catalog-business-objects` |
| `dea-catalog-organizational-units` | `technehub-labs.github.io/dea-catalog-organizational-units` |
| `dea-catalog-actors` | `technehub-labs.github.io/dea-catalog-actors` |
| `dea-catalog-stakeholders` | `technehub-labs.github.io/dea-catalog-stakeholders` |
| `dea-metamodel` | `technehub-labs.github.io/dea-metamodel` |
| `dea-architecture-framework` | `technehub-labs.github.io/dea-architecture-framework` |

### 2.7 Migration plan

7 phases, each a separate CR:

| Phase | Action | Carrier |
|---|---|---|
| 1 | Add `domain` field to the cross-catalog resolution registry | **CR-BP-132** (this CR) |
| 2 | Update the dea:// URI scheme spec (CR-BP-127) with the authority domain | CR-BP-133 |
| 3 | Update `dea_uri_resolver.py` + `dea_uri_web.py` + `dea_uri_sync.py` to use the domain | CR-BP-134 |
| 4 | IANA submission (T9.2) with the authority domain | T9.2 (user-action) |
| 5 | IETF I-D submission (T9.4) with the authority domain | T9.4 (2027-Q1) |
| 6 | Production server (T9.8) on the chosen domain | T9.8 |
| 7 | Sync daemon (T9.9) authenticated against the domain | T9.9 |

## 3. Release alignment (user directive 2026-10-15)

Per the user directive 2026-10-15:

> "Approved plan for now so we should be able to play it back later and make changes. It's imports to note the intent to ensure alignment with the release assets when the times comes."

The intent: the plan may be **replayed** (re-read and revised later) and the changes should **align with the release assets** when the time comes. The release assets are:

- `CHANGELOG.md` (the in-repo changelog; updated per CR per the established pattern).
- `CATALOG.yaml` (regenerated per CR per the established pattern).
- `CITATION.cff` (the author + version metadata; updated per release).
- Git tags (annotated tags per CR-BP-mv1 + per release).
- GitHub Releases (per the established pattern; per memory #167).
- The dea:// URI scheme's authority domain declaration in the IANA registration (T9.2).

When the time comes to ship a release that incorporates this plan, the release assets must be updated **in sync** (per memory #133: peakable v3 version management; version hygiene is a production-quality concern, not a suggestion). The release procedure:

1. Pick a branch (this CR's branch or a follow-on).
2. Update `CHANGELOG.md` + `CITATION.cff` in one atomic commit.
3. Open a PR; after merge, create annotated tags against the historically-accurate merge commits (per memory #167).
4. Cut a `gh release create` for each new tag.

The plan is **replayable**: this CR doc is the source of truth. The kanban card (T9.10) is the live status; the CR doc is the formal record. The plan may be revised by amending this CR or by issuing a follow-on CR.

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `change-requests/CR-BP-132-dea-domain-tying-plan.md` | NEW | This file (the carrier CR + the plan) |
| `change-requests/README.md` | MOD | New row at top of table |
| `CHANGELOG.md` | MOD | [Unreleased] entry |
| `CATALOG.yaml` | MOD | Regenerator bump |

**No code changes** in this CR. The plan is the deliverable; the implementation is in the follow-on CRs (CR-BP-133, CR-BP-134, etc.).

## 5. Acceptance criteria

- AC-01 This CR doc captures the 7-section plan.
- AC-02 The user has approved the plan (per 2026-10-15 directive).
- AC-03 The release alignment section documents the intent to align with the release assets.
- AC-04 The kanban card (T9.10) references this CR for replay.
- AC-05 D-004 (no en/em-dash, no U+2E3B) is clean across all new/modified files.
- AC-06 118a/118b/118c/123/124/125/126/127/128/129/130/131 authorship + entity-system gates remain CONFORMANT.

## 6. Test posture (live, 2026-10-15)

This is a planning CR; no test changes. The 93-test suite for the dea:// programme remains green.

## 7. What this CR is NOT

- **NOT a code change.** The implementation is in CR-BP-133, CR-BP-134, etc.
- **NOT the IANA submission.** T9.2 is the user-action follow-on (blocked until CR-BP-132 + CR-BP-133 land).
- **NOT the IETF I-D submission.** T9.4 is the 2027-Q1 follow-on.
- **NOT the production server.** T9.8 is the operational follow-on.
- **NOT a metadata change.** No entity, schema, or id changes.

## 8. Out-of-scope follow-ons

- **CR-BP-133**: update the dea:// URI scheme spec (CR-BP-127) with the authority domain.
- **CR-BP-134**: update the resolver scripts (CR-BP-128, -129, -130, -131) to use the domain.
- **T9.2** (IANA Submission): submit the IANA registration template with the authority domain.
- **T9.4** (IETF I-D Submission): submit the Internet-Draft with the authority domain.
- **T9.8** (Production Server): wrap the web resolver in a production WSGI/ASGI server on the chosen domain.
- **T9.9** (Sync Daemon): long-running daemon authenticated against the chosen domain.
- **Per-catalog disposition registers**: per-repo work in the 11 sibling repos (per the entity-system cascade).

## 9. Cross-references

- **CR-BP-127** (T9.1): the dea:// URI scheme spec.
- **CR-BP-126** (Stage 7): the U-01 Cross-Catalog URI Standard.
- **CR-012** (org-wide governance CR): the 12 EGV-001..012 normative requirements.
- **DEA-ID-000**: the foundation paper.
- **T9.2, T9.4, T9.8, T9.9**: the user-action and operational follow-on cards.
- **Memory #133**: peakable v3 version management (version hygiene is production-quality).
- **Memory #167**: release cut pattern (annotated tags + gh release create).
- **Memory #183**: technehub-labs.github.io as the GitHub Pages site.
- **RFC 7595** (URI scheme registration): the IANA template format.
- **RFC 8615** (Well-Known URIs): the `.well-known/dea` discovery endpoint.
