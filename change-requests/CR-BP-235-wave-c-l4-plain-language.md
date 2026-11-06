# CR-BP-235: Wave C — L4 Task Plain-Language Authoring (2,900 Records)

**Status**: Proposed (this PR)
**Layer**: Process Catalog (operational documentation completions)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-05
**Depends on**: CR-BP-230 (the five plain-language fields this wave authors), CR-BP-231 (the profile v3 README that renders them), CR-BP-232 (the HUM-001..007 gate whose L4 findings this wave drains to zero), CR-BP-233/234 (Waves A/B — the authoring method, driver pattern, and audit-trail convention this wave repeats at the L4 floor)

> **Scope.** Wave C of the two-layer remediation programme — the largest tranche: author the five plain-language fields for **all 2,900 L4 Task records**. Task grounding is the record's own required fields (`definition`, `trigger`, `outcome`, `responsibility` — the 5-phase verb-object decomposition already documents each task's working object, phase trigger, phase outcome, and custodian), plus the parent Activity and its parent Business Process for worked-example casting. No invention; documented custodian roles and parent-BP actors may be referenced. Every record gains the five fields appended at EOF with the CR-BP-225 comment-banner convention via the idempotent driver `scripts/author_cr235_wave_c.py`. After authoring: READMEs regenerate (Part I renders the provided prose on all 2,900 L4 records — including the worked example the standing pointer could only defer), `CATALOG.yaml` regenerates, and the L4 layer's HUM presence findings drain to zero.

**Lands against**: 2,900 L4 record files (EOF-appended comment banner + five fields); `scripts/author_cr235_wave_c.py` (the applying driver, idempotent); `reconciliation/closure/cr235-wave-c.json` (execution manifest); `reconciliation/authoring/cr235-wave-c/` (the authored-content audit trail, one JSON per batch); regenerated READMEs; regenerated `CATALOG.yaml` + HUM reports; this CR + CHANGELOG + register row. **0 id changes. 0 gate changes. 0 schema changes. 0 L2/L3/L1/L0 record changes.**

## 1. The authoring method

Identical contract to CR-BP-233 §1 / CR-BP-234 §1 (grounding, MECE, jargon denylist, semantic containment, agent typing from documented custodian roles, idempotency), with the L4 grounding simplification: the task's own required fields carry the full phase semantics. Authored in 50 verified batches (58 records each); every batch mechanically verified (id coverage, lengths, denylist, MECE) before application; the driver re-validates everything at apply time and refuses the run on any violation.

## 2. What does NOT change

- No canonical name, id, status, responsibility, boundary, trigger, outcome, or IO changes — the five fields are additive documentation attributes.
- No gate logic or posture changes; no schema changes; no L2/L3/L1/L0 record changes.
- The generated Part II sections are byte-stable for every L4 record.

## 3. Verification / Acceptance Criteria

1. HUM gate on the L4 layer: **0 findings** across all seven rules for all 2,900 L4 records (corpus-wide presence findings drop by 2,900 × 5 = 14,500, to 490 = the 98 L1/L0 records × 5).
2. Schema validation green (3,675 CI-visible records) with the five fields present on all 2,900 L4 records.
3. RDM-001/002/003 CONFORMANT on the regenerated corpus; each L4 README's Part I renders the authored prose — including a valid `worked_example` — with no standing pointer.
4. Driver idempotency: second run writes 0.
5. Full gate suite green; freshness procedure (commit → CATALOG regen → amend) honoured.
