#!/usr/bin/env python3
"""Completeness gate (CR-BP-CE-0).

Measures every canonical record against its level's completeness profile
(§3 of change-requests/CR-BP-CE-0-completeness-profiles.md), reconciled to the
canonical schemas under schemas/entities/*.schema.json and
schemas/entity.schema.json.

Level is inferred by record TYPE, not by the draft's L-number (the draft numbers
L1-L4; the canonical model is L0-L4 and is already enforced by the id-system and
EXT-05 gates). Mapping: ProcessContext=canonical L0, ProcessGroup=L1,
Process=L2, Activity=L3, Task=L4.

Modes:
  --advisory   report findings, rc=0 always (default; the ratification phase)
  --strict     rc=1 if any blocking finding
  --self-test  built-in positive/negative probes
  --json       machine-readable output

The gate WRITES reconciliation/completeness-report.yaml (CE-900): per-level and
per-domain completeness percentages, plus the adoption counters for the seven
operational fields and process_classification.
"""
import argparse, json, sys, glob, re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
ENT = ROOT / "entities" / "v1-alpha"
SKIP = ("/research/", "/documentation/", "/discovery/", "/reports/", "/templates/")
REPORT = ROOT / "reconciliation" / "completeness-report.yaml"

SEVEN = ["owner", "stakeholders", "actors", "kpis", "services_provided",
         "components_involved", "specialization_pattern"]
TASK_PHASES = {"intake custodian", "records custodian", "processing custodian",
               "confirmation custodian", "verification custodian"}


def level_of(r):
    t = r.get("type")
    if t:
        return t
    i = r.get("id", "")
    if i.startswith("processes:pc-"):
        return "ProcessContext"
    return None


# Canonical level for a rule code. The rule codes carry the level in their
# second segment (CE-L0-001 -> ProcessContext, CE-L1-* -> ProcessGroup,
# CE-L2-* -> Process, CE-L3-* -> Activity, CE-L4-* -> Task), per the
# CR-BP-CE-0 R1 level mapping. CE-000 is cross-level (level not inferable).
RULE_LEVEL = {
    "L0": "ProcessContext",
    "L1": "ProcessGroup",
    "L2": "Process",
    "L3": "Activity",
    "L4": "Task",
}


def level_of_rule(code):
    """Canonical level for a finding rule code, or None for cross-level rules."""
    parts = str(code).split("-")
    if len(parts) >= 3 and parts[1] in RULE_LEVEL:
        return RULE_LEVEL[parts[1]]
    return None


def domain_of(r):
    """Resolve a record's canonical domain.

    Only ProcessContext carries a top-level `domain`. Every ProcessGroup,
    Process, Activity, and Task resolves its domain through
    `ecfConformance.canonicalReferences[0].domain`. The finding counter and
    the denominator MUST use the same resolution, otherwise the per-domain
    completeness figures divide by a different population than they count
    (CR-BP-CE-0 R7).
    """
    d = r.get("domain")
    if d:
        return d
    ecf = r.get("ecfConformance")
    if isinstance(ecf, dict):
        refs = ecf.get("canonicalReferences")
        if isinstance(refs, list):
            for ref in refs:
                if isinstance(ref, dict) and ref.get("domain"):
                    return ref["domain"]
    return "?"


def load_records():
    out = []
    for f in sorted(ENT.rglob("*.yaml")):
        if any(s in str(f) for s in SKIP):
            continue
        try:
            r = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(r, dict) and r.get("id"):
            out.append((f, r))
    return out


def present(v):
    return v not in (None, "", [], {})


def find(rule, rid, path, msg, blocking=True):
    return {"rule": rule, "id": rid, "path": str(path), "message": msg,
            "severity": "blocking" if blocking else "advisory"}


def check_record(f, r, pcs_by_id):
    """Return findings for one record against its level profile."""
    lv = level_of(r)
    if lv is None:
        return [find("CE-000", r.get("id", "?"), f, "level is not inferable (no type field and no processes:pc- id prefix)")]
    rel = str(f.relative_to(ROOT)) if str(f).startswith(str(ROOT)) else str(f)
    out = []
    fid = r["id"]

    if lv == "ProcessContext":
        req = ["id", "domain", "lifecycle_stage", "name", "definition", "scope",
               "outcomes", "adjacent_contexts", "processes", "cell_charter", "status"]
        for k in req:
            if not present(r.get(k)):
                out.append(find("CE-L0-001", fid, rel, f"required field '{k}' missing or empty"))
        sc = r.get("scope") or {}
        if present(sc):
            if len(sc.get("includes") or []) < 3:
                out.append(find("CE-L0-002", fid, rel, "scope.includes has fewer than 3 entries", blocking=False))
            if len(sc.get("excludes") or []) < 3:
                out.append(find("CE-L0-003", fid, rel, "scope.excludes has fewer than 3 entries", blocking=False))
        if present(r.get("outcomes")) and len(r["outcomes"]) < 3:
            out.append(find("CE-L0-003b", fid, rel, "outcomes has fewer than 3 entries", blocking=False))
        cc = r.get("cell_charter") or {}
        if present(cc):
            need = ["enterprise_concern", "lifecycle_concern", "combined_semantic_meaning",
                    "expected_outcomes", "inclusions", "exclusions", "adjacent_boundaries"]
            for k in need:
                if not present(cc.get(k)):
                    out.append(find("CE-L0-005", fid, rel, f"cell_charter.{k} missing or empty"))
        for bad in ("type", "version", "process_intent", "process_audience"):
            if present(r.get(bad)):
                out.append(find("CE-L0-006", fid, rel, f"prohibited field '{bad}' present on ProcessContext"))

    elif lv == "ProcessGroup":
        req = ["id", "type", "name", "definition", "process_context", "scope",
               "outcomes", "composes", "process_group_kind", "status", "lifecycle_status", "version"]
        for k in req:
            if not present(r.get(k)):
                out.append(find("CE-L1-001", fid, rel, f"required field '{k}' missing or empty"))
        if not present(r.get("owner")):
            out.append(find("CE-L1-005", fid, rel, "adopted field 'owner' unpopulated (candidate -- awaiting ratification)", blocking=False))

    elif lv == "Process":
        for k in ("id", "name", "type", "version", "process_intent"):
            if not present(r.get(k)):
                out.append(find("CE-L2-001", fid, rel, f"required field '{k}' missing or empty"))
        if not present(r.get("process_classification")):
            out.append(find("CE-L2-002", fid, rel, "adopted field 'process_classification' unpopulated", blocking=False))
        if not present(r.get("context")):
            out.append(find("CE-L2-003", fid, rel, "no 'context' reference to a parent ProcessContext", blocking=False))
        for k in ("trigger", "outcome"):
            if not present(r.get(k)):
                out.append(find("CE-L2-004", fid, rel, f"'{k}' missing or empty", blocking=False))
        if not present(r.get("identity")):
            out.append(find("CE-L2-005", fid, rel, "'identity' block missing", blocking=False))
        for k in ("owner", "actors", "stakeholders"):
            if not present(r.get(k)):
                out.append(find("CE-L2-006", fid, rel, f"adopted field '{k}' unpopulated", blocking=False))
        if present(r.get("capabilities_delivered")):
            out.append(find("CE-L2-010", fid, rel, "prohibited field 'capabilities_delivered' present (soft-deprecated, BP-MIG-002)"))

    elif lv == "Activity":
        req = ["id", "type", "name", "version", "belongs_to_business_process", "cohesion_rationale"]
        for k in req:
            if not present(r.get(k)):
                out.append(find("CE-L3-001", fid, rel, f"required field '{k}' missing or empty"))

    elif lv == "Task":
        req = ["id", "type", "name", "definition", "belongs_to_activity", "trigger",
               "outcome", "version", "lifecycle_status", "status", "ecfConformance"]
        for k in req:
            if not present(r.get(k)):
                out.append(find("CE-L4-001", fid, rel, f"required field '{k}' missing or empty"))
        resp = (r.get("responsibility") or "").strip().lower()
        if resp and resp not in TASK_PHASES:
            out.append(find("CE-L4-002", fid, rel, f"responsibility '{resp}' outside the 5-phase custodian vocabulary", blocking=False))

    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--advisory", action="store_true", default=True)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        return self_test()

    recs = load_records()
    pcs_by_id = {r["id"]: r for _, r in recs if level_of(r) == "ProcessContext"}
    findings = []
    for f, r in recs:
        findings += check_record(f, r, pcs_by_id)

    blocking = [x for x in findings if x["severity"] == "blocking"]
    advisory = [x for x in findings if x["severity"] == "advisory"]

    # CE-900: per-level, per-domain completeness + adoption counters
    import collections
    tot = collections.Counter()
    domain_tot = collections.Counter()
    rule_bad = collections.Counter()
    level_findings = collections.Counter()
    domain_findings = collections.Counter()
    for f, r in recs:
        tot[level_of(r) or "?"] += 1
        domain_tot[domain_of(r)] += 1
    # Findings are keyed by rule code; the rule code carries the level
    # (CR-BP-CE-0 R1 mapping). Attributing the level from the rule code is
    # what makes the per-level finding counts real: keying the counter on the
    # level NAME while the findings are keyed on the rule code yields a
    # structurally-zero column.
    #
    # A record may raise SEVERAL findings, so the completeness percentage is
    # computed over the RECORDS carrying at least one finding, not over the
    # finding count. The finding count is reported alongside it.
    id_to_domain = {r["id"]: domain_of(r) for _, r in recs}
    id_to_level = {r["id"]: (level_of(r) or "?") for _, r in recs}
    bad_level_recs = collections.defaultdict(set)
    bad_domain_recs = collections.defaultdict(set)
    for x in blocking + advisory:
        rule_bad[x["rule"]] += 1
        rid = x["id"]
        lv = level_of_rule(x["rule"]) or id_to_level.get(rid, "?")
        level_findings[lv] += 1
        domain_findings[id_to_domain.get(rid, "?")] += 1
        bad_level_recs[lv].add(rid)
        bad_domain_recs[id_to_domain.get(rid, "?")].add(rid)

    def pct(incomplete, n):
        if not n:
            return 100.0
        return round(100.0 * (n - incomplete) / n, 2)

    seven_pop = {k: 0 for k in SEVEN}
    pclass = 0
    for _, r in recs:
        for k in SEVEN:
            if present(r.get(k)):
                seven_pop[k] += 1
        if present(r.get("process_classification")):
            pclass += 1

    report = {
        "cr": "CR-BP-CE-0",
        "mode": "strict" if a.strict else "advisory",
        "record_count": len(recs),
        "by_level": {
            k: {
                "records": tot[k],
                "records_with_findings": len(bad_level_recs.get(k, ())),
                "findings": level_findings.get(k, 0),
                "completeness_pct": pct(len(bad_level_recs.get(k, ())), tot[k]),
            }
            for k in sorted(tot)
        },
        "by_domain": {
            k: {
                "records": domain_tot[k],
                "records_with_findings": len(bad_domain_recs.get(k, ())),
                "findings": domain_findings.get(k, 0),
                "completeness_pct": pct(len(bad_domain_recs.get(k, ())), domain_tot[k]),
            }
            for k in sorted(domain_tot)
        },
        "by_domain_findings": dict(sorted(domain_findings.items())),
        "by_rule": dict(sorted(rule_bad.items())),
        "adoption": {
            "operational_fields": {k: {"populated": seven_pop[k], "of": len(recs)} for k in SEVEN},
            "process_classification": {"populated": pclass, "of": len(recs)},
        },
        "summary": {"total_findings": len(findings), "blocking": len(blocking), "advisory": len(advisory)},
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(yaml.safe_dump(report, sort_keys=False), encoding="utf-8")

    if a.json:
        print(json.dumps({"summary": report["summary"], "findings": findings[:50]}, indent=2))
        return 1 if (a.strict and blocking) else 0

    print(f"Completeness (CR-BP-CE-0): {len(recs)} records; {len(blocking)} blocking, {len(advisory)} advisory findings")
    for lv in sorted(tot):
        print(f"  {lv:15s} {tot[lv]:5d} records")
    print(f"  report -> {REPORT.relative_to(ROOT)}")
    if blocking:
        print("  first blocking findings:")
        for x in blocking[:10]:
            print(f"    [{x['rule']}] {x['id']}: {x['message']}")
    return 1 if (a.strict and blocking) else 0


def self_test():
    # positive: a complete ProcessContext yields no CE-L0 blocking findings
    good_pc = {"id": "processes:pc-x-y-z1", "domain": "D", "lifecycle_stage": "S",
               "name": "N", "definition": "d", "scope": {"includes": ["a", "b", "c"], "excludes": ["a", "b", "c"]},
               "outcomes": ["x", "y", "z"], "adjacent_contexts": ["p"], "processes": ["q"],
               "cell_charter": {k: "v" for k in ["enterprise_concern", "lifecycle_concern", "combined_semantic_meaning", "expected_outcomes", "inclusions", "exclusions", "adjacent_boundaries"]},
               "status": "active"}
    assert not [x for x in check_record(Path("/t/pc.yaml"), good_pc, {}) if x["severity"] == "blocking"], "complete PC should have no blocking findings"
    # negative: empty PC is flagged
    assert check_record(Path("/t/pc.yaml"), {"id": "processes:pc-x-y-z2"}, {}), "empty PC should produce findings"
    # negative: prohibited field on PC
    bad = dict(good_pc); bad["type"] = "ProcessContext"
    assert any(x["rule"] == "CE-L0-006" for x in check_record(Path("/t/pc.yaml"), bad, {})), "prohibited type on PC not caught"
    # negative: process_classification absent -> advisory on Process
    p = {"id": "processes:process-x", "type": "Process", "name": "N", "version": "1.0.0", "process_intent": "manage"}
    assert any(x["rule"] == "CE-L2-002" for x in check_record(Path("/t/p.yaml"), p, {})), "process_classification adoption not flagged"
    # negative: task with bad responsibility
    t = {"id": "processes:task-x", "type": "Task", "name": "N", "definition": "d", "belongs_to_activity": "a",
         "trigger": "t", "outcome": "o", "version": "1", "lifecycle_status": "c", "status": "c",
         "ecfConformance": {}, "responsibility": "bogus custodian"}
    assert any(x["rule"] == "CE-L4-002" for x in check_record(Path("/t/t.yaml"), t, {})), "bad task responsibility not flagged"
    print("self-test: 5/5 probes pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
