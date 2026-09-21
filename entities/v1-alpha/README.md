# v1-alpha Process Catalog Entries

This directory contains the authoritative `v1-alpha` Business Process catalog entries for the TechNeHub Labs Digital Enterprise Architecture (DEA) ecosystem. 

Rather than a flat file structure, this directory implements a **containment tree** mapped directly to the **Enterprise Concept Framework (ECF) 7×7 foundation matrix**. This topology ensures that every process is explicitly contextualized by its primary architectural domain (the scope of work) and its lifecycle stage (how the work evolves), preventing taxonomy drift and enabling rigorous, tree-aware conformance testing.

---

## 🏛 Architectural Context: The ECF Matrix

The directory structure is not arbitrary; it is a physical manifestation of the ECF, an axiom-derived, lifecycle-aware matrix that describes any enterprise. 

Every process in this catalog is anchored to an **ECF Coordinate** `(Domain, Stage)`. This provides classification context without conflating it with the process's intrinsic identity. 
* **Domains (Rows)** answer: *"What kind of enterprise work is this?"*
* **Stages (Columns)** answer: *"What lifecycle phase is this process artifact representing?"*

> **Note on Process Traversal:** While a Process Context (PC) file resides in a specific directory representing its *primary* or *initiating* coordinate, the actual business process it describes may traverse multiple ECF stages (e.g., a process conceived in `sd-conceive` will eventually be operated in `sd-operate`). The directory placement denotes its canonical registration point, not its entire lifecycle.

---

## 📁 Directory Topology & Naming Conventions

Subdirectories strictly follow the `<domain-abbr>-<stage-abbr>` pattern, aligned with the **ECF Domain Enum v2.3.0** canonical set (established in `CR-BP-ECF-01`). 

### Active Domains in v1-alpha
| Prefix | ECF Domain (v2.3.0) | Architectural Scope |
| :--- | :--- | :--- |
| `ao-` | **Agency & Organization** | Internal agentive fabric, workforce coordination, capability development. |
| `eo-` | **Enablement & Operations** | Execution mechanisms, operational processes, infrastructure, and service delivery. |
| `fa-` | **Finance & Accounting** | Monetary reality, planning, allocation, transaction recording, and reporting. |
| `pv-` | **Product & Value** | Value-bearing propositions, product lifecycle, packaging, and evolution. |
| `sd-` | **Strategy & Direction** | Intentional trajectory, positioning, ambition, and resource allocation priorities. |

*(Note: Governance & Existence `ge-` and Party & Relationship `pr-` are defined in the ECF but are not yet populated in this specific v1-alpha slice).*

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
As established in the `CR-BP-mv1` migration, **Process Context files in this tree deliberately omit the `type:` field**. This is by design. The vendored, tree-aware Conformance System Test (CST) suite identifies these as PCs based on their directory placement and canonical record structure, honoring a specific PC profile that does not require explicit `type`, `version`, or `lifecycle_status` fields at the root level.

### Canonical YAML Shape
```yaml
# id pattern: processes:<domain-abbr>:<stage-abbr>:<unique-identifier>
id: processes:eo:operate:incident-response
name: Incident Response Management
process_intent: operational          # e.g., operational, support, management
process_audience: enablement-operations # Maps to v2.3.0 ECF Domain enum
description: >
  Triage, resolve, and learn from operational incidents to maintain 
  service level objectives (SLOs) and prevent recurrence.
stakeholders:
  - dea:stakeholder-sre-team
actors:
  - dea:actor-noc
  - dea:actor-incident-commander
```

---

## 🛡 Governance & Conformance Gates

This catalog is protected by a rigorous, automated CI pipeline. The upstream `dea-metaframework` CST suite was vendored and adapted here to be **layout-agnostic**, recognizing the containment tree and the unique PC profile. All PRs must pass the following gates:

1. **`check_ecf_conformance.py`**  
   *What it does:* Validates that all `process_audience` and domain references strictly match the v2.3.0 canonical ECF Domain Enums.  
   *Why it matters:* Prevents "silent inference" and taxonomy drift (e.g., rejecting legacy terms like `SupplyAndResources` in favor of `StrategyAndDirection`).
2. **`check_process_context.py`**  
   *What it does:* Validates the structural integrity of PC records, ensuring required fields are present and the `id` pattern correctly reflects the directory's ECF coordinate.  
   *Why it matters:* Guarantees that the containment tree and the internal YAML metadata remain perfectly synchronized.
3. **`check_process_semantics.py`**  
   *What it does:* Enforces business logic rules, such as valid `process_intent` classifications and proper actor/stakeholder referencing.  
   *Why it matters:* Ensures processes are not just syntactically valid, but semantically meaningful within the DEA metamodel.
4. **`check_cr_metadata.py --strict`**  
   *What it does:* Verifies that any structural change, new process admission, or domain migration is explicitly tied to an approved Change Request (CR) markdown file in the repository root.  
   *Why it matters:* Enforces the "no undocumented mutations" rule. Every change must have an auditable governance trail (e.g., `CR-BP-17`, `CR-BP-ECF-01`).

---

## 🔄 Lifecycle, Reconciliation, and Baselines

This directory does not exist in isolation. It is the source of truth for the repository's reconciliation artifacts:
* **`CATALOG.yaml`**: Automatically refreshed to reflect the current state of all entities in this tree.
* **`reconciliation/inventory.yaml` & `reconciliation/baseline/v1.yaml`**: Generated to provide a byte-identical, round-trip verifiable snapshot of the catalog. 

When modifying this directory, contributors must run the reconciliation build scripts to ensure the baseline remains consistent with the committed tree.

---

## 🚀 Contributor Workflow

To add or modify a process in this catalog:

1. **Identify the Coordinate:** Determine the primary ECF Domain and Stage for the process.
2. **File a Change Request (CR):** Create or reference an existing CR (e.g., `CR-BP-NN-<title>.md`) detailing the rationale, impact, and metamodel alignment of the change.
3. **Create/Update the YAML:** Place the file in the correct `<domain>-<stage>` directory. Ensure the `id` matches the directory context. *Do not add a `type:` field.*
4. **Run Local Conformance:** Execute the local CST suite (`pytest tests/conformance/ --strict`) to verify all gates pass.
5. **Regenerate Baselines:** Run the reconciliation tools to update `CATALOG.yaml` and baseline artifacts.
6. **Submit PR:** Link the PR to the CR. The CI pipeline will enforce the gates described above.

---
*For deeper metamodel definitions, refer to `../../schemas/process-context.schema.json` and the OpenDEA Glossary in `technehub-labs/dea-metamodel`.*
