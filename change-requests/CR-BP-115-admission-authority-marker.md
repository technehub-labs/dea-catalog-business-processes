# CR-BP-115: Admission-Authority Marker (Data over Regex) and open_change_requests Count Fix

**Status**: Proposed (this PR)
**Layer**: Cross-cutting (catalog governance)
**Owner**: Coder (for eaojnr)
**Date**: 2026-10-13
**Depends on**: CR-BP-107 (admission-allowlist retro-fit precedent; CR-META normalization that made Merged a dead status value)
**Trigger**: User directive 2026-10-13, eaojnr: "Replace the admission allowlist regex with data; fix the duplicated condition in regenerate_catalog.py:466 while you're in there."
**Scope note**: the accompanying content-policy question (templated L4 Task generation) is explicitly excluded by the same directive; this CR takes only the two mechanical fixes.
**Carrier**: Single-PR, two moves: (a) replaces the hardcoded _ADMISSION_CR_RE allowlist in scripts/check_admission_gate.py (21 enumerated CR ids + a 45-line narrative comment with a verbatim-duplicated paragraph) with a machine-readable Admission-authority marker carried in the CR files themselves - the allowlist becomes derived data, and authoring an admission tranche and registering its authority collapse into the same edit; (b) fixes the duplicated condition at scripts/regenerate_catalog.py:466 ("Status**: Merged" in head or "Status**: Merged" in head), whose dead branch currently counts all 125 CR files as open, including the 33 Accepted ones.

Lands against: 1 validator (scripts/check_admission_gate.py); 1 generator (scripts/regenerate_catalog.py); 33 change-request files gain one metadata line each (the backfill manifest, §2); 2 new test modules; CHANGELOG + CATALOG.yaml regenerated (open_change_requests moves per §6). 0 entity-record changes. 0 id changes. 0 gate-count changes (ADM-001 semantics unchanged; the authority set is identical before and after).

1. Background and Authority
Two defects, one root pattern  -  governance state encoded in code instead of data:

The admission allowlist is a regex. check_admission_gate.py:303-306 hardcodes 21 CR ids as _ADMISSION_CR_RE; ADM-001 (blocking under --strict-provenance in CI) requires every L2 record's change_history to cite at least one of them. Each new admission tranche must extend the regex in a different file than the CR it lands  -  the proven failure mode: CR-BP-106 landed without the extension and needed the entire CR-BP-107 follow-on (cc35d905) to repair. The 45-line comment narrating every addition (lines ~257-302), including the CR-BP-80 paragraph pasted twice verbatim (lines 282-284 and 285-287), is the codebase recording that the design is wrong.
The open-CR counter has a dead branch. regenerate_catalog.py:466 reads if "Status**: Merged" in head or "Status**: Merged" in head:  -  both operands identical; the second was intended for a second closed status. Impact is not cosmetic: after CR-BP-107 normalized CR-BP-mv1's status from Merged to Accepted, no CR file carries Merged (that marker survives only in change-requests/README.md rows, which this function never reads). The closed branch never fires, so every file falls through to open: open_change_requests: 125 today counts 33 Accepted CRs and 2 Rejected/Superseded-class files as open. The published count has been wrong by ~27% for its entire history.
2. Current-State Inventory (frozen as the backfill manifest)
The regex, verbatim:


python
_ADMISSION_CR_RE = re.compile(
    r"^(?:CR-BP-13[a-z]?|CR-BP-19|CR-BP-20|CR-BP-21[a-z]?|CR-BP-03C|CR-BP-64|CR-BP-65|CR-BP-66|CR-BP-67|CR-BP-71|CR-BP-73|CR-BP-75|CR-BP-78|CR-BP-81|CR-BP-82|CR-BP-83|CR-BP-86|CR-BP-101|CR-BP-101a|CR-BP-106|CR-BP-111)(?:\.\d+)*$"
)
Applied to bare ids (CR-BP-13a) in change_history[].cr for L2 records only (the ADM-001 loop walks processes-process-*.yaml, check_admission_gate.py:350). Expanded to disk, the 21 bases match 33 CR files (completion suffix (?:\.\d+)* admits the 21a.1-21f.1 tranche completions). The frozen backfill manifest, derived mechanically from the regex  -  this exact list receives the marker in §3:

CR-BP-03C, CR-BP-101, CR-BP-101a, CR-BP-106, CR-BP-111, CR-BP-13, CR-BP-13a, CR-BP-13b, CR-BP-19, CR-BP-20, CR-BP-21a, CR-BP-21a.1, CR-BP-21b, CR-BP-21b.1, CR-BP-21c, CR-BP-21c.1, CR-BP-21d, CR-BP-21d.1, CR-BP-21e, CR-BP-21e.1, CR-BP-21f.1, CR-BP-64, CR-BP-65, CR-BP-66, CR-BP-67, CR-BP-71, CR-BP-73, CR-BP-75, CR-BP-78, CR-BP-81, CR-BP-82, CR-BP-83, CR-BP-86.

3. Design: the Admission-Authority Marker
Field spec. One optional metadata line in the CR file's header block:

    **Admission authority**: yes

Parenthetical qualifier permitted and encouraged: `**Admission authority**: yes (L2 admission tranche, 5 BPs, A&O regulator-tied)`.

Parsing rule (mirrors the _normalize_status precedent in check_cr_metadata.py): value is the trimmed token before the first (, case-insensitive compared to yes. Anything else is not an authority and is ignored silently  -  the marker is opt-in, never blocking. check_cr_metadata.py performs no unknown-field rejection (verified), so the new line does not trip CR-META-001..006; formal CR-META registration is deliberately deferred (§9).

Why a marker in the CR file, not a YAML allowlist. A data file in reconciliation/ would still be a second artifact to remember  -  the exact forget-mode that produced the CR-BP-106/107 incident, just relocated. The marker travels with the thing it describes: writing an admission tranche's CR and registering its authority become the same edit, in the same file, in the same PR. The CR file is already PR-review-governed, so the trust boundary is unchanged from the regex era.

Forward rule. The tranche-authoring checklist (already codified post-CR-BP-101 as "extend the allowlist in the same commit") becomes: mark the CR when you write it. The gate's --json output exposes the derived set for review (§4).

4. Gate Rewire  -  scripts/check_admission_gate.py
Specific changes:

Delete _ADMISSION_CR_RE (lines 303-306) and the entire 45-line narrative comment above it (lines ~257-302, including the duplicated CR-BP-80 paragraph). Replace with a five-line comment: authority = CR files carrying **Admission authority**: yes; marker introduced and 33-CR backfill performed by CR-BP-115.
Add _load_admission_authorities(root: Path) -> set[str]: walk change-requests/CR-*.md; derive the bare CR id from each filename by stripping the slug (same derivation check_cr_metadata.py uses for CR-META-006 filename↔id matching); parse the first-30-lines header for the marker per §3; return the set of ids. Computed once per run, cached in a module-level dict keyed by root.
ADM-001 check becomes exact membership: has_admission = any((e.get("cr") or "") in authorities for e in change_history). The (?:\.\d+)* completion-suffix magic is unnecessary  -  completion CRs exist as their own ids in the derived set, so CR-BP-21d.1 matches exactly.
--json output gains "admission_authorities": [sorted ids] so a PR's reviewers see the derived set without reading code.
--self-test updated: a synthetic marked CR admits a fixture record; an unmarked CR fails ADM-001; a malformed marker value (yes-ish, Yes ( truncation edge) is ignored, not crashed on.
New tests/test_check_reference_embargo.py-style module tests/test_check_admission_gate.py (this validator currently has none): marker parsing, id derivation from slug filenames, backfill-manifest equality (the 33 ids of §2, asserted against the live change-requests/ tree so a deleted marker fails CI), and CLI subprocess tests.
5. Fix  -  scripts/regenerate_catalog.py count_open_change_requests()
Before (lines ~462-479; the bug at 466):


python
head = "\n".join(text.splitlines()[:30])
if "Status**: Merged" in head or "Status**: Merged" in head:
    continue
if "Status**: Proposed" in head or "Status**: Draft" in head:
    open_count += 1
    continue
if "Status**:" in head:
    # Some other status (Accepted, Superseded, etc.): conservative: open.
    open_count += 1
    continue
open_count += 1
After:


python
CLOSED_STATUSES = ("Merged", "Accepted", "Rejected", "Superseded")
OPEN_STATUSES = ("Proposed", "Draft")

head = "\n".join(text.splitlines()[:30])
if any(f"Status**: {s}" in head for s in CLOSED_STATUSES):
    continue
if any(f"Status**: {s}" in head for s in OPEN_STATUSES):
    open_count += 1
    continue
if "Status**:" in head:
    open_count += 1
    warnings.append(f"{path.name}: unrecognized Status line counted as open")
    continue
open_count += 1
warnings.append(f"{path.name}: no Status line in first 30 lines counted as open")
Specifics: module-level constants (documented as aligned with check_cr_metadata.py's APPROVED_STATUSES minus Draft); the duplicated operand's intended value  -  Accepted  -  joins the closed set; Rejected/Superseded close as well (they are resolved, not open); substring matching continues to handle qualified variants (Proposed (this PR), Accepted (paperwork-only normalization)). The signature becomes count_open_change_requests(catalog_root: Path, warnings: list[str] | None = None); build_payload threads its all_warnings through so unrecognized or missing status lines surface in regeneration output instead of passing silently. The docstring's "whose status is not 'Merged'" is updated to name the closed set. New tests/test_regenerate_catalog_open_count.py: tmp_path fixtures covering each closed status, each open status, qualified variants, no-status file, and the warning emissions.

6. Impact Analysis
Authority set: unchanged. Derived-marker set == frozen regex set == the 33 ids of §2 (asserted by the backfill-equality test in §4.6). No record's ADM-001 verdict moves; --strict-provenance CI behavior is identical.
open_change_requests: 125 → 92 on current upstream main (91 files with Proposed-class status + 1 file with no status line in the first 30 lines stay open; 33 Accepted + any Rejected/Superseded flip closed). Each Proposed carrier landing in the same window adds +1. This is a one-time step correction, not a regression  -  the published count has never excluded closed CRs.
Coupling: none. Verified by sweep: no test, gate, or schema pins the allowlist regex, the count value, or count_open_change_requests (catalog-index-schema requires the counts block's presence, not its values; historical CHANGELOG/README rows quoting old counts are history and untouched).
7. Conformance + Test Posture
python3 scripts/check_admission_gate.py --strict-provenance → CONFORMANT, identical findings to pre-change (authority set unchanged).
--self-test PASS for both touched scripts.
python3 scripts/conformance_result.py → CONFORMANT; gate count unchanged (this CR rewires an existing gate, adds none).
New tests: tests/test_check_admission_gate.py, tests/test_regenerate_catalog_open_count.py  -  0 failures.
8. CATALOG.yaml Posture
Regenerated in the same PR: open_change_requests 125 → ~92 (§6; exact value re-derived at land time from the live CR tree). All other counts, paths, and states unchanged (no entity files touched). Per the house fix(catalog) commit pattern.

9. NOT-List (Out of Scope)
No L4 content-policy change. Per the user directive, the "stop generating filler Tasks" question (templated definition/trigger/outcome content on 2,900 Tasks) is excluded; this CR is the two mechanical fixes only.
No CR status-hygiene sweep. 87+ CRs whose content landed remain Status: Proposed; flipping them to Accepted is a separate governance slice. Noted interaction: after §5, open_change_requests becomes a meaningful signal, which is what makes that hygiene slice worth doing later.
No CR-META-007 registration. The marker is parsed by the admission gate alone; formally adding it to check_cr_metadata.py's optional-field set is deferred until a second consumer exists.
No restructuring of ADM-002..008. Only the ADM-001 authority mechanism changes.
10. Acceptance Criteria
grep -n "_ADMISSION_CR_RE" scripts/check_admission_gate.py returns nothing; the 45-line comment block (incl. the duplicated CR-BP-80 paragraph) is deleted.
All 33 manifest CRs (§2) carry **Admission authority**: yes; check_admission_gate.py --json lists exactly those 33 ids as admission_authorities.
check_admission_gate.py --strict-provenance CONFORMANT with findings identical to pre-change; --self-test PASS.
tests/test_check_admission_gate.py backfill-equality assertion (derived set == the 33 live manifest ids) passes  -  deleting a marker fails CI.
regenerate_catalog.py contains no duplicated condition; CLOSED_STATUSES/OPEN_STATUSES constants present; Accepted/Rejected/Superseded count closed.
count_open_change_requests unit tests cover every status class, qualified variants, the no-status file, and warning emission; all pass.
Regenerated CATALOG.yaml shows open_change_requests equal to the live count of open-status CR files (≈92 on current main; ±carriers), and no other moved counts.
CHANGELOG.md carries a ## [Unreleased] entry for CR-BP-115.
11. Result
The last two pieces of governance state that lived in code move into the artifacts they govern: admission authority is declared by the CR that carries it (one edit, one file  -  the CR-BP-106 class of incident becomes structurally impossible), and open_change_requests reports a number that means something. The validator loses 50 lines and gains a test suite; the generator loses a bug that has silently inflated the catalog's headline open-work figure since the first regeneration.

35
