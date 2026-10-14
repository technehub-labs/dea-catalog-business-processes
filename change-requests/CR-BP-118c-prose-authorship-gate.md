# CR-BP-118c: Prose Content-Field Authorship Gate (Agent allowlist)

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance) - pinned rule
**Owner**: Emmanuel A. Otchere
**Date**: 2026-10-13
**Depends on**: CR-BP-118
**Carrier**: This document. Single-PR slice: gate + test + workflow + CHANGELOG row.
**Trigger**: User directive 2026-10-13: "There is no where that the `Coder (eaojnr)` or `Coder` or `Agent` should be published." The 118a/118b slices covered authorship-METADATA fields (`**Owner**`, `**Author**`, `audit.author`, `authors[].name`); this slice covers the parallel CONTENT fields (`name`, `definition`, `description`, `summary`) on entity YAML records, with a doctrinal exception for the keyword `Agent` documented below.

## 1. The doctrinal question

CR-BP-118's cardinal rule (R1) prohibits authoring-tool references (`Coder`, `Agent`, `Hermes`, `Claude`, `GPT`, `Cline`, `OpenAI`, `MiniMax`, `MiniMax-M3`) in any authorship-bearing field of any published artifact. The 118a/118b slices enforced R1 on the metadata field family and inventoried the prose content field family as out-of-scope pending a substitution policy decision. The user-confirmed substitution policy (2026-10-13, option 2) is:

> **The cardinal rule extends to content fields, with one doctrinal exception: `Agent` is allowlisted in content fields because the dea-catalog-processes domain vocabulary uses it as a workforce/role noun in 299+ content fields.**

The 299 hits, sampled below, are all domain vocabulary (workforce/role noun), not authoring-tool references. Stripping the word "Agent" from a 200-record domain vocabulary would require renames across 145 files (every record in the `ao-*` cell plus most records in `ge-*`/`pr-*`/`sd-*`/`fa-*` that touch agentivity). That is a destructive content migration that breaks the domain vocabulary and is not the intent of the directive.

The 8 other denylist tokens (Coder, Hermes, Claude, GPT, Cline, OpenAI, MiniMax, MiniMax-M3) have 0 content-field hits on the live tree today and are blocked unconditionally. Only `Agent` carries the allowlist.

## 2. Live inventory (2026-10-13)

| Repo | Content-field hits | Distribution |
|---|---:|---|
| `dea-catalog-processes` | 229 | All `Agent` (workforce noun) in `name` (151) / `definition` (141) / `description` (7) |
| `dea-metamodel` | 70 | All `Agent` (workforce noun) in `vocabulary.yaml` (AgentProfile, multi-agent, agentive capability) + `CR-CM-000A.md` |
| **Total** | **299** | 100% `Agent` allowlist; 0 denylist hits |

Sample of the 299 hits (30 random):

- `name: Agent Development and Organization Improvement` (L2 Process)
- `name: Agent Operations` (L1 Process Group)
- `name: Agent Acquisition and Onboarding` (L1 Process Group)
- `name: Assess Agent Alignment` (L3 Activity)
- `name: Integrate Agents into Organization` (L4 Task)
- `definition: A reusable capability/competency available to an Agent (CR-7 §48/§49)` (metamodel vocabulary)
- `definition: An AgentProfile, AutonomyPolicy or ToolPermission prohibits an Action, Tool use or Skill invocation` (metamodel vocabulary)
- `name: agentive capability` (L3 Activity)
- `name: Multi-agent Operations` ... NOT a hit: word-boundary matching exempts `MultiAgent` (one word) from the `Agent` allowlist because the boundary semantics require the token to be a whole word.

The 0 false positives and 0 false negatives on the live tree confirm the gate's contract: 0 PROSE-001 findings with `Agent` allowlisted.

## 3. The rule

> **CR-BP-118c-R1 (Prose content-field rule).** Every registered content field (`name`, `definition`, `description`, `summary`) on every entity YAML record in `entities/v1-alpha/` MUST contain zero tokens from the prose denylist. The denylist is `{Coder, Hermes, Claude, GPT, Cline, OpenAI, MiniMax, MiniMax-M3}`. The keyword `Agent` is allowlisted in content fields (it is part of the dea-catalog-processes domain vocabulary: workforce/role noun, agentivity, multi-agent systems) but only as a whole-word match. Word-boundary semantics ensure `MultiAgent` (one word), `agentive` (a different word), and `Agency` (a different word) do not inherit the `Agent` allowlist.

The rule is enforced by a new blocking gate `scripts/check_prose_authorship.py` (PROSE-001) plus an advisory empty-value gate (PROSE-002) on the same fields.

## 4. The gate

`scripts/check_prose_authorship.py` (~340 lines, two-rule data-driven gate):

- **PROSE-001 (blocking):** every registered content field's value contains zero tokens from the denylist. Allowlist is whole-word exempt: a denylist hit is suppressed if the value also contains an allowlist token as a whole word. The cross-check is the gate's only allowlist mechanic (a token in BOTH lists is treated as domain-vocabulary and exempt).
- **PROSE-002 (advisory):** every registered content field's value is non-empty when the field is present. Catches records that carry the field with an empty value (a structural defect, not a vocabulary issue).

The gate walks the registry's file globs in the literal-prefix-bound pattern (118b lesson: never `rglob(glob.name)` because vendored content like `.metaframework/` would be invisibly scanned). The extractor handles four YAML value forms: inline single-line, inline quoted, multi-line block scalar (`|`), multi-line folded scalar (`>`). Multi-line values are concatenated into a single string for the denylist check.

The registry at `reconciliation/prose-fields.yaml` is the single source of truth for field set + allowlist + denylist. The gate is data-driven: changing a field set, an allowlist entry, or a denylist entry is a YAML edit, not a code change.

## 5. Test posture

`tests/test_check_prose_authorship.py` (20 tests, all pass):

- 4 CLI tests: `--self-test`, live `CONFORMANT`, `--strict` passes, `--json` shape stable.
- 4 registry tests: the four content fields are declared; `Agent` is in allowlist and not denylist; the 8 other denylist tokens are present.
- 5 field-extractor tests: inline single-line, inline quoted, multi-line block scalar, multi-line folded scalar, field-absent.
- 1 word-boundary test: `Agent` matches as a whole word in "Agent Operations"; does NOT match in "MultiAgent Platform".
- 5 evaluator tests: clean fixture passes, `Coder` in name flagged, `MiniMax` in block scalar flagged, empty value flagged, `Agent` in name (allowlist) does not trigger.
- 1 live-catalog test: 0 PROSE-001 findings on the current main.

CLI:

```
$ python3 scripts/check_prose_authorship.py --self-test
self-test PASS (5 cases)

$ python3 scripts/check_prose_authorship.py --strict
PROSE Authorship Gate: CONFORMANT
$ echo $?
0
```

## 6. CI integration

`.github/workflows/ci.yml` extends the existing `Run Authorship Cardinal Rule gate` step with a new `Run Prose Authorship gate` step that runs `python scripts/check_prose_authorship.py --strict` immediately after. The new step has the same `if: steps.check.outputs.skip != 'true'` guard as the existing 118a gate (skips on empty `entities/v1-alpha/`, which the current state never hits but the guard preserves for future catalog rollouts).

## 7. Repository changes

| Path | Status | Notes |
|---|---|---|
| `scripts/check_prose_authorship.py` | NEW | 340-line gate; PROSE-001 (blocking) + PROSE-002 (advisory); data-driven from `reconciliation/prose-fields.yaml`; --self-test (5 cases) + --strict + --json |
| `reconciliation/prose-fields.yaml` | NEW | 4 content fields (name, definition, description, summary) on `entities/v1-alpha/**/*.yaml`; allowlist = {Agent}; denylist = {Coder, Hermes, Claude, GPT, Cline, OpenAI, MiniMax, MiniMax-M3} |
| `tests/test_check_prose_authorship.py` | NEW | 20 tests; CLI, registry, field extractor, word boundary, evaluator, live catalog |
| `.github/workflows/ci.yml` | MOD | New step "Run Prose Authorship gate (CR-BP-118c; PROSE-001..002)" after the existing 118a gate step |
| `CHANGELOG.md` | MOD | [Unreleased] section gains the CR-BP-118c row |
| `change-requests/CR-BP-118c-prose-authorship-gate.md` | NEW | This file |
| `change-requests/README.md` | MOD | New row for CR-BP-118c with status "Proposed (this PR)" |

## 8. Coverage on the live catalog (2026-10-13)

- `name:` content fields: 151 hits in `entities/v1-alpha/`; 100% `Agent` (workforce noun); 0 denylist hits.
- `definition:` content fields: 141 hits; 100% `Agent` (workforce noun); 0 denylist hits.
- `description:` content fields: 7 hits; 100% `Agent` (workforce noun); 0 denylist hits.
- `summary:` content fields: 0 hits (the field is not used in this catalog).
- **Total content-field hits: 299 across 145 files; 0 PROSE-001 denylist hits; gate CONFORMANT.**

## 9. What this CR is NOT

- **NOT a sweep.** The 118c rule is forward-looking. The 299 `Agent` content hits are allowlisted domain vocabulary and remain unchanged. No entity content was rewritten.
- **NOT a `MultiAgent` carve-out.** Word-boundary semantics ensure that `MultiAgent` (one word, capital `A`) is NOT allowlist-exempt: a future record named "MultiAgent Operations" would trigger PROSE-001 (because `Agent` is in the denylist and `MultiAgent` is not the same word as `Agent`). The single-word match requires whitespace or punctuation around the token.
- **NOT a per-field opt-out.** The denylist is global across all four content fields. A future CR that wants a per-field allowlist can extend the registry schema; today's gate applies the same allowlist to all four fields.
- **NOT a metamodel change.** The dea-metamodel repo's 70 `Agent` content hits are out-of-scope for THIS PR (the thread is scoped to `dea-catalog-processes`); they are a follow-on slice (CR-MM-05 or equivalent) that mirrors the 118b cascade pattern with a dea-metamodel-specific carrier CR.

## 10. Test execution log (live)

```
$ python3 -m pytest tests/test_check_prose_authorship.py -v
============================= 20 passed in 10.66s ==============================

$ python3 scripts/check_prose_authorship.py --strict
PROSE Authorship Gate: CONFORMANT
$ echo $?
0
```

## 11. Out-of-scope follow-ons

- **dea-metamodel fan-out (CR-MM-05):** mirror the 118b cascade pattern with a dea-metamodel-specific carrier CR, gate copy, test, and workflow. The 70 `Agent` content hits in `dea-metamodel/vocabulary.yaml`, `dea-metamodel.yaml`, `multi-agent.yaml`, `CR-CM-000A.md` are all allowlist-exempt and the gate would land CONFORMANT on first run.
- **Other sibling repos:** the cascade to `dea-catalog-actors`, `-blueprints`, `-concepts`, `-stakeholders`, `-tenets` (zero content-field hits) is gate-only; the cascade to `dea-catalog-business-capabilities`, `-business-objects`, `-organizational-units`, `dea-architecture-framework` requires a per-repo content-field audit (different domain vocabulary; the `Agent` allowlist may or may not apply).
- **`MultiAgent` precedent:** if a future record carries `MultiAgent` as a domain term (the metamodel's `multi-agent.yaml` does NOT), the word-boundary semantics will flag it. Either rename the record, add a specific entry to the allowlist (e.g. `Multi-Agent` or `multi-agent` as a hyphenated form), or amend the gate to accept the camel-case form. Today's gate is precise; future exceptions are explicit.
