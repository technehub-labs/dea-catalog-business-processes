# Implementation and Adoption Plan

> **Stage 1 output 4 of CR-BP-121 (renumbered from CR-BP-16).**
> The ordered follow-on CRs, acceptance criteria, migration policy, and CI enforcement for the General Entity System in `dea-catalog-processes`.
> Foundation: [00-charter.md](00-charter.md), [01-existing-decisions-and-gap-register.md](01-existing-decisions-and-gap-register.md), [02-normative-design-proposal.md](02-normative-design-proposal.md).

## 1. Implementation sequence (6 stages; CR-BP-121 covers Stage 1; Stages 2-6 are follow-on CRs)

The implementation follows the 6 stages of CR-BP-16 / CR-BP-121. Stage 1 (this CR) is the recon + charter slice. Stages 2-6 are follow-on slices, each with its own carrier CR and PR.

### Stage 1: Reconnaissance and Disposition (CR-BP-121, this CR)

**Outputs (in this PR):**
- `docs/entity-system/00-charter.md` (Stage 1 output 1)
- `docs/entity-system/01-existing-decisions-and-gap-register.md` (Stage 1 output 2)
- `docs/entity-system/02-normative-design-proposal.md` (Stage 1 output 3)
- `docs/entity-system/03-implementation-and-adoption-plan.md` (Stage 1 output 4, this file)
- `change-requests/CR-BP-121-general-entity-system-stage-1.md` (the carrier CR)
- `change-requests/README.md` (new row)
- `CHANGELOG.md` (new entry)
- `CATALOG.yaml` (regenerated after the above edits)

**Acceptance criteria:**
- AC-01 The 4 Stage 1 outputs exist in `docs/entity-system/`.
- AC-02 The carrier CR is filed under `change-requests/CR-BP-121-...md`.
- AC-03 The CR README + CHANGELOG have a new row / entry.
- AC-04 `python3 scripts/regenerate_catalog.py --check` returns 0 (CATALOG.yaml is current).
- AC-05 D-004 (no en/em-dash, no U+2E3B) is clean across all new/modified files.
- AC-06 The 9 N-classification decisions in the Gap Register each have a normative rule in the Normative Design Proposal.
- AC-07 The 7 U-classification open questions each have a disposition (codified, deferred, or out-of-scope).

### Stage 2: Specification and Approval (CR-BP-122)

**Outputs (separate PR):**
- `docs/entity-system/specs/01-identity-standard.md` (the Identity Standard normative spec)
- `docs/entity-system/specs/02-entity-contract-standard.md` (the Entity Contract Standard normative spec)
- `docs/entity-system/specs/03-relationship-standard.md` (the Relationship Standard normative spec)
- `docs/entity-system/specs/04-lifecycle-standard.md` (the Lifecycle Standard normative spec)
- `docs/entity-system/specs/05-conformance-standard.md` (the Conformance Standard normative spec)
- `change-requests/CR-BP-122-entity-system-specifications.md` (the carrier CR)
- `change-requests/README.md` + `CHANGELOG.md` updates
- `CATALOG.yaml` regen

**Acceptance criteria:**
- AC-01 Each of the 5 spec docs is filed under `docs/entity-system/specs/`.
- AC-02 Each spec is normative: every rule is machine-verifiable or has an explicit "informational" annotation.
- AC-03 The 7 deferred U-classification open questions (U-01 cross-catalog URI; U-07 authority chain) are resolved or explicitly deferred to a follow-on CR.
- AC-04 The exception mechanism (per the Normative Design Proposal §6) is codified as a normative spec.
- AC-05 The identity-scope declaration for cross-catalog references is documented.
- AC-06 The lifecycle state machine is documented with per-transition rules and a worked example.

### Stage 3-4: Reference Implementation (CR-BP-123)

**Outputs (separate PR):**
- `scripts/check_entity_system.py` (the 5-rule umbrella gate; ES-001..ES-005)
- `reconciliation/entity-system-registry.yaml` (the registry of identity-bearing fields; data-driven)
- `tests/test_check_entity_system.py` (30+ tests; CLI, each rule, live catalog, exception mechanism)
- `.github/workflows/ci.yml` (wires the new gate under --strict; the position in the rollup is the next free number, recorded in `scripts/conformance_result.py`)
- `scripts/conformance_result.py` (the rollup position; the new gate row)
- `change-requests/CR-BP-123-entity-system-gate.md` (the carrier CR)
- `change-requests/README.md` + `CHANGELOG.md` updates
- `CATALOG.yaml` regen

**Acceptance criteria:**
- AC-01 The gate is data-driven from `reconciliation/entity-system-registry.yaml` (the same pattern as the 118a/118b/118c gates).
- AC-02 The 5 rules (ES-001..ES-005) are individually testable; the live-catalog test asserts 0 blocking findings on the current main.
- AC-03 The exception mechanism is consulted: a record carrying a review-retained verdict in `reconciliation/normalization.yaml` is not blocking.
- AC-04 The gate runs under --strict in CI; non-conformant PRs cannot merge.
- AC-05 The gate position in the rollup is documented in `scripts/conformance_result.py` and in the carrier CR.
- AC-06 D-004 is clean; the 118a/118b/118c gates remain CONFORMANT.

### Stage 5: Catalog-wide Adoption (CR-BP-124)

**Outputs (separate PR):**
- `reconciliation/entity-system-disposition-register.yaml` (per-record disposition for any non-conformant records found in Stage 3-4)
- `reconciliation/migration-id-map.yaml` (the legacy id reconciliation registry; per EGV-012; 35 `dea:` ids in entities/v1-alpha/)
- `reconciliation/cross-catalog-resolution.yaml` (the cross-catalog reference resolution registry; deferred U-01 codified if applicable)
- `change-requests/CR-BP-124-entity-system-catalog-adoption.md` (the carrier CR)
- `change-requests/README.md` + `CHANGELOG.md` updates
- `CATALOG.yaml` regen

**Acceptance criteria:**
- AC-01 The disposition register covers every record that the entity-system gate flags as non-conformant.
- AC-02 The migration id map documents every legacy `dea:` id with `old_id`, `new_id` (or `grandfathered`), `disposition`, `provenance`, `cr` (the carrier CR).
- AC-03 The cross-catalog resolution registry (if applicable) declares the target catalog + id scope for every cross-catalog relationship.
- AC-04 No bulk renames (per EGV-012); every disposition is per-record.
- AC-05 The disposition register is auditable: every entry has a `cr` (the carrier), `owner` (eaojnr), `date` (the disposition date).
- AC-06 The catalog's count of records is unchanged; the gate stays CONFORMANT on the post-disposition tree.

### Stage 6: Institutionalisation (CR-BP-125)

**Outputs (separate PR):**
- `docs/governance/entity-system.md` (the canonical doctrine; the long-form reference)
- `docs/governance/cardinal-rules.md` (add the entity-system rules to the existing cardinal-rules doc; one new section "Entity System" with EGV-001..012 references)
- `CONTRIBUTING.md` (add the entity-system requirements to the contribution flow)
- `schemas/entities/_template.yaml` (the common entity envelope, as a worked example)
- The exception process: documented in `docs/governance/exception-process.md`
- `change-requests/CR-BP-125-entity-system-institutionalisation.md` (the carrier CR)
- `change-requests/README.md` + `CHANGELOG.md` updates
- `CATALOG.yaml` regen

**Acceptance criteria:**
- AC-01 The doctrine doc is filed; the cardinal-rules doc has a new section; CONTRIBUTING.md has the new requirements.
- AC-02 The entity envelope template is in `schemas/entities/_template.yaml`; a worked example shows the envelope applied to a real record.
- AC-03 The exception process is documented (input, decision, recording, renewal, audit).
- AC-04 The conformance rollup is updated: the entity-system gate is now a blocking row in `conformance_result.py`.
- AC-05 New entity records cannot be admitted without satisfying the entity-system standard; the ADM gate consults the registry.

## 2. Migration policy (per EGV-012)

**No bulk renames.** The migration policy for `dea-catalog-processes` is:

1. **Existing records**: stay as-is. The 35 `dea:` legacy tails in `entities/v1-alpha/` are grandfathered historical record; new records MUST use the `processes:` family.
2. **Migration registry**: every legacy id is documented in `reconciliation/migration-id-map.yaml` with: `old_id`, `new_id` (or `grandfathered`), `disposition` (one of: grandfathered / admit-with-override / require-migration / retire / accept-residual), `provenance` (the CR that introduced the legacy id), `cr` (the entity-system carrier CR that codified the disposition).
3. **Cross-repo migration**: T7 of the umbrella programme cascades the entity-system gate to the 11 sibling repos. The per-repo CR docs are: BC-04, BO-04, OU-04, MF-010, MM-06, AF-04, ACT-02, BL-02, CON-02, STA-07, TEN-02.
4. **Cross-catalog references**: T8 of the umbrella programme reconciles cross-catalog references. The disposition register documents every per-record disposition.

## 3. CI enforcement

The entity-system gate runs under --strict in `.github/workflows/ci.yml` after the existing 30+ gates. The rollup row in `scripts/conformance_result.py` is the new gate position; the CI workflow's "Conformance Result" step writes the verdict to `reconciliation/conformance_result.yaml`.

The exception mechanism is consulted by the gate: a record carrying a review-retained verdict in `reconciliation/normalization.yaml` is not blocking. The exception is logged in the gate's output for audit.

## 4. Acceptance criteria for the umbrella programme

The General Entity System is considered institutionalised in `dea-catalog-processes` when:

1. The 5 normative specs are approved and filed under `docs/entity-system/specs/`.
2. The 5-rule umbrella gate is in place and runs under --strict in CI.
3. The disposition register covers every non-conformant record.
4. The migration id map documents every legacy `dea:` id with a disposition.
5. New entity records cannot be admitted without satisfying the entity-system standard.
6. The cardinal-rules doc has a new section; CONTRIBUTING.md has the new requirements.
7. The exception process is documented and exercised (at least one review-retained verdict in `reconciliation/normalization.yaml`).
8. The umbrella programme's T7 (cross-repo cascade) is in progress; the 11 sibling repos have their per-repo entity-system CR docs.

## 5. Risks and mitigations

| Risk | Mitigation |
|---|---|
| The 5 normative specs are too rigid (cannot accommodate future types) | The spec doc notes that type-specific extension is allowed; the umbrella gate delegates to per-type gates |
| The umbrella gate's 5 rules miss a real concern (e.g. security classification) | The 5-rule decomposition is a deliberate scope decision; future concerns land as new rules (ES-006, etc.) via a new CR |
| The exception mechanism is overused (silent bypass via review-retained) | The exception is time-bounded; renewal requires a new CR; the user (eaojnr) is the only approver |
| The cross-repo cascade (T7) fails because a sibling repo has no entity-system record | The T7 cascade is gate-only for repos with 0 entity records; per-repo CR doc is the adoption vehicle |
| The migration policy conflicts with the existing mv1 migration (CR-BP-mv1) | The migration policy is a superset: per-record disposition + per-record grandfathered verdict; the 35 `dea:` legacy tails are already documented in the existing migration id map |

## 6. Cross-cutting alignment

The Implementation and Adoption Plan aligns with:

- **DEA-ID-000** (foundation paper): the 4 implementation phases + 7 workstreams
- **CR-012** (org-wide governance CR): the 6 implementation stages (Stage 1+2 = Foundation spec; Stage 3-4 = Reference implementation; Stage 5+6 = Catalog adoption; T7 = Automated enforcement; T8 = Legacy reconciliation)
- **CR-BP-16 / CR-BP-121** (this CR): the 6 stages of repo-specific implementation
- **The 118a/118b/118c cascade**: the per-repo gate copy + registry pattern; the data-driven gate architecture

## 7. Out of scope (per CR-BP-16 / CR-012)

- **Bulk renames**: explicitly forbidden (per EGV-012). The migration policy is per-record.
- **Redefinition of the canonical `BusinessProcess` concept**: the catalog instantiates the metamodel's `dea:entity-business-process`; it does not redefine it (per DEA-ID-000 §2 authority model).
- **Cross-repo governance of non-catalog repos**: the umbrella programme is scoped to the 12 catalog repos + the metamodel + the architecture framework. The semantic-architecture, ontology, and other foundation repos are out of scope (per EGV-001).
- **The 118a/118b/118c authorship cardinal rule**: that is a separate discipline (per EGV-008 the rule is referenced; the gate is the 118a/118b/118c work).

## 8. Carrier CR for Stage 1 (this CR)

`change-requests/CR-BP-121-general-entity-system-stage-1.md` references this implementation plan and the 3 other Stage 1 outputs. The carrier CR is the audit anchor for what landed in Stage 1.
