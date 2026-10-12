# Improve Regulated Workforce Capability

**id:** `processes:process-ao-improve-qqxe4d`
**type:** BusinessProcess
**version:** 1.0.0
**admitted by:** CR-BP-106 (carrier for 5-cell A&O regulator-tied admission tranche)
**discovery record:** `dea:discovery-agency-and-organization-improve-escape` (CR-BP-105 / PR #155)

## What this BP is

Improve Regulated Workforce Capability is the regulator-tied specialization admitted at the
**AgencyAndOrganization x Improve** ECF coordinate. It was admitted as the
canonical decomposition for this cell because the substrate-neutral general-case BP
is insufficient on its own: regulator-licensed roles require a distinct governed
workflow with regulator-controlled scope, fitness-and-propriety attestation,
supervised-training completion, and continuing-supervisor notification.

## Trigger and outcome

- **Trigger:** The enterprise is improving regulator-licensed roles' capability through regulator-mandated continuing-competence programs, fit-and-proper annual assessments, recurrent training, and remediation programs that differ from substrate-neutral learning-and-development operations, and the improvement must align to the regulator's continuing-supervision framework before being recorded on the regulated personnel record.
- **Outcome:** The regulator-licensed roles' capability is improved per the regulator's continuing-competence framework; regulator-mandated training, fit-and-proper re-assessment, and remediation cycles are recorded on the regulated personnel record, and the continuing-supervisor has been notified.

## Evidence anchors

- (regulation) https://www.handbook.fca.org.uk/handbook/SYSC/25/
- (regulation) https://www.handbook.fca.org.uk/handbook/FIT/
- (standard) https://www.sra.org.uk/solicitors/standards-regulations/
- (standard) https://www.jointcommission.org/en-us/standards/
- (standard) https://content.naic.org/cipr-topics/producer-licensing-model-act
- (regulation) https://www.ecfr.gov/current/title-14/chapter-I/subchapter-F/part-121/subpart-Y
- (regulation) https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- (regulation) https://eur-lex.europa.eu/eli/reg/2018/1139/oj
- (standard) https://www.finra.org/rules-guidance/rulebooks/finra-rules/3110

## Adjacent contexts

This BP lives within the AgencyAndOrganization x Improve cell. The
upstream Conceive (regulated-scope declaration) and downstream Operate
(regulator-aligned continuing-compliance oversight) and Retire
(regulated-workforce wind-down) cells carry the regulator-tied chain; the
Design and Build cells carry the upstream regulated-scope declaration and the
upstream regulator-ready candidate pool build respectively.

## L3 / L4 decomposition

L3 Activities and L4 Tasks land in **CR-BP-111** (deferred follow-on tranche).
The 5-phase verb-object decomposition pattern (intake -> record -> transform ->
verify -> confirm) is the same pattern used by `scripts/decompose_l4.py` per
CR-BP-102.
