# v1-alpha Process Catalog Entries

This directory contains the authoritative `v1-alpha` Business Process catalog entries for the TechNeHub Labs Digital Enterprise Architecture (DEA) ecosystem.

Rather than a flat file structure, this directory implements a **containment tree** mapped directly to the **Enterprise Concept Framework (ECF) 7×7 foundation matrix**. This topology ensures that every process is explicitly contextualized by its primary architectural domain (the scope of work) and its lifecycle stage (how the work evolves), preventing taxonomy drift and enabling rigorous, tree-aware conformance testing.

This README is the structural template for the entities-root README of every catalog repository in the org-wide id-system rollout (`technehub-labs/dea-catalog-*`). When the ECF domain enum, the id-system spec, or the conformance gate set changes, this document is the canonical reference; sibling catalogs are expected to mirror it.

---

## 🏛 Architectural Context: The ECF Matrix

The directory structure is not arbitrary; it is a physical manifestation of the ECF, an axiom-derived, lifecycle-aware matrix that describes any enterprise.

Every process in this catalog is anchored to an **ECF Coordinate** `(Domain, Stage)`. This provides classification context without conflating it with the process's intrinsic identity.

* **Domains (Rows)** answer: *"What kind of enterprise work is this?"*
* **Stages (Columns)** answer: *"What lifecycle phase is this process artifact representing?"*

> **Note on Process Traversal:** While a Process Context (PC) file resides in a specific directory representing its *primary* or *initiating* coordinate, the actual business process it describes may traverse multiple ECF stages (e.g., a process conceived in `sd-conceive` will eventually be operated in `sd-operate`). The directory placement denotes its canonical registration point, not its entire lifecycle.

---

## 📁 Directory Topology & Naming Conventions

Subdirectories strictly follow the `<domain-abbr>-<stage-abbr>` pattern, aligned with the current **ECF Domain Enum** (ratified through the standing ECF migrations; see `change-requests/` for the most recent). Each directory is a **cell** in the 49-coordinate foundation matrix.

### Active Domains in v1-alpha (all 7 of the ECF 7×7)
| Prefix | ECF Domain | Architectural Scope |
| :--- | :--- | :--- |
| `ao-` | **Agency & Organization** | Internal agentive fabric, workforce coordination, capability development. |
| `eo-` | **Enablement & Operations** | Execution mechanisms, operational processes, infrastructure, and service delivery. |
| `fa-` | **Finance & Accounting** | Monetary reality, planning, allocation, transaction recording, and reporting. |
| `ge-` | **Governance & Existence** | The enterprise's mandate, policy posture, charter direction, and existential definition (boards, charters, codified policies, risk and control apparatus). |
| `pr-` | **Party & Relationship** | The enterprise's exchange with external parties (customers, suppliers, partners), including channels, acquisition, and demand generation. |
| `pv-` | **Product & Value** | Value-bearing propositions, product lifecycle, packaging, and evolution. |
| `sd-` | **Strategy & Direction** | Intentional trajectory, positioning, ambition, and resource allocation priorities. |

All 49 cells (7 domains × 7 stages) are populated at every level of the tree. See [Population snapshot](#-population-snapshot) for the per-domain inventory.

### Lifecycle Stages
| Suffix | Stage | Semantic Meaning for Processes |
| :--- | :--- | :--- |
| `-conceive` | Conceive | Naming the need, policy intent, or strategic opportunity. |
| `-design` | Design | Specifying the process controls, workflows, and boundaries. |
| `-build` | Build | Constructing, provisioning, or acquiring the process capability. |
| `-activate` | Activate | Cut-over, launch, and mobilization into service. |
| `-operate` | Operate | Running, serving, monitoring, and maintaining (steady state). |
| `-improve` | Improve | Measuring performance, learning from incidents, optimizing. |
| `-retire` | Retire | Sunsetting, migrating, or decommissioning the process. |

---

## 📄 Entity Anatomy: Process Contexts (PCs)

Files within these directories represent **Process Contexts (PCs)**. Per the DEA Metamodel, `dea:Process` is an abstract kernel; concrete instances are specialized (e.g., `dea:BusinessProcess`).

### Critical Metamodel Distinction
As established in the `CR-BP-mv1` migration (Wave 1, PR #149), **Process Context files in this tree deliberately omit the `type:` field**. This is by design. The upstream, layout-agnostic Conformance System Test (CST) suite (now at `dea-metaframework/tools/conformance_test_catalog_structure.py`, ports of which are vendored under `scripts/`) identifies PCs based on their directory placement and canonical record structure, honoring a specific PC profile that does not require explicit `type`, `version`, or `lifecycle_status` fields at the root level.

### Canonical YAML Shape

```yaml
# PC id pattern: processes:pc-<domain-abbr>-<stage-abbr>-<hash6>
# Hash is content-addressed over a 31-symbol alphabet (a-z minus i/l/o + 2-9),
# derived from the record file's SHA-256[:4]. See docs/id-system.md in
# dea-metaframework for the full contract.
id: processes:pc-eo-operate-7ab3ma
name: Incident Response Management
domain: EnablementAndOperations     # canonical ECF domain (v2.4.x)
lifecycle_stage: Operate            # canonical ECF stage
process_intent: operational         # e.g., operational, support, management
process_audience: enablement-operations  # derived from ECF coordinate
description: >
  Triage, resolve, and learn from operational incidents to maintain
  service level objectives (SLOs) and prevent recurrence.
stakeholders:
  - stakeholders:stakeholder-sre-team-xxxxxx   # org-wide id form
actors:
  - actors:actor-noc-xxxxxx
  - actors:actor-incident-commander-xxxxxx
links:
  - rel: change-request
    href: change-requests/CR-BP-13a-customer-and-demand-admission.md
```

IDs across the four levels of the tree follow the patterns:

| Level | id form |
| :--- | :--- |
| L1: Process Context (PC) | `processes:pc-<domain>-<stage>-<hash6>` |
| L2: Process Group | `processes:group-<domain>-<stage>-<hash6>` |
| L3: Process | `processes:process-<domain>-<stage>-<hash6>` |
| L4: Activity / Task | `processes:activity-...-<hash6>`, `processes:task-...-<hash6>` |

Every record file is uniquely identified by a 6-character content-derived hash; renaming a record file's contents (without renaming the file) would change its hash. This is what makes the tree content-addressed rather than directory-addressed.

### Containment Tree

Within each `<domain>-<stage>` cell, the structure is a strict four-level containment tree (PC → Group → Process → Activity → Task):

```
<domain>-<stage>/                                # cell root (L1 PC + L2 Group live here)
├── processes-pc-<dom>-<stage>-<hash6>.yaml                  # L1, exactly one per cell
├── <dom>-<stage>-<hash6>/                                  # L2 Group subtree
│   ├── processes-group-<dom>-<stage>-<hash6>.yaml          # L2 group record
│   ├── <dom>-<stage>-<hash6>/                              # L3 Process subtree
│   │   ├── processes-process-<dom>-<stage>-<hash6>.yaml
│   │   ├── <dom>-<stage>-<hash6>/                          # L4 Activity subtree
│   │   │   ├── processes-activity-<dom>-<stage>-<hash6>.yaml
│   │   │   └── <dom>-<stage>-<task-name>-<hash6>/          # Task records (5 standard verbs)
│   │   │       └── processes-task-<dom>-<stage>-<task>-<hash6>.yaml
│   │   ├── candidates/                                     # candidate L3s awaiting admission
│   │   ├── retired/                                        # retired L4s
│   │   └── research/                                       # L3 candidate-universe registers
│   └── research/
└── README.md                                                # cell charter (optional)
```

Per-cell counts follow the standard 1-1-N-N×5 progression: 1 PC, 1 Group, N Processes (typically 1 to 5 per cell), each with 5 standard task verbs (intake / record / transform / confirm / verify).

---

## 📈 Population Snapshot

Per-domain inventory at the time of last regeneration. Counts are read from `CATALOG.yaml` and the entity tree; see `reconciliation/inventory.yaml` for the machine-readable form.

| Domain | L1 (PC) | L2 (Group) | L3 (Process) | L4 (Activity) | L4 (Task) |
| :--- | ---: | ---: | ---: | ---: | ---: |
| `ao` Agency & Organization        | 7 | 7 | 20 | 80  | 400 |
| `eo` Enablement & Operations      | 7 | 7 | 30 | 121 | 605 |
| `fa` Finance & Accounting         | 7 | 7 | 22 | 88  | 440 |
| `ge` Governance & Existence       | 7 | 7 | 18 | 68  | 340 |
| `pr` Party & Relationship         | 7 | 7 | 11 | 44  | 220 |
| `pv` Product & Value              | 7 | 7 | 18 | 72  | 360 |
| `sd` Strategy & Direction         | 7 | 7 | 21 | 87  | 435 |
| **Total**                         | **49** | **49** | **140** | **560** | **2800** |

The asymmetry in process counts per domain (e.g., `eo` 30 vs `pr` 11) reflects the natural scope of each ECF domain, not incomplete population. Every cell is fully populated at every layer.

---

## 🛡 Governance & Conformance Gates

This catalog is protected by an automated CI pipeline with the following gates. All gates run on every PR via `.github/workflows/catalog-conformance.yml` (and adjacent workflows):

1. **`validate-entries`** (CI job)
   Validates every record file against `schemas/entity.schema.json` and the cell-charter contract.
   *Why it matters:* Catches malformed records and structural drift before they reach the catalog.

2. **ECF Conformance Consumer** (`scripts/check_ecf_conformance.py`, vendored from `dea-metaframework`)
   Validates that `domain`, `process_audience`, and ECF coordinate references match the canonical ECF Domain Enum ratified through `CR-BP-ECF-08` and `CR-BP-ECF-09` (current enum: v2.4.x).
   *Why it matters:* Prevents "silent inference" and taxonomy drift (e.g., rejects legacy `SupplyAndResources` in favor of `StrategyAndDirection`; rejects legacy `CustomerAndDemand` in favor of `PartyAndRelationship`).

3. **Catalog Conformance Suite** (CST, layout-agnostic, from `dea-metaframework/tools/conformance_test_catalog_structure.py`)
   Runs the 16-test CST suite that checks id-pattern conformance, content-derived hash correctness, containment-tree invariants, and the PC profile.
   *Why it matters:* Enforces the org-wide id-system contract across all 7 catalog repositories.

4. **ID System Gate** (`scripts/check_id_system.py`)
   Runs IDM-001..007 (catalog-wide) plus IDM-008 (PR-scoped coherence via `id-system-coherence-report.md` artifact).
   *Why it matters:* Catches id drift between branches and the canonical baseline before merge.

5. **Register Audit Gate** (`scripts/check_register_audit.py`)
   Walks the 49-cell L1 register and confirms every cell's `audit_status: landed` vs `pending`.
   *Why it matters:* Keeps the L1 register honest as a single source of truth.

6. **CR Metadata Gate** (`scripts/check_cr_metadata.py --strict`)
   Verifies that any structural change, new process admission, or domain migration is explicitly tied to an approved Change Request (CR) markdown file in `change-requests/`.
   *Why it matters:* Enforces the "no undocumented mutations" rule. Every change must have an auditable governance trail.

7. **`allocate / validate`** (CI job)
   Generates a per-cell allocation matrix and validates it against the L1 register.
   *Why it matters:* Detects orphan or duplicated records that escape the schema-level checks.

---

## 🔄 Lifecycle, Reconciliation, and Baselines

This directory is the source of truth for the repository's reconciliation artifacts under `reconciliation/`:

* **`CATALOG.yaml`** (repo root): Automatically refreshed to reflect the current state of all entities in this tree. The CI gate runs `scripts/regenerate_catalog.py --check` and fails on any drift.
* **`reconciliation/inventory.yaml`**: Flat inventory of every entity, indexed by id.
* **`reconciliation/baseline/v1.yaml`**: Byte-identical, round-trip verifiable snapshot of the catalog at the last accepted baseline.
* **`reconciliation/conformance_report.yaml`**: Last CST run output (16 CSTs, 0 warnings at HEAD).
* **`reconciliation/cr-bp-99-matrix.yaml`**: The 49-cell L1 register (CR-BP-99 ratification reference).
* **`reconciliation/cross-check-org-wide.md`**: Cross-check report for the most recent structural CR.
* **`reconciliation/migration-id-map.yaml`**: Id map from the `CR-BP-mv1` Wave 1 migration (legacy `dea:process-*` to `processes:process-...-hash`).
* **`reconciliation/tranches/`**, **`reconciliation/diffs/`**, **`reconciliation/dispositions/`**: Per-tranche evidence packs.

When modifying this directory, contributors must run the reconciliation build scripts to ensure the baseline remains consistent with the committed tree. CI enforces this.

---

## 🔗 Cross-Repo References

This catalog is one of seven in the DEA ecosystem. Records reference other catalogs using the org-wide id form `<namespace>:<level>-...-<hash6>`:

| Namespace | Catalog | Status |
| --- | --- | --- |
| `actors:` | `technehub-labs/dea-catalog-actors` | Wave 3 scaffold (empty, ready for first admissions) |
| `orgunits:` | `technehub-labs/dea-catalog-organizational-units` | Wave 3 scaffold |
| `objects:` | `technehub-labs/dea-catalog-business-objects` | Wave 3 scaffold |
| `stakeholders:` | `technehub-labs/dea-catalog-stakeholders` | Wave 3 scaffold |
| `capabilities:` | `technehub-labs/dea-catalog-business-capabilities` | Populated (31 records, Wave 2) |
| `services:` | `technehub-labs/dea-catalog-business-services` | Populated (18 records, Wave 2b) |
| `processes:` | `technehub-labs/dea-catalog-business-processes` | This catalog (3,598 records) |

The `processes:` namespace has its own secondary references to the `dea:catalog-*` identity records (the catalog's own self-identity), which remain in the legacy form on purpose.

---

## 🚀 Contributor Workflow

To add or modify a process in this catalog:

1. **Identify the Coordinate.** Determine the primary Domain × Stage for the process. Confirm the cell is in the L1 ratification (CR-BP-99 register); if not, file a CR first.
2. **File a Change Request (CR).** Create or reference an existing CR in `change-requests/` (e.g., `CR-BP-NN-<title>.md`) detailing the rationale, impact, and metamodel alignment.
3. **Create/Update the YAML.** Place the file at the correct level in the containment tree. Compute the content-derived hash for the id. *Do not add a `type:` field on PC records.* Use the org-wide id form for cross-repo references.
4. **Run Local Conformance.** Execute `scripts/check_id_system.py --strict` and the CST suite locally (see `docs/conformance.md` in dea-metaframework). The CI pipeline runs the same gates on every PR.
5. **Regenerate Reconciliation Artifacts.** Run `scripts/regenerate_catalog.py --check --schema catalog-index-schema/catalog-index-schema.json` and the reconciliation build scripts. CI will fail if `CATALOG.yaml` is stale.
6. **Submit PR.** Link the PR to the CR. The CI pipeline enforces the gates described above.

For deeper metamodel definitions and the canonical id-system / entity-storage-layout specs, refer to:

* `technehub-labs/dea-metaframework` → `docs/id-system.md` (org-wide id contract)
* `technehub-labs/dea-metaframework` → `docs/entity-storage-layout.md` (ECF-coordinated tree layout)
* `technehub-labs/dea-metaframework` → `docs/conformance.md` (CST suite reference)
* `schemas/entity.schema.json` (record schema)
* `schemas/identity.schema.json` (identity schema)
* `schemas/contribution.schema.json` (contribution schema)
* The OpenDEA Glossary in `technehub-labs/dea-metamodel`.