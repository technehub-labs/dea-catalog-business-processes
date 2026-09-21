# CR-BP-SPEC-BP-01: Business Process Specialization Catalog

> **Layout note (CR-BP-mv1, 2026-09-20):** This CR was authored against the
> pre-migration entity layout (`entities/v1-alpha/dea:*`, `contexts/v1-alpha/`)
> and the legacy `dea:*` id family, and may reference the pre-rename repo name
> `dea-catalog-processes`. Paths, ids, and repo names cited below are historical;
> see `reconciliation/migration-id-map.yaml` for the old-to-new id mapping and
> the dea-metaframework `docs/entity-storage-layout.md` for the current
> containment tree.

| Field | Value |
|---|---|
| **CR** | CR-BP-SPEC-BP-01 |
| **Title** | Business Process Specialization Catalog |
| **Status** | Proposed (working-folder draft; awaiting sign-off) |
| **Type** | Catalog specialization + governance |
| **Scope** | `technehub-labs/dea-catalog-processes` |
| **Predecessor** | CR-MM-PROC-01 (kernel + specialization; **must land first**); CR-BP-01 (catalog-side, superseded premise; this CR re-anchors its governance work on the correct premise) |
| **Authority** | WSF (`wsf:Process`; Tier-3 derived construct); `dea:Process` (Core kernel); `dea:BusinessProcess` (Core specialization) |
| **Author** | Coder (for eaojnr) |
| **Date** | 2026-09-03 |

## 1. Change Request

Reframe the Business Process Catalog (`dea-catalog-processes`) as
the **Business Process specialization catalog** under the OpenDEA
Metamodel's Process kernel + specializations discipline (CR
-). The
catalog now declares **two** entity ids in its metamodel pointer:

```
dea:Process              (abstract Core kernel; not directly instantiated)
  legacy_identifiers: [dea:entity-process, Process]

dea:BusinessProcess      (Core specialization; instantiated)
  legacy_identifiers: []    # no legacy; the legacy is on the kernel
```

The catalog retains all of CR-BP-01's governance / validator / CI
work (preserved byte-equivalent from `a34c7ff`) and re-anchors it
on the new canonical structure. The `dea:BusinessProcess` schema
title in `schemas/entities/process.json` is renamed from `"Process"`
to `"Business Process"` as a minor cleanup.

## 2. Why This CR Exists Now

CR-BP-01 (merged at `a34c7ff` on `dea-catalog-processes`) was
drafted under the assumption that `dea:BusinessProcess` is the
sole canonical OpenDEA semantic identity for Process. CR-MM-PROC-01
reverses that premise: `dea:BusinessProcess` is a **specialization**
of the abstract Core kernel `dea:Process`.

This CR:

- acknowledges that CR-BP-01's premise was wrong;
- preserves CR-BP-01's reusable artifacts (governance doc,
  validator, CI wire, README/CHANGELOG);
- re-anchors them on the correct kernel + specialization structure.

## 3. Architectural Position

```
WSF
 └─ Process              (Tier-3 derived; structural activity organization)

      └─ DEA inherits via specialization:

            dea:Process             (abstract Core kernel; CR-MM-PROC-01)
              │
              ├── dea:BusinessProcess   (Core specialization; this catalog)
              │       ├─ dea-catalog-processes (Business Process specialization catalog)
              │       ├─ ECF: business architecture use case
              │       ├─ supports: business operations
              │       ├─ sub-classifications (catalog-internal, not kernels):
              │       │     · operational  (process_intent: operational)
              │       │     · support      (process_intent: support)
              │       │     · management   (process_intent: management)
              │       └─ … future Business Process sub-classifications as
              │             needed (catalog governance, not kernel entities)
              │
              └── (future specializations; gated on use case)
                    · dea:OperationalProcess (operations context)
                    · dea:EngineeringProcess (engineering context)
                    · … others
```

The catalog at `dea-catalog-processes` is one of potentially several
Process-specialization catalogs; other specializations will get
their own catalogs (or sub-folders) when their use cases emerge.

## 4. Decisions

**Decision BP-SPEC-01-D01** — The catalog's metamodel pointer
declares **two** entity ids: `dea:Process` (kernel) and
`dea:BusinessProcess` (specialization). The kernel is abstract
and is not directly instantiated; the specialization is the
catalog's subject.

**Decision BP-SPEC-01-D02** — The legacy id `dea:entity-process`
is recorded under `dea:Process.legacy_ids` (as a pre-WSF authority
id), not under `dea:BusinessProcess.legacy_ids`. This reflects that
the legacy id was the pre-WSF root model identifier for the
general Process concept, not for Business Process specifically.

**Decision BP-SPEC-01-D03** — The catalog's CR-BP-01 §7 canonical
definition ("A structured set of activities that produces a
defined outcome") is preserved verbatim as the Business Process
**specialization** definition. The kernel `dea:Process` carries
the WSF-derived definition ("A structural organization of
activities into a meaningful temporal/causal pattern").

**Decision BP-SPEC-01-D04** — The catalog sub-classifications
(`operational` / `support` / `management` carried by the
`process_intent` field) remain catalog-internal semantics, not
kernel entities. This preserves the CR-BP-01 §6 "no semantic
expansion" promise.

**Decision BP-SPEC-01-D05** — The CR-BP-01 §6 Decision BP-01-D02
("No generic normative entity named `dea:Process` will be
introduced") is **superseded**. CR-MM-PROC-01 introduces
`dea:Process` as the abstract Core kernel; the CR-BP-01
decision's intent (no Business Process confusion with a
generic Process entity) is preserved by the kernel + specialization
discipline itself.

## 5. Required Changes — `dea-catalog-processes`

### 5.1 Revert CR-BP-01's pointer + validator changes

This CR **re-anchors** the work landed at `a34c7ff` (PR #10).
Specifically, before opening this CR's PR:

- A revert PR (PR #11) reverts the `a34c7ff` merge on
  `dea-catalog-processes`, restoring the pre-BP-01 state of:
  `metamodel-pointer.yaml` (with the original
  `dea:entity-process` id and the `v0.2.1` root-model pin),
  absence of the BP-01 validator, and absence of the
  BP-01 governance doc.
- The revert is a single commit (`git revert -m 1 a34c7ff`).
  No conflict is expected; `a34c7ff` has only `main` as parent.

This CR's PR then lands its own updates on the clean tree.

### 5.2 `metamodel-pointer.yaml` — declare both ids

Replace the post-BP-01 pointer with:

```yaml
# Metamodel Pointer: Business Process Catalog
# CR-BP-SPEC-BP-01 alignment (refines + supersedes CR-BP-01 PR #10).
#
# Authority chain:
#   - WSF (org): wsf:Process (Tier-3 derived; structural activity organization)
#   - dea-metamodel (Core authority): dea:Process (abstract kernel) +
#     dea:BusinessProcess (Core specialization); CR-MM-PROC-01; PR #163.
#   - dea-architecture-framework (root model v0.6.0): dea:entity-process
#     (abstract kernel; class_alias PRC; discriminator process-kernel) +
#     dea:entity-business-process (specialization; class_alias BP);
#     CR-AR-FMWK-01; PR #10 + tag v0.6.0.
#   - dea-catalog-processes (catalog authority): this pointer declares
#     both ids in the multi-entity form so the consumer-validator
#     (scripts/validate_consumer.py; v0.6.0 abstract-kernel branch)
#     recognizes the kernel + specialization contract.

metamodel:
  version: v0.6.0
  # The primary subject uses the OpenDEAM root-model id
  # (dea:entity-business-process), not the metamodel Core id
  # (dea:BusinessProcess). The consumer-validator
  # (scripts/validate_consumer.py in dea-architecture-framework)
  # resolves consumer declarations against the root model 1:1.
  # The two ids are 1:1 mapped (LOSSLESS) via the federation
  # mapping recorded in dea-metamodel/metamodel/dea-metamodel.yaml
  # (CR-MM-PROC-01 §4) and in docs/governance/process-specialization.md.
  entity_id: dea:entity-business-process
  class_alias: BP
  layer: L3
  building_block: L3-value-delivery
  viewer_url: "https://technehub-labs.github.io/metamodel/?entity=BP"
  # Kernel entry (CR-MM-PROC-01; CR-AR-FMWK-01; the catalog's contract
  # with the root model). The validator verifies the kernel's
  # class_alias (PRC) and discriminator (process-kernel)). The kernel
  # entry must NOT declare layer or dimension per the v0.6.0
  # abstract-kernel branch in scripts/validate_consumer.py.
  entities:
    - entity_id: dea:entity-process
      class_alias: PRC
      discriminator: process-kernel
    # future Process specializations (dea:entity-operational-process;
    # dea:entity-engineering-process; ...) land here as additional
    # entries with their own class_alias + discriminator.

catalog:
  name: Business Process
  repo: technehub-labs/dea-catalog-processes
  status: semantic-baseline (CR-BP-SPEC-BP-01)
  specialization:
    specializes_root_model_entity: dea:entity-process
    class_alias: BP
    description: |
      The Business Process specialization of the OpenDEAM Process
      kernel. Supports Business Architecture and Business Operations
      use cases. Sub-classifications (operational / support /
      management) are catalog-internal via the process_intent field
      and do not promote to root-model entities.

links:
  metamodel_repo: https://github.com/technehub-labs/dea-metamodel
  root_model: https://github.com/technehub-labs/dea-architecture-framework
  viewer: "https://technehub-labs.github.io/metamodel/?entity=BP"
  github: https://github.com/technehub-labs/dea-catalog-processes
  change_request: change-requests/CR-BP-SPEC-BP-01.md
  governance_decision: docs/governance/process-specialization.md
```

**Note on naming convention choice (final):**

The primary `metamodel.entity_id` uses the **OpenDEAM root-model id**
(`dea:entity-business-process`) rather than the metamodel Core id
(`dea:BusinessProcess`) because the consumer-validator
(`scripts/validate_consumer.py` in `dea-architecture-framework`)
resolves consumer-declared ids 1:1 against the root model. Using the
metamodel-side id would cause the consumer validator to false-positive
as drift (`entity_id dea:BusinessProcess not in OpenDEAM model`).

The two ids are mapped 1:1 (LOSSLESS; EXACT) via the federation
mapping in `dea-metamodel/metamodel/dea-metamodel.yaml` (CR-MM-PROC-01
§4) and in the catalog's governance doc
(`docs/governance/process-specialization.md`). Both ids carry the same
canonical semantics; the choice is purely which authority's id to use
in the consumer-facing pointer.

### 5.3 Schema title cleanup

`schemas/entities/process.json` title is changed from
 `"title": "Process"` to `"title": "Business Process"`. The
 `description` field is updated to reflect the specialization:

> A business-context specialization of the OpenDEA Process kernel
> (`dea:Process`). Supports the Business Architecture and Business
> Operations use cases. Classified by intent
> (`operational` / `support` / `management`) and audience (the
> ECF domain whose work this Business Process most advances).

No structural schema changes (no `required[]` / `properties`
additions or removals).

### 5.4 Validator — extended for the dual-id declaration

`scripts/check_bp01_canonical.py` (the BP-01 artifact, byte-preserved)
is **renamed** to `scripts/check_process_specialization.py` (clearer
purpose post-kernel-introduction) and extended with the following
rules:

**BP-SPEC-01-001** — The pointer declares the **specialization**
(`metamodel.entity_id: dea:BusinessProcess`; in the root model:
`dea:entity-business-process`) as the primary `metamodel:` block.
Missing the specialization entry is a hard failure.

**BP-SPEC-01-002** — The pointer declares the **kernel** as the
first entry in the `metamodel.entities:` list, with
`entity_id: dea:entity-process`, `class_alias: PRC`, and
`discriminator: process-kernel`. The kernel entry must NOT declare
`layer` or `dimension` (per the v0.6.0 abstract-kernel branch in
`scripts/validate_consumer.py`). Missing or mis-declared kernel
entry is a hard failure.

**BP-SPEC-01-003** — The specialization entry's `class_alias` is
`BP`. Any other value is a hard failure (the BP alias is preserved
for backward compatibility with consumers pinned to pre-v0.6.0 root
model versions; cf. ADR-0006 D1).

**BP-SPEC-01-004** — The pointer's `metamodel.version` is pinned to
a `vX.Y.Z` tag that contains **both** `dea:entity-process` (kernel)
and `dea:entity-business-process` (specialization) in the root
model. v0.5.0 lacks both; v0.6.0 carries both. Pinning to a model
version that does not declare both is a hard failure.

**BP-SPEC-01-005** — The schema title in
`schemas/entities/process.json` is `"Business Process"` (not
`"Process"`). The schema `description` references the WSF /
Process-kernel lineage. Any deviation is a hard failure.

**BP-SPEC-01-006** — The governance doc
`docs/governance/process-specialization.md` exists and references
both CR-MM-PROC-01 (kernel) and CR-AR-FMWK-01 (root-model sync).
Missing doc is a hard failure.

**BP-SPEC-01-007** — The catalog's `process_intent` enum
(`operational` / `support` / `management`) remains **catalog-internal**.
It must NOT appear as a root-model entry (`dea:entity-...`). Any
catalog entry that promotes `process_intent` to a root-model entity
is a hard failure.

The existing BP-01-001/002/003 rules are folded into
BP-SPEC-01-001..007 with the same exit codes (0/1/2) and the same
built-in self-test pattern.

### 5.5 README — reframe as a specialization catalog

The "Purpose" and "Current Status" sections of `README.md` are
updated to reflect the specialization framing:

> ## Purpose
>
> The **OpenDEA Business Process Catalog** establishes the
> canonical, structured, and machine-consumable foundation for the
> **Business Process specialization** of the OpenDEA Process
> kernel. The catalog supports the Business Architecture and
> Business Operations use cases. It is one of potentially several
> Process-specialization catalogs in the OpenDEA ecosystem; other
> specializations (Operational, Engineering, etc.) will have their
> own catalogs when their use cases emerge.

### 5.6 Governance doc — preserved and re-anchored

`docs/governance/canonical-identity-business-process.md` (CR-BP-01
artifact, byte-preserved) is renamed to
`docs/governance/process-specialization.md`. Its content is updated
to reflect the kernel + specialization structure (the validator
behaviour, the dual-id declaration, the legacy-id placement, the
WSF discipline citation, the root-model federation mapping).

The old "`dea:BusinessProcess` is canonical" framing is removed; the
new framing is "`dea:entity-process` is the root-model kernel;
`dea:entity-business-process` is the OpenDEA Business Process
specialization; the metamodel-side id `dea:Process` is the Core
kernel and `dea:BusinessProcess` is the Core specialization, aligned
1:1 with the root-model ids via the federation mapping recorded in
the governance doc".

### 5.7 CHANGELOG — supersede CR-BP-01

`CHANGELOG.md` gains a new `[Unreleased]: CR-MM-PROC-01 + CR-AR-FMWK-01 + CR-BP-SPEC-BP-01` entry that:

- acknowledges CR-BP-01's superseded premise;
- records the revert of `a34c7ff` (PR #11) and the merge of
  CR-MM-PROC-01 (PR #163) + CR-AR-FMWK-01 (PR #10);
- records the kernel + specialization structure landed by
  CR-MM-PROC-01 (metamodel), CR-AR-FMWK-01 (root model), and this
  CR (catalog-side re-anchoring);
- notes the OpenDEAM root-model version bump from v0.5.0 to v0.6.0.

## 6. Acceptance Criteria

- [ ] `dea-catalog-processes/main` does not carry the
      `a34c7ff` merge commit (revert PR #11 merged first).
- [ ] `metamodel-pointer.yaml` primary block declares
      `entity_id: dea:BusinessProcess`, `class_alias: BP`,
      `version: v0.6.0`.
- [ ] `metamodel-pointer.yaml` `entities:` list declares the
      kernel as the first entry:
      `entity_id: dea:entity-process`, `class_alias: PRC`,
      `discriminator: process-kernel`; no `layer`, no
      `dimension`.
- [ ] `schemas/entities/process.json` title is
      `"Business Process"` (was `"Process"`).
- [ ] Validator renamed and extended; `BP-SPEC-01-001..007`
      enforced; built-in self-test green.
- [ ] Existing `BP-01-001/002/003` rules folded into
      `BP-SPEC-01-001..007`.
- [ ] README reframed as Business Process specialization
      catalog (Purpose + Current Status).
- [ ] Governance doc updated and renamed
      (`canonical-identity-business-process.md` →
      `process-specialization.md`).
- [ ] CHANGELOG entry records the supersession + revert +
      kernel/specialization landing.
- [ ] No catalog entry uses bare `dea:Process` or
      `dea:entity-process` as its id (`dea:Process` /
      `dea:entity-process` are kernel-level ids; catalog entries
      carry lowercase namespaced ids).
- [ ] Sub-classifications (`operational / support / management`)
      remain catalog-internal; no schema or kernel changes
      introduce them as root-model entities.
- [ ] Consumer validator (`validate-against-model.yml@v0.6.0`)
      returns 0-drift for the new pointer.

## 7. Out of Scope
      introduce them as entities.

## 7. Out of Scope

- Other Process specializations (`dea:OperationalProcess`,
  `dea:EngineeringProcess`, etc.) — gated on concrete use cases.
- The OpenDEAM root model update — handled by CR-AR-FMWK-01.
- Workflow modeling, Activity semantics — WSF discipline applies
  unchanged.
- CR-BP-02 (Process Context register + Cell Charter schema) —
  deferred until this CR and CR-MM-PROC-01 land. The Process
  Context register's canonical entity references update to
  reflect the specialization framing (`dea:BusinessProcess`
  as the entry's `type`, not its `id`).

## 8. References

- `dea-metamodel/change-requests/CR-MM-PROC-01.md` — kernel
  introduction + specialization (this CR's dependency).
- `dea-metamodel/change-requests/CR-016.md` — Capability
  specialization precedent.
- `dea-catalog-processes/change-requests/CR-BP-01.md` —
  superseded catalog-side CR (premise reversed; artifacts
  preserved).
- `dea-catalog-processes/change-requests/CR-BP-02.md` —
  Process Context register (deferred).
- `World-Semantic-Foundation/00_inbox/WSF-Foundational-Semantic-Synthesis-baseline-insight.md`
  §6 (Capability Becomes Specialization template).
- `dea-catalog-processes/docs/governance/canonical-identity-business-process.md` —
  CR-BP-01 governance doc (renamed and updated by this CR).

## 9. Pitfalls

- The pointer schema change from flat `entity_id` to a list of
  `entities[]` requires the catalog's `validate-allocation`
  workflow update (it currently expects a single `entity_id`).
  This is in CR-AR-FMWK-01's scope; until then, the workflow
  will fail and that failure is acceptable (it is diagnostic of
  the root-model lag, not of the catalog).
- The schema title rename (`Process` → `Business Process`) may
  break downstream consumers that match on the title string;
  none are currently known, but the CHANGELOG entry calls this
  out.
- The CR-BP-01 validator rules (`BP-01-001/002/003`) and the new
  `BP-SPEC-01-001..005` rules share an exit-code space (0/1/2)
  and a self-test pattern; the migration must preserve the
  self-test behaviour.

## 10. Provenance

- Date: 2026-09-03
- Triggered by: user reframe 2026-09-03 (WSF is authoritative on
  the concept of process; DEA inherits and specializes).
- Working folder: `/home/hermes/dea-work/process/00_inbox/`.
- Supersedes: CR-BP-01's catalog-side artifacts (preserve
  byte-equivalent the governance doc, validator, CI wire,
  README/CHANGELOG scaffolds; re-anchor their canonical-id
  assertions).

## 11. Sequencing

1. Revert PR #11 (`git revert -m 1 a34c7ff`); merge. **DONE**
   (PR #11 merged; commit `417114f`; CI green on revert commit).
2. CR-MM-PROC-01 lands on `dea-metamodel`. **DONE** (PR #163
   merged; commit `1665209`).
3. CR-AR-FMWK-01 lands on `dea-architecture-framework`
   (root-model update for `dea:entity-process` (kernel; PRC) +
   `dea:entity-business-process` (specialization; BP);
   validator extension). **DONE** (PR #10 merged; commit
   `76463b2`; tag `v0.6.0`).
4. CR-BP-SPEC-BP-01 (this CR) lands on `dea-catalog-processes`.
   **CURRENT STEP**.
5. CR-BP-02 (Process Context register) follows, gated on this
   CR's merge.

Steps 2 and 3 may run in parallel; step 4 is gated on both.