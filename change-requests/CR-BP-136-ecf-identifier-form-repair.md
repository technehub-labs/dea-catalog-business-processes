# CR-BP-136: ECF Coordinate Identifier Form Repair (And-Stripped Convention)

**Status**: Accepted
**Layer**: Process Catalog (Structural data model)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-31
**Depends on**: CR-ECF-012 (dea-metaframework PR #59: the And-stripped DOMAIN_ID table is the normative identifier convention), CR-MET-018 (dea-metamodel PR #206: the mirror test + detector truthfulness fixes)

> **Scope.** Mechanical identifier-form repair: 11 live records carry And-kept ECF coordinate identifiers (`ecf:partyAndRelationship.build`, `ecf:governanceAndExistence.*`) that the metamodel drift detector's canonical 49-space rejects — forms the deprecated generic-camelization builder produced before CR-ECF-012 finalized the And-stripped convention (`ecf:partyRelationship.build`, `ecf:governanceExistence.*`; EnablementAndOperations is the one connective-keeping domain). The same repair covers one reconciliation-register entry and two historical tranche scripts. Zero semantic changes — the domain and stage are identical; only the serialization of the identifier differs. Found by the identifier-convention census that followed the CR-ECF-012 reconciliation (no CI gate scanned these records in this form, which is why they survived).

---

## 1. What changes

| Site | Change |
|---|---|
| 2 live records (`pr-build` Customer-Channel-and-Acquisition-Build subtree) | `ecf:partyAndRelationship.build` → `ecf:partyRelationship.build` |
| 9 live records (`ge-conceive`, `ge-design`, `ge-build`, `ge-improve`, `ge-operate` subtrees) | `ecf:governanceAndExistence.*` → `ecf:governanceExistence.*` |
| `reconciliation/dispositions/register.yaml` (1 entry) | `ecf:financeAndAccounting.activate` → `ecf:financeAccounting.activate` |
| `scripts/apply_phase_7a_tranche.py` (5 sites) | `ecf:strategyAndDirection.*` → `ecf:strategyDirection.*` (historical tranche script; consistency, not executed) |
| `scripts/apply_phase_7d_tranche.py` | `"EnablementAndOperations": "operationsEnablement"` → `"enablementAndOperations"` (deprecated form → canonical) |
| `scripts/check_intent_purposive.py` (PSP-003 denylist) | canonical And-stripped domain tokens added (the gate previously recognized only the deprecated And-kept forms, so canonical identifiers in intent text went unflagged); And-kept forms retained as denylist aliases |
| `tests/test_check_intent_purposive.py` | fixture covers both identifier conventions; stale corpus-count pins (140) updated to the live count (145; pre-existing failure on main) |
| `CATALOG.yaml` | regenerated (subtree last_modified shifts for the 11 touched records) |

## 2. What does NOT change

- No domain, stage, relationship, or record semantics change — the PascalCase domain/stage values in each `ecfConformance`/reference block are untouched; only the `ecf:<domain>.<stage>` serialization of five domains' identifiers is repaired to the CR-ECF-012 convention.
- The `enablementAndOperations` form everywhere is correct and untouched (the one connective-keeping domain).
- No id-system change: entity ids, target ids of non-ECF relationships, and all other content are preserved.

## 3. Authority chain

CR-ECF-012 finalized the identifier convention in the metaframework (executing the CR-ECF-005 §3 deferral); metamodel CR-MET-018 added the all-49 mirror test between the two repos and the detector truthfulness fixes. This CR repairs this catalog's surviving artifacts to that convention; the deprecated forms resolve through the detector's `DEPRECATED_DOMAIN_ID_ALIASES`, but repair is preferred over alias-dependence for live records.

## 4. Verification

1. Zero And-kept forms remain in `entities/`, the touched scripts, and the reconciliation register.
2. Full catalog regeneration is deterministic (`--check` current).
3. The metamodel drift detector, pointed at this catalog, reports no identifier findings.

## 5. NOT-list

1. No relationship or record semantic changes.
2. No schema, gate, or vocabulary changes.
3. No migration of `operationsEnablement` historical evidence entries (register history; the detector's aliases resolve them).
