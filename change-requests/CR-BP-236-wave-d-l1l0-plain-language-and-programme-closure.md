# CR-BP-236: Wave D — L1/L0 Plain-Language Authoring (98 Records) + Two-Layer Programme Closure and HUM Blocking Flip

**Status**: Accepted (landed via PR #232; status backfilled post-merge per the immutability rule)
**Layer**: Process Catalog (operational documentation completions) + Cross-cutting (gate posture)
**Owner**: Emmanuel A. Otchere
**Date**: 2026-11-05
**Depends on**: CR-BP-230 (the plain-language fields), CR-BP-231 (the profile v3 README), CR-BP-232 (the HUM gate this CR flips to blocking), CR-BP-233/234/235 (Waves A/B/C — 3,627 records authored), CR-BP-CE-RL (the posture-flip precedent this closure follows)

> **Scope.** The final wave of the two-layer remediation programme. Two parts: **(a) Wave D authoring** — the five plain-language fields for the last 98 records (49 L1 Process Groups, grounded in scope/grouping/composes + owner; 49 L0 Process Contexts, grounded in cell charter/outcomes/governance roles/metrics); **(b) programme closure** — with all 3,723 records backfilled, the HUM-001..004 presence findings are 0 and gate **[51] Human Readability flips advisory → BLOCKING** in `conformance_result.py` (`--strict` on the HUM invocation), mirroring the CR-BP-CE-RL flip: the blocking profile is 0 across the corpus at flip time, so strict mode fails only on NEWLY introduced provided-layer defects (unbackfilled fields, jargon, MECE violations, bad agent types). HUM-005/007 have been 0 since the first authored record; they now police the layer permanently. The programme's foundational requirement (CR-BP-230 §1) is met corpus-wide: every entity is both semantically precise and human-relatable.

**Lands against**: 98 record files (49 L1 + 49 L0; EOF-appended comment banner + five fields); `scripts/author_cr236_wave_d.py` (the applying driver, idempotent); `scripts/conformance_result.py` (gate [51] posture flip); `reconciliation/closure/cr236-wave-d.json` (execution manifest); `reconciliation/authoring/cr236-wave-d/` (audit trail, 2 batch JSONs); regenerated READMEs; regenerated `CATALOG.yaml` + HUM reports; this CR + CHANGELOG + register row. **0 id changes. 0 schema changes. 0 existing-gate logic changes beyond the [51] posture flip.**

## 1. Wave D grounding

| Level | Grounding sources |
|---|---|
| L1 Process Group (49) | own `definition`/`scope`/`grouping_basis`/`membership_criteria`/`owner`; the `composes[]` child L2 names (the family's contents) |
| L0 Process Context (49) | own `cell_charter` (concerns, inclusions/exclusions/adjacent), `outcomes`, `scope`, `governance.roles`, the EXT-24 metrics register entries (KPI/KRI/KCI names in plain words), `definition` |

The CR-BP-233 §1 authoring contract applies unchanged (grounding, MECE, denylist, semantic containment, agent typing, idempotency), executed in 2 batches of 49, each mechanically verified before application.

## 2. The HUM blocking flip (gate [51])

- `conformance_result.py`: the [51] Human Readability entry changes `False` → `True` (blocking) with the invocation gaining `--strict`, annotated "BLOCKING since CR-BP-236 (all five waves landed; the blocking profile is 0 across 3,723 records, so strict fails only on NEWLY introduced provided-layer defects)".
- Posture registry (`check_conformance_posture_ext23.py`): the [51] CLASSIFICATION row's `reason` is updated to record the flip.
- At flip time the HUM report reads **0 findings corpus-wide** — verified in this PR's gate run before the flip lands.

## 3. Programme closure statement

With this CR, the nomenclature assessment's foundational requirement is met on all 3,723 records: **Part I** (identity card, In a Nutshell, Why It Matters, Where You'd Encounter It, Worked Example) renders authored human-relatable prose on every README; **Part II** remains the CI-generated canonical record under byte-identity. The metamodel companion CR (CR-BP-230 §4) remains enabled-but-deferred; the waves' authored content lives in YAML and flows through the generator, so any future schema/model alignment inherits it mechanically.

## 4. What does NOT change

- No canonical name, id, status, owner, charter, scope, or metrics changes — the five fields are additive documentation attributes.
- No other gate's logic or posture; the RDM/DOC machinery untouched.

## 5. Verification / Acceptance Criteria

1. HUM gate corpus-wide: **0 findings** (all seven rules × 3,723 records); the committed report shows `findings_total: 0`.
2. Gate [51] registered blocking and passing under `--strict` in `conformance_result.py`.
3. Schema validation green; RDM-001/002/003 CONFORMANT; all 3,723 Part I sections render authored prose (zero standing pointers in the corpus).
4. Driver idempotency: second run writes 0.
5. Full gate suite green; freshness procedure honoured.
