#!/usr/bin/env python3
"""
_entity_walk.py
CR-BP-mv1: shared canonical-record walker for the L0-rooted containment tree.

Every validator / generator / build script that previously globbed the flat
`entities/v1-alpha/dea:*` layout now walks the tree via these helpers.
Filenames are id-derived (`processes-<level>-...yaml`) so level filtering
is a filename-prefix match; PCs are the only records without a `type:` field
so the filename prefix is also the discriminator there.
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTITIES = ROOT / "entities" / "v1-alpha"

LEVEL_FILE_PREFIX = {
    "pc": "processes-pc-",
    "group": "processes-group-",
    "process": "processes-process-",
    "activity": "processes-activity-",
    "task": "processes-task-",
}


def walk_level(level: str, root: Path | None = None):
    """Yield (path, record) for every canonical record of the given level.

    level is one of: pc, group, process, activity, task.
    """
    base = root or ENTITIES
    prefix = LEVEL_FILE_PREFIX[level]
    for p in sorted(base.rglob(f"{prefix}*.yaml")):
        with p.open() as f:
            yield p, yaml.safe_load(f)


def walk_all(root: Path | None = None):
    """Yield (path, record, level) for every canonical record in the tree."""
    for level in ("pc", "group", "process", "activity", "task"):
        for p, rec in walk_level(level, root):
            yield p, rec, level


def iter_entity_dirs(level: str, root: Path | None = None):
    """Yield the per-record directories for a level (task/activity/process/group
    records live in their own dirs; pc records are flat files at cell level)."""
    for p, _ in walk_level(level, root):
        yield p.parent if level != "pc" else p.parent
