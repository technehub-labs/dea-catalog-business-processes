# CR-BP-37: Cross-Repository Integrity (XRI-001..005)

**Status**: Proposed
**Layer**: Cross-cutting
**Owner**: Emmanuel A. Otchere
**Date**: 2026-09-12
**Carrier**: Ninth execution slice of the BP-32/33/34 tranche plan; third slice of Phase 5. See `01_plan/CR-BP-32-33-34-foundation/POSITIONING.md` §5/§7.
**Depends on**: CR-BP-SPEC-BP-01 (metamodel-pointer authoring); CR-BP-16 (conformance gate); CR-BP-19 (register re-derivation); CR-BP-21 (domain admission tranches); CR-BP-23 (ECF v2.5.0 cascade); CR-MM-PROC-01 (metamodel Core authority; cross-repo); CR-AR-FMWK-01 (root model v0.6.0 authority; cross-repo); CR-ECF-CG-001..004 (ECF conformance; cross-repo); CR-CATALOG-STRUCT-01 (catalog repository standard; cross-repo)
**Lands against**: 1 metamodel-pointer.yaml; 1 README Cross-repo context section; 161 canonical records; conformance level L4

---

## 1. Change Request

Codify the catalog's cross-repo reference surface as a documented contract plus a small runtime validator. The catalog's cross-repo surface lives in two places:

1. `metamodel-pointer.yaml` — the catalog's authoritative declaration of which metamodel / root-model / WSF entities it references, and the federation mapping between them.
2. `change-requests/README.md` — the `## Cross-repo context` section that names companion CRs in sibling repos (dea-metamodel, dea-architecture-framework, dea-metaframework, dea-catalog-business-capabilities, dea-catalog-business-objects, dea-catalog-organizational-units).

This slice adds:

1. A retrospective CR doc (this file) that documents the cross-repo surface as it actually stands in `main`.
2. A runtime validator `scripts/check_cross_repo_integrity.py` (XRI-001..005) that codifies five invariants about the pointer + the README's companion CR lineage section.
3. **No CI gate wiring.** CR-BP-37 is documentation-heavy (per tranche plan, "~200 LOC + contracts"). The validator is a runtime / CI-runnable asset for the catalog maintainer; promoting it to a conformance gate is deferred to a future CR if needed.

## 2. The cross-repo surface (2026-09-12)

### Canonical lineage CRs (the catalog's load-bearing contracts)

| CR | Repo | Authority | What this catalog depends on |
|---|---|---|---|
| `CR-MM-PROC-01` | `technehub-labs/dea-metamodel` | metamodel Core | `dea:Process` (abstract kernel) + `dea:BusinessProcess` (specialization); PR #163 MERGED, commit 1665209 |
| `CR-AR-FMWK-01` | `technehub-labs/dea-architecture-framework` | root model v0.6.0 | `dea:entity-process` (root-model kernel; `discriminator: process-kernel`) + `dea:entity-business-process` (specialization; `class_alias: BP`); PR #10 MERGED, commit 76463b2; tag v0.6.0 |

These two CRs together establish the **1:1 LOSSLESS federation mapping** between the metamodel Core ids and the OpenDEAM root-model ids. `metamodel-pointer.yaml` declares both ids in the multi-entity form so the consumer-validator (`scripts/validate_consumer.py`; v0.6.0 abstract-kernel branch) recognizes the kernel + specialization contract.

### ECF conformance lineage (CR-ECF-* in `dea-metaframework`)

| CR | What | Catalog companion |
|---|---|---|
| CR-ECF-CG-001..004 | ECF Conformance Gate | catalog-internal ECF conformance check (`check_ecf_conformance.py`); CG-001..006 referenced from README |
| CR-ECF-006 + ADR-ECF-001 | ECF Domain enum v2.3.0 migration | CR-BP-17 (PR #44) |
| CR-ECF-007 + ADR-ECF-002 | ECF Domain enum v2.4.0 migration (AgencyAndOrganization) | CR-BP-18 (PR #45) |
| CR-ECF-008 + ADR-ECF-003 | ECF Domain enum v2.5.0 migration (EnablementAndOperations) | CR-BP-23 (PR #61) |

### Companion catalog CRs (sibling repos)

| CR | Repo | Catalog-side companion |
|---|---|---|
| `CR-BC-ECF-03` | `dea-catalog-business-capabilities` | CR-BP-23 companion |
| `CR-BO-02` | `dea-catalog-business-objects` | CR-BP-23 companion |
| `CR-OU-02` | `dea-catalog-organizational-units` | CR-BP-23 companion |

Each companion CR lands the same ECF version migration in its own catalog repo; together they constitute the federation-level ECF version migration.

### WSF lineage

`wsf:Process` (Tier-3 derived; structural activity organization) — declared in `metamodel-pointer.yaml` authority chain for completeness; no active WSF-derived record types in this catalog.

## 3. The XRI-001..005 validator

The validator enforces five invariants over the pointer + README:

| # | Rule | Predicate |
|---|---|---|
| **XRI-001** | **metamodel-pointer.yaml structure.** | Pointer is valid YAML; has the required top-level keys (`metamodel`, `catalog`); `metamodel.entities` is a non-empty list; `metamodel.entity_id` / `class_alias` / `layer` are non-empty. |
| **XRI-002** | **Entity entry completeness.** | Every entry in `metamodel.entities[]` has the fields required by its role: kernel entries require `entity_id` + `class_alias` + `discriminator`; opt-in entries (`lifecycle: proposed`) require `entity_id` + `lifecycle` from the approved vocabulary. |
| **XRI-003** | **Federation mapping + canonical CR lineage.** | The pointer file's leading comment block references the canonical CR lineage (`CR-MM-PROC-01`, `CR-AR-FMWK-01`), the federation mapping (`1:1` + `LOSSLESS`), and both federation pairs (`dea:Process <-> dea:entity-process`; `dea:BusinessProcess <-> dea:entity-business-process`). |
| **XRI-004** | **Entity_id uniqueness.** | No two entries in `metamodel.entities[]` share the same `entity_id` (silently shadows under consumer-validator's 1:1 resolution). |
| **XRI-005** | **Companion CR lineage references resolve.** | Every CR referenced from `change-requests/README.md`'s `## Cross-repo context` section either exists as a file in `change-requests/` or is in the validator's `COMPANION_CRS` table (acknowledged as a foreign-repo CR). |

The validator is a **runtime asset**, not a conformance gate. Promotion to gate [18] in `scripts/conformance_result.py` is deferred to a future CR if cross-repo integrity becomes conformance-critical. The validator's 12-case `--self-test` and 23-case pytest suite establish its correctness independently.

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `scripts/check_cross_repo_integrity.py` | NEW | XRI-001..005 validator; CLI mirrors prior slices (`--self-test`, `--strict`, `--json`); runtime asset, not a CI gate |
| `tests/test_check_cross_repo_integrity.py` | NEW | 23 tests; rule-level + CLI + live catalog |
| `change-requests/CR-BP-37-cross-repo-integrity.md` | NEW | Slice carrier CR (this file) |
| `change-requests/README.md` | MOD | CR-BP-37 row added; CR-BP-35 status corrected to "Merged (PR #77)" |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 48 → 49 |

**No validator added to `conformance_result.py`.** No schema change. No record mutation. The slice is documentation-heavy plus one runtime asset.

## 5. Coverage on the live catalog (2026-09-12)

```
$ python3 scripts/check_cross_repo_integrity.py
Cross-Repository Integrity (CR-BP-37; XRI-001..005): CONFORMANT
  Findings: 0
    XRI-001 (metamodel-pointer.yaml structure): 0
    XRI-002 (entity entry completeness): 0
    XRI-003 (federation mapping + canonical CR lineage): 0
    XRI-004 (entity_id uniqueness): 0
    XRI-005 (companion CR lineage references resolve): 0
```

The pointer and README are in good standing. The validator is a **forward-looking regression guard**: the first sibling-repo CR to be added without proper lineage references will be flagged by XRI-005.

## 6. Tranche plan status

| Phase | Slice | Status |
|---|---|---|
| 1 | CR-BP-32/33/34 foundation carrier | Merged (PR #69) |
| 2 | CR-BP-34a/b/c/d (4 slices) | Merged (PRs #70–73, gates [11]–[14]) |
| 3 | CR-BP-32 Activity Model | Merged (PR #74, gate [15]) |
| 4 | CR-BP-33 Execution Boundary | Merged (PR #75, gate [16]) |
| 5 | CR-BP-36 MECE Validation | Merged (PR #76, gate [17]) |
| 5 | CR-BP-35 Process Catalog Architecture retrospective | Merged (PR #77) |
| **5** | **CR-BP-37 Cross-Repository Integrity (XRI-001..005)** | **This slice** |
| 5 | CR-BP-38 ECF Matrix Population retrospective | Next per user direction |

## 7. What this CR is NOT

- **NOT a new conformance gate.** XRI-001..005 do NOT appear in `scripts/conformance_result.py`. The validator is a runtime / CI-runnable asset.
- **NOT a metamodel CR.** No metamodel entities are added; no `dea-metamodel` changes are proposed.
- **NOT a record mutation.** No canonical entity changes; no schema bump.
- **NOT a new ECF migration.** The ECF v2.5.0 cascade (CR-BP-23 / PR #61) is the latest; no v2.6.0 work is proposed.
- **NOT a federation-programme carrier.** Cross-federation coordination lives in a separate workstream; this CR documents the catalog's surface only.

## 8. Acceptance criteria

1. `scripts/check_cross_repo_integrity.py` runs on the live catalog with 0 findings.
2. `scripts/check_cross_repo_integrity.py --self-test` passes (12 cases).
3. `tests/test_check_cross_repo_integrity.py` passes (23 tests).
4. `change-requests/README.md` CR-BP-37 row added.
5. `CATALOG.yaml` reflects `open_change_requests: 49` (was 48).
6. No canonical record, schema, or validator-rule change outside the additive changes listed in §4.

## 9. Result

CR-BP-37 documents the catalog's cross-repo surface as it stands after Phase 1..4 of the BP-32/33/34 harvest and the first two Phase 5 slices (PR #76 MECE; PR #77 Architecture retrospective). The XRI-001..005 validator is a runtime regression guard for the pointer + README companion CR lineage section. Conformance gate promotion is deferred.
