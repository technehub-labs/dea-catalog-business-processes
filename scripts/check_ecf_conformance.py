"""ECF conformance gate for technehub-labs/dea-catalog-processes.

Validates, per CR-ECF-CG-001..004:
  1. block presence on every catalog entry (when entries exist);
  2. framework + contractVersion + profile + status fields;
  3. canonicalReferences resolve to canonical PascalCase Domain/Stage enums;
  4. identifier matches the canonical lowerCamelCase pattern
     (^ecf:[a-z][a-zA-Z0-9]*\\.[a-z][a-zA-Z0-9]*$);
  5. held-unmapped state documented with rationaleRef;
  6. process_audience (kebab-case) does NOT leak into canonicalReferences
     (governance decision CG-004 §10: it is a separate semantic axis);
  7. extensions carry doesNotRedefine.

Exit code: 0 on full pass, 1 on any failure. Designed for GitHub Actions.

When entities/ is empty (Phase 2 deferred), the script reports and exits 0:
the catalog cannot declare per-entry conformance until entries exist, but the
schema-level declaration (dea:ecf@1.0.0 + status=not-yet-assessed) is what
matters for the gate's matrix view.
"""

from __future__ import annotations
import glob, os, re, sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
ENT = REPO / 'entities'
CONTRACT_VERSION = '1.0.0'
PROFILE = 'dea:ecf@1.0.0'
FRAMEWORK = 'EnterpriseConceptFramework'
CANON_DOMAINS = {
    'GovernanceAndExistence', 'StrategyAndDirection', 'AgencyAndOrganization',
    'PartyAndRelationship', 'ProductAndValue', 'EnablementAndOperations',
    'FinanceAndAccounting',
}
CANON_STAGES = {'Conceive', 'Design', 'Build', 'Activate', 'Operate', 'Improve', 'Retire'}
ID_PATTERN = re.compile(r'^ecf:[a-z][a-zA-Z0-9]*\.[a-z][a-zA-Z0-9]*$')
STATUSES = {'conformant', 'conformant-with-extension', 'non-conformant', 'not-yet-assessed'}
KABAB_DOMAINS = {
    'governance-existence', 'strategy-direction', 'agency-organization',
    'party-relationship', 'product-value', 'enablement-operations', 'finance-accounting',
}


def check_entry(e: dict, fp: str, errors: list):
    cid = e.get('id') or fp
    # CR-BP-mv1: L0 Process Context records are the coordinate anchors; they
    # carry their ECF coordinate as top-level `domain` + `lifecycle_stage`
    # fields rather than an ecfConformance block (they ARE the coordinate).
    if isinstance(cid, str) and cid.startswith("processes:pc-"):
        d = e.get('domain')
        s = e.get('lifecycle_stage')
        if d not in CANON_DOMAINS:
            errors.append(f"{cid}: pc domain '{d}' not a canonical ECF domain")
        if s not in CANON_STAGES:
            errors.append(f"{cid}: pc lifecycle_stage '{s}' not a canonical ECF stage")
        return
    blk = e.get('ecfConformance')
    if blk is None:
        errors.append(f"{cid}: missing ecfConformance block")
        return
    for k in ('framework', 'contractVersion', 'profile', 'status', 'affiliation'):
        if k not in blk:
            errors.append(f"{cid}: ecfConformance missing field '{k}'")
    if blk.get('framework') != FRAMEWORK:
        errors.append(f"{cid}: framework '{blk.get('framework')}' != canonical '{FRAMEWORK}'")
    if blk.get('contractVersion') != CONTRACT_VERSION:
        errors.append(f"{cid}: contractVersion '{blk.get('contractVersion')}' != '{CONTRACT_VERSION}'")
    if blk.get('profile') != PROFILE:
        errors.append(f"{cid}: profile '{blk.get('profile')}' != '{PROFILE}'")
    if blk.get('status') not in STATUSES:
        errors.append(f"{cid}: status '{blk.get('status')}' not in {STATUSES}")

    aff = blk.get('affiliation')
    if aff == 'held-unmapped':
        if not blk.get('rationaleRef'):
            errors.append(f"{cid}: held-unmapped missing rationaleRef")
        if blk.get('canonicalReferences'):
            errors.append(f"{cid}: held-unmapped must have empty canonicalReferences")
        return
    if aff not in ('mapped', 'inherits-catalog'):
        errors.append(f"{cid}: affiliation '{aff}' must be 'mapped', 'held-unmapped', or 'inherits-catalog'")

    # CG-004 §10 governance check: process_audience (kebab-case internal field)
    # must NOT appear inside canonicalReferences as a value. canonicalReferences
    # must contain canonical PascalCase enum values.
    pa = e.get('process_audience')
    for ref in blk.get('canonicalReferences') or []:
        if ref.get('kind') != 'coordinate':
            errors.append(f"{cid}: reference kind '{ref.get('kind')}' not 'coordinate'")
            continue
        d = ref.get('domain')
        s = ref.get('stage')
        if d not in CANON_DOMAINS:
            # explicit gate: kebab is rejected in canonicalReferences
            if d in KABAB_DOMAINS:
                errors.append(f"{cid}: canonical reference domain '{d}' is kebab-case; CG-004 §10 forbids collapsing process_audience into ECF Domain")
            else:
                errors.append(f"{cid}: canonical reference domain '{d}' not in canonical enum")
        if s not in CANON_STAGES:
            errors.append(f"{cid}: canonical reference stage '{s}' not in canonical enum")
        ident = ref.get('identifier') or ''
        if not ID_PATTERN.match(ident):
            errors.append(f"{cid}: identifier '{ident}' does not match canonical pattern")

    for ext in blk.get('extensions') or []:
        if 'doesNotRedefine' not in ext:
            errors.append(f"{cid}: extension '{ext.get('name')}' missing doesNotRedefine")
        if ext.get('doesNotRedefine') is False:
            errors.append(f"{cid}: extension '{ext.get('name')}' doesNotRedefine=false is prohibited by CG-001")

    # record-level: process_audience presence is required by schema, but
    # the value is kebab-case by design and is NOT a canonical ECF reference.
    if pa and pa not in KABAB_DOMAINS:
        errors.append(f"{cid}: process_audience '{pa}' not in kebab-case enum")


def main():
    files = sorted(glob.glob(str(ENT / '**' / '*.yaml'), recursive=True))
    # Skip non-entry files: READMEs (subtree index docs) and any YAML
    # living under a per-entity state directory (research/, candidates/,
    # retired/) per CR-CATALOG-STRUCT-01 §5. State-directory files are
    # research/candidate/retired artifacts, not catalog entries; they are
    # not required to carry the ecfConformance block.
    def is_state_dir_file(path: str) -> bool:
        parts = Path(path).parts
        return any(p in ('research', 'candidates', 'retired') for p in parts)

    files = [
        f for f in files
        if '/README' not in f and '/readme' not in f
        and not is_state_dir_file(f)
    ]
    if not files:
        print(f"PASS (no entries to validate; Phase 2 not started). Schema-level declaration enforced via CI: validate-entries job.")
        return
    errors: list[str] = []
    for fp in files:
        try:
            e = yaml.safe_load(open(fp))
        except yaml.YAMLError as ex:
            errors.append(f"{fp}: YAML parse error: {ex}")
            continue
        if not e:
            errors.append(f"{fp}: empty document")
            continue
        check_entry(e, fp, errors)
    if errors:
        print(f"FAIL: {len(errors)} conformance error(s):", file=sys.stderr)
        for e in errors:
            print(' -', e, file=sys.stderr)
        sys.exit(1)
    print(f"PASS: {len(files)} entries conform to ECF Conformance Gate.")


if __name__ == '__main__':
    main()