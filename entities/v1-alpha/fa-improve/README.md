# Process Context Register — v1-alpha

**Status (2026-09-03):** Architecture established (CR-BP-02);
**matrix is empty by design.**

## Why the matrix is empty

CR-BP-02 §22 (Implementation Sequence) explicitly states:

> Do not yet populate the matrix with newly invented processes.
> That belongs to CR-BP-10 after the architecture is established.

The CR establishes the **contextual architecture** (Process Context +
Cell Charter + ECF coordinate discipline) without populating
business processes into it. Populating the 7×7 = 49-cell matrix is a
subsequent exercise that depends on:

1. The Process kernel + specialization discipline (CR-MM-PROC-01;
   CR-AR-FMWK-01; CR-BP-SPEC-BP-01; merged 2026-09-03).
2. The Process Context schema + Cell Charter schema (CR-BP-02;
   this CR).
3. The L0/L1/L2/L3/L4 decomposition semantics (CR-BP-03+;
   future).

## What this directory is for

When Process Context entries land, each file will be a single
Process Context record at this canonical location:

```
contexts/
└── v1-alpha/
    ├── cd-op.yaml           # example: PartyAndRelationship x Operate
    ├── cd-dsgn.yaml         # example: PartyAndRelationship x Design
    └── ...                  # 49 cells maximum; populated deliberately
```

Each file conforms to `schemas/entities/process-context.schema.json`
(CR-BP-02). Validator `scripts/check_process_context.py` enforces
PC-001..PC-008 on every entry in this tree.

## Coordinate naming convention

The CR-BP-02 convention for `id` is:

```
dea:pc-<domain-abbrev>-<stage-abbrev>
```

Where `<domain-abbrev>` is a two-letter abbreviation of the canonical
ECF Domain (e.g. `cd` for PartyAndRelationship) and `<stage-abbrev>` is
the lowercase Lifecycle Stage name (`conceive`, `design`, `build`,
`activate`, `operate`, `improve`, `retire`). Example:
`dea:pc-pr-op` = PartyAndRelationship × Operate.

The convention is for human readability; the validator does not
enforce a specific abbreviation (only the regex
`^dea:pc-[a-z0-9-]+$`).

## Out of scope

- 49-cell matrix population (CR-BP-10).
- L0 Process Scope semantics (CR-BP-03).
- Activity / Task / Workflow (CR-BP-04 / CR-BP-05).
- Process Discovery execution (CR-BP-09).