# CR-BP-121: General Entity System Stage 1 (Reconnaissance + Charter)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance) - pinned rule
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-13
**Renumbered from**: CR-BP-16 (the user-provided doc; CR-BP-16 was a tentative identifier per its own numbering note; renumbered to CR-BP-121 because CR-BP-116..118 are all taken by existing CRs and CR-BP-119/120 are reserved)
**Depends on**: DEA-ID-000 (foundation paper, `dea-governance/docs/design/entity-system-foundation.md`); CR-012 (org-wide governance CR, `dea-governance/change-requests/CR-012-org-wide-entity-governance.md`)
**Companion**: CR-BP-122 (Stage 2 Specifications); CR-BP-123 (Stage 3-4 Reference Implementation); CR-BP-124 (Stage 5 Catalog Adoption); CR-BP-125 (Stage 6 Institutionalisation)

## 1. Purpose

This is the Stage 1 slice of the General Entity System institutionalisation in `dea-catalog-business-processes`. It produces the 4 doc outputs specified in DEA-ID-000 §7 (Recommended next step):

1. **Entity System Charter** (`docs/entity-system/00-charter.md`): the normative scope, principles, authority boundaries, and applicability.
2. **Existing Decisions and Gap Register** (`docs/entity-system/01-existing-decisions-and-gap-register.md`): what is already established, what is missing, what disposition is recommended.
3. **Normative Design Proposal** (`docs/entity-system/02-normative-design-proposal.md`): the 5 normative decisions (identity, contract, relationships, lifecycle, conformance).
4. **Implementation and Adoption Plan** (`docs/entity-system/03-implementation-and-adoption-plan.md`): ordered follow-on CRs, acceptance criteria, migration policy, CI enforcement.

This slice is **non-destructive**: 0 entity changes, 0 schema changes, 0 bulk renames. The Stage 1 outputs are the foundation for Stages 2-6 (which ship the specs, the gate, the disposition register, and the institutionalisation).

## 2. Scope

### 2.1 In scope (this PR)

- The 4 doc outputs in `docs/entity-system/`.
- The carrier CR (this file).
- `change-requests/README.md` row (new entry).
- `CHANGELOG.md` entry.
- `CATALOG.yaml` regeneration after the above edits.

### 2.2 Out of scope (this PR)

- The 5 normative specs (Stage 2, CR-BP-122).
- The umbrella gate `scripts/check_entity_system.py` (Stage 3-4, CR-BP-123).
- The disposition register (Stage 5, CR-BP-124).
- The institutionalisation (Stage 6, CR-BP-125).
- The cross-repo cascade (T7 of the umbrella programme).
- The legacy id reconciliation (T8 of the umbrella programme).

## 3. Numbering note

The user-provided doc was named `CR-BP-16.md` with a "Numbering note: CR-BP-16 is a proposed identifier. Confirm availability against the repository's authoritative CR registry before admission." On 2026-10-13:

- CR-BP-115: admitted (admission-authority marker)
- CR-BP-116: parked (release-history-reset)
- CR-BP-117: admitted (entity-id-convention-clarity)
- CR-BP-118: admitted (authorship-cardinal-rule, 118a/b/c)
- CR-BP-119 / CR-BP-120: not yet used
- CR-BP-16: tentative; would collide with the existing CR-BP-mv1 family that uses bare numeric identifiers in the 100s (e.g. CR-BP-16 was historically the BP Identity Family precedent doc, now superseded by CR-BP-04)

Per the user's DP-5 ("Renumber to CR-BP-116+ (or higher if 116 is now taken by the parked release-history CR)"), the new number is **CR-BP-121**. The next-free number after CR-BP-120.

## 4. The 4 doc outputs

### 4.1 Entity System Charter (`docs/entity-system/00-charter.md`)

- Purpose: establish the General Entity System as a first-class architectural concern
- Applicability: all entity records in `entities/v1-alpha/**`, `contexts/v1-alpha/**`, future catalog versions
- Authority boundaries: per DEA-ID-000 §2 (Architecture Framework → ECF/Metamodel → General Entity System → Catalogs)
- 5 architectural principles (identity / semantics / relationships / lifecycle / conformance)
- 11 existing decisions retained (R-classification)
- 9 decisions needing framing (N-classification; Stage 2 outputs)
- 7 open questions (U-classification; Stage 2 norm design resolves)

### 4.2 Existing Decisions and Gap Register (`docs/entity-system/01-existing-decisions-and-gap-register.md`)

- 6 categories (Identity / Semantics / Relationships / Lifecycle / Conformance / Cross-cutting)
- 33 decisions walked
- 15 R (retained) - no change
- 2 H (historical-only) - leave as-is
- 9 N (needs framing) - Stage 2 outputs (G-01..G-07)
- 7 U (open questions) - Stage 2 norm design resolves
- 6 legacy-tail repos - per-repo disposition register under EGV-012

### 4.3 Normative Design Proposal (`docs/entity-system/02-normative-design-proposal.md`)

- 5 normative decisions: Identity, Contract, Relationships, Lifecycle, Conformance
- For each: the rule, the rationale, the alternatives considered, the disposition
- Cross-cutting: the exception mechanism (resolves U-06)
- Open questions still open: U-01 (cross-catalog URI form), U-07 (OpenDEAM authority chain alignment) - both deferred to Stage 2

### 4.4 Implementation and Adoption Plan (`docs/entity-system/03-implementation-and-adoption-plan.md`)

- 6 implementation stages (CR-BP-121 = Stage 1; CR-BP-122..125 = Stages 2-6)
- Migration policy: no bulk renames (per EGV-012); per-record disposition
- CI enforcement: gate under --strict in `.github/workflows/ci.yml`
- Acceptance criteria for the umbrella programme
- 5 risks + mitigations
- Cross-cutting alignment with DEA-ID-000, CR-012, the 118a/b/c cascade

## 5. Repository changes

| Path | Status | Notes |
|---|---|---|
| `docs/entity-system/00-charter.md` | NEW | Stage 1 output 1; ~10K |
| `docs/entity-system/01-existing-decisions-and-gap-register.md` | NEW | Stage 1 output 2; ~14K |
| `docs/entity-system/02-normative-design-proposal.md` | NEW | Stage 1 output 3; ~18K |
| `docs/entity-system/03-implementation-and-adoption-plan.md` | NEW | Stage 1 output 4; ~13K |
| `change-requests/CR-BP-121-general-entity-system-stage-1.md` | NEW | This file (the carrier CR) |
| `change-requests/README.md` | MOD | New row at top of table with status "Proposed (this PR)" |
| `CHANGELOG.md` | MOD | New entry in [Unreleased] section |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` and stamps dates |

## 6. Acceptance criteria

- AC-01 The 4 Stage 1 outputs exist in `docs/entity-system/`.
- AC-02 The carrier CR is filed under `change-requests/CR-BP-121-...md`.
- AC-03 The CR README + CHANGELOG have a new row / entry.
- AC-04 `python3 scripts/regenerate_catalog.py --check` returns 0 (CATALOG.yaml is current).
- AC-05 D-004 (no en/em-dash, no U+2E3B) is clean across all new/modified files.
- AC-06 The 9 N-classification decisions in the Gap Register each have a normative rule in the Normative Design Proposal.
- AC-07 The 7 U-classification open questions each have a disposition (codified, deferred, or out-of-scope).
- AC-08 No entity, schema, or id changes (the slice is non-destructive).
- AC-09 The 118a/118b/118c authorship gates remain CONFORMANT (no overlap with this slice).

## 7. Cross-references

- **DEA-ID-000**: `dea-governance/docs/design/entity-system-foundation.md` (the foundation paper)
- **CR-012**: `dea-governance/change-requests/CR-012-org-wide-entity-governance.md` (the org-wide governance CR)
- **118a/118b/118c**: `change-requests/CR-BP-118-authorship-cardinal-rule.md` + the 11-repo cascade (the authorship cardinal rule)
- **CR-BP-04**: `change-requests/CR-BP-04-id-family-reconciliation.md` (the four canonical id families)
- **CR-BP-mv1**: `change-requests/CR-BP-mv1-entity-storage-and-id-system-migration.md` (the entity storage and id migration)
- **CR-BP-115**: `change-requests/CR-BP-115-admission-authority-marker.md` (the admission-authority marker)

## 8. Test posture (live, 2026-10-13)

```
$ python3 scripts/check_authorship.py --strict
Authorship Cardinal Rule (CR-BP-118; AUT-001..003): CONFORMANT
  AUT-001 hits: 0
  AUT-002 hits: 0
  AUT-003 hits: 0

$ python3 scripts/check_prose_authorship.py --strict
PROSE Authorship Gate: CONFORMANT
$ echo $?
0

$ python3 -m pytest tests/ -q
... (all 118a/118b/118c tests pass; no overlap with this slice)
```

## 9. What this CR is NOT

- **NOT a sweep.** The 35 `dea:` legacy ids in entities/v1-alpha/ are grandfathered historical record; no changes to entity content.
- **NOT a bulk rename.** Per EGV-012, no existing records are renumbered.
- **NOT the umbrella gate.** The 5-rule gate (ES-001..ES-005) ships as CR-BP-123 (Stage 3-4).
- **NOT the institutionalisation.** The cardinal-rules update + CONTRIBUTING update + envelope template ship as CR-BP-125 (Stage 6).
- **NOT a metamodel change.** The 70 `Agent` content hits in `dea-metamodel` are out of scope (different repo; CR-MM-05 follow-on if applicable).
- **NOT a cross-catalog reference resolution.** U-01 (cross-catalog URI form) is deferred to Stage 2.
- **NOT the open questions.** U-01 + U-07 are deferred to Stage 2 (CR-BP-122).

## 10. Out-of-scope follow-ons

- **CR-BP-122** (Stage 2 Specifications): 5 normative spec docs.
- **CR-BP-123** (Stage 3-4 Reference Implementation): the umbrella gate + tests + workflow.
- **CR-BP-124** (Stage 5 Catalog Adoption): the disposition register + migration id map + cross-catalog resolution.
- **CR-BP-125** (Stage 6 Institutionalisation): the doctrine doc + cardinal-rules update + CONTRIBUTING + envelope template + exception process.
- **T7 of umbrella programme** (Cross-repo cascade): 11 sibling repos get per-repo entity-system CR docs (BC-04, BO-04, OU-04, MF-010, MM-06, AF-04, ACT-02, BL-02, CON-02, STA-07, TEN-02).
- **T8 of umbrella programme** (Legacy ID reconciliation): per-repo disposition registers + cross-catalog reference resolution + cross-catalog URI form (U-01 resolution).
