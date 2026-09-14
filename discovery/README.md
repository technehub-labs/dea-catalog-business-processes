# Lifecycle Process Discovery Records

Machine-readable discovery records produced by lifecycle process-discovery
exercises under CR-BP-62 (sections 15-18). One record per discovery exercise
per ECF context, at `v1-alpha/<domain-slug>-<stage-slug>.yaml`.

Records here are **discovery outcomes, not catalog admissions**. A candidate
with disposition `ADMIT-CANONICAL` is a recommendation whose canonical
admission remains governed by catalog maintainers (CR-BP-62 section 20);
`ADMIT-SPECIALIZATION` is a recording construct, not a license to create
specialization records (CR-BP-62 section 30).

Schema: `schemas/discovery/lifecycle-discovery.schema.json`.
Structural gate: `scripts/check_lifecycle_discovery.py` (DISC-001..008,
advisory gate [19]).

## Exercises

| Exercise | CR | Records | Contexts |
|---|---|---|---|
| Activate/Retire boundary-stage discovery | CR-BP-63 | 14 | 7 domains x Activate + Retire |
