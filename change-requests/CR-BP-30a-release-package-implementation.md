# CR-BP-30a: Release Package Implementation (slices CR-BP-30a..30g co-landed)

**Status**: Accepted (this PR)
**Layer**: Process Catalog (release / governance)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-04
**Depends on**: CR-BP-30 (design carrier; decisions D1–D6 locked at recommended defaults 2026-11-04 per its §0 decision syntax), CR-BP-116 (release discipline), CR-DEA-BC-05/BC-11 (the proven BC patterns this implementation mirrors)

> **Scope.** Implements the CR-BP-30 §2 artifact family and §4 CI surface as one co-landed series (the §5 slices 30a–30g; 30h — the first cut — follows as the post-merge tag). Per-slice authority is CR-BP-30 §3 as locked: **D1=A** ECF grid overlay · **D2** six sheets · **D3=A** BPMN seed library · **D4=A** curated decisions log + verbatim dispositions · **D5** `dependencies.yaml` adopted · **D6=A** lockstep artifact versioning. The builders read the current substrate (3,723 records; the CR's 196-record citations were its 2026-09-10 vantage — see the CR's layout note). Determinism is the enforced contract: identical substrate produces byte-identical artifacts (proven by the 30g gate and the test suite).

## 1. What landed (per slice)

| Slice | Deliverable | Notes |
|---|---|---|
| **30a** | `scripts/generate_process_map.py` → `process-map.html` (+ `--png` → `process-map-a3.png` via weasyprint→pdftoppm, per §2 artifact 2) | D1=A: ECF 7×7 grid; cells = the 49 PCs, ribbons = L1 groups, bullets = L2 BPs; deterministic (sorted, no timestamps) |
| **30b** | `scripts/build_catalog_xlsx.py` → `catalog.xlsx` | D2: six sheets (01_records with the `version` column / 02_lineage / 03_dispositions / 04_register_audit — the 49 PCs ARE the post-mv1 register / 05_change_requests / 06_contributions); docProps timestamps and zip entry mtimes pinned for byte-determinism |
| **30c** | `scripts/build_bpmn_artifact.py` → `bpmn-library.bpmn` | D3=A: one `<bpmn:process>` per canonical L2 (145), seed Task + documentation carrying canonical ids, ECF cell, PC, trigger/outcome; stdlib ElementTree instead of the suggested lxml (zero extra runtime dep; noted deviation) |
| **30d** | `scripts/build_release_notes.py` → `RELEASE-NOTES.md` + `decisions.md` | D4=A: curated decisions table from `reconciliation/dispositions/register.yaml`; workflow copies the register verbatim to `decisions/dispositions-register.yaml` |
| **30e** | `dependencies.yaml` | D5: `ecf_contract: dea:ecf@2.5.0`, `metamodel_pin: "1.0.0"`, self-reference `dea:catalog/business-processes@v0.5.0` |
| **30f** | `.github/workflows/publish-versioned.yml` | tag-push (`v*`); substrate validation first (conformance rollup `--strict` + id-system + RDM — "no release on a non-conformant snapshot"); generate → copy substrate (entities + contributions + dependencies.yaml) → MANIFEST → zip → Release |
| **30g** | `.github/workflows/validate-release-package.yml` | PR gate: every generator runs twice; byte-compare (PNG excluded from bytes, existence enforced) — the determinism contract in CI |

**30h** (first cut) is the post-merge act: carrier CR per `docs/release-cut-procedure.md` (fresh CI on the tag SHA per hardening A; prior-cut history table per B; signing per D), then tag `v0.5.0` — the first post-reset cut (0.1.0–0.4.0 withdrawn/abandoned; the 0.x ≥5 row: minor on substantial evolution).

## 2. What does NOT change

- No entity-record changes (this CR is pure tooling; the substrate it renders is main's).
- No ci.yml gate change (per CR-BP-30 §4.5: the existing gate remains the release precondition; 30f adds its own substrate-validation step).
- No MANIFEST drived invented values: sha256 over actual bytes; generating-script provenance from a fixed map.

## 3. Verification / Acceptance Criteria

1. `tests/test_build_release_package.py` (5 tests) green: grid renders all 49 cells / known BP appears; xlsx has the 6 sheets with ≥3,724 rows on sheet 1 and the `version` column; bpmn has 145 processes + 145 tasks; notes + decisions deterministic; manifest sha256 correct.
2. The 30g determinism contract holds locally (two builds byte-compare for every artifact except PNG bytes).
3. `validate-release-package.yml` runs green on this PR.
4. Freshness gate green (commit→regen→amend).
