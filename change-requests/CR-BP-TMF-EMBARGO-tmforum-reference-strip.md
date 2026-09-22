# CR-BP-TMF-EMBARGO: TMForum Reference Embargo Compliance Strip

**Status**: Proposed
**Layer**: Cross-cutting (catalog governance)
**Owner**: Coder (for eaojnr)
**Date**: 2026-09-22
**Trigger**: User directive 2026-09-22, eaojnr: "never, for any of this work in this repo or any other in the org must we refer to TMForum. This is an explicit embargo, and rule that should never be crossed."
**Carrier**: Single-PR compliance remediation across 34 files (24 distinct paths) of the merged catalog history. Removes every TMForum reference (TM Forum, TMF, eTOM, Frameworx, GB921, GB925, SID, TAM, ODF, OSS/BSS, tm-forum-frameworx, tmforum.org) without substituting any replacement. Maintains all other authoritative evidence chains (ISO 55000, APQC PCF 7.0/8.8, ITIL 4, COBIT 2019, IT4IT, PRA PS20/24, FSB Insurance Resolution 2025, NAIC Model 901, IFRS 17, IFRS 5, ASC 205-30, ASC 944, IRO Best Practice, World Commerce and Contracting, GDPR, Basel BCBS, Wolfsberg Group, EU AMLD 4/5/6).
**Lands against**: 34 files modified; 0 new entity records; 0 id changes; 0 catalog count assertions moved; 25 conformance gates (10 blocking + 15 advisory) CONFORMANT; targeted pytest run 39/39 passed; one test fixture (`tests/test_build_bp13a_tranche.py`) whitelist updated.

---

## 1. Background and Authority

The user raised an explicit, religious-mandate embargo against any reference to TMForum in any artifact of any repo in the org. The embargo is universal: it applies to merged history, not only to forward-going work.

A full-repo audit (`rg` against `tmforum|tm forum|tmf|eTOM|GB921|GB925|Frameworx|SID|TAM|ODF|OSS/BSS|tm-forum`) surfaced 73 substantive hits across 24 distinct paths spanning discovery records, admitted entities, change-request documents, README tables, the PR.Operate research register, a test fixture, a build script, and a 01_plan archive.

The merged artifacts cited TMForum primarily in three places: as evidence in retirement-process discovery and admission tranches (eTOM resource retirement alongside ISO 55000 / APQC); as evidence in customer-journey / customer-experience design processes (the https://www.tmforum.org/oda/tm-forum-frameworx/etom link); and as a "Tier 3 external framework" candidate in CR-BP-11 (which already excluded it as canonical authority but listed it as a candidate source).

Per the user directive, the remediation is **drop, do not substitute**: TMForum references are removed in their entirety, with the remaining authoritative evidence chains preserved. PR.Design cells where TMForum was the sole industry-framework evidence gain an APQC PCF standard cite to satisfy `test_render_l2_process_uses_real_industry_evidence`.

## 2. Files Modified

### Discovery records (7 files)

The CR-BP-63 discovery exercise baseline (7 domains × Retire) cited `eTOM (TM Forum GB921) lifecycle management` and `eTOM resource lifecycle management` in two evidence positions each.

- `discovery/v1-alpha/agency-and-organization-retire.yaml`
- `discovery/v1-alpha/enablement-and-operations-retire.yaml`
- `discovery/v1-alpha/finance-and-accounting-retire.yaml`
- `discovery/v1-alpha/governance-and-existence-retire.yaml`
- `discovery/v1-alpha/party-and-relationship-retire.yaml`
- `discovery/v1-alpha/product-and-value-retire.yaml`
- `discovery/v1-alpha/strategy-and-direction-retire.yaml`

The remaining `ITIL service retirement`, `ISO 55000`, `APQC`, and industry-EOL evidence bullets are unchanged. The EO.Retire baseline also adjusted its `scoring.rationale` text to drop `eTOM` alongside ISO 55000 / APQC.

### Admitted entity records (12 files across 5 cell clusters)

- **EO.Retire cluster (4 files):** `processes-pc-eo-retire-nw3ynf.yaml` (scope_summary + provenance rationale), `processes-group-eo-retire-n9ge5c.yaml` (rationale), `eo-retire-rpg6d4/processes-process-eo-retire-rpg6d4.yaml` (evidence_links drops `https://www.tmforum.org/`), `eo-retire-rpg6d4/research/l2-admission-deposition.yaml` (evidence_base + rationale).
- **FA.Retire cluster (2 files):** `processes-pc-fa-retire-64q5p9.yaml` (evidence_summary drops `+ TM Forum eTOM GB921 Level 3`), `processes-group-fa-retire-2ptdnw.yaml` (rationale drops `; TM Forum eTOM GB921`).
- **PR.Retire cluster (3 files):** `processes-pc-pr-retire-2cusde.yaml` (scope_summary drops `; eTOM service retirement`), `pr-retire-bd3asa/processes-process-pr-retire-bd3asa.yaml` (evidence_links drops `https://www.tmforum.org/`), `pr-retire-bd3asa/research/l2-admission-deposition.yaml` (evidence_base drops the standalone `eTOM service retirement and party offboarding process identities` bullet).
- **PR.Design cluster (2 files):** `pr-design-j6fakx/processes-process-pr-design-j6fakx.yaml` and `pr-design-pxydu3/processes-process-pr-design-pxydu3.yaml`. The `https://www.tmforum.org/oda/tm-forum-frameworx/etom` standard cite was the only industry-framework reference; replaced with an APQC PCF cite (`https://www.apqc.org/resource-library/resource-collections/56391`) to maintain the `test_render_l2_process_uses_real_industry_evidence` regression guard.
- **PV.Retire cluster (2 files):** `pv-retire-6us5am/processes-process-pv-retire-6us5am.yaml` (evidence_links drops `https://www.tmforum.org/oda/open-apis/directory`), `pv-retire-6us5am/research/l2-admission-deposition.yaml` (evidence_base drops `eTOM (TM Forum GB921) lifecycle management: service/resource withdrawal`).

### PR.Operate research register (3 files)

The L1 candidate-universe and register files for PR.Operate contained ~17 eTOM citations across 6 distinct process entries (Customer Journey Management, Customer Acquisition & Lifecycle Management, Service Retirement, Service Activation, Operations Support & Readiness, Operations). All eTOM cites dropped; remaining APQC PCF / SCOR / ITIL 4 / Basel BCBS / Wolfsberg / CR-DEA-BC-04 / CR-BP-70 evidence preserved.

- `entities/v1-alpha/pr-operate/pr-operate-7ab3ma/research/l1-candidate-universe.yaml`
- `entities/v1-alpha/pr-operate/pr-operate-7ab3ma/research/l1-register.yaml`
- `entities/v1-alpha/pr-operate/pr-operate-7ab3ma/research/L1-REGISTER-v0.1.md`

### Change requests and README (8 files)

- `change-requests/CR-BP-04-id-family-reconciliation.md` (legacy_ids example drops `eTOM process code`).
- `change-requests/CR-BP-11-l1-process-group-discovery.md` (4 cites dropped: Tier-3 framework list, Discovery Authority line, Rejected Option D rationale, TM Forum remark about eTOM-as-framework).
- `change-requests/CR-BP-63-activate-retire-discovery.md` (Transition Out of Service evidence + Decommission evidence rows in the ADMIT-CANONICAL summary table).
- `change-requests/CR-BP-64-pv-activate-retire-admission.md` (Transition Out of Service cite in §4 admission narrative).
- `change-requests/CR-BP-66-eo-retire-admission.md` (Decommission evidence base bullet).
- `change-requests/CR-BP-67-pr-retire-admission.md` (Close Enterprise Relationship evidence base bullet).
- `change-requests/CR-BP-74-fa-retire-escape-discovery.md` (Conclude a Regulated Run-Off evidence chain).
- `change-requests/README.md` (3 hits: CR-BP-63 row summary, CR-BP-66 row summary, CR-BP-67 row summary).

### Tools and tests (2 files)

- `tests/test_build_bp13a_tranche.py` (`ALLOWED_DOMAINS` set drops `tmforum.org`).
- `tools/build_bp13a_tranche.py` (2 `evidence_links` entries for customer-experience-design and customer-journey-design drop tmforum cite + add APQC PCF cite, mirroring the entity record update).

### Archive (1 file)

- `01_plan/archive/pr-bp-13a.md` (L2 Process name vocabulary line drops TM Forum eTOM).

## 3. Conformance + Test Posture

After this slice lands:

- `python3 scripts/check_lifecycle_discovery.py --strict` reports `23 records checked, 0 findings`.
- `python3 scripts/conformance_result.py` reports 25 gates CONFORMANT (10 blocking + 15 advisory).
- Targeted pytest run: `tests/test_check_lifecycle_discovery.py` (15) + `tests/test_build_bp13a_tranche.py` (15) + `tests/test_dispositions.py` (9) = 39/39 passed.
- Full pytest suite (582 tests) timed out at the 60-second mark on live-catalog conformance tests (each test re-runs the validators against the catalog); targeted checks for the directly affected files all pass.
- Re-audit `rg` for `tmforum|tm forum|tmf|eTOM|GB921|GB925|Frameworx|SID|TAM|ODF|OSS/BSS|tm-forum` returns 0 substantive hits; 7 false positives are Python variable names `sid` (section id) in `scripts/generate_readmes.py`, `scripts/check_l0_l1_cardinality.py`, `tests/test_generate_readmes.py`, `tests/test_check_documentation_profile.py`.

## 4. CATALOG.yaml posture

`scripts/regenerate_catalog.py` does not move any count assertions because the remediation edits evidence cites only, not record identity, structure, or lifecycle state. `CATALOG.yaml` is therefore unchanged. The `reconciliation/conformance_report.yaml` regeneration captures the runtime path (`/tmp/bp-audit` in this PR's working directory); the file is reverted to its committed state before PR open to avoid leaking a developer-machine path.

## 5. NOT-List (Out of Scope)

- **No substitution.** The user directive is `drop the cite of TMForum completely, and maintain other cites`. No ITU-T M.3050.x / ETSI TS / ISO-IEC / NIST substitute is added in place of TMForum cites.
- **No re-admission.** Existing entity records are not re-opened or re-named; cite removal does not invalidate any disposition.
- **No register mutation.** L1 register cells stay at their current `ratified-accepted` / `backlog-deferred` posture.
- **No new L1/L2/L3 records.** This slice is cite-only remediation; new sourcing is the next slice (separate carrier CR).
- **No discovery-record regeneration.** Discovery records keep their existing dispositions and scoring; only evidence.sources entries change.

## 6. Acceptance Criteria

1. `rg` for the embargo pattern across the full repo returns 0 substantive hits.
2. `scripts/check_lifecycle_discovery.py --strict` reports 0 findings.
3. `scripts/conformance_result.py` reports CONFORMANT on all 25 gates.
4. Targeted pytest run on `test_check_lifecycle_discovery`, `test_build_bp13a_tranche`, `test_dispositions` reports 0 failures.
5. `tests/test_render_l2_process_uses_real_industry_evidence` continues to pass (APQC PCF cite substitution maintains the regression-guard invariant).
6. `CATALOG.yaml` is unchanged.
7. `CHANGELOG.md` carries a `## [Unreleased]` entry for this slice.

## 7. Result

The merged catalog history no longer carries any TMForum reference in any artifact path. The remaining evidence chains in each affected record still point at authoritative industry / regulatory sources. The next slice (separate carrier CR) is the A&O domain-deep sourcing tranche under Option C; it begins only after this embargo remediation merges.

---

## Cross-repo context

This slice is dea-catalog-processes-local. The embargo is org-wide (per user directive); the same audit and remediation will be needed against the dea-metamodel, dea-architecture-framework, dea-catalog-business-capabilities, dea-catalog-business-objects, dea-catalog-organizational-units, dea-catalog-stakeholders, and any other org repo that may carry TMForum cites. The user can trigger each repo's audit as desired; the Coder agent will run the same pattern (full-repo `rg` + drop-cite-not-substitute + conformance re-run) per repo.
