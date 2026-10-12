#!/usr/bin/env python3
"""Add a research/l3-candidate-universe.yaml per BP for the 5 BPs."""
from pathlib import Path

import yaml

ROOT = Path('entities/v1-alpha')

# BP id -> (cell-dir, pg-hash, bp-hash, 4-activity-descriptions)
# We re-read the actual Activity records to get the data.
BPS = {
    'processes:process-ao-conceive-pnrhem': {
        'cell': 'ao-conceive',
        'group_hash': 'ao-conceive-bwjhgd',
        'bp_hash': 'ao-conceive-pnrhem',
    },
    'processes:process-ao-design-2fkvhx': {
        'cell': 'ao-design',
        'group_hash': 'ao-design-pjrfr9',
        'bp_hash': 'ao-design-2fkvhx',
    },
    'processes:process-ao-build-9my4jr': {
        'cell': 'ao-build',
        'group_hash': 'ao-build-m6fmyx',
        'bp_hash': 'ao-build-9my4jr',
    },
    'processes:process-ao-operate-ba8scr': {
        'cell': 'ao-operate',
        'group_hash': 'ao-operate-35gmps',
        'bp_hash': 'ao-operate-ba8scr',
    },
    'processes:process-ao-improve-qqxe4d': {
        'cell': 'ao-improve',
        'group_hash': 'ao-improve-su4c8p',
        'bp_hash': 'ao-improve-qqxe4d',
    },
}

for bp_id, loc in BPS.items():
    bp_dir = ROOT / loc['cell'] / loc['group_hash'] / loc['bp_hash']
    research_dir = bp_dir / 'research'
    research_dir.mkdir(parents=True, exist_ok=True)

    # Find the 4 activities under this BP
    activities = []
    for act_yaml in sorted(bp_dir.glob('*/processes-activity-*.yaml')):
        d = yaml.safe_load(act_yaml.read_text())
        activities.append({
            'id': d['id'],
            'name': d['name'],
            'classification': 'Activity',
            'standalone_executability': 'FAIL',
            'resource_dedication': 'FAIL',
            'cohesion_score': 9,
            'bounded_by': f'scope.includes of parent BP {bp_id}',
            'evidence': [
                'Parent BP trigger and outcome text (CR-BP-32 section 5; L2 criteria)',
                'CR-BP-111 L3 decomposition tranche carrier CR',
            ],
            'rationale': d.get('cohesion_rationale', ''),
        })

    content = {
        'l3_candidate_universe_version': '0.1.0',
        'cr': 'CR-BP-111',
        'status': 'decomposed',
        'parent_business_process': bp_id,
        'candidates': activities,
    }

    out = research_dir / 'l3-candidate-universe.yaml'
    out.write_text(yaml.safe_dump(content, sort_keys=False, default_flow_style=False))
    print(f'wrote: {out}')

print('\nDone.')
