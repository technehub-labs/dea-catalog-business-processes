# CR-BP-13: L1 Process Group Research Ratification

**Status**: Proposed
**Layer**: L1 (Process Catalog)
**Owner**: TechNeHub Labs
**Depends on**: CR-BP-11 (49-coordinate L1 disposition register; merged),
CR-BP-12 (L1 Process Group profile/schema; merged)
**Companion to**: CR-BP-11 (L1 disposition register; this CR ratifies the
research artefacts against that register), CR-CATALOG-STRUCT-02 (cross-repo;
process catalog adoption; this CR flips that row from "Proposed" to
"Merged" in `change-requests/README.md`).
Validator note: the CR-META-005 CR_REF_PATTERN matches `CR-BP-NN` intra-repo
refs; the cross-repo `CR-CATALOG-STRUCT-NN` companion is documented in prose
until CR-META-005 is extended to admit cross-repo CR patterns.

## What this CR is

Closes the research-status question left open by CR-BP-11. The CR-BP-11
register records 49 coordinates with dispositions: 38 accepted, 11
deferred. It is explicitly `candidate-not-canonical; subject to review`
(CR-BP-11 §1). This CR ratifies the register: the 38 accepted
dispositions become `ratified-accepted`; the 11 deferred dispositions
become `backlog-deferred` with a single shared rationale.

This is the research half of the catalog story. The seven-domain
admission tranches (CR-BP-13a..BP-13g, one per ECF Domain) are a
separate concern: they promote each accepted L1 coordinate to a
canonical Process Group record. CR-BP-13 only ratifies the register;
it does NOT create new L1 records.

## What changes

### Data changes

- **`l1-register.yaml`**: every `disposition: accepted` flips to
  `disposition: ratified-accepted` with `ratified_at: '2026-09-05'` and
  `ratified_by: CR-BP-13`. Every `disposition: deferred` flips to
  `disposition: backlog-deferred` with the same ratification stamp
  and a `deferral_reason` block (the shared rationale). A top-level
  `ratification: { version: 1, cr: CR-BP-13, ratified_at: '2026-09-05',
  ratified_accepted: 38, backlog_deferred: 11, deferred_rationale: ... }`
  block is added before `register:`.
- **`l1-candidate-universe.yaml`**: same per-candidate flip applied to
  all 102 L1 candidates (86 ratified-accepted, 16 backlog-deferred).
  Top-level `ratification:` block added.
- **`L1-REGISTER-v0.1.md`**: status line flips from
  `candidate-not-canonical; subject to review` to
  `ratified-canonical-2026-09-05 (CR-BP-13)`. Adds a ratification summary
  block at the top.
- **`research/README.md`**: adds CR-BP-13 to the Governing CR section
  and a new `Ratification evidence` section with the disposition table.
- **`dea:group-customer-lifecycle-management.yaml`**: appends a
  `change_history` entry recording the ratification.

### Tool changes

- **`tools/ratify_research_register.py`** (NEW, ~210 lines): idempotent
  script that performs the flips. Line-by-line approach preserves source
  formatting and comments. Detects existing `ratification:` block and
  exits as a no-op (idempotency gate).
- **`tests/test_ratify_research_register.py`** (NEW, 9 tests): offline
  tests covering basic ratification, top-level block insertion, deferral
  reason, comment preservation, idempotency, dry-run, and unknown-
  disposition safety.

### Documentation changes

- **`change-requests/README.md`**: add a row for CR-BP-13. Flip the
  CR-CATALOG-STRUCT-02 row from "Proposed" to "Merged" (PR #21 landed).

## The rationale (CR-BP-13 §4)

**Why the 11 deferred coordinates stay in backlog rather than being
ratified or rejected**:

The 11 deferred coordinates all sit on the **Activate** or **Retire**
lifecycle stages. These are transition stages, not stable Process Group
operating scopes:

- **Activate** is the handover from Build to Operate. It is a sub-step
  of the receiving Process Group (the Operate coordinate already
  carries an accepted Process Group; Activate lives inside that group's
  scope).
- **Retire** is the wind-down of a Process Group. It is a sub-step of
  the ending Process Group (the Operate coordinate's group handles its
  own retirement).

Neither forms a stable L1 group on its own. Adding them as L1
Process Groups would create scope overlap with their sibling Operate
Process Group (PG-006 MECE violation).

**What this means for the seven-domain admission tranches**:

The 38 accepted coordinates are eligible for promotion to canonical L1
records. The 11 deferred coordinates are NOT (out of scope for the
admission tranches); they remain in the research backlog. If a
discrete Activate/Retire process identity is later identified
(e.g. the catalog adopts a new Process Scope for transition stages,
separate from Process Group), a follow-up CR can revisit the deferred
dispositions.

## Verification

- `python3 tools/ratify_research_register.py` flips 38 coordinates to
  `ratified-accepted` and 11 to `backlog-deferred` in
  `l1-register.yaml`; 86 L1 candidates to `ratified-accepted` and 16
  to `backlog-deferred` in `l1-candidate-universe.yaml`.
- Idempotency: re-running the script is a no-op (the `ratification:`
  block's `version: 1` gate prevents re-application).
- All 102 L1 candidates carry `ratified_at: '2026-09-05'` and
  `ratified_by: CR-BP-13`. The 16 backlog candidates carry the shared
  `deferral_reason`.
- `python -m pytest tests/test_ratify_research_register.py` returns
  `9 passed`.
- `python3 scripts/regenerate_catalog.py`: regenerates `CATALOG.yaml`
  cleanly with the updated research files.
- `python3 scripts/check_catalog_index.py --strict`: passes.
- `python3 scripts/conformance_test_catalog_structure.py --strict`:
  16/16 CSTs pass.
- Dash sweep on new prose: clean.
- Secret scan: 0.
- `git diff --check`: clean.

## Sequencing

| CR | Status |
|---|---|
| CR-BP-11 (research register) | Merged |
| CR-BP-12 (L1 Process Group profile) | Merged |
| **CR-BP-13 (research ratification)** | **This PR** |
| CR-BP-13a..BP-13g (seven-domain admission tranches) | future |

After this CR lands, the **research register is ratified** and the
catalog's first L1 Process Group is fully backed by canonical research
evidence. The admission tranches (separate work) can proceed against
the ratified register.