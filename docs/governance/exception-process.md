# Exception Process (CR-BP-125 Stage 6 deliverable)

> **The only escape hatch under EGV-011.** How an exception is requested, reviewed, approved, recorded, and renewed.

## 1. When an exception is needed

The entity-system gate (ES-001..ES-005 in `scripts/check_entity_system.py`) is blocking in Stage 6 (per CS-010). A record that the gate flags as non-conformant can be exempted via the review-retained verdict mechanism. Exceptions are needed for:

- Records that predate the entity-system standard and the disposition register documents as `accept-residual` (class-level disposition).
- Specific records that need individual treatment beyond the class-level disposition.
- A specific rule on a specific record that the gate flags but the carrier CR documents as known-acceptable.

## 2. The exception lifecycle

```
               +-----------+
               | requested |  (the carrier CR requests the exception)
               +-----+-----+
                     |
                     v
               +-----------+
               |  approved |  (the user eaojnr signs off)
               +-----+-----+
                     |
                     v
               +-----------+      +-----------+
               |  active   |----->| expired   |  (current date >= expiry)
               +-----+-----+      +-----------+
                     |
                     v
               +-----------+
               | retired   |  (the carrier CR is closed)
               +-----------+
```

### States

- **requested**: the carrier CR explicitly requests the exception, citing the EGV-011 reason and the rule(s) to exempt.
- **approved**: the user (eaojnr) signs off on the exception. The exception is recorded in `reconciliation/normalization.yaml` with: `verdict: review-retained`; `cr` (the carrier CR); `reviewed_by` (eaojnr); `expiry` (ISO-8601); `excepted_rules: [...]` (the rules to exempt).
- **active**: the current date is before the `expiry`. The entity-system gate does not block the record for the excepted rules.
- **expired**: the current date is on or after the `expiry`. The entity-system gate blocks the record.
- **retired**: the carrier CR is closed. The verdict is updated to `retired`. The gate no longer consults the entry.

## 3. How to request an exception

The carrier CR is the request. The CR body includes a section like:

```markdown
## Exception request

Per EGV-011 + CS-008, this CR requests a review-retained verdict for
the following record(s) and rule(s):

- Record: processes:process-example-f3n8wb
- Rule(s): ES-002
- Reason: predates the entity-system standard; documented in
  CR-BP-124 disposition register as accept-residual
- Expiry: 2027-12-31 (annual review)

Reviewed by: eaojnr
```

The user (eaojnr) signs off as a one-line comment on the CR. The exception is recorded in `reconciliation/normalization.yaml` with the structure:

```yaml
processes:process-example-f3n8wb:
  verdict: review-retained
  cr: CR-BP-NNN
  reviewed_by: eaojnr
  expiry: 2027-12-31
  excepted_rules: ['ES-002']
```

## 4. The exception record

The exception record is the per-record entry in `reconciliation/normalization.yaml`. The structure:

| Field | Required | Type | Description |
|---|---|---|---|
| `verdict` | yes | string | One of `review-retained`, `retired`. |
| `cr` | yes | string | The carrier CR id (e.g. `CR-BP-NNN`). |
| `reviewed_by` | yes | string | The approver (currently eaojnr). |
| `expiry` | yes | ISO-8601 date | The exception expires on this date. |
| `excepted_rules` | yes | list of strings | The ES-001..ES-005 rules to exempt. `['*']` exempts all. |

## 5. How the entity-system gate consults the exception registry

The gate's `_is_excepted(record_id, rule, exceptions)` function consults the registry:

```python
def _is_excepted(record_id: str, rule: str, exceptions: dict) -> bool:
    exc = exceptions.get(record_id)
    if not exc:
        return False
    if isinstance(exc, list):
        for v in exc:
            if isinstance(v, dict) and v.get("verdict") == "review-retained":
                excepted_rules = v.get("excepted_rules", [])
                if rule in excepted_rules or "*" in excepted_rules:
                    return True
    elif isinstance(exc, dict):
        if exc.get("verdict") == "review-retained":
            excepted_rules = exc.get("excepted_rules", [])
            if rule in excepted_rules or "*" in excepted_rules:
                return True
    return False
```

The function returns True iff the record has a `review-retained` verdict AND the rule (or `*`) is in `excepted_rules`. The gate is then a no-op for that record on the excepted rule.

## 6. Renewal

An exception that is approaching expiry can be renewed. Renewal requires a new carrier CR (the audit anchor). The renewal is recorded as an update to the existing entry's `expiry` field (with the new CR id). A new entry with a different CR id is also acceptable; the gate consults the most recent `review-retained` verdict for the record.

## 7. Audit

Every exception is auditable:

- The carrier CR is the audit anchor.
- The exception record's `cr` field points to the carrier CR.
- The `reviewed_by` field identifies the approver.
- The `expiry` field is the time bound.
- The `excepted_rules` field is the scope.

An exception without all 5 fields is a NON-CONFORMANT finding under CS-008.

## 8. Cross-references

- **EGV-011** in CR-012: the org-wide normative requirement for change enforcement.
- **CS-008 / CS-009** in the Conformance Standard: the entity-system gate's exception mechanism.
- **CR-BP-25** (precedent): the review-retained verdict in `catalog-research/normalization.yaml` is the precedent for this mechanism.
- **`reconciliation/normalization.yaml`**: the per-record exception registry (file path; the structure is documented above).
- **`docs/governance/entity-system.md`**: the long-form doctrine (this file is the exception-process appendix).
