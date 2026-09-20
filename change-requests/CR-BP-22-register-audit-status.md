# CR-BP-22: Register Audit-Status Reconciliation (v2 register → catalog reality)

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

**Status**: Accepted
**Layer**: Process Catalog (research register)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-08
**Depends on**: CR-BP-19 (register v2; ratified 2026-09-07); CR-BP-21a (StrategyAndDirection landing); CR-BP-21b (AgencyAndOrganization landing); CR-BP-13a/b (PartyAndRelationship and GovernanceAndExistence prior landings)
**Related**: CR-BP-11 (L1 Process Group discovery); CR-BP-13 (research ratification); CR-BP-21c..e (D5/D6/D7 landing tranches, planned)

## 1. What this CR is

The CR-BP-19 register v2 (ratified 2026-09-07) claims 35 `ratified-accepted` coordinates across the 7x7 ECF matrix. As of 2026-09-08 the canonical catalog (`entities/v1-alpha/`) carries only **12 L1 Process Groups**, distributed across 4 of the 7 Domains. The remaining 23 ratified-accepted coordinates have no canonical landing yet — they are admitted in principle (the research register has accepted them with their L1/L2 candidate lists) but no `dea:group-*` or `dea:process-*` entity exists at the corresponding Process Context.

This CR introduces a new `audit_status` axis that distinguishes *research-register acceptance* (a forward-looking admission) from *catalog landing* (the existence of a canonical L1 Process Group at the corresponding coordinate). The two are different operational facts:

- **Acceptance** is decided by CR-BP-11 / CR-BP-13 / CR-BP-19 — does the register carry an explicit disposition for the coordinate?
- **Landing** is decided by the admission-tranche PRs (CR-BP-13a/b, CR-BP-21a/b, CR-BP-21c..e) — does `entities/v1-alpha/dea:group-<...>` exist?

Mixing them as a single `disposition` field hides the gap. CR-BP-22 keeps both: `disposition` (register-side, unchanged) and `audit_status` (catalog-side, new).

## 2. Why this is necessary

Without the audit axis:

1. The register's `38 accepted` claim in `L1-REGISTER-v0.1.md` (CR-BP-13 ratification language) is **inconsistent with the actual catalog state** (12 L1 Process Groups landed). The persona-readable summary still cites the v1 numbers; the YAML register v2 says 35. A consumer reading either is misled about reality.
2. The 3 unadmitted Domains (ProductAndValue, EnablementAndOperations, FinanceAndAccounting) carry zero L1 records. Until CR-BP-21c..e land, the gap is invisible to anyone reading the register alone.
3. There is no machine-readable cross-check between `entities/v1-alpha/` and `research/l1-register.yaml`. The conformance pipeline (`scripts/check_process_group.py`) validates L1 records but does not cross-reference the register.
4. The audit axis is required by the user's standing convention *"L1 process discovery is completed"* — discoverability is complete when the register is self-consistent with the catalog. Today it is not.

## 3. The audit_status axis

A new field is added to each coordinate entry in `l1-register.yaml` and `l1-candidate-universe.yaml`. The field is orthogonal to `disposition`:

| `audit_status` | Meaning | Mapping |
|---|---|---|
| `landed` | At least one canonical `dea:group-*` record exists at the coordinate's Process Context. | `disposition=ratified-accepted` AND `landed_count>=1` |
| `ratified-pending-landing` | `disposition=ratified-accepted` but no canonical L1 record exists yet. Tranche pointer names the planned CR. | `disposition=ratified-accepted` AND `landed_count=0` |
| `backlog-deferred` | `disposition=backlog-deferred`. Lifecycle transition stage (Activate/Retire); not a landing gap. | `disposition=backlog-deferred` |

The audit axis does not change the register's existing disposition policy (CR-BP-11 §5; CR-BP-19 `deferred_rationale`). The 14 backlog-deferred cells remain unchanged.

## 4. The audit reconciliation (as of 2026-09-08)

Counts computed by reading every canonical L1 record in `entities/v1-alpha/`, joining on `process_context` to the register's `dea:pc-*` ids, and comparing `disposition` vs `landed_count`:

| `audit_status` | Coordinates |
|---:|---|
| `landed` | 12 |
| `ratified-pending-landing` | 23 |
| `backlog-deferred` | 14 |
| **Total** | **49** |

### Per-Domain breakdown (post-audit)

| Domain | Conceive | Design | Build | Activate | Operate | Improve | Retire | L1 landed |
|---|---|---|---|---|---|---|---|---:|
| GovernanceAndExistence | landed | landed | landed | deferred | landed | landed | deferred | 5 |
| StrategyAndDirection | landed | pending | pending | deferred | pending | pending | deferred | 1 |
| AgencyAndOrganization | landed | pending | pending | deferred | pending | pending | deferred | 1 |
| PartyAndRelationship | landed | landed | landed | deferred | landed | landed | deferred | 5 |
| ProductAndValue | pending | pending | pending | deferred | pending | pending | deferred | 0 |
| EnablementAndOperations | pending | pending | pending | deferred | pending | pending | deferred | 0 |
| FinanceAndAccounting | pending | pending | pending | deferred | pending | pending | deferred | 0 |
| **Totals** | 7 | 7 | 7 | 7 | 7 | 7 | 7 | **12** |

Pending tranche pointers:
- StrategyAndDirection Design/Build/Operate/Improve → **CR-BP-21c.1** (sub-slice of D2; planned) or part of a refreshed 21a landing if scope permits
- AgencyAndOrganization Design/Build/Operate/Improve → **CR-BP-21b.1** (sub-slice of D3; planned) or part of a refreshed 21b landing
- ProductAndValue Conceive/Design/Build/Operate/Improve → **CR-BP-21c** (D5 full landing; planned)
- EnablementAndOperations Conceive/Design/Build/Operate/Improve → **CR-BP-21d** (D6 full landing; planned; may sub-slice into 21d.1 + 21d.2)
- FinanceAndAccounting Conceive/Design/Build/Operate/Improve → **CR-BP-21e** (D7 full landing; planned; may sub-slice into 21e.1 + 21e.2)

## 5. The deliverable shape

This CR ships four changes:

1. **New file**: `change-requests/CR-BP-22-register-audit-status.md` (this file).
2. **Modified**: `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-register.yaml`
   - Add `audit_status: { landed | ratified-pending-landing | backlog-deferred }` to every coordinate entry
   - Update `ratification` block to `version: 3`, `cr: CR-BP-22`, `ratified_at: '2026-09-08'`, `supersedes: version 2 (CR-BP-19, 2026-09-07)`
   - Add `audit_audit_counts: { landed: 12, ratified-pending-landing: 23, backlog-deferred: 14, total: 49 }`
3. **Modified**: `entities/v1-alpha/dea:group-customer-lifecycle-management/research/l1-candidate-universe.yaml`
   - Mirror `audit_status` per candidate (candidates inherit their coordinate's status by default; explicitly overridden when the candidate is landed while the coordinate is not — e.g., a Conceive cell with 1 landed L1 + 2 un-landed L1 candidates)
   - Bump `ratification.version` to 3
4. **Modified**: `entities/v1-alpha/dea:group-customer-lifecycle-management/research/L1-REGISTER-v0.1.md`
   - Update persona summary to reflect audit_status counts
   - Add a "Registry vs Catalog" reconciliation table
5. **Modified**: `change-requests/README.md` — index row for CR-BP-22.
6. **Modified**: `CHANGELOG.md` — entry for CR-BP-22.

No canonical entity, no schema, no validator, no CI surface change. This is a register audit; the same local validators apply unchanged.

## 6. Conformance with existing gates

- **Process identity** (`check_process_identity.py`): unchanged; no new entity ids.
- **Process group** (`check_process_group.py`): unchanged; no new L1 records.
- **ECF conformance** (`check_ecf_conformance.py`): unchanged; no new coordinate references.
- **CR metadata** (`check_cr_metadata.py`): this CR follows the existing template (Status / Layer / Owner / Date / Depends on / Related; sections 1-7). Index row added.
- **Catalog index** (`check_catalog_index.py`): unchanged; the register lives under `entities/v1-alpha/dea:group-customer-lifecycle-management/research/` and is not part of the catalog index regeneration surface.
- **Catalog structure** (`check_struct.py`): unchanged; no directory restructuring.

A new helper script `scripts/check_register_audit.py` is OPTIONALLY added (one-shot, idempotent) to validate that `audit_status` matches the catalog reality. This is not a blocking gate; it is a tool the user can run after every landing tranche to confirm the register did not drift. The script is NOT required for the S17/S18/S19 conformance pipeline.

## 7. Acceptance criteria

1. `audit_status` is present on every coordinate in `l1-register.yaml` (49/49).
2. `audit_status` is present on every L1 candidate in `l1-candidate-universe.yaml` (102/102).
3. `audit_counts` block in the register matches the per-coordinate recomputation: 12/23/14/49.
4. The persona summary `L1-REGISTER-v0.1.md` reports both the register-side counts (35 accepted / 14 deferred per v2) AND the audit-side counts (12 landed / 23 pending / 14 deferred).
5. The CR is indexed in `change-requests/README.md`.
6. The CHANGELOG records the CR.
7. Existing local validators continue to pass (`check_process_group.py`, `check_process_identity.py`, `check_ecf_conformance.py`).
8. CATALOG.yaml regeneration (`scripts/regenerate_catalog.py`) remains byte-stable under the audit (the register is not part of the catalog index surface; this is a sanity check).

## 8. Consequences

### Positive

- The register and the catalog are now self-consistent at the coordinate level. A consumer can answer "is X coordinate landed?" by reading `audit_status` rather than reverse-engineering the catalog.
- The 23-coordinate gap is named, counted, and pointed at the planned tranche. The research-register acceptance and the catalog landing are explicitly separate facts.
- The persona summary stops citing the v1 numbers (38/11) which were inconsistent with the v2 register (35/14) and with the catalog (12/0/14).

### Negative

- The `audit_status` axis is a new field. Downstream consumers that read `l1-register.yaml` and expect a fixed schema must add support for it. The field is additive (ignoring unknown fields is the convention); no breaking change.
- The audit counts will drift each time an admission tranche lands. The register must be re-audited after every landing. CR-BP-22 does not automate the re-audit; the optional `check_register_audit.py` script can be run manually or wired into CI as a future CR.

### Forecloses

- Demoting un-landed coordinates back to `backlog-deferred` (the alternative considered in planning). The ratification evidence is preserved by the audit_status axis.
- Authoring a permanent new validator in the S17/S18/S19 conformance pipeline. The audit script is a tool, not a gate.
- Restructuring the register directory or moving it back to `docs/research/`. The CR-CATALOG-STRUCT-02 migration (2026-09-05) placed it under `entities/v1-alpha/dea:group-customer-lifecycle-management/research/` and the audit continues there.

## 9. Rejected alternatives

### A: Demote un-landed cells back to `backlog-deferred`

Rejected because: the 23 cells are ratified-accepted by CR-BP-19 against ECF v2.4.0 with explicit L1/L2 candidate lists. Demoting them loses the ratification evidence and contradicts the register's `deferred_rationale` (Activate/Retire only). The audit axis preserves the evidence and exposes the gap.

### B: Skip the audit; just land the D5/D6/D7 tranches

Rejected because: the user's verification question ("L1 process discovery is completed") required a register-vs-catalog reconciliation. Without the audit, the register claims 35 accepted while the catalog carries 12. The audit is the deliverable that makes the question answerable.

### C: Restructure the register directory

Rejected because: the CR-CATALOG-STRUCT-02 migration (2026-09-05) is recent and stable. The audit continues at `entities/v1-alpha/dea:group-customer-lifecycle-management/research/`.

## 10. Explicit non-decisions

This CR does NOT decide:
- The shape of the D5/D6/D7 landing tranches (CR-BP-21c..e scope; sub-slice or full-domain; slice-by-slice cadence). The audit only names the gap; the landing shape is the user's call per the slice-by-slice convention.
- Whether `audit_status` becomes a blocking CI gate (S17/S18/S19 promotion). The audit script is a tool, not a gate.
- The future location of the register (e.g., back to `docs/research/`). The audit continues at the current path.
- The schema of new validators. No new validator ships in this CR.

## 11. Required follow-on CRs

- **CR-BP-21c** (planned): ProductAndValue full-domain landing; closes 5 of the 23 pending coordinates.
- **CR-BP-21d** (planned): EnablementAndOperations full-domain landing; closes 5 of the remaining 18 pending coordinates.
- **CR-BP-21e** (planned): FinanceAndAccounting full-domain landing; closes 5 of the remaining 13 pending coordinates.
- **CR-BP-21a.1 + CR-BP-21b.1** (optional): completion of StrategyAndDirection and AgencyAndOrganization landing — they currently carry only the Conceive cell each. The audit exposes this gap; closing it would reduce the pending count by 8 (4 cells × 2 domains).
- **CR-BP-23** (future, conditional): promote `check_register_audit.py` from tool to blocking CI gate, if and when the audit has been stable across ≥3 landing tranches.

The chain closes at CR-BP-21e under the current scoping; CR-BP-23 is conditional.

---

*Status: Accepted. Parent: CR-BP-11 (L1 discovery). Register upgrade: v2 → v3 (audit axis additive). Implementation: register YAML + universe YAML + persona summary + CHANGELOG; no canonical entities, no schema, no CI gate.*