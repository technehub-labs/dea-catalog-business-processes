# Normative Design Proposal

> **Stage 1 output 3 of CR-BP-121 (renumbered from CR-BP-16).**
> The 5 normative decisions for the General Entity System in `dea-catalog-processes`: identity, contract, relationships, lifecycle, conformance.
> Foundation: [00-charter.md](00-charter.md), [01-existing-decisions-and-gap-register.md](01-existing-decisions-and-gap-register.md).

This proposal codifies the 9 N-classification decisions from the Gap Register into normative specifications. Each section states the rule, the rationale, the alternatives considered, and the disposition.

## 1. Entity Identity Standard (resolves G-01)

### 1.1 The rule

> Every governed entity in `dea-catalog-processes` SHALL possess a persistent identifier that distinguishes it from other entities within its declared identity scope. The canonical identifier format is `processes:<token>-<descriptor>-<base32hash>` (per CR-BP-mv1, IDM-001..008). The `dea:` family is reserved for legacy migration references (per CR-BP-04) and for the metamodel's entity-type definitions (per EGV-001).

### 1.2 The rationale

- Persistent: an id identifies the entity, not its name, position, classification, or release (per DEA-ID-000 §5; CR-012 EGV-002).
- Canonical: the four id families (`dea:process-*`, `dea:pc-*`, `dea:group-*`, `dea:scope-*`) and the post-mv1 `processes:` family are the only approved forms; the `dea:bp:*` legacy family is a migration reference, not a live format.
- Scope-bound: identity is per-catalog (this catalog), not portfolio-wide; cross-catalog references use canonical URIs (see §3 Relationship Standard).
- BASE32 strict alphabet: `abcdefghjkmnpqrstuvwxyz23456789` (no `i`, `l`, `o`, `0`, `1`) - prevents OCR / transcription ambiguity.
- 6-character hash suffix: content-addressed entropy; assigned at canonicalization; never recomputed live.
- The `dea:` family is the metamodel's identifier space (per EGV-001); the `processes:` family is the catalog's identifier space.

### 1.3 Alternatives considered

- **A1. Globally unique UUIDs**: rejected. UUIDs are not human-readable; they don't carry semantic content; they make cross-catalog references harder to audit.
- **A2. URL-based URIs (e.g. `https://dea.technehub-labs.org/processes/...`)**: rejected for v1. The catalog's identity scope is the catalog itself; URLs imply a network resolution mechanism that doesn't exist. URIs are reserved for cross-catalog references (§3).
- **A3. Adopt the metamodel's `dea:` family for catalog records**: rejected. The metamodel owns entity-type definitions; the catalog owns entity instances. The two spaces must be distinct (per EGV-005 / the kernel + specialisation discipline).
- **A4. Hash-only (no semantic content)**: rejected. The 6-character hash is for collision prevention, not for human navigation. The semantic segment (`<token>-<descriptor>`) is what makes ids human-readable.

### 1.4 Disposition

- **Normative**: the `processes:<token>-<descriptor>-<base32hash>` format is the canonical identity.
- **Legacy**: the 35 `dea:` ids in `entities/v1-alpha/` are grandfathered historical record; new records MUST use the `processes:` family.
- **Migration**: no bulk renames (per EGV-012). The 35 legacy tails are documented in `reconciliation/migration-id-map.yaml` (Stage 5 output).
- **Verification**: `scripts/check_id_system.py` (IDM-001..008) is the enforcement gate. New: `scripts/check_entity_system.py` adds an umbrella check that the id is present, format-valid, scope-bound, and unique (EGV-002 + EGV-003).

## 2. Entity Contract Standard (resolves G-02)

### 2.1 The rule

> Every governed entity in `dea-catalog-processes` SHALL conform to a common entity envelope. The envelope specifies the universal fields (id, type, name, definition, description) and the type-specific profiles (Process, ProcessContext, ProcessGroup, Activity, Task, ProcessScope) that extend the envelope with type-specific required and optional fields.

The common envelope (per DEA-ID-000 §4, CR-012 EGV-005):

```yaml
id: <persistent-entity-identifier>     # required, universal
type: <canonical-entity-type>           # required, universal
name: <preferred-human-readable-name>   # required, universal
definition: <normative-meaning>         # required, universal
description: <optional-explanatory>     # optional, universal

relationships: []                       # optional, universal; typed references
classifications: []                     # optional, universal; ECF coordinates + process_type + process_intent
provenance: {}                          # required, universal; CR linkage, change history, audit

lifecycle:                              # required, universal
  status: <governed-lifecycle-state>
  admitted_at: <iso-8601>
  admitted_by: <cr-id>
  deprecated_at: <iso-8601>             # optional
  retired_at: <iso-8601>                # optional
```

### 2.2 The rationale

- Universal: every entity has the same shape at the top level; type-specific extension is below the envelope, not beside it.
- Common invariants live in the envelope; type-specific rules live in profiles.
- The envelope is the conformance check target: `scripts/check_entity_system.py` walks the envelope fields and asserts presence + format.
- The type-specific profiles are the existing per-record-type schemas (PG, BP, Activity, Task) - they remain; the envelope sits ABOVE them.

### 2.3 Alternatives considered

- **A1. No envelope; per-type schemas only**: rejected. Per-type schemas are inconsistent across types; an envelope provides the universal conformance check.
- **A2. Strict envelope (no type-specific extension)**: rejected. The catalog has 6 distinct entity types with different requirements; strict envelope would lose fidelity.
- **A3. Envelope = the schema**: rejected. The envelope is a contract, not a schema. The schema is the implementation; the envelope is the governance.

### 2.4 Disposition

- **Normative**: the envelope is the universal contract.
- **Implementation**: the existing per-type schemas (PG, BP, Activity, Task, ProcessContext, ProcessScope) are the type-specific profiles that extend the envelope. No schema rewrites required.
- **Verification**: `scripts/check_entity_system.py` (Stage 3-4) walks the envelope fields and asserts presence + format for every record. The 5 entity types (Process, ProcessContext, ProcessGroup, Activity, Task) have different `required:` lists; the gate asserts the universal fields are present, the type-specific required fields are present (delegated to the existing per-type gates), and the optional fields conform when present.

## 3. Relationship Standard (resolves G-03 + G-06)

### 3.1 The rule

> Every relationship between governed entities SHALL conform to the metamodel's relationship-type definitions. The canonical relationship types in this catalog are:
>
> - `composes` (L1 ProcessGroup --composes--> L2 Process; L0 ProcessContext --composes--> L1 ProcessGroup)
> - `realizes` (L2 Process --realizes--> BusinessCapability, in `dea-catalog-business-capabilities`)
> - `specializes` (L2 Process --specializes--> L2 Process, per the kernel + specialisation discipline)
> - `part-of` (the derived inverse of `composes`; view-time only, not in the metamodel relationship-type enum)
>
> Every cross-catalog reference SHALL resolve to a valid entity within the target catalog's identity scope. The reference SHALL carry the target's identity-scope declaration (e.g. `scope: dea-catalog-business-capabilities`).

### 3.2 The rationale

- Typed relationships: the metamodel defines the abstract relationship types; the catalog instantiates them.
- Source / target type constraints: `composes` only goes from L1 / L0 to L2 / L1; `realizes` only goes from L2 to BC; `specializes` only goes from L2 to L2.
- Cardinality: MECE-001 (every BP is composed by at least one PG), MECE-006 (every BP has a PG), MECE-008 (deprecated BPs are exempt). Cardinality rules are documented per relationship type.
- Cross-catalog: the target catalog's id scope is declared in the relationship; resolution is by `(scope, target_id)`. The metamodel-pointer.yaml is the catalog-level declaration; per-record resolution is the rule.

### 3.3 Alternatives considered

- **A1. Free-form `relationships: []` (no type constraint)**: rejected. The current implementation has typed relationships (`relationship_type: composes`); codifying the type is the norm.
- **A2. URL-based cross-catalog references**: deferred. URLs are the future; today's references use the target id + scope. URLs are introduced in a follow-on CR if the resolution mechanism is built.
- **A3. Implicit relationships (inferred from filename)**: rejected (per DEA-ID-000 §4 "Structural relationships shall not be inferred solely from filenames, directory paths, naming conventions, or identifier segments when the same information can be represented as governed semantic data").

### 3.4 Disposition

- **Normative**: the 4 relationship types (`composes`, `realizes`, `specializes`, `part-of`) are the only approved forms.
- **Verification**: BP-SEM-001..014 (process semantics), BP-SPEC-01-001..007 (process specialisation), MECE-001..008 (composition) are the existing gates; the umbrella check is the new `scripts/check_entity_system.py` that asserts every relationship entry has a valid `relationship_type` and a resolvable target.
- **Cross-catalog resolution**: T8 of the umbrella programme (legacy reconciliation); the resolution mechanism is the `reconciliation/cross-catalog-resolution.yaml` registry (Stage 5 output).

## 4. Lifecycle Standard (resolves G-04 + G-07)

### 4.1 The rule

> The entity lifecycle state machine is:
>
> ```
>            admitted
>              |
>              v
>   proposed ---> admitted ---> deprecated ---> retired
>                  |               |
>                  +-> superseded (terminal; no resurrection)
> ```
>
> - `proposed`: the entity is documented but not yet admitted to the catalog. The contribution workflow (`contributions/processes/`) creates proposed records.
> - `admitted`: the entity is canonical. The record is in `entities/v1-alpha/`, satisfies the gate roster, and is referenced from other records.
> - `deprecated`: the entity is no longer the recommended choice; superseded by a successor. The record remains in the catalog; new records should reference the successor.
> - `retired`: the entity is removed from active use. The record remains in the catalog for historical traceability; the gate roster continues to validate it.
> - `superseded`: terminal state; the entity has been replaced. No resurrection; the successor carries the identity forward (per EGV-004).

### 4.2 The rationale

- Explicit transitions: every transition is an approved CR (the CR IS the transition record).
- Identity continuity: a renamed / reclassified entity stays in the same identity (per EGV-004); the `change_history` block records the change.
- Provenance: every transition carries `admitted_at` + `admitted_by` (CR id) + the `change_history` block (per EGV-008).
- The state machine is conservative: no skipping states; no resurrection from `superseded` or `retired`.

### 4.3 Alternatives considered

- **A1. No state machine (any field set is valid)**: rejected. Without explicit states, the gate cannot distinguish proposed / admitted / deprecated / retired.
- **A2. `deleted` state (removal from catalog)**: rejected. The catalog's records are append-only; the `retired` state is the terminal form. Removal is not in the lifecycle.
- **A3. Resurrection from `superseded`**: rejected (per EGV-004). The successor carries the identity forward; the superseded record is terminal.

### 4.4 Disposition

- **Normative**: the 5-state machine (`proposed / admitted / deprecated / retired / superseded`) is the lifecycle.
- **Verification**: the existing admission gate (ADM-001..008) + LCM-001..005 (lifecycle state-machine) are the existing gates; the umbrella check is the new `scripts/check_entity_system.py` that asserts the lifecycle block is present, the state is one of the 5, and the transitions are valid.
- **Identity continuity**: the `change_history` block (per CR-BP-31) carries the per-transition record; the umbrella gate asserts every change_history entry has the `change:` key (per CR-BP-113 provenance).

## 5. Conformance Standard (resolves G-05 + U-04 + U-05)

### 5.1 The rule

> The entity-system gate is `scripts/check_entity_system.py`. It runs as gate [N+1] in the conformance rollup (after the existing 30+ gates; the rollup position is the next free number when CR-BP-122 lands). The gate has 5 rules (one per concern):
>
> - **ES-001 (Identity)**: every record has a present, format-valid, scope-bound, unique id.
> - **ES-002 (Contract)**: every record satisfies the common envelope (universal fields present).
> - **ES-003 (Relationship)**: every `relationships[]` entry has a valid `relationship_type` and a resolvable target.
> - **ES-004 (Lifecycle)**: every record has a present, valid lifecycle block; the state is one of the 5; the transitions are valid.
> - **ES-005 (Conformance umbrella)**: the record's per-type gate (PG-001..PG-008, BP-SEM-001..014, etc.) is also CONFORMANT; the entity-system gate is the umbrella over the per-type gates.
>
> The gate is **advisory** under default mode; **blocking** under `--strict`. The first 3 stages of CR-BP-121 (Stage 1 + 2 + 3) ship the gate as advisory; Stage 4 (T4 of umbrella programme) promotes to blocking under `--strict`. The user's DP-7 is to defer the gate to Stage 3 (CR-BP-121); the staging here is consistent with that decision.

### 5.2 The rationale

- 5 rules, one per concern (identity / contract / relationships / lifecycle / conformance-umbrella).
- Advisory-then-blocking: the gate is conservative at first (advisory) so the catalog can adopt it; once stable, the gate promotes to blocking under --strict.
- Rollup integration: the entity-system gate is a single rollup row (gate [N+1]), not 5 separate rows; the umbrella semantics are inside the gate.
- Per-type gate delegation: ES-005 delegates to the existing per-type gates; it does not duplicate their work.

### 5.3 Alternatives considered

- **A1. Ship the entity-system gate as 5 separate gates (one per rule)**: rejected. The 5 rules are one concern, not 5; one rollup row is the natural fit. The internal separation is in the gate code, not the rollup.
- **A2. Ship the entity-system gate as blocking from day one**: rejected. The catalog has 3,882 records; the gate should be advisory first so the catalog can identify any false positives (via the live-catalog audit in Stage 3-4) before blocking.
- **A3. Skip the umbrella gate; rely on the existing per-type gates**: rejected. The existing gates are component-level; the umbrella gate is what makes the General Entity System a single conformance discipline.

### 5.4 Disposition

- **Normative**: the 5-rule umbrella gate is the conformance mechanism.
- **Implementation**: `scripts/check_entity_system.py` (Stage 3-4 output), `reconciliation/entity-system-registry.yaml` (the registry of identity-bearing fields), `tests/test_check_entity_system.py` (30+ tests).
- **Rollup**: gate [N+1] in `scripts/conformance_result.py` (the position is the next free number; the umbrella programme tracks it).
- **CI**: `.github/workflows/ci.yml` runs the gate under --strict after the existing 30+ gates.

## 6. Cross-cutting: the exception mechanism (resolves U-06)

### 6.1 The rule

> The exception mechanism under EGV-011 is the "review-retained" verdict in `reconciliation/normalization.yaml` (per CR-BP-25's precedent). An exception is granted by:
>
> 1. The carrier CR explicitly requests the exception, citing the EGV-011 reason.
> 2. The user (eaojnr) approves the exception as a one-line comment on the CR.
> 3. The exception is recorded in `reconciliation/normalization.yaml` with: `verdict: review-retained`; `cr: <carrier-cr-id>`; `reviewed_by: eaojnr`; `expiry: <iso-8601>` (exceptions are time-bounded; renewal requires a new CR).
> 4. The exception registry is consulted by the entity-system gate; a record carrying an exception is not blocking.
>
> Exceptions are NOT silent. They are: explicit, time-bounded, CR-linked, owner-signed, and auditable.

### 6.2 The rationale

- Explicit: no silent bypass (per EGV-011).
- Time-bounded: exceptions expire; renewal requires a new CR.
- CR-linked: the exception's provenance is the carrier CR.
- Owner-signed: the user (eaojnr) is the only approver.
- Auditable: the exception registry is a documented file in the repo.

### 6.3 Alternatives considered

- **A1. Inline annotation on the record (e.g. `exception: yes`)**: rejected. Inline annotations are not auditable; the exception would live on the record with no central registry.
- **A2. Waiver process (one-time, no renewal)**: rejected. The catalog's exception pattern (per CR-BP-25) is time-bounded; a one-time waiver is insufficient.
- **A3. Per-rule exceptions (e.g. "IDM-001 is exempt for record X")**: rejected. The exception is a per-record verdict, not a per-rule verdict.

### 6.4 Disposition

- **Normative**: the review-retained verdict in `reconciliation/normalization.yaml` is the exception mechanism.
- **Verification**: the entity-system gate consults the registry; a record carrying an exception is not blocking.
- **Lifecycle**: exceptions expire; renewal requires a new CR.

## 7. Open questions still open

The following are deferred to Stage 2 (Specification and Approval):

- **U-01 Cross-catalog URI form**: deferred to T8 of the umbrella programme. Today's references use target id + scope; URLs are a future enhancement.
- **U-07 OpenDEAM authority chain alignment**: the 12 EGV-001..012 are ratified under the new dea-governance repo's authority track; the alignment with CR-001..008 (OpenDEA 1.0.0) is a Stage 2 spec doc.
