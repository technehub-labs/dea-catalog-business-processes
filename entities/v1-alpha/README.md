# v1-alpha Process Catalog Entries

This directory contains the actively maintained `v1-alpha` Business Process catalog entries. The catalog is structured as a containment tree that maps directly to the **Enterprise Concept Framework (ECF) 7x7 foundation matrix**, classifying processes by their primary Domain (what the enterprise does) and Stage (how the work evolves).

## 📁 Directory Structure (`<domain>-<stage>`)

The subdirectories follow a strict naming convention representing the intersection of an ECF Domain and an ECF Stage.

### ECF Domains (Rows)
The prefix denotes the ECF Domain:
*   `ao-`: **A**gency & **O**rganization (Internal agentive fabric, workforce coordination)
*   `eo-`: **E**nablement & **O**perations (Execution mechanisms, operational processes)
*   `fa-`: **F**inance & **A**ccounting (Monetary reality, planning, reporting)
*   `pv-`: **P**roduct & **V**alue (Value-bearing propositions, product lifecycle)
*   `sd-`: **S**trategy & **D**irection (Intentional trajectory, positioning, ambition)

*(Note: The ECF defines 7 domains. Governance & Existence (`ge`) and Party & Relationship (`pr`) are currently unpopulated in this v1-alpha slice).*

### ECF Stages (Columns)
The suffix denotes the lifecycle Stage:
1.  `conceive`: Naming the need or policy
2.  `design`: Specifying the object or controls
3.  `build`: Constructing, provisioning, or acquiring
4.  `activate`: Deploying, cutting over, launching
5.  `operate`: Running, serving, and maintaining
6.  `improve`: Measuring, learning, and optimizing
7.  `retire`: Sunsetting, migrating, or renewing

## 📄 Entity Contents (Process Contexts)

Each directory contains YAML files representing **Process Contexts (PCs)** or concrete Business Process entities. These files serve as the authoritative record for processes traversing that specific ECF coordinate.

### Schema Conformance
Every entry must conform to the canonical DEA metamodel schemas:
*   `../../schemas/entity.schema.json` (Core entity definition)
*   `../../schemas/process-context.schema.json` (Process-specific extensions)

### Example Entry
```yaml
id: processes:eo:operate:incident-response
type: Process
name: Incident Response
process_intent: operational
process_audience: enablement-operations
description: Triage, resolve, and learn from operational incidents.
version: 1.0.0
stakeholders:
  - dea:stakeholder-sre-team
actors:
  - dea:actor-noc
```

## 🛠 Contribution & Conformance Gates

The catalog is governed by a suite of Conformance System Tests (CST) that run in CI. Before opening a Pull Request, ensure your entries pass the following local gates:

1.  **Layout & Identity**: Process Contexts are correctly placed in the containment tree and carry valid `id` fields.
2.  **ECF Conformance** (`check_ecf_conformance.py`): Validates that domains and stages correctly map to the v2.3.0 ECF Domain Enums.
3.  **Process Semantics** (`check_process_semantics.py`): Validates intent, audience, and taxonomy alignment.
4.  **Change Requests** (`check_cr_metadata.py`): Ensures any new admission or migration is backed by an approved Change Request (CR) file.

## 🔄 Recent Migrations
*   **ECF Domain Enum v2.3.0 (`CR-BP-ECF-01`)**: Domains were updated to the canonical v2.3.0 set (e.g., `CustomerAndDemand` → `PartyAndRelationship`; `SupplyAndResources` → `StrategyAndDirection`).
*   **Entity Storage & ID Migration (`CR-BP-mv1`)**: All Process Contexts were moved into this containment tree structure, migrating away from flat layouts.
```

---

### 💡 Why These Improvements Make It Robust

1.  **Decodes the Naming Convention**: The most confusing part of the current directory tree is the prefixes (`ao`, `eo`, `fa`, etc.). By explaining that these are initials for the **ECF Domains** (Agency & Organization, Enablement & Operations, etc.), you turn cryptic folder names into a logical, navigable matrix.
2.  **Reflects Actual Activity**: It removes the outdated "Phase 2 will begin" language and acknowledges the massive recent migrations (`CR-BP-mv1` and `CR-BP-ECF-01`) found in your commit history.
3.  **Actionable Contribution Guidelines**: Instead of just pointing to a schema, it lists the specific **CI scripts** (`check_ecf_conformance.py`, `check_cr_metadata.py`) that developers must satisfy. This reduces the "back-and-forth" on PR reviews by setting expectations upfront.
4.  **Matrix Context**: It explicitly links the file structure to the **ECF 7x7 matrix**, helping enterprise architects and developers understand *why* a process is located in `sd-conceive` versus `sd-build`.

### 🚀 Suggested Next Step for Maintainers
To keep this robust long-term, consider adding a script that automatically generates a `CATALOG.yaml` or a "Table of Contents" at the bottom of the README, summarizing the total number of process entities currently registered in each `<domain>-<stage>` bucket.

### USER
enrich it further, including more depth and less simple references that lack added context

### ASSISTANT
Here is a significantly enriched, deeply contextualized version of the README. It moves beyond surface-level descriptions to explain the *architectural rationale*, *metamodel distinctions*, and *governance mechanics* that govern this directory, ensuring contributors and consumers understand not just *what* is here, but *why* it is structured this way.

---

### 📝 Enriched README: `entities/v1-alpha`

```markdown
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

See [DEA Metamodel process schema](https://github.com/technehub-labs/dea-metamodel/blob/main/schemas/entities/process.json) and [process-type-taxonomy.md](https://github.com/technehub-labs/dea-metamodel/blob/main/docs/process-type-taxonomy.md) for full canonical definitions and worked examples.labs/dea-metamodel`.*
