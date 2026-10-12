#!/usr/bin/env python3
"""Rename 4 CR-BP-111 activities whose entropy contains a forbidden char
(`1`, `0`, `l`, `o` per IDM-001 / IDM-004). The 4 affected activities
are 4 of the 20 Activities I authored for CR-BP-111; their auto-generated
6-char entropy slipped a `1` through.

For each activity:
  1. Generate a fresh 6-char entropy from the strict IDM-004 alphabet
     (`abcdefghjkmnpqrstuvwxyz23456789`).
  2. Rename the activity directory from `<old-slug>` to `<new-slug>`.
  3. Rename the activity yaml from `processes-activity-<old>.yaml` to
     `processes-activity-<new>.yaml`.
  4. Update the `id:` field inside the activity yaml.
  5. Update the parent BP's `metadata.activity_references` to use the new id.
  6. Rename all 5 nested Task directories under the activity.
  7. Update each Task's `id:` and `belongs_to_activity:` fields.
"""
import secrets
import shutil
from pathlib import Path

import yaml

ROOT = Path('entities/v1-alpha')
SAFE_ALPHABET = 'abcdefghjkmnpqrstuvwxyz23456789'

# Activities with bad entropies
AFFECTED = [
    'ao-build-f5k1m3',
    'ao-conceive-pzmwkl',
    'ao-improve-v3h8k1',
    'ao-operate-q3w6r1',
]


def fresh_entropy() -> str:
    return ''.join(secrets.choice(SAFE_ALPHABET) for _ in range(6))


def rename_activity(old_slug: str) -> str:
    new_entropy = fresh_entropy()
    new_slug = old_slug.rsplit('-', 1)[0] + '-' + new_entropy
    print(f'\n{old_slug} -> {new_slug}')

    # Find the activity dir
    act_dirs = list(ROOT.glob(f'*/*/*/{old_slug}'))
    if not act_dirs:
        print(f'WARN: activity dir not found: {old_slug}')
        return ''
    if len(act_dirs) > 1:
        print(f'WARN: multiple activity dirs match: {old_slug}: {act_dirs}')
        return ''
    act_dir = act_dirs[0]
    new_act_dir = act_dir.parent / new_slug
    # Step 1+2: rename dir
    shutil.move(str(act_dir), str(new_act_dir))
    # Step 3: rename the activity yaml
    old_yaml = new_act_dir / f'processes-activity-{old_slug}.yaml'
    new_yaml = new_act_dir / f'processes-activity-{new_slug}.yaml'
    if not old_yaml.exists():
        print(f'WARN: activity yaml not found: {old_yaml}')
    else:
        shutil.move(str(old_yaml), str(new_yaml))
        # Step 4: update id
        d = yaml.safe_load(new_yaml.read_text())
        old_id = d['id']
        d['id'] = f'processes:activity-{new_slug}'
        new_yaml.write_text(yaml.safe_dump(d, sort_keys=False, default_flow_style=False))
        print(f'  renamed yaml: {old_id} -> {d["id"]}')

    # Step 6: rename nested task dirs
    for task_dir in new_act_dir.iterdir():
        if not task_dir.is_dir():
            continue
        if not task_dir.name.startswith(old_slug.rsplit('-', 1)[0]):
            continue
        # task dir name: <domain>-<stage>-<old-activity-entropy>-<task-entropy>
        # extract the task entropy (last 6 chars)
        parts = task_dir.name.split('-')
        task_entropy = parts[-1]
        # check if task entropy is valid
        if any(c not in SAFE_ALPHABET for c in task_entropy):
            new_task_entropy = fresh_entropy()
            new_task_dir_name = '-'.join(parts[:-1] + [new_task_entropy])
            new_task_dir = new_act_dir / new_task_dir_name
            shutil.move(str(task_dir), str(new_task_dir))
            print(f'  renamed task dir: {task_dir.name} -> {new_task_dir_name}')
            task_dir = new_task_dir
        # Step 7: update task id and belongs_to_activity in the task yaml
        task_yamls = list(task_dir.glob('processes-task-*.yaml'))
        for ty in task_yamls:
            td = yaml.safe_load(ty.read_text())
            old_tid = td['id']
            td['id'] = f'processes:task-{new_slug}-{task_entropy}'
            td['belongs_to_activity'] = f'processes:activity-{new_slug}'
            ty.write_text(yaml.safe_dump(td, sort_keys=False, default_flow_style=False))
            print(f'    task: {old_tid} -> {td["id"]}')

    # Step 5: update parent BP's metadata.activity_references
    bp_dir = new_act_dir.parent
    bp_yamls = list(bp_dir.glob('processes-process-*.yaml'))
    if not bp_yamls:
        print(f'WARN: BP yaml not found in {bp_dir}')
    else:
        bp_yaml = bp_yamls[0]
        bd = yaml.safe_load(bp_yaml.read_text())
        refs = bd.get('metadata', {}).get('activity_references', [])
        new_refs = []
        for r in refs:
            if r == f'processes:activity-{old_slug}':
                new_refs.append(f'processes:activity-{new_slug}')
                print(f'  BP ref: {r} -> processes:activity-{new_slug}')
            else:
                new_refs.append(r)
        bd.setdefault('metadata', {})['activity_references'] = new_refs
        bp_yaml.write_text(yaml.safe_dump(bd, sort_keys=False, default_flow_style=False))

    # Update composes[] on the renamed activity to point at the renamed tasks
    if new_yaml.exists():
        ad = yaml.safe_load(new_yaml.read_text())
        if 'composes' in ad:
            for entry in ad['composes']:
                old_tgt = entry.get('target_id', '')
                # task id is now processes:task-<new_slug>-<task-entropy>
                # the entry's target_id was the old slug
                if old_tgt.startswith(f'processes:task-{old_slug}'):
                    # extract task entropy
                    parts = old_tgt.split('-')
                    task_entropy = parts[-1]
                    entry['target_id'] = f'processes:task-{new_slug}-{task_entropy}'
            new_yaml.write_text(yaml.safe_dump(ad, sort_keys=False, default_flow_style=False))

    return new_slug


def main():
    print('Renaming CR-BP-111 activities with bad entropies...')
    for old in AFFECTED:
        rename_activity(old)
    print('\nDone.')


if __name__ == '__main__':
    main()
