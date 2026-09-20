#!/usr/bin/env python3
"""
check_l0_l1_cardinality.py :  L0 (ProcessContext) <-> L1 (ProcessGroup) cardinality gate.

Implements CR-BP-100 rules L0L1-CARD-001..003.

Doctrine (eaojnr 2026-09-19): the L0 layer is the Process Context matrix
(processes:pc-*) and is already canonical; the L1 layer is the
Process Group records (entities/v1-alpha/dea:group-*). The canonical
cardinality is exactly one L1 Process Group per L0 Process Context (1:1)
and exactly one L0 Process Context per L1 Process Group (1:1). This
invariants is enforced by admission tranches (CR-BP-13a, CR-BP-71, CR-BP-73,
CR-BP-75, CR-BP-78, CR-BP-81) but has never been codified as an automated
gate. CR-BP-100 lands it as advisory gate [24].

Rules:
  L0L1-CARD-001 :  Every Process Context has exactly one Process Group.
                  Builds a (process_context -> [group_ids]) map from
                  entities/v1-alpha/dea:group-*/*.yaml and asserts each
                  known dea:pc-* has exactly one composed L1 group.
                  Cells with 0 groups OR >1 groups fail.
  L0L1-CARD-002 :  Every Process Group references exactly one Process Context.
                  Builds a (group_id -> process_context) map from
                  entities/v1-alpha/dea:group-*/*.yaml and asserts each
                  declared process_context resolves to a known PC in
                  tree. PG records whose process_context
                  is missing, malformed, or unknown fail.
  L0L1-CARD-003 :  ProcessScope (dea:scope-*) is uninstantiated by design.
                  Asserts that the entities tree contains zero ProcessScope
                  records. This is a deliberate non-event: CR-BP-95 introduced
                  the schema + validator as a forward-compatibility surface;
                  CR-BP-100 (this gate) declares the layer dormant because
                  the L0 layer IS the Process Context matrix. If a future
                  slice admits a ProcessScope record, this gate flips to
                  finding, prompting the slice to justify the duplication.

Exit: 0 = all rules pass (or no entities tree); 2 = self-test; 1 = at least
      one rule failed.

CR-BP-100 design note: gate is wired **advisory** initially because the
cardinality is currently 1:1 by data and the historical record shows that
admission tranches enforce the discipline. Promoting to blocking requires
2+ release cycles with the advisory gate producing zero findings.
"""
import argparse
import re
import sys
import tempfile
from pathlib import Path

import yaml

ID_PC_PATTERN = re.compile(r"^processes:pc-[a-z0-9-]+$")
ID_GROUP_PATTERN = re.compile(r"^processes:group-[a-z0-9-]+$")
ID_SCOPE_PATTERN = re.compile(r"^dea:scope-[a-z0-9-]+$")


def _load_pc_ids(entities_dir: Path) -> set[str]:
    """Load all canonical Process Context ids (CR-BP-mv1 containment tree)."""
    ids: set[str] = set()
    if not entities_dir.exists():
        return ids
    for path in sorted(entities_dir.rglob("processes-pc-*.yaml")):
        if path.name == "README.md":
            continue
        try:
            data = yaml.safe_load(path.read_text()) or {}
        except yaml.YAMLError:
            continue
        cid = data.get("id")
        if isinstance(cid, str) and ID_PC_PATTERN.match(cid):
            ids.add(cid)
    return ids


def _load_pgs(entities_dir: Path) -> tuple[list[dict], list[dict]]:
    """Load all Process Group + ProcessScope records from entities/v1-alpha/.

    Returns (group_records, scope_records). Documentation, examples, and
    non-conforming entries are skipped.
    """
    groups: list[dict] = []
    scopes: list[dict] = []
    if not entities_dir.exists():
        return groups, scopes
    for path in sorted(entities_dir.rglob("*.yaml")):
        if "/documentation/" in path.as_posix():
            continue
        if "/examples/" in path.as_posix():
            continue
        try:
            data = yaml.safe_load(path.read_text()) or {}
        except yaml.YAMLError:
            continue
        if not isinstance(data, dict):
            continue
        t = data.get("type")
        gid = data.get("id", "")
        if t == "ProcessGroup" and isinstance(gid, str) and ID_GROUP_PATTERN.match(gid):
            groups.append(data)
        elif t == "ProcessScope" and isinstance(gid, str) and ID_SCOPE_PATTERN.match(gid):
            scopes.append(data)
    return groups, scopes


def _check_cardinality(
    *,
    pc_ids: set[str],
    group_records: list[dict],
    scope_records: list[dict],
    errors: list[str],
) -> None:
    # L0L1-CARD-001 :  every PC has exactly one PG.
    by_pc: dict[str, list[str]] = {}
    for grp in group_records:
        pc = grp.get("process_context", "")
        gid = grp.get("id", "<unknown>")
        if not isinstance(pc, str) or not ID_PC_PATTERN.match(pc):
            # L0L1-CARD-002 will catch this; skip.
            continue
        by_pc.setdefault(pc, []).append(gid)

    for pc_id in sorted(pc_ids):
        groups = by_pc.get(pc_id, [])
        if len(groups) == 0:
            errors.append(
                f"L0L1-CARD-001 ({pc_id}): Process Context has 0 Process Groups. "
                f"Canonical cardinality is exactly 1 L1 Process Group per L0 "
                f"Process Context (eaojnr 2026-09-19; CR-BP-100)."
            )
        elif len(groups) > 1:
            errors.append(
                f"L0L1-CARD-001 ({pc_id}): Process Context has {len(groups)} "
                f"Process Groups ({sorted(groups)}). Canonical cardinality is "
                f"exactly 1 L1 Process Group per L0 Process Context "
                f"(eaojnr 2026-09-19; CR-BP-100). Multi-PG cells violate the "
                f"CR-BP-02 §22 admission discipline and require a dedicated CR."
            )

    # Detect PGs whose process_context references an unknown or absent PC.
    # This is L0L1-CARD-002.
    for grp in group_records:
        gid = grp.get("id", "<unknown>")
        pc = grp.get("process_context", "")
        if not isinstance(pc, str) or not ID_PC_PATTERN.match(pc):
            errors.append(
                f"L0L1-CARD-002 ({gid}): process_context={pc!r} is missing or "
                f"does not match `^dea:pc-[a-z0-9-]+$`."
            )
            continue
        if pc_ids and pc not in pc_ids:
            errors.append(
                f"L0L1-CARD-002 ({gid}): process_context={pc!r} does not resolve "
                f"to a canonical Process Context in the containment tree. "
                f"Known contexts: {len(pc_ids)} entries."
            )

    # L0L1-CARD-003 :  ProcessScope is uninstantiated by design.
    if scope_records:
        scope_ids = [s.get("id", "<unknown>") for s in scope_records]
        errors.append(
            f"L0L1-CARD-003: ProcessScope layer is dormant by design (CR-BP-100; "
            f"eaojnr 2026-09-19 doctrine: L0 layer IS the Process Context matrix). "
            f"Found {len(scope_records)} ProcessScope records: {scope_ids}. "
            f"Admitting a ProcessScope record requires an explicit CR justifying "
            f"why the L0 layer is no longer identical to the Process Context matrix."
        )


def run_checks(catalog_root: Path) -> tuple[list[str], list[dict]]:
    errors: list[str] = []
    suggestions: list[dict] = []

    entities_dir = catalog_root / "entities" / "v1-alpha"
    entities_dir = catalog_root / "entities" / "v1-alpha"

    pc_ids = _load_pc_ids(entities_dir)
    group_records, scope_records = _load_pgs(entities_dir)

    if not entities_dir.exists():
        print(
            "L0<->L1 cardinality (CR-BP-100; L0L1-CARD-001..003): PASS "
            "(no entities/ directory; self-test fixture scope)."
        )
        return errors, suggestions

    _check_cardinality(
        pc_ids=pc_ids,
        group_records=group_records,
        scope_records=scope_records,
        errors=errors,
    )

    return errors, suggestions


def self_test() -> int:
    """Exercise L0L1-CARD-001..003 on deliberately broken + fixed catalogs."""
    with tempfile.TemporaryDirectory(prefix="l0l1_card_self_test_") as tmp:
        tmp_path = Path(tmp)
        ent_dir = tmp_path / "entities" / "v1-alpha"
        ent_dir.mkdir(parents=True)

        def _reset() -> None:
            for p in ent_dir.rglob("*.yaml"):
                p.unlink()

        def _write_pc(pc_id: str, name: str) -> None:
            fname = pc_id.replace(":", "-") + ".yaml"
            (ent_dir / fname).write_text(
                f"id: {pc_id}\ntype: ProcessContext\nname: {name}\nversion: 1.0.0\n",
                encoding="utf-8",
            )

        def _write_pg(gid: str, pc_id: str) -> None:
            fname = gid.replace(":", "-") + ".yaml"
            (ent_dir / fname).write_text(
                f"id: {gid}\ntype: ProcessGroup\nname: {gid}\nversion: 1.0.0\n"
                f"process_context: {pc_id}\nprocess_group_kind: functional\n"
                f"status: active\nlifecycle_status: active\n",
                encoding="utf-8",
            )

        def _write_scope(sid: str) -> None:
            fname = sid.replace(":", "-") + ".yaml"
            (ent_dir / fname).write_text(
                f"id: {sid}\ntype: ProcessScope\nname: {sid}\nversion: 1.0.0\n",
                encoding="utf-8",
            )

        # --- Scenario 1: clean (1 PC, 1 PG). expect PASS.
        _reset()
        _write_pc("processes:pc-a", "A")
        _write_pg("processes:group-a1", "processes:pc-a")
        errs, _ = run_checks(tmp_path)
        if errs:
            print("L0L1-CARD self-test: expected clean pass on 1:1 catalog; got:")
            for e in errs:
                print(f"  {e}")
            return 2

        # --- Scenario 2: 0 PG in dea:pc-b. expect CARD-001 failure.
        _reset()
        _write_pc("processes:pc-a", "A")
        _write_pc("processes:pc-b", "B")
        _write_pg("processes:group-b1", "processes:pc-b")
        errs, _ = run_checks(tmp_path)
        if not any("L0L1-CARD-001" in e and "processes:pc-a" in e for e in errs):
            print("L0L1-CARD self-test: expected CARD-001 (dea:pc-a orphan) but got:")
            for e in errs:
                print(f"  {e}")
            return 2

        # --- Scenario 3: 2 PG under dea:pc-a. expect CARD-001 failure (many).
        _reset()
        _write_pc("processes:pc-a", "A")
        _write_pg("processes:group-a1", "processes:pc-a")
        _write_pg("processes:group-a2", "processes:pc-a")
        errs, _ = run_checks(tmp_path)
        if not any("L0L1-CARD-001" in e and "2 Process Groups" in e and "processes:pc-a" in e for e in errs):
            print("L0L1-CARD self-test: expected CARD-001 (dea:pc-a multi-PG) but got:")
            for e in errs:
                print(f"  {e}")
            return 2

        # --- Scenario 4: PG with unknown PC. expect CARD-002 failure.
        _reset()
        _write_pc("processes:pc-a", "A")
        _write_pg("processes:group-bad", "processes:pc-unknown")
        errs, _ = run_checks(tmp_path)
        if not any("L0L1-CARD-002" in e and "processes:group-bad" in e for e in errs):
            print("L0L1-CARD self-test: expected CARD-002 (dea:group-bad unknown PC) but got:")
            for e in errs:
                print(f"  {e}")
            return 2

        # --- Scenario 4b: PG with malformed process_context. expect CARD-002 failure.
        _reset()
        _write_pc("processes:pc-a", "A")
        _write_pg("processes:group-bad", "processes:pc-")
        # The id pattern requires a-z0-9- chars after pc-, so write a real id but
        # with a process_context value that violates the pattern. Easier: write a
        # custom invalid value into process_context field via direct yaml.
        (ent_dir / "processes:group-bad.yaml").write_text(
            "id: dea:group-bad\ntype: ProcessGroup\nname: Bad\nversion: 1.0.0\n"
            "process_context: 'not-a-pc'\nprocess_group_kind: functional\n"
            "status: active\nlifecycle_status: active\n",
            encoding="utf-8",
        )
        errs, _ = run_checks(tmp_path)
        if not any("L0L1-CARD-002" in e and "processes:group-bad" in e and "missing" in e for e in errs):
            print("L0L1-CARD self-test: expected CARD-002 (malformed PC) but got:")
            for e in errs:
                print(f"  {e}")
            return 2

        # --- Scenario 5: ProcessScope record. expect CARD-003 failure.
        _reset()
        _write_pc("processes:pc-a", "A")
        _write_pg("processes:group-a1", "processes:pc-a")
        _write_scope("dea:scope-pilot")
        errs, _ = run_checks(tmp_path)
        if not any("L0L1-CARD-003" in e and "ProcessScope" in e for e in errs):
            print("L0L1-CARD self-test: expected CARD-003 (ProcessScope admission) but got:")
            for e in errs:
                print(f"  {e}")
            return 2

        print("L0L1-CARD self-test: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog-root", type=Path, default=Path("."))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    errors, _ = run_checks(args.catalog_root)
    if errors:
        print(f"L0<->L1 cardinality (CR-BP-100; L0L1-CARD-001..003): NON-CONFORMANT ({len(errors)} findings)")
        for e in errors:
            print(f"  {e}")
        return 1
    print("L0<->L1 cardinality (CR-BP-100; L0L1-CARD-001..003): PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())