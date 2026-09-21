#!/usr/bin/env python3
"""Resolve PR#148-vs-migration merge conflicts in Task YAMLs.

Shape: ours = migration (new ids/structure), theirs = CR-BP-L4-03 enrichment
(rich content, old ids). Splice theirs' content region (definition..evidence)
into ours' skeleton, keep ours' id/belongs_to_activity, rewrite old ids in the
spliced region via reconciliation/migration-id-map.yaml.
"""
import re
import subprocess
import sys

import yaml

ROOT = "/home/hermes/dea-catalog-processes"

id_map = yaml.safe_load(open(f"{ROOT}/reconciliation/migration-id-map.yaml"))["id_map"]

# longest-first so prefix-collisions resolve correctly
old_ids = sorted(id_map, key=len, reverse=True)
pat = re.compile(r"\b(dea:(?:activity|task|process|group|pc)-[a-z0-9-]+)\b")

unmapped = {}


def rewrite(text):
    def rep(m):
        old = m.group(1)
        new = id_map.get(old)
        if new is None:
            unmapped[old] = unmapped.get(old, 0) + 1
            return old
        return new
    return pat.sub(rep, text)


conflicted = subprocess.run(
    ["git", "diff", "--name-only", "--diff-filter=U"],
    cwd=ROOT, capture_output=True, text=True, check=True,
).stdout.split()

tasks = [p for p in conflicted if p.startswith("entities/") and p.endswith(".yaml")]
other = [p for p in conflicted if p not in tasks]
print(f"conflicted: {len(conflicted)} total, {len(tasks)} task files, other: {other}")

REGION_START = "definition:"
REGION_END = "version:"          # first top-level 'version:' after evidence
KEEP_LINE = "belongs_to_activity:"

ok = fail = 0
failures = []
for path in tasks:
    ours = subprocess.run(["git", "show", f":2:{path}"], cwd=ROOT,
                          capture_output=True, text=True).stdout.splitlines()
    theirs = subprocess.run(["git", "show", f":3:{path}"], cwd=ROOT,
                            capture_output=True, text=True).stdout.splitlines()

    def region(lines):
        try:
            i = next(n for n, l in enumerate(lines) if l.startswith(REGION_START))
            j = next(n for n, l in enumerate(lines)
                     if n > i and l.startswith(REGION_END))
        except StopIteration:
            return None
        keep = [l for l in lines[i:j] if l.startswith(KEEP_LINE)]
        return i, j, keep

    ro = region(ours)
    rt = region(theirs)
    if not ro or not rt or len(ro[2]) != 1 or len(rt[2]) != 1:
        fail += 1
        failures.append(path)
        continue

    splice = [ro[2][0] if l.startswith(KEEP_LINE) else l
              for l in theirs[rt[0]:rt[1]]]
    splice = [rewrite(l) for l in splice]
    merged = "\n".join(ours[:ro[0]] + splice + ours[ro[1]:]) + "\n"
    with open(f"{ROOT}/{path}", "w") as f:
        f.write(merged)
    ok += 1

print(f"spliced OK: {ok}, skeleton failures: {fail}")
for p in failures[:10]:
    print("  FAIL:", p)
if unmapped:
    print("UNMAPPED old ids left in spliced content:")
    for k, v in sorted(unmapped.items()):
        print(f"  {k} x{v}")
sys.exit(1 if fail else 0)
