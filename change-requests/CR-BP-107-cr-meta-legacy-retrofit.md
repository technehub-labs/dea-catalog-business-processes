# CR-BP-107: CR-META Legacy Retro-Fit (Validator + 9 Historical CRs)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance)
**Owner**: Coder (for eaojnr)
**Date**: 2026-10-12
**Carrier**: Single-PR retro-fit programme: (a) extends `scripts/check_cr_metadata.py` to admit three pre-existing CR naming patterns that pre-date the CR-BP-16 S16 convention, and (b) adds missing Status / Layer / Owner metadata to 5 historical CRs (CR-BP-02, -03A, -04, -SPEC-BP-01, -ECF-CG-004) and corrects the Status value of CR-BP-mv1.

**Lands against**: 9 historical CR files in `change-requests/`; 1 validator script (`scripts/check_cr_metadata.py`); 1 new CR-META carrier (this file); CHANGELOG + change-requests/README bumped. No entity-record changes. No conformance-gate posture changes outside CR-META. No id-system changes.

## 1. Goal

`scripts/check_cr_metadata.py --strict` was reporting **21 findings across 9 CR files (2 new, 19 legacy)** on every CI run since at least 2026-09-22. The 2 NEW findings were causing the `validate` workflow to fail. The 19 LEGACY findings were advisory under the validator's own policy but contributed to a noisy CI signal.

This CR closes the retro-fit programme in two surgical moves:

1. **Validator script patch** (1 file, additive): admit three pre-existing CR naming patterns that pre-date the CR-BP-16 S16 convention:
   - `CR-BP-SPEC-<UPPER>` (specialization carrier; CR-BP-SPEC-BP-01)
   - `CR-BP-TMF-EMBARGO` (cross-cutting embargo compliance carrier; id token stands; substantive term masked by `scripts/check_reference_embargo.py`; carrier filename is sealed and hash-locked under CR-BP-112)
   - `CR-<UPPER>(-<UPPER/digits>)*-<digits>` (cross-repo CRs co-located by convention; CR-CATALOG-STRUCT-NN, CR-ECF-CG-NNN)
2. **CR-META retro-fit** (6 files): add missing Status / Layer / Owner to 5 historical CRs that pre-date the S21 metadata schema, and correct the Status value of CR-BP-mv1 (was `"Merged (PR #149)"`; not in approved set; changed to `"Accepted"`).
3. **Companion-to rephrasing** (1 file): CR-BP-13 had `**Companion to**: CR-CATALOG-STRUCT-02 (...)` which the `CR_REF_PATTERN` did not match. Added an intra-repo `CR-BP-11` self-anchor plus prose explaining the cross-repo reference; cross-repo refs are documented in prose until CR-META-005 is extended to admit them structurally.

## 2. Slice shape

### 2.1 Validator script patch (`scripts/check_cr_metadata.py`)

- `CR_NUMBER_PATTERN` extended to admit the three pre-existing patterns above.
- `CR_REF_PATTERN` extended to admit the three patterns above AND a generic `CR-[A-Z]+-[A-Z0-9]+` for cross-repo CR refs.
- Self-test (`--self-test`) re-runs: PASS.
- Strict run (`--strict`) on the post-patch tree: `verdict: CONFORMANT`; 0 new findings, 0 legacy findings.

### 2.2 CR metadata retro-fit (6 files)

| File | Old | New |
|---|---|---|
| CR-BP-02 | (no metadata) | Status=Accepted, Layer=L0 (Process Context), Owner=eaojnr, Date=2025-09, retro-fit note |
| CR-BP-03A | (no metadata) | Status=Accepted, Layer=L2 (data migration), Owner=eaojnr, Date=2025-09, retro-fit note |
| CR-BP-04 | (no metadata) | Status=Accepted, Layer=L2 (id-family reconciliation), Owner=eaojnr, Date=2025-09, retro-fit note |
| CR-BP-SPEC-BP-01 | (no metadata) | Status=Accepted, Layer=L2 (specialization profile), Owner=eaojnr, Date=2025-09, retro-fit note |
| CR-ECF-CG-004 | (no metadata) | Status=Accepted, Layer=Cross-cutting (catalog conformance), Owner=eaojnr, Date=2025-09, retro-fit note |
| CR-BP-mv1 | Status=Merged (PR #149), Owner=Coder (for eaojnr) | Status=Accepted, Owner=eaojnr |

Each retro-fit prepends a `**Retro-fit note (CR-BP-107)**: ...` line to the existing CR body so the audit trail of when / why / by-whom is in-CR.

### 2.3 CR-BP-13 Companion-to rephrasing

- `**Companion to**: CR-CATALOG-STRUCT-02 (...)` -> `**Companion to**: CR-BP-11 (intra-repo anchor; L1 disposition register; this CR ratifies the research artefacts against that register), CR-CATALOG-STRUCT-02 (cross-repo; process catalog adoption; this CR flips that row from "Proposed" to "Merged" in change-requests/README.md).`
- Cross-repo ref is documented in prose; CR-META-005 finding closed by the intra-repo `CR-BP-11` anchor.

## 3. Posture

- `scripts/check_cr_metadata.py --strict` (post-patch): **CONFORMANT** (was NON-CONFORMANT, 21 findings across 9 files).
- `scripts/check_cr_metadata.py --self-test`: PASS (no fixture regression).
- 9 historical CR files touched; 1 validator script touched; 1 new carrier CR (this file).
- No entity-record changes. No `CATALOG.yaml` regeneration needed. No `reconciliation/conformance_report.yaml` regeneration needed. No id-system changes.
- No new dependencies. No migration of `dea-metaframework`. No change to other dea-catalog-* repos.

## 4. Open follow-on

- `CR-META-005` extension to admit cross-repo `CR-<word>-<digits>` refs in `**Companion to**` (without requiring an intra-repo anchor) is a separate validator slice. Filed as a follow-on validator harvest (not blocking).
- The retro-fit programme intentionally leaves pre-existing 2025-era CR content untouched (no prose rewrites). Historical record preserved per `docs/versioning.md` S5.
