# Entity System Doctrine

> **CR-BP-125 Stage 6 deliverable.** The canonical doctrine for the General Entity System in `dea-catalog-business-processes`. Companion: [DEA-ID-000](../../../../dea-governance/docs/design/entity-system-foundation.md) (the foundation paper), [CR-012](../../../../dea-governance/change-requests/CR-012-org-wide-entity-governance.md) (the org-wide governance CR), [00-charter.md](../00-charter.md), [the 5 spec docs in specs/](../specs/).

## 1. Purpose

This doctrine establishes the General Entity System as the **mandatory entity-governance baseline** for `dea-catalog-business-processes`. The entity system governs how every record in this catalog is **identified, typed, related, evolved, and validated** over time. The doctrine is the long-form reference; the cardinal-rules (in `cardinal-rules.md`) are the pinnable rules; the specs (in `specs/`) are the normative rules; the gate (in `scripts/check_entity_system.py`) is the enforcement mechanism.

## 2. Scope

The doctrine applies to:

- All entity records in `entities/v1-alpha/**`, `contexts/v1-alpha/**`, and any future `entities/<version>/` directories.
- All change requests in `change-requests/CR-*.md` whose body or header carries an entity-affecting change.
- All governance documents in `docs/governance/`, `docs/architecture/`, `docs/identity/`, `docs/identity.md`, `docs/classification.md`, `docs/relandscape.md`, and `docs/conformance.md`.
- The conformance pipeline (`scripts/conformance_result.py`, every gate listed therein, every CI workflow in `.github/workflows/`).
- The cross-repo references (ECF coordinates; cross-catalog `relationships[]` entries; the `metamodel-pointer.yaml`).
- Future catalog versions (`entities/v2-alpha/`, etc.) introduced through approved CRs.

The doctrine does NOT apply to:

- Vendored content (e.g. `.metaframework/` from CI's checkout of `dea-metaframework`).
- The `01_plan/` directory (tranche planning documents; pre-decisional).
- Generated content (e.g. `reconciliation/conformance_report.yaml`; regenerated each gate run).
- Reconciliation and migration tooling (these are governed by their own change requests).

## 3. The 5 concerns (per DEA-ID-000 §1)

The General Entity System is built on 5 distinct concerns. Each concern has a normative spec, a gate rule, and a discipline:

1. **Entity identity** (Identity Standard IS-001..IS-006): persistent, scope-bound, unique. The `processes:` namespace is canonical; the `dea:` family is grandfathered per EGV-012. The corrected IDM-001 pattern `^[a-z]+:[a-z]+(-[a-z]+){1,4}-[a-z2-9]{6}$` covers all 5 type families (process- / pc- / group- / activity- / task-).
2. **Entity semantics** (Entity Contract Standard EC-001..EC-004): the common envelope + 5 type-specific profiles. ProcessContext uses a slim profile (id + name); the other 5 types use the full envelope (id + type + name + definition + lifecycle + provenance).
3. **Entity relationships** (Relationship Standard RS-001..RS-005): 3 stored types (`composes` / `realizes` / `specializes`) + 1 forbidden (`part-of`, derived view-time only). Cross-catalog references carry `identity_scope` per IS-006 + RS-004.
4. **Entity lifecycle** (Lifecycle Standard LS-001..LS-007): 5-state machine (proposed / admitted / deprecated / retired / superseded); identity continuity per EGV-004; version-separation per EGV-007.
5. **Entity conformance** (Conformance Standard CS-001..CS-011): 5-rule umbrella gate (ES-001..ES-005) at `scripts/check_entity_system.py`; data-driven from `reconciliation/entity-system-registry.yaml`; the exception mechanism (CS-008/CS-009) consults `reconciliation/normalization.yaml`.

## 4. Authority model (per DEA-ID-000 §2)

```
OpenDEAM Architecture Framework  (dea-architecture-framework)
  └─ Architectural authority: ADRs that resolve architecture-level conflicts

ECF + Canonical Metamodel        (dea-metaframework + dea-metamodel)
  └─ Entity-type definitions, properties, relationships

General Entity System            (dea-governance; THIS REPO's domain)
  └─ Identity, lifecycle, references, governance, conformance

Business Process Catalog         (dea-catalog-processes; THIS REPO)
  └─ Process-specific profiles and instances
```

`dea-catalog-processes` instantiates the metamodel through profiles that conform to the entity system. The metamodel is the cross-reference for entity-type definitions; the architecture framework is the architectural authority; the governance repo is the identity/lifecycle/conformance authority.

## 5. The cardinal rules (per CR-118 / EGV-008)

The authorship cardinal rule (per CR-118a/b/c) is cross-referenced by EGV-008. Every authorship-bearing field in any governed artifact SHALL carry `Emmanuel A. Otchere` (or, for org-level CITATION.cff authors, `TechNeHub Labs`). The authoring-tool denylist (Coder, Agent, Hermes, Claude, GPT, Cline, OpenAI, MiniMax, MiniMax-M3) is enforced by the authorship gate at `scripts/check_authorship.py` and the prose gate at `scripts/check_prose_authorship.py`.

## 6. The exception mechanism (per CS-008/CS-009)

The only escape hatch under EGV-011 is the **review-retained verdict** in `reconciliation/normalization.yaml`. An exception is granted by:

1. The carrier CR explicitly requests the exception, citing the EGV-011 reason.
2. The user (eaojnr) approves the exception.
3. The exception is recorded with: `verdict: review-retained`; `cr` (the carrier CR); `reviewed_by`; `expiry` (ISO-8601); `excepted_rules: [...]`.
4. The entity-system gate consults the registry; a record carrying an exception is not blocking for the excepted rules.

Exceptions are NOT silent. They are: explicit, time-bounded, CR-linked, owner-signed, and auditable.

## 7. The migration policy (per EGV-012)

No bulk renames. Existing records stay as-is; the 35 `dea:` legacy tails in `entities/v1-alpha/` are grandfathered per `reconciliation/migration-id-map.yaml`. New records MUST use the `processes:` family. A future migration CR (T8 of the umbrella programme) may deprecate the 35 legacy ids; the migration is per-record with a `superseded` lifecycle state transition.

## 8. Adoption (per CR-BP-123/124/125)

The entity system is adopted in this catalog as:

- **Stage 1 (CR-BP-121)**: reconnaissance + charter (the 4 doc outputs).
- **Stage 2 (CR-BP-122)**: specifications (the 5 spec docs).
- **Stage 3-4 (CR-BP-123)**: reference implementation (the umbrella gate).
- **Stage 5 (CR-BP-124)**: catalog adoption (the disposition register + cross-catalog resolution).
- **Stage 6 (CR-BP-125, this doctrine)**: institutionalisation (the gate is promoted to blocking; the cardinal rules are updated; the contribution flow includes the entity-system requirements; the exception process is documented).

After Stage 6, **no new entity can be admitted without satisfying the entity-system standard**. Exceptions are governed, not silent.

## 9. Cross-cutting alignment

The doctrine aligns with:

- **DEA-ID-000** (foundation paper): the 5-concern taxonomy, the authority model, the 7-workstream taxonomy, the 4-phase adoption programme.
- **CR-012** (org-wide governance CR): the 12 EGV-001..012 normative requirements; the 8 deliverables; the 6 implementation stages.
- **ADR-0001** (OpenDEAM governance): the OpenDEAM root model authority; the 6-layer ecosystem-on-top model.
- **ADR-0004** (v0.4.0 cleanup): the L2 cleanup + vocabulary purge; the catalog version discipline.
- **ADR-0006** (process-kernel + specialisation): the kernel + specialisation discipline that CR-BP-SPEC-BP-01 codifies.

## 10. Success criteria

The entity system is considered institutionalised in this catalog when:

1. The 5 normative specs are approved and filed under `docs/entity-system/specs/`.
2. The 5-rule umbrella gate is in place and runs under `--strict` in CI (advisory in Stage 3-4 and Stage 5; blocking in Stage 6 per CS-010).
3. The disposition register covers every non-conformant record (per EGV-012; no bulk renames; per-record grandfathered / accept-residual / require-migration / retire).
4. The migration id map documents every legacy `dea:` id with a disposition.
5. New entity records cannot be admitted without satisfying the entity-system standard; the ADM gate consults the registry.
6. The cardinal-rules doc has a new section; CONTRIBUTING.md has the new requirements.
7. The exception process is documented and exercised (the review-retained verdict in `reconciliation/normalization.yaml`).
8. The umbrella programme's T7 (cross-repo cascade) is in progress; the 11 sibling repos have their per-repo entity-system CR docs.
