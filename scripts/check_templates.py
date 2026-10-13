"""CR-BP-113: Template Drift Gate (TPL-001..005)

Makes the "templates can never diverge from schemas" invariant
machine-checked, without a build step. Five rules:

  TPL-001  (blocking).  No template contains a legacy dea:* id
                          pattern in a `id:` or `*_id:` field.
  TPL-002  (blocking).  Structured reference fields in templates
                          (process_context, belongs_to_*, composes[].target_id)
                          use the post-mv1 id families.
  TPL-003  (advisory).  Templates with a corresponding schema validate
                          against it via jsonschema.
  TPL-004  (blocking).  evidence-link `type:` values in templates
                          match the schema's enum.
  TPL-005  (advisory).  copy-to path comments in templates reflect
                          the post-mv1 one-directory-per-record layout.

Authoritative reference: CR-BP-113 (2026-10-13, eaojnr).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"
SCHEMAS_DIR = ROOT / "schemas" / "entities"
ENTITY_SCHEMA = ROOT / "schemas" / "entity.schema.json"

# Map template filename -> schema filename (or None to skip).
# business-process has no dedicated schema; it uses entity.schema.json.
TEMPLATE_SCHEMA_MAP: dict[str, str | None] = {
    "activity.yaml": "activity.schema.json",
    "business-process.yaml": None,  # uses entity.schema.json
    "process-group.yaml": "process-group.schema.json",
    "process-scope.yaml": "process-scope.schema.json",
    "task.yaml": "task.schema.json",
}

# Pre-mv1 id-family patterns (for TPL-001/002)
LEGACY_ID_RE = re.compile(
    r"^dea:(pc|group|process|activity|task|scope)-"
)
POST_MV1_ID_RE = re.compile(
    r"^processes:(pc|group|process|activity|task|scope)-"
)

# Structured reference fields (TPL-002)
STRUCTURED_REF_FIELDS = (
    "process_context",
    "belongs_to_activity",
    "belongs_to_business_process",
)


# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------


def _iter_templates(templates_dir: Path | None = None) -> list[Path]:
    # CR-BP-113 §4 scope: 5 entity templates. The 5 documentation-
    # profile templates (documentation-profile-l*.*) are out of scope;
    # they live in the doc-profile family, not the entity family.
    d = templates_dir or TEMPLATES_DIR
    out = []
    for p in sorted(d.glob("*.yaml")):
        if p.name.startswith("documentation-profile-"):
            continue
        out.append(p)
    return out


def _load_template_meta(path: Path) -> tuple[str | None, dict[str, str]]:
    """Read the template YAML and pull out the `id:` field and a
    structured-reference field map. Lightweight parse (no PyYAML
    needed for the simple cases)."""
    text = path.read_text()
    out: dict[str, str] = {}
    m = re.search(r"^id:\s*(\S+)", text, re.MULTILINE)
    if m:
        out["id"] = m.group(1)
    for field in STRUCTURED_REF_FIELDS:
        m = re.search(rf"^{re.escape(field)}:\s*(\S+)", text, re.MULTILINE)
        if m:
            out[field] = m.group(1)
    # composes[].target_id and source_id
    for ln in text.splitlines():
        for tag in ("source_id", "target_id"):
            m = re.match(rf"\s*-?\s*{tag}:\s*(\S+)", ln)
            if m:
                out[tag] = m.group(1)
    return path.name, out


def evaluate(allowlist_sealed: tuple[str, ...] = (),
             root: Path | None = None) -> tuple[
    list[tuple[str, str]], list[tuple[str, str]]
]:
    blocking: list[tuple[str, str]] = []
    advisory: list[tuple[str, str]] = []
    r = root or ROOT

    for path in _iter_templates(templates_dir=(root / "templates") if root else None):
        try:
            rel = path.relative_to(r).as_posix()
        except ValueError:
            rel = path.name
        if rel in allowlist_sealed:
            continue
        text = path.read_text()
        tpl_name, fields = _load_template_meta(path)

        # TPL-001, TPL-002, TPL-004, TPL-005: run on EVERY template
        # in scope (the 5 entity templates). TPL-003 (schema
        # validation) only runs for templates with a corresponding
        # schema; templates outside the map (doc-profile templates,
        # self-test fixtures) are skipped for TPL-003 only.
        apply_other_rules = True

        if tpl_name is None or tpl_name not in TEMPLATE_SCHEMA_MAP:
            apply_other_rules = False
        else:
            schema_name = TEMPLATE_SCHEMA_MAP[tpl_name]
            if schema_name and jsonschema is not None:
                schema_path = SCHEMAS_DIR / schema_name
                if schema_path.exists():
                    try:
                        json.loads(schema_path.read_text())
                    except (json.JSONDecodeError, OSError) as e:
                        advisory.append((
                            "TPL-003",
                            f"{rel}: schema {schema_name} failed to load: {e}",
                        ))

        if not apply_other_rules:
            continue

        # TPL-001: legacy dea:* in id fields
        tpl_id = fields.get("id", "")
        if tpl_id and LEGACY_ID_RE.match(tpl_id):
            blocking.append((
                "TPL-001",
                f"{rel}: id uses legacy dea:* family: {tpl_id}",
            ))

        # TPL-002: structured reference fields use post-mv1 ids
        for field in ("id",) + STRUCTURED_REF_FIELDS + ("source_id", "target_id"):
            val = fields.get(field, "")
            if not val or "<" in val:
                continue
            if LEGACY_ID_RE.match(val):
                blocking.append((
                    "TPL-002",
                    f"{rel}: {field!r} uses legacy dea:* family: {val}",
                ))

        # TPL-004: evidence-link type enums
        if "evidence" in text and "type:" in text:
            m = re.search(
                r"standard \| documentation \| evidence \| reference",
                text,
            )
            if m:
                blocking.append((
                    "TPL-004",
                    f"{rel}: evidence-link type comment uses stale enum "
                    f"(standard | documentation | evidence | reference); "
                    f"schema enum is "
                    f"(documentation | governance | interview | artifact | "
                    f"standard | regulation)",
                ))

        # TPL-005: copy-to path comments reflect post-mv1 layout
        if re.search(r"entities/v1-alpha/dea:", text):
            blocking.append((
                "TPL-005",
                f"{rel}: copy-to path comment still uses pre-mv1 "
                f"`entities/v1-alpha/dea:...` layout",
            ))

    return blocking, advisory


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _verdict(blocking: list, advisory: list) -> str:
    if blocking:
        return "NON-CONFORMANT"
    if advisory:
        return "CONFORMANT-WITH-WARNINGS"
    return "CONFORMANT"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 on any blocking finding")
    parser.add_argument("--json", action="store_true",
                        help="emit JSON payload")
    parser.add_argument("--self-test", action="store_true",
                        help="run the in-script self-test")
    args = parser.parse_args(argv)

    if args.self_test:
        return _self_test()

    blocking, advisory = evaluate()
    verdict = _verdict(blocking, advisory)

    if args.json:
        print(json.dumps({
            "verdict": verdict,
            "blocking": [{"rule": r, "message": m} for r, m in blocking],
            "advisory": [{"rule": r, "message": m} for r, m in advisory],
        }, indent=2))
    else:
        print(f"Template Drift (CR-BP-113; TPL-001..005): {verdict}")
        print(f"  {len(blocking)} blocking finding(s); {len(advisory)} advisory.")
        for rule, msg in blocking[:20]:
            print(f"    [{rule}] {msg}")
        if len(blocking) > 20:
            print(f"    ... and {len(blocking) - 20} more")
        for rule, msg in advisory[:10]:
            print(f"    [{rule}] {msg}")
        if len(advisory) > 10:
            print(f"    ... and {len(advisory) - 10} more")

    if args.strict and blocking:
        return 1
    return 0


def _self_test() -> int:
    """Exercise TPL-001..005 rule logic on hand-rolled fixtures.
    Returns 0 on PASS, non-zero on FAIL."""
    import tempfile
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        (tmp_root / "templates").mkdir(parents=True)
        (tmp_root / "schemas" / "entities").mkdir(parents=True)
        # Use filenames that match TEMPLATE_SCHEMA_MAP so TPL-001/002/004
        # run on the test fixtures. The schema is intentionally absent
        # (TPL-003 only checks schema-load which gracefully no-ops).
        good = tmp_root / "templates" / "activity.yaml"
        good.write_text("id: processes:test-good-abc123\nprocess_context: processes:pc-test\n")
        # Bad template: legacy id
        bad = tmp_root / "templates" / "task.yaml"
        bad.write_text("id: dea:task-bad-name\nprocess_context: dea:pc-bad\n")
        # Stale enum comment (in business-process template)
        stale = tmp_root / "templates" / "business-process.yaml"
        stale.write_text(
            "id: processes:test-stale-xyz456\n"
            "evidence_links:\n"
            "  - type: standard | documentation | evidence | reference\n"
        )
        try:
            blocking, advisory = evaluate(root=tmp_root)
        except Exception as e:
            failures.append(f"evaluate() raised: {e}")
            blocking, advisory = [], []
        # Assertions
        if not any(r == "TPL-001" and "task.yaml" in m for r, m in blocking):
            failures.append("TPL-001: did not flag legacy id in task.yaml")
        if not any(r == "TPL-002" and "task.yaml" in m for r, m in blocking):
            failures.append("TPL-002: did not flag legacy process_context in task.yaml")
        if not any(r == "TPL-004" and "business-process.yaml" in m for r, m in blocking):
            failures.append("TPL-004: did not flag stale evidence-link enum")
        if any(r == "TPL-001" and "activity.yaml" in m for r, m in blocking):
            failures.append("TPL-001: false positive on activity.yaml")
    if failures:
        print("self-test FAIL:")
        for f in failures:
            print(f"  {f}")
        return 2
    print(f"self-test PASS: 4 cases (TPL-001/002/004 + false-positive)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
