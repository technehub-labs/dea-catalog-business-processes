# `dea://` URI Scheme Specification (CR-BP-127; U-01 follow-on)

> **T9 deliverable.** The full URI scheme specification for the `dea://` cross-catalog reference scheme. This document is the IANA submission template (per RFC 7595 §7.4) for the `dea://` scheme registration. Companion: the Cross-Catalog URI Standard (`specs/06-cross-catalog-uri.md`), the Identity Standard IS-006, the Relationship Standard RS-004, the cross-catalog resolution registry at `reconciliation/cross-catalog-resolution.yaml`.

## 1. Scheme name

```
dea
```

The scheme name is `dea` (lowercase, ASCII). It is registered as a **Permanent** URI scheme per RFC 7595.

## 2. Status

**Provisional** (initial registration; will be promoted to **Permanent** after mailing list review per RFC 7595 §7.2).

## 3. Applicability

The `dea://` URI scheme identifies entities in the OpenDEAM entity catalog. Each entity has a stable identity (per EGV-002 + the Identity Standard) and is associated with a single catalog (a `technehub-labs/*` repository). The URI is the canonical identifier of the entity; the URI is not directly resolvable but is resolved through the OpenDEAM cross-catalog resolution registry (`reconciliation/cross-catalog-resolution.yaml`).

The scheme is for use in:
- Entity records (YAML files in `entities/v1-alpha/**`).
- Cross-catalog relationships (per RS-004).
- Documentation (cross-references between catalogs).
- Tooling (a CLI resolver that fetches the file by URI).

## 4. Authority, contacts, and change control

- **Scheme owner**: Emmanuel A. Otchere (emmanuel@otchere.com) on behalf of TechNeHub Labs.
- **Change control**: TechNeHub Labs; significant changes require a CR in `dea-governance/change-requests/CR-*.md` and a public review period of at least 14 days.
- **Bug reports**: emmanuel@otchere.com.
- **Mailing list**: TBD (will be established at `dea-uri@technehub-labs.org` before permanent registration).

## 5. Scheme syntax

```
dea-uri        = "dea://" scope "/" entity-id
scope          = 1*( ALPHA / DIGIT / "-" )
entity-id      = canonical-id / legacy-id
canonical-id   = namespace-prefix ":" canonical-form
legacy-id      = "dea:" legacy-form
canonical-form = type "-" descriptor *( "-" descriptor-segment ) "-" base32hash
type           = 1*ALPHA
descriptor     = 1*ALPHA
base32hash     = 6 base32-chars
base32-chars   = "0" / "1" / "2" / "3" / "4" / "5" / "6" / "7" / "8" / "9" /
                 "a" / "b" / "c" / "d" / "e" / "f" / "g" / "h" / "i" / "j" /
                 "k" / "l" / "m" / "n" / "o" / "p" / "q" / "r" / "s" / "t" /
                 "u" / "v" / "w" / "x" / "y" / "z"
                 (per IDM-004 strict BASE32 alphabet: no 0/o, 1/l confusion)
```

The `dea-uri` is the only URI form. There is no query or fragment component.

### 5.1 Example URIs

| Reference | URI |
|---|---|
| A canonical BC record | `dea://dea-catalog-business-capabilities/capabilities:capability-workforce-planning-b43rhm` |
| A canonical BP record | `dea://dea-catalog-business-processes/processes:process-manage-customer-relationship-f3n8wb` |
| A legacy `dea:` id | `dea://dea-catalog-business-processes/dea:process-manage-customer-relationship` |
| A cross-catalog reference (BP -> BC) | `dea://dea-catalog-business-capabilities/capabilities:capability-financial-stewardship-c7xtfk` |

## 6. Scheme semantics

The `dea://` URI is the **canonical identifier** of an entity in the OpenDEAM entity catalog. The URI is not directly resolvable in the HTTP sense; it is resolved through the OpenDEAM cross-catalog resolution registry.

The semantics of the URI are:
- The entity exists in the catalog whose identity_scope is `scope`.
- The entity's id (within the catalog) is `entity-id`.
- The entity's identity is stable across lifecycle state changes (per EGV-004).
- The entity's identity is stable across catalog version changes (per EGV-007).

## 7. Encoding and character set

The `dea-uri` uses the URI generic syntax (RFC 3986). The scheme-specific part is restricted to ASCII (no internationalization at this time; the entity id is ASCII by design). The fragment identifier is not used. The query is not used.

Future versions of this specification MAY add internationalization (per RFC 3987 IRI), but the current version is URI-only.

## 8. Resolution algorithm

A `dea://` URI is resolved as follows:

1. Parse the URI: extract `scope` and `entity-id`.
2. Look up `scope` in the cross-catalog resolution registry.
3. If the scope is not found, the URI is unresolvable; the resolver returns an error.
4. Extract the repository, id_format, and path_template from the registry entry.
5. Determine the file path using the path_template + the entity's id.
6. Fetch the file from the repository (via HTTPS or git).
7. Verify the entity's id matches the URI's id.
8. If the entity is not found or the id mismatch, the URI is unresolvable.

The resolution algorithm is deterministic and reproducible. A reference implementation is at `scripts/dea_uri_resolver.py` (a CLI tool, future work; T9 follow-on).

## 9. Security considerations

The `dea://` URI scheme identifies entities in a public catalog. The security considerations are:

- **Information disclosure**: the URI is a public identifier; it does not contain secrets. The referenced entity may be public or restricted; the resolver is responsible for enforcing access control.
- **URI spoofing**: an attacker cannot register a new entity that the URI points to without write access to the catalog repository. The repository is on GitHub with branch protection; the risk is low.
- **Repository impersonation**: the resolver MUST verify the repository's identity via the cross-catalog resolution registry. The registry is signed (per TechNeHub Labs governance; future work).
- **Cross-catalog trust**: a cross-catalog reference from catalog A to catalog B assumes that catalog B's identity_scope is correctly declared. A malicious catalog could impersonate another catalog's identity_scope. The registry's repository identity verification mitigates this risk.
- **Denial of service**: the resolver is rate-limited per RFC 6585; the rate limit is documented in the cross-catalog resolution registry.

## 10. Privacy considerations

The `dea://` URI references public catalog entities. The privacy considerations are:

- The URI itself does not contain personal data.
- The referenced entity may contain personal data (e.g., an actor's name); the catalog's privacy policy applies.
- The resolver does not log the URIs it resolves (no audit trail at the URI level; the GitHub access logs are the audit trail).

## 11. Interoperability considerations

The `dea://` URI scheme is interoperable with:

- HTTP and HTTPS: a `dea://` URI can be converted to an HTTPS URL via the cross-catalog resolution registry.
- Git: a `dea://` URI can be resolved to a git commit hash via the cross-catalog resolution registry.
- Other URI schemes: a `dea://` URI can be cross-referenced from other URI schemes (e.g., a `https://` URL that links to a `dea://` URI in its body).

## 12. Examples (RFC 7595 §7.4 example format)

The `example` URI scheme (RFC 7595 §8) is a placeholder; the `dea://` URI scheme is a real scheme with concrete examples:

```
dea://dea-catalog-business-capabilities/capabilities:capability-workforce-planning-b43rhm
dea://dea-catalog-business-processes/processes:process-manage-customer-relationship-f3n8wb
dea://dea-catalog-business-processes/dea:process-manage-customer-relationship
dea://dea-metamodel/dea:entity-type-business-capability
```

## 13. IANA registration template (RFC 7595 §7.4)

The IANA registration template per RFC 7595 §7.4:

```
URI Scheme Name: dea
Status: Provisional (pending Permanent)
Description: The OpenDEAM cross-catalog entity reference scheme. Identifies
  entities in the OpenDEAM entity catalog (a set of technehub-labs/* GitHub
  repositories) by stable id, with cross-catalog resolution via the
  OpenDEAM cross-catalog resolution registry.
Scheme Syntax: See Section 5 of the scheme specification.
Scheme Semantics: See Section 6 of the scheme specification.
Encoding Considerations: ASCII only (no internationalization at this time).
Applications/Protocols That Use This Scheme: OpenDEAM entity catalogs.
Interoperability Considerations: See Section 11 of the scheme specification.
Security Considerations: See Section 9 of the scheme specification.
Contact: Emmanuel A. Otchere <emmanuel@otchere.com>
Author/Change Controller: TechNeHub Labs.
References: RFC 3986 (URI generic syntax); RFC 7595 (URI scheme registration);
  CR-BP-121 (OpenDEAM entity system Stage 1);
  CR-BP-122 (OpenDEAM entity system Stage 2);
  CR-BP-126 (OpenDEAM entity system Stage 7 - legacy id reconciliation);
  CR-BP-127 (this CR - dea:// URI scheme registration).
```

## 14. Registration procedure

The registration procedure is:

1. **Submit the IANA registration template** (Section 13) to the IANA URI Schemes registry.
2. **Initial status**: Provisional (per RFC 7595 §4).
3. **Mailing list review**: within 6 months of the initial registration, submit the dea:// scheme to the `apps-discuss@ietf.org` mailing list for review (per RFC 7595 §7.2).
4. **Permanent status**: after mailing list review + IESG approval, the status is promoted to Permanent (per RFC 7595 §3).
5. **Document publication**: the scheme specification is published as an Internet-Draft (I-D) for the IETF review; the I-D is the canonical reference for the scheme.

## 15. Timeline

- **2026-10-15 (this CR)**: scheme specification drafted, IANA template prepared.
- **2026-11-01 (planned)**: IANA submission for Provisional registration.
- **2027-Q1 (planned)**: I-D submitted to IETF for review.
- **2027-Q3 (planned)**: Permanent status achieved.

## 16. Cross-references

- **CR-BP-121** (Stage 1): the 4 doc outputs that frame the entity system.
- **CR-BP-122** (Stage 2): the 5 normative spec docs.
- **CR-BP-126** (Stage 7): the U-01 Cross-Catalog URI Standard.
- **CR-012** (org-wide governance CR): the 12 EGV-001..012 normative requirements.
- **DEA-ID-000**: the foundation paper.
- **Identity Standard IS-006**: cross-catalog identity_scope declaration.
- **Relationship Standard RS-004**: cross-catalog reference resolution.
- **`reconciliation/cross-catalog-resolution.yaml`**: the resolution registry.
- **`reconciliation/migration-id-map.yaml`**: the 3640-line legacy id migration registry (CR-BP-mv1).
- **RFC 3986** (URI generic syntax): the foundational URI standard.
- **RFC 7595** (URI scheme registration): the registration procedure.
- **RFC 2119** (key words for RFCs): the MUST/SHOULD/MAY conventions.
- **RFC 8615** (Well-Known URIs): future work for `/.well-known/dea` discovery.

## 17. Document metadata

- **CR**: CR-BP-127
- **Status**: Proposed (this PR)
- **Layer**: Cross-cutting (catalog governance)
- **Owner**: Emmanuel A. Otchere
- **Date**: 2026-10-15
- **Depends on**: CR-BP-121..126 (the 7 stages of the entity system)
- **Companion**: the dea:// URI scheme specification (this file)
