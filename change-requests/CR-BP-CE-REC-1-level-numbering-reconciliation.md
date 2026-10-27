# CR-BP-CE-REC-1: Umbrella CR Level-Numbering Reconciliation

**Status**: Proposed
**Layer**: Process Catalog (Cross-Cutting Documentation)
**Owner**: Emmanuel A. Otchere
**Depends on**: CR-BP-CE-0
**Companion to**: CR-BP-CE-L0, CR-BP-CE-L1, CR-BP-CE-L2, CR-BP-CE-L4

> **Scope.** The umbrella CR `CR-BP-CE-0-completeness-profiles.md` currently
> exists on `main` in its pre-reconciliation draft form (re-landed by
> PR #205), which numbers the levels **L1..L4**. The landed programme
> artefacts — the gate (`scripts/check_completeness.py` rule ids
> CE-L0-001..CE-L4-002), the four tranche CRs (CR-BP-CE-L0/L1/L2/L4), the
> S16 filename pattern, and the tranche registrations — all use the
> **canonical L0..L4** model per the CR-BP-CE-0 §R1 reconciliation
> (originally landed via PR #201). This CR reconciles the umbrella text to
> the canonical numbering so the programme's documents read consistently.
> **No normative content changes**: every profile row, rule, and tranche
> statement in the draft is preserved; only the level labels, the stale
> record counts, and the internal rule-id references are corrected.

---

## 1. The mapping (normative)

| Draft label | Draft population | Canonical label | Actual population |
|---|---|---|---|
| L1 — Process Context | 49 | **L0 — Process Context** | 49 |
| L2 — Process Group | 49 | **L1 — Process Group** | 49 |
| L3 — Business Process | 140 | **L2 — Business Process** | 145 (post-CR-BP-106) |
| L4 — Activity (560) / Task (2,800) | 3,360 | **L3 — Activity (580)** / **L4 — Task (2,900)** | 3,480 |

The draft's population counts predate the CR-BP-106 regulator-tied
admission tranche (+5 BPs, +20 Activities, +100 Tasks) and the
CR-BP-101 SD-Retire admission (+1 Activity +5 Tasks); both are reflected
in the canonical counts above and in the live completeness report.

## 2. What changes in the umbrella CR (§3/§4/§6 of the draft text)

1. **§3 profile headings**: `L1 — Process Context` -> `L0 — Process
   Context`; `L2 — Process Group` -> `L1 — Process Group`; `L3 — Business
   Process` -> `L2 — Business Process`; `L4 — Activity/Task` -> `L3 —
   Activity` + `L4 — Task` (the gate profile already treats them
   separately).
2. **Internal rule-id references**: `CE-L1-003` -> `CE-L0-003`;
   `CE-L1-004` -> `CE-L0-004`; `CE-L1-005` -> `CE-L0-005`;
   `CE-L2-002` -> `CE-L1-001`-family (group required fields);
   `CE-L3-006` -> `CE-L2-006`; `CE-L4-002` -> `CE-L4-002` (already
   canonical: the Task responsibility vocabulary rule).
3. **§6 tranche sequence**: relabelled to the landed CR names
   (CR-BP-CE-L0 -> L1 -> L2 -> L4; all four MERGED with their PR numbers),
   with the CR-BP-CE-RL gate-posture step remaining open pending the
   governance sweep.
4. **Population counts** updated to the live figures (145 / 580 / 2,900;
   catalogue total 3,723).
5. The **`type`/`version`-on-L1-PCs** note is relabelled
   `type`/`version`-on-L0-PCs (the reaffirmed deliberate omissions are
   unchanged in substance).

## 3. What is NOT changed

- No profile requirement, prohibition, or severity changes.
- No gate code, rule id, schema, record, or template changes — the gate
  already implements the canonical numbering; only the umbrella document
  drifts.
- The pilot contribution `contributions/processes/ce-l1-eo-operate.yaml`
  (landed by #205 under the draft numbering) is NOT renamed: its target is
  a L0 ProcessContext record, the file is a historical artefact of the
  pilot, and renaming would churn provenance for no normative gain. Its
  `cr:` reference resolves unchanged.

## 4. Verification

- `python scripts/check_cr_metadata.py --strict` — CONFORMANT (the S16
  header is preserved).
- `python scripts/check_cr_readme.py --strict` — CONFORMANT.
- `python scripts/check_completeness.py` — unchanged verdict (0 blocking,
  290 advisory); the gate is untouched.

## 5. Next steps

1. **CR-BP-CE-RL** — the gate-posture flip, once the CE-L2-006 governance
   sweep (actors/stakeholders; owner confirmations) closes.

**D-004 clean.**
