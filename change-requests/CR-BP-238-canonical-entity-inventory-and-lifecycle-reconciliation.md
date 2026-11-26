# CR-BP-238: Canonical Entity Inventory and Lifecycle Reconciliation

**Status**: Proposed
**Layer**: Cross-cutting
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-26
**Depends on**: CR-BP-94-EXT-24 (operational governance and catalogue baseline), CR-BP-223 (register truth), CR-BP-30/30a..30h (release package), CR-BP-116 (release discipline), CR-BP-237 (metaframework toolchain pin v2.7.0)

> **Scope.** Establish a reproducible, authoritative inventory of the Business Process Catalog's canonical entity records; reconcile that inventory with the lifecycle register, catalogue index, programme-closure evidence and human-facing documentation; and use the reconciled baseline as the mandatory foundation for subsequent release packages. This CR does not redefine process semantics, alter canonical entity identities, or treat research artefacts as canonical entities.

---

## 1. Executive decision

The catalogue shall have one reproducible answer to the question:

**What canonical entity records exist at a given repository commit, what is their lifecycle state, and do all governed representations describe that same set?**

The canonical filesystem inventory is the source for entity existence and identity. The generated `CATALOG.yaml` is the machine-consumable catalogue index. The lifecycle register is the governance view of those same canonical identities. Programme-closure baselines remain dated historical evidence; they are not silently reinterpreted as current population counts.

The intended integrity relationship is:

```text
Canonical entity files
        │
        ├── generated CATALOG.yaml index
        │
        ├── one-to-one lifecycle register
        │
        ├── current inventory baseline and reconciliation report
        │
        └── release-package source snapshot
```

Every representation must be traceable to the same source commit and must distinguish canonical, retired, research, candidate and other supporting material.

## 2. Evidence established by the initial repository recon

The initial implementation audit was performed against `main` at commit `e8d777b90c6749413530a6b06b4f08fae4d388d5` (2026-11-10).

### 2.1 Canonical filesystem inventory

The entity tree contains 3,723 canonical entity record files:

| Level | Entity kind | Physical records |
|---|---|---:|
| L0 | ProcessContext | 49 |
| L1 | ProcessGroup | 49 |
| L2 | Process | 145 |
| L3 | Activity | 580 |
| L4 | Task | 2,900 |
| | **Total** | **3,723** |

This includes the retired entity record. It does not include research files, candidate research material, documentation manifests or other supporting files.

### 2.2 Generated catalogue index

The committed `CATALOG.yaml` reports:

- `entities: 3723`
- `canonical: 3722`
- `retired: 1`
- `candidates: 0`

The index's total entity count agrees with the physical entity-file inventory. Its state counts distinguish the retired record from the 3,722 canonical-state entries.

### 2.3 Lifecycle register defects

The current `reconciliation/closure/lifecycle-register.json` reports 3,725 rows. Record-level inspection identifies two additional rows that do not represent additional canonical entity identities:

1. A duplicate `record_id`, `processes:process-pr-improve-t6uvan`, appears twice. The second row is labelled **Operate Customer Retention Programs (documentation manifest)**. A documentation manifest is not a second process entity.
2. The register contains `dea:research-l2-admission-dea-process-effect-regulator-mandated-governance-unwind`, with an empty name and `entity_kind: unknown`. This is a legacy research artefact, not a canonical entity identifier or entity lifecycle record. Preserve the research evidence in its appropriate research location/register; do not count it as a canonical entity.

The register therefore has 3,725 rows, 3,724 unique identifiers, and only 3,723 identities that correspond to the physical canonical entity files. The duplicated identity and legacy research row must be dispositioned separately.

### 2.4 Historical and derivative count drift

The dated `reconciliation/closure/catalogue-baseline.json` records 3,724 entities, including 146 L2 Processes. It is dated 2026-10-20 and identifies itself as a programme-closure baseline. It remains historical evidence and shall not be overwritten to make it appear current.

Other count claims require reconciliation against the new baseline:

- `reconciliation/catalogue-status-manifest.json` is dated 2026-10-19 and reports L0 as zero, so it is not a current entity inventory.
- The root README currently claims 146/146 L2 input/output declarations.
- The v0.5.0 release note states a total of 3,723 while its listed level counts sum to 3,724.
- CR-BP-30a records 145 BPMN processes and a workbook acceptance threshold of at least 3,724 rows, the latter including a header row. These package-specific figures must be verified against the actual generated artifacts, not mechanically changed.

The historical v0.5.0 release record shall remain immutable. Corrections to user-facing current counts belong in current documentation and the next release notes.

### 2.5 L2 ownership and decomposition registers

The same duplicate identity is present in two further L2 artefacts:

- `reconciliation/closure/ownership-register.json`: 146 dispositions but 145 unique `bp_id` values. The duplicate is `processes:process-pr-improve-t6uvan`, repeated as the documentation-manifest row.
- `reconciliation/l2-inventory.json`: 146 inventory rows with the same duplicate L2 identity.

The EXT-22 reconciliation matrix contains 2,901 rows, but its distinct identity sets resolve to 145 L2 Processes, 580 L3 Activities and 2,900 L4 Tasks. Its additional row is the known deprecated L2 process with no decomposition; this is a reconciliation case, not an additional canonical entity. The matrix must retain this explicit structural disposition rather than be forced to the 2,900-task cardinality.

The EXT-12 inputs/outputs manifest is dated 2026-10-19 and reports 3,882 scanned YAML records with zero findings. That report is useful evidence of the validator run, but it is not proof that the current L2 identity population is 146. The README's 146/146 L2 statement must be revalidated against the 145 physical L2 identities and the relevant validator's actual scope.

## 3. Objectives

CR-BP-238 shall:

1. Establish a deterministic filesystem inventory of L0-L4 canonical entity records.
2. Validate identifier uniqueness and the relationship between record identifiers, filenames and entity kinds.
3. Reconcile the filesystem inventory with the generated `CATALOG.yaml` entity set and state counts.
4. Reconcile the lifecycle and ownership registers, plus the L2 inventory, one-to-one with canonical entity identities, retaining retired entities exactly once.
5. Identify duplicate, orphaned, missing, misclassified and legacy records without deleting source evidence.
6. Establish a current, commit-addressed inventory baseline distinct from the dated EXT-24 programme-closure baseline.
7. Reconcile all current count claims in README, reports, registers, release builders and package tests.
8. Provide a machine-readable reconciliation report and a strict conformance check.
9. Make inventory and lifecycle reconciliation a release-package precondition.
10. Establish a release pathway that promotes only reproducible, internally consistent catalogue snapshots.

## 4. Normative inventory contract

### 4.1 Canonical population

A canonical entity is a governed L0-L4 entity record represented in the canonical entity tree under `entities/v1-alpha/`.

The inventory shall:

- include active and retired canonical entity records;
- count each canonical identifier exactly once;
- classify records by the L0-L4 entity-kind contract;
- exclude research files, candidate research material, documentation manifests, generated reports and other non-entity support artefacts;
- preserve retired identities and lifecycle state rather than treating retirement as physical deletion.

### 4.2 Identity and cardinality

For the inventory commit:

- every canonical entity identifier must be unique;
- every canonical entity file must resolve to exactly one identifier;
- every lifecycle-register row must resolve to exactly one canonical entity identifier;
- every canonical entity identifier must have exactly one lifecycle-register row;
- entity kind and lifecycle state must agree across the source record, lifecycle register and generated index;
- no count may be inferred from a stale baseline or copied from a prior release.

### 4.3 Source authority

| Concern | Authority |
|---|---|
| Entity existence, identity and canonical file location | Canonical entity files |
| Generated discovery/index representation | `CATALOG.yaml`, regenerated by `scripts/regenerate_catalog.py` |
| Lifecycle state, review and governance metadata | Lifecycle register, reconciled to canonical identities |
| Historical programme closure | Dated EXT-24 closure baseline and report |
| Current population and reconciliation status | Commit-addressed current inventory baseline/report |
| Package contents and provenance | Release-package manifest generated from the tagged source commit |

A generated representation must not become an independent source of entity identity.

## 5. Implementation plan

### Slice A — Read-only inventory audit (this implementation PR)

- Add `scripts/check_canonical_inventory.py`.
- Add focused tests for level classification, duplicate identities, path/identifier consistency, lifecycle coverage, baseline drift and index agreement.
- Produce deterministic machine-readable findings and a human-readable command result.
- Keep the checker read-only; do not rewrite entity files or registers during discovery.
- Update the generated catalogue index's open-CR count for this CR.

### Slice B — Register and baseline correction (implemented in this PR)

- Removed the duplicate documentation-manifest row from the lifecycle register, ownership register and L2 inventory while retaining the canonical `Operate Customer Retention Programs` identity and ownership disposition.
- Removed the legacy `dea:research-l2-admission-dea-process-effect-regulator-mandated-governance-unwind` row from the canonical lifecycle register. The original admission deposition remains preserved at `entities/v1-alpha/ge-retire/Regulated-Governance-Unwind/Effect-Regulator-Mandated-Governance-Unwind/research/l2-admission-deposition.yaml`, linked to parent process `processes:process-ge-retire-mjq5hg`.
- Reconciled lifecycle population to 3,723 rows / 3,723 unique IDs; ownership to 145 rows / 145 unique L2 IDs; L2 inventory to 145 rows / 145 unique L2 IDs.
- Confirmed 145/145 canonical L2 records declare both inputs and outputs in the reconciled L2 inventory.
- Published `reconciliation/closure/current-inventory-baseline.json`, commit-addressed to the canonical entity snapshot at `f88472eac891331801400028ba3270cb64444cd3`.
- Preserved the 2026-10-20 EXT-24 programme-closure baseline unchanged.
- Corrected the README's current L2 I/O coverage statement from 146/146 to 145/145.
- Extended the inventory audit and tests to check ownership and L2 inventory identity sets, duplicates, I/O declaration coverage and the current baseline.
- Corrected the EXT-19 L2 inventory generator to exclude documentation/support mirrors from all canonical scans; reconciled its L2 backfill manifest and L2-to-L3 matrix to the 145-record population. The one genuine L2 decomposition gap remains explicitly reported.

No canonical entity record or identity was changed. The current baseline's source commit identifies the entity snapshot inventoried; subsequent governance-only reconciliation commits do not change that entity snapshot.

### Slice C — Continuous conformance and report freshness

- Keep the canonical inventory checker as a blocking gate in the main conformance pipeline and release-publication workflow. This enforcement was introduced in PR #240 after Slice B's register and baseline corrections.
- Require current-baseline agreement and one-to-one lifecycle, ownership and L2 inventory identity coverage.
- Add a generated-report freshness check so any committed or published inventory report is demonstrably generated from the exact canonical entity snapshot and current governed-register state it claims to represent.
- Require the checker and freshness validation to fail on duplicate or missing lifecycle identities, index drift, unexplained records, baseline mismatch, stale report inputs or report/source-commit disagreement.
- Retain approved exceptions only through explicit, evidence-backed dispositions; an exception must never be inferred from a warning.
- Preserve the distinction between the canonical entity snapshot commit and later governance-only commits when validating the baseline's source-commit reference.

### Slice D — Reproducible release-package integration

- Make the reconciled inventory a required input to `publish-versioned.yml`; the strict inventory precondition is already wired by PR #240.
- Ensure the map, workbook, BPMN, decisions log, dispositions, contributions, canonical source snapshot, publication assets and MANIFEST derive from the same tagged source commit and, where applicable, the same versioned publication model.
- Record source commit, toolchain and dependency pins, inventory counts, entity-state counts, artifact hashes, model digest and tag-signature verification in the release manifest.
- Validate package determinism at both artifact and archive level, including package counts against the current inventory baseline.
- Normalize archive entry ordering, timestamps and permissions so the ZIP itself is reproducible, not only its constituent generated files.
- Derive generated release-note dates from the tagged source commit rather than the wall-clock date, so rebuilding a tag cannot change package bytes.
- Publish the curated `release-notes/vN.M.P.md` as the GitHub Release notes and set the release/prerelease classification explicitly; do not substitute unreviewed auto-generated notes.
- Verify the annotated tag signature in the publication workflow and record the verified signer/fingerprint in the manifest.
- Reconcile the release-cut procedure's hard-coded gate-count language with the current versioned conformance registry; release readiness must follow the active gate inventory, not a stale numeric total.
- Decide and document whether schemas, profiles and controlled vocabularies are included in the self-contained package or referenced through immutable dependency pins.
- Keep artifact versions lockstep with the catalogue release version, per CR-BP-30 decision D6.

No canonical entity is to be deleted, renamed or semantically rewritten merely to reconcile a count.

## 6. Release package strategy

The release package is the governed distribution unit for the catalogue. A Git tag without a complete, reproducible and verified package is not a completed catalogue release.

### 6.1 Release layers

1. **Canonical source layer** — entity records, schemas, controlled vocabularies, lifecycle and reconciliation registers.
2. **Machine index layer** — regenerated `CATALOG.yaml`, inventories and machine-readable reports.
3. **Consumer artifact layer** — process map HTML/PNG, XLSX workbook, BPMN seed library, decisions log, dispositions and contribution evidence.
4. **Provenance layer** — release notes, MANIFEST, SHA-256 hashes, source commit, dependency pins and signature-verification evidence.

All layers in a release must represent the same source commit and release version.

### 6.2 Release readiness contract

A release candidate shall not be promoted until:

- the canonical inventory audit is clean;
- the lifecycle register has exactly one row per canonical identity;
- `CATALOG.yaml` is freshly regenerated and passes schema and structural validation;
- generated READMEs and derived reports are fresh;
- the complete required conformance pipeline and all three established CI workflows succeed on the proposed tag SHA, using the active gate registry rather than a hard-coded historical gate count;
- the release-package validation workflow passes, including deterministic rebuild comparisons at both artifact and archive level;
- the package release notes, GitHub Release notes, tag date and manifest all identify the same version and source commit;
- every advisory finding is visible and has an explicit governance disposition under the existing conformance and exception policies;
- package contents, row counts, process counts and manifest hashes reconcile to the same source commit;
- dependency pins and the ECF/metamodel contract are declared;
- the release tag is signed and its signature is verified in accordance with CR-BP-116.

CR-BP-238 does not silently weaken the existing blocking/advisory gate policy. Any change to release acceptance of advisory findings requires an explicit governance decision and corresponding CR.

### 6.3 Version pathway

The current version policy remains authoritative:

| Release class | Trigger | Application |
|---|---|---|
| Patch | Documentation, generated-index, lifecycle-register or governance reconciliation without a canonical semantic or identity change | Candidate next cut: **v0.5.1**, after Slices B and C are complete and all release gates pass |
| Minor | Canonical admission/retirement wave, material non-breaking catalogue evolution or an ECF domain rename cascade | Increment the 0.x minor version |
| Major 1.0.0 | Stable catalogue contract and sustained operational conformance, with upstream ECF at a stable point | Promote only when the 1.0 exit criteria below are met |

The v0.5.0 release record is retained as historical evidence. Its count inconsistency is corrected in current reporting and the next release notes, not by rewriting the already-published release history. The current v0.5.0 GitHub Release is marked as a prerelease, and its post-cut note records that the tag is annotated but not GPG-signed. The next cut must explicitly resolve both release classification and signing; the existing deviation is not to become the default.

### 6.4 1.0.0 exit criteria

The catalogue may be considered for 1.0.0 only when all of the following are evidenced:

1. The current canonical inventory, catalogue index and lifecycle register reconcile without unexplained differences.
2. The upstream ECF/metamodel dependency is at an explicitly stable and supported contract.
3. The normative schemas, profiles, vocabularies, identity rules and decomposition contracts have controlled compatibility and migration policies.
4. All blocking conformance gates pass; remaining advisory findings have explicit owners, evidence, review dates and approved dispositions.
5. Operational ownership, lifecycle review, evidence refresh and change-impact governance are functioning rather than merely documented.
6. At least two consecutive release cycles demonstrate reproducible packages, verified provenance and sustained conformance.
7. Downstream consumers can identify and pin the source version, dependency contract and package artifacts without ambiguity.
8. The release-signing and verification procedure is operational and evidenced.

## 7. Explicit exclusions

CR-BP-238 does not:

- redefine the World Semantic Foundation Process concept or the OpenDEA Process kernel;
- change the Business Process specialization or the L0-L4 decomposition semantics;
- create new process entities to make totals match;
- change canonical IDs or entity names as a count-reconciliation technique;
- delete research artefacts or historical evidence;
- rewrite the historical EXT-24 closure baseline or the v0.5.0 release record;
- introduce a new package format or replace the CR-BP-30 artifact family;
- declare the catalogue 1.0-ready merely because the inventory totals reconcile.

## 8. Acceptance criteria

CR-BP-238 is complete when:

1. A deterministic inventory tool enumerates every canonical L0-L4 entity record and reports per-level counts.
2. The tool validates identifier uniqueness, file/identifier consistency and entity-kind classification.
3. The catalogue index and canonical filesystem inventory agree exactly.
4. The lifecycle and ownership registers and L2 inventory contain exactly one row for every applicable canonical entity identity and no unexplained additional rows.
5. The legacy research artefact is preserved and correctly classified outside the canonical entity lifecycle population.
6. The dated EXT-24 closure baseline remains immutable and a current commit-addressed baseline is available.
7. Current README, status reports, release builders and package tests use reconciled counts.
8. The inventory check is enforced in CI and in release publication.
9. The release package is reproducible, version-consistent and traceable to its tagged source commit.
10. The next release is cut only after the stable-base conditions and release-readiness contract are satisfied.

## 9. Implementation status and evidence

Implementation status is recorded incrementally. Completion of an implementation slice does not, by itself, constitute acceptance of CR-BP-238 as a whole.

### Slice A — Read-only inventory audit: implemented

Implemented by [PR #239](https://github.com/technehub-labs/dea-catalog-business-processes/pull/239), merged 2026-11-26 at `f88472eac891331801400028ba3270cb64444cd3`.

- Added the read-only canonical inventory auditor and focused tests.
- Established the initial 3,723-file L0-L4 population and exposed the lifecycle, ownership and L2 inventory discrepancies.
- Kept the first-slice audit informational while the known register defects remained unresolved.

### Slice B — Register and baseline correction: implemented

Implemented by [PR #240](https://github.com/technehub-labs/dea-catalog-business-processes/pull/240), merged 2026-11-26 at `05e57aadfb2f17101f354dc1d220b721b86ad36d`.

- Reconciled the lifecycle register to 3,723 rows and 3,723 unique canonical identities.
- Reconciled the ownership register and EXT-19 L2 inventory to 145 unique L2 identities each.
- Preserved the research deposition and historical EXT-24 closure baseline.
- Published the current commit-addressed inventory baseline against the unchanged canonical entity snapshot at `f88472eac891331801400028ba3270cb64444cd3`.
- Corrected current-facing L2 input/output coverage to 145/145 and repaired the EXT-19 generator's canonical scan scope.
- Left the genuine L2 decomposition gap explicitly visible.

No canonical entity record, canonical ID or entity semantic content was changed by these register corrections.

### Slice C — Continuous conformance: partially implemented

PR #240 promoted the inventory audit to strict/blocking execution in the main CI workflow and made it a release-publication precondition in `.github/workflows/publish-versioned.yml`. The focused inventory tests and strict audit are part of the validation path.

Outstanding work:

- Generated inventory-report freshness enforcement, including source-snapshot and governed-register provenance.
- Explicit validation that any committed or published report is current for the source state it describes.
- Final evidence that the freshness rule is blocking in both conformance and release contexts.

### Slice D — Release-package integration: partially implemented

PR #240 established the strict inventory precondition in the release workflow. The broader release contract remains outstanding, including deterministic artifact and ZIP construction, normalized archive metadata, curated release-note and release-classification controls, tag-signature verification and signer provenance, active conformance-registry alignment, dependency/schema packaging policy, and lockstep artifact versioning.

### Acceptance posture

CR-BP-238 remains **Proposed / in implementation**. It shall not be marked Accepted or Complete until all ten acceptance criteria in §8 are satisfied with repository evidence. In particular, the strict inventory gate does not imply that the full release package is already reproducible, signed, provenance-complete or ready for publication.

The next implementation work may proceed under the dependent CR-BP-239 publication-model contract, but no release may be cut until the remaining CR-BP-238 and CR-BP-239 release-readiness requirements are satisfied.

---

**Decision requested:** approve CR-BP-238 as the governing reconciliation and release-foundation change. Slice A and Slice B are implemented; Slices C and D remain partially implemented and require the evidence and work recorded above.
