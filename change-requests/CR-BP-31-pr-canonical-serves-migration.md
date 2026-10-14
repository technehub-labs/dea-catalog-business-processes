# CR-BP-31: PartyAndRelationship — Canonical `serves` Relationship Migration (v2.3.0 → v2.5.0)

**Status**: Accepted (paperwork-only normalization)
**Layer**: Process Catalog
**Owner**: Emmanuel A. Otchere
**Date**: 2026-09-10
**Depends on**: CR-BP-15-IMP (Phase 5 trunk migration); CR-BP-18 (ECF v2.3.0); CR-BP-22 (register v3); CR-BP-23 (Domain 6 migration, v2.5.0)
**Supersedes**: — (additive; does not change IDs, names, or L1 register)
**Registered in**: register v4 (CR-BP-28) — no register change required

---

## 1. Background

The ECF (Enterprise Concept Framework) has been renamed twice since the PartyAndRelationship domain was admitted:

| ECF | Domain code (used in `relationships[].target_id`) |
|---|---|
| v2.3.0 (CR-ECF-CG-004) | `customerAndDemand` |
| v2.4.0 (CR-BP-18)        | `partyAndRelationship` |
| v2.5.0 (CR-BP-23, register v4) | `partyRelationship` |

The canonical `ecfConformance.canonicalReferences[].identifier` field is correctly maintained as `ecf:partyRelationship.<stage>` for every PR-domain BP. However, **7 PR-domain BPs still carry only the v2.3.0 `ecf:customerAndDemand.<stage>` value in their `relationships[].target_id` (serves)**. The Phase 5 migration added the `context:` block and the canonical `canonicalReferences` entry, but did not append the canonical v2.5.0 `serves` relationship alongside the stale v2.3.0 one.

**Two other PR BPs already carry both pairs** (`dea:process-customer-channel-and-acquisition-build`, `dea:process-demand-generation-build`) — they were updated as part of CR-BP-23 Domain 6 migration work. The remaining 7 records were missed.

---

## 2. Scope

**7 records, all `PartyAndRelationship` × {Conceive, Design, Build, Operate, Improve}, paperwork-only.**

| BP | Cell | Needs addition |
|---|---|---|
| `dea:process-customer-strategy-conception` | PR × Conceive | `ecf:partyRelationship.conceive` |
| `dea:process-market-and-demand-conception` | PR × Conceive | `ecf:partyRelationship.conceive` |
| `dea:process-customer-experience-design` | PR × Design | `ecf:partyRelationship.design` |
| `dea:process-customer-journey-design` | PR × Design | `ecf:partyRelationship.design` |
| `dea:process-demand-design` | PR × Design | `ecf:partyRelationship.design` |
| `dea:process-manage-customer-relationship` | PR × Operate | `ecf:partyRelationship.operate` |
| `dea:process-customer-insight-and-retention` | PR × Improve | `ecf:partyRelationship.improve` |

For each record:
- **Append** a new `relationships` entry with `relationship_type: serves`, `target_id: ecf:partyRelationship.<stage>`. **Preserve** the existing v2.3.0 `customerAndDemand.<stage>` entry (it is the historical provenance — see §6).
- **Append** a `metadata.change_history` entry naming this CR.

---

## 3. Non-Goals (Explicit)

- **No ID rename** (`dea:process-customer-strategy-conception` stays as-is; the v2.3.0 name is preserved as a synonym alias for APQC traceability).
- **No register change** — register v4 already accepts these cells as landed; only the `relationships` block is being made conformant.
- **No new entities, no new cell charters, no L1 group changes.**
- **No disposition-register changes** — these records are already in the disposition register as `RETAIN` or `RECLASSIFY`; their disposition is not altered by this CR.
- **No other domains touched** — Strategy, Agency, Product, Enablement, Finance all already carry canonical serves pairs (verified by gap scan). PR is the lone holdout.
- **No conformance-gate strictness changes** — pre-existing ADM-005 advisories on schema trigger/outcome format remain pre-existing.

---

## 4. Why a Separate CR (Not Bundled Into a Larger Wave)

This is the cleanest paperwork-only normalization in the current repo state:

- The change is **purely additive**: 7 records × 1 new relationship entry + 7 change_history entries. Zero changes to IDs, names, dispositions, gates, or register.
- It **closes the last residual v2.3.0 → v2.5.0 migration debt** in the PR domain specifically, without requiring the 14-cell Activate/Retire programme to start.
- It is **independently verifiable**: re-running the gap scan should drop from 7 missing to 0 missing; all CI gates should remain green; pytest should remain 148/1 pre-existing.

If bundled with a larger wave, the larger wave's scope changes would obscure whether the migration pair was the cause of any gate fluctuation. Keeping it isolated preserves diagnostic clarity.

---

## 5. Acceptance Criteria

1. All 7 listed BPs have a `relationships` entry with `target_id: ecf:partyRelationship.<stage>` (case matches the v2.5.0 register, **not** `partyAndRelationship` and **not** `customerAndDemand`).
2. The 7 existing v2.3.0 `customerAndDemand.<stage>` entries are preserved unchanged.
3. Each of the 7 records has a new `metadata.change_history` entry: `cr: CR-BP-31, date: 2026-09-10, change: "Added canonical v2.5.0 serves relationship alongside v2.3.0 historical entry (migration-pair completion per CR-BP-31)."`.
4. `reconciliation/inventory.yaml`, `reconciliation/baseline/v1.yaml`, and `reconciliation/conformance_report.yaml` are regenerated and committed.
5. `python3 scripts/conformance_result.py` reports `CONFORMANT` (15 gates, 0 blocking, 0 advisory **new**).
6. `python3 scripts/check_admission_gate.py --strict-provenance` exits 0 (status `CONFORMANT-WITH-WARNINGS` accepted, no new warnings).
7. `python3 -m pytest tests/ -q` reports 148 pass / 1 pre-existing failure (no new failures).
8. `python3 scripts/check_cr_metadata.py --strict` reports 0 new findings.
9. A reproduction script (`scripts/check_canonical_serves.py`) is added under the repo, encoding the gap-scan check, so future regressions are caught at CI time.

---

## 6. Preservation Rationale (Why Keep the v2.3.0 Entry)

The v2.3.0 `customerAndDemand.<stage>` `serves` relationship is the historical artifact that documents how the record was first admitted under the previous domain enum. Removing it would sever the **provenance chain** that `metadata.change_history` is meant to capture (CR-BP-15-IMP §1; CR-BP-16 §8). The pattern is established in the two PR BPs already carrying both pairs (`customer-channel-and-acquisition-build`, `demand-generation-build`): both forms coexist, the canonical one resolves the ECF conformance check, the legacy one preserves the audit trail.

---

## 7. Deliverables

- 7 BP YAML edits (additive only).
- `change-requests/CR-BP-31-pr-canonical-serves-migration.md` (this file).
- `scripts/check_canonical_serves.py` — gap-scan regression guard.
- Regenerated inventory + baseline + conformance report.
- README pointer block at the top of the repo's `change-requests/README.md` referencing this CR.

---

## 8. Out-of-Scope Reminders

- **Activate and Retire cells** (14 cells across all 7 domains) remain deferred by register v4. This CR does not open them.
- **`dea:process-manage-customer-relationship`** is **not** moved to a new cell, **not** renamed, **not** retired. It already lives in `dea:pc-pr-op` (PR × Operate) and continues to do so. The "1 unresolved BP" surfaced in earlier coverage reports was an artifact of an over-strict gap scanner; this CR is the explicit closure.
- **The `01_plan/CR-BP-30-release-package/` directory** is untracked on disk and is **not** part of this CR. It is a separate workstream pending user direction.
