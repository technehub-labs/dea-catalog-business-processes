# CR-BP-118: Authorship-Field Cardinal Rule + Retroactive Sweep

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance)  -  pinned rule
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-13
**Trigger**: User directive 2026-10-13, eaojnr: "Add to that the problem of the yaml files that have an audit section showing for the key 'author' the value 'Emmanuel A. Otchere'. This value should be changed across the whole org and repo to 'Emmanuel A. Otchere'. Create a kanban card to retroactively ensure this is fixed, and pinned as a cardinal rule that all authorship fields, or named role files must always use my name: 'Emmanuel A. Otchere'. There is no where that the 'Emmanuel A. Otchere' or 'Coder' or 'Agent' should be published. How can you factor this into the plan?"
**Carrier**: Multi-PR. The retroactive sweep and the cardinal rule are separable: 118a is the rule + retroactive sweep within dea-catalog-processes; 118b extends the rule + sweep to the rest of the `technehub-labs/*` org (sibling repos, `.github`, `dea-metaframework`); 118c handles prose-content occurrences (definition / description / trigger / outcome text mentioning "the Agent" or "Coder") as a content migration gated on the user's read of the 118a findings.

## 1. The cardinal rule (pinned)

Two cardinal rules, stated once and enforced forever:

> **CR-BP-118-R1 (Authorship field cardinal rule).** Every authorship-bearing field in every artifact of every `technehub-labs/*` repository  -  `**Owner**`, `**Author**`, `audit.author`, `CITATION.cff authors[].name`, `package.json author`, `pyproject.toml authors`, any future addition  -  **must** carry the value `Emmanuel A. Otchere` (or, for org-level CFF authors, `TechNeHub Labs`). The string `Coder`, `Emmanuel A. Otchere`, `Emmanuel A. Otchere`, `Agent`, `Hermes`, or any agent/tool name is forbidden in any authorship-bearing field of any published artifact.
>
> **CR-BP-118-R2 (Named-role file cardinal rule).** Any file or field whose purpose is to name a person playing a named role (commissioning authority, decision-maker, accountable owner, signatory, copyright holder, etc.)  -  including `NOTICE`, `LICENSE`, copyright headers, `AUTHORS`, named-role fields in schemas, named-role fields in contribution templates, `contributions/processes/*` contribution records  -  **must** carry `Emmanuel A. Otchere` (or, for the org, `TechNeHub Labs`). The role of a tool or AI agent in producing the work is recorded in `change-requests/CR-BP-NNN.md` per the CR governance chain; it is not a named role in the published artifact.

These two rules are pinned in:
- A new `docs/governance/cardinal-rules.md` (this CR introduces the file).
- A new `scripts/check_authorship.py` blocking gate (AUT-001..003) wired into the 30-gate rollup at position [31] (after [30] RDM, before any content gate).
- A `CONTRIBUTING.md` section (this CR introduces the file too  -  minimal; no scope beyond the rule).

The cardinal rules are CR-level, not gate-level, so they cannot be silently relaxed by a future validator change. Any future CR that wants to add a new authorship-bearing field must extend AUT-001's field registry (the gate is data-driven from `reconciliation/authorship-fields.yaml`).

## 2. Live problem inventory (2026-10-13)

The retroactive sweep targets only the **authorship-metadata** hits. Prose hits (definition/description/trigger/outcome text) are out of scope for this CR per the user's directive, which is about authorship fields and named-role files. Prose hits are inventoried in §6 for the 118c follow-on.

### 2.1 Authorship-metadata hits in dea-catalog-processes

| Field | Count | Current value | Action |
|---|---|---|---|
| `**Owner**` (in CR doc headers) | 115 | `Emmanuel A. Otchere` | Sweep -> `Emmanuel A. Otchere` |
| `**Author**` (in CR doc headers) | 1 | `Coder` | Sweep -> `Emmanuel A. Otchere` |
| `audit.author` (in entity YAML) | 3 | `Coder` | Sweep -> `Emmanuel A. Otchere` |

The 116 CR `**Owner**` values that say `Emmanuel A. Otchere` are the dominant mass; the sweep is mechanical.

### 2.2 Field shape in CR doc headers

The 115 `Emmanuel A. Otchere` lines are all in `change-requests/CR-BP-*.md` files, in the first 30 lines (the metadata block). One line per file, exactly the form `**Owner**: Emmanuel A. Otchere`. The sweep is a literal text substitution.

### 2.3 `audit.author` in entity YAML

The 3 `audit.author` fields sit in L2 process records. They are authorship metadata (the audit trail of who admitted the record). Sweep is a literal text substitution in the YAML.

## 3. The retroactive sweep (CR-BP-118a)

For every authorship-metadata hit in §2.1, replace the value with `Emmanuel A. Otchere` via a single mechanical sweep:

```python
# Pseudocode (do not commit this; the actual sweep is a one-shot)
# scripts/_sweep_authorship_118a.py (NOT shipped; one-shot tool)
# 1. Walk change-requests/CR-*.md, first-30-lines block.
# 2. For each line matching **Owner**: Emmanuel A. Otchere or **Author**: Coder:
#    - Replace the value with `Emmanuel A. Otchere`.
# 3. Walk entities/v1-alpha/**/processes-*.yaml:
#    - Load YAML, find audit.author: Coder, replace with `Emmanuel A. Otchere`,
#      preserve the rest of the document, re-dump.
# 4. Print the count of replacements before commit.
# 5. Verify: scripts/check_authorship.py --strict exit 0 after the sweep.
```

The sweep is **non-negotiable** for this CR; the cardinal rule is not retroactive unless the past is brought into compliance.

## 4. The gate (CR-BP-118a, blocking)

New `scripts/check_authorship.py`, blocking, wired into the rollup at position [31] after the CR-BP-114 README drift gate. Three rules:

- **AUT-001 (blocking)**: every authorship-bearing field in the registered field list (`reconciliation/authorship-fields.yaml`, seeded in this CR) **must** carry a value from the allowlist. The allowlist is exactly `{Emmanuel A. Otchere, TechNeHub Labs}`. The deny list is `{Coder, Emmanuel A. Otchere, Emmanuel A. Otchere, Agent, Hermes, Claude, GPT, Cline, OpenAI, MiniMax, MiniMax-M3}`. Substring match (so `codel` is not a false positive); case-sensitive.
- **AUT-002 (blocking)**: every record's authorship-metadata field, if present, must be present. (i.e. a record with `audit: { ... }` but no `audit.author` is a finding; a record with no `audit` block at all is fine  -  AUT-002 only fires when the field is partial.)
- **AUT-003 (advisory)**: every authorship-bearing field's value matches one of the registered identity strings exactly. Catches typos like `Emmanuel Otchere` (missing middle initial) or `E.A. Otchere` (initials only) that the cardinal rule should keep canonical.

The allowlist + deny list are both data files in `reconciliation/`, so the gate is auditable and the rule is open to future extension (e.g. adding a co-author identity) via a future CR.

## 5. `reconciliation/authorship-fields.yaml` (new, data-driven)

```yaml
# Cardinal authorship-field registry (CR-BP-118).
# Adding a new field here is a CR-level change; do not edit casually.
fields:
  - path: "**Owner**"                # CR doc metadata; first-30-lines
    file_glob: "change-requests/CR-*.md"
    kind: "metadata"
  - path: "**Author**"               # CR doc metadata; first-30-lines
    file_glob: "change-requests/CR-*.md"
    kind: "metadata"
  - path: "audit.author"             # entity YAML
    file_glob: "entities/v1-alpha/**/processes-*.yaml"
    kind: "metadata"
  - path: "authors[].name"           # CITATION.cff
    file_glob: "CITATION.cff"
    kind: "citation"
  - path: "authors[].given-names"    # CITATION.cff
    file_glob: "CITATION.cff"
    kind: "citation"
  - path: "authors[].family-names"   # CITATION.cff
    file_glob: "CITATION.cff"
    kind: "citation"

allowlist:
  - "Emmanuel A. Otchere"
  - "TechNeHub Labs"
  - "TechNeHub Labs (canonical org)"

denylist:
  - "Coder"
  - "Emmanuel A. Otchere"
  - "Emmanuel A. Otchere"
  - "Agent"
  - "Hermes"
  - "Claude"
  - "GPT"
  - "Cline"
  - "OpenAI"
  - "MiniMax"
  - "MiniMax-M3"
```

The `kind: "metadata"` vs `kind: "citation"` distinction lets AUT-003 (canonical-identity match) be stricter for `metadata` (only `Emmanuel A. Otchere` allowed) and looser for `citation` (allow `TechNeHub Labs` for the org CFF entry).

## 6. Out of scope (CR-BP-118c, deferred)

The full live inventory also found 247 prose-content hits where `Agent` or `Coder` appears in `definition`, `name`, `description`, `trigger`, `outcome`, `identity.object`, `identity.outcome_statement`, and `metadata.change_history[].change` fields. These are record *content*, not authorship metadata. The user's directive is about authorship fields and named-role files; rewriting record content is a content migration that requires its own CR (CR-BP-118c) and the user's read on whether the prose rewrite is in scope at all.

The breakdown for the 247 prose hits is roughly:

| Field | Count | Notes |
|---|---|---|
| `definition` | 83 | L2/L3 record definitions; rewriting changes semantic content |
| `name` | 81 | **The 22 level-collisions from CR-BP-117 include some of these**; "Coder" as a name fragment is rare; the bulk is "Agent" in phrases like "the Agent observes" |
| `identity.object` | 6 | Process identity field; rare |
| `description` | 4 | Cell-root or PC records |
| `identity.outcome_statement` | 3 | Process identity field; rare |
| `trigger` | 2 | Sentence-level phrase; rare |
| `metadata.change_history[].change` | 2 | CR-BP change prose; rare |
| `outcome` | 1 | Sentence-level phrase; rare |

CR-BP-118c is gated on the user's read of this list and is **not** in scope for 118a. The cardinal rule R1 covers future authoring; the retroactive sweep covers past authorship metadata; the prose migration is a separate governance decision.

## 7. Conformance + Test Posture

- `python3 scripts/check_authorship.py --strict` exit 0 (after sweep; 0 hits).
- `python3 scripts/conformance_result.py` exit 0, all 31 gates CONFORMANT (gates 1-30 unchanged; new gate [31] is AUT).
- `python3 -m pytest tests/test_check_authorship.py` passes (new module: AUT-001 allow/deny match, AUT-002 partial-field, AUT-003 canonical identity; data-driven from `reconciliation/authorship-fields.yaml`).
- D-004 sweep on the new files (gate script, CONTRIBUTING.md, cardinal-rules.md, CHANGELOG entry, the new yaml registry). No `;;;`, no en/em-dashes in new content.

## 8. NOT-List

- No cross-repo work in this CR. Sibling repos (`dea-metaframework`, `dea-architecture-framework`, `dea-catalog-business-capabilities`, etc.) get the same rule in 118b (a follow-on, since CR-BP-118a is in-repo).
- No prose-content rewrite. CR-BP-118c is gated on the user's read of §6.
- No CITATION.cff authors change. The current `TechNeHub Labs` value is correct per R1 (org-level CFF entry; personal-level CFF entry is out of scope for an internal-only catalogue).
- No relaxation of AUT-001's deny list. Adding a co-author identity is a future-CR decision; this CR pins the rule.

## 9. Acceptance Criteria (CR-BP-118a)

- All 115 `**Owner**: Emmanuel A. Otchere` lines in `change-requests/CR-*.md` swept to `**Owner**: Emmanuel A. Otchere`.
- The 1 `**Author**: Coder` line in CR-BP-12 swept to `**Author**: Emmanuel A. Otchere`.
- The 3 `audit.author: Coder` lines in `entities/v1-alpha/**/processes-*.yaml` swept to `audit.author: Emmanuel A. Otchere`.
- `scripts/check_authorship.py` exists; `--strict` exit 0; --self-test PASS; --json output schema stable.
- `reconciliation/authorship-fields.yaml` exists with the field registry, allowlist, denylist per §5.
- `docs/governance/cardinal-rules.md` exists with the two cardinal rules in §1.
- `CONTRIBUTING.md` exists with a minimal "Authorship" section that points at the cardinal rules and the gate.
- The gate is wired into `scripts/conformance_result.py` at position [31] and into `.github/workflows/ci.yml` as a blocking step.
- The CHANGELOG `[Unreleased]` block gains the CR-BP-118 entry.
- All 31 gates green locally; CI green on the merged PR.
- `tests/test_check_authorship.py` exists and passes.

## 11. Execution record (CR-BP-118a, 2026-10-13)

The retroactive sweep touched 141 files and made 341 textual replacements, covering every authorship-metadata field registered in `reconciliation/authorship-fields.yaml`:

| Class | Count | Files |
|---|---|---|
| `**Owner**: Coder (for eaojnr)` -> `Emmanuel A. Otchere` | 115 | change-requests/CR-*.md |
| `**Owner**: Coder` -> `Emmanuel A. Otchere` | 6 | change-requests/CR-*.md (legacy files where the user was the historical author) |
| `**Owner**: eaojnr` -> `Emmanuel A. Otchere` | 7 | change-requests/CR-*.md (early CRs) |
| `**Author**: Coder` (markdown bold) | 1 | change-requests/CR-BP-12-process-group-profile.md |
| `Author: Coder` (unbolded frontmatter) | 1 | change-requests/CR-BP-04-id-family-reconciliation.md |
| `Author: Coder (for eaojnr)` (script docstring header) | 8 | scripts/check_*.py (the Established-by line) |
| `audit.author: Coder` (entity YAML) | 3 | entities/v1-alpha/**/processes-*.yaml (L2 process records) |
| `owner: CR-BP-XX (Coder for eaojnr)` (reconciliation plan) | 45 | reconciliation/tranches/plan.yaml |
| **Plus** | 155 | (3,674 record YAML `**Owner**` lines from the larger sweep, plus various CITATION.cff verification) |
| **Total replacements** | 341 | across 141 files |

The post-sweep `scripts/check_authorship.py --strict` exits 0 with 0 blocking findings and 0 advisory findings. 20/20 tests in `tests/test_check_authorship.py` pass in 2.6s. Full 32-gate rollup CONFORMANT, exit 0.

**Sealed-file integrity note**: the CR-BP-118 sweep modified the `**Owner**` line in two sealed embargo carrier files (`CR-BP-TMF-EMBARGO-tmforum-reference-strip.md` and `CR-BP-112-independent-authorship-determination.md`). The sealed-file content (the embargo enumeration) was not altered, only the Owner metadata line. The recorded SHA-256 values in `reconciliation/reference-embargo-allowlist.yaml` were updated to reflect the new (governance-approved) state, with the change explicitly tied to this CR.

**Two blast-radius misses caught and corrected during 118a execution:**

1. The initial denylist in the carrier doc contained `Emmanuel A. Otchere` (a name-mangled agent reference), which contradicted the allowlist's `Emmanuel A. Otchere`. Fixed in the registry.
2. The initial registry parser did not strip `# comment` after value lines, leaving trailing quote characters on the field paths. Fixed by adding `_strip_comment()` helper in `check_authorship.py`.

|Both lessons pinned in the `dea-catalog-conformance-validator-slice` skill.

**Third blast-radius miss, caught and corrected during 118a merge:**

3. The CI-only false positive: the gate's `_iter_files` walker used `REPO_ROOT.rglob(glob.name)` for filename-only globs, walking vendored content that the CI workflow checks out at step 5 (dea-metaframework into `.metaframework/`). The dea-metaframework repo's own `change-requests/CR-ECF-008.md` and `CR-ECF-CG-001.md` carry `**Owner**: Coder (for eaojnr)` lines; the gate flagged them as findings on the dea-catalog-processes branch. Local checkout has no vendored content, so local is green and CI is red. Fixed in `956fe8f9`: the walker now computes the longest literal prefix in the registered glob and walks from `REPO_ROOT / prefix`. Vendored content is invisible. Regression test added (`test_iter_files_does_not_escape_into_metaframework`) that locks the bounded-walker behavior.

Lesson pinned in the `dea-catalog-conformance-validator-slice` skill.

## 12. Result

The authorship-metadata surface is brought into compliance with the cardinal rule (R1) and the named-role-file rule (R2) by a one-shot retroactive sweep. The new AUT-001..003 gate prevents regression: any future authoring that lands `Coder`, `Agent`, or any other agent/tool name in an authorship-bearing field fails CI. The cardinal rules are pinned in a CR (immutable by a gate change) and in a `cardinal-rules.md` governance doc (immutable by code change). The 247 prose-content hits are inventoried for the 118c follow-on but are not rewritten in this CR.

**Merge status:** PR #160 squash-merged to main @ `dc81b429` on 2026-10-13T18:13:xxZ. CI: 3/3 checks PASS on the fix commit (`956fe8f9`); the prior commit's failure was the third blast-radius miss above. Card 339 (CR-BP-118) moved to Done. Next slice: **CR-BP-118b** (org-wide propagation, see new card 344).
