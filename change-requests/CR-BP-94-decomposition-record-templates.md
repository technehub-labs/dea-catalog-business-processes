# CR-BP-94: Decomposition Record Templates

**Status**: Proposed
**Layer**: Process Catalog
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-18
**Carrier**: Recon-programme implementation slice that lands the canonical authoring templates for L0-L4 + the human-oriented decomposition-template guide. Six artifacts: `templates/process-scope.yaml`, `templates/process-group.yaml`, `templates/business-process.yaml`, `templates/activity.yaml`, `templates/task.yaml`, and `docs/decomposition-template-guide.md`. Each template encodes both machine-oriented schema structure AND human-oriented authoring guidance (CR-BP-92 §15).
**Recon programme**: CR-BP-92 §9 + §15.
**Depends on**: CR-BP-92 (recon programme), CR-BP-93 (decomposition semantic contract), CR-BP-95 (L0/L1 conformance gate + PG-009/010 fields).
**Lands against**: 139 canonical BP records, 48 canonical PG records, 35 canonical PC records, 553 canonical Activity records; 20 conformance gates CONFORMANT; v0.4.0 tagged; v0.4.0+4 commits on main (CR-BP-91 / -92 / -93 / -95).

---

## 1. Change Request

Land the **canonical authoring template family** for the L0-L4 decomposition chain plus the human-oriented **decomposition-template guide**. Six artifacts:

| Path | Status | Notes |
|---|---|---|
| `templates/process-scope.yaml` | NEW | L0 authoring skeleton. Schema-mirrored; PSCOPE-001..008 rule citations at every required-field site. Backed by `schemas/entities/process-scope.schema.json` (CR-BP-95) and `scripts/check_process_scope.py`. |
| `templates/process-group.yaml` | NEW | L1 authoring skeleton. PG-001..010 rule citations; CR-BP-95 `grouping_basis` + `membership_criteria` blocks strongly recommended for new records; existing 48 PGs remain conformant without them. |
| `templates/business-process.yaml` | NEW | L2 authoring skeleton. BP-C1..C4 + BP-SEM-001..014 + LCM + SIV + PSP gate citations at every required-field site. |
| `templates/activity.yaml` | NEW | L3 authoring skeleton. ACT-001..010 + EXE-001..010 rule citations; `decomposition_boundary: l4-reached` vs `composes:` explained. |
| `templates/task.yaml` | NEW | L4 authoring skeleton. First normative description of the L4 record shape; `TODO(CR-BP-98)` markers for fields that CR-BP-98 will codify. |
| `docs/decomposition-template-guide.md` | NEW | Human-oriented authoring guide. Layer-by-layer guidance + disallowed mistakes + cross-cutting authoring rules + validation flow. |

## 2. Deposition mechanics (pattern per CR-BP-92 §9 + §15)

1. **Layer-by-layer authoring skeleton.** Each template mirrors the schema field set for its layer, with inline `# authoring:` guidance comments at every required-field site documenting the rule that enforces the field.
2. **Dual encoding.** Per CR-BP-92 §15, each template encodes both machine-oriented schema structure (YAML skeleton the validators enforce) AND human-oriented authoring guidance (inline comments + this guide's prose).
3. **Forbidden superficially-complete.** The `definition` minimum lengths (2000 chars), `cohesion_rationale` mandatory field on Activity, `trigger` / `outcome` mandatory on BP, `decomposition_basis.statement` (1000 chars) on Scope, `boundary.inclusions` / `boundary.exclusions` on Task: these minimums force substantive prose at every required-field site. Boilerplate is a review rejection risk.
4. **Back-compat rule documented.** The L1 template documents the OPTIONAL `grouping_basis` / `membership_criteria` back-compat rule (CR-BP-95): existing 48 PGs remain conformant without them; backfill is CR-BP-99 or a dedicated enrichment tranche, NOT CR-BP-94.
5. **L4 placeholder rule documented.** The L4 template marks every not-yet-gated field with `# TODO(CR-BP-98):` because CR-BP-98 will establish the L4 schema + gate. Until then, the L4 record shape is normative-by-template (no validator enforces it today).
6. **Reconciliation artifacts.** No record-level changes; baseline and conformance report regenerate unchanged.
7. **Count assertions.** None changed.

## 3. Gate posture

- Gate [15] Activity Model (ACT-001..010): **CONFORMANT, 553 Activity records, 0 findings** (unchanged).
- Gate [16] Execution Boundary (EXE-001..010): **CONFORMANT, 740 records checked, 0 findings** (unchanged).
- Gate [20] Process Scope (PSCOPE-001..008): **CONFORMANT, no ProcessScope entries found; L0 layer intentionally pre-population per CR-BP-95** (unchanged).
- Gate [7] MECE (Process Group): **CONFORMANT, PASS (PG-001..010)** (unchanged).
- Full suite: **20 gates, 0 blocking, 0 advisory** (unchanged).
- CR-META: **0 new findings** (CR-BP-94 contributes 0 new findings).

## 4. Repository changes

| Path | Status | Notes |
|---|---|---|
| `templates/process-scope.yaml` | NEW | L0 authoring template |
| `templates/process-group.yaml` | NEW | L1 authoring template |
| `templates/business-process.yaml` | NEW | L2 authoring template |
| `templates/activity.yaml` | NEW | L3 authoring template |
| `templates/task.yaml` | NEW | L4 authoring template |
| `docs/decomposition-template-guide.md` | NEW | Human-oriented authoring guide (~250 lines) |
| `change-requests/CR-BP-94-decomposition-record-templates.md` | NEW | Slice carrier CR (this document) |
| `change-requests/README.md` | MOD | CR-BP-94 row added before `## Cross-repo context` |
| `CATALOG.yaml` | MOD | Regenerator bumps `open_change_requests` 104 -> 105 |
| `reconciliation/baseline/v1.yaml` | MOD | Regenerated (no record-level changes) |
| `reconciliation/conformance_report.yaml` | MOD | Regenerated by gate [10]; 788 records (unchanged) |

No schema, validator, gate, or canonical-record change. No count-assertion change. The templates are **additive**: they introduce a new `templates/` directory (which the repo previously did not have) and a new `docs/decomposition-template-guide.md`. No existing record, gate, or test is touched.

## 5. What this CR is NOT

- **NOT a schema, validator, or gate change.** The template family is normative-by-template; gates still enforce the same schemas as before.
- **NOT a canonical-record change.** No new L0 records; no backfill of `grouping_basis` / `membership_criteria` on existing PGs.
- **NOT a re-opening of CR-BP-20 Option A.**
- **NOT a tightening of specialization validation.** Held under CR-BP-92 §21.
- **NOT a count-assertion update.** Counts unchanged.
- **NOT a L4 schema / gate establishment.** That is CR-BP-98's work; this template marks L4 fields with `# TODO(CR-BP-98):`.

## 6. Acceptance criteria

1. `templates/process-scope.yaml` exists and mirrors `schemas/entities/process-scope.schema.json` shape.
2. `templates/process-group.yaml` exists and includes the OPTIONAL `grouping_basis` + `membership_criteria` blocks (CR-BP-95) with PG-009/010 rule citations.
3. `templates/business-process.yaml` exists and cites BP-C1..C4 + BP-SEM-001..014 + LCM-001..005 + SIV-001..004 + PSP-001..003 at every required-field site.
4. `templates/activity.yaml` exists and cites ACT-001..010 + EXE-001..010; documents the `decomposition_boundary: l4-reached` vs `composes:` choice.
5. `templates/task.yaml` exists and marks every not-yet-gated field with `# TODO(CR-BP-98):` per the L4 placeholder rule.
6. `docs/decomposition-template-guide.md` exists with the layer-by-layer guidance + disallowed mistakes + cross-cutting authoring rules + validation flow.
7. `python3 scripts/check_activity_model.py` reports **CONFORMANT, 553 Activity records, 0 findings** (unchanged).
8. `python3 scripts/check_ecf_conformance.py` reports 788 entries conform (unchanged).
9. `python3 scripts/build_inventory.py --self-test --strict` passes after regeneration.
10. `python3 scripts/check_cr_metadata.py` reports 0 new findings on CR-BP-94.
11. `python3 scripts/check_catalog_index.py --strict` passes (the new `docs/` page and `templates/` directory do not break the index).
12. Em-dash / en-dash audit: 0 violations in new prose (the GitHub language rule excludes fenced code blocks and inline code spans).
13. Full pytest suite passes (pre-existing `test_dispositions::test_tranche_count_is_ten` failure unchanged; NOT introduced by this slice).

## 7. Result

CR-BP-94 lands the canonical authoring template family for the L0-L4 decomposition chain plus the human-oriented decomposition-template guide. Six artifacts: five templates + one guide. Each template encodes both machine-oriented schema structure AND human-oriented authoring guidance, with substantive-prose minimums that make it difficult to create a superficially complete element. No schema, validator, gate, or canonical-record mutation. The 20-gate suite remains CONFORMANT (0 blocking, 0 advisory); `open_change_requests` 104 -> 105.
