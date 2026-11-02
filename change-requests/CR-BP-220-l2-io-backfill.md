# CR-BP-220: L2 IO Backfill — Complete Process-Level Declaration

**Status**: Accepted (owner directive 2026-11-02: "perform the backfill to complete it")
**Layer**: Process Catalog (Structural data model)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-02
**Depends on**: CR-BP-94-EXT-12 (Proceed, PR #219: the semantics these declarations follow)
**Companion**: dea-catalog-information-assets CR-IA-CAT-06 (the bridge batch minting the information-typed outputs as assets)

## 1. What changes

All 144 previously-undeclared L2 Process records now declare `inputs[]` and `outputs[]` per EXT-12 sections 6-7, derived mechanically from each record's own documented content (`description`, `trigger`, `outcome`, `process_intent` — every item's `description` cites the field it formalizes). IO coverage: **146/146 L2 records** (2 pilots + 144 backfill).

## 2. Derivation rules (honest, mechanical, documented)

- **Input** (one per record): type classified from the description/name/trigger text (information / request / material / business_object); name from the process name + type; source = "Record documented content"; mandatory=true.
- **Output** (one or two): type classified from the outcome text via pattern match (document / information / service_result / decision / changed_object); consumer = downstream per the documented outcome. Deliverable-type outputs also carry a companion changed_object output (the state change the outcome documents).

No IO item is invented: each is a formalization of what the record already documents. Records whose documentation is thin produce thin (but honest) declarations.

## 3. Verification

- EXT-12 checker (gate 37): OK, 0 findings across all 3,882 records.
- README regeneration (gate 30 RDM-001): CONFORMANT.
- CATALOG.yaml regenerated and current.

## 4. What does NOT change

- No record semantics (descriptions, triggers, outcomes) are modified.
- No L3/L4 declarations (EXT-12 table: L3/L4 IO is optional and separately gated).
- No cross-references or relationship semantics.
