# CR-BP-240 — L1–L2 Hierarchy Reconciliation

**Status**: Proposed  
**Layer**: Cross-cutting  
**Owner**: Emmanuel A. Otchere  
**Type:** Canonical hierarchy correction and publication-validation reconciliation  
**Depends on:** CR-BP-239 Slice A publication model (PR #243, merged)  
**Enables:** CR-BP-239 Slice B poster and offline HTML publication  
**Baseline:** `2707db63a5502c676923511f896df439bd7d6398

## 1. Purpose

Resolve the 12 diagnostic hierarchy findings produced by the CR-BP-239 production publication model. Reconcile the provenance and intent of each assertion before correcting canonical L1–L2 composition. The change shall not infer a parent from names, directories, process context, or ECF placement; it shall not rewrite a canonical L0 context to make a composition appear valid.

## 2. Governing distinction

- **L1–L2 composition:** `ProcessGroup.composes[]` is canonical containment and shall identify the L1 Process Group that owns the L2 process within its declared Process Context.
- **L2–L0 context:** `context[].ref` independently declares the process context. It is not a substitute for composition and is not changed by this CR.
- **Cross-process / cross-context relationships:** meaningful relationships may exist outside canonical containment. A relationship must be supported and represented through an appropriate relationship assertion, not by adding a second or foreign L1 composition.
- **Lifecycle:** a deprecated L2 retained as a migration/history record is not required to have an active L1 composition. Its lack of composition is not an error.

## 3. Investigation evidence

The diagnostic model from PR #243 at its exact head commit materializes 12 error findings: six `HIERARCHY-L2-CONTEXT-CONFLICT`, five `HIERARCHY-L2-MULTIPLE-GROUPS`, and one `HIERARCHY-L2-GROUP-MISSING`. The 12 rows are overlapping findings against six distinct L2 records, not 12 independent records.

The source records and original CRs establish the following:

- **Frame Physical Asset Approach** was landed by CR-BP-21d.1 into Enablement & Operations × Conceive and is explicitly composed by `Operations Model Conception`. The Finance & Accounting × Conceive group also has a composition assertion whose rationale says it informs the financial model's asset-accounting posture. That rationale describes a possible cross-process concern, not canonical containment.
- **Design Financial Plan Structure** was seeded by CR-BP-21e and completed under CR-BP-21e.1 in Finance & Accounting × Design. The Finance & Accounting × Conceive group has an additional composition assertion, despite its scope excluding financial planning design.
- **Conduct Cost Optimization Review** was seeded by CR-BP-21e for Finance & Accounting × Improve and is composed by `Financial Improve`. A second composition from Finance & Accounting × Conceive is outside that group's declared scope.
- **Operate General Ledger** was seeded by CR-BP-21e for Finance & Accounting × Operate and is composed by `Everyday Financial Operations` (Finance & Accounting × Operate). Its additional Finance & Accounting × Conceive composition is outside that group's declared scope.
- **Audit Policy Compliance** was admitted under CR-BP-13a in Governance & Existence × Operate and is composed by `Governance Oversight`. CR-BP-21e.1 also added it to Finance & Accounting × Improve; the Finance Improve group's scope includes policy-compliance auditing. The L2 itself remains contexted and ECF-affiliated to Governance & Existence × Operate, with a Governance & Existence Process Owner. The financial-improvement interest is therefore retained as a cross-context concern for later relationship-model review, not as a second canonical composition. Its additional Finance & Accounting × Conceive composition is likewise not supported by that group's scope.
- **Develop Governance Strategy** is a deprecated historical record. CR-BP-20 explicitly planned its migration from Governance & Existence × Conceive to Strategy & Direction × Conceive; CR-BP-21a executed the migration to **Develop Corporate Strategy**. The old record remains deprecated, while the receiving process is canonical in Strategy & Direction × Conceive. A missing active L1 composition on the deprecated record is intentional.

The accepted CR-BP-19 register-v2 grounding and CR-BP-20 alignment are the authoritative cell intent. CR-BP-21d/21d.1, CR-BP-21e/21e.1, CR-BP-13a, and CR-BP-21a provide the landing and migration provenance.

## 4. Governed dispositions

| Diagnostic finding | L2 record | Disposition |
|---|---|---|
| Context conflict + multiple groups | Frame Physical Asset Approach | Retain canonical composition under Operations Model Conception (Enablement & Operations × Conceive). Remove Finance & Accounting × Conceive composition. Preserve its historical rationale in this CR; do not invent a replacement relationship. |
| Context conflict + multiple groups | Design Financial Plan Structure | Retain canonical composition under Financial Design (Finance & Accounting × Design). Remove Finance & Accounting × Conceive composition. |
| Context conflict + multiple groups | Conduct Cost Optimization Review | Retain canonical composition under Financial Improve (Finance & Accounting × Improve). Remove Finance & Accounting × Conceive composition. |
| Context conflict + multiple groups | Operate General Ledger | Retain canonical composition under Financial Operate (Finance & Accounting × Operate). Remove Finance & Accounting × Conceive composition. |
| Two context conflicts + multiple groups | Audit Policy Compliance | Retain canonical composition under Governance Oversight (Governance & Existence × Operate). Remove compositions from Finance & Accounting × Conceive and Finance & Accounting × Improve. Retain the Finance Improve scope statement as a cross-context concern; do not assert a replacement cross-process relationship until its target and relationship semantics are evidenced and governed. |
| Group missing | Develop Governance Strategy (deprecated) | Disposition as intentional lifecycle state: migrated by CR-BP-21a to Develop Corporate Strategy in Strategy & Direction × Conceive. Do not add an L1 composition to the deprecated record. Publication-model validation shall not report missing active composition for deprecated L2s. |

## 5. Implementation scope

1. Remove only the six composition assertions identified above: five from Finance & Accounting × Conceive and one from Finance & Accounting × Improve.
2. Leave each affected L2's canonical `context[].ref`, ECF conformance, identity, lifecycle, process definition, and source provenance unchanged.
3. Record the reconciliation in the affected L1 group change history, referencing CR-BP-240.
4. Update publication-model hierarchy validation so deprecated L2 records are not required to have an incoming active L1 composition. Other hierarchy checks remain in force.
5. Add regression coverage for the deprecated-record disposition.
6. Run strict publication-model generation, verify no hierarchy findings remain, and verify the canonical population and ECF coordinates are unchanged.

## 6. Explicit non-goals

- No L2 context or ECF-coordinate rewrites.
- No inferred cross-process relationship creation.
- No change to L1 scope, definition, outcome, or identity beyond the composition assertions described here.
- No lifecycle changes to the six L2 records.
- No suppression of unresolved findings for active L2 processes.
- No renderer changes in this CR; Slice B consumes the reconciled strict model.

## 7. Acceptance criteria

- [ ] Every one of the 12 diagnostic finding rows is explicitly dispositioned in §4.
- [ ] The six affected L2 records retain their canonical context, identity, and lifecycle.
- [ ] The six foreign composition assertions are removed, and the five canonical L1 compositions remain.
- [ ] Deprecated Develop Governance Strategy remains deprecated and is not given an active L1 composition.
- [ ] Regression tests cover the lifecycle exception and retain strict checking for active L2s.
- [ ] Strict publication-model build succeeds with zero error-level hierarchy findings.
- [ ] Entity population remains 3,723 and ECF coordinates remain 49.
- [ ] No publication renderer is allowed to guess or conceal hierarchy.

## 8. Release boundary

CR-BP-240 establishes the governed semantic disposition and corrects the canonical assertions. Slice B remains gated on a strict publication-model rebuild. The diagnostic poster/HTML preview from PR #244 is not release-ready until it is rebuilt from the reconciled model without `--allow-findings`.
