# CR-BP-225: Operational Completions (L2 Definition Promotion, L3/L4 IO Declarations, L0 Register Confirmation)

**Status**: Accepted (this PR)
**Layer**: Process Catalog (operational documentation completions)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-04
**Depends on**: CR-BP-220 (the derivation method: mechanical composition from documented record fields, no invention, source-cited), CR-BP-94-EXT-12 §9 (the IO applicability contract — the authority for what "correctly applied inputs" means at each level), CR-BP-94-EXT-24 (the L0 register this CR confirms), CR-BP-224 (the disposition whose last two caveats this CR closes)

> **Scope.** User directive 2026-11-04: complete the pending L2 and L0 actions, including the Operational sub-blocks, with correctly applied inputs. Three completions, all mechanical (CR-BP-220 method — derived from documented record content, source-cited, no invention): (a) **L2 definition promotion** — 145 records gain their `definition` field, verbatim from the record's own documented `description` (the README fallback remains as a safety net, now unused); (b) **L3/L4 IO declarations** — 580 activities + 2,900 tasks gain `inputs[]`/`outputs[]` per the EXT-12 §9 applicability contract, which explicitly forbids copying child IO from the parent and requires the actual use to be described: L4 entries derive from the task's own required `trigger`/`outcome` fields (its documented working objects); L3 entries derive from the activity's **own child tasks** (intake-phase trigger = the working input; concluding-task outcome = the contribution) with the child ids cited; (c) **L0 register confirmation** — every PC's `governance.provenance.status` flips to confirmed (user directive 2026-11-04), completing the EXT-24 window's remaining act ahead of schedule. Generator: the L1–L4 Operational Details gain the `scope` field-name fallback (the same mismatch class CR-BP-224 fixed at L0) — the last 49 not-declared renders eliminated.

**Lands against**: 145 L2 + 580 L3 + 2,900 L4 + 49 L0 record files (appends/in-place provenance line); `scripts/generate_readmes.py` (one fallback); 3,723 regenerated READMEs; `scripts/author_cr225_completions.py`; `reconciliation/closure/cr225-completions.json`; this CR + CHANGELOG + register row. **0 id changes. 0 gate changes. 0 count moves.**

---

## 1. The authority applied (EXT-12 §9)

| Concern | L2 | L3 | L4 |
|---|---|---|---|
| Inputs | Process-level business inputs *(declared: CR-BP-220)* | Activity working inputs *(this CR)* | Task working objects *(this CR)* |
| Outcomes | Process-level intended outcomes *(declared: CR-BP-220)* | Contribution to parent outcome *(this CR)* | Contribution to Activity result *(this CR)* |

The contract's hard rule — *"A child input or output MUST NOT automatically be copied from the parent. Where a child uses a parent-level input, the relationship must be explicit and the child's actual use described."* — drives every derivation: L4 uses its own required `trigger`/`outcome` fields (the phase's actual use, already documented at deposition under CR-BP-102); L3 uses its own child tasks' intake trigger and concluding outcome, with child ids cited in each entry.

## 2. What does NOT change

- No id, gate, CI, or count changes; the L2 schema stays non-strict (the CR-BP-220 precedent: extra props validate).
- The README renderer's L2 definition fallback stays (safety net; unused on live records after promotion).
- L0 metric targets remain directional stage standards — now **owner-confirmed**; numeric target-setting stays the annual review's discretion.
- The 12 governed residual gaps / 12 improvement items remain in the closure registers.

## 3. Verification / Acceptance Criteria

1. EXT-12 gate (IT-001..IT-010): **0 findings** — CR-BP-96 entry baseline (id/name/description), local id uniqueness, controlled vocabulary.
2. `io not-declared` renders: **3,729 → 0** across the README corpus; DOC-016..020 unchanged (4 pre-existing DOC-016 advisories).
3. L2 `definition` populated on 145/145; L0 `governance.provenance.status: confirmed` on 49/49.
4. Gates green: activity-model, mece, execution-boundary, entity-system, id-system, process-semantics, readme-consistency (RDM-001..003); parse-clean on 3,723 files.
5. Execution manifest committed (`reconciliation/closure/cr225-completions.json`); authoring idempotent (second run: 0).
6. Freshness gate green (commit→regen→amend).
