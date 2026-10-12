# Conceive Licensed or Regulated Agent Capacity

**id:** `processes:process-ao-conceive-pnrhem`
**type:** BusinessProcess
**version:** 1.0.0
**admitted by:** CR-BP-106 (carrier for 5-cell A&O regulator-tied admission tranche)
**discovery record:** `dea:discovery-agency-and-organization-conceive-escape` (CR-BP-105 / PR #155)

## What this BP is

Conceive Licensed or Regulated Agent Capacity is the regulator-tied specialization admitted at the
**AgencyAndOrganization x Conceive** ECF coordinate. It was admitted as the
canonical decomposition for this cell because the substrate-neutral general-case BP
is insufficient on its own: regulator-licensed roles require a distinct governed
workflow with regulator-controlled scope, fitness-and-propriety attestation,
supervised-training completion, and continuing-supervisor notification.

## Trigger and outcome

- **Trigger:** The enterprise's agent-capacity strategy will include roles whose holders must hold regulator-issued licences, registrations, certifications, or admissions (FCA SMCR CF1..CF11; state healthcare licensure scopes; FAA / EASA type-rating catalogues; NAIC producer line-of-authority designations; state bar admissions; EU AI Act high-risk AI-system human-oversight roles), and the enterprise's regulated-entity approval authority must determine the regulated-scope of those roles before the roles enter Design or Build stages.
- **Outcome:** The enterprise's agent-capacity strategy carries an explicit regulated-scope declaration: the count and category of regulator-licensed roles, the supervisor-controlled scope of each, the fitness-and-propriety attestation regime, and the alignment between the regulated personnel record and the regulator's continuing-supervision framework.

## Evidence anchors

- (regulation) https://www.handbook.fca.org.uk/handbook/SYSC/25/Annex1/
- (regulation) https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- (regulation) https://www.ecfr.gov/current/title-14/chapter-I/subchapter-F/part-119
- (standard) https://content.naic.org/cipr-topics/producer-licensing-model-act
- (standard) https://www.sra.org.uk/solicitors/standards-regulations/
- (regulation) https://www.federalregister.gov/documents/2016/05/02/2016-10567

## Adjacent contexts

This BP lives within the AgencyAndOrganization x Conceive cell. The
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
