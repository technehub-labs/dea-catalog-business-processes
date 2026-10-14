# Contributing to `dea-catalog-processes`

Minimal. The cardinal rules govern the only contribution shape matters
for this repository.

## Authorship

Every authorship-bearing field in this repository must carry
`Emmanuel A. Otchere` (or, for org-level CFF entries, `TechNeHub Labs`).
The string `Coder`, `Agent`, `Hermes`, `Claude`, `GPT`, `Cline`, `OpenAI`,
`MiniMax`, `MiniMax-M3`, or any other agent/tool name is forbidden in
any authorship-bearing field of any published artifact.

This rule is enforced by gate [32] (`scripts/check_authorship.py`,
blocking). It is data-driven from
`reconciliation/authorship-fields.yaml`. The full rule statement lives
in `docs/governance/cardinal-rules.md`.

If your contribution introduces a new authorship-bearing field, extend
the registry in the same PR; the gate will block the change otherwise.

## How to land work

1. Open a `feature/...`, `fix/...`, or `refactor/...` branch.
2. Develop, test, commit.
3. Open a PR; CI runs all 32 conformance gates. Address any failures
   before requesting review.
4. Squash-merge on approval; the branch is auto-deleted.

## Cardinal-rules reference

- [docs/governance/cardinal-rules.md](docs/governance/cardinal-rules.md)
- `reconciliation/authorship-fields.yaml`
- `scripts/check_authorship.py` (gate [32])
- `change-requests/CR-BP-118-authorship-cardinal-rule.md`
