# Entity Conformance Standard

> **CR-BP-122 Stage 2 output 5.** Normative spec for the General Entity System's conformance discipline in `dea-catalog-business-processes`. Foundation: [00-charter.md](../00-charter.md), [02-normative-design-proposal.md §5-6](../02-normative-design-proposal.md). Companion: [CR-012 EGV-010, EGV-011](../../../../dea-governance/change-requests/CR-012-org-wide-entity-governance.md).

## 1. Scope

This spec codifies the **conformance discipline** for the General Entity System. The discipline is built on CR-012 normative requirements **EGV-010 (Machine-Verifiable Conformance)** and **EGV-011 (Change Enforcement)**, and includes the **exception mechanism** (the only escape hatch under EGV-011).

The discipline covers:
- The umbrella gate's 5 rules.
- The rollup integration.
- The CI enforcement.
- The exception mechanism (per EGV-011).
- The advisory-then-blocking staging.

## 2. The 5-rule umbrella gate

The entity-system gate is `scripts/check_entity_system.py`. It has 5 rules, one per concern (identity / contract / relationships / lifecycle / conformance-umbrella). The rules are data-driven from `reconciliation/entity-system-registry.yaml` (the registry of identity-bearing fields).

### CS-001 (ES-001 - Identity) - blocking

> Every record in `entities/v1-alpha/` and `contexts/v1-alpha/` SHALL have a present, format-valid, scope-bound, unique id (per the Identity Standard, IS-001..IS-006).
>
> **Verification**: the gate walks every record, asserts the id is present, format-valid (per IDM-001), scope-bound (the `processes:` namespace for new records; the grandfathered `dea:` legacy tail per IS-004), and unique (no two records share the same id).

**Source rules**: EGV-002 (stable identity), EGV-003 (identifier and namespace governance), EGV-004 (identity continuity), IS-001..IS-006. **Verification**: the entity-system umbrella gate's ES-001 rule.

### CS-002 (ES-002 - Entity Contract) - blocking

> Every record SHALL satisfy the common envelope (per the Entity Contract Standard, EC-001..EC-004). The required envelope fields are: `id`, `type`, `name`, `definition`, `lifecycle`, `provenance`. The optional fields (`description`, `relationships`, `classifications`) are validated when present.
>
> Per-type schemas (PG, BP, Activity, Task) are validated by their existing per-type gates; the umbrella gate delegates to them.

**Source rules**: EGV-005 (canonical entity contract), EC-001..EC-004. **Verification**: the entity-system umbrella gate's ES-002 rule; the per-type gates (PG-001..PG-008, BP-SEM-001..014, etc.) for type-specific fields.

### CS-003 (ES-003 - Relationship) - blocking

> Every `relationships[]` entry SHALL satisfy the Relationship Standard (RS-001..RS-005): canonical `relationship_type`, source / target type constraints, cardinality rules, `identity_scope` declaration for cross-catalog references, no competing definitions.

**Source rules**: EGV-006 (relationship and reference integrity), RS-001..RS-005. **Verification**: the entity-system umbrella gate's ES-003 rule; the existing per-type gates (MECE-001..008, BP-SEM-001..014) for cardinality and composition.

### CS-004 (ES-004 - Lifecycle) - blocking

> Every record's `lifecycle` block SHALL satisfy the Lifecycle Standard (LS-001..LS-007): governed state, transition table, identity continuity, terminal states, provenance per transition, version-separation discipline.

**Source rules**: EGV-007 (version and lifecycle separation), EGV-004 (identity continuity), LS-001..LS-007. **Verification**: the entity-system umbrella gate's ES-004 rule; the existing LCM-001..005 gate for the state machine.

### CS-005 (ES-005 - Conformance Umbrella) - blocking

> The record's per-type gate (PG-001..PG-008 for ProcessGroup, BP-SEM-001..014 for Process, the Activity/Task gates, the ProcessContext gate, the ProcessScope dormant check) SHALL also be CONFORMANT. The entity-system umbrella gate is the umbrella over the per-type gates; it does not duplicate their work.
>
> A record is CONFORMANT iff all 5 rules (ES-001..ES-005) pass. A record is NON-CONFORMANT iff at least one rule fails.

**Source rules**: EGV-010 (machine-verifiable conformance), EGV-011 (change enforcement). **Verification**: the entity-system umbrella gate's ES-005 rule; the existing per-type gates for delegation.

## 3. The rollup integration

### CS-006 (rollup position) - blocking

> The entity-system gate is a single rollup row in `scripts/conformance_result.py`. The position is the next free number when CR-BP-123 lands (Stage 3-4 of the implementation plan). The rollup's single CONFORMANCE RESULT verdict (CONFORMANT / CONFORMANT-WITH-WARNINGS / NON-CONFORMANT) is the canonical pre-merge verdict source.

**Source rules**: CR-BP-16 S18 (the conformance rollup; the single CONFORMANCE RESULT verdict), the slice skill's "Wire the gates, then regen CATALOG" discipline. **Verification**: the rollup's verdict line is the audit anchor.

### CS-007 (CI enforcement) - blocking

> The entity-system gate runs under `--strict` in `.github/workflows/ci.yml` immediately after the existing 30+ gates. Non-conformant PRs cannot merge.
>
> The gate's output (the JSON shape, the verdict line, the per-record findings) is captured by the rollup and persisted to `reconciliation/conformance_report.yaml` (regenerated each run).

**Source rules**: EGV-011 (change enforcement), the slice skill's "CI enforcement" discipline. **Verification**: the CI workflow's per-gate step + the aggregate step.

## 4. The exception mechanism (the EGV-011 escape hatch)

### CS-008 (review-retained verdict) - blocking

> The exception mechanism is the **review-retained verdict** in `reconciliation/normalization.yaml`. An exception is granted by:
>
> 1. The carrier CR explicitly requests the exception, citing the EGV-011 reason.
> 2. The user (eaojnr) approves the exception as a one-line comment on the CR.
> 3. The exception is recorded in `reconciliation/normalization.yaml` with: `verdict: review-retained`; `cr` (the carrier CR); `reviewed_by` (the approver; eaojnr); `expiry` (ISO-8601; exceptions are time-bounded; renewal requires a new CR).
> 4. The exception registry is consulted by the entity-system gate; a record carrying an exception is not blocking.
>
> Exceptions are NOT silent. They are: explicit, time-bounded, CR-linked, owner-signed, and auditable.

**Source rules**: EGV-011 (change enforcement), the precedent (CR-BP-25's review-retained verdict in `catalog-research/normalization.yaml`). **Verification**: the entity-system umbrella gate consults the registry; a record carrying an exception is not blocking.

### CS-009 (exception lifecycle) - blocking

> Exceptions have a lifecycle:
>
> - **Granted**: the verdict is `review-retained`; the carrier CR + reviewer + expiry are recorded.
> - **Active**: the current date is before the expiry; the gate does not block the record.
> - **Expired**: the current date is on or after the expiry; the gate blocks the record.
> - **Renewed**: a new CR is filed, the verdict is updated with a new expiry, the cycle restarts.
> - **Retired**: the carrier CR is closed; the verdict is updated to `retired`; the gate no longer consults the entry.
>
> Expired exceptions that are not renewed become blocking. The user (eaojnr) is the only approver of new exceptions or renewals.

**Source rules**: EGV-011, the precedent. **Verification**: the entity-system umbrella gate asserts the verdict's `expiry` is in the future (or the verdict is `retired`).

## 5. The advisory-then-blocking staging

### CS-010 (staging) - informational

> The entity-system gate ships as **advisory** under default mode and **blocking** under `--strict`. The staging is:
>
> 1. **Stage 3-4 (CR-BP-123)**: the gate is added to the rollup; the gate is **advisory** under default mode. CI runs the gate under `--strict` so the catalog can identify any false positives; the gate's findings are reported but do not block.
> 2. **Stage 5 (CR-BP-124)**: the disposition register is filed; any non-conformant records are documented with a per-record disposition. The gate is **advisory** until the disposition register is filed.
> 3. **Stage 6 (CR-BP-125)**: the gate is promoted to **blocking** under `--strict` in CI. Non-conformant PRs cannot merge.
>
> The staging is the user's DP-7 ("defer gate to Stage 3-4"); the staging here is consistent with that decision.

**Source rules**: EGV-011, the user's DP-7. **Verification**: the gate's exit code under `--strict` and the staging per CR-BP-123..125.

## 6. The registry

### CS-011 (entity-system-registry) - blocking

> The gate is data-driven from `reconciliation/entity-system-registry.yaml`. The registry declares:
>
> - The fields that the gate inspects (per envelope + per-type).
> - The cross-catalog resolution map (per RS-004 + CS-003).
> - The exception registry path (`reconciliation/normalization.yaml`; the `review-retained` verdicts).
> - The per-type schema paths (`schemas/entities/<type>.schema.json`).
>
> The registry is the single source of truth for the gate's configuration. Changing the gate's behavior is a YAML edit, not a code change.

**Source rules**: the 118a/118b/118c data-driven gate pattern (per CR-BP-118, CR-BP-118c). **Verification**: the gate reads the registry on every run; the registry is a YAML file in the repo.

## 7. Acceptance criteria

- AC-CS-01 The 5 rules (ES-001..ES-005) are individually testable; the live-catalog test asserts 0 blocking findings on the current main.
- AC-CS-02 The exception mechanism is consulted: a record carrying a review-retained verdict in `reconciliation/normalization.yaml` is not blocking.
- AC-CS-03 The gate runs under `--strict` in CI; non-conformant PRs cannot merge.
- AC-CS-04 The gate position in the rollup is documented in `scripts/conformance_result.py` and in the carrier CR.
- AC-CS-05 The gate is data-driven from `reconciliation/entity-system-registry.yaml`; changing the gate's behavior is a YAML edit, not a code change.
- AC-CS-06 The staging is honored: the gate is advisory in Stage 3-4 and Stage 5, blocking in Stage 6.

## 8. Cross-references

- CR-012 EGV-010, EGV-011 (the org-wide normative requirements)
- The 118a/118b/118c data-driven gate pattern (per CR-BP-118, CR-BP-118c)
- The Identity Standard (§1) for ES-001
- The Entity Contract Standard (§2) for ES-002
- The Relationship Standard (§3) for ES-003
- The Lifecycle Standard (§4) for ES-004
- The Exception Mechanism precedent (CR-BP-25's review-retained verdict)
- The per-type gates (PG-001..PG-008, BP-SEM-001..014, MECE-001..008, LCM-001..005, etc.) for ES-005 delegation
- The implementation plan ([03-implementation-and-adoption-plan.md §1](../03-implementation-and-adoption-plan.md)) for the staging discipline
