# Operate Regulated Performance Oversight

**id:** `processes:process-ao-operate-ba8scr`
**type:** BusinessProcess
**version:** 1.0.0
**admitted by:** CR-BP-106 (carrier for 5-cell A&O regulator-tied admission tranche)
**discovery record:** `dea:discovery-agency-and-organization-operate-escape` (CR-BP-105 / PR #155)

## What this BP is

Operate Regulated Performance Oversight is the regulator-tied specialization admitted at the
**AgencyAndOrganization x Operate** ECF coordinate. It was admitted as the
canonical decomposition for this cell because the substrate-neutral general-case BP
is insufficient on its own: regulator-licensed roles require a distinct governed
workflow with regulator-controlled scope, fitness-and-propriety attestation,
supervised-training completion, and continuing-supervisor notification.

## Trigger and outcome

- **Trigger:** The enterprise is operating regulator-licensed roles whose continuing-supervisor notification obligations, conduct-rule compliance, fitness-and-propriety annual attestations, hours-of-work and rest-rule compliance, and continuing-competence tracking must be maintained on the regulated personnel record throughout the role's live operation period, separate from substrate-neutral agent performance operations.
- **Outcome:** The regulator-licensed roles' regulator-aligned compliance evidence is current on the regulated personnel record; continuing-supervisor notification, conduct-rule compliance, fitness-and-propriety annual attestation, hours-of-work and rest-rule compliance, and continuing-competence tracking are current and auditable.

## Evidence anchors

- (regulation) https://www.handbook.fca.org.uk/handbook/COCON/
- (standard) https://www.finra.org/rules-guidance/rulebooks/finra-rules/3110
- (regulation) https://www.ecfr.gov/current/title-14/chapter-I/subchapter-F/part-117
- (regulation) https://www.ecfr.gov/current/title-14/chapter-I/subchapter-F/part-121/subpart-Y
- (regulation) https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- (standard) https://content.naic.org/cipr-topics/producer-licensing-model-act
- (standard) https://www.sra.org.uk/solicitors/standards-regulations/
- (standard) https://www.jointcommission.org/en-us/standards/

## Adjacent contexts

This BP lives within the AgencyAndOrganization x Operate cell. The
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
