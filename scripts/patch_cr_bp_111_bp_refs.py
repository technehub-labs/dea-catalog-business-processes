#!/usr/bin/env python3
"""Patch the 5 A&O regulator-tied BP records to add metadata.activity_references
and a CR-BP-111 change_history entry. Patches the existing metadata block
in place (no wholesale rewrite).
"""
import re
from pathlib import Path

import yaml

# BP id -> 4 Activity ids
BPS = {
    'processes:process-ao-conceive-pnrhem': [
        'processes:activity-ao-conceive-cqkwrm',
        'processes:activity-ao-conceive-vnkqzf',
        'processes:activity-ao-conceive-fmxtqr',
        'processes:activity-ao-conceive-pzmwkl',
    ],
    'processes:process-ao-design-2fkvhx': [
        'processes:activity-ao-design-jbf2v9',
        'processes:activity-ao-design-wnqz3k',
        'processes:activity-ao-design-x9k4m7',
        'processes:activity-ao-design-v8r5n2',
    ],
    'processes:process-ao-build-9my4jr': [
        'processes:activity-ao-build-q7m3k9',
        'processes:activity-ao-build-w2n8p4',
        'processes:activity-ao-build-f5k1m3',
        'processes:activity-ao-build-r6h2t8',
    ],
    'processes:process-ao-operate-ba8scr': [
        'processes:activity-ao-operate-z4n9m2',
        'processes:activity-ao-operate-j8k5p7',
        'processes:activity-ao-operate-q3w6r1',
        'processes:activity-ao-operate-b5v2k9',
    ],
    'processes:process-ao-improve-qqxe4d': [
        'processes:activity-ao-improve-x7m4n2',
        'processes:activity-ao-improve-k9w5p8',
        'processes:activity-ao-improve-f2r6t4',
        'processes:activity-ao-improve-v3h8k1',
    ],
}

ROOT = Path('entities/v1-alpha')

for bp_id, acts in BPS.items():
    bp_slug = bp_id.replace('processes:process-', '')
    paths = list(ROOT.glob(f'*/*/processes-process-{bp_slug}.yaml'))
    if not paths:
        paths = list(ROOT.glob(f'*/*/*/processes-process-{bp_slug}.yaml'))
    if not paths:
        print(f'WARN: BP not found: {bp_id}')
        continue
    p = paths[0]
    text = p.read_text()
    # Replace the empty activity_references block with 4 ids
    new_refs = '\n'.join(f'  - {a}' for a in acts)
    new_text = re.sub(
        r'activity_references: \[\]',
        f'activity_references:\n{new_refs}',
        text,
    )
    if new_text == text:
        print(f'WARN: no activity_references block matched in {p}')
        continue
    # Append CR-BP-111 change_history entry
    cr_entry = """  - cr: CR-BP-111
    date: '2026-10-12'
    change: 'L3 decomposition tranche (CR-BP-111): added metadata.activity_references
      back-references to the 4 Activity records decomposing this BP. Version
      unchanged per SIV-004 (additive metadata-only). Activities classified
      per CR-BP-32 section 5 (fails standalone executability and resource
      dedication); decomposition boundary marker per CR-BP-32 section 12
      cleared (each Activity is decomposed into 5 L4 Tasks per the
      `scripts/decompose_l4.py` 5-phase verb-object completion pattern).'
"""
    # Insert before the first list-item `- cr: ...` of the change_history
    # Find the closing `]` of the change_history list -- easier: insert at end
    # We rely on the fact that change_history is the last key in metadata.
    # The cleanest spot is right before the closing `>` of the YAML file.
    # But many BP files end with a YAML scalar `---\n` or just `\n`.
    # Use a regex to find the last `^>` end-of-block line and insert before it.
    # Actually the file ends without a top-level `>`; instead, append at end.
    new_text = new_text.rstrip() + '\n' + cr_entry
    p.write_text(new_text)
    print(f'patched: {p}')

print('\nDone.')
